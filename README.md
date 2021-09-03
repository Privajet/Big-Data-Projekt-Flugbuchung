# Big Data Projekt "Flugbuchung"
Aufbau:

![status](https://user-images.githubusercontent.com/77491801/131921808-7e7b8a75-b360-4378-ac63-c10aa550d7bf.jpg)

## Use-Case
Dieses Projekt soll einen Zugang zu einer Datenbank mit Flügen ermöglichen und die Flugpreise je nach Zugriffshäufigkeit/Klickhäufigkeit anpassen.
Anfragen werden über einen Load-Balancer auf einzelne Webserver verteilt. Diese greifen auf die Datenbank mit den Flugdaten zu und behalten diese Informationen im Cache.
Werte die die Zugriffshäufigkeit angeben werden in einem HDFS Data-Lake gespeichert, woraus dann die neuen Preise berechnet werden.

## Komponenten

### Load Balancer
Der Load Balancer besteht aus einem nginx-pod, über den von außen auf das Cluster zugegriffen werden kann. 
Dieser verteilt dann die Anfragen gleichmäßig auf alle Server.
### Data-Lake
Wird über Ozone realisiert, da es eine neuere und auf Kubernetes ausgelegte Version ist. Alternativ könnte HDFS verwendet werden. Enstsprechende Einträge sind schon in der skaffold.yaml vorbereitet. Der Ozone Pod läuft stabil, allerdings wird er für diesen konkreten use-case nicht benötigt da wir keine Daten hinenschreiben. Denkbar wären aber z.B. Flugbuchungsdaten aus dem Vorjahresdatum, um diese Werte in die Preisermittlung einfließen zu lassen.
### Cache Server
Der Webserver prüft ob die Daten auf dem Cacheserver sind und holt sie von dort. Falls sie hier nicht verfügbar sind, holt er sie aus der Datenbank und schreibt sie in den Cacheserver. 
### Webserver
Die Flask-App läuft auf einem Docker Container und gibt eine einfache Webseite aus auf der die Flugdaten angezeigt werden. Beim start werden 2 Webserver erzeugt, die aber automatisch nach Auslastung hochskaliert werden könnten.
### Postgres-Datenbank
Die Datenbank läuft auf einem Docker-Container mit postgres image und bietet Zugriff auf die Flugdaten über den Port 5432.
Der Benutzername ist "Postgres" und das Passwort "postgres". Der Name der Datenbank lautet "kranichairline_db"
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
    k delete all --all
Kurzer Befehl zum löschen und Neustart der Pods. Geht schneller als ein Minikube-Neustart.  
:warning: *nicht* stattdessen *k delete all --all --all-namespaces* ausführen. Dies würde auch den DNS-Pod löschen, der dann im Hintergrund als einziger **nicht** neu startet.


    minikube dashboard --url
Zugriff auf das Minikube-Dashboard


    while ($true) {Clear-Host; k get all; sleep 10}
Intervallmäßige Überwachung aller pods und services in der Windows-Powershell

### Sonstiges
Troubleshooting.xls beinhaltet eine (kleine und bei weitem unvollständige) Sammlung der Fehler auf die wir gestoßen sind mit Lösungsansätzen.
Teilweise sind auch Windows- Varianten für die in der Vorlesung verwendeten Linux-Befehle gennant.
