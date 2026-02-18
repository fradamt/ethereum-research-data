---
source: ethresearch
topic_id: 20140
title: The case for decentralization increasing efficiency is overstated
author: captgouda24
date: "2024-07-24"
category: Economics
tags: []
url: https://ethresear.ch/t/the-case-for-decentralization-increasing-efficiency-is-overstated/20140
views: 2462
likes: 7
posts_count: 3
---

# The case for decentralization increasing efficiency is overstated

Block-building on Ethereum has become quite centralized. 90% of blocks are auctioned off through MEV-Boost. Numerous solutions have been proposed, including anonymous inclusion lists and execution tickets. People are concerned about this, both for essentially ideological reasons, and for reasons of efficiency. Blockchains have an ethos of being open to all people, whether or not that is maximally efficient. There is a tradeoff between efficiency (in the sense of getting each block built in the most efficient way, by the most efficient builders) and “fairness”, or including all transactions, if people’s use of the chain is unaffected by the degree of centralization. If blockchain users are concerned their transactions will eventually be sanctioned and rendered worthless, they may avoid that blockchain, or avoid cryptocurrencies altogether. Thus, seemingly inefficient decentralization may be optimal for the blockchain as a whole, and would be unanimously preferred by all blockbuilders to the present equilibrium.

I am concerned, however, that the efficiency case is overstated. Imagine there is a firm so efficient at MEV extraction that they build all of the blocks on chain. If them doing so would cause people to leave the blockchain altogether, then they are incentivized to not bid on some blocks at all.

In “[On block-space distribution mechanisms](https://ethresear.ch/t/on-block-space-distribution-mechanisms/19764)”, Neuder, Garavmidi, and Roughgarden propose execution-tickets as a mechanism for distributing block-building rights, using a proportional all-pay auction. Bidders buy lottery tickets for the right to build a block. In the example given, they have two buyers, buyer 1 with value 4, and buyer 2 with value 2. Under a perfectly efficient system, buyer one always gets the block, at price 2+epsilon. Under their all-pay system, buyer 1 bids 8/9th and buyer 2 bids 4/9th, with them receiving the block rights 2/3rds and 1/3rd of the time, respectively.

Under the description of the example, however, this necessarily *cannot* improve efficiency. If excessive centralization would scare away some users from using the chain at all, the winning monopolist is incentivized to give away some of the block. The value of efficiency is already reflected in their valuations. If you assume that their valuation is always higher, then you are assuming that there is no efficiency case whatsoever. You only have an ideological case, which is fine on its own terms — but you should not mix and match arguments which overstate your case. Note too that we are only caring about one side of the ledger, those who want their transactions to be included. Mightn’t it be possible that some people are repulsed by crypto’s shady reputation?

Nor should this necessarily apply in cases of monopolistic competition. To simply not bid is not the only way to redistribute blocks. If it were the case, the main block-builders would indeed be stuck in a prisoner’s dilemma — they could choose not to bid, but they would have to all do it. If, however, the winners hold another auction for the block, with some of the fairness raising characteristics as before, they can decentralize to the extent which is optimal for them.The drawback is that now the builders internalize a smaller portion of the gains. There is a free-rider problem with decentralization. However, as the market becomes more decentralized, doubtless people will be less concerned about censorship.

The efficiency argument for decentralization therefore much smaller than it would appear. There should probably be a split between allocatively efficient auctions for blocks, and allocatively fair but inefficient markets. What is the right split between the two? It is highly unlikely that it is optimal to only sell blocks in one way all the time.

I think that this is an ideal question for a prediction market. The right amount of decentralization is a macro question. You’re not going to be able to A/B test it in a couple days. Your choices are trying to influence people’s choice in the long run, and answer the question: what is the long run amount of decentralization that maximizes the amount of capital put on the chain. Is there any better use of prediction markets than this? I am somewhat agnostic to the exact method of determining the split — and have no opinions whatsoever as to the proper proportion.

*This post was first posted on my blog [here](https://nicholasdecker.substack.com/p/the-case-for-blockchain-decentralization). Thank you for reading this, please tell me if you disagree.*

## Replies

**MicahZoltu** (2024-07-25):

I’m not aware of anyone who is claiming that decentralized solutions are more efficient than centralized ones.  Everyone I speak with is well aware that the trade being made is censorship resistance for efficiency.  I could build a centralized journaling database today that is extremely efficient, and extremely censorable.

---

**captgouda24** (2024-07-25):

Then I shall claim it. There are very plausible models under which decentralization solves a prisoner’s dilemma and benefits everyone. It implies that there is an as-yet-unknown optimal level of decentralization. We should find it, and do that and no more.

I apologize for having misunderstood others, and for putting arguments in their mouth they may not agree with!

