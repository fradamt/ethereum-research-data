---
source: ethresearch
topic_id: 9492
title: Mechanism Design for Decentralized Banking
author: kelvin
date: "2021-05-14"
category: Economics
tags: []
url: https://ethresear.ch/t/mechanism-design-for-decentralized-banking/9492
views: 2374
likes: 4
posts_count: 11
---

# Mechanism Design for Decentralized Banking

There are two very different types of debt:

1. Debt issued to buy a liquid asset, or issued with a liquid asset as collateral
2. Debt issued with an illiquid asset as collateral, or backed mostly by reputation

The first type is very simple, does not require complex institutions such as banks, and can be made to have very little risk. If the creditor can liquidate the asset whenever it decreases in price too much, then its own money will only be at risk in case of a relatively rare sudden price shock. This is the type of lending that we often see in exchanges and in DeFi today. (Other liquidation rules, if used, would introduce some risk premium equivalent to the premium for an option contract.)

The second type of debt is very different. The promise of the debtor to repay in the future is an asset, but because of adverse selection it is a very illiquid one and can hardly be sold. As a result, the institution providing such credit needs to both have specialized knowledge and substantial reserves to put such knowledge to use.

At first glance, one might think that there is not much opportunity for the second type of lending in a decentralized fashion, but that would be untrue. While a decentralized bank cannot accept a house or a car as a collateral for a loan, for it would need a government to back up claims on such goods, it can offer loans using NFTs or other valuable but illiquid assets as collateral. It can be expected that the number of such assets, perhaps representing possession of real-world assets in the blockchain, will increase in the future.

Moreover, there is much lending that is backed solely by reputation or by a credit score. Because government regulations in this regard often increase credit risk (e.g. by requiring that negative credit score information be erased after 5 years), and because governments will be incapable of enforcing these regulations on decentralized banks, it can be argued that such banks may end up with a competitive advantage. Decentralized banks, if they exist, will likely require personal information for such loans, and will sell rights on eventual defaulted debts to third-party debt collectors, just as traditional banks do. Therefore, decentralized banks may well be able to obtain a significant profit by using their reserves for such lending.

However, the history of banking shows that those with the specialized knowledge to provide such loans are often limited by the amount of capital they have. At the same time, many investors who have the available capital lack the knowledge to lend them productively. Therefore a decentralized bank, if it is to be successful, has to both lend money and borrow it from others.

This cannot happen unless there is a mechanism in place to protect the *depositors*, those that lend money to the bank. Of course, the bank insider should not be able to abscond with depositors’ money, but this is hard to do. Some mechanism needs to be in place not only to prevent the insider from outright stealing money from the bank’s treasury, but also to prevent it from tunnelling money to himself or to his associates.

I’ll sketch a potential solution to this problem, which is indebted to the classical analysis of [Calomiris (1991)](http://www.bu.edu/econ/files/2012/01/calomiris-kahn.pdf). To be clear, my proposed mechanism can certainly be improved dramatically. I will also assume that the bank is free to disclose all relevant information about the contracts it participates in (so I’ll ignore privacy considerations of bank borrowers).

A banker creates a smart contract and provides some initial capital of its own. This will be the bank’s equity capital. It also invites depositors to put money at the contract in order to receive interest. The banker can then use the bank’s treasury to give out loans, but these can only be done slowly (e.g. only 5% of the available funds may be used every week). This is so that, if the banker is committing fraudulent transfers, the depositors have some time to act.

The depositors can withdraw money on demand. The banker is supposed to keep a significant reserve. If a bank run does happen, however, and the bank remains without sufficient cash for some determined period (a few days), a bankruptcy process begins, in which all the illiquid assets of the bank are auctioned off over the next weeks. Any money obtained in this way is divided proportionally to the remaining depositors up to the amount due to them, with any surplus being given back to the banker.

If fraud is being committed, the first depositors to withdraw their money will not suffer any losses, and thus will be rewarded for causing a liquidation in this scenario. The liquidation, while potentially causing losses to the other depositors, will still save a substantial part of their capital, as compared to fraud continuing undetected. During a liquidation, equity capital from the banker is likely to be wiped out, generating a strong incentive for him to maintain transparency and a sustainable cash flow. If the bank operates reliably and profitably, the banker will be able to cash out profits slowly over time according to some predetermined rule (e.g. at most 1% of available funds per week).

To prevent bank runs from happening unnecessarily, the banker should have the right to put more of his own money into the bank. However, a better-designed mechanism should also allow:

- Non-controlling shareholders controlling bank equity. This will allow the bank to issue new stock to raise funds to avoid liquidation if needed. The bank would allow profits to be distributed to shareholders by having the bank buy its own shares at the market. Of course, there
would be a need for some governance protocol to replace the banker if needed.
- Junior debt that may be emitted to outsiders at higher interest rate, and that is not payable on demand. Such debt can be emitted both during liquidity crises, to avoid unnecessary bankruptcies, and preventively, as a cushion to reassure depositors.

Any comments on the feasibility of these ideas would be very much appreciated!

## Replies

**alimaltamash** (2021-06-05):

Hi Kelvin,

First of all I love the way you explained the defi banking system and its workings.

The concept of decentralized banking seems interesting but the existing system of banking which is exercised by the Central Bank is to keep gold reserves to back the valuation of the currency and in case of decentralized banking, the digital currency is backed by actual USD or the currency in respective countries. What happens in case USD depreciates against INR and leads to excessive surge in INR and hence results in inflation.

The concept of defi in this case, “I believe” will not work here.

My email ID is: [alimaltamash@gmail.com](mailto:alimaltamash@gmail.com), please connect with me in order to discuss more.

I would love to hear from you on this regard.

---

**Azalea** (2021-06-11):

Usually, when people take loans from banks, those loans have a specified maximum repayment date, right? How would this work if there was a sudden liquidation on the bank by the bank’s creditors? Would the debt with attached collateral be distributed by auction to the creditors, or would the collateral be attempted to be sold immediately? In the case of liquid collaterals the person who took the loan could just rebuy it back with what they borrowed, but if the collateral is an NFT or a house this becomes difficult.

---

**kelvin** (2021-06-11):

Hi Azalea, great question!

If the maximum repayment date has not yet been reached, the creditor (bank or otherwise) should not have the right to sell the collateral. So in case of bankruptcy, all such debts should be sold with collateral attached.

Even for debts that are overdue, I still believe the bankruptcy process should not attempt to sell the collateral assets themselves. It may well be better to sell the debt with the collateral attached and let the buyer decide what to do with it (whether to liquidate it or not).

One question is how to sell the assets of the bank in case of bankruptcy. There is a continuum with each asset sold in a separate auction in one side and all assets sold as a bundle in the other. Selling all assets separately is probably not good, as any debtors with money to pay could then buy their debts for cheap (probably much less than the money borrowed), leaving mostly worthless debt behind. Also, getting information on each specific asset is harder to getting an assessment of what a bundle is worth because you can use statistics to evaluate the latter. At the same time, auctioning big bundles means only the biggest investors can participate.

The best approach is probably to have some other institution managing the bankruptcy process, bundling similar assets together for auction. Such institution might even be capable of brokering a reorganization agreement if the majority of the depositors agree, but this is very complex, particularly if there if there are multiple classes of bank creditors.

---

**kelvin** (2021-06-11):

Hi Ali,

I’m not sure I understand your question. This banking institution that I have described is not particularly dependent on any specific currency, and may have debtors owing different currencies. Can you elaborate more? What goes wrong if the USD depreciates?

---

**alimaltamash** (2021-06-16):

Hi Kelvin,

First of all sorry for the late reply and its Alim and not Ali.

I was saying that when a dollar depreciates, it is backed by some value, be it gold or any other asset whatsoever.

In case of cryptocurrency, it is not backed by any sort of physical tangible value which can be used to deter severe inflation.

What happens, supposedly the price of USD in India rises whereas the monetary value of gold remains stable and the coins with which we are trading in USD, will it appreciate as well?

---

**chnejohnson** (2021-06-26):

Hi kelvin,

I really like this idea, and there is a question I want to ask you.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> A banker creates a smart contract and provides some initial capital of its own. This will be the bank’s equity capital. It also invites depositors to put money at the contract in order to receive interest.

I think the quote above is the core of this idea, and the mechanism you want to discuss is that how to protect depositors from bankruptcy.

On the other side, the banker can use money in the contract for giving out loans in order to earn profit, as the quote below.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> The banker can then use the bank’s treasury to give out loans, but these can only be done slowly

In the current DeFi ecosystem, people usually talk about “bankless” or similar idea that we build a market for sellers and buyers with smart contract instead of a centralized institution to handle money for people. In your use case, there is a banker who help depositors dealing with lending, so my question is that why we need a banker instead of a market to match up sellers and buyers?

As you said, there is an Information asymmetry.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> However, the history of banking shows that those with the specialized knowledge to provide such loans are often limited by the amount of capital they have. At the same time, many investors who have the available capital lack the knowledge to lend them productively. Therefore a decentralized bank, if it is to be successful, has to both lend money and borrow it from others.

So what do you think of having a decentralized market in which debt can be issued with an illiquid asset as collateral or backed by reputation instead of a banker dealing with it?

---

**kelvin** (2021-06-28):

Hi Johnson,

A peer-to-peer market for debt backed by illiquid assets is also interesting, but it will probably suffer from adverse selection issues. We must remeber that if the collateral is illiquid, that is because people do not know how much it is worth. And if you don’t know how much it is worth, it is really hard for you to be willing to lend money using that as a collateral.

If there is someone who is particularly gifted at evaluating the risks related to such illiquid assets, then this person can make money at this market, but he’ll probably run out of personal money to lend before he runs out of lending opportunities. Thats the point where he should become a banker and borrow money from other people (depositors). And is it at this point that the banking mechanism that I am proposing may be useful.

But maybe you are right and we should first develop the market for peer-to-peer lending with IOUs / illiquid assets as collateral first. As this market matures successful lenders (buyers of such debt) will run out of personal money and will seek to become bankers as I described above.

---

**kelvin** (2021-06-28):

Hi Alim,

I am sorry but I still do not understand. Are you talking about the money used to describe the loans and the interest? If so, yes: by taking a loan denominated in USD, while living in India, you assume the risk that the price of USD rise. So I believe people would mostly take loans denominated in their own home currencies (and decentralized banks could easily provide such loans). Even if depositors place USD in a bank, the bank can still use it to buy INR to lent, and may even hedge this foreign-exchange operation so that it can generate interest denominated in USD.

---

**sheegaon** (2021-06-29):

I applaud your attempt to think through how a decentralized bank would function. However I believe you are putting the cart before the horse. What’s really needed before any of these decentralized banking institutions can develop is a solid legal foundation allowing the holder of the NFT collateral token to use the existing legal system and bankruptcy process to go after borrowers in default. I also think one would have better luck developing the right organizational structure (not sure mechanism design is the right term, here) with institutional borrowers, such as governments and large corporations. These institutions already have several types of debt outstanding. The logical next step for DeFi is either tokenizing existing debt or issuing debt directly on the blockchain. Blockchain-based ownership could improve capital efficiency via distributed ownership and risk-taking and would result in lower borrowing costs, incentivizing more participation by large issuers and resulting in a virtuous cycle of adoption. But none of this can get started without strong legal recourse to pursue borrowers in default.

Eventually a parallel rating system similar to the one maintained by the NRSROs (S&P, Moody’s, etc.) could develop, and a well-functioning system could gradually be expanded to smaller borrowers. As it is, the costs of gathering information on the credit-worthiness of potential borrowers are likely too high relative to the potential profits for all but the largest loans.

---

**kelvin** (2021-07-02):

[@sheegaon](/u/sheegaon), I totally agree on the importance of tokenizing bonds, and on the advantages of a legal foundation giving rights to the holder of such tokens. In the short term this may indeed be the most important thing to do. I even agree that we are still not ready for decentralized banking (that’s why, while discussing this idea here, I’m actually working on a completely different thing, namely, how to solve the problem of MEV in decentralized exchanges and latency-arbitrage for trading in general).

In the very long-term, however, governments may not even be needed to enforce most debt obligations. I expect companies in the future to have much more value in virtual assets that can be tokenized than in physical assets that are controlled by governments. If this is correct, we may in the future have ‘crypto-jurisdictions’ in which companies may register, issuing debt with their virtual assets as collateral, and these crypto-jurisdictions will have power both to enforce contracts among such companies and to arbitrate bankruptcy and other disputes.

And yes, we’ll need a rating system to do what S&P, Moody’s and other rating agencies do today. But for heaven’s sake I hope we can do better than that! Rating agency capable of rating subprime mortgage securities as triple-A are nearly worthless.

