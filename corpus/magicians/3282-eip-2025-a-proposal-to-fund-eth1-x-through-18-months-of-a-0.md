---
source: magicians
topic_id: 3282
title: "EIP-2025 : A proposal to Fund Eth1.x through 18 months of a 0.044ETH Developer Block Reward"
author: MadeofTin
date: "2019-05-15"
category: EIPs > EIPs core
tags: [funding, block-reward]
url: https://ethereum-magicians.org/t/eip-2025-a-proposal-to-fund-eth1-x-through-18-months-of-a-0-044eth-developer-block-reward/3282
views: 6218
likes: 17
posts_count: 12
---

# EIP-2025 : A proposal to Fund Eth1.x through 18 months of a 0.044ETH Developer Block Reward

I created an EIP



      [github.com/MadeofTin/EIPs](https://github.com/MadeofTin/EIPs/blob/ETH1.X/EIPS/eip-2025.md)





####

  [ETH1.X](https://github.com/MadeofTin/EIPs/blob/ETH1.X/EIPS/eip-2025.md)



```md
---
eip: 2025
title: Block Rewards Proposal for funding Eth1.x
author: James Hancock (@madeoftin)
discussions-to: https://github.com/MadeofTin/EIPs/issues
status: Draft
type: Standards Track
category: Core
created: 2019-04-20
requires: 1890
---

## Simple Summary

Add `0.0055 ETH` per block for 18 months (A total of 17050 ETH) as a developer block reward reserved for funding specific Ethereum1.X working groups. The working groups are State rent (750k), Better sync (360k), Finality gadget (360k), Fee market (360k), Testing infrastructure (360k). Governance of the funds will be through a multisig of trusted individuals from the ecosystem including client teams, the foundation, and the community.

[EIP-1890](http://eips.ethereum.org/EIPS/eip-1890) proposes a mechanism to capture a portion of block rewards for sustainably funding ongoing network development. That EIP sets values and addresses to zero and so does not actually collect any rewards. This proposal is to explicitly set those values and begin collecting a portion of block rewards for 18 months in order to fund Ethereum 1.X working groups and organization efforts. This funding will be used to repay an initial loan provided by investors in the community funding this work with a small amount of interest. After 18 months the block reward would again reduce to zero.

```

  This file has been truncated. [show original](https://github.com/MadeofTin/EIPs/blob/ETH1.X/EIPS/eip-2025.md)










and submitted a PR for its inclusion in istanbul.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2025)














####


      `master` ← `MadeofTin:ETH1.X`




          opened 11:30PM - 13 May 19 UTC



          [![](https://avatars.githubusercontent.com/u/1226869?v=4)
            MadeofTin](https://github.com/MadeofTin)



          [+218
            -0](https://github.com/ethereum/EIPs/pull/2025/files)







This is a proposal for the addition of a 0.044 block reward for 3.1 million bloc[…](https://github.com/ethereum/EIPs/pull/2025)ks (about 18 Months) to be used to payback a loan for ETH1.X Development efforts.

I recognize this EIP will require a lot of collecting signals from the community for it to even be considered. I will champion these efforts.

https://github.com/MadeofTin/EIPs/blob/ETH1.X/EIPS/eip-2025.md












Issues can be filed here


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [GitHub](https://github.com/MadeofTin/EIPs/issues/)



    ![](https://opengraph.githubassets.com/6c798ff3e5a38fb4662bcd9fdd96532cb415bc830904ecd26383145f4eaaf38f/MadeofTin/EIPs)

###



The Ethereum Improvement Proposal repository. Contribute to MadeofTin/EIPs development by creating an account on GitHub.










as well as Feedback on this thread is appreciated.

# Summary

Add  `0.044 ETH`  per block for 18 months as a developer block reward reserved for funding Ethereum1.X development.

Currently, EIP 1890 is a proposal for a mechanism to capture Block Rewards for funding Development. That EIP has values and addresses set to zero. This proposal is to set those values to non-zero for 18 months focused on funding Ethereum 1.X working groups and organization efforts. The block reward will go towards paying back a loan with a small amount of interest to organizations in the Ethereum Community. After 18 months the block reward would again be set to zero

Funds would be managed by the Eth1.X Devs. They are currently developing a mechanism for this already.

## Replies

**timbeiko** (2019-07-22):

For archival’s sake, here’s a big twitter thread about the issue that blew up today:



      [twitter.com](https://twitter.com/econoar/status/1153097014449565696)



    ![image](https://pbs.twimg.com/profile_images/1892950144296927232/sDDH9-EB_200x200.jpg)

####

[@econoar](https://twitter.com/econoar/status/1153097014449565696)

  Reading through the latest Ethereum Core Dev call notes and it appears that EIP-2025 is being seriously considered as an EIP for Istanbul.

EIP-2025 adds 0.044 ETH per block for 3,100,000 blocks to go to a dev fund. That’s 136,400 ETH.

Absolutely absurd! This cannot happen.

  https://twitter.com/econoar/status/1153097014449565696










And a few related ones:

https://twitter.com/spencernoon/status/1153300532808888320

https://twitter.com/iamDCinvestor/status/1153288047540211712

---

**Swader** (2019-07-22):

I whipped up a small smart contract that lets all people registered in HumanityDAO vote on this. It won’t affect a single thing, it’s just my curiosity. Vote here: https://oneclickdapp.com/chant-castro/

---

**CL20** (2019-07-22):

Made an account just to reply to this.

Crypto is about returning the issuing power of a decentralized currency back to the people. Not for a group of developers to insert a paycheck for themselves every new block. What you’re proposing sounds more like something fiat money would do.

I am not against helping development, but you have to be aware that you’re proposing a change to the monetary policy of the second biggest cryptocurrency at the moment. Do you have any idea what kind of impact a change like this will have? What about long term impact of this change on the confidence in the monetary properties of ETH?

You’re trying to build the future of money, **and focus on the monetary properties of ETH should be the utmost important.** Why should anyone buy ETH in the future when the devs can just print few millions of $ for themselves? Miner have no incentive to support this either. If this proposal gets passed, ETH will look like an absolute joke.

---

**postables** (2019-07-22):

As someone who is both a developer building on ethereum, and a large scale miner of Ethereum I can’t help but be shocked as to the seriousness of this proposal.

Ethereum as a platform is massively behind schedule. There have been delays left right and centre. Some delays are just due to unforeseen technical issues, and then we also have delays like the previous hard fork being delayed due to a security issue that was barely noticed before it was too late. I don’t think the core Ethereum developers have shown that they deserve a development fund. Maybe if we weren’t so behind schedule it would be deserved. But it isn’t, a developer fund could be considered similar to a bonus you get in the corporate world. Bonuses are only given to employees who Excel at their jobs and go above and beyond the call of duty.  With the massive amount of delays, I absolutely do not think a bonus is deserved.

Now speaking as a miner (a large scale miner with a facility worth multiple millions of dollars) I’m getting shafted by this EIP. First you reduce my block rewards down to 3ETH from 5. Okay fine whatever I wasn’t too upset and I can manage. But now you want to take from my rewards even more, and distribute them to a group of people who are dropping the ball on their one job which is timely development of the ethereum ecosystem? What an absolute joke.

It’s miners people like me and others that have an extremely high amount of skin in the game that are responsible for producing blocks. Where does this end? Does the ethereum community not give a shit about the people responsible for providing the hash power that secures the network?

If this is really about developers needing funding to work on ethereum, maybe y’all shouldn’t have been giving grants worth 400k to companies that did ICOs and raised MILLIONS of dollars (status for example).

---

**maxlaumeister** (2019-07-22):

Hey all, software dev chiming in.

I don’t often speak up about Ethereum’s governance because I usually find myself in agreement with EIPs. But I feel the need to address this specific EIP, because I believe that if it were ratified it could put the Ethereum network at risk of a hard-fork and governance schism in the near future, and I don’t think that is an overstatement.

Monetary policy is one of the most sensitive and critical aspects of Ethereum protocol governance, and there is a strong expectation in the community that the core developers will be impartial with regards to Ether issuance. If this EIP were to be ratified by the core dev team and thus more money printed for the 1.X working group, my expectation is that a significant portion of the Ethereum community would come together and create a hard-fork where the Ether supply is not debased. This would split developer mindshare, weaken the network’s security by fragmenting miners, and create uncertainty and hesitance among potential adopters of the Ethereum network, including individuals, DeFi companies, and large tech companies.

Even more critically - unless I am mistaken, additional funding for Ethereum working groups is not even necessary. As far as I know, the Ethereum Foundation already has enough funding from the 2014/2015 crowdsale to fund all Ethereum working groups necessary to see Ethereum through the end of the Serenity network phase at the current price of Ether. **Since adequate layer-2 funding sources already exist and have proven to be functional, printing additional money is not required.**

I fully expect the majority of Ethereum core developers to come out publicly against this proposal to print more money for the 1.X working group. But to anyone who believes it may be a good idea, I urge them to consider the real dangers of debasing Ethereum’s currency so far along in the network’s life. We are no longer in the network’s infancy trying to bootstrap development - we already have a well-funded foundation, and companies are building real products on the Ethereum network, expecting it to be stable with a predictable monetary policy.

Ethereum’s issuance model is already on very tenuous ground compared to, say, Bitcoin’s, due to the monetary policy still being up to interpretation rather than being permanently enshrined in the definition of the currency. **Printing more money for the 1.X working group would cause the market to re-price Ether based on new knowledge that there could potentially be an unlimited amount of new issuance in the future to fund additional working groups.** Firstly, this price drop could significantly devalue the Ethereum Foundation’s financial reserves, putting the Ethereum developer community in a worse-off state financially than if the EIP had not been accepted. Secondly, this price drop could cause the economic incentives of the Ethereum blockchain to degenerate, thus causing irreparable economic harm to the Ethereum network itself.

In short, I believe that this EIP and [EIP 1890](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1890.md) pose significant systemic risk to the Ethereum network if they are ratified. I urge the Ethereum core developers to consider the social implications of attempting to debase the Ether supply at this point.

---

**Ethernian** (2019-07-24):

I agree fully and oppose the [eip-2025.md](https://github.com/MadeofTin/EIPs/blob/ETH1.X/EIPS/eip-2025.md) in current form.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> We are asking users to a) effectively subsidize a loan with no guarantees of accountability or without key metrics to identify progress and effective use of funds, b) trust that the proposed figures will result in the completion of the overall effort without the risk of additional requests for added funding, c) trust that the governance surrounding fund allocation and disbursement will be effective, transparent, and not capturable by interested parties.

Nevertheless, let me try to improve the [@MadeofTin](https://ethereum-magicians.org/u/MadeofTin)’s proposal.

We could promise to infrastructure investors an ROI funded by community money (fund, inflation or tax) ONLY after the project gets released and merged into the mainnet.

No release - no ROI/profit.

Additional mechanism may tune payout after release depending on usage and utility (ToBe defined)

---

**econoar** (2019-07-25):

I strongly oppose this EIP.

To me, the only thing that block rewards (on ETH or BTC) should be used for is securing the chain. From there, it should be a neutral and secure protocol for anyone to build applications on and it should not play favorites. People invest in ETH for many reasons but one of the reasons is the assumption that it has strong economic principles of a known and low issuance schedule. This means that your holdings cannot be easily diluted by inflation. By allowing random increases in block rewards, we are taking away a large reason that some people invest in ETH. If at any point, the issuance schedule can be altered UP outside of a reason for security, that confidence is shaken.

All of these assumptions and investment theses are important because as ETH price rises, the chain becomes more costly to attack.

The most dangerous part to me is the fact we’d be embarking on a giant slippery slope of where do we stop? If we set a precedent that one team can get funding via block rewards, where does it end? Why is it just this team? This is not something we want to open. It’s not meant to be a honeypot for funding.

The EIP process states that the author must gather community consensus and I do not see that in this case. I’m confident it would cause a contentious fork.

---

**whyrusleeping** (2019-07-26):

Just curious, if the core devs have to stop and get other jobs because they don’t have any income, what happens then? Obviously there are other solutions, but I’m not seeing any alternatives discussed in the thread

---

**Ethernian** (2019-07-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/whyrusleeping/48/2134_2.png) whyrusleeping:

> Obviously there are other solutions, but I’m not seeing any alternatives discussed in the thread

Do you know any other threads or forums, where such ideas get discussed?

---

**MadeofTin** (2019-08-01):

But 0 progress on Eth would destroy Eths monetary properties. ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=9)

---

**rumkin** (2019-08-07):

This is just a new feudalism. Developers of Ethereum should provide services to community to earn money, not casting them and not bringing taxes.

Decentralization means that any group of developers could produce features for Ethereum independently, would core developers allow other groups to add new tax for funding their development processes?

