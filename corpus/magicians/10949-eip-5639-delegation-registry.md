---
source: magicians
topic_id: 10949
title: "EIP-5639: Delegation Registry"
author: wwhchung
date: "2022-09-20"
category: EIPs
tags: [signatures, registry]
url: https://ethereum-magicians.org/t/eip-5639-delegation-registry/10949
views: 2457
likes: 6
posts_count: 3
---

# EIP-5639: Delegation Registry

This is the discussion thread for EIP 5639: Delegation Registry, which allows for d elegation of permissions for safer and more convenient signing operations.

EIP found here:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5639)





###



Delegation of permissions for safer and more convenient signing operations.

## Replies

**sbauch** (2022-10-03):

I really appreciate the thoughtfulness and work that’s gone into the deployed protocol and the EIP - I’ve been playing around with the project the past few days to see what it would be like to compose into a project I’m working on.

I’d encourage supporting EIP-2771 meta-transactions so that users can create or revoke delegations gas free.

**My Context**

I’m building in the gaming space. We’re using a project from [Audius named Hedgehog](https://hedgehog.audius.org/) to offer users a persistent burner wallet.

Users can then delegate permission from a primary EOA to the burner wallet so that burner address can “use” the primary EOA NFTs in games. The burner wallet uses private keys in browser to sign messages for our meta-transaction stack, so users can take game moves without any wallet popup.

We currently use our own very simple delegation protocol - delegations are stored on chain so that our protocol can verify delegation.

I see a lot of value in composing a global registry for this delegation, and kept our version very simple in the hopes something like this would come along. I’ve updated our protocol to use the same interface - should that be standardized through this EIP, we’d be able to easily swap out spec-compliant registry providers, but again see so much value in composing the global registry.

**Meta-Transaction Support**

A blocker for us using delegate.cash or another protocol based on this EIP is that there is not support for meta-transactions when creating or revoking delegation. A delegation transaction would be the only transaction in our entire experience that requires a user to pay for gas. We are building cross-chain tooling, so will be doing delegations on L2s where gas tokens may be frustrating to acquire.

I think the delegate.cash team is mixing the concepts of off-chain registry and meta-transaction support? I’m not suggesting off-chain storage of delegations, and believe that adding this support helps possible adoption without sacrificing anything and with minimal overhead.

**Example**

I spiked out what this would look like and addressed some of the signature pushback from the project README in a pull request on my fork - [Adds meta-transaction support to DelegationRegistry by sbauch · Pull Request #1 · 0xEssential/delegation-registry-meta-tx · GitHub](https://github.com/0xEssential/delegation-registry-meta-tx/pull/1)

Perhaps this is a moot point given delegate.cash having been deployed already, and I’m not sure it makes a ton of sense for an EIP to specify supporting meta-transactions. But it just feels like something that is 99% what we need off the shelf, and would hate to roll our own for that 1%, so figured a conversation couldn’t hurt - apologies if this isn’t the right place for it.

---

**SanLeo461** (2023-03-25):

Is there any reason why the addresses for delegation events are not indexed to ease searching of logs?

i.e.

```auto
    /// @notice Emitted when a user delegates their entire wallet
    event DelegateForAll(address vault, address delegate, bool value);

    /// @notice Emitted when a user delegates a specific contract
    event DelegateForContract(address vault, address delegate, address contract_, bool value);

    /// @notice Emitted when a user delegates a specific token
    event DelegateForToken(address vault, address delegate, address contract_, uint256 tokenId, bool value);

    /// @notice Emitted when a user revokes all delegations
    event RevokeAllDelegates(address vault);

    /// @notice Emitted when a user revoes all delegations for a given delegate
    event RevokeDelegate(address vault, address delegate);
```

Should be

```auto
    /// @notice Emitted when a user delegates their entire wallet
    event DelegateForAll(address indexed vault, address indexed delegate, bool value);

    /// @notice Emitted when a user delegates a specific contract
    event DelegateForContract(address indexed vault, address indexed delegate, address indexed contract_, bool value);

    /// @notice Emitted when a user delegates a specific token
    event DelegateForToken(address indexed vault, address indexed delegate, address indexed contract_, uint256 tokenId, bool value);

    /// @notice Emitted when a user revokes all delegations
    event RevokeAllDelegates(address indexed vault);

    /// @notice Emitted when a user revoes all delegations for a given delegate
    event RevokeDelegate(address indexed vault, address indexed delegate);
```

