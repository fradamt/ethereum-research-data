---
source: ethresearch
topic_id: 8801
title: How to Implement Digital Community Currencies with Ethereum?
author: chnejohnson
date: "2021-03-03"
category: Applications
tags: []
url: https://ethresear.ch/t/how-to-implement-digital-community-currencies-with-ethereum/8801
views: 3575
likes: 3
posts_count: 12
---

# How to Implement Digital Community Currencies with Ethereum?

Hi everyone,

I want to start a discussion about building a boilerplate of [local currency](https://en.wikipedia.org/wiki/Local_currency) (or complementary currency) system for local residents with solidity.

In economics, a local currency is a currency that can be spent in a particular geographical locality at participating organizations.

There are some example in this world. Fuse is a company which provides communities to issue ERC-20 token and paying with their wallet service. Besides, there is an another practical story I have heard. There’s a lady in Kenya, created a set of local digital currencies in slums. The key was that there was a central community owned business whose revenue acted as the backing for the local currency. So if the business earned $1000 of Kenyan shillings and there are 10000 units of slumCoin in circulation then each slumCoin is worth $0.1. The currency was dished out like a UBI (Unconditional Basic Income) to residents and they could transfer via phone with QR codes like regular crypto but the currency was geofenced.

In my opinion, a local currency aims to encourage spending within a local community, especially with locally owned businesses. So the difference between local currency and most of Ethereum projects (De-fi, Gitcoin, etc…) is that local currency can only be used in the particular region. It can not get access on the internet for everyone.

As you may imagine, people would use local currency for local living, such as paying for daily necessities. Under the vision, we should have a boilerplate of the token smart contract (like ERC-20) and the wallet app (such as argent because of its feature of ETH-less account). If there is a boilerplate, any local organizations in the world can use that template, deploying their own token contract and developing their own mobile wallet app for their local communities.

The benefits of digitalization of local currency, is that when the currency is in circulation, it would be more easily to implement idea written in Radical Markets, including Common Ownership Self-Assessed Tax or Quadratic Voting, or Quadratic Funding for local public goods written in Liberal Radicalism. It seems like an ideal high-tech local community we could build in the future.

Practically, some of the local currency in circulation, has the price linked to another currency like fiat currency or cryptocurrency. But I think the key is that local currency must not link to any currency. It means that the local issuer (maybe a civil township or public interest groups) issue the local currency which is valueless, just like bitcoin, in the beginning.

The valueless currency would like a [shell money](https://en.wikipedia.org/wiki/Shell_money) as the medium of exchange in the primitive tribe, and the value of the currency would be gradually determined by the local markets of goods and service.

To achieve this goal, the token contract should prevent token from being transferred to the outside of the particular geographical region because a local currency aims to encourage spending within a local community.

So, there comes to my final question I want to discuss: How to write a simple token contract which token can only be transferred within the specific geographical region?

I got some answers and I summarized as follows:

1. Use an oracle from the smart contract to fetch those data and revert depending on the IP address.
2. Creating a whitelist of addresses that will be the only ones to transfer local currency.
3. The project FOAM which provides the tools to enable a crowdsourced map and decentralized location services. (actually I haven’t understand how they work…)

Thank you for reading. My english is not so good, so the grammar or words may look weird…

Any questions, resources, ideas would be greatly appreciated.

## Replies

**dankrad** (2021-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/chnejohnson/48/7804_2.png) chnejohnson:

> Use an oracle from the smart contract to fetch those data and revert depending on the IP address.

This is impossible, as there is no IP address associated with a transaction once it has reached the mempool. The oracle would have to use quite advanced techniques to get this data, and it wouldn’t be reliable.

![](https://ethresear.ch/user_avatar/ethresear.ch/chnejohnson/48/7804_2.png) chnejohnson:

> Creating a whitelist of addresses that will be the only ones to transfer local currency.

I think this is your only option. Note that this doesn’t mean the currency can’t be spent outside the geographic region; but this restriction isn’t meaningful because transactions on Ethereum are global and simply can’t be restricted. The restriction would purely be to person/businesses who have some kind of link (e.g. a residence address) in the region, and if they have another branch/residence outside that region they can still use the token there.

---

**chnejohnson** (2021-03-04):

The loss of **whitelist** solution is that:

1. the token issuer must do KYC to the residents. In this way, issuer becomes a centralized person (or organization) to operate the local currency. They can control who can use the token.
2. as you said, members in the whitelist outside the region can also transfer the token. It means that the local currency system cannot prevent token from leaking out of the region. At worst, there is a possibility that bad person in the whitelist have a chance to manipulate the price of local currency on the internet.

Although there is currently no method to restrict the transfer function only called in the particular region, the meaning of the restriction is that it promise the job of local currency for local economy.

Besides, if there is a geofence, the token issuer do not need to do KYC. It would be **more decentralized**, and the money transfer could be easily done without validating whether the person is in the whitelist.

---

**chnejohnson** (2021-03-05):

I found the best expression of this discussion should be Digital Community Currencies, like this report: [Digital community currencies for global challenges](https://discovery.rsm.nl/articles/368-digital-community-currencies-for-global-challenges/).

Besides, I gradually agreed the whitelist solution for resolving restriction of geographical region. And I want to extend the thoughts about implementing the whitelist.

I think the power of adding/removing members in the whitelist should not be centralized by a man or an organization. We should figure out a mechanism about whether the member is in the whitelist should be determined by the community. For example, a person who wants to participate into the whitelist must be agreed by two members in the whitelist.

There are many ways to design this mechanism. Perhaps [EIP-1261](https://eips.ethereum.org/EIPS/eip-1261) is one of it. Look forward to further discussions and resources.

---

**pmcgoohan** (2021-03-11):

You could fork geth and add a restriction that will only peer with nodes from a certain ip range, then run your own local blockchain.

---

**chnejohnson** (2021-03-11):

Does the local blockchain connect to Ethereum main network? I think it does not, so the currency would not be decentralized, and it can be controlled by the operator. It would be useless to use Ethereum instead of traditional backend.

---

**pmcgoohan** (2021-03-12):

How decentralized and secure it is would be a function of how many nodes the community runs, as always with any blockchain.

---

**chnejohnson** (2021-03-12):

Oh, you mean we could create some nodes restricted in a certain ip range for running my own blockchain, so that the node outside the ip range cannot verify the transaction.

But the problem of digital community currency is that we should prevent token from transferring to the address which is outside the local region. I think in your case, people could still transfer token to the address outside the region, and the transaction is verified by the node in the specific ip range.

---

**monsterd0n** (2021-03-13):

in order to prevent re-inventing the wheel - have you looked at other initiatives of local [community inclusion currencies](https://gitlab.com/grassrootseconomics/cic-docs/-/blob/master/README.md) on xDai, etc?

Here is a highlevel read on this topic: [The impact of community currencies in low-income communities — TK Matima](https://www.tkmatima.com/blog/impact-of-community-currencies)

---

**johnx25bd** (2021-03-14):

Geographically-bound currencies is a strong example of the many use cases for geospatial analytics capabilities in smart contracts.

We haven’t given much thought to local blockchains or restricting transactions based on IP address, but it does seem like this could possibly be easily spoofed or gamed - and as chnejohnson mentioned, restrict the system from benefiting from a globally decentralized network.

For a geofenced token - one that can be spent by anyone within a specific geographic area (polygon or polyhedron), transactions - one approach would be to include a wallet owner’s geographic location as one of the parameters passed into the `transfer` function of the smart contract.

In the body of the function, the code would `require` that the point is within the polygon representing the geographic zones, only letting the transfer invocation proceed if that condition is met.

[![pt-in-poly](https://ethresear.ch/uploads/default/original/2X/1/1b2acb59528466fc11ed22b0f97eadbfd6007a86.gif)pt-in-poly317×200 4.67 KB](https://ethresear.ch/uploads/default/1b2acb59528466fc11ed22b0f97eadbfd6007a86)

There are a few real challenges here. The first: verifying the location proof. Technically it is *extremely* difficult (if not impossible) to create a definitive proof that some information was created at a specific physical location.

There are technical ways to improve trust in the position - signing position captured by the sensor triangulating with the GPS or FOAM network in a secure enclave, for example. It would require a special app or - eventually - a plugin for mobile crypto wallets that allows users to generate the **“universal location check-ins”** (credit [@jabyl](/u/jabyl) from Distributed Town for the term and his help thinking this through). Otherwise, incorporating other sensor readings (like from a camera or microphone) could help build trust, as could requiring users to scan a cycling QR code only available at the location, form social check-ins in which they verify that the others were present, etc. We’re in early stages of working out the best ways of trusting verifiable location proofs.

The other obvious concern is privacy. Sharing where I am on a blockchain? Lots of people would be rightfully concerned. In some contexts it might be ok - people broadcast their locations publicly when they check in on Foursquare or geotag an Instagram post or tweet. But building in privacy by design would unlock many additional applications.

We’ve been doing some early thinking about **zero-knowledge location proofs**, which prove that a point is inside a polygon without revealing the user’s position. This could then be verified on chain in the require statement. I have no idea what work on this has been done - [@tux](/u/tux) at NuCypher was interested but not sure if they’ve looked at it any further. We don’t have any cryptographers working with us so right now it’s just speculation lol … this cryptographic primitive could have profound implications in so many contexts - for example, in physical security applications, international relations, intelligent mobility systems etc.

We’re working on the tools developers will need to build location-based dapps and spatial contracts at [Astral](https://astral.global/). A few years ago we prototyped a location-aware wallet contract at ETHParis, have been continuing to develop [Spatial.sol](https://github.com/AstralProtocol/spatial-sol), a Solidity library of geometric and topological functions.

We’re also working on verifiable spatial data registries that could support these kinds of geospatial applications. Build some prototypes with the LABS team you could look at - Hyperaware’s Jurisdiction Registry and Geolocker. We think these verifiable spatial data registries could be the basis of the composable location-based decentralized web.

We’d love to collaborate with anyone working on these ideas ![:folded_hands:](https://ethresear.ch/images/emoji/facebook_messenger/folded_hands.png?v=14)![:sparkles:](https://ethresear.ch/images/emoji/facebook_messenger/sparkles.png?v=14)

---

**bradleat** (2021-03-15):

I think the solution here is low tech. By creating many different local currencies and providing an additional service (analytics or visibility into the local economy), you’ll empower the use of local currency, locally.

If you want to get more blockchain about it but accept some censorship into your local economy, you can require well known local entities to serve as the backstop for the local currency. The local entities would be required to (every epoch) provide local codes to anyone who requests them. However, the method of serving the code is an offline device with a known public key that signs: the epoch, a nonce, and the requester’s public address. When someone wants to spend money in the local economy, they would hash their local code and transaction body.

If anyone’s local code is ever found online, their account may be slashed. The slash is split between being burned, and going to the submitter of the local code.

---

**chnejohnson** (2021-03-17):

Thank for everyone’s replies. I have to summarize this topic here.

About what **community currency (or local currency)** is, the article below really explain it all.

![](https://ethresear.ch/user_avatar/ethresear.ch/monsterd0n/48/5621_2.png) monsterd0n:

> Here is a highlevel read on this topic: The impact of community currencies in low-income communities — TK Matima

Quote one of its paragraph:

> community currencies are complementary mediums of exchange to a national currency and serve a particular purpose - stimulating local economies during times of business downturns and help provide for basic needs when the national currency is in short supply.

And an excellent example of implementation is **community inclusion currencies** (CICs) in Kenya by Grassroots Economics and Bancor.

CICs was built on xDai and its [smart contract](https://github.com/GrassrootsEconomics/CIC-Liquid-Token/tree/master/solidity/contracts) integrated with Bancor Network, running on the way they called “tokenomics”. (see their [white paper](https://gitlab.com/grassrootseconomics/cic-docs/-/blob/master/CIC-White-Paper.pdf) in Chapter 2). There is a complex economic mechanism about seeding CICs liquidity pool, which is the simplified story I heard.

![](https://ethresear.ch/user_avatar/ethresear.ch/chnejohnson/48/7804_2.png) chnejohnson:

> there is an another practical story I have heard. There’s a lady in Kenya, created a set of local digital currencies in slums. The key was that there was a central community owned business whose revenue acted as the backing for the local currency. So if the business earned $1000 of Kenyan shillings and there are 10000 units of slumCoin in circulation then each slumCoin is worth $0.1. The currency was dished out like a UBI (Unconditional Basic Income) to residents and they could transfer via phone with QR codes like regular crypto but the currency was geofenced.

### Transfer Restriction

About the question I asked that **how to write a simple token contract which token can only be transferred within the specific geographical region**, the purpose of it is to prevent currency from leaking out of community, there are two approaches:

1. identity-based: There are many methods to do the KYC, for example: A person who want to join the community should be verified in person by well known local entities, or referred by a member, and verified by another one.
2. location-based:
Thanks for johnx25db’s great work in Spatial.sol, although the technology seems difficult for me, the geofenced solution may be the way to solve this problem in the long term.

These two approaches refers to johnx25db’s Spatial.sol mentioned:

> we each engage in a social contract to adhere to two forms of governance: identity-based and location-based. Identity-based governance mechanisms are most often opt in, though smart contracts may enforce these more successfully. Location-based governance mechanisms depend on where our bodies are on the Earth: which jurisdiction we are in.

### Does restriction of transferring really matters?

Maybe not. As bradleat said:

![](https://ethresear.ch/user_avatar/ethresear.ch/bradleat/48/527_2.png) bradleat:

> By creating many different local currencies and providing an additional service (analytics or visibility into the local economy), you’ll empower the use of local currency, locally.

It comes to the situation that the community currency would be worth to people in the community and worthless to people outside the community. For example in Kenya, I think almost no one not in Kenya is interested in their ERC20 token. In other words, if CIC could be transferred outside Kenya (actually I don’t know), do people buy the token on the cryptocurrency exchange? I don’t think so. In short, the restriction of transferring token in specific region is just a precaution, but it matters in a long term when the community currency even become valuable for the people outside the community.

### My Opinion on Community Currencies

The difference between CICs in Kenya and the community currencies I want to build is that CICs is for poor community whose national currency is not stable. In my country, although the community is in the rural area, people living there can use national currency stably. Community currency in developed country seems redundant for the residents.

So what’s the use case for community currencies in developed country?

In my opinion, community currencies could be used for governance with market mechanism. I think the advantage of issuing community currencies in developed country is that it can be used to promote the actions to the **public good**. And the goal is to implement Quadratic Funding for the real world actions what non-profit organizations do in the current system. In that world, people use fiat currency for measuring preference of private goods, and use community currency for measuring preference of public good. In that way, we could get closer to the [effective altruism](https://80000hours.org/podcast/episodes/vitalik-buterin-new-ways-to-fund-public-goods/).

I think I attempt to apply internet governance in crypto world to the local community governance in the real world. Although it seems low tech discussion here, I still hope that the idea could be seen and discussed more.

