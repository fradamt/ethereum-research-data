---
source: magicians
topic_id: 20100
title: "ERC-7715: Grant Permissions from Wallets"
author: pedrouid
date: "2024-05-24"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7715-grant-permissions-from-wallets/20100
views: 3383
likes: 13
posts_count: 9
---

# ERC-7715: Grant Permissions from Wallets

Adds JSON-RPC method for requesting permissions from a wallet

https://github.com/ethereum/ERCs/pull/436/

## Replies

**xinbenlv** (2024-06-12):

In the context of this ERC, How does wallet identify a DApp and ensure it was still the same DApp? It seems to me there are some implied assumptions that i might not know and probably better spell out.

If the assumption is that DApp maintains a secure connection with wallet, that shall be spelled out and investigated I think. For example, a hardware wallet could be connected to an offline DApp that only signs TX signature and be distributed in less common ways

---

**jayk** (2025-01-21):

Is there still active work on this proposal? One question I have: this standard defines an `expiry` for the session end time, but I’m thinking providing an additional constraint on the start time would be useful. Similar to how we have `validAfter` and `validUntil` in ERC-4337. Thoughts?

---

**lukaisailovic** (2025-01-22):

[@jayk](/u/jayk) Its being actively worked on. Do you think `validAfter` should be at the top level request? IMO Its more fitting in the specific permission like this:

```auto
 permissions: [
          {
            type: 'native-token-transfer',
            data: {
                allowance: '0x1DCD6500',
                validAfter: 1737550474
            }
          }
        ],
```

---

**jayk** (2025-01-22):

Thanks for the response! Curious - what would be the use case for being able to specify different `validAfter`s for different permissions? Would we also want to specify different `validUntil`s for each as well then?

In the context of session keys, it seems simpler to think about a valid range at the key level, during which all of the permissions it has been granted is valid. Put another way, this would be equivalent to having time range be an additional permission which must be checked for each action. This is how Alchemy and ZeroDev do it today, with [TimeRangeModule](https://github.com/alchemyplatform/modular-account/blob/bd75c9eca7ff5a66aaebc3cf2dab43ddc4622482/src/modules/permissions/TimeRangeModule.sol#L38) and [TimestampPolicy](https://github.com/zerodevapp/kernel-7579-plugins/blob/fa82c08748ff591767cbcbda98142415bfb4b3b3/policies/timestamp/src/TimestampPolicy.sol#L17), respectively.

---

**lukaisailovic** (2025-01-26):

If you check out the 7715 spec, currently we have `RateLimitPermission` for example in the spec. I think ZeroDev and Alchemy would map their permissions to a top level ones.

`validUntil` is the expiry and `validAfter` can be modeled as a separate permission.

---

**glitch-txs** (2025-02-19):

Given the fact that crypto assets are usually very volatile, would there be a way to update the permissions on the go?

---

**V00D00-child** (2025-06-23):

The 7715 spec is a significant value add to the wallet layer. However, during the implementation of the [first iteration in MetaMask](https://github.com/MetaMask/snap-7715-permissions), I encountered a few pain points that I believe could hinder broader adoption.

I’ve opened a PR against the spec proposing some minor modifications to help make the standard more manageable for wallet implementations.

Feedback is welcome!



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1098)














####


      `master` ← `V00D00-child:chore/simplify-7715`




          opened 03:23PM - 17 Jun 25 UTC



          [![](https://avatars.githubusercontent.com/u/34751375?v=4)
            V00D00-child](https://github.com/V00D00-child)



          [+187
            -197](https://github.com/ethereum/ERCs/pull/1098/files)







This PR proposes simplifications to the ERC-7715 specification to support a more[…](https://github.com/ethereum/ERCs/pull/1098) manageable implementation across wallets.

For additional context and rationale behind these changes, please refer to the supporting document: [Proposal to Simplify ERC-7715](https://metamask-consensys.notion.site/Proposal-to-Simplify-ERC-7715-215f86d67d688041b580dd161968b2df?pvs=143)

---

**justus** (2025-07-07):

ERC-7715 describes the `PermissionResponse` as being a (presumably TypeScript-like) union of the `PermissionRequest` type with additional properties. A `PermissionRequest` is a list of objects. Is it the author’s intention here to make the `PermissionRequest` a list of objects, as well? See the following for an excerpt from the document:

```tsx
type PermissionRequest = {
  chainId: Hex; // hex-encoding of uint256
  address?: Address;
  expiry: number; // unix timestamp
  signer: {
    type: string; // enum defined by ERCs
    data: Record;
  };
  permissions: {
    type: string; // enum defined by ERCs
    data: Record;
  }[];
}[];
// union of list and properties
type PermissionResponse = PermissionRequest & {
  context: Hex;
  accountMeta?: {
    factory: `0x${string}`;
    factoryData: `0x${string}`;
  };
  signerMeta?: {
    // 7679 userOp building
    userOpBuilder?: `0x${string}`;
    // 7710 delegation
    delegationManager?: `0x${string}`;
  };
};
```

