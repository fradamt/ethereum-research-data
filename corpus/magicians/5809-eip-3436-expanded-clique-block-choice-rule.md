---
source: magicians
topic_id: 5809
title: "EIP-3436: Expanded Clique Block Choice Rule"
author: shemnon
date: "2021-03-26"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-3436-expanded-clique-block-choice-rule/5809
views: 3001
likes: 3
posts_count: 9
---

# EIP-3436: Expanded Clique Block Choice Rule

In early March we had a couple of deadlocks on the Goerli network. These resulted from clients observing competing out of order blocks and settling on different equally preferred chain head blocks.  This EIP proposes a block choice rule that should be deterministic regardless of when the blocks were observed.  I have weak opinions as to what the particular rules should be, so if you have better ideas feel free to propose.  But I have a strong opinion that first observed should not be one of the rules as that is not deterministic across nodes and is what caused the deadlock.

https://github.com/ethereum/EIPs/pull/3436

## Replies

**shemnon** (2021-03-29):

[@karalabe](/u/karalabe) can I get your take?

---

**meowsbits** (2021-04-23):

Hey [@shemnon](/u/shemnon). I’m working on implementing this at etclabscore/core-geth.

I ran into an issue with the second *Rationale > Scenario* defined in the spec. It seems that the second fork `2,4,6` is invalid, since signer `6`'s block will be rejected for having signed too recently.

Below I’m using zero-indexed block signer order indexes, so `7` is really `8`

On that fork, the sequence of signers is described to be `... 7, 0, 1, 2, 3, 4, 5, 6, 1, 3, 5`. This supposes that the latest fork block from signer `5` (zero-index name for signer `6`) is 4 blocks from their last block on the common segment. With 8 signers and a `SIGNER_LIMIT` of `8/2+1` from EIP-225 this causes that latest fork block to be invalid (`5>4`).

Maybe I’ve got something wrong? Or misunderstood the scenario?


      [github.com](https://github.com/etclabscore/core-geth/blob/358a532375b217a9dfddbba5039c9714779c0a3f/consensus/clique/clique_test.go#L273-L292)




####

```go

1. FIXME(meowsbits): This scenario yields a "recently signed" error
2. when attempting to import Signer 5 (really #6 b/c zero-indexing) into the
3. second fork.
4. On that fork, the sequence of signers is specified to be
5. ... 7, 0, 1, 2, 3, 4, 5, 6, 1, 3, 5
6. (vs. the other fork)
7. ... 7, 0, 1, 2, 3, 4, 5, 6, 0, 2, 4
8. The condition for "recently signed" is (from *Clique#verifySeal):
9. // Signer is among recents, only fail if the current block doesn't shift it out
10. if limit := uint64(len(snap.Signers)/2 + 1); seen > number-limit {
11. return errRecentlySigned
12. }
13. Evaluated, this yields
14. => recently signed: limit=(8/2+1)=5 seen=13 number=17 number-limit=12

```

---

**shemnon** (2021-04-23):

Yea, the even length halt scenario isn’t as clean as I hoped.

Here’s a revised one.  8 nodes, zero based.  0-6 all produce in-order blocks, then a netsplit. 0, 2, and 3 on the first fork and 1, 4, 6, 7 on the second fork, and 5 goes offline.  7, 0, and 1 all missed an important in-turn block.

How does this scenario sound?

> 0, 1, 2, 3, 4, 5, 6,
>
>
> fork 1 - 0, 3, 2.
>
> Possible next: 1, 4, 5, 7
> On this fork: 0, 2, 3
>
>
> fork 2 - 1, 7, 4.
>
> Possible next: 0, 2, 3, 5
> On this fork: 1, 4, 6, 7
>
>
> Offline after split: 5

Do we prefer fork 1 or fork 2?  I don’t have a strong opinion but IMHO it should be calculated strictly based on what is in the tested block, not on the eligible next blocks nor on the prior blocks, and not depend on knowledge of the forks other validators are on.

---

**holiman** (2021-05-07):

> Then choose the block whose validator had the least recent in-turn block assignment.
> Then choose the block with the lowest hash.

As for those rules… Rule number `3` means that determining whether to reorg is not really bounded. If it were 7 signers, only 5 were active, and chugged through `10M` blocks. And suddenly number 6,7 pops up, and constructs a block each. Then we’d have to go through `10M` blocks while searching for the ‘least recent’.

I guess I don’t see why we don’t just skip `3`, and go directly to `4`  and compare hashes ? That seems like the ultimate tie-breaker, and it’s highly ‘localized’ and cheap to perform.

---

**shemnon** (2021-05-07):

Least recent may not be the best wording.  The specification of the EIP describes what that means, and it does not imply a 10M block lookback, just calculating data within the header and knowing what the full set of validators is:

> When resolving rule 3 clients should use the following formula, where validator_index is the integer index of the validator that signed the block when sorted as per epoch checkpointing, header_number is the number of the header, and validator_count is the count of the current validators. Clients should choose the block with the largest value. Note that an in-turn block is considered to be the most recent in-turn block.
>
>
>
> ```auto
> (header_number - validator_index) % validator_count
> ```

We could skip 3 and go to 4 but that turns it into a PoW race when trying to censor the chain. With rule 3 in place you are only ever in a PoW race with yourself.

---

**tlqcore** (2023-03-22):

Hello I would like to reopen [EIP-3436: Expanded Clique Block Choice Rule · Issue #300 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/300) or better understand why it was closed without being implemented.

We are using a modified clique consensus for our [Q blockchain](https://q.org/). We would like to implement deterministic fork choice as proposed. We can do it in our client (derived from geth) only, but

1. we prefer to change it in geth as contribution, but also for peer review purpose
2. also, the rationale for not doing the proposed changed is not available. Maybe we overlook something, but deterministic fork choice appears very desireable

---

**shemnon** (2023-03-23):

The rationale for not doing the proposed changes within context of Ethereum Mainnet was mootness, all the testnets that used clique were being transitioned to PoS, so within the scope of Mainnet there were no more networks using the protocol.

What is needed is developers outside of Mainnet willing to get the Geth code changed to support the EIP.  However, upstreaming the changes may prove difficult as the Geth maintainers have publicly expressed an interest in removing code not actively used for Mainnet.

---

**tlqcore** (2023-03-28):

I see, thanks for the info. At least it seems there was no technical concern. I think, we’ll then do the implementation in our client. I’ll keep the community here updated, so geth maintainers can still choose to use our solution.

