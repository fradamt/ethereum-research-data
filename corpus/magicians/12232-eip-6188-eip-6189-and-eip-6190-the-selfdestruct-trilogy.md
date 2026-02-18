---
source: magicians
topic_id: 12232
title: "EIP-6188, EIP-6189, and EIP-6190: The SELFDESTRUCT trilogy"
author: Pandapip1
date: "2022-12-20"
category: EIPs > EIPs core
tags: [evm, opcodes, cancun-candidate]
url: https://ethereum-magicians.org/t/eip-6188-eip-6189-and-eip-6190-the-selfdestruct-trilogy/12232
views: 2936
likes: 3
posts_count: 17
---

# EIP-6188, EIP-6189, and EIP-6190: The SELFDESTRUCT trilogy

This is the discussion link for EIP-6188, EIP-6189, **and** EIP-6190.

The goal of these EIPs is to modify `SELFDESTRUCT` in a mostly non-breaking manner to support Verkle trees and to limit the number of changes that are to be performed.

## Replies

**Pandapip1** (2022-12-20):

First thing’s first: why three EIPs?

It’s because I want them to be usable independently of each other. It’s quite possible that EIPs (i.e. I am planning on making EIPs that) can use the magic value of EIP-6188 and don’t necessarily need the selfdestruct stuff.

Likewise, there could be a selfdestruct-like thing that would find EIP-6189 very useful, even if EIP-6190 isn’t implemented.

---

**SamWilsn** (2022-12-21):

EIP-6188’s behaviour with CREATE and CREATE2 is inconsistent with [EIP-2681](https://eips.ethereum.org/EIPS/eip-2681). The former allows the creation to proceed, but the latter does not.

---

**SamWilsn** (2022-12-21):

Where does the `25` extra gas per hop come from? I’d expect it to cost at least as much as a call plus a storage read.

---

**SamWilsn** (2022-12-21):

I think there’s an interesting attack here that needs some math to estimate. How much would it cost to get a self-destructed contract “close enough” to a not-yet-CREATE2’d contract to be able to use its storage?

---

**Pandapip1** (2022-12-21):

25 gas *in addition to* the EIP-2929 costs.

---

**Pandapip1** (2022-12-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I think there’s an interesting attack here that needs some math to estimate. How much would it cost to get a self-destructed contract “close enough” to a not-yet-CREATE2’d contract to be able to use its storage?

Not sure. But I’m not sure how it would let it “use” its storage, if it simply forwards calls (after all, if it hasn’t been CREATE2’d yet, then it can’t really be called, so its storage can’t be modified this way).

---

**SamWilsn** (2022-12-25):

What I’m imagining is: an attacker computes where the target contract will be deployed with `CREATE2`. Then they brute force where to deploy their malicious contract using The Price is Right rules (close but less than the target contract’s eventual address.) Then the malicious contract self-destructs multiple times to close the gap, eventually ending up where the target contract would’ve been deployed.

---

**Pandapip1** (2022-12-25):

> Then the malicious contract self-destructs multiple times to close the gap, eventually ending up where the target contract would’ve been deployed.

… causing the `CREATE2` to either succeed, deploying the contract at a different address that the original address points to, or causing the `CREATE2` to fail. I don’t see an issue here.

---

**SamWilsn** (2022-12-26):

I could transfer ownership of a token to an address that hasn’t been created yet (perhaps I don’t want to reveal the implementation, or don’t want to pay for the deployment until I need to transfer the token again.) Someone could deploy other code to the same address.

---

**Pandapip1** (2022-12-26):

Fair enough. I’ll calculate that.

---

**Pandapip1** (2022-12-26):

As more and more contracts get selfdestructed sequentially, the gas cost for each selfdestruct increases linearly. So this attack will take polynomial gas as the number of hops increases.

Okay, so assuming that the attacker is willing to spend $E$ ether, with a gas price of $G$, then an upper bound for the maximum number of hops $n$ that the attacker can perform (ignoring the cost of creating the contracts and calling the function that selfdestructs) is given by:

$$\frac{10^9E}{G}=\frac{5000n(n+1)}{2}+\frac{100(n-1)n}{2}+2600n$$

Solving for the positive value of $n$:

$$n = \frac{1}{102}\frac{\sqrt{10201 G + 4080000000 E}}{\sqrt{G} - 101}$$

So using 100 ether with a gas cost of 20, the attacker could perform a maximum of 1,399 hops. Not counting the cost of deploying the contracts. But even the implausible 1,400x risk of an address collision is still safe due to the minuscule probabilities involved.

---

**Pandapip1** (2023-01-05):

[@SamWilsn](/u/samwilsn) do you have any other comments/concerns?

---

**SamWilsn** (2023-01-06):

This is good content for the Security Considerations section.

---

**SamWilsn** (2023-01-06):

> The gas cost of SELFDESTRUCT is increased by 5000 for each alias contract that forwarded to the contract being self-destructed.

How is this calculated? Assume there are contracts at `0x5` and `0x6`, then if I self-destruct the contract at `0x5`, `0x5` becomes an alias contract for `0x7`, correct? I then perform a `CREATE2` and redeploy the contract at `0x5` (now stored at `0x7`.) Finally I call the contract at `0x7` directly and cause it to self-destruct.

I don’t think this is functionally a problem since the next call into `0x5` will update the storage slot, but it does make me question:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> As more and more contracts get selfdestructed sequentially, the gas cost for each selfdestruct increases linearly.

---

**Pandapip1** (2023-01-07):

Now that I think of it - why don’t I just point it to the contract that would be `CREATE`’d? This would avoid all of these issues by using something we already know to be secure.

---

**Pandapip1** (2023-01-11):

Adding [cancun-candidate](https://ethereum-magicians.org/t/cancun-eip-consideration/12060/5) tag.

