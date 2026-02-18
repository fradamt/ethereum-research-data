---
source: magicians
topic_id: 6562
title: Some thoughts on ETH2 monetary policy
author: samueldashadrach
date: "2021-06-28"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/some-thoughts-on-eth2-monetary-policy/6562
views: 894
likes: 2
posts_count: 6
---

# Some thoughts on ETH2 monetary policy

Wanted sentiment check on all of the following:

In my opinion, objectives of monetary policy - in decreasing order - are as follows

1. Chain security
2. Compensating validator costs
3. Minimise delegation
4. Do what ETH holders like

10% of all ETH in existence being staked feels like a sufficient defence for chain security against double-spends and block reorgs. Firstly because that already exceeds bitcoin as well as ethereum PoW chain’s security, which has proven sufficient till date. And secondly because automatic slashing of any greater amount than 10M ETH will anyway be socially contentious and a non-slash fork can emerge  - so we might as well take such decisions via manual social coordination.

Another major problem with having more ETH staked is there is a finite amount of ETH that is owned by both technically and politically motivated actors who are willing to solo stake. Having too much ETH staked dilutes the fraction of ETH being staked by people who actually own the ETH. Actors with ETH being delegated to them have less skin-in-the-game economically, they also reduce the number of distinct human and conceptual entities involved in staking (sybil resistance).

I feel like solo stakers are more altruistic and less profit-motivated as compared to users who delegate their ETH to these pools who accept delegation. Hence we shouldn’t assume that more staking rewards is always better; it might be possible that less rewards ensures only the altruistic stakers remain.

Delegation involves some counterparty risk (measurable economically), in equilibrium, the yield for each validator will anyway be lower than this counterparty risk due to market efficiency.

I just wanted to know how much of these statements the overall community agrees with.

[My post covers all this in more detail: [ETH 2.0 monetary policy and delegation - Noma](https://noma.substack.com/p/eth-20-monetary-policy-and-delegation) ]

## Replies

**edmundedgar** (2021-06-29):

One thing you don’t mention is… how good the monetary policy is for the thing being useful as money, in whatever way it’s supposed to be doing that. For instance, if you’re expecting it to be used as a token to pay for gas, and you want people to send transactions, you probably don’t want the “bitcoin pizza” characteristic of “I expect it to gradually increase in value and make me feel like a chump for spending it”. I don’t know what the correct policy is here and it’s probably too early to say but I do think it’s a more important consideration than making ETH holders happy.

On the “how much staking is enough” question I don’t think you can extrapolate much from the failure of people to attack large PoW systems to date, because the amount that can be stolen through a reorg is very hard to predict, or even measure. The same applies to the extent to which a non-slash fork would save you, and how fast it would have to happen to be practical. You have a very different reward profile if you’re settling - say - a bond market representing serious money and moving very fast - rather than a niche currency mainly used for trading itself where the main way to profit from rewriting history involves getting money out of crypto exchanges.

I think the unpredictability of the profitability of attacking shows us that “minimal viable issuance” isn’t a very useful guide to monetary policy in PoS. There’s just no way to know how much is “viable”. What you instead have is a goal for more security, but you’ll never know when you’ve got enough. PoS also reduces the importance of minimizing issuance, because it’s given to ETH holders (in exchange for staking) instead of hardware manufacturers and electricity companies. This means that you can increase issuance without reducing the attractiveness of holding (and staking) ETH, and the value of the ETH I hold now is the same whether the issuance for the next 10 years will be 10% of supply or 100%, provided the system works well.

---

**samueldashadrach** (2021-06-30):

Interesting points. Regarding monetary policy, I don’t think there is consensus among the community whether ETH is a suitable replacement for fiat or should play major role in the global macroeconomic environment. As of today ETH is insanely volatile in dollar terms and such considerations aren’t important. So as of today atleast, it is more in the class of “what ETH holders want” imo, this can be changed later.

Agreed completely that profitability from attacking is very unpredictable. But I also feel that having more ETH staked won’t increase security, in fact it might actually decrease it because it reduces the number of distinct humans and corporations needed to get supermajority. Having less parties required to coordinate an attack, especially with ETH that doesnt even belong to them, can make an attack more viable. There are also risks of regulatory capture (governments telling staking providers what to do or who to censor).

I also feel that having say 40M ETH staked and then slashing a majority of that (hypothetically) is going to be contentious. People are anyway going to deploy both forks and see which one wins out. Automated slashing won’t obviate the need for laboriously reached social consensus at that scale.

---

**schone** (2021-07-02):

I think all your thoughts about the altruism and the need for more/less rewards is taken a bit to the extreme given that everybody’s funds are locked.  In other words, you can’t tell everybody’s true nature/intentions while nobody has a way to get out.

As long as this deal is a one way in, without the option for exit, it’s really hard to tell what the motives and intentions are and what set of incentives will influence further behavior.  About the only thing guaranteed at the moment is the telling that for the time being 6.X% is enough to still attract ‘new blood’.  That’s all you know for certain.

---

**samueldashadrach** (2021-07-04):

Agreed that we will have more clarity post-Merge, but I would like to know which statements specifically you feel are too early to assume true.

---

**schone** (2021-07-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samueldashadrach/48/3500_2.png) samueldashadrach:

> I feel like solo stakers are more altruistic and less profit-motivated as compared to users who delegate their ETH to these pools who accept delegation. Hence we shouldn’t assume that more staking rewards is always better; it might be possible that less rewards ensures only the altruistic stakers remain.

This part in particular.  I personally don’t think anybody is doing any of this out of the goodness of their hearts or as you like to call it, altruistic reasons.  Sure altruism might be a secondary motive, as are positive ideals.  But to say people stake entirely first and fore most on altruistic reasons with no regards to the rewards offered.  That’s naive and I believe to be baseless given the fact nobody can truly back out at this point after going in.

Further more, given this one way contract.  I don’t believe any tinkering of the rewards would be ‘fair’ or build confidence, given that all those who deposited initially had a particular contract in mind.  You can’t change the contract without offering a way out first.

