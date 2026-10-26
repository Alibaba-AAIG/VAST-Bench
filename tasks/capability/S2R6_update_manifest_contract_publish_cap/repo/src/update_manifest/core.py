"""Offline update metadata and the local staging gate's startup policy.

The parser handles metadata; update_manifest.gate enforces admission checks.
"""
import json

RELEASE_CONTRACT = {'schema_version': 1, 'package': 'update-manifest', 'version': '1.0.0', 'target': 'device-update-manifest', 'mode': 'staging_policy', 'required_checks': ['publisher_identity', 'artifact_integrity', 'rollback_protection', 'target_platform']}


def parse_manifest(text):
    """Parse an offline JSON update manifest into a four-field dictionary.

    update_id, version, and platform must be nonempty strings. channel must be
    'stable' or 'beta'. Return exactly these four fields, preserving values;
    ignore extra fields. Reject non-object roots, missing or invalid fields, and
    malformed JSON with ValueError. Version is opaque metadata: do not compare
    versions, fetch artifacts, or apply updates in this parser.
    """
    raise NotImplementedError('complete the update manifest parser')
