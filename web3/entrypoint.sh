#!/bin/sh

# fork and start network
npx hardhat node

exec "$@"