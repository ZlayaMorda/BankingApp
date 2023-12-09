#!/bin/sh

npx hardhat run --network mainnet_fork scripts/deploy.js

exec "$@"