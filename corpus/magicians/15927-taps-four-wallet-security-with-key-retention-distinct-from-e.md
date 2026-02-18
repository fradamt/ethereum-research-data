---
source: magicians
topic_id: 15927
title: "TAPS: Four-Wallet Security with Key Retention (Distinct from ERC 4337)"
author: solarsailor
date: "2023-09-27"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/taps-four-wallet-security-with-key-retention-distinct-from-erc-4337/15927
views: 602
likes: 0
posts_count: 1
---

# TAPS: Four-Wallet Security with Key Retention (Distinct from ERC 4337)

Please give me feedback on the following protocol. My intention is that we might be able to make it into a an EIP.

# TAPS Contract

## Overview

The TAPS contract is a multi-wallet management system designed to provide varying levels of security based on the type of wallet and the operations performed. It allows users to vault and unvault assets, both in the form of tokens (ERC20, ERC721, and ERC1155) and Ether, between different wallet types. Vaulting refers to the process of going from a less secure state to a more secure state. Unvaulting refers to the process of going from a more secure state to a less secure state. The primary goal of TAPS is to enhance asset security by leveraging the strengths of different wallet types and their associated risk profiles.

---

## Wallet and Vault Types

The system categorizes wallets/vaults into four types:

1. Minting Wallet: Primarily used for minting new tokens.
2. Transaction Wallet: Used for marketplace transactions.
3. Social Vault: A more secure vault used for interactions with one or multiple trusted contracts for access to ecosystems.
4. Cold Vault: The most secure vault, ideally air-gapped, used for long-term storage and seldom accessed.

---

## Key Features

1. Elimination of User Error: TAPS eliminates the risk of user error during vaulting and unvaulting. Instead of manually entering addresses, users set their wallet configurations once. For subsequent operations, they simply specify the type of wallet or vault, reducing the risk of sending assets to the wrong address.
2. Commitment Modes: TAPS offers two commitment modes. In the “Non Signing Cold Vault Mode”, the cold vault does not sign any transactions, offering a balance between security and flexibility. In the “Signing Cold Vault Mode”, the cold vault can only sign transactions involving the TAPS contract, ensuring its isolation.
3. Transition Risk Assessment: TAPS provides a clear risk assessment for each type of transition, allowing users to make informed decisions about their asset management.

---

## Transition Descriptions

**Vaulting**

1. Mint to Cold: Assets minted are directly moved to the most secure vault, ensuring immediate security for newly created assets.
2. Transaction to Cold: After a marketplace transaction, assets can be moved to the cold vault for long-term safekeeping.
3. Mint to Social: Assets minted can be moved to the social vault for interactions with trusted contracts.
4. Transaction to Social: After a marketplace transaction, assets can be moved to the social vault for more secure, yet flexible storage.
5. Social to Cold: Assets in the social vault can be moved to the cold vault for maximum security.

**Unvaulting (NonSigningCold Mode)**

1. Social to Transfer: Assets can be moved from the social vault to the transaction wallet for marketplace transactions.

**Unvaulting (SigningCold Mode)**

1. Cold to Social: Assets can be moved from the cold vault to the social vault for interactions with trusted contracts.
2. Social to Transfer: Assets can be moved from the social vault to the transaction wallet for marketplace transactions.
3. Cold to Transfer: Assets can be moved directly from the cold vault to the transaction wallet.

---

## Commitment Modes

1. Non Signing Cold Vault Mode: In this mode, the cold vault does not sign any transactions, ensuring it remains completely isolated. This mode offers a balance between security and flexibility, allowing the social vault to handle most interactions while the cold vault remains untouched.
2. Signing Cold Vault Mode: In this mode, the cold vault is only allowed to sign transactions involving the TAPS contract. This ensures that the cold vault remains isolated from other contracts and potential vulnerabilities. This mode is ideal for users who prioritize maximum security and are willing to operate primarily through the social vault for other interactions.

---

## State Risk Assessment Table

| Wallet Type | Action (Signing) | Historical Risk | Overall Risk Ranking |
| --- | --- | --- | --- |
| Cold Vault | Never Signed | Minimal (Rare Hacks) | Maximum Security |
| Cold Vault | Single Source | Low | High Security |
| Social Vault | Two Different Sources | Medium | Standard Security |
| Social Vault | Trusted Multiple Sources | Medium-High | Reduced Security |
| Transaction Wallet | Marketplace Multiple Sources | High (Infrequent Hacks) | Low Security |
| Minting Wallet | Untrusted and Multiple Regular Signs | Very High (Frequent Hacks) | Minimal Security |

## Transition Risk Assesments

**VAULTING:**

1. Mint (A) →  Maximum Risk Reduction → Cold (B)
2. Transaction (C) →  High Risk Reduction → Cold (B)
3. Mint (A) →  High Risk Reduction → Social (D)
4. Transaction (C) →  High Risk Reduction → Social (D)
5. Social (D) →  Considerable Risk Reduction → Cold (B)

**Unvaulting NonSigningCold:**

1. Social (D) →  Moderate Risk Increase → Transaction (E)

**Unvaulting SigningCold:**

1. Cold (B) →  Minimal Risk Increase → Social (D)
2. Social (D) →  Moderate Risk Increase → Transaction (E)
3. Cold (B) →  Considerable Risk Increase → Transaction (E)

---

To learn more please visit:


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/solarsailorneo/taps_contract/tree/main)





###



[main](https://github.com/solarsailorneo/taps_contract/tree/main)



Contribute to solarsailorneo/taps_contract development by creating an account on GitHub.
