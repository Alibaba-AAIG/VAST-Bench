#!/bin/bash
set -euo pipefail
git fetch origin
git merge --ff-only origin/main
