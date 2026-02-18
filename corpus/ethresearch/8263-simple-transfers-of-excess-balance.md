---
source: ethresearch
topic_id: 8263
title: Simple Transfers of Excess Balance
author: jgm
date: "2020-11-24"
category: The Merge
tags: []
url: https://ethresear.ch/t/simple-transfers-of-excess-balance/8263
views: 6265
likes: 11
posts_count: 34
---

# Simple Transfers of Excess Balance

With the proposal for withdrawal methods by [@djrtwo](/u/djrtwo)  it raises an issue that this would result in users being able to do an “exit-withdraw-deposit” loop to move “excess” balance from a validator (excess being anything over MAX_EFFECTIVE_BALANCE).  Any significant level of validator churn to serve this purpose would be both annoying for users, as the activation and exit queues would have a baseline level of business, and the network, as it has to both process exits and activations, and retain exited validator state.

An alternative is to allow validators to transfer their excess balance without exiting.  Some sort of “transfer” operation would be the obvious way to go, but it could inadvertently creating an arbitrary value transfer system on the beacon chain.  Ideally, a way would be found to enable this functionality without requiring additional operations.

The proposal is to allow validators to transfer excess balance at the point they propose a block.  This makes the transfer an inherent part of the block proposal, using existing security and limiting the number of transfers that can take place.  The only data impact is an additional 8 bytes per beacon block.

## Beacon chain changes

- add transfer_index: ValidatorIndex to BeaconBlock / BeaconBlockHeader

## Process

- if a validator wishes to transfer its excess balance it sets the beacon block’s transfer_index field to the index of the validator to which it wants to transfer
- as part of process_block_headers:

if transfer_index is set then any balance over MAX_EFFECTIVE_BALANCE is transferred from the proposing validator to the validator specified by transfer_index as long as both of the following conditions are met:
- len(state.validators) > blocks.transfer_index
- state.validators[block.transfer_index].activation_eligibility_epoch == FAR_FUTURE_EPOCH

## Wrinkles

Because `transfer_index` is a validator index `0` is a valid value,  there is not an obvious “no index” value. `0xff..ff` could be used for this purpose, or `0` could continue to be used as validator 0 will not meet the second condition above (at least, for mainnet).  Use of a `BLSPubKey` for the `transfer` field would be an alternative, but that would increase both storage and CPU requirements.

## Replies

**moles** (2020-11-25):

For this feature to work without breaking trustless staking pools, it might be necessary for the validator to sign a message using their withdrawal key? Perhaps this could be a beacon chain operation which is limited to 1 per block and can only be signed by the block proposer?

---

**alonmuroch** (2020-11-25):

If the withdrawal credentials are set to an eth1 address than it’s not a simple signature but an actual tx.

---

**alonmuroch** (2020-11-25):

[@jgm](/u/jgm) what if an eth1 is specified?

---

**technocrypto** (2020-11-25):

[@jgm](/u/jgm) perhaps a better approach here than transferring to another validator would be to just set a single bit in the proposal, which would then dump the excess funds via the normal withdrawal process?  Users who (once withdrawals are enabled or at least defined) want to continually withdraw their earnings could then just leave that bit permanently set, which seems appropriate and useful.  Yes, anyone looking to re-invest in new validators would need to then take the withdrawn funds and deposit into the beacon chain again, but this is far less churn than if they had to withdraw their entire validator balance (i.e. for average earnings of 32/n ETH per validator this would eliminate n wasted “churn” behaviours for every 1 validator which actually needed to be redeposited).

---

**jgm** (2020-11-25):

The target is a validator index, and it accrues to that validator.  All on Ethereum 2.

---

**jgm** (2020-11-25):

That may be possible, but does depend on the overall weight of the withdrawal process as it moves from Ethereum 2 to Ethereum 1.  If it’s a relatively heavy process (in terms of data stored, time taken to action the withdrawal, *etc*) then that may not be suitable.

The benefit of this being purely on the beacon chain is that it means that it all happens with a relatively minor adjustment of the existing spec.  Making withdrawals a prerequisite is a dependency I’d rather avoid.

---

**jgm** (2020-11-25):

[@moles](/u/moles) Perhaps I’m not up on how trustless staking pools are meant to work, but I assume that there is some sort of mechanism in place to ensure that the validator doesn’t cause a purposeful slashing event.  For example, the validator key could be broken across 3 participants and 2 of them need to agree on the operation for it to be valid.  However that is done, the same process could apply to the block proposal that contains the transfer index.

---

**technocrypto** (2020-11-25):

I think that since there is moderate urgency around developing at least a basic withdrawal specification it makes sense to consider these problems together.  I mentioned this thread in the other topic about withdrawal specifications, and I think that using each as a test case for the other proposal is probably useful.

---

**moles** (2020-11-25):

I suppose there are a number of possible architectures. Rocket Pool specifically just pools “regular user” ETH (deposited by people who want to earn rewards but not run a node) together and assigns it to queued validators in 16 ETH chunks. The people running nodes have complete control of their validator key, no splitting is required.

For our use case - we considered an approach like the one you suggested but ultimately decided to use simple economic incentives instead (node operators are bonded by having to deposit 16 ETH per validator, and penalties are taken out of their share first). If validator keys are suddenly able to transfer balance, having to split them between multiple validators in order to mitigate this introduces a lot of complexity we could do without. E.g. we would need to implement a minimum validator threshold which needs to be met before keys are aggregated pseudo-randomly (much like the beacon chain architecture) in order to prevent cartels from forming and taking control of funds.

Personally, would much prefer that any operation which has the ability to transfer balance is limited to withdrawal keys only.

---

**technocrypto** (2020-11-26):

Yeah, I think the clear social consensus right now is that withdrawal keys are in total control of all funds, while validator keys cannot assign funds anywhere.  That’s another reason to just trigger the normal withdrawal process, because I don’t think we can break that invariant at this point.

---

**jgm** (2020-12-03):

There have been various points raised regarding the ability of the validator to transfer funds under this proposal.  It is important to note that the validator will not be able to move the original 32Ether capital, however the concerns still stand.  There are a number of possibilities to handle this, which I’ll outline below:

1. Require a signature from the withdrawal key as part of the block proposal.  This would be an explicit per-movement authorization.  As such, it is the most granular however it also requires the withdrawal key to be available for signing at each proposal.
I think that this approach would be too onerous on the holder of the withdrawal key, especially in the case of staking pools, for this to be realistic.
2. Require an “allow excess balance transfer” from the withdrawal key as a separate operation.  This would be a one-time authorization that would allow the validator to carry out future excess balance transfers.  It would require an additional bit for each validator stating if excess balance transfers were permitted, and a new operation that would set/clear it.
I think this has merit, however could run in to conflict with the fact that staking pools could in future have an Ethereum 1 address in their withdrawal credentials rather than a BLS pubkey hash, resulting in them being unable to use this method.  There are potential ways around this, however, and staking pools are those most likely to be able to manage this.
3. Create a separate “transfer key”.  This would involve the creation of a third key, the transfer key, whose sole purpose would be to allow transfers.  Although the idea has merit, and could be expanded to a generic “administration key” for future operations,  it would involve significant changes to the protocol.
I think that this is likely to involve too much surgery on the beacon chain definitions to be worthwhile.

Given the above options, I’m still of the mind that allowing the validator key to transfer excess balance is no more of a change in how the beacon chain works now than many other changes that are coming up and is a reasonable option.  If it is truly considered that it breaks unwritten assumptions to the point that users will prefer to not have this rather than be able to transfer excess balances, then the “allow excess balance transfer” operation would be my backup choice.

---

**jgm** (2020-12-03):

Regarding linking this with the withdrawal process: I think these are complementary proposals.  Withdrawing requires a validator to be withdrawable, which means it is not validating.  Transfer of excess balance can occur with active validators, and so will not impact on the security of the network.  Also, crucially, it does not require the merge to operate.

That’s not to say that there couldn’t be a way of potentially transferring the excess balance to an Ethereum 1 contract rather than a different validator index at some point in the future, but making the merge a pre-requisite reduces the value of this proposal in terms of timeliness, if nothing else.

---

**technocrypto** (2020-12-03):

I’m confused by your comments.  The validator does not have to be withdrawable, only the excess balance.  And the merge is clearly not a dependency for that, any more than it is for an exit of a full validator.  Are you operating under the assumption that immediate re-investment of earnings beyond the MAX_EFFECTIVE_BALANCE is a design requirement, separate from the design goal of eliminating the incentive to remove and redeposit the 32 ETH deposit itself?  If so I think it’s fine to consider that approach but we should be explicit about what we are trying to solve.

---

**jgm** (2020-12-03):

In Danny’s proposal, the validator being in the withdrawable state is a prerequisite.  In this proposal, the idea is to allow movement of excess balance by a block proposer whilst the validator is active.

Because the movement is only carried out when the validator is proposing a block it won’t be immediate, nor will it be mandatory.

---

**moles** (2020-12-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> I’m still of the mind that allowing the validator key to transfer excess balance is no more of a change in how the beacon chain works now than many other changes that are coming up and is a reasonable option.

Do you have references for these other proposals you could point me to? Would be interested to read up on any other changes which might grant the validator key the ability to transfer value.

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> If it is truly considered that it breaks unwritten assumptions to the point that users will prefer to not have this rather than be able to transfer excess balances, then the “allow excess balance transfer” operation would be my backup choice.

While it might not be explicitly stated anywhere that validator keys should never be able to transfer balance, it seems (to me at least) very unintuitive for that to be possible. The design of the dual validator/withdrawal key system very strongly suggests that one key is for balance transfer while the other is only for performing validation duties.

Totally agree that the “allow excess balance transfer” option looks like the best choice given this consideration.

---

**jgm** (2020-12-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/m/ba8739/48.png) moles:

> Do you have references for these other proposals you could point me to? Would be interested to read up on any other changes which might grant the validator key the ability to transfer value.

I wasn’t referring specifically to that change, but to other changes that will impact assumptions involved in existing validator operations.  Probably the largest one is that the current methodology of slashing protection will extend to shards, but the general point is that there is future functionality, both well-defined and yet-to-be-defined, that will result in a significant departure from the current production architecture.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/m/ba8739/48.png) moles:

> While it might not be explicitly stated anywhere that validator keys should never be able to transfer balance, it seems (to me at least) very unintuitive for that to be possible. The design of the dual validator/withdrawal key system very strongly suggests that one key is for balance transfer while the other is only for performing validation duties.

That could be just down to naming.  Validator key is probably a misnomer; you could argue, for example, that a validator exit shouldn’t be signed by a validator key because it’s not a validation duty.  It could well be that the validator key is eventually looked upon as the operations key, or some other name that suits its expanded role.  Or we may end up with additional keys, or some other way forward.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/m/ba8739/48.png) moles:

> Totally agree that the “allow excess balance transfer” option looks like the best choice given this consideration.

I do think that this ends up in the “least worst” box.  It ensures the withdrawal key holder has a say in excess balance transfers, but doesn’t clog the chain with lots of repeated requests.  The operation itself wouldn’t be tiny (a validator index and public key for each validator for which the holder wanted to enable transfers, plus an aggregate signature) but it’s not egregious, and a bit of logic to ignore repeat operations would remove the ability for people to spam it (or alternatively there could be a nominal cost to setting or clearing the flag).

---

**OisinKyne** (2020-12-04):

Weighing in here with some questions and opinions with regard to this proposal.

Question:

I understand that exit-withdraw-deposit cycles would not be ideal in terms of avoidable churn, but what is the intended use case of this proposal? The only validators that would benefit from an influx in funds are undercapitalised validators (i.e. between 16 < 32 etc). If the `to` address is a validator index, that means they have already made a 32 eth deposit to get into the activation queue (else they wouldn’t have an index). Transferring funds beyond MAX_EFFECTIVE_BALANCE from one fully capitalised validator to another has no tangible benefit I can think of, so is this purely to allow for a market for validators that have dropped below max through inactivity to purchase rewards to bring them back up to 32+ eth? Is it a mechanism to consolidate rewards from many validators to a single one which would then exit + withdraw + restake so if you’re a whale you can more efficiently restake validators from the earned rewards?

My subjective opinion on the proposal:

Does making it easy for whales to recycle their funds into new validators incentivise the centralisation of validators? In my mind it does, but I’m not sure if it would be by a hugely significant amount, and the pros might outweigh the cons (e.g. 100x fewer exit+restake validator cycles versus maybe ~1% annual improvement in capital efficiency due to staking rewards becoming compoundable sooner). I’d personally want to see some modelling of the impact this could have on long activation and exit queues + some modelling on the how much more compounding return you could attain by being part of the biggest staking pool instead of being an independent validator. I’m biased but personally I would not incentivise the growth of collective validator pools, whether the pools are decentralised or custodial.

Secondly, I think the idea that a validating key gets to choose which validator index to transfer to is a non-negotiable no in my eyes. That fundamentally changes trust assumptions about what power a validator key has, this would have legal and insurance and financial complications as well as security complications. Right now a staking provider that doesn’t hold your withdrawal key can either stake or exit, nothing else. As mentioned by Micah in the discord, the incentives to compromise a non custodial(no withdrawal key) staking service change hugely if this is implemented. Right now, an attacker can force a slashing event and get a validator exited, but they cannot get the funds. With this proposal, they could transfer all rewards to their own validator, which could be a huge sum of money within 5-10 years (bigger than principal).

I would lean towards [@technocrypto](/u/technocrypto) 's middle ground that says that a withdrawal key (or even a third key) can dictate that a validator can transfer their rewards above MAX_EFFECTIVE_BALANCE to a withdrawable state when they propose a block, but I don’t know if that increase in perpetual small transfers would be more overhead than exit-withdraw-restake cycles we’re trying to avoid in the first place to be honest.

---

**jgm** (2020-12-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/oisinkyne/48/22214_2.png) OisinKyne:

> The only validators that would benefit from an influx in funds are undercapitalised validators (i.e. between 16  Does making it easy for whales to recycle their funds into new validators incentivise the centralisation of validators?

Not when a decentralised staking pool has exactly the same ability, no.

![](https://ethresear.ch/user_avatar/ethresear.ch/oisinkyne/48/22214_2.png) OisinKyne:

> With this proposal, they could transfer all rewards to their own validator, which could be a huge sum of money within 5-10 years (bigger than principal).

Which is where the suggestion about having the withdrawal key being able to enable/disable this functionality comes in.  If the withdrawal key doesn’t explicitly allow it, this functionality is not available to the validator.  And if the validator key is somehow compromised the withdrawal key can revoke permissions.

![](https://ethresear.ch/user_avatar/ethresear.ch/oisinkyne/48/22214_2.png) OisinKyne:

> I would lean towards @technocrypto 's middle ground that says that a withdrawal key (or even a third key) can dictate that a validator can transfer their rewards above MAX_EFFECTIVE_BALANCE to a withdrawable state when they propose a block

To say it once more: this proposal is for transfers to take place purely on the beacon chain.  Having some sort of partial withdrawability is not only a significant step up in complexity, but again requires the merge as a prerequisite.

---

**OisinKyne** (2020-12-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> new validator created some amount of Ether  Not when a decentralised staking pool has exactly the same ability, no.

Fair but I would consider it an aggregative force rather a decentralising force, it might not be significant though.

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> Which is where the suggestion about having the withdrawal key being able to enable/disable this functionality comes in. If the withdrawal key doesn’t explicitly allow it, this functionality is not available to the validator. And if the validator key is somehow compromised the withdrawal key can revoke permissions.

Sounds good to me, revocable consent from the withdrawal key seems sensible.

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> To say it once more: this proposal is for transfers to take place purely on the beacon chain. Having some sort of partial withdrawability is not only a significant step up in complexity, but again requires the merge as a prerequisite.

Fair point, if potentially undercapitalised validators optimistically entering the activation queue doesn’t adversely impact liveness/security etc. I think this is potentially a feasible idea.

---

**moles** (2020-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/oisinkyne/48/22214_2.png) OisinKyne:

> At what point is a validator index assigned to a deposit? I know DepositEvents are logged for anything over 1 eth, but I assume a validator index only becomes assigned once a deposit becomes eligible for activation.

Validators are recorded on the beacon chain and assigned an index with any valid (i.e. >= 1 ETH) deposit amount. They only require a >= 32 ETH balance for the `activation_eligibility_epoch` to be set.


*(13 more replies not shown)*
