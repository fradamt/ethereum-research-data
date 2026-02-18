---
source: magicians
topic_id: 2084
title: Highlighting the other standards & specs that make up Ethereum
author: boris
date: "2018-12-01"
category: Magicians > Process Improvement
tags: [json-rpc, standards-adoption, eip-1474]
url: https://ethereum-magicians.org/t/highlighting-the-other-standards-specs-that-make-up-ethereum/2084
views: 1948
likes: 5
posts_count: 10
---

# Highlighting the other standards & specs that make up Ethereum

I just made a [PR against the EIPs repo to list other specifications that make up the Ethereum network](https://github.com/ethereum/EIPs/pull/1632).

Being able to create an Ethereum client is more than the Yellow Paper. Highlighting the location of all of the relevant pieces that make up running the Ethereum network is important for implementors and to help in understanding how and where changes and upgrades are made.

I am proposing that relevant standards used by the Ethereum network be linked from the README of the EIPs repo, thus helping in discovery of these other locations and their maintainers.

In addition, I would also propose that these other standards and specifications have a minimum of 2 maintainers identified and listed.

I haven’t yet added those maintainers in this PR, but if people can help identifying them and they volunteer to be “official” maintainers, we can add them.

Here’s the contents of the PR:

---

# Standards and Specifications

Aside from improving and upgrading the Ethereum platform, the goal of the EIP process is to document the standards and specifications that define it. Following these specifications, an implementation team should be able to build interoperable components that connect to the Ethereum main net, various test nets, and other layers of the Ethereum network.

The list of Ethereum components is as follows. Each component may have a different process for maintenance and updates, but will create or update EIPs to reflect breaking changes and current canonical versions.

- Formal Specification for Ethereum / EVM https://github.com/ethereum/yellowpaper, complimented by the Jello Paper https://jellopaper.org/
- DevP2P https://github.com/ethereum/devp2p/
- API/JSON-RPC https://github.com/ethereum/wiki/wiki/JSON-RPC
- Contract ABIs https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI
- Interfaces repo https://github.com/ethereum/interfaces
- Light Ethereum Subprotocol https://github.com/ethereum/wiki/wiki/Light-client-protocol
- Whisper https://github.com/ethereum/go-ethereum/wiki/Whisper-Overview
- Swarm https://github.com/ethereum/go-ethereum/pull/2959

---

For reference, there is a group forming around the JSON-RPC interface.

[#1474](https://github.com/ethereum/EIPs/issues/1474) is the in progress EIP to do an initial specification, created by [@bitpshr](/u/bitpshr), who has also agreed to be one of the two initial maintainers.

We had an [initial call this past week](https://ethereum-magicians.org/t/json-rpc-specifications-and-testing-community-call-nov-27th-2018/2031) that has more details. We have created a [separate repo as a home for the spec going forward](https://github.com/spadebuilders/ethereum-json-rpc-spec).

There are a number of groups looking to extend the JSON-RPC API, and next steps would also be about looking at the process for proposing those extensions. The JSON-RPC API can potentially be upgraded without waiting for hard forks, although there could be breaking changes that affect middleware providers (web3js, ethersjs, etc.) that are widely used.

cc [@Arachnid](/u/arachnid)

## Replies

**Ethernian** (2018-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> I am proposing that relevant standards used by the Ethereum network be linked from the README of the EIPs…

I see the problem you would like to solve, but I have to disagree fundamentally with your approach, [@boris](/u/boris).

It assumes there should be an **official list of relevant standards** used by Ethereum and to be used by ethereum based projects. Yes, Whisper and Swarm are a “official” part of Ethereum, but does it make them better choice for the projects?

Swarm itself have decided NOT to use “an official” whisper and created own PSS. So far about usage of one “official part of Ethereum” by another “official part”.

Swarm itself is not ready and will be replaced by IPFS in praxis. Even when it will be ready, it is uncertain that it will be the best available technology for all the cases. So should Swarm be “official” technology? IMHO, not.

Trying to make an list of relevant standards in EIPs repo, we will make it “official one” despite whether it fits changing requirements and if it becomes successful projects. Why should we prefer Swarm over IPFS in the list? Is it just because we thought some years ago we will use Swarm as part of Ethereum to store the chain data and host the DAPPs? But the things are changing, we have new technologies like Plasma coming.

Another aspect: Who will decide on the list? Is it an EIP Editor? If yes - it will greatly reduce an inclusivity of ethereum ecosystem.

I see the problem you would like to solve, but any “official list” of ethereum standards can not be used without usecase requirements in mind. But if you will take care about requirements, you should have both Swarm and IPFS in the list, but **EIPs is a bad place for that**.

I believe the right way is to have Reference Architectures created for particular set of requirements and utilizing best technology available (even if it is not a pure Ethereum). As an Architect, I would prefer any working non-ethereum technlogy over an “official”, but still-in-development one.

---

**boris** (2018-12-02):

Whisper is debatable, as is Swarm, since neither is required to connect to main-net.

Everything else is required to make an interoperable main net client. That’s the goal - bring together all the required specs, maintain them, and how to coordinate changes to them.

As an example, the Yellow Paper is currently “under maintained”. The Jello Paper and Beige Paper are more useful for implementors. Which of them should be considered the canonical specification?

Who decides: EIP editors plus anyone in the community until rough consensus is reached. Which means that I might just turn this into an “Informational EIP” as someone suggested on GitHub.

---

**Ethernian** (2018-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Whisper is debatable, as is Swarm, since neither is required to connect to main-net.

This is exact the way of thinking I would like to have changed!

Whisper and Swarm are not only that debatable cases. I doubt even ABI standard “is required to make an interoperable main net client.” because there is no ABI on the EVM level.

Main-net connectivity and consensus relevance should not be ONLY the criteria to decide what is Ethereum and what is not. Any list of relevant Ethereum technologies is welcome, but EIP process in its actual version is wrong place for that. Current EIP process is too focused on Core Client development, led by Core Dev Editors, while huge value of Ethereum depends on ecosystem outside the Core.

We should extend and decentralize EIP process first before we try to press the whole ethereum universe into it.

More reasoning [I have made here](https://ethereum-magicians.org/t/decentralizing-eip-workflow/1525) (sorry for shameless self-reference).

Once more, I would support any approach for “*Highlighting the other standards & specs that make up Ethereum*” but not as part of current EIP process - it is not suitable for this global task. It will be either ignored or will hit development dramatically.

---

**boris** (2018-12-02):

You’re essentially saying — if I understand correctly — that a wider set of standards needs work and that it needs to broaden beyond EIPs. Sure.

I understand your point of view. I am personally focused on making compatible core clients for now, which requires valid specifications.

Where the line is for ABIs or JSON-RPC is debatable. Having them well specified is valuable.

The only specifications that are going to get done are those where maintainers sign up and work on it. So we’ll see on which of them we can get to rough consensus. It will start with doing work.

Consider this my signaling that I am going to do some of this work.

---

**Ethernian** (2018-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> … that a wider set of standards needs work and that it needs to broaden beyond EIPs.

My points are:

1. Don’t make some existing parts of ethereum “more official” than others. Only usage should decide on it, not an “official endorsement”. Any technology listings should not be “official”. EIP is quite official.
2. Don’t insist on management of non-Core parts of ethereum in current EIPs process. Non-Core is something, that CoreDevs will not implement in their Clients. Current EIP Editors are Core Devs and they should not manage everything.
3. I see creating of specifications, lists of standards and technologies as a task for Architects and would support any efforts there. This is because these documents are necessary to decide on architectures.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Consider this my signaling that I am going to do some of this work.

I am interested to be part of the process and would like to learn more about how to create specifications.

---

**boris** (2018-12-02):

Great. Numbered form is useful.

(1) You don’t think ABI or Whisper are Core. But the Yellow Paper and JSON RPC are OK. Please give feedback on which are “non Core”.

(2) how exactly specs evolve is undetermined. In part up to the maintainers of each spec. There are EIPs today for certain specs. Editors mainly edit. I see them helping to determine consensus, and taking feedback from working groups / maintainers. Since these specs can evolve / upgrade outside of hard forks, they can move through consensus more quickly.

(3) it’s the work of everyone that wants to build compatible implementations. Pick a spec, identify the maintainers, give feedback on what needs to be changed/ updated.

---

**Ethernian** (2018-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> (1) You don’t think ABI or Whisper are Core.

No. It was not my statement. I see Whisper and Swarm as “officially pre-selected” messaging and storage solutions now, but I doubt this official endorsement is a good thing. Whisper is not used by Swarm and the Swarm is still not production ready. I suppose inclusiveness and friendly competition would bring more benefits and is more healthy than a sticky pre-selection.

Personally, I am trying to avoid statements what is Core and what is not. It is just because I am not a CoreDev. **Generally I would avoid to define responsibilities for others. Anyone should decide only on stuff he is working on:** CoreDevs (not me!) should define Core technologies, Wallet Devs (not me!) should define their Wallet technologies, and so on. If for example Core Devs will see Whisper as official Core Tech, I have nothing against it, but I would expect they should take care about its compatibility to other Core parts **first**. If they don’t care, they should not make Whisper “official”, otherwise we become a nice gap between official statement and the real state.

All in all: I see only one rule to determine what is Core Tech and what is not:

Have Core Devs provided a standard implementation in their clients and ready to maintain it? If yes - it is Core Tech, if not - it is third party.  Whisper looks like third party soft currently, ABI looks like Core.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> (2) how exactly specs evolve is undetermined. In part up to the maintainers of each spec. There are EIPs today for certain specs.

I will completely agree with you if EIP process will become more decentralized and not owned by CoreDevs (and EIP Editors) for EIPs they will not take care about.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> (3) it’s the work of everyone

for sure. I don’t make exclusive claims.

---

**Ethernian** (2018-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> (1) Don’t make some existing parts of ethereum “more official” than others. …  EIP is quite official.
>
>
>
>
>  boris:
>
>
> (1) You don’t think ABI or Whisper are Core.

Better wording:

(1) is not about what is in the Core and what is not.

My appeal was: if you make some technology “official”, you make other “less official” or “undesired”. Ethereum is a swarm of strong and independent players, like Parity, ConsenSys, Status, Gnosis and so many others. Making “official endorsements” will split the community.

---

**boris** (2019-01-10):

I’m abandoning the PR to the EIPs repo, I just put a MAINTAINERS page on the Ethereum wiki https://en.ethereum.wiki/maintainers

