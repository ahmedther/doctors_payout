#!/bin/sh

set -e

# npm run dev -- --port 8007
ln -snf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && echo Asia/Kolkata > /etc/timezone

npm ci

npm run build

node server.js

# node /doctors_payout_sveltekit/build/index.js

# ORIGIN=http://0.0.0.0:8007 node build

# node /doctors_payout_sveltekit/build/index.js

# "build": "vite build && npm run package",