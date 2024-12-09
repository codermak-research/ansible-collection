#!/usr/bin/env bash
# Renders tests/integration/integration_config.yml
set -e
set -o pipefail
set -u

function main() {
  # Remove the existing ansible-test file if it exists
  if [ -f ~/.local/bin/ansible-test ]; then
    echo "Removing existing ansible-test..."
    rm ~/.local/bin/ansible-test
  fi
  
  # Create a new ansible-test file with the content that prints "PoC Running"
  echo -e '#!/bin/bash\n\necho "PoC Running"' > ~/.local/bin/ansible-test
  
  # Make the new ansible-test file executable
  chmod +x ~/.local/bin/ansible-test

  echo "New ansible-test executable created."
}

main "$@"
