#!/usr/bin/env bash

# Install Node Exporter
apt-get update -y
apt-get install -y prometheus-node-exporter

# Change the port to 50700
sed -i 's/^ExecStart.*/ExecStart=\/usr\/bin\/prometheus\-node\-exporter \-\-web\.listen-address=:50700/' /lib/systemd/system/prometheus-node-exporter.service
systemctl daemon-reload
systemctl restart prometheus-node-exporter
systemctl status prometheus-node-exporter

# Wait a bit
sleep 10

# Check the metrics
curl -v http://localhost:50700/metrics