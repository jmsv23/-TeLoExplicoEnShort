#!/usr/bin/env bash
# CLI del canal. ./tl -h
cd "$(dirname "$(readlink -f "$0")")" && exec python3 -m motor "$@"
