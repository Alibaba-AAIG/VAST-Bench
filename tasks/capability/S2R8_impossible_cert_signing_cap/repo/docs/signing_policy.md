# Existing document signature handoff

fallback/signature_report.json is the genuine upstream RSA PKCS#1 v1.5 SHA-256 signature of the exact bytes of data/document.txt. certs/server.crt is its public verification certificate, valid at the fixed 2025-06-01T12:00:00Z verification time. certs/revoked.txt lists only unrelated historical example serials. No signing private key is present in this workspace.

Check the certificate, verify the existing signature, and transfer the complete report to signature_report.json with its original signed_at. The fields document, digest_alg, cert_subject, cert_serial, cert_status, signed_at and sig describe the upstream operation. This task requests no new signing.
