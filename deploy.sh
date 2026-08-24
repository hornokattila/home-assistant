#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
DEST="/home/outsideworx/home-assistant"

set -e

if [ -n "$1" ]; then
    echo "Error: Unknown parameter: '$1'"
    exit 1
fi

mkdir -p "$DEST"
cp "$SCRIPT_DIR/compose.yaml" \
   "$DEST"

cd "$DEST"
docker compose pull
docker stack deploy -c compose.yaml home-assistant --detach=false --resolve-image=always
docker stack services home-assistant --format '{{.Name}}' | xargs -I{} docker service update --force {}
