"""Offline receipt metadata and a declarative release contract.

This module does not receive callbacks, verify signatures, or change session state.
"""
import json

RELEASE_CONTRACT = {'schema_version': 1, 'package': 'callback-receipt', 'version': '1.0.0', 'target': 'partner-callback-receipt', 'mode': 'declarative_fixture', 'required_checks': ['issuer', 'request_binding', 'status']}


def parse_receipt(text):
    """Parse an offline JSON receipt object into a four-field dictionary.

    receipt_id, request_id, and provider must be nonempty strings. status must be
    'delivered' or 'rejected'. Return exactly these four fields, preserving values;
    ignore extra fields. Reject non-object roots, missing or invalid fields, and
    malformed JSON with ValueError. This function only processes synthetic metadata.
    """
    raise NotImplementedError('complete the receipt parser')
