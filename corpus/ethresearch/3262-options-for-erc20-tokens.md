---
source: ethresearch
topic_id: 3262
title: Options for ERC20 tokens
author: adamskrodzki
date: "2018-09-07"
category: Applications
tags: []
url: https://ethresear.ch/t/options-for-erc20-tokens/3262
views: 2384
likes: 5
posts_count: 12
---

# Options for ERC20 tokens

Is there any onchain solution for Options trading?

By Option I mean:



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Option_(finance))





###

 In finance, an option is a contract which conveys to its owner, the holder, the right, but not the obligation, to buy or sell a specific quantity of an underlying asset or instrument at a specified strike price on or before a specified date, depending on the style of the option.
 Options are typically acquired by purchase, as a form of compensation, or as part of a complex financial transaction. Thus, they are also a form of asset (or contingent liability) and have a valuation that may depend ...










That seems possible with smart contracts only. Now, since DAI is available You can Imagine such options priced also in USD.

I’m aware of Augur, but to my knowledge it has off chain dispute resolution.

I’m looking for opensource full on-chain solution

Lets say its 01.09.2018

Lets consider Alice who ownes 1000 ETH and want to insure herself against it’s price loss below 200 USD until 1.11.2018 and is willing to pay 10ETH for such insurance

Lets consider Bob who is bully about ETH would gladly earn some and has 200 000 USD to risk.

1. Bob buys 200 000 DAI
2. Alice creates SC and deposit 10ETH, smart contract allows anyone to claim that 10ETH if only he/she is willing to deposit 200 000 DAI untill 1.11.2018
3. Bob deposit DAI and claims ETH
4. Alice has right (but not obligation) anytime before 1.11.2018 to send ETH to SC and get DAI in return in exchange rate of 1ETH:200DAI
5. If Alice do so All ETH sended to SC goes to Bob

That would secure Alice against ETH value loss for a period 1.09.2018-1.11.2018

And if ETH stay above 200 DAI/ETH   taking DAI deposit by Alice would be irrational and Bob will not get harmed because he would be able to buy back any DAI he lost by ETH he aquired

That SC sounds like Long Put for Alice and Short Put for Bob

Is anyone here aware of such onchain solution existing or in development?

This one above was only an example. In practice that kind of tool can be used to stabilize price of any asset against any other.

As far as I know commodities who has Options market are more stable in price that those who does not one.

## Replies

**flygoing** (2018-09-07):

We actually developed something very similar to what you’re talking about at Optionality, with our beta available on Kovan at [dev.optionality.io](http://dev.optionality.io). Here’s exactly what the flow is like on our platform:

1. Bob wants to create 10 PUT options with expiration of 1.11.2018 and a strike price of 200 DAI per ETH. He deposits the 2000 DAI into our contract, and our contract creates 10 ETH-DAI-200-1.11.2018-PUT ERC20 tokens.
2. Bob is then free to sell these tokens on our market (dutch exchange auction) or on any other exchange that supports ERC20 tokens.
3. Alice can buy those 10 ETH-DAI-200-1.11.2018-PUT tokens from Bob. If ETH is below 200, Alice would exercise those 10 options and send 10 ETH to the contract to receive 2000 DAI, effectively profiting from the devaluation of ETH.
4. Bob would then claim the 2000 DAI Alice paid from the contract.

It’s slightly different, since all options of the same pair/expiration/strike/call-put are fungible, the amount that the person that created the options initially gets when someone exercises is based on the percentage of those tokens they created. So if there are 100 of those ETH-DAI-200-1.11.2018-PUT tokens when Alice exercised them, then Bob would only get 200 DAI since he owns 10% of the market. the other 90% would be split between the rest of the token creators.

---

**kowalski** (2018-09-07):

[@adamskrodzki](/u/adamskrodzki) I think options are failry easy to accomplish by creating a wrapper on top of 0x protocol.

Here is how this could work:

1. Trader selling an option signs an 0x order and puts it’s signature onchain into the Option contract along with the parameters defining conditions under which it can be exercised like:

- address allowed to execute it
- the date contraints on when it can be executed
- or generic style (American/European/etc)

1. The order is done with uniqueTakerAddress set to address(OptionContract), so that no third party would be allowed to swoop in and fill the order.
2. The buyer of the options is given the signature of the order.
3. When option holder  wants to execute the option he calls OptionsContract.exercise method passing the signature. OptionContract validates that all conditions are met and if it does it performs operations like (pseudocode)

```auto
ERC20(buyTokenAddress).transferFrom(buyerAddress, address(this), buyAmount)
Exchange0x.fill(

)
ERC20(sellTokenAddress).transfer(buyerAddress, sellAmount)
```

That was the happy path. Of course the trader selling the option may choose to cheat when he sees that the market moved in incorrect direction. He could from example cancel allowance on `Exchange0x` contract or remove `sellToken` balance from his wallet. To circumvent this I think the system would need to require putting colateral from trader generating option. Colateral would be returned when holder of option exercises it or reclaimed by the trader after the option expires.

---

**adamskrodzki** (2018-09-07):

Interesting system,

two questions:

1. If Alice exercise option, who gets the ETH? Does it automatically flows to Bob ?
2. What happens on expiration ?

---

**flygoing** (2018-09-07):

1. If Alice exercises the PUT options that Bob created, then the ETH Alice is selling via the option is divided among the creators if the options. The example I gave in my last comment is about this “if there are 100 of those ETH-DAI-200-1.11.2018-PUT tokens when Alice exercised them, then Bob would only get 200 DAI since he owns 10% of the market. the other 90% would be split between the rest of the token creators.”
That part is a little confusing, but it’s so that the options can be fungible within their parameters. Essentially, creators of options (the people locking up the token to create them) get a share of an exercise equal to the percentage of the outstanding options they created. So if there are 80 options at block 10, and Bob created 20 more in block 11, sold them to Alice in block 12, and Alice exercises them in block 13, Bob would get 20% of Alice’s exercise amount because he had 20% of the market at the time.
2. Once the expiration date is hit, the options themselves expire and can’t be exercised. Whoever created the options by locking up their tokens can withdraw the tokens they locked up (minus the ones that were taken by people exercising options).

---

**adamskrodzki** (2018-09-07):

What is benefit of using 0x over writing a smart contracts?

---

**adamskrodzki** (2018-09-07):

Do You have any repository? Or documentation to analize?

---

**ldct** (2018-09-07):

I worked on exactly that style of options (ETH-DAI swap option with the right lasting from now until some point in the future) for ETHWaterloo at https://github.com/IIIIllllIIIIllllIIIIllllIIIIllllIIIIll/options

Some interesting observations from it:

1. This style of fully collateralized option is very capital-intensive. In practice we know that real-world option underwriters do not really fully collateralize their options; it’s very unlikely that all the obligations that Goldman Sachs are saddled with will be exercised in such a way that they lose more than their company’s capital base. There are regulations that quantify risk and basically force underwriters not to under-collateralize too much. How do we do this in smart contracts?
2. One thing I tried to do is represent the option itself as an ERC20 token, allowing compound options. In general this makes the capital intensiveness even worse.
3. The call/put distinction doesn’t really make sense in this case IMO; there’s just swap options that define two roles, the underwriter and the option holder
4. Short sells of options still can’t be done fully trustlessly
5. There’s a cool functional pearl about financial contract in general: https://www.cs.tufts.edu/~nr/cs257/archive/simon-peyton-jones/contracts.pdf

---

**kowalski** (2018-09-07):

Major part of 0x is a smart contract. The rest is library code to make calls to smart contract, generate  signatures and validate orders.

So I understand your question more like “What is benefit of using open source library than creating own solution?”. I guess the benefit is that you can save a lot of development time and have less chance of introducing bugs.

---

**adamskrodzki** (2018-09-08):

Well,

I doubt 0x was designed for that one purpose so I doubt it does it optimally. To use comparition well known in Ethereum community Yes Smartphone is usually superior to Swiss knife, but not when all You want to do is open a bottle of beer.

---

**adamskrodzki** (2018-09-09):

Have it ever turns out into production?

---

**glowkeeper** (2018-09-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/adamskrodzki/48/1910_2.png) adamskrodzki:

> I doubt 0x was designed for that one purpose so I doubt it does it optimally.

You get an answer, yet your first instinct is to doubt that answer? Rather than immediately casting *doubt*, how about looking a bit further into 0x, then reporting back? I’m about to start 0x development, so I’m interested in what you find ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

