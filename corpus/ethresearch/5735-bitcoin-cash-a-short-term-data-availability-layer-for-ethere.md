---
source: ethresearch
topic_id: 5735
title: "Bitcoin Cash: a short-term data availability layer for ethereum?"
author: vbuterin
date: "2019-07-13"
category: Sharding
tags: []
url: https://ethresear.ch/t/bitcoin-cash-a-short-term-data-availability-layer-for-ethereum/5735
views: 28348
likes: 14
posts_count: 20
---

# Bitcoin Cash: a short-term data availability layer for ethereum?

**Conceptual background**: [Layer 2 state schemes](https://ethresear.ch/t/layer-2-state-schemes/5691)

**Summary of conceptual background**: there’s a large space of quite powerful and effective scalability solutions that rely on a non-scalable *computation layer* (ie. the current ethereum chain suffices) plus a scalable data layer. The general principle of these techniques is that they use interactive computation techniques (eg. [Truebit](https://truebit.io/)) to compute the state on the ethereum side, crucially relying on the data availability verification guaranteed by the data layer to make sure that fraudulent submissions can be detected and heavily penalized. One could use techniques like this to make a highly scalable general-purpose EVM-like system.

In the longer term (1+ year out) the scalable data layer is going to be ethereum 2.0, because its planned 10 MB/sec data throughput is much higher than that of any existing blockchain. In the shorter term, however, we can start working on these techniques *immediately* by using existing blockchains, particularly those that have lower transaction fees per byte than ethereum, as the data layer. Bitcoin Cash arguably fits the bill perfectly for a few reasons:

- High data throughput (32 MB per 600 sec = 53333 bytes per sec, compared to ethereum ~8kb per sec which is already being used by applications)
- Very low fees (whereas BTC would be prohibitively expensive)
- We already have all the machinery we need to verify Bitcoin Cash blocks inside of ethereum thanks to http://btcrelay.org/ ; we just need to repoint it to the BCH chain and turn it back on. Verifying BCH blocks is also quite cheap compared to eg. ETC blocks
- The BCH community seems to be friendly to people using their chain for whatever they want as long as they pay the tx fees (eg. https://memo.cash)

The main weakness of the BCH chain is its 10 minute block time. This seems unlikely to change unfortunately. However, there is active interest in the BCH community on strengthening zero-confirmation payments using techniques like [Avalanche pre-consensus](https://idelto.com/2018/12/bch-devs-discuss-securing-instant-transactions-with-the-avalanche-protocol/). If these techniques become robust for the use case of preventing double-spends, we could piggy back off of them to achieve shorter finality times as follows. On the Ethereum chain, we randomly select N “proposers”. We incentivize people to send small BCH transactions to these proposers. We require in our layer-2 protocols that for data on the BCH chain to be valid, it must include as one of its inputs a particular UTXO that sends a small BCH payment to them. This way, once a proposer publishes a transaction, if BCH’s anti-double-spend machinery works it will prevent that transaction from being replaced. Though this technique may be too complex to implement in practice, and we may want to just settle for being okay with 10-minute block times for a full general-purpose VM until eth2 comes out.

Another natural alternative is the Ethereum Classic chain, as its has a much quicker 14 second block time; however, it has lower scalability (~8kb/sec) than BCH, and verifying ETC proof of work is much harder. There are changes that ETC could adopt to tip the balance. Reducing the gas costs for calldata (as ETH is planning to) would increase its data rate, and adding flyclient support could reduce gas costs of header verification to a level sufficiently low that the ETH chain can handle it cheaply (note that for these constructions, header verification being delayed by even a day is no big deal, so flyclient is perfect here).

## Replies

**Smithgift** (2019-07-14):

Another potential candidate data-chain would be STEEM. It is designed to store large chunks of consensus-meaningless data (hypothetically posts, but it is culturally accepted to store anything as long as one has the resource credits.) It also has “free” transactions under a sort of fractional reserve system. Hypothetically, as a DPoS chain it will have an easily verified light client system. Or so I thought.

Unfortunately, as far as I could tell, there is no simple way to compute the current witnesses *except* by manually counting votes. This is not a problem for a full node, but obviously impracticable for Ethereum. As I wrote this it occurred to me that the witnesses could fork STEEM to include this information, but that would ultimately be self referential–“Hey, we’re totally the legit witnesses to this block, the block said so!”

In, re: the general idea, how much of this can be done with off-the-shelf parts? I haven’t dived into Truebit yet, but if it can apparently read from IPFS or onchain (ETH) storage, then it can be rewired to work with BCH. (For that matter, if you didn’t mind a little subjectivity, you could create some STEEM-to-IPFS gateway and just hope it all works.)

---

**MaverickChow** (2019-07-15):

If BCH blockchain gets hacked, then what will happen to Ethereum’s data?

---

**James-Sangalli** (2019-07-15):

[@vbuterin](/u/vbuterin) using a library like [summa-tx](https://github.com/summa-tx/bitcoin-spv) would be a cheaper way to verify the bitcoin cash transactions as btcrelay requires the chain be constantly in sync which is expensive and has poor incentives to relayers.

---

**vbuterin** (2019-07-15):

That’s probably not robust enough IMO at least if used in the same way that it’s used in the one-way BTC<->ETH DEX. It becomes much harder to design general-purpose systems when you have to worry about individual components being attackable for relatively small amounts of money, and you have no idea what value is at stake from any given attack. I don’t think devs are capable of working with a mental model anything more complex than “this thing’s fine unless it gets 51% attacked in which case all hell breaks loose but at least that’s very unlikely and expensive”.

Also consider that here we have the luxury of being able to do challenge games over the course of a week, so there’s plenty of other ways to cut validation costs. For example one could even do a challenge-response game where one party claims a new header with a deposit backing it, and then actual verification of headers only happens if someone else claims that a chain not containing that header is canonical. Perhaps using the summa-tx library could be the easiest way to implement such a game though?

---

**Smithgift** (2019-07-15):

> Perhaps using the summa-tx library could be the easiest way to implement such a game though?

A simple method would be, rather than worry about canonical-ness per se, would for the challenger to provide a larger and thus more difficult subchain of headers, some intersecting the claimant’s heights, the claimant can challenge back. and then the protocol just gives the victory to whoever has the heaviest subchain after the challenge period has ended. Chances are this wouldn’t go on for more than a round, as the honest challenger could post days worth of headers for nothing but gas costs, and a dishonest claimant must mine them. Of course, arguably you could set the required initial subchain’s difficulty to be higher than the economic value at risk, but the challenge game is at least more elegant.

EDIT: This of course assumes that there is not a chain with an identical PoW algorithm and with similar difficulty. In this case, an attacker could provide real BTC chain headers to challenge the entirely valid and canonical BCH chain headers. To mitigate this, one could require a proof that BCH-only UTXOs were spent in that block, but that would no longer be simple.

Actually, I’m curious how summa-tx avoids this same problem. Or is it BTC-only?

---

**mrabino1** (2019-07-15):

would the intent be to then migrate the data from BCH back to ETH at some point in the future? anything that goes to another chain exponentially increases the systemic risk as the community has not control on that chain or its future.

---

**ericools** (2019-07-15):

Sounds like Dash would be a good option.  I suspect the community would be open to it’s use in this manner as the Bitcoin Cash community is.  Dash has a shorter block time and instantly secured transactions.  Since nodes on Dash are paid the economic viability of scaling them is known.  I run a masternode myself and have done the math on scaling it up based on my current resource usage and the current costs of available cloud hosting services.  Even if the price of Dash didn’t rise and hosting costs didn’t drop the network would be sustainable for doubling transaction volume 9-10 times (6 million tx a day or so).  We also know that the blocksize for Dash will be increased if the fees grow to be more than 1 US cent since the masternodes were polled and voted overwhelmingly in support of that.

Edit: That was calculated assuming 1 cent per tx fee on average.  I also assumed it would take until 2028 to get to that level and fees would make up a substantial portion of income for nodes at that point.

---

**ChillingSilence** (2019-07-16):

Hi Vitalik,

Respectfully I would recommend investigating DigiByte rather than Bitcoin Cash.

Our RPC calls are almost 1:1 as we are based also on the Bitcoin Core codebase and regularly maintain feature parity with upstream. We are far more secure than Bitcoin Cash though against any form of longer chain re-org thanks to our MultiAlgo PoW and MultiShield difficulty adjustment. We also solve your issue of 10 min blocks by being 40X faster than Bitcoin.

https://medium.com/@josiah_digibyte/why-ethereum-should-use-digibyte-1ddcaf36bfc1

I’ve gone into it a little more in detail here, but I would welcome any feedback on this amendment to your proposal.

Sincerely

Josiah

On behalf of the DigiByte blockchain

---

**MaverickChow** (2019-07-16):

Why not just use solid-state storage device?

---

**colingplatt** (2019-07-16):

[@vbuterin](/u/vbuterin) if I understand your suggestion correctly, you are proposing to include this data in the BCH OP_RETURN space.

If so you may also need to account for the size of the “base” transaction (~227 bytes) and maximum OP_RETURN size per transaction (currently 220 bytes).

---

**juanmixphd** (2019-07-16):

Hi [@vbuterin](/u/vbuterin),

Have you considered FLO as a candidate for an alternate data availability layer for ETH applications?

1. It’s a Litecoin-fork PoW chain from 2013 with a fair launch, using max reorg depth algorithm (same as BCH), and its entire purpose is to store data on-chain
2. 40 second block times with 1mb blocks = 15MB per 600 sec (afaik a hard fork to increase block size is being considered by the devs)
3. There are several live applications on-chain making use of the floData field (electron microscope tomography database, 185,000 Teton County, Wyoming land records).
4. Fees are extremely low
5. All of the supporting software is focused on the floData field

Hope it helps ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=14)

---

**andrarchy** (2019-07-16):

As a member of the Steemit team (the team that released the Steem blockchain) I can say that we are open, eager even, to collaborate with other blockchain projects like Ethereum. Relevant to this specific topic, the Steem Witnesses have chosen to increase the number of custom JSON ops an account can post per block from 1 to 5 in the next hardfork (HF21). So it’s going to become even easier to store a lot more arbitrary code on the Steem blockchain which, in addition to Steem’s 3-second block times and fee-less transactions, I think makes it an extremely attractive layer 2 option for Ethereum. If anyone wants to explore this further, feel free to e-mail me at [andrarchy@steemit.com](mailto:andrarchy@steemit.com)

---

**Milerius** (2019-07-16):

Although I read the entire post, I really feel that the answer to your problems is also found in the blockchain **komodo**. Security, Scalability, Simplicity

---

**PaulSnow** (2019-07-16):

Factom is likely a better solution.

Factom anchors into ethereum so you already have receipts for data based on ethereum.

Factom is cheaper (1000 entries each up to 1024 bytes each for a dollar)

Current Network runs at at least 15 tps, and improving.

Data is organized into tagged lists. You create a chain for your application, defined by the tag of your choice, and add data to that chain as over time. Then you can get those entries later as an ordered list.

External IDs on each entry allow you to easily tag entries, or even treat one entry as a list of data entries, making packing of a set of data into one write easy.

While the cost is to write data into Factom is 1 MB per dollar, the user has significant flexibility in how to use that data.  One can view it as 1000 1k entries per dollar, or 100 10k entries per dollar.  Each entry is 1 to 10k .

Factom uses a two token system so you can write data to Factom without a Factom wallet.  Entry credits are like non transferable pre paid fees, simplifying deployments of Factom/Ethereum integrations.

ChainEstate was a hackathon team that used Factom to add data to erc721 tokens to manage leasing of real estate.  They have won or placed at least a couple of hackatons that I know of.

---

**sidhujag** (2019-07-16):

How does flyclient protect against re-organizations on other chains? For example you throw in data into another chain and that chain re-orgs the last 100 blocks but your policy is to leverage flyclient to determine the longest chain after 5 or 10 blocks, and act on that on some business value with that data that was attested on another chain, would you re-org the external state if so how? Or do you simply just wait a long enough time to remove probabilistic scenario of state becoming invalidated due to re-org? Wouldn’t then still a game around watching for longest chain still work better? aslong as one honest validator is present then it will keep the costs down because you can aggregate blocks and provide simple proofs on demand for under 1m gas and otherwise just store hashes of aggregated blocks say 100-200 blocks at a time for under 300k gas. Your overall gas costs go down but you still have to wait the minimum allotted time to prevent re-org issues so even leveraging a zero-confirmation strategy I don’t know makes much sense in this context just because it needs to be settled for the minimum amount of chain work to be considered probabilistically settled to be able to depend on.

---

**Blocknugget** (2019-07-17):

Hi, please don’t ignore Syscoin. 60k TPS third party verified ( whiteblock) and a functioning zero counter party SYS-ETH bridge. It’s been designed for this purpose.

“THE EVOLUTION OF SYSCOIN PROTOCOL: SYSCOIN 4.0” by Syscoin https://link.medium.com/BdTT1eegoY

“Z-DAG White Paper: Syscoin’s Blockchain Scalability Solution” by Syscoin https://link.medium.com/s990FcIgoY

---

**Blocknugget** (2019-07-17):

“Analysis: Syscoin’s Z-DAG” by Eric Lim https://link.medium.com/x7eNH9kkoY

If you want to test out the bridge yourself via rinkeby testnet go here:

“Syscoin 4.1 Syscoin-Ethereum Bridge” by John Syscoin https://link.medium.com/G8WLR3qkoY

---

**Mikerah** (2019-07-18):

Why not just store all this data in IPFS/swarm/filecoin?

---

**ileuthwehfoi** (2021-04-13):

Aren’t there potential issues around tying yourself to a 3rd party? This feels like treating another chain as a data “miner”, but once you start relying on them, any misalignment in incentives will probably not resolve in Ethereum’s favor.

Edit: whoops, didn’t see the last reply was so long ago. I guess this makes sense, since everything recently on this problem has to do with stateless clients and state expiry instead.

