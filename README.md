# Safecast Reporting

A quilt of applications used for reporting in the [Safecast](https://safecast.org) data ecosystem.

## Apps

### Grafana

Hosted on-instance, available at https://grafana.safecast.cc.

### Kibana

A proxy to https://cloud.elastic.co to provide anonymous data access. Available at https://kibana.safecast.cc

## Local Dev

The following assumes your docker ports are accessed at `127.0.0.1`. Replace that IP below if your setup uses a different IP.

First set `KIBANA_BASIC_AUTH` to a base64 of your kibana `username:password`. You can use `.envrc` for this, or whatever you like.

For example:
```
echo 'MYUSER:MYPASS' | base64 -i -
```

Then copy that value into something like `.envrc.example`.

Then up the conatiners:

```
> docker-compose up
```

Then access the apps using a hostname that starts with grafana or kibana. For example:

- https://grafana.127.0.0.1.nip.io:8000/
- https://kibana.127.0.0.1.nip.io:8000/

(or http to port 8000)

Note that the grafana db comes up empty when running locally, so you'll need to configure data sources and dashboards if you want to do a thorough test.

## Deployment

Github actions will build & publish a bundle to the `reporting` beanstalk app. You can then deploy this with [safecast_deploy](https://github.com/safecast/safecast_deploy) by name.

For example:

```
> ./deploy.py same_env reporting dev reporting-master-208670495-e72e974414e7574d7d74271d50f42695959343c4
```

## Ops

ECS manages the containers on EC2, so the names that appear in `docker ps` aren't very ergonomic for bare docker commands.

[z_docker.sh](profile.d/z_docker.sh) adds `dlog` and `dexec` helpers to check docker container output or exec into a container via partial string match.
