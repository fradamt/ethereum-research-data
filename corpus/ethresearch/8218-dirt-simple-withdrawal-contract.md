---
source: ethresearch
topic_id: 8218
title: Dirt Simple Withdrawal Contract
author: technocrypto
date: "2020-11-14"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/dirt-simple-withdrawal-contract/8218
views: 4968
likes: 7
posts_count: 17
---

# Dirt Simple Withdrawal Contract

Not sure if something like this has already been discussed, but I would like to propose the following Dirt Simple (no BLS verification, very easy to audit and formally verify) Withdrawal Contract:

There are only two functions. One is a constant function named “is_withdrawal_active” which returns bool FALSE.

The second is a function “set_withdrawal_address” which takes arguments “(address withdrawal_address_to_set, bool is_final, bytes validator_pubkey, bytes bls_signature)”, emits the submitted arguments as an event, and then throws them away with no further processing.

The contract should be written in and compiled from whichever language will make it easiest to audit and formally verify.  An important goal of this design is to allow that to happen as soon as conceivably possible, in order to support use cases like trustless staking pools.

In order to set a withdrawal address, the address and the is_final bit are signed with the **withdrawal** key for a single validator ID.  Then the address, the bit, the pubkey for the corresponding *validator*, and the created signature are submitted via the “set_withdrawal_address” function.  The rule for interpreting the Dirt Simple Withdrawal Contract in the future is that the withdrawal address for each validator is set to:

1. If no valid BLS signed message for the validator has ever been sent to the Withdrawal Contract, deposits will eventually be claimable by signed withdrawal message from the Withdrawal Key.
2. If any valid BLS message for the validator has ever been submitted with the is_final bit set to TRUE, then the deposit will be sent to the address given in the first valid message which was submitted with an is_final bit set to TRUE. All others will be ignored.
3. If any valid BLS message has ever been submitted for the validator, but all valid messages have set the is_final bit to FALSE, then the deposit will be sent to the address given in the latest message submitted.  All others will be ignored.

Note that since the contract itself neither verifies BLS signatures nor keeps track of either final or updateable messages, all such verification must be done out of band.

If desired in a future hard fork, a more complex version of the Withdrawal Contract may be deployed in place of the Dirt Simple Withdrawal Contract, which may do things such as actually verifying the BLS signatures, maintaining an actual list of current withdrawal addresses which have been set, etc.

Eventually, when withdrawals are ready to be enabled, the Dirt Simple Withdrawal Contract or its later replacements will be updated so that the “is_withdrawal_active” function returns TRUE and deposits will actually be processed for validators which have been exited within the beacon chain.  It is up to the specifications of later phases to decide what that withdrawal logic is and how it is implemented.

At the time of deploying the Dirt Simple Withdrawal Contract there would be only a very basic EIP created which specifies the rules for updating withdrawal addresses and specifies that withdrawals to addresses set in this way will be performed as simple value sends with no attached metadata.  If various contract designers want to use such information when standards for it are eventually decided upon, they will have to design updateable contracts which can retrieve any necessary metadata from, e.g. a beacon chain light client within the EVM when it is standardised and released.  Similarly, contract designers who anticipate needing to differentiate based on the specifics of particular validator IDs/histories should be careful to deploy *different* upgradeable contracts for each validator, since there would be no way to distinguish the source of an incoming deposit.

Note that the above Dirt Simple Withdrawal contract is sufficient *both* for setting a contract in charge of any validator income *and* for enabling transfers or tokenisation of exited deposits prior to the existence of actual withdrawal or transfer capability.  To irrevocably commit to a contract owning exited funds one simply sends a signed message with the is_final bit set to the Dirt Simple Withdrawal Contract.  If desired this can be done prior to depositing in the deposit contract (with deposit data specifying the same withdrawal key which was used to set the withdrawal address for that validator).  To transfer or tokenise funds which have already been exited one simply uses an appropriate contract in this fashion.  Several audited examples already exist with the necessary functionality from the world of DeFi.

It’s my belief that this would be the fastest and safest path for enabling trustless staking pools and trading or tokenisation of exited validator balances. It is backwards compatible with all existing mainnet validators and requires very minimal due diligence and associated tooling.  It would also allow projects which need to develop and audit contracts for trustless staking pools to begin that development immediately, even before the Dirt Simple Withdrawal Contract was successfully audited, verified, and deployed.  I’m open to feedback and improvements to the design.  One possible improvement, for example, would be to design the signature format in a way that would make it amenable to easy aggregation. But the basic philosophy here is that the Dirt Simple Withdrawal Contract has no logic, only a specification for the future interpretation of submitted messages.

## Replies

**alonmuroch** (2020-11-15):

Great proposal.

I think my only worry is that is_final bit, I’d be hesitant to use it without knowing what a future contract will look like. Of-course you could always have an upgradable proxy contract but that complicates thing.

It seems to me that a lot will choose to stick with a non final address until things are more set and tested which kind of misses the point because now the user will need to maintain 3 keys instead of 1.

---

**technocrypto** (2020-11-15):

There is no need for users to use the withdrawal contract at all if they just want to keep their existing deposit and withdrawal keys.  Indeed, until/unless compelling usecases are developed I expect few users to make use of the Dirt Simple Withdrawal Contract at all.  The most important part of this proposal is that it can be developed against right away.  It probably won’t really be used until some of that development comes to fruition.

But obviously the is_final bit is needed to grant binding control over withdrawals for validators who have already been deposited.  If withdrawal keys retain the ability to revoke or modify withdrawal destinations, then it will be impossible for trustless staking pools to apply programmatic conditions and guarantees to the proceeds of staking.

I do think it’s important to realise that these conditions can be exceptionally simple and still provide a very serious improvement to the level of representation and decentralisation we see among stakers.  Even a regular multisig allowing users to share control over a validator slot and make changes to their agreement by mutual consent is an enormous opportunity to tear down the 32 ETH wall and make staking financially accessible to people who can’t afford to lock up 15k USD for 2+ years.

---

**alonmuroch** (2020-11-15):

I definitely understand the value in that, no doubt.

For me, if we had some more clarity around how an eth2->eth1 transaction will look like post merger it will make things much easier.

---

**technocrypto** (2020-11-15):

I don’t think you’re quite understanding the proposal yet.  The point of the DSWC is that we obtain this clarity by specifying it:  a normal ETH transfer so that we can easily test by doing the same thing right now.  This certainly does not preclude the development of more metadata-rich methods later, but since such methods will undoubtedly take longer to finalise those use cases which need them can wait for them while the ones which do not depend on such metadata (such as simple multisigs etc.) can go ahead now without being further delayed while those details are hashed out.  Do it now, do dirt simple, and let people who want to develop against that while we figure out how to provide the more information rich version that more elaborate use cases require.

---

**alonmuroch** (2020-11-15):

Then we should start from specifying exactly what use-cases we want to support. If it’s a simple multisig than you don’t need this at all, BLS keys will enable you to do it quite easily.

If it’s more complicated use cases like staking pools than IMO we will need more data than a simple tx.

---

**technocrypto** (2020-11-16):

There is a world of difference between a multisig based on BLS where participants must actively sign every action and one based on contracts where parties can pre-commit to programmatic policies, like we already have in the EVM.  There is a perfectly exact specification for use cases included in the DSWC design:  anything you can do with normal ETH transfer, no beaconchain specific metadata attached.  There are an enormous amount of simple tools which have already been designed for this scenario in the EVM which would become available immediately, without having to wait for an exact specification of how beaconchain data will delivered to the EVM, which could take many months.  Simple trustless pools are needed now to cut the 32 ETH wall into halves, thirds, quarters, etc. and the DSWC is a simple and safe way to do that.

---

**vbuterin** (2020-11-16):

How would you compare and contrast this scheme versus this proposed alternative for transferability / smart contract pool friendliness that I came up with:

Allow deposits to specify an ETH address as their withdrawal credentials, and precommit to implementing withdrawals going to that address when withdrawals become possible. Then users can just set their withdrawal address to be a contract where the rights to receive the ETH from that contract can be tokenized as an ERC721 or ERC20.

---

**technocrypto** (2020-11-18):

In many ways this is similar.  One big difference is in enabling support for existing deposits since they have already started, and in permitting traditional withdrawal keys to re-assign the withdrawal address until they mark it as final.  Both considerations make the DSWC preferable in my view.

Sidenote:  several discord commenters have noted that it seems useful to specify the source address of the “simple ETH transfer”, and I would propose specifying that this will be the DSWC itself, but without necessarily committing to either a push or pull standard.  This leaves room for a future meta-data rich standard to be implemented either way.

---

**vshvsh** (2020-11-19):

[@vbuterin](/u/vbuterin) it’s a good idea but there is an important caveat of how much gas the receiver contract can have to act upon. Is. it unbounded? If so, who pays for it?

---

**technocrypto** (2020-11-19):

A standard plain send of ETH has a bounded amount of gas which is basically just enough to log that it happened.  If contracts want more functionality than this they will have to implement other functions which can be called to process the log once the ETH has been received.

---

**samueldashadrach** (2020-11-21):

What you are saying can be implemented in the receiver contract. Validator sets withdrawal address to a receiver contract, this can’t be changed. However the receiver contract could have pre-defined logic such as which address the eth can further be withdrawn to, and whether this is final (an is_final bit).

---

**technocrypto** (2020-11-21):

Two problems with this.  First, there is no support in that approach for users who have already deposited. Many users will want to or already have deposited with BLS withdrawal keys and then will later decide to exit.  If you want to be able to tokenize and trade those exited funds, you need to support irreversibly adding a contract to an existing BLS controlled account, so doing this with the actual deposit contract would require a hard fork.  Second, if you have to develop a second contract to manage logic such as the is_final bit, then you still have the challenge of making *that* contract as simple and easy to audit as possible.  I would argue that you are unlikely to come up with a design for this second contract which is simpler and easier to audit than the DSWC.  But I’m happy to hear proposals for simple contracts which could be directly set as receivers.  Do you think you can come up with one that is easier to audit than the DSWC?

---

**kladkogex** (2020-11-21):

It does not seem to be easily implementable, because there will be ETH issued on ETH2, so the amount of ETH on ETH2 will be larger than the amount stored in the deposit contract.

I understand that one can separate initial deposits from staking rewards but it  is probably not desirable …

When ETH2 rewards go back to ETH1,  there will be any way a fork to enable printing of ETH on ETH1 from ETH2.  This mechanism can print the original deposits too, so there is probably no need to additionally fork the deposit contract …

---

**technocrypto** (2020-11-21):

You’re correct that all of this will be done at once with a fork.  But the nice thing about the DSWC is that we don’t need the fork to assign contracts to be in control of the eventual withdrawals.  We can implement the DSWC today and start using it to do trustless pools, and then still go ahead with the planned fork at a later point in time.

---

**technocrypto** (2020-11-25):

Note that for all those following this thread [@djrtwo](/u/djrtwo) has made a more beacon-chain centric proposal which I have responded to [here](https://ethresear.ch/t/simple-eth1-withdrawals-beacon-chain-centric/8256/10).

---

**samueldashadrach** (2020-11-28):

First problem I don’t have a solution for.

Second problem doesn’t seem like a problem. Ethereum philosophy has always been to code the minimal amount into the protocol, and let what can be done using contracts be done by contracts. This passes on the buck of coding + auditing the rest to users, which is a good design principle imo, even if it leads to a bit more complexity.

