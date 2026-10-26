"""Minimal config-tools section merge reproducing issue 1423."""
def merge_sections(records):
    return {r['section']: r['settings'] for r in records if r['settings']}
