---
source: magicians
topic_id: 5470
title: "EIP-3322: Efficient Gas Storage"
author: wjmelements
date: "2021-03-04"
category: EIPs
tags: [evm, opcodes, gas]
url: https://ethereum-magicians.org/t/eip-3322-efficient-gas-storage/5470
views: 3810
likes: 9
posts_count: 25
---

# EIP-3322: Efficient Gas Storage

https://github.com/ethereum/EIPs/pull/3322

## Replies

**wjmelements** (2021-03-04):

Yet another alternative would be to create a gas token builtin contract. That would avoid overhead from adding the gas refund counter field to accounts.

---

**MicahZoltu** (2021-03-05):

Copying my argument against this change from another discussion at [Let addresses directly store gas for refunds · Issue #3291 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/3291#issuecomment-785052942)

> Currently, block space is a resource that has a fairly even availability over time, similar to cloud servers, electricity, or space on a toll road. We do not have any way (currently) to move the supply around, just as you cannot move the supply of road space from night time to day time. Because of this, we do not want people to be able to pay off-peak prices in order to use space during on-peak hours. What we want people to do is move their usage to off-peak.
>
>
> There is currently a proposal floating around to remove refunds specifically because they are used predominately for paying off-peak prices for on-peak usage.
>
>
> What I think would be an interesting problem to solve is figuring out how we can move off-peak resources to on-peak time, so during peak season we have more resources available. One could imagine this like a battery, where you save up some off-peak space for on-peak demand. For example, if blocks are empty at night, we make up for that emptyness during the daytime. 1559 does this over very short time periods, and I’m not sure how to extend the strategy over longer periods of time other than changing the base-fee adjustment rate to be very slow (which has its own set of problems).

---

**chriseth** (2021-03-05):

I second Micah’s comments. Furthermore, I think that we should try to reduce the exposure of the EVM to gas mechanics instead of extending it. I would prefer to not complicate the EVM further (this adds state and yet another stack) and instead solve the problem outside of the EVM or even at the user level.

---

**wjmelements** (2021-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriseth/48/2111_2.png) chriseth:

> yet another stack

What do you mean? I don’t think it adds another stack.

---

**chriseth** (2021-03-09):

Right, I misread the EIP. It does not add another stack.

---

**timbeiko** (2021-03-15):

Copied from a [Github issue](https://github.com/ethereum/pm/issues/266):

> Adding 3 new opcodes and a 5th item to track with every account is too much for London. If it were to target Shanghai we could discuss the merits, but the timeframe makes this a non-starter because of complexity.

---

**wjmelements** (2021-03-15):

[@shemnon](/u/shemnon)

> Adding 3 new opcodes and a 5th item to track with every account is too much for London. If it were to target Shanghai we could discuss the merits, but the timeframe makes this a non-starter because of complexity.

- Modifications to refunds are being considered for London due to relatively urgent concerns about 4x elasticity with EIP-1559, and gas token storage.
- Any of my engineers should be able to implement and test this EIP in 2-5 days. If core developers are short on resources, we can help with implementations.
- As aforementioned, if the nullable account gas counter is a major concern, we could instead go with a gas token ERC20 precompile, though that would reduce extensibility and limit future innovation.

---

**wjmelements** (2021-03-15):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Currently, block space is a resource that has a fairly even availability over time, similar to cloud servers, electricity, or space on a toll road. We do not have any way (currently) to move the supply around, just as you cannot move the supply of road space from night time to day time. Because of this, we do not want people to be able to pay off-peak prices in order to use space during on-peak hours. What we want people to do is move their usage to off-peak.

I disagree with this. The greatest cost component of gas is the long-term cost, which is why gas limit discussions among miners focus on state growth rather than validation time. We are not close to being bound by short-term costs, so this proposal achieves what you describe later in your argument: shifting bandwidth from low-demand to high-demand periods. This proposal achieves that while still bounding the short-term overhead via the 2x refund limit.

As proof we are not bounded by short-term validation costs, as miners colluded to raise the gas limit from 10m to 12.5m, the uncle rate declined. If miners were even close to their validation limits, the uncle rate would have increased or perhaps stayed the same.

---

**shemnon** (2021-03-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Modifications to refunds are being considered for London due to relatively urgent concerns about 4x elasticity with EIP-1559, and gas token storage.

These are not mutually exclusive proposals.  Just because phasing out gas refunds goes in for London does not preclude this from being added to Shanghai or later. If this is desirable and has net positive value it can very easily go in then.

> Any of my engineers should be able to implement and test this EIP in 2-5 days. If core developers are short on resources, we can help with implementations.

I think that obscures the true cost. First the PRs would need to be reviewed by the client teams.  My experience has been that this can be 50% to 100% as much effort as simply writing a PR from a client team member.  There are many distant side effects in each client that needs to be considered.  Second, the reference tests need to be written and accepted by the EF’s testing team.  Even if provided externally they have very specific desires that are not always well documented and will also add to the gaant chart.

There are also the coordination costs relating to getting this tested on a YOLO network prior to production testnets. And the slowdown that invariable happens when interpretations of sections vary slightly or are mis-read.

There’s also the implicit safety concern of having one team implement a feature in all of the mainnet capable clients.  Do you have a financial interest in seeing this passed?  If so would you be willing to post a grant to allow at least one of the client teams to implement it themselves or via bounty?

> As aforementioned, if the nullable account gas counter is a major concern, we could instead go with a gas token ERC20 precompile, though that would reduce extensibility and limit future innovation.

That would have a worse effect on state storage IMHO, there would need to be two reads down the account trie (but the ERC-20 trie would be smaller).  If kept it should be part of the account record.

The downstream impact on other specs like Binary tries are my concern here.   They have 4 items enshrined fairly deeply in the details of the implementation (by overwriting two bits of an account hash).  This would either need to be rethought (with separate data forks down the trie) or the bit space increased to three.

>

However my deepest concern is that this will enshrine arbitrage as a core feature of the protocol, whereas before it was an emergent behavior.  I think some deep thought needs to go in to the follow on effects of such a movement before it is put into effect.  For one this will have a negative impact on miners and block producers (post-PoW) in that the gas fee for the tip will be reduced during spike times and replaced with lower fee gas consumption.  They may start playing MEV games like excluding accounts with high gas storage during high tip periods.  Moving it into account data rather than in the various gas tokens make it easier for the MEV miners to identify such transactions, at least for the transaction issuer.

When I say “too complex for London” its this kind of secondary effect that I am referring to.  I don’t think there is nearly enough time to think out the impacts of this between now and when we have to stop adding to the EIP candidate in 2-4 weeks.

---

**wjmelements** (2021-03-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> They may start playing MEV games like excluding accounts with high gas storage during high tip period

So-long as the refunds are not counted against the gas target, such behavior is unprofitable. The proposal is in many ways a continuation of the status quo so I do not anticipate secondary-order effects besides supplanting storage-based gas tokens.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> That would have a worse effect on state storage IMHO, there would need to be two reads down the account trie (but the ERC-20 trie would be smaller). If kept it should be part of the account record.

This is unintuitive for me; I would expect the ERC20 approach to use less space, but I don’t work on the trie.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> There’s also the implicit safety concern of having one team implement a feature in all of the mainnet capable clients. Do you have a financial interest in seeing this passed? If so would you be willing to post a grant to allow at least one of the client teams to implement it themselves or via bounty?

That would also be acceptable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> For one this will have a negative impact on miners and block producers (post-PoW) in that the gas fee for the tip will be reduced during spike times and replaced with lower fee gas consumption.

Boo-hoo. Think about the users, not the service providers. We can smooth peak congestion by amortizing its costs, and we should.

---

**shemnon** (2021-03-16):

‘Boo-hoo’ to the miners is not a constructive response.  That’s what’s causing the EIP-1559 mess.

---

**wjmelements** (2021-03-16):

The important difference between what you are advocating and 1559 is that refunds are the status quo. From a miner’s perspective the marginal difference is that the elasticity costs less storage.

---

**shemnon** (2021-03-16):

But what is not different is the dismissiveness shown to miners.  There is also the consideration of block producers for Eth 2, their marginal reward will be lower so there is a greater incentive to ensure that they get the most tippable gas out of the transaction.

The status quo is that gas arbitrage is an emergent behavior, not a deliberate design choice. I have concerns about regulatory capture if we make it explicit in the protocol.

---

**wjmelements** (2021-03-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I have concerns about regulatory capture if we make it explicit in the protocol.

What do you mean by regulatory capture?

---

**bradleat** (2021-03-16):

Your post makes me think that you’d want to enable a futures market for gas.

---

**wjmelements** (2021-03-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriseth/48/2111_2.png) chriseth:

> Furthermore, I think that we should try to reduce the exposure of the EVM to gas mechanics instead of extending it.

Having used the `GAS` and `GASPRICE` opcodes, and planning to use the `BASEFEE` opcode, I disagree. Gas is the best feature of the EVM; it’s how we meter the use of shared resources and prevent DoS.

---

**mtefagh** (2021-03-28):

This EIP incentivizes users to bulk purchase gas whenever the price is low. These mass buyers would benefit a lot more if we combine this with EIP-1559. The problem is that EIP-1559 does not account for slippage. I have already discussed this point two years ago in [here](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/26) (last paragraph). Users are paying for the burden which the previous users put on the network rather than their own. Hence, if we start hoarding gas by making an otherwise under-used block full, then the users in the next block will have to pay the extra charges while we spend the stored gas gradually. This gets even worse when we realize that EIP-1559 tells us that if we see a usage spike in the current block, then the gas price will go up sharply in the next block. Therefore, rational users are incentivized to pre-purchase gas for the next block, which in turn, makes the current spike even sharper. This is the opposite of what happens if we had considered slippage by simply replacing the gas used in the previous block with the gas used in the current block in the update rule’s formula.

---

**wjmelements** (2021-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mtefagh/48/1890_2.png) mtefagh:

> Therefore, rational users are incentivized to pre-purchase gas for the next block, which in turn, makes the current spike even sharper

It’s cheaper for them to buy it on a DEX than to mint it themselves in this case. Available liquidity is much deeper than the current block.

---

**pipermerriam** (2021-03-29):

> Disclaimer that I haven’t read the discussion above.  Posting this here just so that my opinion is documented in the official discussion.

I am strongly opposed to enshrining the concept of “gas tokens” into the protocol.

- refunds are of questionable usefulness and have not been shown to be an effective measure to mitigate state growth.
- 1559 already provides elasticity for the “supply”
- the current plans to mitigate state growth are fully independent from the refund mechanism

These lead me to my opinion that this introduces significant complexity with minimal benefit.

---

**wjmelements** (2021-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pipermerriam/48/65_2.png) pipermerriam:

>

> refunds are of questionable usefulness and have not been shown to be an effective measure to mitigate state growth.

Strongly refuted [here](https://ethereum-magicians.org/t/eip-3298-removal-of-refunds/5430/10)

> 1559 already provides elasticity for the “supply”

To handle peak congestion we will need to be able to sustain >1x throughput for much longer than allowed by 1559, while still amortizing the long-term costs, which are not limited to state growth. There is no reason that bandwidth costs should surge 50x when usage increases 3x for a few hours. Grocers don’t raise their prices in the afternoon; they hire part-time workers.

The elasticity of 1559 is unproven on a congested blockchain, and may not come until PoS due to [increased uncle risk under PoW](https://medium.com/@willmorriss/block-bulimia-in-eip-1559-b4576a9bab55). Consider deferring your judgment about the elasticity provided by 1559 when it wasn’t designed to provide it, but instead to pump the ETH price.

> the current plans to mitigate state growth are fully independent from the refund mechanism

If you prefer state rent, I encourage you to live with it for 10 years before forcing it on everyone else. You may find it annoying that the ENS handle you had reserved for 100 years is gone now, the few who have the info you need to prove it back into existence are charging you a fortune for the privilege, and the state size has not actually shrunk because of the stubs. It’s unreasonable to plan around a system that nobody has a good design for, never mind an implementation. State rent is a pie-in-the-sky solution to numb you until we realize state growth is not that bad when we let the miners-soon-stakers who pay for it set hard limits on its growth.

> These lead me to my opinion that this introduces significant complexity with minimal benefit.

The complexity is 32 bytes per contract account that stores gas. I don’t recommend storing this attribute on every account by default. The benefit is that this uses significantly less storage for more elasticity than provided in the status quo. If you don’t care about storage you must not run a node.

edit: formatting


*(4 more replies not shown)*
