---
source: ethresearch
topic_id: 5963
title: Where will reward money on Beacon chain come from?
author: kladkogex
date: "2019-08-13"
category: Economics
tags: []
url: https://ethresear.ch/t/where-will-reward-money-on-beacon-chain-come-from/5963
views: 7034
likes: 5
posts_count: 28
---

# Where will reward money on Beacon chain come from?

I was trying to figure out where the ETH rewarded to validators on the ETH 2.0 will come from. Can someone explain this to me?

Will their be additional ETH printing on the main net specifically for ETH 2.0 rewards?

## Replies

**adlerjohn** (2019-08-13):

It’s a new coin, colloquially called “BETH” (beacon chain ether). The beacon chain is a side chain with a one-way bridge, so it can do whatever it wants, including having its own native coin. Funds are never bridged back to the PoW chain.

---

**payvint** (2019-08-13):

1. But people will presumably be able to convert 1 ETH to 1 BETH by one-way bridge - correct?
2. And this 1 ETH will presumably be burnt in the process of transfer - correct ?
3. And then, if I deposit 32 ETH but I get paid in BETH, how do I calculate ROI?  How is it determined how much BETH I get for my ETH  ?

---

**adlerjohn** (2019-08-13):

1. Yes.
2. Yes.
3. Transfers are disabled in phase 0, so you’d have a pretty hard time selling your rewards without simply giving all your coins to a centralized exchange unfront. As such your ROI in terms of fiat is zero—for now. Your rewards (denominated in BETH) are described here.

---

**kladkogex** (2019-08-14):

John - I am still a bit lost on what the table means.  The table says 18% return - but the return is in BETH and the deposit in ETH.  What does 18% return mean.  If I deposit 32 ETH do I get 5.76 BETH?

---

**adlerjohn** (2019-08-14):

It has nothing to do with the one-way bridge of ETH -> BETH, which is always 1:1.

The table is annual return of being a validator. In the scenario of 1M BETH actively being staked, each active validator would get ~18% of their stake as rewards per year.

---

**kladkogex** (2019-08-14):

I am a bit lost … I thought what was staked was ETH. Is staking done on main net or on beacon net? If staking is done on beacon net, you kind of effectively staking ETH anyway, since you are converting 32 ETH into 32 BETH ? Correct?

---

**jgm** (2019-08-14):

ETH is sent to a smart contract on the Ethereum 1 mainnet.  This ETH is locked away in the smart contract and doesn’t come out again.

Separately, the Ethereum 2 nodes are listening to events from the Ethereum 1 smart contract mentioned above.  When it sees that someone has made a deposit it creates Ethereum 2 ETH (called BETH above) and expects the validator mentioned in the deposit contract to start validating the Ethereum 2 beacon chain.

As long as the validator does a good job validating the Ethereum 2 beacon chain the amount of BETH held for the validator increases (as the validator is given rewards for its work).  At some stage the validator can decide they don’t want to validate any more, at which point they receive whatever BETH they staked plus the rewards.

(note that there are various delays and complications in place in reality, omitted for brevity).

It is worth noting that although you can swap 1 ETH for 1 BETH through the deposit contract this does not lock in the value of BETH because you cannot swap BETH to ETH.  They may remain close to each other or may diverge, but there is no peg because the transfer is one-way.

---

**kladkogex** (2019-08-14):

It looks like the first validators will need to assume huge risk.

32 ETH is $6000.

Why would I want to take $6000 dollars and burn them in exchange for something with unclear value?

---

**MaverickChow** (2019-08-16):

Regarding the 1:1 peg, at first I thought it may likely diverge if the beacon chain has its own issuance rate independent of the main chain. But if this becomes so, then I suspect the likelier outcome will be 1 ETH : more than 1 BETH, thus allowing ETH holders to indirectly gain from validating reward without the need to be validators. To prevent this “exploit”, further thoughts lead me to believe the peg will be made not to diverge, in other words, it will permanently be strictly 1:1.

---

**kladkogex** (2019-08-16):

Well … how do you think 1:1 peg will be enforced ? I am not sure I see any mechanism for this.

The beacon chain will not be usable much until the shards will run, which will presumably happen many years after. So you have a token, BETH not really usable much and not convertable back to ETH.

Then arguably you will have a strong discount of BETH vs ETH, unless there is an altruistic party that purposefully converts ETH to BETH.

So what is probably going to happen at the start is that ETH foundation and other parties connected to it will altruistically

---

**MaverickChow** (2019-08-17):

Enforced by the smart contract for a strict peg. Since this will be a one way street, it should not be hard to get done. If the model will eventually be fully Proof of Stake, then the total supply of the Beacon chain will take precedence over the total supply of the main chain.

Any situation where there is a discount or premium in the peg would allow exploits to be possible. So only a strict 1:1 peg hard coded into the system can prevent any potential opportunity of exploit.

Because the Beacon chain will have better scaling, thus its money velocity will be much higher, thus this will result in much higher issuance of BETH. There may be a situation where the total supply of main chain may be 140 mil (example) while the total supply of beacon chain may be at 170 mil (example).

If the peg will be such that 1 ETH get more than 1 BETH, then there is no need to join the beacon chain so early to be validators along with the potential risk of things may go wrong and you lose everything. And smart people may not participate early until things are proven flawless. If the peg will be such that 1 ETH get less than 1 BETH, then it makes no difference because a loss of ownership by having less than 1 BETH per 1 ETH is balanced out by the deflation from the beacon chain.

The most ideal situation is to maintain a strict 1:1 peg, by hook or by crook.

But of course this is just my speculation on how things can be done most effectively.

---

**jgm** (2019-08-17):

ETH1 and ETH2 are for all intents and purposes separate currencies, you just happen to be able to purchase 1 ETH2 for 1 ETH1 (although even then it isn’t that simple because your purchased ETH2 is going to be locked in to a staking contract for a while so you need access to a validator if you don’t want to lose a chunk of it, time value of money, utility of ETH2 in the next year or two, *etc.*).

Under the current proposals ETH2 will be less inflationary than ETH1.  For example, if 50 million ETH2 are staked then ETH2 issuance will be around 1.1million per year.  This is far less than the ~7 million ETH1 per year at current issuance rates.  However, because the deposit contract ETH1 can be swapped for ETH2 at a flat rate you would expect a continual flow of ETH1 to ETH2 to keep the inflation rates roughly balanced (and hence ETH1 and ETH2 would keep close to 1:1 in value).

If the ultimate goal is to move ETH1 to ETH2 it makes sense for there to be two actions.  First, an ongoing reduction in ETH1 issuance, most likely based on the amount of ETH1 outstanding *i.e.* as the amount of non-staked ETH1 decreases the issuance decreases likewise.  Second, a reduction in the value of ETH1 compared to ETH2 over time *i.e.* the deposit contract should decrease the amount of ETH2 issued per ETH1.  Both of these would result in ongoing pressure to move ETH1 to ETH2.

Alternatively, the ETH1 issuance could just be reduced to be below ETH2 issuance at a selected expectation of ETH2 staked.  However that would result in the per-block issuance of ETH1 going down to something around ~0.4ETH1 and would be a bit of a system shock.  But attempting to keep a 1:1 peg over time when the two systems have different issuance models would prove difficult.

---

**kladkogex** (2019-08-19):

Vow - this is big news to me.  This is very helpful, thank you! I always though that ETH 2.0 was supposed to do  the two-way  peg at some point.

To be a bit of devils advocate why isnt ETH2 = 0.1 ETH1 a scenario? I understand that ETH 2.0 is less inflationary,  but ETH 1 may still raise in value faster than ETH 2.

---

**fubuloubu** (2019-08-19):

This is a big design goal that the working group on the finality gadget is figuring out. The main concept is that the two assets will be equivalent and thus hopefully considered by the market as the same asset; however, as you point out there is a bit of an economic dissonance going on with the current structure.

My main goal would be to ensure all of the value created on ETH 2.0 (through validator rewards) gets accounted for on the current chain, so this dissonance is as minimal as possible.

As a point against any conversion price other than 1 ETH = 1 bETH, it would be difficult to justify considering much of the crowd sale and future value prop of the Ether token has the idea that ETH 2.0 would ship baked into it. The market may reject anything else as unfair. The first validators take the highest risk, but likely would earn the most rewards upfront, as more Validators join the ROI reduces per the target issuance schedule. It remains to be seen if it is attractive enough to reach the minimum threshold required to start the beaon chain. Maybe some of the ideas in this thread can help.

Lastly, it is plausible that the sale of private keys for staked Validators may occur, especially if it is a long time before the Ether can be unstaked. It may be prudent to allow at least a transfer of the validator slot to a new key pair, which I don’t think can occur currently. Interesting thought however. (cc [@djrtwo](/u/djrtwo))

---

Finality Gadget WG:

https://ethereum-magicians.org/t/finality-gadget-for-ethereum1x-working-group/3177

---

**jgm** (2019-08-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> As a point against any conversion price other than 1 ETH = 1 bETH, it would be difficult to justify considering much of the crowd sale and future value prop of the Ether token has the idea that ETH 2.0 would ship baked into it.

I struggle to see how this is sustainable, given the different issuance models of the two chains.  It makes sense to say that ETH1:ETH2 *starts* at 1:1 but will diverge over time; artificially tying the two together, given the mechanics of the validator process and the one-way bridge, sounds unrealistic to me.

Is there a general discussion about the impact of the economic models on the relative values of ETH1 and ETH2 over time going on somewhere?

---

**MaverickChow** (2019-08-21):

While ETH1 and ETH2 are separate currencies, remember ETH2 will eventually fully displace ETH1. Thus, the total supply and issuance rate of ETH2 will take precedence over ETH1’s. Whether ETH2 will eventually be inflationary or deflationary relative to ETH1 over time, that will not matter, in my opinion, even if the peg is strictly maintained at 1:1 without change throughout. It is only when the peg is not strictly maintained that exploits become possible. Maintaining the 1:1 peg is not difficult at all, in my opinion. The only time such task will be difficult is when you want to maintain an equal value between the two chains after inflation-adjusted or deflation-adjusted.

A peg is difficult to be maintained only if it is allowed to be flexibly determined by market forces. And if that will be so, then it will only create complications unnecessarily. Otherwise, even a hard-coded peg will not be a problem. **A hard-coded peg is only a problem if we continue to see Ethereum to have 2 independent chains, where the values of both chains are maintained to be equal, after inflation/deflation-adjusted relative to the two chains.** Otherwise, knowing that ETH2 will eventually fully displace ETH1 (to be 100% Proof of Stake), then a strict peg 1:1 is both easy and fine, in my opinion.

---

**MaverickChow** (2019-08-21):

1. Yes, is not sustainable only if Ethereum will have 2 separate and independent chains indefinitely.
2. Yes, the 1:1 peg will diverge over time only if it is allowed to be set by market forces. And the divergence will persist indefinitely as long as Ethereum will continue to have 2 separate and independent chains.

Just my opinion, by the way.

Will Ethereum maintain 2 separate and independent chains indefinitely?

---

**jgm** (2019-08-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> Maintaining the 1:1 peg is not difficult at all, in my opinion.

I’d love to hear more about this.  How is it possible to maintain a 1:1 peg when ETH1 and ETH2 have different issuance rates, and it is possible to move ETH1 to ETH2 but not the other way round?  What would the mechanics of such a system look like?

(I’m not particularly interested in long-term steady state, I’m trying to understand how we reach a long-term state from a system that starts with ~110MM ETH1 and ~2MM ETH2, with annual issuance of ETH1 being ~4MM and ETH2 being ~250K with a 1:1 peg)

---

**MaverickChow** (2019-08-21):

Complications arise only if we assume Ethereum will maintain 2 separate and independent chains indefinitely into the distant future. But we know that will not be the case, that ETH1 will eventually retire and be fully displaced by ETH2. So lets assume we are in charge of the smooth transitioning from ETH1 to ETH2, how best do you think we can do to ensure that? In my opinion, only a steady peg of 1:1, hard-coded and one-way, will do the job.

If we insist to keep on thinking that such peg will be based on market dynamics, i.e. not hard-coded (i.e. it can change up and down based on the whims and fancy of market forces) and not one-way (i.e. everyone will eventually be able to transfer coins between ETH1 and ETH2 in a two-way direction, despite the fact that ETH1 will be retired entirely), then of course complications and exploits will arise.

And I suspect a reason why you think this is not possible is because they issuance rate will influence either one of the coins to be more inflationary and the other one more deflationary, relative to each others, and thus it needs complex algorithm to maintain a peg in real time that would ensure the value of 1 ETH1 is always equal to the value of 1 ETH2, thus impossible. If that is the case, then I suppose you may be right.

But to explain differently, I would say ETH1 will be a subset of ETH2, thus whatever the issuance rate of each chain will make no difference. ETH2 issuance rate will definitely be higher once it gets used far more than ETH1, thus ETH2 will be inflationary relative to ETH1, not deflationary. And even at 1:1 peg, the relative inflation will still not be a problem. Problem arises only when the peg is not maintained in order to reflect the inflation in ETH2, thus holders of ETH1 will have less incentive to transition to ETH2 to stake. In order to incentivize holders from ETH1 to transition to ETH2 to stake, the peg needs to be maintained at 1:1, regardless of inflation from ETH2.

Maintaining 1:1 peg is possible with hard-coding and one-way as stated. Period. It also means taking market dynamics out of the picture. If ETH1’s total supply is 110 mm ETH, then so will be ETH2’s total supply at the very minimum. Because when all the ETH1 holders transition to ETH2, all 110 mm ETH in ETH1 will become 110 mm ETH in ETH2.

Of course all these are just my personal opinion.

Edit: Didn’t they also announced the issuance rate of ETH1 will drop by 10x? I believe ETH1’s issuance rate will be reduced to negligible amount, thus a majority of the inflation will take place in ETH2.

---

**jgm** (2019-08-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> And I suspect a reason why you think this is not possible is because they issuance rate will influence either one of the coins to be more inflationary and the other one more deflationary, relative to each others, and thus it needs complex algorithm to maintain a peg in real time that would ensure the value of 1 ETH1 is always equal to the value of 1 ETH2, thus impossible. If that is the case, then I suppose you may be right.

Well yes, two different inflation rates and an ongoing ability to swap 1 ETH1 for 1 ETH2 is the issue, as far as I see it.  I don’t see how a fixed peg would work in this situation and although you say it would work “Period” I don’t see how.  What would you expect to happen the first day the beacon chain starts validating in this scenario?

I could see a floating exchange rate work (start at 1:1.2, for example, and move to 1:0.1 over time); if the change in the rate is known in advance it would allow market forces to move ETH1 over to ETH2 at the time they are comfortable with it (a later date would involve less risk but lower reward).

Eventually the exchange rate has to go to 0 or there be some mechanism in the deposit contract (or beacon chain) to stop accepting new deposits, as otherwise we could reach a state where the ETH1 chain is basically abandoned and someone can run it in their basement generating ETH1 and depositing them for ETH2.

(There are meta-constraints here, as well: we don’t want to see 100% of ETH1 being deposited in to ETH2 early on because then there will be no way of paying gas on ETH1, for example.)


*(7 more replies not shown)*
