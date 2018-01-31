#!/usr/bin/env bash

set -e

if rpm -q grafana; then
  echo "Grafana already installed."
  exit 0
fi

yum install -y https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana-4.6.3-1.x86_64.rpm

grafana-cli plugins install petrslavotinek-carpetplot-panel

/sbin/chkconfig --add grafana-server
service grafana-server start
