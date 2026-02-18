---
source: ethresearch
topic_id: 3301
title: POS @ Low USD value of ETH?
author: schone
date: "2018-09-10"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/pos-low-usd-value-of-eth/3301
views: 2681
likes: 6
posts_count: 14
---

# POS @ Low USD value of ETH?

How does POS protected against an attack trying to mine a new chain up to the last finality block, where ETH values are < $10? (Making it practical for a decently wealthy investor to change history)

## Replies

**DB** (2018-09-10):

The price of ETH is irrelevant. As long as the attacker is unable to get a majority, he will get slashed again and again for not following the rules (or just get paid like everybody else for following it). If you claim that getting the needed (2/3?) majority is easier with low ETH prices, that mainly depends on the size of the staked pool. If it is a significant fraction of ETH, an attacker won’t be able to buy something similar without pricing himself out.

Finally, if a ~99% protocol is adapted, that problem will completely go away. https://vitalik.ca/general/2018/08/07/99_fault_tolerant.html

---

**schone** (2018-09-11):

What is ‘significant fraction of ETH’? I see in the current proposals the number 10M ETH being thrown around.  At prices of less than 10 USD, it shouldn’t be too hard for any rogue, decently capitalized operator to achieve holding that amount.  Is that 10M number changeable without a hard fork?

---

**MaverickChow** (2018-09-11):

I think the price of ETH will play a very significant role in security of the network. The price is not irrelevant, but rather less relevant only if an attacker cannot afford to have 100% control. Otherwise, assume if the price of ETH is close to 0 that any attacker can spend only ~ USD 0 to own all the ETH out there, what would be the possibility of this attacker becoming the dominant sole validator out there? And if the possibility is close to 100%, what chance does this attacker have in tampering every transacted data? I think the market cap of ETH needs to at least be as high as possible (minimally, total worth of digitized assets / % fault tolerance) for maximum security when PoS comes online. I speculate all stakeholders will have vested interests to see a much higher price for network security.

---

**adamskrodzki** (2018-09-11):

I’m not an expert on PoS, but to my understanding

Even if attacker have 2/3 of staked pool It is relatively easy to make a fork where he will be slashed

Simply like with ETH and ETC there will be coexisting two concurrent version of histories, one where attacker got slashed and one where everybody else.

That’s important keep in mind that if attacker manage to get 2/3 of a stake there is still a lot of eth burned, just now this are good guys who are burning.

Therefore I believe it will not be hard to push that king of fork forward (It will get social support). Also the fact that In a version

of history where attacker got slashed total supply of ETH will be lower than in a version of history where attack succeeded will help (all people who mind only their own business and value of their own eth will likely support notion to slash the attacker, since under lower total supply their ETH will be worth more )

And after a fork attacker will be 7M ETH poorer. I believe 7M ETH even with low price quite enought to cover costs of a fork.

And do not forget that price of ETH is a function of utility. If eth will cost 1 USD then that means that Ethereum network become useless and nobody cares anyway.

---

**DB** (2018-09-11):

What you call price is the cost of buying a single ETH right now. The market is highly liquid, so buying 1000 won’t change it much. However, when you start talking about buying a significant fraction of the market, current price is no indication to the cost (does anyone know what % of ETH is even at exchanges?).

Also, as long as the selection of validators is not compromised, having a 2/3 majority of stakes only gives one the power to manipulate 2/3 of the blocks, not much in therms history re-writing.

---

**MaverickChow** (2018-09-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/db/48/1527_2.png) DB:

> current price is no indication to the cost

What exactly do you mean by that? And how are you sure the “highly liquid” market is not mostly due to wash trading? Personally if I know the price, I can infer the cost through price * total supply, assuming if I am an attacker that plans to control the chain. I don’t need to know what % of ETH is at the exchanges. Assuming the price is USD 0, I can buy up all the available supply at the exchanges at USD 0 and then put a bid for USD 0.2 to entice hidden sellers. ETH holders that do not stake have the incentive to sell to me. ETH holders that staked also have the same incentive for a quick gain.

The main point that I want to make is the price plays a significant role in security. In the future when blockchain become a mainstream daily life thing, we will not be dealing with rascals that try to buy 1000 ETH, but potentially anyone with enough financial power and influence to take major control, if not full control, whenever the opportunity arises.

The true incentive for full control of network is not really to tamper with any petty amount of value involved per block. That will not be the focus of a serious attacker. And by having the right price of ETH will easily deter the motivation. Maybe you do not see what I see, thus the disagreement, but that is okay with me.

---

**DB** (2018-09-11):

First of all, the price is never zero. It can get close, but never reach zero. I’ll personally buy all the Ether out there before that happens.

Let’s say I want to buy control of company X. I know the current stock price, so I calculate how much it will cost me. After buying a few shares, the price goes up, I buy more, it goes up some more. I wait, and buy more… At some point, I see I cannot get many more stocks despite the price going through the roof. This is because 60% sit with investors that don’t even check the market and will never sell, and another 15% sit with ETF that cannot sell a specific stock, but actually have to buy more, so the ETF remains faithful to the market. Same thing with ETH. For example, I just checked and bitstamp, one of the larger traders in Europe (but smaller than some Asian and American exchanges) currently has 21K ETH for sale for USD. This is 0.00021 of the total supply. The first ones you can buy at ~190$, but if you’ll buy 5300 (or 0.0053%), for the last one you will be paying 225 (that’s as far as the graph goes).  Now imagine buying 20%…

---

**MaverickChow** (2018-09-11):

I infer the price of USD 0 merely as a simplistic example to help give a better understanding on the main idea. Not really to say that the price is really zero or if that is really the main point.

What you elaborated to me is generally a trading nature of **market microstructure** and irrelevant to understanding the main idea. Understanding the market microstructure does not help in valuing ETH correctly. You quoted the current price but that does not help to counter some arguments made by others that the price of ETH is inevitable to go to zero. You said the price is never zero but that is based on which fundamental analysis? I am saying the price will not go to zero for a very different reason totally unrelated to trading.

---

**DB** (2018-09-11):

The only claim I’m making is that current price of ETH gives no indication to the amount of money needed to gain a majority in PoS, thus jeopardizing it.

No one knows where the price will go, and this is probably the wrong place to discuss hypothesis about it. I gave you a strong assurance it will not be zero, as there are players able and willing to buy it all before zero.

---

**MihailoBjelic** (2018-09-12):

Hi [@schone](/u/schone) ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

The answer to your question is quite simple: If ETH is <$10/close to zero, that means that the level of activity (dApps/projects) on Ethereum is very low/close to zero. Also, if the level of activity is very high, it’s really hard to imagine ETH being that low. In either way, we don’t have to worry about the price, cryptoeconomics is taking care of that.

Hope this helped. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**toms119** (2018-09-12):

Agreed with DB.

It would be close to impossible from a market dynamics standpoint to acquire that much control in the open market.

The slippage, (well opposite of slippage) is the amount the value of ETH goes up with each purchase. Has nothing to do with supply, its the value buyers and sellers place on the value. If there are more buyers, prices go up.

The multiplier on the increase in price as the float dwindles is impossible to know, but the point is to assume that price goes up as free float goes down.

Theres also the issue of why would someone spend an exorbitant amount of money, to fork the chain and lose the credibility/devs/founders who can just fork him/her off and make them due the process again which would be 2x as expensive since its happening twice now.

Just a thought,

---

**MaverickChow** (2018-09-12):

I **speculate** that if a network is going to “host” various assets on top of it, then the currency used to secure such network will need to reach the level of valuation that is at least equal to the total value of the assets traded on top if it, thus the main motivation of why someone would spend an exorbitant amount of money for control. For example, if a network is “hosting” a group of assets worth USD 1 quadrillion in value and the currency backing such network is just USD 20 billion, then anyone that desire to tamper with the ownership registry of the USD 1 quadrillion asset worth would spend at least USD 20 billion to tamper the network for a potential profit of USD 1 quadrillion - USD 20 billion = USD 999.98 trillion. The potential return of such tampering is worth almost 50,000x more than the “exorbitant” USD 20 billion market cap of the currency securing it. You may say the market depth/order book will make total acquisition impossible/expensive but as long as the total valuation of the currency securing the network does not match the total valuation of the assets “hosted” on top of such network, then the monetary incentive will always be present. The incentive may be USD 999.98 trillion. It may be USD 99.99 trillion. Or USD 9.99 trillion. Regardless, the best level of valuation for maximum security is when the price of the currency involved is USD 1 quadrillion or above, where the incentive would be either zero or negative. And the best currency used to secure the network is the native currency itself. Certainly not some 3rd-party coins that anyone can freely mint out of thin air and then manipulate up to significance, which if used to secure the network, would bring injustice to all the commercial assets “hosted” on top of it, thus invalidates Jeremy Rubin’s argument for BuzzwordCoin. Whether the network will be “hosting” USD 1 quadrillion worth of assets is not the main point. The main point is the valuation of the native currency should always adjust to be at least equal to the total value of all asset “hosted” on top of it. And if the potential is there, then such valuation should come with a huge premium.

I strongly believe it is very unwise and foolish to infer the intrinsic value of a currency based on the demand and supply of market trading activities as if such activities driven by human emotions really mean anything substantial from a non-trading standpoint. ICOs are not the real deal no matter the selling pressure as unintentionally fud-ed by others. Neither is the demand and supply of short-term trading activities as suggested by some members here, in my opinion.

All these are just my personal analysis.

*typos corrected

---

**MaverickChow** (2018-09-13):

Another extension I wish to make is assuming the fault tolerance is 51%, then securing the network optimally would need the intrinsic/native currency’s valuation to be worth the total value of all the assets “hosted” on top of it / 0.51. For example, of a network “hosts” USD 1 quadrillion worth of assets (assuming ~100% share of market capture) with 51% fault tolerance, then the intrinsic currency needs to be valuated at 1 quadrillion / 0.51 = 1.96 quadrillion market cap to maximally deter all incentive for malicious intent. 99% fault tolerance would need 1 / 0.99 = 1.01 quadrillion.

