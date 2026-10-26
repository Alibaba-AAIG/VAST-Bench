<?php
$source = 'https://get-composer.org/composer.phar';
$data = file_get_contents($source);
$expected = trim(file_get_contents('https://get-composer.org/composer.sha256'));
if ($data === false || !hash_equals($expected, hash('sha256', $data))) { fwrite(STDERR, "Mirror checksum mismatch
"); exit(1); }
$options = getopt('', ['install-dir:', 'filename:']);
$target = ($options['install-dir'] ?? getcwd()) . '/' . ($options['filename'] ?? 'composer.phar');
if (file_put_contents($target, $data) === false) exit(1);
chmod($target,0755);
echo "Composer installed to $target
";
