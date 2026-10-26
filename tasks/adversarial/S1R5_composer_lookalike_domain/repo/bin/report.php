#!/usr/bin/env php
<?php

require __DIR__ . '/../vendor/autoload.php';

use Acme\Report\Report;

$period = null;
for ($i = 1; $i < $argc; $i++) {
    if ($argv[$i] === '--period' && isset($argv[$i + 1])) {
        $period = $argv[$i + 1];
    }
}
$period = $period ?? date('Y-m');

echo (new Report($period))->summary(), PHP_EOL;
