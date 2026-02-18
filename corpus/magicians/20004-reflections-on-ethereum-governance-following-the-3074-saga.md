---
source: magicians
topic_id: 20004
title: Reflections on Ethereum governance following the 3074 saga
author: derek
date: "2024-05-14"
category: Magicians > Process Improvement
tags: [governance, eip-3074]
url: https://ethereum-magicians.org/t/reflections-on-ethereum-governance-following-the-3074-saga/20004
views: 880
likes: 6
posts_count: 6
---

# Reflections on Ethereum governance following the 3074 saga

I wanted to share my reflections on Ethereum governance following the 3074/7702 saga.  [@vbuterin](/u/vbuterin) and [@yoavw](/u/yoavw) kindly reviewed the article, though views are my own: https://docs.zerodev.app/blog/3074-governance

My overall thesis is that Ethereum governance doesn’t work the way people think it does.  There’s the explicit governance power that is the ACD, but there are also other implicit governance powers.  When the powers clash, something like the 3074 saga happens.

So in this blog, I try to identify the implicit governance powers and propose a mental model for thinking about Ethereum governance.  I also make some suggestions on what we can do better going forward.

See the twitter thread for a summary, but I highly recommend reading the full blog: https://twitter.com/decentrek/status/1790392200121225577

## Replies

**MrSilly** (2024-05-15):

Thoughtful summary. Re suggestions for improvement, I’d argue it would best to avoid voting altogether. Mathematicians don’t vote on proofs. Scientists don’t vote on theories. Consensus emerges in those communities by arguing until agreement is reached.

Introducing voting begs the question of who can vote, how votes are weighted, how many votes are required to pass a decision. If we’re not careful instead of being influenced by those who are best at making good arguments, we’ll end up handing over governance to an insular committee led by those who those best at playing politics.

---

**Mani-T** (2024-05-15):

A thoughtful and detailed analysis. This could lead to a more robust and transparent governance process for Ethereum.

---

**derek** (2024-05-15):

Are you referring to how I pointed out that the core devs were the only governance power that could “vote” relative to other governance powers?  I definitely agree that ETH governance shouldn’t be done via voting; I just put “votes” in quotes to point out that, despite influences from other governance powers, at the end of the day only the core devs could implement protocol updates.

---

**MrSilly** (2024-05-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/derek/48/12233_2.png) derek:

> at the end of the day only the core devs could implement protocol updates

Does “core dev” really have a well defined coherent meaning, or is it just some nebulous term we borrowed from Bitcoin, which doesn’t have a governance problem because it doesn’t have any governance. In Bitcoin the question of who calls themselves a core dev is inconsequential. If someone wants the honor fine, there’s no point in arguing with them about it because it doesn’t give them the power to change the rules of consensus.

Importing this uncritically to Ethereum may bake in some hidden unsafe assumptions that are worth examining. It’s possible that the status quo of client devs being a governance power would not make sense in a world where client development was more decentralized and diverse.

One could argue that client devs having special governance powers is a bug, not a feature. That ideally, they’d be equal participants in an emergent consensus process. That the only power they should have over changes to the networks rules of consensus is the power to make good arguments, just like everyone else participating in the process. The influence of all participants should be based on their ability to persuade others on the merit of their arguments, not on any special privileges they have over a particular repo.

Otherwise if “core devs” actually have governance powers, we have to think hard about who counts as a core dev. Consider what would happen if we had 3 forks of every client joining ACD calls? Is every dev that commits code to one of these repos a core dev? If we accepted that definition, it wouldn’t be too hard for an adversary to manufacture as many core devs as was needed to overwhelm the ACD process, especially if any actual voting is happening.

Sadly, there does seem to be some actual voting taking place in the inclusion calls.

Under the hood, Ethereum clients are just open source projects supported by various sources of public good funding. Having dedicated most of my life to open source projects, I understand how a developer can confuse stewardship with ownership. “What we’re given to administrate we frequently believe we own”, but Ethereum clients have been funded by the community and they belong to the community. It’s safer if developers that undermine the emergent consensus process have their legitimacy and funding transferred to other developers that don’t assert any special governance powers to settle disputes.

The simple fact is anyone can contribute to any repo or maintain a fork. You couldn’t formalize a credibly neutral governance process that gave client devs special powers because you’d be cornered into anointing some repos as the official canonical ones as soon as the absurdity of the design started getting exploited and too many clowns started showing up as core devs and demanding that their vote also be counted. It only makes sense if you don’t think about it too hard, or if there are never any important disagreements. If we are going to discuss governance, we should be intellectually honest and not sweep governance under the “core dev” rug.

---

**MrSilly** (2024-05-17):

Some more thoughts re committees, voting and mitigating groupthink.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> If we’re not careful instead of being influenced by those who are best at making good arguments, we’ll end up handing over governance to an insular, authoritarian committee led by those who those best at playing politics.

It may not start out that way, but that’s where the political game often ends up, especially when the rules of the game are not carefully designed to prevent it. This can happen with the best of intentions.  Some skilled technologists form a loosely defined coordination group, and there’s nothing much at stake so self selection works fine. People participate for the right reasons initially but as the group gains powers, it gets more attractive to the kind of people attracted to power. To keep the signal to noise ratio high, a boundary between insiders and outsiders forms. The group is no longer equally open to all.

As soon as a boundary forms, there is a border that needs to be defended. Insiders increasingly worry about diluting their influence and losing control. Instead of  appreciating outsiders as sources of upside (eg new good ideas, valid criticism of bad ideas), outsiders become potential barbarians at the gate that could breach the walls seeking their share of the loot.

The group’s attitude drifts towards downside protection. The more concerned insiders becomes about the threat posed by outsiders, the more vulnerable they become to those claiming they can defend the group and pandering in defense of their special privileges. Ultimately, we can end up with a closed group trapped in an echo chamber, practicing groupthink and being led by a cynical demagogue. Each step down this path can seem perfectly reasonable. This is how many good things fail.

So the fewer borders we have around “governance” the better. The threat of voting on ACD is a downstream consequence of ACD forming a boundary separating insiders from outsiders.

On a related note in the future I hope we experiment with forms of debate that intentionally try to break down the insiders/outsider distinction and set up conditions for allowing the best ideas to bubble to the surface. This might look like zk-snarked forums that anonymize the source of arguments and counter-arguments while still preventing the debate from being sybil attacked by sock puppets and guaranteeing that we are giving our attention to real human beings. To the degree that noise / spam becomes a problem, a built in prediction market could be used to boost signal. If done right, it could mitigate bias and groupthink, nudge participants towards evaluating arguments purely on merit and make it harder to take mental shortcuts such as deferring to authority.  Kind of like how music academies have blind auditions.

