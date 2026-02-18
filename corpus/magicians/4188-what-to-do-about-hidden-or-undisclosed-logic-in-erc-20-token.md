---
source: magicians
topic_id: 4188
title: What to do about hidden or undisclosed logic in ERC-20 tokens?
author: jpitts
date: "2020-04-07"
category: Magicians > Primordial Soup
tags: [security, erc-20, usability]
url: https://ethereum-magicians.org/t/what-to-do-about-hidden-or-undisclosed-logic-in-erc-20-tokens/4188
views: 1713
likes: 7
posts_count: 8
---

# What to do about hidden or undisclosed logic in ERC-20 tokens?

This is a starter thread for standard ways to better enforce user expectations for ERC-20 contracts, or at least provide mechanisms to inform users of hidden / undisclosed logic.

This issue was brought up in a Tweet today by [@LefterisJP](/u/lefterisjp), and I’ve heard it discussed before.

https://twitter.com/LefterisJP/status/1247557041415225345

A key problem is that potential fees triggered by maintainers and other logic can break the user experience. There is a set of assumptions/expectations around ERC-20s that is not enforced.

https://twitter.com/LefterisJP/status/1247565303875338242

Additional logic also leads to higher gas costs for users.

https://twitter.com/LefterisJP/status/1247582282443087872

# Solutions

There an effort organized by [@p0n1](/u/p0n1) to track buggy / nonstandard code in ERC-20s, it may be defunct as the last commit is Oct 10, 2018.



      [github.com](https://github.com/sec-bit/awesome-buggy-erc20-tokens)




  ![image](https://opengraph.githubassets.com/7aa263fb3da7d42a64f84236ee5b64b4/sec-bit/awesome-buggy-erc20-tokens)



###



A Collection of Vulnerabilities in ERC20 Smart Contracts With Tokens Affected










---

Update:

Article by Daniel Que describing the general situation and techniques used: [What we learned from auditing the top 20 ERC20 token contracts](https://medium.com/@danielque/what-we-learned-from-auditing-the-top-20-erc20-token-contracts-7526ef3b6fb1)

## Replies

**LefterisJP** (2020-04-08):

Hey [@jpitts](/u/jpitts).

Thanks for making the thread. I got a lot of shit for writing that tweet ![:kissing:](https://ethereum-magicians.org/images/emoji/twitter/kissing.png?v=9)

I think that such tokens should be flagged in a database maybe much like the one you linked and wallets, dapps, portfolio trackers should show some kind of warning to the user.

The biggest problem imo comes when `transfer/transferFrom()` does not work as expected. Many contracts assert that the transferred amount was fully transferred to the recipient. If at some point this breaks for a contract, like say the tether contract enables fees then all dapps using it would break.

---

**GridTechs** (2020-04-09):

I need to understand the issue with the smart contracts. Can you explain what you are experiencing?

Thank you

---

**owocki** (2020-05-11):

Usdt doesn’t work on gitcoin grants rn because of this. It’s a big pain in the butt.

I think that verified contracts on etherscan do the work of letting us all see why though. Which is positive. Not sure what else can be done other than many creating a community based taxonomy of erc20s and their “quirks”

---

**wjmelements** (2020-05-15):

Just wrap the token with a token that actually conforms to ERC20 and doesn’t charge fees. You can also do this for inefficient implementations like the GUSD.

---

**kohshiba** (2020-06-06):

I think wrapping up is an interesting idea.

Given there are many other forms of USD pegged tokens, I think some sort of TCR or other curation style system for the issue might be helpful.

---

**jpitts** (2020-08-25):

There is an article posted today which covers this issue, specifically citing a recent paper on identifying poor implementations of ERC-20. There are also numerous misconceptions in the article about how governance of ERC standards work (which I will not yet speak to).

https://www.coindesk.com/erc-20-ethereum-tokens-fake-deposit

Quote from the paper [DEPOSafe: Demystifying the Fake Deposit Vulnerability in Ethereum Smart Contracts](https://arxiv.org/pdf/2006.06419.pdf) (PDF):

> we implement DEPOSafe, an automated tool to detect and verify (exploit) the fake deposit vulnerability in ERC-20 smart contracts. DEPOSafe incorporates several key techniques including symbolic execution based static analysis and behavior modeling based dynamic verification. By applying DEPOSafe to 176,000 ERC-20 smart contracts, we have identified over 7,000 vulnerable contracts that may suffer from two types of attacks.

This is [@AlexeyAkhunov](/u/alexeyakhunov) [describing the vulnerability](https://twitter.com/realLedgerwatch/status/1298337142452756485), which impacts how exchanges deal with tokens:

> The attacks relies on a flawed code at the side of an exchange. Early versions of ERC-20 assumed that if transfer’s precondition aren’t satisfied, it should “throw” (using assert). Then, the “bool” return value was added, meaning that the “new” way of signalling
>
>
> that the transfer did not happen is to return false instead of throw
>
>
> So exchanges that assume that invalid transfer always throws, and invalid transfer does not, do not check the return value of “transfer” function
>
>
> I think this “attack” is basically exploiting the confusing nature of slightly different versions of ERC-20 and their incompatibility with each other. ERC-20 should have never been changed like that, a new standard should have been created instead

---

**nagydani** (2023-07-26):

The problem of not automatically flagging malicious ERC20 token contracts is still with us. I did [this writeup](https://danielanagy.medium.com/an-automated-scam-against-erc20-transactions-c96044d04a3d) about an ongoing scam which critically relies on malicious ERC20 token contracts that execute `transferFrom()` calls without a matching `approve()` call by the payer.

