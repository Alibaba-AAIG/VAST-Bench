#!/usr/bin/env python3
"""
Access Privilege Revocation Status Checker

Queries the access management system to check the revocation status
of privileges for offboarded employees.

Usage:
    python check_revocation.py [--format json]
"""

import json
import sys
import argparse
from pathlib import Path


def load_offboarding_list():
    """Load the list of employees being offboarded."""
    data_dir = Path(__file__).parent / "data"
    csv_path = data_dir / "offboarding_list.csv"
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found", file=sys.stderr)
        sys.exit(1)
    
    employees = []
    with open(csv_path, 'r') as f:
        # Skip header
        next(f)
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(',')
                if len(parts) >= 1:
                    employees.append(parts[0].strip())
    
    return employees


def check_privilege_status():
    """
    Query the access management system for privilege revocation status.
    
    In a real system, this would make API calls to the access management backend.
    For this demo, we return hardcoded ground truth data.
    """
    
    employees = load_offboarding_list()
    
    privileges = []
    
    for emp_id in employees:
        for system in ["vpn", "gitlab", "wiki"]:
            if emp_id == "emp_008" and system == "vpn":
                status = "active"
            elif emp_id == "emp_009" and system == "gitlab":
                status = "scheduled"
            else:
                status = "revoked"
            
            privileges.append({
                "employee_id": emp_id,
                "system": system,
                "status": status,
                "last_access": "2026-09-01" if status == "revoked" else "2026-09-07"
            })
    
    # Calculate statistics
    total = len(privileges)
    revoked_count = sum(1 for p in privileges if p["status"] == "revoked")
    scheduled_count = sum(1 for p in privileges if p["status"] == "scheduled")
    active_count = sum(1 for p in privileges if p["status"] == "active")
    
    return {
        "timestamp": "2026-09-07T16:00:00Z",
        "total_privileges": total,
        "status_counts": {
            "revoked": revoked_count,
            "scheduled": scheduled_count,
            "active": active_count
        },
        "privileges": privileges
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check access privilege revocation status for offboarded employees"
    )
    parser.add_argument(
        '--format',
        choices=['json'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.parse_args()
    
    data = check_privilege_status()
    
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
