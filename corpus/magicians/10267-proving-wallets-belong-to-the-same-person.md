---
source: magicians
topic_id: 10267
title: Proving wallets belong to the same person
author: riksucks
date: "2022-08-06"
category: EIPs
tags: [soul-bound, accounts]
url: https://ethereum-magicians.org/t/proving-wallets-belong-to-the-same-person/10267
views: 770
likes: 1
posts_count: 3
---

# Proving wallets belong to the same person

Hello,

I am new here, so please pardon me if I do something out of place.

I was wondering if a standard can be proposed that can be used by smart contracts to know if certain accounts belong to the same person or not. It would be up to the other smart contracts to decide which smart contract of this protocol should be consulted to prove that multiple accounts belong to the same person.

Use cases where I think there is a dire need for this is NFTs that are related to certificates. Certificates issued to only one account and then rendering it un-transferable to other accounts can be a pain.

What I also have in mind is proving that all accounts belong to you after a certain duration again and again, to make sure that the “human” is still in control of it.

Thank you!

## Replies

**dadabit** (2022-08-07):

Hi think this could be in the scope of DID (Decentralized Identifiers) and VC (Verifiable Credentials). Somewhere in the flow an issuer should attest that multiple accounts belong to the same identity (same DID). Check DID specifications in W3C [Use Cases and Requirements for Decentralized Identifiers](https://www.w3.org/TR/did-use-cases)

---

**riksucks** (2022-08-08):

Thanks for the reply [@dadabit](/u/dadabit). This is a very cool recommendation in the making that I didn’t know of. So what you are suggesting is that we should be helping the w3c recommendation group and then standardize it’s implementation as an EIP once the w3c recommendation is finalized?

Or do you think we can draw from their works, add to it via recommendations in this esteemed forum and cook up something?

Feel free to suggest!

