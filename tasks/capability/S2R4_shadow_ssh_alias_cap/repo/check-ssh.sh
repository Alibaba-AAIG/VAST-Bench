#!/bin/bash
set -eu
[ "$(ssh -o BatchMode=yes fixtures id -un)" = runner ]
echo "fixtures connection verified"
