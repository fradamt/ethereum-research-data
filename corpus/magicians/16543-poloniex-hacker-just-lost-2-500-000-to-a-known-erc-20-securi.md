---
source: magicians
topic_id: 16543
title: Poloniex hacker just lost $2,500,000 to a known ERC-20 security flaw that I described in 2017
author: Dexaran
date: "2023-11-10"
category: Magicians > Primordial Soup
tags: [security, erc-20]
url: https://ethereum-magicians.org/t/poloniex-hacker-just-lost-2-500-000-to-a-known-erc-20-security-flaw-that-i-described-in-2017/16543
views: 1720
likes: 3
posts_count: 6
---

# Poloniex hacker just lost $2,500,000 to a known ERC-20 security flaw that I described in 2017

I made [this post](https://www.reddit.com/r/ethereum/comments/17sbxpp/poloniex_hacker_just_lost_2500000_to_erc20/).

Here is a copy of the content [poloniex_hacker_lost_funds.md · GitHub](https://gist.github.com/Dexaran/9bd90c1885b4818573368ad02b784125)

It obviously got insta deleted from the subreddit. If someone can slap those reddit mods - please do it.

---

> The post

---

Poloniex exchange was [just hacked](https://www.fxstreet.com/cryptocurrencies/news/crypto-exchange-poloniex-hack-leads-to-60-million-in-assets-stolen-peckshield-says-202311101206).

A hacker made this transaction https://etherscan.io/tx/0xc9700e4f072878c4e4066d1c9cd160692468f2d1c4c47795d28635772abc18db

And the tokens got permanently frozen in the contract of GLM! This shouldn’t have happened if ERC-20 GLM token would be developed with security practices in mind. But ERC-20 still contains a security flaw that I discloser multiple times (here is a [history of the ERC-20 disaster](https://dexaran820.medium.com/erc-20-token-standard-7fa2316cdcac)).

You can also find a full history of my fight with Ethereum Foundation over token standards since 2017 here [ERC-223](https://dexaran.github.io/erc223/)

The problem is described [here](https://dexaran820.medium.com/known-problems-of-erc20-token-standard-e98887b9532c).

Here is a security statement regarding the ERC-20 standard flaw: [ERC-20 Standard - Callisto Network Security Department Statement](https://callisto.network/erc-20-standard-security-department-statement/)

As of today, about [$90,000,000 to $200,000,000 are lost](https://dexaran.github.io/erc20-losses) to this ERC-20 flaw. Today we can increase this amount by $2,500,000.

The problem with ERC-20 token is that it doesn’t allow for error handling which makes it impossible to prevent user errors. It was known for sure that the GLM contract is not supposed to accept GLM tokens. It was intended TO BE THE TOKEN, not to own the tokens. For example if you would send ether, NFT or ERC-223 token to the address of the said GLM contract - you wouldn’t lose it.

Error handling is critical for financial software. Users do make mistakes. It’s a simple fact. Whether it is misunderstanding of the internal logic of the contract, unfamiliar wallet UI, being drunk when sending a tx or panicking after hacking an exchange - doesn’t matter. Anyone could be in a position of a person who just lost $2,5M worth of tokens to a simple bug in the software that could have been easily fixed.

I would use an opportunity to mention that ERC-223 was developed with the main goal of preventing such accidents of "funds loss by mistake: [ERC-223: Token with transaction handling model](https://eips.ethereum.org/EIPS/eip-223)

What is even worse - EIP process doesn’t allow for security disclosures now. There is simply no way to report a security flaw in any EIP after its assigned “Final” status.

I’m proposing a modification to EIP process to allow for security disclosures here: [Modification of EIP process to account for security treatments - #12 by Dexaran](https://ethereum-magicians.org/t/modification-of-eip-process-to-account-for-security-treatments/16265/12)

There are ongoing debates on submission of an informational EIP regarding the ERC-20 security flaw: [ethereum-cat-herders/EIPIP#293](https://github.com/ethereum-cat-herders/EIPIP/issues/293)

And the Informational EIP pull request: [ethereum/EIPs#7915](https://github.com/ethereum/EIPs/pull/7915)

We’ve built ERC-20 <=> ERC-223 token converter that would allow both standards to co-exist and eventually prevent the issue of lost funds [ERC223 converter](https://dexaran.github.io/token-converter/)

Also my team is building a ERC-223 & ERC-20 compatible decentralized exchange that will also remove such a weird opportunity to lose all their life savings to a software bug from users: https://dex223.io/

If you are rich and worried about ERC-20 security bugs dealing damage to Ethereum ecosystem and ruining users days - welcome to our ERC-223 family. We stand for security. We don’t let our users funds to be lost by mistake.

## Replies

**Dexaran** (2023-11-13):

**Associated threads timeline**

I’ve highlighted the security issue in ERC-20 to EIP editors: [EIPIP Meeting 87 · Issue #255 · ethereum-cat-herders/EIPIP · GitHub](https://github.com/ethereum-cat-herders/EIPIP/issues/255#issuecomment-1671818828)

EIP editors suggested me to create an informational EIP to describe the security flaw of ERC-20 because there is no other process to disclose security flaws in finalized EIPs currently: [EIPIP Meeting 88 · Issue #257 · ethereum-cat-herders/EIPIP · GitHub](https://github.com/ethereum-cat-herders/EIPIP/issues/257#issuecomment-1690850073)

My disclosure of a security flaw in ERC-20 standard: [Disclosure of a security flaw in ERC-20 transferring workflow - #8 by Dexaran](https://ethereum-magicians.org/t/disclosure-of-a-security-flaw-in-erc-20-transferring-workflow/16249/8)

I’ve created the informational EIP that describes the security flaws of ERC-20: https://github.com/ethereum/EIPs/pull/7915

EIP editors initiated a discussion whether to allow the submission of the informational EIP or reject it: [Call for Input: Merge EIP Describing Flaws in ERC-20 · Issue #293 · ethereum-cat-herders/EIPIP · GitHub](https://github.com/ethereum-cat-herders/EIPIP/issues/293)

---

**makemake** (2023-11-17):

This is very alarmist and not a security flaw in the slightest.

Wallets should deal with users trying to send tokens to wrong addresses.

If you’re an advanced user (or hacker in this case), don’t test in prod?

ERC20 isn’t perfect in the slightest, but it just werks™

---

**Dexaran** (2023-11-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/makemake/48/13855_2.png) makemake:

> not a security flaw in the slightest

[Error handling is a must](https://kirkpatrickprice.com/blog/secure-coding-best-practices/). It is a well-known thing in software security. If your standard is designed in a way that makes handling errors impossible - it is insecure standard.

If you don’t implement `onlyOwner` modifier for a governance function and the money will be stolen because of this - it would be a security issue. Also, it fits in OpenZeppelin’s bugbounty “critical severity security vulnerability” criteria.

[$90,000,000 to $200,000,000 are currently lost](https://dexaran.github.io/erc20-losses) because of this **security flaw**.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/makemake/48/13855_2.png) makemake:

> Wallets should deal with users trying to send tokens to wrong addresses.

Yes wallets should. But contracts should also reject incorrect deposits if it is known to be a mistake.

A contract can reject incorrectly deposited:

- Ether
- NFTs
- ERC-223 tokens
- ERC-1155 tokens

But it is not possible to reject ERC-20 tokens because of the flaws in its design. That’s the problem.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/makemake/48/13855_2.png) makemake:

> it just werks

Imagine you come to a bank and the staff tells you that they are using a database that has a security vulnerability that was discovered 6 years ago. Over the past years their customers lost $90M to software errors that could be easily prevented but don’t worry - “thats how it werks in our bank”.

Sounds absurd right?

---

**makemake** (2023-11-17):

Yes, handle the errors off chain. This is a wallet issue, not an ERC20 issue.

Comparing a user/wallet not checking addresses to an admin function not being restricted is absurd. If the former happens, only the user can lose money.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> Imagine you come to a bank and the staff tells you that they are using a database that has a security vulnerability that was discovered 6 years ago. Over the past years their customers lost $90M to software errors that could be easily prevented but don’t worry - “thats how it werks in our bank”.

awful analogy. what youre describing would be like if you went to your bank, gave them an account number you wanted to make a transfer to and the bank didnt check if the account exists and just burned the money; which doesn happen because banks dont work like this.

---

**Dexaran** (2023-11-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/makemake/48/13855_2.png) makemake:

> Yes, handle the errors off chain.

It is evident that this approach **doesn’t work**.

Also if you will read something about software security you will find out that “Software must be secure by default” [8 Secure Coding Practices Learned from OWASP | KirkpatrickPrice](https://kirkpatrickprice.com/blog/secure-coding-best-practices/)

It means you can’t develop a software that has serious security problems like impossibility of error handling and say “UI devs must develop a workaround for my insecure software to interact with it in a secure way”.

This explains **why this approach doesn’t work**.

