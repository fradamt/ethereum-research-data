---
source: ethresearch
topic_id: 9060
title: MEV Auctions Will Kill Ethereum
author: pmcgoohan
date: "2021-03-31"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/mev-auctions-will-kill-ethereum/9060
views: 23094
likes: 67
posts_count: 57
---

# MEV Auctions Will Kill Ethereum

TL;DR

*MEV Auctions enshrine the right of the richest to extract money from the poorest at a protocol level, and when people realize that, it will kill the network.*

Here is an explanation of MEV Auctions in case you haven’t come across the idea before:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/karl/48/9_2.png)
    [MEV Auction: Auctioning transaction ordering rights as a solution to Miner Extractable Value](https://ethresear.ch/t/mev-auction-auctioning-transaction-ordering-rights-as-a-solution-to-miner-extractable-value/6788) [Economics](/c/economics/16)



> Special thanks to Vitalik for much of this, Phil Daian as well (& his amazing research on MEV), Barry Whitehat for also coming up with this idea, and Ben Jones for the rest!
> Blockchain miners (also known as validators, block producers, or aggregators) are nominally rewarded for their services by some combination of block rewards and transaction fees. However, being a block producer tasked with producing a particular block gives you a lot of power within the span of that block, letting you arbit…

OK, so now for the long version…

Have a look at this spreadsheet:



      [drive.google.com](https://drive.google.com/file/d/1xYpZ1MI6ZH3u4lgrgsiHwkEUW2Bh9byA/view?usp=sharing)



      https://drive.google.com/file/d/1xYpZ1MI6ZH3u4lgrgsiHwkEUW2Bh9byA/view?usp=sharing

###

Google Drive file.










It’s a simple model of a Uniswap pool. It shows the relative cost/benefit of bidding in an auction for average users vs whales. It shows that whales can extract value from everyone else continuously under an MEV auction system and that it is impossible to protect yourself from it.

Rather than fixing the problem of MEV, auctions worsen it and then attempt to whitewash the fact with promises of virtuous spending.

It’s like trying to fix the problem of organized crime by giving mafia bosses jobs in the civil service and letting them run the country.

Consider what may happen if we go down this path…

Optimism will be released to mainnet shortly. Users will enjoy massive speed improvement and cost reduction. Yay! Assuming the centralized sequencers are honest and do not attempt to run MEV auctions, users will also enjoy slippage free transactions on Defi. Triple yay! They are going to notice how much better off they are than when MEV was a problem, and they’ll love it.

Then the distributed MEV auction sequencer comes out and it’s like a bomb going off…

The slippage returns, but not just that, it is far worse than it was before. Users start to hear something about how their orders are now being exploited not just by a few naughty miners, but *by design* in the new protocol.

The press picks up on it. The right to rip you off is now being sold to the most wealthy in the Ethereum network. Furthermore, the spoils are going to the developers and advocates- the very people that engineered the crime! They’re not going to see this as a virtuous funding of the commons. It’s going to look like corruption. Who do you think is Gamestop and who is Citadel in this narrative?

This will create a crisis that the developers will be forced to react to. If MEV Auctions are the only plan, then at this point failure is the only option. Either Optimism returns to centralized sequencers for good and Ethereum becomes Binance Coin, or it sticks with MEV Auctions and the user base enters terminal decline.

The Flashboys 2.0 MEV analysis paper and MEV-Inspect are brilliant. So valuable. MEV-Geth not so much. We need to drop the idea of MEV ever being virtuous and drop MEV auctions as a solution.

There are *much* better ways of doing this stuff.

UPDATES:

Where Ethereum is headed with [MEV left unfixed](https://www.coindesk.com/ethereum-mev-frontrunning-solutions).

In response to Phil Daian’s post “Mev… wat do?”, I have published this Medium article [“Mev… do this.”](https://pmcgoohan.medium.com/mev-do-this-beb2754bca63)

## Replies

**kladkogex** (2021-04-01):

Basically rollup operator is a perfect front runner …

---

**pmcgoohan** (2021-04-01):

The point is, the backrunning of order flow I described is just one example of a new kind of MEV that you can’t do at the moment but will be able to with MEVA (MEV Auctions). Let me explain…

Right now there is no point entering a bidding war to backrun a small transaction, it’s just too costly in gas.

This is well known, and it it’s why people keep their transactions sizes low on Uniswap. It’s a decent protection against the bots and it works ok. Many small time users with small orders sizes don’t even realize they are being protected by it.

But with MEVA it won’t protect you at all, because the one-off cost to the auction winner has already been paid. In fact, they *must* exploit every order to recoup their auction costs. A whole raft of new exploits will appear like this targeting orders that used to be too small to bother with.

That isn’t a small thing. It means that *every single order in the network will be exploited continuously and without exception by the auction winner in ways that are impossible now*.

As well as that, all of the traditional frontrunning, backrunning, sandwich trading strategies will be open to the auction winner with absolutely zero risk.

Look how bad MEV extraction is at the moment. You won’t even believe how bad it’s going to be under MEVA. It will make Ethereum hands down the most exploitable marketplace in the world, second literally to none. By design.

Really, I think there’s some serious groupthink going on here which is why I stepped in.

There’s really no point throwing your users under the bus to save the integrity of the network if you end up without any users.

The Layer 2 sequencing represents a chance (possibly the last) to fix a problem that has haunted Ethereum since genesis- transaction reordering and censorship. I’m afraid it absolutely is a systemic problem hence the title.

There are solutions to this. MEVA isn’t it.

---

**pmcgoohan** (2021-04-01):

Also, the auction winner will punish transactions that they can’t profit from by censoring/delaying them.

So if you set your Uniswap slippage % tightly to protect yourself, they’ll send you a message by withholding it indefinitely.

Or perhaps our benevolent centralized master sequencer at JP Morgan will look kindly on us? ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=9)

---

**kladkogex** (2021-04-01):

I see … interesting …

because you do not know  MEV in advance, you will need to participate in the auction even if the ultimate MEV is small …

---

**thegostep** (2021-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> The Flashboys 2.0 MEV analysis paper and MEV-Inspect are brilliant. So valuable. MEV-Geth not so much. We need to drop the idea of MEV ever being virtuous and drop MEV auctions as a solution.
>
>
> There are much better ways of doing this stuff.

FWIW the current version of mev-geth is not meant to be a long term solution. It is meant to solve for the real danger that naughty miners will partner with Citadel (or others) to do the extraction themselves, and Citadel suddenly gets to decide which transactions get to be included in a block. If you start with the assumption that all available MEV will be extracted, I think mev-geth can be seen as a lesser evil.

The Flashbots org is interested in funding any research that reduces harmful MEV / negative externalities of MEV. Would love to hear more about your ideas around better ways of approaching the problem at hand: [GitHub - flashbots/mev-research: Project management for MEV Research](https://github.com/flashbots/mev-research)

---

**pmcgoohan** (2021-04-01):

I appreciate the response. I can see from the way you have described it that the mev-geth project is coming from the right place.

![](https://ethresear.ch/user_avatar/ethresear.ch/thegostep/48/7751_2.png) thegostep:

> If you start with the assumption that all available MEV will be extracted, I think mev-geth can be seen as a lesser evil

That’s what I have a problem with- I’m not ready for that. I looked to Ethereum to be the solution to these kinds of problems, and I still do.

I understand that Ethereum had other priorities than transaction ordering and censorship when it launched, but I don’t relish watching the same shortcomings being repeated with eth2 and rollups.

As an aside, when you know that a system has certain limitations, I think you have a responsibility to code around them.

Uniswap could have been written to wait a block before performing a simultaneous constant product calculation on the first call of the next block.

That one change would have saved hundreds of millions in MEV being lost to it’s users.

That their code allows this level of MEV extraction should be considered an exploit in my opinion.

In fact how I ended up here was that I was looking at coding a simultaneous version of Uniswap when I thought…is there any point if L2 is coming out soon.

So then I looked at how Optimism was going to handle transaction order and all I could find on it was MEV Auctions selling to the highest bidder.

Not what I wanted to hear.

Thank you for the research links. I’ll definitely be in touch over the next few weeks as I gather my ideas together.

---

**thegostep** (2021-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> That’s what I have a problem with- I’m not ready for that. I looked to Ethereum to be the solution to these kinds of problems, and I still do.
>
>
> I understand that Ethereum had other priorities than transaction ordering and censorship when it launched, but I don’t relish watching the same shortcomings being repeated with eth2 and rollups.

Yeah I that’s fair, I know there are several teams looking at better composability models. I recommend checking out MEV-roast # 11 with sunny as the roast master. I think he did a great job highlighting the design space here and I know he shares your perspective that MEV auctions are not good enough alone. [GitHub - flashbots/pm: Everything there is to know about Flashbots](https://github.com/flashbots/pm#mev-roast-recordings)

I leave others with more familiarity with AMMs comment on your solution for Uniswap. I previously worked on a commit reveal solution to prevent front running but the block n+1 restrictions made the UX difficult for people to adopt. https://libsubmarine.org/

I think it would be interesting to think about what a world where uniswap routes their orders through FlashBots would look like. I think FlashBots can work for sandwich protection just as well as for sandwich execution given its credible neutrality.

---

**kladkogex** (2021-04-02):

At SKALE we are using 2/3-N-threshold encryption to provably remove MEV.

A transaction is TE-encrypted on submission. It is then committed to the chain, decrypted by a committee and then processed.

---

**mtefagh** (2021-04-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> But with MEVA it won’t protect you at all, because the one-off cost to the auction winner has already been paid. In fact, they must exploit every order to recoup their auction costs. A whole raft of new exploits will appear like this targeting orders that used to be too small to bother with.

I was recently reviewing the price impact literature from the economy for another [reason](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/367?u=mtefagh), and there is a ton of articles about different market irregularities. Unfortunately, constant-function market makers meet the requirements for almost all of these irregularities. For example with a 30 seconds search, you find [this](https://doi.org/10.1137/110822098) article among many others, and first of all, we don’t have any transient price impacts in our models. Moreover, we also don’t have temporary price impacts. And finally, none of our functions are convex, which is a real surprise for me as I am used to usually pick a random economy question to design convex optimization problems for my final exams.

I am not saying that constant-function market makers are inherently a bad idea. I am just trying to tell that we have at least a century of how different price impact models can safe-guard against front-running to at least ameliorate the undesired effects. And what I see here is that the wonderful innovations of the Ethereum community are just reinventing the wheel little by little.

In summary, I totally disagree with the sentence, “we also observe front-running in traditional finance, so it is inevitable!” We might be able to cut down MEV into a negligible fraction before considering how we are going to deal with that unavoidable remaining part.

---

**pmcgoohan** (2021-04-02):

Ah so you worked on submarine sends. Nice one- it’s a great idea! It was the solution I was reaching for when I first looked at this stuff and I was very cheered when I found you’d done it. But yes, I get that people like to do things in one block, apparently whatever the cost.

On that point, do you or any of your geth guys know… how easy would it be to add a msg.IsFinalTxn global boolean to the EVM?

If you could tell that you are the final transaction for the executing contract address you could trigger a simultaneous MEV-free calculation for all transactions in the block without needing an n+1.

You could then fix all this stuff definitively at app level.

I will definitely check out the roast- thanks for the link.

---

**pmcgoohan** (2021-04-05):

Really, the more I think about this… once MEVA is released all Binance Coin has to do is make an announcement that they will not extract MEV from their users and people will move over to them in droves.

They can run an explosive ad campaign using MEV-Inspect data to show what a better deal they are for their users- and they’ll be right! What a massive own goal for Ethereum.

Plus what do you think the SEC is going to make of our legitimizing frontrunning? They’ve just about calmed down about ETH being a security. Why poke that particular hornets nest by building violations of their laws into the protocol.

Decentralization takes a lot of work- it’s expensive. As soon as a decentralized solution becomes less fair than a centralized competitor *as well as* more expensive, it’s all over.

Thanks for the links. Is the general argument that the constant product is inferior to say an order book because price impacts are by definition permanent with constant product because each trade changes the balance of the pool permanently?

I actually really like the ideas in Uniswap v3 in terms of concentrated liquidity and range trades- a sort of order book of constant products. It seems genuinely innovative. But again, they’ve done nothing to address MEV and the transaction rate will be far higher as people move their ranges around.

I think we have to make a distinction between white-hat arbing and black-hat arbing. White-hat would be where a price is moved back to fair value by arbers. That’s market efficiency. Black-hat would be sandwiching your victim’s order between trades such that you extract money from them due to an unfixed exploit in the network and completely irrespective of fair value. A lot of the literature won’t be considering this situation (yet) because it is so extreme and simply hasn’t existed risk-free until Ethereum- which does not reflect well on Ethereum.

---

**mtefagh** (2021-04-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> Thanks for the links. Is the general argument that the constant product is inferior to say an order book because price impacts are by definition permanent with constant product because each trade changes the balance of the pool permanently?

I’m not suggesting removing permanent price impacts but instead adding the other types of price impacts as well. And I am not an expert in this field, but I am trying to just copy what is being used in the economy. However, I may have a very limited intuition about why it might help.

For a simple example, if you can reorder the transactions in an AMM, you can just break down an adversary large order into smaller ones and interlace them with opposite matching orders to pay almost zero slippage. This slicing trick is mutual and also exists in traditional portfolio execution. The part that you can reorder transactions is obviously an instance of MEV. However, the fact that even by this reordering you can bring down the slippage to zero because you don’t pay any kind of temprory or transient price impact is also exclusive to AMM right now.

If we had some kind of those price impacts, at least the margin of profit for this example of MEV would have been reduced. That is all my point! Yes, front-running exists in traditional finance as well but it seems that here it is way more profitable. We might want to cut down the margin of profit by these simple measures before doing something more extraordinary like MEVA.

---

**karl** (2021-04-05):

Interesting post! Just want to quickly disambiguate two concepts:

- MEV Auctions #1 – Auction off the right to sequence transactions.

I’ll call this "Sequencer Auction"s for this response. This is the topic of the post you linked to.

MEV Auctions #2 – MEV-Geth where traders can express more complex transaction inclusion preferences than a simple gas price auction (GPA).

- I’ll call this MEV-Geth (just for this post). This is an awesome project by flashbots and is being used by L1 PoW miners.

Sequencer Auctions are simply the auction mechanism for selecting who is the next sequencer. In fact there is a bit of a ‘sequencer auction’ in Ethereum L1 – it’s the PoW which determines the next block proposer. The insight with sequencer auctions is that instead of selecting block proposers by burning energy, sequencers can instead *pay for the privilege* of selecting contents of the next block.

Sequencer Auctions **can and should** be coupled with things like submarine sends/time-lock encryption for reducing total possible extractable MEV. However, for any remaining MEV (like slow market arbitrage), we can at least give the profits back to *users* instead of distributing them to random sequencers (aka miners).

As for MEV-Geth, MEV-Geth is software that any individual sequencer (or block producer) would run to extract a block’s MEV in a standard way that allows traders to be involved & express their preferences.

---

So one way to think about this is that there are 2 auctions that occur which are fundamental to the blockchain designs we’ve seen so far:

1. the auction for being the next block producer (sequencer auction), and
2. the auction for what gets included in the next block (GPA/MEV-Geth).

The term MEV Auctions have unfortunately been used to talk about both of these distinct functions. I guess that’s the downside of using super general terms like MEV Auction! Whoops!

---

**kladkogex** (2021-04-06):

MEV evolution naturally leads to block proposer and MEV extractor becoming the same entity. Small ETH2 block proposers will  not have computational resources for MEV extraction.  Ultimately the largest staking pool/MEV extractor will be the most profitable.

This by the way will burn huge amounts of electricity since MEV extractors will run neural networks on graphic cards. The funny thing is  that PoS may become as eco-unfriendly as PoW.

The largest MEV extractor will naturally be the most profitable one.

Then, for the largest MEV extractor it does not make any sense to run an auction, since MEV extraction value will be more than the auction profit (this is because the largest extractor is the smartest and has the most computational resources)

Even if auctions are introduced, the block proposer/MEV extractor can trivially fake them and censor out undesired parties as people above mentioned.

This brings us back to threshold encryption on a blockchain as a way better MEV elimination mechanism.

---

**pmcgoohan** (2021-04-07):

Thanks Karl, that is very helpful to point out. I have conflated the two projects in my discussions and I will distinguish between them from now on where relevant.

![](https://ethresear.ch/user_avatar/ethresear.ch/karl/48/9_2.png) karl:

> Sequencer Auctions can and should be coupled with things like submarine sends/time-lock encryption for reducing total possible extractable MEV. However, for any remaining MEV (like slow market arbitrage), we can at least give the profits back to users instead of distributing them to random sequencers (aka miners).

I am extremely pleased to hear that we are attempting to reduce MEV in the sequencer and to only use auctions for the remainder. Are we doing this with the block producers too? Our aim must be to make MEV so low that it’s not worth bidding for in an auction.

![](https://ethresear.ch/user_avatar/ethresear.ch/karl/48/9_2.png) karl:

> The insight with sequencer auctions is that instead of selecting block proposers by burning energy, sequencers can instead pay for the privilege of selecting contents of the next block.

Here are a few ideas to chew over:

Our problems with MEV are because Ethereum is not fully decentralized.

Block structure is fully decentralized. Blocks are proposed and validated by consensus across tens of thousands of nodes.

Block content is created by a centralized authority (miner/validator).

In short, block content is not trustless.

There is a historical reason for this. The Ethereum devs had their hands full in the run up to genesis. Creating the world’s first and best blockchain smart contract network was a massive deal and rightly took all of their stretched resources to complete.

As a result the consensus mechanism had to be largely borrowed from Bitcoin. In Bitcoin the transaction order within a block is irrelevant. Transaction censorship isn’t really a problem either, just an inconvenience. As the MEV analysis shows, this is very much not the case with smart contracts. It was understandable at the time but it’s 6 years later now and we’ve seen the harm it causes.

Addressing the hidden centralization in block content creation is where I feel our energies should be directed. I would love to see all these sharp minds getting stuck into *this* problem.

---

**kladkogex** (2021-04-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> Our problems with MEV are because Ethereum is not fully decentralized.

Words of wisdom!!

> Blocks are proposed and validated by consensus across tens of thousands of nodes.

Ooops … why do you think there are thousands of nodes?  For PoW, pools control proposals (I think there are roughly 10-20 of them)

---

**pmcgoohan** (2021-04-08):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> For PoW, pools control proposals (I think there are roughly 10-20 of them)

The node count is >10000. I get that the proposer count is far less.

But my point is whatever deficiencies the structural layer of the consensus may or may not have, it’s a lot stronger than the content layer which is… non-existent.

This is a technical problem. We need developers to fix this problem, not the market. There’s a market for stolen credit card details. Perhaps it’s wonderfully efficient and a great example of the free interplay of supply and demand. But it never should have had the opportunity to exist because, like MEV, it is the product of an exploit that never should have happened.

Just saw [this](https://www.coindesk.com/miners-front-running-service-theft?amp=1) (it isn’t me btw)

---

**pmcgoohan** (2021-04-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/mtefagh/48/3417_2.png) mtefagh:

> in an AMM, you can just break down an adversary large order into smaller ones and interlace them

It’s a good idea, but you can do it more simply and efficiently than that with a simultaneous constant product calculation. I’ll have more to say on application layer MEV fixes like this soon (which will include a model for this). For now I am concentrating on a content layer fix.

I have an admission to make to Flashbots [@thegostep](/u/thegostep). I now understand that as a short term fix, MEV-Geth reduces gas prices and transaction bloat etc, and I agree that right now on mainnet it is net positive and a force for good. My apologies for lumping it in with eth2/rollups MEV auctions.

My fears lie in organized MEV auctions/extraction continuing into eth2 and rollups.

What I feel we must avoid is fostering the same culture of entitlement with validators/sequencers that we currently have with miners.

On Monday I will post my ideas for fixing MEV in the content layer. It is sadly too late to apply them to mainnet because it is so against miner’s interests to adopt that it would likely create a fork and destabilize the network.

But we get a clean slate with validators/sequencers…

We need to start putting out the idea that as a validator/sequencer you will *not* be entitled to (or even be able to) exploit users for MEV the way that miners currently can, and that this is for the long term good of the network. Because it is!

Traditional finance is never going to move over to Ethereum in a serious way while it is as exploitable as it is, and if they do, it will be for the wrong reasons- because they want to exploit it themselves!

Anyway more from me on Monday, in what will be a far more upbeat thread.

---

**mtefagh** (2021-04-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> Traditional finance is never going to move over to Ethereum in a serious way while it is as exploitable as it is, and if they do, it will be for the wrong reasons- because they want to exploit it themselves!

I am not suggesting copying every notion of traditional finance. I am talking about the specific notion of slippage and slippage is not designed so that people can exploit other people. In this case, why we don’t have this in DeFi is not because we don’t want to exploit our users. Instead, it is because we want to provide a better UX for greedy users! I talked about just one instance in my previous comment. Another one is that in Uniswap v3.0, if all those greedy users concentrate all their liquidity on a very short interval, a whale can just buy all the reserve of one token in a trading pair with zero slippage whatsoever!!!

---

**justsomelurker** (2021-04-17):

I’ve enjoyed reading the conversation here over the past few weeks and i agree with the threat that built-in extractable value poses. I’m surprised no one is talking about chainlink’s proposal to abstract sequencing into an oracle layer. Seems like a pretty novel approach to me, but i am justsomelurker, and now i will return to my shadows ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

pg 48 [a5511b75-559d-441c-8142-2b5226a9e332.pdf](https://docs.google.com/viewerng/viewer?url=https://files.elfsight.com/storage/d7d04be0-5073-4228-9315-5d8f63b05bb3/a5511b75-559d-441c-8142-2b5226a9e332.pdf)


*(36 more replies not shown)*
