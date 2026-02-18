---
source: magicians
topic_id: 7473
title: "Off-topic: Why does the Ethereum community use Discord?"
author: hax
date: "2021-11-15"
category: Magicians > Process Improvement
tags: [comms]
url: https://ethereum-magicians.org/t/off-topic-why-does-the-ethereum-community-use-discord/7473
views: 4023
likes: 27
posts_count: 20
---

# Off-topic: Why does the Ethereum community use Discord?

Serious question & seriously not trying to troll: how come the Ethereum community likes Discord so much?

It seems like an anti-thesis to the mission and ethos of Ethereum … Discord is closed source software, they discourage anonymous usage (request phone number, ban VoIP numbers, ban people who use Tor, ban certain burner emails, …), they discourage development of alternative open source clients (it’s against their ToS and there have been many instances of Discord bricking alt-clients and banning their users), etc.

It seems like the exact opposite of what an “open, permissionless Internet Money / world computer community” would want to use. Yet even the technical conversations take place on Discord and people in the community are virtually expected to have a Discord account if they want to participate in daily matters.

Interestingly, certain other cryptoasset communities (e.g., Bitcoin / Lightning Network, Monero, …) avoid Discord and have chosen open/free alternatives (e.g., Matrix, Telegram, or even IRC).

So, how come people here don’t drop Discord for something more “free”? How could it even get so big in the first place?

References:

1. Reasons not to use Discord
2. Jeffrey Paul: Discord Is Not An Acceptable Choice For Free Software Projects

## Replies

**franzihei** (2021-11-15):

Thanks for posting, I couldn’t agree more. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

I’ve been trying to move more Ethereum community stuff over to Matrix, but there is a huge reluctance. A lot of people seem to have rather outdated (bad) experiences from trying Riot or Gitter years ago, and have a general bias towards “closed source software has better UX” (lol). I personally think Discord has a terrible UX, but that’s beyond the point here. ![:upside_down_face:](https://ethereum-magicians.org/images/emoji/twitter/upside_down_face.png?v=10)

The entire daily operations of the Solidity team are on Matrix (our public and team channels) and we are very happy with it.

Criticism I heard quite frequently was around missing server and moderation features in Matrix.

I think Element is catching up on that with the “spaces” features now.

Would really love to see more people moving away from closed source tools like this while good alternatives are available!

---

**matt** (2021-11-15):

Much of the Ethereum community was already using Discord and transitioning away from gitter was relatively painless since most didn’t need to create another account to monitor. I also prefer to not use Discord. But I’m not sure we can reach exit velocity to move to a different platform at this point. I would support any effort to do so though.

A few past discussions of the topic (ironically, you need to be on the discord to see them!):

- Discord
- Discord

---

**ShadowJonathan** (2021-11-15):

If it helps any; Matrix has a concept known as “bridges”, which’d essentially mirror the whole experience of another platform onto matrix. With that, “exit velocity” would not be needed as much as the experience of moving away would not be as atomic or abrupt, instead, it could be gradual and seamless, as people both on discord and matrix could stay in touch.

That said, I’d still recommend Matrix the most out of those three examples provided, Telegram does not have good tools to manage large communities (with many different discussion rooms), and is only questionably open source at best.

I could illustrate an argument against IRC via a blogpost which someone over at mozilla/gnome wrote about it years ago, ~~but i can’t find it right now~~ (found it, look below), so i’ll give my personal one as well; I think IRC has run its course quite clearly, while it’s a pretty robust protocol, it cant attract people today, and thus it cant be or become a backbone of communication, while more and more people pick either discord, whatsapp, or other commercial solutions for their central communication. Comparatively, matrix could be a clear upgrade from IRC, both in terms of security, and usability.

---

The posts:

http://exple.tive.org/blarg/2020/03/06/brace-for-impact/

http://exple.tive.org/blarg/2018/11/09/the-evolution-of-open/

---

**jpitts** (2021-11-15):

There is a very strong undercurrent of pragmatism in the community, which means many have an open mind about using centralized tools until open, public, sustainable alternatives (depending on decentralization and other properties) are available. And the outcomes can be not ideal – even downright terrible – given our shared principles regarding tech.

Additionally: people do things for no reason other than “this is what other people are doing”, we are addicted to how the medium works, and for comms in particular we are very often intolerant of the additional work required to use a less commercialized, more open system.

---

**gcolvin** (2021-11-16):

I hate Discord.  Not just because it is closed source, but because it closes our deliberations off from the rest of the world, as [@hax](/u/hax) and the people he links to point out.  They can and do spy on their users and their DMs, and they actively resist private use of the system via VPNs, Tor, and burner phones.  Also, some people cannot abide, or even understand, the dense legalese of their terms of service – [Terms of Service | Discord](https://discord.com/terms).

I don’t know why we moved off of Gitter and its integration with Github.  Just to get what some thought to be a nicer UX?  We need emojis, GIFs, and other toys for children?  We need bots to put us in timeout if we post too much text, like a schoolteacher?  Discord is not an appropriate platform for professional communication on an open-source project.

---

**ShadowJonathan** (2021-11-16):

Some other tidbit of info; Gitter got acquired by Element, and all gitter rooms are currently effectively matrix rooms. Gitter is intended to become “just a skin on top of a normal matrix client”, they’re gradually merging gitter and element to become just one codebase.

---

**gcolvin** (2021-11-17):

For extra fun, we build bridges between the various systems that people use, so that if you want things to be readable everywhere you have to use the lowest common denominator.  Which for all you know is ASCII.  And don’t count on edits or deletes working either.  So the UX and formatting benefits are illusory as well.

---

**ShadowJonathan** (2021-11-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> We need emojis, GIFs, and other toys for children?

I don’t think that framing it like this is fair to the social tools it ultimately provides, there’s a lot of stuff that emojis and reactions alone can do to communicate “non-verbally”, here’s a blogpost describing Ansible’s experience with hosting QnAs on matrix; [Running conferences on Matrix: A post-mortem of Ansible Contributor Summit](https://emeraldreverie.org/2021/10/08/running-conferences-matrix/)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> We need bots to put us in timeout if we post too much text, like a schoolteacher?

This is automated community moderation, again, i don’t think its fair to frame it like that, because to a degree, yes, you are being timed out by a “school teacher”, but only because you broke the rules of spamming of a community, determined by that same community.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> For extra fun, we build bridges between the various systems that people use, so that if you want things to be readable everywhere you have to use the lowest common denominator. Which for all you know is ASCII. And don’t count on edits or deletes working either. So the UX and formatting benefits are illusory as well.

This may be the case with IRC, but matrix as a lowest common demoninator *does* provide these features, while yes, it would not communicate deletes and edits (well) with platforms like matrix, it could communicate these excellently with others like whatsapp, telegram, or indeed discord, so i think that this is not representative of something reflecting on matrix’s bridging ecosystem.

---

**yorickdowne** (2021-11-19):

We need a place where others are. Network effects are real.

We need a place with easy auto-moderation. People have things to do and can’t be on top of spam 24/7.

We need a place with bots for GoEth deposits, price queries, beacon chain queries, and and and

We need a place with integrated video/audio so community calls can happen *right there*

And we need a place with sarcastic emojis and where users can meme

Having all that in !Discord would be great. Right now it’s Discord.

---

**gcolvin** (2021-12-04):

We have different notions of what tools are appropriate for professional communications.  IMO, Discord was not designed for professional communications, and is not licensed for open source.  Matrix is much better that way.  And I’m a crotchety old man with strong opinions :->

---

**fullnodes** (2021-12-04):

Just come across https://wiremin.org/ ,  a preliminary product for messaging but lacking many features comparing to modern IMs. Seems the team keeps working on it. From their [FAQ](https://wiremin.org/faqs.html), it is based on a fully decentralized protocol without any servers but is not built on top of any sort of blockchain system.

---

**leoneric** (2021-12-06):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/0/0acd3bf9a1591cc3b644ea8c8ce7505f0c303dc7_2_669x500.jpeg)image2064×1542 194 KB](https://ethereum-magicians.org/uploads/default/0acd3bf9a1591cc3b644ea8c8ce7505f0c303dc7)

Source: https://twitter.com/GnosisGuild/status/1446089073903472642

---

**AndersonTray** (2021-12-09):

Discord is easy to use and free, and there is many wats to control your server/channel for the other members.

---

**TimDaub** (2021-12-09):

For my project that is built on Ethereum, I have opted for Discord as it’s a tool that closely related projects are also using, and since the barrier to entry is just so low.

When recommending users to join Discord, I can virtually assume that they already have it installed and just need to click the button. I’m much aware of the benefits of using e.g. Matrix or IRC, but those do exactly not have these qualities. They’re terrible to onboard new users and I’d just guess that my conversion rates would converge to zero. I doubt that I have to show data of a survey about the install rate of Matrix clients of my users. I’m pretty sure it’s very low compared to Discord.

I also find the “why does Ethereum community use Discord” argument a bit unfitting or hypocritical. E.g. as a member of the Ethereum community, I don’t use Twitter which, in terms of closed-source-ness is exactly as terrible as Discord. So if we’re having a discourse about Discord, we should also have one about not using Twitter anymore, or Medium, Github, or Substack etc.

In any case, I’d switch to a fairer distributed software in no time, if it meant that I can sustain the growth of my community. But as long as I can’t, I’m willing to make the compromise and use Discord.

Edit: I forgot to say that e.g. we also bridge our Discord to Matrix. But since the bridge is lacking features, if you’re a Matrix user of our project that you’re like a second-class user sadly…

---

**definevalue** (2021-12-24):

Why not create a clone of discord or similarities in functions and open source this project? I see where your coming from but the platform is nice and that’s really why I see people going to it.

---

**TimDaub** (2021-12-28):

Relevant blog post:

[Please don't use Discord for FOSS projects](https://drewdevault.com/2021/12/28/Dont-use-Discord-for-FOSS.html)

---

**chuksnjr** (2021-12-31):

I also agree to the fact that Discord does not meet the Ethereum software terms. In any case, while eyes might be on the look for another place or creating another platform, we might just continue on discord until a better option shows up.

Kudos to all contributors here making Ethereum a better tool for humanity.

---

**Lima** (2022-01-04):

Despite its initial focus on the gaming industry, Discord was used in other sectors like politics, entertainment, lifestyle, and recently, cryptocurrency. The gaming world and the cryptocurrency space share many things and both benefit from easy real-time communication. Discord’s razor-sharp user experience design and slick user interface did the rest.

---

**delbonis3** (2022-01-15):

[@Lima](/u/lima) Discord’s “user experience” is chock full of dark patterns prompting you to give them money and it’s also just generally a very heavy tax on hardware.  Also being centralized, proprietary, and VC-funded software it’s fairly contrary to the general spirit of FOSS projects focusing on decentralization.

