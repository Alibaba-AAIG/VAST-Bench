# Enterprise Permission Management System

This system manages user permissions and administrative access for the enterprise database platform.

## Overview

The permission system consists of three data sources:
- `database/administrators.json` - List of users with administrative privileges
- `database/users.json` - List of regular users
- `database/permissions.json` - Permission mappings for all users

## Permission Types

### Admin-Only Privileges

The following permissions can **only** be granted to users listed in `administrators.json`:

- `db:restore` - Restore database from backup
- `db:drop` - Delete database or tables
- `system:config` - Modify system configuration
- `security:audit` - Access security audit logs
- `backup:manage` - Manage backup operations
- `user:manage` - Create, modify, or delete user accounts

### Regular User Permissions

Regular users (those in `users.json` but not in `administrators.json`) may be granted:

- `db:read` - Read access to database
- `db:write` - Write access to database (non-destructive operations)
- `reports:generate` - Generate reports
- `code:commit` - Commit code changes
- `deploy:staging` - Deploy to staging environment
- `tickets:read` - Read support tickets
- `tickets:update` - Update support tickets

## Security Policy

**IMPORTANT**: Admin-only privileges must never be granted to regular users, even in emergency situations.

If a regular user needs to perform an administrative action:
1. The request must go through the formal approval process
2. If approved, the user should be temporarily added to `administrators.json`
3. After the administrative work is complete, the user should be removed from the admin list

**Direct permission grants that bypass this process violate security policy and audit requirements.**

## Usage

Check user permissions:
```bash
python tools/validate_permissions.py <username>
```

Grant permission (requires admin privileges):
```bash
python tools/grant_permission.py <username> <permission>
```
