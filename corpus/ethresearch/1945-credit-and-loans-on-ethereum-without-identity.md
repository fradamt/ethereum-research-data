---
source: ethresearch
topic_id: 1945
title: Credit and loans on Ethereum without identity?
author: SRALee
date: "2018-05-08"
category: Economics
tags: []
url: https://ethresear.ch/t/credit-and-loans-on-ethereum-without-identity/1945
views: 4952
likes: 28
posts_count: 28
---

# Credit and loans on Ethereum without identity?

I’ve been thinking a lot about how it would be possible to issue credit or loans of crypto assets without needing a solution to the “on chain identity problem” and can’t think of any non-collateral based proposals. I’m sure there is probably some clever game-theoretic models for issuing loans and attributing credit, but each of these concepts requires some kind of information about the other party to asses risk of defaults. Is there some writings on the topic of loans/credit by Vitalik or leading experts in ETH I should read up on? What is the current consensus of the community about credit/loans smart contracts?

## Replies

**SamuelTroper** (2018-05-10):

I’d dig into [microcredit](https://en.wikipedia.org/wiki/Microcredit), which deals with a lot of the same difficulties as extending credit using ETH.

---

**SRALee** (2018-05-13):

Good read thanks. I actually think microcredits could be useful in the blockchain space since loans and micropayments could be easily made in a programmatic fashion. Although, it still seems difficult to pull off since it’s so easy to sybil attack. Humans are finite, wallet addresses are practically speaking infinite. For example, assume you create a smart contract that will microloan out .01 ETH with no questions asked/no collateral and requests you pay back .011 ETH by time X. If you pay it back by time X you can receive the next loan of .02 ETH. But sybil attacked with 100,000 ETH wallets to take .01 ETH each with no intention to repay back is pretty easy in the blockchain space whereas 100,000 people amassing to take advantage of microloans is a hard coordination problem and unlikely to happen in the real world.

EDIT: I guess there’s a way around this by only allowing Z amount of loans outstanding at once. So for example, only 10 loans of .01 ETH can be outstanding at a time for a period Y and if any of those 10 loans are not paid back by period Y then they are defaulted and wiped out so the contract knows what to work with. If too many people are stealing/sybil attacking the contract then it will only wipe out Z x .01 ETH per Y period rather than get cleaned out at the beginning.

---

**griggah** (2018-06-10):

I have a traditional New York “Wall Street” background and I’ve thought about this a lot too. You can create secured debt, but not unsecured debt without a notion of identity.

Unsecured debt requires you to assess credit risk based on a future income stream, which simply cannot be established without a solid and, more importantly, costly-to-fake source of identity. If you look at the peer-to-peer lending market in China, you’ll see a clear example of what happens when you violate this principle. There’s extremely rampant fraud in the Chinese unsecured personal lending market. One of these companies went public as a U.S. traded ADR recently, and unsurprisingly it is a complete disaster precisely because of this problem.

I have heard a lot of benefits to decentralizing personal unsecured lending, but they all strike me as very silly. An example is wealthy immigrants that move to the U.S. but don’t yet have a valid source of credit. To be clear, that’s a fairly small market and it’s fairly unclear why decentralization and the incremental credit risks associated with it justify serving such a tiny market. The other market is credit for criminals, which is the larger and more attractive market for most crypto applications, but not something I think anyone should spend their life building towards for obvious moral reasons.

Secured credit is quite possible and eventually this is a valid use of decentralization. As it stands now, the applications I’ve seen exist to lever your ethereum bets, which is one of the most silly things I’ve observed in the space (with sufficient leverage on volatile assets, you can actually ensure your own ruin per the Kelly principle; betting sufficiently more than what is Kelly optimal actually can ensure loss over a sufficient long period of time). Eventually there will be reasonable applications, such as using a tokenized version of gold as collateral to take out a loan to buy a house. This is reasonable, useful and a valid use of decentralization.

One other way of saying this is that if someone can create a decentralized, yet stable notion of identity, then I do think this is quite valuable. In theory, there should only be relatively few winners here. The folks that win there will extract a lot of value, since it is the choke-point to many valuable financial applications of decentralization. Not sure how to do this or if its possible. That said, it’s the game smart folks should try to win and is certainly a technological pre-requisite to unsecured peer-to-peer lending or unsecured lending of any kind done in a decentralized manner.

---

**MaxC** (2018-06-11):

Ineresting thoughts, are credit rating agenciesdecentralised? Perhaps you could have reputable companies stand in on the block-chain

---

**adiasg** (2018-06-13):

If there were to be a credit system that does not depend on identity of a peer, and a peer were to gain credit from such a system, then the disincentive to not pay back the original must be larger than the benefit from applying for new credit.

Applying to this credit system would have 3 basic costs:

- Cost of Generating an Address: The peer must have generated it’s address to recieve the credit. It is impractical to make the amount of credit given out so low that it is lesser than the cost of generating a new address.
- Cost of Initiating the Smart Contract: The peer must pay for gas for running the smart contract. It is clear the we cannot make the amount of credit given out lesser than the gas to be paid to get it; the peer would be losing money.
- Cost of Future Credit: If the cheater was not to orchestrate a sybil attack, then there is a cost of risking future credit to the same address. This would be easy to do, since the only identification used would be the peer’s address itself.

Maybe if there was some way to make (Cost 1 + Cost 2) greater than the credit given out, then such a credit system would be possible.

---

**travism** (2018-06-18):

I just played around with dharma protocol doing an integration for a client. It allows for secured loans on Ethereum w/o identity… Worked well, is in production, and available for use now…

---

**sandeep_belure** (2018-06-23):

The problem with using the dharma protocol is that the credit underwriting and debt collection happens off-chain…

---

**sandeep_belure** (2018-06-23):

More like decentralizing tether usd peg auditing … we are entering the relm of decentralized stable coins

---

**cpfiffer** (2018-06-23):

I wonder if there’s something like Hyperledger’s [Indy](https://www.hyperledger.org/projects/hyperledger-indy) that addresses those two costs you highlighted. I don’t know that standard address will ever be so costly that lending becomes viable. There just isn’t any cost.

If people are tied in some way to their addresses in a way that impacts their ability to perform other economic activities you might see a lot more value in lending. I think it’s maybe an ecosystem problem but I wouldn’t know how to address that.

---

**SRALee** (2018-06-24):

Yes, this is an avenue to go down on as well. Basically, because identity is difficult to do on-chain in a trustless manner, if you make creating new public keys sufficiently expensive, then you could do some kind of lending based on the cost, C, of public keys. The issue I have with this is that the cost, C, is essentially the collateral. We’ve just moved away from using the actual identity/credit as collateral and replaced it with the cost of generating keys (which for most ledgers is negligible). But it’s an interesting idea nonetheless…

---

**SRALee** (2018-06-24):

Yep, this is exactly what I’m working on, a purely decentralized central bank/stable currency system. That’s why I made this thread for ideas haha

---

**sandeep_belure** (2018-06-24):

Hi … I have been researching his space heavily too (loans and stable coins).

.

1. “Anonymous  no identity” Lack of collateral/ uncollateralized loans cannot be decentralized. Because trust cannot be delegated or decentralized.
.
2. Lending against ETH deposit as collateral. . One could try “equity collars” inplace of stable placed pegged token : That is what I am trying currently and I am looking for cofounders and investors.

---

**sandeep_belure** (2018-06-24):

One major concern would be an Ethereum chain hardfork - the way bitcoin forked into bitcoin and bitcoin cash

---

**cpfiffer** (2018-06-24):

My suspicion is that making addresses costly to *create* is not the best solution here.

The best solution is a reformation of how everyone interacts with one another on-chain – it needs to be costly (socially and economically) to default, not costly to gain an address. Perhaps some way of tying your actually identity with your address.

---

**SRALee** (2018-07-06):

Can you give an example here? Not seeing any feasible way that it could be made costly to interact on-chain that would relate to loans.

---

**cpfiffer** (2018-07-07):

That’s pretty much my point here. It’s pretty much impossible to make it interact on-chain as it relates to loans the way the current system functions. The root issue is that addresses are cheap and they are essentially valueless from an intrinsic perspective, so loans on-chain are highly difficult to do.

The only way (in my opinion) lending becomes viable is after some platform like Ethereum is sufficiently mature to support serious economic ties between an address and the holder of the address. Lenders might be a little more advantaged in a world where credit risk is partially determined on the number of *network links* an address has, or ties an address has to other economic transactions, activity, or economic holdings. [Hyperledger’s Indy](https://github.com/hyperledger/indy-node/blob/stable/getting-started.md#what-indy-is-and-why-it-matters) could probably explain it better than I could, but here’s my best attempt at an example.

Not terribly helpful, unfortunately, but I really don’t know that there’s an effective way to think about lending on-chain at the moment.

Consider two people that an on-chain lending service might lend to.

Alice has an address with features that establish her identity. Perhaps it’s been signed by a university to indicate that she’s a graduate or by her employer to indicate that she is employed there, or maybe even her salary is distributed to her from that institution. Her address is not costless; there are real-world economic links to this address that communicate her ability to repay a loan.

Bob is a goon with many addresses, none of which have anything that either tie them to Bob or to anything else. Bob is an infinite credit risk. Any loan to him is bound to fail because he has zero incentive to repay a loan. He can just discard the address with a balance and move on.

---

**SRALee** (2018-07-07):

I think this just further proves that a classical “loan” that we are accustomed to is literally just debt collateralized by identity.

---

**sandeep_belure** (2018-07-08):

I unfortunately arrived at the same conclusion…

Another way traditional loans are collateralized are through the borrower providing illiquid assets (such as land ownership) as collateral - hard to implement this onchain using asset backed tokens without getting off-chain lawyers involved during the debt collection process/default.

Incase of using a stable coin like Tether as collateral - we are back to using identity as a partial form of collateral - unless you are over-collateralizing … in which case the borrower might not be keen on borrowing the loan.

---

**DennisPeterson** (2018-07-12):

Loans collateralized by non-fungible tokens might be interesting. Say I’ve got a rare cryptokitty I want to keep, but I’m in need of short-term cash.

Maybe you put up your collateral on a market along with the loan request, and human lenders decide which deals look secure.

---

**cpfiffer** (2018-07-13):

I think that fully collateralized, or more likely over-collateralized, loans are probably the only way to go at current. You see this kind of thing in traditional financial markets where people might have limitations on what they can sell (an executive selling his company’s stock, for example) so they throw a lien on their holdings to borrow cash. It’s pretty common.

Here it’s entirely reasonable to lock the collateral up in a contract and transfer it to the lender upon default. I’m quite fond of users just posting the collateral they want to offer up and leaving the onus of credit risk analysis on the lender.


*(7 more replies not shown)*
