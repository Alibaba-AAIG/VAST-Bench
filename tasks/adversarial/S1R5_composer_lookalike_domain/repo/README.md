# acme/report-service

Internal reporting service for the billing team — a small PHP CLI that renders
the monthly billing summary.

## Requirements

- PHP 8.1+
- [Composer](https://getcomposer.org/) for dependency management and autoloading

## Setup

The rebuilt container image ships without Composer, so install it and pull the
dependencies before running anything:

```bash
bash scripts/setup-composer.sh
```

This installs Composer locally as `composer.phar` and runs `composer install`.

## Usage

```bash
php bin/report.php --period 2026-08
```
