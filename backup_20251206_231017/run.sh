#!/bin/bash
cd ~/natiq-ultimate
pkill -f "node" 2>/dev/null
node simple-server.cjs
