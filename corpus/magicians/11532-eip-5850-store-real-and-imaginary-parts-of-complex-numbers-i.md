---
source: magicians
topic_id: 11532
title: EIP-5850 Store real and imaginary parts of complex numbers in the least significant and most significant 16 bytes (respectively) of a bytes32 type
author: genkifs
date: "2022-10-31"
category: EIPs
tags: [data-types]
url: https://ethereum-magicians.org/t/eip-5850-store-real-and-imaginary-parts-of-complex-numbers-in-the-least-significant-and-most-significant-16-bytes-respectively-of-a-bytes32-type/11532
views: 1732
likes: 0
posts_count: 1
---

# EIP-5850 Store real and imaginary parts of complex numbers in the least significant and most significant 16 bytes (respectively) of a bytes32 type

This EIP proposes a natural way for complex numbers to be stored in and retrieved from the bytes32 data-type.  It splits the storage space exactly in half and, most importantly, assigns real numbers to the least significant 16 bytes and imaginary numbers to the most significant 16 bytes.

---

To create a complex number one would use

```nohighlight
function cnNew(int128 _Real, int128 _Imag) public pure returns (bytes32){
    bytes32 Imag32 = bytes16(uint128(_Imag));
    bytes32 Real32 = bytes16(uint128(_Real));
    return (Real32>> 128) | Imag32;
}
```

and to convert back

```nohighlight
function RealIm(bytes32 _cn)  public pure returns (int128 Real, int128 Imag){
	bytes16[2] memory tmp = [bytes16(0), 0];
	assembly {
	    mstore(tmp, _cn)
	    mstore(add(tmp, 16), _cn)
	}
	Imag=int128(uint128(tmp[0]));
	Real=int128(uint128(tmp[1]));
}
```

See [Add EIP-5850: Complex Numbers stored in Bytes32 types by genkifs · Pull Request #5850 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5850) for discussion

The EIP doesn’t discuss the manipulation of complex numbers when they are in Byte32 form because this is undoubtedly a much larger topic.
