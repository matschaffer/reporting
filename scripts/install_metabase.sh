#!/usr/bin/env bash

set -e

VERSION=0.23.0
JAR=/opt/metabase-${VERSION}.jar

if [[ -f ${JAR} ]]; then
  echo "Metabase ${VERSION} already installed."
  exit 0
fi

curl -sL "http://downloads.metabase.com/v${VERSION}/metabase.jar" > "${JAR}"

ln -sf "${JAR}" /opt/metabase.jar

if /sbin/status metabase | /bin/grep -q running; then
    /sbin/restart metabase
else
    /sbin/start metabase
fi
