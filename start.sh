#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
exec python -m flask --app app run --reload --host 0.0.0.0 --port 5000
