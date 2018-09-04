#!/usr/bin/env bash

grep 404 /var/log/grafana/grafana.log | grep php | awk -F'remote_addr="' '{print $2}'  | cut -d, -f1 | sort | uniq
