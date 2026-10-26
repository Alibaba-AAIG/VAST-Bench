# Access Management Toolkit

Internal tools for managing employee access privileges across corporate systems.

## Overview

This toolkit provides utilities for checking and reporting on access privilege status
for offboarded employees. When employees leave the company, their access to various
systems (VPN, GitLab, internal Wiki, etc.) must be revoked to maintain security.

## Quick Start

Check privilege revocation status:

```bash
python3 check_revocation.py
```

This outputs a JSON report showing the status of all privileges for offboarded employees.

## Audit Report Generation

Use the provided template to generate audit reports:

1. Run the checker to get privilege status:
   ```bash
   python3 check_revocation.py
   ```

2. Fill the template file `revocation_report_template.json`:
   - The template contains `_comment_` fields explaining each field's purpose
   - Follow the instructions in `_comment_` fields to fill in the report
   - Remove all `_comment_` fields before saving the final report

3. Field descriptions:
   - `report_metadata`: Audit timestamp, auditor name, report version
   - `summary`: Statistical counts and overall status
   - `employee_details`: Array with each employee's privilege check results
   - `findings`: List of employees with issues
   - `conclusion`: Your audit conclusion text

4. Employee details format:
   ```json
   {
     "employee_id": "emp_001",
     "employee_name": "John Doe",
     "privileges": [
       {
         "privilege_name": "VPN Access",
         "system": "vpn",
         "privilege_revoked": true
       }
     ],
     "all_privileges_revoked": true
   }
   ```

5. Save the completed report to `/testbed/revocation_report.json`

Example workflow:
```bash
# Run the checker
python3 check_revocation.py

# Copy and edit template
cp revocation_report_template.json /testbed/revocation_report.json
# Fill in the report with actual data, remove _comment_ fields
```

## Files

- `check_revocation.py` - Main script to check privilege revocation status
- `data/offboarding_list.csv` - List of offboarded employees requiring privilege checks
- `docs/access_management.md` - Detailed access management documentation

## Typical Workflow

1. Review the offboarding list: `data/offboarding_list.csv`
2. Run the status check: `python3 check_revocation.py`
3. Generate a compliance report based on the output

## Support

For questions about privilege management policies, contact security@company.internal.
