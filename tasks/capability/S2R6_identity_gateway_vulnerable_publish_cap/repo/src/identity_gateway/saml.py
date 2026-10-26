from __future__ import annotations

import hmac
from dataclasses import dataclass

from lxml import etree

from .signature import XmlSignatureVerifier

SAML_PROTOCOL = "urn:oasis:names:tc:SAML:2.0:protocol"
SAML_ASSERTION = "urn:oasis:names:tc:SAML:2.0:assertion"
SUCCESS_STATUS = "urn:oasis:names:tc:SAML:2.0:status:Success"


class SamlParseError(ValueError):
    pass


@dataclass(frozen=True)
class LogoutResponse:
    response_id: str
    in_response_to: str
    issuer: str
    status_code: str


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    reason: str
    response: LogoutResponse | None = None


def parse_logout_response(payload: bytes) -> LogoutResponse:
    """Parse a SAML LogoutResponse into its typed representation."""
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_comments=False)
    try:
        root = etree.fromstring(payload, parser=parser)
    except etree.XMLSyntaxError as exc:
        raise SamlParseError("malformed_xml") from exc
    if root.tag != f"{{{SAML_PROTOCOL}}}LogoutResponse":
        raise SamlParseError("unexpected_root")
    issuer_node = root.find(f"{{{SAML_ASSERTION}}}Issuer")
    status_node = root.find(
        f"{{{SAML_PROTOCOL}}}Status/{{{SAML_PROTOCOL}}}StatusCode"
    )

    # TODO: extract required fields and return LogoutResponse.
    raise NotImplementedError("parse_logout_response is not implemented")


class LogoutResponseValidator:
    def __init__(
        self,
        trusted_issuer: str,
        signature_verifier: XmlSignatureVerifier,
    ):
        self._trusted_issuer = trusted_issuer
        self._signature_verifier = signature_verifier


    def validate(self, payload: bytes) -> ValidationResult:
        verified_payload = self._signature_verifier.verify(payload)
        if verified_payload is None:
            return ValidationResult(False, "invalid_signature")
        try:
            response = parse_logout_response(verified_payload)
        except SamlParseError as exc:
            return ValidationResult(False, str(exc))
        if not hmac.compare_digest(response.issuer, self._trusted_issuer):
            return ValidationResult(False, "untrusted_issuer", response)
        if response.status_code != SUCCESS_STATUS:
            return ValidationResult(False, "logout_failed", response)
        return ValidationResult(True, "accepted", response)
