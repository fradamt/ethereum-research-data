---
source: magicians
topic_id: 22675
title: Hardware and Bandwidth Recommendations for Full Nodes and Validators
author: SamWilsn
date: "2025-01-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/hardware-and-bandwidth-recommendations-for-full-nodes-and-validators/22675
views: 1134
likes: 11
posts_count: 11
---

# Hardware and Bandwidth Recommendations for Full Nodes and Validators

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9270)














####


      `ethereum:master` ← `kevaundray:kw/hardware-bandwidth-recs`




          opened 09:51PM - 26 Jan 25 UTC



          [![kevaundray](https://avatars.githubusercontent.com/u/37423678?v=4)
            kevaundray](https://github.com/kevaundray)



          [+152
            -0](https://github.com/ethereum/EIPs/pull/9270/files)







Original documents are here (for validators):

- Hardware: https://hackmd.io/G[…](https://github.com/ethereum/EIPs/pull/9270)3MvgV2_RpKxbufsZO8VVg?view
- Bandwidth: https://hackmd.io/DsDcxDAVShSSLLwHWdfynQ?view

## Replies

**OisinKyne** (2025-01-27):

Following up on a comment [from github](https://github.com/ethereum/EIPs/pull/9270#issuecomment-2616187667):

> If I had to choose one right now, I would perhaps tend towards “x% of a validator price can get you” or “y% of a validator’s annual reward can get you” – and we could figure out what x or y is by answering the question of “how long should it take a validator to recoup their hardware capex”

I agree, and I strongly think that it should be Y=10. i.e. 10% of a validator’s annual reward - its operational costs =  budget to pay off hardware over its expected lifetime. The reason I think 10 rather than like 100 is that 10% is roughly the number where its cheaper to give up and delegate your eth, which we want to discourage or at the very least benchmark off of.

---

**kevaundray** (2025-01-27):

Would this apply to validators who want to build blocks locally too, or just validators using mev-boost?

---

**OisinKyne** (2025-01-27):

The most conservative option would be to use the value a local building solo validator makes in APR as the reference. I personally don’t mind using a value that a mev-extracting validator makes, (though i generally hope something like mev-burn comes in to negate this disparity).

---

**kevaundray** (2025-01-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oisinkyne/48/5729_2.png) OisinKyne:

> ld be to use the value a local building solo validato

I would lean towards doing it for validators with mev-boost because in my opinon, once we add things like zkvm proofs, the hardware needed to do local block building might exceed this number (I imagine a GPU would be needed to produce those proofs in a reasonable amount of time).

I have no strong opinion on the 10% figure, so would defer to whomever has more experience with validator economics. The rationale for it makes intuitive sense to me though.

---

**nixo** (2025-01-29):

An alternative to these hardware and bandwidth requirements:

Though the proposed hardware requirements make sense today and in the foreseeable 1-2 years, they don’t scale beyond that. For bandwidth, the numbers are quite arbitrarily chosen in response to the *global average* upload speed and they’re neither based on current usage nor widespread availability. The following also future-proofs any proposed EIP with dynamic rather than fixed requirements so that they aren’t wholly dependent on the current state of hardware prices or external links.

## Hardware:

*Non-validating* node hardware requirements are more difficult to quantify (beyond commercial availability) than *validating* node hardware requirements because we don’t know the rationale for running one is, so I’ll focus on *validating* node hardware requirements.

*Validator* hardware requirements should be a purely economical consideration. If we set hardware requirements to a fixed time-to-profit rather than a fixed size, we can keep pace with things like [Moore’s law](https://en.wikipedia.org/wiki/Moore's_law) and also acknowledge that the willingness of a rational financial actor is in their ability to make up the initial and ongoing costs of an action.

With 32 ETH and an average network APR of 3.10% (via rated.network), each validator earns around $200-250 per month. The proposed hardware requirements by the Consensus R&D team, *today*, result in a validator operating in pure profit (minus internet and negligible electricity costs) in 4-5 months. Given that this kind of hardware generally doesn’t need replacement for 2-5 years, this makes operating a validator an economically rational endeavor.

I would propose that rather than publishing an EIP with simple external links, we publish a target time-to-profit. This could then externally link to an actively maintained list that has specs and examples of hardware that currently fit that requirement. This is scalable for any point into the future. My preference for that time-to-profit value would be between 6-12 months. We are currently below this, at ~4 months, and this gives us room to scale hardware requirements even slightly beyond your proposal.

**Downsides**:

- Hardware costs fluctuate often, both increasing and decreasing without much rhyme or reason. Active maintenance a list should probably choose a cadence on which to update these recommendations.
- Hardware costs fluctuate based on location because of external costs like shipping and VAT. In my opinion, we should not attempt to accommodate for any individual situations. Much of the world has different external costs and including a ~10-20% buffer in the total cost could act as a blanket accommodation for most regions.
- Does not account for distributed validator costs which, due to redundant systems, are much higher than a vanilla home staking setup.

## Bandwidth:

Accurate data on bandwidth is extremely difficult to obtain due to the fact that ISPs do not publicly publish details about their network coverage - fiber, cable, or DSL. The best we have is:

- FCC National Broadband map: maximum advertised upload and download speeds of a census block (US-only)
- Digital Economy and Society Index: Overall digital performance on national levels (Europe)
- Median measured upload and download speeds by city and country, published by Ookla (Global)

These datasets each have their drawbacks - the FCC National Broadband map often over-represents their actual speeds (hence the usual terminology of “up to”) and they only need to offer those advertised speeds to one residence in a census block in order to make the claim. DESI doesn’t offer granularity by region. The Ookla dataset may have some sampling bias in that the dataset is created by testing their speeds on the web interface - users who test their speeds may over-represent people experiencing network issues or slower speeds in general.

Even so - these are currently the best datasets we have to represent speeds in various areas. Ookla’s, especially, is better than using the global average because of its granularity and the fact that it publishes *median* instead of average.

Upload speeds are currently a bottleneck in staking - for those without symmetric connections, download speeds in most areas generally so far exceed requirements for staking that it’s not necessary to quantify. Upload is trickier - for symmetric connections, the necessity to quantify is also moot - but many neighborhoods in some of the world’s most populous cities still have poor upload bandwidth availability. Some neighborhoods this affects are those in New York City, Los Angeles, Brussels, Brooklyn, Sydney, Rome, Vienna, etc.

Given that current validator peak usage is viable with <10 Mbps upload speed, the proposed 50 Mbps is a 5-8x increase and somewhat arbitrarily chosen.

My proposal is that we actually work to quantify bandwidth availability among existing home stakers and optimize for keeping ~90% of that set. This can easily be done in a self-reported manner with the annual staking survey that’s set to begin collecting data very soon.

In a larger and more ambitious effort, we could make or fund an effort at quantifying bandwidth availability in cities that intersect at:

1. A median income level that creates a credible possibility that a not-insignificant number of people in that area might reasonably have 32 ETH
2. Among the 100 most populous cities in the world (which, today, brings us to cities with populations larger than ~4.3 mil)

In this more ambitious data collection scheme, we might optimize for making running a node available to the top ~75% of that population in terms of upload speeds.

---

**MicahZoltu** (2025-05-14):

> Full nodes: Nodes that follow the tip of the chain without necessarily proposing blocks.

> Full Node 4 TB NVMe

A node can follow the tip of the chain without any history beyond what is necessary to handle reorgs (e.g., only back to finality).  A node that actively prunes history (which clients can do today) only needs state and 48 hours of history.  This means out of the 1TB of disk that Nethermind requires according to their docs ([Database | Nethermind documentation](https://docs.nethermind.io/fundamentals/database#database-size), which may be out of date), you only actually need ~200GB of disk.  This doesn’t tell the full story because active pruning requires an additional 250GB of disk space, though that could potentially be relieved with alternative database designs.

Regardless of whether you count the pruning overhead or not, this is still **way** below the 4TB requirement claimed in this document.  The document should be updated to accurately reflect the minimum requirements for a node to follow head and maintain head state, without retaining any history beyond finality.

---

**dankrad** (2025-05-15):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Regardless of whether you count the pruning overhead or not, this is still way below the 4TB requirement claimed in this document.

The intention is that users can not only run a node now, but if they want to make the investment to buy a machine that it should be able to follow the chain for at least 2-4 years.

In the light of scaling the L1, this will still be a 4TB machine, even after more aggressive history expiry has been implemented.

---

**CelticWarrior** (2025-05-15):

With state expiry today, for Nethermind and Geth (and maybe other ELs), a 2TB drive is only 50% full.  That will likely be sufficient for another 1+ years.  Maybe forever if EIP4444 gets included in time.  That’s certainly enough for an attesting node.

---

**MicahZoltu** (2025-05-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> The intention is that users can not only run a node now, but if they want to make the investment to buy a machine that it should be able to follow the chain for at least 2-4 years.

My understanding was that this document was meant to be descriptive, not prescriptive.  Getting a prescriptive EIP agreed on is relatively easy, you just need people to assert what is.  Getting agreement on a prescriptive EIP is much harder as you need everyone to agree on where things are going.

If this EIP is intended to be prescriptive, then it suddenly becomes a lot more contentious as we need everyone to agree on whether we want to move to a world where 4TB drives are necessary just to maintain head state, or a world where 100GB is all you need.  Currently, you can maintain head state with under 100GB in a trusted way (flat state DB, history only back to finality), and with some relatively minor additions to the protocol we could make that untrusted (blocks include a state diff proof).

4TB is 40x bigger than 100GB, and radically changes the demographic of people who can maintain head state, so is a pretty huge decision and one that I think should be made more intentionally rather than just by having a group of people draft an EIP and then assert that these are the requirements.

---

**rolfyone** (2025-08-07):

Are we able to expand this EIP to cover peerDAS super nodes somehow? I think it’ll be a different requirement to the rest of what’s currently covered…

