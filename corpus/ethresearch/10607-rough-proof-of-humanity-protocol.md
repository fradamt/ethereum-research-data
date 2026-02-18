---
source: ethresearch
topic_id: 10607
title: Rough Proof of Humanity Protocol
author: kladkogex
date: "2021-09-08"
category: Applications
tags: []
url: https://ethresear.ch/t/rough-proof-of-humanity-protocol/10607
views: 1676
likes: 3
posts_count: 4
---

# Rough Proof of Humanity Protocol

At SKL we are interested in solving the proof of humanity problem now even if roughly, because Dapps cant work well without a solution. I think many other blockchains are interested in this problem.

Basically, for fast and cheap chains you need to be able to enforce that your registered users are humans, otherwise you will have too many bots and DoS.

Google, FB etc are solving this problem using either SMS or email verification, but it is

- first centralized
- and second blockchain is passive, so it cant send an email or SMS.

So here is a practical solution, which is probably the best you can do at the moment for billions of users. It is based on Gmail signing message headers with Google public key (DKIP signatures)

1. A user sends a short email from Gmail to a relaying party on Internet, that posts this email to a smart contract on ETH-compatible blockchain. The relaying party is simply a reposting service, does not have security relevance and could be the user herself.
2. The email includes user public ETH key.
3. A smart contract verifies Google-signed email headers and then posts email/public-key pair on-chain.
4. To be roughly human means to have your email/public-key on chain
5. Thats it! We are looking for people that want to help us impement this as opensource library.
6. Also looking for more privacy-preserving tweaks to this.

## Replies

**lekssays** (2021-09-09):

I think that the first thing that should be shown is the usefulness of even roughly proving that an entity is a human because a user might just buy a lot of Gmail accounts and let his/her bots use them. So, the purpose of the proof is ambiguous. On the other hand, you mentioned the problem of privacy where emails will be mapped to ETH addresses, but I don’t think this problem will be fixed just with tweaks. For the headers, I think you meant DKIM signatures, right?

For the implementation, I’d love to contribute, but first the idea/protocol should be elaborated.

---

**subzerofx** (2021-09-10):

As [@lekssays](/u/lekssays) says => one can easily have multiple Gmail accounts. Also, not everyone has to have a Gmail account. On other hand most people have just one telephone number, and most people do have mobile phones so you could try go that route, not sure which exactly but of course first thing comes to mind is SMS verification, perhaps there are better, more reliable ways using ones mobile phone.

---

**Econymous** (2021-09-14):

oracles overlooking physical public (i.o.t.) infrastructure is the only way you’re going to get  identity on the blockchain

