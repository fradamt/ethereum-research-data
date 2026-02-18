---
source: ethresearch
topic_id: 466
title: Call-out assurance contracts
author: vbuterin
date: "2018-01-06"
category: Better ICOs
tags: [public-good]
url: https://ethresear.ch/t/call-out-assurance-contracts/466
views: 7708
likes: 11
posts_count: 15
---

# Call-out assurance contracts

The purpose of this post is to describe a coordination mechanism that could be used to better fund public goods in blockchain ecosystems, serving as an alternative to both pure individual donations and on-chain “public funding” schemes of the sort I criticize [here](http://vitalik.ca/general/2017/12/17/voting.html). The mechanism does NOT require any in-protocol features, so it could simply be “layered on top” of any existing blockchain.

The mechanism works as follows. Suppose that there is a currency (eg. ETH) with a set of accounts that have balances. Every period (eg. 1 week), a set of N (eg. N = 6) accounts is randomly selected (perhaps by choosing a random address and taking the nonempty account closest to it; note that the randomness should NOT be weighted by account balance). Suppose that there are M registered charities (anyone could register as a charity). Each of the N accounts is asked what percent of their tokens they are willing to contribute to each charity; that is, account i is required to provide a vector [p_{i,1}, p_{i,2} ... p_{i, M}]. At the end of the process, for each charity j, min(p_{1, j}, p_{2,j} ... p_{N, j}) (that is, the minimum of the percentages that the participants are willing to contribute to the charity) is computed. We can then determine the charity with the *highest* minimum percentage, and all participants are then required to actually contribute that percent of their balances to the charity.

For example, suppose that the charities are the Apple Fund, the Pineapple Fund and the Kumquat Fund, and the participants that are called out are Alice, Bob and Charlie. Alice specifies `{apple: 5, pineapple: 12, kumquat: 0}`, Bob specifies `{apple: 15, pineapple: 15, kumquat: 30}` and Charlie specifies `{apple: 40, pineapple: 10, kumquat: 9}`. The minima are `{apple: 5, pineapple: 10, kumquat: 0}`, so the end result is that Alice, Bob and Charlie all sacrifice 10% of their deposits to the Pineapple Fund.

The mechanism is fully voluntary, because anyone can avoid getting taxed by voting `[0, 0... 0]`, and because of this it can theoretically be implemented as a layer on top of existing blockchains (non-participation is equivalent to voting 0). However, there is an incentive to vote higher amounts, because by voting higher amounts you are not only potentially giving up your own money to the charity you vote for, but you also increase the money that the *other participants* end up giving up. In every case, an increment to your donation either (i) is a no-op (because someone else voted less) or (ii) donates your money to the charity with N:1 leverage (at least, if all balances are equal).

You might notice that this is similar to the old idea of assurance contracts; the only thing that really differs is the presentation, and the fact that a specific set of participants is “called out” rather than opening participation to everyone. The fact that participants are chosen randomly without taking into account balance, and then called out to give a percentage, is important; it ensures that:

1. Both wealthy and small holders find it attractive to participate, as wealthy holders are large enough that they very significantly benefit from public goods produced, and small holders get very high leverage on their donations
2. Coin holders get called out to donate an amount of funds that is, in expectation, proportional to their balances, so there is no incentive to try to “hide” from being called out by splitting one’s funds into many accounts or merging many users’ funds into one account

## Replies

**skilesare** (2018-01-06):

This is really interesting. In Catallax we have this problem where voluntary taxation is a capped part of a decay fee but we don’t want to limit what organizations people elect as taxing authorities.  That coupled with the problem that distributing decay to all elections at one time is expensive makes me think that there may be something here that is relevant to selecting the taxing authority in a random manner amongst one persons elections.  It is too late to think about more tonight, but I’m book marking to come back and think through it more thoroughly.

---

**turb0kat** (2018-01-06):

Funny i was just thinking about mechanisms a crypto-centric economy would need to fund governance in the real world.  This thought was triggered as I dreampt of government tax authority draining away in the face of truly private money (a brief and pleasant day dream).  Of course Vitalik, having the same thought, goes and solves the problem straightaway.

---

**nieldlr** (2018-01-06):

Heya [@vbuterin](/u/vbuterin),

I responded on Twitter to this briefly ([@nieldlr](/u/nieldlr) on there). I like this a lot. I thought I found a potential attack, but misread a few things. So all good! ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=9)

While I’m here, just a few more questions/thoughts. The subset of randomly selected N accounts. How does one determine the size of that? Do you have something in mind here?

Also, let’s say I’m the only one that signals for Peach Fund. And I never get chosen, or very seldom, like once a year, then my funding never gets to the charity. Do you have any thoughts on how one could mitigate this? Since then I’d rather donate directly through another mechanism so I know my funds do end up getting to them in a timely way. Some ways to make mitigate this:

1. increasing the subset of N,
2. decreasing the period (eg once a day?),
3. or perhaps one could create your own subset of users who will get randomly selected from?

One thing that’s useful in funding for me at least (why I’m building [StakeTree](https://staketree.com)) is having predictable income. In a system that’s random based on periods that are infrequent it could be hard to determine possible cashflow. For small projects & charities, this could be life or death of their organization.

Overall, I love the game around leverage related to the highest minimum. That is really awesome.

Keen to think about this about a bit more.

---

**vbuterin** (2018-01-06):

The purpose of this mechanism is not to fund a bunch of small charities that are individual donors’ favorite projects; that can be done with donations as is the case today. The purpose of this mechanism is to increase the level of funding given to reasonably popular charities that almost everyone has some degree of approval for. For example, I could see popular charities among ETH holders including (i) the Ethereum Foundation, (ii) a “citizen’s dividend” fund that splits all receipts evenly among all KYC’d addresses, (iii) client development teams, (iv) research teams, (v) non-Ethereum-related effective altruism groups, etc etc.

I’d definitely be interested in the problem of more effectively funding more speculative and possibly unpopular public goods, but that would likely require different mechanisms.

---

**vbuterin** (2018-01-06):

Also, I should add that the converse mechanism of weighting selection probability by address and having people specify funding amounts, rather than percentages, should also be tried. It seems to have less desirable properties on some dimensions (eg. less attractive for small holders to participate) but also it’s more clear and unambiguous that there’s no benefit or cost from merging or splitting funds.

---

**nieldlr** (2018-01-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The purpose of this mechanism is not to fund a bunch of small charities that are individual donors’ favorite projects; that can be done with donations as is the case today. The purpose of this mechanism is to increase the level of funding given to reasonably popular charities that almost everyone has some degree of approval for.

Ah. That clears things up a bit thanks! I could see this work for this use case. ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12)

---

**denett** (2018-01-06):

Since the voting is not weighted, doesn’t this encourage a Sybil attack? Create multiple accounts with small amounts and only vote for your preferred charity?

---

**h00701350103** (2018-01-06):

This system is vulnerable to a single bad actor in the pool that really despises a charity. If a single person is upset at the ETH foundation they can vote 0.0000000000000001 at them - out of spite (instead of a 0 vote) - to make sure they don’t get anything (or if they do get anything, very little).

Could be avoided by having [multiple] smaller pools, as well as a more complex function instead of min(), ie disqualify bottom X% (like, 2%) of non-0 votes and treat them as 0-votes. If X is sufficiently high, the charity maybe doesn’t deserve donations if >X% of the pool despises them.

If it’s a very controversial charity (think Wikileaks or something) they can probably raise donations through other means and point to the griefing as a reason to.

Another way would be to change the selection process such that past griefers aren’t selected, but I don’t immediately come up with an easy way to determine it (you cannot do the same as with previous solution, as consistently ignoring bottom x% would dry up the potential pool.) Griefers can also simply make new accounts.

---

**vbuterin** (2018-01-06):

This problem is fixed by keeping N not too large (eg. I think N = 8 could be reasonable).

---

**h00701350103** (2018-01-06):

right, but then the leverage gets weak[er]. The actors will also feel really singled out (though that might be positive, idk). With a big charity set and/or low rate of participation N=8 feels really low though, though I’ll wager you mean targeting leverage=8x and adjusting it for participation rate & rate of non-zero votes among charities (if 40 people all vote only for a single charity, split among 5 different, you get 8x on avg).

If doing *all* addresses as you suggested somewhere or with big pools in general I think one needs to address this in some way, but much less so with smaller pools for sure.

---

**mkoeppelmann** (2018-01-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Every period (eg. 1 week), a set of N (eg. N = 6) accounts is randomly selected (perhaps by choosing a random address and taking the nonempty account closest to it; note that the randomness should NOT be weighted by account balance). Suppose that there are M registered charities (anyone could register as a charity). Each of the N accounts is asked what percent of their tokens they are willing to contribute to each charity; that is, account ii is required to provide a vector [pi,1,pi,2…pi,M][p_{i,1}, p_{i,2} … p_{i, M}].

Just to clarify. Is an account ONLY asked to submit the vector when they are randomly selected?

I think the mechanism would be much better if each account has to upfront commit to a vector. Otherwise if a big account is randomly selected together with a bunch of very small accounts the big account has almost no leverage on their donation. If they commit to a vector upfront their expected leverage is at least still N*(average account size).

Communicating/committing to a funding preference might also have additional “prestigious”/“social credit” payoff.

---

**vbuterin** (2018-01-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> I think the mechanism would be much better if each account has to upfront commit to a vector. Otherwise if a big account is randomly selected together with a bunch of very small accounts the big account has almost no leverage on their donation. If they commit to a vector upfront their expected leverage is at least still N*(average account size).

Interesting! I haven’t thought about the pre-commitment approach. That could work really well, I’d have to think more about it.

---

**RhysLindmark** (2018-02-06):

I like this iteration of a bottom-up charity taxation system. AFAICT, this is a variant on an initiative the community is working on—the #CryptoPledge. You can imagine the #CryptoPledge as a meme/community that actively self-taxes themselves to give to various causes. It’s similar to other effective altruist pledges (Giving What We Can, FoundersPledge, The Life You Can Save, etc.).

One note on where the funds go: you can imagine your example charities as “buckets” that then have sub-charities within them. So I could donate to an EA bucket, and the funds within it would be donated to various EA causes (like EA funds). This is similar to Giveth’s [DAC + campaign model](https://medium.com/giveth/what-is-the-future-of-giving-d50446b0a0e4).

Finally, I have a slight instinct that these self-imposed taxation models will actually be the long-term future of funding public goods. See [Co-evolving the Phase Shift to Crypto Capitalism by Founding The Ethereum Commons Co-op](https://medium.com/@RhysLindmark/co-evolving-the-phase-shift-to-cryptocapitalism-by-founding-the-ethereum-commons-co-op-f4771e5f0c83).

---

**sinamahmoodi** (2018-09-16):

I find the idea really interesting, specially if combined with pre-commitment. When trying to think how it could work in **practice**, I faced a challenge. I’d appreciate any input or insight into this.

- It seems difficult to “call out” individuals. If this were to be implemented as a dapp, due to the extremely low probability of being called out at any point, even highly motivated people wouldn’t check the dapp every week to see if it’s their turn.
- Furthermore, the given parameters would likely result in one-time collection of a relatively large sum from each individual, which might result in more people opting out, than if it were small sums spread out over a more regular period.

One idea could be that, projects participating as a charity (e.g. wallets), could display a message when a user is called out, as they have an incentive to do so. But this might create an uneven ground for projects which don’t interact with end users directly. Moreover, to remedy the second point, **multiple** such "campaign"s could take place simultaneously.

