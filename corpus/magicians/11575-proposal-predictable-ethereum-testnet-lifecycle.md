---
source: magicians
topic_id: 11575
title: "Proposal: Predictable Ethereum Testnet Lifecycle"
author: q9f
date: "2022-11-02"
category: Magicians > Process Improvement
tags: [testing, testnet, testnets, goerli]
url: https://ethereum-magicians.org/t/proposal-predictable-ethereum-testnet-lifecycle/11575
views: 18277
likes: 22
posts_count: 21
---

# Proposal: Predictable Ethereum Testnet Lifecycle

## Proposal: Predictable Ethereum Testnet Lifecycle

This proposal is one of the results of the previous discussion in the [testnet workgroup with client teams and application developers](https://ethereum-magicians.org/t/testnet-workgroup-paths-out-of-the-goerli-supply-mess/11453/12). We seek general feedback from the Ethereum community on the following plan.

**TL;DR**

- launch a new testnet every two years on a defined date, e.g., Oct 1st, 2023, 2025, 2027, etc.
- limit lifetime of testnets to five years maximum (four years plus one year long-term support if necessary)
- extend Goerli long-term support for another two years till 2024 if possible (depending on the outcome of the supply issue discussion)

#### Problem Statement

The current situation of deprecating multiple testnets at once in preparation for the merge with only a few weeks’ notice caused some frustration among application developers and infrastructure providers. The supply issues on the Goerli testnet added to this, unfortunately.

As it stands, post-merge there are only two major testnets available ([youtube#1UtcvVve32A](https://www.youtube.com/watch?v=1UtcvVve32A)):

- Goerli, which is the only testnet for public testing of staking infrastructure (permissionless)
- Sepolia, which primarily targets application developers due to its permissioned nature

However, the better and more widely available infrastructure for Goerli prompted many application stacks and layer-2s to migrate to Goerli instead of Sepolia. Both, the network effect of already existing applications on Goerli and the lack of communication for best practices prior to the testnet deprecation and the merge may have caused this.

There are efforts to address the Goerli supply issues through the Capella protocol upgrade on the Prater consensus layer for Goerli through *boosted* withdrawals ([ethereum/consensus-specs#3073](https://github.com/ethereum/consensus-specs/pull/3073)). This would hopefully allow extending the lifetime of the testnet drastically. Simulations and technical discussion is currently still outstanding ([eth-clients/goerli#135](https://github.com/eth-clients/goerli/issues/135)).

#### Proposed Lifetime

It is proposed to limit the lifetime of a public Ethereum testnet predictably to four years after genesis and allowing to consider one additional year of long-term support, in case networks are heavily used, to a maximum of **five years**. After the end-of-life date of a testnet, it will no longer receive support from client teams.

In addition, a new testnet will be launched every two years respecting a predetermined schedule. Both client teams and infrastructure providers should commit to support these schedules to allow application developers preparing necessary migrations in advance.

Such a schedule will allways guarantee the availability of at least two public testnets for every stakeholder in the ecosystem. A migration of applications will only be necessary every four years on average given the proposed schedule.

#### Applied Schedule

Applying the schedule to the existing testnets would result in Goerli already entering the long-term support phase in Q1/2023. ~~However, since there is currently a lot of migration happening *to* Goerli, it should be extended by two years till at least 2024.~~ (Update, this is not going to be fixed, so we have to sunset Goerlin in 2023.)

Starting with ~~Sepolia~~ Goerli, we commit to the previously defined 4+1 schedule.

| Testnet | Flavour | Genesis | LTS | EOL | Status |
| --- | --- | --- | --- | --- | --- |
| Olympic | PoW | Q1/2015 | No | Q3/2015 | Dead |
| Morden | PoW | Q3/2015 | No | Q4/2016 | Dead |
| Ropsten | PoW | Q4/2016 | No | Q4/2022 | Dead |
| Kovan | PoA | Q1/2017 | No | Q4/2019 | Dead |
| Rinkeby | PoA | Q1/2017 | 1 year | Q2/2023 | EOL |
| Goerli | PoS | Q1/2019 | 1 year | Q4/2023 | LTS |
| Sepolia | PoA | Q4/2021 | 1 year | Q4/2026 | Live |
| Holesky | PoS | Q4/2023 | 1 year | Q4/2028 | Planned |
| TBD | PoA | Q4/2025 | 1 year | Q4/2030 | Planned |

[![testnet-lifecycle-tbd](https://ethereum-magicians.org/uploads/default/optimized/2X/2/2ab07b001f7e750532a38b7738475d7e0c7b190a_2_186x500.png)testnet-lifecycle-tbd490×1312 41 KB](https://ethereum-magicians.org/uploads/default/2ab07b001f7e750532a38b7738475d7e0c7b190a)

The next testnet would be launched end of 2023 to prepare for the Goerli shutdown.



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












Any feedback and comments both by client teams but also application developers are much appreciated.

## Replies

**noam** (2022-11-02):

Thanks for summarizing the discussion!

Chiming in with a few thoughts from the perspective of application developers:

1. There was a LOT of friction in migrating recently from Kovan/Rinkeby/Ropsten to Goerli as was recommended for post-Merge testing. It’s a lot more complicated than redeploying contracts - state and dependencies on state all need to be sequenced and migrated to minimize breaking environments.
2. There is a lot of value to the demand and mainnet-likeness of Goerli we’re seeing right now. Composability, liquidity, traffic volumes, decentralized/permissionless validator sets all make for a mainnet-like environment which is great for testing and iterating pre-mainnet.
3. There is a lot of value to having a long term testnet where state can accrue, as opposed to ones that reset every few years. This builds on points (1) and (2) but you both lose a lot of value when migrating and there’s a lot of overhead.

Would recommend as a v0 we explore a way to make Goerli more sustainable long term. One such step, as discussed, would be increasing the supply of gEth. I’m sure more community members (Alchemy included) would step in to help the long term viability of this network and not put the whole load on the EF. If we’re unable to mitigate supply side issues in a reasonable manner then perhaps we can try to identify paradigms that might be better suited to long lived testnets. I understand there’s a certain burden on client/protocol development imposed here, but there’s also a large, and increasing (with ethereum adoption) burden on the application layer as well.

Thoughts?

---

**q9f** (2022-11-02):

Are you saying two more years on Goerli is not enough?

My point is, providing a fixed schedule gives the entire ecosystem more time to plan and coordinate. If you are on Goerli now, you will need to prepare for your next migration in 2024. That gives Goerli a total lifespan of 6 years which is really long for an Ethereum testnet.

---

**noam** (2022-11-02):

Taking a step back, what would it look like to have an indefinitely long lived testnet? I think that would solve a lot of the problems mentioned in (1) and (2) in the first post above.

---

**q9f** (2022-11-03):

Update: after EL teams also the CL teams indicated we should not recover Goerli and instead prepare the community for a testnet deprecation and encourage applications to migrate to either Sepolia now directly, or to Holesovice end of next year.

---

**r1cs** (2022-11-07):

As far as I am concerned, only permissioned network saves us.Now the Goerli test network is permissionless with POS.POS consensus depend on the “Stake”, and the Stake is the punishment of the dishonest participates.If the “Punishment” is useless and ez to get, pos  strategy broke down.Although there is a good case of permisionless test network, such as Ropsten.But that is POW, “work” power is a punishment of dishonest miner, and he can use the work power to make money in other chains.What’s worse, even there is no malicious, some normal can make network stuck.To be honest, I deposit 64 goerli befor and want to have a try of beacon chain.I deposit to be an validator but then I find it’s too late then go to bed, so I turned them off and have never validated. Assume if there exist a lot of curious fomo users like me,maybe 40%, the network is over.

---

**noam** (2022-11-07):

Is there a world where Sepolia and/or Holesovice have longer shelf lives than 2-3 yrs? This is going to be a major developer UX issue if teams have to migrate testnets every few years.

---

**Pandapip1** (2022-11-08):

Not sure why it should be a major UX issue - it has always been stated that testnets should be considered ephemeral.

---

**noam** (2022-11-11):

While I appreciate all of the support invested in testnets I wouldn’t necessarily say the UX can’t be improved still, especially from an application dev perspective ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Not having to migrate testnets would be a huge improvement.

---

**q9f** (2022-11-17):

Discussed the proposal with the EthStaker community today.

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/a/a8bf54f0654f4bc34a8100d1c4c8034920e0337e.jpeg)](https://www.youtube.com/watch?v=Y-WPKPBtVtQ&t=228)

---

**taxmeifyoucan** (2022-11-24):

This ephemeral testnet project intends to automatically restart after a short period of time, probably a few weeks. In this context, it could take of some load from testnets with long lifecycle so it might be easier to support them even longer. Also, the reset mechanism, once it is properly specified and implemented, could help with predetermined sunset of newly launched networks.



      [github.com](https://github.com/taxmeifyoucan/ephemeral-testnet)




  ![image](https://opengraph.githubassets.com/98769be01c153325ea80170b8681d82a/taxmeifyoucan/ephemeral-testnet)



###



Resources and project management of Ethereum ephemeral testnet

---

**pappas999** (2022-11-25):

Why is this the case though? Because If I’m developing on many of the other chains, there’s just 1 testnet for devs, and its always available, it’s easy to get gas/native tokens, and its always the place to go to develop applications.

- Polygon: Mumbai
- Avalanche: Fuji
- Solana: Devnet
- BSC: BSC Testnet

I’d like to echo the sentiments from [@noam](/u/noam). From an application perspective, having to migrate to a new network every few years is a large burden on both developers and application/infra owners.

As Ethereum continues to grow and gain adoption and more developers, I feel more focus should be placed on DX (developer experience)

Right now, here is what IMO is the best developer experience regarding testnets:

- There should be one, and only one testnet for developers. This network shouldn’t ever change (or not for a very long time)
- Network should run on POA so its not dependant on stake or community validators, & have the ability to mint lots of ETH (or infinite). There should always be 0 demand for OTC testnet ETH
- This testnet should have all the major applications & infra (alchemy, opensea, chainlink, the graph etc)
- Network clients should be upgradeable over time rather than spinning up a new testnet

Right now it’s really hard to get gETH, and gas prices can spike which means what little ETH devs have gets chewed up. I feel with these issues more and more devs will likely turn to L2’s and other EVM chains to develop their applications (Polygon, BSC, Avalanche Fuji etc). We recently had to turn off our ETH faucet due to someone getting around our security measures and taking it to sell it OTC

---

**Pandapip1** (2022-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pappas999/48/7847_2.png) pappas999:

> Why is this the case though?

Simple: so that people don’t start treating testnets like mainnets. Görli ether, for example, is sold OTC. If Görli was expected to be deprecated in one year, it would lose its speculative value.

DApps should aspire to work with any EVM-compatible chain. See [ERC-1820: Pseudo-introspection Registry Contract](https://eips.ethereum.org/EIPS/eip-1820#deployment-transaction) for how this could be done. For example, a chain-agnostic Uniswap would check to see if there’s already a router deployed, and if not, request that users send ether to the predetermined address and subsequently deploy the predetermined contract.

In summary: ephemeral testnets encourage best practices.

---

**q9f** (2022-11-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pappas999/48/7847_2.png) pappas999:

> Polygon: Mumbai
> Avalanche: Fuji
> Solana: Devnet
> BSC: BSC Testnet

All of them launched less than 5 years ago and they are not facing the issues we are facing with high-load, long-standing testnets.

---

**q9f** (2022-11-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pappas999/48/7847_2.png) pappas999:

> Right now it’s really hard to get gETH, and gas prices can spike which means what little ETH devs have gets chewed up. I feel with these issues more and more devs will likely turn to L2’s and other EVM chains to develop their applications (Polygon, BSC, Avalanche Fuji etc). We recently had to turn off our ETH faucet due to someone getting around our security measures and taking it to sell it OTC

That’s exactly what we are addressing by predictably deprecating testnets.

---

**pappas999** (2022-12-01):

thanks [@q9f](/u/q9f) and [@Pandapip1](/u/pandapip1) , points understood. We (Chainlink Labs) are internally discussing plans to move all Chainlink services to Sepolia

---

**q9f** (2022-12-05):

Scheduled Holesovice launch for September 15, 2023.



      [github.com](https://github.com/eth-clients/holesky)




  ![image](https://opengraph.githubassets.com/37046e9636bb8468b8130c8976f7dd08/eth-clients/holesky)



###



the holesovice post-merge testnet configuration.

---

**rmeissner** (2022-12-20):

Considering something like the Graph (or other indexer services), which service would you recommend? As most of the apps will only be on the “application test net” (aka Sepolia) the data that should be tested for indexing is there, but if you want to have a “Mainnet like” environment to test reorgs and similar cases the “validator test net” (aka Goerli) would be more fitting.

Another way would be to test indexing in “prod” (so Mainnet) as it is “only” reading state.

On a general note I have to say that the communication around this is quite confusing as the [Ethereum Website](https://ethereum.org/en/developers/docs/networks/) doesn’t link any of this and it is currently only visible on [GitHub](https://github.com/eth-clients/goerli).

---

**q9f** (2023-01-16):

Good point. I updated the website.



      [github.com/ethereum/ethereum-org-website](https://github.com/ethereum/ethereum-org-website/pull/9191)














####


      `dev` ← `q9f:q9f/testnets`




          opened 01:22PM - 16 Jan 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a16f40cbe4b618b7bc9b7246c471f28c4af32b99.jpeg)
            q9f](https://github.com/q9f)



          [+34
            -51](https://github.com/ethereum/ethereum-org-website/pull/9191/files)







removed kovan and ropsten, ref #8773

deprecated goerli

emphasized sepolia

---

**q9f** (2023-08-02):

[![image](https://ethereum-magicians.org/uploads/default/original/2X/e/e544c5e39135e35e76f23722c9e585c4d92effdb.jpeg)](https://www.youtube.com/watch?v=NbZTvJAbMLQ)

---

**xinbenlv** (2024-03-25):

Hi I know this is is to propose a Holesky and LTS testnets so maybe people will be interested in a relevant proposal but with a major different consideration: dApps.

I am proposing a longer term support for testnets that suit dApps, L2s and smart contracts that depend on other smart contracts:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png)
    [Proposal: Longer Term Testnet](https://ethereum-magicians.org/t/longer-term-testnet/19348)



> Good bye goerli tesetnet. I propose even longer LTS testnets, for dApps, L2s and wallets and other things that co-depend on each other.
> We keep moving to new testnets, which caused the smart contracts to be wiped out and if someone want to build smart contracts that depend on other smart contracts, such as ENS or Uniswap, they have to wait until the team deploy to the teams deploy on new testnets and that’s unideal. L2s too. Wait and see how long it will take for all those @arbitrum , @Optimism …

