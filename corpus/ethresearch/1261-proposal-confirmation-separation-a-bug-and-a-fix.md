---
source: ethresearch
topic_id: 1261
title: "Proposal/confirmation separation: a bug and a fix"
author: vbuterin
date: "2018-03-01"
category: Sharding
tags: [proposal-commitment]
url: https://ethresear.ch/t/proposal-confirmation-separation-a-bug-and-a-fix/1261
views: 4676
likes: 13
posts_count: 10
---

# Proposal/confirmation separation: a bug and a fix

The proposal/confirmation separation mechanism [proposed by Justin a few days ago](https://ethresear.ch/t/separating-proposing-and-confirmation-of-collations/1000/6) works as follows:

1. Proposers (a set that anyone can join) all create collations with headers, containing transactions, and broadcast the (signed) header (but not the body!). Each header also specifies a fee F, and we assume that the transactions in the collation have some total fee T which goes to the proposer.
2. The validator assigned to create a collation chooses a collation (generally, the one with the highest fee), an counter-signs it.
3. The proposer publishes the body

Only collations that are double-signed (by proposer and validator) and have an available body are eligible for inclusion in the canonical chain. The fee F goes to the validator *regardless* of whether or not the collation gets into the canonical chain, though the transaction fees T only go to the proposer if the collation does get included into the canonical chain. This creates incentive alignment: proposers have an incentive to publish the body, and validators have an incentive to co-sign the proposal that pays the highest fee.

However, there is one problem. An attacker can create collation headers with fees higher than actual available transaction fee levels, and then never publish the correponding collation bodies. Normally, this would be equivalent to publishing very expensive transactions to spam the network and shut out legitimate users that cannot afford to outbid the attacker, an attack that can cause some damage though ultimately can’t stop high-value transactions from getting in. Here, though, it’s worse, because by not publishing collation bodies, an attacker can prevent the main chain from growing, thereby facilitating a 51% attack.

The problem arises for a simple fundamental reason: *this mechanism allows an open set (proposers) to prevent validators’ blocks from contributing to the chain’s security*. One natural fix is conceptually simple: change the scoring rule of the chain to GHOST, and allow collation headers with unavailable bodies to contribute to a block’s score. This actually fixes the problem; however, GHOST is hard to implement.

We create a simpler version of GHOST with the following scheme. We start off by creating a one-layer-restricted version of GHOST, where we follow the following rule: if a block has score N, and the block has `k` children, then all children of that block have score N+k (and we can also interpret the “virtual score” of the block as being N+k-1). For example:

![image](https://ethresear.ch/uploads/default/original/3X/d/5/d5cd73e891101d1eb641f1fe54fd00a78bd19872.svg)

This already gives us much of what we want; collations that are one hop away from being in some collation’s ancestry chain contribute to that collation’s score. A malicious proposer may be able to create a bunch of collations that are all missing bodies that are on top of the same head, but the legitimate head’s score will continue accumulating at the same rate. However, it is hard to calculate; a block deep in history getting a child would lead to that block’s score increasing, and then the score of every other descendant of that block.

So I propose a simplification. We add to collation headers a field (chosen by the validator), `lookbehind_score_update`. We add to the storage record of each block a field, `child_count`, that stores the number of children the collation has. When processing `add_header`, we look back `lookbehind_score_update` steps in its ancestry, and at each step (proceeding further to nearer in history), set `collation.score = collation.parent.score + collation.parent.childcount`. Then at the end, we set `collation.score = collation.parent.score + min(1, collation.parent.childcount)` and then `collation.parent.childcount += 1`.

We may also wish to expose a function that allows the publisher of a header to retroactively recalculate the score of their header at any time, if they feel it is worth it to pay the gas fees to do so.

This allows the shard chains to continue to use a simple score-based fork choice rule, while incorporating enough elements of GHOST to ensure collations with missing bodies continue to contribute to security. It also solves the problem with direct uncle inclusion, where newer blocks are favored over older blocks because newer blocks can include older blocks as uncles but not vice versa.

## Replies

**jannikluhn** (2018-03-01):

> One natural fix is conceptually simple: change the scoring rule of the chain to GHOST, and allow collation headers with unavailable bodies to contribute to a block’s score.

If I understand correctly, the validator would add all proposal headers he can find to the chain. If at least one proposer is honest and publishes his body, the chain can grow. In this case who would get and who would have to pay fees?

My guess is that all proposers have to pay F, otherwise one could spam the validator (he has to pay for main-chain gas for each proposal). T is in the end always split up between all proposers that publish the body (either on average over time if only the winning proposal gets the fee, or explicitly at each collation height if all headers with bodies get a share). But this would be a problem, because proposers would have to predict the number of other proposers with which they have to split with, in order to set a good value for F (otherwise they would risk running on a loss).

---

**vbuterin** (2018-03-02):

> If I understand correctly, the validator would add all proposal headers he can find to the chain.

That’s not what I had in mind. One piece I forgot to mention is that there is a slashing condition where a validator *cannot* sign multiple proposals.

If you allow a validator to co-sign multiple proposals, then he could cheat proposers by stealing all of their fees; basically, exactly as you say. One possibility is to allow a validator to only submit *two* proposals, where the second one is empty; this essentially gives the next validator in line the opportunity to choose what to build off of. However, this is broken because the next validator will have the incentive to build off the empty one to steal its transaction fees.

Rather, what I am suggesting is that if the proposer griefs a validator by not publishing the collation body, then the double-signed collation will exist anyway, and will be published to the chain anyway, so this might as well be counted to contribute to the parent block’s security (see my diagram: the two siblings of the collation in the canonical chain with score 4 each effectively still contribute 1 point to its score).

---

**djrtwo** (2018-03-05):

Is the following restatement of the proposal/confirmation bug correct?

If the attacker holds enough available capital on the shard, they can outbid all honest proposers’ fees (F) by bidding above the economically viable max(T) for the current shard transaction pool/gas limit. The validator selects the attacker’s collation header because of the high F assuming that even if the data is withheld, they will receive the fee F.

The attacker then withholds the collation body, orphaning the collation header. If the chain continued to grow, the fee F would be transferred to the validator regardless of this orphaning, but because the chain has been stalled, the attacker has not yet lost their fee F and can simply perform the attack again on the next validator with the same source of capital. This attack can indefinitely stall the chain unless a validator chooses to build their own (potentially empty collation) or accept a non-attacking collation of much lower fee.

EDIT:

Realized that the transferring of fee F would happen in main-shard/VMC. So while the attacker can continue to attack, they would at least have to pay the fee F per attack and would incur a real cost.

---

**MaxC** (2018-03-05):

> It also solves the problem with direct uncle inclusion, where newer blocks are favored over older blocks because newer blocks can include older blocks as uncles but not vice versa.

Do you mean older blocks are favoured over newer blocks?

Suppose [7] is a valid block in your diagram. If a block proposer knows that data is unavailable, or likely to be, there is no incentive for him to add the block to [7], because he knows his block will be uncled and he will most likely have to wait longer to receive a reward. So he may as well add the block to [6] parent of [7] and be rewarded quicker.

However, in doing this, he still strengthens block [7].

---

**vbuterin** (2018-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> So while the attacker can continue to attack, they would at least have to pay the fee F per attack and would incur a real cost.

Correct. The problem is that the cost is far too low to be a deterrent. In regular proof of work or proof of stake, being able to temporarily outbid fees plus block rewards is not enough to accomplish an actual 51% attack in practice; you need to also get the majority of miners/validators to actually take some manual exceptional step to cooperate with you.

---

**JustinDrake** (2018-03-05):

(Putting on my devil’s advocate hat on ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9).)

I can’t get incentives to align. Before going into details I want to propose a basic model for proposer revenue T-F versus F:

1. Marginality: Because of proposer open competition we should expect small profit margins (and small revenue T-F) for proposers. The more proposers join in, the smaller the profit margins. This is in contrast to F which derives from an open auction where the more users means a higher F. In short, in a healthy market with many proposers and many users, T-F should be marginal versus F.
2. Unpredictability: Proposer open competition should also yield steady (non-volatile) profit margins. This is in contrast to total transaction fees T being wildly volatile and hard to predict (as we know empirically). In short, the ratio between T-F and F changes widely and is hard to predict.

We now go back incentive alignment. In general, if the design assumes validators do *not* have access to the collation body before posting the collation header to the VMC (in contrast to the [commitment-and-trapping scheme](https://ethresear.ch/t/proposer-withholding-and-collation-availability-traps/1294)) then either:

1. Proposers can grief validators, or
2. Validators get full payment (proposer fees and collation subsidy) for collations that contribute to security, even for unavailable collations.

Proposers having the option to grief validators seems bad. The marginality of T-F versus F (or versus F+S, where S is the collation subsidy) means there is a high incentive to grief. In turn, this encourages validators to do “credit scoring” on proposers (see [a similar argument here](https://ethresear.ch/t/alternative-fix-for-proposer-withholding-attack/1268/6)). The greater the demand for transaction fees the higher the incentive to grief, which in turn increases the need for validators to do credit scoring on proposers.

The other option is to give validators full payment, but this seems to introduce other bad things. In the diagram above the proposers for two of the three collations with a virtual score score of 4 (namely the leftmost and rightmost collations) would have to forgo F without any reward. The huge discrepancy between the potential reward (T-F) and the potential penalty (F), combined with the unpredictability of F, may make it hard for proposers to effectively run a business without taking huge risks.

This also opens the possibility for proposers to get griefed by other proposers, or by validators. Notice for example that because validators are guaranteed payment they can grief proposers for free, i.e. the griefing factor is infinite. In general I also dislike the idea of paying validators for unavailable collations because the clean separation between availability (enforced by validators) and validity (enforced by proposers) gets muddied.

---

**vbuterin** (2018-03-05):

Yep, agree that the scheme increases risks for proposers. My thinking so far has been “eh well, that just means that F will have a somewhat steeper discount against T”, though I suppose there may also be centralization risks as it encourages proposers to be more sophisticated actors?

---

**kladkogex** (2018-03-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> An attacker can create collation headers with fees higher than actual available transaction fee levels, and then never publish the correponding collation bodies

Here is an interesting alternative to think about:

1. You require proposers to publish encrypted bodies together with header, but encryption is weak - one can brute force key.
2. The strength of encryption is selected in such a way, that it is normally economically not viable for a validator to do brute forcing. In other words, the price of the computational time required to brute force is higher than T, so it makes more sense for the validator to ask the proposer for a key.
3. As the last resort, if the proposer withholds the key, the validator recovers the body by brute forcing  (this will require the validator to spend a significant amount of computational time ) and files a complaint against the proposer.
4. A proposer with a large number of complaints is punished against its deposit

---

**dlubarov** (2018-03-09):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> You require proposers to publish encrypted bodies together with header, but encryption is weak - one can brute force key.

Couldn’t proposers could still grief validators with proposals which turn out to be nonsense after they’re decrypted? Proposers could be punished for malformed proposals of course, but might as well skip the encryption and punish withholding.

