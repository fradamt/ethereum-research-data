---
source: magicians
topic_id: 24620
title: Upgradable 7702 Delegator
author: 0xkoiner
date: "2025-06-20"
category: ERCs
tags: [erc, upgradeable-contract, eip-7702]
url: https://ethereum-magicians.org/t/upgradable-7702-delegator/24620
views: 88
likes: 0
posts_count: 4
---

# Upgradable 7702 Delegator

Hola Magicians, I want to share my thoughts and get feedback from devs who have been working lately on 7702 delegators.

We know that after the Pectra upgrade it’s possible to attach code to an EOA, so we can have smart contract like behavior in the context of an EOA.

During development of a delegator with my team, we realized that since we’re working with ephemeral EOAs, after delegation and initialization of the account the ephemeral key is removed from the system and it’s not possible to use the esdca key in the future.

Here comes the question: how can the user invoke a new implementation for their EOA? The solution is proxy contracts. The user attaches a proxy contract acting as a delegator pointing to an implementation. This means in the future if the user wants to upgrade the current implementation, they can use the upgrade function to invoke a new implementation. Of course, we follow best practices and avoid the risks of the proxy pattern.

Another question arises: how can we be 100% sure that another implementation will have the same pattern and behavior in the proxy contract, with the same logic for updating the implementation? For my core team, we can be trusted and ensure we continuously implement the same pattern in upgraded implementations. But what about other teams or projects? How can we ensure that a user who started with our contract and then upgrades to an implementation not produced by us will still have the upgrade function? Otherwise, the user could end up stuck with the upgraded implementation, since we can’t be sure the next implementation includes an upgrade function.

My thought: we could provide an ERC standard so that all delegator contracts include a function like `upgrade7702proxy`. This would allow an ephemeral EOA to upgrade its implementation at any moment.

Please share your thoughts about this case.

Im starting to plan this ERC draft. How it will be a solution for ephemeral EOAS

Best wishes!

## Replies

**nicocsgy** (2025-06-21):

I don’t see how having such an ERC (which by nature isn’t enforced) improves the trust assumption for end users

---

**nicocsgy** (2025-06-21):

If the answer is the end user just has to read the  ‘upgrade7702proxy’ function to be sure he’s not getting rugged I’m not convinced this moves the needle

---

**0xkoiner** (2025-06-23):

***The issue arises when a new account is created with an ephemeral key:*** there is no way to upgrade the account’s implementation except via the proxy pattern. In cases like Porto or Openfort, which work with ephemeral keys and delegate the owner role to a WebAuthn signer or another EOA (depending on the contract logic), there is no opportunity to attach a new implementation directly upgrades are only possible through a proxy.

The problem appears if the user wants the option to rotate implementations between whitelisted, trusted delegators (designators). I’m not addressing storage slots or admin key validation logic here, but consider this scenario for  user starts with Porto (using WebAuthn as the admin key) and then upgrades to Uniswap. Two issues arise:

1. The user becomes tied permanently to the Uniswap implementation, since it’s now managed by the proxy pattern.
2. Initialization of the new implementation may not activate the current admin key as expected.

**I see two main issues when using ephemeral keys:**

1. The user might upgrade the account and become stuck forever with an implementation that lacks an upgrade function or proxy support.
2. The user could lose access to their assets if the new implementation uses different admin-key access or validation logic.

For these reasons, I believe we need a standard for this case so users can reliably rotate or upgrade their accounts without falling through the cracks or losing access to their assets

