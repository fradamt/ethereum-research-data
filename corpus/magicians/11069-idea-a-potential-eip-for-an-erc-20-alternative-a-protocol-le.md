---
source: magicians
topic_id: 11069
title: "Idea: A potential EIP for an ERC-20 alternative - a protocol-level implementation"
author: nth-commit
date: "2022-09-27"
category: EIPs
tags: [token]
url: https://ethereum-magicians.org/t/idea-a-potential-eip-for-an-erc-20-alternative-a-protocol-level-implementation/11069
views: 626
likes: 1
posts_count: 3
---

# Idea: A potential EIP for an ERC-20 alternative - a protocol-level implementation

Hey team,

First post and I’m fairly newb, so feel free to point me to some educational material if I’m way off the mark.

I’ve been deep in the weeds of Uniswap lately, doing some analysis on pairs. And I’ve run into something which I think is a massive blocker to open and secure DeFi, the ERC-20. As I’m sure you are well aware, the ERC-20 is only a standard and doesn’t drive any implementation. This means you can design creative tokenomics around the supply of the token, how it’s exchanged between addresses (e.g. applying a tax), and much more. However, it also means that you can have terrible scammy shit like have an allowlist of addresses that can sell the token, which enables honeypot scams, and means we need super complicated tools to determine if a simple interface is hiding a scam or not.

It would be great if there was an out-of-the-box alternative to ERC-20 that could only be configured by data (not code), so you could immediately know that it does not contain malicious code, and its behaviour was completely expressed by visible configuration data. The protocol would guarantee that the token was safe to buy and sell.

If this worked, it means you could:

- Decrease the surface of diligence required for vetting new projects, which would improve the reputation of the whole ecosystem
- Create a pit-of-success for security
- One less moving part to dev/test/audit
- Potentially implement DeFi components that take literally any token as collateral, with some extra auditing required

The way I see it you’d need (at least) two components:

- SealedERC20, which implements the ERC standard as described above, and cannot be customized with code.
- SealedERC20Authority, a custom contract that has permission to mint ERC-20, change the total supply, all that good stuff. This is the hook to implement (probably almost) any tokenomics you desire, but pulling custom behaviour out of the token contract itself means that you can freely buy/sell the ERC-20 without subjecting yourself to malicious code.

I think there are still potential vulnerabilities - but I think it’s possible to distill/restrict behaviour enough into configuration where it’s both useful and secure. For example, one vulnerability might be using an arbitrary token as collateral, having control of the authority and suddenly minting all the tokens - devaluing your collateral.

Thanks for reading, I look forward to hearing some feedback.

## Replies

**Joe** (2022-11-30):

Did you mean a no-coding required standard?

---

**xinbenlv** (2022-12-01):

For what I saw on Solana, an out of box canonical option has its merit, but also have problem is it stifle competition of implementations. Ethereum seems to operate under an principle they want competing ideas. And hence there are go python cpp js version of EVM implementation and beacon chain client. ERC / smart contract world is the same. ERC20 shall have a lot of implementations, and IMHO there shall not be a “canonical” version of ERC20 smart contract implementation.

That said I love a lot of ideas you stated above, I encourage you to create such a ERC20 implementation make it as secure as possible and share as openly as possible and make it a “de facto canonical”. This is pretty much the position of OpenZepellin today I think. Feel free to challenge and make Ethereum better.

