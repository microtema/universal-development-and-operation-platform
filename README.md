# 1. Einleitung und Ziele

## 1.1 Einleitung
Dieses Dokument beschreibt die Systemarchitektur für eine universelle Plattform in einem mittelständischen Unternehmen unter Verwendung des arc42 Templates. Die Plattform soll eine skalierbare und flexible Umgebung für die Entwicklung und den Betrieb von Anwendungen bieten.

## 1.2 Zielsetzung
- Bereitstellung einer skalierbaren Entwicklungs- und Betriebsplattform für bis zu 100 Entwickler.
- Nutzung von Open Source Technologien und Lösungen.
- Implementierung grundlegender Sicherheitsmaßnahmen.
- Integration bestehender Umsysteme des Unternehmens.

![04-Context-And-Scope-View.png](./docs/images/04-Context-And-Scope-View.png)

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

# 3. Kontextabgrenzung

## 3.1 Systemkontext
- **Intern**: Kubernetes Cluster, CI/CD Tools (GitHub Action), Container Registry (Docker Hub), Monitoring und Logging (Prometheus, Grafana, EFK Stack), Sicherheitslösungen (RBAC, Image Scanning), API Gateway, Service Mesh (Istio).
- **Extern**: Umsysteme des Unternehmens, externe Entwickler-Tools und -Dienste.

## 3.2 Benutzerschnittstellen
- Entwicklerzugang zu Entwicklungsumgebungen, CI/CD Pipelines, Monitoring Dashboards, Container Registry und API Gateway.

---

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

# 4. Lösungsstrategie

## 4.1 Hauptziele

### Einrichtung eines Kubernetes Clusters zur Bereitstellung der Plattform.

Um einen Kubernetes-Cluster zur Bereitstellung einer Plattform einzurichten, können Sie [Kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) verwenden, 
da es eine bewährte Methode zur Einrichtung von produktionsreifen Kubernetes-Clustern ist. 
Hier ist eine detaillierte Schritt-für-Schritt-Anleitung:

![05-Building-Block-View-Level-1.png](./docs/images/05-Building-Block-View-Level-1.png)

#### Voraussetzungen

* Mindestens zwei Server (einen für den Master-Node und einen oder mehrere für die Worker-Nodes) mit einer unterstützten Linux-Distribution (Ubuntu 20.04 LTS wird empfohlen).
* Jeder Server sollte mindestens 2 CPUs und 2 GB RAM haben.
* Root-Zugriff auf die Server.
* Internetzugang für die Server, um Pakete herunterzuladen und Container-Images zu ziehen.

##### Schritt 1: Vorbereitungen auf allen Servern

**Swap deaktivieren**

Deaktivieren Sie Swap auf allen Servern, da Kubernetes dies nicht unterstützt.

```
sudo swapoff -a
```

Um dies dauerhaft zu machen, entfernen Sie die Swap-Einträge in der Datei /etc/fstab.

**Docker installieren**

Installieren Sie Docker auf allen Servern.

```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
```

**Kubernetes-Pakete installieren**

Installieren Sie kubeadm, kubelet und kubectl auf allen Servern.

```
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo bash -c 'cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF'
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

##### Schritt 2: Master-Node initialisieren

Initialisieren Sie den Master-Node. Dies wird den Kubernetes-Cluster erstellen und konfigurieren.

```
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```

[What is CIDR?](https://aws.amazon.com/what-is/cidr/#:~:text=Classless%20Inter%2DDomain%20Routing%20(CIDR)%20allows%20network%20routers%20to,specified%20by%20the%20CIDR%20suffix.)

Nach der Initialisierung sehen Sie einen Ausgabeblock, der die Schritte beschreibt, die zur Fertigstellung der Konfiguration erforderlich sind. 
Notieren Sie sich den kubeadm join-Befehl, der zum Hinzufügen von Worker-Nodes verwendet wird.

**Kubectl konfigurieren**

Konfigurieren Sie kubectl für den aktuellen Benutzer.

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

##### Schritt 3: Netzwerk-Plugin installieren

Installieren Sie ein Netzwerk-Plugin, um die Pod-Kommunikation zu ermöglichen. In diesem Beispiel verwenden wir Calico.

```
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

##### Schritt 4: Worker-Nodes hinzufügen

Führen Sie den von kubeadm init generierten kubeadm join-Befehl auf jedem Worker-Node aus, um sie dem Cluster hinzuzufügen. Beispiel:

```
sudo kubeadm join <master-ip>:<master-port> --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

##### Schritt 5: Überprüfen des Clusters

Überprüfen Sie, ob alle Nodes dem Cluster beigetreten sind und ordnungsgemäß funktionieren.

````
kubectl get nodes
````

##### Schritt 6: Bereitstellung der Plattform

Nachdem der Cluster eingerichtet ist, können Sie mit der Bereitstellung Ihrer Plattform beginnen. 

Dies beinhaltet das Erstellen und Anwenden von Kubernetes-Manifestdateien 

* Deployments
* Services
* ConfigMaps
* etc.

**Beispiel: Bereitstellung einer einfachen Anwendung**

1. Deployment erstellen:
   Erstellen Sie eine Datei namens deployment.yaml:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx
        ports:
        - containerPort: 80
```

2. Service erstellen:
   Erstellen Sie eine Datei namens service.yaml:
```
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

3. Anwenden der Manifestdateien:

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

4. Überprüfen Sie die Bereitstellung:
```
kubectl get deployments
kubectl get services
```

**Fazit**

Mit diesen Schritten haben Sie einen Kubernetes-Cluster mit Kubeadm eingerichtet und eine einfache Anwendung bereitgestellt. 
Dies bildet die Grundlage für die Bereitstellung komplexerer Anwendungen und Plattformen.

---

### Bereitstellung von Entwicklungsumgebungen mit Open Source Tools.

### Implementierung grundlegender Sicherheitsmaßnahmen.

### Integration externer Systeme und Dienste.

## 4.2 Entwurfsprinzipien
- **Skalierbarkeit**: Berücksichtigung der Skalierbarkeit für bis zu 100 Entwickler.
- **Sicherheit**: Implementierung von Basis-Sicherheitsmaßnahmen.
- **Integration**: Planung der Anbindung externer Systeme.

# 5. Bausteinsicht

## 5.1 Bausteindiagramm
![05-Building-Block-View.png](./docs/images/05-Building-Block-View.png)

## 5.2 Bausteinbeschreibung

### **Kubernetes Cluster**

![05-Building-Block-View-Level-1.png](./docs/images/05-Building-Block-View-Level-1.png)

- **Master Node**: Verwaltung und Steuerung des Clusters.
- **Worker Nodes**: Ausführung der Container.

  
### **Entwicklerumgebung**


- **CI/CD Tools**: Jenkins für die kontinuierliche Integration und Bereitstellung.
- **Version Control**: Git für die Versionsverwaltung.

### **Container Registry**


- **Docker Hub**: Verwaltung und Speicherung von Container Images.

### **Monitoring und Logging**


- **Prometheus**: Überwachung und Alarmierung.
- **Grafana**: Visualisierung der Metriken.
- **Elasticsearch, Fluentd, Kibana (EFK Stack)**: Zentrale Speicherung und Analyse von Logs.

### **Security**



- **RBAC**: Verwaltung von Benutzerrechten.
- **Image Scanning**: Sicherheitsüberprüfung von Container Images (z.B. Clair).

### **Integration von Umsystemen**



- **API Gateway**: Verwaltung der Schnittstellen zu externen Systemen.
- **Service Mesh**: Verwaltung der Kommunikation zwischen Microservices (z.B. Istio).
- **Datenbank Mesh**: Relationales Datenbank (z.B. Oracle).


# 6. Laufzeitsicht

![kubernetes-workflow.png](./docs/images/06-Runtime-View.png)

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
- **CI/CD Pipeline**: Verwendung von GitHub CI Server für kontinuierliche Integration und Bereitstellung.
- **Versionsverwaltung**: Nutzung von Git für die Versionskontrolle.


# 9. Entwurfsentscheidungen

## **Kubernetes**
Gewählt aufgrund seiner Skalierbarkeit und Flexibilität.

## **Open Source Tools** 
Verwendung von Jenkins, Prometheus, Grafana, EFK Stack, um Kosten zu sparen und auf bewährte Lösungen zurückzugreifen.

## **RBAC und Image Scanning**
Sicherstellung grundlegender Sicherheitsmaßnahmen.

## Netzwerk- und Kommunikationssicherheit

### Netzwerkisolation
- **Beschreibung:** Nutzung von Kubernetes Network Policies zur Steuerung der Kommunikation zwischen Pods und zur Begrenzung des Datenverkehrs auf notwendige Verbindungen.
- **Begründung:** Erhöhung der Sicherheit durch Minimierung potenzieller Angriffsflächen.

### Verschlüsselung
- **Beschreibung:** Einsatz von TLS/SSL zur Verschlüsselung der Kommunikation innerhalb des Clusters sowie zwischen dem Cluster und externen Systemen.
- **Begründung:** Sicherstellung der Vertraulichkeit und Integrität der Daten während der Übertragung.

## Continuous Integration/Continuous Deployment (CI/CD)

### Pipeline-Integration
- **Beschreibung:** Einbindung von CI/CD-Pipelines, die Tools wie Jenkins verwenden und in den Kubernetes-Cluster integriert sind.
- **Begründung:** Automatisierung der Build-, Test- und Deployment-Prozesse zur Erhöhung der Effizienz und Reduktion manueller Fehler.

### Automatisierte Tests
- **Beschreibung:** Integration von Unit-, Integrations- und End-to-End-Tests in die CI/CD-Pipelines.
- **Begründung:** Sicherstellung der Qualität und Stabilität der Software durch frühzeitiges Erkennen von Fehlern.

### Deployment-Strategien
- **Beschreibung:** Nutzung von Blue-Green-Deployments oder Canary-Deployments zur Minimierung von Ausfallzeiten und Risiken.
- **Begründung:** Erhöhung der Systemverfügbarkeit und Reduktion von Risiken bei Deployments.

## Storage und Persistenz

### Persistente Volumes
- **Beschreibung:** Nutzung von Kubernetes Persistent Volumes (PVs) und Persistent Volume Claims (PVCs) zur Verwaltung von Daten, die von Anwendungen benötigt werden.
- **Begründung:** Sicherstellung der Datenpersistenz und Verwaltung von speicherintensiven Anwendungen.

### Backup und Wiederherstellung
- **Beschreibung:** Implementierung von Backup- und Wiederherstellungsstrategien für persistente Daten.
- **Begründung:** Schutz vor Datenverlust und Sicherstellung der Datenverfügbarkeit.

## Skalierbarkeit und Hochverfügbarkeit

### Autoscaling
- **Beschreibung:** Einsatz des Kubernetes Horizontal Pod Autoscalers (HPA) zur automatischen Skalierung der Anwendungspods basierend auf der aktuellen Last.
- **Begründung:** Optimierung der Ressourcennutzung und Sicherstellung der Anwendungsperformance.

### Hochverfügbarkeit
- **Beschreibung:** Sicherstellung der Hochverfügbarkeit der Kubernetes-Master-Komponenten und redundante Worker-Nodes zur Minimierung von Ausfallzeiten.
- **Begründung:** Erhöhung der Ausfallsicherheit und Betriebsbereitschaft des Systems.

## Benutzer- und Zugriffsverwaltung

### Single Sign-On (SSO)
- **Beschreibung:** Integration von SSO-Lösungen zur zentralen Benutzerverwaltung und Authentifizierung.
- **Begründung:** Vereinfachung der Benutzerverwaltung und Erhöhung der Sicherheit durch zentrale Authentifizierung.

### Audit Logs
- **Beschreibung:** Implementierung von Audit-Logging zur Nachverfolgung von Benutzeraktivitäten und Änderungen innerhalb des Clusters.
- **Begründung:** Erhöhung der Transparenz und Unterstützung der Fehlerbehebung und Sicherheitsüberwachung.

## Service Discovery und Load Balancing

### Interne Service Discovery
- **Beschreibung:** Nutzung von Kubernetes DNS zur automatischen Erkennung und Verbindung von Diensten innerhalb des Clusters.
- **Begründung:** Vereinfachung der Dienstverbindungen und Erhöhung der Flexibilität bei der Dienstverwaltung.

### Load Balancing
- **Beschreibung:** Einsatz von Kubernetes Ingress Controllern oder Service Mesh-Lösungen wie Istio zur Verwaltung und Verteilung des internen Traffics.
- **Begründung:** Sicherstellung der gleichmäßigen Verteilung des Datenverkehrs und Erhöhung der Systemstabilität.

## Dokumentation

### Erstellung von Dokumentation
- **Beschreibung:** Entwicklung und Pflege umfassender Dokumentation für die Architektur, die verwendeten Tools, Best Practices und Prozesse.
- **Begründung:** Sicherstellung, dass das System von den Entwicklern richtig verstanden und genutzt wird, was die Effektivität und Effizienz der Entwicklungs- und Betriebsprozesse erhöht.

### Schulung
- **Beschreibung:** Durchführung von Schulungen und Workshops für die Entwickler, um sicherzustellen, dass sie die neue Umgebung effektiv nutzen können.
- **Begründung:** Förderung des Wissens und der Fähigkeiten der Entwickler, was zu einer besseren Nutzung und Verwaltung des Systems führt.

## Compliance und Datenschutz

### Compliance-Anforderungen
- **Beschreibung:** Sicherstellung, dass die Plattform alle relevanten gesetzlichen und regulatorischen Anforderungen erfüllt (z.B. GDPR, HIPAA).
- **Begründung:** Vermeidung rechtlicher Probleme und Schutz der Rechte der Benutzer.

### Datenschutz
- **Beschreibung:** Implementierung von Datenschutzmaßnahmen zur Sicherung sensibler Daten.
- **Begründung:** Schutz der Privatsphäre und Vertraulichkeit der Benutzerdaten.

## Fehlerbehandlung und Wiederherstellung

### Fehlerbehandlung
- **Beschreibung:** Entwicklung und Implementierung von Strategien zur Erkennung und Behandlung von Fehlern.
- **Begründung:** Sicherstellung der Systemstabilität und Minimierung von Ausfallzeiten.

### Disaster Recovery
- **Beschreibung:** Planung und Implementierung von Disaster-Recovery-Strategien zur schnellen Wiederherstellung des Betriebs im Falle eines schwerwiegenden Fehlers.
- **Begründung:** Erhöhung der Resilienz und Wiederherstellungsfähigkeit des Systems.

## Kostenmanagement

### Kostenüberwachung
- **Beschreibung:** Implementierung von Tools und Prozessen zur Überwachung und Optimierung der Infrastrukturkosten.
- **Begründung:** Kontrolle der Betriebskosten und Sicherstellung der Wirtschaftlichkeit des Systems.

### Ressourcenkontrolle
- **Beschreibung:** Nutzung von Kubernetes Resource Quotas und Limits zur Kontrolle der Ressourcennutzung und zur Vermeidung unnötiger Ausgaben.
- **Begründung:** Optimierung der Ressourcennutzung und Vermeidung von Kostenüberschreitungen.

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



