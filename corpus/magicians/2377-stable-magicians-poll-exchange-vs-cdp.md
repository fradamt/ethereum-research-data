---
source: magicians
topic_id: 2377
title: "Stable Magicians (POLL: exchange vs. CDP)"
author: ligi
date: "2019-01-10"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/stable-magicians-poll-exchange-vs-cdp/2377
views: 2334
likes: 20
posts_count: 35
---

# Stable Magicians (POLL: exchange vs. CDP)

I want to have some more eye-balls on this [emerging discussion on github.](https://github.com/ethereum-magicians/scrolls/issues/55)

Really like the movement from ETH->DAI for covering costs of events. (Stable Magicians FTW) - now there are 2 main ways to convert ETH to DAI

1. direct exchange ETH->DAI (e.g. via oasis)
2. a CDP

I would prefer #1 - wonder what the rest of the magicians think.

- direct exchange
- CDP

0
voters

## Replies

**boris** (2019-01-10):

Hey [@ligi](/u/ligi) as I said in the Github issue – that thread is about finding a volunteer. I don’t think we need a vote here.

The “what we are trying to solve” context is:

- we are asking for people to pay ETH for tickets to next Council
- there will be expenses in fiat for catering
- someone will need to pay fiat, and get re-imbursed in crypto
- turning ETH into DAI (edited!) as it is accepted means that we can be sure we have the right amount to cover the catering expenses
- at the same time, the ECF sponsorship of 2KEU (that we have listed in the budget) should also get turned into DAI now
- any other sponsors that pay in crypto should also be converted to cover hard fiat costs

A longer term issue is what to do with the rest of the (very small) EthMagicians treasury. I think keeping portions of it in DAI makes sense – but I personally would like to find more people who will accept ETH directly.

This process – of turning ETH into DAI and helping to manage the treasury – is what I want to see a volunteer help with. How to do it? I don’t care either way – someone with more experience can advise us.

I hope that helps scope what is needed.

---

**ChainSafe** (2019-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> This process – of turning ETH into DAI and helping to manage the treasury – is what I want to see a volunteer help with. How to do it? I don’t care either way – someone with more experience can advise us.

I would love to help with this as I mentioned on github. I think it is extremely important not to speculate with funds that have specific needs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> but I personally would like to find more people who will accept ETH directly.

I think this moving forward is the most important step to take so that we are able to avoid off ramps from ETH or DAI donations.

---

**ligi** (2019-01-10):

Great to see we are on the same page here. My reason to start this poll was that CDP was mentioned in the initial issue text and one potential volunteer mentioned he has experiences with CDP’s. So I thought it might go in this direction and hence I wanted to signal soon that I think CDP’s are the wrong tool for *this* job and also get a feeling how the rest is thinking about this.

---

**Flash** (2019-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> turning DAI into ETH as it is accepted means that we can be sure we have the right amount to cover the catering expenses

I think you mean ETH => DAI here for the allocated catering funds to be fixed.

I’m not on the same page as the previous two posters. A CDP allows us to generate DAI on the fly without worrying about fees, slippage or managing multiple transactions. Personally I think it makes sense to generate them directly rather than have to rely on someone else to stabilise the funds.

The other benefit would be that anyone can see and repay the CDP’s debt or add collateral as a way to support whatever the funds are being used for (you could theoretically use this model to allow the community to vote on which part of an event they want their money to go to).

I like the simplicity, transparency and security that come with using a CDP, but honestly, it won’t make a huge difference either way.

EDIT: I should probably note that we would need to safely collateralize the CDP until it is payed back, you can’t simply convert everything into DAI.

---

**boris** (2019-01-10):

Awesome! Learning so much here, thank you [@Flash](/u/flash)!

And yes, ETH to DAI – I edited my comment.

So, feels like the two options are:

### (1) Convert ETH to DAI

On a weekly basis / when some amount of ETH from ticket sales have accumulated, do a direct exchange using Oasis[^multisig]. Exchange fees are paid, 2-of-3 wallet holders must schedule and do these transactions weekly (say, 4 or 5 times).

[^multisig]: Can a multisig wallet use Oasis or do we need to trust eg. me or [@jpitts](/u/jpitts) to transfer into our own wallets and then back?

DAI is held in the EthMagicians wallet.

Expenses are paid back from the DAI held in the EthMagicians wallet.

### (2) Create a CDP

A CDP is created, presumably requiring some minimum amount funds from the EthMagicians wallet. It can be topped up with ticket sales over time.

*[@Flash](/u/flash) – can you point us to and/or explain what creating a CDP means? Is there a minimum? Are there costs? Can it be done from a multisig wallet? Do we get interest?*

When expenses are submitted, the CDP generates DAI as needed.

New sponsorships in ETH (for example) could be sent to this CDP in the future.

### Convert projected costs now

Since we *do* have a treasury, we could choose to do (1) or (2) soon – essentially lock in that we need 3KEU for catering, and 2KEU from previous ECF sponsorship.

---

Closer to the event (basically, as people submit expenses), most of which would occur around the time of the event or shortly after, DAI would be transferred to the people who paid (who would be responsible for converting to fiat or holding DAI).

Right now, who will pay the caterers is an open question. I think we can ask Jerome if he / Asseth might do this. I can do this if need be as long as they will take EU with an IBAN transfer. Tomo might be able to as well. I’ll follow up on this.

---

**Flash** (2019-01-10):

[The MakerDao CDP](https://cdp.makerdao.com) is a decentralised loaning system, you lock up as much Eth as you want, minimum being around 0.005 Eth and in return you can create DAI. At any time you can deposit and withdraw your Eth as long as you keep the DAI collateralize at over 150%. It charges 2.5% of the created DAI per year(0.0068% per day) as its fee.

I’m not sure how we would go about creating one as I haven’t done it from a multisig before but it should be straightforward. Call the MakerDao contract that creates it, deposit Eth as collateral, and then create DAI as required.

The debt is public, those that want to buy tickets in DAI could pay it back directly and watch the number shrink.

After the event, once everything has been payed for, we can close the CDP by paying back the remaining debt (in DAI) or set a goal for the next one(donations to the CDP effectively lowering the ticket prices for next time.)

Some DAI will need to be bought if we want to close the CDP by paying the remainder of the debt in full. The advantage being that there is no rush for this.

---

**boris** (2019-01-10):

Awesome! Thanks for the explanation.

---

**ligi** (2019-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/flash/48/1356_2.png) Flash:

> Personally I think it makes sense to generate them directly rather than have to rely on someone else to stabilise the funds.

I think this is where we disagree. I strongly believe in the unix philosophy: “Do one thing, and do it well” - and I think managing CDPs should not be what we do.

Also - I do not think we really “rely” on someone there - we just “use” a service someone offers.

My main issue is (apart from the added complexity) that you get less DAI for your ETH when using a CDP. Sure the upside is you can get your ETH back and so maybe gain value in the long term. But is this what we should do? I do not think so. The funds from participants are as far as I see intended to be used to cover the costs in short term and not to gain value in the long term.

Also we might not need much exchanging at all. IMHO we should just request DAI from participants instead of ETH. Perhaps we should even make it more expensive if people really want to use ETH to encourage using a stablecoin which makes planning more easy and is less risky.

---

**Flash** (2019-01-10):

My idea for the CDP was to create a clear separation of funds. We can guarantee that DAI can be pulled from it at short notice to cover expenses as they arise. I like that this is transparent and community facing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> Flash:
>
>
> Personally I think it makes sense to generate them directly rather than have to rely on someone else to stabilise the funds.

My main issue is (apart from the added complexity) that you get less DAI for your Eth when using a CDP.

You only get “less DAI” if you are looking to draw out a large sum at one time, obviously if the collateral we have is insufficient then I wouldn’t recommend doing this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> Sure the upside is you can get your Eth back and so maybe gain value in the long term. But is this what we should do? I do not think so. The funds from participants are as far as I see intended to be used to cover the costs in short term and not to gain value in the long term.

This is false, we are not buying Eth with the DAI so this does not apply, the DAI used to close the CDP can be bought at any time. If we want a part of the wallet’s funds to be in DAI long term (as I believe [@boris](/u/boris) has hinted at) then we would buy them separately.

I believe I’ve made my reasoning clear so I’ll leave it at that. I think the CDP idea is neater but if people would rather things be done more traditionally, the end result will be the same.

EDIT: The biggest downside is that a significant amount of Eth could be locked up at one time(even if it’s easily released) to secure it. If the funds need to be on hand for something else or if it makes people uncomfortable to move a large amount then I would advise going with another solution.

---

**ligi** (2019-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/flash/48/1356_2.png) Flash:

> This is false

What exactly do you think is “false”

---

**Flash** (2019-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> This is false

What exactly do you think is “false”

We are not buying Eth with the DAI so there is no value to be gained or lost, there is no speculation.

---

**ligi** (2019-01-10):

I disagree as you then still are attached to the ETH in the form of the collateral - so you still are speculating with ETH.

It might look like a detail - but I think it is quite important as it is also shapes this non-organisation. I strongly think the non-organisation should hold no long-term assets apart from a buffer for like 1-2 events to protect organizers from losses. As soon as you aggregate assets you become more and more of an organisation and I think it is very important the magicians stay a “non-organisation” as much as possible.

---

**Flash** (2019-01-10):

With CDP:

=> Eth is stored in CDP leaving DAI to be freely generated => DAI is used to pay for expenses (leaving debt in its place) => Ticket sales are used to pay off CDP debt (if in Eth, this necessitates a conversion to DAI)

Without CDP:

=> Eth is converted to DAI through an exchange in multiple steps (to try and avoid slippage costs) => DAI is used to pay for expenses

I don’t see the speculation but maybe I’m missing something. I don’t feel like I’m adding anything new to this thread anymore so I’m going to let other people chime in.

---

**Ethernian** (2019-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Hey @ligi as I said in the Github issue – that thread is about finding a volunteer. I don’t think we need a vote here.

Agree. Even I have voted “no”, the poll results should have no decision power. This decision should not be made by voting. This decision is up to the guy responsible for events finances.

---

**ligi** (2019-01-10):

true - the vote has no decision power or is even intended for this. Just wanted to get a feeling how others think about it.

---

**boris** (2019-01-10):

That’s a really excellent summary of the flows and how it would work as one liners – thank you!

Ligi – no speculation, the in/out is all in DAI, and the CDP is per event. Both ticket sales and sponsorships are used to pay down the debt (or, in the case of early sponsorships, top up the CDP).

We understand the “risk” of holding the event with committed funds. So sounds like there would be an “event CDP” for about 3 months or so (usual timeframe of organizing councils from last year).

I’m willing to experiment either way. And we’re looking to [@Flash](/u/flash) for expertise in how this works ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

I have asked Megan from Veriledger to do a treasury management best practices call with us (andy any other company or organization), I hope anyone interested in this topic will join.

---

**Flash** (2019-01-10):

I would love to hear what Megan has to say!

---

**jpitts** (2019-01-10):

**RE: Opening a CDP**

This would require some monitoring and ongoing work as “we” the operators are exposed to having to put up more collateral should the value of the deposited ETHl fall under a threshold.

[Super-helpful overview of CDP and DAI](https://medium.com/cryptolinks/maker-for-dummies-a-plain-english-explanation-of-the-dai-stablecoin-e4481d79b90)

**RE: Converting ETH to DAI, and vice-versa**

Ok, so I also started elaborating on a process (and that was out of topic).

What we should do instead is brainstorm on complete processes and then review later, after we hear from Megan and other experts.


      ![](https://ethereum-magicians.org/uploads/default/original/1X/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://hackmd.io/@wK4HAsEVSyqFwYyXiv2y0A/H1ZWRSrz4?type=view)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



****# Procedure Brainstorming: Converting ETH to DAI when you have funds in a Multisig    ## Jamie's

---

**AdamDossa** (2019-01-11):

I may be missing something, but there is a real difference between using a CDP to generate DAI, and converting ETH to DAI using an exchange.

The former retains your exposure to ETH whereas the latter removes your exposure.

Given that EMs costs are going to be in USD (DAI) and not ETH, unless you want to take a “trading position” on the future value of ETH (which IMO is not something EM should be doing as it has no expertise in this area), a CDP doesn’t make any real sense.

Note that if you open a CDP, and the value of ETH falls, you will end up losing materially more value than if you had turned your ETH into DAI (due to the collateralisation ratio and liquidation fees).

If EM is looking to prudently manage its finances, and not speculate on the value of ETH the only rational option IMO is to turn received ETH into DAI on a regular basis (and accept that between the point where you receive the ETH and turn it into DAI you have an open risk position to ETH / USD so try and keep this period reasonably short).

Surprised this seems so controversial in the above discussion ;-).

---

**boris** (2019-01-11):

Most people come from zero trading / finance background, so none of this comes naturally.

Your post was – again! – well articulated and is super useful to other people reading. I’m looking forward to our treasury management education session!

P.S. [@ligi](/u/ligi) and I both have German backgrounds. Regular conversation may be perceived as “controversial” when it is, in fact, just strong willed discussion ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) ![:de:](https://ethereum-magicians.org/images/emoji/twitter/de.png?v=9)


*(14 more replies not shown)*
