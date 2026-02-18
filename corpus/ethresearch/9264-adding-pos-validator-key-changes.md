---
source: ethresearch
topic_id: 9264
title: Adding PoS validator key changes
author: vbuterin
date: "2021-04-26"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/adding-pos-validator-key-changes/9264
views: 5552
likes: 10
posts_count: 5
---

# Adding PoS validator key changes

One feature that would be nice to add to eth2 would be the ability for a validator to switch their staking key. This is nice because it would allow a form of de-facto “delegation” where validators give their staking keys to a pool, and if the pool misbehaves or starts to have a high risk of misbehaving they can quickly switch the key to a different pool or to a self-hosted key, without *any* downtime. Currently, switching keys requires one withdraw → re-deposit cycle, incurring a minimum of 27 hours of downtime.

The reason why no functionality for delegation or switching keys is available in eth2 is not (as some [have guessed](https://twitter.com/hasufl/status/1386350453106040836)) out of a deliberate attempt to prevent these behaviors; rather, it was because it is difficult to do this while at the same time preserving accountability for slashing. Most protocols with easy delegation mechanics do not have an accountability mechanism where the user themselves gets slashed if the user they delegate to misbehaves. Here is a proposal for allow key switching in a safe way that preserves accountability.

### Data structure changes

We replace the `pubkey` variable in the `Validator` object with three variables:

```auto
old_pubkey: BLSPubkey
new_pubkey: BLSPubkey
switch_epoch: Epoch
```

The pubkey of a validator in some epoch is just `validator.new_pubkey if epoch >= validator.switch_epoch else validator.old_pubkey`. Attestations and slashings can be processed with the correct pubkey automatically.

### Key switching

A validator can send a message `KeySwitch = {new_pubkey: BLSPubkey, switch_epoch: Epoch, signature: BLSSignature}` which can get included on-chain. It checks that the `switch_epoch` is in the future, and that the signature is valid against the current `validator.new_pubkey`. Processing the key switch is simple:

```auto
validator.old_pubkey = validator.new_pubkey
validator.switch_epoch = key_switch.switch_epoch
validator.new_pubkey = key_switch.new_pubkey
```

To prevent the existing `old_pubkey` from being overwritten too early and thus escaping slashings, we also require the validator to be *well past* its key transition. That is, we require `current_epoch >= validator.switch_epoch + {8 months}` (note: if a transition has not yet happened, the check passes because `validator.switch_epoch = 0`, assuming the chain is at least 8 months old).

To allow validators to switch keys more frequently when this is safe, we add an additional mechanism: during the exit queue clearing process, if normal exit clearing fully clears the exit queue, the remaining exit slots for that epoch are instead used to take the validators whose `switch_epoch` is furthest in the past but nonzero, and set it to zero (the `old_pubkey` can be set to zero at the same time to cut down storage space). This should allow pubkey switches to complete very quickly under normal circumstances, and only actually take up to 8 months in exceptional periods of congestion.

### Control of key switching rights

The last question is, which validator key has the right to control signing key switches? We don’t want the signing key to control signing key switches, as that gives the signing key too much power and runs counter to the goal of safe delegation. The withdrawal credentials are not necessarily a key at all. My proposed solution is to expand to *three* keys:

- Signing key
- Administration key
- Withdrawal credentials

The administration key has the right to control (i) key switches and (ii) when the validator withdraws. The signing key can also trigger a withdrawal, though not a key switch. The administration key and withdrawal credentials can be stored under a single hash to save state space.

## Replies

**alonmuroch** (2021-04-27):

That’s very interesting!

One benefit of this would be a really vibrant Secret-Shared-Validator(SSV) market place.

SSV is the ability to distribute the validation key to trustless operators, the ability to switch the key with an admin key can make switching to different operators more secure (no need to re-share an existing key).

---

**vshvsh** (2021-04-28):

This proposal is a good step to full-fledged delegation protocol in ETH but is not very consequential by itself IMO.

Delegation is sort of possible now: delegator holds the withdrawal credentials, delegate has validation keys and is legally or otherwise bound to exit when the delegator asks them to (see stakefish example, it’s a design perfect in its simplicity, and thus popular in the wild). Switching validator key iff a lot of time has passed or exit queue is free will reduce churn somewhat but doesn’t change the featureset or delegation simplicity very much. There will be a safety hatch of sorts that will not require validator’s goodwill, but there still will have to be legal binding or protocol design around profit sharing, or exits in congested times - all very important to delegation that works in practice. So while safety of delegation improves, UX doesn’t really, and UX is the key to delegation mechanism design IMO. We can learn much from Cosmos staking design, these folks are truly visionary in that area.

Adding admin role to a validator is a really important part of the proposal, and one that I would wholeheartedly agree with, but only if it’s possible for smart contracts to take that role. Otherwise custodial staking pools and TSS-based solutions once again will have the upper hand, and that’s not great for security of the network.

---

**samueldashadrach** (2021-04-28):

Just wanted to add to your consideration that delegation, by far, will not be peer-to-peer, it’ll be peer-to-pool. So the popular model is not A delegates to B, it’s A delegates to pool delegates to B.

Reasons for pooling are numerous - you can get liquidity and higher price on tokenised representations of ETH, you can save gas by doing actions in pooled fashion, you can slap on a speculative governance token that helps fundraise for dev work as well as we provide people a sense of community ownership (fake or real, the fact is the DeFi crowd likes the speculation and drama) and ofcourse it makes the founders rich.

---

**kladkogex** (2021-04-28):

Peer-to-pool delegation is what we use at SKL.  Delegators delegate to validator that

runs nodes on SKL network proportional to delegated stake.


      [github.com](https://github.com/skalenetwork/skale-manager/blob/6dcd9d94ee75bbd96a0365c14572290d007411e6/contracts/delegation/DelegationController.sol)




####

```sol
// SPDX-License-Identifier: AGPL-3.0-only

/*
    DelegationController.sol - SKALE Manager
    Copyright (C) 2018-Present SKALE Labs
    @author Dmytro Stebaiev
    @author Vadim Yavorsky

    SKALE Manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SKALE Manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with SKALE Manager.  If not, see .
```

  This file has been truncated. [show original](https://github.com/skalenetwork/skale-manager/blob/6dcd9d94ee75bbd96a0365c14572290d007411e6/contracts/delegation/DelegationController.sol)








ETH2 deposit contract was specifically designed to not allow smart contracts to delegate, so I think it is hard to implement in on ETH without updating the deposit contract.

BTW [@samueldashadrach](/u/samueldashadrach)  - we at SKALE are interested to design a tokenized representation of SKL, as well as a pool contract that helps small delegators pool funds and save gas fees.

Would you be interested to work on this? We could issue you a token grant  ![:imp:](https://ethresear.ch/images/emoji/facebook_messenger/imp.png?v=9)

