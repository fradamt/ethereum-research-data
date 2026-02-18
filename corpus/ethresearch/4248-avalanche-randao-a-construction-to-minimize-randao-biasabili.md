---
source: ethresearch
topic_id: 4248
title: Avalanche RANDAO – a construction to minimize RANDAO biasability in the face of large coalitions of validators
author: rcconyngham
date: "2018-11-13"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/avalanche-randao-a-construction-to-minimize-randao-biasability-in-the-face-of-large-coalitions-of-validators/4248
views: 7757
likes: 16
posts_count: 23
---

# Avalanche RANDAO – a construction to minimize RANDAO biasability in the face of large coalitions of validators

# TL;DR

The Avalanche RANDAO is an improvement of the RANDAO-based RNG. In the classical RANDAO, each proposer can bias the entropy by one bit through the choice of not revealing their pre-committed entropy. We circumvent this problem by gradually constructing larger and larger committees in which every single validator knows the secret to be revealed. Early in the construction, when committees are small, it is easy to influence the outcome, but hard to predict the result. In later stages, knowing the result becomes easier but influencing it becomes near impossible, thus limiting the possibilities for bias. For example, using a tree of 128 proposers, this construction can limit the probability that a colluding fraction of 30% of proposers can bias the entropy by one bit to around 2%.

This post is based on a shared idea with [@poemm](/u/poemm). Thanks to [@barryWhiteHat](/u/barrywhitehat) for input on secret sharing and helping with zero knowledge proofs.

# Background

The RANDAO has been considered [[RNG exploitability analysis assuming pure RANDAO-based main chain](https://ethresear.ch/t/rng-exploitability-analysis-assuming-pure-randao-based-main-chain/1825)] as a possible RNG for the beacon chain. It is based on the simple idea that each validator commits to a hash onion H(H(H(…S…))) when they enter the validator set. Each time it is their turn to contribute entropy, they reveal one further layer from this onion. Thus, they only have one choice when revealing entropy, to either reveal the precomitted value or to not reveal at all, forgoing the block reward. If a large amount of money is at stake, a validator could choose the latter, as a random roll might give them a better expected return than the entropy they are about to reveal – thus they have the ability to bias the entropy by 1 bit.

However, it has turned out that even this ability to introduce a 1-bit bias on a per-validator level can lead to very significant control when many validators collude. The simple RANDAO-based chain can in fact be completely taken over by 34% of the validators [[RANDAO beacon exploitability analysis, round 2](https://ethresear.ch/t/randao-beacon-exploitability-analysis-round-2/1980)]. Nevertheless the RANDAO is still used as a base source of “biasable” entropy, on which the currently favoured construction based on verifiable delay functions can be built [[Minimal VDF randomness beacon](https://ethresear.ch/t/minimal-vdf-randomness-beacon/3566)].

Several attempts have been made to improve on the pure RANDAO construction by reducing the bias. One idea is to have an additional one bit clock, generated from the next reveals of the validators “voting” on whether the current entropy should be used for the next validator selection [[Making the RANDAO less influenceable using a random 1 bit clock](https://ethresear.ch/t/making-the-randao-less-influenceable-using-a-random-1-bit-clock/2566)]. While this construction can reduce the biasability by single validators, it actually greatly increases the influence of large numbers of validators colluding. The original construction based on majority voting could be improved using low influence functions, further decreasing the chances of introducing bias for a single validator, however also weakening the construction to opponents with a large share of validators. Ever since, there has been the question if there are also constructions that could stand up to large coalitions and actually reduce the amount of bias they can introduce.

More recently, a new idea going into the same direction was introduced, in a way bringing the “low influence” to a different level: Letting committees pre-share their secret, so that at the time when the secret has to be revealed, it is enough that any of the validators reveal it, thus limiting the ability of one or even many validators to bias the entropy by not revealing [[Limiting Last-Revealer Attacks in Beacon Chain Randomness](https://ethresear.ch/t/limiting-last-revealer-attacks-in-beacon-chain-randomness/3705)]. The idea is promising, but it lacked a feasible way to construct these pre-shared secret.

Here we introduce the Avalanche RANDAO, a way to construct a shared secret among many validators, and analyse the biasability of this construction.

## Goal

We want to create a scheme with the following properties:

1. The validators agree on a common secret S, that by construction is known to all validators. No validator can construct a valid S without all the participating validators knowing about it

Ensures that if even a single validator participating in the construction is honest, they will be able to share the common secret when it’s their time
2. The secret S is uniquely determined by the validators participating in the secret-sharing scheme. The only influence a validator can have on it is whether they participate or not

Minimises the possibilities of validators manipulating the resulting entropy. Keeps the RANDAO property that at best, a single validator can have a single bit of bias by revealing or not.
3. Every validator should be able to prove that the secret was constructed in this way

When sharing the secret on chain, this proof should be included
4. The construction should go ahead even if some of the validators are not participating or are withholding collaboration part way

Validators being offline or maliciously not participating should not stop the scheme
5. A part of the committee, even if they are in the majority, should not be able to construct this secret while excluding someone who wants to be inside it if they are online; in other words, anyone in the committee should be able to force their way into the secret as long as they are connected to the network

If more than 50% of the validators on a committee are in one malicious colluding fraction of  validators, they should not be able to construct a secret only they know

## Setup

We assume that we have a set of n validators in a committee. Each validator v_n is committed to a secret a_n by means of a suitable scheme (e.g. through a hash \text{sha256}(a_n) or by publishing a_nG where G is an elliptic curve element). This basically means we use the RANDAO construction as our basis, to make sure that validators have minimal choice going through the process.

## Diffie-Hellman

Our secret sharing mechanism is based on two-party Diffie-Hellman.

We use the elliptic-curve notation for Diffie-Hellman shared secret construction below. The idea works with any DIffie-Hellman scheme, but the elliptic curve construction will probably fit most naturally with the zero knowledge proofs which are required at each stage to show that the construction of the secret was done correctly.

# Avalanche RANDAO construction

The idea is that we create a binary tree of shared secrets, with the property that all of the participants in each subtree know the shared secret of that subtree, while generally people outside do not know it, except if it is shared with them by a validator in that subtree.

In the early stages of building up the tree, when each subtree consists of, say, 1, 2 or 4 validators, it is easy to influence the outcome but difficult to know it, so it is hard to bias.

Once the subtrees become larger, large parties of colluders do actually get a more significant chance of knowing the outcome, but by now the shared secrets are known to so many other validators that it is “too late” to stop it (the avalanche).

At each level of the tree, we use Diffie-Hellman to share the secrets of the two subtrees.

## First step

The first step consists of all n=2^m validators publishing their secret commitment a_iG. (Might be part of the pre-commitment already)

## Second step:

- v_1 and v_2 compute  a_1a_2G, from which they compute a shared (secret) integer S_{12}=\text{int}(a_1a_2G) and publish S_{12}G
- v_3 and v_4 compute a_3a_4G, from which they compute a shared integer S_{34}=\text{int}(a_3a_4G) and publish S_{34}G
- …
- v_{n-1} and v_n compute a_{n-1}a_nG, from which they compute a shared integer S_{n-1,n}=\text{int}(a_{n-1}a_{n}G) and publish S_{n-1,n}G

Note that either of the two validators sharing a secret can compute it for each of these secrets. The collaboration of the other validator is not necessary, but even if they don’t participate they will still be able know the secret.

## Third step

In the third step, v_1 and v_2 both know S_{12} as well as S_{34}G; v_3 and v_4 both know S_{34} and S_{12}G. So each of the four can compute S_{12}S_{34}G without participation of any of the other validators. Our third step thus consists of

- v_1, v_2, v_3 and v_4 compute S_{12}S_{34}G, from which they compute a shared integer S_{1234}=\text{int}(S_{12}S_{34}G) and publish S_{1234}G
- v_5, v_6, v_7 and v_8 compute S_{56}S_{78}G, from which they compute a shared integer S_{5678}=\text{int}(S_{56}S_{78}G) and publish S_{5678}G
- …
- v_{n-3}, v_{n-2}, v_{n-1} and v_n compute S_{n-3,n-2}S_{n-1,n}G, from which they compute a shared integer S_{n-3,n-2,n-1,n}=\text{int}(S_{n-3,n-2}S_{n-1,n}G) and publish S_{n-3,n-2,n-1,n}G

## nth til last steps

This process carries on until in a final step, there are only two subtrees A and B left, with shared secrets S_A and S_B. The commitments S_AG and S_BG are already shared on chain, so at this point, any validator in the whole committee can compute and share the common secret S_AS_BG which will be used as entropy for the Avalanche RANDAO.

[![image](https://ethresear.ch/uploads/default/optimized/2X/1/18c80f8fc241c5ab7a2332a2727660cc7c87e6be_2_690x388.jpeg)image1670×940 223 KB](https://ethresear.ch/uploads/default/18c80f8fc241c5ab7a2332a2727660cc7c87e6be)

At each step, a zero knowledge proof has to be provided that the computation is indeed correct and no “garbage” or invented values were published. This should be fairly simple using SNARKs as all the computations are very simple EC operations.

## Avalanche RANDAO analysis

We want to analyse what influence someone possessing a fraction f of the total stake (a single entity or a coaliton) can have on the randomness of the Avalanche RANDAO.

We can analyse the Avalanche RANDAO by layer. Except for the bottom layer of the tree, a complete analytic expression is very complicated, so we resort to a computer simulation instead. Biasability by layer can be evaluated like this:

- First round (share aiG): Bias possible if the coalition controls v_n as well as one in each pair before; probability of this is f(1-(1-f)^2)^{n/2-1}
- Second round (share S_{i,i+1}G): Bias possible if controlling any pair, one in each group of four before and one in each pair that comes after
- Third round (share S_{i,i+1,i+2,i+3}G): Bias possible if controlling any subtree of four, one in each subtree of four that follows and one in each group of eight that comes before

Here is a python program that uses a Monte-Carlo simulation to estimate the biasability:

```
import random
import math
import numpy as np

def get_committee(layer, committee_no, compromised_nodes):
    layer_subcommittee_size = 2 ** layer
    committee = compromised_nodes[layer_subcommittee_size * committee_no:layer_subcommittee_size * (committee_no + 1)]
    return committee

def check_committee_infiltrated(layer, committee_no, compromised_nodes):
    return any(get_committee(layer, committee_no, compromised_nodes))

def check_committee_compromised(layer, committee_no, compromised_nodes):
    return all(get_committee(layer, committee_no, compromised_nodes))

def layer_compromised(layer, compromised_nodes):
    layer_subcommittee_size = 2 ** layer
    num_nodes = len(compromised_nodes)
    for i in range(num_nodes / layer_subcommittee_size):
        if check_committee_compromised(layer, i, compromised_nodes):
            if all(check_committee_infiltrated(layer, j, compromised_nodes) for j in range(i)):
                if all(check_committee_infiltrated(layer + 1, j, compromised_nodes) for j in range((i/2) * 4 + 1, num_nodes / layer_subcommittee_size / 2)):
                    return True
    return False

def layers_compromised(compromised_nodes):
    layers = int(math.log(len(compromised_nodes))/math.log(2)) + 1
    ret = []
    for i in range(layers):
        ret.append(layer_compromised(i, compromised_nodes))
    ret.append(any(ret))
    return map(lambda x: 1 if x else 0, ret)

def generate_random_compromised_notes(f, n):
    return [1 if random.random() 50% probability of being biasable; from other trials it seems plausible that this is some sort of fundamental limit
- The main contribution to the probability of the tree being compromised (biasable) comes from layers in the middle in the tree. As the tree gets larger, the layer that is most likely to be compromised moves up in the tree. (The plots below show the probability of a tree being compromised for different fraction sizes at n=128, 512 and 2048; so with arbitrary large trees we can move the “kink” of the curve more and more to the right)
- Looking at the nodes that contribute to trees being compromised, we might expect that it is the nodes that reveal later in the process that contribute more. Analysis shows that this is indeed the case for small fraction sizes, but for large fractions it is very evenly distributed across the tree. This means there is probably very little to gain by trying other, asymmetrical, tree structures; for large colluding fractions, the complete binary tree seems close to optimal

# n=128

[![](https://ethresear.ch/uploads/default/optimized/2X/e/e65494bdf739356450e9adf44c467b79a46110c9_2_624x423.png)752×510 73.3 KB](https://ethresear.ch/uploads/default/e65494bdf739356450e9adf44c467b79a46110c9)

# n=512

[![](https://ethresear.ch/uploads/default/optimized/2X/f/fea17cede0bb2b73a81ca580af1c1fa553e99c29_2_624x419.png)756×508 84.4 KB](https://ethresear.ch/uploads/default/fea17cede0bb2b73a81ca580af1c1fa553e99c29)

# n=2048

[![](https://ethresear.ch/uploads/default/optimized/2X/4/406834d4838d71e8cd09cd01ef3223c1de4283b1_2_624x413.png)772×512 88.1 KB](https://ethresear.ch/uploads/default/406834d4838d71e8cd09cd01ef3223c1de4283b1)

## Replies

**jrhea** (2018-11-13):

I’m still digesting this, but i think I found a mistake in the second bullet of the **Second Step**:

> v3 and v4 compute a1a2G, from which they compute a shared integer S34 = int(a3a4G) and publish S34G

should be:

> v3 and v4 compute a3a4G, from which they compute a shared integer S34 = int(a3a4G) and publish S34G

(Sorry for the hand typed quote…for some reason when I used the quote feature the formatting was wacky)

---

**rcconyngham** (2018-11-14):

You are, of course, right. Fixed that and a couple more typos. Let me know if you have any questions, I’m sure I could do better in explaining some of this.

---

**jrhea** (2018-11-14):

This is an interesting idea.  I think I get the gist of it, you are essentially organizing the validators into a binary tree and performing a commit/reveal ceremony at each level of the tree.  This essentially takes away the opportunity (or minimizes the likelihood) for a validator to bias the entropy bc if they choose not to reveal, then the other proposer can continue the ceremony without them.

Quick question:

If was to rerun your simulations…obviously, i need to change n and f accordingly, but it also looks like this line:

```auto
print zip(np.average(results,0),["Layer %d compromised" % i for i in range(8)] + ["Tree compromised"])
```

is looping through the layers of the tree and using the avg results of each trial to display the prob of the layer being compromised.  I am assuming that instead of using `range(8)`, I can just calc the number of layers like this: `int(math.log(n,2)) + 1` .  I just want to make sure I am understanding.

---

**rcconyngham** (2018-11-14):

Yes, exactly. Let me know if you need any other help with the code. The by-layer probabilities are likely not so relevant for most purposes, the overall biasability given by

```auto
np.average(results,0)[-1]
```

is what you should look  at first (by layer analysis might be helpful if you want to improve the tree layout though).

---

**jrhea** (2018-11-14):

Cool thanks, that helps.

So I am able to run the code and understand it well enough to print out some diagnostic information when a layer is compromised/infiltrated and while looking at those scenarios it struck me that they should be easy enough to flag in a real world situation, right?  If, for example, a coalition works together to bias the entropy and they recognize that they are in a configuration that would allow their bias to influence the tree, then they would all have to decide to not reveal, right?  Wouldn’t this be something that we could detect and flag?  If so, it seems like we could either:

- at a protocol level force a re-shuffling that splits up the coalition so that it is futile to attempt biasing the tree (if the coalition is big enough, then they could stall the blockchain, but I’m thinking that level of centralization would affect any consensus scheme)
- or just flag it as suspicious and let dapps know that the result is questionable

Am I way off-base here?  It seems like it would cost a lot of money to indefinitely stall the chain.

---

**rcconyngham** (2018-11-15):

Yes, for sure, four or eight validators collaborating not to reveal should be an extremely rare event in normal circumstances. For example, a service that wants to notify users if something fishy is going on with the entropy could work like this:

- observe the number of “no-shows” among single revealers, which gives you the base probability p_\text{reveal}.
- For all higher layers, observe whether the number of revealed secrets is significantly less than 1-(1-p_\text{reveal})^l, where l is the layer number. If it is, than that’s a clear warning sign that an entropy manipulation attack is going on.

Of course, this does not work very well if only a single or very few very high value outcomes are manipulated.

Otherwise, it’s an interesting idea to use the non-reveal information to “separate” validators that might be controlled by the same person. But note that most of the validators in the attack don’t have to be active at all, the attacker just needs to know their secret. So this would only have an effect on attack that is done repeatedly over a long period. But it might have an effect when the attacker is trying to take over the complete beacon change, as in this analysis: [RANDAO beacon exploitability analysis, round 2](https://ethresear.ch/t/randao-beacon-exploitability-analysis-round-2/1980)

---

**poemm** (2018-11-15):

Excellent work with the Monte-Carlo analysis.

Interesting that at ratio f=0.5, the probability of bias is \approx 0.5. We observed similar behavior in the subcommittee scheme (linked in the original post), and did a combinatorial analysis to find that this behavior is because the cases of bias and no bias are compliments of each other.

Perhaps the Avalanche scheme is best used alone. But it is generic enough to also be used with the subcommittee scheme (linked above), having each subcommittee use Avalanche to agree upon their shared secret.

Again, great work and great ideas.

---

**rcconyngham** (2018-11-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> Interesting that at ratio f=0.5f=0.5, the probability of bias is ≈0.5\approx 0.5. We observed similar behavior in the subcommittee scheme (linked in the original post), and did a combinatorial analysis to find that this behavior is because the cases of bias and no bias are compliments of each other.

Yes, I also found this in my committee analysis. I agree that it is connected to the fact that for f=0.5, the probability of being able to bias a secret is the complement of the probability of being able to know that secret.

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> Perhaps the Avalanche scheme is best used alone. But it is generic enough to also be used with the subcommittee scheme (linked above), having each subcommittee use Avalanche to agree upon their shared secret.

Agree, I think it is an interesting mixture that it can be seen as only the scheme that is used to share secrets, but it also quite naturally leads to a reveal scheme by itself.

---

**vbuterin** (2018-11-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/rcconyngham/48/2570_2.png) rcconyngham:

> In the third step, v_1 and v_2 both know S_{12} as well as S_{34}G; v_3 and v_4 both know S_{34} and S_{12}G. So each of the four can compute S_{12}S_{34}G

Huh? How can you compute G * ab knowing only G, G*a and G*b? Isn’t that literally a violation of computational diffie hellman hardness? Or am I missing something?

---

**JustinDrake** (2018-11-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How can you compute G * ab knowing only G, G*a and G*b?

That’s not the setup. One group (v_1 and v_2) knows a and G*b, and another group (v_3 and v_4) knows G*a and b. (Specifically, a = S_{12} and b = S_{34}.) A zkproof is then used for public verifiability that G*a*b was correctly constructed.

---

**vbuterin** (2018-11-17):

Ah, I see where I messed up. I thought S_{12} *was* a_1a_2G the elliptic curve point.

---

**vbuterin** (2018-11-17):

> This should be fairly simple using SNARKs as all the computations are very simple EC operations.

I think you actually don’t need a SNARK, you just need elliptic curve pairings. Proving that S_{12}G was correctly constructed can simply be done by checking e(S_{12}G, G) = e(a_1G, a_2G).

---

**rcconyngham** (2018-11-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think you actually don’t need a SNARK, you just need elliptic curve pairings. Proving that S12GS_{12}G was correctly constructed can simply be done by checking e(S12G,G)=e(a1G,a2G)e(S_{12}G, G) = e(a_1G, a_2G).

I also hope that the construction is actually simple enough that full-blown zk  proofs won’t be needed. As far as I can see, an elliptic curve pairing could be used to show that a_1 a_2 G was correctly derived, which is a cool insight ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Unfortunately, for this construction to work, we need to keep a_1 a_2 G secret, and derive the shared secret of v_1 and v_2 from it, which is S_{12} = \text{int}(a_1 a_2 G) (where int is a suitable mapping from EC elements to integers). S_{12} should not be publicised (as it would allow anyone to derive all the further steps in the tree), only S_{12}  G will be public. I think the pairing idea does not immediately work to show that S_{12}  G was correctly derived, or am I missing something here?

Still really hope to find some better crypto that can prove correct derivation. SNARKs is just the fallback (but according to [@barryWhiteHat](/u/barrywhitehat) the SNARKs needed here would be very simple).

---

**barryWhiteHat** (2018-11-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/rcconyngham/48/2570_2.png) rcconyngham:

> Still really hope to find some better crypto that can prove correct derivation. SNARKs is just the fallback (but according to @barryWhiteHat the SNARKs needed here would be very simple).

Yeah should be just a hash function and then a few encryptions so the previous committers can decrypt the commited value. I rather the simple version too. But perhaps we will want something more complicated and then the snark will be more useful. It gives us scope to turn this into a much more reactive secret sharing scheme if need be.

---

**vbuterin** (2018-11-17):

Right, I see. I still feel like there’s some simple elliptic curve construction that should be able to do what you want, but that conversion from a_1a_2G into an integer definitely seems like a challenging thing to prove.

Perhaps the solution might be to make the secret that goes one level up be a_1a_2, or is revealing that value (and hence revealing a_1 to the user that submitted a_2 and vice versa) unacceptable?

---

**rcconyngham** (2018-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Perhaps the solution might be to make the secret that goes one level up be a1a2a_1a_2, or is revealing that value (and hence revealing a1a_1 to the user that submitted a2a_2 and vice versa) unacceptable?

This may be possible, then v_1 and v_2 would use a public key encryption scheme* to share their secrets  a_1 and a_2 with each other in the first round, thus creating a shared secret integer a_1 a_2. But now the problem is that they would have to prove that this encryption was done correctly, and they did not “cheat” their partner by not encrypting the secret that they committed to.

So it then boils down to proving that a piece of asymmetric encryption was done correctly. Not sure if this is a simplification?

Another effect of this is that, should  v_2 pull out after v_1 has already shared their secret with them, then v_2 will still know the shared secret all the way down in the tree. I think one interesting property of the original construction is that “when you’re out, you’re out”: Once you fail to share at any given stage, you will not be “in” on the remainder of the secrets. This may be good (failing to share might mean you’re manipulating, so it’s better that you don’t know the secret) or bad (of course, it could be an advantage that a validator who was offline earlier can still come in and fill in later parts of the process, should other validators now be offline or maliciously withholding).

*) We can’t use the shared secret a_1 a_2 G  for this encryption scheme because we want to publish this one later, and then everyone would know their secret which is counter to the point of this scheme. So we need a separate public key encryption scheme here.

---

**burdges** (2018-11-18):

If we accept using zkSNARKs, then we could run both the ECDH and the subsequent Pederson commitment on JubJub, and then verify them with zkSNARKs on BLS12-381.  I think ZCash have pushed verification of scalar multiplications on JubJub down to like 6 constraints, but the ECDH presumably takes more, so this sounds speedy but not actually “fast”, and verification costs some pairings.

Instead, we could go faster by fixing the height and building some tower of curves, so that each layer boils down to some simple two-signer VRF like constriction.  It’d require doing elliptic curve arithmetic on many different curves, likely using Weierstrass arithmetic from the AMCL library, so ugly but still far faster than zkSNARKs, especially for verification.

We can likely make this go fast-ish without any exotic curve constructions using an additive blinding:  We have commitments A_i = a_i G and the $i$th party reveals f(a_1 a_2 G) where f regards a curve point as an integer.  Our 1st participant creates:

- some B = b A_2 and B' = f(B) G,
- NIZK that b A_2 is the ECDH of B and A_2
- NIZK that (a_1 + b) A_2 is the ECDH of A_1 + B and A_2
- NIZK that f((b + a_1) A_2) G's scalar is the curve addition of the scalars of f(a_1 A_2) G and f(b A_2) G.

Now our final NIZK is quite nasty because the arithmetic in the scalar must happen in the base field, but curve addition is easy enough that doing it sounds plausible.

In fact, we should likely replace f with some encoding of the curve point as multiple scalars, maybe like 14 or more since our addition formula has degree six, or maybe some CRT trick improves that.  I think doing this encoding badly technically exposes bits from a_1 A_2, so maybe another layer of blinding is required.

---

**rcconyngham** (2018-11-18):

Just trying to understand your post here. I think your f is what I called “int”, trying  to be very suggestive. We agree that what we’re trying to do is

- Given two commitments a_1 G and a_2 G, give a proof that \text{int}(a_1a_2 G) G was computed correctly, without revealing a_1 or a_2 or a_1a_2 G or, for that matter, \text{int}(a_1a_2G).

Is it right that you are basically trying to prove that statement by constructing a series of other DH secrets (b A_2, (a_1 + b) A_2) which can be published, and proving correctness along the way?

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> some B = b A_2 and B' = f(B) G,

I think you meant B = b G?

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> NIZK that (a_1 + b) A_2 is the ECDH of A_1 + B and A_2

Wouldn’t publishing (a_1 + b) A_2 mean that anyone could compute a_1 A_2 by subtracting (a_1 + b) A_2 - B, which kind of defeats the purpose? Or is the intention to do this step without publishing (a_1 + b) A_2 (just an intermediate step inside an NIZK)?

---

**burdges** (2018-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/rcconyngham/48/2570_2.png) rcconyngham:

> Wouldn’t publishing (a_1 + b) A_2 mean that anyone could compute a_1 A_2 by subtracting (a_1 + b) A_2 - B, which kind of defeats the purpose?

Yes oops.  If you meant b A_2 instead of B then yes it’s broken as written. I’d wanted to avoid verifying any scalar multiplications, or encoding f evaluation, inside the NIZK, but botched it.  We should probably avoid scalar multiplications inside NIZKs if possible, but actually encoding f evaluation sounds tolerable, so we might repair my answer that way:

We cannot hide f(a_1 A_2) G of course.  We might however hide b A_2 by combining the first and third NIZK and encoding f inside this NIZK, so probably several range proofs.  Avoids scalar multiplication still… ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Also, I think the DLEQ proofs in [PrivacyPass](https://blog.cloudflare.com/privacy-pass-the-math/) suffice for the middle NIZK that proves an ECDH, but this combinations of the first and third gets way messier.  I think the hash function evaluation could stays outside the NIZK here, so maybe this makes the curve tower the fastest and most compact solution.

---

**kladkogex** (2018-11-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> Interesting that at ratio f=0.5f=0.5, the probability of bias is ≈0.5\approx 0.5.

My interpretation is that an unbiasable RNG (common coin) is probably very much related to consensus in synchronous, because “revealing”  very much means a synchronous broadcast.

From this perspective,  it could be that unbiasable RNG for > 50% of bad guys is **provably impossible**, in a similar way to a synchronous consensus for more than 50% of bad guys.


*(2 more replies not shown)*
