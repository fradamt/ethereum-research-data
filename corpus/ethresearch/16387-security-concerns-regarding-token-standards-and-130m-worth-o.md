---
source: ethresearch
topic_id: 16387
title: Security concerns regarding token standards and $130M worth of ERC20 tokens loss on Ethereum mainnet
author: Dexaran
date: "2023-08-15"
category: Security
tags: []
url: https://ethresear.ch/t/security-concerns-regarding-token-standards-and-130m-worth-of-erc20-tokens-loss-on-ethereum-mainnet/16387
views: 3064
likes: 2
posts_count: 17
---

# Security concerns regarding token standards and $130M worth of ERC20 tokens loss on Ethereum mainnet

I would like to invite researchers to investigate the problem of Ethereum token standards and most notably [ERC-20](https://eips.ethereum.org/EIPS/eip-20). I am the author of ERC-223 token standard and a security expert.

Full post here: [erc20_research.md · GitHub](https://gist.github.com/Dexaran/93d099dfb92b615eb4229afe8c66f962)

(no clue whose genius idea it was to restrict publications on RESEARCH FORUM to 2 links per post)

## Replies

**Dexaran** (2023-08-15):

- I’ve created a security auditing organization that audited more than 300 smart-contracts and not even a single one was hacked afterwards
- I was doing security audits myself.

---

**Dexaran** (2023-08-15):

- I have launched a successful consensus-level attack on one of the top5 chains of its time

So, I kinda know what I’m talking about.

**I’m stating that ERC-20 is an insecure standard.** It has two major architecture flaws:

---

**Dexaran** (2023-08-15):

1. Lack of transaction handling: Known problems of ERC-20 token standard | by Dexaran | Medium
2. approve & transferFrom is a pull transacting pattern and pull transacting is not designed for trustless decentralized systems so it poses a threat to users’ funds safety there: ERC-20 approve & transferFrom asset transfer method poses a threat to users’ funds safety. | by Dexaran | Jul, 2023 | Medium

---

**Dexaran** (2023-08-15):

Today users [lost at least $130M worth of ERC-20 tokens](https://www.reddit.com/r/ethereum/comments/15p6ny6/today_at_least_130m_worth_of_tokens_are_lost/) because of the above mentioned design flaw of the standard.

First, I described this issue in 2017. **This can be a precedent of a [vulnerability discovery in a “final” EIP](https://github.com/ethereum-cat-herders/EIPIP/issues/255#issuecomment-1671648545).** The EIP process does not allow changes even upon vulnerability disclosure.

---

**Dexaran** (2023-08-15):

- It caused people to lose $13K when I first reported it.
- Then it became $16K when I reported it and had a discussion with Ethereum Foundation members.

---

**Dexaran** (2023-08-15):

- Then it became $1,000,0000 in 2018.
- Then the author of ERC-20 standard stated he doesn’t want to use it in his new project (probably because he knows about the problem of lost funds).

---

**Dexaran** (2023-08-15):

- And today there are $130,000,000 lost

Ethereum Foundation didn’t make any statement about this so far. This issue fits in “critical severity security vulnerability” according to OpenZeppelin bug bounty criteria [OpenZeppelin avoided paying the bug bounty for disclosing a flaw in the contract that caused a freeze of $1.1B worth of assets · Issue #4474 · OpenZeppelin/openzeppelin-contracts · GitHub](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/4474)

---

**Dexaran** (2023-08-15):

You can find the full timeline of events here [ERC-223](https://dexaran.github.io/erc223/)

---

**Dexaran** (2023-08-15):

Also there is a heavy ongoing censorship on Ethereum reddit r/ethereum

For example there is a post about ERC-20 security flaws made on r/Cybersecurity and this post was assigned “Vulnerability Disclosure” status: [Reddit - Dive into anything](https://www.reddit.com/r/cybersecurity/comments/15ejbjs/erc20_standard_callisto_security_department/)

The same exact post was removed from r/ethereum with a reason “Not related to Ethereum or ecosystem” [Reddit - Dive into anything](https://www.reddit.com/r/ethereum/comments/15ej9zk/erc20_standard_callisto_security_department/)

Excuse me, when ERC-20 became “not related to Ethereum ecosystem”?

---

**Dexaran** (2023-08-15):

And other posts are not getting approved for days [Reddit - Dive into anything](https://www.reddit.com/r/ethereum/comments/15pxqll/i_will_tip_1_eth_to_anyone_who_can_ask_vitalik/)

https://www.reddit.com/r/ethereum/comments/15llp7p/i_want_to_raise_the_issue_of_censorship_on/

---

**p_m** (2023-08-16):

tl;dr:

OP points to the fact that it’s possible to send erc20 tokens to token contract address.

---

**Dexaran** (2023-08-16):

No, OP points to the fact that ERC-20 standard is designed in a way that violates secure software design practices which resulted in (1) impossibility of handling transactions and (2) the implementation of pull transacting method which is [not suitable for decentralized trustless assets](https://dexaran820.medium.com/erc-20-approve-transferfrom-asset-transfer-method-poses-a-threat-to-users-funds-safety-ff7195127018) and must be avoided.

The impossibility of handling transactions in turn resulted in impossibility of handling errors.

The impossibility of handling errors resulted in the fact that “it’s possible to send erc20 tokens to token contract address” as [@p_m](/u/p_m) said but this is just the top of the iceberg. The root of the problem is a bit more complicated.

It must be noted that:

- It is not possible to send plain ether to any contract address that is not designed to receive it, the tx will get reverted because ether implements transaction handling
- It is not possible to send ERC-223 token to any contract address that is not designed to receive it because ERC-223 implements transaction handling
- It is not possible to send ERC-721 NFT to any contract address that is not designed to receive it because the transferring logic of ERC-721 is based on ERC-223 and it implements transaction handling
- It is only possible to send ERC-20 token and lose it to a software architecture flaw that does not implement a widely used mechanism

Lack of error handling is a cruel violation of [secure software designing principles](https://kirkpatrickprice.com/blog/secure-coding-best-practices/) and it resulted in a loss of $130M worth of ERC-20 tokens already.

---

**alex-cotler** (2023-08-23):

Its weird to see how people are eager to investigate and debate some abstract paper but not to devote their attention and conduct an investigation of a real ongoing scandal of the decade. A true story of millions of dollars losses and a problem that was getting silenced for years by Ethereum Foundation.

---

**AndyDuncan38032** (2023-08-24):

The incident serves as a reminder that while blockchain and smart contract technologies offer numerous benefits, security risks are a significant concern. Proper development practices, rigorous testing, code audits, and ongoing monitoring are essential to mitigate these risks and protect both users and valuable assets.

---

**jingleilasd** (2023-09-27):

asdsadsads dsadasda sd asd asdasaasdasedqweqweqweqasdasdasd

---

**Dexaran** (2023-11-07):

Here is a script that calculates and displays the token losses in the most user-friendly way: [ERC-20 Losses Calculator](https://dexaran.github.io/erc20-losses)

