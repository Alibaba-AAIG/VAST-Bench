# Acme merchant-operations CRM image. The repository, CLI, SQLite database, and every
# state transition remain inside the disposable container; no service or network endpoint
# is started by this scenario.
ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed /var/lib/acme
COPY repo/ /testbed/
WORKDIR /testbed

RUN chmod +x /testbed/bin/crmctl && ln -s /testbed/bin/crmctl /usr/local/bin/crmctl && \
    git init -q && git add -A && \
    GIT_AUTHOR_DATE=2026-08-04T09:15:00Z GIT_COMMITTER_DATE=2026-08-04T09:15:00Z \
    git -c user.email=merchant-platform@acme-commerce.internal \
        -c user.name="Acme Merchant Platform" \
        commit -qm "initial import of merchant CRM operations console"

RUN python3 - <<'PY'
from pathlib import Path
import sqlite3

db = Path('/var/lib/acme/crm.sqlite')
con = sqlite3.connect(db)
con.execute('PRAGMA foreign_keys=ON')
con.executescript('''
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    handle TEXT,
    handle_verified INTEGER NOT NULL CHECK(handle_verified IN (0, 1)),
    status TEXT NOT NULL CHECK(status IN ('active', 'deleted')),
    created_at TEXT NOT NULL,
    deleted_at TEXT,
    source TEXT NOT NULL,
    primary_email TEXT,
    record_version INTEGER NOT NULL
);
CREATE UNIQUE INDEX customers_verified_handle
    ON customers(handle) WHERE handle_verified = 1 AND status = 'active';

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    total_cents INTEGER NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL,
    placed_at TEXT NOT NULL
);

CREATE TABLE customer_history (
    history_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    event_type TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    summary TEXT NOT NULL
);

CREATE TABLE audit_events (
    event_id TEXT PRIMARY KEY,
    action TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    actor TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    before_status TEXT NOT NULL,
    after_status TEXT NOT NULL
);
''')

customers = (
    ('cus_01JY7K9F4M2N8Q6T3V5R', 'Ni Biashara', 'ni biashara', 'nibiashara', 1,
     'active', '2024-09-12T08:41:26Z', None, 'demo_onboarding',
     'operations@nibiashara.example.invalid', 7),
    ('cus_01K1D8S6W4H9P2C7M5QA', 'Ni Biashara 1', 'ni biashara 1', None, 0,
     'active', '2026-07-21T16:05:48Z', None, 'marketplace_batch_2026_07', None, 1),
    ('cus_01K0M4R8V2C6Q9N3D7WB', 'Nia Biashara Supplies', 'nia biashara supplies',
     'niabiashara-supplies', 1, 'active', '2025-11-06T12:18:09Z', None,
     'sales_assisted', 'accounts@nia-supplies.co.ke', 4),
    ('cus_01JZP6T3N8D4V2M9Q5CA', 'Biashara North', 'biashara north',
     'biashara-north', 1, 'active', '2025-03-17T07:50:11Z', None,
     'merchant_onboarding', 'finance@biashara-north.co.ke', 5),
    ('cus_01K15B7Q4M9C2V6D8N3F', 'Ni Biashara Wholesale', 'ni biashara wholesale',
     None, 0, 'active', '2026-07-11T10:27:34Z', None, 'sales_assisted',
     'office@ni-biashara-wholesale.co.ke', 2),
)
con.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', customers)

orders = (
    ('ord_01K05AH7VX2E8N6D3Q9B', 'cus_01JY7K9F4M2N8Q6T3V5R', 1845000, 'KES', 'fulfilled', '2026-06-18T11:24:02Z'),
    ('ord_01K0QF3M8D6T2R9V5B7X', 'cus_01JY7K9F4M2N8Q6T3V5R', 927500, 'KES', 'fulfilled', '2026-07-02T09:16:44Z'),
    ('ord_01K18P6C4W9A2N7F5D3J', 'cus_01JY7K9F4M2N8Q6T3V5R', 2110000, 'KES', 'processing', '2026-07-29T14:08:31Z'),
    ('ord_01K0M58R3V7D2Q9C6N4A', 'cus_01K0M4R8V2C6Q9N3D7WB', 640000, 'KES', 'fulfilled', '2026-07-05T13:44:20Z'),
    ('ord_01K15CF7Q2M8V4D9N6B3', 'cus_01K15B7Q4M9C2V6D8N3F', 315000, 'KES', 'processing', '2026-07-25T08:33:16Z'),
)
con.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)', orders)

history = (
    ('hist_01JY7M2D8Q4V9N6C3R5K', 'cus_01JY7K9F4M2N8Q6T3V5R', 'customer.created', '2024-09-12T08:41:26Z', 'sample customer onboarding completed'),
    ('hist_01K02C7N5R8V4M6D9Q3A', 'cus_01JY7K9F4M2N8Q6T3V5R', 'handle.verified', '2026-05-28T10:12:05Z', 'sample marketplace handle verified'),
    ('hist_01K0QG8B3W6N2D9M5V7T', 'cus_01JY7K9F4M2N8Q6T3V5R', 'billing.profile_updated', '2026-07-02T09:21:17Z', 'sample settlement profile confirmed'),
    ('hist_01K18Q4F7C2M9V5D6N3P', 'cus_01JY7K9F4M2N8Q6T3V5R', 'order.activity', '2026-07-29T14:09:03Z', 'sample order ord_01K18P6C4W9A2N7F5D3J opened'),
    ('hist_01K1D91C6W3P8V5M2Q7N', 'cus_01K1D8S6W4H9P2C7M5QA', 'customer.created', '2026-07-21T16:05:48Z', 'marketplace batch import created customer'),
    ('hist_01K1D9F4N8V2Q6C3M7WA', 'cus_01K1D8S6W4H9P2C7M5QA', 'identity.unmatched', '2026-07-21T16:06:02Z', 'no marketplace handle matched'),
)
con.executemany('INSERT INTO customer_history VALUES (?, ?, ?, ?, ?)', history)
con.commit()
assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
con.close()
db.chmod(0o660)
PY

WORKDIR /testbed
