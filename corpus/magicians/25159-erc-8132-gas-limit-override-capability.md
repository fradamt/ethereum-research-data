---
source: magicians
topic_id: 25159
title: "ERC-8132: Gas Limit Override Capability"
author: ajhodges
date: "2025-08-19"
category: ERCs
tags: [erc, wallet, smart-account]
url: https://ethereum-magicians.org/t/erc-8132-gas-limit-override-capability/25159
views: 225
likes: 2
posts_count: 6
---

# ERC-8132: Gas Limit Override Capability

## Abstract

With the introduction of ERC-5792, apps can now request calls to be batched by a Wallet, but there is no way for an app to set a gas limit for those calls. Gas estimation for 5792 batches is currently fully delegated to the wallet. This proposal introduces a capability that restores the ability for apps to specify a gas limit for calls in a 5792 batch, analogous to the `gas` parameter of an `eth_sendTransaction` request.

## Motivation

Some calls can have nondeterministic behavior that make it difficult for a wallet to accurately estimate gas limits for them. Apps have the most context around the calls they are making and can provide reasonable gas limits for them.

## Specification

One new EIP-5792 wallet capability is defined.

### gasLimitOverride Capability

The `gasLimitOverride` capability is implemented by both apps and wallets.

#### Wallet Implementation

To conform to this specification, wallets that implement the `gasLimitOverride` capability:

1. MUST indicate support for the gasLimitOverride capability for all chains (0x0) in their EIP-5792 wallet_getCapabilities response.
2. SHOULD use the app-provided gas limits when processing calls that include them.
3. MUST estimate gas for calls that do not include a gasLimitOverride capability.
4. MAY add additional gas to account for batch processing overhead.
5. MUST return an invalid params error (-32602) if a provided gas limit is zero or exceeds the block gas limit of the target chain.

##### wallet_getCapabilities Response Specification

```typescript
type GasLimitOverrideCapability = {
  supported: boolean;
}
```

###### wallet_getCapabilities Example Response

```json
{
  "0x0": {
    "gasLimitOverride": {
      "supported": true
    }
  }
}
```

#### App Implementation

When an app wants to override the gas limits used for calls in a batch, they SHOULD do this using the `gasLimitOverride` capability as part of an EIP-5792 `wallet_sendCalls` call.

This is a call-level capability. Apps MAY specify gas limits for only some calls in a batch; the wallet MUST estimate gas for any calls that do not include a `gasLimitOverride` capability.

##### wallet_sendCalls Gas Limit Override Capability Specification

```typescript
type GasLimitOverrideParams = {
  value: `0x${string}`; // hex-encoded uint256
}
```

###### wallet_sendCalls Example Parameters

```json
[
  {
    "version": "1.0",
    "chainId": "0x01",
    "from": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
    "calls": [
      {
        "to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
        "value": "0x9184e72a",
        "data": "0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675",
        "capabilities": {
          "gasLimitOverride": {
            "value": "0x1234"
          }
        }
      },
      {
        "to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
        "value": "0x182183",
        "data": "0xfbadbaf01",
        "capabilities": {
          "gasLimitOverride": {
            "value": "0x765"
          }
        }
      }
    ]
  }
]
```

The wallet will then account for these provided gas limits when processing the batch of calls.

## Rationale

The complexities with applying app-supplied gas limits are discussed briefly in the [Rationale section of EIP-5792](https://eips.ethereum.org/EIPS/eip-5792#rationale).

To restate the issue, apps have no context around how calls may or may not be batched by wallets that implement EIP-5792, so they cannot account for any batching overhead. Wallets have low context around the nature of app-provided calls, so they cannot always provide an accurate gas limit.

This proposal allows apps to specify call-level gas limits, and delegates the responsibility of estimating batching overhead (via static analysis or tracing) to the wallet.

### Alternative Approaches

#### Top-level Gas Limit Override Capability

This simplifies the interface somewhat by allowing the app to pass a single gas limit value, but there are a few issues with this approach

1. The app isn’t aware of what batching overhead the wallet might have.
2. Apps would need to sum the call gas limits on their end, which puts more responsibility on the app and more room for error (apps would need to understand that they need to sum gas limits for ALL calls)
3. This wouldn’t be compatible with atomic: false/EOA mode for wallet_sendCalls, where a wallet might be making multiple transactions.

## Backwards Compatibility

- Applications SHOULD only include the gasLimitOverride capability in their wallet_sendCalls requests if they are aware that the wallet supports it (e.g., by checking the wallet_getCapabilities response).
- Applications MAY include the gasLimitOverride capability with optional: true to ensure compatibility with wallets that do not support this capability. When marked as optional, wallets that do not support the capability will ignore it rather than rejecting the request.

## Security Considerations

- Wallets MUST validate that provided gas limits are non-zero and do not exceed the block gas limit of the target chain.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**ajhodges** (2025-08-20):

Some feedback gathered from the AllWalletDevs call:

- ‘gasLimitHint’ makes more sense than ‘gasLimitOverride’, as wallets might choose not to use the app-specified gas limit
- Apps may want to only specify a gas limit for certain calls (not all calls). An example is an approval + swap - the app might not have a gas limit estimate for the approval call of an arbitrary ERC20

Similarly, a wallet wouldn’t have the context needed to produce this estimate for an individual arbitrary call. Maybe the wallet could naively call eth_estimateGas for each unspecified call?

---

**MicahZoltu** (2025-08-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajhodges/48/10747_2.png) ajhodges:

> ‘gasLimitHint’ makes more sense than ‘gasLimitOverride’, as wallets might choose not to use the app-specified gas limit

While we cannot stop the wallet from ignoring gas limits set by apps, why would we want to encourage this behavior? The app has much more context than the wallet for estimating gas costs and if they are supplying a gas limit it is likely because they “know better” than the wallet as to how much gas a transaction may cost when it lands (including things like not being first-in-block).

---

**ajhodges** (2025-08-23):

I tend to agree here. The counterexample that I think was raised during the AllWalletDevs call was that a dex that is batching an approval + swap might not know the approval gas limit for an arbitrary ERC20 token. And that the wallet should absorb this complexity.

But as a wallet dev, it would similarly be difficult for me to pick a gas limit for an arbitrary token approval, and now I have to introspect each call that is passed via wallet_sendCalls.

I think I’d prefer to keep the spec simple by keeping it strict - if any gas limit is provided for any call, they should be provided for all calls. And maybe even change the language that the wallet MUST use the provided gas limit for that calls portion of the batch gas limit.

cc [@azf20](/u/azf20) [@Ivshti](/u/ivshti) - I know you both had thoughts here

---

**MicahZoltu** (2025-08-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajhodges/48/10747_2.png) ajhodges:

> I think I’d prefer to keep the spec simple by keeping it strict - if any gas limit is provided for any call, they should be provided for all calls. And maybe even change the language that the wallet MUST use the provided gas limit for that calls portion of the batch gas limit.

- If a gas limit is provided for a call, that gas limit SHOULD be used.
- If a gas limit is not provided fora call, then the wallet MUST estimate the gas used and use that as the gas limit for that call.

I think these two rules are quite simple, clear, and provide the behavior that we want to see from wallets.  When an app knows better, it provides a gas limit.  When the app doesn’t know better or wants to leave estimation up to the wallet, it simply doesn’t provide a gas limit for that call.

In the approve and call case, the app may not provide a limit for the approve (because it is out of their sphere of intimate knowledge) but they may provide a known limit for the call because that is their own contract that they have deep understanding of.

The reason the first point is a **SHOULD** is because there are situations where the wallet may have additional information.  For example, if you are sending a transaction from a counterfactually deployed contract wallet, or batching transactions with a 7702 transaction, the wallet may know that extra gas will be needed in which case they may take the gas limit provided by the app and increase it by some fixed amount to account for the overhead they know is going to be incurred.

---

**ajhodges** (2026-01-22):

^ *finally* got around to making these changes, and went ahead and put up a draft PR: [Add ERC: Gas Limit Override Capability by ajhodges · Pull Request #1485 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1485)

