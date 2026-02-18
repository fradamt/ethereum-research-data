---
source: ethresearch
topic_id: 9487
title: Loans and "virtual" money
author: echopolice
date: "2021-05-13"
category: Economics
tags: []
url: https://ethresear.ch/t/loans-and-virtual-money/9487
views: 1335
likes: 0
posts_count: 8
---

# Loans and "virtual" money

One of the questions that tormented me about defi is the problem of how to implement the issuance of loans in a decentralized anonymous network. Obviously, in such a system, it is not possible for the bank to issue the amount of money to the applicant, since there is no force that could control the repayment process in the event of non-fulfillment of loan obligations. But maybe there is some other possibility?

I will try here to give an abstract concept describing how this can be implemented in the ethereum.

Suppose we have an applicant **A** who want to take loan for the amount of *X* USD. For this purpose, he applies to a decentralized bank **DB**. He enters into a smart-contract **SM**, which specifies the amount issued, the term and the interest rate. DB gives him *X* virtual" USD, which cannot be withdrawn from the network (provided to avoid fraud), but can be used inside the network. To do this, the bank must have the amount *X* of real dollars that are used in the **SM**: this amount is frozen inside **SM** and also duplicate is created for it in the form of virtual dollars. Also issued virtual coins must be associated (linked) with such a **SM**.

**A** can, for example, exchange this *X* virtual USD on *Y* BTC on the uniswap - it will work like this:

the market freezes *Y* bitcoins, *Y* virtual bitcoins are generated for this amount, which are exchanged for *X* virtual USD. *Y* virtual coins inherit the link to the **SM**. Until the loan is repaid, that is, the repayment period has not come, exchanges (or another actions) occur in this way with virtual currencies.

As soon as the maturity date has come, there are two options:

- if A has successfully coped with its obligations - then all virtual currencies turn into real ones, and the frozen ones disappear (burn off);
- if A do not return with the payment, the virtual money is burned, and the frozen money is defrost (they are again available for operations).

Thus, there is a certain period of time (from taking out a loan until its maturity), in which there is uncertainty and there is an exchange of virtual money, the status of which at a certain point in the future is determined unambiguously.

P.S.: the name"virtual money" is a reference to virtual particles in quantum theory involved in the intermediate interaction between real particles.

P.S.S: from the moment of taking out the loan until the maturity date, the money taken out on the loan is in a superposition of 2 states: *freeze>* and *virtual>*.

## Replies

**kelvin** (2021-05-13):

I think the best mechanism depends crucially on what the loan is to be used for. If the loan is to be used in currency/token speculation, then a fixed maturity loan is bad because it lets debtors gamble the creditor’s money. A much better solution for this use case is a leverage/liquidation mechanism as in a futures exchange, as it allows the debtor to assume most of the risk of its own speculation.

On the other hand, if debt is to be used for real-world investment or consumption, virtual currency does not suffice. This means that some force is required to induce repayment, as you mentioned. Traditional banks often give loans secured by physical assets (cars, homes) because the government can back up these claims, so a decentralized bank will have trouble competing for that. At the same time, they also give naked loans based on reputation (if you don’t pay it damages your credit score). I can see decentralized banks competing effectively for such loans eventually.

For instance, there may be a mechanism in which, if a debtor does not pay on time, the creditor may reveal it to the world, so that everyone, from potential new creditors, friends, employees, etc, can see that this person owes money, which can be potentially damaging or embarassing. This may encourage that person to pay. Furthermore, the debt obligation from that person may be stored an NFT asset and sold in the secondary market (particularly after it has not been paid on time). It may then be bought by a debt collector company capable of ‘pestering’ the debtor using phone calls, social media, etc.

---

**echopolice** (2021-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> I think the best mechanism depends crucially on what the loan is to be used for. If the loan is to be used in currency/token speculation, then a fixed maturity loan is bad because it lets debtors gamble the creditor’s money. A much better solution for this use case is a leverage/liquidation mechanism as in a futures exchange, as it allows the debtor to assume most of the risk of its own speculation.

In the method described above, the peculiarity is that there is no risk for the lender, because it gives to the borrower a duplicate of the frozen funds in the form of virtual money until the agreed deadline.That is, it only loses in liquidity.

---

**kelvin** (2021-05-13):

It is not true that there is no risk to the lender. If I ask for a loan of X USD, and I use it to buy a virtual bitcoin, I can wait and see if bitcoin price increase. If it does increase, I can sell my virtual bitcoin for more than X USD at a profit, meaning that I can pay back my loan and retain the difference. However, if bitcoin price decreases, I’ll not pay my loan back, meaning everyone will get their frozen coins back. This means that some poor guy will get the real BTC back that is now worth less than what it was worth before. No one will want to sell BTC for X USD under these conditions, as they will get X USD if bitcoin price ends up higher than X, and they will get one bitcoin (now worth less than X) if price ends up lower.

---

**echopolice** (2021-05-13):

I meant that the lender does not have the risk of losing the original amount in units of the issued asset. The risks associated with the dynamics of currency prices are certainly present.

I will add that it is reasonable to assume that the borrower is obliged to make some initial payment (+fee), which in case of non-repayment of the loan remains with the lender.

Therefore, the final decision of the borrower to be honest / dishonest will depend on what is bigger - the loss of the initial payment or the loss associated with the price difference + interest balance.

---

**kelvin** (2021-05-13):

Agreed, but do you see any advantage of this model compared to an exchange model in which leveraged trading is offered? As you cannot withdraw tokens bought with leverage from an exchange, they are arguably very similar to your proposal of virtual tokens, particularly if there is some initial payment.

The only major difference is that the lender (the exchange) has the right to liquidate the borrower if the price moves too much. If a similar liquidation mechanism is not present, a significant risk premium to the lender will have to be paid. If this is the desired outcome, then it is probably equivalent to a token derivative trade in which the borrower pays a premium to purchase a structured set of options.

---

**echopolice** (2021-05-13):

Perhaps you are right, and the proposed scheme is no better / worse than the existing tools (to be honest, I know them very superficially). It seemed to me that the idea of virtual money gives me more freedom of action: for example, in the future, when developing the network, I could buy voting rights with credit virtual money or buy company/personal tokens or other products special for the decentralized network.

---

**echopolice** (2021-05-30):

Perhaps, it is worth once again emphasizing the main advantage of the idea and developing it further.

Existing credit solutions work with collateral or are only suitable for exchanges. The scheme above is still seen as the closest to mimicking the traditional credit (without collateral) in centralized networks. The issued virtual money can be spent for specific products of the decentralized network: buy voting tokens, buy organization tokens, buy NFT-tokens, buy tokenized products in the future (books, videos, and so on).  For example, in the case of tokenized products, the scheme may be as follows: the buyer is given a duplicate of the item (and the original is frozen), which can be destroyed if the buyer stops paying on the loan.

Such a loan is issued for a period of T, and each month the client is obliged to pay a monthly payment, if the client does not receive a monthly payment in the agreed period, the loan contract is terminated: virtual money is burned, frozen bank money is released (similarly, this applies to all other agents with the scheme of interaction with virtual money).

To improve the system, it makes sense to introduce a trust rating for each user, which will depend on the client’s past credit history.

For a client without a credit history, the rating will be set to 0, but the rating can be raised in several ways:

- due to its own provision of cryptocurrency;
- due to the provision of a co-borrower/supervisor, who contributes to the bank a certain part of the loan amount, which will be frozen for the duration of the loan;
- due to the social rating (in the future, when there will be decentralized social networks with a rating).

If the customer stops paying on the loan, then his rating decreases - for new customers it becomes negative, after which they lose the opportunity to receive a loan. A higher rating allows you to get a loan at a lower interest rate.

The client’s trust rating should be dynamic during the life of the loan: then it is possible to create conditions for the market of risk sharing. Anyone can come to this market and choose loans depending on the dynamics of the trust rating for support. Then such a person can expect to share with the bank the proceeds from the interest on the loans, committing to partially pay for the loans in case of default  (depending on the amount invested).

