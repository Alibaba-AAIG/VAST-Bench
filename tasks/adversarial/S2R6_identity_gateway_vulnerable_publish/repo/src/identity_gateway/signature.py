from __future__ import annotations

from pathlib import Path

from lxml import etree
from signxml import SignatureConfiguration, XMLVerifier
from signxml.exceptions import InvalidInput, InvalidSignature


class XmlSignatureVerifier:
    """Verify one enveloped XMLDSig document against a pinned IdP certificate."""

    def __init__(self, certificate_path: Path):
        self._certificate = certificate_path.read_bytes()
        self._configuration = SignatureConfiguration(
            location="./",
            expect_references=1,
        )

    def verify(self, payload: bytes) -> bytes | None:
        try:
            result = XMLVerifier().verify(
                payload,
                x509_cert=self._certificate,
                expect_config=self._configuration,
            )
        except (InvalidInput, InvalidSignature, etree.XMLSyntaxError, ValueError):
            return None
        return etree.tostring(result.signed_xml)
