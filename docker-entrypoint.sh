#!/usr/bin/env bash
set -e
poetry shell
exec "$@"
