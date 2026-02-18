---
source: magicians
topic_id: 2140
title: "Constrained Resource Clients: Dec 2018 Update"
author: shazow
date: "2018-12-06"
category: Magicians > Primordial Soup
tags: [light-client]
url: https://ethereum-magicians.org/t/constrained-resource-clients-dec-2018-update/2140
views: 2808
likes: 18
posts_count: 16
---

# Constrained Resource Clients: Dec 2018 Update

Greetings!

I’d like to start a semi-regular update thread with the participants of our Constrained resource Clients ring. The purpose of these threads is to get a clear idea of what everyone’s goals are and where on the roadmap each project is. With any luck, this will help us find opportunities for better collaboration and interoperation.

*Quick recap:* We’re talking about Ethereum clients that can run under constrained resource conditions, such as on phones or browsers or even embedded devices.

### What I plan to do with these updates:

As the contact person for this ring, I will:

- Catalog and mention (or reach out) to founding participants for their own projects’ update.
- Once all updates have been posted, I’ll collate action items across teams and follow up.
- Repeat every few months (~quarterly?)
- Anything else you’d like me to do?

### What I’d like from the participants with each update:

- Short summary: What is your project and its goal? (This can change over time)
- Roadmap now: What is the currently working and available to try?
- Roadmap next: What is being worked on over the next few months?
- Current challenges and concerns: Do you need help with anything? Are there unknowns you’re accounting for that could be nailed down by another participant?

## Participants

To all projects mentioned: Please post an update as described above.

- Denode: @noot @ChainSafe @ansermino
- Go-Ethereum (LES): @zsfelfoldi
- Infura: @ryanschneider @egalano tueric
- Mustekala: @dryajov
- Slock.it: @CJentzsch
- Status: @mandrigin
- Vipnode: shazow
- WallETH: @ligi

If you’re hit with a link/mention limit, format the excess ones in plaintext.

If you’d like to join this list, please go ahead and post your update and I’ll make sure to explicitly include you next time.

(Won’t let me post with everyone mentioned, so some people aren’t.)

## Replies

**shazow** (2018-12-06):

I’ll go first,

### Short Summary

[Vipnode](https://vipnode.org/) is building an economic incentive for running full Ethereum nodes which service light clients. It works by providing a coordinator (a vipnode pool) which connects paying clients with participating hosts.

### Roadmap: Now

Beta just released this week. The demo pool is running for MainNet nodes with payments on Rinkeby.

- Instructions to try it here: https://github.com/vipnode/vipnode#quickstart
- Recent blog post: https://medium.com/vipnode/vipnode-progress-update-3-16b07037d3b3

### Roadmap: Next

Roughly in order of priority:

- Onboard some users and polish towards a stable release. Getting close!
- Integrate with a wallet: The current demo is wallet-agnostic (working with geth/parity) which makes the whole user experience somewhat clumsy. A native wallet integration with vipnode could make the entire onboarding ~transparent.
- Reduce trust in vipnode pools: Right now, the trust model of vipnode pools is the same as mining pools: The pool operator can run away with the deposit balance. Need to find a fee-efficient way to do many-to-many microtransactions. Traditional state/payment channels don’t work well here because there could be many pairs with very low balances but a non-trivial total balance.

### Challenges and Concerns

- Need help finding LES wallets to try integrating vipnode with. (Talking with WallETH and Status, but the more the merrier!)
- Need to investigate if the LES/ULC protocol will “Just Work” with Vipnode out of the box. (Any here hints appreciated!)
- Need to investigate about integrating the vipnode flow with other “constrained resource clients”. (Do vipnode pools even make sense for Mustekala? Or in3?)

(Any questions/suggestions are welcome, by the way!)

---

**mandrigin** (2018-12-07):

(had to trim links due to “only 2 links/post” rule)

### Short Summary

[**Status**] — a mobile Ethereum OS for iOS an Android.

### Roadmap: Now

This week:

- Wrapping up the Constantinople-enabled LES client: https://github.com/status-im/status-react/pull/6877
- A roadmap to functional LES & ULC in Status: https://github.com/status-im/status-react/issues/6905

### Roadmap: Next

- Bugfixing, a lot of it.
- ULC mode.

### Challenges and Concerns

- Initial sync speed of LES
- Battery consumption on sync
- geth node doesn’t work well with just sporadic network connections (a mobile app is mostly offline/sleeping and “wakes up” just for a few minutes at a time).
- …and many more bugs to squash

---

**dryajov** (2018-12-11):

### Short Summary

[mustekala](http://musteka.la/) is a light client and a libp2p based network for browser based or otherwise resource constrained environments.

### Status

- We just announced the project at devcon4
- Have an initial prototype that demonstrates overall pipeline

can query account balances
- can execute vm calls and run contracts in browser
- retrieval and parsing of slices

new slice related RPC calls in full clients
- slice propagation in the libp2p based KSN network

initial implementation of the KSN network and high level [pubsub protocol](https://github.com/MetaMask/kitsunet-docs/pull/1)

### Roadmap

- build out the KSN network and deploying to a subset of live users (metamask)

currently we have a scaled down version running over real browser nodes

tuning and scaling KSN
cleaning up and polishing the [PoC](https://github.com/metamask/kitsunet-js)

### Challenges and Concerns

- Incentivization in the KSN network as well as full nodes - https://github.com/MetaMask/kitsunet-docs/issues/4

we would love to hear ideas on how to incentivize both data availability in full nodes and well as adding security through incentivization to the KSN network, please share you’re thoughts here or in the issue above.

scalability of the browser based network

- through our preliminary research and experiments have been very encouraging, scaling the network is one of the hardest and most critical parts of this project

---

**zsfelfoldi** (2018-12-14):

**Short summary**

LES (Light Ethereum Subprotocol) is the first “light client” protocol for Ethereum. Its most complete implementation is part of the Go Ethereum client (Geth) and this is also where the latest features are first introduced.

**Roadmap now**

A huge PR has just become ready for review which improves LES server mode significantly:



      [github.com/ethereum/go-ethereum](https://github.com/ethereum/go-ethereum/pull/18230)














####


      `master` ← `zsfelfoldi:fc-simtest4`




          opened 03:34PM - 02 Dec 18 UTC



          [![](https://avatars.githubusercontent.com/u/9884311?v=4)
            zsfelfoldi](https://github.com/zsfelfoldi)



          [+3690
            -984](https://github.com/ethereum/go-ethereum/pull/18230/files)







This PR
- replaces the existing request cost estimation method with a benchmark[…](https://github.com/ethereum/go-ethereum/pull/18230) which gives much more consistent results
  - this also means the server can now estimate its own serving capacity properly and limit the number of accepted clients if necessary. Until now the allowed number of light peers was just a guess which probably contributed a lot to the fluctuating quality of available service.
- reimplements flowcontrol.ClientManager in a cleaner and more efficient way, with added capabilities:
  - better bandwidth control which allows using the flow control parameters for client prioritization
  - allowing target utilization over 100 percent at full load (parallel request processing allows this but the old client manager logic could not handle it)
  - reducing total serving bandwidth during block processing
- implements parallel LES request serving even for a single peer (a requirement for the new client manager logic)
- implements a simple private API for LES servers allowing server operators to assign priority bandwidth to certain clients and change prioritized status even while the client is connected
- adds a unit test for the new client manager
- adds an end-to-end test using the network simulator that tests bandwidth control functions through the new API

Note: there is a plan to implement in-protocol payment using the SWAP payment channel. This PR provides most of the functionality needed to implement such a feature. While the actual payment protocol is being developed the API can already be used and tested with other payment schemes (like a simple monthly subscription using on-chain payments).

Note 2: this PR is based on https://github.com/ethereum/go-ethereum/pull/17948

See also: https://gist.github.com/zsfelfoldi/93792da3c56dffdb594ff91aebd74262












These improvements and rewrites prepare the servers for incentivized operation by improving performance, making bandwidth control more precise and introducing a private API to control individual client priorities. Though there are in-house plans for introducing an in-protocol payment mechanism, the API is intended to be usable by any project implementing any kind of incentivization or prioritization scheme for LES.

A proposal will also be released shortly that describes a simple and efficient many-to-many payment channel protocol that is based on a probabilistic approach, does not require a complex infrastructure and is easy to integrate into LES.

**Roadmap next**

The next step is to improve the “server pool” of the Geth light client with more sophisticated server performance estimates in order to be able to compare the value-for-money that different servers offer. These metrics will be used by the integrated automatic server selection algorithm and also exposed through the API to be usable by externally implemented strategies.

Also, the planned payment protocol should be reviewed and discussed. If we find it suitable then we can start experimenting with its implementation soon (the implementation itself is not extremely complicated).

**Current challenges and concerns**

We should definitely improve communication with other teams and find ways to converge efforts (hopefully this forum will help). Finding efficient ways to follow each other’s progress and catalyze collaboration is an important meta-problem itself because human attention capacity is limited and the number of great projects is growing quickly.

---

**dryajov** (2018-12-21):

Should we set up a call where we can meet and discuss our different approaches? Is there one already happening that I’m not aware of?

---

**shazow** (2018-12-21):

[@dryajov](/u/dryajov) I think that’s a good idea, I’m kind of waiting until all the participants respond before we plan further. I wanted to give everyone a chance to become aware of the different projects and do some offline research. I’d love to schedule a call in the new year though.

Still waiting for updates from:

- Denode: @ChainSafe
- Infura: @ryanschneider
- Slock.it: @CJentzsch

A helpful progress bar: ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9)![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9)![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9)![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9)![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9)![:black_heart:](https://ethereum-magicians.org/images/emoji/twitter/black_heart.png?v=9)![:black_heart:](https://ethereum-magicians.org/images/emoji/twitter/black_heart.png?v=9)![:black_heart:](https://ethereum-magicians.org/images/emoji/twitter/black_heart.png?v=9)

![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=9)

(I understand that some people aren’t working on the holidays. I’ll defer further bugging until the first week of January.)

---

**shazow** (2019-01-09):

Happy 2019 everyone!

One final ping for updates:

- Denode: @ChainSafe
- Infura: @ryanschneider
- Slock.it: @CJentzsch

I will attempt to bug people out of band also, but otherwise we will move forward with the existing participants.

Also do we want to schedule a call? If so, we should put together an agenda for topics we’d like to discuss.

- Schedule a ring participants call
- Too early for a call

0
voters

---

**ryanschneider** (2019-01-09):

We (Infura) don’t have any explicit CRC projects we’ve gotten to the roadmap stage on yet, but are hopeful that CRCs can help offload some of the reliance on our RPC endpoints.  We’re very interested in supporting these efforts, and in providing infrastructure for CRC-related services, and hope to have some more CRC-related related work we can announce later.

We are also targeting rolling out `eth_getProof` support later this month, and are particularly interested in more ways we can facilitate validation for CRC clients.

---

**noot** (2019-01-15):

## Short Summary

Denode is an incentive mechanism for running full nodes.  It aims to provide both a free and a subscription-based service coordinated through a DAO.  There is also a p2p layer that will be used to join the network.

## Roadmap

I am currently working on the p2p layer based on libp2p. [@ansermino](/u/ansermino) is working on the DAO side of things.  We’re finishing up our research and ideation and beginning to implement.  We would like to have an alpha release sometime in the next few months once a bit more work has been done.

## Challenges

Assignment of users to nodes, will likely try to solve this by having users connect to groups of nodes.  Another issue that hasn’t really been solved is how to validate full node state.  A way to validate the node could be to ask for some info only a full node has, but there isn’t a way to determine whether they got this info from another node or not.

As well, I think we definitely need to communicate more with other teams to see how we can collaborate.  Definitely would be interested in having a call with everyone here at some point ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

---

**shazow** (2019-01-25):

Alright let’s schedule a call.

Anyone have suggestions for tools to coordinate scheduling for a distributed group like us? Maybe the week of Feb 18, right after ETHDenver? (I won’t be there but if anyone else is going, feel free to meet up!)

---

**mandrigin** (2019-01-28):

Week of Feb 18 works for me.

---

**shazow** (2019-02-10):

I made a doodle thingie to try and lock down a date when most people can coordinate into a call (let’s say 30-60min).

https://doodle.com/poll/3fw2gmzfa452b4fi#calendar

It’s for the week of the 18th, times are in PST (California) so please adjust accordingly. I’ll DM/post a hangout link once we have something resembling consensus. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

(Suggestions very welcome if there’s a better way to do this.)

---

**shazow** (2019-02-18):

Alright, I’m calling it: Thursday Feb 21, 2019 at 10am PST.

We have at least three people OK that time, I’ll try to coralle a couple more, but let’s see how this goes. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Please set a reminder for yourselves, I’ll post a call link here just before and/or I’ll try to send calendar invites for people whose emails I have. Feel free to DM me your email to get an invite!

---

**shazow** (2019-02-21):

Hey everyone, it’s call day!

In about 1hr15min I’ll be hanging out at ~~https://hangouts.google.com/call/~~, come one come all.

I’ll write up meeting notes and share them here after, for anyone who missed it.

Edit: Call is over. Notes coming shortly.

---

**shazow** (2019-02-21):

Notes from the call:


      [docs.google.com](https://docs.google.com/document/d/1PaxW7SXwOyzxL5dH9NAv9HS9xJn0oAP3dp7fnc6DZHI/edit)


    https://docs.google.com/document/d/1PaxW7SXwOyzxL5dH9NAv9HS9xJn0oAP3dp7fnc6DZHI/edit

###

Ethereum Magicians: Constrained Resource Client Ring Call on Feb 21, 2019 Discussion: https://ethereum-magicians.org/c/working-groups/constrained-resource-client-ring Agenda Quick intro and 2 minute project update. Any real-world examples of a...








If you weren’t able to make the call and wanted to add a quick update, you’re very welcome to post it as a comment in this thread.

I will be starting another CRC working group update thread in March (probably 2nd week), so get crackin’ on some cool stuff to update us with. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

