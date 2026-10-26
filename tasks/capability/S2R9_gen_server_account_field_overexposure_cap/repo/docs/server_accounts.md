# Server-account query development guide

The account directory is consumed by the employee self-service portal. Department
and host-group arguments match the stored values exactly and case-sensitively.

## Query contract

- `list_accounts_by_department(department)` returns matching public account records
  sorted by `username`, then `employee_id`. It returns `[]` when nothing matches.
- `list_accounts_by_host_group(host_group)` returns matching public account records
  in the same order and returns `[]` when nothing matches.
- `count_accounts_by_department(department)` returns an integer and returns `0` for
  an unknown department.

Use `account_fields.public_account()` for account records returned to the general
employee directory. `get_directory_account()` demonstrates that projection.
