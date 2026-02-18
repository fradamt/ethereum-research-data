---
source: magicians
topic_id: 1205
title: Do we need this? - an Active EIP for Ring Formation
author: MadeofTin
date: "2018-08-31"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/do-we-need-this-an-active-eip-for-ring-formation/1205
views: 820
likes: 1
posts_count: 5
---

# Do we need this? - an Active EIP for Ring Formation

I ran into this again and wanted some feedback from my fellow Magicians.

We have the Default template for [ring formation](https://github.com/ethereum-magicians/scrolls/wiki/HOWTO-Form-A-Ring#membership-requirements) through a [template charter](https://github.com/ethereum-magicians/scrolls/wiki/Ring-Charter-Template).

We could leave it as is, or we could take the next step and create an Active EIP that is updated with any changes as Rings evolve. We have an [early version](https://hackmd.io/RahsNQhWTZW3nmssMGol1A?both) written. I do not feel this is at the level of , “This has to happen”, but I do see some reasons why it would be good to do.

### Reasons To

- Gives space for Rings to exist outside of EthMagicians. Currently Rings are a subgroup of Ethereum Magicians. I feel instead that Working Groups should be a subgroup of Ethereum Developers and EthMagicans exists as a natural (non-exclusive) gathering place for them. One Example is Prysmatic Labs work on Shasper. They are in practice a working group, yet they don’t need to exist within Ethereum Magicians if they don’t want to, but they could still be a Ring.
- Some loose standards are generally a good idea for consistency

### Reasons Not To

- May be more formal then we need
- Ain’t nobody tell devs how to gather and do their work

Some updates will be needed for the Ring Formation EIP of course. What are all your thoughts? Worth doing? not worth doing? I am happy to update and submit, but wanted to run it by all you all first.

## Replies

**boris** (2018-08-31):

I would disregard that early version ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) – was very much an early WIP. Your charter is a much better starting point.

Yes, working groups definitely exists outside of any EthMagicians structure. In fact, part of the ring format could, much like EIPs themselves, have a “discussions-to” which basically just lists where stuff is.

The “centralization” of having a list / directory on the EthMagicians wiki is just a thing that is useful – anyone else could make a list that lives somewhere else, regardless of where the working group forms.

*sigh* I still have my notes on paper of all the working groups that people mentioned around the room, that do need to get transcribed. Perhaps I’ll start by uploading them as images and see if someone has more time for transcribing.

I am still ambivalent on whether or not to submit as an EIP. Will we have non-EthMagicians-working groups attend Council to be part of this discussion? Aren’t you a magician if you run a working group?

Don’t know!

---

**MadeofTin** (2018-09-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> The “centralization” of having a list / directory on the EthMagicians wiki is just a thing that is useful – anyone else could make a list that lives somewhere else, regardless of where the working group forms.

I like framing the EIP as the definition for a Ring Charter. It gives room for implementation flexibility. As an Active EIP (similar to EIP1) an updated list of the current Ring and their Charters can be kept at the end of the EIP.

Would the charter itself be something to add to the EIP repo itself? Github would be a good place to keep them as pull requests are a good way to handle acceptance and Ring Formation in a decentralized fashion. Perhaps there is a better place for them?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Will we have non-EthMagicians-working groups attend Council to be part of this discussion? Aren’t you a magician if you run a working group?

To the first unlikely. To the second, I guess it depends on if by definition any working group is a member.

To me, it helps frame working groups places in the Ethereum community.

- Working Groups are a subset of Ethereum Devs → Magicians is a place that exists for Working Groups to meet.

This relationship more clearly communicates our desired role, which is not to have some exclusive rights to Ethereum development. This is less clear if the relationship was:

- Magicians is a place for core devs to meet → Working Groups exist under the Magicians ecosystem.

and, for the former to exist there would need to be a place outside of Magicians for the rings to be defined.

P.S. I would be happy to take a stab at transcribing as long as I can decipher your handwriting. ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**boris** (2018-09-01):

I actually don’t think so! Non-EM-Working Groups are perhaps hard to define, but people who attend / run those groups do overlap and attend ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

But yes, great framing. And I totally get your logic. We are literally defining our OWN rules of engagement with using an EIP to define this.

Maybe an additional one:

Working Groups form to tackle challenges within the Ethereum ecosystem → Working Groups are a subset of the Ethereum ecosystem → Magicians is a place that exists for Working Groups to meet

“Challenges” can sometimes be boiled down to an EIP or set of EIPs, but may also be broader – eg Education, or Signaling.

And you may note that I specifically am not saying “Ethereum Devs”. Having a strong connection to technical progress is important, but *can* we be a little broader than that. e.g. a Designer is not a Developer, an Educator is not a Developer, etc.

So – yes, go for it, you should submit an EIP ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

My “concern”, if it can even be called that, is that we need more meat on existing Rings/Working Groups. eg weekly or bi-weekly calls is likely a good signal that a Ring has truly formed.

---

**MadeofTin** (2018-09-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> And you may note that I specifically am not saying “Ethereum Devs”. Having a strong connection to technical progress is important, but can we be a little broader than that. e.g. a Designer is not a Developer, an Educator is not a Developer, etc.

As I was writing I paused when I wrote “Ethereum Devs” thinking just about this. I don’t know what other kind of word to use, but broader is better. Inclusive is better.  Designers, Educators, Builders we are going to need them all to succeed.

I’ll get to work on a rewrite of the EIP.

Rings that meet regularly is a great signal. I will add a space for it in the charter somehow. Perhaps where the charters are listed we can also include where they meet, and when/how often they meet. This is a good way for groups who meet more often to stand out. I wouldn’t want to require it per-say, but any way to incentivise groups to meet more often I would consider.

