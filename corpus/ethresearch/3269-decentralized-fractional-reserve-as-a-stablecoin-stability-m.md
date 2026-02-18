---
source: ethresearch
topic_id: 3269
title: Decentralized Fractional Reserve as a Stablecoin Stability Mechanism
author: SRALee
date: "2018-09-08"
category: Economics
tags: []
url: https://ethresear.ch/t/decentralized-fractional-reserve-as-a-stablecoin-stability-mechanism/3269
views: 1276
likes: 1
posts_count: 6
---

# Decentralized Fractional Reserve as a Stablecoin Stability Mechanism

There is a stablecoin STBL. The stablecoin smart contract accepts deposits in a particular asset (let’s say ETH). Any address is permitted to deposit assets into the contract (similar to a bank). Assets must be deposited for some period P (where P could in theory be 0 which means assets can be withdrawn back the next block). The contract then calculates some interest rate R annually/per block that each account is entitled to from their deposited assets when they call the `collect_interest` function. The interest is paid out in STBL by minting new STBL from the contract. R can be dynamically adjusted by the contract to attract more deposits given certain conditions.

There is a constant variable, `reserve_ratio`, which describes the amount of the deposited assets that can be used by the contract. For example, if the `reserve_ratio` is .4 then 40% of deposited assets can be used at any current time. Put in another way, for every 1 ETH deposited, .4 ETH can be used at a reserve_ratio of .40. The used assets are put into a DEX for trading pairs ASSET:STBL and STBL:ASSET auctions at the pegged price and used as market makers to keep the price from fluctuating outside the thin band of stability. In our example, the pairs would be ETH:STBL and STBL:ETH.

Finally, all assets are “insured” by the contract in STBL during bank runs. For example, let’s say that 30% of the assets have currently been used in the DEX but 80% of assets are being requested for withdrawal. There is a deficit of 10% which the contract does not have. The value of the 10% of ETH is returned to depositers in STBL instead of the ETH itself.

This system is interesting because it can be used as a “drop-in” stability mechanism in most stablecoin designs without directly interfering with other mechanisms. It is a standalone mechanism that does not impede or competitively counteract any seigniorage shares, MakerDAO, or [Basis.io](http://Basis.io) type system. The one clear weak point here is obviously bank runs, but the insurance policy is a good workaround. I am interested in thoughts or if there are better work arounds to mitigate bank runs.

## Replies

**savant.specter** (2018-09-08):

The setup isn’t quite clear, but if I understand correctly, there are a few issues.

> The contract then calculates some interest rate R annually/per block that each account is entitled to from their deposited assets when they call the collect_interest function.

Where does the money come from to pay interest? Sounds like you are also suggesting the deposits are needed to defend the stablecoin, and so they can’t even be used for something else.

More importantly, these is an issue here

> The value of the 10% of ETH is returned to depositers in STBL instead of the ETH itself.

When users want to withdraw funds they will be effectively selling STBL. The system can’t “return 10% in STBL” - the user is specifically trying to get rid of STBL. Any system created around this logic will be issuing coins (STBL) to pay off debts. This works in a sense (it’s what the US government does), but it causes inflation and kind of defeats the purpose of a stablecoin.

---

**SRALee** (2018-09-08):

> Where does the money come from to pay interest? Sounds like you are also suggesting the deposits are needed to defend the stablecoin, and so they can’t even be used for something else.

Sorry this wasn’t clear. It is printed/minted by the contract since it’s the stablecoin contract itself, it has that power (edited now to make it more clear). The deposits in this scheme are indeed used to market make the stablecoin.

> When users want to withdraw funds they will be effectively selling STBL. The system can’t “return 10% in STBL” - the user is specifically trying to get rid of STBL. Any system created around this logic will be issuing coins (STBL) to pay off debts. This works in a sense (it’s what the US government does), but it causes inflation and kind of defeats the purpose of a stablecoin.

I’m not sure if I get exactly what you mean by “the system can’t return 10% in STBL.” The system can definitely print the 10% STBL, but are you saying that since there’s no more deposits to market make the price, it effectively is worthless stablecoins? Because if that’s what you mean, you’re right. And yes, the idea is actually exactly like the US gov, it is indeed paying off debts.

Keep in mind that the interest rate R can be increased dynamically so that more people are enticed to deposit assets in the case that there are not enough deposits to keep the STBL price from falling. Can you expand on your 2nd criticism though on"the user is specifically trying to get rid of STBL."

---

**savant.specter** (2018-09-09):

> It is printed/minted by the contract since it’s the stablecoin contract itself

If there are no new deposits into the contract and no services rendered, then the system is paying for the “interest” through inflation. It’s a zero sum game.

> The deposits in this scheme are indeed used to market make the stablecoin.

I’m not sure it’s really “market making.” The hypothetical contract is using deposits to defend the peg. This is, if nothing else, a very capital intensive process - it’s not a revenue business.  This is an important point because normally a commercial bank uses deposits to lend out money. Through lending, the commercial bank has new revenue to pay interest to savings accounts. The difference in lending rates is the commercial bank’s profit.

Unless I’ve misunderstood your proposed system, I don’t think you can just change “R” to be whatever is most convenient for maintaining the peg - it has to be funded by something.

---

**SRALee** (2018-09-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/savant.specter/48/2057_2.png) savant.specter:

> Through lending, the commercial bank has new revenue to pay interest to savings accounts. The difference in lending rates is the commercial bank’s profit.
>
>
> Unless I’ve misunderstood your proposed system, I don’t think you can just change “R” to be whatever is most convenient for maintaining the peg - it has to be funded by something.

If I understand you correctly, you like the mechanism but just don’t think it is properly configured if the interest rate payment is coming out of “thin air” by printing STBL tokens. What if I modify the mechanism a bit where there is a reserve which holds STBL tokens earned through transaction fees and other types of network revenue generating events. This reserve of STBL tokens is where the interest in STBL is paid out in. Then the interest rate R is dynamically adjusted up and down based on how much STBL is in the reserve. Additionally, one could use other types of stability mechanisms to fund the reserve such as [basis.io](http://basis.io) type bonds and expansions in STBL so that there is excess STBL to pay interest and accrue deposited assets. What do you think of this change?

---

**arne9131** (2018-09-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/sralee/48/1134_2.png) SRALee:

> There is a constant variable, reserve_ratio , which describes the amount of the deposited assets that can be used by the contract. For example, if the reserve_ratio is .4 then 40% of deposited assets can be used at any current time. Put in another way, for every 1 ETH deposited, .4 ETH can be used at a reserve_ratio of .40. The used assets are put into a DEX for trading pairs ASSET:STBL and STBL:ASSET auctions at the pegged price and used as market makers to keep the price from fluctuating outside the thin band of stability. In our example, the pairs would be ETH:STBL and STBL:ETH.

I agree with your direction of thought. To reframe the concept, every stable coin can be redeemed for one dollar worth of Ether. Assuming there is a market for Ether, a stable coin can sustain its stability. The issue that you might face is when Ether falls drastically, and then stable coin users will be unable to redeem all amount. To counter such issue, you can have a system which pegs every stable coin with one dollar worth of Ethereum network gas time. The addresses that can deposit to such a stable coin smart contract are Ethereum miners.

Such a mechanism would tackle your bank run problem as well ( when deposit makers remove their deposits ). Assuming there exist at least one miner, each stable coin can always be redeemed back for Ethereum network gas time.

![](https://ethresear.ch/user_avatar/ethresear.ch/sralee/48/1134_2.png) SRALee:

> If I understand you correctly, you like the mechanism but just don’t think it is properly configured if the interest rate payment is coming out of “thin air” by printing STBL tokens. What if I modify the mechanism a bit where there is a reserve which holds STBL tokens earned through transaction fees and other types of network revenue generating events. This reserve of STBL tokens is where the interest in STBL is paid out in. Then the interest rate R is dynamically adjusted up and down based on how much STBL is in the reserve. Additionally, one could use other types of stability mechanisms to fund the reserve such as basis.io type bonds and expansions in STBL so that there is excess STBL to pay interest and accrue deposited assets. What do you think of this change?

Transaction fee sinks and taxation would allow the stable coin supply to be contracted, but wouldn’t be sufficient since most of the transaction happen on exchanges and are never posted on block chain. Basis bond mechanism may work, but as a foundation, you will still be closely relying on the volatile price of Ether to back the outstanding stable coins.

