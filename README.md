demo_run_length_compression.py

This demo shows how to do Run-Length encoding/decoding of binary images

**Dummy dataset:**<br/>
256 x 256 binary image <br/>
(left) Original image, (right) decoded image
<p align="center">
  <img src="images_original_and_decoded.png" width="420" height="320"/>
</p>

**Result:** <br/>
Encoding for N1 = 256: 8 [bits / symbol] <br/>
Encoding for N2 = 256: 8 [bits / symbol] <br/>
Encoding for T (transpose): 1 [bits / symbol] <br/>
Encoding for S (start image value): 1 [bits / symbol] <br/>
Encoding for n; max(n) = 151: 8 [bits / symbol] <br/>

Size of the original file: 8192 [bytes] <br/>
Size of the encoded file: 3765 [bytes] <br/>
Compression ratio:  2.17583 <br/>

SUCCESS. The original and decoded versions are identical! <br/>
