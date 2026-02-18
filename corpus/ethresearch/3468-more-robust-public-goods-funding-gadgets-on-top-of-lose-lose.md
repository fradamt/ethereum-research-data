---
source: ethresearch
topic_id: 3468
title: More robust public goods funding gadgets on top of lose-lose games
author: vbuterin
date: "2018-09-21"
category: Economics
tags: [public-good]
url: https://ethresear.ch/t/more-robust-public-goods-funding-gadgets-on-top-of-lose-lose-games/3468
views: 1883
likes: 6
posts_count: 5
---

# More robust public goods funding gadgets on top of lose-lose games

See also a simpler older idea: [Call-out assurance contracts](https://ethresear.ch/t/call-out-assurance-contracts/466)

Suppose that there is a set of N participants that are already playing some lose-lose game. For simplicity, we’ll suppose that there are two moves, cooperate and defect, and if the majority cooperates each participant gets H if they cooperate and H - D if they defect, and if the majority defects each participant gets L if they cooperate and L - D if they defect. Casper is an example of roughly this model.

We modify the rules of the game as follows. First, we run the game, and simultaneously use some gadget (eg. voting, quadratic voting, liberal radicalism…) to choose a charity to donate funds to.  If the majority defects, every participant gets L if they cooperated and L - D if they defected. If no charity is chosen and approved by a majority, but the majority cooperates in the game, every participant gets H if they cooperated and H-D if they defected. If the majority cooperates and a charity is chosen, they get some reward M where L < M < H if they cooperated and M - D if they defected, and they themselves can choose whether to donate the difference H - M to the chosen charity or to burn it.

This scheme has the following nice properties:

- It is ~50% fault tolerant in that charities still get funded even if up to 49% are dishonest
- The modification does not cause anyone to suffer a risk of losing funds that they did not suffer before
- The scheme cannot be exploited to extract funds even by a majority attacker, as any “victim” of such an attack would vote to burn the funds, effectively converting an attack on the voting gadget into an attack on the underlying game, which is lose-lose in the case of attacks.

This allows us to do better than assurance contracts and other “fully voluntary” schemes (ie. schemes where no one loses money), by instead leveraging the “involuntary” nature of *existing*  lose-lose games.

## Replies

**slee981** (2018-10-01):

Would you mind elaborating a bit more on implementation? (Unless this was more of a theoretical exercise for you)

Are you suggesting that such a public good funding mechanism would first require Casper PoS, or does the lose-lose game refer to the structure of the smart contract system that “decides” on the funding?

S

---

**vbuterin** (2018-10-02):

This is definitely a line of research I am feeling out: public goods funding mechanisms that achieve properties stronger than those achievable by “pure” algorithms by slapping them on top of other games that have various form of structure that we assume people are already participating in. See https://vitalik.ca/jekyll/general/2017/03/11/a_note_on_charity.html for another much earlier attempt at this in a different context.

Constructions like this, if we can work out a satisfactory one, are theoretically useful as a public good funding gadget which could directly use in-protocol issuance or reclaimed transaction fees as funding, which is certainly something that there has been demand for from many circles, but where naive attempts at implement it easily collapse into the natural vote-buying equilibrium (eg. see the recent EOS scandal https://twitter.com/MapleLeafCap/status/1044958643731533825 and https://twitter.com/MapleLeafCap/status/1046021687114956800). That said, this research is definitely still early enough that I would not be comfortable putting the above on chain.

---

**slee981** (2018-10-04):

I see - that’s an interesting thing to consider and something I’ll dive into more as my schedule allows (and I still have your recent working paper with Glen and Zoe on my to-read list).

As far as application, do you have anything specific in mind with the public good provisioning? Your papers and recent work are very timely for me to discover in that I’ve been thinking a lot recently about how a sufficiently interoperable smart contract system could essentially become infrastructure for a public good i.e. the data itself as a public good. Specifically, if a smart contract system manages some industry data (say hotel room availability), and that system has some open access interface for other projects or businesses to interact with, then one of two things happens:

1. Free use i.e. no transaction fees to smart contract designers – in which case who has incentive to write and maintain the smart contracts? Everyone would position on the interface level where you could potentially charge a usage or service fee.
2. Not free use i.e. transaction fees, paid to the smart contract designers, are written into the contracts – but in this case what stops a group from replicating the code and releasing it without the transaction fees?

Don’t have a clear answer or direction on this yet, so any input is very welcome. To me this is a key thing I’m stuck on since I believe that interoperability is a huge undersold advantage of a public blockchain. Essentially, I think storing key industry data publicly (like hotel room availability) lowers the barrier for firms to enter an industry when large positive network effects can effectively create natural monopolies.

S

---

**vbuterin** (2018-10-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/85f322/48.png) slee981:

> As far as application, do you have anything specific in mind with the public good provisioning?

My short-term target is satisfying people’s desire for an “on-chain treasury” that can fund blockchain-related public goods, essentially doing what EOS and co wanted to do with delegate subsidies but without the plutocratic vote buying risk. This treasury could theoretically fund anything that very many users of the blockchain benefit from but which cannot be easily funded due to the usual tragedy of the commons problems. The long-term “radical markets” target is seeing if techniques like this can be incorporated into wider society.

