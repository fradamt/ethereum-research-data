---
source: magicians
topic_id: 2321
title: Charging for Tickets, Participant Numbers & Event Ticketing for Council of Paris 2019
author: boris
date: "2019-01-02"
category: Protocol Calls & happenings
tags: [council-paris-2019, events, ticketing]
url: https://ethereum-magicians.org/t/charging-for-tickets-participant-numbers-event-ticketing-for-council-of-paris-2019/2321
views: 2836
likes: 15
posts_count: 27
---

# Charging for Tickets, Participant Numbers & Event Ticketing for Council of Paris 2019

Hello all!

Happy 2019! We’re only a little over 2 months away from the Council of Paris, happening alongside [ETHCC](https://ethcc.io) in Paris.

Here are some items from this morning’s [@council-volunteers](/groups/council-volunteers) call, which happen Wednesday morning 8AM PST / 17:00 Central Europe time.

## Charging for Tickets

I proposed that we charge for tickets for the Council of Paris 2019.

Our costs for food (lunch and coffee) are roughly 30EU per person, and food is also the single largest cost. So, this seems like the right number to ask for.

The second reason for charging for tickets is to make sure we have a more accurate idea of how many people are attending.

As always, “all are welcome” – so anyone not able to pay would still be welcome. This just makes sure that we ask people to support the event right up front, and get commitment to attend by paying. Ideally, we would collect ticket fees in ETH – participants are active in the Ethereum community, and creating a wallet and getting access to 30EU worth of ETH doesn’t seem too much of a barrier for new participants.

Anyone have thoughts on why we shouldn’t charge for tickets?

## Participant Numbers

We are planning for 200 participants. ETHCC is, I think, planning for about 1000 attendees, so at 20% this seems a decent guess. We did find in Prague that many more people registered than attended, so either Kickback (for “free” events) – or actually charging for tickets – we think will help get more commitment from participants.

For space planning, we mainly need to be concerned with the maximum amount for a “main stage” gathering, plus looking at smaller classrooms / break out spaces.

Think this number will be lower or higher? How many participants do you think we should be planning for?

## Event Ticketing

We ask that people register / get a ticket so we can 1) plan numbers 2) communicate with them. As above, it also means collecting fees to help cover costs.

I have reached out to the Kickback team to ask if they would actually let us charge for tickets (that is – no refund!). If we do get enough sponsors, we *could* refund tickets still, but this all comes down to budgeting and sponsorship interest.

I have also used [Tito](https://ti.to) for tickets in the past (just for ticketing / event management) – but we would need to ask for payment via ETH in some other way.

Eventbrite would be the same – could do the ticket event management, but would need to take ETH payment separately.

I will be researching this area, if other people have favourite event ticketing apps that can send email updates, please share!

Alternate solutions on how to accept ETH for tickets while also gathering name and (optional) email address for communications also welcome.

---

P.S. Yes we are looking for more volunteers and sponsors. Talk to [@tomislavmamic](/u/tomislavmamic) or message [@council-sponsorships](/groups/council-sponsorships)  who is the lead organizer to get involved. We’ll ideally finalize ticketing and open registrations at the end of next week, so start planning your ring topics and other things you want to discuss!

## Replies

**fubuloubu** (2019-01-03):

Kickback should allow designating a large portion of the amount staked towards event costs, meaning it should be possible to use it like Eventbrite basically (or up the stake to 40 EUR to experience the “kickback effect”)

I know the team is working pretty hard on the dapp, and with the idea that the coat be collected in ETH, this seems reasonable to me. It would be great to promote a reasonable community project.

---

**ligi** (2019-01-03):

I suggest [pretix](http://pretix.eu) as a ticketing solution. It is libre software. I was at multiple events using this system - always happy with it - just recently 35c3 with 16k participants - but also at very small events using it.

ETH payment could be easily done as a plugin: https://docs.pretix.eu/en/latest/development/api/payment.html

I would strongly signal against using Tito - let’s use libre software and dogfood as much as possible!

---

**makoto** (2019-01-03):

Hello. Makoto from Kickback.

Thanks for considering the use of Kickback. I would like to ask a few questions to clarify the requirement.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> so anyone not able to pay would still be welcome

Does this mean just an event crasher with no registration, or do you still want registration but payment as an option (like ETHDenver application process)? What are the actual cost

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> If we do get enough sponsors, we could refund tickets still, but this all comes down to budgeting and sponsorship interest.

Is this either “get all refund or no refund” or some sort of partial refund (eg: if total cost is 100 and you got sponsorship of 70, then you refund 30 split across participants)?

---

**boris** (2019-01-03):

Not really concerned about event crashing. We ask for registration for planning and communication. And, with payment, to help cover costs.

I don’t have the budget link handy. Simple thing is that we need to order catering which is roughly 30EU per person.

All or partial refund:

I would say that all or nothing would be the most likely scenario.

---

**makoto** (2019-01-07):

Sorry for the bit of the silence. To handle “paid event”, it’s technically not difficult to modify `payout` logic so that the max payout can be adjustable by the organiser, etc.

Having said that, we just announced using Kickback for  [various ethereum meetups around the world](https://medium.com/wearekickback/kickback-is-coming-to-your-town-befaf8dd58a9), and supporting both free and paid event for March deadline is not feasible for us (especially coming up with UI which makes sense for both free and paid event).

We just did a bit of brainstorming in our team and came up with a couple of solutions which could serve the purpose.

Option 1: Use Kickback as is

Currently we have the infamous “cooling off” feature where event organiser can claim the remaining ETH if attendees do not withdraw their ETH within one week cooling period. In the past 10~30% of people haven’t withdrawn but the figure may become lower as your commitment is 3~5 higher than the usual.

This is the default way to have "optional donation" but this does not give you any assurance to cover the cost which you are after (NOTE: We are planning to get rid of this feature in Q1).

Option 2: Abuse Kickback

You (ETHMagicians) can just RSVP along with other participants but only mark yourself in so that you can get all the ETH. This is actual the dispute case #1 which I described [here](https://medium.com/wearekickback/handling-disputes-at-kickback-82dc6f49d3e2), but you guys can try it as one off experiment in the following conditions.

- You will write description and make sure that people are aware that they may not being marked as attended despite the fact that they do attend. Kickback will not be responsible for involved in any disputes.
- You will still encourage participants to help you refer sponsorship
- In case you could not raise enough sponsorship and you don’t kickback, then we will modify our site to delist from our event listing page (/events) after the event ended. This is because having 1/200 attendees is unintended use of our platform and we would like stop confusing people visiting the site later on.
- As a platform usage fee, we usually charge $1 per attendance. If you decide not to kickback attendees, then we do charge per RSVP as you guys are not marking anyone as attended.

Would either of them solve your problem?

If you really want to make modification to our code, then I suggest forking our old [BlockParty code](http://github.com/makoto/blockparty) and deploy on your own though this misses lots of new features (eg: sign up, email notifications, better admin UI, etc).

Weather you decide to use Kickback or not, I am more likely to attend ETHcc/EthMagicians and would happy to help.

---

**boris** (2019-01-07):

Thank you for this long thoughtful response [@makoto](/u/makoto)!

It sounds like selling tickets in the traditional sense isn’t really something that Kickback is focused on – totally understand that.

Ideally we’re going to make an initial decision this week.

---

**boris** (2019-01-07):

Hey [@ligi](/u/ligi) I just had a look at Pretix. It is either a hosted version (basically equivalent to lots of other services out there, no Ethereum support) or I guess you meant a community install.

I looked at the [Docker installation](https://docs.pretix.eu/en/latest/admin/installation/docker_smallscale.html). I try and run things on Heroku so I don’t have to deal with servers ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) – but it does look like there is a pretix docker image and I could arrange to have someone get this setup – either `tickets.ethereum-magicians.org` or I would use the `tickets.ethereumevents.global` domain that I own.

And then developing a custom Ethereum payment system that integrates with pretix ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

I’m interested in working on a community / EthMagicians ticketing solution that can accept ETH (and DAI and other arbitrary ERC20s) and especially at the beginning of the year there could be lots of others that want to use this throughout 2019.

I’m not sure if we can get this done quickly enough. We could use a self-hosted pretix for registration and then follow up in a couple of weeks? a month? once a payment solution is deployed?

Do you have other thoughts on this [@ligi](/u/ligi)?

---

**ligi** (2019-01-08):

[@boris](/u/boris): there seems to be a docker image: https://docs.pretix.eu/en/latest/admin/installation/docker_smallscale.html

but we could also IMHO at first use the hosted version and then confirm ETH payments manually as there is not much time left for ETHCC.

---

**boris** (2019-01-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> then confirm ETH payments manually as there is not much time left for ETHCC.

This is the exact issue ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) I mean, I can put a message that says “you have to pay in ETH” but essentially we are doing free tickets and hoping people pay and/or lots of work in matching this up. The best way to ensure people pay is to have ticket registration all in one flow.

And running the hosted version isn’t really that different than just using, say, Eventbrite or Tito which would be much easier to use (since I know those systems already).

I still think this is worth doing and getting setup for future events, so I will look at both the docker option and the hosted option.

---

**ligi** (2019-01-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> And running the hosted version isn’t really that different than just using, say, Eventbrite or Tito

I think there is a difference.It is still libre software in contrast to Eventbrite or Tito - so the upgrade path to self-hosting and the possibility to improve the software is there. The more you use systems like Tito or Eventbrite - the more you lock your self in into a jail of closed software …

---

**boris** (2019-01-08):

OK, I setup an organizer account on the hosted version for FEM. [@ligi](/u/ligi) I added you to the “admin” team, just so someone else has access for now.

Will set it up so there is a team per event and hand out more access to volunteers.

Turns out there is a “manual payment” option. Where you can give instructions on how to go pay by ETH, for example.

I am waiting for my organizer account to be “approved” before I can bring it live. I’ve had to put in my credit card and I guess you get charged even for manual payments? But I’m willing to try out.

Here’s a screenshot of the “manual payment” configured to use ETH. Elsewhere, I have email directing people to the EthMagicians donations page / wallet address. Will need some help testing this once it is live.

*Note to self: mark this down on the Infrastructure page in the Scrolls wiki*

[![38](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f9d9a2d8c0f81e54993c8e7ca2743ac1359c819c_2_689x402.png)382474×1444 251 KB](https://ethereum-magicians.org/uploads/default/f9d9a2d8c0f81e54993c8e7ca2743ac1359c819c)

---

Also, funny coincidence [@codydjango](/u/codydjango) jumped into our Discord chat and it turns out he has a background with Python/Django that pretix is written in, but is new to Ethereum. He’s going to look into what it would take to build a plugin.

---

**codydjango** (2019-01-08):

Yep, I’ll take a look this evening. ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=9)

---

**boris** (2019-01-09):

No hurry on this. The “manual” payment option means we are unblocked.

But, I think running our own instance as a service to the Ethereum community who want to collect in ETH would be pretty great.

---

**ligi** (2019-01-09):

Just wondering: perhaps it could make sense to take DAI instead of ETH

---

**codydjango** (2019-01-09):

I haven’t worked with DAI before, but I’m pretty sure I could do this as well.

---

**makoto** (2019-01-09):

FYI GörliCon choose option 1 https://kickback.events/event/0xe2d2c31c68626b6c1301a49ed50854e1cae0c8fa

```auto
About your Kickback contribution: as mentioned, Görli Testnet is facing funding difficulties. We are setting up a 0.2 ETH deposit to come to the event. As in Kickback’s usual fashion, you can either choose to claim it back, or donate to the project - this is entirely up to you and no fingers will be pointed. All proceeds will go to funding Görli Testnet.```
```

---

**markoprljic** (2019-01-09):

[@boris](/u/boris) I just purchased the ticket. Did you set up everything already, because I’m seeing my order still pending even though I have confirmed transaction on Etherscan https://etherscan.io/tx/0x5ccad705e6d5418fe4875aed07aa0b54bee6ff0288af6f8e63953ddb0429efe6

---

**markoprljic** (2019-01-09):

Update: it just went through and got my ticket.

---

**boris** (2019-01-09):

oh awesome! Thank you for testing! That was the next step, getting people to go through it.

This is a manual process right now. So I saw this message, logged in to pretix, verified that the transaction [was in the EthMagicians wallet](https://donations.ethereum-magicians.org) and then “marked the order as paid” in pretix. I also added a comment to the order with a link to your transaction in Etherscan.

Please, do you have any notes on the ticket process or the instructions?

I am proposing we go ahead with this method for now. I can give access / permission to other people to also help manage pretix and edit the wording and so on. I would say I need at least one other person for this event (and, [@ligi](/u/ligi) is also an admin on the FEM organizer acount).

---

**markoprljic** (2019-01-09):

Thanks for that!

No special comments, the purchase process ran quite smoothly, nothing significant to report.

However, I was rushing a bit and wanted to add my order number to the message afterwards, too late and I couldn’t find where to add it since the website with my order already had the order number written. From that point I wasn’t clear to what the “website” refers to and wether I should have added the order number to message in transaction?

Just that, otherwise all good and IMO you can push the button [@boris](/u/boris)


*(6 more replies not shown)*
