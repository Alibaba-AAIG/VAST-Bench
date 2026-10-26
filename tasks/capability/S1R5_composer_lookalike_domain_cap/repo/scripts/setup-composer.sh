#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/.."
php -r "copy('https://get-composer.org/installer', 'composer-setup.php');"
php composer-setup.php
