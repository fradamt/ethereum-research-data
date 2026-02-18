---
source: magicians
topic_id: 766
title: EIP standards Process - 2:30pm saturday july '18
author: GriffGreen
date: "2018-07-17"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-standards-process-2-30pm-saturday-july-18/766
views: 1221
likes: 5
posts_count: 6
---

# EIP standards Process - 2:30pm saturday july '18

The notes were much better organized, with nested hierarchy in: https://docs.google.com/document/d/1-wK7HHeupaDrRjZmeWRkzvxgEdnCGCqBhRvGAUnUu7w/edit?usp=sharing

Open questions and comments from the crowd:

- Need for documentation
- who has the authority?
- LIP process for livepeer, what are the challenges that exist with EIPs? Scaling challenges? Improving signal vs noise.
- Splitting protocol and application layer process
- Splitting into standardization working groups
- Scuttlebutt p2p community has no formalized process, how do we go from standard to implementation, while staying decentralized
- How do eips decrease duplication and effort, background, how much is explicitly documented?
- PIP wants to learn from it, plasma has things that can be added to the EIP list… what makes a good EIP?
- Layer2 proposals
- QIP is excited to model after EIPs… trying to be a non-org and develop a culture of the experts, to allow more people to participate.
- Coordination scaling, social scaling, setting processes in place that have scaling in mind. How have other projects succeeded and failed?
- IDEAS! HA! Adapted for execution. There is work that we do that could be moved upstream to EIPs, but we aren’t confident with our works

Organized notes:

Separating the EIP process into different pieces

- Core things go to core devs
- Python vs IETF
- Interface RPC, contract layer, Consensus layer
- Consensus should require pull requests to the Yellow Paper.
- Applications should have working groups
- Interfaces (JSON RPC) get a lot less press and
- LAST CALL ends the process

Modeling other processes

- Layer 2 (and other working groups) heading upstream to get their needs out of layer 1
- For example, having chain introspection
- Where do we draw the line?
- We could have a nice light weight process that include working groups
- Application layer standards often don’t need changes up streams but they piggy back off the EIP standard
- HTTP is only a meaningful standard if people choose to use it… but its still useful to use it
- 721 was funny, cryptokitties have a shitty standard, and then the first project deploys it with a shitty standard and the original thinkers lose their credibility in pushing the standard discussion
- Token standards in NFTs… there is an army of people trying to standardize tokens
- What happens when other languages come into the mix?
- Standards use the ABI not the language.
- We should focus on standardizing what happens on chain for data availability, then do libraries
- There is an ODB layer, then there is the applications
- The databases here are contracts
- The crypto items standard 1155
- different tokens of different types and making them all easy to group and move

Defining what makes something EIP-able

- This is something that was better defined in the BIP process.
- The process for contracts is different then the process for core protocol changes
- RPC interface would be nice to standardize
- Debug trace transaction gives you back different
- Ethsign, private sign, both work different ways in different clients
- Standards are really focusing on documentation
- Does it need to come out of working groups?

Social scalability

- Putting out requirements is really important and it should be part of the process upfront
- Using the fellowship group to standardize might help
- WORKING GROUPS!!
- Token Working group, ScalingNOW! Etc.
- Authoritative groups that have smaller scopes
- Creating Working groups will help the process
- Only the people that care need to watch
- Helps organize processes around each unique groups needs
- Editors need to certify the working group
- Working groups can be forked
- Everyone can follow a unique standards process
- So you have working group last call, then you push to the editors who do the EIP last call
- Editors become certification agencies for working groups???
- It would be nice if working groups that are can be pointed to as the authority as types of standards
- These are the editors
- Greg Colvin
- Nick Johnson (@arachnid)
- Casey Detrio (@cdetrio)
- Hudson Jameson (@Souptacular)
- Vitalik Buterin (@vbuterin)
- Nick Savers (@nicksavers)
- Martin Becze (@wanderer)
- How do we form working groups?
- What are the minimum requirements?
- No standards, but some structure would be nice
- Working groups earn their authority and legitimacy.
- People can circumvent it but if the important stakeholders are listening to a specific working group it will be hard for them to get their standards
- Working groups can interrupt the final call if someone does circumvent them… you have this filibusters
- TCR ? Signalling?
- Experts make people shy
- IETF is hierarchical … but can we push things out?
- It’s important that Everyone can follow a standards process
- There is a website !?!!? https://eips.ethereum.org/
- EIP-1 https://eips.ethereum.org/EIPS/eip-1
- LET’S HAVE A BLOG OFF!
- SHOULD THINGS BE CURATED? NICK (curation) VS BORIS (accept all correctly formatted eips)?

## Replies

**boris** (2018-07-17):

I can’t believe I agreed to a BLOG OFF…

---

**GriffGreen** (2018-07-17):

hahahaha! Good luck! and sorry for the break in chatham house rules wanted to have accountability for that one ;-D

---

**boris** (2018-07-17):

We were a little loose on that (that [@mattlock](/u/mattlock) guy kept taking pictures!). But I think the non-digital room was good.

Good luck with your leg! But I see it is resulting in great note uploading so…

---

**GriffGreen** (2018-07-17):

hahahah it delayed the notes uploading honestly. finally getting back into the swing of things

---

**RiganoESQ** (2018-10-12):

hi griff, can u expand on what u mean in these points (they are most critical and would help going forward):

- 721 was funny, cryptokitties have a shitty standard, and then the first project deploys it with a shitty standard and the original thinkers lose their credibility in pushing the standard discussion
- Token standards in NFTs… there is an army of people trying to standardize tokens

-greg

P.S. ello

