---
source: ethresearch
topic_id: 14134
title: A Tor-based Validator Anonymity Approach (incl. comparison to Dandelion)
author: kaiserd
date: "2022-11-07"
category: Privacy
tags: []
url: https://ethresear.ch/t/a-tor-based-validator-anonymity-approach-incl-comparison-to-dandelion/14134
views: 4189
likes: 4
posts_count: 10
---

# A Tor-based Validator Anonymity Approach (incl. comparison to Dandelion)

# Abstract

This post proposes a Tor-based approach for relatively easy-to-deploy validator anonymity,

with a focus on protecting the next epoch’s validator from DoS attacks.

The proposed approach uses the Tor network to anonymously push messages into the existing BN gossipsub network.

This post also compares our Tor-based approach to a [Dandelion++](https://arxiv.org/abs/1805.11060)-based approach.

In summary:

- the well established Tor network can be used to make finding the next validator’s network parameters significantly harder
- still, a custom onion routing solution for the validator/BN network is desirable as a future goal, but requires more R&D
- Tor and Dandelion both add latency; thus compete for the same resource
- the latency added by Tor or Dandelion is feasible
- compared to Dandelion, Tor offers more desirable anonymity properties for roughly the same added latency

Many thanks to @Menduist for suggestions and feedback.

# Privacy/Anonymity Goals

## Unlinkability of Validator ID to IP Address

Validator IDs should not be linkable to the IP address (and peer-ID) of the beacon node they are connected to.

There are two main reasons

1. If an attacker is able to link a validator ID to the corresponding IP address, the attacker can identify proposer chosen for the next slot, learn its IP address, and DoS the corresponding node.
2. protecting the anonymity of validators

The main issue to solve is 1), even though it is not directly related to anonymity.

It is important to solve this issue, because it can actually be exploited and DoS Ethereum operation.

## Future Anonymity Goals

Future goals that are currently out of scope comprise

- hiding participation in the beacon network

# Dandelion Approach

[Dandelion](https://arxiv.org/abs/1701.04439) and its successor [Dandelion++](https://arxiv.org/abs/1805.11060) are mitigation techniques against mass deanonymization. (The first sections of [44/WAKU2-DANDELION](https://rfc.vac.dev/spec/44/) can be used as an overview over Dandelion’s functioning.)

Dandelion has been investigated regarding its potential as a solution for validator anonymity in

[Ethereum consensus layer validator anonymity using Dandelion++ and RLN conclusion](https://ethresear.ch/t/ethereum-consensus-layer-validator-anonymity-using-dandelion-and-rln-conclusion/12698).

The conclusion of this analysis is that Dandelion is not a feasible solution.

Even though the latency added by Dandelion is lower than first assumed – see my comment on this post – the relatively poor anonymity properties that Dandelion offers still make it too expensive in terms of latency added for the gained anonymity.

Dandelion was designed for Bitcoin (with longer block-times and looser latency-bounds), where the latency cost is no issue and the anonymity gain (even though small) comes basically for free.

Further research analysing the relatively small anonymity gain: [On the Anonymity of Peer-To-Peer Network Anonymity Schemes Used by Cryptocurrencies](https://arxiv.org/pdf/2201.11860.pdf).

Dandelion is a *message spreading method*, which increases the uncertainty of an attacker when trying to link messages to senders.

Unlike Tor, it does not guarantee unlinkability in a relatively strong attacker model.

## Expected Latency cost

The expected added latency for Dandelion stem is ~500ms (assuming 100ms average latency between nodes and 5 hops on average).

For now, we ignore an optional random delay added on each fluff hop.

## Issues

Since in stem phase, Dandelion messages are sent to a single peer, resilience is significantly worse than plain gossipsub (which has a recommended mesh out-degree of 8).

This requires a fail-safe, where sending nodes store a message and re-send it if they don’t receive it via gossipsub after a random time in the range of the expected latency.

This adds to the expected latency.

The main issue with Dandelion is that it only provides mitigation and no unlinkability guarantee.

The application to the Beacon network adds to this problem:

messages in the beacon network are inherently linkable to validators IDs.

This allows attackers to link messages to specific sources, where only the network parameters (IP address, peer-ID, …) are unknown.

Such an attacker is much stronger than the attacker model the Dandelion papers use,

which breaks the anonymity guarantees of Dandelion.

An attacker can (try to) connect to peers (sending graft) from which he receives messages originated by a specific validator.

Dandelion will make this process longer and more prone to failures compared to plain gossipsub,

but eventually an attacker can detect the network parameters of the originator.

# Tor Approach

The following gives an overview over a potential Tor-based approach to validator anonymity.

## Prerequisites

The proposed Tor-based approach requires a way of allowing validator/BNs to push messages to one (or more) beacon node(s) over Tor circuit(s).

We propose tor-push, which allows message originators to push messages over Tor to gossipsub peers.

Tor-push uses the same protocol ID as gossipsub, which makes it fully backwards compatible.

Messages sent via tor-push are sent via a separate libp2p tor-switch, which forwards messages over Tor. (This requires [SOCKS5 support for libp2p](https://github.com/status-im/nim-libp2p/issues/358).)

Tor and non-tor switches must never be mixed; attackers must not be able to link these two switches.

Non-tor switches must not be used as a fail-safe for tor-push messages.

The tor-switch

- is not subscribed to any pubsub topic;
- only sends messages the validator/BNs originates, while the non-tor switch handles the typical gossipsub tasks;
- connects to a separate set of peers (via Tor), randomly chosen via a discovery method (discv5).

## Functioning

Beacon nodes receiving a tor-push message relay this message via gossipsub.

Since tor-push messages are typical gossipsub messages,

every BN can act as such a diffuser node, even if it does not support tor-push itself.

(Because hiding participation is not a goal for now, tor-push is not offered as an onion service.

This saves latency, as the number of hops is only 3, and allows backwards compatibility.)

Validators can either directly send messages they originate via tor-push,

or let the beacon node they are directly connected to (and which is controlled by the same entity) send tor-push messages.

Validator/BNs send messages to `D` (gossipsub mesh out-degree) diffuser beacon nodes.

This keeps resilience at a level similar to gossipsub, and is a significant advantage over Dandelion.

Per default, tor-push connections are kept open for one epoch.

The connection life-time can be adjusted as a trade-off between efficiency and anonymity (further analysis necessary).

Establishing circuits for a given epoch can be done ahead of time (in the preceeding epoch).

Since `D` connections are established, at least some of them are expected to be ready for their respective epoch. Establishing connections ahead of time avoids adding latency to message delivery.

## Issues

The following is a list of known issues (non-comprehensive):

- Malicious guards could identify validator traffic because it features distinct patterns, and correlate it to specific messages

e.g. specific validators send attestations in specific slots
- padding / cover traffic could mitigate this; still needs further investigation

naive solution: each validator that does not attest in a given slot sends a dummy attestation

task: identify all patterns specific to Validator/BN network traffic

similar to [website fingerprinting](https://www.usenix.org/conference/usenixsecurity22/presentation/cherubin), an attacker between the victim node and the Tor network could identify and correlate validator traffic

- also mitigate with padding, cover traffic

Using Tor for hiding validators could incentivise large scale DoS attacks on Tor

- also, cannot check message validity until messages reach a diffuser node, which might be abused for spam
- however, this requires an attacker with lots of resources, which could DoS the current network, too

the discovery mechanism could be abused to link requesting nodes to their Tor connections to discovered nodes

- an attacker that controls both the node that responds to a discovery query, and the node who’s ENR the response contains, can link the requester to a Tor connection that is expected to be opened to the node represented by the returend ENR soon after

the discovery mechanism (e.g. discv5) could be abused to distribute disproportionately many malicious nodes

- e.g. if p% of the nodes in the network are malicious, an attacker could manipulate the discovery to return malicious nodes with 2p% probability
- the discovery mechanism needs to be resilient against this

Even though these are potential attack vectors, the proposed Tor approach makes finding the network parameters (e.g. IP address) of the next validator significantly more difficult.

### Further Issues + Solutions

The Tor approach requires validator/BNs to setup a tor daemon.

The overhead for operators can be significantly reduced by bundling tor with the validator/BN software (cmp. [Tor Browser](https://www.torproject.org/)).

If there are only a few validators/BNs using Tor, attackers can narrow down the senders of Tor messages to the set of BNs that do not originate messages.

This could be ignored, explaining that anonymity guarantees only hold when a certain percentage of BNs support the Tor approach.

Validators who want anonymity guarantees from day one on should have separate sets of network parameters for their non-tor and tor switches, respectively.

For the best protection, the tor-switch and gossipsub switch can be run on separate physical machines.

## Latency

For now, we assume an added latency around 500ms, similar to Dandelion.

[Experimental evaluation of the impact of Tor latency on web browsing](https://witestlab.poly.edu/blog/latency-tor/) can be used as a reference.

(I could work on more analysis of tor latency, if desired.)

Note: Tor has since introduced [congestion control](https://blog.torproject.org/congestion-contrl-047/), further reducing average latency.

Also, the analysis linked above measures RTT not latency.

The effect of broken circuits has to be investigated, but opening `D` connections should mitigate the effect.

As connections are established ahead of time ([see Functioning](#functioning)), connection establishment does not add additional latency to message delivery.

# Dandelion vs Tor-based solution

Advantages of Tor

- offers significantly better anonymity properties
- relatively high resilience; same as gossipsub (same out-degree), while Dandelion has an effective stem out-degree of 1
- easier to deploy (even though Dandelion is relatively easy to deploy, too)
- fully backwards compatible; could be started by a single validator (Dandelion is also incrementally deployable, but needs critical mass to be useful)

Advantages of Dandelion

- can check message validity at each stem hop
- does not rely on an external anonymization network

In our opinion, the main advantage of Tor – offering significantly better anonymity properties – clearly outweighs the advantages of Dandelion.

## Combined Solution

Tor and Dandelion could be combined:

Validator/BNs use tor-push to introduce new messages to the gossipsub network, and diffuser BNs feature Dandelion.

A message first gets routed though Tor and then along a Dandelion stem.

The Dandelion stem would make it more difficult for attacks to link messages to the nodes that received said message via Tor.

While this adds further mitigation against correlation attacks, it seems not enough to justify the added latency.

Current conclusion: adding Dandelion would roughly double the added latency,

and the anonymity added by Dandelion does not seem worth it.

# Integrated Onion-Routing/Encryption Approach

We propose the Tor-based solution as an intermediate solution, while researching the integration of onion routing/encryption into gossipsub.

The main advantages of the Tor-based solution for now is:

it can yield a significant anonymity gain very soon.

Integrating a custom onion routing solution into gossipsub takes much more R&D time.

In the long run, the integrated solution has several advantages:

- avoids having to bundle the tor daemon and depending on an external anonymization network
- allows specific tweaking to better fit the Ethereum beacon network

for instance, it can be aware of the fact that beacon messages follow strict rules

could include spam protection: ZK proof in each onion layer

## Replies

**kaiserd** (2022-11-08):

Thank you very much [@AtHeartEngineer](/u/atheartengineer) for the questions and feedback on Discord.

Here is a slightly edited transcript:

> Does any code exist for this yet?

Not yet. But it should not take too long to implement.

SOCKS5 support for libp2p, which is the main thing to implement, is already on the [nim-libp2p roadmap](https://github.com/status-im/nim-libp2p/issues/777).

I am waiting a bit for feedback/suggestions/opinions before we start implementing.

> So you are proposing setting up a mesh network on tor for message originators to initially propagate messages? and then they will be brought back into the main gossipsub mesh networks?

Originators send messages over Tor to gossipsub nodes.

The proposal does not setup a mesh network on Tor, it rather uses the existing Tor network to anonymously push messages into the existing BN gossipsub network.

And yes,  messages are then propagated within the BN gossipsub network.

(I added a sentence to the original post abstract to make this more explicit.)

> Are you worried about the path construction time per epoch?

This can be mitigated by establishing the connections ahead of time: during a given epoch we establish the connections for the next.

Establishing `D` connections should make sure that enough connections are successful.

We could also decrease the connection refresh rate (but still establish ahead of time).

(I edited the original post clarifying this.)

> Or latency in the tor network?

I don’t expect any issues there:

- generally, the latency added by Tor should not exceed 500 ms on average, which would be fine
- we have several connections, even if some should have high latency, others will propagate faster
- Tor just added congestion control which reduces expected average latency further (studies before May 2022 do not consider this yet)

If the proposed Tor approach is of general interest, I could work on an updated latency study.

> So every BN/validator would run a Tor node as well? I like that idea, but extra work might make the barrier to entry too high.

Every BN/validator who wants to protect itself would run a Tor daemon. Running a Tor node would be optional.

The idea here is bundling a consensus layer client, e.g. nimbus, with Tor so that the overhead on the operator side is minimal; similar to Tor browser, where you just install a Browser that comes with batteries included.

---

**AtHeartEngineer** (2022-11-09):

What about setting up a tor network strictly for the beacon chain and every BN be a tor/onion relay node as well?

If a circuit collapses before a message gets through tor, how would the validator know their message never made it out? Would it just be a missed attestation/block? Is there some attack vector there where a malicious party could spin up a bunch of relay nodes and drop packets? Which for regular tor is just annoying, but for the beacon chain it might actually be an attack vector.

---

**Mikerah** (2022-11-09):

I’ve written about my thoughts on this a few years ago (see my profile for more details and the issues [in this repo](https://github.com/ethresearch/p2p/issues/created_by/Mikerah)). In short, I actually think Tor is not really suitable for this or even a custom onion routing protocol, mainly due to latency concerns. As such, I’ve been mainly looking into approaches that use user coordination (e.g. dicemix) or relays (e.g. Organ) as these approaches offer the best set of tradeoffs given the unique needs of the Ethereum consensus layer p2p system.

---

**kaiserd** (2022-11-10):

[@AtHeartEngineer](/u/atheartengineer)

> What about setting up a tor network strictly for the beacon chain and every BN be a tor/onion relay node as well?

Using the existing Tor network would make deployment much quicker, and more stable.

> If a circuit collapses before a message gets through tor, how would the
> validator know their message never made it out?

The validator does not get feedback in case a single circuit fails.

It is very unlikely that all `D = 8` circuits fail.

If an implementation wants to react in that case, a fail-safe similar to Dandelion’s fail-safe can be used:

store sent messages and check if they are received via gossipsub after the expected latency (+ random buffer) time has passed.

> Would it just be a missed attestation/block?

Only if all circuits would fail.

> Is there some attack vector there where a malicious party
> could spin up a bunch of relay nodes and drop packets? Which for regular tor is
> just annoying, but for the beacon chain it might actually be an attack vector.

When using the existing Tor network (as the proposal does),

this attack is possible, but costs significant resources.

You would have to DoS the Tor network.

Using Tor for anonymization of validators can incentivise such attacks though (see OP).

Using a Tor fork, this attack would be easier, especially in the roll-out phase,

because an attacker would have to compete against significantly less honest nodes.

---

**kaiserd** (2022-11-10):

[@Mikerah](/u/mikerah)

> I actually think Tor is not really suitable for this or even a custom onion routing protocol, mainly due to latency concerns.

According to [Tor performance metrics](https://metrics.torproject.org/onionperf-latencies.html), Tor latency should not be a problem.

Also see [this post](https://witestlab.poly.edu/blog/latency-tor/).

Citing from a comment above and the OP:

- generally, the latency added by Tor should not exceed 500 ms on average, which would be fine
- we have several connections, even if some should have high latency, others will propagate faster
- Tor just added congestion control which reduces expected average latency further (studies before May 2022 do not consider this yet)

Do you have studies that show otherwise?

What other issues to you see with Tor?

---

**AtHeartEngineer** (2022-11-10):

Those latencies aren’t bad, and for broadcasting messages/udp, the tor connection will still be over TCP, but we really only care about the “upload” side and not the response since the response will just be some form of “ack/message received and forwarded to the beacon-chain.”

---

**Mikerah** (2022-11-12):

[@kaiserd](/u/kaiserd) Thanks for the reply.

I still think 500 ms is quite a lot especially when you consider the incentives of eth2 validators as a whole. For most validators, the pros of privacy at this level don’t outweigh their gains when participating in systems like MEV-boost and how cutthroat the environment is for signing/attesting blocks and sending across the network as quickly as possible. Many validators have invested a lot into that infra.

As for other concerns for using Tor is the fact that Tor traffic is blocked in a lot of places. Set aside the usual culprits e.g. rogue governments, many relatively innocent (not sure if this is a good term ![:person_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/person_shrugging.png?v=12)) block Tor traffic for a variety of reasons. For example, universities might block Tor traffic. Further, there are metadata concerns with using Tor as well that people here don’t take into account. If you are the only entity within a specific area using Tor then your traffic sticks out like a sore thumb effectively getting us back to square one.

I have some more thoughts that I should write up as I’ve been thinking about this problem for a few years now but these were the most obvious ones.

---

**kaiserd** (2022-11-16):

[@Mikerah](/u/mikerah) Thank you for the reply.

> I still think 500 ms is quite a lot

How much latency overhead would you consider as tolerable?

It is comparable in added latency to other solutions like the Dandelion solution.

For the latency cost, the Tor solution offers good anonymity properties and is easy-to-deploy.

I assume the current expected latency is lower than 500ms.

I’d proceed with further latency testing and a test implementation if there are no apparent issues making the Tor solution infeasible.

I am waiting for more comments :).

> For most validators, the pros of privacy at this level don’t outweigh their gains when participating in systems like MEV-boost and how cutthroat the environment is for signing/attesting blocks and sending across the network as quickly as possible.

Agreed. But this Tor extension would not have to be used by all validators.

It would be optional, and would make linking a validator’s network parameters significantly harder.

Also, could [proposer/builder separation](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725) mitigate this pressure for validators?

> As for other concerns for using Tor is the fact that Tor traffic is blocked in a lot of places. Set aside the usual culprits e.g. rogue governments, many relatively innocent (not sure if this is a good term ￼) block Tor traffic for a variety of reasons. For example, universities might block Tor traffic.

Good point. But the Tor approach would be optional. If it is feasible at the validator’s location, it can be used.

I agree, we need further research to get to solutions that cover these validators as well.

But for now, Tor would be an easy-to-deploy solution.

It would be interesting to investigate, what percentage of validators could not feasibly use Tor.

> Further, there are metadata concerns with using Tor as well that people here don’t take into account. If you are the only entity within a specific area using Tor then your traffic sticks out like a sore thumb effectively getting us back to square one.

I see guard fingerprinting as well as exit fingerprinting as potential related attacks (see OP).

Simply knowing that someone uses Tor within a given network segment allows censorship, but not yet correlating or fingerprinting (it helps enabling such attacks, but is not sufficient yet).

Imo, this does not bring us back to square one.

Yes, there are weaknesses of the Tor approach. But, imo, non of these make it infeasible or not worth the effort of rolling it out in a testnet;

it is a significant improvement over the status quo that is worth to further investigate and/or test.

> I have some more thoughts that I should write up as I’ve been thinking about this problem for a few years now.

That would be very helpful :).

---

**kaiserd** (2022-12-02):

Here is our first raw spec of gossipsub Tor Push: [46/GOSSIPSUB-TOR-PUSH | Vac RFC](https://rfc.vac.dev/spec/46/)

A PoC will follow soon.

