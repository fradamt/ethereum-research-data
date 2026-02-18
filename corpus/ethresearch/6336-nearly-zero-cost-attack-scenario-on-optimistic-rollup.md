---
source: ethresearch
topic_id: 6336
title: Nearly-zero cost attack scenario on Optimistic Rollup
author: gluk64
date: "2019-10-16"
category: Layer 2
tags: []
url: https://ethresear.ch/t/nearly-zero-cost-attack-scenario-on-optimistic-rollup/6336
views: 15414
likes: 26
posts_count: 12
---

# Nearly-zero cost attack scenario on Optimistic Rollup

> TL;DR: Optimistic rollup relies on absolute censorship-resistance of L1 for its security. While L1 provides some decent economic incentives against mass censorship, it is easy to construct a scenario in which censorship of a particular single transaction is strongly rewarded, while non-censoring behavior is strongly penalized for a prolonged period of time. Optimistic Rollup’s 1 honest observer assumption is in reality 51% altruistic (not just honest!) L1 miners assumption. This constitutes an ultimate threat to the security model of Optimistic Rollups, especially because high concentration of assets in rollups turnes them into a sweet honeypot for hackers.

Year 2021. Pig-unicorn trade has turned into the fastest growing world industry. A single exchange built on optimistic rollup has $100M funds locked in it.

Step 1. With the help of Mr. Robot or a bribe, an attacker Eve compromises one of the private keys used to submit state transitions to an Optimistic Rollup.

Step 2. Eve acquires/orchestrates over 51% of the mining hashpower. This can be done gradually by slightly subsidizing mining, or suddenly by renting out a lot of GPUs, whatever is cheaper. Nominal cost of the required hashpower is < $100k per hour, the cost of the attack itself is low since we get all the mining rewards.

Step 3. Eve issues a malicious transaction which will steal all the funds from the Rollup to Eve’s Swag Futures Contract, and immediately starts censoring all challenge transactions. Since she owns 51% of the hashpower, she can enforce censorship as a soft-fork at zero-cost.

Step 4. Eve announces that the ownership in Swag Futures Contract is tokenized with a Swag Futures Token (SFT). She starts to distribute SFT to all miners who will comply with her soft-fork (such that half of the entire supply is distributed by the time Rollup state is finalized).

At this the miners have two options: 1) to comply and get a large share of the swag, 2) not to comply and make losses, because Eve’s 51% hashpower will override their blocks.

With miners being [perfectly rational and profit-seeking actors](http://frontrun.me/), what is the chance they opt to comply?

Once they comply, Eve’s extra hashpower is not needed anymore, she can turn it off. The soft-fork can now be maintained for indefinite period of time, until the Rollup hack is finalized. Moreover, mining pool operators will enjoy plausible deniability: they comply not for the sake of profit, God forbid, but to responsibly avoid the losses, because they understand that other miners are very likely to comply.

To visualize the chance of this attack actually taking place, I’ll just say that Eve’s real name is Colonel Kim Young Han, commander of the [special blockchain operations](https://qz.com/1110419/north-korea-may-be-using-malware-to-secretly-mine-ethereum-monero-or-zcash/) group.

P.S. For comparison, ZK-Rollup is completely immune to this kind of attacks, because it relies on proofs of validity verified by L1 on every state transition, rather than game-theoretical fraud proofs.

## Replies

**bh2smith** (2019-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> Nominal cost of the required hashpower is  ZK-Rollup is completely immune to this kind of attacks

Yes, I completely agree that the holy grail of layer 2 scalability is significantly better than its optimistic relative.

---

**adlerjohn** (2019-10-16):

In the [original paper](https://ethresear.ch/t/building-scalable-decentralized-payment-systems-request-for-feedback/5312) I wrote that laid the foundations for what would later become [optimistic rollups](https://ethresear.ch/t/minimal-viable-merged-consensus/5617), I analyzed the possibility of a majority-censorship attack and proposed a mitigation, namely: [drivechain](http://www.truthcoin.info/blog/drivechain/) incentives.

https://twitter.com/jadler0/status/1133224101047357440

If miners engage in clearly-visible censorship over an extended period of time, a UASF can be used to coerce them to behave properly. Also note that we have historical evidence that bribing miners to engage in such an attack on a large chain is a practical impossibility.

https://twitter.com/jadler0/status/1126237329444700162

Finally, Ethereum [is inherently resistant to censorship](http://hackingdistributed.com/2016/07/05/eth-is-more-resilient-to-censorship/), as enforcing a blacklist without [explicit access lists](https://github.com/ethereum/EIPs/issues/648) leads to opening up a trivial  DoS vector for the blacklister. This DoS vector is most definitely not “nearly-zero cost.”

---

**gluk64** (2019-10-17):

These are some very interesting reads, thank you!

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> Also note that we have historical evidence that bribing miners to engage in such an attack on a large chain is a practical impossibility.

Where do we have such evidence? In the case of Binance rollback, the costs exceeded the reward. From the article you linked:

> “The idea that this rollback of days would even be practical at all for anyone involved is insane. A day of mining costs 1800 BTC. Rolling back four days costs more than the hack itself.”

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> Finally, Ethereum is inherently resistant to censorship, as enforcing a blacklist without explicit access lists leads to opening up a trivial DoS vector for the blacklister. This DoS vector is most definitely not “nearly-zero cost.”

This is really cool! Definitely not zero cost. However, not incredibly expensive either: the attacker can simply sequentially execute transactions, gradually adding to the blacklist the sender addresses which ended up interacting with the contract being censored. The whitehat hackers will run of ETH much faster than the attacker runs out of computational resources.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> If miners engage in clearly-visible censorship over an extended period of time, a UASF can be used to coerce them to behave properly.

One key takeaway for me is that in order to prevent such attacks the challenge period must be long enough for the community to be able to agree on some collective counter-action. Definitely much more than 1 day.

---

**adlerjohn** (2019-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> In the case of Binance rollback, the costs exceeded the reward.

After four long days had passed, sure. But the rollback could have been initiated much earlier (even after one block). My point was less about the economic feasibility, and more about the social infeasibility: we witnessed a resounding an unambiguous decry from the public against the possibility of a bribe-encouraged rollback, *even to save user funds*. The only “rollback” we’ve seen (on a meaningful chain, that wasn’t due to some weird in-protocol bug) was the irregular state transition to recover TheDAO funds, which was (debatably) initiated by the community, not accomplished by bribing miners.

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> the attacker can simply sequentially execute transactions, gradually adding to the blacklist the sender addresses which ended up interacting with the contract being censored.

Interesting counter-counter-measure. This would, however, make the blacklisting more obvious, which makes it easier to coordinate a drivechain-like UASF. The issue with game theory is that for any n-th order move, there is an n+1-th order counter-move, ad infinitum (a valid argument for not using game theory and instead only relying on cryptographic properties and universal composability). If only mechanism design actually worked in the blockchain space…

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> Definitely much more than 1 day.

Yes. I personally used 2 weeks when implementing my prototype code of optimistic rollups. I’ve even suggested [the possibility of months, if not a year, to withdraw funds](https://ethresear.ch/t/trustless-two-way-bridges-with-side-chains-by-halting/5728), with the majority of user funds being “withdrawn” through atomic swaps instantly, rather than having to wait for the withdrawal period.

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> One key takeaway for me is that in order to prevent such attacks the challenge period must be long enough for the community to be able to agree on some collective counter-action.

Pretty much. We don’t want to do a rollback/irregular state transition to save funds, but we could do a UASF (especially with PoS, as burning attacker’s funds is made easy)!

---

**edmundedgar** (2019-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> If miners engage in clearly-visible censorship over an extended period of time, a UASF can be used to coerce them to behave properly.

One key takeaway for me is that in order to prevent such attacks the challenge period must be long enough for the community to be able to agree on some collective counter-action. Definitely much more than 1 day.

In a world in which censorship-based attacks like this are a serious threat it might be worthwhile to pre-coordinate some potential social defences. For example, you might have a general agreement that an anti-censorship UASF should take place to force the blockchain to include transactions (or replacements with the same address+nonce) which:

- Pay 5x more than typical gas prices for that period (I’m not sure quite how you’d specify this part)
- Have been published for 24 hours, 24 hours previously, in one of the Bitcoin blockchain, Twitter with a particular hashtag and the New York Times

In uncensored conditions it would be possible for any non-attacking miner to mine these transactions profitably during the 24 hours between the trigger and the fork, and people intending to execute the UASF would want to make sure the transactions in question were widely shared through other channels so that other people joined them in their defence. So although there are potentially ways to game the coordination process to cause disruption by tinkering with later editions of the New York Times or whatever to make it ambiguous whether the conditions were met, they only risk forking the chain if there’s actually a successful censorship attack in progress.

---

**gluk64** (2019-10-31):

[@edmundedgar](/u/edmundedgar), [@adlerjohn](/u/adlerjohn) how is this UASF affected by [unforkability of Ethereum due to DeFi](https://medium.com/dragonfly-research/ethereum-is-now-unforkable-thanks-to-defi-9818b967738f)?

---

**hkalodner** (2019-10-31):

That article argues that there won’t be another fork event that leads to a chain split, not that forks won’t happen. In a lot of ways, the logic of that the article argues that the major DeFi applications could force everyone to follow a fork that they support. If the major DeFi apps formed a social consensus that UASF should be used to respond to the attacks to described here, then they would be able to push it through.

---

**gluk64** (2019-11-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/hkalodner/48/2466_2.png) hkalodner:

> If the major DeFi apps formed a social consensus that UASF should be used to respond to the attacks to described here, then they would be able to push it through.

What is the best interest for the DeFi operators? To me it seems: to avoid controversies. It must be a unanimous decision to support a fork, otherwise I expect them to default to no-action. The risks are too high to be on the wrong side of the fork.

---

**hkalodner** (2019-11-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> What is the best interest for the DeFi operators? To me it seems: to avoid controversies. It must be a unanimous decision to support a fork, otherwise I expect them to default to no-action. The risks are too high to be on the wrong side of the fork.

Certainly we should assume that the DeFi operators will try to act in their own best interests. There are a few reasons I can think of for why they would support the UASF.

1. A general social consensus is formed around the Ethereum community that the correct response to an attack of this nature would be a UASF. In this case the operators should go along with the everyone’s wishes. This point may be weak because of the difficulty of actually measuring social consensus.
2. Some DeFi applications move over to fraud proof based systems like Optimistic Rollup. In this situation, impacted DeFi operators would push for a UASF and the extremely interconnectedness of the DeFi ecosystem would probably cause most others to align with them.
3. The decision is reached that the social cost of an attack on any major Ethereum application is greater than the cost of solving it through a UASF. The question is whether immutability or application level security is more important to the value proposition of Ethereum smart contracts since one or the other is violated.

---

**gluk64** (2019-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/hkalodner/48/2466_2.png) hkalodner:

> The question is whether immutability or application level security is more important to the value proposition of Ethereum.

I’m clearly biased because of my affiliation with ZK Rollup development, but I honestly believe the community should favour technological solutions which eliminate the need to answer such “either-or” questions. Blockchain system design should embrace BOTH immutability and security through automated alignment of selfish incentives.

---

**adlerjohn** (2019-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> @edmundedgar, @adlerjohn how is this UASF affected by unforkability of Ethereum due to DeFi?

For once I agree with Zamfir, in that the idea that Ethereum is unforkable because of centralized projects masquerading as DeFi, or because of DeFi,  is nonsense.

https://twitter.com/VladZamfir/status/1190329078798147585

https://twitter.com/VladZamfir/status/1190337137100513280

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> Blockchain system design should embrace BOTH immutability and security through automated alignment of selfish incentives.

For what it’s worth, I share this same sentiment, and I’m very much a PoW maximalist at heart. However, the Ethereum community has made it clear that it favors a transition to PoS which, due to the long range attack, inherently doesn’t provide this (automated, in all cases) property. As such, why not just fully embrace the new “[make it as expensive as possible for attackers if we ever need social recovery](https://ethresear.ch/t/responding-to-51-attacks-in-casper-ffg/6363)” philosophy?

