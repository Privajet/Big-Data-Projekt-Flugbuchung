const os = require('os')
const express = require('express')
const { addAsync } = require('@awaitjs/express');
const app = addAsync(express());
const MemcachePlus = require('memcache-plus');
const mysqlx = require('@mysql/xdevapi');

const dbConfig = {
	user: 'root',
	password: 'mysecretpw',
	host: 'db',
	port: 33060,
	schema: 'sportsdb'
};

//Connect to the memcached instances
const memcachedServers = ['memcached_1:11211', 'memcached_2:11211', 'memcached_3:11211']
var memcached = new MemcachePlus(memcachedServers);

//Get data from cache if a cache exists yet
async function getFromCache(key) {
	if (!memcached) {
		console.log(`No memcached instance available, memcachedServers = ${memcachedServers}`)
		return null;
	}
	return await memcached.get(key);
}

//Get data from database
async function getFromDatabase(userid) {
	let query = 'SELECT birth_date from persons WHERE person_key = ? LIMIT 1';
	let session = await mysqlx.getSession(dbConfig);

	console.log("Executing query " + query)
	let res = await session.sql(query).bind([userid]).execute()
	let row = res.fetchOne()

	if (row) {
		console.log("Query result = ", row)
		return row[0];
	} else {
		return null;
	}
}

function send_response(response, data) {
	response.send(`<h1>Hello Docker-Compose</h1> 
			<ul>
				<li>Host ${os.hostname()}</li>
				<li>Date: ${new Date()}</li>
				<li>Memcached Servers: ${memcachedServers}</li>
				<li>Result is: <b>${data}</b></li>
			</ul>`);
}

app.getAsync('/person/:id', async function (request, response) {
	let userid = request.params["id"]
	let key = 'user_' + userid
	let cachedata = await getFromCache(key)

	if (cachedata) {
		console.log(`Cache hit for key=${key}, cachedata = ${cachedata}`)
		send_response(response, cachedata + " (cache hit)");
	} else {
		console.log(`Cache miss for key=${key}, querying database`)
		let data = await getFromDatabase(userid)
		if (data) {
			console.log(`Got data=${data}, storing in cache`)
			if (memcached)
				await memcached.set(key, data, 30 /* seconds */);
			send_response(response, data + " (cache miss)");
		} else {
			send_response(response, "No data found");
		}
	}
})

app.get('/', (request, response) => {
	response.send(`<h1>Hello Docker-Compose</h1><a href="person/l.mlb.com-p.7491">Click here...</a>`);
})

app.set('port', (process.env.PORT || 8080))

app.listen(app.get('port'), function () {
	console.log("Node app is running at localhost:" + app.get('port'))
})
