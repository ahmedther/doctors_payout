#!/bin/sh

set -e

# npm run dev -- --port 8007



npm run build

node -r dotenv/config build

# ORIGIN=http://0.0.0.0:8007 node build

# node /doctor_payout_sveltekit/build/index.js