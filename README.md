# Safecast Reporting

A quilt of applications used for reporting in the [Safecast](https://safecast.org) data ecosystem.

## Apps

### Grafana

Hosted on-instance in docker, available at https://grafana.safecast.cc

### Kibana

A proxy to https://cloud.elastic.co to provide anonymous data access. Available at https://kibana.safecast.cc

## Dev

```
> docker-compose up
```

Then access the apps under the `vcap.me` domain which resolves to 127.0.0.1

- http://kibana.vcap.me:8000/
- http://grafana.vcap.me:8000/

If your docker isn't 127.0.0.1, update the `proxy/templates` to use some other overridable server names.

## Deployment

First build & push and updated container

```
docker login docker.pkg.github.com # use github user name and api token

docker build -f Dockerfile.grafana -t docker.pkg.github.com/safecast/reporting2/grafana:latest .
docker push docker.pkg.github.com/safecast/reporting2/grafana:latest
```

Then trigger a deploy

```
# deploy dev env
> eb deploy $(eb list | grep dev)

# deploy prd env
> eb deploy $(eb list | grep prd)
```
