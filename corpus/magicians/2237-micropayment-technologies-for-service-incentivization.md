---
source: magicians
topic_id: 2237
title: Micropayment technologies for service incentivization
author: zsfelfoldi
date: "2018-12-17"
category: Magicians > Primordial Soup
tags: [light-client, payments]
url: https://ethereum-magicians.org/t/micropayment-technologies-for-service-incentivization/2237
views: 1571
likes: 3
posts_count: 6
---

# Micropayment technologies for service incentivization

In this thread I would like to open a discussion about efficient micropayment technologies suitable for incentivizing “light client” service (regardless of the actual protocol being used). In order to start the topic I’d like to share the first version of my write-up of what I currently have in mind for realizing LES in-protocol payments:



      [gist.github.com](https://gist.github.com/zsfelfoldi/df66b0226068761a7654d6c2bb2e3ed3)





####



##### les_payment_channel.md



```
## A payment channel protocol for LES incentivization

Author: Zsolt Felfoldi (zsfelfoldi@ethereum.org)

Special thanks to:
- Daniel A. Nagy for the idea of the "stamper" role
- Viktor Tron and the rest of the Swarm team for their work on the SWAP, SWEAR and SWINDLE framework

### Abstract
```

   This file has been truncated. [show original](https://gist.github.com/zsfelfoldi/df66b0226068761a7654d6c2bb2e3ed3)










Please feel free to criticize either the whole idea or just parts of it ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Right now it seems like a good idea to me but I feel that I need more feedback before going further in this direction. Also if you like some other technology or especially if you know about something that is more or less ready to use and would be suitable then this is the right place for it.

## Replies

**shazow** (2018-12-18):

This is interesting!

I’d love to see a draft smart contract for what this would look like. It seems like a fairly complex arrangement but maybe the contract isn’t as bad as I imagine?

Is there a ballpark estimate of what kind of gas fee efficiency we can expect from this kind of model and how it scales?

My biggest concern overall would be the stamper setup. It feels like the logical conclusion of a generalized implementation is that a stamper becomes a fully collateralized relay like a lightning network node. That is, the stamper would need to lock in at least the total value that would be relayed over it as collateral to fully disincentivize cheating (double spend, etc). Especially considering the worst case that the customer could also be the stamper. Does that sound right?

---

**zsfelfoldi** (2018-12-21):

Thanks for the reply! I will shortly give at least some contract function descriptions, I believe it is not as complex as is might sound at first. But first let me reply to the collateralization issue.

Total collateralization is not necessary and also would not be easy to verify because recipients are unable to directly check the total amount of deposits a stamper is assigned to. The idea here is that by cheating you can only buy a lot of LES service really quickly which you just don’t need. As soon as your fraudulent stamper service is caught you lose your deposit. You will definitely be caught during redeem period but probably a lot sooner if the recipients are also sharing their cheques with each other (which they will probably do for another reason too, see the “Redeeming reward” section). So let’s say that 100$ stamper deposit is usually acceptable for recipients. If there are a lot of servers then it is theoretically possible that the cheater could use more than 100$ worth of service at a 100$ cost before being caught but it is highly doubtful that buying basically any amount of service in a short period would be actually so valuable to anyone. Colluding with thousands of clients in order to make it worth the cost would also not work in practice because it would mean that a lot of them would know about the cheating and they could apply for a whistleblower reward.

In conclusion, the sufficiently high stamper deposit would probably be not so high and it is also easy to know if it is not enough. Once a stamper is caught cheating every recipient would instantly know that its deposit was probably not high enough under the given market circumstances and they could all raise their requirement for stamper deposits.

---

**shazow** (2018-12-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zsfelfoldi/48/1697_2.png) zsfelfoldi:

> The idea here is that by cheating you can only buy a lot of LES service really quickly which you just don’t need.

I agree that this limits the practical damage in this specific scenario, but for the sake of argument I’m trying to imagine that this scheme is being used for other things too. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Also, the other side of the question: What is a minimum fee required to sufficiently encourage stampers to exist? I suspect the floor will ultimately set by whatever fees you earn as a Casper staker, as a percentage of your deposit.

We should also write up some back-of-the-envelope estimates for potential host earnings in different scenarios (e.g. say we convert 10% of the network into paying light clients). This will inform what kinds of deposits we could expect from stampers.

---

**zsfelfoldi** (2018-12-27):

> I agree that this limits the practical damage in this specific scenario, but for the sake of argument I’m trying to imagine that this scheme is being used for other things too.

Sure, let’s imagine that ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) I think the main limitation is that such a system without full collateralization cannot be used for buying stuff that you can “consume” quickly or transfer/resell. It may be similarly suitable for incentivization of other protocols too. For higher level applications the “lightning style” multi-hop approach sounds better, especially because the probabilistic behavior is also a serious inconvenience when paying higher amounts.

> Also, the other side of the question: What is a minimum fee required to sufficiently encourage stampers to exist? I suspect the floor will ultimately set by whatever fees you earn as a Casper staker, as a percentage of your deposit.
> We should also write up some back-of-the-envelope estimates for potential host earnings in different scenarios (e.g. say we convert 10% of the network into paying light clients). This will inform what kinds of deposits we could expect from stampers.

First I’ve made some very rough estimates for LES service assuming a big enough network with enough players so that market mechanics can work:

- a home PC can serve about 50-100 clients with minimal capacity (equivalent to free service)
- earning 50-100 USD per month should be enough incentive for many average users to run a light server (almost) 24/7 so the price of a “minimal capacity slot” (MCS) should not be higher than cca 1 USD per month
- having 5 MCSs at different servers ensures a high-quality, high-reliablility connection to the network (for most use cases 2 might be enough)
- 5 USD per month equals 0.7 cents per hour. For a regular user who is not constantly connected this service is definitely cheap enough.
- for 24/7 connected applications the 2-5 USD/month price may still be suitable or alternatively they can go for their own full node. In the future the pricing models can become more sophisticated (giving a discount to those who are really just syncing headers 99% of the time) but we can already say that even with a really simple pricing model there will be demand at 1 USD/MCS/month.

For the price of the stamper service it’s really hard to make a guess at this point but I think there is a good reason to assume that it will work itself out. The main reason for a stamper to exist is that paid servers require them in order to be able to accept payments so stamper service will probably be provided by some of the servers themselves. I would go as far as making the stamper protocol an optional part of the LES server side protocol. Since stamping only requires receiving, signing and sending few hudred bytes packages cca every minute per client-server connection, a PC capable of running LES service can very easily also handle the stamping needs of 10 or even 100 other servers. If there is a stamper for every 10 servers and we accept spending 1% of the revenues on stamping service then the estimated extra revenue one can gain by having a deposit and allowing stamping is 10% of the service revenue or 5-10 USD per month. If we demand 100 USD deposit this sounds perfectly fine but if there will ever be a shortage of stampers at this price, the server to stamper ratio can easily go up to 100 while the server revenue to stamper cost ratio can also raise to a few percents, allowing hudreds of dollars of stamper revenue if necessary (which I really doubt).

Of course starting off from the current state of a non-existent market is a different story but right now a few stampers can easily serve the whole world and I would definitely run one just to be safe, regardless of the revenue ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Also I am not sure about LES service prices at the early stages but it even kind of works almost good enough without any payment and most of the server operators will turn on accepting payments because why not. Some clients will also try paying when they get shitty service for free (which happens a lot) so I guess it will figure itself out somehow.

---

**shazow** (2019-01-02):

Sounds sensible!

My vipnode calculations were similar, I ended up setting the default price at 100 gwei/minute which comes out to about $0.5 USD/mo at current prices for now.

Another thought: If we do the vipnode pool model, then the pool could also act as a stamper. The pool already likely wants to take some fee for operating/existing, so that just increases its utility.

Are there any existing stamper prototypes? Should that be the next step?

