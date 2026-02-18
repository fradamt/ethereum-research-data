---
source: magicians
topic_id: 20404
title: Beacon Validators Contract for online governance
author: g11in
date: "2024-06-27"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/beacon-validators-contract-for-online-governance/20404
views: 653
likes: 14
posts_count: 12
---

# Beacon Validators Contract for online governance

Lately there has been a greater emphasis on implementing the EIPs as system contracts whenever possible (7702,4788,2935 etc). However most of these contracts have hardcoded params (for e.g. ring buffer size, target queue length for price computations etc) and are not upgradable.

Upgrading those params generally require a hardfork overloading the development process and also to some extend bring down the benefit of implementing them as contracts rather than native code (tradeoff of efficiency has already been made for using this path of implementing the EIPs)

One way to leverage their implementation being contract is to add a mechanism in them to upgrade the params via an online governance proposal. With such a mechanism for eg max blob gas limit could be raised in a phased and coordinated manner for a feature like peerDAS.

For this purpose a special Beacon Validators Contract can be deployed which triggers the upgrade functions. Note that BeaconBlockRoot contract allow ones to verify if a validator is actually part of an active validator set, as well as its balance via proof against a recent beacon block root. Obviously the system contracts would need to be code/redeployed/adopted to treat a call coming from BVC as privileged. This mechanism also allows system contracts to “opt in” to such an upgrade process.

The BVC contract will keep track of proposals which will effectively be the up-gradation call to the system contracts. Anyone could add proposals and the validators can vote on it with their effective balance weight using their withdrawal keys and with proof to the beacon header of holding the withdrawal key of an active validator. Once a threshold is reached the BVC can be triggered to call the system upgrade function with the proposed input and the voted threshold (which can also be verified by the system contracts allowing them to have their own customized threshold  for e.g. some contracts can demand very high thresholds)

Additional mechanics of verifying the active validator weight while triggering the final upgrade can be added in to prevent churning validators to hack a vote as the proof of the validator statuses  can be provided against a recent beacon block root.

Overall this will also the validator community to be part of ethereum governance especially for the topics around the params that determine the resource consumption. Also the development community has the choice to opt in or not to such an upgrade process and to have its own thresholds of accepting an upgrade.

Overall this could de-load the developers as well as to get the voice of validator community included for the topics that concern them.

## Replies

**shemnon** (2024-06-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/g11in/48/3906_2.png) g11in:

> Upgrading those params generally require a hardfork

My opinion is that this is a feature, not a bug.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/g11in/48/3906_2.png) g11in:

> One way to leverage their implementation being contract is to add a mechanism in them to upgrade the params via an online governance proposal.

Another feature of the Ethereum All-Core-Developers process is that there really isn’t a single tangible thing that can be captured. It’s a collection of multiple amorphous and hard to define things. Online governance proposals create that tangible thing to capture. This would irrevocably and existentially change the ethereum development process if implemented. I think we would need absolute certainty that this is the right thing to do before implementing it. More certainty than needed to schedule the merge.

---

**potuz** (2024-06-27):

My only comment is that it feels that testing the consensus mechanism for this will be orders of magnitude harder and more bug prone than just hardforking and changing the contract

---

**g11in** (2024-06-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Online governance proposals create that tangible thing to capture.

correct, this proposal is super limited in its scope to upgrade the params which are set to be upgradable in system contracts. So its opt in, and can EIPs/system contracts can design what they could/would be ok upgrading with using a validator community readiness signal.

There could be a ACD veto where authorized clients could come and veto a proposal but that would make things a bit more messy.

So idea is that system contracts would only accept the upgrade params they are ok putting on a upgrade path for e.g. max blobs per block.

---

**g11in** (2024-06-28):

yes the system contracts’ testing scope would definitely increase. May be we can try with something small like max blobs per block? So a system contract which accepts blob transactions with a min price on lines of 7702

Another point why this could be a good thing despite the increased scope of testing is that the validator community would feel represented (albeit in a super limited and pre-designed tangible way)

---

**gballet** (2024-06-28):

> Upgrading those params generally require a hardfork

The biggest problem, imo, isn’t so much changing the params of the buffer size, as ensuring operations can work seamlessly. For instance, in the case of 4788/2935, if the size of the buffer increases, the data that was written before the upgrade still needs to be found.

For example, if the size of the buffer was 16 and it is changed to 50 at block 100, then a simple modulus will no longer work as e.g. 99 % 50 = 49 while 99 % 16 = 3. So there needs to be a mechanism that handles historical changes. What if, within 3 blocks, the buffer size is changed from 16 to 50 back to 32?

This can be handled in the contract logic, but I would argue that this is akin to knowing in advance:

1, what are the parameters that we will want to change in the future

2. that these parameters need to be given a lot of thought, less the community picks something that breaks the whole system.

Regarding 2, It is very good to give the community a bigger voice in design decisions (although the validator set is a subset of the community with specific interests, it’s a start). The question is, how do we ensure that the range of parameters don’t break anything? Imagine we leave the gas limit as an open parameter, it would immediately be raised, and ethereum would be dead within 2 years.

Regarding 1, if for whatever reason we want to add a parameter, we need to move to another contract, which will requite a hardfork. Also, if we want to remove a parameter because we find that it is being abused, this will be both a technical and political challenge.

I’m not opposed to this at all, it is important not to leave all the decisions to a group of core devs, I’m just seeing some limits to this model that need to be addressed.

---

**g11in** (2024-06-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> 1, what are the parameters that we will want to change in the future
> 2. that these parameters need to be given a lot of thought, less the community picks something that breaks the whole system.

thats correct and the upgrade params would be super limited to what each system contract would design (or not)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> it would immediately be raised, and ethereum would be dead within 2 years.

i am assuming validators are rational actors and make informed decisions. However we could have an ACD veto mechanism for safety purposes (with weights proportional like the PG for e.g.)

---

**shemnon** (2024-06-28):

> i am assuming validators are rational actors and make informed decisions. However we could have an ACD veto mechanism for safety purposes (with weights proportional to the PG for e.g.)

Any explicit voting or veto mechanism involving ACD (or worse, PG) gets a hard no from me.  This is exactly the kind of things that would be captured.

---

**jochem-brouwer** (2024-07-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> Imagine we leave the gas limit as an open parameter, it would immediately be raised, and ethereum would be dead within 2 years.

AFAIK gas limit is still a parameter within the protocol - right? It’s just that all / most software is configured to keep it at 30M. (Cannot find a recent block with a gas  limit other than 30M)

EDIT, ah nvm here is one https://etherscan.io/block/20211115

---

**g11in** (2024-07-01):

if ACD is captured, then isn’t the protocol already captured? The only way out of such a capture is when a competing dev group forks the chain (and then the market decides which is the canonical and which is forked) Here as well in the forked chain one could deploy a new BVC contract with the new ACD seed group and then obviously the market decides.

However my intention is not to lead us on that path and hence this is a proposal for super limited and well designed params upgrade process without hardfork. system contracts should/would only expose such params to be upgraded by BVC.

For e.g. we deem that blobs can be upgraded from 6 to 20 in a step wise manner, a system contract which accepts and maintains blob excess queue like 7002 could help upgrade the max blobs via BVC proposal upgrade. So may be system contracts will never expose up gradation of params outside ACD acceptable limits

Even ACD acceptable limits could be placed in system contracts again via a ACD vote and that would not require veto.

---

**shemnon** (2024-07-01):

We have shown we can do “parameter update” forks very well, the multiple times we pushed back the difficulty bomb. We can also do it on incredibly short notice. What is needed is it has to be a situation where literally everyone is impacted (as was the design of the difficulty bomb).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/g11in/48/3906_2.png) g11in:

> if ACD is captured, then isn’t the protocol already captured?

True, ACD could get captured anyway. But something like this makes it easier to capture ACD. There is no need to pave a garden path to capture when viable and proven alternatives exist.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/g11in/48/3906_2.png) g11in:

> The only way out of such a capture is when a competing dev group forks the chain

Moving this to a TX makes the “fork veto” a less viable way to exit capture.

The node operators are free to ignore the code ACD produces and install their own development process. Ethereum Classic has already done this, and  EthPOW tried and failed due to not being able to gather sufficiently skilled devs in time for it to matter. I consider both of these examples as the system “working.” (If there was a market for another PoW ethereum devs would have been easy to get, or another team would have started the POW fork first).  But if forks have to filter out a TX such fork vetos will be less likely to be attempted, especially when warranted.

---

**g11in** (2024-07-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I consider both of these examples as the system “working.”

agreed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> if forks have to filter out a TX such fork vetos will be less likely to be attempted, especially when warranted.

my point being here is that  a limited params upgrade can be designed and kept range bound while having the validator community to weight in.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> the multiple times we pushed back the difficulty bomb. We can also do it on incredibly short notice.

time and again it has been raised the cost of rolling out small hardforks involving super high coordination. I think this would make that part easy without stakers requiring to upgrade their nodes.

