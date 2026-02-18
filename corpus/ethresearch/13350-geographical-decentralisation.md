---
source: ethresearch
topic_id: 13350
title: Geographical Decentralisation
author: pdsilva2000
date: "2022-08-12"
category: Economics
tags: []
url: https://ethresear.ch/t/geographical-decentralisation/13350
views: 7853
likes: 35
posts_count: 52
---

# Geographical Decentralisation

Hi, I would like to conduct a research to understand where will be the PoS validators (once moved from PoW to PoS) geographically in Ethereum network. It’s important to understand If there is a fair representation from different parts of the world (i.e.developing nations) . This research will enable us to understand landscape, challenges and barriers to have a true decentralisation from global geographical perspective.

Please feel free to post your thoughts and any material, personal i can reach out to make this research successful.

Thank you all in advance.

## Replies

**MicahZoltu** (2022-08-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/pdsilva2000/48/9947_2.png) pdsilva2000:

> It’s important to understand If there is a fair representation from different parts of the world

Why is this important?  Validators have a job to do and they are paid to do it.  Anyone from anywhere in the world can do this job and they will be paid the same regardless of their location, based only on their ability to complete the job successfully.

Keep in mind, censorship resistance is the goal, decentralization is the means to achieve this goal.  Decentralization isn’t by itself a goal.  Proof of Stake is designed so that it *should* work even if validators centralize (though centralization still does introduce some risks so we would prefer it doesn’t).

---

**levs57** (2022-08-13):

I feel in a light of ongoing regulatory crackdown the possibility of consensus-level attack from the state should be considered as a practical threat. For example, in a coordinated compliant softfork.

---

**pdsilva2000** (2022-08-15):

Thanks for your feedback. Idea of decentralisation is very personal in my opinion. as an ecosystem that is striving to achieve true decentralisation, it’s important to understand where the validators are based and what challenges current system is creating  to other geographical regions to participate this economic game. In my opinion some of the regions I mentioned in the research scope are the areas that need the most decentralisation.

---

**pdsilva2000** (2022-08-15):

Correct, it’s important to know where the validators and keeping a live map enable to determine the jurisdictional risk. i.e. validators having to comply with SDN contract addresses etc.

---

**simbro** (2022-08-15):

I couldn’t agree more with your statement, it is crucially important to understand if there is a fair representation of validators and nodes from different parts of the world.

There are a number of dimensions to consider in maintaining a healthy level of decentralization, and I think the community is understanding this more over time.  The canonical model for measuring decentralization is the nakamoto coefficient, of which the concentration of nodes by country is a key metric.

Right now we have: [Countries - ethernodes.org - The Ethereum Network & Node Explorer](https://www.ethernodes.org/countries) - assuming that all EL clients will be paired with a CL client, this info could give you what you need?

For the beacon chain we have some excellent data from https://migalabs.es/ - perhaps their tools can be leveraged for plotting geographical dispersal of nodes?

---

**pdsilva2000** (2022-08-15):

Thank you so much [@simbro](/u/simbro) . I will start with the sources you have shared and let you all know if i need further. Good to see there are others thinking in the same line of decentralisation. much appreciate it.

---

**randomishwalk** (2022-08-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/simbro/48/3821_2.png) simbro:

> Right now we have: Countries - ethernodes.org - The Ethereum Network & Node Explorer  - assuming that all EL clients will be paired with a CL client, this info could give you what you need?
>
>
> For the beacon chain we have some excellent data from https://migalabs.es/  - perhaps their tools can be leveraged for plotting geographical dispersal of nodes?

There is an important distinction b/w consensus participants (PoS validators) vs. full nodes. Sounds like [@pdsilva2000](/u/pdsilva2000) is interested more in seeing how validators, and I would assume by extension economic stake, by geography? Not sure if fair to assume properties of the validator set (aka geo) mirror full nodes.

![](https://ethresear.ch/user_avatar/ethresear.ch/pdsilva2000/48/9947_2.png) pdsilva2000:

> Correct, it’s important to know where the validators and keeping a live map enable to determine the jurisdictional risk. i.e. validators having to comply with SDN contract addresses etc.

Agree that assessing censorship resistance in the context of regulatory risk would be the key topical question here.

![](https://ethresear.ch/user_avatar/ethresear.ch/pdsilva2000/48/9947_2.png) pdsilva2000:

> fair representation from different parts of the world

I think the harder thing is determining “fair.” Should it be proportional to address count (how would you determine this by geography?) or to economic value secured (again same question)? Or, more simply, should validator geo distribution be proportional to GDP or internet-enabled population count?

Keep us updated though [@pdsilva2000](/u/pdsilva2000)! I’d be keen to see what results you come up with.

---

**pdsilva2000** (2022-08-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> interested

Thanks for your comments. from the regulatory risk perspective (i.e. if the validators have to comply with SDN list prior including transactions) , i think we need to determine where the full nodes are located as they are the only one can include transactions yea ? apologies for my ignorance in advance.

---

**simbro** (2022-08-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> There is an important distinction b/w consensus participants (PoS validators) vs. full nodes

Yes absolutely, you’re right.  I’m not sure though how you can unpick nodes vs. nodes that are also validators. Could node operators and solo stakers be convinced to self-report using the grafftti field?

---

**randomishwalk** (2022-08-17):

Nodes can read the chain directly and send transactions to be included by *validators*, who are responsible for building and proposing blocks to be attested on by other validators.

Crudely speaking, you can think of full nodes has having “read-only” access to the chain (with the ability to send in changes via transactions), while validators have “read and write” access to the chain

---

**randomishwalk** (2022-08-17):

Validators are identifying via unique public keys (and associated index # representing I think time of deposit or activation): https://beaconscan.com/validators#active

Wait hasn’t this analysis already been done here? See: [migalabs.es](https://migalabs.es/beaconnodes). Shows that **~34% of the ~4.3k validator nodes are located in the US**

[![image](https://ethresear.ch/uploads/default/optimized/2X/2/2932e6c22a26cefa674912c987c5bb4cd4c9a689_2_690x352.png)image1142×584 70.9 KB](https://ethresear.ch/uploads/default/2932e6c22a26cefa674912c987c5bb4cd4c9a689)

---

**simbro** (2022-08-17):

Yes indeed that’s the Miga labs dataset, but is this clients or actual validators?

---

**randomishwalk** (2022-08-18):

I emailed them to check if it’s the entire validator node count (aka the physical machines / nodes) vs. a subset of the validator set.

I don’t understand the distinction between clients and nodes? I don’t think the geo dataset they have shows clients by type?

---

**simbro** (2022-08-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> I don’t understand the distinction between clients and nodes?

I think in this context they are synonymous, but technically a “node” is an instance of a CL client and an EL client talking to each other over the engine API using a shared JWT secret.

Not all nodes are validators.  A validator is a node (EL + CL client) AND a validator (signing key, withdrawal key, 32 ETH stake etc.).  One example of a validator is:


      ![](https://ethresear.ch/uploads/default/original/3X/0/0/00d0cc268c5ae07fadeac8b40e989b8fdd8f97c7.png)

      [attestant.io](https://www.attestant.io/posts/introducing-vouch/)





###



Attestant uses their own multi-node validator client, providing high levels of security and availability whilst fitting neatly in to production environments. This article introduces Vouch and explains its features.










…although most CL client have an in-built validator.  The point is that not all nodes on the network run validators as well.  For example, Alchemy, Infura, Moralis, Blockdaemon an all those providers will run a whole bunch of nodes (CL+EL clients) without actually have validators associated with them.

This is where the confusion lies in this case.  It’s going to get even more confusing when we have DVT, but I suspect more decentralized at the same time.

---

**randomishwalk** (2022-08-19):

Ah okay understood all that—just thought you were asking about client diversity / distribution of types of clients.

In that case, yes I think this is based on validator node count.

---

**simbro** (2022-08-19):

Apologies for mansplaining! ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)  Did Miga Labs confirm that?

---

**randomishwalk** (2022-08-19):

All good! No just my hunch for now…waiting for them to reply to my message. Or to hop into this thread ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

---

**barra** (2022-08-20):

This site might help too:


      ![](https://ethresear.ch/uploads/default/original/3X/2/8/28ff94e37256735b163a7c793a37a57df08a9f88.png)

      [nodewatch.io](https://nodewatch.io/)





###



Nodewatch - Eth2 Node Analytics

---

**MaverickChow** (2022-08-20):

I just want to add something which I hope will be useful in increasing/improving the decentralization of authority/power post-PoW and post-Tornado Cash sanction.

Beside having a wider geographical dispersion of validators, I think 2 additional things can be very important to minimizing the influences of state power:

1. Make sure 1 validator can have only 1 vote, regardless of how much ETH is staked by this validator. Therefore entities such as Coinbase and others cannot have a dominant say.
2. Make sure anyone (as long as he/she staked 32 ETH at the minimum) can validate any transaction, including sanctioned ones, by choice. Therefore, even those based in offshore countries can validate transactions. Once such transaction is validated, it must be included into the blockchain, and anyone that previously refused to validate such transaction will still need to process it as valid.

I am not in support of terrorism but I do feel sanctions at protocol level is a direct violation to the network. And I am worried allowing such sanction to be in place at protocol level will set precedence to a far more serious state control in the future.

I do not follow the blockchain development as closely as most does and thus I am not sure, but I believe if the above 2 elements are firmly in place, then Ethereum would be safe from state hijack even at protocol level. At best, state power will have to fork the chain to impose control but ultimately the majority will dictate which network (the one that is strictly controlled or the one that is free) will prevail.

Edit:

In addition, I learned some are worried that slashing the stakes of participants that support state sanctions will hurt the smaller guys that stake their ETH through larger centralized entities. For that, I believe if the slashing can be implemented at least 1 year after the Merge, whereby individual participants are notified to unstake their ETH from large centralized entities (such as Coinbase) post-Merge only to restake their ETH elsewhere that does not support sanctions, then implementing the slashing mechanism will help enforce the dignity of the network while still save the smaller guys from losing their share.

---

**barra** (2022-08-25):

Its a little unclear what he means by “fair”, but I think the chain will be more censorship resistant if validators are spread over different regions of the world (lesser chance of > 1/3 of the validators being subject to decisions of a single government). Therefore, I believe making ethereum known in “underrepresented” parts of the world is important, even if that takes more effort than making it known in the US for example. Of course there should be a balance, but you probably get what I mean.


*(31 more replies not shown)*
