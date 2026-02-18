---
source: ethresearch
topic_id: 10021
title: "0x03 Withdrawal Credentials: Simple Eth1-triggerable withdrawals"
author: gakonst
date: "2021-07-07"
category: The Merge
tags: []
url: https://ethresear.ch/t/0x03-withdrawal-credentials-simple-eth1-triggerable-withdrawals/10021
views: 9416
likes: 39
posts_count: 18
---

# 0x03 Withdrawal Credentials: Simple Eth1-triggerable withdrawals

Post co-authored with [@lsankar4033](/u/lsankar4033)

*(note: 0x03 picked to disambiguate from [WIP 0x02 credential PR](https://github.com/ethereum/eth2.0-specs/pull/2454))*

**Context**:

- Currently, in order for a validator to be ejected, they need to manually trigger it via a voluntary exit
- However, in cases such as staking pools, the owner of the funds being staked is not necessarily the validator. The validator has an opportunity to hold the owner’s funds hostage
- We could get around this if there was a way for a smart contract to trigger voluntary exits and know that an exit has happened
- This proposal outlines a way to implement this:

‘Exit’ contract whose events are read by eth2 clients (similar to the Deposit Contract)
- Exposing the beacon state root to the eth1 engine so that the EVM knows whether a validator has been activated yet (by providing a merkle proof)

**Approach**

We designate a canonical contract in eth1, the ExitContract, that looks like [this gist](https://gist.github.com/lsankar4033/5c118c99e8ca53ba2e7952414a7c1ae0).

Anyone can call the withdrawal method with a message originating from the specified credentials and a validator pubkey.

The Beacon chain clients listen for events from this contract and executes the following actions:

1. Looks up the withdrawal credential corresponding to the specified validator pubkey
2. Checks if:

the credential matches the one emitted by the event
3. The specified validator is active

If it does not, the algorithm terminates and is effectively a no-op.
Initiate the logic for a [VoluntaryExit](https://github.com/ethereum/eth2.0-specs/blob/378d167ee03a4017b53dc54cac15a99ea4392313/specs/phase0/beacon-chain.md#voluntaryexit) for the validator

In an ideal world, we’d also like the Ethereum chain to be able to assess whether a validator is active or not. This would allow smart contracts interacting with the ExitContract to provide additional ‘safety checks’ to their users, so that they can avoid getting in the no-op case by accident.

Strawman Example:

1. User burns 32 stETH expecting to reclaim 32 ETH once the corresponding validator is exited
2. The calling contract issues a message to the ExitContract specifying (by accident) a validator that isn’t active yet
3. The emitted event does not cause the VoluntaryExit, since it falls in the 2b) case mentioned above, and gets interpreted as a no-op
4. The user does not receive any ETH since no validator is exited

To combat that, we could expose a BEACONROOT opcode at the EVM which would operate similar to the BLOCKHASH code. This would allow consumers of the BEACONROOT to be able to prove that a validator is active in the Beacon State. In the above example, the user would also provide a merkle proof showing that the chosen validator is active at the time the exit request is processed.

**Next Steps**

- Enshrining an ExitContract in Eth1 similar to the DepositContract
- Implementing the event processing logic in Eth2 clients, similarly to how they process validator entry events via the DepositContract
- Adding the BEACONROOT opcode at the EVM level
- Investigate the above protocol’s soundness / DoS vectors etc.

We acknowledge that these are changes which SHOULD NOT be prioritized before The Merge. But we also believe it’s worth having the discussion from now, so we can prioritize accordingly for when we’ll enable withdrawals after The Merge.

## Replies

**djrtwo** (2021-07-07):

## Consider extending 0x01

I think something similar to this functionality can/should be added to 0x01 creds. Although you can probably come up with a degenerate case in which a set of actors was relying on 0x01 creds to not be able to exit, such a case is unlikely to be in production and adding functionality to the *ultimate owner* of the funds is natural.

## Active validator verifiability is critical to avoid DOS on beacon chain operations

Because emitting such messages is essentially free (just the cost of a TX) and because the beacon chain would then be forced to process all such messages, it is a **requirement** that this contract/state can not only track who has submitted exits already but also be able to prove that a validator is in fact *active*. A requirement, rather than a nice ‘safety check’ for users. You need to restrict it such than only an active validator without an exit_epoch already set is able to submit these messages and only to be able to submit them a maximum of one time to avoid the DOS on the beacon chain.

## Discussion of beacon opcode choices should happen in parallel to these feature discussions

This could be handled via the `BEACONROOT`  opcode as mentioned, but given we expect upgrades to the beacon state root structure, a more direct opcode is potentially favorable (otherwise, the exit contract would have to be upgraded at any hardfork that modified the beacon state in a meaningful way to proving validator activeness). I expect a minimum of `BEACONROOT` to be exposed, but more direct opcodes (e.g. `VALIDATOR(index) -> validator`) should be considered when discussing beacon <-> execution interactions.

---

**gakonst** (2021-07-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> I think something similar to this functionality can/should be added to 0x01 creds

Yes - no disagreement. My assumption was that the functionality of credentials was not to be mutated, but if possible, let’s do it there.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Because emitting such messages is essentially free (just the cost of a TX) and because the beacon chain would then be forced to process all such messages

I assumed that L1 messages are not “free”, hence thought that the tx fee would be enough of a rate limiter. Agree we’d want some form of DoS protection if that assumption is false.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> I expect a minimum of BEACONROOT to be exposed, but more direct opcodes (e.g. VALIDATOR(index) -> validator) should be considered when discussing beacon ↔ execution interactions.

Also agree that there’s a lot of creative ways we can expose beacon state to Ethereum, just suggested the Beacon Root as the most “minimal” way / least invasive way to do it.

---

**djrtwo** (2021-07-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> My assumption was that the functionality of credentials was not to be mutated, but if possible, let’s do it there.

I think that the discussion should at least happen. If we can’t demonstrate a degenerate case on mainnet, my preference would be to extend 0x01 capabilities.

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> I assumed that L1 messages are not “free”, hence thought that the tx fee would be enough of a rate limiter.

Maybe not “free” but at least easy to fill and asymmetric compared to the restriction on beacon block operations

- Assuming we can add roughly the same amount of Exits as there are Deposits on the beacon chain – that’s 16 per block.
- Now assume that an Exit costs roughly the same gas in the contract as a Deposit does today – ~50k gas.
- Thus a single, non-validator actor can cram ~300 invalid Exits into a single execution layer (eth1) payload and prevent any honest Exits for happening for at least 18 slots. Or at least make them much slower on average.

There is a cost here in ETH tx fees but it doesn’t seem like the correct way to evaluate the cost of an attacker being able to grief core actions of the validator set that are only meaningfully taken by validators.

It’s not a DOS in terms of the chain grinding to a halt. Although I haven’t gone into a detailed analysis of all things an attacker could do here with capital available, it does seem like an attacker should not be able to *pay* to prevent honest exits.

---

**lsankar4033** (2021-07-07):

Definitely agree the free-ness of ‘exit’ messages create DoS surface for clients. An earlier version of this proposal involved verifying a signature in the Exit contract to make sure creds were being exited by a party authorized to exit them and only once for any cred/pubkey pair. This improves things somewhat, but is not possible in the case where the cred eth1 address is a contract; no way to create a contract signature.

IMO this is the part of the proposal that needs the most thinking/iteration. The path seems clearer for the rest

And ya, just extending 0x01 is almost certainly the thing to do if we reach agreement!

---

**zilm** (2021-07-08):

I’d require it’s signed with withdrawal key and signature is verified on-chain in Eth1.

And it’s not the first case which could be useful for users and when we are stuck with loss of `0x00` key. It would be very useful to have both BLS withdrawal key and withdrawal credentials for validators, where key is a master signature for changing credentials and initiate withdrawal actions.

---

**vshvsh** (2021-07-08):

I think it should not be a specialized `Exit` contract, but a generic `MessageBeaconChain` contract, where  the semantics of the message are only parsed on beacon chain side.

If spam is a consideration even with tx fees, one can hook up an additional eth-burning to the contract (e.g. you have to send 0.001 ETH for message to be passed on the beacon chain side).

---

**lsankar4033** (2021-07-08):

Hmm, interesting idea to generalize the message bus. What messages other than {deposit,exit} do you foresee being interesting here?

---

**Kazuya1987** (2021-07-08):

I’m a community member of Shared Stake. Our eth2 staking protocol has ~16K underlying ether and one of our main devs – the one holding the eth2 staking validating keys – has rugged us (to keep it succinct). Our Veth2 eth2 keys are currently held only by him. In our community we have been wanting a solution like this implemented ASAP because of what’s at stake (potentially losing 16k+ Eth to a rogue dev who has ownership of the keys and not being able to fully trust his actions moving forward). As it stands the dev seems willing to share the keys → allow a solution like this to emerge. I post this just to let you know this really matters to a bunch of people (hundreds who were staking with Veth2/Shared Stake with tens of millions of dollars behind them) and hope researchers can work + collaborate/talk with the white hat devs left on our protocol on a solution that will allow us to safely secure our funds at the merge.

---

**mkalinin** (2021-07-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> ## Discussion of beacon opcode choices should happen in parallel to these feature discussions
>
>
>
> This could be handled via the BEACONROOT opcode as mentioned, but given we expect upgrades to the beacon state root structure, a more direct opcode is potentially favorable (otherwise, the exit contract would have to be upgraded at any hardfork that modified the beacon state in a meaningful way to proving validator activeness). I expect a minimum of BEACONROOT to be exposed, but more direct opcodes (e.g. VALIDATOR(index) -> validator) should be considered when discussing beacon ↔ execution interactions.

One of potential ways to abstract state layout is to expose host functions or precompiles that verify the proof linking validator, shard data commitments or any other pieces of beacon state to the state root, e.g. `verify_validator_proof(proof: bytes)`. Commitment scheme and state layout updates will cause this function to be updated with no requirement on changing existing applications.

---

**vshvsh** (2021-07-09):

Off the top of my head:

- credential rotation
- “skimming” rewards from a validator without full withdrawal and redeposit

---

**vshvsh** (2021-07-09):

Speaking as a tech guy from liquid staking protocol, we likely wouldn’t have any use for individual proofs about validator states. We’ve got thousands of them, it’s too expensive to process them one by one.

What we’ll do is probably make a zk proof over some aggregate function over beacon state, so we would only need `BEACONROOT`, and the rest would be handled by ZK cryptography.

---

**lsankar4033** (2021-07-09):

thanks for your message! had followed the shared stake situation loosely and hope that we can use some of the ideas here to ameliorate the problem(s). if you think it’s helpful to connect the threads with any of the whitehat devs in that community, feel free to connect me on telegram: @paperun

---

**samueldashadrach** (2021-07-09):

Very cool proposal!

Just wanted to add one point to this discussion. Namely that the cost of griefing - be it via DOS on eth2 or censorship bribes on eth1 needs to only be comparable to the time duration required to get the ETH slashed with incorrect attestations.

There isn’t much benefit for a pool operator to bleed funds and censor forever. What can, however, make sense is to spend a small amount of funds and censor just long enough to get the 32 ETH slashed.

This will be part of the larger “pay me 16 ETH ransom for honest 32 ETH withdrawal” attack which is possible in status quo.

---

**mkalinin** (2021-07-12):

Potentially such host functions may be able to verify multiple validator entries at once given multi proof. It would add complexity to the gas formula of the function but looks feasible to do. This verification is about to be enshrined in system contract that burns receipt, emits required amount of ETH and sends it to withdrawal address. What place do you think ZK circuit can be put at?

---

**alonmuroch** (2021-07-15):

maybe in the future some withdraw excess ETH msg?

---

**alonmuroch** (2021-07-15):

I like this direction, makes a lot of sense to have contract control exit as well.

I do think if we keep adding specialized cases (prefixes) it will confuse people, add attack vectors and will complicate potential “migration” between those prefixes.

Might be worth while thinking about a more generic solution (like the message bus mentioned) where different “extensions” can be added and DOS could be mitigated via fee.

---

**vshvsh** (2021-08-09):

We need to get sum of 20k of validators in a smart contract once per day. That’s a very rough estimation but I think it will cost about 2B gas if done via merkle root verificatio, which is obviously unfeasible.

