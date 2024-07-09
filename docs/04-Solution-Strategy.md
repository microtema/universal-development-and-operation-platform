# 4. Lösungsstrategie

## 4.1 Hauptziele

### Einrichtung eines Kubernetes Clusters zur Bereitstellung der Plattform.

Um einen Kubernetes-Cluster zur Bereitstellung einer Plattform einzurichten, können Sie [Kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) verwenden, 
da es eine bewährte Methode zur Einrichtung von produktionsreifen Kubernetes-Clustern ist. 
Hier ist eine detaillierte Schritt-für-Schritt-Anleitung:

![05-Building-Block-View-Level-1.png](./images/05-Building-Block-View-Level-1.png)

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