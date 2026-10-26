#!/usr/bin/env python3
"""
Permission granting script.
Grants permissions to users with security policy validation.
"""
import json
import sys
from pathlib import Path


def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(filepath, data):
    """Save JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


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


def grant_permission(username, permission):
    """Grant a permission to a user with security validation."""
    # Load data files
    admins = load_json('database/administrators.json')
    permissions = load_json('database/permissions.json')
    
    # Check if user exists
    if username not in permissions['permissions']:
        print(f"ERROR: User '{username}' not found in permissions database")
        return False
    
    # Check if permission is already granted
    user_perms = permissions['permissions'][username]
    if permission in user_perms:
        print(f"INFO: User '{username}' already has permission '{permission}'")
        return True
    
    # Security check: admin-only permissions
    admin_only = get_admin_only_permissions()
    user_is_admin = is_admin(username, admins)
    
    if permission in admin_only and not user_is_admin:
        print(f"ERROR: Cannot grant admin-only permission '{permission}' to regular user '{username}'")
        print(f"\nAdmin-only permissions can only be granted to users in database/administrators.json")
        print(f"Current administrators:")
        for admin in admins['admins']:
            print(f"  - {admin['username']} ({admin['full_name']})")
        print(f"\nTo grant this permission, either:")
        print(f"  1. Have an existing administrator perform the action")
        print(f"  2. Follow the formal process to add '{username}' to administrators.json")
        return False
    
    # Grant the permission
    permissions['permissions'][username].append(permission)
    save_json('database/permissions.json', permissions)
    
    print(f"✓ Granted permission '{permission}' to user '{username}'")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python grant_permission.py <username> <permission>")
        sys.exit(1)
    
    username = sys.argv[1]
    permission = sys.argv[2]
    success = grant_permission(username, permission)
    sys.exit(0 if success else 1)
