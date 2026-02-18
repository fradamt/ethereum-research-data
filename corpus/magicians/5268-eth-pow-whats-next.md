---
source: magicians
topic_id: 5268
title: "ETH PoW : Whats next ?:)"
author: kladkogex
date: "2021-02-01"
category: Magicians > Primordial Soup
tags: [pow]
url: https://ethereum-magicians.org/t/eth-pow-whats-next/5268
views: 3282
likes: 21
posts_count: 37
---

# ETH PoW : Whats next ?:)

As ETH 2.0 is pretty much guaranteed to move from PoW to PoS some time in 2021/22, the question is what is going to happen to the original PoW chain?

It is clear that when the PoW chain is about to die, some people will remove the difficulty bomb and continue mining.   The question is only how many people will do it.

It is a  pretty unique situation, and it is hard to even call it a fork, since the original thing will be killed.  It is something that never happened in the history of blockchain before.

Since the PoW chain is pretty much guaranteed to survive in some shape or form (it takes one miner to keep it alive), it makes sense to discuss how it will operate.

Here are some questions to discuss about the future of the PoW chain:

1. How should it be governed? Should it be some kind of a DAO?
2. Should it switch to ProgPoW or use the current PoW algorithm?
3. Should it keep all the current accounts or zeroize some of them (like the ETH1 premine)?
4. How should it pay for development?
5. What should the monetary policy be?

## Replies

**esaulpaugh** (2021-02-02):

turn it into a test net with faucets everywhere

---

**thor314** (2021-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> How should it be governed? Should it be some kind of a DAO?

I imagine it will be governed by those that remain, of whom we may not be a representative sample, so we’re purely speculating, but given that Miners suffer the most from the PoS transition, and naive newcomers to the space suffer most from confusion (and thereby scams) around Eth2 vs Eth1, I lean toward a complete abandonment of the original Eth1 to minimize that confusion

---

**esaulpaugh** (2021-02-02):

just leave a difficulty bomb on it with a short fuse and refer to the it as “the dead chain” and to the proof-of-stake chain as “Ethereum” (i.e. not Eth2)

---

**kladkogex** (2021-02-03):

Actually for ETH investors, keeping ETH1 may be the best thing economically.

If say, market cap of ETH2 is $150B, and, independently,  market cap of ETH1 is $50B,  doesnt it make sense to keep both?

The sum of two may be much more than the original,

---

**Galena1227** (2021-02-04):

1. I’m not sure. You could try stealing the Ravencoin model of having different groups electing a representative using different methods. i.e: use block extradata to elects a miner rep, use transaction extradata to elect a user representative. Devs are represented by being the ones who choose what gets implemented.
2. Switch to progpow, a PoW chain should aim for decentralization to play towards our strengths.
3. Zeroize the staking smart contract and Ether premine
4. Impose a x% transaction fee and x% block fee. Allow the miners and user representatives to distribute the collected fees. There should be an even split in budgetary power between the two groups. Allow the representatives to allocate funding to the different EIPs. In the short-term, create a development fund equal to the amount of Ethereum zeroed from the premine and staking contracts and allow n% to be allocated per month on development.
5. The monetary policy should aim for a constant annual inflation rate of 2% (I’m open to ideas about how much the inflation rate should be. We want something that is comparable to other major currencies since we want to be a currency.)

How do we achieve 2% annual inflation? We make the network faster. Perform research on how quickly a large block can be propagated. Have the target time per block decrease at a rate of 2% Since state growth is going to increase we need to reward node operators since they will need to upgrade their hardware just like miners. I lean towards having a %share of transaction fees get distributed to node operators since that should grow at the same rate as state complexity. I’d also like to see block rewards get set to 5 in order to attract new miners since there will be an immediate dip in profitability since we’ll be the other coin.

I’m not sure how we should do all this, but that’s for smarter people than me.

---

**esaulpaugh** (2021-02-04):

No, it does not. That would destroy the network effects that result from everyone being on the same chain. Hence why every old chain has been abandoned except Ethereum Classic.

If facebook splits in two it becomes less of a network and more of a joke.

Eth1 and Eth2 could in no way be described as independent. Even if Eth1 changed its name to Bitcoin Platinum

---

**kladkogex** (2021-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> If facebook splits in two it becomes less of a network and more of a joke.

Well - a contrargument will be that the change is too big.

Satoshi Nakamoto arguably likes PoW.

ETH2 team likes PoS.

Elon Musk likes PoW, but does not get smart contracts.

There are people who like PoW more than PoS and also like smartcontracts. ![:smiling_imp:](https://ethereum-magicians.org/images/emoji/twitter/smiling_imp.png?v=12)

I have met a number of people in the  ETH community, some of them PhDs in CS, who hold a subjective point of view that PoW is more secure than PoS.

---

**esaulpaugh** (2021-02-08):

The switch to PoS is too big for miners, you mean? Not to go all Tron, but I think Ethereum is and should be about the users. The bitcoin and ethereum whitepapers are both about providing for users. There doesn’t seem to be a shortage of staker/validators so I don’t see a problem.

As for security, I don’t really see how PoW is more efficient at providing security, especially in light of the constant threat of a new ASIC design appearing and causing rapid centralization. Oh, yeah, and it seems to cost 10X as much, so it had better provide at least 10X the security compared to PoS, per dollar spent.

---

**Galena1227** (2021-02-09):

I’m going to breakdown your security concerns and address them since a lot of them already have existing solutions.

> As for security, I don’t really see how PoW is more efficient at providing security, especially in light of the constant threat of a new ASIC design appearing and causing rapid centralization.

We already have ProgPoW waiting in the wings. If we are going to be gutting the difficulty bomb, then we might as well switch algorithms. The reason why ProgPoW reduces the threat of ASICs is that any ProgPoW ASIC will at most be 1.2x times more effective than a GPU. This raises the risk over GPUs since they are now at risk of being invalidated by any future algorithm swap and hold no additional resale value. It becomes a much riskier proposition at that point.

> so it had better provide at least 10X the security compared to PoS, per dollar spent.

I’d argue that it does accomplish this. It is much easier to buy 101% of the currently staked Eth than it is to purchase enough GPUs and ASICs to double the current hashrate. There are only so many computer chips being produced at a time, and existing hardware is unlikely to be sold so long as it is profitable to mine with them, which means that a malicious attacker would need to perform a logistics miracle. In contrast, a malicious party in Proof of Stake simply funnels Eth from exchanges to anonymous wallets over time and pays for cloud hosting of their nodes. By all metrics, the current Ethereum difficulty should be 12k terahash based on profitability, but it is still only a quarter of that because of how slow GPU production is.

---

**esaulpaugh** (2021-02-09):

> currently staked Eth

is irrelevant. I never argued that PoS could replace PoW tomorrow. It’s probably more than a year away even by the most optimistic estimates.

> 101%

It’s not 101% – it’s more like 1001%, because as far as I can tell, proof-of-work produces something like 10x the inflation of proof-of-stake. So if someone wants to secretly buy up $100 billion worth of ETH (a financial miracle) and run hundreds of thousands or millions of validators, then at that point they bought the network fair and square and frankly deserve to have control of it.

And you can’t assume that GPUs will continue to be competitive with ASICs, especially since Ethash replacement will likely not happen even if (or especially if) ASICs are 100% of hashpower.

---

**Galena1227** (2021-02-10):

> then at that point they bought the network fair and square and frankly deserve to have control of it.

That goes against the entire logos of the Ethereum network. It is the world computer, not “Some rich guy’s computer.” You seem to be laboring under the misunderstanding that a malicious attacker needs to purchase 51% of the total supply. This is false. They don’t need to control the network forever, just long enough to do their business, destroy trust in Ethereum, and go on their merry way.

That is why a PoW network would switch to ProgPoW. If we’re going to be forking the network and arguing that we are the more secure and decentralized chain, then we better be getting rid of ASICs.

---

**esaulpaugh** (2021-02-10):

Then proof-of-work also goes against the entire logos of Ethereum because it requires less than an infinite amount of resources for an entity to take over the network. It’s abhorrent that you would suggest proof-of-work as a mechanism for security when it’s not literally perfect.

But in the meantime I’d rather get 10X the security for the same price by throwing miners overboard (preferably in the most vulgar manner available) like was the plan from the beginning. You clearly agree that proof-of-work costs vastly more per unit of security, but you believe that miners are entitled to unending alimony payments even though their position was always only temporary, and that’s something I can never support.

My point is that if ETH holders want to allow a presumably hostile entity to buy up two-thirds of the stake without rallying to out-stake them, then that’s essentially a conscious choice more than it is a fait accompli, because to keep the attack secret would be, as you say, a logistics miracle.

---

**Galena1227** (2021-02-11):

> to keep the attack secret would be, as you say, a logistics miracle.

It isn’t though, there is no way to determine which wallet belongs to who when Eth leaves an exchange. A number Eth transactions leave exchange wallets headed to unrelated wallets every day, all you have to do is combine them into a number of unrelated 32 Eth wallet, then you’re in business.

---

**esaulpaugh** (2021-02-11):

300,000+ uncorrelated private keys, tens of billions of dollars, hundreds of millions of dollars in fees alone, easy peasy. A rapid (more than) tripling of the total stake… and no one will find out. Not a logistics miracle in any sense. Okay, buddy. Have fun with that.

---

**kladkogex** (2021-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> It’s abhorrent that you would suggest proof-of-work as a mechanism for security when it’s not literally perfect.

Proof of Work was the original mechanism suggested by Satoshi Nakamoto.

It worked incredibly well, and Bitcoin has no plans to  move to PoS.

We all hope PoS can long term provide security and decentralization similar to PoW, but there are many unsolved problems.

The largest problem is tendency to centralization.  Currently four parties can stop ETH2 from finalizing. Four.

PoS is still an early stage startup, I hope it succeeds. Would I put my life time savings today on a Layer 1 PoS chain? No. May be 5 years from now.

---

**esaulpaugh** (2021-02-13):

Bitcoin is lame, and is it not the case that three mining pools collectively control 60% of Ethereum hash power? If I’m not mistaken, three is fewer than four.

Not to mention that a 51% attack under PoW is far worse than mere non-finalization.

---

**Galena1227** (2021-02-16):

It’s worth clarifying that it isn’t just 4 parties, it’s 4( or fewer) individuals with the power to prevent Eth 2.0 from functioning. Mining pools are loose coalitions of freelance workers who are capable of switching representatives at any time. In the event of an attack, the pools orchestrating it will see their hashrate rapidly evaporating as miners switch to pools that aren’t actively harming their profits.

---

**esaulpaugh** (2021-02-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/g/8797f3/48.png) Galena1227:

> 4( or fewer) individuals with the power to prevent Eth 2.0 from functioning

Ummm, for how many minutes? These 4 individuals who collectively stake more than 965,000 ether, worth 1.7 billion dollars, are willing to be slashed and leaked into oblivion just for fun? They deserve however many minutes of pleasure they’ll get. They will certainly have paid for it in full.

And mining pools aren’t freelance workers like freelance journalists actively deciding what to do on an hourly basis. That’s not even close to an accurate portrayal. And again, 51% attack is far more effective than some lame-ass 1.7 billion-dollar non-finalization prank.

---

**kladkogex** (2021-02-18):

It is not the point. The point is that the government needs to control 4 entities to control the chain.

They can issue a court order to four entities to  freeze it. You cant freeze PoW like that.

My point is that there have to be some rules against concentrating too much stake in a single organization. One way to do it is to use modifications to GPL

---

**esaulpaugh** (2021-02-19):

Please link the addresses of these four parties.


*(16 more replies not shown)*
