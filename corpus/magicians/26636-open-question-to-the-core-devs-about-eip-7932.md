---
source: magicians
topic_id: 26636
title: Open question to the core devs about EIP-7932
author: SirSpudlington
date: "2025-11-19"
category: Uncategorized
tags: [wallet, postquantum]
url: https://ethereum-magicians.org/t/open-question-to-the-core-devs-about-eip-7932/26636
views: 325
likes: 5
posts_count: 25
---

# Open question to the core devs about EIP-7932

Considering that [EIP-6404 may implement native interop to EIP-7932](https://github.com/ethereum/EIPs/pull/10755), would it align better with the Ethereum roadmap for EIP-7932 to be a lower scope `registry` + `precompile` setup?

This would allow efficient-*ish* account abstraction as signature verification for *all* algorithms could be performed with just:

```auto
(bool ok, bytes memory result) = sigrecover.staticcall(
    abi.encodePacked(sig_hash: Hash32, signature: Bytes)
);

require(ok);
require(address(result) == AA_expected_address);

// A shim may be needed for access with native signatures e.g.
require(msg.sender == AA_expected_address)
```

As core developer feedback is mixed (to put it lightly), I have decided to ask an open question here on whether to keep the RLP wrapper or strip down the EIP to favour AA. Also, if EIP-6404 and EIP-7932 are included in the same fork, the RLP wrapper would be invalidated anyway. If the wrapper version of EIP-7932 is included before EIP-6404, it’ll make implementation 4x more difficult and cause even more apprehension towards EIP-6404.

There is a draft PR of the stripped down EIP-7932 below:

https://github.com/ethereum/EIPs/pull/10754

## Replies

**shemnon** (2025-11-23):

That’s something I’ve worked on privately and is the same design decision I came to, except the signature should come first and the hash/message should come last.

The reason is some PQ schemes sign over the whole message and not just a hash, although for common account we can sign over a transaction data hash. Putting the hash last allows precompiles to have open ended messages to still be useful outside of account signatures.

---

**SirSpudlington** (2025-11-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> The reason is some PQ schemes sign over the whole message and not just a hash, although for common account we can sign over a transaction data hash. Putting the hash last allows precompiles to have open ended messages to still be useful outside of account signatures.

`sigrecover` is designed be as close to a `ecrecover` drop in as possible. Which means that it only really works with accounts, and as you said using the hash is fine for transaction signing (which would be the only real use for `sigrecover`).

I am not saying that there shouldn’t be a mechanism for signing over non-hashed data. Algorithms definitions **should** introduce their own precompile for more fine grained PQ interactions, i.e. non-hashed data signing. A good example would be the [ML-DSA](https://github.com/ethereum/EIPs/pull/10557) EIP, it has both a precompile for direct verification and EIP-7932 algorithm support for transactions.

---

**shemnon** (2025-11-24):

It would be bad engineering engineering and wasteful to force two precompiles when a re-ordering of parameter order would be appropriate.

We also need to consider other post-quantum concerns, such as leaving space to expand the size of the has to accomodate concerns about Grover’s Algorith,  Putting the message at the end and letting the size of the input determine it’s size is the lowest-byte way to accompish both tasks without increasing the testing surface and number of precompiles.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> A good example would be the ML-DSA EIP, it has both a precompile for direct verification and EIP-7932 algorithm support for transactions.

I think you are mis-reading the EIP, there are two different algorithms, not one for hashed signing and one for unhashed.  One uses SHAKE256 as the XOF (the NIST standard) and one with Keccak. I’m doubtful how needed the second one will be if we have the NIST standard.  A better comparison would be secp256k1 and secp256r1, botha re ECDSA but distinct.

---

**SirSpudlington** (2025-11-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I think you are mis-reading the EIP, there are two different algorithms, not one for hashed signing and one for unhashed. One uses SHAKE256 as the XOF (the NIST standard) and one with Keccak. I’m doubtful how needed the second one will be if we have the NIST standard. A better comparison would be secp256k1 and secp256r1, botha re ECDSA but distinct.

I can confirm that I am not mis-reading, the EIP defines two algorithms. In each definition, a precompile and a separate EIP-7932 integration is defined.

[I have reordered the precompile parameters to support potential extension EIPs](https://github.com/ethereum/EIPs/commit/ecaa087eff4b117376104fcc6425c2ae1b2200c9). However, the entire framework revolves around Hash32 for verification as **everything** uses keccak256 and having a really complex EIP would not go well for hard fork inclusion.

If an EIP is defined to extend the address space / use keccak512, it’ll be easy to update 7932.

---

**shemnon** (2025-11-24):

Would it be possible to get rid of the sizing field in the signature of the signature size?

There are several design considerations for this:

1. How many parts are the signature in?
2. Does it support direct key extraction?
3. Do we support multiple algorithm strengths?

For the last question, supporting multiple strengths in the same precompile intuitively feels like a bad idea. I doubt we will get requirements of the form “supports Algo X of strength Y or higher” more likely it will be “X-Y algo” and we can have one precompile per algo/strength. Single purpose non-switching precompiles are in general better for testing and snarkification.

For part two I doubt we will get a variable length signature from the NISTor other standards body. Falcon is evidence for this, as their compressed form has an upper limit of 666 bytes and mandated zero padding, making it fixed. A two byte sizer would have made the signature typically shorter, but from the discsussions I could find the desire for a fixed width form is overwhelming.

Finally for the first part, I went with an opaque byte string and mandated that what is seen in a transaction is also what would be passed into the precompile. Magic V number and separate r and s?  Whatever, just keep the order and offsets the same. PubKey and hash and signature? Just pack it the same in both places.  It helps that standard serializations are coming out of NIST for these features.

---

**SirSpudlington** (2025-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Would it be possible to get rid of the sizing field in the signature of the signature size?

Yes. If we assume a 256 bit hash function, we could take the last `n` bytes of the provided precompile data as the hash data and just assume `data[:-32]` is the signature data. This still creates a forward compatability issue though, so we can have either the size parameter, some other selector/magic or forward compatability issues.

The alternative is just to create another precompile that shares functionality but with an expanded hash length, however this is another excessive workload that dev teams have to deal with.

Personally, I’d go with `0x20 || hash || signature` as it allows future hash sizes to work by just changing the magic `0x20` to something like `0x40` while still allowing a simple:

```auto
assert(data[0] == 0x20)
hash = data[1:33]
signature = data[33:]
```

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Do we support multiple algorithm strengths?

**Yes and no**. An algorithm could define multiple strengths, but each would require a unique ID unless the algorithm does some soft of dynamic routing.

I agree with the sentiment that this is hard to test and prove, and would discourage it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> How many parts are the signature in?
> Does it support direct key extraction?

Having the signature be just a blob allows EIP-7932 to safely ignore these issues, because as far as the registry is concerned, we take `bytes` and turn it into either an error or an `address`. The algorithm does all the heavy lifting. This means we can keep 7932 as lean as possible, which should help overcome the already high implementation complexity of this proposal.

When it comes to fixed length signatures, we *could* have a system where algorithms define a fixed size and we use that for serialization. However, it feels overly complex for what would only be used in the precompile.

---

**shemnon** (2025-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> 0x20 || hash || signature

A single byte size prefix limits messages to 256 bytes, which will result in limitied utility of the precomple.

`<signatuere_blob> || hash` is cleaner and allows the message to be validated by the signature to be unbounded.  I wan to emphasize this again, not all signature schemes only sign fixed-width hashes. All the standardized and standards track post-quantum cryptography algorithms sign over the entire message, not the hash. To limit input size is to cripple utility.

---

**SirSpudlington** (2025-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> A single byte size prefix limits messages to 256 bytes, which will result in limitied utility of the precomple.

I may have been a bit vague in my description of the single byte, I do apologise for that. The single byte was not a length indicator, it was a type indicator, i.e. keccak256 → 0x20, keccak512 → 0x40, raw data → 0xFF.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I wan to emphasize this again, not all signature schemes only sign fixed-width hashes. All the standardized and standards track post-quantum cryptography algorithms sign over the entire message, not the hash.

While directly signing the message may be the norm of PQ algorithms, the majority of preexisting infrastructure uses keccak256. The `sigrecover` precompile is *not* for general use, it is a drop in replacement for `ecrecover` specifically for account related tasks e.g. an ERC20Permit. Fine grained control (e.g. signing over a raw message) should use the precompile specific to each algorithm.

---

**shemnon** (2025-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> i.e. keccak256 → 0x20, keccak512 → 0x40, raw data → 0xFF.

And how do we indicate the length of the raw data?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> While directly signing the message may be the norm of PQ algorithms, the majority of preexisting infrastructure uses keccak256.

This is a point in time argument, however in the life of the precompile I fully expect financial regulators to mandate longer hashes.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> The sigrecover precompile is not for general use, it is a drop in replacement for ecrecover specifically for account related tasks e.g. an ERC20Permit.

Constructed properly (message at the end) it is both a replacement for ecrecover and for general use.

---

**SirSpudlington** (2025-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> And how do we indicate the length of the raw data?

It could be possible to rework the registry to take generic `signature: Bytes, data: Bytes` → `ExecutionAddress`. But some field would still need *some form* of size indicator. If the signature data was at the end, we’d need a data length field or vice versa.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> This is a point in time argument, however in the life of the precompile I fully expect financial regulators to mandate longer hashes.

If we let the registry take some generic `Bytes` for the signing data, we push hashing to the individual algorithm. This may make migration harder.

Also, which PQ algorithms operate on the entirety of the data?

From the quick look I had at the publications of some algorithms I have seen that:

- Falcon uses SHAKE-256
- ML-DSA uses SHAKE-256
- XMSS uses SHAKE-256/512
- SLH-DSA uses SHAKE/SHA-256
- LMS uses SHA-256

So while they may take any arbitrary length data, as long as the input data is greater than the bit security of the individual algorithm, the security is still preserved.

If we take that into account, making the registry use a fixed 512 bit hash seems like a better option over allowing arbitrary data. It also allows algorithms that **cannot** support 512 bit hashes to just take `hash[:32]`

---

**shemnon** (2025-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> Also, which PQ algorithms operate on the entirety of the data?

Falcon, ML-DSA, and SLH-DSA, so all of the standardized ones. The first step is to hash the message with a random salt/nonce that is provided as part of the signature (this is considered part of the security as re-using the salt has not been ruled out for ways to crack the sigs).

SLH-DSA does specify that “pure” and “hash” signing get different domains for this initial hash.  But for size reasons SLH-DSA is not a good ledger signature.  Falcon and ML-DSA do not.

---

**SirSpudlington** (2025-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Falcon, ML-DSA, and SLH-DSA, so all of the standardized ones. The first step is to hash the message with a random salt/nonce that is provided as part of the signature (this is considered part of the security as re-using the salt has not been ruled out for ways to crack the sigs).

Thank you for clarifying,

I think my point here is that as long as we pass a hash that has a greater security guarantee of any sensible algorithm, there shouldn’t be an issue. Also the fixed length approach makes it *really* easy to take `n` bytes of entropy from the hash depending on the algorithm used.

The only exception would be secp256k1 which would have to provide backwards compatibility with existing infrastructure (at least until it is deprecated).

---

**shemnon** (2025-12-05):

Both of these uses can be easier satisfied if the message is the last value and the gas schedule only makes certain values viable.  Changing the gas schedule is much easier than creating a precompile.

for algorithms with key recovery:

>  ||

for algorithms without key recovery

>

 ||  ||

This presumes the key and signature for each algorithm are fixed width, which NIST appears to be committed to maintain (Falcon’s signature padding is the  evidence of this)

The returns would be either 32-byte 0x00 for failure, and on successful verification either 32 bit 0x01 or (if an address derivation exists) the address derivation for the public key. (pendantic note, this locks out the zero address from use, but if you can figure out the pubkey of the zero address there are many researchers that would want to know your techniques)

The next step to reduce zk complexity when we want to limit message to certain lengths is to make the gas schedule something like

```python
if len(input) != (pubkey_size + sig_size + hash_size):
  return MAX_GAS
else:
  return actual_cost
```

Then L2s that want to either use longer hash sizes, variable hash sizes, or even pure message signing, they just need to adjust he gas schedule instead of posting a new API.

With this schedule setup the transactions will not succeed unless they observe hashes only approach, as they will revert on the call if the message size is incorrect.

Yes, `ecrecover` has the hash first, but that is because Elliptic Curve signatures can only ever sign to the size of their curve. All current PQC algorithms sign over an unbound message size. Putting the message at the end allows the input size to imply the message size without additional parameters.

---

**SirSpudlington** (2025-12-05):

I am starting to like the idea of a fixed-sized system. I feel like the differentiation with key recovery does not have to be explicitly included because algorithms can do that to satisfy the single `verify(signature: Bytes[n], sig_data: Bytes) -> public_key` logic.

The precompile could sensibly:

- Read signature[0]
- Get the size and gas cost
- Check that the data is valid
- Assume the remaining data is sig_data
- …etc

The only concern I have with allowing `sig_data` instead of `Hash32` is that the backwards compatibility of secp256k1 will be broken (unless we check in the secp256k1 algo if the signature data is 32 bytes, if not hash it).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> This presumes the key and signature for each algorithm are fixed width, which NIST appears to be committed to maintain (Falcon’s signature padding is the evidence of this)

I’d assume that since almost all algorithms have a fixed length, it should make sense for all future ones to continue this pattern.

---

Currently adoption for EIP-7932:

- EIP-6404 has native support for the registry (even though SSZ seems unlikely it is good for future compatibility)
- EIP-7932 natively defines the precompile for AA purposes, this may be the most valuable.

I was considering a new version of the wrapper that was more or less:

```auto
TBD byte || EIP-2718 tx
```

The presence of the byte instructs nodes to replace `y_parity`, `r` `v` with `signature`, `0` `0`. Verification can be done with whatever the signing data of the tx is, hashed or otherwise.

This would be in a separate EIP so that EIP-7932 can be implemented without the TX-level logic while keeping the it as an optional bolt-on.

---

**shemnon** (2025-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> The only concern I have with allowing sig_data instead of Hash32 is that the backwards compatibility of secp256k1 will be broken (unless we check in the secp256k1 algo if the signature data is 32 bytes, if not hash it).

For validating EOA transactions I think we should use a 32-byte hash, regardless of the size of the message supported by the underlying DSA. Encourage it for AA transactions too, but they have their own code to do what they want. In the future we may need longer hashes, but I anticipate it will be 5+ years. But with this construction we just use a longer hash.

I expect we will see the pure message signatures for non-transaction messages, such as redemptions or other non-account-transaction uses.

---

**SirSpudlington** (2025-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> For validating EOA transactions I think we should use a 32-byte hash, regardless of the size of the message supported by the underlying DSA. Encourage it for AA transactions too, but they have their own code to do what they want. In the future we may need longer hashes, but I anticipate it will be 5+ years. But with this construction we just use a longer hash.

I agree, this should be for a future migration EIP to handle. Keeping a minimal scope for this EIP makes it more favourable.

Would you have any for handling both datatypes for signature data within the registry? I have a couple thoughts but feel like there is a better way:

- Two functions verify_raw and verify_hash for the registry and some routing logic in the precompile
- Two functions verify_raw and verify_hash for the registry and two precompiles.
- Only support raw data, and have a compatability shim in the secp256k1 algorithm

I prefer the last one as it does add an edge case but keeps things simple.

---

**shemnon** (2025-12-08):

More precompiles equals testing, and more places for clients to introduce bugs and screw things up.  Unless we are brining in SLH-DSA in which has separate domains for pure and hashed messages, I strongly feel we should bring in the cryptography in it’s purest and simplest form, and not hide it behind `verify_raw` and `verify_hash` gatekeepers.

---

**SirSpudlington** (2025-12-08):

This was more or less how I felt. Given that `secp256k1` is not going to be around for long, it would make sense for a small “hash if `len(data) != 32`” shim to be in place.

Anyway, with something like `SLH-DSA` we can define two algorithm types, a pure and a hashed   type.

Does the following interface sound good for *most* algorithms?

```rust
trait AlgorithmEntry {
   // The magic function to actually do the verification
   fn verify(signature: Bytes, signing_data: Bytes) -> Bytes | Error;

   // The complete gas penality, removing the dynamic calculate function
   GAS_COST: uint;

   // The required size of signature data
   SIZE: uint
}
```

---

**shemnon** (2025-12-09):

Gas could be variable if the size is variable, so make gas cost a function.  And making it a function would allow us to tailor fit it to performance, where performance bumps happening at 1/32/48/64 byte barriers due to how the hash works is abstracted away.

But yes.

---

**SirSpudlington** (2025-12-09):

Given that the signature would have a fixed size, I don’t know whether this would actually be warranted….


*(4 more replies not shown)*
