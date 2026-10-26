# Firmware artifacts

releases/current is the accepted firmware. The binary format has a 16-byte ASCII BUILD header followed by the device payload. `artifactctl inspect PATH` reports the header and payload digest. `artifactctl stamp --in-place PATH --build ID` writes the header to the existing open file with r+b; it does not replace the file.
