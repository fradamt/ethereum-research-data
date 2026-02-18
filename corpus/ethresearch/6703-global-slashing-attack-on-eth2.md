---
source: ethresearch
topic_id: 6703
title: Global slashing attack on ETH2
author: kladkogex
date: "2019-12-29"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/global-slashing-attack-on-eth2/6703
views: 2533
likes: 1
posts_count: 9
---

# Global slashing attack on ETH2

Here is a pretty scary attack one can do on ETH2 (or any other proof of stake PoS network)

An opensource developer can include a malicious piece into code of geth (or openssl or another part of the Linux stack) that intentionally creates a double sign transaction. The same can be done by an employee of a major cloud provider such as AWS.

Then the malicious code could be used to create a double sign evidence for ALL staked funds on all or a significant portion of nodes.  The attacker could then either kill the entire network by submitting the evidence, or use the evidence for blackmail.

Note that the malicious code can be anywhere starting from Linux drivers and ending with the microcode executed by the CPU, so diversity of clients such as geth vs parity wont really help much.

## Replies

**dankrad** (2019-12-29):

It is possible to mitigate against this:

1. Validator maintainers can have a second “no-slash” device that checks all outgoing messages from their validator. If that device is logically independent, it would not be susceptible to the same attack
2. Validators can be run secret-shared as an MPC

In each of the situations you described, the attacker would also be in a position to exfiltrate the validator key. It is well known that PoS will have much stricter requirements on keeping this secret, so I’m not sure this is a new attack. The security requirements for running a validator are certainly higher than we are currently used to.

---

**kladkogex** (2019-12-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Validator maintainers can have a second “no-slash” device that checks all outgoing messages from their validator. If that device is logically independent, it would not be susceptible to the same attack

This is actually not easy to do since the messages will be encrypted and sent through a covert channel. They do not have to be sent through a normal protocol.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> In each of the situations you described, the attacker would also be in a position to exfiltrate the validator key.

Not really true either … You need just need to have access to a device that signs, not the key itself. In most cases you wont be able to extract the key

---

**vbuterin** (2019-12-29):

How is this different from inserting a malicious piece of code that steals people’s private keys for non-signing wallets?

---

**kladkogex** (2019-12-29):

The difference is that you do not need private keys.  You only need to be able to sign.

Many many validators set up a signing centralized server connected to nodes over a network. Note that the signing server needs to be always on and that one can not require human confirmation for signatures.  You can not have a guy that constantly pushes the yes button.

The point that I wanted to make though, is that slashing does encourage some types of attacks, that would not be attractive if it did not exist.

---

**dankrad** (2019-12-29):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The difference is that you do not need private keys. You only need to be able to sign.

I can see a difference in attack target here. Nevertheless, the assumption that you gain such deep access on so many systems is pretty strong.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The attacker could then either kill the entire network by submitting the evidence, or use the evidence for blackmail.

I think blackmailing would be difficult – in order to provide enough evidence that you can perform the attack, you would probably also provide enough evidence to fix it.

Killing it would probably be undone by human intervention in most cases. I think if you had such an attack vector it would probably be best used for a real attack on the system (e.g. double spending attack).

---

**kladkogex** (2019-12-30):

[quote=“dankrad, post:6, topic:6703”]

I can see a difference in attack target here. Nevertheless, the assumption that you gain such deep access on so many systems is pretty strong.

Well, if there is a Linux vulnerability, you can get access to zillions servers at the same time.  People do it constantly.

Double spend is actually much much harder to do …

---

**jgm** (2019-12-30):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Well, if there is a Linux vulnerability, you can get access to zillions servers at the same time. People do it constantly.

Hyperbole aside, there is a big difference between people installing servers from a stock image and leaving them wide open, and installing servers properly such that they have a minimal attack surface.  Education and staking services can significantly reduce this risk (as will diversification of operating systems on which validators run, physical locations of validating servers, multiple beacon chain implementations *etc.*)

---

**kladkogex** (2019-12-30):

Totally agree!  thats why ETH2 needs to invest into an awareness campaign for validators running ETH2 nodes.

From talking to validators, the most vulnerable point seems to be nodes -> HSM connection, since many validators plan to run nodes on AWS, and HSMs in their datacenters, so if one compromises the node->HSM connection, one can do a double sign …

