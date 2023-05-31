#!/bin/sh

set -e

# npm run dev -- --port 8007

npm run build

node /doctor_payout_sveltekit/build/index.js