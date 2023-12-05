# Prototyp Kafka: Producer und Consumer 

## Projektbeschreibung
Beispiel eines Apache Kafka Producer und Consumers in einem Data-Ingestion-Layer eines Lambda-Frameworks.

Der Producer sowie der Consumer laufen in einem Docker-Container. Zookeeper ist ein Koordinierungsdienst zur Verwaltung des Kafka-Clusters.

Ein Kafka Producer produziert zufällig Sensordaten für drei Sensoren, ein Consumer konsumiert diese Topics und verarbeitet den Input.

## Installation 
Das Projekt kann geklont und lokal gestartet werden. Dazu muss Docker auf dem lokalen Rechner vorhanden sein. 

    git clone https://github.com/teleponi/kafka_prototype

Docker Container starten (dazu muss docker-compose lokal installiert sein)

    docker-compose up --build 

Wenn der Cluster und Zookeeper hochgefahren sind, sieht man in der Konsole die Ausgabe des Kafka-Consumers,
der die Sensordaten ausgibt. Das Hochfahren kann gut 3 bis 4 Minuten dauern.
