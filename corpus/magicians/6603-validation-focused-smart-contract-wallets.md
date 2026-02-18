---
source: magicians
topic_id: 6603
title: Validation Focused Smart Contract Wallets
author: matt
date: "2021-07-05"
category: Magicians > Primordial Soup
tags: [eoav2]
url: https://ethereum-magicians.org/t/validation-focused-smart-contract-wallets/6603
views: 4759
likes: 5
posts_count: 3
---

# Validation Focused Smart Contract Wallets

Some [concerns](https://ethereum-magicians.org/t/we-should-be-moving-beyond-eoas-not-enshrining-them-even-further-eip-3074-related/6538/6) were recently raised about EIP-3074 and it’s compatibility with the future goal of eradicating EOAs from the protocol. I’ve spent some time thinking about this, and I think EIP-3074 actually provides an interesting alternative upgrade path.

If we’re going to replace EOAs, we should think carefully about what will replace them.

#### Protocol Smart Contract Wallets

Smart contract wallets today are generally implemented top down. In the simple case, the wallet acts as a bouncer. It validates the call to it and then forwards the message to the target contract. In more complicated cases, it is a collection of functions that are used in different ways to create complex access policies.

A simple bouncer contract is the natural replacement for EOAs. But although it has feature parity with existing EOAs, it has none of the [benefits](https://ethereum-magicians.org/t/we-should-be-moving-beyond-eoas-not-enshrining-them-even-further-eip-3074-related/6538) of smart contract wallets that Vitalik outlined.

There are [alternatives](https://gnosis-safe.io/) to this, but they fail to provide two attributes that are desirable for a protocol wallet:

1. Agnostic to tooling of today. Solidity and current ABIs should not leak into the protocol.
2. Extensible without requiring on-chain initialization.

To meet these requirements, we’ll need to rethink how smart contract wallets are designed.

#### Validation Focused Wallets

At their core, smart contract wallets just enforce access policies for the address they’re deployed at. Actually instantiating the `CALL` or performing replay protection in the smart contract wallet is just an implementation detail.

If we focus on this property, we can build a smart contract wallet that is unopinionated and extensible.

In this paradigm, the migration from EOAs to protocol smart contracts would look something like this:

- deploy EIP-3074, mostly as-is
- deploy EIP-3540 (EOF)
- add a new EOF section validate
- convert all EOAs to bouncer smart contracts that also implement the validate section which checks that ecrecover(msg, sig) == address()
- if no AA yet, make a special allocation in clients that allows accounts with code_hash equal to the EOA contract to initiate a transaction
- modify the behavior of AUTH to call the validate section on the recovered address, and only set authorized if the account’s validate returns true
- add AUTH2 which takes a target parameter whose validate section is immediately called upon invokation and only sets authorized if the target returns true (alternatively, we could immediately ship AUTH2 in EIP-3074 and require target == recovered address until the EOF section validate is added.)

This would give us all the benefits Vitalik outlined, while also i) not enshrining Solidity / a certain ABI encoding into the core protocol and ii) allowing *anyone* to enjoy those benefits (and new ones) without first interacting on-chain.

This also gives us some nice new benefits to EIP-3074. Instead of “signing a [blank check](https://youtu.be/uhvhfxiC-NA?t=1931) forever”, users can modify their own `validate` function to block certain invokers. This is much nicer than doing it in the invoker itself, because only users who wish to block an invoker must pay the storage costs to check if the invoker is blocked.

I’m curious to know other’s thoughts on this.

## Replies

**vbuterin** (2021-07-12):

Interesting! I think my main concern is the cross-dependency with EIP 3540, and the fact that this is still permanently adding a new concept of “authorization”, increasing the complexity of cross-contract interaction. Theoretically, in a smart-contract-account-only world, calling is all you need: if you want to authorize someone, then the smart contract itself can add a condition `if self.is_authorized[msg.sender]: skip_signature_checks()`.

> Agnostic to tooling of today. Solidity and current ABIs should not leak into the protocol.

I guess this depends on what you mean by “the protocol”. Are mempools part of the protocol? (Especially in a world where we could have multiple custom mempools that all compete on a meta-level through proposer/builder separation). Or are you referring to whatever the logic that existing EOAs get replaced by is? (which is part of the protocol, because that would be a compulsory code change to existing accounts created by a hard fork). If it’s the latter, then EOAs could just be hardcoded to unpack an existing RLP transaction.

---

**axic** (2021-07-12):

Thank you [@matt](/u/matt) for considering EIP-3540. I think this is in a similar vein as [Account Abstraction with EVM Object Format - HackMD](https://notes.ethereum.org/@axic/account-abstraction-with-eof), but without requiring the larger set of AA-changes (`PAYGAS`).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Interesting! I think my main concern is the cross-dependency with EIP 3540, and the fact that this is still permanently adding a new concept of “authorization”, increasing the complexity of cross-contract interaction. Theoretically, in a smart-contract-account-only world, calling is all you need: if you want to authorize someone, then the smart contract itself can add a condition if self.is_authorized[msg.sender]: skip_signature_checks().

~~I think it is not permanent.~~ Update: I think I misunderstood what you wrote. I think you meant permanent because it introduces new specific opcodes (`AUTH`)?

Even in the semi-enshrined version (i.e. a single code is assumed for all EOAs) it would be possible to have code which has a revoke list:

```python
def main():
    if msg.selector == abi("set_revoke"):
        set_revoke(...)
    // Other features

def set_revoke(target: address, revoked: bool):
    self.revoked[target] = revoked

# This is the validate section
def validate():
    return self.revoked[msg.sender] != true
```

Since adding a dependency on a fully-fledged AA solution in the short term seems unrealistic, doesn’t this proposal really hinges on nailing down the proper functionality for the default EOA code?

