---
source: magicians
topic_id: 19599
title: "ERC-7682: Auxiliary Funds Capability"
author: lsr
date: "2024-04-09"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7682-auxiliary-funds-capability/19599
views: 1314
likes: 1
posts_count: 5
---

# ERC-7682: Auxiliary Funds Capability

## Abstract

An EIP-5792 compliant capability that allows wallets to indicate to apps that they have access to funds beyond those that can be accounted for by looking up balances onchain given the wallet’s address.

## Motivation

Many applications check users’ balances before letting them complete some action. For example, if a user wants to swap some amount of tokens on a dex, the dex will commonly block the user from doing so if it sees that the user does not have that amount of tokens at their address. However, more advanced wallets have features that let users access funds from other sources. Wallets need a way to tell apps that they have access to additional funds so that users using these more advanced wallets are not blocked by balance checks.

## Specification

One new EIP-5792 wallet capability is defined.

### Wallet Implementation

To conform to this specification, wallets that wish to indicate that they have access to auxiliary funds MUST respond to `wallet_getCapabilities` calls with an `auxiliaryFunds` object with a `supported` field set to `true` for each chain they have access to auxiliary funds on. This specification does not put any constraints on the source of the auxiliary funds.

#### wallet_getCapabilities Response Specification

```typescript
type AuxiliaryFundsCapability = {
  supported: boolean;
}
```

##### wallet_getCapabilities Example Response

```json
{
  "0x2105": {
    "auxiliaryFunds": {
      "supported": true
    },
  },
  "0x14A34": {
    "auxiliaryFunds": {
      "supported": true
    }
  }
}
```

### App Implementation

When an app sees that a connected wallet has access to auxiliary funds via the `auxiliaryFunds` capability in a `wallet_getCapabilities` response, the app SHOULD NOT block users from taking actions on the basis of asset balance checks.

## Rationale

### Alternatives

#### Advanced Balance Fetching

An alternative we considered is defining a way for apps to fetch available auxiliary balances. This could be done, for example, by providing a URL as part of the `auxiliaryFunds` capability that apps could use to fetch auxiliary balance information. However, we ultimately decided that a boolean was enough to indicate to apps that they should not block user actions on the basis of balance checks, and it is minimally burdensome for apps to implement.

The shape of this capability allows for a more advanced extension if apps feel more functionality is needed.

#### Auxiliary Funds per Asset

We could also specify auxiliary funds support per asset. We decided against this because this list could get quite large if a wallet has auxiliary funds supports for many assets, and a single boolean should be enough for apps to not block users from taking actions.

## Security Considerations

Apps MUST NOT make any assumptions about the source of auxiliary funds. Apps’ smart contracts SHOULD still, as they would today, make appropriate balance checks onchain when processing a transaction.

## Replies

**bumblefudge** (2024-04-13):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/l/58956e/48.png) lsr:

> When an app sees that a connected wallet has access to auxiliary funds via the auxiliaryFunds capability in a wallet_getCapabilities response, the app SHOULD NOT block users from taking actions on the basis of asset balance checks.

Wait, so any wallet that self-attests to having auxFunds SHOULD just be exempted from balance-checks?  I was expecting, when I got this far in the spec, to see a logic provided for checking those auxFunds against the balance check amount instead… this might be clearer with at least an illustrative advanced balance-fetch pseudocode or something?

---

**MilkyTaste** (2024-11-17):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/l/58956e/48.png) lsr:

> the app SHOULD NOT block users from taking actions on the basis of asset balance checks

Could we update this ERC to include an optional `balance`? The current approach implies the wallet has access to unlimited funds.

```auto
type AuxiliaryFundsCapabilityAsset = {
  address: `0x${string}`;
  balance?: `0x${string}`; // hex max available
}
type AuxiliaryFundsCapability = {
  supported: boolean;
  assets?: AuxiliaryFundsCapabilityAsset[];
}
```

---

**MilkyTaste** (2024-11-17):

The way this ERC is written, it is currently only usable by the front end. If the capability is sent in 5792’s `wallet_sendCall` request, the back end would be prompted to check / obtain / use the auxiliary funds.

I don’t think the back end should be assuming auxiliary funds are always accessed and explicit request would be better.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5792#wallet_sendcalls-rpc-specification)





###



Adds JSON-RPC methods for sending multiple calls from the user's wallet, and checking their status










```auto
[
  {
    "version": "1.0",
    "from": "0x...",
    "calls": [
      {
        "to": "0x...",
        "value": "0xde0b6b3a7640000", // 1e18
        "data": "0x...",
        "chainId": "0x01"
      }
    ],
    "capabilities": {
      "auxiliaryFunds": {
        "assets": {
          "address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
          "amount": "0xde0b6b3a7640000" // 1e18
        }
      }
    }
  }
]
```

---

**ArikG** (2025-08-18):

I only recently found this ERC and I really like the value it can bring. I believe it is very useful for a number of situations (some of which may or may not have been considered by the authors, but all are relevant):

1. Omnibus Wallets – Where a service provider keeps funds for retail users that they can use in DeFi operations (e.g. Magic Spend)
2. HD Wallets – Where users can have funds in multiple derivations of the same private key.
3. WAAS services - Where users might have access to multiple wallets by different keys that are still manages on the same system.
4. Privacy Wallets – Where some of the user’s funds are in private assets on the same wallet but not visible to the dApp.
5. Chain Abstraction Wallets – With funds on other chains and a “unified balance”.

I am assuming this EIP was born from Magic Spend as a core usecase, but would like to acknowledge  all of these as first class citizen usecases.

A few thoughts I want to raise:

### 1. Privacy

The current approach feels somewhat reversed from what I’d expect from first principles. Ideally, applications should not assume knowledge of my wallet balance - ever. Such assumptions quickly become outdated and compromise user privacy. Amazon does not check my balance before allowing me to buy something. It’s crazy that this is the norm.

- Suggestion: EIP-7682 compatibility should mean that apps either:

Support auxiliary funds by default, or (new)
- Support them if a wallet requests it (current spec in the ERC)

Both should be valid, but the first approach (default to privacy) is preferable. This would encourage the ecosystem to move towards stronger respect for user privacy instead of just incremental improvements on UX for existing UX).

### 2. Required Assets Parameter

The `requiredAssets` parameter feels underspecified for real-world use. Critical information is missing, such as:

- Slippage
- Deadline / time-to-fulfillment

Without these, there may be situations where auxiliary funds are fetched (e.g., taking 10 minutes), but the transaction validity is unclear. This risks making `requiredAssets` impractical in production scenarios. While adding these details complicates the spec, they may be necessary.

### 3. Amounts for ERC-721

It’s unclear why we need an amount field for ERC-721. Perhaps the default should be `0x01` with an optional override for extreme cases (if such cases even exist).

### 4. Transaction Validity and Nonce Issues

There may be scenarios where fetching auxiliary funds requires transactions that could invalidate the signature being requested by the dapp. While I don’t have a concrete example, it seems possible.

Maybe we want to add clarification which methods of aux funds are compatible with this flow? For example, is increasing the account nonce allowed or not during the process? not sure about other relevant conditions.

This may be a minor issue, but worth specifying.

### 5. Security & Reorg Risks

If apps rely on users bringing in funds on-the-fly, we may encounter risks such as:

- Funds appearing to arrive but later being invalidated due to a chain reorg or some other more malicious “trick”.
- Question: Do we assume apps are responsible for protecting themselves against such risks, or should the ERC address this concern directly? I am asking because we are bascially pushing apps towards support ad-hoc aux funds, and that can add risks.

Appreciate your thoughts on this

