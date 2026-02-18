---
source: ethresearch
topic_id: 4698
title: Concept - etherless - a pow based barrierless EVM
author: pr0toshi
date: "2018-12-28"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/concept-etherless-a-pow-based-barrierless-evm/4698
views: 3545
likes: 10
posts_count: 28
---

# Concept - etherless - a pow based barrierless EVM

etherless - a pow based barrierless EVM

The purpose of this proposal would be to make a decentralised p2p evm network where the barrier to entry will be 0. We do this through removing the need for ether in ethereum. By having the gas fee be a personal transaction hash the network will be able to allow for an open decentralised evm and the ability to perform non monetary operation on information without needing to worry about holding cryptocurrency. This will not affect ethereum but will be somewhat like a fork but remain dependent on the eth project for core functionality. Think of it more for offloading non financial projects like supply chain.

How it works

The underlying implementation of the evm will remain for interoperability and compatibility purposes. The underlying ether will be replaced by a new concensus and fee model. All transactions will have gas costs for operations just as they do now but will also include a pow field with the nonce needed to produce a hash of the transaction that will be more than the gas used if it is not the transaction will just fail. The pow needed will be roughly the network cost to perform the transaction and perhaps an overhead. Like if the transaction were to be a 21k gas transaction taking .01s and the node group would be 5000 then the pow should take more than 50s to perform the pow for. This may be adjusted. Gas will also have a price but will be based off the pow provided. If the pow is 0000 and only 000 was needed for the min pow then the transaction will have a higher priority based on the pow that it has and how much higher it is than was needed. This will allow for prioritization during high use and let the user put more pow behind it to get it confirmed.

Concensus

Concensus will involve validator nodes that will sign using a threshold signature on proposed blocks made from within the group. The group will be allocated a slot by putting up a pow token as collateral for their blocks. 5000 slots will make up this group.

The pow token

For users who are unable to perform the pow this will be able to be delegated to other nodes through a burned pow token. Nodes who have resources to spare might want to use these to produce tokens by special transactions where they create a mint transaction that will look like a transaction to transfer pow token from the coinbase to themselves and by submitting a pow that would match the requirement for the gas cost it will be replacing the resource cost can be moved. This will be the rough process.

Assume 1 token will replace 100k gas

Pow miner submits 10 pow hashs for a pow that meets 200k per for 10 tokens from the coinbase to themselves this will be valid if they meet the minimum threshold. The miner then will be able to transfer this to mobile user bob for .05 USD for 1 token. The transaction will cost 21k and they will get back .79 pow token.

Note

The mined tokens are not as efficient as doing the pow but they are reimbursed while pow is not.

This is just a late night thought i had none of it is final just getting others thoughts.

## Replies

**fahree** (2018-12-28):

What is the economic incentive to participate?

---

**pr0toshi** (2018-12-29):

Was thinking that the sub group that makes the block whoever submits it will get .3x of the gas tokens in fees. Rest get destroyed. This is pretty open im kind of just playing with the concept none of its final. If you remove the need for paying for a transaction in a fee i feel it opens up the network to applications like on chain messaging or supply chain management. People are far more happy to pay indirectly and it would remove the need to buy eth to use an open network but remain resilient.

---

**MaverickChow** (2018-12-29):

I believe the best course of action (or participation) from everyone by now is not to introduce a totally new concept, idea, or approach, but to follow along the official Ethereum development road map and suggest improvements and refinements on them.

The barrier to entry will be 0 with central bank-issued stablecoins.

---

**pr0toshi** (2018-12-29):

Yeah that wont happen. And until it does getting crypto will always be the hard part for interaction with any blockchain and smart contract. Eth will never not run off gas backd by ether which would be highly useful for adoption if you didn’t need to hold it. Also you could have tokens run without having to hold eth.

---

**MaverickChow** (2018-12-29):

Recently an article mentioned the Brazilian government will issue its own local currency-backed stablecoin. Before this, I believe the Singaporean government also stated it is planning the same. So, that will happen.

Might as well think of a much better solution, i.e. have tokens running without having to hold the tokens, or have dapps running without having to hold any token. Now that would be killer dapp.

---

**pr0toshi** (2018-12-29):

Yeah they need to do it and for supply it would need to be then worrying about custody of the funds to pay for the fee. That’s not a eth problem almost no project needs a token. And now this doesn’t either.

---

**jtremback** (2019-01-01):

Ok, let me get this straight- a node would need either the PoW token, or a GPU to submit a transaction? If that’s the case, it doesn’t seem that this lowers any barriers.

---

**pr0toshi** (2019-01-01):

No not gpu. The pow will just work as a fee to allow regular transactions to reasonably go through during attacks. It would also let transactions be made without any token or eth needed. Like imagine you live in mid Africa. You can get a node up no problem but you have no bank access and so no way to buy eth to use any dapp with this you do just enough to have pow to get in. The token would be there for offloading the pow so you could use the network on a phone without having to do the pow locally and allow for the node incentivisation. The token could be removed its just useful for allowing high gas app use on a phone and node rewards.

---

**jtremback** (2019-01-01):

Why not participate in a mining pool to earn Ether?

---

**pr0toshi** (2019-01-01):

Because in the ideal case you would be able to do it from a phone. It’s about allowing as many to join as possible with as little barrier as possible. Honestly I’m hoping to potentially not even need an address. Without the need for a fee you could have transactions that run and you could have the input be completely anonymous. This would allow for leaks to be published to a dapp with no analysis possible of fund source. Or you have it be part of a game where you buy with gold on the dapp and you do the transaction without having to know about or have bought any crypto currency you just have your address and keys. Yeah you could mine but not only do you need far more power to cost. You need to set it all up.

---

**pr0toshi** (2019-01-01):

Hopefully the pow would be low enough that a phone would work. But if it gets attacked then you can just use more pow to up the gas price on your transaction to compensate.

---

**jtremback** (2019-01-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/pr0toshi/48/4504_2.png) pr0toshi:

> Hopefully the pow would be low enough that a phone would work. But if it gets attacked then you can just use more pow to up the gas price on your transaction to compensate.

I’m just trying to understand what it is about this scheme that makes require much less PoW than regular mining, to the point that generating PoW on a phone is useful.

Scenario 1: Generate PoW and send to a pool, getting ether. Spend ether on gas.

Scenario 2: Generate PoW and use instead of gas.

What fundamental difference is there which means that scenario 2 requires a lot less PoW? I’m not trying to shoot down your idea, just wondering what the underlying principle is. Some rough math might be helpful to prove out the concept.

---

**pr0toshi** (2019-01-02):

Well right now mining is done using a gpu optimized pow. Further to mine a block the hash rate right now is 175gh. A high power gpu can do 30mh. You would get 0.0031 eth for 24h of mining. Current transaction would be 0.00006 that’s 30m per transaction if you use gpu. For comparison nano does the pow in under 1s. It’s not just about the ability its the efficiency. Right now the mining is constant and pow competing with the whole network pow to get your cut that are running all the time. With this it only competes with other transactions and you don’t need to set up a miner. The pow would be probably pretty low from this.

---

**projectoblio** (2019-01-02):

Nice. I was thinking of using Monero’s consensus algorithm for something like this. I was going to use it to combat spam on a centralized site.

---

**kladkogex** (2019-01-02):

We are implementing a similar thing in Skale network - accepting PoW in lieu of gas …

---

**pr0toshi** (2019-01-02):

Do you have somewhere that I could look into it. Id honestly like it to just be an independent network kinda like an altnet like rinkeby and fully compatible with eth standards. There would be no ico the pow token would be only for pow offloading rather than monetization.

---

**HarryR** (2019-01-02):

I really like the idea of proof-of-work as a mechanism to prevent peer-to-peer spam, the typical demonstrative use case for this is an extension to e-mail/SMTP (or other P2P messaging systems) where the receiver sets the difficulty threshold for successful message delivery - the amount of time you spent writing the e-mail on your personal computer is disposable income that proves you invested an initial time and energy to get in touch with a person that deserves to read whatever it is you have to say.

e.g. if you burned five minutes of your time, I want to hear what you have to say, as we only have limited time on this earth and PoW is the best way we have, at the moment, of proving that in a way which transcends boundaries. Does arbitrary computation work the same way?

If the cost of sending V1@ġRā e-mails goes from 1000/sec for $75/month to 1/min at the same price, we’ve mostly eliminated spam, put the recipient in-charge of their preferences, and created an implicit cost/benefit relationship, rite? And while it may cost a few extra deciamps to initially get in-touch, once the receiver knows who we are the cost can return to the minimal. You can (kinda) model this using Erlang’s theorem with two additional parameters - maximum acceptable cost per message and recipient cost threshold on a per-sender basis.

But, how does this apply to blockchain, what are the caveats, and how does consensus work without centralised miners?

> Right now the mining is constant and pow competing with the whole network pow to get your cut that are running all the time. With this it only competes with other transactions and you don’t need to set up a miner. The pow would be probably pretty low from this.

Accepting PoW in lieu of gas seems to be the way forward, but what are the caveats? How can individual proof of work be abused in a way which provides much less security than the collective probabilistic proof of work threshold of a consensus…

Random project I made, where you are rewarded with arbitrary tokens in return for proving work of some kind:

https://github.com/HarryR/PoWtoken

This follows HashCash, but the idea is that you benchmark each algorithm and offer to swap your mined tokens for tokens of another algorithm which would’ve cost you more to mine. e.g. if I can do 10 gigahash/s of algorithm A and somebody else can mine 20 gigahash/s of algorithm B, but I can only do 11 gigahash/s of algorithm B and they can only do 9/s of A, then offering 10 units of A for 15 units of B is beneficial for both parties?

---

**pr0toshi** (2019-01-05):

Well the gas replacement and consensus are independent. But I think a pos threshold would be the best for this design.

---

**qizhou** (2019-01-05):

I think nano has similar concept - a transaction must finish some PoW before submitting and being accepted by the network.  Nano claims feeless (or etherless in Ethereum context), however, my thoughts are:

- It is not costless since some PoW is done.
- The system may be flooded by lots of transactions generated by transaction submitters who has better PoW machines and lower electric cost - preventing the reset transactions with lower PoW being accepted by the network.

---

**pr0toshi** (2019-01-05):

Actually I talked to the dev working on threshold consensus for them before it was public. Yeah of course there has to be cost its not about cost its about accessibility. The flood attack has been addressed by having pow be the gas and higher pow being the fee price. If they flood they would need to do far more pow to push up the fee than you would need to do for your transaction. Like if a block can fit 200 transactions they would need to do 200 more pow to push the pow you would need up by 1. It’s highly costly for no real gain.


*(7 more replies not shown)*
