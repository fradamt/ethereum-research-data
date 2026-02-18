---
source: magicians
topic_id: 12694
title: Escrowed and private bribes for Generalized DAO voting
author: 0xTraub
date: "2023-01-25"
category: Magicians > Primordial Soup
tags: [erc]
url: https://ethereum-magicians.org/t/escrowed-and-private-bribes-for-generalized-dao-voting/12694
views: 1869
likes: 5
posts_count: 4
---

# Escrowed and private bribes for Generalized DAO voting

I’m investigating the issue of DAO members being bribed for their votes on non gauge-proxy based systems. While a ton of effort has gone into building bribe systems for DAOs like Curve/Frax/Etc. not a lot of focus has been put on how bribes on other, more general DAO votes, may affect outcomes. Bribes are a lucrative market on many popular DAO’s, and it stands to reason that people are willing to accept them for voting on other proposals, especially if they have no personal stake in the outcome.

I think it’s worth focusing on for a few reasons.

1. Current bribe schemes for votes based on pro-rata distribution are economically innefficient and result in worse outcomes for voters. If voter A votes on a proposal with the expectation of receiving $10 in bribes, they can just be backrun by a larger voter, diluting their share of the pool. It may no longer be economical to make the decision they did. Using an OTC mechanisms is more efficient because the amount is “locked in” when the bribe is made and the recipient has much more concrete assurances on which to base their decision.
2. Injecting transparency about whom is bribing whom for what. This makes it possible for the community to organize around potential solutions. Ex: Alice pays Bob $10 for his 1k votes in the DAO. This is now known on-chain and next time someone who cares about the outcome can offer Bob $11 for the votes. This maximizes profit to the recipient. Comparison wise it would work very similar to a sealed-bid auction, except in this case it’s not known to anyone that the auction is occuring in the first place.
3. The lack of an existing standard means that parties are relying entirely on trust in one-another to obey. Bob has to trust Alice to pay out and Alice has to trust Bob to vote. Even if the two of them were to use an escrow contract, it may have flaws like relying on a trusted third-party, or simply that its outside the technical reach of both parties.
4. Bribes are going to happen on any DAO. It’s not possible to stop actors from colluding off-chain on things like this. I think flashbots is a good analogy where the interim solution of MEV was to realign the incentives of actors in a way that allows everyone to profit and injects some transparency into this economy. By building an OTC bribe market it allows anyone to reap the potential benefits and decentralize the profits by creating a more efficient marketplace.

I’ve had several express some potential ethical issues with what they say is “facilitating governance attacks”, of which I think there is merit to. However, I think the way to look at it is not, “should we be encouraging these activities”, but rather, “what is the worse outcome if we don’t do anything about it”, similar to MEV.

The idea would be the following: A system that acts as an escrowed and private bribe system for general votes.

1. Alice wants to give bob $10 to vote YES on DAO proposal #420. She wants an assurance he will do it and gets the money back if he doesn’t
2. It should work as an escrow service for both on-chain and snapshot based voting, releasing funds only after the vote has concluded, and it can be verified the recipient voted in line with the vote. It should be done without a trusted third-party.
3. It should be private until after the vote has passed. Alice should be able to pass this information on the bribe to Bob without a prior communication channel, and it should not be know to whom Alice is bribing. Once the vote has occured, then the contents of the bribe can be revealed. I think privacy is important for two reasons:
1. The protocol is non-interactive. Bob should not need to establish prior communication with Alice to solicit the bribe or accept it. Without it Bob has to actively manage and negotiate with Alice, which is a hassle. Having a system where before someone votes all they have to do is visit a site and see the bribe is a very easy UX. If they don’t take it then they can just go on with their life, and if they choose to they just vote as normal and then submit one more simple transaction to claim the reward.
2. Forces Bob to potentially doxx himself or his pseudo-nonymous identity.

I’ve got some preliminary designs for how it could work using commit-reveal schemes, public-key-management, and challenge windows. I’ll post more if people want but I want to get some feedback on what people think of an idea like this. Im envisioning two parts

1. A new protocol to actually implement the system.
2. An ERC for it. Since the implementation would be different based on how each DAO is structured an EIP could be useful for helping each DAO build a version specific to them.

## Replies

**xinbenlv** (2023-01-25):

Thank you for the first draft, have you looked in to ERC-1202 which might work in your scenario?

---

**0xTraub** (2023-01-25):

Somewhat but I think this is different. I see ERC-1202 as a companion ERC. 1202 is meant for how people specifically vote vs. this which I see as being salient to the vote direction itself, rather than the interface it uses to cast that vote. I think this ERC would be about how you would implement an escrowed bribe for the voting of those 1202-compliant contracts. Having a voting standard definitely helps with the off-chain components too though.

---

**0xTraub** (2023-05-04):

[@xinbenlv](/u/xinbenlv) just an FYI I finished working on the ERC and have uploaded a full example implementation and a more finely researched report on the specs and justifications behind the potential EIP.

https://github.com/jhweintraub/ERC-6506



      [github.com/jhweintraub/ERC-6506](https://github.com/jhweintraub/ERC-6506/blob/main/ERC-6506-report.pdf)





####

  [main](https://github.com/jhweintraub/ERC-6506/blob/main/ERC-6506-report.pdf)

  This file is binary. [show original](https://github.com/jhweintraub/ERC-6506/blob/main/ERC-6506-report.pdf)

