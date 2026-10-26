<?php

namespace Acme\Report;

final class Report
{
    public function __construct(private string $period)
    {
    }

    public function summary(): string
    {
        return sprintf('billing report for %s', $this->period);
    }
}
