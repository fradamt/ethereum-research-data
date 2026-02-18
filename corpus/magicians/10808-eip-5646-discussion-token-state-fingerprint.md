---
source: magicians
topic_id: 10808
title: "EIP-5646 Discussion: Token state fingerprint"
author: ashhanai
date: "2022-09-11"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5646-discussion-token-state-fingerprint/10808
views: 2966
likes: 4
posts_count: 9
---

# EIP-5646 Discussion: Token state fingerprint

![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5646)





###



Unambiguous token state identifier










DeFi protocols currently do not have a convenient way to identify tokens that derive value from underlying assets unambiguously. Examples of such tokens in the context of this EIP are derivative tokens (tokenized LP positions, token bundles) or, more generally, tokens that could change their state without changing their token identifier.

For example, imagine a token bundle with ten rare tokens and the same bundle after withdrawing nine of them. The bundle will most likely not change its token identifier. However, it is evident that the intrinsic value of the bundle has changed (bundlers could be implemented differently, but you get the gist). To prevent bundle owner from receiving an offer, withdrawing most of the intrinsic value out, and then accepting the offer, DeFi protocols can currently do one of two things:

1. Wrap derivative token
2. Know derivative token implementation details

## Wrap derivative token

A protocol can prevent a token owner from modifying the token state by forcing the user to wrap its derivative token first. However, that creates additional inconveniences. First is the inability to use tokens utility that does not change the state (e.g., voting, token gated access, potential airdrops). Second, unnecessary wrapping and unwrapping transactions cost gas.

## Know derivative token implementation details

DeFi protocol can have the knowledge of bundle state properties and include them in a proposed offer. That unambiguously identifies the bundle and its state and prevents the owner from accepting an offer after modifying the bundle.

However, protocols need to add support for every new derivative token, which leads to an obvious bottleneck.

[![support-per-abi](https://ethereum-magicians.org/uploads/default/original/2X/7/735098806d072995220bf2796cbfe9293b9ce9c9.png)support-per-abi681×242 9.97 KB](https://ethereum-magicians.org/uploads/default/735098806d072995220bf2796cbfe9293b9ce9c9)

## Solution: Token State Fingerprints

By defining a simple getter function for a token state fingerprint, DeFi protocols can use it and support derivative tokens without knowing the implementation details. It removes the bottleneck issue with new derivative tokens.

[![support-per-eip](https://ethereum-magicians.org/uploads/default/original/2X/8/8401c991aeee20cd1e637bb84e67ed4aabda8ed2.png)support-per-eip681×242 8.59 KB](https://ethereum-magicians.org/uploads/default/8401c991aeee20cd1e637bb84e67ed4aabda8ed2)

This standard does not define *how* should be the `getStateFingerprint` function implemented. For example, a simple hash of an abi encoded state parameters could be enough as a state fingerprint. However, some tokens could implement a more gas-efficient way for their specific state. For example, some implementations could compute the fingerprint on the fly, whereas others can store it and update its value with every state-mutating call.

It is unnecessary to prevent state fingerprint collision between two different token contracts as state fingerprints should be compared only in the context of one token contract. Because of that, an implementation does not have to include any domain separators.

This standard can be implemented by EIP-721, EIP-1155, or any other token contract that identifies tokens via `uint256` value.

Contrary to EIP-1948, this standard does not define a function for directly updating state fingerprints. Instead, the intention is to update state fingerprints only via state-mutating calls.

Compared to [Non-Fungible Token State Verification](https://github.com/ethereum/EIPs/issues/1180), this standard leaves token state fingerprint composition to developers. As a result, it should lead to easier adoption of the standard as protocols do not have to compose the state fingerprint themselves.

Two possible workarounds exist for already deployed tokens that cannot implement this EIP directly.

1. Token developers can deploy an auxiliary contract, implementing EIP-5646 and promoting it as an official extension.
2. Protocol developers can deploy their auxiliary contract implementing EIP-5646 for every supported token.

In both these cases, the protocol has to support tokens specifically.

It works well with other standards. Take EIP-4400 as an example. State fingerprints can include consumer addresses and will be updated every time the consumer address changes.

## Open questions

- Should EIP-5646 define a StateFingerprintUpdate event that is emitted on state fingerprint change? The event cannot cover 100% of updates (e.g., when the state depends on a block.timestamp, or oracle value).

## Replies

**vorcigernix** (2022-12-03):

This sounds better than mentioned EIP-1948, defining the way to update as a part of standard could be restrictive. On the other hand, some sort of DSL example that describes the use case for eg cryptokitties would be helpful (at least to me to understand the implementation part).

---

**ashhanai** (2022-12-07):

Defining the DSL would be another level of complexity, which is not part of this EIP. If we want to keep the premise of not knowing the implementation details of the mutable token, the function would have to accept an encoded data about state properties and return bool as an indicator if the conditions are met or not.

I currently don’t have an example of such DSL, but it can heavily inspired by [EIP-1180](https://github.com/ethereum/EIPs/issues/1180).

---

**ashhanai** (2022-12-07):

1. I updated the EIP to mention mutable tokens instead of derivative tokens, as I believe it’s broader set of tokens.
2. I changed one requirement of the getStateFingerprint function to include all state properties that are mutable (can change during the lifecycle of the token).

---

**ashhanai** (2022-12-13):

Moved this EIP to last call with deadline on 21.12.2022, any feedback appreciated.

---

**deadm3m3** (2022-12-13):

No feedback on EIP but wanted to compliment you on your presentation on Eth Cat Herders.  Was very informative and well done.  I’m just starting my crypto journey.  I learned not only your EIP proposal but also the underlying tech and the issue you are trying to solve.  You have a real talent for presenting/instructing technical issues in a simple and understandable way.  Thank you for the effort you put into that and good luck with the proposal!

---

**ashhanai** (2022-12-14):

Thank you, really appreciate that. I’m glad it was helpful to you ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**ashhanai** (2022-12-20):

Linking [PEEPanEIP video](https://www.youtube.com/watch?v=bb9exDj5CVk) [@deadm3m3](/u/deadm3m3) mentioned earlier.

---

**ashhanai** (2023-01-24):

This EIP just become Final ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=12)

