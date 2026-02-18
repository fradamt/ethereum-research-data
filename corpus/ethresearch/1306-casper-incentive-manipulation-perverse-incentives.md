---
source: ethresearch
topic_id: 1306
title: Casper incentive manipulation / perverse incentives
author: cspannos
date: "2018-03-05"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/casper-incentive-manipulation-perverse-incentives/1306
views: 5216
likes: 5
posts_count: 15
---

# Casper incentive manipulation / perverse incentives

Hi all,

I’m doing some cryptoeconomic research on Casper’s incentive structures, specifically exploring how bad actors could manipulate them or where there may be perverse incentives, as well as any consequences/corrections.

I’m hoping to verify a few details that I’ve not been able to confirm in the public documentation; details I may have overlooked.

These are:

- does Casper have a cap on the number of individual validators/deposits required? Not a target for Total Deposits as percentage of market cap, but in the sense that Tendermint has its top 100 validator candidates who have the most stake. I’ve read Casper requires 250, but can’t confirm.
- does Casper have a minimum required deposit to become a validator? For example, 50 ETH, 1500 ETH, etc.
- I’ve seen research suggesting, if I understand correctly, that interest on deposits will fluctuate up or down according to proximity to a desired Total Deposit target. Is this confirmed/accurate or are there other strategies?
- is there a set withdraw limit on the deposit, ie held for four months minimum?
- do I understand correctly that interest, and rewards/penalties generally, are dispensed per epoch?
- do answers to the above apply to both Casper FFG and CbC?

I have more questions, but for now, any answers/links to the above would be greatly appreciated.

Thanks so much!

Chris

## Replies

**vbuterin** (2018-03-06):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/c/ebca7d/48.png) cspannos:

> does Casper have a cap on the number of individual validators/deposits required?

No.

> does Casper have a minimum required deposit to become a validator? For example, 50 ETH, 1500 ETH, etc.

1500 ETH currently.

> I’ve seen research suggesting, if I understand correctly, that interest on deposits will fluctuate up or down according to proximity to a desired Total Deposit target. Is this confirmed/accurate or are there other strategies?

No, though we *have* explored the possibility of mechanisms where the minimum deposit goes up as the number of active validators goes up.

> is there a set withdraw limit on the deposit, ie held for four months minimum?

The entire deposit is held for 4 months before it can be withdrawn.

> do I understand correctly that interest, and rewards/penalties generally, are dispensed per epoch?

Yes.

> do answers to the above apply to both Casper FFG and CbC?

Not sure; ask [@vlad](/u/vlad) about CBC.

---

**cspannos** (2018-03-06):

That clarifies a lot and is very helpful.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> though we have explored the possibility of mechanisms where the minimum deposit goes up as the number of active validators goes up.

What would be the reasoning for that?

On the topic of interest on deposits, assuming there is, what is the interest rate set at? Is it fixed then?

Thanks!

---

**vbuterin** (2018-03-06):

> What would be the reasoning for that?

To reduce the uncertainty in the total number of validators (which directly translates into overhead).

> On the topic of interest on deposits, assuming there is, what is the interest rate set at? Is it fixed then?

Right now it’s still the inverse square root of the total amount of ETH deposited.

---

**cspannos** (2018-03-06):

Okay, I understand now. Thank you!

---

**nootropicat** (2018-03-06):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/c/ebca7d/48.png) cspannos:

> specifically exploring how bad actors could manipulate them or where there may be perverse incentives

See



    ![](https://ethresear.ch/user_avatar/ethresear.ch/nootropicat/48/258_2.png)
    [Cartel formation incentive in full PoS - interest rates must rise with the total deposit size](https://ethresear.ch/t/cartel-formation-incentive-in-full-pos-interest-rates-must-rise-with-the-total-deposit-size/973) [Proof-of-Stake](/c/proof-of-stake/5)



> In the Casper testnet interest rate is proportional to inverse square root of total deposits. That would be very bad for full PoS.
> Changes in validator sets are transactions.
> Bob is a selfish profit-optimizing validator. If Bob’s expected future return on staked eth is expected to drop due to new validators joining he’s not going to include their join transactions. Fee loss is infinitesimal under any significant adoption scenario, as he only loses the difference to the next highest gas priced …

---

**cspannos** (2018-03-06):

Thanks for bringing your work on this to my attention nootropicat. This is exactly the kind of problem I am interested in.

Cheers,

Chris

---

**gititGoro** (2018-03-08):

With a minimum deposit of 1500eth, it seems inevitable that validator pools will be set up. After all, what’s to stop me from issuing 1500 000  tokens at 0.001 eth each and staking the pool, paying out token holders in proportion to their holding?

---

**MicahZoltu** (2018-03-08):

Trust.  With mining pools your opportunity cost is the hashing power between payouts.  With validator pools, the opportunity cost is the maximum amount of your money the pool could lose between payouts.  I don’t actually know what the maximum loss rate of a malicious/lossy validator is each week (reasonable payout period), but if that is higher than “the cost of electricity and hardware wear for a week” that miners take on then it means the risks are higher than mining.

---

**vbuterin** (2018-03-10):

Nothing wrong with validator pools; they are inevitable, and I do think that the centralization risks can be contained with mitigations like the partial slashing incentive to join smaller pools over larger ones.

---

**ihlec** (2018-03-13):

How could an ideal validator pool contract look like?

Scenario 1:

A validator runs a full node and provides proof that he holds half of the required stake himself and collects only the missing ETH over a pooling contract.

This seems like a feasible variant for a pooling contract but is not fully decentralized.

Scenario 2:

Each staker of the pool runs a validator node and archives consensus with the others for the validation result.

Voting is weighted using the amount of stake a validator has.

This would be the most complex, but also most decentralised approach. Of course it would compromise performance a bit.

Is this flawed?

---

**cspannos** (2018-03-13):

Could a DAO be set up to act as pool manager where coins are sent to a contract and some proportion of users need to sign prepare and commit messages for deposits/withdrawals? Among other threshold parameters, the DAO would have to maintain the minimum staking level, say 1500 ETH, or – if failing to uphold the minimum – dissolve after distributing dividends according to each user’s stake.

---

**tim** (2018-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> inverse square root

What is the frequency of distribution? 365 days?

i.e. I stake 1 Ether. Leave it in for 365 days and then withdraw it.

So 365 days + 4 months would mean I have a balance of:

1 ether + 1/sqrt(1 ether) = 1 + 1 = 2 ether?

Will the staking support double/float staking or does it have to be an integer ether amount?

Thanks!![:grin:](https://ethresear.ch/images/emoji/facebook_messenger/grin.png?v=12)

---

**vbuterin** (2018-03-29):

A likely formula is that it will be targeted to give stakers a 5% annual return if there is 10 million ETH staking. So if there is 2.5 million ETH staking, and you stake 10000 ETH, and you perform optimally as a validator, then you would have 11000 ETH in a year.

Fractional quantities of ETH are okay.

---

**Lars** (2018-04-14):

If a DAO is used for a validator pool, it can issue a coin/token to members. Payouts would go to the holders of these coins. Instead of having to dissolve the stake when someone wants to leave, it would be possible to sell your coins.

