---
source: magicians
topic_id: 2552
title: How much should I care about the price of ETH?
author: lrettig
date: "2019-01-31"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/how-much-should-i-care-about-the-price-of-eth/2552
views: 3171
likes: 23
posts_count: 17
---

# How much should I care about the price of ETH?

There have been a couple of interesting threads on this topic on Twitter lately. This is my effort to move the conversation over here in threaded format:



      [twitter.com](https://twitter.com/ameensol/status/1090040726086250497)



    ![image](https://pbs.twimg.com/profile_images/1881042351398776833/3HJEJCp__200x200.jpg)

####

[@ameensol](https://twitter.com/ameensol/status/1090040726086250497)

  So long as security is a function of market cap (which it is in all PoS systems) anyone designing these systems needs to think about *and optimize for* price of the staking token.

  https://twitter.com/ameensol/status/1090040726086250497










https://twitter.com/ameensol/status/1090841973466947585?s=20

As a core developer, I don’t feel that it’s my job to a. follow the price of ETH, b. care about the price of ETH, or c. optimize for the price of ETH. As Justin says here, the price is an “external factor” that’s going to do what it’s going to do – the markets are stupid and irrational and should not have an impact on our building.

https://www.reddit.com/r/ethereum/comments/ajc9ip/ama_we_are_the_eth_20_research_team/eeyqlro/

However, as [@ameensol](/u/ameensol) and several other community members have pointed out, we should be concerned about price in so far as a more valuable currency makes for a more secure network – this is true in both POW and POS.

Some have also pointed to the concept of [reflexivity](https://www.investopedia.com/terms/r/reflexivity.asp) which, if I understand correctly, suggests that investors’ *perceptions* matter as much as reality and in fact there is a feedback loop whereby these perceptions can lead to price movements that are detached from reality. The risk here would be that a perception on the part of app developers or investors today that Ethereum was losing its lead could be a self-fulfilling prophecy that could in fact cause it to lose its lead.

One reason I’m unconvinced that the price of ETH matters is because I feel that, in theory, we could take all of the things that make ETH great – smart contracts, the VM, the tooling, the apps, the community, etc. – and migrate it so that its base-layer security depends upon Bitcoin, or Polkadot, or some other protocol, *if* that protocol hypothetically proved more secure.

I can see both sides to this story and I haven’t yet figured out how to reconcile these two opposing ideas but I’m curious to hear what others think.

## Replies

**tomislavmamic** (2019-01-31):

I’d like to add another question to this thread.

At what price of ETH does Ethereum network become insecure?

---

**lrettig** (2019-01-31):

Another interesting perspective. [@lkngtn](/u/lkngtn) suggests that maybe we should not try to have a staking token that’s also a “money” or SoV token:

https://twitter.com/lkngtn/status/1091009832730222594?s=20

---

**ryanseanadams** (2019-01-31):

> As a core developer, I don’t feel that it’s my job to a. follow the price of ETH, b. care about the price of ETH, or c. optimize for the price of ETH. As Justin says here, the price is an “external factor” that’s going to do what it’s going to do – the markets are stupid and irrational and should not have an impact on our building.

So I think we should clarify so we’re not discussing the wrong position: I’m not seeing anyone arguing that developers should optimize for the price of Ether in the short run, only that they should optimize for Ether price in the long-run. And of course, they’re also not saying the price of Ether is the only thing to optimize for, only that it should be one of several of Ethereum’s stated [design principles](https://notes.ethereum.org/9l707paQQEeI-GPzVK02lA).

I plan to reply further with some reasons for the Price Matters position, but I think this clarity is warranted before we start debating the wrong position

---

**clesaege** (2019-01-31):

We need to think about what are our targets:

**Make the ETH buyers rich?**

Well this one is self explanatory.

**Develop an ecosystem?**

The price is important here. Higher ETH value means more money for projects. Either by adopters now having extra capital to start new projects (that was my case). Or putting this money into new ones (token sales). Those projects then reinforce the ecosystem, thus the price, creating a positive feedback loop.

**Make a secure system which cannot be attacked?**

- With proof of work, the higher the ETH is, the higher are incentives for miners to mine securing the network. Thus, the most costly 51% attacks are.
- With proof of stake, higher ETH price, means higher budget (what you need to do an attack) and cost (what you loose when doing it as you’d probably be forked away) of doing a 51% attack.

So yes price matters. We’ve seen a lot of craze in 2017 and as a community more or less decided to stop talking about the price. This was probably a good move to attract builders by distancing us from other “get-rich-quickly” schemes which flourished in the bull market.

But now I think we have overshot, and it may be one of the reasons ETH price was more impacted than BTC. Funding is starting to become an issue and we need to find solutions.

---

**ameensol** (2019-01-31):

I replied to your tweet with one of mine but wanted to post it here too:

[Regarding the social norms of “don’t talk about prices”]

https://twitter.com/ameensol/status/1090051455237611520?s=19

---

**lkngtn** (2019-01-31):

> As a core developer, I don’t feel that it’s my job to a. follow the price of ETH, b. care about the price of ETH, or c. optimize for the price of ETH. As Justin says here, the price is an “external factor” that’s going to do what it’s going to do – the markets are stupid and irrational and should not have an impact on our building.

I think it is fair for a core dev to not worry about price at all, but if you are involved in specifying the economic aspects of the protocol it is absolutely critical to think about the economic dynamics of the system including price (and many other factors).

> Another interesting perspective. @lkngtn suggests that maybe we should not try to have a staking token that’s also a “money” or SoV token:

I’m not sure if this is completely on topic with regard to whether devs should care about ETH price, but since the twitter thread was posted I figured I would clarify and expand on my position.

I think it is a mistake to attempt to design a token to take on the dual purpose of staking and as a store-of-value currency/commodity money. Though I do believe that having a native store-of-value asset is important for capital allocation, investment, and healthy ecosystem growth.

My suggestion, which has already be explored by [Cosmos](https://blog.cosmos.network/cosmos-fee-token-introducing-the-photon-8a62b2f51aa), is to separate the staking token economics from that of the fee token economics. There are a few intuitive reasons why this might be a good idea:

1. The utility of a fee token (commodity/currency) is improved with liquidity, and by the predictability and stability of issuance.
2. Security of a proof of stake network is improved by illiquidity. It is much more difficult (or at-least more time consuming) to acquire a significant amount of an illiquid asset in order to perform an attack, and if your attack fails and you are slashed (in protocol or via a fork) both the capital cost and time cost must be considered.

The liquidity of a token can be influenced by a dynamic supply policy, which adjusts the inflation rate based on a target percent of the supply which is locked up to stake. See [this article](https://medium.com/@petkanics/inflation-and-participation-in-stake-based-token-protocols-1593688612bf) about participation rate targeting for a more thorough exploration.

If a single token is used for both fees and staking, adopting such a policy in order to make the token price illiquid (and as a result more volatile) would come at the expense of the utility and practicality of the fee token. But if these tokens are kept separate, we can optimize liquidity of the staking token independently of the issuance policy for the fee token.

The goal of staking protocol design should be to optimize for cost-effective security. We want to be able to process many transaction at low cost and we want to be able to create and secure value on top of the protocol. One way to increase security is to increase token price and market cap, as this represents the budget an attacker would need to perform an attack. This is intuitive and easy to quantify–but this is not a particularly efficient means to increase security.

There may be many optimizations, some of which we have yet to even conceive, which become possible over time. We may move away from from proof-of-stake and instead rely on Web-of-Trust graphs for social sybil resistance in order to provide more cost-effective security and better decentralization and means of more fair and sustainable wealth distribution. We may use tokens to emit reputation for staking, to further manipulate liquidity of the validator set and reduce the capital costs of validating the network.

By tightly coupling the fee token and speculative value capture to the economics of the staking token we significant limit our current and future options in terms of optimizing for cost effective security. I suggest we optimize for the value proposition of participating as a validator without trying to optimize issuance to imbue the staking token with store-of-value properties, and instead optimize a separate token for store of value properties (including using it as the designated payment token for transacting on the network or paying storage rent).

---

**lightuponlight** (2019-02-01):

1. The price of ETH ultimately pays for most of the ongoing development for Ethereum as well as projects using Ethereum.
2. The price of ETH must be as high as possible to allow high-value tokens, such as bearer instruments, to live securely on Ethereum.
3. The price of ETH generally provides security to prevent 51% attacks on the network, even if Ethereum isn’t hosting a lot of high-value bearer instruments.
4. The price of ETH signals to potential developers that Ethereum is a worthwhile platform to consider for their projects.
5. Lastly, an increasing price of ETH provides the future economic livelihood (ie. retirement) for most participants in the ecosystem.

So overall, increasing the price of ETH is imperative for making Ethereum a successful platform now and into the future.

---

**madcapslaugh** (2019-02-01):

Ultimately price will reflect the greatest amount of value being provided in the world.

There were two comments you made that struck me as noteworthy, to paraphrase:

1. I don’t care about the price of ETH
2. I don’t care who “wins” as long as we get the vision of Web3

To reiterate what many others in this thread have mentioned, the price of ETH is strongly correlated with the security and thus usefulness of the Ethereum platform. Low cost ETH means a few things which hurt the Ethereum platform

A) cost of an attack is low

B) funding for future development is low

C) funding for supporting innovative 3rd party development teams is low

Regarding the second point, given your critical role in developing the future of Ethereum, it would strike me as more effective if you had an attitude that included the following points:

1. I want to do everything I can to make Ethereum into the most useful and value generating platform in the world
2. I want to build something that captures the attention of the largest group of developers building things in the Dapp space, and make sure that my platform is the best platform for the largest group of people. I want to enable these people to most easily create the most value and ship good products to market that change the world
3. I want to be a thought leader, and innovator, I want other blockchain/smartcontract teams looking at what we are doing and learning from us and trying to catch up to us, because we are nailing it
4. I want to be able to support my family, and those in need through the financial reward my contribution to this innovation will generate

When I hire developers, these are the attributes that I look for, and these are the attributes I would hope to see in the Ethereum team, which is responsible for what may be the most important technical project of our lifetime.

If you truly believe that what is most important it the general success of Web3 and IoV, know that if Ethereum flops due to continuous missed deadlines, and economic policies that do not capture dollar value, it will significantly delay the revolution we are all hoping for.

You are in a powerful position, have your ideals, don’t just work for money, but never forget what a tool money can be.

---

**lrettig** (2019-02-02):

Regarding your first point, I somewhat reluctantly admit that you are right. Price does matter in a macro sense. It is necessarily something that I and other core devs should keep in mind, but it is not my number one priority. I’d say my number one priority is to remain true to my values and do all I can to realize my vision for what Ethereum, Web3, and this technology and community in general have the potential to do and to become. I’d say my number two priority is good code, good engineering, good governance, etc. (“good work”).

The good news is that all of these goals are bound up into tight positive feedback loops: optimizing for values, good engineering, and good governance should all contribute to macro-level value accrual to the network and its native token.

Regarding the second:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/madcapslaugh/48/1499_2.png) madcapslaugh:

> I want to do everything I can to make Ethereum into the most useful and value generating platform in the world
> I want to build something that captures the attention of the largest group of developers building things in the Dapp space, and make sure that my platform is the best platform for the largest group of people. I want to enable these people to most easily create the most value and ship good products to market that change the world
> I want to be a thought leader, and innovator, I want other blockchain/smartcontract teams looking at what we are doing and learning from us and trying to catch up to us, because we are nailing it

I generally agree with these goals, with one critical caveat: *they only apply as long as I believe Ethereum is the platform that is truest to my values and most likely to achieve my vision.* I won’t let ego become a part of this, and the work that’s already gone into the project is a sunk cost. I wouldn’t hesitate to “jump ship” if I were confident that another project were more values-aligned and/or more likely to achieve this vision.

For instance, I think the wealth distribution in Ethereum is atrocious and it keeps me up at night. If another platform existed that were identical to Ethereum in every way but had a fairer wealth distribution, I would prefer that one.

I’m working towards a vision, not a specific brand.

In reality, I don’t think it would ever be that black-and-white. As a concrete example, even if, hypothetically, Polkadot/substrate were to prove a superior technology, there are a thousand ways it and Ethereum could be made compatible.

Let me be very clear: Ethereum is far and away the platform that best satisfies these conditions at present, and I think it’s unlikely that will change anytime soon. But I won’t close myself off to that possibility entirely. To do so would be antithetical to everything I’m building towards. I don’t believe in blind loyalty, maximalism, dogmatism, or “chain nationalism.”

Some may be more self-interested than I and may prioritize other things over “vision” and “values.” That’s fine, I respect that too. I speak only for myself.

---

**lrettig** (2019-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/madcapslaugh/48/1499_2.png) madcapslaugh:

> Ultimately price will reflect the greatest amount of value being provided in the world.

I just reread this. What an interesting point! I’m not sure I agree with this. This is sort of one definition of capitalism. I’m not anti-capitalist by any means, but I’m totally unconvinced that markets have succeeded in capturing every form of “value” that matters in the world. Certain forms of art and self-expression, public goods, and human welfare and dignity are all examples of things that markets do not accurately reflect.

We should take this point to [www.etherean.org](http://www.etherean.org) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**madcapslaugh** (2019-02-03):

When the value of the subnetworks that Ethereum provide security too surpass the value of Ethereum. For example, let’s say the market cap of ETH was $100, and I build a network on top that is valued at $1000. Now the potential gain from an attack on the Ethereum network is too high for me to safely grow my DAO. I will need to migrate to a security layer with a higher market cap, and thus a greater cost for a 51% attack.

---

**lrettig** (2019-02-04):

I think this could go either way: either Ethereum could cap the growth of your protocol, or your protocol could raise the value and overall security provided by Ethereum (“a rising sea lifts all boats”). In practice I think both effects would play out, so it would be very interesting to see which one would dominate. My gut tells me that it would be the latter, due to network effects - that as apps and protocols like Maker continue to grow and gain in value, they’ll lift all other apps and protocols deployed on Ethereum along with them.

---

**ryanseanadams** (2019-02-07):

Here’s the argument I published in eth.research [previously](https://ethresear.ch/t/in-defense-of-ethereum-and-its-fatness-a-discussion-of-eths-value-capture-potential/3913/24?u=ryanseanadams):

I haven’t seen any conversation related to the money thesis in this thread, yet this is where the underlying value of BTC seems to resides (just ask the BTC community). The idea: a sufficiently hard (difficult to inflate) commodity asset can become a money by first becoming a Store of Value, then a Medium of Exchange, and finally a Unit of Account. (Note: this can happen in parallel in a series of adoption waves) This is the path taken by Silver, then later dominated by Gold. Gold itself has low utility value (e.g. industrial use), but high monetary premium (e.g. gold bars in vaults) due to its history as a Store of Value. It is moated by strong network effects.

Monetary premium can quite literally be memed into existence.

Why does this matter?

If Ether does not become some form of money, it will not have a monetary premium. If no monetary premium, the security of the Ethereum network will be less than the security of a similar network whose underlying asset has monetary premium, thus Ethereum will not be most secure. If Ethereum is to continue hosting currencies (e.g. DAI) and high value financial assets (a decentralized world financial stack), it must be competitive as the most secure network.

Given this, it seems we should encourage Ether’s use as a money, both in protocol economics & issuance policy.

---

**lrettig** (2019-02-07):

There is a very, very deep rabbit hole of threads on this topic from some smart, important people in this Twitter thread and they don’t all agree on these points:

https://twitter.com/licuende/status/1093056334289883136

---

**CRN** (2019-04-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> One reason I’m unconvinced that the price of ETH matters is because I feel that, in theory, we could take all of the things that make ETH great […] and migrate it so that its base-layer security depends upon Bitcoin, or Polkadot, or some other protocol,  if  that protocol hypothetically proved more secure.

Does this statement assert that the price of ETH can be dismissed without dismissing the importance of security? That would be false, as there is agreement that price matters for security in POW and POS.

Or is the above statement saying that price of ETH, and by extension the security of Ethereum, doesn’t matter because we could always migrate to a network that is more secure? That also seems untenable, for if that other hypothetical network proved more secure because it included price as a priority, then we would be valuing the priorities of other developers more highly than our own. Clearly, if we value price as a priority in another network enough that we would migrate to it for its security benefits, then we should value that priority with Ethereum as well.

---

**lrettig** (2019-04-04):

My views on this have matured a bit as I’ve thought more deeply about it. Clearly we cannot rely upon the base-layer security of another network without outsourcing important decisions about security to that network. (It’s a little like a country choosing to peg its currency to the USD, which in practice outsources its monetary policy to the Fed.)

Also I’m not even sure this would be possible with a network that doesn’t have smart contracts, like Bitcoin. Could Ethereum’s security *theoretically* be anchored in Bitcoin by e.g. checkpointing to it every so often, like RSK?

