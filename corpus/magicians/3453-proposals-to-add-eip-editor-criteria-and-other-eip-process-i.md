---
source: magicians
topic_id: 3453
title: Proposals to add EIP editor criteria and other EIP process improvements
author: jpitts
date: "2019-07-07"
category: Magicians > Process Improvement
tags: [eip-editors]
url: https://ethereum-magicians.org/t/proposals-to-add-eip-editor-criteria-and-other-eip-process-improvements/3453
views: 1279
likes: 2
posts_count: 4
---

# Proposals to add EIP editor criteria and other EIP process improvements

[loredanacirstea](https://github.com/loredanacirstea) has submitted a PR to EIP-1 proposing a selection process for EIP Editors.

https://github.com/ethereum/EIPs/pull/2172

There is also a [Medium write-up](https://medium.com/@loredana.cirstea/make-ethereum-future-proof-one-proposal-at-a-time-18b8b98b08fc) of this change, as well as a proposal to improve the EIP process itself.

> In addition, I am working on a decentralized solution to  randomly assign editors to EIPs and keep track of their work . My work, in its very early stages, can be found at https://github.com/loredanacirstea/eip-process.

The proposed improvement to the EIP pipeline involves a dapp and an approach to ensure attention on each EIP, “randomly assigning editors to Ethereum EIPs and keep track of their work.”

https://github.com/loredanacirstea/eip-process

## Replies

**boris** (2019-07-09):

[@loredanacirstea](/u/loredanacirstea) thanks for kicking this off. To recap, in the linked GitHub issue, several of us suggested that more process wasn’t needed, but rather just doing the work of regularly reviewing EIPs & ERCs.

> Basically, I believe the issue is actually recruiting knowledgeable people and asking them to commit time to do the work — not handing someone a title.
>
>
> If there were a line up of people begging for editor titles and/or tons of people consistently reviewing — this might be needed.
>
>
> If it were me, I would put effort into recruiting more people rather than adding process that it’s unclear what it solves.
>
>
> That’s my 2gwei. Good luck!

Here are some quick thoughts on ideas that might grow participation / how to participate more:

Subscribe to new GitHub issues / PRs by “Watching”

Leave a comment saying “I’m reviewing”

- this lets people know if anyone is working on a particular EIP

Run “what is an EIP / how do EIPs work” sessions at various conferences.

- Any in person conferences and Hackathons are good times for this

Hold a weekly EIP review / edit session

- Pick a time, gather in the EIPs Gitter
- Post chats as you edit / Review
- Have one or more existing editors there to approve PRs and do issue management

Run a weekly review of new EIPs

- post them here and on Twitter

Use GitHub issues for more categorization:

- if the current repo maintainers want to add new people (essentially more editors), then labels and other GitHub features could be used.

Related — I still have a PR in to add a full RSS feed of all EIPs. That handles them when they hit Draft on the website, not when they first get added to GitHub.

Anyway, the main thing is getting more humans involved. The bar for helping to correct EIPs into Draft is quite low. The next step of reviewing the technical content is probably about cross posting an announce here to the forum and promotion.

Also: I think Core EIPs have way different issues, so a lot of this mainly applies to ERCs.

---

**xinbenlv** (2019-07-09):

Thanks Boris for constructively polling the idea of campaign.

Can I add that:

It seems according to [this issue comment](https://github.com/ethereum/EIPs/pull/2172#issuecomment-508970296)  that “Editor to check technical soundness” is not a consensus.

Then can I say that at least “someone”(or some defined or undefined group of people) have to check / vet on technical soundness of an EIP - (is that a consensus?).

If that’s a case, we might also need to add a role / rule for checking that.

I propose, for tech soundness, if at least one EIP-final status author of same category step up and say LGTM for the technical soundnesss, and within the time range of last call no obligations, it’s being considered technically sound. If people have no consensus in technical soundness, then it blocks the Final-status bit until a technical soundness consensus ([similar to how Wikipedia gets consensus](https://en.wikipedia.org/wiki/Wikipedia:Consensus) check is reached.

---

**boris** (2019-07-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I propose, for tech soundness, if at least one EIP-final status author of same category step up and say LGTM for the technical soundnesss, and within the time range of last call no obligations,

That is a different discussion.

The process of getting EIPs to “Accepted” is the domain of the Core Dev process for Core EIPs.

Otherwise, for ERCs, it’s no “over my dead body” complaints during the “Last Call” period.

