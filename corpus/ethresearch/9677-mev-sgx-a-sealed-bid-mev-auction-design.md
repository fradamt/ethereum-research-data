---
source: ethresearch
topic_id: 9677
title: "MEV-SGX: A sealed bid MEV auction design"
author: bertmiller
date: "2021-05-31"
category: Economics
tags: []
url: https://ethresear.ch/t/mev-sgx-a-sealed-bid-mev-auction-design/9677
views: 21830
likes: 20
posts_count: 19
---

# MEV-SGX: A sealed bid MEV auction design

## MEV-SGX: A sealed bid MEV auction design

### Introduction to Flashbots

Flashbots is a research and development organization working on mitigating the negative externalities of current MEV extraction techniques and avoiding the existential risks MEV could cause to state-rich blockchains like Ethereum. Our primary focus is to enable a permissionless, transparent, and fair ecosystem for MEV extraction.

We plan to achieve this by:

- Bringing transparency to MEV activity
- Democratizing access to MEV revenue
- Distributing MEV revenue in a way the benefits the community

Flashbots has released two products so far which make progress on resolving the MEV crisis:

- Flashbots Alpha: a proof of concept communication channel between miners and users for transparent and efficient MEV extraction. Our Alpha consists of MEV-Geth, a fork of the Geth client that provides a sealed-bid blockspace auction that allows users to communicate granular transaction order preferences, and MEV-Relay, a transaction bundle relay.
- MEV-Explore: a public dashboard and live transactions explorer of MEV activity.

Today there are two primary groups of users for Flashbots’ products: miners and searchers. Miners are the block producers of Ethereum who secure the network by performing work in return for the block reward, uncle rewards, and fees from transactions. Miners group together cooperatively in “mining pools” to collectively generate blocks, thereby increasing their probability of successfully mining a block.

Searchers send transactions through Flashbots for inclusion in a block. Searchers are users that “search” for MEV to extract. For example if the price of ETH/DAI is high on Uniswap and low on Sushiswap, then the searcher could buy on Sushiswap and sell it on Uniswap, thus making a profit from the price difference. The searcher would capture this profit by creating a transaction to perform the aforementioned arbitrage and send it to miners, who would include it in return for a transaction fee from the searcher.

Flashbots plays an important role in Flashbots Alpha today as the operator of the MEV-Relay that sits between miners and searchers. The relay is necessary today to prevent DOS or spam attacks on miners for reasons which will be expanded on below.

### MEV-Geth and Flashbots’ design goals

In early 2021 Flashbots released Flashbots Alpha. These were the design goals we launched with:

- Permissionless
A permissionless design implies there are no trusted intermediaries which can censor transactions.
- Efficiency
An efficient design implies MEV extraction is performed without causing unnecessary network or chain congestion.
- Pre-trade privacy
Pre-trade privacy implies transactions only become publicly known after they have been included in a block. Note, this type of privacy ensures that transactions not included in a block remain private, but does not guarantee privacy from privileged actors such as transaction aggregators, gateway, or miners.
- Failed trade privacy
Failed trade privacy implies losing bids are never included in a block, thus never exposed to the public. Failed trade privacy is tightly coupled to extraction efficiency.
- Complete privacy
Complete privacy implies there are no privileged actors such as transaction aggregators / gateways / miners who can observe incoming transactions.
- Finality
Finality implies it is infeasible for MEV extraction to be reversed once included in a block. This would protect against time-bandit chain re-org attacks.

**[![](https://ethresear.ch/uploads/default/optimized/2X/b/b01f5c122d02b007792085bded3123c6ae2018c0_2_347x162.png)1151×537 204 KB](https://ethresear.ch/uploads/default/b01f5c122d02b007792085bded3123c6ae2018c0)**

While Flashbots Alpha has been and continues to be successful it offers incomplete trust guarantees. It is not *permissionless* because miners who adopt it have to be whitelisted by MEV-Relay in order to be forwarded bundles. It is not *completely private* because bundles can be seen by miners prior to inclusion on-chain. Lastly, Flashbots Alpha offers no *finality* protection against chain reorgs. While finality is important, we are focusing first on permissionless and complete privacy as the next design goals to achieve.

The properties of permissionlessness and complete privacy are difficult to achieve for three reasons. First, Flashbots introduced 0 gas price transactions which pay the miner through a smart contract transfer. These create a potential DOS vector as miners need to simulate transactions in order to determine their profitability, if any at all, and a malicious searcher could spam miners with worthless transactions at no cost to force them to expend resources simulating these transactions. In contrast with regular Ethereum transactions there is an inherent cost to sending transactions because of the fees paid due to the gas price of the transaction. Further, nodes on the network help to filter out bad transactions sent through the public mempool.

Second, many proposed solutions to provide complete privacy or permissionlessness introduce latency and reduce overall system performance, which could lead to a higher rate of mining uncle blocks. Lastly even worse than mining an uncle block is mining a block that is altogether invalid. A completely private system will need to provide miners additional guarantees that the blocks they are mining without seeing are valid and profitable to mitigate the risk of mining invalid blocks.

### Approaches to completely private and permissionless MEV auctions

There are a few different proposals for completely private and permissionless MEV auctions. In this section we will briefly review each as well as their associated tradeoffs. Some further discussion can be found in our #MEV-Research [Discord channel](https://discord.com/invite/7hvTycdNcK) as well as the “[Privacy Solutions for MEV Minimization](https://drive.google.com/file/d/1_4-E_i6WIDMNRDIgBIf0YiaJtm33XW9s/view?usp=sharing)” roast.

**Using block headers for privacy**

One proposal for achieving a permissionless and completely private MEV auction is for searchers to craft full blocks and send the headers of those blocks to miners while withholding the content of the transaction trie. Using these headers miners would be able to perform proof-of-work, but they would not see the full block or the transactions that went into it. After a miner finds a proof-of-work solution the searcher would reveal the full block data to the miner, at which point the transactions would become visible to the miner and the block would be sent to the network for inclusion. Although this achieves our desired privacy guarantees, miners are unable to verify the validity of a block before performing work and therefore this proposal does not solve for permissionlessness. Thus without some kind of permissioned system or whitelist a malicious searcher could send invalid blocks to the miner and DOS the network.

**Bonded block headers**

A variation of the block header mechanism would be to require searchers to post bonds before they can send block headers to miners. If searchers act maliciously (e.g. spam invalid blocks, withhold block content), their bond could be either slashed or claimed by the miner, thereby introducing a cost to bad behavior. A drawback of this mechanism is it increases the barriers to entry for new users by requiring them to lock up a significant amount of capital (commensurate to the opportunity cost of DOS). We are still exploring this solution in parallel. [MiningDAO](https://miningdao.io/) has implemented a variant of this system and other community proposals can be found [here](https://hackmd.io/uTptoEtLQwOrt9sm2fc2cw) and [here](https://github.com/flashbots/pm/discussions/27#discussioncomment-613235).

**Timelock encryption**

Timelock encryption, often referred to as “commit reveal scheme,” is a cryptographic primitive that ensures an encrypted message can only be decrypted after a certain period of time has passed, using for example Verifiable Delay Functions. In our context searchers could send their encrypted transactions to miners where they would be added to the block immediately. After a period of time (or number of blocks), miners and other users of the network could decrypt the transaction to reveal its content. Since transactions would be encrypted for a period of time then current permissionless methods for propagating Ethereum transactions could be used.

Using timelock encryption has several drawbacks. First, many MEV extraction opportunities are timebound (e.g. they will be captured in the next block) and a solution that delays the execution of searchers’ transactions would make it impossible to extract these opportunities. Making all transactions timelocked could level the playing field, but that would severely degrade user experiences. Furthermore there is an inverse correlation between user experience and security: the longer the delay between transaction inclusion and execution, the stronger the security offered by timelock encryption.

**Threshold encryption**

Another cryptographic solution would be to use threshold encryption such that a committee of block producers is required to decrypt encrypted transactions sent by searchers. Each miner would have a share of a decryption key and some threshold (e.g. n of m) would be needed to decrypt transactions. While this solution provides some additional privacy and validity guarantees, it relies on an honest majority assumption that the key holders won’t collude to break the encryption, therefore it is difficult to make joining the set of key holders a permissionless process. Threshold encryption by committee also introduces a bandwidth intensive step to block production which may be found to be untenable. Threshold encryption could be a promising path forward if these concerns are resolved.

**Secure enclaves**

Secure enclaves, like Intel’s SGX or AMD’s SEV, could also be leveraged. Searchers would use an enclave to validate that their bundles are valid and profitable, thus mitigating DOS and enabling permissionless interactions between searchers and miners. Miners would use an enclave to store encrypted blocks from searchers, and receive truncated header hashes they can use to perform proof-of-work. The miner’s enclave would unencrypt and seal the searcher’s block when provided a proof-of-work solution.

A drawback of this solution is that the searcher’s privacy guarantees are only as strong as the security of the miner’s enclave and it would be difficult for the searcher to determine if the miner has broken the enclave. Furthermore, using enclaves may introduce latency into the system that make it infeasible to use.

**Summary of approaches and their tradeoffs**

|  | Permissionless | Complete privacy | Latency | Drawbacks |
| --- | --- | --- | --- | --- |
| Secure Enclaves | Yes | Yes | Low - Medium | Non-falsifiable guarantees for the searcher, potentially latency |
| Timelock | Yes | Correlated to delay | Low | High transaction execution delay |
| Threshold Encryption | Yes | Yes | High | Assumes an honest committee and is bandwidth expensive |
| Block headers | No | Yes | Low | Malicious searchers can spam miners or send invalid blocks |
| Bonded block headers | High startup cost | Yes | Low | Requires significant capital (commensurate with the opportunity cost of a DOS) to become a searcher |

While all of these solutions deserve to be researched further, this post presents a proposal for how permissionlessness and complete privacy guarantees can be achieved through the use of secure enclaves. Other designs are not being ruled out, but we are seeking to implement a system that achieves our design goals as soon as possible.

### MEV-SGX

MEV-SGX uses secure enclaves, specifically Intel’s SGX, to provide complete privacy and permissionlessness. In MEV-SGX both searchers and miners have their own SGX, and here we use “miners” interchangeably for “mining pool.” Searchers craft a full block with their transaction(s) included in it and validate that block in their SGX. The searcher’s SGX then encrypts the block and sends it to miners along with the unencrypted truncated header hash of that block. Miners would store the encrypted block in their SGX and use the truncated header hash for proof-of-work. Only after finding a proof-of-work solution and providing that to their SGX can miners decrypt the encrypted block, seal it, and propagate it to the network. Sealing is the process of adding the mix hash and nonce to a block header.

Prior to interacting, searchers and miners perform a handshake and use cryptographic attestations to ensure that each party is running the right software in an SGX. Due to the tamperproof nature of SGX these attestations provide cryptographic trust to searchers and miners, as they have guarantees that their counterparty is running specific code in an environment that cannot be tampered with or broken into. The searcher’s use of the enclave allows them to permissionlessly interact with miners by ensuring the blocks that searchers send them are valid. The miners’ use of the enclave provides complete privacy to searchers.

**MEV-SGX Architecture and Process**

The architecture for MEV-SGX looks like this:

**[![](https://ethresear.ch/uploads/default/optimized/2X/3/36c1e5c143a721710d02b56b4f5511278f12b835_2_624x176.png)1600×451 82.2 KB](https://ethresear.ch/uploads/default/36c1e5c143a721710d02b56b4f5511278f12b835)**

Building off of the architecture, these are the steps involved in the process of MEV-SGX:

1. Handshake: The searcher and miner perform a handshake to discover each other, exchange public keys, and verify that each party is running MEV-SGX in an SGX through cryptographic attestations.
2. MEV Opportunity Detection: The searcher detects some MEV then creates transactions that extract it and pay the miner upon successful extraction.
3. Block Creation: Searchers use their node to generate a block including their MEV-extracting transactions. They also generate the block witness and input both the block and the witness into their SGX.
4. Block Validation: The searcher’s SGX processes the block to ensure it is valid and profitable for the miner by using the block witness generated in (3).
5. Block Transfer: The searcher’s SGX encrypts the block with the miner’s public key and sends it to the miner. The searcher’s SGX also sends the miner the block’s truncated header hash and how profitable that block was.
6. Block Selection: The miner selects the most profitable block they’ve received.
7. Proof-of-Work: The miner uses the most profitable block’s truncated header hash to request proof-of-work from workers.
8. Block Sealing: After finding the proof-of-work solution the miner passes that into their SGX. With this solution the miner’s SGX decrypts, seals, and exports the block outside of their SGX.
9. Block propagation: The miner’s node propagates the decrypted and sealed block to the network.

A detailed list of steps, definitions, and the inputs and outputs of each step can be found in [the appendix](https://docs.google.com/document/d/1DvphqpEmG2RZgfg2XoNkzq1yxhBwb3Gn1Nl9Qvtbgis/edit?usp=sharing).

**MEV-SGX block production process diagram**

MEV-SGX changes the process by which blocks are produced, validated, and propagated to the network. The block production process is as follows:

**[![](https://ethresear.ch/uploads/default/optimized/2X/7/7cc212f66db714e23c10f7f8082edfc333f950ab_2_624x188.png)1600×484 122 KB](https://ethresear.ch/uploads/default/7cc212f66db714e23c10f7f8082edfc333f950ab)**

A higher resolution version of this diagram can be viewed [here](https://whimsical.com/mev-sgx-block-production-process-7e27fxtTDJxM94Sa1Ta4mG).

**Limitations of MEV-SGX**

Below are several limitations of MEV-SGX in bold, along with mitigating actions in non-bolded text:

- Increased latency from using SGX: Minimize what is done in the SGX, explore new generations of SGX, perform rigorous benchmarking, and move towards low-level implementation for optimal performance.
- Searchers could break their SGX: Falsifiable by the miner by checking for invalid blocks. If it happens the systems falls back to Flashbots Alpha.
- Miners could break their SGX: This is non-falsifiable by the searcher. Currently exploring solutions like threshold committees that mitigate this limitation.
- Searchers must propose full blocks: If searchers need to propose full blocks then it is much more difficult to do bundle merging between multiple searchers. We are researching methods of partial block proposals for searchers and privacy preserving bundle merging in the miner’s SGX as well.
- Reliance on SGX: Explore feasibility of offering multiple types of secure enclaves as well as continuing research into software and cryptoeconomic based methods of achieving complete privacy.
- Miners can see searchers transactions after sealing the block, but before propagating it: Explore alternative structures that don’t rely on the miner for data availability

**Summary of MEV-SGX proposal**

MEV-SGX could enable Flashbots to achieve its design goals of creating a completely private and permissionless system. Searchers would craft blocks with their bundles included, validate and encrypt those blocks in their SGX, and send them to miners alongside block truncated header hashes. Miners receive truncated header hashes and encrypted blocks they know are valid and profitable for them to mine. They use the truncated header hashes to perform proof-of-work on blocks without seeing them, and upon finding a proof-of-work solution are able to decrypt and seal blocks.

### Next Steps and Open Questions

MEV-SGX is in early stages of development. Flashbots intends to take this design and implement a proof-of-concept that can help us learn more, pressure test our assumptions, and carry out latency benchmarks. From there we will release our findings and start work on a version of MEV-SGX that searchers and miners can test, and will keep testing and iterating on MEV-SGX thereafter. In parallel we intend to continue to research alternatives for ensuring complete privacy and permissionlessness.

There are several open technical and theoretical questions with MEV-SGX that we are seeking to explore in the coming months (please reach out if you want to contribute!).

**MEV-SGX**

1. What is the latency overhead from MEV-SGX compared to the normal block production process?
2. How can MEV-SGX provide complete privacy and merge non-competing bundles at the same time?
3. In the current design for MEV-SGX the searcher cannot provably tell if miners have broken into their SGX. In other words the trust guarantees of the miner’s SGX are non-falsifiable. How can we either provide falsifiable guarantees or mitigate the risk of a miner breaking their SGX?
4. MEV-SGX relies on the miner to propagate blocks to the network although the miner has no role in crafting or validating that block. Can we rely on the searcher for propagating sealed blocks instead?

**ETH2.0**

1. How does the design of MEV-SGX change in ETH2.0?
2. Does ETH2.0 make it easier to achieve our design goals with cryptographic or cryptoeconomic methods besides secure enclaves?
3. In ETH1 miners have to perform proof-of-work before they are able to decrypt and seal the block, and this gives them an incentive to immediately propagate the block instead of frontrunning the searcher and mining a new block with their transaction in it. In ETH2 validators would not have to expend resources before they can decrypt and seal the block. How should our design change to account for this?

**System design**

1. What are the alternatives to secure enclaves for achieving our design goals of permissionless and complete privacy? Which of these can be achieved without a protocol change?
2. Should MEV-SGX be considered an add on to existing systems, or a replacement? In other words, should MEV-SGX be run in parallel to the existing non-private MEV-Relay or should it replace it?

### Appendix

Please see [this link](https://docs.google.com/document/d/1DvphqpEmG2RZgfg2XoNkzq1yxhBwb3Gn1Nl9Qvtbgis/edit?usp=sharing) to find a list of definitions and a table detailing the process of MEV-SGX step by step with data inflows and outflows for each step.

### Call for Feedback & Contributions

- Contribute to MEV-Research
We invite you to review our MEV-Research GitHub repo to learn about our MEV Fellowship program. Start contributing through opening or answering a Github issue, and/or writing a Flashbots Research Proposal (FRP), and join our discussion on our MEV-Research discord community.
- Try our proof of concept
We hope to have a proof of concept released shortly. We encourage traders and miners to review our code base and try MEV-SGX out. Join our Flashbots discord community or contact us at info@flashbots.net
- Subscribe to MEV Ship Calendar
You can follow the latest updates and events by subscribing to our MEV Ship Calendar: join us on our semi-monthly community call “MEV Ship Treasure Map Roast”, semi-weekly core dev call, weekly research workshop, and the upcoming unconference: MEV.wtf
- Work with us
Flashbots has several open jobs, including a systems engineer role that encompasses MEV-SGX work. If you are a self-directed individual who puts collective success above your own and are motivated by solving hard problems with asymmetric impact, you will fit right in.

## Replies

**vbuterin** (2021-05-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> If searchers act maliciously (e.g. spam invalid blocks, withhold block content), their bond could be either slashed or claimed by the miner, thereby introducing a cost to bad behavior.

What is the mechanism by which this slashing works? How would the chain reliably tell if a searcher withheld the block body by one slot?

---

**kladkogex** (2021-06-01):

Hey

Threshold-encryption-based MEV protection is under heavy development at SKL and will be released on SKL main net in July,

In our case TE does not introduce delays since decryption is done during consensus by the same committee that does consensus literary during consensus.

It also works with existing libraries (such as web3.js). The entire body of the transaction is encrypted except things like gas price, gas limit and sender.

If anyone else wants to implement TE-based protection, our implementation of TE is here



      [github.com](https://github.com/skalenetwork/libBLS)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/f/7/f749de1f54c26e4bcbc370a71c0f1c5eb61dfd5f_2_690x344.png)



###



If you like this project, please ⭐⭐⭐ it on GitHub!! Solidity-compatible BLS signatures, threshold encryption, distributed key generation library in modern C++. Actively maintained and used by SKALE for consensus, distributed random number gen, inter-chain communication and protection of transactions. BLS threshold signatures can be verified in

---

**wminshew** (2021-06-02):

iiuc in miningDAO the funds are claimed by the miner for providing the completing nonce (rather than slashed–I am not familiar with the other ideas/protocols grouped into this bucket). Image below from their medium launch post

[![image](https://ethresear.ch/uploads/default/optimized/2X/a/ac1470d78010aa68b01924dd28b259723ff2ad28_2_690x309.png)image826×370 38 KB](https://ethresear.ch/uploads/default/ac1470d78010aa68b01924dd28b259723ff2ad28)

---

**Yaeldo** (2021-06-02):

Hi Robert,

This is a great post, thanks for clarifying the SGX scheme! I have 2 questions:

1.

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> The relay is necessary today to prevent DOS or spam attacks on miners for reasons which will be expanded on below.

What is done by the relayer to prevent DOS attacks?

Do Flashbots whitelist only the miners or also the searchers? What is the criteria to be whitelisted?

1.

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> Handshake: The searcher and miner perform a handshake to discover each other, exchange public keys, and verify that each party is running MEV-SGX in an SGX through cryptographic attestations.

What is the latency for the handshake? Is this supposed to happen between each miner and searcher in the network before they start to produce blocks together or is it done as part of the block creation?

---

**Shymaa-Arafat** (2021-06-02):

> Using timelock encryption has several drawbacks. First, many MEV extraction opportunities are timebound (e.g. they will be captured in the next block) and a solution that delays the execution of searchers’ transactions would make it impossible to extract these opportunities.

You r describing the main “commit-reveal” advantage as a drawback?!

As if u want miners to front run users transactions, u even want to delay the block to enable them to and consider the latency as the only problem?!

.

For ur solution, what I get as the main ideas

1-u added handshake step to authenticate the searchers, thus trust they’re not malicious.

2-In ur system miners depend completely on searchers to decide & choose their MEV

3- u want the decrypting (u encrypting) to happen after presenting the POW but before adding the block to the blockchain so that miners approve the searchers choice?

What about the victimized user?

---

**bertmiller** (2021-06-02):

Yep so mining DAO is effectively searchers “pre-paying” for their blocks/MEV extraction. An alternative would be something like what Micah proposed in Flashbots’ #MEV-Research channel, which was a “credibly neutral layer 2” for proofs leveraging block headers from the searcher and nonces from the miner.

I think Phil is also working on a slashing mechanism for a similar proposal. I’ll ping him on that. But we’re interested in more community involvement on this design generally.

---

**bertmiller** (2021-06-03):

> What is done by the relayer to prevent DOS attacks?

We simulate every bundle and filter out invalid bundles and bundles that are not competitive (e.g. they pay far below the market rate for gas, and thus would never get included).

> Do Flashbots whitelist only the miners or also the searchers? What is the criteria to be whitelisted?

Initially searchers had to be whitelisted, but we moved to a system that is permissionless for searchers earlier this year. There is no whitelisting for searchers anymore. We do whitelist miners though, let me get the right person to reply to you about the criteria.

> What is the latency for the handshake? Is this supposed to happen between each miner and searcher in the network before they start to produce blocks together or is it done as part of the block creation?

The handshake is something that only needs to be done once so long as the searcher and miner maintain a connection. So it can be done prior to producing blocks and doesn’t need to be repeated for every block. It only takes a very seconds - not very long at all.

---

**bertmiller** (2021-06-03):

> You r describing the main “commit-reveal” advantage as a drawback?!
> As if u want miners to front run users transactions, u even want to delay the block to enable them to and consider the latency as the only problem?!

Yes I think it is a clear drawback that users’ transactions would be delayed. It’s a bad experience. A few Flashbots team members were involved with efforts to get protocols and users to use commit-reveal schemes (https://libsubmarine.org/) and found that people did not want to accept the tradeoff of having a worse UX.

> For ur solution, what I get as the main ideas
> 1-u added handshake step to authenticate the searchers, thus trust they’re not malicious.
> The searcher also authenicates/attests that the miner is running MEV-SGX in an SGX.

> 2-In ur system miners depend completely on searchers to decide & choose their MEV

Yes, and the blocks in general.

> 3- u want the decrypting (u encrypting) to happen after presenting the POW but before adding the block to the blockchain so that miners approve the searchers choice?
> What about the victimized user?

Yes, decrypting does happen after the POW solution is presented but before the block is propagated to the network. This is a potential vulnerability of the solution, as a miner could look at the block prior to propagating it and frontrun the user.

However, note that in order to frontrun the user the miner would need to create a new block and find another POW solution. Given the time that this will take and the competitiveness of mining this essentially means forgoing that block’s reward. In some cases (e.g. very large MEV) there will be an incentive to do so. Two potential ways to mitigate this:

1. Use threshold encryption to store blocks across multiple miners and have a committee decrypt them
2. Rely on the searcher for data availability. Specifically the searcher would not give the encrypted block to the miner, and instead only forward the truncated header hash to the miner. The miner would provide the POW solution to the searcher after finding it, and the searcher would seal and propagate the block. This introduces new complexity, e.g. we need to ensure that the searcher does not withhold the block somehow.

I’m not sure what you’re referring to by “what about the victimized user” but I would note that anyone can run MEV-SGX, even regular users, and get frontrunning protection.

---

**Shymaa-Arafat** (2021-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> Yes I think it is a clear drawback that users’ transactions would be delayed. It’s a bad experience

I’m not arguing that delay is a drawback, I’m just saying in this particular case the delay is like an alarm/symptom of MEV happening against the normal user will inspite of using Commit-reveal (that’s why I consider the user as a victim, I guess it all depends on where u draw the line bet accepted MEV & malicious MEV; there’s a topic entitled towards zero MEV)

.

Anyways, that’s what I meant & I understood about the cause of delay from what u wrote, I didn’t read the link u attached in ur reply yet.

---

**pmcgoohan** (2021-06-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> I’m not sure what you’re referring to by “what about the victimized user”

The victimized user is the sender of a transaction that gets frontrun, backrun, sandwiched, etc to their very great cost. They represent the vast majority of users on Ethereum.

MEV-SGX will make the situation worse for these users because it will allow MEV extraction to be more efficient for the searchers.

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> anyone can run MEV-SGX, even regular users

As I have shown before, the vast majority of victimized users cannot afford to win MEV auctions (as is currently the case with MEV-Geth) so being MEV-SGX searchers will not help them.

Users may try to aggregate their bids in an attempt to win MEV auctions against larger competitors (eg: MistX).

However, in this case users win the block for the aggregator who then has the power to extract MEV. This is still the case even if you get MistX/MEV-SGX working because the centralized aggregator only needs enough enc txs to win the block, at which point they can use the rest of the block to extract MEV from the mempool in the usual way.

The aggregator may behave and not do so. So may Binance. So may Nasdaq. It is neither trustless nor decentralized, so we’re back to the why not just run Ethereum on an instance of MySQL argument.

The best case for how I see MEV-SGX evolving is that it becomes fully distributed and encrypts individual txs successfully for a fully distributed aggregator (or becomes one itself). If you then build this into the core protocol so that block producers fail attestation when they diverge from the distrbuted aggregator content, you get an encrypted content layer which is what I am trying to do.

---

**bertmiller** (2021-06-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> The victimized user is the sender of a transaction that gets frontrun, backrun, sandwiched, etc to their very great cost. They represent the vast majority of users on Ethereum.

Some MEV is extractive (in most cases I don’t think backrunning is, though) and the cost is borne by (mostly) users. You’re right we should try to reduce that. In the context of the message I wasn’t sure what exactly Shymaa-Arafat was referring to.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> MEV-SGX will make the situation worse for these users because it will allow MEV extraction to be more efficient for the searchers.

I think you discount the degree to which a truly private system will aid in preventing “bad” MEV extraction. Today if you want to avoid hungry sandwich bots in the mempool you need to go direct to a miner, but you’re trusting the miner not to sandwich you then. MEV-SGX ensures that even miners can’t sandwich users. I can’t think of a better frontrunning protection mechanism right now.

A more efficient mechanism for MEV extraction is also desirable because it should reduce the negative externalities from PGAs.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> As I have shown before, the vast majority of victimized users cannot afford to win MEV auctions (as is currently the case with MEV-Geth) so being MEV-SGX searchers will not help them.
>
>
> Users may try to aggregate their bids in an attempt to win MEV auctions against larger competitors (eg: MistX).
>
>
> However, in this case users win the block for the aggregator who then has the power to extract MEV. This is still the case even if you get MistX/MEV-SGX working because the centralized aggregator only needs enough enc txs to win the block, at which point they can use the rest of the block to extract MEV from the mempool in the usual way.
>
>
> The aggregator may behave and not do so. So may Binance. So may Nasdaq. It is neither trustless nor decentralized, so we’re back to the why not just run Ethereum on an instance of MySQL argument.
>
>
> The best case for how I see MEV-SGX evolving is that it becomes fully distributed and encrypts individual txs successfully for a fully distributed aggregator (or becomes one itself). If you then build this into the core protocol so that block producers fail attestation when they diverge from the distrbuted aggregator content, you get an encrypted content layer which is what I am trying to do.

I don’t think your claim is true and we have empirical evidence today that it isn’t. Individual and regular users - who are not aggregated at all nor are they whales - are consistently winning the MEV auction against searchers and being included in blocks today. MistX is a great example, and MistX does *not* aggregate any bids together.

It may be the case that there are relays or aggregators in the future which merge a bunch of user’s transactions together to form blocks that are input into MEV-SGX. We should be able to use secure enclaves to give those users guarantees that they won’t be frontrunned/have MEV extracted from themselves.

---

**mightypenguin** (2021-06-06):

There have already been several published attacks on SGX.

And that’s assuming no one is holding onto private attacks.

Relying on it for anything important seems very risky to me.

This would allow more powerful entities to have an unfair advantage vs the more open nature of the current, but still flawed situation.


      ![](https://ethresear.ch/uploads/default/original/3X/e/e/ee8c06420f791149e821f7950625adf6813a2b40.png)

      [Ars Technica – 10 Nov 20](https://arstechnica.com/information-technology/2020/11/intel-sgx-defeated-yet-again-this-time-thanks-to-on-chip-power-meter/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/f/8/f80d3442509ea2f207f66e183f52e5dfc17644fd_2_690x436.jpeg)

###



New research sends chipmaker scrambling to fix side channel that exposes secret data.












      [en.wikipedia.org](https://en.wikipedia.org/wiki/Software_Guard_Extensions#Attacks)





###

Intel Software Guard Extensions (SGX) is a set of instruction codes implementing trusted execution environment that are built into some Intel central processing units (CPUs). They allow user-level and operating system code to define protected private regions of memory, called enclaves. SGX is designed to be useful for implementing secure remote computation, secure web browsing, and digital rights management (DRM). Other applications include concealment of proprietary algorithms and of en SGX invo...

---

**yoavw** (2021-06-08):

Great post.  I’ll try to address some of the open questions:

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> In the current design for MEV-SGX the searcher cannot provably tell if miners have broken into their SGX. In other words the trust guarantees of the miner’s SGX are non-falsifiable. How can we either provide falsifiable guarantees or mitigate the risk of a miner breaking their SGX?

It’s impossible to prove if SGX has been compromised after the handshake attestation but the searcher could use decoys that automated frontrunners are likely to bite, and watch the miner’s behavior.  For example, include two transactions.  One that puts 1 ETH in a contract with an unprotected withdraw() that only works in the current block.number and an ownerOnly withdraw2(), followed by another transaction that calls withdraw().  Any automated miner would frontrun the second transaction, stealing the 1 ETH and revealing that it violated pre-trade privacy.  Discarding the block to frontrun it in a later block won’t work because only the ownerOnly withdraw2() can be called on later block.

Simple decoys could reveal miners that figured out how to compromise SGX, but they’ll only work as long as miners are not aware of them and opt to play the long game by not taking the decoy reward.  A smart decoy-generator could make them indistinguishable from other MEV opportunities unless the miner uses a whitelist for known MEV calls.

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> MEV-SGX relies on the miner to propagate blocks to the network although the miner has no role in crafting or validating that block. Can we rely on the searcher for propagating sealed blocks instead?

Probably not.  What would stop a searcher from spamming miners with valid blocks and then never propagating them or just doing it too slowly?  With PoW this is time critical, so timelocks for letting the miner also propagate the block after a while won’t solve it.

However, why is it an issue?  The miner already spent resources and successfully found PoW for the block and can collect the honest reward.  Attempting to gain more by mining a new block for frontrunning the searcher is a losing proposition, as someone else will probably mine the block by then.  The searcher could (should?) send the same block (with different coinbase address) to different miners, so one honest/greedy miner will likely propagate the block.  The censoring miner gains nothing, only loses money.

Therefore I’m not sure if this direction is worth pursuing.

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> Does ETH2.0 make it easier to achieve our design goals with cryptographic or cryptoeconomic methods besides secure enclaves?

It could.  See discussion in [Proposer/block builder separation-friendly fee market designs](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725)

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> In ETH1 miners have to perform proof-of-work before they are able to decrypt and seal the block, and this gives them an incentive to immediately propagate the block instead of frontrunning the searcher and mining a new block with their transaction in it. In ETH2 validators would not have to expend resources before they can decrypt and seal the block. How should our design change to account for this?

Since you already rely on SGX security and I assume the validator’s private key only exists in SGX, why not use it to prevent the miner from signing a different block with the same number?

When the enclave is running, it keeps the latest block number it released the plaintext of.  The number is updated whenever the caller reads a plaintext signed block.  The enclave will refuse to sign any block lower or equal to this number.

This prevents the validator from frontrunning in the current slot.  It can either propagate the block, or withhold it and let the next validator take the reward.  As long as these two random validators are not colluding, the winning strategy for the validator is to propagate the block.

Note on rollback attacks: SGX doesn’t have its own storage and relies on the caller to provide it upon creation.  By default it means that the validator could terminate and recreate the enclave with an old state, and have it sign another block with the same number.  The “standard” mitigation is to ensure state freshness using SGX’s monotonic counters which are saved to NVRAM.  I wouldn’t use it in this case because this memory wears out after ~10000 writes and the hardware needs to be replaced.  Instead, add a forced 10 seconds delay when the enclave is created (as in proof of elapsed time).  It can only start signing blocks 10 seconds after boot.  It doesn’t affect normal operation but prevents a rollback attack from signing two blocks in the same slot.  Enclave restart is guaranteed to miss the current slot.

This seems to be the minimal change to support PoS, as it doesn’t change the architecture in any way, and is invisible to honest validators.

---

**lsankar4033** (2021-06-09):

> In ETH2 validators would not have to expend resources before they can decrypt and seal the block. How should our design change to account for this?

Isn’t the fact that PoW isn’t grindable crucial to mev-sgx working? I.e. having to compute PoW to decrypt the block is what keeps miners honest here and makes it distinct from *not* having sealed bids.

I could be mistaken, but this suggests to me that there wouldn’t be much of a benefit to using an analogue of mev-sgx in proof of stake land.

---

**yoavw** (2021-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/lsankar4033/48/10215_2.png) lsankar4033:

> Isn’t the fact that PoW isn’t grindable crucial to mev-sgx working? I.e. having to compute PoW to decrypt the block is what keeps miners honest here and makes it distinct from not having sealed bids.
>
>
> I could be mistaken, but this suggests to me that there wouldn’t be much of a benefit to using an analogue of mev-sgx in proof of stake land.

Doesn’t my suggestion above solve this?  If the enclave increments the saved block number and refuses signing an additional block with the same number, then the miner cannot change its decision after decrypting the block (as long as SGX is not compromised).

---

**siddutta** (2021-08-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> Doesn’t my suggestion above solve this? If the enclave increments the saved block number and refuses signing an additional block with the same number, then the miner cannot change its decision after decrypting the block (as long as SGX is not compromised).

Isn’t the assumption here that a validator uses a SGX-based key to sign blocks? Would that be a good practice to begin with?

---

**yoavw** (2021-08-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/siddutta/48/6951_2.png) siddutta:

> Isn’t the assumption here that a validator uses a SGX-based key to sign blocks? Would that be a good practice to begin with?

Yes, it requires that the validation key will exist only in SGX.  Why is that bad?  The enclave generates the key, seals it and exports it.  The sealed key can be unsealed and used by the enclave for validation.  It can also be backed up and restored on a new machine running the same enclave.  The validator never needs direct access to the validation key because it can always validate in SGX as long as it remains compliant with the above policy.

Also keep in mind that the validation key is not the withdrawal key.  The validation key must be online, so it seems safer to keep it in SGX where it is used with some sanity checks.  The withdrawal key is never kept online and is not needed by SGX.

---

**dB2510** (2022-01-15):

Hi [@bertmiller](/u/bertmiller)

How can this affect the Implementation or future of MEV-SGX?

[Refer Page Number 51](https://t.co/rmXASGttxo)

Thanks

