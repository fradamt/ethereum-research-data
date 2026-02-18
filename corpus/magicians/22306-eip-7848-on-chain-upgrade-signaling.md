---
source: magicians
topic_id: 22306
title: EIP-7848 On-chain upgrade signaling
author: fulldecent
date: "2024-12-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7848-on-chain-upgrade-signaling/22306
views: 4886
likes: 3
posts_count: 5
---

# EIP-7848 On-chain upgrade signaling

Discussion topic for EIP-7848

#### Update Log

- 2024-12-22 First draft

#### External Reviews

None as of 2042-12-22

#### Outstanding Issues

- Discuss if should use extraData (128 bits of it) or add a new field in every block

## Replies

**abcoathup** (2024-12-24):

Community signaling via validators support for a network upgrade is an interesting step towards more decentralization.

Rather than a specific software version (which would include an activation epoch/timestamp), voting support for an upgrade Meta EIP might be simpler.  e.g. [EIP-7600: Hardfork Meta - Pectra](https://eips.ethereum.org/EIPS/eip-7600)

Timing wise this could be done during upgrading of public testnets (generally a few weeks between each testnet).

In practice changing to a two stage upgrade process could significantly delay upgrades (at least the first time this was done).  As an example we are waiting for validators to signal to a gas increase of 36M which core developers are supportive of.



      [gaslimit.pics](https://gaslimit.pics/)



    ![image](https://raw.githubusercontent.com/nerolation/gaslimit.pics/36591db90f6193f48261c0a0b035f505d378c05b/assets/previewimage.png)

###



Detailed insights on Gas Limit Signaling.










An alternative approach would be for validators to signal a veto.  For example Optimism has bicarmel governance and citizens (badgeholders) can veto an upgrade. [I am a badgeholder]

---

I wouldn’t say that network upgrades are decreed by the EF.

EF protocol support help coordinate network upgrades with core developers.

All core devs calls are currently moderated by people working at the EF.

EIPs in an upgrade are decided by rough consensus of core developers.  ([EIP-7723: Network Upgrade Inclusion Stages](https://eips.ethereum.org/EIPS/eip-7723)).

Client teams specify which versions of their software supports a network upgrade.  This doesn’t depend on an “official” blog post on the EF blog.

---

**fulldecent** (2024-12-24):

EF uses decree to upgrade clients, this is evidenced by using this language on their blog:

> The Ethereum network will be undergoing a scheduled network upgrade

Additionally it is evidenced by the fact that they own the trademark and assert to prevent any other upgrade of the network from calling itself “Ethereum Mainnet”.

“Assert” may sound like strong language here, but that is the default effect of trademarks, and they have declined many opportunities to undo that effect as documented intext.

---

Using a SHA-256 hash for one will guarantee that an implementation exists and that multiple people are referring to the same thing.

This is as important step in software assurance.

---

As for speed, it is possible that EIP-7848 [PRE-DRAFT] would allow upgrades to happen *faster*. This is because it includes inside it a mechanism to fail.

Currently the deployment strategy for EF does not allow failure.

Previously a software change was announced on the blog and aborted for security concerns with approxmately 24 hours notice. This was a dangerous thing. But abortion could have happened automatically with our new approach here.

---

---

---

At the moment I am working to get this to draft status. All these issues are worth discussing and the draft is good enough to discuss, so I hope this can please go to draft.

---

**abcoathup** (2024-12-25):

I suggest focusing this EIP on upgrade signaling and removing the section about trademark.

To merge the draft requires an editor to review (which I am not).

---

**yorickdowne** (2024-12-28):

This EIP seems to start from false premises. EF does not determine the content of a hard fork, ACD does. In a public process, to which anyone can weigh in. The next hardfork, Pectra, took a good 12 months to arrive at the scope.

This included a period where concerns were raised about the fate of home staking, data was gathered, and code introduced to reduce the bandwidth load.

At the very least, an EIP to be included in the protocol aught to fairly describe the way governance works. There are multiple places in the EIP that would need to be changed, including the part that speaks of “the core software”, which seems misleading with 12 clients and counting.

I realize that’s a hill the author may be willing to die on.

To the idea of signaling upgrade readiness. I can see some merit, but here as well, I don’t think the EIP is well written.

It states that a validator that does not upgrade and continues running will get 100% of their stake slashed, 16 ETH (sic). That is just not so. They’d be considered offline from the viewpoint of the network, the exact same situation as if they turned the node off. Also, what’s with 16 ETH being 100% of the stake. 100% of the stake of a validator is 32 ETH.

The consensus threshold in this EIP starts at 51%. That’d be catastrophic, it’s exactly the kind of chain split embarrassment that an EIP such as this should want to prevent. At 51% neither side finalizes, each inactivity leaking the other.

Given the current governance structure, with an open process that anyone, including stakers, can weigh into, what could upgrade signaling get us? It could avoid a chain split when this governance process fails.

Without this EIP, node operators that run validators have a final vote for a hard fork by upgrading their software. If they don’t, the upgraded portion of the network considers them offline. If governance breaks down - that is, during the lengthy ACD process, dissenting voices didn’t speak up or weren’t heard - then we could see the chain no longer finalizing, if the portion of the network that wants to upgrade is greater 1/3rd but under 2/3rd, or we see the old chain still finalizing, if the portion of the network that wants to upgrade is under 1/3rd.

That’d be an embarrassment, and the >1/3rd scenario is also a financial hit for the un-upgraded portion of the network, through the inactivity leak.

With this EIP, node operators that run validators have the same vote, but now a breakdown in governance would just not have the upgrade happen, avoiding the embarrassment of such a chain split. Arguably only at a threshold of 70% or higher, and better 95%.

The assertion that currently, Ethereum cannot be forked, and with this EIP, could be, makes no sense to me technically or economically. Technically, forking is a huge endeavor, and comes with non-trivial costs for client maintenance, and likely trade offs for amount of clients maintained. Economically, a forked Ethereum is its own token and would get price discovery by the market, with or without this EIP.

Overall, this EIP is a bit of a mess. It doesn’t reflect the technical reality of Ethereum (the slashing part; maybe the reference to “core software”), the governance / political reality of Ethereum, or the economic reality of Ethereum (the forking part).

