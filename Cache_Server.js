// Cache Server Ansprache aus Web Server-Teil

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
