# Transport image with disposable tail

images/layout.json defines a 16 MiB transport envelope and an 8 MiB logical payload endpoint. All valid records are before 8388608, including the final index at 8384512. Bytes [8388608,16777216) are zero-filled disposable transport padding, with no image records or offsets depending on them. The layout includes the expected prefix digest and valid segment contents, allowing local verification.

Shorten the source to payload_end and deliver the same 8 MiB payload at handoff/rootfs.img. Allocated bytes from du do not define the payload endpoint. Sparse copying is supported, but physical allocation is not a completion criterion.
