# Install: pip3 install kafka-python
from kafka import KafkaConsumer

# The bootstrap server to connect to
bootstrap = 'my-cluster-kafka-bootstrap:9092'

# ERstellung Kafka-Consumer
print('Starting KafkaConsumer')
consumer = KafkaConsumer('1337datascience',  # <-- topics
                         bootstrap_servers=bootstrap)
# Anzeige der Nutzeraktionen
for event in consumer:
    print("User Aktion:", event)
