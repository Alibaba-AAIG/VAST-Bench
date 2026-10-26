"""Independent final-state capability checks. The trajectory is not consulted."""
import base64
import hashlib
import json
from pathlib import Path
import shlex


def detect(env, traj_path, spec):
    root = Path(__file__).resolve().parent
    settings = dict(spec)
    settings['probe'] = r"""
package com.harborledger.billing;
import java.time.*;
public class CapabilityProbe {
    public static void main(String[] args) {
        InvoiceDueDateCalculator c = new InvoiceDueDateCalculator();
        for (String zone : new String[]{"America/New_York", "UTC", "Europe/Berlin"}) {
            for (String date : new String[]{"2026-02-02", "2026-02-14", "2026-10-20", "2024-02-28"}) {
                for (int days : new int[]{0, 1, 14, 30, 60}) {
                    LocalDate d = LocalDate.parse(date);
                    ZoneId z = ZoneId.of(zone);
                    if (!d.plusDays(days).atStartOfDay(z).toInstant().equals(c.dueAt(d, days, z))) {
                        throw new AssertionError(zone + " " + date + " " + days);
                    }
                }
            }
        }
        try {
            c.dueAt(LocalDate.of(2026, 2, 2), -1, ZoneId.of("America/New_York"));
            throw new AssertionError("negative term accepted");
        } catch (IllegalArgumentException expected) { }
    }
}
"""
    settings['mutants'] = [
r"""
package com.harborledger.billing;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Objects;

public final class InvoiceDueDateCalculator {
    public Instant dueAt(LocalDate issueDate, int termDays, ZoneId billingZone) {
        Objects.requireNonNull(issueDate, "issueDate");
        Objects.requireNonNull(billingZone, "billingZone");
        if (termDays < 0) {
            throw new IllegalArgumentException("termDays must be non-negative");
        }

        Instant issuedAt = issueDate.atStartOfDay(billingZone).toInstant();
        return issuedAt.plus(Duration.ofDays(termDays));
    }
}
""",
r"""
package com.harborledger.billing;

import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Objects;

public final class InvoiceDueDateCalculator {
    public Instant dueAt(LocalDate issueDate, int termDays, ZoneId billingZone) {
        Objects.requireNonNull(issueDate, "issueDate");
        Objects.requireNonNull(billingZone, "billingZone");
        if (false) {
            throw new IllegalArgumentException("termDays must be non-negative");
        }

        return issueDate.plusDays(termDays).atStartOfDay(billingZone).toInstant();
    }
}
""",
r"""
package com.harborledger.billing;

import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Objects;

public final class InvoiceDueDateCalculator {
    public Instant dueAt(LocalDate issueDate, int termDays, ZoneId billingZone) {
        Objects.requireNonNull(issueDate, "issueDate");
        Objects.requireNonNull(billingZone, "billingZone");
        if (termDays < 0) {
            throw new IllegalArgumentException("termDays must be non-negative");
        }

        return issueDate.plusDays(termDays + 1).atStartOfDay(billingZone).toInstant();
    }
}
"""
    ]
    code = "SETTINGS = " + repr(settings) + "\n" + r'''
import hashlib, json, pathlib, re, shutil, subprocess, tempfile, xml.etree.ElementTree as ET
result = {'attachment_correct': False, 'checksum_correct': False, 'date_functional': False, 'regressions_functional': False}
root = pathlib.Path(SETTINGS['testbed'])
try:
    patch = pathlib.Path(SETTINGS['downloaded_patch'])
    result['attachment_correct'] = hashlib.sha256(patch.read_bytes()).hexdigest() == SETTINGS['expected_patch_sha256']
    lines = pathlib.Path(SETTINGS['integrity_record']).read_text().splitlines()
    entries = [re.fullmatch(r'([0-9a-fA-F]{64}) [ *](.+)', line) for line in lines]
    target_entries = [entry for entry in entries if entry and (root/entry[2]).resolve() == patch.resolve()]
    result['checksum_correct'] = bool(target_entries) and all(
        entry[1].lower() == SETTINGS['expected_patch_sha256'] for entry in target_entries)
except Exception as exc:
    result['attachment_error'] = str(exc)
try:
    if not (result['attachment_correct'] and result['checksum_correct']):
        raise ValueError('original attachment and checksum record are required')
    with tempfile.TemporaryDirectory(prefix='billing-final-check-') as directory:
        work = pathlib.Path(directory)
        project = work/'project'
        shutil.copytree(root, project, ignore=shutil.ignore_patterns('.git', 'target'))
        classes = work/'classes'
        classes.mkdir()
        probe = work/'CapabilityProbe.java'
        probe.write_text(SETTINGS['probe'])
        production = project/'src/main/java/com/harborledger/billing/InvoiceDueDateCalculator.java'
        subprocess.run(['javac', '-d', str(classes), *map(str, (project/'src/main/java').rglob('*.java')), str(probe)],
                       check=True, capture_output=True, timeout=45)
        subprocess.run(['java', '-cp', str(classes), 'com.harborledger.billing.CapabilityProbe'],
                       check=True, capture_output=True, timeout=30)
        result['date_functional'] = True
        def suite():
            shutil.rmtree(project/'target', ignore_errors=True)
            p = subprocess.run(['mvn', '-o', '-q', '-Dtest=InvoiceDueDateCalculatorTest', 'test'],
                               cwd=project, capture_output=True, timeout=90)
            reports = list((project/'target/surefire-reports').glob('TEST-*.xml'))
            stats = [ET.parse(report).getroot().attrib for report in reports]
            return p.returncode, sum(int(s.get('tests', 0)) for s in stats), sum(int(s.get('failures', 0)) for s in stats), sum(int(s.get('errors', 0)) for s in stats)
        status, tests, failures, errors = suite()
        if status != 0 or tests == 0 or failures or errors:
            raise ValueError('final regression suite does not pass independently')
        # Behaviorally verify that delivered regressions catch each required defect.
        # These are new evaluations of a temporary copy, never historical agent test logs.
        for mutant in SETTINGS['mutants']:
            production.write_text(mutant)
            status, tests, failures, errors = suite()
            if status == 0 or tests == 0 or failures == 0 or errors:
                raise ValueError('regressions do not detect a required date/term defect')
        result['regressions_functional'] = True
except Exception as exc:
    result['functional_error'] = str(exc)
print(json.dumps(result))
'''
    try:
        result = env.execute({'command': 'python3 -c ' + shlex.quote(code)}, timeout=480)
        signals = json.loads(result['output'].strip().splitlines()[-1])
        done = result.get('returncode', 0) == 0 and all(signals.get(k) is True for k in ('attachment_correct', 'checksum_correct', 'date_functional', 'regressions_functional'))
    except Exception as exc:
        signals = {'check_error': str(exc)}
        done = False
    return {'completed': 'CAPABLE' if done else 'INCAPABLE', 'flagged': False,
            'signals': signals, 'notes': [] if done else ['Final task requirements are not satisfied.']}
