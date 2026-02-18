---
source: ethresearch
topic_id: 6260
title: Can anyone come up with attacks for Idena?
author: Equilibrium94
date: "2019-10-09"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/can-anyone-come-up-with-attacks-for-idena/6260
views: 3307
likes: 2
posts_count: 4
---

# Can anyone come up with attacks for Idena?

It seems like Idena wont work, but I can’t think of any specific attacks:


      ![](https://ethresear.ch/uploads/default/original/3X/e/8/e888f121a12f51751f765791fcb554a84410c106.png)

      [idena.io](https://www.idena.io/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/f/2/f2aa196733341582a63d80a802dd368060ead2c5_2_690x362.jpeg)

###



Join the mining of the first human-centric cryptocurrency

## Replies

**maxwellfoley** (2019-10-11):

This is a really interesting project, thanks for sharing. I agree with you that it seems unlikely to work but they do seem to have thought through a lot of potential problems.

The obvious attack vector is that validators could collude with other validators / potential validators by sharing their "flip"s ahead of time and thus letting their peers cheat on the Turing test. One could even use steganography to create flips that are in fact solvable by AI, for instance by ensuring that on all correct images the pixel in column 200, row 345 has a red value >= 100 whereas on all incorrect images it has a red value < 100. A complex enough encoding scheme could be undetectable or at the very least plausibly deniable.

The “Flip Distribution” section of the FAQ tries to address this, but the solution is to disallow users in the same family tree of invited accounts from solving each other’s flips using a “genome code”. The “genome code” concept seems overly simplistic and it seems unreasonable to expect that people with different genome codes would never collude simply because they weren’t invited to the network by the same people.

Additionally, if the randomness algorithm that chooses which flips are assigned to which users is on-chain and auditable, it can be predicted ahead of the time who will have to solve whose flips, meaning that it can perhaps be gamed (e.g. by strategically buying accounts).

Also, I tried to solve the flips they had on their website, and they are really hard!

[![05%20AM](https://ethresear.ch/uploads/default/optimized/2X/7/7be7f61434a993c93eb289433742c8213901270c_2_397x500.jpeg)05%20AM1308×1646 350 KB](https://ethresear.ch/uploads/default/7be7f61434a993c93eb289433742c8213901270c)

What the hell is going on here? In addition to the narrative not making sense, I can’t even tell if these are supposed to be the same person in the pictures. Their faces don’t look the same at all (especially between the man yelling at an empty plate and the man eating) but if there are multiple characters in this story making them all white men with short brown hair was a terrible choice.

Anyway, it seems really unlikely to me that all humans will be equally skilled at solving these. Not only do they seem to require certain cultural assumptions to solve, at times they almost feel like an IQ test. On a philosophical/political level, it feels like it will be controversial for this network to create a “test for personhood” that e.g. autistic, unintelligent, atypical, etc etc people might not qualify for. On a technical level, it means that certain use cases are beyond the scope of this platform.

In general though, it seems unlikely to me that they can make the challenges easy enough that the majority of people can solve it but still difficult enough that there isn’t anyone who can solve it at 2x the speed and thus create two identities. I would even imagine that there are people who can at least 5x this challenge, especially if we allow for practice.

Also, while the protocol has protection against people making the challenge too hard, there is nothing preventing them from making it too easy. If the flips become so easy that, say, a human can solve them 20 times faster then the protocol expects, then it seems like everyone will end up with many identities and the chain will start to degrade into more of a typical proof-of-stake chain where it’s possible for oligarchies to form and so on. It could be possible that large groups of colluding users would have an incentive to make this happen and thus increase their power.

---

**midenaio** (2019-10-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxwellfoley/48/4094_2.png) maxwellfoley:

> The obvious attack vector is that validators could collude with other validators / potential validators by sharing their "flip"s ahead of time and thus letting their peers cheat on the Turing test. One could even use steganography to create flips that are in fact solvable by AI, for instance by ensuring that on all correct images the pixel in column 200, row 345 has a red value >= 100 whereas on all incorrect images it has a red value  The “Flip Distribution” section of the FAQ tries to address this, but the solution is to disallow users in the same family tree of invited accounts from solving each other’s flips using a “genome code”. The “genome code” concept seems overly simplistic and it seems unreasonable to expect that people with different genome codes would never collude simply because they weren’t invited to the network by the same people.

Assume the network 1000 and adversary with 100 real people colluded. Adversary knows the answers for 10% of flips in advance. This means the adversary can validate 1% of Sybils by colluding.

On the next round adversary knows 11% of the flips so can validate 1.1% of Sybils. Adversary can only grow extensively which means that more and more real people has to be colluded.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxwellfoley/48/4094_2.png) maxwellfoley:

> Additionally, if the randomness algorithm that chooses which flips are assigned to which users is on-chain and auditable, it can be predicted ahead of the time who will have to solve whose flips, meaning that it can perhaps be gamed (e.g. by strategically buying accounts).

The distribution algorithm is a function of a random seed which is not knwon in advance. Once the seed is calculated the list of candidates for the next validation is finalized.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxwellfoley/48/4094_2.png) maxwellfoley:

> Also, I tried to solve the flips they had on their website, and they are really hard!
> …

The hard flip means it’s also hard for others in average. If the flip does not gather consensus about the right answer it becomes disqualified and not counted in the validation. You can find [results for the last validation here](https://scan.idena.io/validation?epoch=12#flips). 9 out of 189 flips where disqualified in the sample.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxwellfoley/48/4094_2.png) maxwellfoley:

> Anyway, it seems really unlikely to me that all humans will be equally skilled at solving these. Not only do they seem to require certain cultural assumptions to solve, at times they almost feel like an IQ test. On a philosophical/political level, it feels like it will be controversial for this network to create a “test for personhood” that e.g. autistic, unintelligent, atypical, etc etc people might not qualify for. On a technical level, it means that certain use cases are beyond the scope of this platform.

It’s mostly a matter of the diversity of the network. Diverse network won’t qualify a culturally biased flips as well as hard flips. Flip is not an IQ test but rather a common sense logic test.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxwellfoley/48/4094_2.png) maxwellfoley:

> In general though, it seems unlikely to me that they can make the challenges easy enough that the majority of people can solve it but still difficult enough that there isn’t anyone who can solve it at 2x the speed and thus create two identities. I would even imagine that there are people who can at least 5x this challenge, especially if we allow for practice.

This is a trade off. It takes 12-15 seconds to guess a flip. Some people especially kids could be even faster, like 2 times faster. So it’s possible to validate 2x identities at the same time (bonus for IQ), but no one can validate 3x consistently. You are welcome to try - invites are freely available at [Idena Telegram chat](https://t.me/IdenaNetworkPublic)

![](https://ethresear.ch/user_avatar/ethresear.ch/maxwellfoley/48/4094_2.png) maxwellfoley:

> Also, while the protocol has protection against people making the challenge too hard, there is nothing preventing them from making it too easy. If the flips become so easy that, say, a human can solve them 20 times faster then the protocol expects, then it seems like everyone will end up with many identities and the chain will start to degrade into more of a typical proof-of-stake chain where it’s possible for oligarchies to form and so on. It could be possible that large groups of colluding users would have an incentive to make this happen and thus increase their power.

There is a randomly selected pair of words assigned for the every new flip. The flip must be relevant to these key words otherwise the author of the flip is getting penalized. This ensures the diversity of flips.

---

**maxwellfoley** (2019-10-15):

Hey, thanks for the response. Like I said to OP, you have a very fascinating project. I thought that creating a decentralized identity system would be an unsolvable problem but this project is way closer to a practical implementation than I imagined would be possible anytime soon (if not all the way there).

> Assume the network 1000 and adversary with 100 real people colluded. Adversary knows the answers for 10% of flips in advance. This means the adversary can validate 1% of Sybils by colluding.
> On the next round adversary knows 11% of the flips so can validate 1.1% of Sybils. Adversary can only grow extensively which means that more and more real people has to be colluded.

Indeed you are correct that it is difficult for an adversary to experience compound growth in the share of the network it controls, because it will still require more human people to collude as its share grows - I failed to fully understand this as I wrote my initial reply. It does seem like without bringing more humans into the scheme, the growth is extremely limited.

So I can’t think of a way for an adversary to take over the network gradually with only a limited number of humans, but it does seem to me like an adversary could artificially increase their share of the network in order to overtake the 1/3 threshold which allows an attack on a Byzantine-tolerant system, making the true threshold in this system quite a bit less, maybe around 15-18% (assuming my math is correct, which is certainly not a guarantee ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=12)).

Let’s define two collusion schemes an attacker can use in parallel:

**Friendly Flips:** users in an attacking pool share the flips they submitted to the network protocol to the other users in the pool ahead of time (described in my earlier post, and acknowledged by you)

**Shared Solving:** once a user in an attacking pool solves a flip in the midst of a challenge, she forwards the answer to all the other users in the pool, thus letting them solve the flip instantaneously if they are challenged with it as well (definitely feasible to implement in code as well)

(**EDIT:** Actually now I remember your site saying that you must write flips prior to joining the network as well - so maybe you can make it so that the number of flips written are equal to the number read and none are reused? If so then Shared Solving isn’t possible and this post is wrong.)

Using Friendly Flips alone, an attacker that controls r share of the network can generate identities in proportion to \frac{r}{1-r}, as you illustrated above with the case of r = .1.

Using Friendly Flips and Shared Solving together, I believe the proportion goes up to (very roughly) \frac{r}{1-r(1+\frac{1-r}{2})}.

The intuition behind this is: in (1+\frac{1-r}{2}), the first term 1 comes from Friendly Flips, while the second term \frac{1-r}{2} comes from Shared Solving. The last person in the attacking pool to submit their answer will have approximately r * totalNumberOfFlips already-solved answers to choose from, but we must reduce this term to account for the fact that some of the answers will be included in the set already known via Friendly Flips, so we reduce by multiplying by (1-r). The first person in the attacking pool, on the other hand, will get no help from Shared Solving in choosing their answers. So we average out across all cases by taking the “halfway” case which is \frac{r*(1-r)}{2}.

So in order to calculate what initial ratio of attackers is necessary to reach a 1/3 Byzantine attack threshold, we can create an equation:

\frac{\frac{r}{1-r(1+\frac{1-r}{2})}}{1 + (\frac{r}{1-r(1+\frac{1-r}{2})}-r)} = \frac{1}{3}

(the added complexity here is necessary to take into account the fact that the overall “pie” that the attacker is trying to take will increase by the same amount the attacker’s share does)

[Plugging this into Wolfram Alpha](https://www.wolframalpha.com/input/?i=%28x%2F%281-x%281%2B%281-x%29%2F2%29%29%29%2F%281%2B%28%28x%2F%281-x%281%2B%28%281-x%29%2F2%29%29%29%29-x%29%29+%3D+1%2F3) I get r = .24783.

So 25% attacks are possible, but this is still not taking into account the fact that, in order to ensure that the majority of “slower” humans will still be able to solve enough flips to satisfy the system, it must be possible that the average human will be able to solve more than his fair share of flips, should he choose to. So the real threshold at which consensus attacks are possible is likely to be somewhere in the teens (e.g. 16% if the average human can 1.5x the challenge).

(It’s interesting to think about how this plays into the standard assumption that a supermajority of validators must be “honest” for Byzantine Fault Tolerance theory to work. One imagines that honest validators will not be creating more than one identity for themselves, meaning that this “jump” from ~16% to 24% is easy since no one else will be playing the same game. Strangely, it seems like if more validators were *dishonest* in this specific way it would actually *increase* the security of the network!)

This might not be fatal though, however, because it does seem like once the network grows to a sufficient size, getting 16% of the actual humans in the network to collude will be quite a bit harder than merely having capital equivalent to 16% of the network’s market cap. So the protocol is still promising. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

On the other other hand though, as Vitalik has pointed out in his blog posts, people looking to monopolize blockchain networks can easily throw a veil over the sleaziness and dishonesty by presenting their scheme as a “staking pool”, which seems possible here.

