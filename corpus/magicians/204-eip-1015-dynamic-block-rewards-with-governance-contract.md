---
source: magicians
topic_id: 204
title: EIP-1015 Dynamic Block Rewards With Governance Contract
author: alexvandesande
date: "2018-04-20"
category: EIPs
tags: [funding, eip-1015]
url: https://ethereum-magicians.org/t/eip-1015-dynamic-block-rewards-with-governance-contract/204
views: 4689
likes: 5
posts_count: 17
---

# EIP-1015 Dynamic Block Rewards With Governance Contract

Just wrote an EIP and I’d love to hear your feedback on it:

http://eips.ethereum.org/EIPS/eip-1015

## Replies

**MicahZoltu** (2018-04-21):

I’m personally against all forms of on-chain governance (so far proposed), including on-chain governance of subsets of the system like block rewards.

I predict that something like this will increase the cost of security because it introduces additional uncertainty for future block rewards.  Right now miners have to take on the risk of a future hard fork changing their future block rewards (and this is currently an extremely high risk due to the expectation of PoS).  This contract will not *remove* that risk, but instead adds a *new* risk in that the assembly can now *also* change future mining rewards, without a hard fork.  So where there was previously one risk of future block rewards changing, there are now two risks.

Since we can’t *prevent* hard forks changing block reward, I argue that adding in a second mechanism for changing block rewards doesn’t solve any new problem and instead just introduces potential problems and attack vectors.

---

**dontpanic** (2018-04-21):

It seems like it would be a hard sell to get miners on board with this.  You have essentially proposed an income tax on mining. Their either is not their’s anymore by virtue of work, rather it is theirs by the grace of the governance contract. The governance contract decides how much of their either will be used for other purposes.

---

**MicahZoltu** (2018-04-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dontpanic/48/98_2.png) dontpanic:

> It seems like it would be a hard sell to get miners on board

Reminder: Miners don’t have a say in hard forks (or anything else).  Miners are a fungible (easily replaced) service provider and they will capitulate to whatever future economic participants want.

---

**dontpanic** (2018-04-21):

That is nonsense and under values a key participant in the network. The future state of eth may be PoS, however it is currently proof of work.  All decisions get ratified by miners or the chain splits.

---

**alexvandesande** (2018-04-22):

[@MicahZoltu](/u/micahzoltu) interesting point regarding the increase on security due to uncertainty. On that regards I’d like to add a few points:

- this would only make sense during the move to PoS, when block rewards to miners are being slashed anyway and validador rewards are likely to still need tweaking
- if there’s a known minimum amount that must go towards security we could put that in the contract, but not sure it’s true since bitcoin for instance moves in the long term to a zero issuance scheme
- miners have some assurances guaranteed by the contract: among them that any changes in issuance can only happen with a huge advance notice, meaning that you are guaranteed that whatever you mine today and in the next six months, you’ll still receive.
- you misunderstood the purpose of split prevention. It’s not that it’s intended to prevent people from creating forks, it’s important that this power remains with users, but it creates a non-consensus layer in which those questions can be addressed to disincentive people from forking. If they still feel disenfranchised then they can have the fork. It’s a negotiation table, not a disarming campaign

[@dontpanic](/u/dontpanic) do you feel miners got rob from “their” ether when we changed reward from 5 to 3? Feels foolish playing the semantic game of who ether in the protocol really belongs.

---

**dontpanic** (2018-04-22):

I dont think it is semantics challenge at all. The system guarantees only 3 ways to own ether, Premine, purchase, or mining. Mining serves as a proxy for purchasing ether in that one pays for electricity an equivalent worth as they would value the ether at (one ether always costs one ether to mine). The social contract, as I understand it is that each account owner owns their ether outright. No preconditions. Miners “purchasing” ether from the system by verifying transactions should have the same assurance that a trader purchasing from another user has; that the ether they purchase is theirs.

If all ether belongs to the system, rather than the indivdual account holder, more interesting taxation is possible but it does require a more formalized governance system.

I saw the reduction as pointless from a technical standpoint. The system functions equally well with 5, 100, or 3 ether being distributed. The change offered no technical benefit, and caused no harm. The average price per m/hash has remained relatively stable the last few years and is on par with coins that use the same algo. The hash market is pretty efficient.

The distinction between validators and miners is small. I would assume the same expectations from a validator in pos as a miner in pow; a way to have fair representation and a long enough period after a vote for the minority to identify the change and adjust accordingly.

---

**alexvandesande** (2018-04-22):

But the miners would still have assurances: if they mine they will receive ether at the agreed upon price and these conditions will remain for at least six months. The only difference is that these conditions can change by a social contract (which will in itself also have delays to further increase these guarantees.

There’s an interesting question there about how can a  lock in work: if the goal is to align the receivers incentives with the long term health of the network and to give some long term guarantees, then i thought justa having a time delay would be sufficient but maybe it’s not (not sure if that’s where you were going), because it can lead to a situation where, if the receiving contract just delays payments by 6 months, it means that once a decision is made, miners mining right after the decision will not receive their ether in 6 months and that’s certainly not something we want.

Maybe it would be necessary to have a period of x weeks between when any change was decided and it actually happening, and another period of x weeks between a change happening and the contract being able to ‘withdraw’ from the issuance contract. This way there’s some assurance that, whatever work you are providing now, you will be surely paid and your ‘contract’ will guaranteed at least a few more months of work.

---

**lrettig** (2018-04-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I’m personally against all forms of on-chain governance (so far proposed), including on-chain governance of subsets of the system like block rewards.

How do you feel about the process today by which miners signal (on-chain) to set the per block gas limit?

---

**MicahZoltu** (2018-04-25):

I am generally fine with it since miners are incentivized to make blocks as big as possible without generating too many uncle’s.  The system isn’t perfect (miners don’t always move the needle when it is in their best interest) but overall I’m satisfied with it because incentives are properly aligned.  Also, it isn’t a democraticmprocess but rather a long term error correcting process.

---

**alexvandesande** (2018-04-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Also, it isn’t a democraticmprocess but rather a long term error correcting process.

So you would be a bit more in favor of this solution if it were about small changes over time, based on some sort of signal that is not hash power?

---

**dontpanic** (2018-04-25):

I think my internal understanding is changing and I agree in principal with the proposal. The role of the Decision Assembly seems pretty important.

Could this also be used as a fork killer? ie One side of the fork would have interest locking the issuance of the minority side of the fork to zero. similar to the bomb 2.0 that was discussed a while back.

---

**alexvandesande** (2018-04-25):

I did not consider the implications of a fork. But then, if you are already doing a fork you can as well also change the rewards contract for it to be in control of a friendly interest group.

I agree, the major outstanding point would be the how the decision is controlled, since I haven’t seen any 100% good governance proposal model. Being it a multisig with multiple governance contracts underneath is a way of allowing multiple contracts to be tested at the same time.

---

**MicahZoltu** (2018-04-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexvandesande/48/101_2.png) alexvandesande:

> So you would be a bit more in favor of this solution if it were about small changes over time, based on some sort of signal that is not hash power?

If we can come up with a mechanism such that selfish actors acting in their own short-sighted greedy self interest can set the block reward to an optimal or near-optimal value then yeah, I’m likely to be OK with it.

I’m not convinced there exists an actor who, when acting in their own short-sighted greedy self interest, can be incentivized to appropriately set the block reward.  Open to hear some arguments otherwise though. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**alexvandesande** (2018-04-26):

Reaching optimal values as a result of a competition between short-sighted greedy selfish parties is also my favorite governance model.

I do not know exactly how it would work either, but that’s why it’s the most open bit of the proposal.

---

**jamesray1** (2018-04-28):

Hi [@alexvandesande](/u/alexvandesande), may you please update the title to include the number? I.e. “EIP 1015: Dynamic…” I have heard arguments against onchain governance, e.g. as listed [here](https://github.com/ethereum/wiki/wiki/Governance-compendium#against-on-chain-governance) by Vlad and Vitalik. Essentially we need to be very careful about any kind of on-chain governance that modifies how the protocol operates, which is what this EIP is proposing, and need to make sure that existing participants that secure the network (such as miners with PoW, validators with PoS and proposers and collators with sharding) are not disenfranchised from the governance process.

---

**dontpanic** (2018-04-29):

The blockchain only provides for persistence of state, the governance concept provides for continuity. Continuity being the human understanding of the future desired state of the chain. Whether the process itself is off chain or on chain isn’t as important as if it is enforceable on chain. I think that this proposal serves as an executive role in the network

