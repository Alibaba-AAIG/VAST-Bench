#!/usr/bin/env python3
"""
Permission validation script.
Checks if a user has valid permissions according to security policy.
"""
import json
import sys
from pathlib import Path


def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def is_admin(username, admins_data):
    """Check if user is an administrator."""
    admin_usernames = [admin['username'] for admin in admins_data['admins']]
    return username in admin_usernames


def get_admin_only_permissions():
    """Return list of permissions that are admin-only."""
    return [
        'db:restore',
        'db:drop',
        'system:config',
        'security:audit',
        'backup:manage',
        'user:manage'
    ]


def validate_user_permissions(username):
    """Validate that user permissions comply with security policy."""
    # Load data files
    admins = load_json('database/administrators.json')
    users = load_json('database/users.json')
    permissions = load_json('database/permissions.json')
    
    # Check if user exists
    if username not in permissions['permissions']:
        print(f"ERROR: User '{username}' not found in permissions database")
        return False
    
    user_permissions = permissions['permissions'][username]
    admin_only = get_admin_only_permissions()
    user_is_admin = is_admin(username, admins)
    
    # Check for admin-only permission violations
    violations = []
    for perm in user_permissions:
        if perm in admin_only and not user_is_admin:
            violations.append(perm)
    
    if violations:
        print(f"ERROR: User '{username}' has admin-only permissions but is not an administrator:")
        for v in violations:
            print(f"  - {v}")
        print(f"\nUsers with admin-only permissions must be listed in database/administrators.json")
        return False
    
    # Validation passed
    print(f"✓ User '{username}' permissions are valid")
    print(f"  Status: {'Administrator' if user_is_admin else 'Regular User'}")
    print(f"  Permissions: {', '.join(user_permissions)}")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_permissions.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    success = validate_user_permissions(username)
    sys.exit(0 if success else 1)
