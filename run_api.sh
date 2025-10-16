#!/usr/bin/env bash
set -e
uvicorn service.app:app --host 0.0.0.0 --port 8000
