---
source: magicians
topic_id: 6557
title: An ice age in PoS - merits and potential implementation
author: yorickdowne
date: "2021-06-26"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/an-ice-age-in-pos-merits-and-potential-implementation/6557
views: 1472
likes: 9
posts_count: 12
---

# An ice age in PoS - merits and potential implementation

Placing this here from R&D Discord, for further discussion.

- General pros and cons of an ice age in PoS
- Technical implementation of same

Proposition: Implement an ice-age mechanism in PoS.

Rationale:

“If one desires no-change, then a default of no-change is a good idea.

If one desires change, then a default of change is a good idea.”

(Micah)

"The main things that I think people really want post-PoS are:

- Data sharding
- Statelessness + state expiry
- ZK-SNARKing the EVM and other state transitions
- Miscellaneous security upgrades like VDF oracle, proof of custody, etc

Account abstraction (can be done mostly-off-chain with flashbots-like techniques, so it doesn’t strictly require consensus changes (!!). And the cost of those changes above being delayed is definitely significantly lower than the cost of the merge being delayed."

(Vitalik)

Technical implementation ideas:

"

- IA kicking in could decrease the gas limit, so that throughput decreases and the chain becomes more and more expensive to use
- IA kicking in could probabilistically invalidate more and more block proposal slots, similar results as above
- IA kicking in could increase slot times. Simple as a concept, but probably hairy in the details due to the implicit assumption of currently perfectly regular 12s slots.

Delaying slots looks easy at first sight, but I’m not sure about what stuff implicitly depends on regular slots. And the regular slots are a bit too beautiful to touch them tbh

Invalidating slots might work, but I’m not sure if there is non-gameable randomness around to do so, so that it isn’t gameable by the other validators / block proposers.

But then it doesn’t even have to be random. Something like “slot x mod n is invalid”, where n is very large initially and then slowly decreasing could work."

(torfbolt)

## Replies

**_pm** (2021-06-26):

If there would be an ice age, it should be predictable. The current one is messy and it’s hard to predict when exactly it would kick in, or how much it would slow down the blocks.

---

**mightypenguin** (2021-06-28):

With ETH PoS, block timing and IAs should be much more predictable.

An extension to the idea of reducing the gas limit, the Block Reward should also go down.

After EIP1559 gas limit reductions won’t hurt block producers as much as a reducing Block Reward will.

This way, block timing and validity of blocks are not affected. Perhaps simpler to implement?

---

**HodlDwon** (2021-07-01):

I support the continuation of an Ice Age (IA) (aka Difficulty Bomb in PoW).

For scheduling, I think as the years go on, there will be less need for frequent forking / upgrades of the base layer. But we don’t want to permanently ossify when we don’t know what “finished forever” looks like, yet.

With that in mind, I was personally hoping IA would roughly double each time they are diffused.

As an example, from date of The Merge:

- First IA would happen in 1.5 years.
- Second IA would happen 3 years after the first (4.5 from Merge).
- Third IA would happen 6 years after the second (10.5 from Merge).

I wouldn’t suggest planning any further out than that, because there are just too many unknowns. If ossification is holding back regular upgrade forks, then we can reserve the right to keep the IA on a regular schedule perpetually. Or if upgrades aren’t having any coordination issues, we can keep extending if further and further into the future, demonstrating a stronger foundation for dApps and protocols to build on top of.

I don’t think the IA should have influence on regular upgrade forks, so a schedule of IAs should not be construed as the *only* forks that are allowed. I think upgrade forks should be at the whim of client devs to write and at the whim of users to adopt.

Pragmatically, Validators in some cases may be able to run both chains if they are cleanly forked away from each other, but dApps will likely have catastrophic choices to make between chains. For dApps the values of locked collateral cannot be equivalent on both chains. So I expect the chain will never actually split and that means the primary feature of an IA is as a protective anti-sybil mechanism for infrastructure providers.

This means bad actors cannot pretend there is significant support for the default state compared to an upgrade. They at least have to make the minimum effort of updating the infrastructure to handle the IA, and I think that alone is an important enough feature to keep the IA around for a while.

---

**mightypenguin** (2021-07-05):

Here are some major features on the horizon for Ethereum:

- “The Merge”
- Sharding
- Statelessness

Those alone should require 3-6 network upgrades.

So I would not be surprised if we easily need a network upgrade 1-2 times a year for the next 4 years.

---

**schone** (2021-07-05):

Did the original ice age ever do anything for Ethereum? It seems like all we ever did was diffuse/delay it since day 1 in 2015.

Not to say I don’t think the time we’ve taken to ship the consensus layer wasn’t a well spent endeavor in the end and has yielded a far superior product.  Still, the ice age in and of it’s own didn’t seem to do much other than be this toothless tiger.

---

**yorickdowne** (2021-07-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/258eb7/48.png) schone:

> Did the original ice age ever do anything for Ethereum?

It did. It made it so change was the default. Hard forks (feature changes) of Ethereum were deployed without a hitch, with everyone coming along. Without the ice age, block producers could just stay on the current software, which is their “path of least resistance”; with the ice age, they need to make a change no matter what - either update to the official client release or roll their own. “Official client release” is their path of least resistance, and so that’s what happened.

Similarly for the R&D / dev community, the looming ice age propels things forward a bit. There’s a deadline - a change needs to happen by then. It could be a minimal change that just moves the ice age, but while at it, what else is so close to done it can be finished and get in?

The ice age is 100% a social construct, it does not solve anything technical.

Hence Micah:

“If one desires no-change, then a default of no-change is a good idea.

If one desires change, then a default of change is a good idea.”

---

**schone** (2021-07-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yorickdowne/48/3120_2.png) yorickdowne:

> Similarly for the R&D / dev community, the looming ice age propels things forward a bit. There’s a deadline - a change needs to happen by then. It could be a minimal change that just moves the ice age, but while at it, what else is so close to done it can be finished and get in?

This part I can see.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yorickdowne/48/3120_2.png) yorickdowne:

> It did. It made it so change was the default. Hard forks (feature changes) of Ethereum were deployed without a hitch, with everyone coming along. Without the ice age, block producers could just stay on the current software, which is their “path of least resistance”; with the ice age, they need to make a change no matter what - either update to the official client release or roll their own. “Official client release” is their path of least resistance, and so that’s what happened.

This on the other hand, I never quite understood.  Suppose we had such a contentious fork that divided the community to 2 (we all know which one comes to mind).  From that moment on the term ‘official client’ is meaningless, because you have two chains competing with one another.  And given that, the old chain can now program whatever it wants to its chain to include the full diffusion of such a bomb.  So long as exchanges of all kinds lend legitimacy by allowing the trading of the newly divergent coin, people don’t know the difference and social contracts or not, all is up for grabs at that point.

---

**yorickdowne** (2021-07-05):

> Suppose we had such a contentious fork that divided the community to 2

Yes, of course. Forks can always happen. That’s not the scenario envisioned. The scenario here isn’t contention so much as being content - “this all works, why upgrade?” It’s just about making “some change has to happen now” the default. As a result, the Ethereum community as a whole is used to change, to upgrading clients regularly.

---

**HodlDwon** (2021-07-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/258eb7/48.png) schone:

> So long as exchanges of all kinds lend legitimacy by allowing the trading of the newly divergent coin, people don’t know the difference and social contracts or not, all is up for grabs at that point.

Consensus is like “Rock Paper Scissors”, as no one person has a monopoly on legitimacy in this or really any distributed community.

Devs can code anything (Rock)

Users can buy anything (Paper)

Miners/Validators can validate anything (Scissors)

Validators cannot run what isn’t coded.

Users cannot use what isn’t validated.

Devs cannot be paid in something users don’t ascribe value.

I can assure you that the Difficulty Bomb / Ice Age has ***absolutely*** worked to enforce the default of “change”. Given the only real world data we have, Bitcoin hasn’t released a hard fork in years and will never be forced to at a technical level. Ethereum codifies that at the *very least* we must diffuse the bomb to continue the network.

Having been around since the Genesis of Ethereum, I think it’s very dangerous to remove the Ice Age as we simply do not know how it could affect future community culture and or FUD around upgrade/hard forks.

---

**schone** (2021-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hodldwon/48/4224_2.png) HodlDwon:

> Ethereum codifies that at the very least we must diffuse the bomb to continue the network.

While I don’t have any better data to backup my claim, I believe that kind of thinking is almost analogous to superstition.  Let’s not change something because of how we think it has served us so far.  Going with that thinking we shouldn’t continue moving away from POW, we shouldn’t merge and we definitely shouldn’t EIP-1559.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hodldwon/48/4224_2.png) HodlDwon:

> dangerous to remove the Ice Age as we simply do not know how it could affect future community culture

Did we know how EIP-1559 was going to change the culture and usage of ETH as the 2nd biggest chain? Still approved it.  I contend that’s a much bigger change.

---

**MicahZoltu** (2022-08-10):

As far as timing goes, I personally prefer an ice age every ~7 months.  From my personal experience, the longer the time between releases, the more likely it is that your release process is broken in some way.  6 months is frequent enough that we are forced to continually exercise the process, but isn’t so frequent that people are spending all of their time on cutting/deploying releases.

Something like 3 years means that by the time you do a release, the process is probably broken in some way.

