---
source: magicians
topic_id: 12060
title: Cancun Network Upgrade Meta Thread
author: timbeiko
date: "2022-12-08"
category: Magicians > Process Improvement
tags: [cancun-candidate]
url: https://ethereum-magicians.org/t/cancun-network-upgrade-meta-thread/12060
views: 12105
likes: 53
posts_count: 26
---

# Cancun Network Upgrade Meta Thread

## Cancun Network Upgrade Meta Thread

On ACDE#153, we agreed to try out [Network Upgrade Meta Threads](https://ethereum-magicians.org/t/proposal-network-upgrade-meta-threads/12552) for Cancun.

Instead of creating a new thread, we can repurpose this one given there were already some comments here. We can use this to discuss things like:

- What should be the main priority/priorities for the upgrade;
- When, roughly, should we aim for the upgrade to happen, and the tradeoffs of including a marginal feature vs. delaying;
- How to split multi-upgrade features across >1 upgrade, and the implications of including a subset of those features in a specific upgrade

### Included EIPs (June 12, 2023):

On [ACDE#163](https://github.com/ethereum/pm/issues/786), the scope of the Cancun upgrade was finalized. The list of included EIPs can be found in [cancun.md](https://github.com/ethereum/execution-specs/blob/master/network-upgrades/mainnet-upgrades/cancun.md#included-eips):

> EIP-1153: Transient storage opcodes
> EIP-4788: Beacon block root in the EVM
> EIP-4844: Shard Blob Transactions
> EIP-5656: MCOPY - Memory copying instruction
> EIP-6780: SELFDESTRUCT only in same transaction

### EIP proposals (May 24, 2023):

**
Click to expand**

EIPs with a ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15) are formally included for Cancun. EIPs with a ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=15) are being considered for inclusion by client teams. EIPs with a ![:x:](https://ethereum-magicians.org/images/emoji/twitter/x.png?v=15) have been rejected by teams for this upgrade. These are tracked in the [Cancun spec](https://github.com/ethereum/execution-specs/blob/master/network-upgrades/mainnet-upgrades/cancun.md#included-eips). In case of differences between what’s listed here and in the spec, the spec is right.

#### Proposed EIPs list

- EIP-4844
- SELFDESTRUCT removal

EIP-6780
- EIP-4758
- EIP-6046
- EIP-6190

[EIP-5920](https://eips.ethereum.org/EIPS/eip-5920)
[EIP-1153](https://ethereum-magicians.org/t/shanghai-cancun-candidate-eip-1153-transient-storage/10784) ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15)
[EIP-2537](https://ethereum-magicians.org/t/eip-2537-bls12-precompile-discussion-thread/4187)  ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=15)
[EIP-4788](https://ethereum-magicians.org/t/eip-4788-beacon-root-in-evm/8281) ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=15)
EVMMAX EIPs

- EIP-6601
- EIP-6690

SSZ changes:

- EIP-6475
- EIP-6493 SSZ signature scheme
- EIP-6465 withdrawals_root
- EIP-6404 / EIP-6466 transactions_root + withdrawals_root

[EIP-5656: MCOPY - Memory copying instruction](https://eips.ethereum.org/EIPS/eip-5656)
[EIP-6193: SETCODE](https://ethereum-magicians.org/t/eip-6913-setcode-instruction/13898)

**
EOF changes ❌**

- EIP-663
- EIP-3540: EVM Object Format (EOF) v1
- EIP-3670: EOF - Code Validation
- EIP-4200: EOF - Static relative jumps
- EIP-4750: EOF - Functions
- EIP-5450: EOF - Stack Validation

**Note: EIP champions who’d like to propose their EIP for Cancun should add the [cancun-candidate](https://ethereum-magicians.org/tag/cancun-candidate) tag to a post about the EIP on this forum.**

---

## Original Post (Dec '22)

**
Click to expand**

Similarly to [what we did for Shanghai](https://ethereum-magicians.org/t/shanghai-core-eip-consideration/10777), I propose using this thread to discuss how we should go about choosing EIPs for the post-Shanghai EL upgrade, [Cancun](https://github.com/ethereum/execution-specs/pull/663).

At the very least, EIPs which wish to be considered for the upgrade should add the `cancun-candidate` to either their existing EthMagicians topics, or create a new one focused on Cancun consideration.

For context, please refer to [AllCoreDevs 151](https://github.com/ethereum/pm/issues/675). Here is a summary posted to the [R&D discord](https://discord.com/channels/595666850260713488/745077610685661265/1050440218739753141):

[![Screenshot 2022-12-08 at 9.50.34 AM](https://ethereum-magicians.org/uploads/default/optimized/2X/2/28af77fee1097274ec169e6e946ca4d3fd2b543f_2_690x367.png)Screenshot 2022-12-08 at 9.50.34 AM1740×926 225 KB](https://ethereum-magicians.org/uploads/default/28af77fee1097274ec169e6e946ca4d3fd2b543f)

and a [relevant Cancun comment](https://discord.com/channels/595666850260713488/745077610685661265/1050449884542681198) by [@protolambda](/u/protolambda):

[![Screenshot 2022-12-08 at 9.51.07 AM](https://ethereum-magicians.org/uploads/default/optimized/2X/6/615c8833538644f2c335cec223379054816e45ad_2_690x151.png)Screenshot 2022-12-08 at 9.51.07 AM1670×366 79.6 KB](https://ethereum-magicians.org/uploads/default/615c8833538644f2c335cec223379054816e45ad)

And here were some proposals shared on in the ACDE agenda comments:

- EthereumJS Shanghai/Cancun Proposal
- @protolambda Shanghai/Cancun Proposal

## Replies

**axic** (2022-12-08):

I’d like to raise that perhaps the discussions around `SELFDESTRUCT` may benefit from a revival. There are two bigger proposals on the topic: [EIP-4758](https://ethereum-magicians.org/t/eip-4758-deactivate-selfdestruct/8710) and [EIP-6046](https://ethereum-magicians.org/t/almost-self-destructing-selfdestruct-deactivate/11886).

A [new analysis](https://hackmd.io/X-waAY49SrW9i36SKOVuGQ) was shared lately by [@jwasinger](/u/jwasinger).

---

**leonardoalt** (2022-12-08):

Solidity would like to propose [EIP-663](https://ethereum-magicians.org/t/eip-663-unlimited-swap-and-dup-instructions/3346) for Cancun. It has been [EFI before in 2019-2020](https://github.com/ethereum/pm/blob/master/AllCoreDevs-Meetings/Meeting%2079.md), dependent on immediate arguments. EOF provides that trivially, so it’s fair to say that with EOF 663’s issues become resolved. It’s supported by Solidity, Vyper and Huff, the main direct users of 663. I need to check with Fe as well, but I don’t think they’d be against because they currently compile to Yul which would benefit from this. With 663:

- All languages can save gas by not moving local variables to memory when they don’t fit on the reachable part of the stack anymore.
- Solidity specifically can cut a big chunk of its roadmap short. The item of “solving stack-too-deep errors”, which include complex optimizers and transformations would simply be done. This also benefits any other language that wishes to optimize local variables by always keeping them on the stack. This consequently brings security advantages by avoiding complex compiler behavior.

If EOF goes in Shanghai, I don’t think it would be possible to add 663 as well.

If EOF goes in Cancun, I think there would be time to add 663 as well given the time until then and how simple it is.

---

**Pandapip1** (2023-01-08):

I would like to propose [EIP-5920: PAY opcode](https://eips.ethereum.org/EIPS/eip-5920). I won’t provide a motivation here, since you can just read [the motivation section of the EIP itself](https://eips.ethereum.org/EIPS/eip-5920#motivation).

---

**Pandapip1** (2023-01-08):

In relation to the selfdestruct stuff, I would like to propose [EIP-6190](https://eips.ethereum.org/EIPS/eip-6190) as a non-breaking selfdestruct solution.

---

**non-fungible-nelson** (2023-01-19):

Thanks for creating this Tim. Some opinions my own and some the Besu team’s:

- Priorities should be EOF and 4844, (and whatever consensus we reach on SELFDESTRUCT). The EIP grab-bag approach from Shanghai, while useful, should be limited if we can. There are often many details that come up during the implementation phase and I think it would be best to avoid creep on this already large fork.
- I think the progress on 4844 in the workshop should drive a timeline. We initially dubbed this a fast-follow fork, which sounds like early 2H. With Shanghai, timelines are dictated by our need to ship withdrawals. While we can accumulate some tech-debt in Shanghai for withdrawals as we have a chance to correct it in Cancun, more pervasive protocol changes in 4844 and EOF will be quickly enshrined tools, langs, and live contracts. To this end, delays are more prudent than shipping “something,” especially with EOF and EVM version requiring support in clients and languages.
- I have no preference on this - protocol schedules are flexible. We can ship code that lives dormant for a while on Mainnet while we iron it out elsewhere. Weakly in favor of ship often, test often approach.

Matt

---

**moodysalem** (2023-01-20):

I’d like to propose EIP-1153 for inclusion in Cancun. I’ve updated the [candidate thread](https://ethereum-magicians.org/t/shanghai-cancun-candidate-eip-1153-transient-storage/10784) with the latest status. Further progress on EIP-1153 is blocked by marking it for inclusion, allowing it to be part of devnets and giving client developers a reason to finish code reviews and merge the outstanding PRs.

And some meta commentary: the main reason EIP-1153 is not in Shanghai is that EOF was added in December and removed a month later. I think this is a failure of prioritization that deserves more discussion. I’d suggest this time around not committing to anything else (other than EIP-4844) for which the spec is not finalized, and EOF is still figuring out parts of the spec (e.g. just a week ago DELEGATECALL into legacy code was brought up).

---

**abcoathup** (2023-01-20):

To increase Layer 2 adoption we need lower cost transactions, hence the need for EIP4844.

**Shapella** was focused on withdra**OWL**s ![:owl:](https://ethereum-magicians.org/images/emoji/twitter/owl.png?v=15).

**Dencun (Cancun + Deneb)** should focus on blobspace ![:blowfish:](https://ethereum-magicians.org/images/emoji/twitter/blowfish.png?v=15).

The timeline for Cancun should be based on EIP4844 readiness. e.g. May/June.

Any additional EIPs should have finalized specs and not add significant delay (e.g. more that 1-2 months) to the delivery of Cancun, otherwise they should be candidates for inclusion in the Prague upgrade later in 2023 or early 2024.

## EIPs to add to Cancun in addition to EIP4844

*Assume finalized EIP spec and EIPs don’t add significant delay to delivery of Cancun.*

- EIP1153: Transient storage opcodes
- EIP2537: Precompile for BLS12-381 curve operations
- EOF
- Other (reply with details)

0
voters

---

**Pandapip1** (2023-01-20):

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5920)





###



Introduces a new opcode, PAY, to send ether to an address without calling any of its functions










It’s simple and the spec is basically finalized. There’s a PR to add it to nethermind: [Add EIP-5920 by Pandapip1 · Pull Request #5166 · NethermindEth/nethermind · GitHub](https://github.com/NethermindEth/nethermind/pull/5166)

---

**hilmarx** (2023-01-28):

EIP2537 or a new implementation for a BLS precompile would be great in order to make it easier for decentralized off-chain networks Lido or Gelato to utilize BLS for threshold signatures.

---

**ralexstokes** (2023-02-23):

EIP-4788 keeps coming up and I think would be a relatively small change that unlocks a lot of benefits so should be CFI in Cancun.

It would also be nice to unlock some kind of BLS arithmetic in Cancun, either via EIP-2537 or something like EVMMax (which requires EOF AIUI).

---

**jwasinger** (2023-02-26):

For reference, the latest proposal for EVMMAX is documented in the EIP-5843 [discussion thread](https://ethereum-magicians.org/t/eip-5843-evm-modular-arithmetic-extensions/12425).

A new spec is being prepared which addresses issues identified in 5843.

---

**etan-status** (2023-03-02):

- EIP-6493 SSZ signature scheme
- EIP-6465 withdrawals_root
- EIP-6404 / EIP-6466 transactions_root + withdrawals_root

These would be great to have in Cancun, still being designed though, specs not final.


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/y1MCA5Q-R4eMVyOBHiRH7Q)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###

---

**timbeiko** (2023-04-13):

On [ACDE159](https://github.com/ethereum/pm/issues/754), we agreed to discuss potential Cancun EIPs on the next call, scheduled for [April 27, 14 UTC](https://github.com/ethereum/pm/issues/759).

I’ll keep track of EIPs proposed for the upgrade in the first post of this thread. If you’d like to propose an EIP and it’s not part of the list, please reach out to me. You can add the `cancun-candidate` tag as well to make it easy for people to see all proposed EIPs’ threads on a single page here ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**shemnon** (2023-04-17):

Can we move EIP-663 into the EOF group?  The current revision of the spec depends on immediate arguments, which is only viable in an EOF container.

---

**LukaszRozmej** (2023-04-18):

Nethermind internal core dev discussions go this way in terms of priorities, what is deliverable, size, state of implementation:

1. Cancun:

- Yes: 4844, 6780, 1153
- Maybe but more yes: 2537, 4788
- Maybe but more no: 5920

1. Next post-cancun hardfork: SSZ, EOF, EVMMAX
2. Next-next post-cancun hardfork: Verkle

---

**timbeiko** (2023-04-18):

Moved the EIP, [@shemnon](/u/shemnon)! And thanks for sharing [@LukaszRozmej](/u/lukaszrozmej)  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**jflo** (2023-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> EIP-6466

This one claims to depend on 6475, which introduces Optionals to the SSZ spec.

---

**wjmelements** (2023-04-25):

If `SELFDESTRUCT` is broken such that it can no-longer remove code (eg via EIP-6780), I want to include EIP-6913 (`SETCODE`) to preserve code mutability.

---

**etan-status** (2023-04-27):

The minimal parts for Cancun should be EIP-6493 SSZ signature scheme, and EIP-6475 SSZ Optional definition. Not deciding on how these should look for Cancun makes it difficult to change in the future.

EIP-6465 and EIP-6404 / EIP-6466 can be addressed later, the overhead is same whether done in Cancun or in E-Fork.

---

**charles-cooper** (2023-04-27):

I’d like to propose inclusion of [EIP 5656 (MCOPY)](https://eips.ethereum.org/EIPS/eip-5656) in Cancun. I don’t think there is any contention about the spec or its usefulness, it’s easy to understand and implement, it would enable better codegen for batch memory copies in compilers, and it already has an [open PR to implement in geth](https://github.com/ethereum/go-ethereum/pull/26181).


*(5 more replies not shown)*
