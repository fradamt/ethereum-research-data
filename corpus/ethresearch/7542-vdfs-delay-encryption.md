---
source: ethresearch
topic_id: 7542
title: "VDFs: Delay Encryption"
author: burdges
date: "2020-06-16"
category: Cryptography
tags: [verifiable-delay-functions]
url: https://ethresear.ch/t/vdfs-delay-encryption/7542
views: 4269
likes: 6
posts_count: 13
---

# VDFs: Delay Encryption

Luca de Feo and I wrote up a discussion of isogenies VDFs in https://eprint.iacr.org/2020/638

One almost never builds protocols using time-lock puzzles because time-lock puzzles encode only one participant’s contribution, making individual puzzles almost worthless.  And time-lock puzzles are expensive of course.

We observe that arbitrarily many participants can encrypt messages to the result of one isogeny VDF run.  It’s basically IBE with the VDF being the private key generator.  This radically simplifies advanced voting schemes.

We’ve one big caveat that you cannot end and restart the isogeny sequence repeatedly, like an isogeny VDF should normally do.  As a result, delay encryption requires terabytes of VDF parameters, where an isogeny VDF alone admits a flexible parameters size.  It’s extremely expensive equip delay encryption evaluators with several terabytes RAM of course, but one might reduce this with enough SSDs in parallel.

Isogeny VDFs require a trusted setup, but a painless one, nothing like the RSA nastiness.  You generate the VDF parameters after the trusted setup, so the trusted setup itself remains tiny.

I’d hoped the large VDF parameters might yield memory bandwidth hardness.  I’m afraid this appears far from applicable, but one might achieve some limited memory bandwidth hardness for commodity CPUs with a 20x improvement in isogeny evaluation time from the theory side.  I still suspect isogenies VDFs can provide higher confidence than other VDF designs, but they require more work and look more expensive per evaluator.

We did not explore if/when physics might impose limits upon piping in those isogeny parameters.  We did not explore if residue number systems for known fixed fields yields higher confidence in VDF performance than residue number systems for RSA moduli or class groups.  Isogenies VDFs have interesting variants that merge isogeny sequence with multiple start times, which we did not explore either.

## Replies

**HAOYUatHZ** (2020-06-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> This radically simplifies advanced voting schemes.

in this scenario, you can also turn it into delay-authentication?

---

**SebastianElvis** (2020-06-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/haoyuathz/48/4618_2.png) HAOYUatHZ:

> in this scenario, you can also turn it into delay-authentication?

The one you refer to is called Timed Signatures https://eprint.iacr.org/2019/644.pdf

---

**burdges** (2020-06-16):

You should view delay encryption as “encryption adapted to smart contracts”.  If you can organize all smart contract participants into starting the contract within some narrow time window, then after some substantial delay everyone learns what everyone else encrypted.  It gives you handy protocols for Vicary auctions and many voting schemes.

---

All VDFs come with some substantial adversarial advantage, like 100+ fold, so they cannot literally provide a clock all by themselves.  You need some network synchronization too.

You cannot avoid this because adversaries can always speed up their hardware.  Asymptotically, we know residue number systems always speed up computation https://twitter.com/hashbreaker/status/1131192651338829825 thanks to DJB, although realizing such gains on GPUs proved difficult.

In practice, you could gain 10x by using a superconducting computer.  On page 17 of https://www.nitrd.gov/pubs/nsa/sta.pdf you’ll find the NSA claiming in 2005 that by 2010 they should be able to produce “An RSFQ processor of approximately 1-million gate complexity, operating at a 50 GHz clock rate.”  On page 120 of http://www.cse.nd.edu/Reports/2008/TR-2008-13.pdf you’ll find projections of 250 GHz being possible “post 2010”.  If achieved, that’s already a 100x improvement over anything doable with commodity hardware, and one adversary may already possesses this hardware.

Assuming you accept a 100+ fold adversarial advantage in your protocol then…

You could do Schnorr signatures on intermediate curves of the VDF run, but using the VDF value there for the base point.  In this way, nobody can compute or verify the signature until that base point gets found.

You might do BLS signatures to prove the signer waited some amount of time while doing the signature, but this requires the signer be an evaluator.  We dislike that because it abandons the VDF energy advantage.

I’ll note however that [Fantômette](https://arxiv.org/pdf/1805.06786.pdf) is a blockchain protocol in which all nodes run VDFs.  It thus abandons our VDF energy advantages, but maybe similar protocols could side step the adversarial VDF advantage.

---

**gokulsan** (2020-06-17):

Great concept. Nice to see this approach to apply Super Singular Isogeny based VDF for encryption. This could help us to introduce an encrypted physical source and encrypted device identity in the smart contracts. In this context, is it possible to construct Lattice cryptography based VDFs which would be more memory efficient than Isogeny based VDFs ? Please advise me if this idea is very naive or irrelevant ! I have seen Random Linear Code based on Lattices in the following research - [Lattices, Learning with Errors, Random Linear Codes](https://dl.acm.org/doi/pdf/10.1145/1060590.1060603)

---

**JustinDrake** (2020-06-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> delay encryption requires terabytes of VDF parameters

Can you expand on the calculation here? If someone built a commodity ASIC evaluator that sped up the VDF evaluator by a factor of 10x would delay encryption then require tens of terabytes?

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> they require more work

Is the Web3 Foundation interested in doing this R&D work? To your knowledge, is anyone intending to use an isogeny-based VDF or delay encryption in production?

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> Asymptotically, we know residue number systems always speed up computation x.com thanks to DJB

This seems to be a common misconception. DJB’s construction was analysed by [@dankrad](/u/dankrad) and the conclusion is that the asymptotic speedup is at best misleading, if not plain wrong. The model of computation in DJB’s analysis does not capture the physics of our world. Indeed, DJB looks at circuit depth alone when instead real-world circuit latency comes from both circuit depth *and* wire length.

My understanding of Dankrad’s analysis is that the asymptotic growth in the number of transistors required to implement DJB’s circuit is extremely unfavourable. The growth is so bad that even perfectly packing transistors in a 3D ball (which itself is unrealistic since ASICs are 2D) the radius of that ball grows significantly faster than the circuit depth. Since the speed of light is finite, latency from wire length in DJB’s construction dominates asymptotically over latency from circuit depth. In fact, the asymptotics of DJB’s construction are significantly worse than simple log-depth repeated squaring. ([@dankrad](/u/dankrad) is that a fair summary?)

Putting asymptotics aside and focusing on the constants, it is possible that DJB’s construction is faster than simple log-depth repeated squaring for small instances. This was also investigated, and it seems that DJB’s construction is concretely slower for small instances (in addition to being slower asymptotically).

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> On page 17 of https://www.nitrd.gov/pubs/nsa/sta.pdf you’ll find the NSA claiming in 2005 that by 2010 they should be able to produce “An RSFQ processor of approximately 1-million gate complexity, operating at a 50 GHz clock rate.”

Now that we have 15 years of hindsight relative to when that projection was made, would it be fair to say that this 2005 projection was wildly over-optimistic? Do you have data on what performance has actually been achieved with RSFQ (as opposed to projections)?

---

**burdges** (2020-06-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Can you expand on the calculation here? If someone built a commodity ASIC evaluator that sped up the VDF evaluator by a factor of 10x would delay encryption then require tens of terabytes?

A faster ASIC does not reduce the memory footprint.  Afaik only a shorter runtime saves memory.

All that memory contains parameters for each low degree isogeny in the chain.  You generate this long chain of low degree isogenies from some starting curve, but an evaluator must remember those parameters.   Also, you find this curve with a trusted setup so that nobody can find faster ways to compute the chain of isogenies.

If you speed the isogeny up enough, then yes you could recompute these parameters on the fly.  As discussed in https://eprint.iacr.org/2019/166.pdf doing this costs at minimum a log p = 1500 factor, which one could make worse fairly easily I think.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Is the Web3 Foundation interested in doing this R&D work? To your knowledge, is anyone intending to use an isogeny-based VDF or delay encryption in production?

We initially found the isogeny VDF attractive for several reasons, including delay encryption.  We’ve no plans to fund more work on them right now though.

We’ve no good commodity hardware story for this delay encryption evaluator: If a 1 hour long VDF needs 16 terabytes then we’d need a machine that costs almost 100k USD for all that RAM.  That’s a “commodity configuration” in that you can simply buy it, but not a “commodity price”.  We could do this cheaper with slower memory or even parallel SSDs, but afaik doing so means ASICs to arrange access to parallelize access to that slower hardware, not a “commodity configuration”.

At some level “distributed” means ordinary people run the code.  I suppose delay encryption might prove useful in national elections or in running financial markets.  It’s still cheaper to spend $100k or $1M per evaluation node than to open ballots by time lock puzzles.

An isogenies VDFs without delay encryption could do many shorter evaluations to trades proof size for memory.  We’ll keep an eye on them though ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) partially due to side interests in two other isogenies based protocols.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> My understanding of Dankrad’s analysis is that the asymptotic growth in the number of transistors required to implement DJB’s circuit is extremely unfavourable.

Interesting.  Is this posted anyplace?

As I said, ASICs alone cannot obviously make isogenies VDFs fast enough to become memory bandwidth limited, but they’re close enough that maybe something does.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Do you have data on what performance has actually been achieved with RSFQ (as opposed to projections)?

I never looked for anything current.  I think https://www.iarpa.gov/index.php/research-programs/c3 indicates serious ongoing work, but maybe not on that timeline.  I think [GitHub - iamcryptoki/snowden-archive: 💥 A collection of all documents leaked by former NSA contractor and whistleblower Edward Snowden.](https://github.com/iamcryptoki/snowden-archive) has some budgets entries, so maybe one could search there.

---

**asanso** (2020-06-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/gokulsan/48/2303_2.png) gokulsan:

> is it possible to construct Lattice cryptography based VDFs which would be more memory efficient than Isogeny based VDFs ? Please advise me if this idea is very naive or irrelevant !

I am not aware of any VDF based on Lattice Cryptography (yet). If this is possible well we do not know yet.

---

**kladkogex** (2020-06-23):

Pretty interesting paper - we may use this at SKALE at some point!

---

**dankrad** (2020-06-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> Interesting. Is this posted anyplace?

I don’t think we published anything but this analysis is actually quite straightforward; I’ll ignore \log factors for easier readability [[1]](#footnote-21559-1) but here’s the gist: The Bernstein algorithm can do an n bit exponentiation (where n is the total number of bits in base, modulus and exponent) in O(n) using ca n^2 processors. If you look at the algorithm closely, the processing nodes need to be fully connected at every step: Each processor needs to send each other processor a message in order to perform the reduction. A simple geometry argument means that each step will actually need at least time O(n^{2/3}) if considering wire delays; O(n^{1}) when only considering flat geometries. This is not considered in the paper as it only considers gate delays and not wire delays.

This means that a full VLSI model considering wire delays would mean that Bernstein’s algorithm needs at least time O(n^{1+2/d}) for d \in \{2, 3\} depending on what geometry you want to choose. In short, once wire delays are taken into account, Bernstein’s algorithm is definitely *not* linear and does not scale better than non-CRR algorithm (such as redundant polynomial representation). This asymptotic analysis however does not mean that there could not be an intermediate regime where it is best. In order to know this, we need to know more about the constants.

1. The log factors in Bernstein’s algorithm are purely due to an extremely unrealistic computing model that is the CRCW PRAM, so I don’t think they matter for this discussion. Achieving O(n) exponentiation without considering wire delays is well known to be possible using other algorithms as well. ↩︎

---

**burdges** (2020-06-28):

> If you look at the algorithm closely, the processing nodes need to be fully connected at every step: Each processor needs to send each other processor a message in order to perform the reduction.

I’d agree PRAM models sound not realistic of course.  I’ve read RNS schemes that communicate a fair bit during the reduction, sure.  I never unpacked all the FFTs and other algorithms DJB throws at the non-parallel parts here.  I also never really understood his staging of the “messages”, but they seemingly tolerated some latency, no?

---

**dankrad** (2020-06-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> I’d agree PRAM models sound not realistic of course. I’ve read RNS schemes that communicate a fair bit during the reduction, sure. I never unpacked all the FFTs and other algorithms DJB throws at the non-parallel parts here. I also never really understood his staging of the “messages”, but they seemingly tolerated some latency, no?

That’s a very vague statement. The point is that at each step of the algorithm (step being one exponentiation and partial reduction), basically all processors need to communicate with each other. This means the latency of passing those messages limits the speed of each step.

That’s all that I need for my analysis.

---

**burdges** (2020-09-16):

About this authentication question:  I’d just authenticate the vote ciphertexts using some ring/group VRF so that VRF outputs being unique prevents double voting.

In this, we sign the ciphertext as an associated message in the Schnorr DLEQ proof, SNARK, etc. part of the ring VRF, not the VRF input obviously.  Any good VRF has such an associated message.  RSA-FDH and BLS sigantures lack this associated message, but those are less nice to make into ring/group signatures, and they were always terrible VRFs in the first place.

All this reduces vote anonymity to your transport layer, ala Tor, mixnet, etc.

Ain’t clear why delay authentication ever helps, but if so then you could do this inside the vote plaintext too.

