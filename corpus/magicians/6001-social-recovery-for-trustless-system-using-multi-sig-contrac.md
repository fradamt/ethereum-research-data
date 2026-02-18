---
source: magicians
topic_id: 6001
title: Social Recovery for trustless system using multi sig contracts
author: vikaskumr
date: "2021-04-15"
category: Uncategorized
tags: [ethereum-roadmap, social-recovery]
url: https://ethereum-magicians.org/t/social-recovery-for-trustless-system-using-multi-sig-contracts/6001
views: 1453
likes: 0
posts_count: 5
---

# Social Recovery for trustless system using multi sig contracts

Hi

I have read a lot about social recovery in this discussion forum

`https://ethereum-magicians.org/t/social-recovery-using-address-book-merkle-proofs/3790/`

but what I am looking for how to make it trustless without storing the password in the database and how to recover the same password as I don’t have to generate a new password.

I thought of using Shamir Secret Sharing but I was thinking how can we do it using multi-sig contracts

## Replies

**vbuterin** (2021-04-15):

You can absolutely do social recovery using multisig contracts. My own preferred technique today is actually to set up a wallet smart contract that specifies a *single* recovery address that has the right to call a function that changes the public key. The address itself can then be a not-yet-published multisig wallet created with CREATE2; the multisig wallet would only need to go on-chain to send the single recovery transaction if there is an actual recovery to be made.

---

**vikaskumr** (2021-04-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> 2; the multisig wallet would only need to go on-chain to send the single recovery transaction if there is an actual recovery to be made.

Hi [@vbuterin](/u/vbuterin) Thanks for your approach but in my case, I don’t want to change the public key.

It is just a simple forgot password case in which I need to recover the password for the same wallet. In this case I am not sure how multi sig contracts can help.

Can you please explain

---

**vbuterin** (2021-04-15):

Is this an ethereum wallet that you are trying to recover the password for, or some different kind of account? If it’s an ethereum wallet, then the idea would be to use a social recovery wallet contract *in place of* a regular wallet. If it’s a different kind of account, then contract-based recovery can’t help and you probably want secret sharing.

---

**vikaskumr** (2021-04-15):

[@vbuterin](/u/vbuterin) yes like an HD wallet, except we can create any keys (bitcoin, ethereum etc).

And my scenario is

If the user later loses access to their account, they will ask the guardian to restore their access. The guardian will produce a signature indicating their approval. So instead of transferring ownership of the smart contract wallet to a new address held by the user, I want the address to remain the same but just to recover the same password.

