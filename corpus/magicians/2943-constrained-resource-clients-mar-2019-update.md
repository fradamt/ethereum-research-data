---
source: magicians
topic_id: 2943
title: "Constrained Resource Clients: Mar 2019 Update"
author: shazow
date: "2019-03-18"
category: Magicians > Primordial Soup
tags: [light-client]
url: https://ethereum-magicians.org/t/constrained-resource-clients-mar-2019-update/2943
views: 1645
likes: 3
posts_count: 5
---

# Constrained Resource Clients: Mar 2019 Update

Hi friends,

Let’s do another update thread!

*Quick recap:* We’re talking about Ethereum clients that can run under constrained resource conditions, such as on phones or browsers or embedded devices or even [on-chain inside a contract](https://ethereum-magicians.org/t/eth2-in-eth1-light-clients/2880) ![:open_mouth:](https://ethereum-magicians.org/images/emoji/twitter/open_mouth.png?v=15).

### Request for updates from each participating project:

- Short summary: What is your project and its goal? (This can change over time)
- Roadmap now: What is the currently working and available to try?
- Roadmap next: What is being worked on over the next few months?
- Current challenges and concerns: Do you need help with anything? Are there unknowns you’re accounting for that could be nailed down by another participant?

### Participants

To all projects mentioned: Please post an update as described above.

- Denode : @noot ChainSafe ansermino
- Go-Ethereum (LES/ULC): @zsfelfoldi
- Infura: @ryanschneider egalano tueric
- Mustekala: @dryajov
- Slock.it : @CJentzsch
- Status: @mandrigin
- Vipnode: @shazow
- WallETH: @ligi

If you’re hit with a link/mention limit, format the excess ones in plaintext.

If you’d like to join this list, please go ahead and post your update and I’ll make sure to explicitly include you next time.

## Replies

**shazow** (2019-03-18):

### Short Summary

[Vipnode](https://vipnode.org/) is building an economic incentive for running full Ethereum nodes which service light clients. It works by providing a coordinator (a vipnode pool) which connects paying clients with participating hosts.

### Roadmap: Now

Vipnode v2.0 release happened last month ([announcement blog post](https://medium.com/vipnode/vipnode-2-0-released-9af1d65b4552)). The demo pool is still running on mainnet nodes but using Rinkeby for payments. I’m not in a position to run a mainnet payments pool right now, but I’m very open to other people trying it.

- Instructions to try it here: https://github.com/vipnode/vipnode#quickstart
- Recent blog post: https://medium.com/vipnode/vipnode-2-0-released-9af1d65b4552

### Roadmap: Next

There is a growing collection of ideas for a v3.0 milestone, but the current challenge is funding this project. Feels like financial support for non-ETH2.0 projects has died down since the end of last year.

I’m not sure I’ll be able to continue work on Vipnode for now as I’m figuring out what to do for money this year.

But hypothetically, these are things I’d want to focus on if I were able to continue working on Vipnode:

- Support for ULC (ultra-light clients), which was merged into Geth.
- Add “mini-Infura” support to pools which provides a web3-compatible JSONRPC endpoint that gets loadbalanced between hosts, and metered similar to clients (so you can use something like MetaMask as a client without running a light node).
- Add more ops and infrastructure-management features to vipnode, such as monitoring (alerts from the pool if your nodes go down), host-to-host peering (if you’re running a bunch of hosts), per-node analytics.

### Challenges and Concerns

- Financial support for Vipnode is a problem. I have a Gitcoin grant setup for Vipnode which is appreciated and partially covers ongoing maintenance costs, but not enough to continue advancing Vipnode.
- In general, it’s not clear that timing for Vipnode is good right now. The network utilization is still low, and light clients are still not standard in any mainstream client. I’m sure there will come a time when it makes a lot of sense, and hopefully we’ll be in a good position for it when it does. Infrastructure/ops features seem like a better timely focus for now.

(Any questions/suggestions are welcome, by the way!)

---

**lrettig** (2019-03-18):

Random question: does doing things inside of a zero-knowledge proof count as resource constrained? ZK-SNARKs and STARKs, for instance, are still very limited in terms of the sorts of computations that can be performed within their circuits.

---

**shazow** (2019-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> does doing things inside of a zero-knowledge proof count as resource constrained?

If you’re asking whether that’s relevant to this working group, then I’d qualify the constrained resource *clients* part. If someone is building an Ethereum client implementation that executes inside of a zero-knowledge proof (![:open_mouth:](https://ethereum-magicians.org/images/emoji/twitter/open_mouth.png?v=12) ![:open_mouth:](https://ethereum-magicians.org/images/emoji/twitter/open_mouth.png?v=12)) then yea, totally.

---

**dominic** (2019-03-28):

### Short Summary

[Diode](https://diode.io) is a project focused on complementing internet PKI with certificate pinning in Ethereum blockchains, making mechanisms such as ENS available to constrained IoT devices, it’s initiated and run at Exosite an IoT company to fix some of the long-standing PKI issues.

At its core is the ability to connect constrained devices to an Ethereum blockchain to allow them to read contract state data and validate the corresponding Merkle proofs. The algorithm we developed coined BlockQuick is a gateway-free reputation based method for embedded devices to get a trustable understanding of a relatively recent block. We haven’t published the full paper yet, as we’re still looking for an independent reviewer - so please hands up if anyone has the time.

### Roadmap: Status

The Diode Proof-of-Concept is functional but also work in progress. It comes in two parts

1. Full Ethereum Node, but modified in block headers, node-to-node, and node-to-edge protocols.
2. Light Client (go) running on a raspberry pi.

### Roadmap: In Progress - Proto

- Get the BlockQuick paper reviewed and published
- Improve PoC implementations to include Light Client incentive structure

### Roadmap: Next - Testnet

- Release full Diode whitepaper including light client incentive structures
- Release Testnet & Sources
- Port the Light Client to C and onto a real embedded device

Device Targets: Arduino, Embedded Chip, e.g., CC3220, Mobile Phone

### Roadmap: Far Future

- Commercial Application for IoT devices

### Challenges and Concerns

ETH1 vs. ETH2 brings a lot of changes that directly affect BlockQuick, some of them good, some we don’t know yet.

- Signatures in Beacon chain are a good thing, something we’re having right now to add in our ETH1 variant. Though changes of consensus group and quick block authorship changes might be an issue for the reputation system, this needs further investigation.
- BLS vs. ECDSA looks like a huge step. Usage if BLS signatures could also for the light client protocol have significant advantages but the maturity of BLS seems still very low and before embedded devices will have hardware accelerated BLS support is likely going to be a couple of years.

