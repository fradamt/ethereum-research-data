---
source: magicians
topic_id: 1145
title: EIP-859 like ideas, approaches and dApp implementations
author: mariapaulafn
date: "2018-08-23"
category: Magicians > Primordial Soup
tags: [ux, meta-transactions]
url: https://ethereum-magicians.org/t/eip-859-like-ideas-approaches-and-dapp-implementations/1145
views: 1675
likes: 9
posts_count: 15
---

# EIP-859 like ideas, approaches and dApp implementations

We are creating a workshop sponsored by Golem for the community, happening during ETHBerlin.

[The workshop will feature a challenge around EIP-859](https://github.com/ethereum/EIPs/issues/859)

We will then present the outcome of the workshop at the UX unconference in Full Node, on the 10th. [@qnou](/u/qnou) can point you out there.

I started doing some reachout to devs and projects working on it. For now I got:

- @austingriffith with metatx: https://medium.com/@austin_48503/ethereum-meta-transactions-90ccf0859e84
- Gnosis Safe, in Beta provides this feature. Testing and excited! @koeppelmann
- Tenzorum that’s also on PK management. I can’t find their dedicated repo to token abstraction though.

Anyone else knows people? would love to gather projects with different approaches that help the discussion. The Workshop will be led by Golem UX, but [@qnou](/u/qnou), Hester & Patrik from Status, Karol and Pat from Colony,and Ben and Chris from 0x also helping out.

If you are already signed up for ETHBerlin, super invited to join us on this discussion! if you cannot make it and have a good project on this topic or similar, post here!

## Replies

**pet3rpan** (2018-08-25):

I was actually planning to conduct the a gasless transactions workshop for the ux unconf. The outline of it is going to  look like…

- What is product onboarding & user activation?
- Problems with web3 onboarding and user activation?
- Present the concept of gasless transactions and their capabilities
- How does it work?
 → Workshop would be to think how it could fit into the participant’s own project

While this workshop could be carried out by various participants, I want to run it at the ux unconf with designers since they are the ones discovering and solving a lot of the web3 ux problems. It would be about giving designers a new web3 tool and to begin the conversation around how they can be used.

I do think this workshop should be conducted at the unconf however I don’t see why we there shouldnt be a similar workshop before hand. The more the merrier imo. We could potentially present the outcomes of the first workshop after the conclusion of the 2nd and compare/contrast ideas/outcomes.

I am working on the product from Tenzorum and would also love to get involved with the discussion as well.

- The web3 ux community usually has discussions on a different forum, we would love for you and others to join the discussion there  http://discuss.conflux.network/

---

**mariapaulafn** (2018-08-26):

Hi [@pet3rpan](/u/pet3rpan) that’s cool, the Golem workshop was set for a few weeks and i started enquiring the teams last week on Twitter.

I think its totally fine to conduct both. the Golem presentation is on  EIP-859 challenge outcomes, i think it makes sense for you to go first, and then we have one of the talks. This is not the thread of the unconf so speak with [@qnou](/u/qnou) for that ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

You are invited to join the ETHBerlin workshop of course, you will have as much voice as anyone else. I spoke with someone from Tenzorum because im having my team check out everything I find however he told me you’re still not ready to open source which is totally fine, however, I can’t work without knowing more, for my workshop.

Chose to have the discussion here because my team is familiarized with this forum, and this is about this particular EIP, moreover, as I am organizing the whole of ETHBerlin, I need platforms I am already using, but happy to ellaborate on the UX forum once this is over.

This is not a UX discussion, that will take place live, I’m just gathering approaches to be able to form the curated workshop with the community mods.

---

**mariapaulafn** (2018-08-26):

Golem found the Status stuff on this too, https://github.com/status-im/contracts/blob/73-economic-abstraction/contracts/identity/IdentityGasRelay.sol

IDK if Hester and Patrick are on this forum.

---

**pet3rpan** (2018-08-26):

Awesome! Sounds good ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**hester** (2018-08-28):

Hi Maria, apologies for the wait. I’m usually more active on Conflux as well. Do you need any further info about the Gas Relay Issue? I don’t know the details of it, but can check with the creator. Let me know:)

---

**mariapaulafn** (2018-08-29):

Found this, guess you all know about it https://github.com/ethereum/EIPs/issues/865

---

**mariapaulafn** (2018-08-29):

No problem Hester, would be good to have some ideas to share in the workshop. Could you get in touch with the creator?

---

**hester** (2018-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariapaulafn/48/534_2.png) mariapaulafn:

> No problem Hester, would be good to have some ideas to share in the workshop. Could you get in touch with the creator?

Do you mean the creator of this issue? [contracts/contracts/identity/IdentityGasRelay.sol at 73-economic-abstraction · status-im/contracts · GitHub](https://github.com/status-im/contracts/blob/73-economic-abstraction/contracts/identity/IdentityGasRelay.sol)

If so yes I can reach out:) Let me know if that’s what you meant.

---

**mariapaulafn** (2018-08-29):

Yesss would be ace. Also check your mail ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**jpitts** (2018-08-29):

Just yesterday I created an MD page listing out links to initiatives and content relating to “meta-transactions”:


      [github.com](https://github.com/jpitts/eth-community-discussions/blob/master/meta-transactions.md)




####

```md
# Meta Transactions and Executable Signed Txns

Conceived by [Dr. Christian Lundkvist](https://twitter.com/ChrisLundkvist), meta txns enable users to interact with Ethereum without holding any ether.

## uPort
- [Making uPort Smart Contracts Smarter, Part 3: Fixing UX with Meta Txns](https://medium.com/uport/making-uport-smart-contracts-smarter-part-3-fixing-user-experience-with-meta-transactions-105209ed43e0) - Medium article
- [Meta Transaction Relaying Server](https://developer.uport.me/rest-apis/relay-server/)

Jim can use his private key to sign some data and then send this signed data to a relayer (which he has specifically given permission to forward his data). This relayer can then pay the gas for this transaction, and send the data through Jim’s proxy contract.

## Avsa / Executable Signed Transactions
- [The magic of executable signed messages to login and do actions](https://ethereum-magicians.org/t/erc-1077-and-erc-1078-the-magic-of-executable-signed-messages-to-login-and-do-actions/351) - post to the Magicians' Forum by [alexvandesande](https://github.com/alexvandesande)
- [ERC-1077](https://github.com/ethereum/EIPs/pull/1077) - Executable Signed Messages refunded by the contract
- [ERC-1078](https://github.com/ethereum/EIPs/pull/1078) - Log in / signup using ENS subdomains
- [Universal Logins for Ethereum - UX Unconf Toronto 2018](https://www.youtube.com/watch?v=qF2lhJzngto&feature=youtu.be) - youtube video

Allowing users to sign messages to show intent of execution, but allowing a third party relayer to execute them is an emerging pattern being used in many projects.

## Gnosis Safe
- [Website](https://safe.gnosis.io/)
```

  This file has been truncated. [show original](https://github.com/jpitts/eth-community-discussions/blob/master/meta-transactions.md)

---

**ChainSafe** (2018-09-01):

If possible, a few of us from ChainSafe would love to attend!

---

**mariapaulafn** (2018-09-02):

It’s an open workshop for all hackers, so definitely!

---

**mariapaulafn** (2018-09-02):

Thanks Jamie! Should i add the ones we found here?

---

**jpitts** (2018-09-17):

Oh I just noticed your comment [@mariapaulafn](/u/mariapaulafn) , please do ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

