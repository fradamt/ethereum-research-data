---
source: ethresearch
topic_id: 6471
title: "Hardware-notes: A physical asset backed by cryptocurrancy"
author: barryWhiteHat
date: "2019-11-20"
category: Applications
tags: []
url: https://ethresear.ch/t/hardware-notes-a-physical-asset-backed-by-cryptocurrancy/6471
views: 1878
likes: 6
posts_count: 5
---

# Hardware-notes: A physical asset backed by cryptocurrancy

## Intro

How do we give cryptocurrancy to people who don’t have computers ( or smart phones)

We need a way to sign transactions. The cheapest way is NFC cards which cost between ~1.5 USD. With discounts for bulk purchases. NFC cards is a kind of trusted hardware. That are used everyday as debit cards and metro cards.

The fact that this hardware is ubiquitous allows us to benefit from economies of scale and produce these cards at very low costs.

## Previous work

Using trusted hardware for physical payments has been done before.

1. Opendime

Locks the private key inside a hardware wallet. The funds can only be spent if you break an anti-tamper strip. These hardware wallets are not reusable once they have been withdrawn. Its also prohibitively expensive to use them for lower price transactions as the hardware currently costs ~ 45 USD

1. Kong

Is a independent currency that is locked inside the kong hardware wallets for a a period on the order of years.

Here we propose hardware-notes. We harden NFC cards with a smart contract so that it can become a reliable medium of exchange in areas with intermittent network connection. Where the physical hardware is passed. And possession of the hardware-note is required to withdraw the cryptocurrancy that is deposited to that card.

We decentralize the role of hardware manufacturer and allow users to accept any hardware that they deem trustworthy. We also allow erc20 support so anyone can create any currency inside these cards.

## Smart contract

### Manufacturer Card Registry

We create a smart contract that a manufacturer lists the cards they have created.

The public key of each card is stored in a merkel tree where a leaf is the public key. The private key is locked inside the card.

### Deposit

A smart contract allows users to deposit cryptocurrancy to any card.

They send a transaction with

`deposit (address erc20, uint amount, uint withdraw_delay             ,address card_pub_key)`

A single card can have multiple currencies with various denominations.

### Withdraw

There is a two step withdrawal process.

Both steps the withdrawer proves possession of the hardware-note by signing one of the last 256 block hashes.

#### Signal Withdraw

First the user signals they want to withdraw.

`signal_withdraw ( bytes32 blockhash, address pub_key)`

The first step is followed by a wait period. The wait period is variable. It is defined when a deposit as `withdraw_delay` was made to that hardware-note.

#### Execute Withdraw

After the wait period a user can withdraw the funds by again signing one of the last 256 block hashes.

The wait period is included here to allow people to accept payments if they are operating with an outdated state. As long as their `state.age < coin.withdraw_delay` they can be sure that they will at least be able to call `execute_withdraw` for the coin they receive.

## Spending Hardware-notes

When deciding on a hardware-note value the app checks

1. That the card has been issued by made by a reputable manufacturer.
2. The currency and amount that the card holds.
3. That the state the app is working with is less than the withdraw delay for that coin.

If all of these are true the merchant can accept the coin for its defined value.

## State Updates

Every once in a while a merchant will need to update their state. This means going online and downloading a list of coins that have been

1. Withdrawn
2. Are in the process of being withdrawn
3. Have been deposited
4. They also need to download the list of new cards from their trusted manufacturers (this can happen much more rarely)

The frequency of state updates required is equal to the min `withdraw_delay` that they want to accept. So this can be tuned by the merchant who can refuse to accept a card with a short `withdraw_delay`

## Example usecase

### Simple Payment

1. I decide to move to country X where the annual inflation rate is 10,000 %
2. I buy a bunch of empty hardware-notes from the most popular manufacturer that merchants accept in country X.
3. I load one hardware-notes with 5 USD the other with 15 USD worth of a stable coin. Both with a 14 day withdraw_delay
4. I arrive and go to a shop in the country.
5. I buy 10 USD worth of food.
6. I pay with the 15 USD hardware-note to the merchant.
7. The merchant checks the hardware-note with the app and agrees to accept it with 15 USD value.
8. The merchant returns to me a 5 USD hardware-note or 5 USD in local currency.

Here we assume the merchant has updated their state since I deposited into my crypto-currancy into the hardware-note.

### Merchant

1. I am a fruit seller in country X.
2. I sell fruit every day and had to accept payment in currency that experiences 10000% inflation
3. I cannot accept hardware-notes in my business because my average transaction size is less than 1 USD where it is uneconomical to create hardware-notes for such a small denominations.
4. So I operate in the local currency as soon as I have earned 10 USD I exchange it to a hardware-note.
5. I use hardware-notes to buy my supplies.

## Attacks

1. NFT war driving
If i get close to someone while they hold these hardware-notes i can steal from them. I can ask the hardware-notes to sign the latest hash. Broadcast it to perform signal_withdraw

Then `withdraw_delay` seconds later I can find that same person again and calling `execute_withdraw`.

This attack is mitigated by

- Having more than one hardware-notes in my pocket. Its really hard to read a single one
- Holding my hardware-notes in a Faraday cage, tin foil package

1. Lying merchant

When I try and spend my hardware-notes a merchant is always able to lie to me and say that the balance is not what I claimed it to be.

I can overcome this by going to another merchant and checking again with them.

In smaller communities this attack is not possible as lieing merchants will soon be found out. In bigger communities people will hopefully have a choice of who to transact with.

But we assume there is a single honest check balance person available.

1. Withdraw instead of check balance

Instead of checking a users balance a merchant can begin the withdraw period for that user. They would then need to reject the coin and re-scan it again after `delay` seconds in order to complete the withdraw.

To overcome this we can add a long time delay for the `withdraw` function on the hardware-notes.

For example a simple check balance can take 1 second. In order to perform a withdraw we could add a delay this to 10 seconds.

If we build a strong expectation that a user only needs to scan their coin for 1 second to check its balance then we can avoid these kinds of attacks.

1. Rouge manufacturer

A manufacturer claims to have locked a given public key in a hardware-note but in fact they have not and this public key is in the clear.

The manufacturer will then be able to double spend the funds held on this hardware-notes.

You have to trust the hardware manufacturer at the time of hardware-notes manufacture.

We hope that an ecosystem of hardware manufacturers exist to allow this so that users have an option on which manufacturers to trust.

Its important to note that this is the same with all hardware that holds crypto-currancyies. You have to trust the hardware you are using. And there is no way to economically validate that your hardware is correct.

## Conclusions

We allow creation of physical crypto-currency assets with variable timeouts. This can allow use of crypto currency in areas that do not have consistent internet connection.

This reduces the time that you need to be online which will allow communities without reliable internet / electricity to use crypto currencies.

Creation of coins is completely open so any actor can create currencies and use this infrastructure to transact with them. These currencies can be converted back to digital form after waiting a delay period which means you can move between the physical and cryptocurrency world.

## Replies

**ligi** (2019-12-03):

Thanks for the initiative.

I wonder if (part of) the [Keycard](https://keycard.tech/) code can be used for the NFC-Side. I Will ping the KeyCard team as they might be interested in this.

They are cheaper than OpenDime - but still not yet in the 1.5USD range you mention in this post. But they are very durable and the new cash-feature (as we do not want to deal with PIN/PUK/pairing pwd’s here) might be useful for this use-case.

I really like the idea - the only problem I see currently is the price of the cards. As let’s say I want to buy food for 5USD with a card that is loaded with 5USD I would effecively pay 6.5USD. I think there could be a scheme that mitigates this - e.g. the value of the card is added to the value that is stored on the card. But a problem I see there is that these cards will most likely get cheaper in the future when they get produced in bigger volumes.

Anyway - really happy to add such a feature to WallETH and iterate on the idea this way.

I have seen Kong at Devcon 5 - also liked it - but somehow I do not trust the long-livety of these. I think the ICs will fall of the flexible PCB at some point. Does anyone buy a Kong there and can say more aout this?

Anyway - I am carrying the KeyCards on my body for a while now and they hold fine as expected - but they also have no exposed IC’s like kong.

Let’s move this forward!

---

**barryWhiteHat** (2019-12-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/ligi/48/784_2.png) ligi:

> They are cheaper than OpenDime - but still not yet in the 1.5USD range you mention in this post. But they are very durable and the new cash-feature (as we do not want to deal with PIN/PUK/pairing pwd’s here) might be useful for this use-case.

Yeah i think that 1.5 might be a bit low. Its from searching on alibaba but probably not the latest version of javacard which i think its required.

> I really like the idea - the only problem I see currently is the price of the cards. As let’s say I want to buy food for 5USD with a card that is loaded with 5USD I would effecively pay 6.5USD. I think there could be a scheme that mitigates this - e.g. the value of the card is added to the value that is stored on the card. But a problem I see there is that these cards will most likely get cheaper in the future when they get produced in bigger volumes.

1. So assuming that new cards come along your 6.5 USD card will get deflated to 5USD. So that is inflation of  13 % considering that alot of countries have inflation order of magnatiude more its probably a risk alot of these people would be happy to take.
2. We could potentially use use CDAI with gives 4% interest would reduce this to 9%.
3. We could also have slightly higher value cards at first and then reduce it.
“bad money drives out good”

> Anyway - really happy to add such a feature to WallETH and iterate on the idea this way.

Cool let me push the smart contract side of things. Hopefully we can use keycard for the hardware and then we are ready to do some experiments ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

---

**ligi** (2019-12-04):

Thanks for the follow up!

Would love to find alternatives to using interest to compensate for the price of the cards as I feel quite negative about interest (especially after the [deVcon talk by brewster kahle](https://www.youtube.com/watch?v=AyaWFicSihE)) as it is moving money from the poor to the rich.

Perhaps advertisements on these cards might be a solution? Yea not a big fan of ads also - but I think they are less bad than interest. Or service providers were if you turn in the card you get back the value of the card (+the value on the card) - sure these providers need to take a fee and can also not give back the full value of the card as it is getting less over time and they need to cover from this - but perhaps we can get the amount down this way?

Anyway - this should not block the experiment and let’s not overengineer  it with such complications in the beginning. That said perhaps ad’s on the card can also be a nice way to bootstrap the whole thing (someone needs to produce these - ideally in big amounts so the cards get cheaper)

Also wondering if such a machine:

https://www.alibaba.com/product-detail/Tenet-TTL-RS232-Card-dispensing-unit_60511544736.html?spm=a2700.7724857.normalList.30.414d72cbNIGFLc

could be a nice way to distribute them. This could be combined with a coin-counter an other payment method and these machines would hand out the “Notes” then.

---

**barryWhiteHat** (2019-12-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/ligi/48/784_2.png) ligi:

> Would love to find alternatives to using interest to compensate for the price of the cards as I feel quite negative about interest (especially after the deVcon talk by brewster kahle ) as it is moving money from the poor to the rich.

Oh i was not suggesting that the hardware note owners would pay interest to the card provider. I was thinking that the hardware note could contain some interest returning coin like cdai. So that would offset the reduction in value of their card. So the hardware note owners would get paid interest for holding a certain currency.

