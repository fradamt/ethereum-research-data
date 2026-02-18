---
source: magicians
topic_id: 3625
title: "Constrained Resource Clients: September 2019 Update"
author: shazow
date: "2019-09-05"
category: Magicians > Primordial Soup
tags: [light-client]
url: https://ethereum-magicians.org/t/constrained-resource-clients-september-2019-update/3625
views: 1138
likes: 3
posts_count: 2
---

# Constrained Resource Clients: September 2019 Update

Hi friends,

DevCon is coming up soon, but let’s do another update thread and get people excited for what’s coming up!

*Quick recap:* We’re talking about Ethereum clients that can run under constrained resource conditions, such as on phones or browsers or embedded devices or even [on-chain inside a contract](https://ethereum-magicians.org/t/eth2-in-eth1-light-clients/2880) or shard runtime!

### Request for updates from each participating project:

- Short summary: What is your project and its goal? (This can change over time)
- Roadmap now: What is the currently working and available to try?
- Roadmap next: What is being worked on over the next few months?
- Current challenges and concerns: Do you need help with anything? Are there unknowns you’re accounting for that could be nailed down by another participant?

### Participants

Please post an update as described above.

Some pings/callouts based on previous participation: (Should I start removing projects from this list if they don’t provide updates repeatedly?)

- Denode: @noot ChainSafe ansermino
- Diode.io @dominic
- Go-Ethereum (LES/ULC): @zsfelfoldi
- Infura: @ryanschneider egalano
- Mustekala : @dryajov
- Slock.it : @CJentzsch
- Status: @mandrigin
- Vipnode : @shazow
- WallETH: @ligi

If you’re hit with a link/mention limit, format the excess ones in plaintext.

If you’d like to join this list, please go ahead and post your update and I’ll make sure to explicitly include you next time.

## Replies

**dominic** (2019-09-06):

### Short Summary

[Diode](https://diode.io) a its core is a) finality gadget with an Ethereum block header change and b) enabled by that a super-light protocol & client for constrained devices to allow them to read contract state data and validate the corresponding merkle proofs. The finality gadget and algorithm are based on BlockQuick. It is gateway-free but requires a block header change, so at least a hard fork.

On top of that the Diode network defines incentives and additional features for data transfer of IoT devices – Think of it as a native integration of Swarm incentives into the consensus. We’re having a hard look at Swarm work and design decisions as well. The ultimate goal here is to put together a decentralized Ethereum based backend for serverless IoT devices. We’re prototyping all of this off-chain in our own experimental Ethereum client.

### Roadmap: Status

1. Released the BlockQuick paper: https://eprint.iacr.org/2019/579
2. Started turning ethereum client, embedded clients, smart contracts open source: https://github.com/diodechain
3. Have running a tiny development network, for demos and testing.

### Roadmap: In Progress - Get Hackable

We’re focused now on making the system easily onboard-able for server-less IoT. Specifically to support maker work (Arduino, RPi, ESP32). The goal is to have this done for October around Devcon5

- Write simple steps and tutorials.
- Filling the cracks, making simple use cases simple to do.
- Faucet for the devnet
- Propose EIP for binary data ABI, so that EVM-less small devices can read smart contract data from guaranteed slots.
- Testing

### Roadmap: Next - Testnet

- E2E Encryption for traffic service. Settle on secure traffic protocol Swarm/Signal/other.
- Release full Diode whitepaper including super light client incentive structures and services.

### Roadmap: Future

- Commercial Application for IoT devices

### Challenges and Concerns

- ETH1 vs. ETH2 brings a lot of changes that directly affect BlockQuick, some of them good, some we don’t know yet.
- The idea that there might be EVM-less clients, has some implications on how to use and query storage. We feel this is currently not well discussed within the Ethereum community. (See EIP milestone above)

That’s it for now. See you guys in Osaka!

