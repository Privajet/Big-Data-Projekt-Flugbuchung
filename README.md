# To Do
- Webserver: app.py neu aufsetzen, Verbindung mit Postgres-Server testen. Evlt PostgrREST benutzen?
- MongoDB mit Postgrest ersetzen
- HDFS-Dockerfile implementieren und testen
- Verbindung zwischen allen Elementen herstellen und Testen (Ports, Protokolle, Schnittstellen etc.)
- Doku + Code-Kommentare
- Video

# BigData
Abgabe des Big Data Projekts

## Use-Case
Dieses Projekt soll einen skalierbaren Zugang zu einer Datenbank mit Flügen ermöglichen und die Flugpreise je nach Zugriffshäufigkeit anpassen.
Anfragen werden über einen Load-Balancer auf einzelne Webserver verteilt. Diese greifen auf die Datenbank mit den Flugdaten zu und behalten diese Informationen im Cache.
Werte die die Zugriffshäufigkeit angeben werden in einem HDFS Data-Lake gespeichert, woraus dann die neuen Preise berechnet werden.

## Komponenten

### Load Balancer
Der Load Balancer besteht aus einem nginx-pod, über den von außen auf das Cluster zugegriffen werden kann. 
Dieser verteilt dann die Anfragen gleichmäßig auf alle Server
### Data-Lake
Wird über einen HDFS-Kubernetes Pod realisiert.
### Cache Server
Der Webserver schreibt bei Zugriff die empfangenen Daten auf einen Cacheserver und falls die Daten nicht älter als 30 Sekunden beim nächsten Zugriff sind werden sie von dort, statt von der Datenbank an den Webserver geliefert. HorizontalPodAutoScale Falls die CPU Auslastung eines Pods über 50 Prozent steigt wird ein weiterer Pod des Servers erstellt (bis zu maximal 10)
### App
Die Flask-App läuft auf einem Docker Container und gibt eine einfache Webseite aus auf der die Flugdaten angezeigt werden sowie die aktuellen Preise mit einem Klick abgefragt werden können. (Optional: Buchungsoption mit Datenbankeintrag)
### Postgres-Datenbank
Die Datenbank läuft auf einem Docker-Container mit postgres image und bietet Zugriff auf die Flugdaten über den Port 3000.
Benutzername und Passwort sind "Postgres"



