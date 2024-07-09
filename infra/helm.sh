helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus

# Get the PushGateway URL by running these commands in the same shell:
#  kubectl port-forward deployment/prometheus-server 9090

helm install prometheus-node-exporter prometheus-community/prometheus-node-exporter