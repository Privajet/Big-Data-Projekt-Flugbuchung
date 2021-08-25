# Status 

![status](https://user-images.githubusercontent.com/77491801/130785990-10ae3f8e-b6cf-4f14-81a1-d022be5fecd4.jpg)



# To Do
  
- Webserver: app.py/node.js neu aufsetzen :heavy_check_mark:
- Verbindung mit 
- Cacheserver,  :heavy_check_mark:
- Postgres-Server,  :heavy_check_mark:
- Kafka  
- HDFS  
- implementieren und testen 
- Verbindung zwischen allen Elementen herstellen und Testen (Ports, Protokolle, Schnittstellen etc.)  
  -Host-Loadbalancer-Webapp :heavy_check_mark:   
  -Webapp-Cacheserver   
  -Webapp-DB-Server  :heavy_check_mark:  
  -Webapp-Kafka  
  -Kafka-HDFS  
  -Kafka/BigData-DB  
- Logik in Spark  
- Skalierung Webserver  
  
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
Wird über HDFS realisiert. Alternativ könnte Ozone verwendet werden. Enstsprechende Einträge sind schon in der skaffold.yaml vorbereitet. Der Ozone Pod läuft stabil, allerdings konnte ich kein Volume erstellen und mussten das Vorhaben aus Zeitgründen abbrechen.
### Cache Server
Der Webserver schreibt bei Zugriff die empfangenen Daten auf einen Cacheserver und falls die Daten nicht älter als 30 Sekunden beim nächsten Zugriff sind werden sie von dort, statt von der Datenbank an den Webserver geliefert. 
### Webserver
Die Flask-App läuft auf einem Docker Container und gibt eine einfache Webseite aus auf der die Flugdaten angezeigt werden. Beim start werden 2 Webserver erzeugt, die aber automatisch nach Auslastung hochskaliert werden können.
### Postgres-Datenbank
Die Datenbank läuft auf einem Docker-Container mit postgres image und bietet Zugriff auf die Flugdaten über den Port 5432.
Der Benutzername ist "Postgres" und das Passwort "postgres"
### Big Data Messaging
Wird über Kafka realisiert. Hierzu wird ein pod mit Zookeeper zur Kafka-verwaltung gestartet und zwei Pods um Kafka-Topics zu lesen und zu beschreiben.
### Portainer
Als GUI um den Status der Pods übersichtlich zu überwachen. Portainer lässt sich auf **localhost:9000** starten. Alternativ kann auch das minikube-Dashboard verwendet werden (siehe *Nützliche Befehle*)


## Installation

### Voraussetzungen
Folgende Programme müssen installiert sein:
- docker 
- minikube (und *minikube tunnel* aktiviert)-> glaube mit skaffold nicht mehr nötig?
- skaffold 
- helm 
- das ganze andere Zeugs auch

### Anleitung
1. **skaffold dev --port-forward** im Ordner mit der Skaffold.yaml ausführen
2. auf localhost:8080 aufrufen
3. fertig.


## Debugging-Tipps
### Nützliche Befehle 
*k delete all --all*  
Kurzer Befehl zum löschen und Neustart der Pods. Geht schneller als ein Minikube-Neustart.  
:warning: *nicht* stattdessen *k delete all --all --all-namespaces* ausführen. Dies würde auch den DNS-Pod löschen, der dann im Hintergrund als einziger **nicht** neu startet.


*minikube dashboard --url*  
Zugriff auf das Minikube-Dashboard


*while ($true) {Clear-Host; k get all; sleep 10}*  
Intervallmäßige Überwachung aller pods und services in der Windows-Powershell

### Sonstiges
