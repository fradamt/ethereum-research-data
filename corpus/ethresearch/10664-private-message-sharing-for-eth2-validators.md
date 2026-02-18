---
source: ethresearch
topic_id: 10664
title: Private message sharing for ETH2 validators
author: blagoj
date: "2021-09-09"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/private-message-sharing-for-eth2-validators/10664
views: 4104
likes: 14
posts_count: 14
---

# Private message sharing for ETH2 validators

### Authors and attributions

Blagoj and [Barry WhiteHat](https://ethresear.ch/u/barrywhitehat).

[Onur](https://github.com/kilic) implemented the RLN construct.

Thanks to Thore for reviewing and suggestions.

# Introduction

Currently validators in the ETH2 network are public and although their IP addresses are not explicitly known, it is easy to obtain with metadata analysis.

Intorducing a private p2p network in ETH2 would lead to massive DoS attacks against validators. Because in private p2p networks it’s not clear who to block in response to spam. In transparent p2p networks, IP based blocking is enough to mitigate most spam attacks.

RLN (Rate limiting nullfier) is a construct based on zero-knowledge proofs that allows for private p2p networks that are spam resistant.

In RLN users sign up with public key. Every message they send also reveals a small portion of their private key. If they send too many messages per epoch their private key is revealed. At the end of every epoch their private key shares are updated.

You can read more about RLN [here](https://medium.com/privacy-scaling-explorations/rate-limiting-nullifier-a-spam-protection-mechanism-for-anonymous-environments-bbe4006a57d).

# Description

This messaging service imlements the [gossipsub-rln](https://hackmd.io/@blagoj/ryBi0HTWK) protocol for the p2p pubsub networking layer, and is separate from the gossipsub-v1.1 pubsub protocol that ETH2 validator clients use for consensus message propagation.

The ETH2 validators will have two connections for two different pubsub protocols, one for the default gossipsub v1.1 for consensus message propagation and one for gossipsub-rln for the private messaging.

The private message channel should use the same underlying discovery service ([discv5](https://github.com/ethereum/eth2.0-specs/blob/dev/specs/phase0/p2p-interface.md#the-discovery-domain-discv5)) as the consensus message propagation service (the native gossip domain) as it provides additional security (we can add add additional key:value pairs for the [ENR](https://eips.ethereum.org/EIPS/eip-778) for extra security and validation, if we need to).

Using gossipsub-rln will also enable spam/DDoS protection for the private messaging channel.

### Rationale

The implementation consist of three parts:

- Smart contract which serves as a registry, and is only used for storage and data availability (i.e LazyLedger approach)
- Private, spam resistant PubSub protocol on a p2p network - gossipsub-rln, which is used for private message propagation part between the validators of the RLN group.
- REST API with a single endpoint which provides list of removed members private keys - used for correctly reconstructing the membership trees of the later joining participants

The blockchain serves only as a data availability layer. It is only used to register an account. Each registeration contains:

1. A signature from ETH2 validator
2. RLN public key

The nodes watch this smart contract, for each validator who signs up, they check:

1. The BLS signature is correct
2. The user has not already signed up
3. If so they insert them into the RLN group.

If a user is spamming, their private key can be revealed. This is gossiped to other peers who remove the spammer from their local membership tree.

## Conclusion

Here we proposed a private ETH2 p2p layer that allows for both privacy and spam resistance. It requires on chain interaction only for registration which means its scalable.

One possible concern is having to come to conesnsus on slashed users.

### Implementation draft

We provide implementation draft for this idea, which can be found here: https://hackmd.io/@blagoj/ryGyO8C-Y

## Replies

**hwwhww** (2021-09-10):

Great work!

> The ETH2 validators will have two connections for two different pubsub protocols, one for the default gossipsub v1.1 for consensus message propagation and one for gossipsub-rln for the private messaging.

Is the plan that we start with simple private message sharing, and eventually we can move consensus message propagation to gossipsub-rln?

---

**blagoj** (2021-09-11):

Hopefully yes in the long term, a good implementation of gossipsub-rln can potentially improve the current consensus message propagation protocol.

---

**barryWhiteHat** (2021-09-13):

I was thinking to have the RLN p2p layer be a kind of p2p attack failsafe.

So the idea would be to also broadcast the minimal messages that you need to to come to consensus here. So that if there is an attack on the p2p network with some kind of huge bot net the network can keep coming to consensus.

---

**nusrettas** (2021-09-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/blagoj/48/5900_2.png) blagoj:

> One possible concern is having to come to conesnsus on slashed users.

Would it be possible to reach a consensus on the slashed users via the blockchain that was used by the nodes to register their accounts? For instance, private keys revealed and published on-chain can be slashed.

---

**hwwhww** (2021-09-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/blagoj/48/5900_2.png) blagoj:

> Hopefully yes in the long term, a good implementation of gossipsub-rln can potentially improve the current consensus message propagation protocol.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> also broadcast the minimal messages that you need to to come to consensus here.

Right, I think we need more pull factors like this for enough validators to join the RLN group and establish a private messaging service. Unless there are some killer application use cases, I’d think about the use cases of broadcasting consensus objects rather than random messages.

> spam_msg_threshold

1. Note that Altair HF will introduce the “sync committee”. The sync committee members have to produce signatures and messages for each slot during the period. → At least 32 sync committee messages for a selected validator per epoch. Lacking these messages won’t cause a liveness issue, but the validators would get fewer rewards, and light clients need these messages for syncing.
2. Each validator has to attest at 1 slot per epoch. Also, they might be selected as an aggregator to aggregate the attestations. The worst case is 32 messages, but probabilistic it’s unlikely that high.
3. There are also protocol-selected sync committee message aggregators. The worst case is 32 messages too.

So we may consider setting `spam_msg_threshold` based on the worst case:

- Minimal messages:

? blocks (on mainnet, having 1 block is lucky)
- 1 attestation
- 32 attestation aggregates

Nice-to-have messages

- 32 sync committee messages
- 32 sync committee message aggregates

---

**SCBuergel** (2021-09-14):

Just started reading into RLN - very interesting concept, thanks for sharing!

> Every message they send also reveals a small portion of their private key. If they send too many messages per epoch their private key is revealed

I guess observers of RLN interactions with computational heavy infrastructure (hello miners!) are able to reconstruct the private key already when less than all fragments of the private key have been revealed? Probably not a big issue but it means that the threshold is more of an upper bound where anyone can slash the spammer. Since we don’t know what resources such slashing front-runners have, it might just make it a bit more difficult to reason about an adequate threshold.

---

**blagoj** (2021-09-14):

That would be a possibility, but we can’t do that with the current implementation as there isn’t an onchain support for BLS signature verification (the eth2 validators have BLS keys and they need to create signature upon registration). Also on-chain slashing will complicate the design a bit for this use-case. The concern about the consensus for slashed users is mainly around data availability, but it can be resolved by the validators hosting an additional API providing slashing data, or maybe a single service instead of all of the participants.

---

**blagoj** (2021-09-14):

The private key reconstruction comes from the properties of the [Shamir’s Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing) scheme.

The mathematical properties of the scheme are:

> Knowledge of any k  or more S_{i} pieces makes S easily computable. That is, the complete secret S can be reconstructed from any combination of k pieces of data.
> Knowledge of any k - 1 or fewer S_{i} pieces leaves S completely undetermined, in the sense that the possible values for S seem as likely as with knowledge of 0 pieces. That is, the secret S  cannot be reconstructed with fewer than k pieces.

So there isn’t really a concern from malicious actors with high computational power to reconstruct the secret by “violating the rules” of the scheme.

---

**blagoj** (2021-09-14):

I agree with this,  tweaking the parameters will definitely require some research and effort (probably based on the concrete application.

---

**barryWhiteHat** (2021-09-15):

> Right, I think we need more pull factors like this for enough validators to join the RLN group and establish a private messaging service. Unless there are some killer application use cases, I’d think about the use cases of broadcasting consensus objects rather than random messages.

Maybe I’m lazy but was thinking to have the push factor being a p2p layer that is enabled by default in teh node. So its basically just turned on by default. So no need to try and make it more attractive ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=12)

[@hwwhww](/u/hwwhww) another question that came up is that we need to have some method of validators signing up where other validators can build a group of validators using a differnt public key. We were thinking to use execution layer for this. But want to see if its possible to use grafiti feild to store this ?

---

**hwwhww** (2021-09-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> So its basically just turned on by default.

p2p layer seems good! But in the current design, the validators have to voluntarily registry membership on RLN contract, right?

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> But want to see if its possible to use grafiti feild to store this ?

If you mean the `graffiti` field in beacon block, since the block proposer seats are probabilistically selected, we don’t have a guaranteed shortest waiting time. It could be in days or months.

p.s. Currently, we have ~236k on the mainnet → *expected value* of the proposer time interval is ~33 days.

---

**barryWhiteHat** (2021-09-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> p2p layer seems good! But in the current design, the validators have to voluntarily registry membership on RLN contract, right?

Yes but we could just have that as part of the sign up procedure for new validators cos they alredy have to place stake. So they would automatically join. For already existing validators we would have to figure something out but seems we would already have a bootstrap a small network and others could join if they wanted to. f

Another possibly pull factor is a validator over tor. Or privacy focused validator.

---

**staheri14** (2021-10-21):

We (the Vac team) are also working on a similar project which we have been building over the past year. Here is a more detailed story of our journey for this project [Privacy-preserving p2p economic spam protection in Waku v2](https://vac.dev/rln-relay).

We are developing the waku-rln-relay protocol which provides a spam-protected transport layer by integrating rln into libp2p Gossipsub protocol.

More context: waku is a suite of privacy-preserving, p2p, and modular protocols for resource-restricted devices (that also suit resourceful devices). The 11/WAKU2-RELAY and 17/WAKU-RLN-RELAY are part of this stack. You can find a full list of our RFCs in the following link rfc.vac.dev. The 11/WAKU2-RELAY protocol is the transport layer and is a thin layer on top of libp2p Gossipsub. The 17/WAKU-RLN-RELAY operates on top of 11/WAKU2-RELAY and enables a spam-protected transport layer using rln. You can use 17/WAKU-RLN-RELAY to provide a private and spam-protected messaging system.

The current implementation of 17/WAKU-RLN-RELAY is in Nim (as a side note we utilize the rln lib developed by Onur). Here is the link to the  [17/WAKU-RLN-RELAY](https://rfc.vac.dev/spec/17/) specs (a few updates are on the way!). We would be looking forward to seeing other implementations e.g., one in Rust to make specs stable.

If we could share the same specs that would be great, or we can also work together to upstream this to Gossipsub. Sharing the same specs has another benefit which is it enables using other protocols of Waku, have interop which is useful for resource-restricted devices.

