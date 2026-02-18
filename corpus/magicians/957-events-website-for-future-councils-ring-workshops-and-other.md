---
source: magicians
topic_id: 957
title: Events website for future councils, ring workshops, and other Ethereum community events
author: boris
date: "2018-08-05"
category: Magicians > Site Feedback
tags: []
url: https://ethereum-magicians.org/t/events-website-for-future-councils-ring-workshops-and-other-ethereum-community-events/957
views: 1329
likes: 3
posts_count: 8
---

# Events website for future councils, ring workshops, and other Ethereum community events

I made an events site for future councils, ring events, and other Ethereum community events.

See https://sleepy-williams-401b9e.netlify.com/

I was the one that made a website for Berlin Council, and I think making a whole website is overkill. I replicated the whole website in one page here https://sleepy-williams-401b9e.netlify.com/events/2018-council-of-berlin/

It’s a standard Jekyll site, so people would do pull requests with new events, or file an issue if they aren’t comfortable with Github and volunteers would do it.

I’ve put this into a Github issue https://github.com/ethereum-magicians/scrolls/issues/15 to track progress, but am posting here for broader discussion.

The data is incomplete / placeholder as I needed some content to work with. I am happy to take pull requests in the repo here https://github.com/bmann/ethereum-events for now. This should be very simple even for non-technical users – you can edit files directly through Github, and then make a PR (Github will prompt you to make a “fork” which will then be in your own account). I am happy to help support someone trying this out so we can improve documentation on how to do this.

And of course: design assistance welcome!

Edit – some additional thoughts: I was inspired by nodeschool, which has each chapter add a little json file https://github.com/nodeschool/nodeschool.github.io/tree/source/chapters

Since I used jekyll, the basic pattern of just adding a post for an event seemed appropriate.

Back in the day, Barcamp exploded around the world by having a Barcamp Wiki where people copied, cloned, and remixed content.

So I hope this will help event organizers come up with templates and patterns.

*I’m sticking this in Site Feedback as the EthMagicians “meta” category – suggesting we use it as the general category for FEM community process.*

## Replies

**Ethernian** (2018-08-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> And of course: design assistance welcome!

I am not designer, but I have a friend (a good web-designer), whom I could ask to help (I’ll cover the expenses).

Let’s talk about what would you like to do. Possibly, we’ll need some design elements for rings etc…

---

**boris** (2018-08-07):

Thanks, that is a generous offer!

Right now:

1. it needs consensus that this is something that EthMagicians wants to take on (using the GitHub organization & domain name)
2. People who want to volunteer on curating events

So not even design or development skills needed, just managing issues / PRs. Although will need a couple of people with basic git skills too.

[@MadeofTin](/u/madeoftin) suggested in chat that this might be a Ring — event curation, best practices, support around sponsorships, etc. That’s fine too — now we just need people ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

Back to your original question — it’s functional now, and I don’t have any particular opinion on design elements until it gets used a bit.

---

**Ethernian** (2018-08-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> it’s functional now, and I don’t have any particular opinion on design elements until it gets used a bit.

I am not asking about design elements itself. I have asked about its reason and usage.

For example, there could be a EA-logo designed to be used by Ethereum Architects on their visitcards or sites.

It could have a good marketing and self-identification value. It will make a membership more attractive.

The EA-logo should be derived from main FEM logo, but distinguishable from other FEM-Rings logos if there will be any.

possibly you have more ideas like that?

We need this for job description for designer if we will hire him.

---

**boris** (2018-08-07):

For your example, I’m not looking to take on work around logos / graphic design for Rings.

The need / audience is something like this:

- don’t have to make custom websites (Council & Ring & regional community organizers)
- share your event with Ethereum builder community (anyone who is making a community focused event)
- check for overlaps or side event opportunities  (event organizers)
- find out the events you want to go to (attendees)

Maybe:

- help with templates and best practices
- help with sponsorships & budgets (this one has issues — but budget templates & best practices)

So, from a design perspective — it’s about helping the site meet the needs of those users. The one side is largely event organizers — the other side is participants, which is mainly about awareness & marketing.

---

**Ethernian** (2018-08-07):

where do you see the distinction of the custom website to FEM forum?

Isn’t possible to do the same there?

Do we create a multiple sources for the same info?

I mean, anybody is free to create any site of his choice, but should it be part of the FEM?

---

**boris** (2018-08-08):

I found that making a destination landing page for events was clearer and actionable than a forum post here where things get lost.

I’m volunteering to run the site and looking for collaborators.

I had a good discussion today where I  *am* going to get a separate domain for this site and just run with it.

One of the “centralized” items that FEM owns is the domain name. Right now that is this forum and the donations subdomain.

Thanks for the discussion!

---

**MadeofTin** (2018-08-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> @MadeofTin suggested in chat that this might be a Ring — event curation, best practices, support around sponsorships, etc. That’s fine too — now we just need people

[@boris](/u/boris)

I have read over this a couple times and each time I feel like I want to be more helpful to the Magican’s in general as well as not sure where I fit. Given that I work on Ethsignals I don’t want to show support for EIPS outside of the scope of tech needed for signaling. I also feel that one role Ethsignals has is to be a tool to help Ethereum Magicians and so there is a good intersection there.

I am happy to help out anywhere that I can also remain independent from a Ring, or showing direct or indirect support for specific EIPs. Helping Rings get set up and running when there has been a request for them and meta-governance with the forum, are some things I have thought. Let me know where you and [@jpitts](/u/jpitts) could use a helping mouse and keyboard. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

