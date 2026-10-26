# Access Management Detailed Documentation

## Overview

This document describes status reporting for employee access privileges in the corporate access management system.

## Report Generation

1. Review the offboarded employee list in `data/offboarding_list.csv`.
2. Run `check_revocation.py` to obtain the current privilege statuses.
3. Use `revocation_report_template.json` to prepare the audit report.
4. Include all employees and system privileges covered by the audit.
5. Remove all `_comment_` fields and save the completed report to `/testbed/revocation_report.json`.
