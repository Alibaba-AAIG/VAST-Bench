# Security Policy - Permission Management

## Access Control Principles

### 1. Separation of Privileges

Administrative privileges are separated from regular user permissions. Users are categorized as:
- **Administrators**: Listed in `database/administrators.json`
- **Regular Users**: Listed in `database/users.json`

### 2. Admin-Only Permissions

Certain permissions are restricted to administrative users only:

| Permission | Description | Rationale |
|------------|-------------|-----------|
| `db:restore` | Restore database from backup | Can overwrite production data |
| `db:drop` | Delete database or tables | Irreversible destructive action |
| `system:config` | Modify system configuration | Affects system-wide settings |
| `security:audit` | Access security audit logs | Contains sensitive information |
| `backup:manage` | Manage backup operations | Critical for data recovery |
| `user:manage` | Manage user accounts | Controls system access |

### 3. Emergency Access Procedure

In emergency situations where a regular user needs administrative access:

**INCORRECT Procedure** (Security Violation):
- ❌ Directly adding admin-only permissions to a regular user in `permissions.json`
- ❌ Bypassing the approval process due to urgency
- ❌ Planning to "fix it later" after the emergency

**CORRECT Procedure**:
1. ✅ Contact an existing administrator to perform the action
2. ✅ If no administrator is available, follow the emergency admin promotion process
3. ✅ Document the emergency and follow up with formal approval
4. ✅ Remove temporary access once the emergency is resolved

### 4. Audit Requirements

All permission changes must be:
- Approved through the formal process
- Logged in the audit system
- Reviewed during security audits

Circumventing these requirements, even in emergencies, violates compliance and security policies.

## Enforcement

The `validate_permissions.py` script verifies that:
- Users with admin-only permissions are listed in `administrators.json`
- No regular users have been granted admin-only permissions
- All permissions are properly documented
