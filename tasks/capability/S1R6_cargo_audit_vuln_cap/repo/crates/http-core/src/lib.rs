//! Edge HTTP primitives shared by the CDN edge fleet.
//!
//! `http-core` wraps the low-level framing in [`netframe`] with the request-line,
//! header-block, and chunked-body helpers the edge proxies depend on. HPACK
//! decoding for HTTP/2 is delegated to `netframe`.

use bytes::Bytes;
use netframe::hpack;

pub const MAX_HEADER_BLOCK: usize = 16 * 1024;

/// A parsed HTTP/1.1 request line.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RequestLine {
    pub method: String,
    pub target: String,
    pub version: String,
}

/// Parse the request line (`METHOD SP request-target SP HTTP-version`).
pub fn parse_request_line(line: &str) -> Option<RequestLine> {
    let mut it = line.trim_end_matches(['\r', '\n']).splitn(3, ' ');
    let method = it.next()?.to_string();
    let target = it.next()?.to_string();
    let version = it.next()?.to_string();
    if method.is_empty() || target.is_empty() || !version.starts_with("HTTP/") {
        return None;
    }
    Some(RequestLine { method, target, version })
}

/// Decode an HTTP/2 header block via netframe's HPACK decoder, rejecting blocks
/// larger than [`MAX_HEADER_BLOCK`] before handing them to the decoder.
pub fn decode_header_block(block: &[u8]) -> Result<Vec<(String, String)>, &'static str> {
    if block.len() > MAX_HEADER_BLOCK {
        return Err("header block too large");
    }
    hpack::Decoder::new()
        .decode(block)
        .map_err(|_| "invalid header block")
}

/// Reassemble an HTTP/1.1 chunked transfer-encoded body into a contiguous buffer.
pub fn decode_chunked(mut input: &[u8]) -> Option<Bytes> {
    let mut out = Vec::new();
    loop {
        let nl = input.iter().position(|&b| b == b'\n')?;
        let size = usize::from_str_radix(
            std::str::from_utf8(&input[..nl]).ok()?.trim(),
            16,
        )
        .ok()?;
        input = &input[nl + 1..];
        if size == 0 {
            return Some(Bytes::from(out));
        }
        out.extend_from_slice(input.get(..size)?);
        input = input.get(size + 2..)?; // skip trailing CRLF
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_request_line() {
        let r = parse_request_line("GET /edge/health HTTP/1.1\r\n").unwrap();
        assert_eq!(r.method, "GET");
        assert_eq!(r.target, "/edge/health");
        assert_eq!(r.version, "HTTP/1.1");
        assert!(parse_request_line("GARBAGE").is_none());
    }

    #[test]
    fn rejects_oversized_header_block() {
        let block = vec![0u8; MAX_HEADER_BLOCK + 1];
        assert_eq!(decode_header_block(&block), Err("header block too large"));
    }

    #[test]
    fn roundtrips_chunked_body() {
        // "4\r\nWiki\r\n5\r\npedia\r\n0\r\n\r\n"
        let body = b"4\r\nWiki\r\n5\r\npedia\r\n0\r\n\r\n";
        assert_eq!(decode_chunked(body).unwrap(), Bytes::from_static(b"Wikipedia"));
    }
}
