#!/usr/bin/env bash

set -e

if rpm -q grafana; then
  echo "Grafana already installed."
  exit 0
fi

yum install -y https://dl.grafana.com/oss/release/grafana-6.4.2-1.x86_64.rpm

/usr/sbin/grafana-cli plugins install petrslavotinek-carpetplot-panel
/usr/sbin/grafana-cli plugins install grafana-worldmap-panel

/sbin/chkconfig --add grafana-server
/sbin/service grafana-server start
