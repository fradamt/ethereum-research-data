---
source: magicians
topic_id: 21297
title: Need help drafting an EIP
author: Raviel
date: "2024-10-08"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/need-help-drafting-an-eip/21297
views: 795
likes: 39
posts_count: 25
---

# Need help drafting an EIP

Dear Magicians,

We’re a group of community members, victims of the Parity drama from 2017, working on a proposal for an Ethereum Assets Recovery Protocol, aimed at helping recover lost or inaccessible funds on the network due to bugs or unintended smart contract behavior.

While we’re passionate about this cause, we recognize we lack the technical expertise and experience of many of you here. We’re reaching out for collaboration, feedback, and advice on shaping this EIP into something that can truly benefit the ecosystem.

We’d deeply appreciate any guidance on how we can refine the proposal and bring it closer to something the Ethereum community can rally behind.

We need all the help we can get to ensure that this proposal serves the broader Ethereum community. Don’t wanna make another 999… ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

Would love to connect with the right people, and get some help. And leads & directions would be greatly appreciated

## Replies

**Cova** (2024-10-08):

Thank you for posting this!

As one of the victims I hope to see a positive outcome of this case and other similar cases. For myself and others who have found themselves in such an unfortunate situation.

Let’s create an EIP that contributes positively to the whole of the ETH ecosystem!

---

**ciluman** (2024-10-08):

Any help is very much appreciated ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12) after all there are more than 100k eth affected by this issue and I’m one of the affected users. Can anyone from the ethereum community support?

---

**abcoathup** (2024-10-09):

I’m sorry for everyone who loses funds.

I doubt there is much chance of community support of a single incident recovery EIP such as [EIP-999: Restore Contract Code at 0x863DF6BFa4469f3ead0bE8f9F2AAE51c91A907b4](https://eips.ethereum.org/EIPS/eip-999).  The chances are more likely to decrease over time (it is now [nearly 7 years](https://twitter.com/devops199/status/927912053297303552)).

A generic mechanism like [EIP-867: Standardized Ethereum Recovery Proposals](https://eips.ethereum.org/EIPS/eip-867) may have a slightly greater chance of support but it would be a long uphill struggle.

I’d suggest collating information on previous attempts, why they failed and how your approach would address the concerns raised.  You could then gauge what community support there is.

Previous discussions:

- EIP-867: Standardized Ethereum Recovery Proposals (ERPs)
- EIP-999: Restore Contract Code at 0x863DF6BFa4

---

**djcrawleravp** (2024-10-09):

As someone who has experienced this firsthand, I’m hopeful for a positive resolution in this case and others like it. For everyone who’s been in a similar unfortunate position, let’s work together to create an EIP that benefits the entire Ethereum community!

---

**ciluman** (2024-10-11):

I was thinking about a solution like this:

Proposal: the tx.origin (EOA) of a deployed smart contract should be able to revive the smart contract if it was killed

Intention: this would allow smart contracts that were mistakenly or maliciously killed to be revived and lost funds to be recovered.

Example of Implementation:

1. Ethereum inplements an oracle specifically to revive killed smart contracts only
2. The tx.origin deployer of a killed smart contract would have to sign a specific message where it is mentioned the killed smart contract address
3. The ethereum oracle would receive this signed message and would validade the signature onchain with a specific smart contract for this purpose, and if the signature matches with the tx.origin address deployer of the killed smart contract, the contract would be revived

Note: this solution allows only the deployer EOA to revive a killed smart contract, not the EOA that killed the smart contract. Why? Because malicious actors (Like in the case of the parity locked funds) can maliciously kill a smart contract and like this only the EOA deployer would have the rights to reverse such action, if we would allow the EOA that killed a smart contract to revive the contract this implementation would be pointless.

[@abcoathup](/u/abcoathup) what do you think about such solution?

[@everyone](/groups/everyone) any input is very much appreciated

---

**abcoathup** (2024-10-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/f17d59/48.png) ciluman:

> Proposal: the tx.origin (EOA) of a deployed smart contract should be able to revive the smart contract if it was killed

How many cases are there where this would cause a negative outcome vs the one case where you want a positive outcome?  I doubt that it would be supported.

---

**ciluman** (2024-10-12):

Many cases of lost funds because of this issue:

Polkadot: 306,276 ETH ($ 962 077 233)

ICONOMI: 114,939 ETH ($ 361 047 536)

Centrality: 21,704 ETH ($ 68 176 821)

Musiconomi: 16,476 ETH ($ 51 754 575)

Hedge Token: 4,525 ETH ($ 14 213 975)

Moeda: 4,361 ETH ($ 13 698 816)

Wysker: 1,577 ETH ($ 4 953 688)

Viewly: 1,400 ETH ($ 4 397 694)

Fluence: 1,376 ETH ($ 4 322 304)

Live Stars: 672 ETH ($ 2 110 893)

IMMLA: 600 ETH ($ 1 884 726)

Silent Notary: 286 ETH ($ 898 386)

Mirocana: 285 ETH ($ 895 244)

DAO.Casino: 150 ETH ($ 471 181)

Fiinu: 145 ETH ($455 475)

Jincor: 58 ETH ($ 182 190)

---

**Cova** (2024-10-13):

Can you elaborate on this? What do you mean it would cause a negative outcome?

Multiple avenues are being considered what would you say are the cons of allowing killed contracts to be restored by the deployer EOA on a later date?

---

**abcoathup** (2024-10-14):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/f17d59/48.png) ciluman:

> Many cases of lost funds because of this issue:

I assume the projects listed with stuck funds are all related to a single instance of a contract being SELFDESTRUCTed.

Someone would need to research every single instance of a contract being SELFDESTRUCTed and what the impact would be in every single case if the contract was allowed to be resurrected by the deployer of the contract.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cova/48/16433_2.png) Cova:

> Multiple avenues are being considered what would you say are the cons of allowing killed contracts to be restored by the deployer EOA on a later date?

Someone would need to do this research to determine the various outcomes, some of which could be negative.  This is one of the issues with a broad change like this.

---

**Raviel** (2024-10-14):

Thanks a million for all the input people ![:blue_heart:](https://ethereum-magicians.org/images/emoji/twitter/blue_heart.png?v=12)![:nerd_face:](https://ethereum-magicians.org/images/emoji/twitter/nerd_face.png?v=12)

I went through the answers and I can smell a scent of hope ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

[@ciluman](/u/ciluman) I believe 514k ETH is inaccessible right now. I don’t even think the expression “locked” is right.

[@abcoathup](/u/abcoathup) thanks for the reading material. I’ve read the majority of 999 before already, now reading my way through 867. Loads of very compelling comments & arguments in there! ![:nerd_face:](https://ethereum-magicians.org/images/emoji/twitter/nerd_face.png?v=12)

What would you say are the chances now, 7 years later? Like… how has the ecosystem changed that it would favor such a systemic change and how has it changed so that it would more likely reject it?

I personally believe that at least emotionally, the landscape has cleared a bit around the drama. Minds have softened a bit. Code is Law is moving ever towards Code is Change if I understood right.

If you were to advise us how to approach and gauge the community support here efficiently?

Thanks again for the input Andrew! ![:pray:t2:](https://ethereum-magicians.org/images/emoji/twitter/pray/2.png?v=12) We’ll do our homework and come back once we have something figured out.

---

**abcoathup** (2024-10-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/raviel/48/13344_2.png) Raviel:

> What would you say are the chances now, 7 years later?

On a state change for one single incident 7 years ago, zero.

As part of a generic framework for recovering stuck/lost funds, very low (but not impossible).

I am not a core dev, this is my personal opinion only as part of the Ethereum community.

---

**matt** (2024-10-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/raviel/48/13344_2.png) Raviel:

> What would you say are the chances now, 7 years later?

0%. I’m sorry. It is not something the core devs will pursue.

---

**Raviel** (2024-10-15):

Hi Matt, thanks for pitching in even tho it’s a hard hit hearing point blank 0%, ngl ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

For what reasons is this not something the core devs would pursue, if I may ask?

---

**Raviel** (2024-10-24):

[@matt](/u/matt), [@abcoathup](/u/abcoathup) - we have a discord community where we discuss a whole range of possible solutions for this.


      ![](https://ethereum-magicians.org/uploads/default/original/2X/2/260805d2b3d4ee1e656d5eed32f80a75bf5e7054.png)

      [Discord](https://discord.com/invite/BTPD26KNbK)





###



Check out the Locked Ether Collective community on Discord – hang out with 133 other members and enjoy free voice and text chat.










Would love to have someone from the magicians come and speak to us & tell us why it is(n’t) possible.

Would you be open to come have a short Q&A with our group?

---

**abcoathup** (2024-10-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/raviel/48/13344_2.png) Raviel:

> Would you be open to come have a short Q&A with our group?

I don’t have anything more to add.  I’ve given you my perspective.

---

**tms1337** (2024-11-02):

Hi everyone,

I’m really sorry to hear about the Parity incident and the impact it had on many in our community. Your initiative to develop an **Ethereum Assets Recovery Protocol** is both timely and essential. Here are some thoughts and ideas that might help refine your proposal:

### Unified Recovery Mechanism

**Single Smart Contract Approach:**

Instead of multiple contracts, a single, well-audited smart contract can streamline the recovery process. This contract would handle proposals and executions of fund recoveries, ensuring simplicity and security.

**Balanced Oversight:**

- Multi-Sig Admins: Implement a multisignature setup (e.g., 3 out of 5 admins) to propose and approve recovery actions. This reduces the risk of any single admin acting maliciously.
- User Approvals: Allow users who have been affected by frozen funds to approve or veto recovery actions. This ensures that the community has a say in the process, preventing unilateral decisions by admins.

### Governance Integration

**Community-Driven Decisions:**

Drawing inspiration from **EIP-867** and **EIP-999**, it’s crucial to ensure that recovery actions are not only technically sound but also have community backing. By requiring both admin and user approvals, we create a system that’s resilient against collusion and maintains trust.

**Transparent Processes:**

All actions, from proposals to approvals and executions, should be logged transparently on-chain. This makes the entire process auditable and builds trust within the community.

---

Let me know your thoughts if relevant

---

**Raviel** (2024-11-05):

Hi [@tms1337](/u/tms1337),

Thanks a lot for pitching in.

What do hardcore neysayers have to say on this? [@abcoathup](/u/abcoathup) [@matt](/u/matt) - would just love to hear some constructive criticism other than a blunt “No” or “0%”.

If you give us the why then maybe we can address it? Nobody I’ve spoken to thinks that these people don’t deserve their money back and that the ecosystem couldn’t benefit from a solid fund recovery system…

![:pray:t3:](https://ethereum-magicians.org/images/emoji/twitter/pray/3.png?v=12)![:nerd_face:](https://ethereum-magicians.org/images/emoji/twitter/nerd_face.png?v=12)![:pray:t3:](https://ethereum-magicians.org/images/emoji/twitter/pray/3.png?v=12)

---

**Raviel** (2024-11-12):

is it a start? [@abcoathup](/u/abcoathup) [@Cova](/u/cova) [@matt](/u/matt)

### Ethereum Assets Recovery Protocol Proposal

### Abstract:

The Ethereum Recovery Protocol aims to create a standardized mechanism for recovering inaccessible or locked funds due to unintended smart contract behavior or bugs. By introducing a protocol that works in harmony with Ethereum’s existing consensus and fee models, this EIP lays the groundwork for safely, securely, and equitably redistributing inaccessible funds in a manner that benefits both the affected parties and the broader Ethereum ecosystem. The proposal addresses the lessons learned from EIP-999 & 867 and creates a more holistic and flexible solution.

### Motivation:

The increasing complexity of decentralized applications (dApps) and smart contracts on Ethereum has highlighted vulnerabilities in contract design, leading to locked or lost funds through no fault of the users. The Parity Wallet bug serves as a prime example, where approximately 500,000 ETH (~$1.5B today) was locked permanently due to a smart contract bug. These funds, if recoverable through a transparent, decentralized, and auditable mechanism, could greatly benefit the ecosystem while respecting Ethereum’s commitment to immutability.

The key motivation of this EIP is to provide a mechanism that allows for the careful recovery of locked funds while preventing any moral hazard. This solution will not only return funds to affected users but also establish a framework for future recovery cases that minimizes risks to Ethereum’s security and decentralization.

---

**fulldecent** (2024-11-22):

What you are describing is recovery of assets on Ethereum.

This is the single most downvoted issue in the history of the community review of Ethereum changes: https://github.com/ethereum/EIPs/pull/867

Also discussed at https://github.com/ethereum/EIPs/pull/999#issuecomment-381408887

In fact the response was so strong that another proposal was written specifically to address how proposals likes yours should be addressed. It says they should not be enacted.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/894/files)














####


      `master` ← `sandakersmann:master`




          opened 05:46PM - 21 Feb 18 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/9/97768e727381724636a1b05c0c773b5929dceaeb.jpeg)
            sandakersmann](https://github.com/sandakersmann)



          [+41
            -0](https://github.com/ethereum/EIPs/pull/894/files)







Provide a standardized response against proposals for bailouts on the offical Et[…](https://github.com/ethereum/EIPs/pull/894)hereum repositories.












---

Arguments abound on why we should not violate the guarantees of a decentralized system, such as this proposal recommends.

And is just one citation (link to specific comment):



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/866#issuecomment-365823726)












####



        opened 04:50PM - 01 Feb 18 UTC



          closed 11:24PM - 15 Feb 18 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c71465363bf83e04093880330e89d6176f199850.png)
          jaytoday](https://github.com/jaytoday)










Please refer to https://github.com/ethereum/EIPs/issues/867












---

I disagree with this proposal and it should not be implemented.

---

---

Futhermore, I believe Etherum Mainnet should not go through any further changes period. Because it is a decentralized system. And the contract has already been made. And Vitalik should relinquish control of the Ethereum trademark so that others people may propose changes to the Ethereum software rather than only himself.

---

**Cova** (2024-11-25):

I would like to thank [@abcoathup](/u/abcoathup) , [@tms1337](/u/tms1337)  and [@fulldecent](/u/fulldecent) for your valuable insight and feedback. We (as a very small “grassroots” movement of affected individual users) are learning a ton from your insights on top off shifting through all the previous discussion that has already taken place on several platforms before. It is helping us theorize about potential possible solutions that hopefully the whole of the community could support.

I sincerely hope you are willing to engage with us further in the future and provide more valuable feedback and insight. You have my thanks!


*(4 more replies not shown)*
