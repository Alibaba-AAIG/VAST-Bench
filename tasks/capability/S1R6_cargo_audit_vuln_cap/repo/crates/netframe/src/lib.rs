pub mod hpack {
    pub struct Decoder { inner: ::hpack::Decoder<'static> }
    impl Decoder {
        pub fn new() -> Self { Self { inner: ::hpack::Decoder::new() } }
        pub fn decode(&mut self, block: &[u8]) -> Result<Vec<(String,String)>, &'static str> {
            self.inner.decode(block).map_err(|_| "invalid HPACK")?.into_iter().map(|(k,v)|
                Ok((String::from_utf8(k).map_err(|_| "invalid name")?, String::from_utf8(v).map_err(|_| "invalid value")?))).collect()
        }
    }
}
