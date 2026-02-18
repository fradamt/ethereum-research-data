---
source: magicians
topic_id: 2420
title: Community Call with Megan Knab -- Treasury Management & Crypto Accounting -- Jan 24th, 2019, 8am PST
author: boris
date: "2019-01-14"
category: Protocol Calls & happenings > Presentations
tags: [community-call, crypto-accounting, treasury-management]
url: https://ethereum-magicians.org/t/community-call-with-megan-knab-treasury-management-crypto-accounting-jan-24th-2019-8am-pst/2420
views: 2812
likes: 13
posts_count: 7
---

# Community Call with Megan Knab -- Treasury Management & Crypto Accounting -- Jan 24th, 2019, 8am PST

I’ve organized a community call on the topics of **Treasury Management & Crypto Accounting** for January 24th, 2019, 8am PST ([Add to calendar, signup for email notifications](https://teamup.com/event/show/id/7dNSzVSSki53nbMafRkkGK5kd5sFjc)). Everyone is welcome to join in [via Zoom](https://zoom.us/j/767928217), and we will record the call.

Megan [@meknab](/u/meknab) will be sharing her knowledge with us (and anyone else with expertise is also welcome to join!)

Megan has come up with a couple of questions / topics to cover:

- Financial Reporting v. Tax Reporting
- What metrics can you use to manage your crypto treasury?
- Crypto bookkeeping best practices
- Accounting edge cases - (hard forks, air drops)

See the [HackMD file](https://hackmd.io/Nf0-fCKmRZ6eP9AqfruZWQ?both) to add your own questions and for all the notes and content for the event.

---

## About Megan

Megan’s professional experience and personal interests revolve around building efficient systems. Megan is the founder of VeriLedger, a project that is working to streamline bookkeeping and financial reporting for crypto-enabled businesses. Prior to founding VeriLedger, Megan was an early member of a cryptocurrency agency brokerage project out of ConsenSys. Before that, she consulted with a venture capital firm focused on making investments in the blockchain ecosystem as well as worked at an AmLaw 100 firm in financial operations. She wants to make financial management and transparency easier for companies.

---

Megan volunteered to [help out the Magicians with finance in this Github issue](https://github.com/ethereum-magicians/scrolls/issues/55). [@Flash](/u/flash) is helping us out, but we’re happy to have advisors with specific expertise like this.

You can also see a [long back and forth about DAI, ETH, conversions, and how DAI CDPs work here](https://ethereum-magicians.org/t/stable-magicians-poll-exchange-vs-cdp/2377/32).

## Replies

**jpitts** (2019-01-14):

You rock [@boris](/u/boris), thanks for organizing the call!

---

**meknab** (2019-01-14):

I promise to make it the most interesting convo about accounting there has ever been!

---

**boris** (2019-01-24):

Thanks everyone for dialing in and joining [@meknab](/u/meknab) (find her on [Twitter as @knotmegan](https://twitter.com/knotmegan)) and myself today. I learned a lot, and appreciate Megan taking the time.

The video capture is here https://zoom.us/recording/share/wOxdfH5gQymvG_6ed6oE4ESDH1afk6JykBy0Oa3EyOywIumekTziMw

I live typed some rough notes as Megan was talking in the [HackMD file](https://hackmd.io/Nf0-fCKmRZ6eP9AqfruZWQ?both) – I’ve pasted in those notes here so we have a permanent record.

Megan shared a budget variance spreadsheet template: https://docs.google.com/spreadsheets/d/1OzM7xu1ss9JJCT5hscIdm_f7QYoT4DMBVCpEZr76Cmg/edit?usp=sharing (File > Make a Copy for your own version).

I previously shared a cashflow / budget template that I use:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)

      [Discussing Long Term Cashflow and Budgets for Ethereum Projects, Teams, and Individuals](https://ethereum-magicians.org/t/discussing-long-term-cashflow-and-budgets-for-ethereum-projects-teams-and-individuals/1849) [Primordial Soup](/c/magicians/primordial-soup/9)




> TL;DR: Here is a template for planning out cashflow and budgets for projects. Let’s use these to have a discussion about sustainability, the complexity & need for some global  entities, and how to work together and improve all of this.
>
> For our own work at SPADE in getting support for ERC1066 and the rest of FISSION Suite, and our new project around EVM Evolution, I modified a set of cashflow / budget planning spreadsheets that I’ve used to support new startups. It’s a vastly simplified version…

For “regular” accounting, we mentioned a “command line accounting tool” [beancount: Double-Entry Accounting from Text Files](http://furius.ca/beancount/). Personally I use and have recommended Xero https://xero.com for multi-currency. [@serapath](/u/serapath) on Twitter recommended Wave https://waveapps.com (Canadian company, they are good for sole proprietorship / small businesses) and QuickFile https://www.quickfile.co.uk/ (UK businesses)

CoinGeck has historical USD / ETH prices https://www.coingecko.com/en/coins/ethereum/historical_data/usd#panel – what other sources of historical price data? For different currency pairs, eg CAD, EUR, etc.?

For EthMagicians, this is my rough TO DO that I’ll turn into Github Issues:

- multisig additions – adding AT LEAST a third person (@Flash) and do 2 of 3
- write down policy for expenses

going back paying Boris back for Berlin while applying policy of cost of ETH at that time

2018 “books” – look back at actuals
budget

- per event budget
- we have one for Paris
- are we doing two more events this year?

open collective - further thoughts on how this interacts as fiscal sponsor

Megan will be at ETHDenver in the Business Models ring – see [ETH Denver Magicians Applications and Gatherings](https://ethereum-magicians.org/t/eth-denver-magicians-applications-and-gatherings/2115)

Find out more about Megan’s startup Veriledger https://veriledger.io/

---

## Notes

Budget v actual analysis template https://docs.google.com/spreadsheets/d/1OzM7xu1ss9JJCT5hscIdm_f7QYoT4DMBVCpEZr76Cmg/edit?usp=sharing

High volume & categorizing transactions is a big pain for accounting

Talked to a lot of people, nothing quite ready

Talked to accounting firms about outsourcing – not that many accountants / book keepers that know anything

Also expensive

Concept of Veriledger – automate super simple accounting procedures – take in data, GAAP standards, international accounting standards

Normal non-crypto, lots of software for automating biz process – lots doesn’t in crypto

Not technical – accounting person

Veriledger – integrating Exchanges and pulling data off of Ethereum

- not just value of portfolio, but simple General Ledger stuff
- creating financial statements
- running a budget
- release in April

Crypto Book-keeping 101

Chart of accounts

- Before Quickbooks etc.
- actual journals kept
- most enter in general ledger
- assets, liabilities, equity, revenue, expenses
- first three are balance sheet – other are income statements
- PNL for Proft and Loss

Find templates online

Using QB or Xero

Megan has a template – can share

Chart of Accounts won’t fit business perfectly

Nature of operations – level of granularity

What is your business doing?

Chart of Accounts tailored to Domicile – esp for tax payments

If you have an international business you need a chart per entity – roll up for consolidated

How to categorize those kinds of transactions?

have a methodology that works for me (Megan)

Financial reporting vs. tax reporting

Chart of Accounts is for financial reporting

Having an account for ForEx differences, fair market value, having something that holds gains or losses

I (Megan) likes a lot of granularity

James Q: templates for chart of accounts

LLC, Service Based business

Don’t touch chart of accounts once setup

Little accounting annoying thing – e.g. different tax accounts

Setting up a budget

- have a template – HackMD
- Boris: share link on EthMagicians
- some people put budgets into another bucket

Reconciliation process

- tagging transactions to the ledger
- month is standard process

When going through crypto transactions

- cost basis – biggest pain points
- price per coin that you paid

Other areas of world, taxed as asset, on cost basis

When you pull off exchanges, don’t have cost basis

Pulling Wallet history off etherscan – cost basis not included

5 day rolling average, closing price on Coin Market Cap

Document

Write a policy in your teams Google Drive

Trade off between precision

https://www.coingecko.com/en/coins/ethereum/historical_data/usd#panel

Equivalency in native currency – USD, CAD, etc

Need to write it down

Can be annoying – making it easier

Once you create good habits

Creating an audit file

Certain software like Quickbooks, Xero – can upload support

File folder that has logical organization

Taking in revenue in crypto

Best practices – convert it to fiat right away

Once you get it, it’s Fair Market Value

Want to convert it right away

Coinbase, BitGo – do it right away

Bryant: what about DAI?

Doesn’t mean you don’t need to track cost basis

G-USD – where it literally is a fiat tie (Gemini) – regulated exchanges, Circle too

Having audited financial statements – most small companies don’t need it

Investors

Line of Credit

Expensive – have to hire them to come in

Months long, sitting with the audit team

Budget to Actual – do a variance

Pop the real, actual numbers – column that will populate the difference

Last piece – taking a moment, to reflect on your numbers

Are these numbers telling the story of your business?

What we were going to do?

We were going to do ETH → DAI

Have someone pay expenses, give DAI to them?

- if you are transacting in and out of crypto, always taxable
- if you’re paying people back – not paying employees in crypto currency W2
- coal miners being paid in coupons
- W2 have to be paid in

Figuring out how to financially empower EthMagicians, open source groups

I (Megan) want to get involved more in open source, why not just create a

What we are trying to do – other cool groups – Digital Chamber of Commercie – AICPA(?) are paying attention

Consensys has done lots of lobbying

This is how it should be – this is how we’re treating it

Another mission, let’s create a good standard – methodology for calculating cost basis

## Treasury Management

Emotional constancy exercises – trading in traditional markets, and especially in crypto markets – is an emotional process

Make logical, financial based decisions

All about setting parameters

When you’re doing your budget

One of the things you should be paying attention to

Once you have that for the next 3, 6, 12 months – if you’re levered – if 80% of expenses is fiat currency, if your portfolio is 50% crypto

Trying to bet, is not a good way to manage your business

At a regular point – depends on the wick of the portfolio

Maybe it’s once a week, once a month

Rebalancing with your liabilities

Risk tolerance

Convert back to USD

Measuring your crypto portfolio – to USD

Continue to keep it in portfolio

But also taxes from profit taking

Flip side – working on escrow service

Need a lot of that native currency in their reserves

Need to pay for gas fees

what is the lowest price you’ll tolerate (stop gap) – before you liquidate

what is reasonable profit margin on crypto? 30x?

principles – like stop gap, is a good policy

memorialize

incorporation documents

Policy folder –

Liquidity strategy

Simple to say – making sure you are in the right exchanges

Making sure you can trade out of alt coins

Prepared to press a button

People who “donate” – can’t take that as a deduction

Closing after big events

Recommend – working through reconciliation

Organizational wallet

- using a multisig
- keeping public address in chart of accounts?
- it’s possible to do?
- implicit in USD – break it down by asset
- aggregate all ETH
- exchange account or wallet

Veriledger

Quickbooks plugin

Accounting leave a lot to be desired

Open source

---

**boris** (2019-02-06):

The video is still up on Zoom for now, but I’m working on my toolchain to export and host this myself. Not yet on IPFS, but that will be the goal ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)




              https://images.spade.builders/video/2019-01-24-treasury-mgmt-crypto-accounting.mp4



Yes! Looks like embedding it directly as an MP4 link works!

---

**serapath** (2019-11-12):

Zoom link doesnt work.

The IPFS thing seems to be not available. …bummer.

---

**boris** (2019-11-12):

Yes I deleted it from Zoom. The embedded video is just a regular server file link — I haven’t put it on IPFS yet. View source and try visiting the file directly? The embed works for me on Mobile Safari.

