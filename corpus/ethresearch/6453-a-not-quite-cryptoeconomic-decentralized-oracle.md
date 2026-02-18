---
source: ethresearch
topic_id: 6453
title: A not-quite-cryptoeconomic decentralized oracle
author: vbuterin
date: "2019-11-15"
category: Economics
tags: []
url: https://ethresear.ch/t/a-not-quite-cryptoeconomic-decentralized-oracle/6453
views: 7778
likes: 12
posts_count: 10
---

# A not-quite-cryptoeconomic decentralized oracle

One challenge of present-day decentralized oracle schemes is that they become unsafe if the amount of funds whose destination is affected by the oracle exceeds the market cap of the oracle token; if this happens, then token holders have the incentive to collude to give false answers to seize the funds. In such a case, the oracle would of course be forked and the oracle token would become worthless, but it would nevertheless be net-profitable for oracle participants.

The following is one possible alternative oracle design to fix this. We set up a contract where there are 13 “providers”; the answer to a query is the median of the answer returned by these providers. Every week, there is a vote, where the oracle token holders can replace one of the providers. This vote could be a simple vote, or it could be some more complicated mechanism such as quadratic vote or even futarchy.

The security model is simple: if you trust the voting mechanism, you can trust the oracle output, unless 7 providers get corrupted at the same time. If you trust the current set of oracle providers, you can trust the output for at least the next six weeks, even if you completely do not trust the voting mechanism. Hence, if the voting mechanism gets corrupted, there will be able time for participants in any applications that depend on the oracle to make an orderly exit (this would not be enough for long-term oracle needs such as Augur, but would suffice for eg. financial synthetics).

## Replies

**torfbolt** (2019-11-15):

The problem I see with this is that you not only need to trust the committee currently, but also that it is not corruptible within the next few weeks by any yet unforeseen events or adversaries. Economic incentives on the other hand work at any time, as long as the economic requirements are fulfilled.

---

**dankrad** (2019-11-15):

I don’t see why the providers aren’t susceptible to the same collusion problem as the oracle token holders in the cryptoeconomic scheme? It seems that you have just replaced the cryptoeconomic bonding by reputation. In this case, the providers are expected to collude to give a false answer once the economic value they can get out of that answer exceeds the economic investment to gain their reputation.

---

**vbuterin** (2019-11-15):

There’s definitely an assumption that there exist *some* intrinsically trustworthy actors in the world and that these actors can be discovered. But this is still a much weaker criterion than an assumption that *protocol designers* can enshrine a set of such actors that everyone will be ok with.

---

**MaverickChow** (2019-11-18):

There is probably (an assumption) only 1 out of 100,000 that would be trustworthy enough to take the role. And probably (another assumption) only 1% out of a group of such trustworthy population to be interested to accept the role. For anyone to find enough of such population for the role is a set of challenge by itself, in my opinion. And for such population to remain trustworthy **sustainably** for a long time to come is also another set of challenge, but a much greater one. Along the way, untrustworthy actors will do their best to game the system (including pretending to be trustworthy) and secure a position. Whenever money is involved, humans have a much higher chance to become corrupt. And this applies equally to trustworthy humans in the first place.

I am not savvy in this but I think the reason why oracles are needed is only because the external source of reference is not part of the same blockchain network. Otherwise, can direct connection without any oracle be possible?

Edit:

Assuming it is unavoidable to have oracle, I am in the opinion that one viable way to secure the accuracy of output is only if the providers are also a significant stakeholder of the blockchain connected to the oracle. This ensures all positive and negative impacts affect both sides of the equation (similarly and equally), align financial interests, and reduce incentive to corrupt.

---

**maxwellfoley** (2019-11-22):

It doesn’t seem difficult at all to find trustworthy actors - just use any established registered company in the space whose owners have names and faces and so on. If they defraud people via false oracle answers they can very likely be held legally liable. Trustlessness is necessary in anonymous and permissionless settings but in the above-ground world of known actors where people can be held liable for fraud trust usually works pretty well (at least in developed countries).

---

**MaverickChow** (2019-11-25):

To find a genuinely trustworthy actor is very challenging. And to sustain the trustworthiness over a long period of time is close to impossible. Observing the law is not an indication of trustworthiness. It merely indicates compliance. Despite having public faces, corruption and frauds continue to be committed anywhere around the world regardless of developed, developing, or underdeveloped countries. It all boils down to human nature. If human nature is inherently good, there would not be so much darkness in the world nor the need to have a trustless system in place. It is not a case of only a few that would commit fraud, but rather a case of most people that would commit fraud  when the opportunity arises. And we do not see most people commit fraud not because most people are trustworthy, but because the system is evolved enough to have sufficient law and order in place to prevent these people from committing fraud. However, this does not prevent the few that are aware of loopholes to do the same, thus we have Enron as an example. When a person says he is trustworthy, he is most likely not. In the face of temptation, i.e. the attraction of money, sex, and power/control, 99.9999% of humans fail the test.

In my opinion, a practical solution is not about finding any trustworthy person, but about creating a system whereby the interests of untrustworthy people are aligned with the interests of everyone else. So that whatever the action an untrustworthy person may take to benefit/harm another will have similar/equal effect on him as well.

If trust-based system really work pretty well in developed countries, then the below 3 statements are true:

1. Craig Wright is Satoshi Nakamoto.
2. Australia is not a developed country.
3. Everyone should trust Craig Wright.

---

**karl-lolme** (2023-04-11):

“One challenge of present-day decentralized oracle schemes is that they become unsafe if the amount of funds whose destination is affected by the oracle exceeds the market cap of the oracle token”

For a system like DAI, what if MKR and DAI are both designed to stake for the security of the oracle? Then could we reach an oracle that’s crypto-economically secure because the destination fund is on a similar order of magnitude as the value used to secure the oracle.

–

edited Apr 13, 2023

I believe I’ve answered by own questions. This present proposal is meant to be a reputation-based (hence the “not-quite-cryptoeconomic”) oracle design. VB has proposed a more cryptoeconomic oracle design here [UNI should become an oracle token - Proposal Discussion - Uniswap Governance](https://gov.uniswap.org/t/uni-should-become-an-oracle-token/11988).

---

**fewwwww** (2023-04-11):

DAI and MKR are essentially smart contracts on Ethereum, restricted by Ethereum. In contrast, for oracles, they are building new networks outside of Ethereum that are not controlled or restricted by Ethereum’s rules.

The challenge is still there, even after 3 years. Before this post was dug up, actually a few days ago, we wrote about [why an economic based oracle is hardly decentralized and secure](https://mirror.xyz/hyperoracleblog.eth/RA-c_9ydwKhSo-KV2Ti5Fu4YwThxSTQuBrlLX1_huFw). Essentially because it uses off-chain data (which Ethereum cannot control), the oracle network is directly related to the security of the application (and the profitability of the attack is not aligned with the value of the network), so the economic security of the oracle network is difficult to quantify.

These problems can occur in almost any oracle or middleware network (Chainlink, Flashbots, The Graph…). That’s exactly why we are building Hyper Oracle, a zk-based oracle/middleware network.

---

**claytonroche** (2023-04-12):

I believe in Vitalik’s post above, he’s referring to a [Schellingcoin](https://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed) economic security model. In the Schellingcoin model (and UMA’s), individual service providers do not issue data, but instead the entire protocol does – And so the entire protocol’s marketcap is on the line.

From your blog post:

> Overall, oracle networks and applications based on them are more affected by PoS with:
>
>
> service provider business model
> direct correlation of data correctness and PoS mechanisms
> same high potential profit of being hacked
> lower staking requirement and lower cost of being slashed

I agree with you that the service provider business model, which uses a “small slash for a small misbehavior” approach, is troublesome. Another example would be the [Venus exploit](https://beincrypto.com/venus-protocol-loses-11m-chainlink-suspension-luna-price-oracle/), which came as a result of Chainlink turning off support for LUNA price oracle, something you might expect to see from a Web2 SaaS product.

