---
source: magicians
topic_id: 21191
title: "ERC-7776: Transparent Financial Statements"
author: Nachoxt17
date: "2024-09-25"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7776-transparent-financial-statements/21191
views: 191
likes: 3
posts_count: 3
---

# ERC-7776: Transparent Financial Statements

# Discussion about

## Abstract

This proposal defines a standard A.P.I. that enables E.V.M. Blockchain-based companies (or also called “Protocols”) to publish their financial information, specifically Income Statements and Balance Sheets, on-chain in a transparent and accessible manner through Solidity Smart Contracts. This standard aims to emulate the reporting structure used by publicly traded companies in traditional stocks markets, like the [S.E.C. 10-Q filings](https://www.sec.gov/about/forms/form10-q.pdf). The financial statements include key information, namely as Revenue, Cost of Goods Sold, Operating Expenses, Operating Income, Earnings before Interest, Taxes, Depreciation, and Amortization (E.B.I.T.D.A.) and

Earnings Per Token (E.P.Share-Token), allowing investors to assess the financial health of blockchain-based companies in a standardized, transparent, clear and reliable format.

## Motivation

The motivation of this E.I.P. is to Bring Seriousness to the CryptoCurrencies Investments Market. Currently, the situation is as follows:

Most ERC-20 Tokens representing E.V.M. Blockchain-based companies (or also called “Protocols”), DO NOT work the same way as a Publicly Traded Stock that represents a Share of ownership of the equity of that such company (so the user who buys a Protocol’s ERC-20, is also now a share-holder and co-owner of the business, its profits and/or its dividends), but rather function as “Commodities” such as oil; they are consumable items created by said E.V.M. Blockchain-based company (or “Protocol”) to be spent in their platform. They are Publicly Traded and advertised to be representing the underlying Protocol like a Share, working in practice the same way as a Commodity and without any Public, Transparent and *Clear* Financial Information as publicly traded stocks have.

Added to that, most token research analysis reports that can be currently found on the internet are informal Substack or Twitter posts, with lots of abstract explanations about the features of the said Protocol to invest in, that lack of transparent financial numbers and factual financial information, that are made by anonymous users without real exposed reputations to affect.

This E.I.P. will improve that by giving users and investors transparent, clear and factual financial information to work with when analyzing as a potential investment the such

E.V.M. Blockchain-based company that implements this E.I.P. in their Solidity Smart Contracts, and that will generate Trust, Transparency and Seriousness in the CryptoCurrencies Investments Market long term.

## FEEDBACK:

Please, everyone is invited to respectfully and constructively provide useful feedback. Have a nice day! ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=15)

## Replies

**tjayrush** (2024-10-05):

I, for one, find the information you’re trying to capture here very interesting. I wonder, though, how the information being reported would be “posted” to the contract reporting them. If the data is “publushed” or “pushed” periodically by “some trusted party,” that’s one thing (and much less interesting to me). If the data is “gathered” as regular operation of the contract (in other words people have to submit invoices, pay bills, etc.) that would be very much more interesting. I looked at your examples, and it appears the data is assumed to be present. Where does it come from?

---

**Nachoxt17** (2024-10-09):

Hello [@tjayrush](/u/tjayrush) ! Very good question. So in brief, the information is provided and upgraded by the same company/protocol that is using their own implementation of ERC-7776, directly from their business smart contracts (directly from their blockchain “bank accounts”).

Each protocol has different smart contracts and ways to generate revenue, name methods, they handle different assets, etc. So the Standard is made in a way to make that adjustable from different cases.

Why would they do that at all? Easy; it’s in their own interest to provide this information to generate trust among investors, and thus to potentially receive more investments.

Also, I just added this line to the specification:

> If the contract owner uses data or methods from other owned smart contracts external to their implementation of ERC-7776, those smart contracts MUST be verified in the correspondent blockchain explorer and of open and visible source code.

