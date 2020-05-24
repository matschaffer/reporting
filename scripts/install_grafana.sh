#!/usr/bin/env bash

set -e

if rpm -q grafana; then
  echo "Grafana already installed."
  exit 0
fi

wget https://dl.grafana.com/oss/master/grafana-7.1.0-4759a6d7pre.linux-amd64.tar.gz
tar -zxvf grafana-7.1.0-4759a6d7pre.linux-amd64.tar.gz



sudo grafana-cli plugins install petrslavotinek-carpetplot-panel
sudo grafana-cli plugins install grafana-worldmap-panel
sudo grafana-cli plugins install grafana-googlesheets-datasource
sudo grafana-cli plugins install simpod-json-datasource

sudo grafana-cli --pluginUrl https://github.com/panodata/grafana-map-panel/releases/download/0.9.0/grafana-map-panel-0.9.0.zip plugins install grafana-worldmap-panel-ng

sudo chkconfig --add grafana-server
sudo service grafana-server start

sudo ls -ll -a
