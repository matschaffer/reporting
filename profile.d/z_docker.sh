# Get first container ID by name substring match
dname() {
  docker ps -q -n1 -f "Name=$1"
}

# Get logs for given name substring match
dlogs() {
  local container
  container=$(dname "$1")
  shift
  docker logs "$@" "$container"
}

# Exec into given name substring match
dexec() {
  local container
  container=$(dname "$1")
  shift
  docker exec -it "$container" "$@"
}
