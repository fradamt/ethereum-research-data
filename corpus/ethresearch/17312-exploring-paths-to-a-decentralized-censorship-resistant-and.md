---
source: ethresearch
topic_id: 17312
title: Exploring paths to a decentralized, censorship-resistant, and non-predatory MEV Ecosystem
author: thogard785
date: "2023-11-06"
category: Proof-of-Stake > Economics
tags: [mev]
url: https://ethresear.ch/t/exploring-paths-to-a-decentralized-censorship-resistant-and-non-predatory-mev-ecosystem/17312
views: 4340
likes: 18
posts_count: 14
---

# Exploring paths to a decentralized, censorship-resistant, and non-predatory MEV Ecosystem

*By [Alex Watts](https://twitter.com/ThogardPvP)*

*Special thanks to [@Julian](/u/julian) for poking holes in multiple earlier versions, [@JustinDrake](/u/justindrake) and [@mikeneuder](/u/mikeneuder) for gaming this out with me in Paris, [Imagine/Snoopy](https://twitter.com/snoopy_mev) and [Doug Colkitt](https://twitter.com/0xdoug) for helping me iterate and for the sandwich example, the Flashbots team who pioneered the entire MEV concept and champion its decentralization, the [FastLane team](https://fastlane.finance) who have built and validated many of these theories over the last year on the Polygon PoS blockchain, and the Polygon team for giving us the opportunity . Thanks also to [@MaxResnick](/u/maxresnick) for his parallel work on ending the proposer monopoly.*

---

**Summary:**

The FastLane on Polygon (PFL) approach to MEV on the Polygon PoS blockchain has stopped predatory forms of MEV (IE “Sandwich Attacks”), stopped the centralizing effects of private orderflow, and removed the execution advantage of centralized (“Private”) relays relative to the decentralized, public mempool.  This is not accomplished without cost; unlike PBS, the PFL system is vulnerable to stake centralization from validators who operate their own vertically-integrated “sandwich” bots. This post analyzes the game theory behind how PFL works and explores how those same concepts could be combined with a new style of ePBS to reduce user predation, increase censorship-resistance, and stop the incentivization of centralized p2p.   To accomplish this would require a form of ePBS that has multiple proposers and a consensus-layer source of randomness. While those prerequisites may be distant or technologically infeasible, my hope is that this post will arm other researchers with new concepts to use in their arsenal when combatting centralization.

---

**PFL Background:**

FastLane Labs is an “On Chain MEV” company focused on using smart contract logic to decentralize the MEV supply chain.

The dominant MEV protocol on Polygon PoS is [FastLane on Polygon](https://fastlane.finance/) (PFL). It was deliberately designed without any sort of private relay to Validators. Although there are many benefits to this approach, such as relay decentralization and Validator security, the primary rationale behind the choice was three-fold:

1. We wanted to strongly disincentivize sandwich attacks against all of Polygon’s Users, including those who use the public mempool.
2. We wanted Validators to capture all revenue from private orderflow auctions (OFA).
3. We wanted MEV bots to be able to submit bundles via the public mempool. In the future, we hope that this will allow for Polygon validators to capture MEV without relying on any sort of PFL-managed infrastructure such as the FastLane sentries.

To elaborate on point 3, PFL currently maintains a relay between itself and Searchers, but does so for latency reasons.  The MEV auctions would still function with this relay turned off, but the bids would arrive slower.

For more on the architechture of the PFL system, please read the whitepaper [here](https://www.fastlane.finance/PFL_WHITE_PAPER_1_5.pdf).

---

**PFL’s Sandwich Disincentive:**

All transactions in all FastLane MEV bundles are broadcast back into the public memory pool. This allows any Searcher to include the transactions of other Searchers in their MEV bundles.

Consider the following structure of a sandwich attack:

[![](https://ethresear.ch/uploads/default/original/2X/a/a9f7851282b387f926648e0bb8844326a2aab45e.png)278×293 15.2 KB](https://ethresear.ch/uploads/default/a9f7851282b387f926648e0bb8844326a2aab45e)

Note that the first transaction from the Searcher - the frontrun - is similar to a “loss leader.” By itself, it will lose money. The Searcher only realizes profit when their second transaction is executed. The capacity for these transactions to execute in an “all or none” batch is called “bundle atomicity.”

PFL intentionally disrupts the atomicity of MEV bundles. All the transactions in an MEV bundle are broadcast to the public mempool, meaning that other Searchers can use them in the construction of their own MEV bundles. Consider a new party, SearcherB, who also wants to make money. What would they do?

[![](https://ethresear.ch/uploads/default/original/2X/1/1187dc568c15474971eaa6d970a313e08b6274c2.png)595×297 23.4 KB](https://ethresear.ch/uploads/default/1187dc568c15474971eaa6d970a313e08b6274c2)

SearcherB will combine SearcherA’s frontrun transaction and the User’s transaction with their own backrun transaction. This leads to three important conclusions:

1. SearcherB’s MEV bundle will always be more profitable than SearcherA’s, because SearcherA will always have higher costs than SearcherB due to the swap fees and gas fees of the frontrunning transaction.
2. Ergo, SearcherB will always be able to bid higher in auction and is expected to win the auction over SearcherA.
3. Ergo, because SearcherB’s MEV bundle includes a cost to SearcherA (the frontrunning transaction), and because SearcherA cannot expect to win the auction without direct and detectable Validator intervention, the rational action for SearcherA is to simply not attempt to sandwich the User in the first place.

This system has been live on Polygon PoS for roughly a year now, and we still have yet to observe a single sandwich attack succeeding via the FastLane relay or smart contract, although we’re certain that one will happen eventually. This observed result is particularly noteworthy due to the disproportionately cheaper cost of gas on Polygon; the minimum profit threshold for a sandwich attack to be actionable is significantly lower than on other chains, even relative to liquidity differences, meaning their frequency *should* be higher here.

Ethereum sandwiches on the left, Polygon sandwiches on the Right:

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9f6c839bb8b5fc4d195ed3f9815695a06e3ee61e_2_624x149.png)1600×383 180 KB](https://ethresear.ch/uploads/default/9f6c839bb8b5fc4d195ed3f9815695a06e3ee61e)

The data: https://dune.com/hildobby/sandwiches (credit to [@hildobby](https://twitter.com/hildobby_) for putting the dashboard together.)

For a more detailed analysis on the math of sandwich attacks and how disrupted bundle atomicity affects a Searcher’s PnL, please see [this spreadsheet](https://fastlane.finance/sandwiches.xlsx).

This mechanism of “*turn everything into a public auction by broadcasting everything to the mempool*” doesn’t just work to disincentivize sandwich attacks - it also realigns all “private” orderflow into an auction for the validator’s benefit.  The validator is therefore able to leverage their monopoly on the blockspace to capture all revenue that otherwise would be going back to users via OFAs, which no longer work without a private path to block inclusion (the exceptions to this are discussed below).

Notably, there are still sandwich attacks occuring on Polygon PoS, but their occurence appears to be limited to two sources:

1. Blocks from the three validators connected to a more extractive type of MEV relay that isn’t affiliated with FastLane. These validators make approximately 1-2% of all Polygon PoS blocks.
2. Liquidity pools on SushiSwap. We are still investigating why a disproportionate number of sandwich attacks (relative to liquidity) are occuring through SushiSwap, but the most likely explanation is that these pools on Sushi may be the only source of liquidity for the sandwiched token, meaning that a single attacker can buy the token and induce bundle atomicity without relying on a private MEV relay.

---

**Sandwicher Safety from Induced Bundle Atomicity via Inventory Monopoly:**

One of the most common responses to the PFL’s approach to MEV is that “sandwich attacks happened before flashbots.”  While this is true, it’s important to examine *how* these sandwich attacks happened and why, thanks to token-sniping MEV bots (E.G. JaredFromSubway), this isn’t a concern any longer. The irony couldn’t be thicker.

Take, for example, the following “frontrun” portion of a sandwich attack: [Ethereum Transaction Hash: 0x6073062555... | Etherscan](https://etherscan.io/tx/0x6073062555c134dbc7ad0a88d4c3bb45f8a5fe9b20df9c061f9ff2dd2edd8968)

Note that the “frontrun” transaction was through a “PGA” (Priority Gas Auction).  It was in the zero index of the block, also referred to as the top of the block (“ToB”). Note also the trade direction - the attacker *purchased* the obscure SFI token that the user *also* intends to purchase.  Finally, note that the user’s purchase was *not* the transaction following the frontrun; it was significantly further down in the block and at a significantly lower effective GasPrice.

The attacker’s backrun was the 14th transaction in the block:


      ![](https://ethresear.ch/uploads/default/original/3X/1/5/1508943b8cf27f62f34a67f2364601eb122c1639.png)

      [Ethereum (ETH) Blockchain Explorer](https://etherscan.io/tx/0xc90c3f98b65cb8e1bc2a6c8ec8b3fac76134fc86695ba8919dfd53e08b772ebd)



    ![](https://ethresear.ch/uploads/default/original/3X/4/1/412acb513cfbcd882b60edb4cbc87bfa6da7f5c7.jpeg)

###



Swap 18.97 SFI for 7.73 ETH on Uniswap V2 | Success | Dec-02-2020 09:33:10 PM (UTC)










*So why did the attacker spend so much money on gas?* In this example - along with most sandwich attacks that occured pre-Flashbots - the attacker was competing for the “Top of Block” tx slot so that they could have a monopoly on token inventory.

The PFL anti-sandwich mechanism and, to a lesser extent, the mempool’s native anti-sandwich mechanism, relies on searchers competing with each other to backrun the user.  But in order to perform the backrun, a searcher has to *sell the token that the user bought.* Competing searchers would therefore need to have access to liquidity for the token being sold.  For highly liquid tokens, this can be through flashloans or flashswaps from other pools… but for illiquid tokens found in only one liquidity pool, *only the searcher who purchased the token at the top of the block would be guaranteed the inventory needed to perform the backrun*.

These days, integrated token sniping / MEV bots such as JaredFromSubway will carry these illiquid tokens in their inventory.  A [relevant twitter thread](https://x.com/bertcmiller/status/1656392876438462464?s=20) from [@bertmiller](/u/bertmiller) does a better job of explaining it than I could.  The result is that for potential sandwich attackers using the mempool, bundle atomicity through an inventory monopoly is no longer as safe as it was three years ago, largely because their competitors will often hold these tokens in inventory just to gain a gas advantage for backruns.

And as we’ve spent the last year demonstrating on Polygon PoS, the best way to stop sandwich attacks is to make them too risky for the attacker.

---

**Issues with Implementating PFL on Ethereum:**

As a layer 1 from which other layers inherit security, it is critical that Ethereum is not subjected to the same centralization vector to which PFL is vulnerable: a vertically-integrated validator sandwich bot.  To block this, we can repurpose some of the work on “inclusion lists” from Mike and Vitalik.

The most basic version of a PFL-like system on Ethereum would target the following objective:

***For a block to be valid, each transaction in it must have been observed in the public memory pool by a threshold of attesters prior to the block deadline.***

This accomplishes three goals:

1. It adds significant risk to “sandwich attacks,” with the intention of stopping them outright.
2. It makes the decentralized mempool the optimal p2p path for users by removing any boost to execution quality (via blocking sandwiching or trade rebates**) that can be provided from centralized relays that have negotiated “off chain” contracts with trusted builders.
3. It removes the value of “private orderflow” for builders, who would still compete to optimize block value but who would now have a level playing field (IE they all have the same transaction set to build with).

*( ** In the interest of full disclosure, I should point out that trade rebates and other User-aligned execution outcomes could still be handled using account abstraction and bundling User Operations and Searcher Operations together into a single transaction. In fact, FastLane’s current project, [Atlas](https://github.com/FastLane-Labs/atlas), does exactly that by using smart contract logic to create a trustless “smart” environment for executing operations and intents without leaking value to relays, builders, proposers, or other adversarial actors in the MEV supply chain.)*

While these three goals are admirable, a problem arises:

*If a vertically-integrated proposer/builder/sandwicher knows that it will propose the next block, it can use its latency advantage to release a sandwich attack to the mempool at ‘last call,’ while simultaneously using this extra value to win the block auction.*

Although I question the likelihood of any large accumulator of stake (coinbase, lido, etc) actually attempting this, it’s still a valid concern that must be explicitly addressed due to the importance of Ethereum’s role as a base layer from which other execution layers inherit security.

---

**Exploring a Potential Implementation on Ethereum:**

Four prerequisites should be in place to nullify the stake centralization vector created by the latency advantage of a vertically-integrated Proposer/Builder/Sandwicher:

1. Multiple proposers.
2. A version of ePBS that requires that the proposer propose the most valuable block.
3. MEV Burn.
4. A source of randomness to determine which proposer proposes the canonical block.

Let’s start by establishing that the deadline for a transaction to be observed in the mempool to be valid must occur *before* the slot’s proposer will be aware that it is solely responsible for proposing the block.  This is to preserve the risk element mentioned above; once the potential proposer learns that it is the actual proposer, it must be too late for it to place a “valid” transaction in the mempool.

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/f45f25e2f05c00c309e17d1ba9b69d4acf47ca0d_2_690x107.png)image927×145 10.1 KB](https://ethresear.ch/uploads/default/f45f25e2f05c00c309e17d1ba9b69d4acf47ca0d)

A specific form of ePBS that requires the proposer select the most valuable block would be required to prevent the proposer from just proposing their own block each time. This is important because, as mentioned earlier, it is *always* more profitable to backrun a user + sandwicher than it is to just sandwich the user. Note that a vertically-integrated Proposer/Builder/Sandwicher could program their smart contract to not execute the frontrun if block.coinbase != tx.origin. By requiring that the proposer take the most profitable block, the proposer would no longer be able to assert that the block.coinbase is their intended one.

MEV burn would be required to prevent eigenlayer-enabled proposer/builder/sandwicher collusion that would trustlessly kickback the revenue from the proposer to the builder/sandwicher.  (Shoutout to the unaligned anons who accidentally justified MEV burn while trying to poke holes in PBS <3)

**One potential implementation:**

1. If >X% of proposers have a tx on their list then it must be included.  That would be for censorship resistance.
2. If <Y% of proposers don’t have the tx on their list then it can’t be included. That would be for sandwich protection and nullifying private orderflow.
3. Importantly, X should greatly exceed Y.
4. The randomly-selected proposer would submit an array of blocks, each of which is checked pursuant to steps 1 and 2.  This redues the likelihood of no block being approved.
5. The proposer also submits their own inclusion list. The backup block for the next block becomes all the txs on the proposer’s list that weren’t in the consensus block.

- Note that inclusion lists are quite complex, and that many of the concerns and solutions identified by @mikeneuder and @vitalik in their inclusion list design are relevant to any sort of hypothetical implementation discussed here.
- All the data needed to do perform these checks is already stored in the execution client. It would be straightforward to add an interface / API call to the EL client to perform these checks.

But the requirement for multiple proposers and access to a trustless source of randomness (return to PoW?) make this implementation an *extremely* heavy lift.  Perhaps even impossible.  If that is the case, then my hope is that some of the mechanisms and concepts described in this post may inspire other designs that similarly seek to reduce the incentivization of private orderflow, user predation, and centralized relays.

## Replies

**Julian** (2023-11-06):

Hi [@thogard785](/u/thogard785),

Thanks for writing this down! I wanted to reply to this post by going into the design philosophy first and unpacking a few arguments separately later.

The [design philosophy of PBS](https://barnabe.substack.com/p/pbs) recognises that validators may want to outsource some of their duties to third-parties. In order to have a credibly neutral validator set, we need to allow all validators, regardless of sophistication, to gain the same rewards. Therefore, we must facilitate validators invoking third-parties to do certain tasks, as long as they are not [“breaking the fence”](https://barnabe.substack.com/p/seeing-like-a-protocol).

Recognizing that it is impossible to known for sure whether some transactions constitute a sandwich, or if they were placed in that order for a different reason, it seems possible for validators to get away with sandwiching users. They are incentivised to do so because they can share in the MEV profits. Why would a single validator decide to opt into this system, instead of extracting more MEV? If it is individually-rational, should the protocol not try to ensure that all participants can get the same amount of MEV?

Moreover, a common vision for the Ethereum protocol is that it is as neutral as possible. Breaking all possibilities of atomicity in order to prevent sandwich attacks is maybe a too opinionated design choice and it requires a lot of extra features from the protocol. Do you think other methods, such as better AMM design or MEV rebating strategies / order flow auctions, can form a valid solution here?

Further Specific Questions:

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> We wanted Validators to capture all revenue from private orderflow auctions (OFA).

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> it also realigns all “private” orderflow into an auction for the validator’s benefit. The validator is therefore able to leverage their monopoly on the blockspace to capture all revenue that otherwise would be going back to users via OFAs

Why is it an explicit design goal to let validators capture all proceeds from order flow auctions? We see that order flow auctions lead to rent extraction by intermediaries, which is not desirable for users, however, order flow auctions can also be used by users as a tool to leverage their market power in certain situations, e.g. a user could get MEV rebates. Furthermore, order flow auctions could be used by designers of applications to capture MEV, like a few have proposed to do with LVR. Is it your design goal to capture all revenue from order flow auctions, or it is a goal to minimize rent extraction by intermediaries? In my view, if you break the functionalities of order flow auctions, you impose a dead weight loss, because certain people will not want to submit their transactions at all.

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> We wanted MEV bots to be able to submit bundles via the public mempool.

The post describes breaking atomicity of sandwich bundles. If a searcher could bypass the FastLane infrastructure, why would it not just submit their sandwich bundles to the public mempool?

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> SearcherB’s MEV bundle will always be more profitable than SearcherA’s, because SearcherA will always have higher costs than SearcherB due to the swap fees and gas fees of the frontrunning transaction.

Although I agree with your conclusion that submitting a sandwich bundle if it’s atomicity will be broken, I don’t agree with the reasoning. Let’s go through an example.

Searcher A submits a sandwich bundle whose atomicity is broken. Searcher B then bids to extract MEV from this bundle. If Searcher B does indeed extract value, this is a transfer of wealth from Searcher A to Searcher B. Based on this extraction only, Searcher A is therefore willing to bid exactly the same amount to prevent Searcher B from winning the auction as Searcher B is willing to bid to win the auction. If Searcher A wins the auction, Searcher A needs to pay up to the losses it would incur if Searcher B wins the auction, hence the extraction of Searcher A can be seen as a sunk cost. Searcher B would need to put in a transaction to extract the MEV, Searcher A does not need to put in a transaction to prevent Searcher B from extracting, hence therefore it seems that Searcher A could very well still win the auction.

Searcher A will be operating at a loss, hence in equilibrium Searcher A will not submit sandwich bundles if their atomicity will be broken.

---

**thogard785** (2023-11-07):

> They are incentivised to do so because they can share in the MEV profits. Why would a single validator decide to opt into this system, instead of extracting more MEV? If it is individually-rational, should the protocol not try to ensure that all participants can get the same amount of MEV?

Agreed. This is why we need to use ePBS.  The path explored in this post provides all of the features you describe, but with the added benefits of disincentivizing centralized relays, centralizing orderflow, and user predation.

> Moreover, a common vision for the Ethereum protocol is that it is as neutral as possible. Breaking all possibilities of atomicity in order to prevent sandwich attacks is maybe a too opinionated design choice and it requires a lot of extra features from the protocol. Do you think other methods, such as better AMM design or MEV rebating strategies / order flow auctions, can form a valid solution here?

With ePBS and the system that I describe, builders could still offer atomicity guarantees at the transaction level.

But to play devil’s advocate here, account abstraction bundling allows far greater degrees of atomicity provided via smart contract logic and encryption, rather than trusted off chain agreements with builders as seen today.  In other words, not only does a non-ePBS version of PFL not break atomicity - there was never any trustless atomicity to begin with.  The PFL system simply enforces decentralization.

However, even if it did break atomicity, it would still be worth considering due to how this trusted atomicity is almost exclusively being used to empower priveleged actors to take value from non-priveleged actors. But that devil’s advocate position is an opinionated stance and might be best left to L2s, which is what PFL was designed for.

> Why is it an explicit design goal to let validators capture all proceeds from order flow auctions? We see that order flow auctions lead to rent extraction by intermediaries, which is not desirable for users, however, order flow auctions can also be used by users as a tool to leverage their market power in certain situations, e.g. a user could get MEV rebates. Furthermore, order flow auctions could be used by designers of applications to capture MEV, like a few have proposed to do with LVR. Is it your design goal to capture all revenue from order flow auctions, or it is a goal to minimize rent extraction by intermediaries? In my view, if you break the functionalities of order flow auctions, you impose a dead weight loss, because certain people will not want to submit their transactions at all.

At FastLane, we believe that a single company should not represent multiple, adversarial parties in the MEV Supply Chain due to the inherent conflict of interest that this creates. (Fastlane therefore cannot make a validator solution for ethereum, since we’re working on a DApp MEV solution).

Regardless, it is a fact that the value lost to sandwiching users of decentralized p2p services is orders of magnitude larger than the value retained by users of centralized, private OFA services.  This may be an opinionated stance, but I believe that justifying the theft of hundreds of millions of dollars from users of decentralized p2p so that we can refund two million dollars to users of centralized p2p is not something that is not aligned with Ethereum’s vision.

But it’s a moot point - as mentioned earlier, account abstraction bundling provides all of the same benefits of OFAs but with trustless smart contract logic governing the interaction.  I therefore reject the premise that we have to choose between “protecting all users” and “refunding some users.”

> The post describes breaking atomicity of sandwich bundles. If a searcher could bypass the FastLane infrastructure, why would it not just submit their sandwich bundles to the public mempool?

Because other searchers would see the bundle in the mempool.  I do not think the PFL infrastructure layout is relevant here, as the network topology for Polygon is different (particularly re: sentry nodes, which make it trivially easy to discern whether or not a tx originated at a validator node).

> Although I agree with your conclusion that submitting a sandwich bundle if it’s atomicity will be broken, I don’t agree with the reasoning. Let’s go through an example.
> Searcher A submits a sandwich bundle whose atomicity is broken. Searcher B then bids to extract MEV from this bundle. If Searcher B does indeed extract value, this is a transfer of wealth from Searcher A to Searcher B. Based on this extraction only, Searcher A is therefore willing to bid exactly the same amount to prevent Searcher B from winning the auction as Searcher B is willing to bid to win the auction. If Searcher A wins the auction, Searcher A needs to pay up to the losses it would incur if Searcher B wins the auction, hence the extraction of Searcher A can be seen as a sunk cost. Searcher B would need to put in a transaction to extract the MEV, Searcher A does not need to put in a transaction to prevent Searcher B from extracting, hence therefore it seems that Searcher A could very well still win the auction.
> Searcher A will be operating at a loss, hence in equilibrium Searcher A will not submit sandwich bundles if their atomicity will be broken.

Yes - I think this is a longer and more thorough version of what I was proposing but that fails to take into account the third parties extracting value - the liquidity pool and the validator.  The swap fee and the gas fee add inefficiency into the system that breaks the equation in your example, but I think the overall concept that you cover is still valid and we still reach the same equilibrium in which SearcherA will not submit the sandwich bundle.

---

**mikeneuder** (2023-11-07):

hey Alex! interesting post. there is a lot to unpack here, but i think i will focus on a single situation.

in the single proposer design, you point out the main issue

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> If a vertically-integrated proposer/builder/sandwicher knows that it will propose the next block, it can use its latency advantage to release a sandwich attack to the mempool at ‘last call,’ while simultaneously using this extra value to win the block auction.

i would go even further and say there are even more options for the HFT builder trying to execute sandwiches

1. have a better view of the network topology and publish the bundle in such a way that it is the “last look” and no copycat bundles will have time to become public, or
2. have an off chain agreement with large block proposers to serve them more valuable blocks so long as they don’t unbundle.

i think you address that with the “multiple proposers” point, which certainly makes it much more difficult. in particular, i think it makes my #1 above less potents. the HFT builder would have a really hard time delivering a bundle to a bunch of potential proposers without getting unbundled. however, i think #2 is still possible. the easiest solution would probably be the following strategy.

i. HFT builders have off chain agreements with big validators to have exclusive access to the block production rights for slots where the validators are candidate proposers.

ii. during a candidate slot, the HFT builders send their candidate bundles to their contracted validators and enough other validators to ensure their bundle will be seen as valid without sufficient time to be unbundled.

iii. if the contracted validators are the proposer, the bundle is included and the HFT builder is happy. otherwise, the bundle is probably not included (because the actual proposer may well have not seen the bundle in time), and the HFT builder is sad but not unbundled.

does that make sense? still thinking through it more on my end, but am trying to find the simplest counter-example of a strategy that wouldn’t have the nice guarantees you describe.

i really appreciate the post and the discussion! i think you and Max are touching on something interesting with the multiple proposers design space.

---

**thogard785** (2023-11-07):

> does that make sense? still thinking through it more on my end, but am trying to find the simplest counter-example of a strategy that wouldn’t have the nice guarantees you describe.

That does make sense.  The first thing that jumps to my mind is that for this scenario to play out such that it’s riskless for the attacking builder, the builder market would need to be fully centralized and the proposer market would need to be fully colluding. One builder would have to monopolize the p2p layer between *all* of the proposers… but if that were the case, that builder would have no reason to do an off chain agreement with the validators anyway.  In other words, it wouldn’t need any sort of guarantee from proposers because it already has a building monopoly.  More importantly, other builders would profit from disrupting the builder’s monopoly.

So while I do think that this situation is worth considering, I don’t believe it would lead to any additional centralization concerns for the proposer market - the centralization would be limited to the builder market, which is already quite centralized.

In fact, I would argue that this proposal would help *decentralize* the builder market.  The rationale is that currently, builders compete over private orderflow and market making / stat arb.  Should a builder “win” that competition, it would be very difficult for other builders to compete in the private orderflow and market making arenas.  But with this proposal, a centralized builder would now also be earning sandwich revenue… and there is now a high amount of profit that a new builder could capture from the central builder that wouldn’t require a sophisticated market making operation or access to private orderflow… They just need to sandwich the sandwiching builder.  Also, the private orderflow vector would be nullified anyway, so that’s kind of a moot point. But I think the general idea here is that builder competition is greatly incentivized with this proposal relative to the current status quo, and the builder centralization concerns you bring up are more strongly disincentivized with this proposal than in the current environment.

I do believe that you touch on a key issue here - proposer collusion in response to a builder monopoly. Builders are competitive with each other - one builder breaking up the monopoly of another would be profitable for the disruptor - whereas proposers aren’t necessarily. This is one of the reasons that MEV burn is so critical to the proposed PFL-like strategy; it prevents kickbacks and revenue sharing between colluding and vertically-integrated proposer/builder/sandwichers.  And due to designs like Eigen Layer, I think that proposer collusion (when rational) should always be assumed… which does complicate things.

Thankfully, ePBS (with enforced highest-bid block) and MEV burn would reduce the surface for collusion, as a single non-colluding builder would be incentivized to disrupt the collusion to the detriment of all the colluders. I do think it’s ironic that we’d be preventing proposer centralization (collusion might be a better word) by inducing builder competition, given that the latter market is currently far more centralized than the former.

On a related note, at FastLane we’ve had a lot of success with randomized auction durations. We’ve found that by making the auction duration uncertain, we remove many of the negative externalities and latency races created by apriori knowledge of when ‘last call’ occurs. Something like that might also be useful here, but the mechanism design to do so in a trustless manner would be quite tricky. At PFL we just have the node generate a random duration, which works fine in our case since we already consider the validator a trusted party.  For Ethereum, that would obviously not work as that assumption is invalid.  Perhaps an Ethereum solution would rhyme with PoW.

---

**thogard785** (2023-11-08):

[@mikeneuder](/u/mikeneuder) I wanted to follow up to address your hypothetical with some specific diagrams to make sure we’re on the same page.

It’s my understanding that the attack vector would look something like this:

[![image](https://ethresear.ch/uploads/default/optimized/2X/0/0bb7e1e078334a4d4a8f0d3d9a7692796911b3f8_2_676x500.png)image1426×1054 44.1 KB](https://ethresear.ch/uploads/default/0bb7e1e078334a4d4a8f0d3d9a7692796911b3f8)

- The colluding proposers would each need to attest that they saw the transactions in the bundle.
- The colluding proposers would each need to not propagate the transaction.
- The colluding proposers would each need to receive the block from the sandwich builder and identify it as such, and pretend that they haven’t seen any higher value blocks.
- The colluding proposers would need to be greater than the N% threshold specified in the original post.

But there’s another important consideration here, too: it would be profit maximizing for one of the colluding nodes to *betray* the colluders.  More importantly, the identity of this “betraying” node would be difficult to discern, as the betrayal would be through releasing the transaction (hard to tag) rather than unbundling a full block (could send slightly different blocks to each proposer).

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/3fe0a552246959a7d5843f7ed8ce95a93d447d66_2_671x500.png)image1506×1122 48.1 KB](https://ethresear.ch/uploads/default/3fe0a552246959a7d5843f7ed8ce95a93d447d66)

The profit maximizing action for the colluding proposers would therefore be to betray each other… especially since the identity of the betrayer could not be ascertained and therefore no “slashing” via Eigen Layer would be possible.

So if N% = 33% and we have 24 proposers, then more than 8 proposers would need to be colluding for profit maximization, but all of them would have to trust that none of the others were acting for individual profit maximization. I think that the inherent contradiction is fundamentally strong enough to keep the chain safe, and I wonder if there would be other, better ways to make money if one were able to get such a cartel together.

Importantly, if the identity of the betrayer *was* something that could be identified and then slashed via eigen layer, then we could use the exact same tool to identify and slash would-be sandwichers.

I therefore think that the only way that such a scenario could reasonably play out is with a builder monopoly as discussed in my previous post, which would then fail for the reasons mentioned.

---

**pixelcircuits** (2023-11-10):

The biggest hole I see with this is that transactions can’t just be “attested” to. They would have to be efficiently proven that their full data was seen. This is something more akin to the data availability problem which is a hard order for current transaction throughput, let alone encoding a whole mempool.

I’m assuming that by “attesting to a tx” you really just mean signing over the hash of the tx, otherwise you’d see a pretty big performance hit when validating signatures. This means proposers can “attest” to a tx without having to be given the full tx.

To be fair, proposers wouldn’t want to sign over anything (they could be signing something slashable for them), but a small zkproof could reveal just enough of the tx to convince a proposer that it is a tx rather than a block.

Please correct me if I’m missing something.

---

**thogard785** (2023-11-16):

> I’m assuming that by “attesting to a tx” you really just mean signing over the hash of the tx, otherwise you’d see a pretty big performance hit when validating signatures. This means proposers can “attest” to a tx without having to be given the full tx.

So the goal here is for the attesters to approve or reject each block in the array of blocks submitted by the randomly selected proposer.  The rejection reason should also include why there’s a rejection (censorship resistance or private orderflow).  There wouldn’t be a need to attest to individual transactions.

---

**pixelcircuits** (2023-11-17):

The problem still stands though. Just because a proposer attested to a whole block of transactions doesn’t mean they actually saw them and know what they are.

With your suggested changes, relayers would just be required to contact n% of the attesting committee on top of the current proposer to still allow block builders to create MEV extracting blocks. At a surface level, this looks like it might make it less likely for an MEV block to get through, but unfortunately more than 96% (last time I checked) of blocks proposed came from a block builder through a relayer. This means that more than 96% of validators are already talking to relayers and are ready to sell their attestations. And you can sell an attestation without needing the transactions to be revealed.

I guess this could work as a good MEV smoothing strategy for validators assuming the relayer is also trusted to spread around who they collect attestations from evenly. However, I see an even worse scenario playing out with relayers biasing a select group of validators to collect all the MEV and price out other stakers (a centralization vector).

---

**thogard785** (2023-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/pixelcircuits/48/13336_2.png) pixelcircuits:

> Just because a proposer attested to a whole block of transactions doesn’t mean they actually saw them and know what they are.

Just to clarify - you’re saying the issue would arise if >N% of validators are willing to lie?

I have a hard time thinking that validators would risk their social reputation by doing that. It would hurt their ability to aggregate stake.

But I’ll think about it some more. You make a good point - it’d be better if there was a better way around it than just assuming the social layer will keep the majority from lying.

---

**pixelcircuits** (2023-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> Just to clarify - you’re saying the issue would arise if >N% of validators are willing to lie?

Yes and it would be hard to concretely prove that they truly are misbehaving.

You post is very interesting though and could be the start in the right direction

---

**thogard785** (2023-11-19):

> Yes and it would be hard to concretely prove that they truly are misbehaving

Got it. Thank you. This also adds some context to me for Mike’s concern - the cartel-inducing relay wouldn’t need to show the txs, just the hashes, which would break the whole “a single honest & profit-maximizing member in the cartel would be incentivized to anonymously break the cartel.”

Currently, isn’t this is also a concern for the timing / block deadline for attestation? But I think the solutions might not be able to share much.

I wonder theres a solution to this might actually be better than the original solution with respect to decentralization and neutering the value of a vertically-integrated builder-proposer-searcher, particularly of the MM / stat arb type.

My thinking is this:

1. Per the original post, it’s extremely risky to sandwich attackers to have their frontrunning txs leak.
2. Per original post, the randomly-selected proposer submits an array of blocks, from highest value to lowest value, and the attesters approve or reject each block in the array based on the anti-private orderflow and the anti-censorship rules discussed above.
3. Because of #2, it can be assumed that Builders for block N+2 will see all the txs of the rejected block candidates for block N+1. We can build that auto-propagation into the clients easily (similar to what happens to txs during reorgs).
4. Because of #1 and #3, sandwich attackers would not submit the attacks unless they know that the actual proposer is part of the cartel.  This is because they would not want to risk having their frontrunning tx end up getting backrun by another MEV bot in block N+2.

From these, it follows that the easiest solution would be to have *all* proposer candidates submit an array of blocks *prior* to the random selection of the actual proposer.  This would require 100% cartel participation for the sandwich attackers to be completely safe.

It would also allow for easier detection of “lying” proposers, as we could compare the contents of their own proposed blocks against the txs that they said they’d seen when attesting to other proposers’ blocks.  It wouldn’t be perfect though - we obviously can’t assume that all txs can fit in all blocks - but these sandwich txs are, in general, quite valuable for builders, so their omission from their own blocks but attestation in other blocks would be very damming from a social perspective.

I’m going to think some more on this subject. I wonder if there’s a way to have a more thorough tx list piggyback off of the inclusion list design… but I’m hesitant to do that without compression of some kind - the full tx pool isn’t something that should be placed in the consensus layer.

EDIT: I think this actually would be even cleaner than I thought - ePBS requires the proposers to propose the most valuable blocks first.  We can assume that each proposer auto-attests to the blocks in their own array. I think we could use that to speed things up, as long as there’s a failover in place.

---

**pixelcircuits** (2023-11-20):

You’re still incorrectly assuming the data will be known by the attestors. This is false. Even in the current PBS model with relayers, the block proposer never sees or executes the full block being signed. They just assume it is correct and let the ralyer or builder gossip the full signed block around the network for them.

I think the same would happen to the attestors in your model. A relayer would just tell them what to blindly sign in exchange for some compensation. The relayer can even put up insurance via a smart contract so that if the attestor gets slashed for blindly signing something bad, they can withdraw from the insurance contract and recover from the loss.

I’m also not sure how you could prevent the builder from filling the proposed block array with a bunch of dummy blocks with dummy transactions that they made up plus the one block they really want to get through which they plan on hiding until enough attestors are bribed.

---

**thogard785** (2023-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/pixelcircuits/48/13336_2.png) pixelcircuits:

> You’re still incorrectly assuming the data will be known by the attestors. This is false. Even in the current PBS model with relayers, the block proposer never sees or executes the full block being signed. They just assume it is correct and let the ralyer or builder gossip the full signed block around the network for them.

Not an assumption - that would be an intentional design choice to bring about the desired result.

Making sure that everyone can see everything is definitely what we’re going for ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)   illuminate the dark forest and all that.

