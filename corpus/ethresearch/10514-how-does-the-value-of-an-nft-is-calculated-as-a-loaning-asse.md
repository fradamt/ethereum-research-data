---
source: ethresearch
topic_id: 10514
title: How does the value of an NFT is calculated as a loaning asset?
author: Shymaa-Arafat
date: "2021-09-06"
category: Economics
tags: []
url: https://ethresear.ch/t/how-does-the-value-of-an-nft-is-calculated-as-a-loaning-asset/10514
views: 3774
likes: 0
posts_count: 13
---

# How does the value of an NFT is calculated as a loaning asset?

I’ve been thinking, maybe the very high NFT prices is a trick:

-Alice have X value

-So, Alice hires Bob off-chain to submit a rubbish NFT in an auction

-Alice buyes the NFT at price X

-Alice redeems (X-Y), pays Y to Bob

-Alice put the NFT as an asset&get a loan2/3X

-Alice makes a Profit=2/3X-Y

-If we assume Bob won’t settle for less than half Y=X/2

-Then Alice gains X/3 out of nowhere, probably less than the loan cost ( I mean interest rate)

-Makes me wonder, what are the liquidation rules for NFT assets??

## Replies

**zhew2013** (2021-09-06):

> Alice put the NFT as an asset&get a loan2/3X

If this NFT is rubbish, I don’t think the loanee will give Alice 2/3X as a loan, right?

The collateral ratio for the rubbish NFT will be low. Also because the liquidity for NFT is much poorer than popular tokens such as ETH, the collateral ratio will generally be lower.

---

**Shymaa-Arafat** (2021-09-06):

On

![](https://ethresear.ch/user_avatar/ethresear.ch/zhew2013/48/7114_2.png) zhew2013:

> If this NFT is rubbish, I don’t think the loanee will give Alice 2/3X as a loan, right?

OK, that leads to the question on what bases does the loaning platform evaluate any NFT?

Is it just the auction price or what?

---

**zhew2013** (2021-09-06):

Definitely not just the price. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

The loan amount equals to evaluated asset price times the discounted ratio.

Discount ratios is determined by a number of factors such as collateral asset type (the more stable, the higher the ratio will be, such as real estate typically has 80%+ discounted ratio), type of lender (the bank, your friend, etc.), length of loan (short term or long term), and many more.

I am not an expert. Someone should answer this better. But hopefully this can provide a bit info. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**Shymaa-Arafat** (2021-09-06):

I’m asking about the fixed tools of DeFi Ecosystems and LPs

The point is this is not a bank where humans will sit and make judgmental decisions on a case by case bases in addition to the rules

DeFi systems work automatically based on just equations.

---

**zhew2013** (2021-09-06):

The point is still the same though, right? Properties like the stability of the collateralized asset can be calculated as the volatility of the price history.

---

**Shymaa-Arafat** (2021-09-07):

If nothing new happened since Mar2021, I think this nearly answers how


      ![](https://ethresear.ch/uploads/default/original/3X/9/3/93c04e97d1043c7483a1855cd7dd95f1355bd57c.png)

      [MVP Workshop – 11 Mar 21](https://mvpworkshop.co/nft-lending-current-state-and-whats-next/)



    ![](https://ethresear.ch/uploads/default/optimized/2X/6/6546e0a96099fe1fa951208c59e9c44590f565a9_2_690x345.jpeg)

###



At the MVP Workshop, we had a chance to organize an internal NFT hackathon. The topic was NFT liquidity. Here's what we've discovered.



    Est. reading time: 6 minutes











> Blockquote
> Many different projects are trying to create efficient price discovery mechanisms. Most of them use auction and sale models, but it seems that they are insufficient as we still don’t have an appropriate price discovery mechanism.

It seems the area is little vague, he didn’t mention true example cases, I think the price determining is the main problem among others; like if represented as NFT how to add to it if u want to, becomes like Bitcoin UTXOS coin selection,…

Other problems if u add an ERC-20 representation

---

**DesktopCommando** (2021-09-08):

Can always place the NFT inside an emblemvault along with a financial backing of cryptocurrencies.

https://desktopcommando.medium.com/what-is-emblemvault-14aaaff92a20

---

**Shymaa-Arafat** (2021-09-08):

Thanks for the link anyway, but It doesn’t say how they calculate the collateral value of the NFT as a loaning asset

---

**Shymaa-Arafat** (2021-09-14):

Adding to the original post:

-Alice could also, due to the anonymity property, create like N addresses & make them look like N bidding account in her own auction; ie transfer the Flashloan money to a different account of hers

---

**Shymaa-Arafat** (2022-02-06):

In addition to papers & Scientific reports emerged since then about NFT auctions, I think these two links shows that what I was doubting actually did happen


      ![](https://ethresear.ch/uploads/default/original/3X/3/8/38a551f6157002f3963476880a6dc882ac79e9c0.png)

      [Chainalysis – 2 Feb 22](https://www.chainalysis.com/blog/2022-crypto-crime-report-preview-nft-wash-trading-money-laundering/)



    ![](https://ethresear.ch/uploads/default/optimized/2X/0/028624755d2f3dfa0f91335090380048c783afc4_2_690x460.jpeg)

###



Chainalysis detects significant wash trading and some NFT money laundering in this emerging asset class. Download the NFT Market Report



    Est. reading time: 9 minutes












      ![](https://ethresear.ch/uploads/default/original/3X/e/9/e93eb556d88dadd661ddbae4aa9e499d6634dd89.png)

      [Engadget – 4 Feb 22](https://www.engadget.com/nft-wash-trading-scams-chainanalysis-report-202537095.html)



    ![](https://ethresear.ch/uploads/default/optimized/3X/e/4/e4852b4a905415ff315b87c718b51eaa65799462_2_690x459.jpeg)

###



Traders are selling themselves their own NFTs to drive up prices, according to a new report by Chainalysis.










You can read in the latter

> The report tracked instances of the same traders selling the same NFTs back and forth at least 25 times, a likely incident of wash trading. It identified a group of 110 alleged NFT wash traders who have made roughly $8.9 million in profit from this practice. Researchers also discovered significant evidence of money laundering in the NFT marketplace in the last half of 2021. The value sent to NFT marketplaces by addresses associated with scams spiked significantly in the third quarter of 2021, worth more than $1 million worth of cryptocurrency, according to the report. Roughly $1.4 million dollars of sales in the fourth quarter of 2021 came from such illicit addresses.

---

**Shymaa-Arafat** (2022-02-10):

Trying to make this post like a library or Archive of all about the topic, let me add:

https://vitalik.ca/general/2021/08/22/prices.html

Here u can find 3 proposed solutions and also a link to proof of personhood or humanity.

.

Here some links I gathered about NFT attacks like rug & pull for example



      [m.facebook.com](https://m.facebook.com/story.php?story_fbid=1610742449280197&id=100010333725264)





###










.

Here you can find 2 rich reports (r2 & r8) from prof. Tim Roughgarden course



      [timroughgarden.github.io](https://timroughgarden.github.io/fob21/index.html#final_projects)





###










.

Here you can find a paper to appear in session 7 of the conference about NFT Auctions as a Stackleberg Game



      [fc22.ifca.ai](https://fc22.ifca.ai/program.html)





###



Financial Cryptography and Data Security is a major international forum for research, advanced development, education, exploration, and debate regarding information assurance, with a specific focus on commercial contexts. The conference covers all...










.

& Finally this is about the impact on museums

https://www.mdpi.com/2076-3417/11/21/9931

---

**Hong_Cha** (2022-08-05):

I think most of the price of NFT comes from the publicity.

