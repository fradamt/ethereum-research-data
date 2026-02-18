---
source: magicians
topic_id: 22623
title: Blob-Parameter-Only (BPO) forks
author: protolambda
date: "2025-01-22"
category: Magicians > Primordial Soup
tags: [sharding, blob]
url: https://ethereum-magicians.org/t/blob-parameter-only-bpo-forks/22623
views: 1269
likes: 24
posts_count: 11
---

# Blob-Parameter-Only (BPO) forks

**TL;DR: a framework to safely and continuously scale blobs via Blob-Parameter-Only (BPO) forks**

*Sam McIngvale ([@sammcingvale](/u/sammcingvale)), Mark Tyneway ([@tynes](/u/tynes)), Proto ([@protolambda](/u/protolambda))*

### BPO forks

BPO forks are simple Ethereum forks that **only** change two parameters: blob targets and blob limits. BPO forks give Ethereum flexibility to safely scale blobs in smaller, more regular increments and they give builders confidence that Ethereum will continuously grow its capacity.

Ethereum hard forks carry a high operational cost/ burden. One goal of BPO forks is to share that burden across both L1 and L2 teams. If we can agree on a BPO fork outline, we and other members of the Optimism Collective will lean-in as much as possible to help shepherd these forks forward and scale Ethereum.

### A simple framework for BPO forks

There are two generally agreed upon priorities with blobs: 1) ensure solo stakers with limited bandwidth can continue to produce blocks, and 2) provide DA scale to L2s to keep tx costs competitive. More flexibility to tweak blob parameters will help Ethereum thread the needle between the two.

We propose three conditions for a BPO fork:

1. Solo staker minimum bandwidth requirements are generally agreed upon
2. The proposed blob parameter increase can be provably shown to not increase solo staker reorgs
3. Blobs are sustainably congested

**Solo staker bandwidth requirements**

There is [growing consensus](https://x.com/kevaundray/status/1880239190996115581?s=46) around 50Mbps download and upload speed for solo stakers not using MEV-boost. We look forward to helping solidify alignment around the right long-term bandwidth requirements for solo stakers and continuously re-evaluate due to changing conditions.

**Blob parameter increase is safe for solo stakers**

Upload bandwidth mostly varies based on block size. Therefore, a blob parameter increase should be considered safe for solo stakes if the trailing 30d p999 block size plus the size of data given the new blob target fit within the solo staker bandwidth requirements. Francis from Base has a [useful framework](https://docs.google.com/document/d/19jZcm5CgWM12Eqg1HRwG_ppd1EL9tduheckBmoFBCNM/edit?pli=1&tab=t.0) for calculating solo staker upload bandwidth requirements.

**Blobs are sustainably congested**

Average blob count per block is pegged to the blob target for at least 10 days. See [anytime](https://dune.com/hildobby/blobs) since Nov 1, 2024.

We’d love feedback on how best to bring BPO forks to Ethereum to safely scale blobs! More details here: https://docs.google.com/document/d/1XpV-5BrC2IuNFpRAjvZ8OXmK2YLIbuFMEZpDzziJTvs/edit?usp=sharing

## Replies

**shemnon** (2025-01-22):

One of the things that help alleviate anxiety when we had difficulty-bomb only forks was to give them a different naming convention, so when people saw “Grey Glacier Fork” their defenses went down knowing it was only tweaking parameters. Marketing matters for stuff like this, as much as we may want to deny it.

I would like to see the EIP proposing the fist such fork (after Pectra) to include a naming convention that can be re-used and aligns with the goals.  Stars and Cities and Geology are taken (and show how effective the branding can be).

---

**philknows** (2025-01-22):

Would definitely be supportive of these types of forks to better serve L2s if the testing shows that the parameters are safe for L1 solo operators. There should be no reason why it would take us up to a year to respond to scaling demands when the need is obviously there. It’s pretty simple to do for Lodestar and can be prepped easily in a release to meet a certain date for inclusion.

---

**TheGreatAxios** (2025-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/protolambda/48/16651_2.png) protolambda:

> g

Is there any clarity/estimates on what the increase in solo staker bandwidth will result in cost wise in the short term?

---

**rolfyone** (2025-01-22):

So this would be more akin to a fork-choice type upgrade where clients need to coordinate, rather than the traditional hard-fork where we have a ton of features…

I think it’s helpful to explore exactly what needs to change overall, as it does appear that we may need to tune this more frequently than the typical fork cadence.

---

**timbeiko** (2025-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I would like to see the EIP proposing the fist such fork (after Pectra) to include a naming convention that can be re-used and aligns with the goals. Stars and Cities and Geology are taken (and show how effective the branding can be).

From ChatGPT:

A simple—and thematically perfect—way to name these *blob‐only* “BPO” forks is to draw on **celestial “gas clouds”** (nebulae, supernova remnants, etc.). These are literally cosmic *blobs* of gas, which neatly parallels the idea of scaling up Ethereum’s blob capacity. It also fits right into Ethereum’s established celestial naming style (constellations, Devcon city + star names) while remaining unique to blob forks.

---

## Why nebulae (or supernova remnants)?

- They are cosmic blobs of gas
Nebulae/supernova remnants are some of the closest real‐world analogies to “blobs” in outer space: large, diffuse expansions of matter.
- They keep you within the “stars/space” naming tradition
Ethereum has often used constellations, star names, or cosmic themes. Nebulae and supernova remnants are a natural extension.
- They convey the idea of scalability & expansion
A nebula often leads to star formation—it’s a place of growth and new beginnings in astronomy. Likewise, BPO forks increase Ethereum’s capacity and open new possibilities for rollups.

—

Here are five **funkier‐sounding** nebula names, in alphabetical order. They’re all real cosmic gas clouds with memorable, “blob‐friendly” vibes:

1. Boomerang (Boomerang Nebula)
2. Flaming Star (Flaming Star Nebula)
3. Medusa (Medusa Nebula)
4. Tarantula (Tarantula Nebula)
5. Witch Head (Witch Head Nebula)

Each name is short, distinctive, and plays nicely into the cosmic “cloud”/“blob” theme for your BPO forks.

---

**ralexstokes** (2025-01-23):

i like this a lot!

a minor point, but we may also want to keep track of the `BLOB_BASE_FEE_UPDATE_FRACTION` parameter along with the blob limit and target parameters.

raising the target implies changing this update fraction given the way the blob fee market works today if we want changes in the target to have smooth impacts on the blob base fee

---

**wjmelements** (2025-01-23):

Why not manage the blob gas limit like the block gas limit, where each block gets to vote them up or down?

---

**nixo** (2025-01-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/protolambda/48/16651_2.png) protolambda:

> There is growing consensus  around 50Mbps download and upload speed for solo stakers not using MEV-boost

I have to push back against the consensus around this number. Median home upload bandwidths available in many very urban locations around the world are below this. Observing just a few from [Ookla’s speedtest global index](https://www.speedtest.net/global-index):

- New York City: 36.14 Mbps
- Los Angeles: 21.56 Mbps
- Helsinki: 46.28 Mbps
- Berlin: 22.65 Mbps
- Rome: 46.83 Mbps
- Brussels: 27.77 Mbps
- Buenos Aires: 42.96 Mbps
- Vienna: 32.38 Mbps
- Montreal: 51.18 Mbps
- Dublin: 47.30 Mbps
- Rome: 46.83 Mbps

Given that the U.S. is particularly poor in this regard and that Rated estimates 38% of nodes are operated in the U.S., and that these numbers are medians (so many people are below), I suspect that an assumption of 50 Mbps will result in a not-insignificant number of home stakers struggling and quietly shutting down their nodes.

My own node would certainly need to be shut down if the upload bandwidth requirement were increased to 50 Mbps.

---

**pauldowman** (2025-01-26):

I don’t think “average” is what matters. What matters is what’s available for a reasonable cost. Those are median numbers, so by definition half of all internet users have more than that.

As a home staker myself I don’t have the same internet as the *median* household in my town, yet it’s still quite affordable.

I don’t think requiring stakers to have something on the high end of home internet is a thread to decentralization.

---

**jflo** (2025-02-21):

Much of the data cited above comes from areas where telecom services are monopolized. It is not a matter of staker budget, but staker location and market access.

BPOs are a good idea, and a capability we should have. The comparison to difficulty-bomb forks is fair. We should have this capability, but I don’t think we are ready to use it yet.

