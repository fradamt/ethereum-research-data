---
source: ethresearch
topic_id: 6169
title: "DeFi Algorithmic Stablecoin: FRAX (feedback wanted)"
author: EazyC
date: "2019-09-19"
category: Economics
tags: []
url: https://ethresear.ch/t/defi-algorithmic-stablecoin-frax-feedback-wanted/6169
views: 5483
likes: 1
posts_count: 11
---

# DeFi Algorithmic Stablecoin: FRAX (feedback wanted)

We’ve been working on this fractional-reserve, algorithmic stablecoin called Frax. The basic premise is that we layer this over a collateralized stablecoin such as Dai and use interest from compound.finance loans to stabilize the price to $1 to 1 Frax algorithmically changing the supply of Frax.

There is a 2 token system: Frax, FRX (the stablecoin) and Frax shares, FXS (the investment token)

The system starts 1:1 backed (reserve ratio of 100). For every 100 Dai you put in, you mint 100 FRX. The Dai is then lent out (either through the compound finance smart contract itself or the exact implementation within the Frax contract). The cash flow from the interest rate earned through the loan is accrued into the smart contract. Once there is a sufficient amount of interest earned, the reserve ratio goes down by X. If X=1 then for every 99 Dai you put in, you mint 100 Frax. The difference in the reserve ratio (aka X) must be paid in FXS as a fee (which is burned out of circulation) so that value isn’t leaving the system but instead captured by the investment token. The investment token, FXS, is essentially valued as the net future fiat value creation of the network in perpetuity.

If the market price of FRX holds at $1 1 FRX then the reserve ratio continues to go more and more fractional by increasing X as more interest cash flow comes in. If the FRX price drops because the market only values FRX based off the backing collateral, then the accrued cash flow is used to buy back FRX and “walk back” the reserve ratio to the market’s value of 1 FRX $1. At all times, there is a small amount of Dai that is always kept in the contract to exchange out for FRX for easy redemption.

Essentially, this is a system to algorithmically measure the market’s value of the “monetary premium” of a currency. This can be used to scale Dai and allow DeFi loans to provide monetary policy/stability.

[![52%20PM](https://ethresear.ch/uploads/default/original/2X/9/92ab4899f79b6dc99e0ba5e7b7496b41fc917b3a.png)52%20PM432×414 15.5 KB](https://ethresear.ch/uploads/default/92ab4899f79b6dc99e0ba5e7b7496b41fc917b3a)

Once there is sufficient monetary premium built into FRX, you can even remove the backing of Dai and make it entirely a fiat stablecoin and simply mint new FRX.

Any ideas/feedback on this system?

## Replies

**DB** (2019-09-21):

The assumption (shared by many projects now) that the current state where one gets a very nice return (~10%APR) on a very secure asset (DAI), may not be valid for very long. Interest may go to nearly zero, same for FRX/S.

Also, not sure what will stop it from collapsing if you remove the DAI.

---

**MaverickChow** (2019-09-30):

Since there is a need to charge interest rate to acquire the FRAX stablecoin, I would like to know is this stablecoin really a stable coin, or in actual fact just a lending coin? The same goes to DAI.

In my personal opinion, no stablecoin can last forever without also being a lending coin, simply because there is counterparty risk. The Federal Reserve does not lend out freshly minted USDs even close to the rate that DAI borrowers are being charged, so it is not appropriate to associate such stablecoin(s) to be just like the Federal Reserve.

---

**EazyC** (2019-09-30):

This is not extremely relevant because even in efficient lending/DeFi markets, there will always be SOME interest rate above 0% for borrowing so there is still positive cash flow in the system. This system doesn’t rely on the exorbitant interest rates in the current markets.

---

**EazyC** (2019-09-30):

I think you might have misunderstood the protocol or it was poorly explained in my post. The idea is you mint FRX stablecoins by placing collateral into the reserve and paying the reserve ratio difference in FXS. There is no interest charged for holding FRX. Once you mint it, it’s yours. The collateral in the reserve is what gets lent out to borrowers and accrues interest into the smart contract for buying back FRX when necessary to stabilize the price.

EDIT: I think I get what you’re saying. You’re saying that if you have to use Dai as collateral and Dai requires paying interest to keep the CDP open or the Dai disappears, then FRX itself is essentially just a wrapper over Dai and not quite a standalone stablecoin. If that’s what you’re saying, fair point. Perhaps we can start the system with Tether (although there’s different risks there).

---

**PatrickDehkordi** (2019-10-01):

As the ratio of DAI to FRX goes down, so does the ratio of your interest bearing collateral, and this decreases the accrued cash flow to buy back FRX to keep it at a dollar if needed. I think it is going to be very difficult to pull off. I don’t see a problem initially with high reserve ratios. But not sure you can keep the value stable, down the line if there is an attack on the currency, or a “run on the bank”. But this is not unique to FRX, this is a problem with any type of “Fiat Value”.  Also, and this maybe just due to my ignorance, when you go from 100 DAI to 99 DAI, you are capturing that value in FXS.  Does FXS liquidate in emergencies to support FRX? If not I would say that value is leaving the stable coin part of the system, no?

---

**EazyC** (2019-10-01):

> As the ratio of DAI to FRX goes down, so does the ratio of your interest bearing collateral, and this decreases the accrued cash flow to buy back FRX to keep it at a dollar if needed.

You’re right about that but the interest cash flow is a function of time and collateral, so even though there is less collateral in proportion to FRX as the fractionality increases, the cash flow continues to come in. The protocol does not go more fractional until there is enough cash flow in the contract to buy back FRX to “walk back” the fractionality to the previous level in case the price falls. So I don’t think it’s mathematically an issue.

> Also, and this maybe just due to my ignorance, when you go from 100 DAI to 99 DAI, you are capturing that value in FXS. Does FXS liquidate in emergencies to support FRX? If not I would say that value is leaving the stable coin part of the system, no?

Ya so this is an astute point. I should make it clear that FXS can be printed and auctioned for FRX as a “lender of last resort” similar to MKR as a final method of stability if necessary, but only in a situation where there’s a black swan event. I don’t think it’s likely because as explained above: the system only goes more fractional if there is enough cash flow to stabilize at that level.

---

**PatrickDehkordi** (2019-10-03):

I don’t see anything blatantly off then. There is already a token that is suppose to provide the cash flow, called cDAI (compound DAI) Maybe you can start with cDAI as a collateral in place of DAI. My only other suggestion is that the easiest path to a stable currency is to let the central bank do the heavy lifting,  by keeping a non-crypto asset off chain. This is what  tether and USDC did. The difficult way is to over-collateralize on chain like Maker, and what you are proposing is at least in my opinion more difficult than both those methods.  But you have the right idea. The trick is to do it very slowly. It took the Bank of England 300 years to go full fiat ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)  Wish you the best!

---

**EazyC** (2019-10-05):

We’ve thought about using cDai as collateral but that would constrain us to using only compound.finance as our lending market for the collateral in the frax reserve. I think it’s better to actually have the Dai/Tether in the Frax reserve and then have the contract place it in compound (or in the future other money markets as the contract is updated to support new DeFi products).

As for your comment that what we are proposing is more difficult to pull off than Maker..in a certain sense I understand what you’re saying, but in a different sense, I think you are wrong because it’s more difficult for Maker’s system to scale to a global currency. A global, stable currency has some fiat properties (which Maker lacks). In that sense, I believe something like Frax (or similar algorithmic protocols) are the only viable products to expand the stablecoin ecosystem ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**kenny-white** (2019-10-16):

Maybe I’m missing something, but why would someone want to hold FRX instead of cDai? If the interest for FRX is derived from lending Dai collateral on Compound, then what is keeping me from lending on Compound directly? Apologies if this is an obvious question with an equally obvious answer…

---

**EazyC** (2019-10-17):

This is a good question that I think should have been directly answered in the OP, sorry for not being clear. The central aim of the Frax protocol is to use the interest earned on defi money markets as an algorithmic layer of stability, essentially another layer of monetary policy over Dai/Tether (whatever is used as collateral). cDai earns you (the holder of cDai) interest for your Dai on loan. It is an interest bearing token for you. When you deposit Dai to mint FRX, you are creating a new stablecoin (FRX) that is backed by both Dai and the interest of the Dai (the interest for loaning the Dai is used to contract the supply of FRX should FRX price fall). Essentially, users of FRX are pooling their interest in Dai to create extra stability/another layer of monetary policy over Dai/the stablecoin collateral. Does that make more sense? Once the system is more robust, it would go more and more fractional where 1 FRX can be created with less than 1 Dai but it will be 1:1 at the beginning. Does that make it more clear? What are your thoughts

