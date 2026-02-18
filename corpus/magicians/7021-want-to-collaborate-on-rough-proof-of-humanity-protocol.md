---
source: magicians
topic_id: 7021
title: Want to collaborate on Rough Proof of Humanity Protocol?
author: kladkogex
date: "2021-09-08"
category: EIPs
tags: [identity]
url: https://ethereum-magicians.org/t/want-to-collaborate-on-rough-proof-of-humanity-protocol/7021
views: 1510
likes: 6
posts_count: 11
---

# Want to collaborate on Rough Proof of Humanity Protocol?

At SKALE we are interested in solving the proof of humanity problem now even if roughly, because Dapps cant work well without a solution.

I think many other blockchains are interested in this problem.

Basically, for fast and cheap chains you need to be able to enforce that your registered users are humans, otherwise you will have too many bots and DoS.

Google, FB etc are solving this problem using either SMS or email verification, but it is

- first centralized
- and second blockchain is passive, so it cant send an email or SMS.

So here is a practical solution, which is probably the best you can do at the moment for billions of users. It is based on Gmail signing message headers with Google public key (DKIP signatures)

1. A user sends a short email from Gmail to a relaying party on Internet, that posts this email to a smart contract on ETH-compatible blockchain.  The relaying party is simply a reposting service, does not have security relevance and could be the user herself.
2. The email includes user public ETH key.
3. A smart contract verifies Google-signed email headers and then posts email/public-key pair on-chain.
4. To be roughly human means to have your email/public-key on chain
5. Thats it! We are looking for people that want to help us impement this as opensource library.
6. Also looking for more privacy-preserving tweaks to this.

## Replies

**Socialgeeks** (2021-09-10):

This is a practical and useful solution towards mass adoption.  This would be a great way to verify individual wallets as human.  Sounds fantastic and really would love to follow this project closely!  Wishing you the best of luck ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

---

**ligi** (2021-09-12):

First of all: I agree this is an important problem to solve!

Unfortunately I do not see how your solution is more decentralized than google email verification (especially as you rely on Gmail here)

The best (most privacy preserving and hard to game) solution to the problem I found so far is [idena](https://idena.io) - what is really needed is a bridge to ethereum - there where some developed via gitcoin grants once - but they have been impractically expensive - maybe this should be reevaluated with L2s now.

---

**norswap** (2021-09-13):

I’m sorry if this is a stupid question, but I’m aware of https://app.proofofhumanity.id/

Is anything wrong/unsatisfactory with it? (I must admit I haven’t looked at how it works)

Regarding GMail specifically, while this would be a relatively good “whale deterrent”, it’s very easy to get many Google accounts. If you’re crafty, you can even scale/game this process up quite a bit. A startup I was briefly associated with used to order free/trial SIM cards by the dozen, and spawn Facebook accounts in order to advertise themselves.

---

**ligi** (2021-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png) norswap:

> Is anything wrong/unsatisfactory with it?

I think privacy there is a huge problem

---

**green** (2021-11-30):

There’s a solution in the works. It’s roughly something like this:

- Register as a human.
- Mint a fungible ERC-20 token that can only be minted once you’re accepted as a human
- Everyone uses a Tornado Cash-like protocol to mix these tokens up.
- Now you have the guarantee those tokens came from humans, but you don’t know which new wallet represents which human.

While you still have the privacy issue of you having to have your picture accessible on the blockchain, but you also unlock things like anonymous voting, that you can use for 1 person 1 vote, quadratic voting, etc…

---

**ligi** (2021-11-30):

That’s a nice idea actually. But I think it should still be on top of a system where you do not have to hold your face in a camera for it.  Really dislike that idea. Also think it can be attacked via deepfakes. Really like a system like idena more and see more future in there.

---

**mimoo7** (2021-12-01):

what about voice verification ?

---

**Tcharl** (2021-12-01):

Super idea to decentralize identity management, it’s pretty cool for ownership.

Just please, If you can keep the OAUTH2/OIDC/UMA standard in mind when implementing the APIs it would really encourage adoption

---

**poma** (2021-12-01):

The question is why do you feel the need to protect from bots? If submitting a valid transaction to the chain is undesirable doesn’t it mean that the economy of the chain is broken? If the distinction between bots and humans is important it’s likely than the transaction costs are not going to be covered by fees, but by some additional value extracted from the fact that users are humans.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> Google, FB etc are solving this problem using either SMS or email verification

This is just a first step. After a user is registered they monitor their behavior and ban accounts as soon as they notice something suspicious. It’s hard to allow fast bans like that without lots of centralization and some false positives. For any sms, email, or captcha based service it’s pretty easy to automate and register thousands accounts for just a few bucks.

---

**Obscuro** (2021-12-01):

Celo has solved this in an interesting way except using mobile numbers. Well worth a read of their [whitepaper](https://celo.org/papers/whitepaper) under section 2.

