const dns = require('dns').promises;
const express = require('express')
const { addAsync } = require('@awaitjs/express');
const app = addAsync(express());
const MemcachePlus = require('memcache-plus');
const mongo = require('mongodb');
const MongoClient = mongo.MongoClient;

//Verbinden zu Memcached Instanzen, Mongo Container Port: 27017
let memcached = null
let memcachedServers = []

const dbConfig = 'mongodb://mongo-connection:27017'

//Get-Funktion für Memcached Server von der DNS, Port: 11211
async function getMemcachedServersFromDns() {
	let queryResult = await dns.lookup('memcached-service', { all: true })
	let servers = queryResult.map(el => el.address + ":11211")

	//Nur ein neues Objekt erstellen, wenn sich die Web-Server Liste verändert hat
	if (memcachedServers.sort().toString() !== servers.sort().toString()) {
		console.log("Updated memcached server list to ", servers)
		memcachedServers = servers
		//Einen verbundenen Client disconnecten
		if (memcached)
			await memcached.disconnect()
		memcached = new MemcachePlus(memcachedServers);
	}
}

//Ursprüchlich versuchen, zu dem Mamcached Server zu verbinden, dann die Web-Server Liste immer nach 5s updaten
getMemcachedServersFromDns()
setInterval(() => getMemcachedServersFromDns(), 5000)

//Get-Funktion um Daten von der Cache zu holen, falls diese bereits existiert
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
