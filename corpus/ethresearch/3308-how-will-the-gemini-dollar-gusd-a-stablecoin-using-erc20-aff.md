---
source: ethresearch
topic_id: 3308
title: How will the Gemini Dollar (GUSD) - a stablecoin using ERC20 - affect the Ethereum mainnet
author: tpmccallum
date: "2018-09-11"
category: Applications
tags: []
url: https://ethresear.ch/t/how-will-the-gemini-dollar-gusd-a-stablecoin-using-erc20-affect-the-ethereum-mainnet/3308
views: 4106
likes: 6
posts_count: 6
---

# How will the Gemini Dollar (GUSD) - a stablecoin using ERC20 - affect the Ethereum mainnet

I am curious to learn how the Gemini Dollar (GUSD) might affect the Ethereum mainchain. This article by Cameron Winklevoss [1] reads “… you will be able to convert U.S. dollars in your Gemini account into Gemini dollars and withdraw them to an Ethereum address you specify”.

I have looked at the GUSD token contract on etherscan [2]. Activity seems quiet at present (63 transfers between 28 holders). It seems that there are 100, 000 GUSDs issued at present [3].

I do not understand how this actually works. For example:

- Does GUSD just share the Ethereum address space?
- If GUSD takes off from a transaction throughput perspective, will calls to the GUSD token contract be “zero ETH transactions”? I see that the smart contract’s code is available at etherscan [4].
- Will this activity choke the network like we have seen in the past?

More questions than answers here ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) Any information will be appreciated.

[1] https://medium.com/gemini/gemini-launches-the-gemini-dollar-62787f963fb4

[2] https://etherscan.io/token/0x056fd409e1d7a124bd7017459dfea2f387b6d5cd

[3] https://gemini.com/wp-content/themes/gemini/assets/img/dollar/gemini-dollar-examination-report-09-09-18.pdf

[4] https://etherscan.io/address/0x056fd409e1d7a124bd7017459dfea2f387b6d5cd#code

## Replies

**ZenChain** (2018-09-12):

From some quick reading the Gemini Dollar seems like it will operate almost identically to TrueUSD (https://etherscan.io/token/0x8dd5fbce2f6a956c3022ba3663759011dd51e73e). It’s basically a standard token that is tied by its mint/burn operations to the USD balance of its associated bank accounts. The correlation doesn’t seem to be directly tied to anything on the blockchain itself, but rather the reputation/trust of the system and its auditors, though at least in this case the Winkevoss twins and Gemini are considered rather well respected, at least compared to many others in this space. To try and address your questions directly:

- GUSD looks like it will operate as a standard token
- GUSD/ETH is likely mostly for centralized exchanges (similar to USDTether(Omni blockchain), and TrueUSD on Ethereum). MakerDao’s DAI is the one stablecoin that is used often on decentralized exchanges, though its mechanics are significantly different than the others. My guess is most the volume for GUSD will be on the Gemini exchange and any of their close partners. Most onchain transfers will be between exchanges and likely not between individuals or to/from personal wallets that often
- They will be standard token transactions, with the # tokens moving from one wallet to another plus the network ETH gas fee added on
- I highly doubt it will cause much network transaction, since with stablecoins the majority of their use is within centralized exchanges by higher volume traders. Furthermore, I’d expect its volume to be lower than that of TrueUSD, simply because the ‘partner/sponsor’ exchange for TrueUSD is Bittrex, which has about double the volume on it of Gemini. My best guess would be itll push +/-50% of the onchain transaction volume of TrueUSD (https://etherscan.io/token/0x8dd5fbce2f6a956c3022ba3663759011dd51e73e) in the short-mid term.

Some day in the future we may see mainstream adoption of a stablecoin with heavy onchain transactions for use in payments, but as of right now these are 99% trading tools for use on exchanges.

---

**tpmccallum** (2018-09-12):

Thank you. This is very interesting! I spent some time today analysing the Gemini ERC20 token smart contracts (creating diagrams to illustrate inheritance and so forth). I wrote a quick GitHub page [1], complete with diagrams, to assist in my understanding. It seems that Gemini are able to facilitate upgradeable smart contract logic by having the equivalent of pure virtual functions on the public facing ERC20Proxy contract, which are then actually implemented in the ERC20Impl contract. They also use Solidity Modifiers extensively to ensure that the smart contract functions are exclusively executed by the appropriate custodian or calling contract. Please let me know if I missed anything in the GitHub write up.

[1] https://github.com/CyberMiles/tim-research/blob/master/gemini_dollar/gemini_dollar.asciidoc

---

**ZenChain** (2018-09-13):

I’d seen a few Twitter/Reddit comments regarding GUSD, and particularly about the upgradeable custodian, but your report is by far the most comprehensive, and fills in a few blanks I had when replying to your initial post ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=9)

It does seem a number of people dislike the changeable custodian from a security and decentralization perspective, but I think it’s more a matter of a lack of awareness of just how common these functions are in many token contracts - especially for stable coins and others whose model requires burn/mint/freeze (eg those working on interoperability). It isnt nearly as comprehensive or detailed as your page, but we put together a little chart for some of the more prominent tokens and what functions the do or don’t have, which I’ve linked below for your reference.

https://monitorchain.com/wp-content/uploads/2018/09/ERC_Token_Functions.xlsx

---

**tpmccallum** (2018-09-14):

Hi,

Thanks again, your chart is great.

I noticed a comprehensive article [1] on smart contract upgrade solutions which you might find very interesting.

Chat soon

Tim

[1] https://blog.trailofbits.com/2018/09/05/contract-upgrade-anti-patterns/

---

**MaverickChow** (2018-09-20):

When it comes to stablecoin, I think the most important point to discuss is the **sustainability** of such stablecoin indefinitely regardless of market condition, i.e. maintaining stable value over a very long period of volatile time. The way I see stablecoin is just another market counterparty that takes the other side of our buy/sell orders. During a severe bear market, the stablecoin takes the biggest hit by absorbing all the trading losses that a stablecoin holder would have incurred if he didn’t hold any stablecoin at the market peak. How long can such stablecoin takes the market beating over and over again before giving way and fail? The only situation that I know of where such stablecoin can even prosper is if a majority of the market participants remain irrational and buy-high-sell-low repeatedly.

