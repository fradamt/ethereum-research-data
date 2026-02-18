---
source: ethresearch
topic_id: 8256
title: Simple eth1 withdrawals (beacon-chain centric)
author: djrtwo
date: "2020-11-24"
category: The Merge
tags: []
url: https://ethresear.ch/t/simple-eth1-withdrawals-beacon-chain-centric/8256
views: 13156
likes: 25
posts_count: 25
---

# Simple eth1 withdrawals (beacon-chain centric)

# Simple eth1 withdrawals (beacon-chain centric)

*[This is a followup and alternative proposal to [@technocrypto](/u/technocrypto)’s [Dirt Simple Withdrawal Contract](https://ethresear.ch/t/dirt-simple-withdrawal-contract/8218)]*

This proposal is a beacon-chain-centric withdrawal plan (a place where we have native access to validators and to BLS verification) that keeps the eth1 promise to an absolute minimum.

This allows for simple (but expressive) withdrawal contracts to be written today and for eth1 addr as withdrawal credentials to be submit as validator deposits today (well as soon as we write it in the spec’s repo). More sophisticated logic/accesses to beacon state *cannot* be carried out with this proposal, but (1) I suspect that 80%+ of withdrawal contract use cases will be satisfied and (2) additional use cases will be opened up when eth1-native reads to beacon state (post-merge) are spec’d/implemented.

*Note, the core commitment to getting this going would be to `Eth1AddressPrefix` withdrawal credentials and to the fact that withdrawn ETH will end up in the specified withdrawal address as a simple send*. All other details are for illustration that this idea is end-to-end coherent.

*Edit*: [@vbuterin](/u/vbuterin) pointed out that we don’t need a new `withdrawal_address` field on `Validator`. Instead the `BLSSetWithdrawalAddress` would change the `withdrawal_credentials` from BLS withdrawal credentials to Eth1 withdrawal credentials. Thanks!

## tl;dr

**Beacon chain changes**:

- Specify Eth1AddressPrefix – 0x01 – withdrawal prefix that allows to specifies the last 20 bytes of the credentials to be a 20-byte eth1-addr
- Validators will have an withdrawal_address. This is initiated to ZERO_ADDRESS - 0x00..00
- When withdrawable

if prefix == BLS_WITHDRAWAL_PREFIX:

validator must submit a BLSSetWithdrawalAddress operation to set their withdrawal_address before they can be withdrawn (this can be sent before withdrawable)
- BLSSetWithdrawalAddress contains the destination eth1-addr and is signed by the bls withdrawal credentials
- once this withdrawal_address is set and the validator is withdrawable, it gets withdrawn at next epoch transition

if `prefix == Eth1AddressPrefix`, validator gets auto-withdrawn at withdrawable epoch during the epoch transition (see `process_withdrawals`)
Being “withdrawn” is the action of a withdrawal receipt being added to beacon state (see `withdraw_validator`)

Clean up

- clean up withdrawn validator indices after year+
- clean up withdrawal receipts after time/consumed

**Eth1 functionality**:

- Eth1 has access to beacon chain receipt merkle root (or entire list)
- Track consumed receipts in either a system contract or some system state
- Normal TX to special system withdrawal contract to finish withdrawal

Normal sender of TX pays gas. Maybe can pay gas with validator balance if/when AA
- TX hits a system address. If withdrawal receipt not consumed:

send ETH to withdrawal_address (normal transfer, no data)
- if/when returns to system contract, mark withdrawal receipt as consumed

## Beacon chain changes

- Add withdrawal_address to validators, initialize all to ZERO_ADDRESS
- Addr withdrawn_epoch to validators, initialize all to FAR_FUTURE_EPOCH

### BLSWithdrawalPrefix

- Add new beacon operation BLSSetWithdrawalAddress

Allows user with an BLSWithdrawalPrefix withdrawal prefix to set their eth1 withdrawal address via a signed message with their BLS withdrawal keys
- Can be performed any time before withdrawn
- Options for discussion:

Should operation be able to be performed more than once?
- If so, should it have a is_final feature like in Dirt Simple Withdrawal Contract?
- Probably would need a fee structure to get these included on chain. If so, need to consider implications of transferring balances of active validators (security). Simplest is to only allow for exited+ validators.

Sample code:

```python
class SignedBLSSetWithdrawalAddress(Container):
    message: BLSSetWithdrawalAddress
    signature: BLSSignature

class BLSSetWithdrawalAddress(Container):
    validator_index: ValidatorIndex
    credentials_pubkey: BLSPubkey
    withdrawal_address: Eth1Address

def process_bls_set_withdrawal_address(state: BeaconState, signed_bls_set_withdrawal_address: BLSSetWithdrawalAddress) -> None:
    set_withdrawal_address = signed_bls_set_withdrawal_address.message
    validator = state.validators[set_withdrawal_address.validator_index]
    # Verify the validator is not already withdrawn
    assert not is_withdrawn_validator(validator, get_current_epoch(state))
    # Verify that the validator has BLS withdrawal credentials
    assert validator.withdrawal_credentials[0] == BLSWithdrawalPrefix
    # Verify that the pubkey is the correct pubkey behind the credentials
    assert hash(set_withdrawal_address.credentials_pubkey)[1:] == validator.withdrawal_credentials[1:]
    # Maybe verify if `withdrawal_address == ZERO_ADDRESS` to only allow setting once
    # Verify signature
    domain = get_domain(state, DOMAIN_BLS_SET_WITHDRAWAL_ADDRESS, get_current_epoch(state))
    signing_root = compute_signing_root(set_withdrawal_address, domain)
    assert bls.Verify(set_withdrawal_address.credentials_pubkey, signing_root, signed_bls_set_withdrawal_address.signature)
    # Set eth1 withdrawal address
    validator.withdrawal_address = set_withdrawal_address.withdrawal_address
```

### Withdraw validators at epoch boundary

Add `process_withdrawals` to `process_epoch`. Note that `Eth1AddressPrefix` withdrawals happen automatically, while `BLSWithdrawalPrefix` withdrawals require a `BLSSetWithdrawalAddress` before the withdrawal can occur.

```python
def withdraw_validator(state: BeaconState, validator: Validator) -> None:
    validator.withdrawn_epoch = get_current_epoch(state)
    # Append withdrawal receipt to the state withdrawal receipts
    # (structure tbd)

def process_withdrawals(state: BeaconState) -> None:
    withdrawable_validators = [
        validator for validator in state.validators
        if (
            is_withdrawable_validator(validator, get_current_epoch(state) and
            not is_withdrawn_validator(validator, get_current_epoch(state))
        )
    ]
    for validator in withdrawable_validators:
        if (
            validator.withdrawal_credentials[0] == BLSWithdrawalPrefix
            and validator.withdrawal_address != ZERO_ADDRESS
        ):
            withdraw_validator(state, validator)
        elif validator.withdrawal_credentials[0] == Eth1AddressPrefix:
            validator.withdrawal_address = Eth1Address(validator.withdrawal_credentials[12:])
            withdraw_validator(state, validator)
```

## Eth1 functionality

Most of the details are in the above tl;dr. The two core elements are

1. once a withdrawal has been initiated on beacon chain side, a normal user TX must trigger the withdrawal to the eth1 addr
2. from the destination addr’s (validator.withdrawal_address) perspective, it just looks like ETH was transferred to it

The particular details of tracking receipt consumption don’t have to be fully figured out in this proposal. If we can agree on the two simple points above, that is enough to specify the `Eth1AddressPrefix` withdrawal credentials and build/deploy withdrawal contracts.

There are potentially more sophisticated features that *cannot* be built with the simple scheme until beacon chain reads are implemented, but I would argue that most designs can be accomplished.

Two important notes when considering designs:

1. Use of child withdrawal contracts can make the handling of withdrawals more granular for a larger pool
2. One interesting thing people want to know is if a withdrawn validator is_slashed. Yes, your pool might be able to do more punitive things but if you use child contracts for granular withdrawal processing, the eth2 protocol will already have punished the slashed validator through the burning of some amount of ETH, so this baseline punitiveness along with granular parsing provides a pretty solid baseline functionality.

## Replies

**vbuterin** (2020-11-24):

Definitely a reasonable way to do it! Of course it’s worth clarifying that this enables transferability, with all the upsides and downsides of that (because withdrawals can go into smart contracts that are essentially wrappers with an ERC20 representing future claiming rights), and so that point needs to be discussed explicitly.

The one technical thing I would change is to get rid of the concept of `withdrawal_address` and instead just have `process_bls_set_withdrawal_address` change the withdrawal credentials in-place into the address-based format. This avoids the need to bloat the validator object further and additionally means that the `process_withdrawals` function would only need to have one clause (the `if validator.withdrawal_credentials[0] == Eth1AddressPrefix` clause).

---

**moles** (2020-11-24):

The possibility of submitting multiple `BLSSetWithdrawalAddress` operations is ruled out by changing withdrawal creds in place, correct? This seems fine to me, just worth noting.

---

**djrtwo** (2020-11-24):

yes, correct

I don’t immediately see much value in the multiple submissions of `BLSSetWithdrawalAddress`, but it was in [@technocrypto](/u/technocrypto)’s proposal so wanted to show it is possible and up for discussion

---

**alonmuroch** (2020-11-24):

Great proposal!

[@djrtwo](/u/djrtwo) how is the withdrawal initiated on the beacon chain side? with what key/ tx?

---

**jgm** (2020-11-24):

`process_bls_set_withdrawal_address`   seems somewhat specific compared to a more general-purpose version that accepted an arbitrary 32-byte value rather than an Ethereum 1 address.  The latter would result in simpler code as well as allowing for further withdrawal methods in future.  Is this specificity intentional, to lock down the functionality to ETH1 addresses only?

---

**moles** (2020-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> if prefix == Eth1AddressPrefix , validator gets auto-withdrawn at withdrawable epoch during the epoch transition (see process_withdrawals )
> Being “withdrawn” is the action of a withdrawal receipt being added to beacon state (see withdraw_validator )

^ automatically initiated within `process_epoch`

---

**moles** (2020-11-25):

My interpretation was that this method was written before the suggestion to update withdrawal credentials in place - agree that a general-purpose `process_bls_set_withdrawal_credentials` method would work better in that case.

---

**kladkogex** (2020-11-25):

I am a bit confused how the Merkle root of the ETH2 chain is going to be available on ETH1?

This assumes that ETH1 is merged into beacon chain, correct ?:))

---

**technocrypto** (2020-11-25):

Okay, first reaction to this proposal:  it feels like we’re not taking advantage of the fact that withdrawal credentials are *BLS* signatures.  There’s a chance to enormously compress withdrawal data here, which could be super useful depending on how the eth1-beaconchain docking ends up working.  Wouldn’t it be nice to be able to aggregate the signatures for withdrawals?  Maybe it doesn’t matter, but that’s just where my mind goes. I want to try and put more thought into that, maybe others can too. That’s more of a sidenote though.

2nd reaction:  how can trustless pools use this method to make a safe deposit?  You have to be able to commit to the withdrawal contract before depositing. But if you’re not even on the beacon chain, you can’t use this method afaict. Or did I miss something?

3rd reaction, [@djrtwo](/u/djrtwo) let me explain why I had room for updating the withdrawal address in DSWC, and the large number of use cases which depend on this capability.

There are several different aspects to this, so I’ll go through them one by one.

**Partial withdrawals**

As [@jgm](/u/jgm) has already pointed out [in his other thread](https://ethresear.ch/t/simple-transfers-of-excess-balance/8263), there are strong reasons why validators will want to withdraw amounts above MAX_EFFECTIVE_BALANCE without withdrawing the rest of the validator balance, and why we should let them do this without having to make a full exit (churn, etc.).  This means that (especially if we were to go with [my suggested “single bit” modification](https://ethresear.ch/t/simple-transfers-of-excess-balance/8263/5) to his proposal) withdrawal addresses are not going to be single use, and they should have the option of being updateable.

**Split keys**

One BLS key does not imply one entity.  There are a myriad of situations where split keys might specifically *not* want to leave the withdrawal address un-set, but might *also* wish to change it in the future.  If one of a set of keyholders wants to quit, for example, they can just give/sell their keys to the other keyholders, but the withdrawal contract which would have presumably divided the proceeds will then need to be updated.  As new, more advanced contracts get developed specifically to handle as-yet-unprocessed withdrawals, keyholders might want to upgrade provided that they can all agree.  If there is a staking service which does the validating they might want to share ownership of the withdrawal key with the client so that they can update the policy under which withdrawals are governed; if there is a DAO the keyholders of the DAO might want the ability to change their minds; etc. It’s also important to note that until the EVM supports BLS operations this is the *only* way to take advantage of BLS functionality, since you can’t just write BLS support into an EVM contract.

**Loss/theft of credentials**

Right now we have the lovely property that for most participants in the beacon chain a single mnemonic backup protects both their validator and withdrawal credentials.  Given the length of time it might be before withdrawals become possible, someone who owns their own validator outright and is not trying to make a commitment to any other party might want to set their withdrawal address to a cold wallet or something to provide a nice level of “safe” redundancy. Then if they lose all their validator/withdrawal credentials they will be eventually exited for inactivity and recover at least some of their funds.  However if they retain control over their mnemonic and lose access instead to the withdrawal address over that time, they can simply restore their withdrawal credentials from their mnemonic and set a new one.

Obviously, even taking the three above considerations into account we still absolutely need the ability to set a non-revocable address for trustless pooling and other use cases which do not have a specific set of keyholders who can be trusted to control withdrawals.

---

**moles** (2020-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> 2nd reaction: how can trustless pools use this method to make a safe deposit? You have to be able to commit to the withdrawal contract before depositing. But if you’re not even on the beacon chain, you can’t use this method afaict. Or did I miss something?

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Normal TX to special system withdrawal contract to finish withdrawal

We don’t need to know the deployed address of the system withdrawal contract ahead of time, just its ABI. We can write and deploy a “receiver” contract for a validator with a method which accepts the system withdrawal contract address, then calls the defined method on it using `address.call`.

---

**technocrypto** (2020-11-26):

That’s not the problem I’m describing. The problem I’m describing is that users of trustless pools want to ensure the eth1 address which their funds will be withdrawn to is fixed and unchangeable at the time they deposit. Or perhaps it is implicit in this specification that the deposit contract would accept the new “0x01” Eth1Address withdrawal credential? If so then this could be specified there during the deposit.

---

**moles** (2020-11-26):

Yes, the deposit contract will accept any 32-byte array for withdrawal credentials. We could deposit using a `0x01` prefix today if we wanted; it’s just not particularly useful until there is a commitment to supporting that withdrawal type.

---

**technocrypto** (2020-11-26):

Gotcha.  Might be good for [@djrtwo](/u/djrtwo) to explicitly mention that in the proposal, just to remove ambiguity.

---

**djrtwo** (2020-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Specify Eth1AddressPrefix – 0x01 – withdrawal prefix that allows to specifies the last 20 bytes of the credentials to be a 20-byte eth1-addr

That’s what I mean about the following:

> Specify Eth1AddressPrefix – 0x01 – withdrawal prefix that allows to specifies the last 20 bytes of the credentials to be a 20-byte eth1-addr

There is no verification in the deposit contract or on eth2 beacon chain side so this can be specified in a minor version spec release and immediately built upon. That’s the primary purpose of the above proposal. To essentially show a viable end-to-end process that would enable `0x01` withdrawals today. In fact, most of the beacon-chain mechanics in this post aren’t even necessary. The most important component is simply how the eth1 chain would see such a withdrawal TX in the future.

---

**djrtwo** (2020-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> Wouldn’t it be nice to be able to aggregate the signatures for withdrawals?

You could do aggregation in, e.g. `BLSSetWithdrawalAddress`, but much of the efficiency is lost because (1) there is no apriori set know and (2) the message signed is not shared

Because of (1), you couldn’t just use a bitfield in the aggregated message and would instead have to explicitly specify validator indices (similar to attester slashings).

And because of (2), you would need to include the actual message signed for each.

You’d end up in a marginal block data savings  and a marginal verification cost saving, but at a higher complexity and an obfuscation as to which message(s) failed to verify in the event of a bad block being created.

Similar to how deposits are not currently aggregated on chain, I don’t expect the savings vs complexity to make sense here.

---

**djrtwo** (2020-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> how can trustless pools use this method to make a safe deposit? You have to be able to commit to the withdrawal contract before depositing. But if you’re not even on the beacon chain, you can’t use this method afaict. Or did I miss something?

*[I think this question might have been asked before you realized I was suggesting that 0x01 deposits should be able to be sent immediately. The logic to resolve 0x00 deposits to 0x01 deposits is just to show that alternate withdrawal workflow]*

Trustless in which sense? The selection of the withdrawal addr?

There are many iterations of design here. One example:

The withdrawal contract is created first. Then funds are pooled that can only be attached to a full 32-ETH deposit including the withdrawal contract as the withdrawal_creds. Then a 32-ETH deposit is made through this proxy contract, verifications are done against the deposit-data, and the 32ETH goes to the deposit contract.

The major downside to this design is that the BLS signature cannot be verified on chain. That said, there are ways around this. For example, a proposed deposit-data could go into this contract and only when N-of-M participants signal that it is valid, does the TX get sent. (with some expiration on the whole thing so funds aren’t in limbo forever).

---

**djrtwo** (2020-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> the large number of use cases which depend on this capability.

As for these alternative usecases for continually updating credentials, many can be handled via an eth1 contract. Once you update or initially set your credentials to a contract, logic in that contract can handle any further updates or theft/loss fallbacks.

The partial withdrawals usecase is certainly worth considering more deeply.

First and foremost, we need to identify whether having an independent transfer functionality is actually worth the complexity/load beyond this happening through validator churn. I see the value, but want to think about the options here a bit more.

---

**dapplion** (2020-12-14):

If a trustless pool specifies a child contract as the target withdraw address for validator X, how can it differentiate between the Beacon Chain’s transfer of validator funds vs me just sending some ETH to it?

---

**djrtwo** (2020-12-14):

In the design here, before there are beacon chain reads on eth1, it could not tell the difference.

I ask you though, if it could tell the difference, would that make a meaningful difference in 80%+ of use cases being designed for?

---

**dapplion** (2020-12-16):

It’s useful for staking pools to know that a validator lifecycle is completed to distribute the funds in a non-linear way. For example, if the final balance of the validator is lower than the starting balance you may want to make a party absorb the loss while distributing the rest to another party.

For that to happen you must know that the entire balance of the validator has already been transferred to the withdrawal account to trigger the above logic. Otherwise, someone could send 1ETH to the withdrawal address and claim the validator got slashed. How could the decentralized staking pool contracts tell the difference?

---

A possible way to achieve that would be for the validator balance transfer to happen when the withdrawal address itself calls the system contract. Then the contract could in one transaction

- Call system contract
- Compute its own balance diff
- Call the staking pool manager contract to mark its status and “done” and trigger accounting logic according to the above diff

A plus would be for the call to the system contract to revert if the withdrawal receipt has already been consumed.


*(4 more replies not shown)*
