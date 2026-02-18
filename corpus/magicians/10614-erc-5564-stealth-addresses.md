---
source: magicians
topic_id: 10614
title: ERC-5564 Stealth Addresses
author: Nerolation
date: "2022-08-31"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-5564-stealth-addresses/10614
views: 5553
likes: 15
posts_count: 15
---

# ERC-5564 Stealth Addresses

This thread may coordinate more practical topics regarding the Stealth-Address-EIP and its implementation.

Find the proposal here:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5566)














####


      `master` ← `nerolation:master`




          opened 01:13PM - 31 Aug 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/d/d4f2263996da2d20c2cfa6fa7537c3849f106b12.jpeg)
            nerolation](https://github.com/nerolation)



          [+934
            -0](https://github.com/ethereum/EIPs/pull/5566/files)







Stealth Addresses for Smart Contract Wallets












The discussion on improving privacy through a stealth address standard has already started here:


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 4 Aug 22](https://ethresear.ch/t/erc721-extension-for-zk-snarks/13237)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_500x500.png)



###





          zk-s[nt]arks






Hi community,  I’ve recently been working on this draft that describes zk-SNARK compatible ERC-721 tokens:  https://github.com/Nerolation/EIP-ERC721-zk-SNARK-Extension  Basically every ERC-721 token gets stored on a Stealth Address that constists...



    Reading time: 11 mins 🕑
      Likes: 47 ❤











Based on Vitalik’s input, the design of the current implementation is now much more lightweight than proposed originally.

I’m looking for contributors!

Blog post on the idea [here](https://medium.com/@toni_w/eip-5564-improving-privacy-on-ethereum-through-stealth-address-wallets-fdf3250e81a1).

Find a simple Stealth Address PoC in Python [here](https://github.com/ethereum/EIPs/blob/1ac8a706a8a0da7dc4495b6e0a6e381c444ce262/assets/eip-5564/minimal_poc.ipynb).

Gnosis safe implementation [here](https://github.com/ethereum/EIPs/blob/1ac8a706a8a0da7dc4495b6e0a6e381c444ce262/assets/eip-5564/gnosisSafeModule.sol) (*draft*).

## Replies

**Row** (2023-06-20):

`p_stealth = p + int(Q_hex, 16)`

**p** may exceed the maximum value, get an invalid privateKey. ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

---

**Nerolation** (2023-06-21):

Just take the result modulo the order of the curve like this:

[![Screenshot from 2023-06-21 09-35-28](https://ethereum-magicians.org/uploads/default/optimized/2X/7/721ee5fd8f67e5d4583ee35ceaf75443c02229f5_2_690x209.png)Screenshot from 2023-06-21 09-35-281129×343 51.3 KB](https://ethereum-magicians.org/uploads/default/721ee5fd8f67e5d4583ee35ceaf75443c02229f5)

---

**iAmMichaelConnor** (2023-06-21):

Regarding the `viewTag`, which is proposed to be 1-byte. The ‘Parsing Considerations’ section mentions that there will be false-positive tag matches with probability roughly 1/256.

It got me thinking whether there was a way to reduce the false-positive matches, thereby improving parsing times.

---

Here’s an initial idea that doesn’t work:

*"*

*What if the view tag `v` was the whole hashed secret `s_h = h(s)`? Well, that wouldn’t be good, because broadcasting all of `s_h` to the world will allow someone to do a kind of rainbow attack to derive the stealth public key `P_stealth`. (They could try every registered ‘stealth meta address spend public key’ `P_spend` to compute `P_stealth = P_spend + s_h * G` until they find a non-empty address.*

*"*

So that doesn’t work.

---

But what if we expanded the ‘stealth meta address public keys’ to include another keypair `(p_tag, P_tag)`.

Then the `generateStealthAddress` function would now perform the following computations (copy-pasted from the EIP, **with changes in bold**, and not using LaTeX, because it doesn’t seem to be working for me):

- Generate a random 32-byte entropy ephemeral private key p_eph
- Derive the ephemeral public key P_eph = p_eph * G.
- Parse the public keys from the stealth meta address: P_spend, P_view, P_tag
- A tag is computed as Tag = p_eph * P_tag.
- A shared secret s is computed as s = p_eph * P_view.
- The secret is hashed s_h = h(s)
- Multiply the hashed shared secret with the generator point S_h = s_h * G
- The recipient’s stealth public key is computed as P_stealth = P_spend + S_h
- The recipient’s stealth address a_stealth is computed as pubkeyToAddress(P_stealth)
- The function returns the stealth address a_stealth, the ephemeral public key P_eph and the Tag (note: an x-coordinate and a sign bit, or a hash of the tag could be broadcast to save on broadcasting costs).

The `checkStealthAddress` function would be changed as follows:

- The Tag is derived as Tag = p_tag * P_eph, and can be compared to the published Tag. If the Tag does not match, this Announcement is not for the user and the remaining steps can be skipped. If the tag matches, continue on.
- Shared secret s is computed by multiplying the viewing private key with the ephemeral public key of the announcement s = p_view * P_eph.
- The secret is hashed s_h = h(s).
- Multiply the hashed shared secret with the generator point S_h = s_h * G
- The stealth public key is computed as P_stealth = P_spend + S_h
- The derived stealth address a_stealth is computed as pubkeyToAddress(P_stealth)
- Return true if the stealth address of the announcement matches the derived stealth address, else return false.

---

It seems like the benefits of this approach are:

- No false-positives, because a tag is not just a single byte, so sync times will be faster.

Downsides:

- An extra public key must be registered as part of the ‘meta stealth address’ registration process.
- An extra 32-bytes (ish, depending on the representation of the tag) will need to be published as part of generateStealthAddress.

Edit: An afterthought after writing all this:

I guess a comparison is needed of which is slower: performing the whole `checkStealthAddress` process 1/256th of the time, or downloading an extra 32-bytes of data for every ‘announcement’.

---

I’m unsure whether re-using the same `p_eph` for deriving `P_eph`, `P_tag`, and `s` is a problem. I can’t see a problem with it.

---

**Nerolation** (2023-06-21):

Thanks for the input!

> It got me thinking whether there was a way to reduce the false-positive matches, thereby improving parsing times.

This is a good point and we actually tried having view tags of 32 bytes, then reduced it to 4 and 2 bytes, and eventually arrived at 1 byte just because of the trade-off between *security vs parsing time* **or** *hashing the view tag twice and parsing time*.

One could either hash the view tag twice and use the 32 bytes view tag, resulting in an increased space requirement in the meta data field.

Without hashing it twice, 1 byte the view tag reduces the security margin from 128 bits to 124 bits, which is still ok but we thought we should not go beyond that.

> But what if we expanded the ‘stealth meta address public keys’ to include another keypair (p_tag, P_tag) .

Regarding the additional key pair, this is an interesting thought.

Currently, to derive the view tag, the recipient has to do 1 EC MUL and then hash the shared secret. With the additional key pair, the “heavy” part, the EC MUL, would remain the same but you’d not have to hash it (but the hashing is fast) for deriving the view tag.

I agree that the trade-off with having a longer stealth meta-address might not be worth it. Besides that, it would require 32 bytes of space within the meta data (which could easily be reduced of course).

> The function returns the stealth address a_stealth, the ephemeral public key P_eph and the Tag (note: an x-coordinate and a sign bit, or a hash of the tag could be broadcast to save on broadcasting costs).

If we do the hash of the view tag, we arrive at the current proposed solution.

---

**Mizuki** (2023-06-27):

Currently, I have a question about implementing eip-5564.

I am currently attempting to implement this [EIP-5564](https://eips.ethereum.org/EIPS/eip-5564).

I don’t know if this is correct because EIP’s algorithm is different from your PR [EIPs-PR](https://github.com/ethereum/EIPs/pull/5566/files) .

So my question is

```auto
function computeStealthKey(
  address stealthAddress,
  bytes memory ephemeralPubKey,
  bytes memory spendingKey
) external view returns (bytes memory);
```

As my understanding, this function uses viewing private key as (p_viewing), but there is no p_viewing in arguments.

What is the correct way to handle this?

---

**Nerolation** (2023-06-27):

Please refer to the newest version of the ERC. Many things changes over time such as:

- Introducing view tags
- Introducing 2 keypairs to allow recipients to delegate the parsing
- Introducing a format for the stealth meta-address

ect.

The above url only shows the first, (very) initial draft of the ERC, used for opening it.

You can find the newest version in the [ethereum/eips](https://eips.ethereum.org/EIPS/eip-5564) repo.

Furthermore, I deployed a quick PoC to [stealth-wallet.xyz](https://stealth-wallet.xyz) (together with a tutorial and all the code, in Python and Javascript, necessary to implement it).

Feel free to reach out on telegram (nero_eth) if you have further questions!

---

**Mizuki** (2023-06-27):

Thanks a replying!

Sorry I have read newest version https://eips.ethereum.org/EIPS/eip-5564 as you mentioned…

Currently I’m implementing EIP-5564 using Solidity.

Ok, I will send message on telegram

https://github.com/MizukiSonoko/sample-EIP-5564

---

**kassandra** (2023-09-03):

Hey I looked at the latest version of the EIP on github, but I agree with [@Mizuki](/u/mizuki) it still seems to have an interface that doesn’t make it possible to compute the stealth key (since it requires both the spendingKey and viewingKey to compute, but the interface does not include the viewing key).

Unless I’m missing something all it would take is to update

```auto
function computeStealthKey(
  address stealthAddress,
  bytes memory ephemeralPubKey,
  bytes memory spendingKey
) external view returns (bytes memory);
```

to instead become

```auto
function computeStealthKey(
  address stealthAddress,
  bytes memory ephemeralPubKey,
  bytes memory viewingKey,
  bytes memory spendingKey
) external view returns (bytes memory);
```

This would make it possible to compute the desired output (the stealth address’ private key) from the arguments. Sorry in advance if I’m missing something trivial or still not looking at the latest version (but current master branch on github is still using the interface without a viewingKey argument afaict).

Happy to make a little PR to the EIP if it’s helpful.

---

**iAmMichaelConnor** (2023-09-08):

I’m returning to this (after quite some time), just because I’m thinking about a similar problem for another project. Here’s some (hopefully correct) high-level analysis of three approaches. I’m seeking fast discovery of addresses, over billions (or maybe trillions) of trial attempts, where the cost of performing repeated hashes would be non-negligible. I’m not sure how many trial attempts this EIP expects (will there be thousands / millions / billions of stealth addresses?).

I tweaked the notation to help my brain. I also had to be a little lax with notation, because this forum doesn’t support latex.

(The `.` is a scalar multiplication. Capital letters are points. Lower-case letters are scalars).

**Original approach (1 byte tag)**

`K = k.G` - ethereum keypair.

`V = v.G` - viewing keypair

`E = e.G` - ephemeral keypair. `E` is published.

`S = e.V = v.E` - shared secret

`h = hash(S)` - secret hash

`tag = h.slice(0, 1)` - tag. `tag` is published.

`P = K + h.G` - stealth public key

`stealth_addr = hash(P).slice(-20)`

**Operations to discover a match:**

1 `mul`, 1 `hash` to derive the `tag`. Or `mul + hash` if you’ll forgive the disgusting notation.

False positives will occur roughly once every  `2^8 = 256` trials, on average, due to a collision with the 1-byte tag. With each false-positive, you need to derive the stealth address to be sure you own it, resulting in some extra operations: 1 `mul`, 1 `add`, 1 `hash` to derive the stealth address, and then a check to see whether this address has a nonzero balance.

So the expected discovery time, on average, allowing for false positives, is:

**`mul + hash + (1 / 256) * (mul + add + hash + "an ethereum balance lookup")`**

---

**Double-hash approach**

`K = k.G` - ethereum keypair

`V = v.G` - viewing keypair

`E = e.G` - ephemeral keypair. `E` is published.

`S = e.V = v.E` - shared secret

`h = hash(S)` - secret hash

`tag = hash(h)` - tag. `tag` is published.

`P = K + h.G` - stealth public key

`stealth_addr = hash(P).slice(-20)`

**Operations to discover a match:**

1 `mul`, 2 `hash` to derive the `tag`. Or, if you’ll again forgive the disgusting notation:

**`mul + 2 * hash`**

False positives are infeasible.

---

**Tag keypair approach**

`K = k.G` - ethereum keypair

`V = v.G` - viewing keypair

`T = t.G` - tagging keypair

`E = e.G` - ephemeral keypair. `E` is published.

`tag = (e.T).serialise() = (t.E).serialise()` - tag. `tag` is published. `serialise()` takes the x-coord and the sign, to compress the tag.

`S = e.V = v.E` - shared secret

`h = hash(S)` - secret hash

`P = K + h.G` - stealth public key

`stealth_addr = hash(P).slice(-20)`

**Operations to discover a match:**

1 `mul` to derive the `tag`. Or, if you’ll again forgive the disgusting notation:

**`mul`**

False positives are infeasible.

---

I don’t have concrete figures for the relative speeds of `mul`, `hash` and `add`. Nor do I know how many stealth addresses are expected to exist. If it’s only thousands of addresses, then the asymptotics aren’t worth exploring. If it’s billions, then they probably are.

---

**iAmMichaelConnor** (2023-09-08):

Aside (and continuing to use my notation): why is the stealth address public key derived as `P = K + hash(S).G` instead of `P = K + S`?

Edit: it’s because the recipient can’t derive the secret key to `P` if you use `S`, because the recipient doesn’t know the ephemeral private key `e`.

---

**ChanHongMing** (2024-03-07):

According to Vitalik in [the original post](https://ethresear.ch/t/erc721-extension-for-zk-snarks/13237), “The reason why this needs to be standardized is that the sender needs the ability to automatically generate an address belonging to the recipient without contacting the recipient.”.

May I know how the sender suppose to get recipient’s *stealthMetaAddress* for *generateStealthAddress*? I originally thought that sender could generate an address belonging to the recipient using its EOA address. If we leave the implementation of this unspecified, what is the difference between using this EIP and the recipient generate a new ethereum address then find their own way to tell the sender.

---

**Nerolation** (2024-03-08):

The stealth meta-address can be published and from the stealth meta-address the sender can generate unlimited number of stealth addresses that cannot be linked back to the recipient and its stealth meta-address.

One could directly use the public key of the recipient but then the sender wouldn’t be sure if the recipient is actually looking for stealth addresses that belong to it for a certain stealth address protocol.

Therefore, I’d argue, stealth addresses require standardization in order to enable sender and recipeint to exchange information about the used stealth address protocol without creating a public link between the two parties.

---

**Nerolation** (2024-04-26):

The hashing is done to convert the EC Point (=DH Secret) to a scalar used similar to a private key in consecutive steps.

I agree that it could be done without the hashing but since the hashing is super fast and compared to the EC MUL negligible.

There are some benchmarks in the paper we wrote alongside the ERC:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/5/56228dc9bce6fab77f462bbf701fd30f0e8e96c1.png)

      [ieeexplore.ieee.org](https://ieeexplore.ieee.org/document/10426757)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/4/47cb9a978206bcfb9e636d25ca7ff9612f0d99a2.png)

###



Stealth addresses represent an approach to enhancing privacy within public and distributed blockchains, such as Ethereum and Bitcoin. Stealth address protocols employ a distinct, randomly generated address for the recipient, thereby concealing...










The hashing is around 220x faster than the ec mul.

---

**eawosika** (2024-12-04):

Hi all! We ([2077 Research](https://research.2077.xyz/)) published a deep dive on ERC-5564 for those interested in learning how the stealth address protocol works under the hood: [ERC-5564 &amp; ERC-6358: Unlocking Privacy on Ethereum with Stealth Addresses](https://research.2077.xyz/erc-5564-erc-6358-unlocking-privacy-on-ethereum-with-stealth-addresses). All feedback and comments are welcome.

