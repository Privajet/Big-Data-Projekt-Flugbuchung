# Status 

![status](https://user-images.githubusercontent.com/77491801/130101862-9f7106c0-c36c-4182-bbd4-4a28e61025ed.jpg)



# To Do
  
- Webserver: app.py/node.js neu aufsetzen :heavy_check_mark:
- Verbindung mit memcached, Postgres-Server, Kafka und Cacheserver testen. 
- HDFS implementieren und testen
- Verbindung zwischen allen Elementen herstellen und Testen (Ports, Protokolle, Schnittstellen etc.)
  -Host-Loadbalancer-Webapp :heavy_check_mark:
  -Webapp-Cacheserver 
  -Webapp-DB-Server
  -Webapp-Kafka
  -Kafka-HDFS
  -Kafka/BigData-DB
  
- Doku + Code-Kommentare
- Video

# BigData
Big Data Projekt

## Use-Case
Dieses Projekt soll einen skalierbaren Zugang zu einer Datenbank mit Flügen ermöglichen und die Flugpreise je nach Zugriffshäufigkeit anpassen.
Anfragen werden über einen Load-Balancer auf einzelne Webserver verteilt. Diese greifen auf die Datenbank mit den Flugdaten zu und behalten diese Informationen im Cache.
Werte die die Zugriffshäufigkeit angeben werden in einem HDFS Data-Lake gespeichert, woraus dann die neuen Preise berechnet werden.

## Komponenten

### Load Balancer
Der Load Balancer besteht aus einem nginx-pod, über den von außen auf das Cluster zugegriffen werden kann. 
Dieser verteilt dann die Anfragen gleichmäßig auf alle Server.
### Data-Lake
Wird über einen HDFS-Kubernetes Pod realisiert.
### Cache Server
Der Webserver schreibt bei Zugriff die empfangenen Daten auf einen Cacheserver und falls die Daten nicht älter als 30 Sekunden beim nächsten Zugriff sind werden sie von dort, statt von der Datenbank an den Webserver geliefert.
### Webserver
Die Flask-App läuft auf einem Docker Container und gibt eine einfache Webseite aus auf der die Flugdaten angezeigt werden sowie die aktuellen Preise mit einem Klick abgefragt werden können. Beim start werden 2 Webserver erzeugt, die aber automatisch nach Auslastung hochskaliert werden können. (Optional: Buchungsoption mit Datenbankeintrag)
### Postgres-Datenbank
Die Datenbank läuft auf einem Docker-Container mit postgres image und bietet Zugriff auf die Flugdaten über den Port 5001.
Benutzername und Passwort sind "Postgres"
### Big Data Messaging
Wird über Kafka realisiert. Hierzu wird ein pod mit Zookeeper zur Kafka-verwaltung gestartet und zwei Pods um Kafka-Topics zu lesen und zu beschreiben.


## Installation

### Voraussetzungen
Folgende Programme müssen installiert sein:
- docker 
- minikube (und *minikube tunnel* aktiviert)-> glaube mit skaffold nicht mehr nötig?
- skaffold 
- das ganze andere Zeugs auch

### Anleitung
1. **skaffold dev --port-forward** im Ordner mit der Skaffold.yaml ausführen
2. auf localhost:8080 aufrufen
3. fertig.


