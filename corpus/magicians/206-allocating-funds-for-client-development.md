---
source: magicians
topic_id: 206
title: Allocating funds for client development
author: charles-cooper
date: "2018-04-21"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/allocating-funds-for-client-development/206
views: 1594
likes: 1
posts_count: 4
---

# Allocating funds for client development

This is a follow up from https://github.com/ethereum/EIPs/pull/867#issuecomment-372858949 and partially copy/pasted from there.

A current issue in governance is that average users don’t have the resources to develop their own clients. Hence the veto power discussed for instance in [Reviewing the current EIP process](https://ethereum-magicians.org/t/reviewing-the-current-eip-process/33/15) is not that strong because, without access to development resources, users who want access to technical developments they do agree with must also opt-in to any other technical developments pushed forward by the development team of their client of choice.

I would like to float the idea of setting aside a portion of block rewards and/or transaction fees towards a development fund. That way ether holders and ether users (collectively, stakeholders) have a clear path towards funding client development wherein the developers will be financially aligned with the funders as opposed to the current regime where client teams may - or may not be - aligned with stakeholders. I’m not saying that the current client teams are doing a bad job. I’m saying that stakeholders should have direct and tangible representation in the development process. While similar in spirit to proposals like /t/querying-stakeholder-groups-as-part-of-governance-process/191/3 *, it differs in that it is facilitated by economic mechanisms rather than social mechanisms.

For the purpose of establishing representation for the different groups, the development funds generated from block rewards (which represent coin holders) could be segregated from the development funds generated from transaction fees (which represent coin users).

Some sort of carbon voting mechanism could be implemented where a user can specify where they would like their ‘portion’ of the funds directed towards. This makes it much less of an ‘all-or-nothing’ deal where users either get stuck with some big compromise that nobody really wanted or a majority inflicts their will on the minority. (Note: I think on a technical basis this is easier to track for block rewards and harder to track for txn fees, especially if users use multiple addresses - but ultimately, technically possible in both cases).

I imagine there could be N listed projects (with the barrier-to-entry of listing very low), and users can elect (possibly through a proxy) which projects they would like their portion of taxes/fees to go towards. If they do not take an election, the default is that the reward gets burned or goes to miners. An analogy with taxation would be like the bureaus publish their funding ‘wishlist’ and taxpayers collectively set the budget.

* Since I’m a new user apparently I can only put 2 links in a post.

## Replies

**MicahZoltu** (2018-04-21):

This has been discussed a bit previously, [@jpitts](/u/jpitts) has been the champion on that front I believe and can probably provide some links to other conversations and a summary of current status.

The problem with solutions like this is that there is nothing to stop people from just declaring *themselves* as the recipient of the funds so this effectively turns into a “donations” box rather than a system of taxation.  If you accept that this is just a donation box, then there is really limited advantage to making it part of the protocol (additional protocol complexity) rather than just having Ethereum clients have donation boxes of their own, separate from the protocol.

---

**cslarson** (2018-04-21):

[This](/t/querying-stakeholder-groups-as-part-of-governance-process/191/3) is the link that was missing.

Also, [this reply by Alex Van de Sande](/t/querying-stakeholder-groups-as-part-of-governance-process/191/2) I think relates to your suggestion - where it’s suggested that a portion of block rewards go to a fund that has some governance mechanism on top and therefore some agency and representation within the development process.

---

**jamesray1** (2018-04-28):

Note [EIP-908: Reward full nodes and clients for a sustainable network](https://ethereum-magicians.org/t/eip-908-reward-full-nodes-and-clients-for-a-sustainable-network/241).

