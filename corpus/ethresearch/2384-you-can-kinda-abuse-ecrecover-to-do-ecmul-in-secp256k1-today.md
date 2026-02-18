---
source: ethresearch
topic_id: 2384
title: You can *kinda* abuse ECRECOVER to do ECMUL in secp256k1 today
author: vbuterin
date: "2018-06-29"
category: Applications
tags: []
url: https://ethresear.ch/t/you-can-kinda-abuse-ecrecover-to-do-ecmul-in-secp256k1-today/2384
views: 12805
likes: 32
posts_count: 19
---

# You can *kinda* abuse ECRECOVER to do ECMUL in secp256k1 today

Here’s the code for elliptic curve signature recovery, copied from pybitcointools, and cleaned of details that are irrelevant to our exposition

```python
def ecdsa_raw_recover(msghash, vrs):
    v, r, s = vrs
    y = # (get y coordinate for EC point with x=r, with same parity as v)
    Gz = jacobian_multiply((Gx, Gy, 1), (N - hash_to_int(msghash)) % N)
    XY = jacobian_multiply((r, y, 1), s)
    Qr = jacobian_add(Gz, XY)
    Q = jacobian_multiply(Qr, inv(r, N))
    return from_jacobian(Q)
```

Suppose that we feed in msghash=0, and s=r*k for some k. Then, we get:

- Gz = 0
- XY = (r,y) * r * k
- Qr = (r,y) * r * k
- Q = (r, y) * r * k * inv(r) = (r, y) * k

Hence, the elliptic curve signature feeds out `k` times the point `(r, y)`, where `r` and `k` are values you feed in, and you specify the parity of `y` via `v`.

Unfortunately, the secp256k1 precompile outputs the truncated hash of Q, and not Q itself. But you can get around that by requiring the function caller to submit Q as a witness. The extra cost of 64 bytes of data is ~4000 gas, so altogether you can get an ECMUL with <10k gas, under a quarter of what you need if you use the ECMUL precompile that uses the alt_bn128 curve.

This could be used as a ghetto hack to optimize ring signatures in the EVM today, as well as other applications.

## Replies

**mattdf** (2018-07-05):

ECADD still has to be done manually though, I take it?

---

**vbuterin** (2018-07-05):

Yep! Though that’s very cheap; at most a few thousand gas I think.

---

**k06a** (2018-07-31):

Tried to implement this trick with Solidity, but had no luck yet. Any suggestions? How `v` should define `y`'s parity? Need this trick for split-key address generation.

**UPDATE:**

Fixed and fully working implementation for `secp256k1` elliptic curve:

```auto
function ecmulVerify(uint256 x1, uint256 y1, uint256 scalar, uint256 qx, uint256 qy) public pure
    returns(bool)
{
    uint256 m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;
    address signer = ecrecover(0, y1 % 2 != 0 ? 28 : 27, bytes32(x1), bytes32(mulmod(scalar, x1, m)));
    address xyAddress = address(uint256(keccak256(abi.encodePacked(qx, qy))) & 0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF);
    return xyAddress == signer;
}

function publicKeyVerify(uint256 privKey, uint256 x, uint256 y) public pure
    returns(bool)
{
    uint256 gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798;
    uint256 gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8;
    return ecmulVerify(gx, gy, privKey, x, y);
}
```

---

**vbuterin** (2018-07-31):

How do you know it doesn’t work? Do you have tests that fail? If so, does it at least work with scalar=1?

---

**k06a** (2018-07-31):

[@vbuterin](/u/vbuterin) just discovered `v` should be inverted parity: 28 for odd `y` and 27 for even `y`. Just tested this code, and it works for `scalar` equal to `1` and `2`, but not for `3` and not for `4`.

**UPDATE:**

I am running tests on `ganache-cli`. Just checked in REMIX JS VM - same result.

---

**vbuterin** (2018-07-31):

Maybe use python with https://github.com/ethereum/py_ecc to implement ECRECOVER, make sure its results are solidity-compatible, but watch each step of the ecrecover procedure and see where it starts “not going according to plan”?

---

**shamatar** (2018-07-31):

We’ve resolved it in a off-chain discussion, the trick is in the last equation

Q = (r, y) * r * k * inv® = (r, y) * k

inv® should obviously be computed modulo the group order of the curve group (usually refered as q), but not the prime field modulus (refered as p).

[@k06a](/u/k06a) please make a tested implementation public for everyone ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**k06a** (2018-07-31):

[@shamatar](/u/shamatar) thank you, sure! Fixed bug in my prev comment.

The source code with tests: https://github.com/1Address/ecsol

---

**HarryR** (2018-08-09):

So, the function can be adopted to do two multiplications and an addition, as is used by ring signatures, see code below.

```python
t = randsn()
T = sbmul(t)
c = randsn()
y = randsn()
Y = sbmul(y)

m = (((N - t) % N) * Y[0]) % N
X = hackymul_raw(Y[0], Y[1], c, m=m)
self.assertEqual(X, add(T, multiply(Y, c)))
```

But, you can’t do plain Schnorr signatures because it requires `t` be hidden, unless you use a witness.

I’ve adopted my Python AOS Ring implementation to use the `ecrecover` hack: https://github.com/HarryR/solcrypto/blob/master/pysolcrypto/hackyaosring.py

It can also be used to verify Pedersen commitments.

And, it seems it *can* be used for linkable ring signatures, but you have to provide witness points for both M^t and \tau^c, then add the witness points together.

---

**HarryR** (2018-08-09):

So, the operations which you can perform are:

1. (g^a + B^c) - multiply a point by a scalar and add it to the generator multiplied by a scalar, if a is zero, it acts just like B^c
2. (A^b + C^d) - multiply two points by two scalars and add them together, however you need to provide the results of A^b and C^d as ‘witnesses’ to verify the ecmul operations are correct, then you can add the two witness points together.

As I mention above, the first makes it possible to verify pedersen commitments using one `ecrecover` operation, or to verify ring signatures (not tagged/linkable ones though).

The second makes it possible to do lots more, e.g. linkable ring signatures, Schnorr signatures, aggregate MuSig etc. but you need to provide a witness point for anything you multiply on-chain to verify correctness.

---

**tetratorus** (2018-10-16):

ecadd for secp256k1 still takes quite a bit of gas (androlo’s version takes ~30k gas), primarily because invmod is pretty expensive when you convert it back to affine from jacobian.

Is there a cheaper way to do ecadd that anyone is aware of?

I’ve already written some code that uses the hacky ecmulVerify by providing witness coordinates - maybe it also makes sense to include invmod precomputes? that would bring the gas costs down to <10k

---

**vbuterin** (2018-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/tetratorus/48/5229_2.png) tetratorus:

> primarily because invmod is pretty expensive when you convert it back to affine from jacobian.

What algorithm are you using for the modular inverse? You can do it with a modular exponentiation, with ~384 average rounds of modmul (10 gas each), or you can do it with the extended Euclidean algorithm, which is more efficient in reality but actually has similar gas costs because modmul doesn’t care about the sizes of the numbers you’re multiplying. I recall doing a modinv in ~6000 gas.

---

**tetratorus** (2018-10-16):

Extended euclidean, it’s the one here https://github.com/androlo/standard-contracts/blob/master/contracts/src/crypto/ECCMath.sol.

---

**cygnusv** (2018-10-17):

Perhaps you can use addition in Jacobian coordinates and only convert to affine when it’s strictly necessary. For example, for adding two points in affine and comparing the result with a third point, also in affine, you can work in Jacobian coordinates the whole time. Doing this with our [Numerology library](https://github.com/nucypher/numerology) costs around 4500 gas in total (~1400 for the addition and ~3100 for the equality comparison). We have just added a couple of functions for doing exactly this.

---

**tetratorus** (2018-10-17):

True, but several signature verifications require affine representation (eg. Schnorr). Was thinking that since we will need to provide precomputes for points if we need to do point multiplication, it might also make sense to include invmod precomputes, which can be easily verified via a single mulmod.

---

**cygnusv** (2018-10-17):

Yes, what I meant is that although your input points are in affine, you can do the computations internally in Jacobian. This uses the fact that affine to Jacobian transformation is trivial (i.e… just take the z coordinate as 1). See this example, where we add two affine points and compare with an expected result, also in affine. The main operations only take 4.5K gas.


      [github.com](https://github.com/nucypher/numerology/blob/8d61a95f63e5252f286550150893633f6a561f1f/contracts/verifier.sol#L69)




####

```sol

1. ];
2.
3. bool sum_is_correct = Numerology.eq_jacobian(Numerology.addJac([expected[0], expected[1], 1], [expected[2], expected[3], 1]), [expected[4], expected[5], 1]);
4. bool kP_is_correct = Numerology.ecmulVerify(P_Q[0], P_Q[1], k_l[0], expected[0], expected[1]);
5. bool lQ_is_correct = Numerology.ecmulVerify(P_Q[2], P_Q[3], k_l[1], expected[2], expected[3]);
6.
7. return sum_is_correct && kP_is_correct && lQ_is_correct;
8.
9. }
10.
11. function test_add_eq_jac() public view returns (bool) {
12. uint256 e0 = 0xaddcb45773b26a2f8ac2143627d54f47a12aab533dc1b41b4e791985e9eca496; // kP_x
13. uint256 e1 = 0x72da5adb3a30a2cf147d309b0cf58c76b322c82a5edae164e13dbeed6429c41d; // kP_y
14. uint256 e2 = 0xf07716879380e987f8b5551a1d989068d0003061088a869a33ceb9848771c6fd; // lQ_x
15. uint256 e3 = 0x2447ed4564b75b0f9ff84013aaa37c2ab67a2c621b0edc91a06895f19a93aebb; // lQ_y
16. uint256 e4 = 0x9ca8f6ff6a2eb6f62787f70b9f7c4939d1a3890ec87343e4f6716f9f6867eb86; // Rx
17. uint256 e5 = 0x290c40f22995dc8b956d2c63ec060d332d082124d638ed618891171db8bc206f; // Ry
18.
19. return Numerology.eq_affine_jacobian([e4, e5], Numerology.add_affine_to_jac([e0, e1], [e2, e3]));
20. }
21. }

```

---

**tetratorus** (2018-10-17):

Yes, but in order to validate a schnorr signature you need to take the hash of the affine x coordinate of the sum of y^e.g^s (where e = H(m||g^k)), so if you want to validate a schnorr signature onchain you’d need to convert it to affine onchain

EDIT: oh ok i think i got it, you can check equality of sum of two points in affine (that’s in jacobian form) vs affine representation of that sum. That does work, but it assumes that you provide the affine representation of the sum of the points. Might as well just provide the invmod

---

**merkleplant** (2025-01-20):

It is important to note that this trick does not work for secp256k1’s full public key space as `ecrecover` [fails if r >= N](https://www.evm.codes/precompiled?fork=cancun#0x01) (`N` being the order of the curve).

Note that `r` is set to the public key’s `x` coordinate which is defined over the prime field and therefore in `[1, P)` with `P >= N`. However, the work to find a private key with a public key’s `x` coordinate greater than `N` is roughly 128 bit of work - and therefore of negligible probability.

PoC:

```js
pragma solidity ^0.8.13;

import {Test} from "forge-std/Test.sol";

uint constant N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;
uint constant P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F;

function ecmul(uint x, uint y, uint scalar) pure returns(address) {
    return ecrecover(0, y % 2 != 0 ? 28 : 27, bytes32(x), bytes32(mulmod(scalar, x, N)));
}

function isOnCurve(uint x, uint y) pure returns (bool) {
    uint left = mulmod(y, y, P);
    uint right = addmod(mulmod(x, mulmod(x, x, P), P), 7, P);

    return left == right;
}

function toAddress(uint x, uint y) pure returns (address) {
    return address(uint160(uint(keccak256(abi.encode(x, y)))));
}

contract EcmulTest is Test {
    function test_ecmulVerify_PoC() public pure {
        // Note that [1]P = P.
        uint scalar = 1;

        uint x;
        uint y;

        // Make a valid secp256k1 point with x >= N.
        x = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffeeffffc2e;
        y = 0xa0981151316a5be677beb8ab97d4a15eba3e4638bfdc86038afffe1f445f4496;
        require(isOnCurve(x, y));

        // Note that ecrecover fails.
        assertEq(ecmul(x, y, 1), address(0));

        // Now lets try some other point (generator).
        x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798;
        y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8;
        require(isOnCurve(x, y));

        // Note that ecrecover works as expected.
        assertEq(ecmul(x, y, scalar), toAddress(x, y));
    }
}
```

