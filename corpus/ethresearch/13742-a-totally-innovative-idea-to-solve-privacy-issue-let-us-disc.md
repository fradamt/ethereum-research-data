---
source: ethresearch
topic_id: 13742
title: A totally innovative idea to solve privacy issue.Let us discuss the feasibility of this plan
author: VitalikFans
date: "2022-09-22"
category: Privacy
tags: []
url: https://ethresear.ch/t/a-totally-innovative-idea-to-solve-privacy-issue-let-us-discuss-the-feasibility-of-this-plan/13742
views: 4509
likes: 8
posts_count: 14
---

# A totally innovative idea to solve privacy issue.Let us discuss the feasibility of this plan

Establish a new server, which I call it “**Privacy Server**”, this kind of server run automatically and cannot be visited by any operator. That means, no one has access to this server’s code except code.

What’s more important, **any part of code needs to be opensource**. Before code is deployed in Privacy Server, it should be released publicly for a sufficient time gap. And code need to provide unified functions to transfer user’s data.

In this way, Any access to data will be only limited by opensource code. If the code runs without mistake, then everyone’s privacy will be protected properly.

Any comment is weclome.

## Replies

**Pandapip1** (2022-09-22):

Who pays for the electricity costs? This idea has “centralization” written all over it.

Why not just use homomorphic encryption with smart contracts?

---

**cybertelx** (2022-10-02):

How exactly does no one have access to this central server? What stops some big adversary from going and finding it to smash it to bits and shut the whole system down?

---

**Pandapip1** (2022-10-03):

My other question is: why would people be worried about storing encrypted data on the blockchain?  It requires a much lower level of trust than this proposal.

---

**cybertelx** (2022-10-03):

So we’re trusting that whoever is keeping the server won’t just enter. If the software was published as FOSS, we have to somehow be able to verify the code running on the server is the same as the open source software.

Your second proposal, it’s definitely decentralized in “fault tolerance” but is not decentralized in “control”.

Since we’re using homomorphic encryption anyways (not a cryptographer idk what this entails), why not just store the data on something like Sia, IPFS or some blockchain/rollup/etc?

---

**MicahZoltu** (2022-10-04):

I think what you are describing is essentially the same as SGX (from Intel).  The problem is that the hardware manufacturer, and anyone that wrenches them, theoretically has access to the private keys on the processors they produce which means an attacker may have access to the private keys and can spoof execution to the network.

---

**MicahZoltu** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vitalikfans/48/7059_2.png) VitalikFans:

> Hardware manufacturer master the private key, but we can design a system creates the private key randomly.

There is no credible way to prove that you are doing this and you are *not* storing those randomly generated keys somewhere.

![](https://ethresear.ch/user_avatar/ethresear.ch/vitalikfans/48/7059_2.png) VitalikFans:

> And the one who can physically touches the microchip, has the access to the private keys. But we can still find ways to avoid this issue. Simply thinking, adding some sensors to monitor physical touch. If it detected some special exceptions, trigger a private key clear system.

This is a very hard problem, I recommend focusing on fleshing this out a bit more.  While tamperresistant hardware is a thing, it is really hard and expensive to design and build.

---

**Dormage1** (2022-10-05):

If you happen to have such system, just put a simple database on it and be done with it?

You are hitting on many open problems…

---

**cybertelx** (2022-10-05):

Personally I’m not a big fan of TEEs as a solution to privacy, because they are not secure against nation states (they can just ask for a key from Intel/AMD to masquerade as a valid TEE) or the chip manufacturers can do so too.

And about the verifiers bit: What if, after the verifiers do their checking and the livestream ends, the person with access to this server decides to just switch the software, and change it back on the next inspection?

---

**Pandapip1** (2022-10-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vitalikfans/48/7059_2.png) VitalikFans:

> There will be no one having the access to this server after verification is finished.

You can’t trustlessly ensure that this is indeed the case.

---

**cybertelx** (2022-10-06):

> We can ask for microchip manufacturers to add a function that it can recreate the random private key at any time.

The way that you can verify a TEE is valid (at least for Intel SGX) is through Attestations, where the enclave has access to a private key signed by the manufacturer (which is trusted not to go and sign keys for a malicious party) and uses it to attest to a remote user that the Enclave sees that it is running that software as claimed.

If the Enclave is hijacked/the private key is grabbed/any private key signed by Intel for SGX is grabbed outside of the Enclave, it falls apart as that key can attest whatever it wants until it gets revoked by Intel.

> There will be no one having the access to this server after verification is finished. The only way to update code and change software is getting approved by the DAO organization in the blockchain . If the DAO organization want to viciously set up a back door program in the open-source code, it still need a fixed sufficient time to change the code. During this period, stakeholders(included users) can review the code to ensure security. If any back door program is detected, everyone still have time to transfer or delete their own data.

This is what is known as the oracle problem: how can an on-chain entity make sure something happens off-chain? No magical blockchain solution is gonna stop somebody from putting a USB drive into the computer and looking through the data.

> If everything goes well, we can create an Ideal Web3 . It has the same excellent performance as traditional Internet, it can be compatible to any existing software architecture so that current applications will be easy to migrate , and in the meanwhile it can avoid any privacy issue .

The entire Internet running on a couple servers? (which are weak points, if a government decides to go and take them down then they certainly can do so)

> When we can ensure the data is true, the value of data will be enhanced. When we truly give data rights to every person, a new data world will come. We can easily transfer and combine our personal data between different applications to realize our purpose. For example, if you allow, when you buy something in application A, you can immediately get the order information in application B .

Blockchains & ZK proofs

> We can even establish a dispute resolution system just as court, which will greatly reduce the space for corruption and make the society more fair.

[Kleros](https://kleros.io) exists, it is an arbitration protocol built on Ethereum.

> On the furthermore, a poll system based on real identity can be utilized to resolve our traditional election issue.

[Proof of Humanity](https://www.proofofhumanity.id/) + ZK voting system (I believe Vitalik had a blog post about blockchain voting)

---

**VitalikFans** (2022-10-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/pandapip1/48/9697_2.png) Pandapip1:

> You can’t trustlessly ensure that this is indeed the case.

If you want to know more detail, I’m very delighted that you can visit my profile.

---

**lappii** (2024-01-05):

Is this just a guess? Or has it already taken shape? Curious if there really will be such a perfect privacy server

---

**ziyinlox-purple** (2024-01-10):

This idea sounds amazing for protecting privacy,but i think still have some problems:

1. If nobody can visit the server, this might pose challenges for routine maintenance and troubleshooting in emergency situations.
2. And how to confirm the code will run without any mistake? Seems it’s difficult to solve right now, sounds like building castles in the air

