---
source: ethresearch
topic_id: 8049
title: Eth2 attack via time servers
author: dankrad
date: "2020-09-29"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/eth2-attack-via-time-servers/8049
views: 4149
likes: 16
posts_count: 17
---

# Eth2 attack via time servers

**TL;DR:** Time server attacks on Eth2 have been considered in the past. It was so far considered that the attack vector would only be able to knock validators offline temporarily, until correct clock synchronization is restored by the node operator. However, a bigger danger lurks if nodes can be tricked into signing an attestation for a far future epoch: due to surround vote slashing, they would not be able to sign any attestation until the time of the future attestation target. For the purposes of consensus, this knocks them out almost permanently, and will be costly for the staker due to inactivity leaks.

# Attack vector

Attestations in Eth2 are a signature on a source and a target checkpoint, each consisting of an epoch number and a block root. The safety of the Casper FFG consensus is ensured by the “no surround vote” rule: No validator should ever sign two attestations where the `attestation1.source < attestation2.source` and `attestation2.target < attestation1.source`.  [1]

We can craft an NTP attack as follows: The first step is to set the attacked validators time to the far future, by manipulating the time of the NTP server to be in the future, for example 15-20 days (it needs to be less than the time of the inactivity leak drawing balances to zero, otherwise the validator will not sign attestations).

Then we need to trick the corresponding node to think that it is synced with the chain so that it will sign attestations. This should always be possible if the attacker controls some of the peers, which is so easy to achieve that it can always be assumed, by sending some attestations and blocks from the future time on the P2P channels.

Once the validator has signed an attestation for the future epoch, the attacker can store this attestation and knows that this validator cannot sign any attestation for the current chain until that future epoch kicks in, otherwise it can be slashed immediately. The Validator Client node of all current Eth2 implementations will actually prevent it from ever signing a conflicting attestation, thus the validator will be effectively offline.

# Result

An attacker can likely knock out all validators it can get control of via an NTP (or similar, e.g. roughtime) attack vector. This attack is worse than previous attacks described using this vector [2], because the result is more permanent: It is likely that an NTP attack will be detected within minutes and almost all nodes with competent operators should be back to normal withing hours. However in this case that won’t help as the damage is already done – and can cause very large financial damage to validators, e.g. if enough validators are knocked out to lead to a quadratic inactivity leak.

# Mitigation

## Add VC no-slash rule

We can add a no-slash rule to Validator Clients that requires them to evaluate the current time before signing anything and not sign any attestations for the future. This only helps if the VC runs on a different node than the BN, and is not affected by the attack. However, it would be a strict improvement in the case of Secret Shared Validators, as it does not allow the leader node to propose a far future attestation and block the validator.

## Add more robustness to time synchronization

This issue highlights that NTP time synchronization is a more serious attack vector than previously thought, and care has to be taken to avoid this.

Small clock skews are annoying but do not cause serious harm. It is thus preferable to only use NTP time updates if they are within a small window of current RTC time (seconds), and otherwise reject them.

This leaves the boot process as an attack window. Note that major power outages do happen and this is still a potentially serious issue that can affect many validators at once. I think it might be a good practice for validator clients to refuse launching (except with an override flag) if the slashing protection database indicates that nothing has been signed for several hours or days, indicating the possibility of an NTP attack.

(Thanks to [@alonmuroch](/u/alonmuroch) for a discussion that led to the discovery of this attack)

[1] https://arxiv.org/abs/1710.09437

[2] [Time attacks and security models](https://ethresear.ch/t/time-attacks-and-security-models/6936)

## Replies

**alonmuroch** (2020-09-30):

Great summary Dankrad.

Another angle on this attack can be on remote signers like HSM/ KSM services. Those signers might have built in slashing protection but a far into the future signing request will go by un-noticed, resulting in a signature.

If such a wallet will sign a far enough into the future attestation, he will block itself to sign anything else up to that point.

https://github.com/ethereum/eth2.0-specs/issues/2085

---

**dankrad** (2020-09-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> If such a wallet will sign a far enough into the future attestation, he will block itself to sign anything else up to that point.

Yes. If attacking the interface between HSM and BN, this is actually a worse attack vector as you can go far further in the future and thus make the validator completely unusable.

---

**edmundedgar** (2020-10-01):

There’s a distributed timestamping system called Bitcoin which, although not generally very useful, has the property of producing very expensive-to-forge timestamps that can be easily verified by a computer. It seems likely that it will keep running for at least the next couple of years.

It might be fun to use that to make a little script that you could run either on boot, to sanity-check your system time, or as a wrapper around a code that starts up your Eth2 validator.

---

**alonmuroch** (2020-10-01):

It has nothing to do with the issue depicted above…

---

**dankrad** (2020-10-01):

The only way in which you could make use of this is by checking that the Bitcoin head is in sync with your current system time. It is basically another online/connected check, which can be circumvented by an attacker who has the ability to also forge some Bitcoin blocks.

I actually agree that since it is very expensive to fake, there may be some value in it: If we are willing to bet on Bitcoin being around for a while, which I agree we can, and not having massive security failures, then we could build a sanity checker into the NTP protocol based on this. I don’t think it’s completely outrageous.

---

**alonmuroch** (2020-10-03):

It adds more complexity on the wallet side which is complex enough with slashing protection. Wallets today are very light weight, we might not like it is what it is.

---

**arnetheduck** (2020-10-05):

This is an interesting topic, because while in theory it’s possible that one might have to vote for a block that is several weeks old, in practice this should never happen - if you’re online and in sync, a configurable horizon for slot distance seems like a mitigation - just like in eth1, there exists no theoretical limit for reorg depth, but clients in practice limit it (and keep a configurable option for when it would make sense to flaunt the limit).

By extension, “some blocks and attestations with a far away timestamp” should also “never” happen on any reasonably working network.

There are several DoS attacks lurking around here as well: to pull off such an attack, one would presumably have to skip lots of slots (or control a significant amount of the block producers) - such empty slot processing is costly, thus it makes some sense for clients to put bounds on how much processing a client has to do, for example before processing an attestation at all. This is something of an open question - there exist some fixed upper bounds, such as the mentioned time it takes for the validator to be taken offline by the inactivity leak - processing more slots than so would render the chain unusable anyway.

---

**dankrad** (2020-10-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/arnetheduck/48/1453_2.png) arnetheduck:

> This is an interesting topic, because while in theory it’s possible that one might have to vote for a block that is several weeks old, in practice this should never happen

You will never vote for an old block in this attack. It is only the FFG source that is old, and this source can be old for many reasons, for example if the network did not justify for several weeks, which can definitely happen in real life, so we don’t want to block it.

![](https://ethresear.ch/user_avatar/ethresear.ch/arnetheduck/48/1453_2.png) arnetheduck:

> There are several DoS attacks lurking around here as well: to pull off such an attack, one would presumably have to skip lots of slots (or control a significant amount of the block producers) - such empty slot processing is costly

It is still much less than processing all the slots with blocks. And clients will have to be able to catch up on this in practice in case they are offline.

---

**alonmuroch** (2020-10-05):

It doesn’t solve the case where a remote signer wants to use a trustless infra provider.

I think, from a UX POV, a user shouldn’t be forced to only use a trusted node connection. It will make life difficult.

If you include a simple time test on the signer, as part of a slashing protection scheme, you can avoid it all together.

---

**SentientFlesh** (2020-10-14):

We still have a performance bottleneck in Bitcoin’s ~10 minute block time to contend with. While I agree that Bitcoin isn’t going anywhere for the foreseeable future, I feel like this would be a last-resort time check as it not only requires validation of the longest chain, but unless being checked immediately after a new block is mined, also requires a *relatively* long wait period.

---

**SentientFlesh** (2020-10-15):

Coming in fresh to ETH2 discussion, can someone post a relevant link to the logic controlling the clocks?

I would be interested to see if the Bully Algorithm could be implemented here, where notes are pinging each other, checking timestamps against local, and if enough other nodes find a node with an invalid time signature, they are temporarily “bullied” out of consensus without negatively affecting the integrity or standing of the node itself. Additionally, a function could be called for the affected node to have it’s time updated by all of the nodes which bullied it off the network for N minutes.

*IF* we can determine that X number of nodes have been running correctly, they can act as validators in the sense of timestamp checking without having to rely on oracles or any off-chain data. This also makes we wonder if it would be beneficial to have nodes “integrity check” each other periodically, or `onBroadcast`… will flesh this idea out more and come back to it.

This would let node operators to ensure they’re running correctly without penalizing them, almost instantly remove a compromised node, and allow the compromised node to re-sync with the valid data from the other nodes within one block’s time assuming it had enough peers.

Likely there will need to be checks to see if the node intentionally is running bad times in order to attack the network, but it’s a starting place.

---

**SentientFlesh** (2020-10-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> If you include a simple time test on the signer, as part of a slashing protection scheme, you can avoid it all together.

Would this not be making the assumption that the signer’s local time is up to date? If the node is already tricked into thinking it’s synced, any time test would be invalid.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> It is still much less than processing all the slots with blocks. And clients will have to be able to catch up on this in practice in case they are offline.

Why allow empty slot processing at all? It can be used for a number of attacks, provides no new information to the network, and the resources could be allocated elsewhere. Seems that by even allowing empty slots to preserve block-time is diverting system resources and leaving a target wide open.

---

**alonmuroch** (2020-10-15):

@SentientFleshI think there are 2 attack vectors here. The one I’ve mentioned is a remote signer with slashing protection. That remote signer Is getting attestation data to sign, checks it’s not slashable and the signs it.

Currently today, all implementations do not consider a scenario that the remote signer gets a signing request for a far into the future attestation. Currently it will sign it, essentially blocking itself from signing any other attestation until that future one.

Under this attack, its internal clock is correct.

---

**dankrad** (2020-10-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/sentientflesh/48/4756_2.png) SentientFlesh:

> Why allow empty slot processing at all? It can be used for a number of attacks, provides no new information to the network, and the resources could be allocated elsewhere. Seems that by even allowing empty slots to preserve block-time is diverting system resources and leaving a target wide open.

Well if you don’t allow empty slots, your algorithm will stall if even one validator is offline, so clearly this is not an option.

![](https://ethresear.ch/user_avatar/ethresear.ch/sentientflesh/48/4756_2.png) SentientFlesh:

> I would be interested to see if the Bully Algorithm could be implemented here, where notes are pinging each other, checking timestamps against local, and if enough other nodes find a node with an invalid time signature, they are temporarily “bullied” out of consensus without negatively affecting the integrity or standing of the node itself. Additionally, a function could be called for the affected node to have it’s time updated by all of the nodes which bullied it off the network for N minutes.

This is not a fix for this attack, because the attack is against the node that has the incorrect time. The node is not attacking the network, it is just knocked offline, so your suggestion of bullying it out of P2P will do nothing.

---

**technocrypto** (2020-10-16):

This is not advocacy, but as a technical note here is a fairly “thin” way to add a simple Bitcoin sanity check:

1. active ETH2 beacon chain nodes use their ETH1 node to pull recent BTC headers from one of the ETH1 contracts which uses them, only aiming to get at least one BTC header with a timestamp every ~200 slots or whatever acceptable threshold you want. They keep the most recent couple BTC headers saved to disk.
2. when an ETH2 node comes back online after a large gap and gets informed by peers that there are significant finality issues it requests a BTC header stamped no more than ~500 slots before the most recent blocks/attestations it is being sent, and uses this as a sanity check on the NTP server time reference. To validate the header it uses a crude rule that the difficulty of the offered block must be at least 5% of the latest stored block it has for a reference, validates it, and then checks the timestamp.  No need to directly connect to the Bitcoin network, which would add huge amounts of code.

If this level of costliness (~$5000 to fake at current prices) isn’t considered high enough the scheme can be modified to be more complicated, but for a $5000 per faked 500 slot window protection this would be pretty thin.  The next level of complexity would be to use either more BTC blocks per check or statistical outliers in difficulty, but this increases the required reliability of the ETH1 contracts consuming BTC headers for the sanity check to work consistently.

Sidenote:  unlike general blockchain clients, isn’t there a fairly strong assumption that validators are actively monitored by humans?  Why not just stall and directly sanity check time with the user if the node is getting told that it’s been offline for a long time? Won’t this solve 99% of the actual expected scenarios where validators would be vulnerable?

---

**dankrad** (2020-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> Why not just stall and directly sanity check time with the user if the node is getting told that it’s been offline for a long time?

Yes, I think it is a good idea (and probably the easiest solution to implement) to just refuse launching and/or stop when already running if there is a time gap between the current time and the last database entry of some period, probably 4h-24h or so. That would stop this attack in its tracks without making validator maintenance too much harder (hardware sometimes reboots/power outages occur, but more than a few hours should be very rare)

