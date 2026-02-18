---
source: magicians
topic_id: 1151
title: "EIP-1352: Restricted address range for precompiles/system contracts"
author: axic
date: "2018-08-24"
category: EIPs
tags: [precompile, eip-1352]
url: https://ethereum-magicians.org/t/eip-1352-restricted-address-range-for-precompiles-system-contracts/1151
views: 6707
likes: 20
posts_count: 29
---

# EIP-1352: Restricted address range for precompiles/system contracts

This topic is intended be the discussion for EIP-1352. Any comment or feedback is very much appreciated!

https://eips.ethereum.org/EIPS/eip-1352

## Replies

**axic** (2018-09-04):

Due to multiple suggestions, extended the reserved range from 256 to 65536 addresses: 00…0000 to 00…ffff is reserved.

[Prior to that I had an idea to split the reserved the range into two parts](https://github.com/ethereum/EIPs/pull/1352#discussion_r214357159). Changed that numbers to reflect the new expanded reserved range:

- 0x0 to 0xffff for precompiles
- 0x10000 to 0x1ffff for “system contracts”, which have code in the state (e.g. blockhash refactoring or (the now obsolete) casper contract).

---

**carver** (2019-04-26):

Since [@boris](/u/boris) mentioned on the call that EEA wants to use this space for custom precompile slots, maybe the EIP should advise that non-mainnet precompiles should start from `0xFFFF` and iterate down. If they just pick a random slot in the space, they could end up with conflicts when they try to import later mainnet forks to their sidechains.

---

**boris** (2019-04-26):

I have passed this on. Thanks!

---

**chaals** (2019-04-30):

EIP-1352 reserves a block of address space for precompiles. However, there is no apparent mechanism to register that anyone intends to use (or is already using) part of that space.

This means that if say a private network client wants to use a given address for a function it implements, primarily serving one network, it will have to either flag the precompile by network or check everything else it connects to in case there is a different precompile at the same address.

I  **think**  the expectation is that precompiles would normally be useful across a lot of different networks (this would seem especially the case for e.g. EEA clients), so it seems to me that it would be useful to actually be able to register addresses in this space…

The idea is that at a minimum people claim an address. In most of the cases I can think of, there is no real reason to hide what is happening there, and if for example the EEA wants to mandate a new precompile across multiple EEA clients, it would be a benefit to be able to state where it is and what it does.

---

**axic** (2019-04-30):

I have briefly thought about this, but figured that private chains would not want to reveal themselves to allocate specific numbers.

Allocating a specific range for some external body which could govern it may be a good middle ground?

---

**boris** (2019-04-30):

Yep, this sounds like it would work for the EEAs purposes at least. But more generally, allow any bodies or chains to get some address space allocated.

Much like we just list chainids at https://chainid.network without “controlling” them per se, this would in part just be informative.

---

**chaals** (2019-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Yep, this sounds like it would work for the EEAs purposes at least. But more generally, allow any bodies or chains to get some address space allocated.

Indeed, it would work fine for EEA. The question is whether it leads to people requesting lots of blocks they don’t need, in which case we might be better with a system where you request addresses as you use them.

I don’t have a strong opinion either way at this stage, but look forward to hearing arguments.

---

**shemnon** (2019-04-30):

So we should think of the precompile address space like port number allocations for TCP/IP?

---

**zoenolan** (2019-04-30):

I was thinking managing the precompile space could work along the lines of the [OpenGL extension registry](https://www.khronos.org/registry/OpenGL/index_gl.php). Addresses are allocated and have a specification attached.

From an old [blog post](https://medium.com/clearmatics/extending-the-evm-d386d858729d)

> OpenGL (a cross-platform, low-level graphic library controlled by the Khronos group) offers a useful precedent on how this can be managed. OpenGL has included an extension mechanism since the mid 1990’s: a registry is managed by the Architecture Review Board (ARB) where any member of the ARB can propose an extension (which if accepted) is allocated a number in the registry). Different classes of extension exist: single vendor; EXT for older generic or multiple vendor extensions; and ARB for more modern extensions supported by a number of vendors.

---

**zoenolan** (2019-05-02):

and just to make things more explicit. If i was writing that blog post today. I would suggest the EVM evolution working group as the natural home for the registry

---

**expede** (2019-05-02):

Would they, though? The address space is enormous. If you, say, hash the binary, or the name of the pro-compile + the deployer’s name (or something along these lines), you get a deterministic address that is unlikely to conflict, no?

---

**chaals** (2019-05-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/expede/48/4738_2.png) expede:

> If you, say, hash the binary, or the name of the pro-compile + the deployer’s name (or something along these lines), you get a deterministic address that is unlikely to conflict, no?

hashing the binary is nice because you don’t expect a different binary to be able to conflict. If you add names, then it becomes easier to create a conflict which seems less helpful.

But precompiles that do the same thing might actually have a different binary across different clients (or even not be actual precompiles, but plain smart contracts), no?

---

**shemnon** (2019-05-03):

What I like about a reserved range instead of a hash of whatever is that code analysis tools or manual inspection can easily identify what is a precompile contract.

Some of these contracts will in essence become “system calls” that can do things regular EVM cannot do, such as a lot of things EEA finds precompiles interesting to do.  So that would present a different attack surface, and audits/tools would want to know when the attack surface grows.

---

**zac-williamson** (2019-05-04):

Would it be within the scope of this EIP to also define how much gas is used when the `CALL`, `CALLCODE`, `DELEGATECALL` and `STATICCALL` opcodes are used to call contracts within the precompile address range?

It seems like, if a precompile address range is defined at the protocol level, we have the opportunity to more formally define the semantics of calling these precompiles.

Right now, the `700` gas cost of the call opcodes is to reflect the time required to fetch these contracts from disk, but this is not relevant for precompiles. For some precompiles, this `700` cost is a substantial overhead (e.g. `ECADD` only costs 500 gas, but the actual cost is `1,200` because of this).

A gas cost of `50` might be more suitable? (or even `0`? the time taken to run the pre-compile should be factored into its gas formula, no?).

---

**chfast** (2019-05-09):

Can you change the title to “EIP 1352: Restricted address range for precompiles/system contracts”?

---

**tjayrush** (2019-05-14):

I scanned all the addresses below and including `0xffff`, and found none with code nor any with a non-zero nonce. I did find, however, that these addresses have ether balances totaling 12,517.53127 eth (that’s around 2.5 million dollars US). 99.5% of that is in a single account (0x000…dead).

The core devs should make a donation of this money to the MolachDAO on behalf of the entire community. While the money is already locked and lost, it feels wasted otherwise (especially in an underfunded open source community).

I understand that burning money is a way to increase the value of the coin, and that’s a totally valid position. I also understand that this idea is a very slippery slope. That point of view is also totally valid.

But, It costs nothing to share an idea, and I had this one, and I didn’t really need it anymore, so I thought I’d give it away for free.

---

**axic** (2019-05-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> 99.5% of that is in a single account (0x000…dead).

IIRC this address is used by ENS as a burn address. [@Arachnid](/u/arachnid) is that correct?

---

**Arachnid** (2019-05-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> IIRC this address is used by ENS as a burn address. @Arachnid is that correct?

That’s correct.

![:unicorn:](https://ethereum-magicians.org/images/emoji/twitter/unicorn.png?v=12) to meet length requirements.

---

**jochem-brouwer** (2019-05-19):

> Due to the extremely low probability (and lack of adequate testing possibilities) no explicit checks should be added to ensure that external transaction signing or the invoking of the  CREATE  instruction can result in a precompile address.

Of course the probability is extremely low, but if this happens we will all be confused which chain has the right chain if there is one chain which overwrites the precompile and another chain which uses the precompile at this address. If this happens, then the chance is very high that we get a consensus issue. I propose that in any case a new contract is created (e.g. call to `null`, `CREATE` or `CREATE2` in a smart contract) code is not deployed in the same way as you try to deploy code using `CREATE2` when re-using the same seed.

---

**holiman** (2019-05-24):

These are the points I raised at the allcoredev-call today…

It’s currently possible to configure a genesis with code at arbitrary addresses. For example, to place a faucet at `0x00...0010`.

So if we accept 1352, then implement some other EIP which makes calls to precompiles cheaper, the question is of calls to `0x00...10` should, or should not, be included in that (I think they shouldn’t be, since they are stored on disk like any other code, whereas ‘true’ precompiles are already in-memory)


*(8 more replies not shown)*
