---
source: magicians
topic_id: 25199
title: "ERC-8009: Proxy Clear Signing"
author: nagydani
date: "2025-08-21"
category: ERCs
tags: [erc, security, blind-signing]
url: https://ethereum-magicians.org/t/erc-8009-proxy-clear-signing/25199
views: 203
likes: 6
posts_count: 17
---

# ERC-8009: Proxy Clear Signing

The new standards proposal aims to solve the vulnerability of blind signing for a large fraction of use cases, when a user must sign a transaction sent to a smart contract unknown to their hardware wallet. The hardware wallet will be able to display a list of constraints consisting of ETH and ERC-20 token balances or balance changes after the execution of the transaction, with a guarantee that if these constraints are not met, the transaction will revert, only imposing a gas cost on the user.

## Abstract

Introduce a singleton, stateless contract that proxies arbitrary smart‑contract calls and enforces user‑supplied outcome constraints. The proxy supports **absolute post‑balance thresholds** and **balance‑difference (delta) checks** over native ETH and ERC‑20 balances. Calls that violate the declared constraints MUST revert.

## Motivation

Current hardware wallets struggle to present meaningful transaction information when interacting with unknown or newly deployed smart contracts. Without prior knowledge of a contract’s ABI or address, these devices can only display raw hexadecimal calldata - an unreadable and unsafe experience for most users. This practice, known as blind signing, leaves users vulnerable to unintentionally approving malicious or incorrect transactions. This vulnerability has already been exploited in high-value attacks.

Instead of parsing transaction calldata, the proposed approach focuses on verifying expected balance differences after execution. This proposal introduces an alternative path to clear signing - defined here as the ability for users to verify the outcome of a transaction before signing, without requiring ABI knowledge. By routing calls through a singleton proxy contract that enforces these expectations on-chain, hardware wallets can reliably display the “balance after transaction” values to the user, taken from the smart-contract parameters. This enables a permissionless, scalable, and understandable transaction confirmation experience, even for unknown contracts.

## Replies

**nagydani** (2025-08-21):

The PR containing the ERC is [here](https://github.com/ethereum/ERCs/pull/1184/). An ERC number is yet to be assigned.

---

**zergity** (2025-08-29):

Yes, blind signing is bad, and we should address it.

Yes, “balance after transaction” check is a good solution, but it’s still blind signing, because the function args require comprehensive display from wallets, especially with hard wallets.

I believe this contract should be callled “router” instead of “proxy”. Because it holds token approval and spent them the same way DeFi peripheral router contracts do. The exactly same idea is proposed, implemented and audited 3 years ago: [ERC-6120: Universal Token Router](https://eips.ethereum.org/EIPS/eip-6120).

But to completely remove the blind signing UX, we need something like this: [ERC-TBD: Intent-Based State Transition](https://ethereum-magicians.org/t/erc-tbd-intent-based-state-transition/24934).

---

**nagydani** (2025-09-06):

After reviewing ERC-6120, we came to the conclusion that it is not the exact same thing. In particular, our proposal does not require the deployment of a routing contract for each smart contract, but only one proxy contract. Also, it has been designed with hardware wallets in mind to be able to display constraints in a user readable fashion. In fact, supporting firmware development for several hardware wallets is in progress.

---

**zergity** (2025-09-06):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/n/c5a1d2/48.png) nagydani:

> does not require the deployment of a routing contract for each smart contract, but only one proxy contract

Same, there’s only 1 single ERC-6120 contract is deployed for all applications.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/n/c5a1d2/48.png) nagydani:

> supporting firmware development for several hardware wallets is in progress.

It’s a long shot to even think that some hardware wallets will make changes to “parse a part of calldata to display something” (with an ABI or a common pattern). If that’s posible, 6120 already have that, wallets can just parse the calldata to display the balance outputs.

Meanwhile, the Intent-based State Transition can display readable intents in clear text on hardware wallets using ̀eth_sigǹ (or 712) that already being standard for every wallets.

---

**markvirchenko** (2025-09-08):

The ERC-6120 contract has several issues that make it unusable for the balance-based clear signing on the hardware wallets.

The first issue is that ERC-6120 only allows to check for positive changes in balances. So, if I want to make a constraint saying “I should not lose more than 1 eth as the result of this transaction”, we cannot use ERC-6120 for that, neither can we use it for a constraint saying “my balance after the transaction should be X USDC”

Yes, ERC-6120 is one for all applications. But the applications have to either implement “NotToken” marker, or 0x61206120 ERC-165 marker.

If they don’t, one would need to write a custom helper contract like the one you showed in your proposal (uniswap v2/v3)

Another thing to mention is that ERC-6120 requires Cancun, so it is not that scalable (not all EVM networks will be supported).

The ERC-8009 however, is less generic, but that’s also a bonus as it will be more gas-efficient and has potential for even better gas-efficiency than the reference implementation.

---

**zergity** (2025-09-08):

Do users need to approve their tokens to the Proxy contract?

---

**markvirchenko** (2025-09-08):

They don’t need, it is optional. They can.

---

**zergity** (2025-09-08):

Here’s a critical vulnerability for you:

When the user approve tokens to the Proxy, anyone can **steal all the tokens** by sending transactions like this:

```auto
proxy.proxyCall(
  [...],
  [...],
  tokenAddress,
  abi.encodeFunction("transferFrom", ...),
  [...]
)
```

---

**markvirchenko** (2025-09-08):

Thank you, I see. I will make edits to the contract

---

**wjmelements** (2025-09-08):

Whatever balance you don’t check is the one that will be drained.

---

**markvirchenko** (2025-09-09):

We expect hardware wallets to display the balance constraint parameters on their screens. So if a certain token balance delta / value is not displayed on the screen, the person holding the hardware wallet is expected to discard the transaction.

---

**wjmelements** (2025-09-09):

For comparison, there was once a smart contract that only made sure that its weth balance increased at the end of a transaction and was otherwise permissionless. But this didn’t check approvals and so it was drained.

> So if a certain token balance delta / value is not displayed on the screen, the person holding the hardware wallet is expected to discard the transaction.

The simulation might show some expected behaviors, but the transaction might behave much differently during execution. For example I once had a honeypot that would behave differently according to `COINBASE` to take advantage of some defaults that were in use by some frontrunning bots, though many environmental parameters can be used for this purpose. So the user would still approve the transaction, and it would pass the checks, but it can take additional actions that are not checked, for example stealing unrelated NFTs or approving someone to steal your tokens.

I don’t think this problem can be solved in the general case because it reduces to the halting problem.

---

**zergity** (2025-09-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> But this didn’t check approvals and so it was drained.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> So the user would still approve the transaction, and it would pass the checks, but it can take additional actions that are not checked, for example stealing unrelated NFTs or approving someone to steal your tokens.

How do these things happen? Is it because the arbitrary call from the generalized “Proxy” contract?

---

**wjmelements** (2025-09-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zergity/48/3631_2.png) zergity:

> How do these things happen? Is it because the arbitrary call from the generalized “Proxy” contract?

They happen because balance checks are insufficient to verify safe execution, and because faith in those checks creates a false sense of security.

---

**markvirchenko** (2025-12-22):

Hello everyone, and thanks for providing the valuable input above.

We have revised the ERC thanks to your comments. Some of the major changes are:

1. Splitting core/periphery to fix the issue with transferFrom vulnerability, thanks @zergity
2. The UI parameters are now solely the responsbility of the periphery contracts. The core contract doesn’t think about UI, and it also doesn’t even think about how exactly it receives the balance that it uses in its transactions.
3. Depending on the target contract intended to be called, one can provide ‘transfer’ flag - meaning that the balance will be not approved to the target contract, but rather transferred right away. This allowed, for instance, uniswap to function fully in all scenarios with our proxy contract.

We have also updated the PR, with new contracts & new ERC file.

The PR has been moved to ‘Review’

---

**markvirchenko** (2025-12-22):

btw, I think we didn’t upload these two links before, but here they go:

1. https://erc8009.xyz/ ← Documentation
2. https://app.erc8009.xyz/ ← Proxy dApp

