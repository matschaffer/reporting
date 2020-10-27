#!/usr/bin/env bash

set -e

if rpm -q grafana; then
  echo "Grafana already installed."
  exit 0
fi

wget https://dl.grafana.com/oss/master/grafana-7.3.0~09f951b5pre-1.x86_64.rpm
sudo yum install grafana-7.3.0~09f951b5pre-1.x86_64.rpm

/usr/sbin/grafana-cli plugins install petrslavotinek-carpetplot-panel
/usr/sbin/grafana-cli plugins install grafana-worldmap-panel
/usr/sbin/grafana-cli plugins install grafana-googlesheets-datasource
/usr/sbin/grafana-cli plugins install simpod-json-datasource
/usr/sbin/grafana-cli plugins install dalvany-image-panel


sudo /usr/sbin/grafana-cli --pluginUrl https://github.com/panodata/grafana-map-panel/archive/0.12.0.zip plugins install grafana-map-panel


/sbin/chkconfig --add grafana-server
/sbin/service grafana-server start

ls -ll -a
