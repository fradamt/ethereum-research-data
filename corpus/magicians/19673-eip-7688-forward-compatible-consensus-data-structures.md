---
source: magicians
topic_id: 19673
title: "EIP-7688: Forward compatible consensus data structures"
author: etan-status
date: "2024-04-15"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7688-forward-compatible-consensus-data-structures/19673
views: 1811
likes: 6
posts_count: 12
---

# EIP-7688: Forward compatible consensus data structures

Discussion thread for [EIP-7688: Forward compatible consensus data structures](https://eips.ethereum.org/EIPS/eip-7688)

# Related

- EIP-7495: EIP-7495: SSZ ProgressiveContainer
- EIP-7916: EIP-7916: SSZ ProgressiveList
- EIP-6493: EIP-6493: SSZ transaction signature scheme

#### Update Log

- 2025-10-02: eip7688: use forward compatible SSZ types in Gloas
- 2025-07-01: Adopt ProgressiveContainer / ProgressiveList

#### Outstanding Issues

- 2025-07-01: Change BeaconBlockHeader to StableContainer?, https://github.com/ethereum/EIPs/pull/9960 → Moved discussion to EIP
- 2024-10-29: Change Validator to StableContainer?, https://ethereum-magicians.org/t/eip-7688-forward-compatible-consensus-data-structures/19673/7 → Moved discussion to EIP

## Replies

**etan-status** (2024-04-17):

Electra would be a good pick for rollout, as a new power of two is reached in number of fields in BeaconState:

- Add EIP-7251 to Electra by ralexstokes · Pull Request #3668 · ethereum/consensus-specs · GitHub

---

**etan-status** (2024-05-15):

Does `DepositReceipt` and `ExecutionLayerWithdrawalRequest` also have to be `StableContainer` or are their schemas immutable across future forks?

---

**etan-status** (2024-05-16):

Updated EIP-7688 to include the latest EIP-7549 PR regarding `Attestation` field order:

- EIP-7549: Append new `committee_bits` field to end of `Attestation` by etan-status · Pull Request #3768 · ethereum/consensus-specs · GitHub

https://github.com/ethereum/EIPs/pull/8567/files

---

**etan-status** (2024-05-30):

Updated the EIP to incorporate planned Electra changes for clarity.

Also documented all the dependent types that would become immutable.

We should consider now whether some of them should become extensible as well (by converting them to `StableContainer`)

https://github.com/ethereum/EIPs/pull/8605/files

---

**etan-status** (2024-07-26):

RocketPool statement related to EIP-7688:

https://nitter.lucabased.xyz/KaneWallmann/status/1816729724145795258

(or, with X login: https://x.com/KaneWallmann/status/1816729724145795258)

---

**wadealexc** (2024-09-23):

Hey, leaving some feedback on this EIP!

I’ve built a few beacon chain proof verifier implementations in Solidity at EigenLayer, so I was initially excited to hear about a stable, forward-compatible merkleization scheme. When a hard fork changes beacon state containers, this almost always means we need to perform a smart contract upgrade to remain compatible - and it would be nice to lessen that load. However, after reviewing EIP-7688, I’m less convinced that this EIP would be useful for us in the short term.

From what it sounds like, a big part of this change involves:

- Making certain type definitions immutable (for example, the Validator container, which we definitely care about)
- Deciding on an upper bound on the capacity of certain types

… and the point of these changes is that if we ever need to, say, add more fields to the `Validator` container, we would need to define a new field outside of the `Validator` container to hold those fields. So I’m picturing a new field in `BeaconState` called `validators_extended` or something, that maps 1:1 with the validators in the standard validators field, but contains the data in these new fields.

If that’s roughly correct, I’d like to point out that the merklization changes we need to make to accommodate forks is actually on the lighter end of fork compatibility efforts. The harder stuff to account for tends to be changes in field semantics — or, changes to how the beacon chain fundamentally runs/processes operations.

---

As an example:

EIP-7251 changes how deposits are applied on the beacon chain by introducing pending balance deposits. Due to this change, processed deposits now register new validators on the beacon chain with a zero balance and create a pending balance deposit, which gets processed once per epoch to credit the deposit amount to the validator’s balance. This means there is now a period of time (>= 1 epoch) when newly-registered validators will have a zero balance.

If I understand EIP-7688 correctly, nothing in these changes would be prevented by forward-compatible merklization. This is introducing some new “pending_x” fields, and changing the semantics of how deposits are applied. However for us, this is actually a fairly annoying change to deal with - because:

1. We’ve been accepting proofs that a validator’s withdrawal credentials are tied to an EigenPod regardless of their current balance
2. We have followup proofs after withdrawal credentials are verified that assume a validator is fully withdrawn if they have a current balance of 0

Merkleization changes, on the other hand, are fairly minor changes to our on-chain/off-chain proofs libraries.

---

So to sum this up — I’m not convinced EIP-7688 would actually help us much, because we’re going to need to make compatibility changes to account for changing beacon chain semantics (regardless of merklization). Fundamentally, changes to the beacon chain spec will end up breaking us in some way, and merkleization specifically is extremely easy to deal with compared to the major semantic changes that tend to come with hard forks.

And if my understanding of 7688 is correct, the way you make changes to beacon chain fields in the future would be significantly more restricted, and possibly messier. I’m picturing something like “ah yes we deprecated `Validator.effective_balance`, you have to use `Validator_Extension.new_effective_balance`, instead, because we’re storing effective balances in wei now” ![:person_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/person_shrugging.png?v=12)

On our end supporting this hypothetical change, it doesn’t matter that the merkleization of `Validator.effective_balance` is unchanged - because we now need to combine our existing `Validator` proofs with a secondary proof to validate this new field in `Validator_Extension`. Ultimately all this would really accomplish for us is doubling the gas cost to verify `Validator`-related proofs.

I would almost rather yall just change the semantics of `Validator.effective_balance` (though I shudder to think how we’d accommodate something like that!)

---

**etan-status** (2024-09-23):

Thanks for the thorough feedback!

Yes, your understanding is correct that with EIP-7688 certain inner types would be considered immutable (they can still be replaced with a new field at a new index), and that list capacities would be fixed at a theoretically viable value (similar to how blob lists are merkleized, with a lower runtime serialization cap), to ensure that the Merkle proof shape remains consistent across forks.

The exact list of immutable containers and capacities could still be refined. The `Validator` container is a natural candidate, as it also contains various epoch numbers that are not necessary to be tracked simultaneously (benefiting from the light-weight `Optional`), which is one of the prime contributors to the `BeaconState` size in memory. However, it needs to be balanced against the number of total hashes necessary to compute the state root. That is the reason why the validator balance already lives in a separate list next to the less dynamic validator configuration.

> I’d like to point out that the merklization changes we need to make to accommodate forks is actually on the lighter end of fork compatibility efforts.

Thanks, this is great to hear and adds a valuable perspective! One aspect to keep in mind, though, is that merkleization changes also have to be implemented by applications and EIP-4788 smart contracts that are not affected by any semantics changes. Not having EIP-7688 represents an ongoing maintenance burden and may be especially tricky when implementing cross-chain bridges across different fork schedules, or when dealing with more immutable designs such as hardware wallets. For EigenLayer, I can see how these concerns mostly don’t apply, but it’s important to look at the concept of `StableContainer` across the broader ecosystem.

As for your EIP-7251 example, for (1) the proof format actually changes with Prague/Electra, despite the general workings of withdrawal credentials not having fundamentally changed (besides the compounding prefix which doesn’t logically belong there to begin with). EIP-7688 would stabilize the proof format so that your smart contract does not need to support both the Dencun and Pectra proof formats (with different length) based on timestamp. For (2), that design seems to have limitations already today, because it is possible to top-up into a fully withdrawn validator and trigger an extra withdrawal that way. You should check for the validator’s state to be ‘Exited’ as well (via the epoch field), in which case the extra initial time with a 0 balance is no longer a special case.

Regarding restrictions, that’s by design. In your example of a Gwei field becoming Wei, the field would change from `uint64` to `uint256` and therefore would have to be assigned to a new gindex). Existing clients could detect when the old field is no longer populated and could gracefully fail, instead of randomly trigger subtle bugs based on incorrect computation, adding extra safety. This is in line with the use of different fields to track the various epoch numbers in the `Validator` structs, even though not all of them are relevant at the same time. Generally, I agree for the `Validator` container, it may make sense to move it from the ‘immutable types’ to the ‘stablecontainer’ section as part of further refinements to the EIP.

As a followup I’d like to ask whether you still see EIP-7688 as generally useful, just with a lower priority, or whether you prefer the current scheme of just having to keep migrating client applications and smart contracts. A Pectra timing provides synergy as it already reindexes the `BeaconState` for other reasons, but based on your post the extra maintenance effort is not significant enough to warrant rushing this into Pectra.

---

**wadealexc** (2024-09-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> EIP-4788 smart contracts that are not affected by any semantics changes

Do you have any examples of contracts that consume EIP-4788 roots to drive core functionality in dapps, but are not impacted by semantic changes on the beacon chain?

I’m not sure who else even uses this oracle - I figured we were probably one of the main consumers.

> For (2), that design seems to have limitations already today, because it is possible to top-up into a fully withdrawn validator and trigger an extra withdrawal that way. You should check for the validator’s state to be ‘Exited’ as well (via the epoch field), in which case the extra initial time with a 0 balance is no longer a special case.

This is fine for us, FWIW. We’re well aware of this edge case and a fully withdrawn validator that gets topped-up after the fact will have no trouble withdrawing from our system with zero proofs required ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Generally this was a very small example, Pectra at large introduces a lot of semantic changes we will need to handle - and semantic changes continue to be the bulk of our ongoing compatibility work!

> As a followup I’d like to ask whether you still see EIP-7688 as generally useful, just with a lower priority, or whether you prefer the current scheme of just having to keep migrating client applications and smart contracts. A Pectra timing provides synergy as it already reindexes the BeaconState for other reasons, but based on your post the extra maintenance effort is not significant enough to warrant rushing this into Pectra.

Thanks for this question. IMO 7688 *is* generally useful! I would just personally not rush this into Pectra. Longer-term, I would be happy to reduce our ongoing beacon chain fork compatibility workload.

In the short term, I feel like (specifically) *smart contract applications* that consume EIP-4788 info to drive on-chain applications are super nascent. On our end, we’ve explored a few different designs and only recently pivoted to a design that we’re quite happy with and utilizes EIP-4788 effectively (and will be generally compatible with Pectra’s various EIPs).

However, I think as the beacon chain spec evolves and more and more 4788-consuming applications are built, I think that both the needs of these applications and the best practices for keeping up to date with beacon chain semantics will become more clear. As it is, we’ve had to figure a good bit of this out by trial and error. I’m guessing anyone else building these applications is feeling the same.

My personal preference is that while this new class of applications is still being figured out that long-term initiatives like 7688 are not as highly prioritized. Later, when this class of apps is more of a solved problem, the path to addressing long-term maintenance of these apps will be more clear.

---

In any case, thanks so much for the thoughtful reply! I appreciate you hearing me out ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**etan-status** (2024-09-26):

> Do you have any examples of contracts that consume EIP-4788 roots to drive core functionality in dapps, but are not impacted by semantic changes on the beacon chain?

1. Decentralized staking pools such as RocketPool use it: x.com – EL triggered withdrawals are interesting for them, but if they use EIP-4788 only to track attestation performance and slashing status to compute smoothing pool rewards, their EIP-4788 functionality does not change semantics in Pectra.
2. Certain researchers use it, for example here to check if a validator got slashed: Slashing Proofoor - On-chain slashed validator proofs - #3 by Nero_eth - Execution Layer Research - Ethereum Research – This is a synthetic example, but once more is EIP-4788 usage with functionality that does not change semantics in Pectra.
3. Future efforts may introduce StableContainer into the EL to support wallets that wish to verify JSON-RPC response data, improving decentralization and censorship resistance as they can use any server to obtain data instead of having to rely on a trusted server with non-ideal data logging policies: https://fusaka-light.box – StableContainer will help provide a streamlined view to client applications that is efficient to verify.

> IMO 7688 is generally useful! I would just personally not rush this into Pectra. Longer-term, I would be happy to reduce our ongoing beacon chain fork compatibility workload.

That’s great to hear. Indeed, Pectra itself is rather large already. However, there is a balance to find to avoid a perpetual low-priority situation, because consuming EIP-4788 is hindered by fork-dependent generalized indices in more advanced cross-chain use cases, built-in mobile phone system frameworks (as part of Android / iOS), or hardware wallets, which all cannot facilitate linking up their release cadence to Ethereum forks.

Lateron, it would also be appreciated to get more finegrained feedback on the classification of individual containers. For example, changing `Validator` may also help reduce `BeaconState` size by dropping information that is no longer needed (e.g., activation epochs for validators that have already exited). There’s hashing overhead though, to mix in the extra bitvector for the stablecontainer (for 1M+ validator entries… at least it’s somewhat cacheable across slots).

---

**etan-status** (2025-07-01):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9960)














####


      `master` ← `etan-status:7688-progressive`




          opened 09:46AM - 01 Jul 25 UTC



          [![](https://avatars.githubusercontent.com/u/89844309?v=4)
            etan-status](https://github.com/etan-status)



          [+102
            -230](https://github.com/ethereum/EIPs/pull/9960/files)







- Adopt latest EIP-7495 changes, the Merkle tree shape is now defined directly i[…](https://github.com/ethereum/EIPs/pull/9960)n the container type.
- Adopt EIP-7916 `ProgressiveList` / `ProgressiveBitlist` to reduce hash count and achieve forward compatibility.












- Adopt latest EIP-7495 changes, the Merkle tree shape is now defined directly in the container type.
- Adopt EIP-7916 ProgressiveList / ProgressiveBitlist to reduce hash count and achieve forward compatibility.

---

**etan-status** (2025-10-02):

Implemented on top of Gloas: [eip7688: use forward compatible SSZ types in Gloas by etan-status · Pull Request #4630 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/4630)

