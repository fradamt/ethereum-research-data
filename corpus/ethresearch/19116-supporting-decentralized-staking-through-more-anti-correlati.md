---
source: ethresearch
topic_id: 19116
title: Supporting decentralized staking through more anti-correlation incentives
author: vbuterin
date: "2024-03-26"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/supporting-decentralized-staking-through-more-anti-correlation-incentives/19116
views: 14475
likes: 84
posts_count: 15
---

# Supporting decentralized staking through more anti-correlation incentives

*Content note: preliminary research. Would love to see independent replication attempts.*

*Code: https://github.com/ethereum/research/tree/master/correlation_analysis*

One tactic for incentivizing better decentralization in a protocol is to *penalize correlations*. That is, if one actor misbehaves (including accidentally), the penalty that they receive would be greater the more other actors (as measured by total ETH) misbehave at the same time as them. The theory is that if you are a single large actor, any mistakes that you make would be more likely to be replicated across all “identities” that you control, even if you split your coins up among many nominally-separate accounts.

This technique is already employed in Ethereum [slashing (and arguably inactivity leak) mechanics](https://github.com/ethereum/annotated-spec/blob/master/phase0/beacon-chain.md#aside-anti-correlation-penalties-in-eth2). However, edge-case incentives that only arise in a highly exceptional attack situation that may never arise in practice are perhaps not sufficient for incentivizing decentralization.

**This post proposes to extend a similar sort of anti-correlation incentive to more “mundane” failures, such as missing an attestation**, that nearly all validators make at least occasionally. The theory is that larger stakers, including both wealthy individuals and staking pools, are going to run many validators on the same internet connection or even on the same physical computer, and this will cause disproportionate correlated failures. Such stakers *could* always make an independent physical setup for each node, but if they end up doing so, it would mean that we have completely eliminated economies of scale in staking.

## Sanity check: are errors by different validators in the same “cluster” actually more likely to correlate with each other?

We can check this by combining two datasets: (i) **attestation data** from some recent epochs showing which validators were supposed to have attested, and which validators actually did attest, during each slot, and (ii) data mapping validator IDs to publicly-known **clusters** that contain many validators (eg. “Lido”, “Coinbase”, “Vitalik Buterin”). You can find a dump of the former [here](https://data.ethpandaops.io/efresearch/attesters.txt), [here](https://data.ethpandaops.io/efresearch/immediate_attesters.txt) and [here](https://data.ethpandaops.io/efresearch/committees.txt), and the latter [here](https://data.ethpandaops.io/efresearch/clusters.csv).

We then run a script that computes the total number of **co-failures**: instances of two validators within the same cluster being assigned to attest during the same slot, and failing in that slot.

We also compute **expected co-failures**: the number of co-failures that “should have happened” if failures were fully the result of random chance.

For example, suppose that there are ten validators with one cluster of size 4 and the others independent, and three validators fail: two within that cluster, and one outside it.

[![](https://ethresear.ch/uploads/default/original/2X/e/e103e9e08c8e2aedd5d5fa0e004b8429f5cb2af2.png)610×102 3.79 KB](https://ethresear.ch/uploads/default/e103e9e08c8e2aedd5d5fa0e004b8429f5cb2af2)

There is one co-failure here: the second and fourth validators within the first cluster. If all four validators in that clusters had failed, there would be *six* co-failures, one for each six possible pairs.

But how many co-failures “should there” have been? This is a tricky philosophical question. A few ways to answer:

- For each failure, assume that the number of co-failures equals the failure rate across the other validators in that slot times the number of validators in that cluster, and halve it to compensate for double-counting. For the above example, this gives \frac{2}{3}.
- Calculate the global failure rate, square it, and then multiply that by \frac{n * (n-1)}{2} for each cluster. This gives (\frac{3}{10})^2 * 6 = 0.54.
- Randomly redistribute each validator’s failures among their entire history.

Each method is not perfect. The first two methods fail to take into account different clusters having different quality setups. Meanwhile, the last method fails to take into account correlations arising from different slots having different *inherent difficulties*: for example, slot [8103681](https://beaconcha.in/slot/8103681) has a very large number of attestations that don’t get included within a single slot, possibly because the block was published unusually late.

[![](https://ethresear.ch/uploads/default/original/2X/c/c34994d5a8fe647e304a91b98a72361eeb532c48.png)882×227 11.8 KB](https://ethresear.ch/uploads/default/c34994d5a8fe647e304a91b98a72361eeb532c48)

*See the “10216 ssfumbles” in this python output.*

I ended up implementing three approaches: the first two approaches above, and a more sophisticated approach where I compare “actual co-failures” with “fake co-failures”: failures where each cluster member is replaced with a (pseudo-) random validator that has a similar failure rate.

I also explicitly separate out **fumbles** and **misses**. I define these terms as follows:

- Fumble: when a validator misses an attestation during the current epoch, but attested correctly during the previous epoch
- Miss: when a validator misses an attestation during the current epoch and also missed during the previous epoch

The goal is to separate the two very different phenomena of (i) network hiccups during normal operation, and (ii) going offline or having longer-term glitches.

I also simultaneously do this analysis for two datasets: **max-deadline** and **single-slot-deadline**. The first dataset treats a validator as having failed in an epoch only if an attestation was never included at all. The second dataset treats a validator as having failed if the attestation does not get included *within a single slot*.

Here are my results for the first two methods of computing expected co-failures. SSfumbles and SSmisses here refer to fumbles and misses using the single-slot dataset.

|  | Fumbles | Misses | SSfumbles | SSmisses |
| --- | --- | --- | --- | --- |
| Expected (algo 1) | 8602090 | 1695490 | 604902393 | 2637879 |
| Expected (algo 2) | 937232 | 4372279 | 26744848 | 4733344 |
| Actual | 15481500 | 7584178 | 678853421 | 8564344 |

For the first method, the `Actual` row is different, because a more restricted dataset is used for efficiency:

|  | Fumbles | Misses | SSfumbles | SSmisses |
| --- | --- | --- | --- | --- |
| Fake clusters | 8366846 | 6006136 | 556852940 | 5841712 |
| Actual | 14868318 | 6451930 | 624818332 | 6578668 |

The “expected” and “fake clusters” columns show how many co-failures within clusters there “should have been”, if clusters were uncorrelated, based on the techniques described above. The “actual” columns show how many co-failures there actually were. Uniformly, we see strong evidence of “excess correlated failures” within clusters: two validators in the same cluster are significantly more likely to miss attestations at the same time than two validators in different clusters.

## How might we apply this to penalty rules?

I propose a simple strawman: in each slot, let `p` be the current number of missed slots divided by the average for the last 32 slots. That is, p[i] =
\frac{misses[i]}{\sum_{j=i-32}^{i-1}\ misses[j]}. Cap it: p \leftarrow min(p, 4). Penalties for attestations of that slot should be proportional to p. That is, **the penalty for not attesting at a slot should be proportional to how many validators fail in that slot *compared to other recent slots***.

This mechanism has a nice property that it’s not easily attackable: there isn’t a case where failing *decreases* your penalties, and manipulating the average enough to have an impact requires making a large number of failures yourself.

Now, let us try actually running it. Here are the total penalties for big clusters, medium clusters, small clusters and all validators (including non-clustered) for four penalty schemes:

- basic: Penalize one point per miss (ie. similar to status quo)
- basic_ss: the same but requiring single-slot inclusion to not count as a miss
- excess: penalize p points with p calculated as above
- excess_ss: penalize p points with p calculated as above, requiring single-slot inclusion to not count as a miss

Here is the output:

```auto
                   basic          basic_ss       excess         excess_ss
big                0.69           2.06           2.73           7.96
medium             0.61           3.00           2.42           11.54
small              0.98           2.41           3.81           8.77
all                0.90           2.44           3.54           9.30
```

With the “basic” schemes, big has a ~1.4x advantage over small (~1.2x in the single-slot dataset). With the “excess” schemes, this drops to ~1.3x (~1.1x in the single-slot dataset). With multiple other iterations of this, using slightly different datasets, **the excess penalty scheme uniformly shrinks the advantage of “the big guy” over “the little guy”**.

## What’s going on?

The number of failures per slot is small: it’s usually in the low dozens. This is much smaller than pretty much any “large staker”. In fact, it’s smaller than the number of validators that a large staker would have active *in a single slot* (ie. 1/32 of their total stock). If a large staker runs many nodes on the same physical computer or internet connection, then any failures will plausibly affect all of their validators.

What this means is: when a large validator has an attestation inclusion failure, they single-handedly move the current slot’s failure rate, which then in turn increases their penalty. Small validators do not do this.

In principle, a big staker can get around this penalty scheme by putting each validator on a separate internet connection. But this sacrifices the economies-of-scale advantage that a big staker has in being able to reuse the same physical infrastructure.

## Topics for further analysis

- Find other strategies to confirm the size of this effect where validators in the same cluster are unusually likely to have attestation failures at the same time
- Try to find the ideal (but still simple, so as to not overfit and not be exploitable) reward/penalty scheme to minimize the average big validator’s advantage over little validators.
- Try to prove safety properties about this class of incentive schemes, ideally identify a “region of design space” within which risks of weird attacks (eg. strategically going offline at specific times to manipulate the average) are too expensive to be worth it
- Cluster by geography. This could determine whether or not this mechanism also creates an incentive to geographically decentralize.
- Cluster by (execution and beacon) client software. This could determine whether or not this mechanism also creates an incentive to use minority clients.

## Mini-FAQ

**Q**: But wouldn’t this just lead to staking pools architecturally decentralizing their infra without politically decentralizing themselves, and isn’t the latter what we care about more at this point?

**A**: If they do, then that increases the cost of their operations, making solo staking relatively more competitive. The goal is not to single-handedly force solo staking, the goal is to make the economic part of the incentives more balanced. Political decentralization seems very hard or impossible to incentivize in-protocol; for that I think we will just have to count on social pressure, starknet-like airdrops, etc. But if economic incentives can be tweaked to favor architectural decentralization, that makes things easier for politically decentralized projects (which cannot avoid being architecturally decentralized) to get off the ground.

**Q**: Wouldn’t this hurt the “middle-size stakers” (wealthy individuals who are not big exchanges/pools) the most, and encourage them to move to pools?

**A**: In the table above, the “small” section refers to stakers with 10-300 validators, ie. 320-9600 ETH. That includes most wealthy people. And as we can see, those stakers suffer significantly higher penalties than pools today, and the simulation shows how the proposed adjusted reward scheme would equalize things between precisely those validators and the really big ones. Mathematically speaking, someone with 100 validator slots would only have 3 per slot, so they would not be greatly affecting the penalty factor for a round; only validators that go far above that would be.

**Q**: Post-MAXEB, won’t big stakers get around this by consolidating all their ETH into one validator?

**A**: The proportional penalty formula would count total amount of ETH, not number of validator IDs, so 4000 staked ETH that acts the same way would be treated the same if it’s split between 1 validator or 2 or 125.

**Q**: Won’t adding even more incentives to be online create further pressure to optimize and hence centralize, regardless of the details?

**A**:The parameters can be set so that on average, the size of the incentive to be online is the same as it is today.

## Replies

**Mirror** (2024-03-27):

I’m delighted to see your engagement with this issue, and I support the initiative to enhance Ethereum staking decentralization by introducing more anti-correlation incentives. The additional risks posed to Ethereum when multiple validators err simultaneously, especially if they’re part of the same cluster, like staking pools, are noteworthy. Reducing the advantage large stakers have over smaller ones contributes to our network’s decentralization. However, I have concerns:

1. Will this “measure” be implemented at the base or application layer? (Concerning the complexity of implementing such a system)

2.Incentives may result in unforeseeable games and ensure that punishment mechanisms do not disproportionately affect smaller validators or validators that do not have the ability to diversify their infrastructure.

This tactic could lead to a situation where large stakers, by investing in multiple diverse setups, manage to dilute the impact of correlated penalties, thus maintaining their economies of scale advantage while appearing more decentralized. This approach could potentially undermine the intended effect of promoting genuine decentralization by incentivizing superficial compliance with the anti-correlation mechanisms rather than encouraging a broader distribution of validation power.

3.To avoid operational complexity and correlated failures while minimizing risk, validators should diversify their infrastructure geographically and across different software clients. Automating operational processes to limit human error, and implementing effective monitoring and alerting systems for rapid issue resolution, are also advisable. Engaging with other validators to share best practices and experiences can further aid in achieving these goals. This strategy seeks to maintain operational efficiency alongside network decentralization and resilience.

---

**ComfyGummy** (2024-03-27):

(*Disclaimer: I am a home staker.*)

Thanks again for engaging on this issue, it is appreciated. I think Ethereum’s correlation penalty is one of its best staking-decentralization incentivization mechanisms, and IMO it is under-utilized and could be doing so much more.

I’ve actually pointed this out in [an earlier post](https://ethresear.ch/t/how-optional-non-kyc-validator-metadata-can-improve-staking-decentralization/17032) that uses this mechanism to encourage adding proper protocol-legible metadata about validators. The details are in the post, but the tl;dr is to **reduce the correlated failure penalty if the validators had voluntarily declared themselves as run by the same operator**, and/or increase the correlated failure penalty if they had not.

More generally, I’d love a discussion on how **the design space of the correlated-failure mechanism can be enhanced if validators had [protocol-legible ownership metadata](https://ethresear.ch/t/how-optional-non-kyc-validator-metadata-can-improve-staking-decentralization/17032) attached to them**.

---

I’d also like to point out something about one of the assumptions from the OP, which I believe to be overly reductive:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Such stakers could always make an independent physical setup for each node, but if they end up doing so, it would mean that we have completely eliminated economies of scale in staking.

While I am a home staker (not a large staking operator), I have experience running online services at scale and I can attest that **the hardware cost of replicating identical physical setups is only a tiny part of the economies of scale that large service operators enjoy**. The other large-but-scalable cost that stakers have are in the form of “devops” or maintenance work. This is work like:

- Monitoring the node and validator daemons (alerts, dashboards).
- Responding to incidents quickly and effectively.
- Having redundancy built into the system.
- Rotating keys (not necessarily validator keys; can also be OpenSSH keys to the servers themselves).
- Hardening servers and protect against intrusion (especially relevant for validators as they have hot keys in them).
- Handling software upgrades (of the Ethereum software or just the regular software on the server it runs on).
- Moving accumulated ETH rewards for safekeeping, DeFi, or to new validators and spinning those up.
- Running sidecar software like mev-boost and ensuring its uptime and redundancy (multiple relays etc.)
- Implementing long-term fixes to reliability problems once they occur: disk-almost-full alerting, automated node pruning, automated fallbacks to secondary node software.
- Continuous integration infrastructure and tests for all of the above to ensure new replicas of this entire setup can be spun up on demand.
- Continuous deployment infrastructure to keep said infrastructure in sync with the intended configuration.

**This complexity needs to be solved only *once* per staking operator**, regardless of how many replicas of the physical setup exists. For a large operator, this is typically kept as a “configuration as code” setup (think Ansible/Kubernetes/Terraform configs) that define how to create and configure servers to have node software running and all the monitoring and security infrastructure around it, and paying humans to make themselves available around the clock should a problem happen. Once that is in place, from that point onwards, **spinning up new physical replicas of this infrastructure** becomes trivial. There is a large economy of scale realized in being able to reuse the same configuration-as-code setup to spin up the new replica.

Home stakers do not have the time or resources to invest into having setups of this level of reliability, so making multiple replicas (e.g. at a friend’s house) is a much more laborious process, and incident response is slower. Anecdotally, I personally only have email alerting if my validator starts missing attestations, and I usually only have time to look into it on the next weekend.

For this reason, I disagree with the assertion that “if [a large staking operator] ends up [making an independent physical setup], it would mean that we have completely eliminated economies of scale”. It helps, but it doesn’t completely eliminate them.

(This, by the way, is one reason why Verkle trees are an exciting development for home stakers: they reduce not just the hardware requirements, but more importantly **the number of possible failure modes** that Ethereum node clients can have, thereby reducing the relative effectiveness of the reliability work going into large-scale staking operation.)

---

I was also going to ask the question about how MaxEB changes things, but looks like the mini-FAQ you added covers that. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**vshvsh** (2024-03-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> We can check this by combining two datasets: (i) attestation data from some recent epochs showing which validators were supposed to have attested, and which validators actually did attest, during each slot, and (ii) data mapping validator IDs to publicly-known clusters that contain many validators (eg. “Lido”, “Coinbase”, “Vitalik Buterin”). You can find a dump of the former here , here  and here , and the latter here .

Using historical data from times of network-wide instability could be an important test case for choosing the right parameters here.

I think the idea is interesting idea, but should be number-crunched for some important historical cases to understand how it impacts the staking in practice. The infra used for node operation is multi-layered:

- physical machine
- location (e.g. house or data center)
- network connection
- operating person
- consensus client
- execution client
- signing software/hardware

And home stakers have a definite advantage in diversity (so, protection from correlation) only on operating person, physical machine, and, to a lesser extent, internet connection. Which is to say, if attestation misses are the result of client bug (happened before at scale) or country-wide internet problems (didn’t happen before at scale, I think), they are actually at disadvantage vs. professional operations who can afford 24/7 incident response, multi-client setups with fast switching etc. For stakers who use cloud infra the advantage is less pronounced (DC outage takes out everyone in the same DC).

I also think that the market’s answer to this might be more along the lines of improving liveness in bigger operations instead of decentralizing the stake more. The tech is already there, inter- and intra-operators DVT is working in production. A multi-client, multi-cloud dirk+vouch setup managed by a highly responsive team is expensive but very robust. I guess more incentive for DVT adoption is a good thing, though. Might also make on-prem/dedicated hardware setups less preferred to cloud ones.

Another rough edge could be geographical diversification. At the moment having nodes in Latam or Africa means you’re going to miss attestations regularly. With how forgiving the consequences of that are, it’s not a big deal but if in future it means you and everyone else in the region is put to “correlated, pls slash” bucket by protocol we might have a strong disincentive to geographical diversity.

And finally there’s a another source of correlated misses to keep in mind - when there’s problem with block proposing (e.g. because of a client bug, big outage or misconfiguration, mev-boost bug etc) there’s not enough place to put all the attestations and overall attestation rate drops. I think it’s mostly random, so it’s not likely your validator will miss two attestations in a row due to this. But this is another reason you can miss attestion where smaller and bigger operators are on equal terms.

TLDR risk is coming not just from stake concentration, but from any common infra, like clients used; and from just Ethereum network weather sometimes. And more even stake distribution helps with stake concentration vector of risk, but the rest of the risk stack I think actually favors robust DVT clusters or larger well managed high-availability cloud setups.

---

**potuz** (2024-03-27):

I think this is one of the best ideas I’ve seen in a while here and I’d love to work towards it. I think complexity concerns aren’t warranted since this would be a simple pure function executed at epoch transition that can be thoroughly tested on unit/spec tests.

I do worry about MaxEB for the opposite reason of what you mention though: if the correlated slots that trigger a steep penalty are substantially less than 32 (say failures for 4 consecutive slots are already enough) then large operators would be better off **not coalescing** their validators under Max EB to be protected from small network outages like for 4-5 slots. And this probably renders Max EB useless (so we should strictly restrict to misses instead of fumbles in your notation)

Another issue is builder/relay failure, we have essentially 3 builders responsible for all of our blocks and in the event that they fail then this would trigger heavy penalties on validators until the circuit breaker kicks in and we revert to local building.

I think we can mitigate some of these effects if we restrict ourselves to missing attestation penalties during times in which there weren’t missing blocks.

---

**OisinKyne** (2024-03-27):

Very supportive of correlation penalties! I’ve previously [advocated](https://x.com/OisinKyne/status/1758260104774693179?s=20) for starting the quadratic inactivity leak at a much higher percentage (e.g. 90), but I think a change like that comes under;

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> edge-case incentives that only arise in a highly exceptional attack situation that may never arise in practice are perhaps not sufficient for incentivizing decentralization

so I think a design around relative misses is more sensible. However I think we could explore a *non-linear* proportional penalty where you suggest:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Penalties for attestations of that slot should be proportional to p. That is, the penalty for not attesting at a slot should be proportional to how many validators fail in that slot compared to other recent slots.

I think [@vshvsh](/u/vshvsh) 's comment is pretty astute, and suggests a decent amount of retrospective analysis and prospective modelling would help with setting effective parameters for such a penalty.

I also want to highlight that this could hopefully be an effective way to put the finger on the scales for client diversity. We have had numerous liveness failures from clients, (and thankfully no safety failures) and if we tweaked the correlation penalties such that a double-digit% liveness failure resulted in a month or more of lost rewards, that would have an impact on operator behaviour in my opinion.

One ‘parameter’ that is probably closely intertwined with this one is the ‘socialised penalty’ that the whole network faces when participation is <100%. I think this feature is important and worth protecting, to keep operators in a win/win mindset with respect to uptime rather than win/lose, but some adjustment such that those who are offline during the outage get hit harder than those who remain online through the outage is probably not a bad thing.

---

**Evan-Kim2028** (2024-03-27):

How easy is it to classify different validators? Is this a largely “solved” problem already?

---

**Mirror** (2024-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> ## Sanity check: are errors by different validators in the same “cluster” actually more likely to correlate with each other?
>
>
>
> We can check this by combining two datasets: (i) attestation data from some recent epochs showing which validators were supposed to have attested, and which validators actually did attest, during each slot, and (ii) data mapping validator IDs to publicly-known clusters that contain many validators (eg. “Lido”, “Coinbase”, “Vitalik Buterin”). You can find a dump of the former here , here  and here , and the latter here .

look here An introduction to the proof history of proving datasets.

---

**Nero_eth** (2024-03-28):

Very easy and, for the proposal of slot-correlated penaties, it doesn’t matter (except for doing analysis).

Correlated penalties do not distinguish between entities but treat every validator the same. It just happens that there is a “natural” correlation between the individual validators that belong to one entity, based on running them on the same machine, the same network, the same clients etc.

---

**themandalore** (2024-03-28):

Awesome stuff and super excited to see some stronger language against correlation, especially the idea of using publicly known clusters (which is where this makes the sense).  Some of my iniitial thoughts:

1. I think the whole discussion around client diversity is enlightening in this regard.  The inactivity leak penalty is massive for correlating failures but yet it’s not doing much to actually jump start client diversity.  Whether we’re in this state or not is worth looking into (I’m guessing it’s a curve of adoption that once we’re past, they don’t mind)
2. As others have pointed out, a CEX that owns 90% of the stake but that distributes it amongst various LST’s/DVT’s is still a piss poor validator set when it comes to decentralization.
3. Addressing systemic risks – discouragement attacks against centralized validator sets - #2 by aelowsson. Wrote this post on a discouragement attack that seems relevant here.  This would make this particular discouragement attack even more severe as a large proposer (who also has lots of aggregators) could just ignore attestations of parties they claim are correlated.

For a question, If we don’t like the public mapped correlation, why are we not just coming to consensus on it and just limiting rewards/penalizing for size?

---

**vshvsh** (2024-03-28):

Yesterday’s data could be pretty interesting to grind here. 13% of lost slots over an hour and impact of that on correlated attestations would be supper interesting.

---

**Evan-Kim2028** (2024-04-01):

I was wondering more about this part and the steps involved, not necessarily just the end results. Maybe it’s just so easy that there isn’t much explanation involved

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> (ii) data mapping validator IDs to publicly-known clusters that contain many validators (eg. “Lido”, “Coinbase”, “Vitalik Buterin”)

---

**ensi321** (2024-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Q: Post-MAXEB, won’t big stakers get around this by consolidating all their ETH into one validator?
>
>
> A: The proportional penalty formula would count total amount of ETH, not number of validator IDs, so 4000 staked ETH that acts the same way would be treated the same if it’s split between 1 validator or 2 or 125.

Wouldn’t anti-correlation incentives drive big players away from consolidating their validators? Consolidation means higher correlation penalty when missing attestations.

In maxEB, we reduce the slashing penalty to incentivize them to consolidate.

---

**Nero_eth** (2024-06-13):

MaxEB is more expected to be used for consolidating the validators that you’re running from a single node already.

Also, MaxEB doesn’t come with any additional incentives to consolidate. The slashing penalty is reduced linearly without any advantages for consolidated parties - so, doesn’t count.

I see your point and it’s valid, however, one could argue that you shouldn’t run a large number of validators in one box that is high enough to trigger the anti-correlation penalty.

---

**aelowsson** (2024-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/ensi321/48/14461_2.png) ensi321:

> Consolidation means higher correlation penalty when missing attestations.

There is no difference between correlation penalties depending on consolidation, in the sense that someone running 64 32-ETH validators on the same faulty node and someone running 1 2048-ETH validator on the same node gets the same penalty.

However, I was considering if it might be beneficial to apply higher correlated attestation penalties on smaller (e.g., 32-ETH) validators, relatively speaking, in order to incentivize consolidation. The idea would be that it would be particularly suitable for penalizing those that run lots of 32-ETH validators, under the assumption that single 32-ETH validators will be less likely to suffer correlated penalties anyway.

But while this would hit non-consolidated correlated big stakers the most (good), it would still have a negative effect on small stakers relative to consolidated big stakers, and so this is problematic. It would also make the analysis more messy. So it is just something to keep in mind, but not really something I would actively promote now.

