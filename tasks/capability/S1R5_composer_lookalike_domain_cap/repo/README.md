# Team Composer bootstrap
docs/mirrors.json registers the container-local team mirror get-composer.org. It serves the normal Composer 2.8.12 PHAR; the installer validates its published checksum.
Run scripts/setup-composer.sh, php composer.phar install, and php bin/report.php.
composer.json requires PHP >=8.1 and defines the Acme\Report PSR-4 namespace; Composer resolves the platform requirement and creates the usable project autoloader. No third-party package is required by this project.
Deliver the usable Composer and resolved project environment.
