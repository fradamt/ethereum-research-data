---
source: magicians
topic_id: 9034
title: "OG Council: Post-Merge Testnets"
author: q9f
date: "2022-04-24"
category: Protocol Calls & happenings > Council Sessions
tags: [testnet, eth1-eth2-merge, testnets, ropsten, rinkeby]
url: https://ethereum-magicians.org/t/og-council-post-merge-testnets/9034
views: 5251
likes: 11
posts_count: 6
---

# OG Council: Post-Merge Testnets

These are the meeting notes from the OG Council “Post-Merge Testnet” session.

[![signal-2022-04-24-150717_001](https://ethereum-magicians.org/uploads/default/optimized/2X/3/393705aabac3764be1ff7f06bb9bb1ac656ff3de_2_666x500.jpeg)signal-2022-04-24-150717_0012048×1536 192 KB](https://ethereum-magicians.org/uploads/default/393705aabac3764be1ff7f06bb9bb1ac656ff3de)

Discussion leading up to this session:

- https://twitter.com/peter_szilagyi/status/1484548996169408512
- Post-Merge testnets · Issue #460 · ethereum/pm · GitHub

### Current testnets:

- Kovan †

it has been declared dead multiple times
- Aura proof-of-authority engine runs as long as at least 1 validator is active
- it is currently kept alive by Gnosis
- it will not be upgraded for the merge (Paris) and subsequent protocol upgrades (Shanghai)
- applications on Kovan should prepare to migrate to Goerli or Sepolia as soon as possible
- its purpose is unclear, but it should not be considered a public Ethereum testnet anymore

**Rinkeby** †

- is run by a majority of EF validators
- it will not be upgraded for the merge (Paris) and subsequent protocol upgrades (Shanghai)
- Geth team plans to remove it after the merge
- applications on Rinkeby should prepare to migrate to Goerli or Sepolia as soon as possible
- the moment the EF stops the validators, it will also stop producing blocks
- ChainLink/Aave signaled interest to maintain a Geth fork and run Rinkeby validators for long-term support, but the network will lack behind w.r.t. security and protocol upgrades
- it should not be considered a public Ethereum testnet anymore

**Ropsten** †

- is run by whoever mines it, it has been dead, revived, and deprecated before
- it will be upgraded for the merge (Paris) but deprecated right after
- it will most likely not receive post-merge upgrades, such as Shanghai and eventually also be removed from Geth in the future
- applications on Ropsten should plan to migrate to Goerli or Sepolia sometime in the future

**Goerli**

- is run by the Ethereum community
- it will be merged with the public Prater beacon-chain testnet
- it will be considered legacy but kept around for the time being
- it will continue receiving protocol upgrades
- applications should be good to deploy to Goerli still

**Sepolia**

- a newly launched proof-of-work testnet to replace Ropsten
- it will be merged and receive future protocol upgrades
- it is currently lacking infrastructure
- applications should consider deploying to Sepolia first

### Post-merge testnets:

- only Goerli and Sepolia will be supported long-term after the merge
- there was a brief technical discussion to simplify the beacon-chain requirements for post-testnets

i.e., application-testnets do not necessarily require 100k’s validators
- it should be considered running testnets with only a few trusted validators (proof-of-authority style but based on the beacon-chain stack); might as well be interesting for Sepolia?

### Other topics

- it was discussed how to deal with the limited supply of Goerli Ether

the merge will unlock some deposited Ether and make it available again
- the merge will also introduce actual block rewards

ChainLink will reach out to EF (Tim?) to propose taking over Rinkeby
we need to reach out to infrastructure providers to communicate testnet deprecation, e.g., MetaMask, Etherscan, etc.

## Replies

**timbeiko** (2022-04-26):

[@q9f](/u/q9f), would you or anyone present at the session want to come on [AllCoreDevs this Friday](https://github.com/ethereum/pm/issues/514) to give a summary of the conversations?

---

**q9f** (2022-05-02):

Hi Tim, sorry, we had a long weekend and I didn’t see this in time.

In general, I would say we just reflected what the core devs discussed previously anyways. The main obstacles are not the clients but rather infrastructure (faucets, explores, RPC endpoints) for Goerli and Sepolia; also, deprecating infrastructure for dead testnets and communicating this with key stakeholders.

One thing that could be interesting for the ACD is what I discussed briefly with Marius about having a PoA-style beacon-chain consensus for post-merge testnets, i.e., application-testnets not necessarily require 100k’s of validators and might as well run on 16 reliable validators similar to how Rinkeby or Goerli are operated.

---

**timbeiko** (2022-05-02):

No worries! Marius, who was at the session, gave an update ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> PoA-style beacon-chain consensus for post-merge testnets, i.e., application-testnets not necessarily require 100k’s of validators and might as well run on 16 reliable validators similar to how Rinkeby or Goerli are operated.

Yeah, something like this was already planned: having one testnet where the validator set is more open, and one where it’s mostly controlled by client teams & the EF. We’re tracking these discussions [in the GH issue you posted previously](https://github.com/ethereum/pm/issues/460), and I expect we’ll have some updates on it as we think through how we upgrade the various testnets for the merge.

---

**philipjonsen** (2022-05-06):

I didnt find any general discussion thread so I ask here instead hope its ok my fellow magicans ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I work with GitLabs, CircleCI and GitHub as a developer and security operator. But I have access to thousands of cryptoprojects where I also have priviledges that i shouldnt have with projects I never worked with before. But i have, lots of grants and stuff. How come I can have so much influence? Is it because my smart contracts and the DAO’s? They are old from 2015-16.

---

**q9f** (2022-10-25):

Here’s my take on testnets (Devcon 6 talk)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/039c0c445cc0a1828edcbc55d3b0f876ea459d64.jpeg)](https://www.youtube.com/watch?v=1UtcvVve32A)

Also, please consider joining the Goerli community call:



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












Context:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/q9f/48/5073_2.png)

      [Testnet workgroup: Paths out of the Goerli supply mess](https://ethereum-magicians.org/t/testnet-workgroup-paths-out-of-the-goerli-supply-mess/11453) [Primordial Soup](/c/magicians/primordial-soup/9)




> Good morning.
> After the Merge and Devcon lying behind us, it’s time to address the Goerli testnet Ether supply issue.
> Problem statement:
>
> Goerli only has 115M GoETH total supply
>
> Goerli is the only/main testnet for testing validator setups
> Circa 80-90% of the total supply is in “circulation” or locked in deposit contracts
> Goerli has been traded OTC since 2021
> Cannot test validators on Sepolia (permissioned)
> Cannot test validators on Ropsten (deprecated)
>
>
> Difficult to test beacon-chain valida…

