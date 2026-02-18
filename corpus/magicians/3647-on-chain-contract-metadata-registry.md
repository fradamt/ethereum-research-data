---
source: magicians
topic_id: 3647
title: On-chain contract metadata registry
author: ligi
date: "2019-09-11"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/on-chain-contract-metadata-registry/3647
views: 972
likes: 3
posts_count: 8
---

# On-chain contract metadata registry

anyone knows about a on-chain contract metadata registry? I imagine a registry contract where deployment keys of other contracts can publish metadata. The registry should support swarm and ipfs hashes. With metadata I mean ABI, contract source, icons, contact options,  …

I really do not want to start another project currently - so asking if perhaps already people working on such a thing. Could really use it now and think I am not the only one.

Perhaps leveraging dType (cc [@loredanacirstea](/u/loredanacirstea))

## Replies

**rumkin** (2019-09-13):

https://www.ethpm.com/

Don’t know much about this project. Only know they are working on a solution.

---

**ligi** (2019-09-15):

Thanks for the hint! I knew about the ethpm manifest part - was not aware of the on-chain part. Looks like this is going in the right direction - just not sure about the “multiple registry” part - with this (as far as I see) we would need a registry of registries …

---

**rumkin** (2019-09-16):

Why IPFS and Swarm? It increases technical debt on management. Not sure if regular users are ready to support both networks. For me Swarm is not an option at all. It requires to have an Ethereum node to setup, what makes the whole process overcomplicated. In the same time IPFS requires no setup, just download and run.

Am I missing something? I’m planning to build a package system into a browser and decided to refuse Swarm and to use IPFS instead.

---

**ligi** (2019-09-16):

swarm would be nice for availability guarantees in the future. Currently e.g. I could not retrieve some IPFS links in some of the ethpm registries. If noone pins them then this is a problem.

Also swarm would be great as e.g. some links in evm bytecode are swarm-hashes. Another reason is that one would not have to run 2 different p2p networks. A lot of reasons to (also) support swarm - but I agree practically IPFS seems to work a (bit) better currently…

---

**rumkin** (2019-09-16):

Guarantees? Could you elaborate? Does it mean that EVM code will be able to check hash existence, or write data directly to swarm?

---

**gh1dra** (2019-11-21):

[@ligi](/u/ligi) After iterating on a few different approaches for an on-chain registry, I just wrapped up hacking together this: https://github.com/gh1dra/eth-metadata-registry.

Should have the functionality you’ve specified, would love any feedback/suggestions you may have! Also interested in how dType could leverage this as well. Next steps would probably be to create a dapp to present everything nicely

---

**ctzurcanu** (2020-02-04):

[@ligi](/u/ligi)  dType has this covered since March - April 2019: [EIP-1921: dType Functions Extension](https://eips.ethereum.org/EIPS/eip-1921)

With this, we can call any registered function while inside the EVM (just by knowing the dType id of the function and providing the correct input). Many other features (including function search) will be demoed soon ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) .

