---
source: magicians
topic_id: 19798
title: "RIP-7696 : generic Double Scalar Multiplication (DSM) for all curves"
author: rdubois-crypto
date: "2024-04-25"
category: RIPs
tags: []
url: https://ethereum-magicians.org/t/rip-7696-generic-double-scalar-multiplication-dsm-for-all-curves/19798
views: 2441
likes: 31
posts_count: 25
---

# RIP-7696 : generic Double Scalar Multiplication (DSM) for all curves

This proposal creates two precompiled contracts that perform a double point multiplication (DSM) and sum then over any elliptic curve  given `p`, `a`,`b` curve parameters.

This operation consists in computing the value uP+vQ, u and v being scalars, P and Q being points.

We managed to implement generic DSM in full solidity with a lower cost than previous implementations (FCL, Daimo, p256-verifier-huff). Such genericity will enable curves such as Ed25519 and Babyjujub (with the use of isogeny we will describe later), Palla,Vesta, Starkcurve, etc.

The proposal includes two precompiles, taking curves parameters as calldata.

The first one is very comparable to RIP7212 and EIP6565, only taking those extra p,a,b parameters.

The second them uses extra values (namely 2^128.P and 2^128Q), to provide a GLV comparable speedup, which is 50% asymptotically (less in full solidity, but ZK version will benefit largely from it).

As of now there is a huge traction on P256, being the first FIDO curve implemented in WebAuthn. Ed25519 shall follow, and is superior in all ways (Schnorr based, no hidden seed constant,MPC friendly).

This precompile also solve the ‘hacky’ use of ecrecover (as implemented for Schnorr based Dapps, such as Ambire Wallet, and secure MPC uses relying on Musig2). This cunning use of ecrecover in fact enables DSM.

Implementing DSM at lower levels (for ZKEVM or nodes) only requires to implement Montgomery multiplications to emulate prime fields. (It is how it is done by Lambda for ZKsync right now). This is how are implemented most generic libraries (OpenSSL, libECC, Bolos, etc.).

https://github.com/ethereum/RIPs/pull/18/files#diff-1991105bd164aa9e87619fa8426d5978f420c7033b30393f07a3b7afd09df7f3

## Replies

**jdetychey** (2024-04-25):

*insert youtube video “Shia LaBeouf “Just Do It” Motivational Speech”*

Thanks for this RIP that will also benefit EVM L2 not sequencing on the Ethereum mainnet.

---

**nlordell** (2024-04-26):

Personally, I would be super happy to see Ed25519 and EdDSA in general over ECDSA. However, AFAIU it uses SHA-512 as the hashing function, for which there is no precompile at the moment, making it not so useful (which is a shame IMO).

Also, as far as I understand, Ed25519 is a **twisted Edwards** curve, while this precompile implements `uP + vQ` given scalars `u` and `v` and points `P` and `Q` for **Weierstrass** curves with coefficients `a` and `b`. Correct me if I’m wrong (this is not my area of expertise), but I think you can map twisted Edwards curves to and from Weierstrass form, allowing this precompile to be used for efficient EdDSA signature verification, but it would be nice to spell out how this is done somewhere (for less cryptographically savvy engineers like myself).

---

**rdubois-crypto** (2024-04-26):

You are totally right, it is very cheap to reuse Weierstrass formulae to implement Ed25519 (only a few multiplication/inversion),  the name of the isogeneous curve is Wei25519, here is the solidity code:

function Edwards2WeierStrass(uint256 x,uint256 y)  view returns (uint256 X, uint256 Y){

//wx = ((1 + ey) * (1 - ey)^-1) + delta

X=addmod(delta, mulmod(addmod(1,y,p),pModInv(addmod(1, p-y,p)),p) ,p);

//  wy = (c * (1 + ey)) * ((1 - ey) * ex)^-1

Y=mulmod(mulmod(c, addmod(1, y, p),p),        pModInv(mulmod(addmod(1, p-y,p), x,p)),p);

}

Concerning SHA512 you are right for L1 where gas is cheap for SHA256 (but that should change as gas cost on L1 shall reflect more the ZK cost in the future). But for a L2, implementing SHA512 circuit is a similar cost to SHA256.

There are also equivalent version of EDdsa, over babyjujub, which uses Poseidon instead (Circom framework), sometimes ZK is not necessary everywhere and using ZK verifier for a simple Eddsa verification is “crushing a fly with a Hammer”.

The concern is also over MPC versions. ECDSA is crippled with vulnerabilities, while Musig2, used for Taproot BTC gives better security proofs. DSM enables MPC signatures.

The thing is also “why choose now ?” option, using 7696 instead of limiting to a single curve through 6565 or 7212 provides maximum degree of freedom.

---

**nlordell** (2024-04-26):

> You are totally right, it is very cheap to reuse Weierstrass formulae to implement Ed25519 (only a few multiplication/inversion), the name of the isogeneous curve is Wei25519, here is the solidity code:

Ok, so if I understand correctly, this code maps Ed25519 curve points to a point on the Wei25519 Weierstrass curve. Given the signature verification equation `[s]B = R + [k]A` (B is base/generator point, s and R are signature components, A is the public key), you would implement this by mapping B, R, and A to Wei25519 and using `ecmulmuladd` to verify the equality holds?

---

An additional point, I noticed that the EIP assumes ECs over prime fields where `p` fits into 256-bit integers. I wonder if it makes sense to consider a mechanism like the [EXPMOD precompile](https://eips.ethereum.org/EIPS/eip-198) where additional widths for the values in Fp are included in the parameters. This would allow supporting `ecmulmuladd` for curves over larger prime fields like P-384. To elaborate on this a bit, the input data would look like:

- Input data: 64 + 7n + 2l bytes of data including:

32 bytes of the size n in bytes required to represent elements of the prime field over which the elliptic curve is defined
- 32 bytes of the size l in bytes required to represent the curve order
- n bytes of the modulus p modulus of the prime field of the curve
- n bytes of the a first coefficient of the curve
- n bytes of the b second coefficient of the curve
- n bytes of the Px x coordinate of the first point
- n bytes of the Py y coordinate of the first point
- n bytes of the Qx x coordinate of the first point
- n bytes of the Qy y coordinate of the first point
- l bytes of the u first scalar to multiply with P
- l bytes of the v second scalar to multiply with Q

We can probably conflate `n` and `l` use a single “size” for all values, since they tend to have a similar order of magnitude in most cases and `max(n, l)` will always suffice.

---

**rdubois-crypto** (2024-04-26):

The thing is that the implication to handle 384 bits curve has a lot of implication at ZK level. Handling variable length is more complex in term of code coverage, audits and potential vulnerabilities.

It implies to handle multiprecision integers (EVM is a 256 bit machine). It seems less probable to be accepted any time soon, as MSM which has been proposed for long now. There is a cursor to place between a fully configurable MSM (not limited to double, but any number of points) over any curve, and very specific (limited to one curve) precompile.

MSM is superior, but too complex. Specific curves precompiles are too limited. Optimized DSM is only 100 lines of solidity code. Actually it is very close to the specific one (mainly handling constant into calldata, and more efforts to handle the stack without via IR which crush performances).

Actually the provided code will be used as a temporary solution by some L2s before implementing it at circuit level.

---

**rdubois-crypto** (2024-04-26):

I forgot to answer the Ed25519 part. Yes I did it. I reproduced the RFC8032 vectors for short length, ECC is OK, but I still work on the SHA512 part.

---

**nlordell** (2024-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rdubois-crypto/48/6815_2.png) rdubois-crypto:

> Handling variable length is more complex in term of code coverage, audits and potential vulnerabilities.
> It implies to handle multiprecision integers

I agree it is at first glance more complex, however, I just figured that since `expmod` precompile already requires arbitrary precision integer math, that it would not be a stretch to add it for `mulmuladd`. I would argue that the implementation difference between implementing this precompile for 256 bit integers vs. arbitrary precision integers is not that crazy, and mostly boil down to figuring out an appropriate gas schedule that is in function of the integer width, like `expmod` does.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rdubois-crypto/48/6815_2.png) rdubois-crypto:

> It seems less probable to be accepted any time soon, as MSM which has been proposed for long now. There is a cursor to place between a fully configurable MSM (not limited to double, but any number of points) over any curve, and very specific (limited to one curve) precompile.

For sure. I also would generally assume that use cases for curves over prime fields where `log2(p) > 256` is not so widespread, and as you mentioned would eliminate the possibility of providing a Solidity fallback.

I do think it might be worth documenting this rationale in the RIP itself.

---

**nlordell** (2024-05-02):

Another significant advantage over 7212 IMO is that this would also allow ECDSA **recovery** to be implemented efficiently for curves like P-256.

---

**mratsim** (2024-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nlordell/48/10721_2.png) nlordell:

> I would argue that the implementation difference between implementing this precompile for 256 bit integers vs. arbitrary precision integers is not that crazy, and mostly boil down to figuring out an appropriate gas schedule that is in function of the integer width, like expmod does.

I didn’t check how good `modexp` gas schedule is, but one artifact is that implementations for odd moduli is wildly different from implementation for even moduli. And below a certain size, moving to Montgomery domain for Montgomery multiplication exposes you to denial-of-service.

That said, it’s “just” a matter of implementing and measuring the gas cost, one can do that in Constantine: [EIP-2537 (BLS12 precompile) discussion thread - #77 by mratsim](https://ethereum-magicians.org/t/eip-2537-bls12-precompile-discussion-thread/4187/77) and even get detailed metering on internal calls, for example: [constantine/metering/eip2537.md at master · mratsim/constantine · GitHub](https://github.com/mratsim/constantine/blob/master/metering/eip2537.md#pairing)

---

**rdubois-crypto** (2024-06-04):

Hi, just some news here.

We added ed25519 computation using the 4MSM described in RIP7696.

It is run over all the rfc8032 vectors here:



      [github.com](https://github.com/get-smooth/crypto-lib/blob/7cef31dd0cb36b9a814866085463d8e758a0d1be/test/libSCL_rip6565.t.sol#L158)





####



```sol


1. res=SCL_RIP6565.Verify_LE(string(Msg), r, s, extKpub);
2.
3. assertEq(res,true);
4. }
5.
6.
7. /*assess all testvectors of  [ED25519-TEST-VECTORS]
8. Bernstein, D., Duif, N., Lange, T., Schwabe, P., and B.
9. Yang, "Ed25519 test vectors", July 2011,
10. .*/
11. function test_rip6565_allrfc() public view {
12. uint256[5] memory extKpub;
13. uint256[2] memory signer;
14.
15. bool res;
16.
17. string memory file = "./test/utils/ed25519tv.json";
18. while (true) {
19.
20. string memory vector = vm.readLine(file);
21. if (bytes(vector).length == 0) {


```










If you have some use cases for the Ed25519, please reach us (we are thinking about farcaster, cosmos bridges, Webauthn with eddsa). Last year, many have built upon FCL (Base Smartwallet, Abstract Wallet, many demos). We would like to support the migration to the more efficient and generic SCL to encourage RIP7696.

---

**mratsim** (2024-07-18):

Maybe we can have 2 different precompiles, one for 256 and one for 384 bits so that it’s also easier for zkEVMs / zkVMs to specialize.

For instance, one use-case for Taiko is verifying signatures coming from Amazon Nitro enclaves which use P-384.

Furthermore for zkEVMs, as soon as you deal with fields larger than the curve order, you already need to deal with “carries” beyond your order.

And BN254 which is the sole valid curve until EIP-2537 is delivered, only has a 254-bit order. Meaning when used with Curve25519, it will need to deal with the extra bits the same way it would deal with extra bits with P384.

---

**rdubois-crypto** (2024-07-18):

Going with a bunch of specific RIP decreases the chance of adoption of each IMHO. So we could adapt the RIP to be more generic.

The thing is that I didn’t realize the fact that progressive precompile is the way for Dapps (pushing something anyone can use, then by its adoption push it to RIP then EIP).

But in fact L2s need node implementations in major clients. And major clients won"t integrate anything destined to L1. Seems like the process is in a “chicken or egg” situation here.

---

**mralj** (2024-09-17):

Hello everyone!

Firstly I want to stress that I have never implemented any cryptographic algorithms nor implemented any EIPs/RIPS. But I want to learn ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

I came across this RIP and I was wondering what’s the process of actually implementing this in prod.

As I am experimenting with various `geth` forks I wanted to see how hard would it be to fork `geth` and implement this. Here is my understanding/what I have so far:

1. I have created my lib for handling general Weierstrass curves (by handling I mean I’ve implemented code to calculate ecMulmuladd). Note this is not prod-ready - not even close.
2. I have a fork of geth and I plan to follow eg. op-geth steps adding RIP-7212 to add support for RIP-7696 in my experimental fork.
3. Write “integration” tests core/vm/contracts_test.go
4. Q: To test this I should have a node running and execute Solidity code similar to this example to check if the precompile was indeed called?
5. Q: To benchmark should I use benchmarkPrecompiled from core/vm/contracts_test.go
6. Q: Is there a way of checking that implementation correlates with suggested gas usage?

Am I missing some steps?

Of course, I understand that this won’t lend in official geth repo, at the moment my journey is for learning purposes.

#### Questions about implementing prod-ready Weierstrass curve

I have an “mvp” version of the implementation [link](https://github.com/NethermindEth/weierstrass)

I believe the implementation is correct since I’ve used Sage to generate a bunch of tests.

It uses the Montgomery ladder to calculate `kP`, it is implemented naively - without any performance improvements, and since it has branched in algo execution, I guess that it is not side-channel attack resistant.

In the RIP description it is stated:

> The node is free to implement the elliptic computations as it sees fit (choice of inner elliptic point representation, ladder, etc).

Since I already have a naive implementation, and since the description also helpfully includes a couple of techniques for performance improvements, I wondering about benchmarking the improvements.

My questions are:

1. How to benchmark the implementation against get-smooth by @rdubois-crypto as their code is in Solidity and this will be Go implementation
2. What’s the best way to make sure implementation is “cryptographically secure” (ie resistant to side-channel attacks)
3. What’s the best way of making sure (testing) the correctness? Is generating test vectors via Sage the way to go or are there better approaches?

I know I asked a bunch of questions, but any answers would be much appreciated!

---

**rdubois-crypto** (2024-09-17):

Hi,

Thanks for you interest in the RIP. I will first answer for the Weierstrass part:

- you can benchmark by selecting various curves from Wycheproof project. We actually run all ed25519 and P256 vectors in the repo. But this is only a start.
- Side channel attack are not in the scope of a node because there is no secret to extract. Except if you consider bugs as a channel (as Shamir bug attack). Bugs can lead to critical vuln (such as this one ) and loss of funds, which lead to next point.
- The only way is to go through audits, SCL currently went through 2 audits (CryptoExperts and Verdise). This is expensive, but i am very surprised that despite HUGE warnings, people still use my last FCL.

---

**rdubois-crypto** (2024-09-17):

For the node implementation part, i did not go through it, but it is clearly important to push 7696. I think op-geth already have its support of 7212 by Clave team. I will gladly help for 7696 integration thus. Do not hesitate to PM me.

---

**mralj** (2024-09-17):

> I think op-geth already have its support of 7212 by Clave team

Yeah they do, [since Fjord fork](https://github.com/ethereum-optimism/op-geth/pull/168/files)

> I will gladly help for 7696 integration thus. Do not hesitate to PM me.

Thanks! I don’t maintain any of the official geth forks, but  if I manage to get this working on node (even with naive algorithm implementation) I’ll let you know so that can be used to kickstart implementing this properly ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**mralj** (2024-09-17):

[@rdubois-crypto](/u/rdubois-crypto)  one more small thing, not sure if I’m *brain farting*, but in [the RIP spec](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7696.md#ecmulmuladd) it is stated:

> #### ecMulmuladd
>
>
>
> The ecMulmuladd precompiled contract is proposed with the following input and outputs, which are big-endian values:
>
>
> Input data: 224 bytes of data including:
>
> 32 bytes of the modulus p modulus of the prime field of the curve
> 32 bytes of the a first coefficient of the curve
> 32 bytes of the b second coefficient of the curve
> 32 bytes of the Px x coordinate of the first point
> 32 bytes of the Py y coordinate of the first point
> 32 bytes of the Qx x coordinate of the first point
> 32 bytes of the Qy y coordinate of the first point
> 32 bytes of the u first scalar to multiply with P
> 32 bytes of the v second scalar to multiply with Q

What’s bothering me is the `224 bytes`.

I’m counting `9 args * 32 bytes = 288 bytes of data`. Is there typo in the spec, or am I wrong?

Note for [ecMulmuladd_b4](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7696.md#ecmulmuladdb4) we have `32 * 13 = 416` as stated in the specs (so that maches)

---

**rdubois-crypto** (2024-09-18):

Your are totally right, gonna push the correction

---

**rdubois-crypto** (2024-09-22):

The Eucleak vulnerability is one from many examples  about why RIP7696 and cryptographic agility seems preferable.

First, there is no true reason to prefer P256 over EDDSA:

- Eddsa is compatible with frost, while ecdsa is not. It is more MPC friendly,
ECDSA-MPC suffered several flaws
- Yubikey P256 is compromised by Eucleak, and there might be other hardwares, including enclave sensible to it. Eddsa is not vulnerable to euckleak because no nonce inversion is required.
- eddsa is deterministic, thus enables to derive secret from the signing algorithm. While a distinct algorithm&key is preferable, leveraging secure enclave is always preferable. Nonce generation is also a strong covert channel,
- actually looking at SHA512, its implementation might be faster than SHA256, because emulating 64 bits numbers from 31/32 bits as in babybear/goldylocks/M31 require 3 elements to parse input by 64 bits, while 32 bits elements require 2 element to parse input by 32. Remember that the roadmap is to align hash function cost to ZK proving cost.
- eddsa has a “proof of generation”, following the “nothing in my sleeves”, while P256 is still opaque.

Remember that ECDSA was a weaker alternative choice to avoid patents no expired. EDDSA would have been the way to go otherwise.

Not saying that P256 should be banned, but be second choice when Eddsa over Ed25519 is possible. It might happen (but less likely) that a HW will have its Ed rather than ECdsa implementation broken.

My concern about Eucleak is that if it had happenned in a more complex hardware than ubikey, another process spying the enclave could enable remote attack (while Eucleak concern is only about cloning capacity).

---

**Arvolear** (2024-12-24):

Really like this one, especially if higher-order curves can be supported.

We actually used double scalar multiplication (Strauss-Shamir method) with 6 bits of precompute to implement on-chain verification of ECDSA signatures over 384-bit curves. Check out the Solidity code [here](https://github.com/dl-solarity/solidity-lib/blob/b94757194de6436062c2d68118c0352be84ac4be/contracts/libs/crypto/ECDSA384.sol) (fuzz-tested and fully covered).

P.S.

Many national passport issuers use higher-order curves to sign off passports. I see this ZK research area benefiting a lot from a DSM precompile.


*(4 more replies not shown)*
