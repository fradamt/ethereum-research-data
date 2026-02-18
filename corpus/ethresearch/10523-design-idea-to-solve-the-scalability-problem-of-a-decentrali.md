---
source: ethresearch
topic_id: 10523
title: Design idea to solve the scalability problem of a decentralized social media platform
author: estebanabaroa
date: "2021-09-07"
category: Applications
tags: []
url: https://ethresear.ch/t/design-idea-to-solve-the-scalability-problem-of-a-decentralized-social-media-platform/10523
views: 6429
likes: 7
posts_count: 16
---

# Design idea to solve the scalability problem of a decentralized social media platform

Ethereum gives us several tools to make a great social media platform: identity/login via public key cryptography, name system via ENS, tipping, token based rewards, token based voting/ranking/curating, etc.

The thing that’s missing is the ability to publish content for free, scale to millions of users, and view this content without spam (spam/sybil resistance).

I think I might have a solution for this that could be used to recreate 99% of the functionalities of a website like reddit.

It would use a pubsub gossip protocol (IPFS already has an experimental implementation of this). A gossip protocol allows peers to send messages to all other peers. Peers filter messages they wan’t/don’t want using “topics”. “Topics” are arbitrary strings. In this case they would be an ENS or public key that represent the name of the subreddit.

A user would sign and publish a subreddit thread/comment/vote through an HTTP provider in his browser, the HTTP provider would broadcast the message to the gossip peers using the correct “topic” (subreddit).

The admin/moderators of the subreddit would run a gossip peer that listens to this “topic” (his subreddit name or public key). They can filter spam automatically by requesting the user includes a captcha challenge answer with his thread/comment/vote. The captcha challenge URL would be up to each subreddit admin, most would use Google or Cloudflare captchas, or whatever effective captcha of the time. They can also filter spam manually, like regular subreddit mods.

The admin/moderators would then publish approved posts to a “name system” gossip protocol (IPFS has this, called IPNS). The “name system” is different from pubsub, only the owner of the ENS or public key can publish to the “topic”, instead of everyone. The “topic” is the ENS name or public key instead of an arbitrary string.

A user would view the content of the subreddit in his browser through an HTTP provider, the HTTP provider would query the name system gossip protocol for the name of the subreddit, and send the content to the user. If the user is running a native app, he doesn’t need an HTTP provider, he can be a direct gossip peer. If not, he can choose any HTTP provider, like Ethereum with Infura.

Anyone sees any problem with this design? I am interested in writing a whitepaper for it, if anyone wants to help, let me know (I can fund the initial development). My telegram is estebanabaroa and discord estebanabaroa#2853

## Replies

**estebanabaroa** (2021-09-16):

I wrote a short whitepaper for my idea:

**Plebbit: A serverless, adminless, decentralized Reddit alternative**

**Abstract**

A decentralized social media has 2 problems: How to store the entire world’s data on a blockchain, and how to prevent spam while being feeless. We propose solving the data problem by not using a blockchain, but rather “public key based addressing” and a peer-to-peer pubsub network. A blockchain or even a DAG is unnecessary because unlike cryptocurrencies that must know the order of each transaction to prevent double spends, social media does not care about the order of posts, nor about the availability of old posts. We propose solving the spam problem by having each subplebbit owner run their own “captcha server” and ignore posts that don’t contain a valid captcha challenge answer.

**Public key based addressing**

In Bittorrent, you have “content based addressing”. The hash of a file becomes its address. With “public key based addressing”, the hash of a public key becomes the address of the subpleddit. Network peers perform a DHT query of this address to retrieve the content of the subpleddit. Each time the content gets updated, the nonce of the content increases. The network only keeps the latest nonce.

**Peer-to-peer pubsub**

Pubsub is an architecture where you subscribe to a “topic”, like “cats”, then whenever someone publishes a message of topic “cat”, you receive it. A peer-to-peer pubsub network means that anyone can publish, and anyone can subscribe. To publish a post to a subplebbit, a user would publish a message with a “topic” equal to the subplebbit public key (its public key based addressing).

**Captcha server**

A “captcha server” is a URL that prompts the user to perform a captcha challenge before a post, then sends him a valid signature if completed successfully. The captcha server can decide to prompt all users, first time users only, or no users at all. The captcha server implementation is completely up to the subplebbit owner. He can use 3rd party services like Google captchas.

**Lifecycle of creating a subplebbit**

1. Subplebbit owner starts a Plebbit client “node” on his desktop or server. It must be always online to serve content to his users.
2. He generates a public key pair, which will be the “address” of his subplebbit.
3. He sets up a captcha server of his choice. It must also be always online to server his users.
4. He publishes the metadata of his subplebbit to his public key based addressing. This includes subpebblit title, description, rules, list of public keys of moderators, and the captcha server url
Note: It is possible to delegate running a client and captcha server URL to a centralized service, without providing the private key, which makes user experience easier, without sacrificing decentralization.

**Lifecycle of reading the latest posts on a subplebbit**

[![5](https://ethresear.ch/uploads/default/optimized/2X/3/39d5d33c86906b3a54c500509ed7f2520056a420_2_690x331.png)51588×764 32.4 KB](https://ethresear.ch/uploads/default/39d5d33c86906b3a54c500509ed7f2520056a420)

1. User opens the Plebbit app in a browser or desktop client, and sees an interface similar to Reddit.
2. His client joins the public key addressing network as a peer and makes a DHT query for each address of each subplebbit he is a member of. The queries each take a several seconds but can be performed concurrently.
3. The query returns the latest posts of each subplebbit, as well as their metadata such as title, description, moderator list and captcha server URL.
4. His client arranges the content received in an interface similar to Reddit.

**Lifecycle of publishing a post on a subplebbit**

[![4](https://ethresear.ch/uploads/default/optimized/2X/9/92e5b4207eda3fb320acbe1fa411de12e3ab9009_2_690x341.png)41688×836 28.3 KB](https://ethresear.ch/uploads/default/92e5b4207eda3fb320acbe1fa411de12e3ab9009)

1. User opens the Plebbit app in a browser or desktop client, and sees an interface similar to Reddit.
2. The app automatically generates a public key pair if the user doesn’t already have one.
3. He publishes a cat post for a subplebbit called “Cats” with the public key “Y2F0cyA…”
4. The app makes a call to “Y2F0cyA…” subplebbit’s captcha server. The captcha server optionally decides to send the user a captcha challenge. User completes it and includes the captcha server’s signature with his post.
5. His client joins the pubsub network for “Y2F0cyA…” and publishes his post.
6. The subplebbit owner’s client gets notified that the user published to his pubsub, the post is not ignored because it contains his valid captcha server signature.
7. The subplebbit owner’s client updates the content of his subplebbit’s public key based addressing automatically.
8. A few minutes later, each user reading the subplebbit receives the update in their app.
9. If the user’s post violates the subplebbit’s rules, a moderator can delete it, using a similar process the user used to publish.
Note: Browser users cannot join peer-to-peer networks directly, but they can use an HTTP provider or gateway that relays data for them. This service can exist for free without users having to do or pay anything.

**What is a “post”**

Post content is not retrieved directly by querying a subplebbit’s public key. What is retrieved is list of “content based addressing” fields. Example: latest post: “bGF0ZXN0…”, metadata: “bWV0YWRhdGE…”. The client will then perform a DHT query to retrieve the content. At least one peer should have the data: the subplebbit’s owner client node. If a subplebbit is popular, many other peers will have it and the load will be distributed, like on Bittorrent.

**Peer-to-peer pubsub scalability**

A peer-to-peer pubsub network is susceptible to spam and does not scale well. Pubsub peers who spam messages without a valid captcha server signature can be blacklisted. And captcha server urls can be behind DDOS protection services like Cloudflare, so it should be possible for subplebbit owners to resist spam attacks without too much difficulty.

**Captcha server lifecycle**

1. The app loads the captcha server URL in an iframe before publishing a post. This URL is operated by each subplebbit owner individually.
2. The server sends a visual or audio challenge and it appears inside the iframe.
3. The user completes the challenge and sends his answer back to the server.
4. If the challenge answer is correct, the server sends back a digital signature for the post.
5. The user can now include this signature with his post, and when the subplebbit owner encounters that post in the pubsub network, he knows it is not spam.

**Conclusion**

We believe that the design above would solve the problems of a serverless, adminless decentralized Reddit alternative. It would allow unlimited amounts of subplebbits, users, posts, comments and votes. This is achieved by not caring about the order or availability of old data. It would allow users to post for free using an identical Reddit interface. It would allow subplebbit owners to moderate spam semi-automatically using their own captcha server implementations. It would allow for all features that make Reddit addictive: upvotes, replies, notifications, awards, and a chance to make the “front page”. Finally, it would allow the Plebbit client developers to serve an unlimited amount of users, without any server, legal, advertising or moderation infrastructure.

---

**estebanabaroa** (2021-10-02):

After getting some feedback I have added 2 new sections:

**Censorship resistance of the captcha server**

Captcha servers are not as censorship resistant as a purely P2P network, because it requires a direct connection to some HTTP endpoint. If this endpoint is blocked by your ISP or DDOSed, then you can’t connect. These attacks can be mitigated in a few minutes by changing the captcha server URL of your subplebbit, or using DDOS protection like Cloudflare. In a pure P2P network, if some peer is blocked by your ISP or DDOSed, some other peer should be available. A pure P2P captcha server solution seems impossible at this time because requesting a captcha challenge is not deterministic, so how would peers in this network deterministically block a bad peer spamming captcha challenge requests? If a solution for a P2P captcha server is found it should be attempted.

**Using anti-spam strategies other than the captcha server**

The captcha server can be replaced by other “anti-spam strategies”, such proof of balance of a certain cryptocurrency. For example, a subplebbit owner might require that posts be signed by users holding at least 1 ETH, or at least 1 token of their choice. Another strategy could be a proof of payment, each post must be accompanied by a minimum payment to the owner of the subplebbit. This might be fitting for celebrities wanting to use their subplebbit as a form of “onlyfan”, where fans pay to interact with them. Both these scenarios would not eliminate spam, but they would bring them down from an infinite amount of spam, to an amount that does not overwhelm the pubsub network, and that a group of human moderators can manage. Proof of balance/payment are deterministic so the P2P pubsub network can block spam attacks deterministically. Even more strategies can be added to fit the need of different communities if found, but at this time the captcha server remains the most versatile strategy.

---

**illuzen** (2021-10-12):

Glad to see people are giving this topic serious thought. Some feedback:

- Ethereum has / used to have a communications network called whisper that had a topics system with bloom filters and even metadata privacy. I’m not sure what happened to it, I think it died of neglect, but there’s some important pieces of the solution in there.
- We should consider “how do we transition people gracefully from existing social media” to be a fundamental part of the problem statement. An amazing system that nobody uses is not a solution.
- We should make a universal format or convention of social media data that can describe all the stuff people do on social media, so that we can start to decouple that data from the social media companies. Social media companies can still exist but they shouldn’t own the data, they should instead compete on organization of that data for human consumption. I’m thinking of something like RSS feeds.
- It’s basically impossible to tell whether a user is human or not. Sybil resistance has to come from expending some kind of limited resource like electricity (proof of work) or money (proof of stake) or time (VDF). Ideally we design the system so it’s mostly irrelevant whether a user is a bot or not. This could be something that clients (socmed cos) compete on.

Basically I would recommend refining the scope of the problem to make it easier to build and adopt.

---

**estebanabaroa** (2021-10-17):

> It’s basically impossible to tell whether a user is human or not.

I think captcha/sms verification is a reasonable way to reduce spam to a human manageable amount. The only problem is each “owner” of a community has to run a public HTTP endpoint, because you can’t request a captcha challenge p2p since it’s not a deterministic request.

> something like RSS feeds

I don’t think an open standard that with a federated approach is enough. Back in the day people used RSS, then Twitter came along and used RSS too. Then once Twitter had captured enough users, it shut down RSS and killed it. IMO the entire network must be serverless and open, like Bittorrent or Bitcoin, so that no one can “embrace, extend, and extinguish” it.

---

**fryorcraken** (2021-10-22):

*Note: I can only post a limited number of link, ping me if there is anything you cannot find*.

Hi,

Excellent thoughts.

# Waku

As [@illuzen](/u/illuzen), mentioned, Whisper was designed to solve some of the problems you exposed. However, Whisper had a number of caveats in practice and was abandoned.

We are building Waku as a successor of Whisper. Waku is a network and family of protocols to enable decentralized, censorship-resistant, off-chain communications.

Waku Relay shares some of the characteristic your described: a gossipsub protocol with (content) topic tagging that help clients filter messages.

We are also looking at novel ways to enable spam protection such as RLN (Rate Limiting Nullifiers).

This is similar to the “owning 1 ETH” strategy, apart that zk tech allows us to **not** link the message sender to their Ethereum address.

You can find more of the Waku v2 specs here: https://rfc.vac.dev/. Comments are welcome on the matching GitHub.

FYI, Waku v2 is our rewrite of the protocol on libp2p stack. Waku v1 was the first version that was a mod of Whisper build on devp2p.

We currently have several implementations:

- nim-waku: as a backend/adaptive node
- js-waku: for web app integration
- go-waku: for integration in the Status app

We are currently working in improving our documentation and websites.

In the mean time, feel free to check [this presentation](https://www.youtube.com/watch?v=rQOp3qoDF0g&list=PLUt355rCCNrSxfYwIRdUMEeuMrgAEoBbF&index=17).

Who are we, we are the Vac research division at Status and we building Waku as a public good because we believe the Ethereum ecosystem needs a decentralized, censorship-resistant and privacy-friendly communication network.

I am happy to answer any question or help you build a PoC using Waku. Also keen to hear whether you would consider using Waku to be build a social platform.

# Status Communities

At Status, we are also building Status Communities on top of Waku v2. The design of Status Communities shares some of the properties that were highlighted such as payment integration for a celebrity/content creator. Let me know if you want hear more about it.

Kind regards,

F

---

**estebanabaroa** (2021-10-24):

After a conversation with [@fryorcraken](/u/fryorcraken) I realized that a full captcha challenge request-anwser-validation actually is deterministic, and could work over P2P. If a peer or IP address relays too many captcha challenge requests without enough correct captcha challenge answers, it gets blocked from the pubsub, deterministically. The captcha challenge request alone is not deterministic, but the entire exchange is. This would require the subplebbit owner’s peer to broadcast the result of all captcha challenge answers, and for each peer to keep this information for some time.

So the “captcha server” over HTTP in the original design can be replaced for a “captcha service over peer-to-peer pubsub” design, which would make the entire design of Plebbit peer-to-peer. I will post an update to the entire redesign soon.

---

**estebanabaroa** (2021-10-24):

**Captcha service over peer-to-peer pubsub**

An open peer-to-peer pubsub network is susceptible to spam attacks that would DDOS it, as well as makes it impossible for moderators to manually moderate an infinite amount of bot spam. We solve this problem by requiring publishers to first request a captcha challenge from the subplebbit owner’s peer. If a peer or IP address relays too many captcha challenge requests without providing enough correct captcha challenge answers, it gets blocked from the pubsub. This requires the subplebbit owner’s peer to broadcast the result of all captcha challenge answers, and for each peer to keep this information for some time.

Note: The captcha implementation is completely up to the subplebbit owner. He can decide to prompt all users, first time users only, or no users at all. He can use 3rd party services like Google captchas.

**Lifecycle of publishing a post on a subplebbit**

[![4](https://ethresear.ch/uploads/default/optimized/2X/b/b29d19c23beca09e85e41ba1dfb8060838462381_2_690x341.png)41688×836 34.2 KB](https://ethresear.ch/uploads/default/b29d19c23beca09e85e41ba1dfb8060838462381)

[![6](https://ethresear.ch/uploads/default/optimized/2X/8/84214675b0e672dae8d4c27d4011b156195be6bf_2_690x341.png)61688×836 34.4 KB](https://ethresear.ch/uploads/default/84214675b0e672dae8d4c27d4011b156195be6bf)

1. User opens the Plebbit app in a browser or desktop client, and sees an interface similar to Reddit.
2. The app automatically generates a public key pair if the user doesn’t already have one.
3. He publishes a cat post for a subplebbit called “Cats” with the public key “Y2F0cyA…”
4. His client joins the pubsub network for “Y2F0cyA…”
5. His client makes a request for a captcha challenge over pubsub.
6. His client receives a captcha challenge over pubsub (relayed from the subplebbit owner’s peer).
7. The app displays the captcha challenge to the user in an iframe.
8. The user completes the captcha challenge and publishes his post and captcha challenge answer over pubsub.
9. The subplebbit owner’s client gets notified that the user published to his pubsub, the post is not ignored because it contains a correct captcha challenge answer.
10. The subplebbit owner’s client publishes a message over pubsub indicating that the captcha answer is correct or incorrect. Peers relaying too many messages with incorrect or no captcha answers get blocked to avoid DDOS of the pubsub.
11. The subplebbit owner’s client updates the content of his subplebbit’s public key based addressing automatically.
12. A few minutes later, each user reading the subplebbit receives the update in their app.
13. If the user’s post violates the subplebbit’s rules, a moderator can delete it, using a similar process the user used to publish.
Note: Browser users cannot join peer-to-peer networks directly, but they can use an HTTP provider or gateway that relays data for them. This service can exist for free without users having to do or pay anything.

---

**MicahZoltu** (2021-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/estebanabaroa/48/7094_2.png) estebanabaroa:

> The thing that’s missing is the ability to publish content for free, scale to millions of users, and view this content without spam (spam/sybil resistance).

Spam and sybil resistance are two separate problems, and should be solved separately.

Sybil resistance is only needed if you need some guarantee of one account per human, but it is unclear to me why a social media network needs such a thing.

Spam protection can be achieved by just making posting content a non-free operation.  I know people like “free”, but remember that if it is free then *you* are the product and in a privacy friendly social media platform the user should not be the product.  Micro transactions can make it so each post costs $0.01 (or whatever).  You don’t need a very high cost to put a significant dent in spam.  Email spam, for example, gets sent by the millions so even a $0.01 per email would result in very significant costs to the spammer and force them to at least do more targeted spamming.

---

**janmajaya** (2021-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/estebanabaroa/48/7094_2.png) estebanabaroa:

> If a peer or IP address relays too many captcha challenge requests without providing enough correct captcha challenge answers, it gets blocked from the pubsub.

I believe blocking IP address of spammers isn’t effective, since switching IP addresses is somewhat easy. Plus, I think this can evolve into a cat & mouse problem where developers keep coming up with new ways to block bad IPs (like blocking a range of IP addresses & more & more) and bad actors keep improving on their attacks. Thus, a relatively simple way would be to use micro transactions per post, mentioned by others.

For content moderation, the solution that moderators assigned to a pleebbit will simply delete violating content does not seems scalable. I would recommend you to check out [Vitalik’s post](https://ethresear.ch/t/prediction-markets-for-content-curation-daos/1312) on using prediction market to scale content curation. I am also developing a platform that uses prediction markets for content curation, and I believe should a good way to test such a system with real users. Would love to collaborate on this!

Also, I believe it’s unnecessary to have sybil resistance in social networking platform. Rather a well defined reputation signalling system, good content moderation, and use of something like micro transactions for spam protection should be a good starting point.

---

**estebanabaroa** (2021-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/janmajaya/48/6753_2.png) janmajaya:

> I believe blocking IP address of spammers isn’t effective, since switching IP addresses is somewhat easy

It is effective in the context of preventing an attacker from DDOSing a P2P network, which is what it’s used for here. Blocking IPs is how all P2P networks prevent DDOS.

![](https://ethresear.ch/user_avatar/ethresear.ch/janmajaya/48/6753_2.png) janmajaya:

> the solution that moderators assigned to a pleebbit will simply delete violating content does not seems scalable

We already know it’s scalable, It’s how Reddit, 4chan, Telegram groups and Facebook groups work. Moderators are not assigned by the creator of Plebbit. Just like on Reddit, anyone can make their own subplebbit without asking permission from anyone, and then assign their own moderators. It is infinitely scalable.

---

**estebanabaroa** (2021-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Spam protection can be achieved by just making posting content a non-free operation.

Using captchas over peer-to-peer pubsub is a superior solution than “pay to post”. “Pay to post” has 3 insurmountable problems:

1. If the amount to post is too small, like less than 1c, spammers will simply pay it and absorb the cost.
2. If the amount to pay is too high, like $10, non-spammers will not want to pay it. There is no perfect price point that will deter spammers but not non-spammers.
3. Only people who have self-custody cryptocurrency can use your app, which is almost no one in 2021.

I believe captchas (or arbitrary challenges) over peer-to-peer pubsub solve this problem perfectly. The owners of their communities can use any captcha (or challenge) implementation they want, to solve whatever spam their community is facing. I also believe that a “pay to post” and “proof of fund” option should be available, because those are very useful in certain scenarios, like a community created around a token.

Also note that the plebbit design only works for social medias where “owners” create and moderate their own communities, this includes Reddit, 4chan, Facebook groups, Telegram groups, etc. It does not work for social medias like Twitter, Instagram, TikTok, Youtube, etc.

> but remember that if it is free then you are the product

Captchas over peer-to-peer pubsub allow free without you being the product.

> Email spam, for example, gets sent by the millions so even a $0.01 per email

A 1c cost would not deter a spammer in a Reddit design, because the attacker has much more information about the target, they can read their post history and target only people they want, unlike email which they must mass send. If an attacker could write infinite Reddit comments for only 1c each, he would make an immense return on investment and would never stop spamming. And since Plebbit is a Reddit alternative, 1c would not work. Neither would $1, or $10, because regular users wouldn’t pay it.

An arbitrary captcha is great because once a spammer figures out how to profitably solve the captchas, with AI or some human captcha solving farm, the community owner can change the captcha to some other type of captcha, and the spammer has to start his work from 0 again.

---

**MicahZoltu** (2021-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/estebanabaroa/48/7094_2.png) estebanabaroa:

> An arbitrary captcha is great because once a spammer figures out how to profitably solve the captchas, with AI or some human captcha solving farm, the community owner can change the captcha to some other type of captcha, and the spammer has to start his work from 0 again.

I believe this assumes that it is cheaper to generate captchas than generate captchas solvers.  I’m not certain this is true?

---

**estebanabaroa** (2021-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I believe this assumes that it is cheaper to generate captchas than generate captchas solvers. I’m not certain this is true?

If you make the challenge hard enough, neither AI nor human captcha farms will be able to solve it, no matter how hard they try. For example certain communities on Reddit require that your account is 60 days old and that you have 500 karma.

The “challenge” can be anything, it doesn’t have to be a captcha, it could be a minimum account age, minimum karma amount, an SMS verification, etc. It’s up to the community owner.

Just like on Reddit, communities that are heavily under attack will have to sacrifice user friendliness. But some subs are less profitable to attack and anyone can post there. It doesn’t seem to affect the popularity of Reddit at all so hopefully it will be the same for Plebbit.

---

**SionoiS** (2021-10-26):

Great thread!

I would like to add that in behavioural economics “free” vs not free as been studied and the perception difference is immense. Understanding human beings is a must for any designer.

![:wave:](https://ethresear.ch/images/emoji/facebook_messenger/wave.png?v=10) [@estebanabaroa](/u/estebanabaroa)

---

**estebanabaroa** (2022-03-30):

2 new sections have been added to the whitepaper:

**Improving speed of public key based addressing**

A public key based addressing network query is much slower than a content addressing based one, because even after you find a peer that has the content, you must keep searching, in case another peer has content with a later nonce (more up to date content). In content based addressing, you stop as soon as you find a single peer, because the content is always the same. It is possible to achieve the same speed in Plebbit, by having public key based addressing content expire after X minutes, and having the subplebbit owner republish the content after the same X minutes. Using this strategy, there is only ever one valid content floating around the network, and as soon as you find one peer that has it, you can deterministically stop your search.

**Unlinking authors and IP addresses**

In Bittorrent, an attacker can discover all the IP addresses that are seeding a torrent, but he can’t discover the IP address of the originator of that torrent. In Bitcoin, an attacker can directly connect to all peers in the network, and assume that the first peer to relay a transaction to him is the originator of that transaction. In Plebbit, this type of attack is mitigated by having the author encrypt his comment or vote with the subplebbit owner’s public key, which means that while the attacker can know the peer published something, he doesn’t know what or from what author.

