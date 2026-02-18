---
source: magicians
topic_id: 1688
title: Ethereum 2.0 Roadmap session
author: mariapaulafn
date: "2018-10-28"
category: Protocol Calls & happenings > Council Sessions
tags: [council-of-prague, consensus-layer, ethereum-roadmap]
url: https://ethereum-magicians.org/t/ethereum-2-0-roadmap-session/1688
views: 2073
likes: 13
posts_count: 7
---

# Ethereum 2.0 Roadmap session

Details here --> https://hackmd.io/Lagu29aMSaKRVT6BeodMKg

We would really appreciate if you could post your notes in this thread.

## Replies

**5chdn** (2018-10-28):

Thanks Maria! Thanks!

---

**boris** (2018-10-31):

I believe [@mariapaulafn](/u/mariapaulafn) is going to turn this into a nicely formatted Medium post, too, but I want to make sure that we have notes “on platform” here, so pasting in from HackMD.

---

ETH2 Github Repos

- https://github.com/ethereum/eth2.0-specs
- https://github.com/ethereum/eth2.0-pm – equivalent to AllCoreDevs, this is where meetings and calls and notes are handled in issues
- https://github.com/ethereum/eth2.0-tests

Afri:

- estimated timeline?

Danny:

- lot of client teams here working on it

Paul G

- Sigma Prime – building ETH2 client called Lighthouse
- first mistake – getting up and giving a timeline for a sw project! (laughter)
- very difficult to plan
- March next year (2019)
- multiple teams working in a decentralized manner

Lane:

- what is the biggest thing that could take longer?

Paul G / Sigma Prime

- can’t think of an unknown – if we come across a problem with the spec

Lane:

- what is Parity’s perspective

Afri:

- we are excited – have a proof of concept
- built on top of Parity Substrate
- we are even more far away than other teams, because we joined later
- parity is a bit more conservative implementing new specs

Afri:

- cross client test net
- need a new test net that isn’t proof of work

Jaciek / Nimbus Status Client:

- ETH2 is not just the beacon chain
- execution, working out sharding, a whole different world
- two specs merged – I see March as a PoC, validate some assumptions
- Give out to community to start tearing apart

Danny:

- targeting first half of next year, is going to pressure us to get the spec in line
- serialization formats, wire formats – some things that are outside of the spec

Jaciek:

- a push gives a target to work against
- give rest of community something to play around with

Lane:

- in Council of Berlin
- lots of questions about core, roadmap
- what is the roadmap? does anyone control it? how is it maintained?
- everyone up here is core?

Vitalik

- public HackMD file
- recently moved to Github as of Sept 20

LANE: What is the Ethereum roadmap?

Danny:

- ever evolving as needed
- any one version can say what it is

Vitalik:

- first documents – Ethereum Whitepaper
- then around March 2015 Vinay Gupta, blog post – Ethereum Launch Process
- Frontier Homestead Metropolis Serenity
- Switch to PoS in Serenity
- Implemented 5/8ths of that vision
- After Homestead delayed by DAO
- Metropolis split into Byzantine, new things of pre-compliles, then Constantinople, and possibly other small hard forks
- and then Serenity – move to Proof of Stake
- this was something floated as an idea, since the beginning
- ideas around sharding developed and tacked on over time
- I feel like there always has been this impression – keep on upgrading and improving the protocol
- getting PoS finished
- scalability through sharding and other improvements
- before 2017 much less clear, then CasparFFG
- hybrid PoS, sad to see it go because I wrote it
- realized it make more sense that PoS and sharding with beacon chain would make more proof of stake
- where do they live? Between blog posts, EthResearch, end of last year, home for research discussions, that’s where a lot of the protocol discussions happen
- some point was a spec in HackMD, that was moved to Github, when we’re past editing it every week
- at this point, proposed changes, will live in issues and PR in the repo
- replacing withdrawal time period with withdrawal rate max
- github issue and EthResearch thread
- most abstractly – goes back several years
- EthResearch defacto home for that – changes to CasperFFG, proof of custody, cross shard transactions
- Eth2 is fine grained

Afri:

- what is the timeline for eWASM?

Vitalik:

- soon?
- eWASM will be the VM for the shard chains

Vitalik:

- retire the VM
- important to reduce complexity

Jamie: What is the currency of ETH2

- how is that considered by the community?

Vitalik:

- make deposits on beacon chain withdraw to shard
- ether on PoW chain to shard chains
- intention to
- don’t feel like anyone has fully decided

Paul:

- same ETH as current chain
- agree with moving it on to shards

Jaciek

- when applications move over
- affects which eth is eth – where value in ETH2 comes over
- that’s up to each application to decide when to move

Paul:

- you never have to move
- majority might

Bryant:

- tools, have a solid toolset for EVM
- eWASM has new opportunities around LLVM
- not clear to me how we can be ready to go with the tooling ready to go

Vitalik:

- eWASM as a backend for Solidity
- Vyper

Greg:

- eWASM and EVM is like an argument
- community seems to be conflict averse
- at universities and for profit companies – technical arguments can become very conflictual
- and then you go to the bar together
- professors hiring people so they can have someone to argue with
- the aversion to conflict causes more conflict
- from early on we’ve had an EVM to eWASM tool, that you can compile VM to
- as Bryant says, we have a toolset that is growing
- the longer it takes to get ETH2, the more EVM code is out there
- and if people ask me, how do you write high value contracts – and we have contracts with $Ms of dollars in value
- I would first write a formal specification, and then write the program in assembly, and then prove that the assembly implements the specifications
- and leave high level compilation out of it – trust as many tools as possible
- can do the same thing with eWASM, once it exists
- we don’t know how long that will be
- if we try and deprecate EVM1, we are going to create a lot of complexity for people who are using it to get work done
- well, we’re writing in Solidity so they have to recompile – because lots of people hired people, and now their contracts just work – no desire, no money, to hire somebody to port their contracts
- we’ve put them in a position

Bryant:

- creates a barrier to entry to ETH2
- on top of learning sharding, the new beacon chain

Greg:

- doesn’t mean eWASM shouldn’t be the base of things
- can’t just abandon what we have
- have to keep evolving what we have
- talking to other development teams – yeah, we’re working with EVM1, has some problems, wouldn’t be hard to fix

[@Ethernian](/u/ethernian):

- account abstraction?

Bryant:

- time to restructure data structures – different asset trees?

Vitalik:

- abstract nonces vs abstracting signatures vs. (something)
- This concept has been discovered but not totally thought through yet.rough y
- (some text missed)

---

Danny:

- earlier there was the sentiment of not doing work on EVM
- I think that we do have time to coordinate on forks on the next 2 years
- that’s Danny’s opinion
- think that good idea that EVM is functional and improved

Greg:

- EIP615 and others implemented on Aleph CPP

Lane:

- is there more than one Ethereum roadmap?

Danny:

- parallel

Greg:

- From the beginning I’ve said there is nothing technically keeping us from making EVM1 run at any speed
- From what I hear, the problem is that we don’t have the technical competence to do so. But we have a very large community and a lot of money
- I don’t have a problem with eWASM but I don’t think it’s necessary. But if that’s where the group, sobeit

– missing notes –

Greg

Casey

- parallel between eWASM and EVM
- why can’t we just improve EVM?
- easier to just switch to eWASM because so much tooling available
- (Bryant: not for smart contract use case)
- ideally main chain just upgrades and its cheaper gas price for everyone – but that’s possible in theory
- EVM was developed for the usecase of smart contracts (solidity, serpent), but not for the use case of computing complex cryptographic functions
- I disagree with Greg on that EVM is proper place to improve for this use-case. It seems like this is the much harder path than to go with EWASM

Greg

- I could see an idea of having parallel compilers, one that is more economical (slower) and one that is much faster. But in the current spec, EWASM needs to be validated on the EVM

(missed some notes)

Ethernian (here is the question I had, but failed to ask clearly):

“Do you think the governance (especially release workflow) should be part of ETH2 specification? May be as some kind of “release game” ?

IMHO, most security deficits we have, are not in the math or software but in workflow and governance.

[As an example I would mention a bitcoin bug fixed hiddenly and nobody have ever noticed that the patch doesn’t match the bug description](https://twitter.com/el33th4xor/status/1043592906857168897). It means our assumptions about release audits made by community are not realistic and that means huge security risk.”

Lane

- Please, if any of this is going over anyone’s heads, feel free to stand up and let us know.

Boris

- E2specs and ethresear.ch are now the primary forums for discussing compiler research and where decisions are being made
- What about EIPs?

Danny

- In my opinion, we’re a little to early for a formal EIP process
(lots of missing notes)
- I would say that there is no theoretical problems on PoS

Vitalik

- There’s a lot of little issues, but that’s all
- The nice thing about the roadmap is that because it’s in phases, so not everything is dependent on phases, so not everything else
- The role randomness plays in roadmap: the way the protocol has been designed does not require secure randomness. Attacker can’t roll back even a single block
- Randomness completion is nice but not necessary

Danny

- Randomness comes from RanDAO
- Contractual method for randomly determining who gets to submit a block
- Mechanism for vbalidators to participate on beacon chain, which reveals the randomness for the next “round”
- Can say that RanDAO is biasable. We do have people researching to harden and propose strong randomness

Vitalik

- Immature blockchains: one guy makes a block, next guy makes a block and chooses another block to build on, another guy makes a block and chooses a block, etc
- Problem with PoS is that if you can predict who will be making the blocks ahead of time (e.g. I know in a span of twenty, I’ll make 15)

Marek

- Question: Would it make sense to do more evolutionary/iterative approach with lots of small hardforks

Vitalik

- That’s kind of it. Start with beacon chain and then other small steps

Danny

(missed comments)

Lane

- We definitely need help with Project Management on roadmap. Open call (even if you have less technical skill)

Ryan

- Eth2.0 goal is to be live during WWIII

Casey

- Is it okay to compromise on that goal? If the world is falling apart, why do we need this?

Etherian

- Does this fall into a blanket question of governance? Should we make governance a part of Eth standard? Actually more formal?

Boris

- can you clarify?

Etherian

- I feel like we don’t have governance as a standard. Think of last Bitcoin hack, there was no governance to find and discover it. Huge security

Boris

- More about hardfork?
- I’ll redirect, how do you coordinate consensus among clients to determine which forks?

Danny

- Right now it’s still pretty early
- Research is still primarly EF, but we’re seeing more from Parity, Status, Pegasus, etc.
- It’s really more of a coordination problem
- I don’t know if we’re moving too fast or two slow.

Vitalik

- If all researchers that retire tomorrow, is the research they’ve done satisfactory for Eth2.0?
- We’re not there yet, some areas where a little more research is valuable. Even on L1
–question from Etherian-- how do we test PoS in situation there is no actual value at stake?
- We could launch a beacon chain with small intervals (only for the data layer) in real time to get technical information.

Question from audience

- How do current ERC20 contracts fit and migrate to 2.0?

Vitalik

- If you have contract for simple, short-lived interactions, just copy/paste onto EWASM and phase one out
- Could be centralized airdrop or script that burns coins on one side and mints them on another side
- Non-financial dApps can just move really quickly
- Solidity in many cases will compile to eWASM
- Could stay on 1.0 chain until it eventually folds into 2.0 chain, in which case it will require some client-side work.
- Could make light client for 2.0chain that fits into 1.0 chain
- Ultimately, this research is something we’d be interested in giving research grants for.

---

**mariapaulafn** (2018-11-02):

Hi! will be transcribing and working on this over the weekend. I spoke with Danny and he told me he would be happy to review and add stuff if needed ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

My raw notes here: [Ethereum 2.0 Q&A session - ROUGH NOTES, NOT READY FOR PUBLISHING - HackMD](https://hackmd.io/40GyFWQSSpyP9D6Zj8NUIg)

---

**mariapaulafn** (2018-11-05):

Ordered and decently readable notes on 2.0, already rolled all Boris’ notes and added some stuff from the dialogue transcript, sent to Danny Ryan and to Lane to add more stuff.

And will also share on social media for anyone that wants to add more.


      [docs.google.com](https://docs.google.com/document/d/1gUlXNC4qKN6f4tXMN6qNmsee3Ce5D3Kbgbh183yYkdc/edit)


    https://docs.google.com/document/d/1gUlXNC4qKN6f4tXMN6qNmsee3Ce5D3Kbgbh183yYkdc/edit

###

Ethereum 2.0/ Serenity Q&amp;A session at ETHMagicians Participants: Danny Ryan (EF), Vitalik Buterin (EF), Afri Schoedon (Parity), Paul Hauner (Sigma Prime - Lighthouse TODO LINK) , Greg Colvin (ETHMagicians), Jacek Sieka (Status - Nimbus TODO LINK),...

---

**lrettig** (2018-11-27):

[@mariapaulafn](/u/mariapaulafn) thanks for putting this together! Great resource. Added a few edits.

---

**mariapaulafn** (2018-11-28):

Thanks Lane! the doc now lives in medium but ill post here too.  https://medium.com/ethereum-magicians/demystifying-the-road-to-ethereum-2-0-8130ade8d00f

