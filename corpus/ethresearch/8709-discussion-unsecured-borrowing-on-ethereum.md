---
source: ethresearch
topic_id: 8709
title: Discussion - Unsecured borrowing on Ethereum
author: tpmccallum
date: "2021-02-19"
category: Applications
tags: []
url: https://ethresear.ch/t/discussion-unsecured-borrowing-on-ethereum/8709
views: 2183
likes: 4
posts_count: 9
---

# Discussion - Unsecured borrowing on Ethereum

Hi,

I want to start a discussion about building a viable Ethereum-based unsecured borrowing application, which does not require collateral (hence the term unsecured borrowing).

We already know the importance of borrowing in terms of improving infrastructure and therefore quality of life and so forth. For example, borrowing underpinned sovereign finances in early-modern Europe.

Interestingly, primary sources attribute the financial stability (during this early-modern period in Europe) to borrowers being able to predictably repay their debt (van Bochove, 2014).

In terms of reliably repaying debt, I do see a handful of Ethereum lending applications which are underpinned by over collateralization. So it appears, at this reasonably early stage, that secured borrowing is viable. Simply put, the risk of loosing collateral seems to be enough to ensure that borrowers are predictably repaying their debts.

I am curious whether anyone has pursued/researched the following question … “is it possible to create **unsecured** borrowing between anonymous accounts, on a trustless, censorship resistant, permissionless network”?

Whilst this problem could be addressed via a social mechanism i.e. lenders mandating that a friend or family member go “guarantor for the loan” (which kinda swings back towards the secured loan side of the fence) I am very interested in learning about the possibility of a technology based solution to this unsecured borrowing.

Any questions, resources, ideas would be greatly appreciated.

# References

van Bochove, C. (2014). External debt and commitment mechanisms: Danish borrowing in Holland, 1763-1825. The Economic History Review

## Replies

**haael** (2021-02-20):

This might might be a bit cringe example, and probably this would be illegal in most jurisdictions, but there was a lending platform in China, where users were supposed to upload their nude photos (really). In case when they didn’t pay, the photos were published.

But this idea may be generalized. There might be some asset of no financial worth, that users still don’t want to lose. It may be something as simple as personal data. If you don’t repay the loan, your data is published.

Other things that may be taken hostage: passwords to social platforms, contact data to friends (that would be bombed with the information that this individual didn’t repay the loan), items in RPG games or some kind of virtual identity.

We could also resort to good old legal instruments. The user could simply fill in a cheque (or some electronic equivalent) and post it in encrypted/hidden form. If he doesn’t repay, the cheque is decrypted/published and may be used for legal action.

---

**tpmccallum** (2021-02-22):

Hi [@haael](/u/haael),

Thank you for your reply, you have added some awesome new ideas which are greatly appreciated.

Perhaps the most valuable message weaved through your response is that **consequences** are a vital factor in solving unsecured borrowing on Ethereum.

The following points are not all responses to your actual post (they are just new ideas and thoughts since my original post) so forgive my style of response writing ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) Just my way of getting thoughts out into the open.

I have separated my response into sub sections (key words) because I like to separate my thinking in order to ultimately reason from first principles. Here goes … firstly, reliability.

**Reliability**

The literature says that the ability for a borrower to repay loans reliably is paramount. This may have worked historically in historical societies but not here. My thoughts around this point are that any amount of reliability can still constitute a long con. A long con, where the borrower will gain the trust of lenders with the primary goal of **eventually** stealing from them; an inevitable net gain for a borrower (at a lender’s expense).

**Anonymity**

I would suggest that in a trustless, censorship resistant, permissionless network, users are never officially identified. An official user-identification service could only work if it were run by a trusted organisation (which would most likely be centralised in nature).

**Trust**

I think it is safe to say that an increase in anonymity, creates a decrease in trust.

**Risk**

Following that logic, it is then safe to say that a decrease in trust, translates to an increase in risk. So in essence, the main issue with unsecured lending on Ethereum is the risk of the lender not getting repaid.

**Consequences**

As per [@haael](/u/haael)’s response, one way to solve this is with consequences; whatever shape or size consequences come in. Simply put, an increase in consequences decrease the risk. An ongoing decrease in risk translates into an increase trust, and as a bi product, reliability.

**Positive consequences**

I have an idea for a loan contract which creates positive consequences by rewarding the borrower for paying the lender on time; and rewards the lenders regardless of whether the borrower repays them. I will create another reply so this post is not too long. The idea isn’t perfect yet but it is a start. Share soon …

Thanks again ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**tpmccallum** (2021-02-22):

Hi,

Additional response, as promised.

This is a sketch of the positive consequence which could drive unsecured borrowing on Ethereum. It all hinges around a loan contract that can mint and burn tokens.

## TL;DR

If loans are repaid:

- the lenders get some interest
- newly minted tokens are shared amongst lenders and borrowers
- the token becomes inflationary due to slightly increased supply

If loans are **not** repaid:

- the newly minted tokens are only shared amongst the lenders
- the token becomes deflationary due to reduction in supply (loan contract can burn tokens)

## Slightly longer version of events

Tokens are minted upon a new loan initialisation. If the borrower repays the loan then the token supply stays the same (and is shared equally amongst borrowers and lenders). If the borrower does not repay the loan, the token supply is slashed, which increases the value of the token. In addition the borrower does not receive any of the tokens and the lenders get all of the remaining tokens.

**Please note:** The percentage below can be tweaked, this is just the basic skeleton of the idea.

Enjoy …

## Loan scenario

Let’s say that Alice wants to borrow 1 Eth:

- Alice initialises her request (requesting 1 Eth) in the loan_1 smart contract
- Alice agrees that she will pay back the 1 Eth at a rate of 5% interest
- Alice is now known as borrower_1

The following is the state of the situation. Alice has no Eth and there are 4 potential lenders:

|  | loan_1(Contract) | borrower_1(Alice) | lender_1 | lender_2 | lender_3 | lender_4 |
| --- | --- | --- | --- | --- | --- | --- |
| Eth | 0 | 0 | 0.5 | 0.5 | 0.5 | 0.5 |
| LB | 0 | 0 | 0 | 0 | 0 | 0 |

Let’s say that 4 lenders see this request:

- The 4 lenders (as shown above) are known as lender_1, lender_2, lender_3 & lender_4
- Each of the 4 lenders stake their 0.5 Eth into the loan_1 contract

The contract is now ready to start the lending/borrowing process:

- The loan_1 contract mints 1200 new tokens
- Let’s say that this new token’s name is LB Token (which stands for Lenders/Borrowers)

The following is the state of the situation

|  | loan_1(Contract) | borrower_1(Alice) | lender_1 | lender_2 | lender_3 | lender_4 |
| --- | --- | --- | --- | --- | --- | --- |
| Eth | 2 | 0 | 0 | 0 | 0 | 0 |
| LB | 1200 | 0 | 0 | 0 | 0 | 0 |

The contract now releases the funds:

- as per the following table, borrower_1(Alice)  gets her 1 Eth, the loan_1(Contract) has 1 Eth left in it. The loan_1 contract sends 100 LB tokens to each lender and keeps as well as 800 of the new tokens for now.

|  | loan_1(Contract) | borrower_1(Alice) | lender_1 | lender_2 | lender_3 | lender_4 |
| --- | --- | --- | --- | --- | --- | --- |
| Eth | 1 | 1 | 0 | 0 | 0 | 0 |
| LB | 800 | 0 | 100 | 100 | 100 | 100 |

The contract now creates a new Uniswap pair of Eth:LB (if it doesn not already exist) and adds liquidity at the ratio of 1:400 (Eth:LB_1).

The situation now looks like this:

|  | loan_1(Contract) | borrower_1(Alice) | lender_1 | lender_2 | lender_3 | lender_4 | UniPool |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Eth | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| LB | 400 | 0 | 100 | 100 | 100 | 100 | 400 |

---

## Successful repayment scenario

If borrower_1(Alice) repays the loan (1 Eth and the aforementioned 5%) of 1.05 Eth then the lenders each get their 0.5 Eth back plus they each get the 5% interest (each lender gets a total of 0.525 Eth)

In addition to this, each lender gets to keep the 100 LB tokens plus an additional 100 LB tokens (from the UniPool) each

Borrower_1(Alice) then also receives the 400 LB tokens from the loan_1(Contract).

This is what a successful repayment scenario looks like:

|  | loan_1(Contract) | borrower_1(Alice) | lender_1 | lender_2 | lender_3 | lender_4 | UniPool |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Eth | 0 | 0 | 0.525 | 0.525 | 0.525 | 0.525 | 0 |
| LB | 0 | 400 | 200 | 200 | 200 | 200 | 0 |

## Failed repayment scenario

If borrower_1(Alice) fails to repay the loan. The lenders each get to keep the 100 LB tokens. In addition, the lenders each get 0.25 Eth and an additional 100 LB tokens each (from the UniPool).

The contract which was holding 400 LB tokens now burns those 400 tokens which (theoretically decreases the supply by 1/3 and theoretically then makes the price of the tokens increase by 33%)

|  | loan_1(Contract) | borrower_1(Alice) | lender_1 | lender_2 | lender_3 | lender_4 | UniPool |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Eth | 0 | 0 | 0.25 | 0.25 | 0.25 | 0.25 | 0 |
| LB | 0 | 0 | 200 | 200 | 200 | 200 | 0 |

This is just a preliminary run at this idea, percentages can be tweaked, does anyone have any other ideas about how to achieve unsecured lending? Thanks so much!!!

---

**TheCookieLab** (2021-02-22):

What’s to stop a bad actor from repeatedly borrowing and defaulting if they don’t care about earning LB? A rich or ideologically driven attacker would not be properly incentivized. Perhaps the lenders don’t mind (or even prefer) this scenario as they are still earning (appreciating) LB.

---

**tpmccallum** (2021-02-23):

Thanks [@TheCookieLab](/u/thecookielab),

That is a very good point which has inspired more thinking.

I have created a list below which outlines some new tweaks to the design, in order to make it more robust and less vulnerable to a rich or ideologically driven attacker. Thank you for your input, much appreciated!

## Positive consequences - interest rate

- Each Ethereum account address is allowed to borrow up to a maximum of 1 Eth at any one time (we might tweak this amount later)
- The  loan_1(Contract) has a default interest rate of 10%
- The  loan_1(Contract) will now accept 400 LB tokens from the borrower’s Ethereum account address; which will automatically reduce the interest rate from 10% down to 5%
- The borrower can obtain the LB tokens by either performing one successful borrow/repayment at the default rate of 10% or by purchasing LB tokens via Uniswap
- The borrower is not allowed to redeem the LB tokens until the borrower has repaid the loan (within the required term)
- LB tokens provided by the borrower (which guarantee a reduction in the borrowing rate i.e. from default rate of 10% down to 5%) will be burned if the borrower does not repay the borrowed amount

## Positive consequences - lottery

- Loans are processed in time-based rounds i.e. 10 loans of 1 Eth each, are available during each time-based round
- A new round can not start, until the previous round has finished (regardless of whether loans have succeeded or failed)
- Loans which succeed (lenders are paid in full) devote a small amount of Eth and LB tokens to a lottery for that round
- At the end of each round one of the borrowers who successfully repaid their loan will win the lottery
- The odds for a borrower winning the lottery are at least 10:1 (10 loans of 1 Eth per round)
- Attacks come with an opportunity cost of 400 LB tokens (which a borrower could have sold or used to reduce interest rate on their future loans)
- Attacks increase the chances that any of the other well-behaved borrowers will win the lottery

I will write up this new design and create another post (perhaps with diagrams). This was just meant to be a discussion but I am actually thinking that we can code this up and test it; seems quite logical and doable.

Thanks again legends!

Any more ideas/comments are welcome ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**tpmccallum** (2021-02-28):

Thank you for your input thus far.

Please see updated tables below. The column to the far left represents an event (one event per row)

The other columns represent the balances of the different entities i.e. the smart contract, the borrower, the lender etc. The loanable currency has been changed to `DAI` for stability. The “loan/borrow token” for this design is still called `LB`

The balances are always in the format of `DAI:LB` i.e. `10:5` is 10 `DAI` and 5 `LB`

# Single round #1

**Just one borrower and one lender to keep table simple**

Shows how total supply of `LB` tokens increases from 0 to 30 because of new borrower activity.

| Event | Borrower | Loan Contract | Uniswap Pair | Lender | Lottery Contract |
| --- | --- | --- | --- | --- | --- |
| Borrower wants 10 DAI | 0:0 | 0:0 | 0:0 | 40:0 | 0:0 |
| Lender provides 20 DAI (200%) to contract | 0:0 | 20:0 | 0:0 | 20:0 | 0:0 |
| Contract issues loan | 10:0 | 10:0 | 0:0 | 20:0 | 0:0 |
| Contract mints LB (loan * 3) | 10:0 | 10:30 | 0:0 | 20:0 | 0:0 |
| Contract creates new Uni Pair | 10:0 | 0:20 | 10:10 | 20:0 | 0:0 |
| Borrower repays loan at 10% | 0:0 | 11:20 | 10:10 | 20:0 | 0:0 |
| Contract disburses funds | 0:5 | 0:0 | 10:10 | 31:10 | 0:5 |
| Honest borrower wins lottery | 0:10 | 0:0 | 10:10 | 31:10 | 0:0 |

At this stage:

- borrower and/or lender can swap LB for DAI
- anyone can swap DAI for LB
- borrower who has LB can buy cheaper interest rate by sending LB tokens to contract
- repeat lender only has to provide 100% (not 200% as per round 1) if loan amount is less than what lender has in Uniswap Pair

# Single round #2 - honest borrower

Shows how:

- borrower buys cheaper interest rate (which causes contract to not mint new LB tokens in relation to that specific borrowers loan)
- lender now only provides 100% capital because loan amount is <= what the lender already has in Uniswap Pair
- if no max interest rate loans in this round (no new borrowers or borrowers who choose not to buy cheaper interest rate) then no lotto initiated
- total LB supply is, and remains, at 30 under honest conditions

| Event | Borrower | Loan Contract | Uniswap Pair | Lender | Lottery Contract |
| --- | --- | --- | --- | --- | --- |
| Borrower wants 5 DAI | 0:10 | 0:0 | 10:10 | 31:10 | 0:0 |
| Lender provides 5 DAI (100%) to contract | 0:10 | 5:0 | 10:10 | 26:10 | 0:0 |
| Borrower provides LB for better % rate | 0:5 | 5:5 | 10:10 | 26:10 | 0:0 |
| Contract issues loan | 5:0 | 0:5 | 10:10 | 26:10 | 0:0 |
| Borrower repays loan at 5% | 0:5 | 5.25:5 | 10:10 | 26:10 | 0:0 |
| Contract disburses funds | 0:10 | 0:0 | 10:10 | 31.25:10 | 0:0 |

# Single round #3 - dishonest borrower

Shows how:

- borrowsers LB tokens are burned if borrower does not pay
- LB total supply is 30 before the round and then 25 after the round (which increases LB's value)

| Event | Borrower | Loan Contract | Uniswap Pair | Lender | Lottery Contract |
| --- | --- | --- | --- | --- | --- |
| Borrower wants 5 DAI | 0:10 | 0:0 | 10:10 | 31.25:10 | 0:0 |
| Lender provides 5 DAI (100%) to contract | 0:10 | 5:0 | 10:10 | 26.25:10 | 0:0 |
| Borrower provides LB for better % rate | 0:5 | 5:5 | 10:10 | 26.25:10 | 0:0 |
| Contract issues loan | 5:5 | 0:5 | 10:10 | 26.25:10 | 0:0 |
| Borrower fails to repays loan at 5% | 5:5 | 0:5 | 10:10 | 26.25:10 | 0:0 |
| Contract burns borrowers 5 LB | 5:5 | 0:0 | 10:10 | 26.25:10 | 0:0 |

Total supply of `LB` has now gone from 30 to 25 which increases the price of `LB`

A few extra points:

- accounts that default on payment are not allowed to borrow

A few extra ideas:

- when transferring LB tokens, the receiver pays a 10% burn rate i.e. sellers can sell them but buyers are not getting 100% exchange rate (10% is burned during transfer).
- borrowers are not 100% guranteed a borrowing position during a round. Borrowers must request a loan and they might be selected to participate in the round. Selection is random. This prevents gaming the rounds and thus makes things a bit fairer.
- for each round, the contract may select a ratio of plain borrowsers (new borrowers / borrowers who are not purchasing cheaper interest rates) vs decorated borrowers (borrowers who have purchased or earned LB tokens and are prepared to deposit them to earn the cheaper rate) i.e. allows 2 new borrowers and 8 decorated borrowers. 2 of these could just steal the funds but the other 8 will cause LB tokens to burn if they steal. This ratio could help stabilise the system and ensure that ongoing dishonest behaviour will still cause the price of LB token to rise over time. Lenders will be able to recoup some funds by selling their LB rewards (which they earned from previous lends).

---

**bradleat** (2021-03-03):

We need a way to calculate a risk score for the account. We also need a way to serve a consequence to the account in case of default.

If clearing transactions for the unsecured borrowed funds took time or were otherwise segregated, we could provide a mechanism in which there is a default event. The counter-party of the these transactions would then have to assume some risk that the creditor would eventually reclaim a portion of their funds.

By looking at a graph of counter-parties which accept transactions with low-default rates and senders of those transactions, we could start to compute a per-account risk score. In the end this might just mean that the counter-parties were doing some sort of KYC or other risk limiting measure, but the creditors do not have to be involved with that process.

A consequence served to dishonest or defaulting accounts could be that things purchases with unsecured funds are placed into a universe in which the creditor can reclaim them from the system. This would involve some sort of coloring of tokens that were exchanged for unsecured funds so that other parties are aware of the default risk they by interacting with an account using unsecured funds. Alternatively, it would involve a system in which the exchange value made with unsecured funds is approved by the creditor and the the creditor can reap an account that is in default.

---

**tpmccallum** (2021-03-03):

Thanks [@bradleat](/u/bradleat),

It would be great to serve a negative consequence to the account address which does not repay a loan. I have not figured out a way to achieve this as yet.

I have been thinking that the contract could maintain a state of “niceness” whereby the contract has the ability to increase or decrease the ratio of:

- plain borrowers (new borrowers / borrowers who are not purchasing cheaper interest rates)

versus

- decorated borrowers (borrowers who have purchased or earned  LB  tokens and are prepared to deposit them to earn the cheaper rate)

## Are the plain borrower’s actions a foregone conclusion?

Whilst it may be inevitable that plain borrowers will run off with the money 100% of the time, it may just be the case that, during a given round of loans, some (or perhaps all) of them will repay; in which case the contract will increase “niceness” and offer a slightly larger amount of plain borrower positions (per round).

If the plain borrowers repeatedly run off with the money then the contract will reduce those plain borrower positions (and perhaps even the borrowable amount) to an absolute minimum for as many rounds as required (i.e. until a plain borrower actually pays back their loan).

## LB Token supply (the right balance of minting and burning)

The trick is to find the correct way to control the LB token supply. A clever design of minting and burning based on borrower actions (honest vs dishonest) should suffice. The LB token is the economic driver (incentive) for lenders to participate and for borrowers to be honest. LB tokens must be rare enough to have value and there must always be enough liquidity in the DAI/LB pool so that borrowers can buy LB and lenders can sell LB.

## Per account risk

I think it is safe to say that dishonest users will just come to the platform with a newly generated account address each time (posing as a new honest user). Definitely open to the per account risk approach and also Know Your Customer (KYC), however this does lean away from the permissionless and censorship resistance attributes of a decentralised network such as Ethereum. Instead, if there is a combination of maths, game theory and tokenomics which would work, then I would be inclined to choose the later over the former.

## Default risk awareness

I really like your idea of making other parties aware that they are accepting value from a borrowed loan agreement.

## Transaction types

There would definitely be types of transactions where this unsecured lending would be better suited i.e. a business selling food would not use this because they can’t re-coupe the food after the customer has eaten and left.

However, a business selling/renting a fixed asset (renting a house) or an ongoing asset like a gym membership would be a good use case i.e. in the case of the fixed asset, the authorities could accept evidence that the house/rent payment was not legitimate. In the case of membership, the gym would simply cancel the ongoing membership etc.

## B2C and B2B applications

Basically this new thinking takes the challenges of KYC, reputation, loan-guarantors, collateral, trust and “the long con” etc. and solves them by making this a 3-way interaction (as apposed to a 2-way interaction).

In a 2-way interaction on the blockchain the borrower can just run off with the money. This is like receiving cash in the hand. However, in a 3-way interaction there is an organic and natural relationship between two of the entities; the B2C or B2B relationship takes care of the anonymity element. Whilst the customer is now still able to lean on a lender from time to time, they are not in a position to re-sign up to the same Gym again and again under different IDs.

[![loan](https://ethresear.ch/uploads/default/original/2X/7/7f35358e4fb29568d35b7dc4d92b3b9a84621c50.png)loan346×392 5.96 KB](https://ethresear.ch/uploads/default/7f35358e4fb29568d35b7dc4d92b3b9a84621c50)

[![uclb2b (1)](https://ethresear.ch/uploads/default/original/2X/7/7e4ec16319e6971dc0adeb2c1dd3cfa793c9632d.png)uclb2b (1)364×422 6.92 KB](https://ethresear.ch/uploads/default/7e4ec16319e6971dc0adeb2c1dd3cfa793c9632d)

On the business side, businesses can register themselves as accepting this method of payment. This way the business is fully aware of the arrangement (the fact that their income from their client is via the unsecured loan DApp). These centralised “buy now, pay later” service like [zip](https://zip.co/) and/or [afterpay](https://www.afterpay.com/en-AU/index) are quite common these days. However, this Ethereum implementation would be decentralised whereby the decentralised lenders are earning the interest.

Thanks so much for your valuable input.

![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

