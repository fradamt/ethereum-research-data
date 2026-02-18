---
source: ethresearch
topic_id: 12097
title: Divide Systems of Ethereum to Improve Decentralization
author: ctrl-alt-lulz
date: "2022-02-23"
category: Architecture
tags: []
url: https://ethresear.ch/t/divide-systems-of-ethereum-to-improve-decentralization/12097
views: 1661
likes: 2
posts_count: 3
---

# Divide Systems of Ethereum to Improve Decentralization

Unavoidable facts

- running a validator without a cloud provider is not scalable or cost efficient at the individual level and is operationally complex (eg. maintain uptime, avoid slashing). It’s not realistic IMO that this goes away within the next 10 years. Large and reliable cloud infrastructure has an overall positive impact on network performance for all participants. They’re economically driven to do so.
- a system such as MEV, has already caused centralization of clients to Geth, and adds substantially to expected rewards. running an MEV validator post merge is the economically rash decision

Current state of slashing

- economically very operationally complex to run and costly and the rewards are so low it doesn’t even come close to covering the operating costs
- depending on how many slashers running, one or two concurrent major cloud outages could potentially create windows in the network where slashing is not enforced. or if the identity of all the slashing monitors on the network is known, a targeted attack could also be a risk

Instead of trying to solve decentralization diversity at all levels, I propose segregating less operationally complex, but still economically important parts of the system to allow for greater decentralization of power.

Here are some systems we could adjust, to start the discussion.

1. MEV (post merge, assumes knowledge about flashbots architecture)

- running builders and relayers of MEV requests via flash bots post merge can be run by individuals and requires trust of actors in the chain.

1. Slashing/Enforcement

- can be expanded to verifying trust of MEV eg slashing bad relay and builder participants, and grow to enforce any new systems (unknown needs of the future)
- if the rewards mechanism is changed and more slashers are run then a “slasher” can be assigned a network section (a range of validators) to watch per given epoch (just one example), instead of having to monitor every validator. or can be assigned a different security mechanism

MEV and slasher components could require a less onerous Eth staking amount, or could require staking some new ethereum governance token created/ICO-ed to allow new and smaller participants to play a vital part of the system as well as derive rewards.

Please share thoughts/concerns/suggestions. Hope to hear from you all!

## Replies

**pietjepuk** (2022-02-25):

I’m not saying there aren’t centralizing forces (I agree that MEV and post-merge tx rewards are), but…

> running a validator without a cloud provider is not scalable or cost efficient

Can you break this down down for me? I know there are countries without sufficient internet speeds, but otherwise I would say it very much is cost efficient to run one at home.

> at the individual level and is operationally complex (eg. maintain uptime, avoid slashing).

If you’re not comfortable with running a system 24/7, that’s fine I guess. I wouldn’t say it’s “operationally complex” though. What is hard in your opinion about maintaining uptime? What is difficult about avoid slashing?

> Large and reliable cloud infrastructure has an overall positive impact on network performance for all participants. They’re economically driven to do so.

Reliable, sure, but large? Could you elaborate, because the incentives are in place to penalize more heavily if the outage affects a large number of validators in parallel.

> economically very operationally complex to run and costly and the rewards are so low it doesn’t even come close to covering the operating costs

Could you elaborate what you mean by “economically operationally complex”? Does it cost a lot of money to run, or is it difficult to run one because you need a lot more knowledge compared to running a validator? I’m interested to hear your answers, because from what I’ve seen and experienced first-hand, it’s very little overhead.

---

**ctrl-alt-lulz** (2022-02-25):

Hi Pietjepuk. Thanks for your questions. Here is some additional context that should answer your questions.

1. Recommended specifications

These hardware specifications are recommended, but not required to run the Prysm client. I would assume that you’d really want this to be solely dedicated to running your staking client.

Processor: Intel Core i7–4770 or AMD FX-8310 or better

Memory: 16GB RAM

Storage: 100GB available space SSD

- from a quick non-exhaustive search
 a computer meeting these requirements is around $500+ (best buy). setting up cheaper ways to run it takes greater technical savvy, which is not common and therefore exclusionary
 average worldwide annual income is ~$18k/year, more than 2/3rds of the world population lives on less than $2 a day (https://www.bbc.com/news/magazine-1751204)

Internet: Broadband connection

- around 15% of the world’s population has broadband access



      [Our World in Data](https://ourworldindata.org/internet)



    ![](https://ethresear.ch/uploads/default/optimized/3X/2/9/2990056c78eedfe412537097da079513da41f80b_2_690x362.png)

###



More than half of the world is online, but the Internet is still young.










1. Requirements for validation

- 32 ETH (today is $88k, avg about $100k over last 6months or so). It’s a volatile asset, so only those who can afford to wait can really hold this or supply it

1. Understanding how to do anything in computing beyond the very minimum basics is a very large barrier. Even knowing how to use a crypto wallet is actually pretty uncommon. Much fewer people know how to use docker, a terminal, what curl is, how to navigate linux, what a shell script it.

here’s the easiest way to run a prysm validator


      ![](https://ethresear.ch/uploads/default/original/2X/3/39a1c38cf2015d89aee4b9ebbae8c6c2aec0b8e1.svg)

      [prysm.offchainlabs.com](https://prysm.offchainlabs.com/docs/install-prysm/install-with-script/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/4/2/4255b0ce256e3a283f6d91d977c14813fceb7a89_2_690x364.png)

###



Step 1: Review prerequisites and best practices










now all you need to do is understand this, how to configure it correctly, understand the architecture (beacon, validator)

what happens if your SSD becomes corrupt, or the DB file is corrupt? you need to sync from scratch. now you’re offline for a week. what happens if you lose your computer due to a natural disaster like a hurricane, fire, or being in an area of conflict (like ukraine). or if you have a prolonged electricity outage.

https://launchpad.ethereum.org/en/checklist

how many people can honestly understand anything related to ports/firewalls, linux time syncs.

From [ethereum.org](http://ethereum.org) directly:

Recommendation disclaimer

Hardware suggestions are an ever-evolving target. Current minimum requirements are likely to increase by an order of magnitude after the merge and introduction of shard chains. Do your own research before depositing funds.

so now your $500 investment initially could no longer be enough to support a client, and you need to be on top of replacing hardware yourself over just selecting a larger cloud instance/resource on AWS etc.

1. updating your clients to account for changes in the network

let’s say someone did get through all those steps. now all they have to do is figure out how to modify their configurations to support the ethereum merge, and then do this again for sharding. also if you don’t upgrade your client quickly enough, eg not being aware of upcoming hardforks, your version of prysm, etc would not work at all. or if a security patch is needed, you again need to be aware and proactive.

1. changing to a new client

let’s say you’re unsatisfied with prysm and want to change your client. doing this incorrectly is one of the most common ways people get slashed. why would you even try if you aren’t very technically savvy

![](https://ethresear.ch/user_avatar/ethresear.ch/pietjepuk/48/6807_2.png) pietjepuk:

> Reliable, sure, but large? Could you elaborate, because the incentives are in place to penalize more heavily if the outage affects a large number of validators in parallel.

with node providers. eg large crypto staking focused companies. an AWS outage, etc, already has mitigation steps and engineers who can execute this. Eg. moving validators across regions or cloud provider.

