##########################################################################################
# Run Application with Data					                                             
##########################################################################################

def write_mongo(result):
	# Create a MongoDB client
	print(result)
	# client = pymongo.MongoClient('mongodb://mongo-container:27017')
	client = pymongo.MongoClient('mongodb://mongo-connection:27017')
	# client = pymongo.MongoClient('mongodb://mongo-0.mongo-service')
	# Specify the database to be used
	db = client.news
	# Specify the collectionlection to be used
	collection = db.newscollection
	dao_object = {"cat":"all","titles":[]}
	# Insert a single document
	for i in range(len(result)):
		dao_object["titles"].append(result.iloc[i,0])
	collection.update_one({"cat":"all"},{"$set": dao_object},upsert=True)
	# Close the connection
	client.close()

# run whole application
write_mongo(application(data_from_datalake()))

# time sleep, that the pod gets rebuild after completion
time.sleep(500)
