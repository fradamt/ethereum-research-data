---
source: magicians
topic_id: 3157
title: Blake2b F precompile
author: tvanepps
date: "2019-04-18"
category: EIPs
tags: [precompile]
url: https://ethereum-magicians.org/t/blake2b-f-precompile/3157
views: 5262
likes: 16
posts_count: 22
---

# Blake2b F precompile

(Written by [@virgil](/u/virgil) ) Special Projects wishes greater Ethereum interopability with Zcash, IPFS, and Handshake. Coincidentally, all of these projects use the Blake2 hash function. So, this is our official request to add the [Blake2b  F  precompile](https://github.com/ethereum/EIPs/issues/152) to the Istanbul hardfork. The first special project here will probably be creating a wrapped ZEC (WZEC) within Ethereum as well as wrapped Ether within Zcash. After that, some yet-to-be-determined bridge architecture will allow Ethereum to benefit from Zcash’s shielded transactions.

If there’s an issue of funding to get this over the finish line, I will personally cover the expenses.

That’s it really. Send questions to [virgil@ethereum.org](mailto:virgil@ethereum.org).

## Replies

**virgil** (2019-04-27):

Sounds right to me.  Let me know if there’s anything I can do to push this forward.

---

**tvanepps** (2019-04-27):

for anyone checking in this effort would be superseded by the [EIP 1829](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1829.md) precompile

edit: I was mistaken, thinking of another EIP mentioned on the CoreDevs Call

---

**AlexeyAkhunov** (2019-04-27):

I am not an expert, but I thought that Blake2b is a hash function, and it is not based on elliptic curve arithmetics and pairings, so I would say no.

---

**virgil** (2019-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> for anyone checking in this effort would be superseded by the EIP 1829  precompile

This is mistaken. The Blake2 precompile is not superseded by EIP 1829. You’re thinking of EIP 665 (another precompile that has come up), which is superseded by EIP 1829. As far as I know, the current proposal is to put Blake2 into Istanbul and EIP1829 to be considered once it’s ready.

---

**AlexeyAkhunov** (2019-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/virgil/48/327_2.png) virgil:

> As far as I know, the current proposal is to put Blake2 into Istanbul

Yes, with a caveat - if someone takes on the work of implementing it, benchmarking, figuring out the gas cost formula, generating tests, etc.

---

**souptacular** (2019-05-01):

Below is an email I sent to Zooko after he showed interest in reviving the EIP. I think it sums up the general current process that a champion would need to go through to make this EIP a reality. It also has relevant links to previous attempts at the EIP:

> A champion of an EIP is the someone who writes, creates tests for, and advocates for the EIP. Advocating for the EIP may involve attending an All Core Dev meeting that happens every other Friday. A champion doesn’t neccessarily implement the code entirely into every client, but they do list implementation examples in different languages at minimum.
>
>
> When you previously tried to revive this in late 2017 Jay Graber contributed to the EIP that Tjaden Hess created in 2016. They made some good progress on the EIP, but there are some pieces missing such as the full spec, Ethereum test cases, and gas calculations. It also isn’t up to standard with the latest EIP formats. We will likely just use that thread (PR #131) to continue iterating on the EIP. Would Jay like to still be involved in this?
>
>
> I am posting this message to a thread on the Fellowship of Ethereum Magicians, where EIP and other technical discussions take place. Here are some relevant links:
>
>
> An issue in the EIP repo that brought up initial discussion, including comments from you. It is no longer a place to put comments since we have the Fellow of Ethereum Magicians Forum: BLAKE2b `F` Compression Function Precompile · Issue #152 · ethereum/EIPs · GitHub
> The EIP (#131) PR that the actual EIP is being written in. This is where changes to it will happen: Draft BLAKE2b precompile EIP by tjade273 · Pull Request #131 · ethereum/EIPs · GitHub
> Fellowship of Ethereum Magicians Forum: Blake2b F precompile
>
>
> I think that IPFS and Handshake and other projects also require BLAKE2b so I think this would be a cool opportunity to get them involved too so it won’t be entirely on the back of ZCash and a few people to get this done.
>
>
> In short, head to the Fellow of Ethereum Magicians forum post I linked to with any questions you have and we can get this going  Anyone from your team who is going to help with this should coordinate on that forum unless it becomes a big enough group that a Gitter chat room is neccessary (which I can set up if needed).
>
>
> Note: We have a deadline for EIPs accepted for our next hard fork in August. That deadline is the end of May so you will only have 1 month or so to complete the EIP if you want it in the next hard fork. Otherwise the one after would be 4-6 months from August most likely.
>
>
> Thanks!

---

**cdetrio** (2019-05-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> (Written by @virgil ) Special Projects wishes greater Ethereum interopability with Zcash, IPFS, and Handshake. Coincidentally, all of these projects use the Blake2 hash function.

New records are being set for doing Blake2b in EVM with the minimum amount of gas:

[added basic cli for huff by zac-williamson · Pull Request #61 · AztecProtocol/aztec-v1 · GitHub](https://github.com/AztecProtocol/AZTEC/pull/61/commits/5754a9087535ffc9201656c98b0b24c4bd26a265) - 512 equihash rounds in ~8,259,212 gas

[added basic cli for huff by zac-williamson · Pull Request #61 · AztecProtocol/aztec-v1 · GitHub](https://github.com/AztecProtocol/AZTEC/pull/61/commits/40e768d94e7d8e89c7eb851f99fca4233117c388) - 512 equihash rounds in ~7,061,173 gas

To justify the necessity of a new precompile, example inputs and outputs of desired use cases (for Zcash, IPFS, and Handshake) should be provided. Then an effort should be made to optimize an EVM implementation that processes the example inputs and outputs, and to analyze the computational bottleneck. The analysis should argue that the optimized implementation requires too much gas to compute the desired outputs, and that further optimizations of the EVM implementation are unlikely.

Also note that gas costs of computational EVM opcodes (as opposed to I/O opcodes such as SLOAD and SSTORE) are highly overpriced at present, for two reasons.

The first reason is because the block gas limit (currently at 8 million gas) simultaneously meters the computational workload and the I/O workload of each block. And under the current opcode gas cost table, 8 million gas of I/O workload already results in an uncomfortably fast rate of state growth. But the computational capacity of the average client is under-utilized. If state growth can be curtailed (e.g. by repricing SSTORE), then a strong case could be made arguing that miners should raise the block gas limit. Alternatively, rather than repricing SSTORE higher and raising the block gas limit, the block gas limit could stay the same and computational opcodes could be repriced lower. Either way would effectively lower the cost of computation and use cases that are currently just out of reach (e.g. 2x or 3x beyond the block gas limit) would become practical in EVM contracts, using the average client today.

Second, even after a repricing of computational workloads relative to what average clients could process today, it should be possible to achieve a significant amount of further reductions. An optimized EVM engine (such as [evmone](https://github.com/chfast/evmone) or [cita-vm](https://github.com/cryptape/cita-vm)) is about 5x or 10x faster than the EVM implementations in the average client (geth and parity) today. If opcodes were repriced according to the speed of an optimized implementation, even more reductions in the gas cost table could be realized.

---

**boris** (2019-05-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> If opcodes were repriced according to the speed of an optimized implementation, even more reductions in the gas cost table could be realized.

Totally agree. We can make Geth and Parity implementations faster today, or use EVMC to link to an optimized EVM.

I’m assuming [@shemnon](/u/shemnon) can poke the Pantheon folks about this too.

---

**shemnon** (2019-05-03):

We would likely pick apart the bouncycastle implementation and figure out where Function F lives, like I did for Keccak f800.  Their license is BSD like.  They also focus on performance and some of their optimizations are unique to Java’s architecture.

---

**zac-williamson** (2019-05-05):

Hi all!

I just wanted to follow up on [@cdetrio](/u/cdetrio)’s post. I’ve been tinkering around with writing a Blake2b smart contract that can execute 512 compression rounds within the block gas limit.

[The contract is written in Huff](https://github.com/AztecProtocol/AZTEC/blob/feat-huff-truffle-integration-ho-ho-ho/packages/weierstrudel/huff_modules/blake2b.huff), and my latest iteration clocks in at ~6,821,545 gas for 512 rounds. I don’t think I’ll be able to get it much lower than that.

As [@cdetrio](/u/cdetrio) mentioned, an optimized EVM engine can run the contract at a reasonable clip. I benchmarked the blake2b contract in [evmone](https://github.com/chfast/evmone/pull/11) and, for 512 rounds, obtained a run-time of 7.062ms . At 6,821,545 gas, `evmone` will process the algorithm at a rate of 968,000,000 gas per second.

As a thought experiment, if opcodes were priced relative to an EVM engine like `evmone`, with a target of 10,000,000 gas per second, the blake2b contract would consume 70,470 gas for 512 rounds, or 138 gas per round.

With each round compressing 128 bytes, that’s ~34 gas per word, which seems pretty reasonable.

---

**boris** (2019-05-05):

Great, thanks for the report Zac. Would be good to use this as the basis for benchmarks in other clients.

---

**MadeofTin** (2019-05-13):

I submitted an updated PR. I can be PoC for the EIP until developers are decided and funded. I wanted to make sure it at least has a chance of getting into Istanbul by doing some of the legwork. https://github.com/ethereum/EIPs/pull/2024

If developers can’t be sourced and funded in time then it will have to wait for the next train.

---

**axic** (2019-05-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/madeoftin/48/1969_2.png) MadeofTin:

> I submitted an updated PR. I can be PoC for the EIP until developers are decided and funded. I wanted to make sure it at least has a chance of getting into Istanbul by doing some of the legwork. https://github.com/ethereum/EIPs/pull/2024

The pull request contains the following `Specification` section:

```auto
Function accepts a variable length input interpreted as:

    [OUTSIZE, D_1, D_2, ..., D_INSIZE]

where `INSIZE` is the length in bytes of the input. Throws if `OUTSIZE` is greater than 64. Returns the `OUTSIZE`-byte BLAKE2b digest, as defined in [RFC 7693](https://tools.ietf.org/html/rfc7693).
```

This description seems rather ambiguous. Is that array a byte array? Is `OUTSIZE` a single byte (uint8)? Does that mean `INSIZE` is the length of input and the first byte of the input is considered as `OUTSIZE` while the rest is the actual input to hash?

And the following gas costs:

```auto
Gas costs would be equal to `GBLAKEBASE + GBLAKEWORD * floor(INSIZE / 32)`
```

If `INSIZE` includes the configuration parameter of output hash size (`OUTSIZE`) shouldn’t this calculation be Gblakebase + Gblakeword + floor((INSIZE - 1) / 32)?

---

Additionally, and older version of the blake2b proposal had a more complex interface exposing a wider feature set of Blake2 and allowing for a more flexible precompile. The issue description of [BLAKE2b `F` Compression Function Precompile · Issue #152 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/152) still has that interface. I’m not sure which option is better, but perhaps we need to weigh which use cases the current precompile proposal can solve compared to the flexible design.

---

**MadeofTin** (2019-05-19):

We are in the process of refactoring tjade273 ‘s go-ethereum implementation into a more recent version. That part of the spec will stay a bit ambiguous for now as we:

1. figure out why he choose those design principles
2. figure out if those are good reasons
3. decide if we should change the spec accordingly
4. benchmark, benchmark, benchmark

I imagine the spec he wrote and the actual code he wrote aren’t in sync either, so there is much to flesh out on this front.

Maybe I should take out the spec portion until we have a better defense for it? Or, at least mark it as WIP.

I’ll gather feedback on where in the spectrum of flexible and optimized we should target. (I don’t know if this is the trade-off we have yet but usually it is something like this). [@virgil](/u/virgil) it would be great to hear from your team as you already have in mind implementaions for it.

After collecting a list of planned uses and possible use cases we can use that to narrow down the intersection of features and requirements.

---

**virgil** (2019-05-19):

It’s starting to look unlikely that this will be ready by Istanbul.  That’s fine—zooko and I both had trouble acting on this quickly. This remains an ask, but it’s fine if it doesn’t go into Istanbul.

---

**MadeofTin** (2019-05-20):

Yes, if I was going to give us an Istanbul inclusion rating it would be rated “low”, but we still have a few weeks before that is really decided.

We are going to do our darn’dest and see how it goes. I’m not going to cry if we don’t get in, but it is still worth the effort. A lot of work has already been done we can piggy back on.

---

**MadeofTin** (2019-05-23):

Adding this feedback on the specification here so it would not be lost in a merge.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/c/c69b938122c5719378ee7452ce42d7e13392b4a3.png)image663×271 17.7 KB](https://ethereum-magicians.org/uploads/default/c69b938122c5719378ee7452ce42d7e13392b4a3)

---

**holiman** (2019-06-24):

I made some comments on the EIP PR and the PR to the geth-fork, but I’ll sum it up here aswell, for completeness.

- I think the EIP needs to specify what the expected input length is,
- And what happens if input is smaller than that (either consider everything to be zeroes, or raise an error)
- And how to treat the padding data. Does it need to be zeroes, or should an implementation just ignore it?
- There should be testcases containing junk-filled padding as well as too-short input.

Also, I’d like the `specification`-part of the EIP to be more terse, and not motivational. Only the technical details, but as much detail as possible.

---

**axic** (2019-08-26):

Anyone wondering where is the current discussion happening about the precompile, please see:

- the EIP here: https://eips.ethereum.org/EIPS/eip-152
- the discussion URL here: https://github.com/ethereum/EIPS/issues/152

---

**axic** (2019-08-30):

I have added three change proposals for the precompile [here](https://github.com/ethereum/EIPs/issues/152#issuecomment-526610735) and [here](https://github.com/ethereum/EIPs/issues/152#issuecomment-526645573).


*(1 more replies not shown)*
