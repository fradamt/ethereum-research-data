---
source: ethresearch
topic_id: 6738
title: Does ECDSA on FPGA solve the scaling problem?
author: leohio
date: "2020-01-08"
category: Layer 2
tags: [security]
url: https://ethresear.ch/t/does-ecdsa-on-fpga-solve-the-scaling-problem/6738
views: 2849
likes: 3
posts_count: 4
---

# Does ECDSA on FPGA solve the scaling problem?

Turing-complete contract execution on L2 is thought to be achieved with TEE like Intel SGX. This seems not to be the best solution simply because this security depends on Intel’s compliance.

This post just requests comments about Trultless Network (Ethereum) × Trusted Machine (FPGA) model and its problems.

# Background

TEE was already a candidate of L2 solution in 2016, as TEEchan was proposed by the team headed by Emin Gun Sierer ,Joshua Lind.

https://arxiv.org/abs/1612.07766LN was focused by the community, because of the reason that Intel should not be the trustpoint.

Ethereum has a different status quo about this topic.

Bitcoin Script is focused on operations of Bticoin like payments and its escrow, and this can be mostly same of LN functions.

EVM operates storages on Ethereum, not focused on operations of Ether, while cryptographical L2 solutions like OVM does not have same functions of EVM.

Intel SGX has almost of all functions of EVM with a verification of the process of executions, though this needs Intel’s hardware level trust.

In Ethereum Community, this kind of ideas are well discussed. [1][2]

And idea about hardware level also appears as a solution about VDF. [1] [3]

# Intel SGX

Intel SGX has encrypted memory “enclave”.[4]

The private key is inside the circuit (e-fuse ,Provisioning Secret) and its public key is registered by Intel.

Verifications of enclave executions can be shown to validator by “Remote Attestation”[5]


      [usenix.org](https://www.usenix.org/system/files/conference/atc17/atc17-tsai.pdf)


    https://www.usenix.org/system/files/conference/atc17/atc17-tsai.pdf

###

3.90 MB








# FPGA

The theme is whether or not the things above can be samely implemented by FPGA and its relevant modules with external key generation / key import . This simply means removing trust of a maker from TEE.

(abandoned: FPGA is a mutable circuit, **thus makers cannot embed backdoors inside it.**)

**If FPGA can principally generate/import key externally with HDL, the maker cannot attack users with stealing the private key** (modified)

If SGX’s performance is not so needed for smart contracts, FPGA’s performance is to a considerable extent.

# ECDSA on FPGA

TEE on FPGA is already well researched.(abandoned: This provides mutable TEE circuit.)

http://www.cs.binghamton.edu/~jelwell1/papers/micro14_evtyushkin.pdf

But it’s hard to find ECDSA on FPGA with certain security and privacy against physical access.

There’s a verify circuit, but not signing.

# Problem

Intel SGX’s verification of keys and executions are provided by Intel. How could we do the same thing with FPGA?

# Reference

[1] see Question for Justin Drake

https://docs.ethhub.io/other/ethereum-2.0-ama/[2] TEE topics

https://ethresear.ch/t/trusted-setup-with-intel-sgx/5531

[3] VDF

https://ethresear.ch/t/verifiable-delay-functions-and-attacks/2365

[4] Good explanation about TEE (it’s in English but only its title is in Japanese )


      [seminar-materials.iijlab.net](https://seminar-materials.iijlab.net/iijlab-seminar/iijlab-seminar-20181120.pdf)


    https://seminar-materials.iijlab.net/iijlab-seminar/iijlab-seminar-20181120.pdf

###

1761.83 KB








[5] Graphene-SGX:


      [usenix.org](https://www.usenix.org/system/files/conference/atc17/atc17-tsai.pdf)


    https://www.usenix.org/system/files/conference/atc17/atc17-tsai.pdf

###

3.90 MB

## Replies

**adlerjohn** (2020-01-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> The theme is whether or not the things above can be samely implemented by FPGA and its relevant modules with external key generation / key import . This simply means removing trust of a maker from TEE.

This shifts the trust to whoever generated the key, and this trust assumption is unavoidable since you need trusted executions to be veritably so. Maybe slightly better than trusting Intel for *everything*, but it’s not a solution to anything.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> FPGA is a mutable circuit, thus makers cannot embed backdoors inside it.

FPGAs are circuits, and can have backdoors built into them.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> TEE on FPGA is already well researched.This provides mutable TEE circuit.
> http://www.cs.binghamton.edu/~jelwell1/papers/micro14_evtyushkin.pdf

The linked paper’s threat model is only untrusted system software. One key component of Intel SGX is hardened hardware to protect against threats that have physical access to the machine ([well yes, but actually no](https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00219.html)). FPGAs provide no such protection.

TL;DR this solves nothing, it just shifts around the trust assumptions to parties that have even less of an incentive to actually make a secure system.

---

**leohio** (2020-01-09):

Thank you for your clear opinion.

Problems are pointed out and became clear.

And I thinks some points are left to discuss. Let’s start from the high priority

TL;DR This post is just a talk about probability of FPGA and scaling. This does not provide any concrete proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> TEE. FPGA is a mutable circuit, thus makers cannot embed backdoors inside it.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> FPGAs are circuits, and can have backdoors built into them.

If this assumption is meaningless, maybe the subject should be closed.

I will paraphrase this sentence.

“**If FPGA can principally generate/import key externally with HDL, the maker cannot attack users with stealing the private key**”

I should have talked clearly about this case, becasuse if Intel wants to attack SGX users they just steal the secret key in e-fuse. Building backdoors in circuit is too obvious and too technically expensive to do crime. (I don’t expect Intel to attack users off course, it’s just a imaginal case)

Makers of FPGA are thought to be same as well.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> This shifts the trust to whoever generated the key, and this trust assumption is unavoidable since you need trusted executions to be veritably so. Maybe slightly better have trusting Intel for everything , but it’s not a solution to anything.

I think no one should generate the key as a smart contract executor. The writer of HDL give the circuit a part of a secret, and with another part of a secret inside the circuit, the private key should be generated.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> One key component of Intel SGX is hardened hardware to protect against threats that have physical access to the machine

Yes, this is the biggest problem of FPGA circuit. If any physical access, the key should be broken. I have no idea about this part.

In the link

http://www.cs.binghamton.edu/~jelwell1/papers/micro14_evtyushkin.pdf

“”“Second, if the

proposed architecture is deployed in a cloud environment,

then it is reasonable to assume that a cloud operator will

offer physical security of the system to protect its reputation.”“”

Seems does not work against physical attacks.

---

**wanghs09** (2020-01-10):

> I should have talked clearly about this case, becasuse if Intel wants to attack SGX users they just steal the secret key in e-fuse.

There are some technology such as physical unclonable function, which makes it harder to steal the secret, though not impossible.

FPGA should not be taken into consideration, because it’s just not provable to others that you actually run your program on a well configured FPGA as required. FPGA can be thought as equivalent to some kind of software, just faster.

In [2], I meant that we could just trust SGX rather than some random people for once, so that it’s not necessary to trust the people every time a new circuit is built.

