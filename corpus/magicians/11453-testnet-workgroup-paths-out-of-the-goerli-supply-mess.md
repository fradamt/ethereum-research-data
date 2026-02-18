---
source: magicians
topic_id: 11453
title: "Testnet workgroup: Paths out of the Goerli supply mess"
author: q9f
date: "2022-10-25"
category: Magicians > Primordial Soup
tags: [testing, testnet, testnets, infrastructure, goerli]
url: https://ethereum-magicians.org/t/testnet-workgroup-paths-out-of-the-goerli-supply-mess/11453
views: 10572
likes: 46
posts_count: 29
---

# Testnet workgroup: Paths out of the Goerli supply mess

Good morning.

After the Merge and Devcon lying behind us, it’s time to address the Goerli testnet Ether supply issue.

Problem statement:

- Goerli only has 115M GoETH total supply

Goerli is the only/main testnet for testing validator setups
- Circa 80-90% of the total supply is in “circulation” or locked in deposit contracts
- Goerli has been traded OTC since 2021
- Cannot test validators on Sepolia (permissioned)
- Cannot test validators on Ropsten (deprecated)

Difficult to test beacon-chain validators currently

I would like to kick off an open discussion on potential paths going forward to address the situation. Please leave a comment with thoughts or join our next community call to go over some of the issues:



      [github.com/eth-clients/goerli](https://github.com/eth-clients/goerli/issues/129)












####



        opened 10:43AM - 25 Oct 22 UTC



          closed 05:52PM - 01 Nov 22 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a16f40cbe4b618b7bc9b7246c471f28c4af32b99.jpeg)
          q9f](https://github.com/q9f)










### Goerli Testnet Community Call #6

Date / Time
- Tuesday, November 1st, 20[…]()22, [3 pm UTC](https://savvytime.com/converter/utc-to-germany-berlin-canada-toronto-ca-san-francisco-china-shanghai-india-mumbai/nov-1-2022/3pm)
- Jitsi: _snip_
- Discussion: <https://ethereum-magicians.org/t/testnet-workgroup-paths-out-of-the-goerli-supply-mess/11453>
- Meeting minutes: https://github.com/eth-clients/goerli/issues/129#issuecomment-1298896603

Agenda
- Post-merge testnet situation: Ropsten, Goerli, Sepolia
  - context: <https://ethereum-magicians.org/t/og-council-post-merge-testnets/9034>
  - context: <https://www.youtube.com/watch?v=1UtcvVve32A>
- Goerli testnet supply issue
  - issue: Goerli OTC trading
  - issue: faucet hacking/draining
  - issue: huge GoETH demand to test staking setup
  - consequence: stopped handing out goerli ether
- Potential paths going forward
  - custom testnet protocol
    - #97
    - #101
    - withdrawals? `WITHDRAWAL_BOOST_FACTOR` idea by @parithosh
  - new ephemeral testnet
    - Holešovice idea
    - reset every X months on a given date
    - needs commitment by client teams and infrastructure providers
    - testnet for stakers by @taxmeifyoucan
      - https://notes.ethereum.org/@mario-havel/stakers-testnet
 - preserve state in a regenesis event
   - precedence? feasibility?

All developers, contributors, and volunteers are invited.












Ideas floating around so far:

- custom testnet protocol

GöeIP-001: Set Balance of 0x552fCB6425a1eD22696c967E741C3bC49c52c338 to Ninety-two Quintillion Ether · Issue #97 · eth-clients/goerli · GitHub
- GöeIP-0002: Set Validator-Balances to Ninety-two Quintillion Ether · Issue #101 · eth-clients/goerli · GitHub
- withdrawals? WITHDRAWAL_BOOST_FACTOR idea by @parithosh

new ephemeral testnet

- Holešovice idea
- reset every X months on a given date
- needs commitment by client teams and infrastructure providers
- testnet for stakers by @taxmeifyoucan

Testnet for stakers - HackMD

preserve state in a regenesis event

- precedence? feasibility?

## Replies

**greg** (2022-10-25):

Thanks for kicking this off, will help however possible!

---

**wmitsuda** (2022-10-26):

Replicating what I had already suggested on twitter: https://twitter.com/wmitsuda/status/1582624228213657601

> Keep deprecating and bootstraping new goerli and sepolia in alternate years to educate people that testnets can be discarded and testnet eth is valueless, give initial allocation to known set of reputable community members, faucet admins, etc, for redistribution

That would “only” require new chainspec deployment/removal from clients every X months, no custom testnet protocol development effort. Infra providers possibly happy because testnet chains will be always small and eventually thrown away after some period of time.

---

**chrishobcroft** (2022-10-26):

Some thinking was done around solving for Görli’s “empty faucet” problem (amongst others) as part of the [Holešovice](https://devpost.com/software/holesovice-testnet) project at ETHPrague in June 2022 (winner of “Sustainability” prize).

The concept of “ephemeral” testnets was discussed, and here I share some of my thoughts from those discussions:

I see many pros of having ephemeral testnets, any of which I am happy to expand upon if required:

a) to default-sync should be quick, and require less storage because chain will be short.

b) faucets can be initialised with a gazillion `holETH`, solving empty faucet problem, in combination with something like [komputing/FaucETH](https://github.com/komputing/FaucETH).

c) can be initialised with absolute latest L1 codebase, allowing identification of issues sooner rather than later.

d) PoS deposit contract can be auto-deployed at genesis, with pre-deposited Validator keys, to enable the potential for a “clean” post-merge network.

e) genesis config / codebase could be read from previous testnet’s chainstate/Swarm, which could even be governed onchain. This can serve to reduce reliance on e.g. github, in favour of decentralised storage methods.

f) they don’t preclude users from continuing to run them after “official” decommissioning, in case they wish to test longer term features.

g) can serve to create some kind of framework for a “cadence” / “rhythm” to coordinate delivery across the community, e.g. a project can target a release to the testnet launching in December. The duration of the testnets could be divided into agile-like sprints by dev teams, so if the duration were e.g. 28 days, then that’s 4x7day sprints, each sprint 5 on / 2 off (like a “standard” work week). I believe this can prove to be powerful in terms of ecosystem coordination.

h) can work in harmony with long-standing permissionless/permissioned testnets, and indeed provides scope for broader inclusivity in terms of collaboration on base-layer evolution.

Some challenges to this approach however:

i) newly initialised networks would (at first) be without “core” protocols e.g. ENS, GnosisSafe, Maker, Uniswap, Aave, Optimism, Arbitrum, zkSync, Polygon, Livepeer, Swarm, Aragon, ChainLink, Golem (the list goes on and on).

I actually think that this can encourage projects to contribute auto-deploy processes, to make sure that their own protocols are available for others to build on.

This can also serve to greatly improve tooling for local devnets, or for the likes of [scaffold-eth](https://github.com/scaffold-eth/scaffold-eth) i.e. users could pick and choose which protocols they want to have available to use in their dApp, when running `yarn chain`.

ii) harder for e.g. Infura/Alchemy to support, though perhaps a minor issue given a), as it will be muuch easier to run a node with a few GB of storage.

iii) more complicated to keep track of, which is perhaps also a minor issue, requiring a change in the mental model of “how testnets are done”. Some thoughts on this have already been shared [here](https://ethereum-magicians.org/t/ephemeral-networks-and-chain-ids/7674)

Happy to hear of more challenges though, but for now I am bullish on this concept.

To conclude this lengthy post, I believe the prize here is to enable all build environments, whether public testnets or private devnets, to have

1. the absolute latest L1 stuff: merge, verge, surge, purge etc. for users to develop on top of, providing them with early-access to the known benefits of these upgrades, as well as future-proofed foundations for dApps, and
2. all network/L2 protocols, for users to integrate their dApps with, providing them with all the “infrastructure legos” afforded to them by building on the Ethereum network.

---

**remyroy** (2022-10-27):

EthStaker implemented a solution suggested by potuz to distributing Goerli ETH for the purpose of doing your validator deposit to stake on Goerli. That solution enables anyone to stake using a 0.0001 Goerli ETH deposit instead of the regular 32 Goerli ETH. It uses a combination of a Discord bot, a custom launchpad and a proxy deposit contract to provide an experience that is very similar to the full experience someone can expect on Mainnet while deterring farmers. It has been running for 3 weeks now with good success. The process does not need any harsh verification beside having a Discord account. It should be a solution that works for months for the purpose of testing a validator setup on Goerli.

The first major low hanging fruit for any improved permissionless testing network is a much higher ejection balance for validators. Anything close to 31 ETH should help in removing validators who are destroyed or simply not started.

An ephemeral and periodically resetting testnet would most likely be another good improvement.

Some of the goals and needs of a permissionless testing network for testing your validator setup might conflict with the goals and needs of a testnet for dapp developers. It might be worth exploring splitting both of these use cases in different testnets if possible. Sepolia seems like a nice place for dapp developers. It might be worth spending some time to advertise it as the place to be for testing dapps.

---

**taxmeifyoucan** (2022-10-27):

The idea of an ephemeral testnet for stakers came up recently during discussions at Devcon. I agree with points brought up by [@chrishobcroft](/u/chrishobcroft) and find it as a feasible solution.

More details in my recent proposal: [Testnet for stakers - HackMD](https://notes.ethereum.org/@mario-havel/stakers-testnet)

---

**q9f** (2022-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/remyroy/48/14377_2.png) remyroy:

> Sepolia seems like a nice place for dapp developers. It might be worth spending some time to advertise it as the place to be for testing dapps.

I actually gave a talk on this where I recommended to test validators on Goerli (for now) and applications on Sepolia only:

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/039c0c445cc0a1828edcbc55d3b0f876ea459d64.jpeg)](https://www.youtube.com/watch?v=1UtcvVve32A)

The problem is that many application stacks now just started to migrate away from Rinkeby and Kovan *to* Goerli instead of directly skipping to Sepolia. We should have started communications earlier along with the deprecation notice of the other testnets…

---

**yorickdowne** (2022-10-28):

I think I understand now why there’s GöETH demand. Protocols like zkSync bridge GöETH over to L2, where they can be used to mint NFTs like the recent zkApe.

This means that whichever network is the long-running dApp testnet will always be pathological with regards to its token use: It’ll always have some value. Whether it also has scarcity is another question. Sepolia for example is permissioned, which means “stupid amounts of SepplETH” does not create issues re griefing the validator set.

We could sunset - or just restart - Görli and have a continuously refreshed validator testground with “plenty of” testETH, while Sepolia becomes the playground for “rational actors”, our beloved utter degens. The continous, every N months, refresh of the validator testnet gives a strong incentive for dApps to land on Sepolia, so we don’t find ourselves in this same situation again.

We can split the use cases, make testETH not scarce for both use cases, and that should do the trick. We can’t make testETH on the dApp testnet not valuable.

It’ll always hold value as long as people want NFTs: But as long as it’s also abundant, that value is so close to zero as to be indistinguishable from zero.

---

**SnapCrackle2383** (2022-10-29):

Great to see this being discussed. Remy’s solution is good.I’m also in favour of restarting the testnet regularly.

We could approach it another way and every wallet gets 32goerlieth when created so from a user perspective they don’t have to hunting for it to test their validator setup.

---

**remyroy** (2022-10-31):

Fundamentally, testnet ETH has utility. It is useful in the sense that it can be used to perform work and it can be used to store data. The main way to keep it *free* is to have an unlimited supply or keep this perception that it is unlimited. Any friction in trying to obtain testnet ETH for any reason will cause someone somewhere to start assigning a real value and a price to that testnet ETH. This is basic supply and demand.

Unlimited testnet ETH has some cons. One of them being the ability for someone to spam the network and potentially deny others from using it. Another one is the ability, in a permisionless consensus layer, to spin up a large amount of validators and break the consensus layer with different levels of majority in the validator set. There are various ways to deal with a malicious actor who is trying to spin up a large amount of validators and that will be visible many weeks and months in advance with the current activation queue.

The relation between the desire to keep it free and the need to have at least a perceived unlimited supply is a tenuous one. The obvious solutions are to limit supply and/or assign a price above *free* to testnet ETH. A lot of efforts and energy has been spent in trying to limit supply and find a fair way to perform distribution. Even if we like to say that testnet ETH should be free, the most successful methods for distributing testnet ETH right now force a *cost* on the user requesting it: time, CPU, third party verification, etc. An unpopular solution that would likely solve many issues around this would be to assign a very low base price to testnet ETH. It could be something like 0.01 USD per 10 testnet ETH. I suspect there might be even better *cost* or *price* solutions to be explored.

On the supply side, seeding or initializing a testnet with a large amount of ETH, let’s say 1000, in every  wallet address that has ever received or sent a transaction on mainnet or any testnet might be a nice way to seed the distribution. It has a few risks and cons too. It isn’t fair to new developers for instance. It would still need a nice way to distribute new testnet ETH. Faucet distribution is still very hard for any faucet who is going to try to distribution any *large* amount.

---

**q9f** (2022-11-01):

Meeting minutes are on Github:



      [github.com/eth-clients/goerli](https://github.com/eth-clients/goerli/issues/129#issuecomment-1298896603)












####



        opened 10:43AM - 25 Oct 22 UTC



          closed 05:52PM - 01 Nov 22 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a16f40cbe4b618b7bc9b7246c471f28c4af32b99.jpeg)
          q9f](https://github.com/q9f)










### Goerli Testnet Community Call #6

Date / Time
- Tuesday, November 1st, 20[…]()22, [3 pm UTC](https://savvytime.com/converter/utc-to-germany-berlin-canada-toronto-ca-san-francisco-china-shanghai-india-mumbai/nov-1-2022/3pm)
- Jitsi: _snip_
- Discussion: <https://ethereum-magicians.org/t/testnet-workgroup-paths-out-of-the-goerli-supply-mess/11453>
- Meeting minutes: https://github.com/eth-clients/goerli/issues/129#issuecomment-1298896603

Agenda
- Post-merge testnet situation: Ropsten, Goerli, Sepolia
  - context: <https://ethereum-magicians.org/t/og-council-post-merge-testnets/9034>
  - context: <https://www.youtube.com/watch?v=1UtcvVve32A>
- Goerli testnet supply issue
  - issue: Goerli OTC trading
  - issue: faucet hacking/draining
  - issue: huge GoETH demand to test staking setup
  - consequence: stopped handing out goerli ether
- Potential paths going forward
  - custom testnet protocol
    - #97
    - #101
    - withdrawals? `WITHDRAWAL_BOOST_FACTOR` idea by @parithosh
  - new ephemeral testnet
    - Holešovice idea
    - reset every X months on a given date
    - needs commitment by client teams and infrastructure providers
    - testnet for stakers by @taxmeifyoucan
      - https://notes.ethereum.org/@mario-havel/stakers-testnet
 - preserve state in a regenesis event
   - precedence? feasibility?

All developers, contributors, and volunteers are invited.












> thanks, everyone for attending and chiming in and sorry for the jitsi issues.
>
>
>
> ### rough meeting minutes (nov/01/2022)
>
>
>
>
> ##### problem statement
>
>
>
>
>
> huge demand for goerli ether due to testing staker setups (32 ether for each validator)
>
>
>
>
> after testnet deprecation earlier this year, a lot of projects migrate to goerli instead of sepolia
>
>
>
>
> faucets getting drained or hacked rendering the network unusable for many developers
>
>
>
>
> goerli ether being traded otc does make it easier to buy them even though they are free
>
>
>
>
> current situation breaks down into two problems
>
>
> stakers have no easy way to test staking
> developers actually pay money to test their applications
>
>
>
>
>
> ##### discussion of protocol changes
>
>
>
>
>
> custom protocols for testnets have been an issue in the past (see: morden consensus failure)
>
>
>
>
> execution-layer teams are not willing to support a testnet-only fork or custom protocol
>
>
>
>
> there might be a chance to utilize upcoming withdrawals in capella fork on the consensus-layer side
>
>
>
>
> add a constant that introduces a withdrawal boost factor that is “1” on all networks
>
>
>
>
> but can be tweaked for testing or testnet environments (here: goerli)
>
>
>
>
> benefit: trivial to implement (one constant, one multiplier)
>
>
> capella: add withdrawal boost factor constant ethereum/consensus-specs#3073
>
>
>
>
> potential drawbacks: people abusing the queues to deposit and exit the validator set to farm more goerli
>
>
>
>
> at least this would reduce pressure on faucets
>
>
>
>
> another caveat: make sure to not hit the max integer value on any account any time soon
>
>
>
>
> action item: simulate deposits/withdrawals and come up with a good number for goerli to extend life for at least 2 years
>
>
> simulate deposits/withdrawals under constraints of prater with various withdrawal boost factor #135
>
>
>
>
>
>
>
> ##### application-layer point of view
>
>
>
> need long-term guarantees for testnets
> the migration from kovan/rinkeby to goerli was very short notice for many projects
> migration for larger projects is often very involved
> maintaining support for more than one testnet binds a lot of resources
> currently huge demand on goerli, the base fee is around 30 gwei (similar levels to mainnet)
> inflating the supply might also increase the base fee
>
>
>
> ##### proposal to have a “release and support schedule” for testnets
>
>
>
>
>
> launch new testnet every 2 or 3 years, pre-announce and “end-of-life date” (5 years lifetime? tbd)
>
>
> goerli end of life: 2024?
> sepolia end of life: 2026?
> sepolia would be the right place to migrate/test applications
> sepolia is permissionless, has better stability guarantees, and better total supply
>
>
>
>
> 5-years testnet long-term support seems reasonable but for goerli this is still too short notice
>
>
> many projects are migrating to goerli instead of sepolia as we speak
> missed opportunity prior to the merge to communicate clearly the expectations for the testnets
>
>
>
>
> benefits: gives projects long-term guarantees for operation and planning capabilities for future migrations
>
>
>
>
> open question: is there a benefit for applications to run on permissionless networks (concerns about the permissioned nature of sepolia)?
>
>
>
>
> open question: if goerli is deprecated, where to test large validator sets for consensus-layer teams?
>
>
> in general, need to discuss the different needs of application and protocol developers
> there is always a need for a ropsten-like testnet
>
>
>
>
> action item: work out and present a testnet release and support schedule; discuss with community stakeholders
>
>
> testnet release and support schedule #136
>
>
>
>
>
> ##### ephemeral testnet for stakers
>
>
>
>
>
> mario worked out a proposal
>
>
> Testnet for stakers - HackMD
>
>
>
>
> action item: refine this with the home-staker community and map out a launch and maintenance plan
>
>
>
>
> please correct me if I got something wrong or forgot an aspect

---

**q9f** (2022-11-01):

Two immidiate action items are:



      [github.com/eth-clients/goerli](https://github.com/eth-clients/goerli/issues/135)












####



        opened 05:50PM - 01 Nov 22 UTC



          closed 04:07PM - 03 Nov 22 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a16f40cbe4b618b7bc9b7246c471f28c4af32b99.jpeg)
          q9f](https://github.com/q9f)










* https://github.com/eth-clients/goerli/issues/129
* https://github.com/ethereu[…]()m/consensus-specs/pull/3073














      [github.com/eth-clients/goerli](https://github.com/eth-clients/goerli/issues/136)












####



        opened 05:51PM - 01 Nov 22 UTC



          closed 02:18PM - 03 Aug 23 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a16f40cbe4b618b7bc9b7246c471f28c4af32b99.jpeg)
          q9f](https://github.com/q9f)










* https://github.com/eth-clients/goerli/issues/129

> - launch new testnet eve[…]()ry 2 or 3 years, pre-announce and "end-of-life date" (5 years lifetime? tbd)
>  - goerli end of life: 2024?
>  - sepolia end of life: 2026?
>  - sepolia would be the right place to migrate/test applications
>  - sepolia is permissionless, has better stability guarantees, and better total supply

examples
* https://github.com/nodejs/Release#release-schedule
* https://ubuntu.com/about/release-cycle












Also, the staker community with async refine the ephemeral testnet idea by Mario


      ![](https://ethereum-magicians.org/uploads/default/original/2X/3/32f2c2579dd4c41c2ec5bf2227cb15da0bb80b26.png)

      [HackMD](https://notes.ethereum.org/@mario-havel/stakers-testnet)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/9/984204b5f4f17aa2ba072948997cf5d861175ab6.png)

###



# Testnet for stakers  This document proposes a new type of testnet dedicated to improving the exper

---

**pk910** (2022-11-02):

“faucets work fine, what’s actually rendering the network unusable is literally 100% of substantial goerli supply being hoarded instead of sent to faucets.”

That’s right. It cannot be prevented when distributing funds freely at the same time.

There will always be people that hoard these funds for personal satisfaction or whatever reason they may think of.

Ideally there would be enough funds in the network so we don’t need to take special care of them.

The current situation on goerli actually introduced a financial benefit for those who hoarded goerli funds earlier. So I’d expect more people are hoarding funds in future testnets as it could happen again.

I really appreciate the efforts to inflate the goerli supply, but there are also some caveats we need to think about - especially that the balance of any account must not exceed the max safe integer value as q9f already pointed out.

I think that limitation will be problematic very soon if we introduce the withdrawal boost factor.

In it’s current proposal state it would allow farmers to multiply their whole balance in every partial withdrawal interval (see my comment on [simulate deposits/withdrawals under constraints of prater with various withdrawal boost factor · Issue #135 · eth-clients/goerli · GitHub](https://github.com/eth-clients/goerli/issues/135))

Just think about what happens if someone runs 100 validators and repeatedly deposits his whole balance to the validator that gets partially withdrawn next… …

I’d suggest creating the “Holesovice” testnet much earlier (probably even this year) and initialize it with **more than** enough funds. That would be a direct successor of goerli, allowing all kind of staking tests etc.

We should still keep up goerli for some time.

It’s still great for testing, but will slowly die due to the funding issues during the LTS timespan.

---

**pk910** (2022-11-02):

I think you’re underestimating the numbers a little bit ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

My faucet currently distributes 2000 GoETH every day - and it’s still a very low amount everyone gets.

Sure there are some bots and farmers, but these can’t be prevented if we’d like to distribute funds “freely”.

Even if some whales would supply the available faucets, it’s more a question of weeks than years till the faucets are drained again.

So the only suitable way from my perspective is inflating the supply in a safe way or head over to the next testnet with enough funds.

---

**pk910** (2022-11-03):

You’re underestimating the numbers again.

I’m just talking for my own faucet (not looking into other wallets):

Testnet eth sent to my faucet since this workgroup was started 9days ago: 17,18 GoETH

Testnet eth sent to my faucet in 2022 total: 351000 GoETH

I can give you an export of the numbers if you’re really interested.

Anyway these reviews of historic fund transfers aren’t very helpful for the situation.

We all know the situation is annoying (I think everyone feels the same)

But just nagging around without any constructive argument doesn’t help anyone.

If a goerli whale would refill one of the less protective faucets, it would just be drained again within days.

---

**lizc** (2022-11-03):

(post deleted by author)

---

**sole12343** (2022-11-07):

hi , we are faucet-dao team.

We try a new type of faucet, we call it a POT faucet , proof of trade. Let me show why we are important.

firstly, the penalty for malicious behavior by the pos network is the confiscation of tokens , on the goelri network, that’s goerli eth . If goerli eth is worthless, then punishment is worthless . Hackers can destroy and attack unscrupulously.

Moreover, if goerli can have a large group of nodes that are really validators for their own interests, then goerli will be the closest and safest test network to the mainnet, and the test in goerli will be more valuable. I believe that goerli may also meet some issues will be valuable to ethereum.

Secondly, as far as I know, many testnet test coins can be sold for money, whether they are in short supply or not. It is very difficult for the network to provide stable faucet for a long time, and all kinds of problems will occur, not to mention the most famous testnet(goerli) , used by many developers and users .

Finally, from the user’s point of view, users hope that they can easily obtain test coins instead of looking around for faucets that are still available. With the current faucet, one person may only receive 0.1 goerli eth a day, which is not enough for everyone, but it can resist hacker attacks. This is ridiculous, the purpose of the faucet is to let the user use it, so almost all faucets failed.

But look at our faucet-dao, hundreds of people have bought goerli eth from us, and everyone who bought it is very happy, they are grateful to us. We like to make our project an exploration of the community. Once we sold over 50k goerli eth at a very low price, about 1 $ = 2000+ goerli eth. We don’t have a strong desire to control, we hope to solve the problem of goerli eth.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5e68bb71a24c8d545e19f311a53176541eeb418f_2_690x156.png)image1082×246 43.8 KB](https://ethereum-magicians.org/uploads/default/5e68bb71a24c8d545e19f311a53176541eeb418f)

What do you think of faucet-dao, q9f  ,offical team , and u ？

---

**Pandapip1** (2022-11-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sole12343/48/7705_2.png) sole12343:

> What do you think of faucet-dao, q9f ,offical team , and u ？

Frankly? I think it’s part of the problem.

---

**sole12343** (2022-11-11):

We faucet-dao, hope that all users can add their excess goerli eth to the pool, so that everyone can get goerli eth more cheaper.

We bought all our goerli eth from others, we never attacked the faucet to get goerli eth in bulk, I think those people are at the heart of the current goerli eth problem.

---

**sole12343** (2022-11-11):

If the official team does what we do, then it is easy to let users go to sepolia for application testing and let those users who participate in the consensus layer have the motivation to be an honest verifier, because he can withdraw test coins and even gain income in the future.large-scale projects can also enjoy the benefits of a benign ecology here

---

**Pandapip1** (2022-11-11):

If there was a way to trustlessly turn like 0.00128 ETH into 128 goerli eth that’s baked into the protocol, specifically that the goerli eth is minted out of nowhere, and the real ethereum disappears, then I would be more in favor of it.

But testnets should be free to use. Adding an optional price tag is fine, but there should be ways of acquiring goerli / testnet eth that don’t involve your wallet.


*(8 more replies not shown)*
