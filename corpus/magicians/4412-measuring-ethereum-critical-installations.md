---
source: magicians
topic_id: 4412
title: Measuring Ethereum critical installations
author: AlexeyAkhunov
date: "2020-07-11"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/measuring-ethereum-critical-installations/4412
views: 785
likes: 8
posts_count: 3
---

# Measuring Ethereum critical installations

During the AllCoreDev call yesterday, 10th of July 2020, we kept discussing the issues of network health and the dominance of go-ethereum in the network, which leads to go-ethereum developers having to bear much more responsibility than they should.

There are few things that I took away from that call, but here is one of them.

On a call 2 weeks ago, we very quickly jumped to the notion of “client diversity”, which was broadly understood as the relative share of different kinds of Ethereum implementations in the network. Somehow we rather implicitly made a connection between two actual goals and the “client diversity”. These 2 goals seem to be:

1. Resilience of the network to implementation bugs (this was suggested in Discord by @matt)
2. Resilience of the network to capture (this was added in Discord by @MicahZoltu)

Before the call, [@shamatar](/u/shamatar) asked in the gitter channel “**How a share of the client in the network is measured**?”. My answer was that it is usually done by crawlers, that record the info from the eth handshakes. This is relatively easy to sybil attack or masquerade.

This question eventually led to the realisation that we do not have a good definition of what “client diversity” that we desire means. Here is a thought experiment. I spin up couple of backend nodes somewhere, and create lots of lightweight devp2p sentries that would talk to the backend nodes but they will appear as distinct nodes. Although it would change the stats on [ethernodes.org](http://ethernodes.org), it will not change the fact that if go-ethereum has a bug, the network will probably suffer. Why? Because **what matters is not exactly the number of installations, but number of critical installations**, which includes mining pools, exchanges with high volume, wallet/dapp backends, etherscan. This makes the definition messier, but also more useful, because it can make our proposals more actionable

So this was my suggestion:

perhaps the first step we can make (and this is what Eth Cat Herders can help us with) is to create a reliable system that would give us info about the critical installations, but without revealing too much info about them. So we can track important metrics rather than vanity metrics.

It does not need to be completely decentralised, it can be mediated, but it would be super useful to assess where we are and any progress we make.

[@vorot93](/u/vorot93) brought up a good point that “**don’t think any major player in their right mind will ever divulge ownership over specific nodes. Too much of a security risk**”

My reply was as follows. That is why I think it might need to be mediated, so that the attribution to the specific critical operators is kept private, but we see the aggregate picture. Or maybe we can use anonymised tokens that Eth Cat Herders will regularly issue to the critical operators, they will drop them in accordingly without attribution, but we can see the stats reliably. I do not see an obvious incentive for the critical operators to anonymously disinform us.

**EDIT**: An afterthought. The presence of such metrics might be enough to start shifting the balance in diversity of the critical installations - because it creates a useful coordination point for all the critical operators - now they will know what happens if they rely on a single implementation, so it might convince them to run at least two, even at a higher cost.

## Replies

**MicahZoltu** (2020-07-11):

Has there been any thought into creating a wrapper application that runs OpenEthereum, Nethermind, Geth all on the same machine with a JSON-RPC multicast proxy in front of them and it shuts off the RPC proxy if one of the clients disagrees on a result?  This sort of thing could be useful for people running nodes that are converting between on-chain value and off-chain value, as it would prevent them from sending off-chain value if the clients desync (until a human intervenes).

I think for the purpose of resilience to consensus bugs, this sort of thing being used may prevent us from getting into the unfortunate situation where Geth has a consensus bug but we end up patching the other clients to *include* the bug because too much off-chain value was sent before people noticed the bug and halted their off-chain value transfers.  Even if exchanges don’t use such a thing, we (Ethereum developers) are in a much better situation to say, “we gave you all the tools to protect yourself, it is on you that you chose not to use them”.  Right now if geth has a bug the statement to exchanges is, “sorry, our bad, you suffer”.

---

**JohnnySheffield** (2020-07-11):

[@MicahZoltu](/u/micahzoltu) I’ve experimented with similar ideas year or two ago, and wrote a small lib for the same reasons. It is not to be used in production, but has some interesting features. Maybe somebody finds it helpful/interesting


      ![image](https://static-production.npmjs.com/b0f1a8318363185cc2ea6a40ac23eeb2.png)

      [npm](https://www.npmjs.com/package/jayeth)



    ![image](https://static-production.npmjs.com/338e4905a2684ca96e08c7780fc68412.png)

###



A highly experimental JSON RPC router/loadbalancer/aggregator server. Allows you to expose multiple JSON RPC services on one interface.. Latest version: 2.0.1, last published: 6 years ago. Start using jayeth in your project by running `npm i jayeth`....

