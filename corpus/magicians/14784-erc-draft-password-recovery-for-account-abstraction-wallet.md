---
source: magicians
topic_id: 14784
title: "ERC draft: Password recovery for Account Abstraction Wallet"
author: bui-duc-huy
date: "2023-06-22"
category: Web > Wallets
tags: [wallet, account-abstraction, zkp, recovery]
url: https://ethereum-magicians.org/t/erc-draft-password-recovery-for-account-abstraction-wallet/14784
views: 1323
likes: 4
posts_count: 4
---

# ERC draft: Password recovery for Account Abstraction Wallet

# Password recovery for Account Abstraction Wallet

This topic proposes a new approach to password recovery for Account Abstraction Wallets, utilizing ZK-SNARKs (Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge).

The central idea behind this proposal is to store the `hash(password, nonce)` on the contract wallet. In the event that a user loses their private key, which controls the contract wallet, they can employ their password to generate a zk-proof. This proof serves to verify that the user knows the password and requests a change of the private key. The confirmation process for this change will take approximately 3 days or more. Once confirmed, the contract wallet will update the `hash(password, nonce + 1)`.

The zk-proof will contain public fields, including the newHash field. This field represents the updated hash value resulting from the password change process.

By utilizing ZK-SNARKs, the password recovery mechanism ensures that the user’s privacy is maintained. The proof only discloses the necessary information to verify the password and update the private key, without revealing any sensitive details about the password itself. This enhances the overall security of the Account Abstraction Wallet system.

In addition to ZK-SNARKs. The extended confirmation period of 3 days or more serves as a safeguard against unauthorized access attempts. It adds an extra layer of protection by introducing a time-based delay, allowing users to regain control of their wallet while mitigating the risk of malicious actors attempting to exploit the recovery process.

Implementing this password recovery mechanism on the contract wallet enhances the user experience by providing an alternative solution to regain access to their wallet in case of a lost private key. It offers a robust and secure approach that balances convenience and privacy, maintaining the integrity of the Account Abstraction Wallet system

## Replies

**microbecode** (2023-08-23):

Hi here

I think this is an interesting approach to use ZK with AA. It’s a combination I’ve never even considered.

What’s the benefit compared to, for example, public key cryptography? Something like:

- This would not be related to wallet/AA keys: a new set of private/public keys
- contract has your public key
- to make changes in the AA configuration, you sign some message with your private key. You send the signed message to AA contract with the plaintext message, and it verifies the data with the public key

---

**bui-duc-huy** (2023-08-26):

Hi, I found a solution to solve my issue above by using current ETH signature/address scheme, We won’t need to build an custom a zk-SNARKs schema, Check it out here: [Password recovery for Account Abstraction Wallet - Applications - Ethereum Research](https://ethresear.ch/t/password-recovery-for-account-abstraction-wallet/15923)

---

**julianor** (2025-08-21):

Have you heard about paper wallets? You’ve basically reinvented one - only worse, because you are flagging a crackable target on-chain.

