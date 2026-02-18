---
source: ethresearch
topic_id: 23876
title: "Crypto Native Cash: Bridging physical Cash and DeFi"
author: Citrullin
date: "2026-01-18"
category: Applications
tags: []
url: https://ethresear.ch/t/crypto-native-cash-bridging-physical-cash-and-defi/23876
views: 162
likes: 2
posts_count: 3
---

# Crypto Native Cash: Bridging physical Cash and DeFi

The Ethereum Ecosystem struggle to bridge between on-chain value and everyday usability.

While NFC wallets (like Tangem, Citizen Wallet or Ledger backups) have introduced contactless interactions, they often remain tied to traditional wallet paradigms.

This proposal introduces **Crypto Native Cash (Native Cash)**. A system that binds on-chain value to physical objects. Such as banknotes.

Realized through Account Abstraction (ERC-4337), NFC, and a multi-layered governance model to **enable the immediacy of paper cash** in DeFi while providing the programmable security of crypto.

This creates a hybrid economy where Central Bank regulated safety meets the programmable flexibility and decentrality of DeFi.

## Motivation

For mainstream adoption, DeFi must map to existing human patterns of tangibility and offline transferability.

The goal is to create a banknote that costs approximately 0.3 EUR at maximum to produce, is collectible, and operates in a L1/L2/L3 sync composability environment.

By separating the account from a single private key, we can create a system that mirrors the relationship between a citizen and a central bank.

## Governance Model

The model moves away from the single private key model, which is too fragile for physical objects and common usability patterns.

Instead, the Smart Account governed by three keys:

1. Key A: Physical Possession (NFC tag/NFC Banknote)

A private key derived from an NFC chip’s UUID or embedded in the data payload.
2. This key is required to sign payment intents but has no ownership authority. It can only spend within policy constraints.
3. Key B: Authority (Central Bank/Guardian)

A revocable authority held by a central bank, banking consortium, DAO, or parent
4. This key enforces AML policies, sets spending thresholds, and acts as a kill switch to freeze the account if the physical item is lost.
5. Key C: Ownership (Economic Claim)

An on-chain claim (can be a DAO or NFT too) that holds the ultimate right to the assets.
6. It can transfer the account, reclaim funds, or request to upgrade authority rules

[![image](https://ethresear.ch/uploads/default/original/3X/7/c/7ccc50b0c27e9b0f894290f8e6535bccd4945616.png)image866×577 23 KB](https://ethresear.ch/uploads/default/7ccc50b0c27e9b0f894290f8e6535bccd4945616)

## Movement and the Physical Lifecycle

The core idea is to bind the tokens to a smart account and physical item.

This allows for two distinct modes of movement:

1. Physical P2P Transfer (Off-Chain Possession)
Because the value is bound to the physical banknote (Key A), possession of the object implies the right to use it for small, cash-like payments.

Trustless Verification: Recipients can check the on-chain status of the banknote to ensure the funds haven’t been frozen or revoked by the Authority (Key B).
2. Low Friction: No complex device setup is needed for small payments, mirroring the simplicity of paper cash. Only moving the Economic Claim around.

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/b/9badd791496dda5237fad3dbc1d7a6b3e083dd72_2_690x345.png)image1000×500 15.9 KB](https://ethresear.ch/uploads/default/9badd791496dda5237fad3dbc1d7a6b3e083dd72)

1. Destructive Settlement
To move the on-chain value to a new address, the current physical object must be killed on-chain by destroying the physical item.

Revocation and Reissue: The old Key A is permanently removed from the Smart Account’s validation logic, and a new one is added. The added key has be the owner of the Economic Claim.
2. Symbolic Destruction: The physical destruction of the banknote is mostly symbolic, but serves an important part for the physical economy.
Therefore this process has to happen in a temperproof environment. The on-chain movement is the real mechanism that prevents double-spending.
An physical exchange can be used as intermediary here. Providing another layer of privacy, yet auditable physical and digital trace.
AML policies set by the authority apply here. The Authority may freeze the assets or block transfers.

[![image](https://ethresear.ch/uploads/default/optimized/3X/8/7/872961c96a2820bcf65a81a06a13a945737bde07_2_690x345.png)image1000×500 12.9 KB](https://ethresear.ch/uploads/default/872961c96a2820bcf65a81a06a13a945737bde07)

## Transaction Flows: From Micropayments to Regulated Transfers

- Small Payments (cash like): The physical tag (Key A) signs a payment intent within an allowed threshold. No external approval is needed, enabling instant, physical exchange.
image1000×500 15.9 KB
- Medium/Large Payments (Authority Approved): Transactions exceeding a threshold require Key B (Authority) and/or Key C (Economic Claim) to approve or reject the move.
This protects against large-scale theft or money laundering while maintaining the cash UX for daily needs.
image1000×500 17.7 KB

## Dealing with physical Loss

Unlike physical Central Bank notes, losing a Crypto Native Cash does not necessarily mean losing the funds.

- Freezing: The Authority (Key B) can invalidate the functional permissions of the lost Key A.
- Safety: The funds remain safely bound to the Smart Account, accessible to the owner (Key C) through a higher-trust recovery process
Key C (owner of the assets) can request to issue a new NFC tag and link it to the existing assets, maintaining the same on-chain identity.

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/c/1c59344039d25f17c9dfe8629f051030fb409c39_2_690x345.png)image1000×500 16.2 KB](https://ethresear.ch/uploads/default/1c59344039d25f17c9dfe8629f051030fb409c39)

## Security and Programmability

This architecture introduces features that traditional paper cash lacks:

- Threshold Signatures (FROST or Threshold ECDSA): Enables T-of-N approvals so multiple guardians (a family or DAO) must approve high-value moves. Authorities may be inherited.
- Revenue Splits: Automated on-chain distribution of fees to vending operators, designers, and investors. Destructive Settlment on-chain within the vending machine.

## Psychological Onboarding into web3

To normalize the idea of programmable cash, we must engage users through tactile feedback and playful interactions.

A psychological approach is need to break holdl culture apart and using available liquidity in existing economic systems.

- Gamified Distribution: Using Gachapon vending machines to dispense crypto native cash that can be used to buy “tinyblock” kits or other physical collectibles
- Tactile Feedback: Kits that interact with the crypto native cash (using lights or sound) link the physical object to its on-chain identity, turning a technical interaction into a social one
- Authenticity: Physical collectibles can be linked to digital collectiable (e.g. NFTs), making the banknotes collectible assets in their own right.
Evolving NFTs that change with the velocity can further embrace the psychological component and motivate people to spent their crypto native cash.

This model enables the Ethereum ecosystem a path to create not only the digital economy, but the physical one. It enabled a regulated, user-friendly bridge that feels exactly like the cash we already know, but with the security of the future.

## Replies

**mmjahanara** (2026-01-20):

crypto native cash is a very important topic, time and time again we are reminded that cashless model breaks down in extreme scenarios like war, natural disaster, etc. (I was reminded of this tweet by [@vbuterin](/u/vbuterin) https://x.com/VitalikButerin/status/1926616257094091216)

However, the ability to transact completely offline is the hardest and perhaps the most important part of the problem, which is not addressed in this proposal since the recipients need to check on-chain status of the banknote … .

---

**Citrullin** (2026-01-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/mmjahanara/48/1593_2.png) mmjahanara:

> However, the ability to transact completely offline is the hardest and perhaps the most important part of the problem, which is not addressed in this proposal since the recipients need to check on-chain status of the banknote … .

Okay, let’s go through the scenarios. A big one is world war etc.

In this extreme scenario, the on-chain state wouldn’t be a concern any more. The banknote still has other security features it maintains. You can settle it once the war is over and just assume they are mostly valid. The country or DAO entity can also issue new banknotes and force the old ones to get settled. Using this as an opportunity to detect fraud, money laundering etc. The Cash-like small payments only require key A any way. The other keys are only used to resolve conflicts within a window. Arguably in that total collapse scenario, the whole Ethereum ecosystem would be dead any way.

What about partially offline scenarios?

Cash-like applies here of course too. So, if you hand a 5, 10, or 100 bill, it’s still to assume the key on there is enough to settle the transaction. You can just settle it once you got a connection again. A PoS, Smartphone, or some other device, still can keep the last state of the chain it receives. You can check the last on-chain state and verify if the banknote was included in that. Additionally, you may also carry proof in the data payload of the chip.

I wouldn’t see it as a need and more 2FA if you will. Another security feature. You still have to leave a trace behind in the physical world if you want to defraud it on-chain eventually. This may be at multiple intermediaries, but you leave a trace behind.

[Mentioned it in this idea too](https://ethresear.ch/t/ai-agent-assisted-merit-driven-token-distribution/23897), it’s not about making fraud, scam etc. impossible. It’s more of a game.

There will always be a certain amount of malicious actors. You won’t change human nature.

Instead of trying to make it impossible to defraud the system, just have good ways to detect those malicious actors within the system. The need to physically exchange to settle it on-chain adds this layer to detect them. The assumption here is, the Authority is involved in the money creation process that is locked in the smart account. So, the Authority is also able to insurance against fraud etc. Giving them even more incentives to detect fraud in this system. We also have to see it in the context of the reality of cash. It’s declining overall and is mostly used as an inconvenient backup solution in case infrastructure breaks down. Which typically, even in war scenarios, doesn’t break down completly, but sparsely. You could even argue a refugee with cash they can easily move into a “bank account” is quite the benefit overall.

The assumption is also that most actors are honest. The fact alone they have to settle it physically at some “official” place in a traceable way will be high enough barrier to not defraud it.

Happy to hear your input on how it can get improved.

