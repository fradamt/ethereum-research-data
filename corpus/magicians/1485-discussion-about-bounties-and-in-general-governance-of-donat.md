---
source: magicians
topic_id: 1485
title: Discussion about bounties and, in general, governance of donated funds
author: jpitts
date: "2018-09-27"
category: Magicians > Primordial Soup
tags: [funding, operations]
url: https://ethereum-magicians.org/t/discussion-about-bounties-and-in-general-governance-of-donated-funds/1485
views: 1517
likes: 11
posts_count: 12
---

# Discussion about bounties and, in general, governance of donated funds

I saw a Twitter conversation w/ [@pet3rpan](/u/pet3rpan), [@lrettig](/u/lrettig), [@boris](/u/boris) & others about the use of funds, particularly in the context of raising for bounties. There is a lot of potential in this approach, so let’s dig into it.

https://twitter.com/pet3rpan_/status/1045351362081566721

So far, donations have been directed at running our Council gatherings and related activities (part of “In-Person Work”). A bounty program may enable Magicians in the community to work more on advancing EIPs and other important work outlined in our [Practices](https://github.com/ethereum-magicians/scrolls/wiki/Principles-of-the-Fellowship#fellowship-practices).

- Online Presence
- In-Person Work
- Iterative Workflow

Participants do research, gain experience, present their work, and make proposals.
- Proposals are discussed and reworked, online and in person, until consensus is reached.

**Is a bounty program a good fit for our goals and practices?**

**How might we best structure a bounty program?**

## Replies

**jpitts** (2018-09-27):

We will soon do a better job of clarifying and documenting the current use of resources.

To briefly sum it up:

1. The ETH stored in the donation multi-sig at 0x85cab7143ff3c01b93e88f5b017692374bb939c2 has not been disbursed.
2. @boris statement captures the rest: “Currently, an all volunteer effort with no formal entity. Sponsors pay for costs. Individuals or Host Organizations pay suppliers (eg catering).” (From the Twitter thread, boris responds to serapath)

---

**lrettig** (2018-09-28):

Linking to a related Github issue I created today in the scrolls! https://github.com/ethereum-magicians/scrolls/issues/24

---

**jpitts** (2018-09-28):

These are really important questions raised in [issue #24](https://github.com/ethereum-magicians/scrolls/issues/24):

1. How many total keyholders should there be?
2. How many need to sign a tx to release it?
3. Who should those keyholders be?
4. How do we “elect” those keyholders?

I will add to the current topic of “bounties”: “governance of donated funds”.

---

**boris** (2018-09-28):

Thanks [@lrettig](/u/lrettig) — that’s exactly the issue that needs tracking.

Some more background: I have a to do which I should file as an issue about tracking finances in fiat and ETH. I am owed some funds from Berlin that I have filed receipts for but not invoiced. Budgets etc from Berlin and Prague are all available.

---

**boris** (2018-09-28):

I have been busy today so did not have time to follow all of this.

[@pet3rpan](/u/pet3rpan) I was confused by your tweet because I assumed you just saw the donation transaction in the leaderboard.

I got this Twitter DM from The Officious BokkyPooBah:

> Hi Boris, I recently got a donation from NAME in $NAME tokens. I’m happy for up to USD 5k of this to be donated to the Ethereum Magicians. The Ethereum Magicians donation page only accepts ETH. Do you want me to convert these to ETH and just send to the ETH address, or can the Ethereum Magicians happy to get $NAME tokens off-chain?

To which I replied:

> Hi! That’s a great offer, thank you. Yes, ETH would be best. We don’t currently have a way to deal with anything else.

So if this was not meant for EthMagicians as a whole it should go somewhere else.

I have no particular opinions on how to use extra funds at this time but we DO need to discuss it.

And I still need to write up a public thank you to TOBPB ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**pet3rpan** (2018-09-28):

[@boris](/u/boris) I had no awareness of that! I think it is definitely for the magicians ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) I just consider it to be different to our main wallet if that makes sense.

Here is a proposed bounty program design: [Magicians Bounty Fund - Google Docs](https://docs.google.com/document/d/1J30QK77709PQxjSKW9BZwTpa_vKrUrei80IZPrj9SFQ/edit?usp=sharing)

A ring of dictatorship governance model idea:

- There X amount of ETH in the Bounty fund, with Y amount of governing parties. Each party has the ability to move their share of their funds at will without requiring consensys of the other governing parties. There is self-sovereign freedom in each individual governing party. So if there is 150 ETH, and 3 governing parties. 50 ETH will be under direct control of each party.

---

**jamesyoung** (2018-09-28):

FYI : we have been working on the Moloch DAO (code complete, working on tests, write-up in edit) : https://github.com/MolochVentures/moloch

Separately I also worked on a bounty chrome extension that integrates with Github. Just checked the creation file date and it is exactly a year ago today - taking that as a sign to open source it. I need to dust the repo off a bit : https://drive.google.com/file/d/1Q2B_GkKzTE_CEliQWYirz9CIYS_1Svmr/view?usp=sharing

Also, this : https://twitter.com/glenweyl/status/1023734717672247297?lang=en

---

**boris** (2018-09-28):

Thank you for sharing! I am digging into moloch more and trying to play catchup.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamesyoung/48/389_2.png) jamesyoung:

> Also, this : https://twitter.com/glenweyl/status/1023734717672247297?lang=en

Well, aside from the one day of the Council itself, there is time / space / interest during post Council / outside of Devcon. Please keep us up to date – I’d love to participate. And I’ll see Glen next week here in Vancouver.

---

**boris** (2018-09-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pet3rpan/48/189_2.png) pet3rpan:

> @boris I had no awareness of that! I think it is definitely for the magicians  I just consider it to be different to our main wallet if that makes sense.

OK. Yes, bounties should be a “different wallet” and handled differently.

I consider the main wallet that donations are currently pointing at to support Council / event activities primarily. That may extend to supporting regional events.

But it’s also such a small amount and we’ve got so many people paying out of pocket for travel and accommodations (my estimate is that people volunteering to organize CoP will be spending $20K to be in Prague) that at this point we’re far away from having funds to do much of anything beyond existing.

---

**jpitts** (2018-09-28):

We’re small now but it is a good idea to iteratively continue on governance should the market price of our donated assets rise again. ![:full_moon:](https://ethereum-magicians.org/images/emoji/twitter/full_moon.png?v=9)

I like the idea of managing funds and governing their use separately for different aspects of the operation, it can generally follow our practices:

- Online Presence
- In-Person Work
- Iterative Workflow

Having said that, it may be a good idea to have a general donation pool and allocate from there.

But rewinding a bit here… we may be solving before understanding.

**Key to developing a viable system for raising and managing the funds is to understand the needs we have, the needs of the community, and the challenges we face.**

Some key challenges I see:

- tragedy of the commons, to not let important things get neglected
- being responsible governors of resources, while enabling open participation
- know the process and the general destination of the funds.
- disruptive influence by those donating funds, or not enough?

---

**jpitts** (2018-09-28):

I could see [@pet3rpan](/u/pet3rpan)’s bounty program proposal as very helpful for **Online Presence** and certain Rings such as Education, to help us get things done™. The communications infrastructure and content areas of work at the Fellowship are well-suited for an iterative, move fast and break some things approach.

The **In-Person Work** i.e. Councils and other gatherings, benefits from a funding and operational model which is far more dependent on the host and sponsors “on the ground”. Funds may be helpful for scholarships, or to serve as a financial buffer or fallback mechanism for running Councils.

For the **Iterative Workflow**, i.e. the actual process of Ethereum improvement that we’re all working to facilitate, may need to be designed far more carefully. Ongoing standards work may not need any funding at all. But the “working code” aspect may benefit greatly the bounty program proposed by [@pet3rpan](/u/pet3rpan).

