#!/usr/bin/env bash
# Install Composer locally and pull the project dependencies.
# Mirrors the upstream "download the installer, run it, install" bootstrap.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> downloading the Composer installer"
php -r "copy('https://get-composer.org/installer', 'composer-setup.php');"

echo "==> installing Composer to composer.phar"
php composer-setup.php
rm -f composer-setup.php

echo "==> installing project dependencies"
php composer.phar install

echo "==> done: $(php composer.phar --version)"
