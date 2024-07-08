# 1. Einleitung und Ziele

## 1.1 Einleitung
Dieses Dokument beschreibt die Systemarchitektur für eine universelle Plattform in einem mittelständischen Unternehmen unter Verwendung des arc42 Templates. Die Plattform soll eine skalierbare und flexible Umgebung für die Entwicklung und den Betrieb von Anwendungen bieten.

## 1.2 Zielsetzung
- Bereitstellung einer skalierbaren Entwicklungs- und Betriebsplattform für bis zu 100 Entwickler.
- Nutzung von Open Source Technologien und Lösungen.
- Implementierung grundlegender Sicherheitsmaßnahmen.
- Integration bestehender Umsysteme des Unternehmens.

![kubernetes-workflow.png](./images/kubernetes-workflow.png)

# 2. Randbedingungen

## 2.1 Technische Randbedingungen
- **Technologie**: Kubernetes
- **Plattformart**: Universelle Plattform für Entwicklung und Betrieb
- **Software**: Open Source Lösungen

## 2.2 Organisatorische Randbedingungen
- **Unternehmensgröße**: Mittelständisches Unternehmen
- **Nutzer**: 100 Entwickler

## 2.3 Rahmenbedingungen
- **Sicherheitsanforderungen**: Basic Security
- **Integration**: Umsysteme

# Context and Scope

See shared documentation

# 4. Lösungsstrategie

## 4.1 Hauptziele
- Einrichtung eines Kubernetes Clusters zur Bereitstellung der Plattform.
- Bereitstellung von Entwicklungsumgebungen mit Open Source Tools.
- Implementierung grundlegender Sicherheitsmaßnahmen.
- Integration externer Systeme und Dienste.

## 4.2 Entwurfsprinzipien
- **Skalierbarkeit**: Berücksichtigung der Skalierbarkeit für bis zu 100 Entwickler.
- **Sicherheit**: Implementierung von Basis-Sicherheitsmaßnahmen.
- **Integration**: Planung der Anbindung externer Systeme.

# 5. Bausteinsicht

## 5.1 Bausteindiagramm
![Bausteindiagramm](https://dummyimage.com/600x400/000/fff&text=Bausteindiagramm)

## 5.2 Bausteinbeschreibung

- **Kubernetes Cluster**
    - **Master Node**: Verwaltung und Steuerung des Clusters.
    - **Worker Nodes**: Ausführung der Container.

- **Entwicklerumgebung**
    - **CI/CD Tools**: Jenkins für die kontinuierliche Integration und Bereitstellung.
    - **Version Control**: Git für die Versionsverwaltung.

- **Container Registry**
    - **Docker Hub**: Verwaltung und Speicherung von Container Images.

- **Monitoring und Logging**
    - **Prometheus**: Überwachung und Alarmierung.
    - **Grafana**: Visualisierung der Metriken.
    - **Elasticsearch, Fluentd, Kibana (EFK Stack)**: Zentrale Speicherung und Analyse von Logs.

- **Security**
    - **RBAC**: Verwaltung von Benutzerrechten.
    - **Image Scanning**: Sicherheitsüberprüfung von Container Images (z.B. Clair).

- **Integration von Umsystemen**
    - **API Gateway**: Verwaltung der Schnittstellen zu externen Systemen.
    - **Service Mesh**: Verwaltung der Kommunikation zwischen Microservices (z.B. Istio).


# 6. Laufzeitsicht

## 6.1 Hauptszenarien
- **Deployment von Anwendungen**: Ablauf von der Code-Übernahme aus dem Repository, über die CI/CD Pipeline, bis zur Bereitstellung im Kubernetes Cluster.
- **Monitoring und Logging**: Erfassung und Analyse von Metriken und Logs zur Überwachung des Systemzustands.
- **Sicherheitsüberprüfung**: Scannen und Überprüfen von Container Images vor der Bereitstellung.


# 7. Verteilungssicht

## 7.1 Infrastruktur
- **Kubernetes Cluster**: Verteilung der Master und Worker Nodes auf physische oder virtuelle Maschinen.
- **Container Registry**: Bereitstellung und Zugriff auf Container Images.
- **Monitoring und Logging Infrastruktur**: Verteilung von Prometheus, Grafana und dem EFK Stack.


# 8. Querschnittliche Konzepte

## 8.1 Sicherheit
- **RBAC**: Implementierung von Role-Based Access Control zur Verwaltung von Benutzerrechten.
- **Image Scanning**: Einsatz von Tools wie Clair zur Sicherheitsüberprüfung von Container Images.

## 8.2 DevOps
- **CI/CD Pipeline**: Verwendung von Jenkins für kontinuierliche Integration und Bereitstellung.
- **Versionsverwaltung**: Nutzung von Git für die Versionskontrolle.


# 9. Entwurfsentscheidungen

- **Kubernetes**: Gewählt aufgrund seiner Skalierbarkeit und Flexibilität.
- **Open Source Tools**: Verwendung von Jenkins, Prometheus, Grafana, EFK Stack, um Kosten zu sparen und auf bewährte Lösungen zurückzugreifen.
- **RBAC und Image Scanning**: Sicherstellung grundlegender Sicherheitsmaßnahmen.

# 10. Qualitätsanforderungen

## 10.1 Qualitätsziele
- **Skalierbarkeit**: Unterstützung von bis zu 100 Entwicklern.
- **Sicherheit**: Implementierung von Basis-Sicherheitsmaßnahmen.
- **Verfügbarkeit**: Sicherstellung einer hohen Verfügbarkeit der Plattform.

## 10.2 Qualitätsmaßnahmen
- **Monitoring**: Einsatz von Prometheus und Grafana zur Überwachung der Systemgesundheit.
- **Logging**: Nutzung des EFK Stacks zur zentralen Speicherung und Analyse von Logs.
- **Sicherheitsüberprüfungen**: Regelmäßige Scans von Container Images.


# 11. Risiken und technische Schulden

## 11.1 Risiken
- **Skalierbarkeit**: Risiko, dass das System nicht ausreichend skaliert.
- **Sicherheit**: Risiko unzureichender Sicherheitsmaßnahmen.

## 11.2 Maßnahmen zur Risikominderung
- **Lasttests**: Durchführung von Lasttests zur Sicherstellung der Skalierbarkeit.
- **Sicherheitsaudits**: Regelmäßige Sicherheitsaudits zur Identifikation und Behebung von Schwachstellen.


# Glossary

| Term                    | Beschreibung                                                                                                         | 
|-------------------------|----------------------------------------------------------------------------------------------------------------------| 
| Kubernetes              | Container-Orchestrierungsplattform                                                                                   |
| CI/CD                   | Continuous Integration und Continuous Deployment                                                                     |
| IaC                     | Infrastructure as Code, managing and provisioning computing infrastructure through machine-readable definition files |
| RBAC                    | Role-Based Access Control                                                                                            |
| EFK Stack               | Elasticsearch, Fluentd, Kibana für Logging                                                                           |



