---
source: ethresearch
topic_id: 9022
title: Simplified Active Validator Cap and Rotation Proposal
author: vbuterin
date: "2021-03-27"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/simplified-active-validator-cap-and-rotation-proposal/9022
views: 14409
likes: 32
posts_count: 23
---

# Simplified Active Validator Cap and Rotation Proposal

The goal of this proposal is to cap the active validator set to some fixed value (eg. 2^{19} validators) while at the same time ensuring three key properties:

1. An economic finality guarantee where close to 1/3 of the cap must be slashed to finalize two conflicting blocks
2. Low long-term variance in validator income
3. Maximum simplicity.

A validator size cap is desirable because it increases confidence that a given level of hardware will *always* be sufficient to validate the beacon chain. The proposed 2^{19} cap reduces the theoretical max number of validators from a near-term ~3.8M to a permanent ~524k, a factor of seven. This extra guarantee can be used to either guarantee a lower level of hardware requirements, increasing accessibility of staking, or reduce the deposit size, increasing the computational complexity of validation again but decreasing the possibly much larger factor of the minimum amount of ETH needed to participate.

The key properties are achieved by bringing back a modified version of the “dynasty” mechanism from the [Casper FFG paper](https://arxiv.org/abs/1710.09437). In short, if there are more than `MAX_VALIDATOR_COUNT` active validators, only `MAX_VALIDATOR_COUNT` of them will be “awake” at any time, and every time the chain finalizes the portion of validators that are awake gets rotated so that it changes by ~1/64. This ensures that the level of finalization safety is almost the same (see the Casper FFG paper for reasoning), while at the same time ensures that rotation is fairly quick, ensuring low variance (meaning, there won’t be validators who get very unfairly low returns due to the bad luck of never being awake).

### Constants

| Constant | Value | Notes |
| --- | --- | --- |
| MAX_VALIDATOR_COUNT | 2**19 (= 524,288) | ~16.7M ETH |
| ROTATION_RATE | 2**6 (= 64) | Up to 1.56% per epoch |
| FINALIZED_EPOCH_VECTOR_LENGTH | 2**16 (= 65,536) | 32 eeks ~= 291 days |
| FINALITY_LOOKBACK | 2**3 (= 8) | Measured in epochs |

### The state.is_epoch_finalized bitarray

We add a new `BeaconState` member value:

```python
    is_epoch_finalized: BitList[FINALIZED_EPOCH_VECTOR_LENGTH]
```

The first value stores which epochs have been finalized; the second stores a counter of how many epochs were finalized in the time that is too far back in history for the array to store.

In the `weigh_justification_and_finalization` function, when `state.finalized_checkpoint` is updated to `new_checkpoint`, we update:

```python
current_epoch_position = (
    get_current_epoch(state) %
    FINALIZED_EPOCH_VECTOR_LENGTH
)
state.is_epoch_finalized[current_epoch_position] = False
# In all cases where we do `state.finalized_checkpoint = new_checkpoint`
new_finalized_epoch_position = (
    new_checkpoint.epoch %
    FINALIZED_EPOCH_VECTOR_LENGTH
)
state.is_epoch_finalized[new_finalized_epoch_position] = True
```

We can also refine the “was this epoch finalized?” helper:

```python
def did_epoch_finalize(state: BeaconState, epoch: Epoch) -> bool:
    assert epoch  get_current_epoch(state)
    return state.is_epoch_finalized[epoch % FINALIZED_EPOCH_VECTOR_LENGTH]
```

### Definition of get_awake_validator_indices and helpers

`get_awake_validator_indices` returns a subset of `get_active_validator_indices`. The function and helpers required for it are defined as follows.

This next function outputs a set of validators that get slept in a given epoch (the output is nonempty only if the epoch has been finalized). Note that we use the finality bit of epoch N and the active validator set of epoch N+8; this ensures that by the time the active validator set that will be taken offline is known there is no way to affect  finality.

```python
def get_slept_validators(state: BeaconState,
                         epoch: Epoch) -> Set[ValidatorIndex]:
    assert get_current_epoch(state) >= epoch + MAX_SEED_LOOKAHEAD * 2
    active_validators = get_active_validator_indices(state, epoch + FINALITY_LOOKBACK)
    if len(active_validators) >= MAX_VALIDATOR_COUNT:
        excess_validators = len(active_validators) - MAX_VALIDATOR_COUNT
    else:
        excess_validators = 0
    if did_epoch_finalize(state, epoch):
        seed = get_seed(state, epoch, DOMAIN_BEACON_ATTESTER)
        validator_count = len(active_validators)
        return set(
            active_validators[compute_shuffled_index(i, validator_count, seed)]
            for i in range(len(excess_validators // ROTATION_RATE))
        )
    else:
        return set()
```

This next function outputs the currently awake validators. The idea is that a validator is awake if they have not been slept in one of the last `ROTATION_RATE` finalized epochs.

```python
def get_awake_validator_indices(state: BeaconState,
                                epoch: Epoch) -> Set[ValidatorIndex]:
    o = set()
    finalized_epochs_counted = 0
    search_start = FINALITY_LOOKBACK
    search_end = min(epoch + 1, FINALIZED_EPOCH_VECTOR_LENGTH)
    for step in range(search_start, search_end):
        check_epoch = epoch - step
        if did_epoch_finalize(check_epoch):
            o = o.union(get_slept_validators(state, finalized_epoch))
            finalized_epochs_counted += 1
            if finalized_epochs_counted == ROTATION_RATE:
                break
    return [v for v in get_active_validator_indices(state, epoch) if v not in o]
```

The intention is that `get_awake_validator_indices` contains at most roughly `MAX_VALIDATOR_COUNT` validators (possibly slightly more at certain times, but it equilibrates toward that limit), and it changes by at most `1/ROTATION_RATE` per finalized epoch. The restriction to finalized epochs ensures that two conflicting finalized blocks can only differ by at most an extra `1/ROTATION_RATE` as a result of this mechanism (it can also be viewed as an implementation of the [dynasty mechanism from the original Casper FFG paper](https://arxiv.org/pdf/1710.09437.pdf)).

### Protocol changes

All existing references to `get_active_validator_indices` are replaced with `get_awake_validator_indices`. Specifically, only awake indices are shuffled and put into any committee or proposer selection algorithm. Rewards and non-slashing penalties for non-awake active validators should equal 0. Non-aware active validators should still be vulnerable to slashing.

### Economic effects

- Once the active validator set size exceeds MAX_VALIDATOR_COUNT, validator returns should start decreasing proportionately to 1/total_deposits and not 1/sqrt(total_deposits). But the functions to compute total_deposits -> validator_return_rate and total_deposits -> max_total_issuance remain continuous.
- Validators active in epoch N can affect the finalization status of epoch N. At that time, the active validator set in epoch N+8 is unknown. Hence, validators have no action that they can take to manipulate the randomness to keep themselves active.
- Validators can delay finality to keep themselves active. But they cannot increase their profits by doing this, as this would put them into an inactivity leak.

### Alternatives

- Upon activation, a validator receives a pseudorandomly generated timezone in 0...511. If VALIDATOR_COUNT > MAX_VALIDATOR_COUNT, the validators awake are those whose (timezone + get_number_of_times_finalized(state, epoch)) % 512 < (512 * MAX_VALIDATOR_COUNT) // VALIDATOR_COUNT. This could simplify the logic for determining who is awake
- Make awake and sleep periods longer, and allow validators who have been asleep recently to withdraw more quickly after exiting (this may only be worth exploring after when withdrawals are available)

## Replies

**jgm** (2021-03-28):

My problem with an attempt to define a validator cap is this:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A validator size cap is desirable because it increases confidence that a given level of hardware will always be sufficient to validate the beacon chain.

I don’t see how this can be the case.  We’re already seeing changes coming that increases the requirements for validators: sync committees, sharding, and the merge all increase CPU, network and storage requirements for a beacon node.  A server that can handle validation with the current number of validators today may not be able to do so in Altair, even without an increase in the number of validators.

I will also say that I’m also not a fan of this specific system.  A system that leaves validators in the activation queue until there is room for them due to others exiting seems to provide superior results for all three key properties listed at the beginning of the proposal.

---

**vbuterin** (2021-03-28):

> I don’t see how this can be the case. We’re already seeing changes coming that increases the requirements for validators: sync committees, sharding, and the merge all increase CPU, network and storage requirements for a beacon node. A server that can handle validation with the current number of validators today may not be able to do so in Altair, even without an increase in the number of validators.

That’s true, but if we have the guarantee *conditional on any specific protocol spec*, then at least when we change the protocol spec we can check how well developers are handling the load and if needed design the spec in such a way that total computing costs go down or stay the same.

> A system that leaves validators in the activation queue until there is room for them due to others exiting seems to provide superior results for all three key properties listed at the beginning of the proposal.

That option *really* fails the “variance” criterion: whoever got there first gets all the rewards, everyone who comes later gets none. The alternative where new validators joining immediately ejects existing ones has the opposite problem, where an attacker can kick out defenders more easily. Hence, we need some probabilistic combination of waiting list and ejection where neither old validators nor new validators are favored. This scheme accomplishes that.

---

**jgm** (2021-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> That option really fails the “variance” criterion…

I suppose it depends on how you are looking at variance.  You appear to be looking at it from the point of view of all validators over a relatively short time period.  I’m looking at it from the point of view of single validator over its lifetime.  So if there was a queue then once the validator becomes active its variance would basically be 0.  Ultimately, those who validate will be more interested in the variance of their validator(s) than those of the network as a whole.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> …whoever got there first gets all the rewards, everyone who comes later gets none…

Yep, but this is at least an informed decision.  At the point in time someone considers becoming a validator they  can look at the active set, queue, and rate of exit and make a call as to if they want to enter the queue or not.  The current proposal is a rewrite of the rewards for all validators, which would be tough to take before at least the option of withdrawal were available.

---

**vbuterin** (2021-03-28):

I guess the better word than “variance” is “fairness”. Some validators getting much more and others getting much less due to random chance is bad, some validators getting more and others getting zero because of who came first is also bad (even more bad imo!).

> The current proposal is a rewrite of the rewards for all validators, which would be tough to take before at least the option of withdrawal were available.

To be clear, I’m not proposing this before the option of withdrawals; in fact I don’t think the current roadmap (Altair, then full-speed-ahead to the merge, then withdrawals and other beacon chain hard forks) leaves open any *possibility* of doing this before withdrawals.

---

**PhABC** (2021-03-28):

> Low long-term variance in validator income

Is this meant to be a claim when comparing to current model or a cap model without the dynasty mechanism? If the former, I don’t think the income variance will be lesser than current model considering your validator may be put to sleep for an unknown period of time. Maybe should specify that it’s a low income variance *across* validators, because the long-term income variance of any single validator is just as high as with a model without a cap.

---

**vbuterin** (2021-03-28):

Right, the claim is just that it doesn’t *make variance much worse*; the variance that exists in the current system still remains.

---

**aelowsson** (2021-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> A system that leaves validators in the activation queue until there is room for them due to others exiting seems to provide superior results for all three key properties listed at the beginning of the proposal

I think a queue could lead to various security issues, since such a quasi-permissioned system will enable stakers “on the inside” to exercise undue control over the chain. It can also lead to rent-seeking behavior.

---

**aelowsson** (2021-03-31):

> Once the active validator set size exceeds MAX_VALIDATOR_COUNT , validator returns should start decreasing proportionately to 1/total_deposits and not 1/sqrt(total_deposits). But the functions to compute total_deposits -> validator_return_rate and total_deposits -> max_total_issuance remain continuous.

Perhaps you could clarify, this means that there will be a hard cap to the total issuance? Because there are two obvious options: (A) either the active validators are compensated in proportion to the rate at which they will be inactive, keeping `1/sqrt(total_deposits)`, or (B) they are not, and the proposal caps total issuance? I think it would be favorable to cap total issuance at the point where the total number of validators is sufficient for security, but only at that point. This lowers the “maximum inflation rate”, which adds additional trust to the long-term economic model of Ethereum.

I should note something in relation to my previous comment to *jgm*. When I read the words “validator cap” in the headline before reading the proposal, I felt uneasy because it sounded like the proposal may contain this type of queueing system that is undesirable due to aforementioned reasons. I was pleased when I read the proposal that it did not. It also seems the best to do this after withdrawals, as you all agree.

---

**barnabe** (2021-03-31):

To note as well that variance is important because of its centralising effects. In a system where the rotation is long (you could be asleep months before your validator comes awake), entities who control many validators have stable income/much lower variance, which assuming they reinvest the income into turning on more validators, only increases their weight over time. Same with an activation queue: insiders who are earning rewards will congest the queue much faster than outsiders looking to join in. So I like much better a system that shuffles validators quickly enough.

---

**vbuterin** (2021-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> Perhaps you could clarify, this means that there will be a hard cap to the total issuance?

Yes, and that hard cap would be the issuance level at the cap. You can compute the issuance as \frac{64 * \sqrt{deposits} * 31556925}{384 * \sqrt{10^9}}; if deposits are capped at 2^{25} ETH that comes out to \approx 963426 ETH per year issuance.

I agree with your points that this also provides more guarantees about ETH’s long-run supply, which is good. It does mean that validators potentially have lower incomes, but they get compensated by (i) lower operating expenses and (ii) the possibility that when asleep they’ll be able to exit faster.

---

**aelowsson** (2021-04-01):

Thanks. Is it feasible to set the hard cap on the number of active validators as a proportion of circulating supply instead of using a fixed power of two? Such a design aligns somewhat with the idea that the security budget should be adapted to the value of what it protects.

If the circulating supply of Ethereum was to decrease through the deflationary mechanism of EIP-1559, a downward pressure on the amount of staked Ether could be acceptable. For example, it would only take 23 years with a deflation rate of 3 % for the circulating supply of Ether to be halved. A hard cap initially set to roughly 1/3 of all Ether would at that point represent 2/3 of the circulating supply, which may be unnecessarily high. I use “may” here, because if the total value of tokens secured by Ether was to rise significantly in relation to the market cap of Ethereum, it could still be desirable from a security perspective with a rising proportion of it being used for staking (this gets complex).

If the circulating supply of Ethereum was to increase, it could only do that at a maximum of 1 %, and likely much lower. This means that the hardware requirements could only increase very slowly. There is of course in this case also the possibility to still hard cap the number of active validators but compensate proportionally with higher rewards until 1 % inflation is reached; (A) in my previous comment. This however breaks property 3 of the proposal.

---

**vbuterin** (2021-04-01):

> A hard cap initially set to roughly 1/3 of all Ether would at that point represent 2/3 of the circulating supply, which may be unnecessarily high

I don’t think this is much of a concern; remember that even in this proposal, it’s theoretically possible for all the ETH to be *locked up*, it’s just that the number of validators *awake* is bounded to ~1M. So from a macroeconomic point of view this proposal doesn’t really give us any properties that were not there before.

---

**aelowsson** (2021-04-01):

After thinking about it a little more, I agree that the active validator cap can and should be hardcoded. The reason is that *the number of validators* specifies a sufficient level of decentralization, which does not directly depend on the circulating supply (though perhaps log-linearly depend on the size of the user base). Rather, it is the *required number of Ether for each validator* that in the future could be changed in adaptation to the circulating supply.

**Just to briefly encapsulate this tangent point:**

To my understanding, as the current protocol is written, the circulating supply of Ether will eventually reach an equilibrium, at which point total staking rewards are equal to burned Ether. This equilibrium is likely to be at a significantly lower supply than the current supply (at that point, staking rewards, as a proportion of the total circulating supply, would be higher than what they are today). Some parameters are tuned based on the current circulating supply and will not automatically be adapted to such a lower circulating supply. One such parameter is the required number of Ether per validator.

---

**alonmuroch** (2021-05-13):

[@vbuterin](/u/vbuterin) where does 2^19 comes from? is there a particular target “resource” package (memory, CPU, I/O, networking) we would like to adhere to?

---

**vbuterin** (2021-05-13):

I guess `2**19` is just roughly the level of validating ETH that we expect; the goal is to make the maximum load close to the expected load.

I don’t think there’s necessarily a specific “target” where we’re okay going up to the target but not beyond it; it’s more like, the lower the resource requirements, the better, and if you push the requirements even lower, there’s even further benefits that you unlock, but what we *do* know is that fixed load is better on users than variable load, because in the variable-load case users would have to buy hardware to cover an extreme case that in practice may not end up ever being reached.

---

**alonmuroch** (2021-05-16):

[@vbuterin](/u/vbuterin) thanks for the explanation.

---

**hooji** (2022-01-23):

I think it’s important to pay special attention to the implied social contract between the Ethereum community, and stakers.

I’m concerned many stakers may be thinking of the rewards formulas as ‘set in stone’, and be basing their investment decisions on that idea.  I don’t recall the original rewards documentation providing warning to stakers about possible future changes to the rewards formula, and thus they may not be expecting it.

I want to avoid a situation where people feel treated unfairly, and thus decide to exit their staking position based on emotional rather than economic factors.

The analogy would be a computer game where a player put in considerable time and resources to optimize a specific aspect of their character, only to find things suddenly changed one day ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=10)

I think it would be good to have more proactive communication and engagement with the staking community at large, with ample notice and discussion before any changes are made.

---

**ivelin** (2023-04-18):

Thank you for making this point about engaging community well in advance of such changes.

I just heard Justin Drake talk about this in an interview post Shapella launch. That triggered a discussion in the Rocketpool community, which led to this comment.

Currently there are around 500,000 validators, but only about 2,000 RP node operators.

If there is a cap on validators set at 2^19 = 524,288, then we are already at this limit and unfortunately the validator seats are predominantly owned by large staking farms. This seems to be in a stark contrast with ETH’s mission to decentralize at the social layer (layer 0).

Yes, there is the correlation penalty, but it does not seem like the broader community is aware of it and unless there are actual disastrous events that hurt delegating stakers, this penalty itself is not enough to incentivize solo staking.

IMHO before setting any limits on number of validators, there has to be a lot stronger incentive for solo staking. Something along the lines of proof of unique location or ZK KYC.

On a broader scope, for a time there was a public campaign to improve objective decentralization metrics such as Nakamoto coefficient, Gini Coefficient and Total Network Resilience. Is anyone still tracking these for ETH?

---

**adam-hurwitz** (2024-05-02):

[@vbuterin](/u/vbuterin), Do you have an estimate on whether the `maxEB` upgrade (EIP-7251) to increase the amount of ETH each validator can stake will reduce the need for a future hard limit on the amount of total ETH that can be staked similar to the concept you originally brainstormed above?

---

**emmanuel-awosika** (2024-05-04):

That depends on how much consolidation people opt for. At full consolidation (2048 ETH), we can shrink the 1M validator set to ~15,625 validators. This assumes every validator is staking exactly 32 ETH, so 32 * 1,000,000 = 32,000,000 ETH / 2048 ETH = 15,625 validators.

[@vbuterin](/u/vbuterin) has mentioned the possibility of a higher 4096 ETH limit for the maximum effective balance [elsewhere](https://ethresear.ch/t/sticking-to-8192-signatures-per-slot-post-ssf-how-and-why/17989), so that number could well reduce. The question is whether people will opt to fully consolidate, consolidate smaller amounts (e.g., consolidating four 32 ETH validators to create a 128 ETH  validator), or consolidate at all.

But if we have enough consolidation, the need for an active validator cap reduces. AFAICT EIP-7251 was proposed to validator set capping + rotation and reducing stake rewards to disincentivize staking (both of which are controversial and have edge-cases). I [published an analysis of EIP-7251](https://ethereum2077.substack.com/p/eip-7251-increase-max-effective-balance) if you’re interested in reading through!


*(2 more replies not shown)*
