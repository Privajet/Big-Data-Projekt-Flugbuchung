const os = require('os')
const dns = require('dns').promises;
const express = require('express')
const { addAsync } = require('@awaitjs/express');
const app = addAsync(express());
const MemcachePlus = require('memcache-plus');
const mongo = require('mongodb');
const MongoClient = mongo.MongoClient;

// -------------------------------------------------------
// Memcache Configuration
// -------------------------------------------------------

//Connect to the memcached instances, Mongo Container Port: 27017
let memcached = null
let memcachedServers = []

const dbConfig = 'mongodb://mongo-connection:27017'

//Get-Funktion für Memcached Server von der DNS, Port: 11211
async function getMemcachedServersFromDns() {
	let queryResult = await dns.lookup('memcached-service', { all: true })
	// Create IP:Port mappings
	let servers = queryResult.map(el => el.address + ":11211")

	// Check if the list of servers has changed
	// and only create a new object if the server list has changed
	if (memcachedServers.sort().toString() !== servers.sort().toString()) {
		console.log("Updated memcached server list to ", servers)
		memcachedServers = servers
		
		//Disconnect an existing client
		if (memcached)
			await memcached.disconnect()
		
		memcached = new MemcachePlus(memcachedServers);
	}
}

//Initially try to connect to the memcached servers, then each 5s update the list
getMemcachedServersFromDns()
setInterval(() => getMemcachedServersFromDns(), 5000)

//Get data from cache if a cache exists yet
async function getFromCache(key) {
	if (!memcached) {
		console.log(`No memcached instance available, memcachedServers = ${memcachedServers}`)
		return null;
	}
	return await memcached.get(key);
}

//Get-Funktion um Daten vom Mongoclient zu beziehen
async function get_data_from_mongo() {
    let db = await MongoClient.connect('mongodb://mongo-connection:27017/news');
        let thing = await db.collection("newscollection").findOne();
        await db.close();
        return thing;
}

app.getAsync('/', async function (request,response) {
	let key = 'user_'
	let cachedata = await getFromCache(key)

	if (cachedata) {
		response.send(`<h1>Willkommen beim Ticketing System. (Quelle: Cache)</h1> 
		<ul>
			<li>Ihr Host</li>
			<li>Welche Memcached Server?: ${memcachedServers}</li>
			<li>Aktuelle Tickets: ${cachedata["titles"]}</li>
		</ul>`)
	} else {
		let data = await get_data_from_mongo()
		if (data) {
			console.log(`Got data=${data}, storing in cache`)
			if (memcached)
				await memcached.set(key, data, 30 /* seconds */);
			response.send(`<h1>Willkommen beim Ticketing System.</h1> 
					<ul>
						<li>Ihr Host</li>
						<li>Welche Memcached Server?: ${memcachedServers}</li>
						<li>Aktuelle Tickets: ${data["titles"]}</li>
					</ul>`); 
		} else {
			response.send("Noch keine Daten. Bitte warten bis Application das nächste mal läuft!");
		}
	}
})

app.set('port', (process.env.PORT || 8080))

app.listen(app.get('port'), function () {
	console.log("Node app is running at localhost:" + app.get('port'))
})
