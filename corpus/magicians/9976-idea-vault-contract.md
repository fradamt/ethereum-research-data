---
source: magicians
topic_id: 9976
title: "IDEA: Vault Contract"
author: reklaw
date: "2022-07-18"
category: EIPs
tags: [erc, wallet]
url: https://ethereum-magicians.org/t/idea-vault-contract/9976
views: 850
likes: 2
posts_count: 3
---

# IDEA: Vault Contract

In order to scale to the mass public, we need to solution for private key storage/management. A Vault Contract sits between an account and wallet and stores private account information; private keys. Similar to a bank vault, a Vault Contract is not supposed to be unlocked often yet when it is it is easy. Accounts have the ability to set security standards on the Vault: 2FA, biometrics, co-signer, security questions, or passwords. In short, the account has control over where their private keys are stored and has control over security management.

This is still a rough idea but I would love to collect your thoughts and feedback to know if I should pursue this further.

## Replies

**PradhumnaPancholi** (2022-07-20):

Interesting notion! I recently came across https://www.kirobo.io/. Maybe, wee can create a standard for something like this.

---

**Joe** (2022-11-30):

Love your idea! But How to Balance Security and Convenience?

