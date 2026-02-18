---
source: ethresearch
topic_id: 3278
title: Token Curated Wikis/Knowledge Bases
author: EazyC
date: "2018-09-08"
category: Applications
tags: []
url: https://ethresear.ch/t/token-curated-wikis-knowledge-bases/3278
views: 2113
likes: 7
posts_count: 7
---

# Token Curated Wikis/Knowledge Bases

I’ve been trying to come up with an interesting concept for a decentralized Wikipedia and would like some feedback/insights.

Say there is a wiki-space where there are some amount of editable wiki-type pages (with new pages created as well). Their states are tracked in a smart contract governed by some token T using a designated consensus method.

To participate, users stake their T tokens for a period P to vote on state changes to a wiki page or create new pages/edits. A state change is defined as a proposal to edit a document within the wiki-space (or to create a new page). The state change is represented as a hash of the document’s new state which points to a hash of the old state (forming a tree of the history of previous states of the wiki). These trees of hashes are stored on-chain. The actual wiki document itself and media can be either hosted centrally on CDNs or hosted through IPFS-type protocols by pinging the on-chain hashes that represent the pages’ states.

Users vote for the canonical state (meaning either the edit is accepted or rejected) through some selected consensus method. The canonical state voters are rewarded minted tokens at some rate R during each period P. The user who proposed the edit by creating the content is also rewarded some minted T at some rate D (assuming the new state was accepted). The idea is that as more users edit and curate the wiki-space, more T tokens are staked and removed from circulation to earn T token rewards for editing and curating content, the less will circulate in the market.

This system could be used for Wikipedia governed on Ethereum where every Wikipedia page is hashed and committed to the token curated wiki contract.

Some things to keep in mind that I’d like help/discussion on:

1. The consensus method used to decide on the state changes/edits of documents is difficult to formulate. Is it simple majority vote of the staking token holders? Or is it a more robust proof of stake system with some type of slashing conditions?
2. How are the rules decided for what types of edits/content is allowed into the wiki-space? That is a governance issue. Is it a free-for-all wiki or an encyclopedic/knowledge base wiki similar to Wikipedia, Wikia which needs standards for citations. This decision seems like it must be decided off chain by some signaling mechanism/social agreement among holders of T tokens.
3. Does the token mechanics work well? Would there need to be additional sinks that would not hinder the user experience?
4. In theory, Wikipedia.org could even start committing their edits to this network and earn T tokens if the token holders see value in the content produced.
(EDIT):
5. Essentially, the current state of the wiki-space is the current will of the presently-staking token holders. This makes attacking the system to insert propaganda expensive since it requires a large lockup of tokens. Since anyone at any point can propose an edit to remove biased content, an attacker can keep the content of the wikis biased only if they continue to stake/lock their tokens.

## Replies

**vbuterin** (2018-09-09):

My personal instinct on all this is, can we not go overboard assuming that “token curation” is even a viable paradigm at all until we get some evidence of how well it works for simple lists?

They rely on very strong assumptions about the behavior and motivations of the token holders, which seem quite suspect especially for highly subjective and high-verification-cost things like wiki cost. Also, incentives to attack the system for various political reasons are going to be large.

---

**EazyC** (2018-09-09):

> My personal instinct on all this is, can we not go overboard assuming that “token curation” is even a viable paradigm at all until we get some evidence of how well it works for simple lists?

Are you suggesting it’s not worth trying at least? Seems kind of defeatist to “wait it out” but I agree a token curated wiki is even more complicated than registries and what is to be learned about curating lists can likely be applied to token curated wikis.

> Also, incentives to attack the system for various political reasons are going to be large.

This is definitely true, especially for something where people go to form their world views and beliefs (ie: decentralized Wikipedia). Secondly, this is actually addressed in my model and I’ll make an edit to clear it up. Large stake is required to take part in changing any state of any wiki, so the economic cost of manipulating this type of dapp is extremely high compared to purchasing a few hundred thousand dollars of fb ads and disseminating fake election propaganda across the country. For example, in order for Coca Cola to change content on Pepsi and other soda wikis, they’d need large enough number of tokens to either be outright majority of the staking pool or at least enough to get their propaganda through (assume their tokens are distributed across many accounts so it’s not an obvious attack). Anyone can propose an edit to remove their biased content, and only if they continue to stake/lock their tokens can they keep the content of the wikis biased. As soon as Coca Cola unstakes and sells its position in the tokens and the current stakers wish to undo their edits, it’s trivially easy to do so. Essentially, the current state of the wiki-space is the current will of the presently-staking token holders. This makes attacking the system higher cost since in order to guarantee the content remains in the wiki-space, one must not unstake and sell their position in tokens. What other types of attacks do you see happening in your opinion? Propaganda is clearly the most obvious and serious one.

---

**vbuterin** (2018-09-09):

> Are you suggesting it’s not worth trying at least? Seems kind of defeatist to “wait it out” but I agree a token curated wiki is even more complicated than registries and what is to be learned about curating lists can likely be applied to token curated wikis.

Sure, but what if the thing that’s learned is that there is no way to make a token curated anything in a way that’s not attackable, except for the most trivial and objectively verifiable information?

Particularly, what if the right incentive structure ends up not even involving issuing a new token?

I’m not being defeatist, I’m just urging caution given that “token curated anything” is an as of yet completely untested primitive that relies on largely untested behavioral assumptions, and where they *have* been tested (particularly, token voting for blockchain governance) the results have not been too promising.

Basically, my advice is at this point to, at least to start off, throw out the assumption that “token voting on anything” will be part of the design at all, and start off with a broader question: how can (crypto)economic incentives be used to improve on the status quo of wikis? There’s many paths one can take with that question as a starting point.

---

**EazyC** (2018-09-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Particularly, what if the right incentive structure ends up not even involving issuing a new token?

It’s quite possible and likely. The main reason there is a token in this design is that the token itself is supposed to accrue value as more participants stake, curate, and edit the wiki-space. If the wiki-space becomes the “source of truth” like how Wikipedia is seen as quasi-fact (even though Wikipedia itself tells people not to think of it like that), then the tokens will be worth a lot. This basically creates a self-sustainable backend and the only part of the ecosystem that needs to be potentially monetized with donations/ads is the front end websites. I think that would be a very good economic step forward. Additionally, if sufficient front ends plug into the token curated wiki contract, there might not even need to be monetization on the front end if the traffic to the articles is sufficiently distributed across many websites/front end portals so the costs are not dropped on one centralized entity to bear (Wikimedia Foundation). The token is necessary for this type of vision, but you have a point that there could be more efficient mechanisms that don’t rely on a fundamental unit of account for the protocol.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> how can (crypto)economic incentives be used to improve on the status quo of wikis? There’s many paths one can take with that question as a starting point.

I’m actually curious what your thoughts on that is yourself. I’ve read Radical Markets and QV seems to be a possible avenue where the payment to vote more can be denominated in anything (like ETH and not necessarily a new ERC20 token). I also read your new paper with Glen but not sure how relevant it would be to improving wikis/Wikipedia tbh. What’s your own take?

---

**SRALee** (2018-09-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Sure, but what if the thing that’s learned is that there is no way to make a token curated anything in a way that’s not attackable, except for the most trivial and objectively verifiable information?

I tend to agree with this sentiment but just want to propose: If the staking period of a token curated ____ is sufficiently long, is it not rationale to assume that the staking token holders would want the price of the token to increase (or earn some revenue/fees) by the time their staking period ends? Now…I’m not saying if that were true that would necessarily imply that you would still get token holders to curate things the way that you hope. But, it does answer your concern that it’s not an impossibly difficult behavioral simulation to at least conclude that long staking periods encourage the stakers to increase the token price by the time their staking period ends. Again…in what ways it would encourage them is up for debate and not clear if they will curate lists/wikis/whatever but at least the first part of the equation is solved.

---

**EazyC** (2018-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/jseiferth/48/2281_2.png) JSeiferth:

> If the token is only designed for the contributing site only the supply is solved but how do average users contribute to the token value?
> They could f.e. Stake their Wiki-Tokens to articles they think are valuable to them, but besides that demand is voluntary.

There shouldn’t be any need to use the token for readers otherwise the entire system is more cumbersome and unnecessary than Wikipedia (which is completely free minus the donation campaigns). Read-only features should be completely free. I agree that it would be interesting to stake tokens on articles that you find important to you, although it’s voluntary. The other thing you could do is to stake your tokens and “delegate” your stake out to “thought leaders” or “editor pools” which you trust and have a particular viewpoint you agree with so that they upkeep the content in the same way that you think is valuable.

![](https://ethresear.ch/user_avatar/ethresear.ch/jseiferth/48/2281_2.png) JSeiferth:

> I think the attack-ability for objective information could be solved by designing a reputation system and let people who post new articles/ correct old ones stake x amount of token dependent on y their reputation score.

Not sure I understand this part, could you provide a direct example of how it would work so I can see a hypothetical case in action? Thanks.

