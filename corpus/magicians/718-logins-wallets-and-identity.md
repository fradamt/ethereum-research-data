---
source: magicians
topic_id: 718
title: Logins, Wallets, and Identity
author: jpitts
date: "2018-07-14"
category: Protocol Calls & happenings > Council Sessions
tags: []
url: https://ethereum-magicians.org/t/logins-wallets-and-identity/718
views: 2471
likes: 11
posts_count: 12
---

# Logins, Wallets, and Identity

Day 1, 1:30 pm - 2:30pm

[![image](https://ethereum-magicians.org/uploads/default/optimized/1X/0edd942f2e94a10f81e0caa3b9529c3ef98558bf_2_666x499.jpg)image1568×1176 472 KB](https://ethereum-magicians.org/uploads/default/0edd942f2e94a10f81e0caa3b9529c3ef98558bf)



      [docs.google.com](https://docs.google.com/document/d/1mJ9akYTE86PcOOKsvzaN6ICth1jMDMw3jCWRF7jV044/edit)



    https://docs.google.com/document/d/1mJ9akYTE86PcOOKsvzaN6ICth1jMDMw3jCWRF7jV044/edit

###

“Logins, Wallets, and Identity” Half-Good Notes by Jamie Pitts  ---  Upgrade path if you do not want to yet deal with private key  ---  At status, users screen snap the 12 words  Company as custodian   How much metadata are you leaking with custodian...

## Replies

**boris** (2018-07-14):

[@benjaminbollen](/u/benjaminbollen)’s session with some distracted interjections from me!

I care about this topic and do want to follow it!

---

**aogunwole** (2018-07-16):

Adding my notes here from this session. [@mariapaulafn](/u/mariapaulafn) also has comprehensive notes here

**Founding Question:** How do we make UX design better for users having access to their keys and their tokens

- Need to find the balance between 12 words on a piece of paper vs. the “giving everything” approach at Coinbase

Also looking at privacy and wallets and login recovery

- Multi signature smart contracts to hold the users tokens for them - use good wallet design, so user doesn’t need to hold the key and a trusted party holds them and when the user has time, then they learn more about how to own and control their keys

If company owns the keys, what are the clear set of values for the companies/Coinbase model?

Private Keys should not migrate - educate users on the experience upfront so they know their value/the experience

*Also, worst user experience is to create another private key* Can users bring their own private key?

Smart contracts managing keys can help for generalized recovery mechanisms (you can always use those 12 words, lose the keys, etc.)

MP challenged that this brings in the layer of centralized Trust - which may go against trustless systems principle

Follow up reading: [Uport white paper](http://blockchainlab.com/pdf/uPort_whitepaper_DRAFT20161020.pdf) for consensus proposals for managing keys

Jason shared that we need to educate users at the point of where they *care* - doesn’t matter if you educate them upfront, it depends on what they need to use the wallet for and size (of need and transaction) matters.

Boris mentioned how do we segregate wallet concepts as they different b/w blockchains vs. identity and login (reclaiming wallets/keys)

Entity vs. Identity (Kopinski’s whitepapers on user frameworks)

Entity is my legal boundary, money is horizontally relevant (it is relevant to all communities that use that currency)

Identity is the sum of all my entities and attention on aspects of you is what creates identity  made by a claim represented by an authoritative party (education, company, etc.); vertically relevant, you cannot take this relevance amongst other groups

Research: Zippy on mobile access and storage, need to tie to mobile hardware and OS for powering mobile blockchain apps (must think beyond just Ethereum community when building wallet structures and must focus on the end user’s goals/resources).

How do we create the dApp userflow for using challenges to educate users to come on board with using their private key?

**Follow Ups**

UX Design for onboarding new users and understanding their wallets/private keys

What technical needs do we have to consider for supporting multiple key management and recovery?

---

**fubuloubu** (2018-07-16):

Two things:

1. I really think people just weren’t meant to screw around with private keys. It should be something that should be embedded deeper into the operating system or browser, with more user friendly management scheme’s on top. Casa wallet’s managed wallet service (3 factor seed phrase recovery and social sharing) is really neat. More experimentation should be done in this regard, eventually building systems like @alexvandesande’s personal DAO idea.
2. Identity needs a lot more work. I think there’s a huge opportunity here to redesign the account systems of all applications and ecosystems. Kill the password dead beyond all reckoning, and introduce new paradigms that are more secure and natural to users (device based authentication, universal profile, not having to set my profile picture on a new app).

Interesting idea I just had is that you can derive multiple accounts from your seed phrase… One (or more) account could be your personal, one could be your professional, or you could have one for each job you ever have, or every year you use a new one for tax reasons. Play with that a bit more? Seems interesting.

Yes, it is probably too late for me to be rambling.

---

**mariapaulafn** (2018-07-16):

I’m adding my notes in dialogue format.

Please everyone check I did write your names (or not - clearly i missed some) and comment on the google doc.


      [docs.google.com](https://docs.google.com/document/d/13ZN_aoOq7nJs-GwndOtzeiAD-Eh5pQ9oYkQ0YpHl0-U/edit?usp=sharing)


    https://docs.google.com/document/d/13ZN_aoOq7nJs-GwndOtzeiAD-Eh5pQ9oYkQ0YpHl0-U/edit?usp=sharing

###

Group discussion Funkturm  PK Management Proxy contracts  Identity  Ben    You key is your coin on one side of the spectrum and the other one is the people that don’t consider this  If we wanna get people into web3 we need a smooth transition curve...

---

**boris** (2018-07-16):

Next step is forming a Ring (working group). Except the Ring-formation meta group needs to define the formation process ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**boris** (2018-07-16):

Thank you [@mariapaulafn](/u/mariapaulafn) so much for great notes!

---

**fubuloubu** (2018-07-16):

I’ve heard Mordor has a forge…

---

**boris** (2018-07-25):

Thanks to [@Danibelle](/u/danibelle) for identifying the video and a short transcript. Video is here: [For Sale - View.ly](https://view.ly/v/ZICBx62MbHdh)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danibelle/48/282_2.png)[Feedback & help wanted: Council of Berlin - raw video, Viewly descriptions and titles, still photos, licensing](https://ethereum-magicians.org/t/feedback-help-wanted-council-of-berlin-raw-video-viewly-descriptions-and-titles-still-photos-licensing/838/9)

> 3rd Video in 1st Row titled FEM Council of Berlin…  this is the Login, Identity & Wallets session which concludes with an affirmation toward a working group (name not determined).
>
>
> It begins at 8 minutes in, after your introduction and overview and some video crowd surfing.  A lively discussion ensues, with some key points surfacing such as questioning the reintroduction of trust by Maria from Golem at 17:32 after some musing that led to discussion of recovery mechanisms with Jarad of Status.
>
>
> There’s a reference to UPorts White Paper, I think this is the link for that? Account Suspended
>
>
> A nice redirect again back to the triumvirate of Wallets, Identities & Logins at 32:10 Boris…
>
>
> There’s a reference at 39:40 to something I cannot make out but would like to look into if anyone can clarify what that is, maybe it’s in notes or check with the speaker whom I could not identify.
>
>
> Some cool exchanges about Entities & Identities, Attention Paid / Acclaim / A Claim, Proof of Attention, Horizontal and Vertical Relevance context… then 15 minutes of wrapping up

uPort White Paper is deprecated, I think this is a pointer to all their stuff: [A Complete List of uPort’s Protocols, Libraries and Solutions | by Kames | uPort | Medium](https://medium.com/uport/a-complete-list-of-uports-protocols-libraries-and-solutions-63e9b99b9fd6)

[@ligi](/u/ligi) this is partially wallets, but I think logins & identity should be decoupled from wallets?

[@benjaminbollen](/u/benjaminbollen) thoughts on naming?

---

**compscidr** (2018-08-17):

Will there be any meetings about this in Prague? I would be interested to be learn more about what you all have been working on.

---

**kameir** (2018-08-18):

It seems unlikely that identity can (or should) be managed via a dApp. Identities should likely exist on the protocol level. Fundamentally each identity might be recognized as an oracle. Does it seem sensible to create a new classification for these?

---

**ageyev** (2018-08-21):

We created a service (like an oracle) for identity verification of Ethereum address/key owners on https://cryptonomica.net

To verify identity of Ethereum address private key owner user has to sign a simple message with his/her verified OpenPGP key (we have online verification service on our website), and send this message from his/her Ethereum address to our smart contract.

Then user requests our system to pull this signed message from smart contract and check it’s signature. If signature can be verified, our server puts user data (first name, last name, birthdate, nationality, OpenPGP key fingerprint, Ethereum address) to smart contract on https://etherscan.io/address/0x846942953c3b2A898F10DF1e32763A823bf6b27

User data from this smart contract can be read by other smart contracts and decentralized applications. Users can use verified identity to make legal binding and also legally enforceable contracts/documents on the Ethereum blockchain.

Ethereum address can be connected to one Cryptonomica verified OpenPGP key only, if OpenPGP key expires, user have to use another Ethereum address for new OpenPGP public key.

This service created to be as much smart contract developer friendly as possible. See smart contract verified code on etherscan: https://etherscan.io/address/0x846942953c3b2A898F10DF1e32763A823bf6b27f#code

