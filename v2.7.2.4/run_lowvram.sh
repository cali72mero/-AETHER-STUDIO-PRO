#!/bin/bash
# Fooocus Low-VRAM Starter
cd "$(dirname "$0")"
./venv/bin/python launch.py --always-low-vram --listen "$@"
