---
source: ethresearch
topic_id: 6646
title: "\"Ethereum Casper FFG PoS, like all PoS consensus protocols, is vulnerable to bribery censorship attacks.\""
author: jamesray1
date: "2019-12-17"
category: Proof-of-Stake
tags: [security]
url: https://ethresear.ch/t/ethereum-casper-ffg-pos-like-all-pos-consensus-protocols-is-vulnerable-to-bribery-censorship-attacks/6646
views: 4347
likes: 11
posts_count: 11
---

# "Ethereum Casper FFG PoS, like all PoS consensus protocols, is vulnerable to bribery censorship attacks."

Requesting for comment on this. #soft_fork #bribery #attacks



      [github.com](https://github.com/zack-bitcoin/amoveo/blob/a807dd26a5af156b8890474df7f709b0ddbe07cf/docs/other_blockchains/ethereum_casper_ffg.md)





####



```md
Review of Ethereum Casper FFG
==========

I wrote a paper about why all PoS blockchains are vulnerable to soft fork bribery attacks https://github.com/zack-bitcoin/amoveo/blob/master/docs/other_blockchains/proof_of_stake.md

In general, any attempt to recover from a soft fork bribery attack will have one of these shortcomings:
1) we undo the history that occured during the soft fork bribery attack, enabling the attacker to do double-spends between that version of history, and the new version.
2) we don't undo the history that occured during the soft fork bribery attack, so there was a period of time during which the soft fork attack was successful, and the attacker could have profited during that time.

In this blog post https://ethresear.ch/t/responding-to-51-attacks-in-casper-ffg/6363
Vitalik talks about Casper FFG and tries to explain why it is secure against this kind of attack.

Finality Reversion
==========

In the section of Vitalik's blog post titled "Finality Reversion", he explains why it is impossible to do a history rewrite attack, even if >50% of the validator stake is cooperating to attack.

Validator Censorship
==========

```

  This file has been truncated. [show original](https://github.com/zack-bitcoin/amoveo/blob/a807dd26a5af156b8890474df7f709b0ddbe07cf/docs/other_blockchains/ethereum_casper_ffg.md)










Edit:

I can attempt to summarize the information, although it is best to read all of it, however my concern was that this issue appeared to unresolved, and that the attack still seems well and truly possible.

Summary of the [first article](https://github.com/zack-bitcoin/amoveo/blob/master/docs/other_blockchains/proof_of_stake.md):

An attacker can theoretically (as ostensibly demonstrated in the proof) bribe validators of a PoS consensus system (including PoS blockchains like Casper FFG / Eth 2) with a small amount relative to the total amount of stake and market cap.

Some key snippets:

> According to tragedy of the commons, the cost to bribe the validators to form a majority coalition and destroy the blockchain is:

> ```auto
> LU = (how much the validators have to lock up)
> #V = (how many validators are there)
> Bribe = LU / (2 * #V)
> ```

> If there are 1000 validators, and the blockchain is worth $1 billion, and 90% of the value is staked, then the total cost to bribe >50% of the validators would be: ($1 billion) * (0.9) * (1/2) * (1/1000) => $450 000

> So less than $1/2 million in bribes is sufficient to completely destroy a $1 billion PoS blockchain.

## Replies

**dankrad** (2019-12-17):

Maybe you need to ask a more specific question if you want to get a reply on this. It seems like the two statements are correct, however they do not respond to the specific way in which [@vbuterin](/u/vbuterin) was addressing the attack, which was at the time the attack is detected. In this case, no reversion of a finalized chain occurs – the finalization essentally stalls until the attack is resolved one way or the other. Does that clarify things for you?

---

**jamesray1** (2019-12-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Maybe you need to ask a more specific question if you want to get a reply on this.

I edited my post.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> It seems like the two statements are correct, however they do not respond to the specific way in which @vbuterin was addressing the attack, which was at the time the attack is detected. In this case, no reversion of a finalized chain occurs – the finalization essentally stalls until the attack is resolved one way or the other. Does that clarify things for you?

I’m unconvinced. It looks like you’re responding to the finality reversion section of [Vitalik’s post](https://ethresear.ch/t/responding-to-51-attacks-in-casper-ffg/6363). However, in the soft fork bribery attack, it is proposed that it can be done by punishing validators who fail to participate in enforcing punishments

More generally speaking, I think the issue needs serious consideration, even to try to simulate or prove that such an attack can occur, and shouldn’t be readily dismissed. Given that PoS blockchains aim to secure billions in value, all possibly attacks should be thoroughly investigated as a priority, rather than BAU R&D. If an attacker can gain control of the network through this kind of attack, once they gain control this becomes stable, and it’s intractably hard to take back control. I think anyone responding in this thread should read the above articles [here](https://github.com/zack-bitcoin/amoveo/blob/1cdd149161037b1f3fa35952cf27b5422db0646e/docs/other_blockchains/proof_of_stake.md), and [here](https://github.com/zack-bitcoin/amoveo/blob/a807dd26a5af156b8890474df7f709b0ddbe07cf/docs/other_blockchains/ethereum_casper_ffg.md) and [Vitalik’s post](https://ethresear.ch/t/responding-to-51-attacks-in-casper-ffg/6363), if they haven’t already. (I’m not saying you didn’t, but just to be sure.)

TBH, I hadn’t read through all of [Responding to 51% attacks in Casper FFG](https://ethresear.ch/t/responding-to-51-attacks-in-casper-ffg/6363).

> The problem with trying to have evidence of censorship attacks is that even if the censorship attack is real, that doesn’t necessarily mean the history rewrite we are using to recover is 100% honest. It could have a double-spend attack embedded in it. It could be the case that the attacker is simultaniously doing a soft fork bribery attack to censor txs on-chain, and he is also doing a history re-write attack to do some double spending, and he can use evidence of the first attack to justify executing the second attack. So whichever side of the fork we go with, one of the attacks succeeds.

[The false flag attack](https://github.com/zack-bitcoin/amoveo/blob/a807dd26a5af156b8890474df7f709b0ddbe07cf/docs/other_blockchains/ethereum_casper_ffg.md#the-false-flag-attack) is a possible scenario/mechanism that it seems like it could potentially be used to attack the minority fork of a chain that attempts to recover from a 51% attack (like a censorship attack, aka a soft fork bribery attack).

I don’t have a lot of time to assess this further, as I: 1) am currently looking for a job 2) have already spent a lot of time volunteering for projects like Ethereum and Holochain 3) Am convinced that Holochain is better than blockchains.

Just wanted to flag to the Ethereum community that maybe they should spend some more time assessing this attack, as I don’t know whether it has been thoroughly disproved or resolved.

---

**dankrad** (2019-12-19):

The problems sound interesting, but I’m unconvinced any of them are as specific to PoS as is claimed. PoW chains are susceptible to bribery attacks. Hey you can just buy hashing power: https://www.nicehash.com/ – and that costs even much less than the amounts claimed in the post!

I understand the concern around the “moralistic enforcement”, that sounds like a serious problem. But I would say the fact that a miner’s equipment can’t be confiscated is a fallacy: If the equipment is specific to one chain’s hash function, then censoring the miner from that chain has the same effect as confiscating their equipment: They invested a huge amount of money and now can’t use it.

Not that this invalidates these as attacks, but it seems like they apply equally to PoW, so shouldn’t be used as an argument against moving to PoS.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> The false flag attack is a possible scenario/mechanism that it seems like it could potentially be used to attack the minority fork of a chain that attempts to recover from a 51% attack (like a censorship attack, aka a soft fork bribery attack).

It is very clear that the social consensus layer can fail, too. It’s a heuristic and the assumption in Vitalik’s post was that it would correctly identify an attack going on. The assumption is that everyone is either able to check the condition themselves or know some people they trust who can verify it for them. If we assume that people can be made to do anything by anyone on social media, then of course anything could happen.

---

**jamesray1** (2020-03-09):

It’s disappointing when I make a comment that compares Holochain and Ethereum, outlining disadvantages of Ethereum compared to Holochain, and the comment is hidden as being too promotional in nature. The problem with this is that there is another project with clear advantages over Ethereum and other blockchains, and it is important to take note. It’s impossible to not be promotional when using an example of another project to point out flaws with Ethereum. I suppose that this comment may be hidden too. ![:man_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/man_shrugging.png?v=14)

---

**dankrad** (2020-03-09):

The problem is that this is a research forum, and not one about opinions on whether one thing or another is better. Your post had a lot of very broadside critiques but no substance. With the introduction of holochain as the one that solves all of these problems it appears to be just advertising material.

I may be interested in your criticisms if you are willing to add substance to your posts.

---

**jamesray1** (2020-03-10):

There’s plenty of more technical detail written about how Holochain differs in architecture to provide scalability where speed improves as the network grows, while maintaining security, data integrity and resiliency.

I could talk about things more abstractly than making reference to Holochain, but I have constraints on my time, and why do that when you can just consider Holochain as a concrete or reference implementation of more abstract concepts and features for a scalable distributed ledger technology framework, that enables distributed apps and digital transactions?

Here is a brief technical intro to Holochain:

https://twitter.com/helioscomm/status/1221839172689784833

https://twitter.com/helioscomm/status/1221840026201276417

https://twitter.com/helioscomm/status/1221863587406180352

There is a core concepts guide that explains the Holochain architecture in an understandable way here: [Holochain Core Concepts: What is Holochain?](https://developer.holochain.org/docs/concepts/). You’ll probably censor my post if I copy and paste from there, but here I go anyway:

> Holochain approaches the problem from a different set of assumptions. Reality offers a great lesson—agents in the physical world interact with each other just fine without an absolute, ordered, total view of all events. We don’t need a server or global public ledger.
>
>
> We start with users, not servers or data, as the primary system component. The application is modeled from the user perspective, which we call agent-centric computing. Empowered by the Holochain runtime, each user runs their own copy of the back end code, controls their identity, and stores their own private and public data. An encrypted peer-to-peer network for each app means that users can find each other and communicate directly.
>
>
> Then we ask what sort of data integrity guarantees people need in order to interact meaningfully and safely with one another. Half of the problem is already solved—because everyone has the ‘rules of the game’ in their copy of the code, they can verify that their peers are playing the game correctly just by looking at the data they create. On top of this, we add cryptographic proofs of authorship and tamper resistance.
>
>
> This is Holochain’s first pillar: intrinsic data integrity .
>
>
> However, we’re only halfway there. It’s not particularly resilient; data can get lost when people go offline. It also makes everyone do a lot of their own work to find and validate data.
>
>
> So we add another pillar: peer replication and validation . Each piece of public data is witnessed, validated, and backed up by a random selection of devices. Together, all cooperating participants detect modified or invalid data, spread evidence of corrupt actors or validators, and take steps to counteract threats.
>
>
> These simple building blocks create something surprisingly robust—a multicellular social organism with a memory and an immune system. It mimics the way that biological systems have managed to thrive in the face of novel threats for millions of years.
>
>
> The foundation of Holochain is simple, but the consequences of our design can lead to new challenges. However, most of the solutions can be found in the experiences of real life, which is already agent-centric. Additionally, some of the trickier problems of distributed computing are handled by Holochain itself at the ‘subconscious’ layer. All you need to do is think about your application logic, and Holochain makes it work, completely free of central servers.

---

**dankrad** (2020-03-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> I could talk about things more abstractly than making reference to Holochain, but I have constraints on my time, and why do that when you can just consider Holochain as a concrete or reference implementation of more abstract concepts and features for a scalable distributed ledger technology framework, that enables distributed apps and digital transactions?

Well, that’s the point. This forum isn’t for links to some other kind of documentation, it’s for direct exchange about new research. If you aren’t willing to write [because you don’t have the time] not just an explanation on how it works and a discussion of its advantages and disadvantages, then why are you writing in this forum? It seems it’s just to advertise the project, and that’s simply not what the forum is for.

---

**jamesray1** (2020-03-11):

It’s also to express concern about how a lot of time and money is being invested into blockchains when they seem to be fundamentally limiting when compared to Holochain apps.

---

**dankrad** (2020-03-11):

Well, you are once again proving the point here. Obviously you want to proselytize and not share research. Please find another forum to do this.

---

**BenMahalaD** (2020-03-11):

This thread is a bit off the rails, but I do want to make a couple of comments on the original link (mostly for my own understanding).

First, censorship attacks on ETH are hard in general ([link](https://hackingdistributed.com/2016/06/28/ethereum-soft-fork-dos-vector/)), so it is non-trivial for a set of validators to decide to censor a transaction even if they are completely colluding without opening themselves up to large vulnerabilities. Given that, in practice, any censorship attack involves changing the software of the colluding validators, and that this is complex software handling large $ sums of coins, there is a large lower bound to the real cost of any attempted attack - how can validators who decide to join the collusion be assured that the new software to support censorship is not backdoored? Regardless of the theoretical costs, this makes the practical cost significantly larger for carrying out any significant real attack.

More importantly, this pushes two general equilibrium - either no censorship, or 100% censorship (empty blocks) as anything in-between is vulnerable. However, an empty blocks attack is the easiest to coordinate community support for minority soft fork expulsion of the attackers. (MSF, or perhaps UAMSF, I’ll get the hats ![:tophat:](https://ethresear.ch/images/emoji/facebook_messenger/tophat.png?v=12))

Secondly, this statement:

> In this section of Vitalik’s paper, he attempts to explain why if >50% of stake decides to censor our txs in the blocks we build, that the remaining minority of stakers is consistently able to do a history re-write attack to undo the censorship attack.

which leads to contradiction. However, this is contraction is not applicable, as a minority soft fork is NOT a history re-write but a reverse censorship attack. For example, assume a majority validator set is censoring X. The MSF make a chain that includes X (which the attacker cannot build on, since they are censoring) and refuse to build on any chain that does not include X (the attacker’s chain).

Assuming neither side gives up, this causes a permanent chain split. After inactivity leakage runs its course, the chain that includes X will have no attacker deposits, and the chain that does not include X will have no MSF deposits. It is then up to the social layer to decide that the MSF is the ‘real’ ETH and the attacker chain is false, and decide to use the MSF chain.

At no point is any history rewritten or finality reverted, two parallel valid histories exist. This is obviously not ideal, but it is probably the best that can be done given the situation.

