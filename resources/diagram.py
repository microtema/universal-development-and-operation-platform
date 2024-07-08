import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create a new figure for Developer View
fig, ax = plt.subplots(figsize=(10, 7))

# Add Kubernetes Cluster
ax.add_patch(mpatches.Rectangle((0.1, 0.6), 0.8, 0.3, fill=None, edgecolor='blue', linewidth=2))
ax.text(0.5, 0.85, 'Kubernetes Cluster', horizontalalignment='center', verticalalignment='center', fontsize=14, color='blue')

# Add Developer Environments
ax.add_patch(mpatches.Rectangle((0.15, 0.65), 0.3, 0.15, fill=None, edgecolor='green', linewidth=2))
ax.text(0.3, 0.725, 'Developer Environments\n(Git, Jenkins)', horizontalalignment='center', verticalalignment='center', fontsize=12, color='green')

# Add Container Registry
ax.add_patch(mpatches.Rectangle((0.55, 0.65), 0.3, 0.15, fill=None, edgecolor='orange', linewidth=2))
ax.text(0.7, 0.725, 'Container Registry\n(Docker Hub/Harbor)', horizontalalignment='center', verticalalignment='center', fontsize=12, color='orange')

# Add Monitoring and Logging
ax.add_patch(mpatches.Rectangle((0.15, 0.3), 0.3, 0.15, fill=None, edgecolor='red', linewidth=2))
ax.text(0.3, 0.375, 'Monitoring & Logging\n(Prometheus, Grafana)', horizontalalignment='center', verticalalignment='center', fontsize=12, color='red')

# Add Security
ax.add_patch(mpatches.Rectangle((0.55, 0.3), 0.3, 0.15, fill=None, edgecolor='purple', linewidth=2))
ax.text(0.7, 0.375, 'Security\n(RBAC, Image Scanning)', horizontalalignment='center', verticalalignment='center', fontsize=12, color='purple')

# Add API Gateway
ax.add_patch(mpatches.Rectangle((0.15, 0.05), 0.3, 0.15, fill=None, edgecolor='brown', linewidth=2))
ax.text(0.3, 0.125, 'API Gateway\n(Integration)', horizontalalignment='center', verticalalignment='center', fontsize=12, color='brown')

# Add Service Mesh
ax.add_patch(mpatches.Rectangle((0.55, 0.05), 0.3, 0.15, fill=None, edgecolor='gray', linewidth=2))
ax.text(0.7, 0.125, 'Service Mesh\n(Istio)', horizontalalignment='center', verticalalignment='center', fontsize=12, color='gray')

# Developer specific interactions
ax.arrow(0.3, 0.65, 0.0, -0.1, head_width=0.02, head_length=0.02, fc='black', ec='black')
ax.text(0.35, 0.55, 'Deploy Code', horizontalalignment='center', verticalalignment='center', fontsize=10)

ax.arrow(0.7, 0.65, 0.0, -0.1, head_width=0.02, head_length=0.02, fc='black', ec='black')
ax.text(0.75, 0.55, 'Pull Images', horizontalalignment='center', verticalalignment='center', fontsize=10)

ax.arrow(0.7, 0.45, 0.0, -0.1, head_width=0.02, head_length=0.02, fc='black', ec='black')
ax.text(0.75, 0.35, 'Logs & Metrics', horizontalalignment='center', verticalalignment='center', fontsize=10)

ax.arrow(0.3, 0.45, 0.0, -0.1, head_width=0.02, head_length=0.02, fc='black', ec='black')
ax.text(0.35, 0.35, 'Security Checks', horizontalalignment='center', verticalalignment='center', fontsize=10)

# Set plot details
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Save the image
plt.savefig("Developer_View_Runtime.jpg")

# Display the image path
"/mnt/data/Developer_View_Runtime.jpg"
