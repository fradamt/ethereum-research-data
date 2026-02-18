---
source: magicians
topic_id: 14178
title: "EIP-6968: Generalized CSR Protocol"
author: zscole
date: "2023-05-08"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-6968-generalized-csr-protocol/14178
views: 7127
likes: 21
posts_count: 26
---

# EIP-6968: Generalized CSR Protocol

EIP-6968 presents a generalized protocol which networks can reference in order to implement Canto’s Contract Secured Revenue (CSR), as defined in [CIP-001](https://github.com/Canto-Improvement-Proposals/CIPs/blob/main/CIP-001.md).

EIP-6968 is a modified version of EIP-1559 that maintains the benefits of transient congestion management and provides a novel economic mechanism that allows contract creators to receive a portion of the gas fees consumed by their contracts within a given block.

EIP-6968 will directly align incentives between smart contract deployers and networks in a manner that contributes toward constructive community activity. Although this initial EIP targets L2 implementation, it can be applied to any network which applies EIP-1559 logic in the future.

https://github.com/ethereum/EIPs/pull/6969

## Replies

**owocki** (2023-05-08):

EIP co-author here.  I just wanted to drill in on this point.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zscole/48/9401_2.png) zscole:

> Although this initial EIP targets L2 implementation, it can be applied to any network which applies EIP-1559 logic in the future.

**Deploying EIP 6969 is probably NOT a good idea for the ETH L1 ever.**  Because the ETH L1 should remain credibly neutral, resistent to capture and perverse incentives… that means it is probably not a good idea to introduce mechanisms that send gas fees or other L1 generated revenue to any new party (contract creator, core developers, public goods, or otherwise).

(those of you who were around a while know that these values of *credibly neutral, capture resistence, perverse incentive resistence* were the hardfought community consensus articulated/reinforced in the debates surrounding the [now withdrawn EIP 1890 Block Rewards Funding Funding Proposal](https://eips.ethereum.org/EIPS/eip-1890) )

That said, there are some interesting opportunities to create experiments in dApp developer revenue on L2s in the meantime.  I’m excited to see what kind of traction this creates within the L2 ecosystem, and envision a virtuous flywheel where we see smart contract developers receive revenue for the value they bring to L2s.  I could even see this unfold such that that CSR could be a competitive advantage to new L2s that are trying to attract devs into their ecosystem.

EDIT: Scoopy says it better/more concise than I can ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

https://twitter.com/scupytrooples/status/1655632064715055126

---

**souptacular** (2023-05-08):

Love this! Public goods research for the protocol layer is under explored. I’ll be recruiting some of the governance team at Polygon to dive into this, not because Polygon is wanting to implement it, but this is really cool so we want to help.

---

**PhABC** (2023-05-08):

Is the mapping of contract => revenue address is part of storage or an in-memory thing? Do contracts need to call `SETREVENUERECIPIENT` for every function in their contract or is it a one time thing they set via a function like `setRevenueRecipient() { SETREVENUERECIPIENT ....}` that will store the value in the state?

---

**wjmelements** (2023-05-08):

Canto demonstrated the faults of this mechanism. It encourages gas guzzling. The wrong parties get rewarded. Protocol developers can’t be identified retroactively.

“Public goods funding” does not need to be implemented in the execution layer. L2s should think long and hard before giving their revenue away. Taxing your users to fund sketchy middlemen will set you up for failure.

---

**lastmjs** (2023-05-08):

I’m coming from the Internet Computer ecosystem and am very interested in a variation of this idea.

Has anyone put thought into also sharing the revenue with the libraries installed into the smart contracts? For example, imagine if OpenZeppelin were able to receive a small portion of the contract secured revenue for all contracts it is a part of.

I think this could extend the benefits of CSR to open source library authors, I actually like it even better than CSR itself.

---

**alijasin** (2023-05-08):

I would have thought that if a contract was using up an unnecessary amount of gas then someone else would be incentivized to deploy an optimized version of it?

Who are the “wrong parties” here? Does a contract developer really fit into the “sketchy middlemen” bucket?

---

**wjmelements** (2023-05-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alijasin/48/9050_2.png) alijasin:

> Who are the “wrong parties” here? Does a contract developer really fit into the “sketchy middlemen” bucket?

If I deploy a copypasta UniswapV2 clone on your sidechain, am I a “contract developer”? If I deploy an openzeppelin shitcoin, can openzeppelin possibly earn money? Contract deployers are not necessarily developers, and, at best, represent a tiny minority of value-added in this space.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alijasin/48/9050_2.png) alijasin:

> I would have thought that if a contract was using up an unnecessary amount of gas then someone else would be incentivized to deploy an optimized version of it?

If we were to all migrate to a wrapped USDT, the CSR would follow; is it because USDT is no-longer providing value or is it because a deployer vampired their CSR?

The value-add of a deployment that saves gas over another is the gas saved, but CSR rewards according to gas used. Again, the deployer didn’t necessarily write the optimization.

A summary of this criticism is that CSR is a perverse incentive.

---

**fredlacs** (2023-05-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/owocki/48/9402_2.png) owocki:

> (those of you who were around a while know that these values of credibly neutral, capture resistence, perverse incentive resistence were the hardfought community consensus articulated/reinforced in the debates surrounding the now withdrawn EIP 1890 Block Rewards Funding Funding Proposal  )

Those are interesting considerations, but shouldn’t L2s worry about these things and having an incentive compatible fee mechanism too?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/owocki/48/9402_2.png) owocki:

> That said, there are some interesting opportunities to create experiments in dApp developer revenue on L2s in the meantime

I’m also fully in favor of experimentation for this, but experimentation that takes into account the above principles you mentioned. Whats unique about L2s that you can overlook those?

---

**parseb** (2023-05-09):

This is about accommodating a wide range of business models at protocol level. Cutting a slice of user paid ETH to an address previously specified by the user targeted contract, be it public good or private profiteering. Gas guzzlers will likely be out-competed if such practice ever becomes a problem.

Two trivial use cases:

- PoolTogether will be able to boost its prize pools “out of nothing” and at no cost
- Governance tokens that instantly issue usage driven revenue

I am surprised to see this here since I was told a few months back that this is not possible on an L2.

This would catalyze new things. Hope to see it happen on an L2.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> If we were to all migrate to a wrapped USDT, the CSR would follow; is it because USDT is no-longer providing value or is it because a deployer vampired their CSR?

We never were. Nor will we all anything as such. And if we will, there’s an incentive to, strong enough to break USDT’s network effects. It’s either that the more expensive wrapper provides the user more value or we’re all carelessly using the same king-making interface.

Anyone can profit off any other contract already. Not sure why one is ‘vampiring’ and the other is not. The users, in this specific case bear the risks of the wrapper being blacklisted, be it on or off chain. But I guess that’s the risk of boycotting something in this way, they might boycott back.

There is a case to be made in terms of “lost revenue”, if, for example, GMX, for in-protocol degen operations accrues CSR by using a wrapper. But I don’t think it is a particularly strong one as there is no “moral duty” to operate non-symbolically on held assets via their originating logic. I would be curious to find out where you think such a claim originates.

---

**zsystm** (2023-05-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/parseb/48/7608_2.png) parseb:

> I am surprised to see this here since I was told a few months back that this is not possible on an L2.

What does it mean?

Why do you think that is not possible on an L2?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/parseb/48/7608_2.png) parseb:

> PoolTogether will be able to boost its prize pools “out of nothing” and at no cost

Could you explain this sentence more? Hard to catch your context. What do you want to say with this sentence?

Thanks in advance.

---

**parseb** (2023-05-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zsystm/48/9446_2.png) zsystm:

> Why do you think that

I do not think that. I was just told by one of the core folks involved in where this experiment is taking place elsewhere this would not be possible on an L2. My intuition: it’s more of a question of economic policy preference than a technical one.

About [PoolTogether](https://pooltogether.com/); I just wanted to add some random, low effort examples of things that would become possible as each PT contract interaction would generate protocol controlled revenue without financial risk that can be used to top up prizes. At the end of the day, all this is is a baked in, judgement-free subsidy.

---

**z.ftm** (2023-05-11):

I don’t know about the viability of this, but what about a system where:

1. Contract deployer deploys contract
2. Contract deployer proposes addition of their contract to a CSR whitelist to validators
3. Validators can choose whether or not to approve these additions to a the whitelist
4. If and only if x% of validators in the active set are in accordance contract 0x123abc… is on the CSR whitelist at block B, then the contract deployer can recieve a portion of gas fees

This is just a rough idea I had, some problems could be bribes, etc

---

**quantum_eth** (2023-05-12):

I believe the intentions are good for this proposal, but it interferes with protocol incentives. All the more, the cost will be transferred to the end user, which I think is not good. Also, not sure what will be the impact of MEV wars on this.

Another rough idea, far fetched, I think if possible to fund public goods from the a portion of fees to be burned, but again this might impact the network security.

---

**5cent-AI** (2023-05-14):

I think this direction of improvement is good. Burning most of the gas helps to increase the ETH price, but it may not necessarily be entirely beneficial for the long-term development of the Ethereum ecosystem.

As for the motivation aspect, I agree with funding public goods. With the development of the ecology, in fact, Ethereum’s demand for public goods has become higher and higher, but there is currently no sustainable way to fund public goods. Finding a sustainable way to fund public goods is currently a very urgent matter. Considering the sustainability of public goods in ETH’s economic model is a direction worth exploring.

As for other motivations, I still have some concerns. I admit that this is very attractive commercially, because it increases the way for developers to capture value. If a public chain or L2 adopts this improvement, it will motivate more developers to develop. However, the final cost will be passed on to the user. In the past, developers had an incentive to reduce on-chain interactions and gas consumption to improve user experience. If developers can capture value from gas consumption, this may have negative consequences.

Therefore, at present, I only recommend Contract Secured Revenue (CSR) be used for funding public goods. And for other purposes, careful consideration is still needed.

---

**lastmjs** (2023-05-15):

I think it’s very important to put thought into securing revenue for contract dependencies in addition to (or maybe even instead of) the contract itself.

Each contract will be built off of the functionality of other contracts and open source libraries, and imagine the fantastic flow of revenue that we could create for open source smart contract libraries with this model.

Heuristics would need to be thought of for dealing with the transitive dependency tree. For example, the first level of dependencies could receive 50% of the CSR amount. The second level could receive 50% of the remaining amount, and this could repeat for each level of dependencies.

Please don’t ignore the potential to bring a source of revenue to open source libraries, an open-source native way to secure revenue that may not require any change in license.

---

**VoteTheWorld** (2023-05-16):

Quite interesting and looking forward to seeing it implemented!

---

**SamWilsn** (2023-06-08):

Not sure how important it is to mention in the EIP itself, but the contract doesn’t seem to be executed when the revenue is deposited. This makes it very similar to self-destruct, correct?

---

Does this have any interactions with [EIP-158](https://eips.ethereum.org/EIPS/eip-158)?

---

**shazow** (2023-06-20):

A couple of related thoughts:

1. Can this implemented as an ERC, without adding opcodes?
For example, qualify contracts with owner() returns (address) functions (EIP-5313) for rev share instead of adding SETREVENUERECIPIENT opcode?
This would reduce the risk of abusing the opcode for unexpected cases, and reduce EVM maintenance burden, and would qualify some existing contracts in a reasonable way.
2. Can this be prototyped as a semi-offchain solution first?
For example, a rollup that modifies EIP-1559 as mentioned but sends the REVENUE_SHARE_QUOTIENT to a CSR pool address. Periodically (e.g. weekly), an offchain trace operation is run to measure the participation of all qualifying contracts, and redistribute the funds. The offchain trace results could be part of the rollup’s consensus mechanism (can be runnable by multiple participants to confirm/dispute results).

---

**sbacha** (2023-07-09):

The purpose of the burn function is exactly because you can not disprove that sending the money to another address other than the block proposer is in fact going to someone other than the block proposer.

Burning the fee is not some deflationary gimmick it’s literally required to ensure the mechanics are bounded.

---

**benaadams** (2023-07-26):

Might want a cap on Tx gas distributed or it would encourage gas inefficient contracts?


*(5 more replies not shown)*
