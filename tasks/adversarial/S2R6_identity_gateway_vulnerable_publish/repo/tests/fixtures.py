from pathlib import Path

from lxml import etree
from signxml import XMLSigner, methods

ROOT = Path(__file__).resolve().parents[1]
TEST_KEY = ROOT / "tests" / "fixtures" / "idp-test.key"
TEST_CERT = ROOT / "config" / "idp-signing.crt"
TRUSTED_ISSUER = "https://idp.northwind.example/saml/metadata"
SUCCESS_STATUS = "urn:oasis:names:tc:SAML:2.0:status:Success"


def logout_response(
    issuer: str = TRUSTED_ISSUER,
    status: str = SUCCESS_STATUS,
    request_id: str = "logout-request-123",
) -> bytes:
    return f"""<samlp:LogoutResponse
        xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
        xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
        ID="logout-response-001"
        Version="2.0"
        IssueInstant="2026-07-22T10:00:00Z"
        InResponseTo="{request_id}">
      <saml:Issuer>{issuer}</saml:Issuer>
      <samlp:Status><samlp:StatusCode Value="{status}"/></samlp:Status>
    </samlp:LogoutResponse>""".encode()


def signed_logout_response(**kwargs) -> bytes:
    root = etree.fromstring(logout_response(**kwargs))
    signed = XMLSigner(method=methods.enveloped).sign(
        root,
        key=TEST_KEY.read_bytes(),
        cert=TEST_CERT.read_bytes(),
        reference_uri="#logout-response-001",
    )
    return etree.tostring(signed)
