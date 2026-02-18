---
source: ethresearch
topic_id: 15923
title: Password recovery for Account Abstraction Wallet
author: terry
date: "2023-06-20"
category: Applications
tags: [account-abstraction]
url: https://ethresear.ch/t/password-recovery-for-account-abstraction-wallet/15923
views: 2619
likes: 6
posts_count: 9
---

# Password recovery for Account Abstraction Wallet

# Password recovery for Account Abstraction Wallet

This topic proposes a new approach to password recovery for Account Abstraction Wallets, utilizing ZK-SNARKs (Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge).

The central idea behind this proposal is to store the `hash(password, nonce)` on the contract wallet. In the event that a user loses their private key, which controls the contract wallet, they can employ their password to generate a zk-proof. This proof serves to verify that the user knows the password and requests a change of the private key. The confirmation process for this change will take approximately 3 days or more. Once confirmed, the contract wallet will update the `hash(password, nonce + 1)`.

The zk-proof will contain public fields, including the newHash field. This field represents the updated hash value resulting from the password change process.

By utilizing ZK-SNARKs, the password recovery mechanism ensures that the user’s privacy is maintained. The proof only discloses the necessary information to verify the password and update the private key, without revealing any sensitive details about the password itself. This enhances the overall security of the Account Abstraction Wallet system.

In addition to ZK-SNARKs. The extended confirmation period of 3 days or more serves as a safeguard against unauthorized access attempts. It adds an extra layer of protection by introducing a time-based delay, allowing users to regain control of their wallet while mitigating the risk of malicious actors attempting to exploit the recovery process.

Implementing this password recovery mechanism on the contract wallet enhances the user experience by providing an alternative solution to regain access to their wallet in case of a lost private key. It offers a robust and secure approach that balances convenience and privacy, maintaining the integrity of the Account Abstraction Wallet system.

## Replies

**MicahZoltu** (2023-06-20):

The VDF seems unnecessary as you can just have the contract start a timer when the password update is initiated.

I’m a big fan of time delays on recovery though!

---

**terry** (2023-06-20):

I completely accept with you, and it is crucial that we retain the inclusion of the term VDF in this proposal

---

**jhfnetboy** (2023-06-28):

If I were a hacker attempting to compromise the system by submitting a false password every three days, the owner would no longer be able to access or recover their wallet. What could be done in such a scenario?

Or a wrong password can’t trigger the confirmation?

---

**terry** (2023-06-28):

The confirmation can only be trigger once the user submits the correct password. If hacker try tro submit wrong password, smart contract will revert hacker’s transaction.

---

**qizhou** (2023-06-28):

What is the difference of using current ETH signature/address scheme with `password == private_key`, and the `hash == address`?  Since the ECDSA+RIPMD160 is also ZK-SNARK, so I can also put the password as `private_key` and the rest is essentially the same?

---

**jhfnetboy** (2023-06-29):

Do you mean the wrong password won’t trigger the three days lock time? If it is reverted by a smart contract, it is security.

---

**terry** (2023-06-29):

Great idea! We can implement a password recovery feature by utilizing the equation `private_key == hash(password, wallet_address)`. Furthermore, we can ensure password validity by validating the signature.

---

**terry** (2023-06-29):

Yes, wrong password will not trigger the three days lock mechanism.

