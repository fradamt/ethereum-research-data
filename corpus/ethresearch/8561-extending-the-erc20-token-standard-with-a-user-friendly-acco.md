---
source: ethresearch
topic_id: 8561
title: Extending the ERC20 token standard with a user-friendly account recovery mechanism
author: GustavHAlbrecht
date: "2021-01-22"
category: Meta-innovation
tags: []
url: https://ethresear.ch/t/extending-the-erc20-token-standard-with-a-user-friendly-account-recovery-mechanism/8561
views: 1509
likes: 0
posts_count: 5
---

# Extending the ERC20 token standard with a user-friendly account recovery mechanism

**Motivation:**

In current ERC20 smart contracts a loss of the private key means an irrecoverable loss of the ERC20 tokens associated with an address. This fact scares non-technical users. This text describes a simple user-friendly mechanism to recover access to tokens.

**Idea:**

In its simplest form the owner chooses a password and stores a double-hashed version of the password in the smart contract. Anybody can then send a commit with the address he request funds from, a certain amount of tokens as a stake and the hash (not the double-hash) of the password. There can only be one pending commit per time frame. Then the person who successfully commits must reveal the clear text password. If the clear text password matches the commited hash and the double-hashed version stored in the smart contract he can access funds. If he doesn’t reveal or the provided clear text password doesn’t match, the provided stake is lost forever.

**Analysis:**

A commit reveal scheme is obviously necessary to prevent a miner from extracting the clear text password from a transaction, discard the transaction and send his own transaction to request access to funds. A miner has however no incentive to imitate a commit transaction because he is unable to reveal – he doesn’t have the password and would loose the required stake. When the user successfully commited nobody else can commit because there is only one commit per time frame. Then the user has the possibility to reveal in a certain time frame and nobody can stop him from doing so.

Obviously an attacker could double hash many different common passwords and match them with double hashes stored on the contract. To prevent this the user must have a long enough password. However one can trick here. The user can just have a “common” password and append a personal unique identifier like *FirstNameSecondNameBirthplaceParentNames .* This unique identifier acts a source of randomness. There is not additional burden because people remember these things and they can even be public. It makes it economically infeasible for an attacker to simply hash through all “common” password because he would have to do it for every single person.

One can also simply steal the password of the owner. To make these attacks infeasible and to add an additional layer of security the owner of the funds (who still controls the private key if only his password is stolen) can abort every commit and the person who commited loses his stake. An attacker who steals the password would not commit assuming the owner would abort. Also the owner can change the password by storing a different double hash of a new password.

One important point is the overhead for the smart contract usage. But this overhead is actually quite low. The existing transfer functionality could just remain the same. One just have to add a mapping from addresses to the double-hash of passwords and the functionality to commit and reveal. Also this recovery option can be fully optional. If the user does not store a double-hash of the password onchain all remains as it is today.

**My question to you**

Is this secure and do you see value in it?

## Replies

**kladkogex** (2021-01-22):

Hey Gustav,

You can do it the way you describe, but there is an even simpler system, where you use the password to generate your ETH key.

Ledger has a feature where the key is derived from recovery phrase + password.

You can use a recovery phrase known to everyone (publish it on internet) , and then have a secret password.

The password needs to be long enough not to be brute-forced.

Then if you lose the ledger, you can simply get another one, enter the recovery phase, and then the password.

---

**GustavHAlbrecht** (2021-01-22):

Hi kladkogex,

thanks for the information i wasn’t aware of this feature. However i see some important differences between these two mechanisms.

First of all the term “account recovery mechanism” is maybe misleading because the mechanism is not intended to recover keys but to recover ERC20 tokens from an account that the user lost the keys. The recovery mechanism only applies to a certain ERC20 contract where the user explicitly stored the double-hash of a password. After a successful commit and reveal the “lost” funds are transferred to the address that commited and revealed.

I see an important difference between these two mechanisms. In the mechanism you described the user can store his passphrase on the internet, effectively meaning he can’t lose it anymore. However if somebody then steals his secret password the attacker can obviously recover the keys and steal the funds. This is also true if the user still controls the keys and doesn’t transfers funds in time.

In the mechanism i described the attacker can steal the password but can’t access the tokens on the ERC20 contract because he would first need to make a commit with the hash of the password to request funds from the address. During this commit time frame the real owner can abort the commit as he obviously is the real owner. The only way for the attacker to leverage the stolen password is to make sure the owner loses his private keys or is unable to abort the commit. Then he can successfully commit and reveal and transfer funds. If the user recognized his password is stolen or somebody makes an unauthorized commit the can abort the commit and change the password.

So in both mechanisms the user only needs to remember a password but in the mechanism i described there is the advantage that an attacker can’t leverage a stolen password if the owner still controls the keys.

I hope my viewpoint becomes clear.

---

**kladkogex** (2021-01-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/g/e95f7d/48.png) GustavHAlbrecht:

> the user can store his passphrase on the internet, effectively meaning he can’t lose it anymore.

Hey Gustav,

If you store the hash of the password on the internet,  it has to be pretty long in order not to be brute-forced.

Thats the problem.  Ultimately you may need to have a complex password similar to Metamask 12 word recovery phrase. ![:imp:](https://ethresear.ch/images/emoji/facebook_messenger/imp.png?v=12)

Actually, the Metamask recovery phrase is reasonably short because BIP key derivation algorithm is pretty computationally intense as compared to simply SHA you would use in a smart contract

---

**lightcycle** (2021-02-17):

If end up having another 12 word recovery phrase, an alternative would be a 1-of-N multisig wallet

