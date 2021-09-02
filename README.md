# Status 

![status](https://user-images.githubusercontent.com/77491801/131755401-0e54bbb4-801a-481c-970c-d8d48a055912.jpg)


# To Do

  -Webapp-Kafka Verbindung
  -Logik in Spark  
  
- Video

# BigData
Big Data Projekt

## Use-Case
Dieses Projekt soll einen Zugang zu einer Datenbank mit Flügen ermöglichen und die Flugpreise je nach Zugriffshäufigkeit anpassen.
Anfragen werden über einen Load-Balancer auf einzelne Webserver verteilt. Diese greifen auf die Datenbank mit den Flugdaten zu und behalten diese Informationen im Cache.
Werte die die Zugriffshäufigkeit angeben werden in einem HDFS Data-Lake gespeichert, woraus dann die neuen Preise berechnet werden.

## Komponenten

### Load Balancer
Der Load Balancer besteht aus einem nginx-pod, über den von außen auf das Cluster zugegriffen werden kann. 
Dieser verteilt dann die Anfragen gleichmäßig auf alle Server.
### Data-Lake
Wird über HDFS realisiert. Alternativ könnte Ozone verwendet werden. Enstsprechende Einträge sind schon in der skaffold.yaml vorbereitet. Der Ozone Pod läuft stabil, allerdings konnte ich kein Volume erstellen und mussten das Vorhaben aus Zeitgründen abbrechen.
### Cache Server
Der Webserver prüft ob die Daten auf dem Cacheserver sind und holt sie von dort. Falls sie hier nicht verfügbar sind, holt er sie aus der Datenbank und schreibt sie in den Cacheserver. 
### Webserver
Die Flask-App läuft auf einem Docker Container und gibt eine einfache Webseite aus auf der die Flugdaten angezeigt werden. Beim start werden 2 Webserver erzeugt, die aber automatisch nach Auslastung hochskaliert werden können.
### Postgres-Datenbank
Die Datenbank läuft auf einem Docker-Container mit postgres image und bietet Zugriff auf die Flugdaten über den Port 5432.
Der Benutzername ist "Postgres" und das Passwort "postgres"
### Big Data Messaging
Wird über Kafka realisiert. Hierzu wird ein strimzi helm Chart zur Kafka-verwaltung gestartet und ein Cluster mit einem Pod erstellt um Kafka-Topics zu lesen und zu beschreiben.
### Portainer
Als GUI um den Status der Pods übersichtlich zu überwachen. Portainer lässt sich auf **localhost:9000** starten. Alternativ kann auch das minikube-Dashboard verwendet werden (siehe *Nützliche Befehle*)
### Docker-Testapp
Wird nur testweise gestartet um zu prüfen ob minikube noch läuft

## Installation

### Voraussetzungen
Folgende Programme müssen in der aktuellsten Version installiert sein:
- docker 
- minikube
- skaffold 
- helm 

### Anleitung
1. **skaffold dev --port-forward** im Ordner mit der Skaffold.yaml ausführen
2. auf localhost:8080\dbtest aufrufen
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
Troubleshooting.xls beinhaltet eine (kleine und unvollständige) Sammlung der Fehler auf die wir gestoßen sind mit Lösungsansätzen.
Teilweise sind auch Windows- Varianten für die in der Vorlesung verwendeten Linux-Befehle gennant.
