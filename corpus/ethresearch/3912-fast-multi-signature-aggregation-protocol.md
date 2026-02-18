---
source: ethresearch
topic_id: 3912
title: Fast Multi-Signature Aggregation protocol
author: nikkolasg
date: "2018-10-24"
category: Sharding
tags: [signature-aggregation]
url: https://ethresear.ch/t/fast-multi-signature-aggregation-protocol/3912
views: 2739
likes: 5
posts_count: 8
---

# Fast Multi-Signature Aggregation protocol

Hi all,

At Pegasys R&D, we are currently working on a *fast* multi-signature aggregation protocol at scale in the presence of Byzantine nodes. Our work lies on top of the San Fermin [0] protocol which is a fast data aggregation protocol with a logarithmic communication complexity. The key insight in San Fermin that the aggregation happens in parallel amongst all nodes, and nodes aggregate larger chunks of data at each phase of the protocol; the number of phase being logarithmic to the number of nodes. San Fermin alone allows for tens of thousands of nodes to aggregate data in a few seconds. Unfortunately, San Fermin is defined in the fail-stop model and we are exploring ways to make it work in the Byzantine model. In that respect, our work-in-progress adds redundancy at each steps of the base protocol to decrease as much as possible the probability of successful attacks such as *eclipse attacks* (where contributions of honest nodes are ignored), while keeping the protocol as fast as possible. While we are still in the research phase, we are working on a paper with a clear description of our threat model, our protocol, an analysis and large-scale experiments. At a second time, we want to deliver an open source library implementing our protocol

tailored to the Ethereum 2.0 context using BLS12-381.

We would be very interested to know if anybody else is working on a similar topic; please reach out to us !

Also, we will be present at the Eth2 meeting in Prague next week, and will be happy to discuss our ideas with folks interested by this subject!

Blazej Kolad, Nicolas Gailly, Nicolas Liochon & Olivier Begassat

Pegasys R&D, Consensys

[0] [https://www.usenix.org/conference/nsdi-08/san-fermín-aggregating-large-data-sets-using-binomial-swap-forest](https://www.usenix.org/conference/nsdi-08/san-ferm%C3%ADn-aggregating-large-data-sets-using-binomial-swap-forest)

## Replies

**vbuterin** (2018-10-24):

We’re already thinking of speeding up aggregation using a two-round protocol, where first signatures for each committee (~128-256 signatures) are aggregated separately in a subnet, then the aggregate signatures are broadcasted in the beacon chain net for inclusion in a beacon chain block (tens of thousands of signatures total).

Is what you are thinking of something of, but possibly with more layers of aggregation in the middle?

---

**khovratovich** (2018-10-24):

Does the BLS aggregated signature work for you? https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html

---

**OlivierBBB** (2018-10-24):

The [Boneh, Drijvers, Neven] scheme (using membership keys and hashing functions on pointed sets of public keys) is useful in a context where rogue public key attacks are possible. It is our understanding that in the current Eth 2.0 (say) the public keys of validators will have to be registered to the beacon chain along with a proof of possession of the secret key. Thus naïve aggregation should be enough.

---

**liochon** (2018-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Is what you are thinking of something of, but possibly with more layers of aggregation in the middle?

Yes. Our best results so far (we can present them next week if people are interested) are with San Fermin, so aggregations are made in parallel on independent sub trees, so there are log2(number of nodes) layers at the end. Today all messages can fit in an UDP message (~500 bytes) if there are less than 6000 nodes, but maybe it’s possible to do better.

---

**jannikluhn** (2018-10-25):

Very cool, looking forward to learning more details about your approach next week.

What exactly are you optimizing for? Network traffic, number of aggregation steps, time, or something else?

---

**jannikluhn** (2018-10-26):

I’ve read parts of the paper and one additional question came up: Who is supposed to participate in the aggregation?

I guess the natural choice would be the validators itself, but here I see a problem with validator privacy: There would have to be a way to connect to specific validators which makes them vulnerable to DoS attacks.

If all nodes aggregate, then one would have to assign one or more validators to each node and the signatures from those validators need to be routed to those nodes. This seems a bit more complicated, but should work.

Are there other options you consider?

---

**nikkolasg** (2018-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> What exactly are you optimizing for? Network traffic, number of aggregation steps, time, or something else?

We are mainly optimizing for time in constituting a final multi-signature ( containing more than 50% of contributions ) and for network traffic.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> I guess the natural choice would be the validators itself, but here I see a problem with validator privacy: There would have to be a way to connect to specific validators which makes them vulnerable to DoS attacks.
>
>
> If all nodes aggregate, then one would have to assign one or more validators to each node and the signatures from those validators need to be routed to those nodes. This seems a bit more complicated, but should work.

That’s a very good point. In that respect, we experimented with a gossip-based solution with a compression scheme that gives a reasonable but higher latency. However, the network load is much higher, since nodes are exchanging more individual signatures as opposed to aggregated signatures.

It’s still possible to limit the effects of a DoS attack with a ‘pure’ ip address solution : one only needs to advertise the ip address used to collect aggregated signatures, and diffuse one’s own contribution from anywhere. Hence a validator under DoS can still contribute to the final multi-signature.

