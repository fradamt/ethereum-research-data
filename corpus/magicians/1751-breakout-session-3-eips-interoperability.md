---
source: magicians
topic_id: 1751
title: "Breakout Session #3: EIPs & Interoperability"
author: boris
date: "2018-10-31"
category: Protocol Calls & happenings > Council Sessions
tags: [council-of-prague, eip-process, eea]
url: https://ethereum-magicians.org/t/breakout-session-3-eips-interoperability/1751
views: 1048
likes: 0
posts_count: 3
---

# Breakout Session #3: EIPs & Interoperability

I was the facilitator & scribe. Here’s the [HackMD](https://hackmd.io/fkYo2geVRvCQFfOb22_Ulw).

A lot of the discussion ended up revolving around Ethereum Enterprise Alliance (EEA) inter-operating with EIPs. Action items are at the bottom, to be turned into Github issues in relevant repos.

---

?? Brazil

- Genisis Block VC fund
- university

Sam / Aion

- AIP process
- modeled on EIPs

Chelsea

- open source
- Spankchain – community education
- newcomers be a part of the process, non tech have a voice
- EIPs going somewhere

Chaals

- work for EEA
- long background in W3C

Thor

Bryant

- freelancer
- helping clients understand technology
- Vyper EVM languages
- education through EthSecDevs

Brooke

- open source – distributed systems and FP
- generally a big fan of specs
- specs are even better than open source

Dan

- standards team at Pegasys
- like Chaals, active in W3C, and some at the IETF

Cyrus

- work at Splyt
- autonomous teams / organizations and scaling them
- part of the open source community – excited to bring my skills, and scaling to this space

James

- New Zealand blockchain economics think

Alex

- Consensus
- Working with EEA
- getting people using open model
- interested in open source model

MP

- work at Golem
- working towards an indsitution of incluseion

Amber

- Clovyr dev tools
- permissioned and public chains
- involved

Bob

- been involved with ETH for 3.5 years at EF, Consensus

Gary

- crypto 5 years
- EF in Switzerland
- interested

## EEA

Amber

- Ethereum Enterprise Alliance
- Heavy focus on permissioned
- Also bridging to public
- Everything around using in business – throughput, privacy, etc.
- Common industry providers

Alex

- not much was produced initially other than discussions
- reformed
- industry groups – use cases, happenings, create requirements
- in addition to requirements to clients – message formats, and specs how
- called Special Interest Groups (SIGs)
- on the other side is tech focused groups – what are some baseline things we need to figure out, identity, off-chain trusted execution
- Technical Specification Working Group
- Main product towards a specification of what an Ethereum client must be capable of doing to be considered Enterprise grade, and then on top industry specific – e.g. healthcare might need encryption
- whole goal is an entire spec – everyone is focused on the spec

Chaals

- client spec v1
- open source the specs layer
- we will have a version 2 of the spec
- will have a spec for offchain trusted computing – taskforce has Golem, iExec, Intel, IBM, etc.
- need a process for building the spec
- we had a starting point – then revisions pushed out
- consensus based process – find a bit of the spec that is rubbish / sub optimal – make a proposal – proposals get shopped around a working group
- when they get consensus – EEA has a formal voting system – if you have to have a vote
- spec on private Github
- except when published specs

Amber

- discussion about tech specs – supposed to be default to be open
- technical discussion to be more public?

Chaals

- will keep pushing for it to be open
- various things connected to member organizations
- EEA is trying to push ahead with things that are important
- want to base this stuff on Ethereum – base it on public Ethereum – get engineer in, they already know it from the open
- compatability has business value
- some of those extensions are things that will never get into public Ethereum
- people will want to have a number of things in public ethereum, permissioning
- figuring out how we work in a way, that change will be in public ethereum
- much better than public world going in one way, and EEA another direction – want to converge
- how do we do that?
- various ideas – we should do this an EIP

Alex

- did biz dev for Consensus
- serious lack of education
- people think Enterprise Ethereum is a thing – rather than interoperability
- Quorum is rushing to take improvements from Geth, etc.
- Enterprise should be participating
- been in these conversations

Chaals

- Pantheon / Pegasys at Consensys – Java Based
- Public first and then go Enterprise

Chelsea

- close everything and better solutions

??

- why not better closed rather than open?

Bob

- Vice Chair on Tech Committee
- everything on technical should be public – but went the other way

Amber

- Amber was arguing
- concern is that if you want them to make EIP
- if people don’t feel incentivized

### Describe EIPs / ERCs Process

Boris

- describes

Alex

- not timebound?

Brooke

- EIPs vs. ERCs
- ERCs are simple – as the author, can make FINAL CALL
- Then ACCEPTED
- If no one implements, too bad
- As the author, can make it as ACCEPTED
- EIPs – even if accepted, needs to be implemented

Bryant

- with ERCs less people involved
- EIPs have more editors

Chaals

- AllCoreDevs – all clients active?
- how many?

60 EIPs vs ERCs?

Will look for real data

54 core

Boris

- EIPs / ERCs

ABI Spec

Vyper compiler

Non standard proposals

JSON RPC

AMber

- Mainnet connects? Maybe 2 or 3
- Dozen clients – Enterprise ethereum

Chaals

- our interest to have a standard

Don

- speak to protections against patent trolls
- one of the reasons for being a member of EEA is for patent protection

Boris

- not aware of anything

Chelsea

- isn’t patents trolling?

Chaals

- enterprise would prefer no patents

Boris

- explain

Brooke

- Apache has a patent covenant
- Outputs of this ring
- Should there be a license that applies?

Thor

- wondering, if EEA members worry that it isn’t accepted?
- I don’t think we need new licenses – doesn’t exist in the web sphere?

Chaals

- W3C went through a process of developing a patent license through their prose
- built a patent policy – was controversial
- if you want to put something in the spec, you can’t patent (patent covenant)

Chaals

- work out how to make a proposal
- possibility is you submit an EIP, do it in parallel
- discussions in private and public

Amber

- legitimate concerns
- any proposal from enterprise may add bloat
- concern that they will die in EIP
- then you end with ego
- looks like they failed

Chaals

- is a real issue
- won’t do it because they’re nervous
- my company has this idea, submitted it, get yelled at by public people
- strong disincentive for individuals who are afraid
- AFAIK no one has taken a proposal and put it in as an EIP

Bob

- something comes both ways
- talked to Hudson (EF AllCoreDevs project manager)
- have a process, can have specs that are better

Amber

- “not our problem” --> not just enterprise should have funds
- not two teams

Alex

- vision for Ethereum?
- expression of vision
- hand slapped around “we”

Chelsea

- for eons open source has done emotional labour that have been co-opted
- then people have to pay

Boris

- long answer to there is no “we”

Amber

- tried to push through EIPs
- approached by EF and tried to push it out
- the process didn’t go forward, lots of people fighting
- meritocracy is an illusion

Alex

- point of EIPs is that it needs to be deployed on public net?

Bryant

- if community believe that it adds to the use cases

Brooke

- there are people who want nothing to do with corporation

James

- moving at lightning speed
- maybe code isn’t being put in (specs)
- blockchain POCs are 80% failing

Chaals

- if it looks irrelevant to public chain – no point
- doing standards work is expensive
- don’t do it if there is no value
- we believe there is a real use case for mainnet
- if proposed contributor believed that
- if EEA was running a mainnet process and a private process
- counter-example: lots of requirements for mainnet clients – don’t need to do PoW
- turns out lots do – that aspire to run on mainnet – making it a requirement

MP

- no core devs here
- is this political?
- if enterprise has an EIP, nothing happens, because you have to pull strings, there might be other actors
- also because it takes dev into a political
- maybe we need to think about other ways to have representatives

Brooke

- we’re doing lots of analysis of why nobody trusts each other? what’s a next step

Jason

- working with large enterprise
- change that is incentives
- when considering interoperability
- the point is to have the same access – whoever they are
- additional changes to EIPs, then needs will grow exponently
- shouldn’t think about enterprise in a way that benefits them

Chaals

- biggest enterprise are very big – the smallest are quite small
- politics happens when you put people together
- optimize for getting work done
- concrete things
- have a look through enterprise issues – can ask other members
- let’s pick out which might be an EIP
- I would like to see EIP process – figure out a patent policy

Alex

- curious to enterprise to articulate what more could get on to mainnet

??

- what is the size of the gap? what is cool?

Amber

- maturing some of the privacy pieces
- precompiles for zkSNARKS

Chaals

- permissions are smart contracts on network
- what does it take to decide to work on mainnet

Chelsea

- nothing optimizes for politics as opacity and closed systems

Dan

- implementing part of the community that have talked privatey
- will be either beneficial to mainnet or not
- no more or less important than other members

Amber

- non controversial piece is privacy
- EEA has enough contentious on the inside – it’s just as hard on the inside as bringing it to public
- more and more questions about who benefits from improvements

Chaals

- also the case, because it’s an individual act
- will be a pain – let individuals

Amber

- literally as a corporate employee
- the EEA as whole could publish

Chaals

- could get a rough list

Alex

- if orgs or individuals make contributions
- then EEA could be a proxy
- hire some on the EIP process – owner to help push forward

??

- Would be great to share not all lists
- rather than rejecting or accepting the whole list

## Topics

### Review and examination of EIP process

EIPs (things that clients must implement) vs ERCs (standards and templates such as ERC20)

DISCUSSED

TO DO

- canonical reference, or perhaps a companion HOW-TO in the Scrolls Wiki or ETHhub?
- Could do with more promotion – why should you EIP, why you should track EIPs, etc. etc

### Do we need more editors?

What should editor do and what not? How do we help ensure that people who submit EIPs get feedback? Many EIPs vs. limited EIPs (AKA Boris vs. Nick)

### How can we better identify and sort EIPs based on their content

i.e. if you have an interest in following Wallet specific EIPs, how can you find all of them and track their progress? See this thread from a current discussion.

### Should we decentralize a EIP process?

as proposed in this thread and in this thread?

### How does the Enterprise Ethereum Alliance (EEA) or other groups inter-operate with the EIP process?

How do EIPs / the Ethereum ecosystem interoperate with other standards processes? (W3C? BIPs or other pan-crypto standards? etc.)

PARTICIPATE IN THE OPEN

## Action Items

### Document

### New License / Contributor Agreement for EIPs for Patent Protection

Needs to go beyond CC0 and add protection against patent trolls

EEA interest in this topic

Need to file this as an issue (probably in EIP repo) and see who might take this on

### JSON-RPC as EEA test case, working together

Connections TBD, [@boris](/u/boris) will take this on, further discussion during DevCon session

Infura might be able to support

EEA test case

### List to be shared with public

Chaals to look at getting an EEA list of top items that might make it into EIPs

### Problems outside YellowPaper

Various things that are under specified to be identified (eg JSON-RPC from above)

## Replies

**boris** (2018-10-31):

From the EIPs / EEA session, we emerged some new items to move forward.

(1) Suggest contributing tests along with EIPs (2) Whisper and (3) DevP2P need a better, more formal spec; (4) EEA needs a public descriptor of its governance model / interfaces.

---

**boris** (2018-11-09):

The JSON-RPC work is moving forward, with a first call planned here https://github.com/spadebuilders/community/issues/15

Please add yourself to that thread / suggest agenda items.

