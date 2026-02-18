---
source: ethresearch
topic_id: 17
title: The governance / fairness tradeoff in Casper
author: vbuterin_old
date: "2017-08-17"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/the-governance-fairness-tradeoff-in-casper/17
views: 2513
likes: 5
posts_count: 15
---

# The governance / fairness tradeoff in Casper

Suppose that an attacker with >=50% of the validator set attempts to carry out a censorship attack where they block all prepares and commits coming from the other validators. From the point of view of inside the protocol, this is indistinguishable from a scenario where the complement of the attacker (ie. the victim minority) is offline due to their own fault.

There are two possible schools of thought for how to design incentives in such a scenario. The first is to **heavily punish both the majority** (who is possibly a censoring attacker, and is possibly innocent) **and the minority** (who is possibly innocent, and possibly nodes that are offline because they are lazy or malicious). If we treat the validators as a captive and unchanging set, this creates strong incentives for all sides to act correctly. However, in the real world, validation is voluntary, and validators are unwilling to join games where they are likely to lose, and will be readily willing to leave such games. Hence, this opens up vulnerability to discouragement attacks, where an attacker carries out a low-grade attack which costs both themselves and victims just enough to make validation unprofitable (and in fact lossy), waits for victims to leave, and then attacks against a much smaller validator set.

**The alternative approach is to only penalize nodes that appear offline, and leave other nodes alone, even though it may be the case that it is the online nodes that are at fault because they are censoring**. In the case of 51% attacks, a “just” outcome can be reached through minority chain splits and market-based adjudication. We assume that honest validators simply ignore chains that appear to be censoring their own prepares and commits, and so we can expect these honest validators to form their own chain. This leads to two chains: chain A, run by the majority validators, where the majority keeps their deposits and the minority loses a large fraction of their deposits, and chain B, run by the minority validators, where the minority keeps their deposits and the majority loses a large fraction of their deposits. Note that the `PREPARE_COMMIT_CONSISTENCY` slashing condition makes it difficult for a validator to repeatedly “switch sides”; once they commit on one side, they will be stuck on that side until the other side reaches the point where it has justified a checkpoint.

We then rely on the market to adjudicate between the two chains, relying on the assumption that the market prefers a chain where attackers have less sway, and so whichever of the two chains is honest is the one that becomes dominant.

The problem is, however, that **this kind of market-based adjudication is expensive and risky**; if a community gets too used to it, then it may pose a centralization risk, and it is certainly a serious usability hurdle every time it happens. **So we want it to be expensive to cause a fault that causes the chain to split and devolve to market-based adjudication**. One possible compromise is to rely on the “penalize both sides” approach for low-grade faults, ensuring that attacking small minorities is unprofitable, but then limit the amount of money that validators who appear online can lose, effectively switching to the market-based adjudication approach in the specific case of high-grade faults where large damage to protocol execution is caused.

What are people’s thoughts on this?

## Replies

**MicahZoltu** (2017-08-17):

I haven’t been following along with Casper research, so I apologize if I’m way off base here.

Couldn’t the honest validators prove their honesty to end-users in this case via gossip network?  The idea would be that when a validator detects that it is being censored, it gossips out its validation to other nodes as a form of proof that “see, I tried to validate but as you can see the majority didn’t accept me”.  Any given node in the network can attempt to forward the validator’s message on behalf of the validator in order to verify that the validator was in fact being censored.

A client that does not want censorship among validators can then automatically choose the minority validator set (in your example) rather than the majority set because they know the majority set to be censoring.  The idea here is that individual clients are given the information necessary to detect censorship via gossip network.  Once they have that information, they can make an informed decision about whether censorship is occurring or the validator has connectivity problems.

Again, this approach may not work depending on how Casper is currently designed, in which case feel free to just say so with minimal details of why.  ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**vbuterin_old** (2017-08-18):

The problem with that line of thinking is that in a consensus network it’s important for all clients to arrive at the same view (or at least, if there are cases where clients might not arrive at the same view, then this should be viewed as an attack, and it should be expensive to cause such a scenario to happen). I personally have written a draft paper on automated censorship rejection [here](https://github.com/ethereum/research/tree/master/papers/censorship_rejection) where I try to approach this topic in a semi-rigorous way, and it’s hard. What you *could* do is try to give validators a level of warning, so that in cases where there is censorship taking place clients will see that they should be suspicious and manually make the decision. If you do it that way, as a warning system and decision-making aid rather than a fully automated mechanism, then I definitely think it can be quite useful in making market-based adjudication resolve more cheaply and quickly.

---

**nate** (2017-08-18):

@vitalik when you say “limit the amount of money that validators who appear online can lose, effectively switching to the market-based adjudication in the specific case of high-grade faults,” does this mean having a well-defined amount of lost deposits that will trigger a governance event?

Also, anyone have any kewl heuristics about validator “supply” based on returns/losses?

---

**vbuterin_old** (2017-08-19):

The idea is to try to design a mechanism where you can mathematically prove a claim of the form “it costs at least $X to trigger a governance event”.

---

**tim** (2017-08-19):

Hey this is a nice form! Let me reflect on this … ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=9)

---

**BenMahalaD** (2017-08-19):

It’s definitely a tough choice.

I don’t like having to punish the whole system for someone who is offline. It leads to people getting angry at each other for innocent mistakes and makes people feel like they aren’t in control of their own funds. If validators well decentralized, I suspect a few will be offline at any given time, leading to an effective decrease in the interest rate from the published value. This probably wouldn’t be large (and could be accounted for in the rate), but it would serve as a constant reminder that you’re ‘losing’ money to other people’s mistakes. A sort of baseline discouragement attack.

Alternatively, I don’t know how well you can automatically split the chain into ‘censors’ and ‘honest’ chain. The attackers could let some messages though randomly to make it seem like a local issue with the network of the node when it is in fact a global attack. It could take considerable time and statistical analysis to identify who the attackers are and exclude them into an honest chain. I guess this could be mitigated via the automated censorship rejection.

I think I’m leaning towards only punishing offline validators. Since, unlike PoW, there is no in-protocol incentive to censor validators, any incentive to do that must be extra-protocol. A large extra-protocol actor is something that human group dynamics and weak subjectivity should be well-suited to handle. Humans are generally loss-averse, so I don’t think a small constant bleed is worth the ability to punish a large attacker in-protocol. Especially, since such an attacker could plan for such a punishment and probably will have written off the losses anyway.

---

**vbuterin_old** (2017-08-20):

> The attackers could let some messages though randomly to make it seem like a local issue with the network of the node when it is in fact a global attack

In order for this to become a serious issue, the attackers would need to block >= 1/3 of prepares or commits in every epoch. If an attacker wanted to only reduce the revenues of one single validator, say because they had a grudge against them, then I agree the attack could be made difficult to detect, but that’s what the griefing factor analysis is for as a second line of defense: such an attack would cost the attacker as much (or at least almost as much) as it costs the victim.

If the attackers are blocking a large portion of prepares or commits, then online nodes would be able to much more clearly see who is responsible. This could be sped up further with commitments: clients could receive blocks from validators with a protocol where the client tells the validator about the prepares and commits *they* know about, and expect the validator to send back a signed message saying “yes, got it, and if I have an opportunity to include these prepares and commits but do not do so, then I will lose my entire deposit”. Malicious validators would then have to not reply to these requests, which would immediately make them look much more suspicious.

---

**Lars** (2017-08-20):

I like the idea of the market adjudicating between two chains. It certainly is expensive and risky, though.

My idea is that the process for such a thing can be prepared in advanced. If it would be well prepared, it would decrease the risk that an attacker would want to go that route. There are various way for such a preparation. E.g. it is possible to detect censorship using applications external to the blockchain. Any node should have all needed information and be able to do it.

It is important to minimize the social disruption and attacks. The goal would be for the economic majority to quickly being able to make a decision. As long as this doesn’t open up for other types of attacks…

---

**vbuterin_old** (2017-08-20):

I see two goals in social 51% attack resistance:

1. Minimize the risk that the attacker will somehow be able to exploit coordination difficulties and default pressures to force the outcome of market resolution in the attacker’s favor.
2. Maximize the amount of cost that needs to be paid by the attacker in order to force users to look at the results of the market resolution proceedings.

(1) then has two sub-goals: (i) preventing attacks from looking like legitimate chains, and (ii) preventing legitimate chains from being mistaken for attacks. If you try to make a formal definition of what is an attack and what is a legitimate chain, then there is going to be disagreement on the margin due to network latency; and arguably levels of service degradation that reach this borderline are themselves attacks in some sense, and so should with at least some probability cost the attacker.

Though this is the point where some of the ideas in my censorship rejection paper ( https://github.com/ethereum/research/tree/master/papers/censorship_rejection ) start to come in…

---

**Lars** (2017-08-31):

I just read the [To Sink Frontrunners, Send in the Submarines](http://hackingdistributed.com/2017/08/28/submarine-sends/). Could this idea be used? That is, if you suspect you are being censored, you could create special transactions with hidden information showing that you are indeed online. This information can be revealed afterwards, which means the censoring nodes can’t detect it. Such a transaction would cost gas, but would not be needed normally.

Admittedly, I suppose you can do a reverse kind of attack here. Where you censor yourself, and send these submarine messages to blame innocent nodes for censorship. I wonder if there is a way around this?

---

**MicahZoltu** (2017-08-31):

I believe the censors would just censor the reveal in this case, though I may be missing something?

---

**Lars** (2017-08-31):

Good question.

Maybe the honest validators would see this, recognize what is happening, and would automatically chain split away from the dishonest validators chain. All nodes would also see this chain split, and select the chain from the honest validators. The only nodes staying with the dishonest validators would be their own nodes.

Still, I don’t have an answer how to prevent a reverse attack, where someone is pretending to be censored.

---

**vbuterin_old** (2017-08-31):

The other problem with the submarine send approach is that the censors could just censor everything except for their own dummy transactions that they include to make it look like the chain is active. It’s a cool trick, but not an ironclad one against censors that are *really* determined.

---

**Tolanut** (2017-10-11):

Require validators to listen to some number of validators for a given number of total validators in a specific time. Offlinne accounts can be detected if they don’t have some special msg I think and could be subtracted from the total number of validators.Require those online to listen to one another Assign each validator a unique ID/index number so you can determine the number of prep msgs n commits to be received for each validator. If requirement is not met you’re punished

