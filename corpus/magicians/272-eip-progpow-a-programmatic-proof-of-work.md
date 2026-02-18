---
source: magicians
topic_id: 272
title: "EIP-ProgPoW: a Programmatic Proof-of-Work"
author: ifdefelse
date: "2018-05-03"
category: EIPs
tags: [progpow, pow, eip-1057]
url: https://ethereum-magicians.org/t/eip-progpow-a-programmatic-proof-of-work/272
views: 13177
likes: 14
posts_count: 62
---

# EIP-ProgPoW: a Programmatic Proof-of-Work

We propose an alternate proof-of-work algorithm tuned for commodity hardware in order to close the efficiency gap available to specialized ASICs. Thanks in advance for your thoughts and comments!

EIP here:  https://github.com/ethereum/EIPs/pull/1057

Implementation here: https://github.com/ifdefelse/ProgPOW

## Replies

**chfast** (2018-05-21):

Hi there.

The https://github.com/ifdefelse/ProgPOW is the fork of https://github.com/ethereum-mining/ethminer. Why did you remove the reference to the upstream project?

Did you implement the OpenCL and CUDA changes there?

I started a new implementation of ethash on a side: https://github.com/chfast/ethash. This is now used in ethminer, partly used in cpp-ethereum and is going to be used in ethereum-js and maybe in Python clients. The library also has good test coverage and testable big-endian support. It might be easier to present your changes there and later depend on other projects to pull in the library.

---

**ifdefelse** (2018-05-22):

Hi Chfast,

Thanks for the tip! We will take a look at your ethash. We hope you can continue to provide helpful advice for this effort. ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=9)

We did optimize for both OpenCL and CUDA in our miner code. This was important to give a fair shake to the capabilities of different GPU implementations.

The reference to the upstream project was dropped when I cloned the project into an initially private repo. Once I made it public, the reference wasn’t restored.

---

**ifdefelse** (2018-05-23):

Hi chfast, could you remind me how ethminer/cpp-ethereum using https://github.com/chfast/ethash? I don’t see any chfast/ethash’s file used by ethminer and eth.

---

**chfast** (2018-05-23):

The chfast/ethash library is a package in Hunter package manager.

ethminer uses it to get metadata about the epoch context (light cache size, full dataset size, etc) and to verify solutions coming from GPUs. It also uses keccak implementation from ethash.

cpp-ethereum uses only keccak implementation from ethash. The legacy ethash library is still in use in cpp-ethereum (libethash dir). I’m working on API changes in chfast/ethash to allow full replacement of ethash library in cpp-ethereum.

---

**ifdefelse** (2018-05-23):

I got, chfast. Thx for your explanation.

---

**eosclassic** (2018-08-03):

I would like to know if there is a implementation for go-ethereum also?

---

**chfast** (2018-08-24):

Is the fnv1a change related to this discussion? https://gitter.im/ethereum-mining/ethminer?at=5b1a1af1144c8c6fea7d40ca

---

**chfast** (2018-09-26):

The functions like ROTL32, clz, popcount should be specified together with cases that are undefined behavior in C.

---

**chfast** (2018-09-27):

Please clarify the Keccak hash function params.

You stated that the bitrate is 448, so the output size is 176 (!) because 800 - 2*176 = 448. But the actually output was truncated to 64-bits. There is no padding (I have to read that from the implementation!). So the name should look like `keccak_f800_176_64_nopadding()`.

Maybe just name this weirdo `keccak_progpow`?

Edit: in other place 256 bits are taken from the Keccak state (while by the spec the output has only 176 bits). Is this allowed by the Keccak spec?

---

**chfast** (2018-10-01):

The implementation of `keccak_f800` takes a header hash and interprets it as an array of 8 32-bit words. This will give different results on big-endian architectures. See https://github.com/chfast/ethash/pull/79.

---

**illuzen** (2019-01-15):

The EIP states:

> If the program only changed every DAG epoch (roughly 5 days) certain miners could have time to develop hand-optimized versions of the random sequence, giving them an undue advantage.

I’m curious what kind of optimization would only be possible by hand here. Do you have any examples?

---

**shemnon** (2019-05-24):

As I mentioned on AllCoreDevs #62 I feel there is a potential change in the EIP ProgPow that must be done before deployment.  This stems from a concern voiced by [Vitalik on AllCoreDevs #60](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2060.md#eip-1057-status-draft).  I forwarded my concerns to Hudson so he could forward it to the team conducting the audit, but since there has been discussion of deploying ProgPow without a finished audit then this issue and possible remediations should be discussed outside the audit.

In short, at the transition block, 1/3 (or less) of the ethash hash power could be used to stall the progression of the chain.  There are one of two things we could change to fix it.

Since ProgPow hashes produce 50% (or less) of the number of hashes per device than Ethash the total difficulty would rise at a slower rate, 50% or less.  To mount this attack the byzantine Ethash hashers would then focus their efforts on publishing new pre-fork blocks with higher and higher difficulties.  Because the byzantine actors produce hashes at twice the rate the pre-fork block could have higher total difficulty with less effort and honest miners may then re-org to the block just prior to the fork.  Emissions are irregular so this may not be able to hold things off forever, but in essence a 33% device pool could mount a 50% hashrate attack aimed at stalling the chain.  This is different from a normal 50% attack in that one generation of blocks has their difficulty measured differently than another generation, and the prior generation can be manipulated.

I see two alternate mitigations.

1. A “difficulty multiplier” can be applied to the ProgPow blocks when calculating total difficulty.  Either 2x to account for the twice as hard memory access or a (much?) larger multiplier to give heavy weight to progpow blocks.
2. A finality gadget, or on-chain checkpoint. This would be like the beacon chain finality gadget except it would be driven by a multi-sig contract.  However that raises governance issues as to who signs the contract and what hash is chosen.  With the beacon chain it is economic interest driving the selection.

Now I may not have my head fully wrapped around uncles and the modified GHOST implementation that was once in the spec, which is why I want people more versed in the mining process to weigh in.

---

**holiman** (2019-07-31):

Nice idea. So essentially, a group of miners would keep ‘polishing’ an old block, to get people to keep reorging to that one?

I don’t think that’s sustainable.

Let’s assume they have 100% hashpower. After 14s, they find a good enough block. After 14s more, they find another good enough block, that may or may not be better. They can’t add these two difficulties together, which is why a chain that actually progresses (and adds block difficulties from N blocks) will always beat one that stands still and just polishes a block.

However, a separate concern is:

1. At fork-time, let’s assume 25% drops off (asics).
2. Also, the difficulty at fork-time will be too high, and needs to adjust. Before adjustment, it will be less ROI to mine ether, and perhaps better spent somewhere else. So let’s assume that another 25% drops off due to bad ROI.

This leaves us with 50% of the hashpower, trying to mine on a chain where the “tuning” between hashpower and diifficulty is 4x (2x for the dropoff, 2x because progpow is harder to mine). This leads to an even longer period before this imbalance will settle.

Remember – miners do not compete *directly* with eachother, so other miners dropping off does not help the ones remaining (in the short term), they compete with the difficulty threshold.

I haven’t checked how long time it will take before the difficulty can re-adjust.

One way to solve this problem can be to, at fork block, add a division by 2, so that for that particular block, the `difficulty` is divided by two. This would instead lead to a short period where it’s *more* lucrative to mine ether, and would have the opposite effect (which would be good), and not drive miners away from the chain at the forkblock.

Also, the “period of imbalance” will adjust faster if the imbalance is in favour of the miners than if the imbalance is in the other direction (faster as in wall-time, not number of blocks)

---

**shemnon** (2019-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Nice idea. So essentially, a group of miners would keep ‘polishing’ an old block, to get people to keep reorging to that one?
> I don’t think that’s sustainable.

It may not be sustainable, but the optics of a rough fork would be a net negative.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Let’s assume they have 100% hashpower. After 14s, they find a good enough block. After 14s more, they find another good enough block, that may or may not be better. They can’t add these two difficulties together, which is why a chain that actually progresses (and adds block difficulties from N blocks) will always beat one that stands still and just polishes a block.

What they are looking for is not another block good enough by the old difficulty, but a block “twice as good” - so it will take 28s on average to find.  And then a four times as good block, and then an 8 times as good block.  You don’t add the difficulties together of the new old height block you keep looking for ones that exceed the TD of the forked ProgPow chain.  If it’s not past the re-org horizon clients should take that one as canonical.

The risks of the “hairy fork” comes in with the miners, if they take these new higher TDs to mine their blocks off of then we get multiple competing heads.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> However, a separate concern is:
>
>
> At fork-time, let’s assume 25% drops off (asics).
> Also, the difficulty at fork-time will be too high, and needs to adjust. Before adjustment, it will be less ROI to mine ether, and perhaps better spent somewhere else. So let’s assume that another 25% drops off due to bad ROI.
>
>
> This leaves us with 50% of the hashpower, trying to mine on a chain where the “tuning” between hashpower and diifficulty is 4x (2x for the dropoff, 2x because progpow is harder to mine). This leads to an even longer period before this imbalance will settle.
>
>
> Remember – miners do not compete directly with eachother, so other miners dropping off does not help the ones remaining (in the short term), they compete with the difficulty threshold.
>
>
> I haven’t checked how long time it will take before the difficulty can re-adjust.

[@OhGodAGirl](/u/ohgodagirl) has discussed this issue several times.  It’s about 3 hours.  And the impact on the ice age is that it moves closer 2 weeks per halving.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> One way to solve this problem can be to, at fork block, add a division by 2, so that for that particular block, the difficulty is divided by two. This would instead lead to a short period where it’s more lucrative to mine ether, and would have the opposite effect (which would be good), and not drive miners away from the chain at the forkblock.
>
>
> Also, the “period of imbalance” will adjust faster if the imbalance is in favour of the miners than if the imbalance is in the other direction (faster as in wall-time, not number of blocks)

A solution I presented at AllCoreDevs Berlin, the one time difficulty adjustment.  This won’t address the slower growth of total difficulty under ProgPow.  The slower TD growth isn’t a problem if we can avoid the “hairy fork.”

---

**shemnon** (2019-07-31):

Here’s the AllCoreDevs Berlin presentation I did on [falling hashrate](https://www.youtube.com/watch?v=HaT-BIzWSew&t=1s) and my [slides](https://drive.google.com/file/d/1BnOqJdupgJu5oJIEW0SuXi9YNRH25nYi/view)

And it’s 3 hours for 50% drop off, 6 hours for 75% dropoff.

log(0.5)/log(1-2/2048)*15 seconds = ~3 hours

log(0.33)/log(1-2/2048)*15 seconds = ~4.6 hours

log(0.25)/log(1-2/2048)*15 seconds = ~6 hours

---

**shemnon** (2019-08-01):

[@holiman](/u/holiman) - after driving home I think you’re right, it’s not as bad as I imagined.  While the attacking group has a higher hashrate polishing the pre-fork block they only get to keep the best block found.  Over time they will have better and better blocks, but the new chain gets to keep all the work it’s found, it doesn’t have to discard their old work like the attack block would have to.

So 33%  of old hash couldn’t stall the fork, but it could significantly slow it down.  The slow down would be worse if the new chain had to “burn down” it’s target difficulty, especially if we let the difficulty burn down naturally.  So a one time difficulty cut of 50% at the fork block would allow the new chain to grow at the  same block per minute rates as before if the same hardware was pointed at the chain.

A one time difficulty adjustment also would reduce the impact to normal users, regardless of the potential stalling efforts of old hash power.

---

**holiman** (2019-08-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> While the attacking group has a higher hashrate polishing the pre-fork block they only get to keep the best block found. Over time they will have better and better blocks, but the new chain gets to keep all the work it’s found, it doesn’t have to discard their old work like the attack block would have to.

Yes, exactly! (that’s what I meant by “can’t add these two difficulties together”). And I didn’t mean it to sound like that “separate concern” was my idea, I know it’s been floated around before, but wasn’t sure whom to attribute.

---

**holiman** (2019-08-01):

Actually, [@shemnon](/u/shemnon), this is a false conception. Difficulty does not work like that. What you’re talking about is what could be called “the true difficulty”, which is the combination block’s hash with it’s nonce.

What Ethereum uses as `difficulty` is a function of of the parent’s difficulty and the time. Under the hood, we then check that the `true difficulty` is above the threshold.

So basically the `total difficulty` is the sum of all “threshold difficulties” (not the sum of all “true difficulties”). So it’s not possible to “polish a block” indefinitely. The `difficulty` for block N is already given by block N-1, but if you re-mine block `N-1` with an earlier timestamp, you can get a higher `difficulty` for block `N` (but only higher by a certain amount).

---

**shemnon** (2019-08-02):

You only get credit for what is the threshold?  No wonder my toy blockchains rarely had tied blocks.

I theory you could start far enough back to juice the difficulty increase.  But it almost instantly pushes it out of the 50% ongoing hash threshold, even if the new blocks grow slower.  And since you can have at most one block per second it does put an ultimate cap on it, no matter how far back you go.

So yea, not an issue.  This analysis would have been better two months ago.

---

**blahblahblah1** (2019-08-17):

Why is a controversial change being shoved through without awareness of the community? Why does [@OhGodAGirl](/u/ohgodagirl) have so much sway over the governance process?


*(41 more replies not shown)*
