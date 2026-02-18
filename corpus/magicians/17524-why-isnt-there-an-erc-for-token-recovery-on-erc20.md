---
source: magicians
topic_id: 17524
title: Why isn't there an ERC for token recovery on ERC20?
author: confoundinterest
date: "2023-12-20"
category: Working Groups > Fund Recovery Ring
tags: [erc-20, fund-recovery]
url: https://ethereum-magicians.org/t/why-isnt-there-an-erc-for-token-recovery-on-erc20/17524
views: 675
likes: 2
posts_count: 3
---

# Why isn't there an ERC for token recovery on ERC20?

I have been wondering why there is not an ERC for token recovery. There are millions of dollars sent to contracts that cannot be recovered by the users that sent them. Tether is a great example of this: ethereum 0xdac17f958d2ee523a2206206994597c13d831ec7 USDC less so, but they seem to have a backdoor to help out with situations like this: ethereum 0xb6c5f621514225dd8622174a81d4db7549d942782a0dff9b3fe6411c21df21c3.

The way this would work arithmetically would be something along the lines of: when a transfer occurs, if debt is not increased to disallow withdrawal, then anyone can withdraw the deposited tokens where “anyone” can be filtered down to the contract owner or token holders or any set of individuals. The two levels that I would propose starting with include the “per token” level and the “per token + account” level. If debt is being tracked by other means, internal to the contract, then the contract only needs to increment and decrement the debt for the token to keep debt updated and tokens protected.

Debt is tracked already within most contracts in some form or another, usually locked in some heuristic or struct or mapping. A standard pattern would simply abstract away the debt tracking that is already happening for most of these contracts into a known ABI. The best part is, for tokens that do not custody funds themselves, they can simply allow for withdrawals of everything attributed to their address and that would suffice. Standard would be opt-in, similar to burnable tokens: an extension of erc20.

Another added benefit is that a standard like this would create appropriate space for MEV bots and provide a more easily trackable means of competing to recover funds. Tokens that are worth less than the gas cost / bounty would mostly sit until anyone attempts to recover them.

Drawbacks include: state needed - some amount of state is needed to track debt - SSTOREs are expensive. Some number of both internal and external functions are needed, increasing the gas cost for method calls. These costs can generally be reduced by writing fewer times, but it is still costly if it is not already being tracked. Deployment costs as well. Contracts will require more bytecode to support more functionality.

I do not see any EIPs similar to what I am suggesting. This solution is bound to the application level. However, this is certainly an issue, no matter what network one checks.

avalanche: 0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664

avalanche: 0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E

optimism: 0x94b008aa00579c1307b0ef2c499ad98a8ce58e58

optimism: 0xda10009cbd5d07dd0cecc66161fc93d7c9000da1

polygon: 0xc2132d05d31c914a87c6611c10748aeb04b58e8f

I will work on writing out an EIP next. Besides the mostly gas drawbacks I outline above, are there any other reasons not to do this?

## Replies

**galimba** (2023-12-20):

Maybe this is relevant:

- https://arxiv.org/pdf/2208.00543.pdf

---

**xinbenlv** (2023-12-20):

I’s less of a technical problem, it’s more of a social problem: who is entitled to the power of deciding and enforcing the recovery.

Once that question is answered, it could be easily resolved by designing mechansim and interface around it.

- Jurisdiction is one way, if there is an on-chain arbitrator like a court, ERC-5485: Legitimacy, Jurisdiction and Sovereignty.
- Access Control or Contract Ownership is another way to do it, such as ERC-5982: Role-based Access Control or ERC-173: Contract Ownership Standard
- Voting could do it, such as ERC-1202: Voting Interface
- Endorsement could do it, such as ERC-5453: Endorsement - Permit for Any Functions
- Social recovery for a contract wallet, such as Gnosis Safe is another way.

And the way to recover fund is so widely diverse, their interface is hardly a single one, that’s why I think we haven’t seen a standardization of the ERC20 or ERC721 recovery.

