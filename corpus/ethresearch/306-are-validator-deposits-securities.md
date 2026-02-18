---
source: ethresearch
topic_id: 306
title: Are validator deposits securities?
author: kladkogex
date: "2017-12-10"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/are-validator-deposits-securities/306
views: 2974
likes: 11
posts_count: 17
---

# Are validator deposits securities?

Validators will profit from their deposits. The question is then whether validator deposits should be considered securities. The startup where I am working is building a p2p network where nodes will have deposits, so we have been researching this issue internally …

Howey test states that an investment is a security if

1. It is an investment of money
2. There is an expectation of profits from the investment
3. The investment of money is in a common enterprise
4. Any profit comes solely from the efforts of a promoter or third party

My take on this is that validator deposits should not be considered securities, since 4. is not satisfied - validators contribute efforts by running validator nodes.

Some of the later court decisions seem provide an alternate definition to 4., where “solely” is replaced by “primarily”. In other words,  if I deposit $1B with a validator, then some can argue that my efforts running the validator wll be insignificant vs. the profits I receive

As specified on page 19 of [“Howey Test Turns 64”](http://scholarship.law.wm.edu/cgi/viewcontent.cgi?article=1016&context=wmblr)

> The Supreme Court itself softened its stance and seemingly endorsed a
> more relaxed standard for the derivation of the expectation of profits by
> omitting the word “solely” from its explication of the Howey test in United
> Housing Foundation v. Forman,94 noting that the “touchstone is the
> presence of an investment in a common venture premised on a reasonable
> expectation of profits to be derived from the entrepreneurial or managerial
> efforts of others.
>
>
> Lower courts have considered whether “solely” means “only” in their articulation of the Howey test, and some
> courts have eased the rigidity of the need to have the profits derived solely
> from the efforts of others by including profits that come “primarily,”
> “substantially,” or “predominantly” from the efforts of others.

I wonder if any legal or economics experts could comment on that.

Note that other networks use alternative solutions.  For instance with Bitshares, my understanding is that owners of consensus nodes are paid a fixed amount ($70K/year), and do not have deposits. Since the payment is fixed and reasonably corresponds to the effort, then imho it is clearly not security …

## Replies

**Lars** (2017-12-11):

Caveat: Not an expert.

I would argue that case 2 isn’t fulfilled. That is, you will not get any profits from the deposit. It will only allow you to participate as a validator. If you only do the deposit, and nothing else, you know for sure you will get no profits.

From that point of view, I would say staking isn’t an investment, and thus point numer one isn’t fulfilled.

---

**kladkogex** (2017-12-11):

Lars - why no profit ?) I thought validators were paid in proportion to their deposits … Why would they deposit in the first place if they do not profit from it ?) Its like all risk and no fun then )

---

**Lars** (2017-12-11):

Right, you get paid in proportion from the deposit. But the payment you get is for doing validation, not for doing deposits. That is, you get payed from doing a work. The deposit is only there to make it possible to punish bad behavior.

---

**kladkogex** (2017-12-11):

Lars  - understood - it gets a bit murky though when a deposit is very large. If you load a truck-full of cash, drive it to a bank and deposit it, and then you are paid a percentage on the deposit, then yes, you did some work in the process, but very little compared to the investment so most of your income is arguably passive … ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**djrtwo** (2017-12-11):

(Not a lawyer ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=9))

A validator not only stands to gain a modest return on their deposit from their efforts, but a validator also stands to *lose* a substantial amount (-100%) from their efforts (or lack thereof). Because of this and operating under the assumption that losses are negative profits, I see #4 being clearly satisfied. Assuming 10% return on some time interval, the payout for the $1B validator ranges from $0 to $1.1B and where they fall on that massive range is almost entirely up to them. The other factors are the particulars of the reward/penalty mechanisms and how the other validators perform during that time interval, but these are insubstantial compared to the potential -$1B.

---

**jonchoi** (2017-12-12):

[@kladkogex](/u/kladkogex), thanks for opening this thread. Definitely important to address this.

*Typical disclaimer, I’m not a licensed financial professional or a lawyer*

[This release from the SEC today](https://www.sec.gov/news/public-statement/statement-clayton-2017-12-11) is now on my reading list.

Some highlights:

> Tokens and offerings that incorporate features and marketing efforts that emphasize the potential for profits based on the entrepreneurial or managerial efforts of others continue to contain the hallmarks of a security under U.S. law.

> Prospective purchasers are being sold on the potential for tokens to increase in value – with the ability to lock in those increases by reselling the tokens on a secondary market – or to otherwise profit from the tokens based on the efforts of others.  These are key hallmarks of a security and a securities offering.

So it’s dangerous and inaccurate to describe the validation process as simply “give us your ETH and you’ll get yield.” I’m actually considering renaming “yield” to “validation reward or revenue” and refer it to as “implied yield” explicitly when necessary.

The question becomes what is the validator actually doing in real life. We often personify the job of the validator to validate transactions, but validators will be running software that does the job. Also, there will be a relatively small number (probably less than 10?) of versions of the software that these validators will be running (@vbuterin2 and [@karl](/u/karl) should have better answers here).

So then, we have to think: **in what ways is getting x% implied yield as a validator different than buying a bond that pays a comparable yield?** Whether or not you receive a small reward per block time or receive a penalty or get slashed depends on the validator node running on your server being online and voting correctly. Also, theoretically speaking, anyone can build a client that can serve as a validator and whether these validators are protocol following nodes will determine the revenue of these validators.

So another way to think about this is that **validators are paying the network to participate in securing the network and get periodic revenue or incur prepaid expense depending on their performance** (and also their performance in relation to the group). Then the receive a rebate or return for the remaining balance.

**The main offline/physical element here is that the “validator” actually needs to maintain good uptime for the server that they’re running.**

And that brings up another tricky point: delegated validator pools. If you’re participating in a validator pool, then you delegate your ETH to another person who will run the validation node. And in that case, you will receive some sort of net return (series of revenues and expenses of the actual/direct validator) in return for ETH that you delegate for depositing to the actual/direct validator. This person participating in the pool is solely picking the right pool to enter and doesn’t do any work. In this case, the arguments above of not being a security doesn’t hold as well. (How does this work for bitcoin mining? I guess BTC miners are often private corporations and mining pools also require you to “bring your own hardware” which would still include action of the pool participant). If the validator pool worked in a way that you have to run some sort of software yourself and you are pooling via middleware, then the argument against it being a security would hold. If they’re just delegating money, then the pool itself is a company that is receiving an investment perhaps. However, the validation process itself ultimately needs servers running validation nodes with uptime and correct software, so it would not be a security.

Open to feedback.

---

**jonchoi** (2017-12-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/lars/48/14_2.png) Lars:

> I would argue that case 2 isn’t fulfilled. That is, you will not get any profits from the deposit.

Think 2 does hold. Let’s be real. Most people will participate to make money. Think it’s more #4 that is the question. (#2 doesn’t say participating automatically gives you money, it says you participate with the expectation of returns)

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> but a validator also stands to lose a substantial amount (-100%) from their efforts (or lack thereof)

This point doesn’t hold because look at subprime mortgages, high yield (akak junk) bonds, venture investments. Significant chance of (significant) capital loss is a feature that gives it high returns.

Again, I think it comes down to who are we calling the “validators” and what do they actually have to do. Elaborated in previous response.

---

**vbuterin** (2017-12-12):

This definitely does make me more in favor of having a yield-free, transaction fees only revenue model, though it’s not a hard distinction - you still have to vote to get paid in Casper FFG, so you can still argue it’s more like a virtual miner than a bond.

We can try to figure out how to go yield-free in full casper. IMO current tx fees (~$800k per day, ~0.6% of ETH market cap per year) are totally high enough for it to be viable.

---

**MicahZoltu** (2017-12-12):

I’m pretty strongly against sacrificing transparency, clarity, and technical purity to capitulate to a particular government with a particular set of rules that are (IMO) quite silly and arbitrary.  If some government decides it wants to label blockchains, or Ethereum, as something illegal it is well within their power to do so regardless how we try to tip toe around existing rules and regulations.  The regulators will just add new rules if that is what they desire.  We are trying to build a better future here and letting government agencies that don’t understand economics dictate how we build technical solutions or communicate those solutions with the public will not get us to the brighter future we are all working towards, it will lead us right back down into the hell we are in (though on a long slow path).

If people want to discuss whether Ethereum is a security or not, I think that is fine.  But that discussion should have *no* impact on how we build or communicate the Ethereum tech stack.

---

**vbuterin** (2017-12-12):

Definitely agree that we should focus on technical and economic excellence first and foremost. That said, there are good economic reasons to go more strongly tie validation to transaction fees. It’s a complicated debate with good arguments both ways; I suspect we’ll need to see how hybrid Casper FFG fares in the wild before making any decisions.

---

**kladkogex** (2017-12-12):

I think it is a good idea to be conservative.

Several weeks ago I had a call with a fintech expert from one of the top US law schools  (she does not want to be quoted on record). Her recommendation was to stay away from being classified a security as far as possible, because some of these things include criminal responsibility. I really got out of this call sweating ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Even if the probability of the  government going after this is 1%, accepting a 1% probability of going to jail is hard  to swallow ) The worst thing that can happen is that  a) a validator deposits money b) there is a slashing condition and the validator is slashed c) the validator goes to a district attorney and files a criminal fraud complaint that she was a victim of unauthorized securities offering.

As far a transaction fees a concerned,  if they are not tied to deposits, then one can provide strong arguments they are payments for the actual work determined by market forces.  Cryptocurrencies had transaction fees for years and very much represent a safe harbor in dealing with the government.

In the transaction model it is OK for validators to have reasonable size deposits. If I work for a taxi company, and the taxi company provides me a car, it is OK for it to require a deposit to be used in case of potential damages in case  I damage the car.

*Disclaimer: This is my personal opinion and  I am not a lawyer in any way …*

> We can try to figure out how to go yield-free in full casper. IMO current tx fees (~$800k per day, ~0.6% of  ETH market cap per year) are totally high enough for it to be viable.

Since the transaction fees are collected by miners,  each miner would be required to transfer a certain percentage  of transaction fees to the Casper contract as part of the minting transaction.

Then one would need to distribute this to validators somehow.  Since validators are supposed to be

long term participants, it is probably ok to pay validators monthly for checkpoints that have long been finalized (say three months ago). Each validator would have a fixed standard deposit, and payment to each validator would depend on the aggregated participation metric.

In this scenario some people would run multiple validators, each with the standard deposit, people would probably use docker containers for that.  This could actually contribute to security since compromise of a single container would not necessary mean compromise of all containers.

There would have to be a formula for the standard deposit where the size of the deposit would be adjusted slowly to target a certain number of validator nodes (say 500 nodes).

As an example, one could target a linear increase in validators going from 1 to 500 in one year.

The standard deposit for new validators would be adjusted every day.

If the current count of validators N is less than  500* (now - beginning_of_casper)/365, then the deposit would be increased by 1%, otherwise decreased by 1%.

After the count of validators reaches 500 one could switch to a formula that keeps validators around 500, for instance, set the deposit size as

D 2[[1]](#footnote-862-1)

Where D is the value of the deposit that was reached when the  count of validators first crossed 500

1. N/500 -1 ↩︎

---

**seth** (2017-12-14):

I am a licensed attorney, but I am not a securities lawyer and this is no way legal advice. Also please let me know if my technical understanding is incorrect in anyway.

That being said, from my understanding cases have usually come down to the fourth prong - **Any profit comes solely from the efforts of a promoter or third party**. When a person stakes their ETH, they are putting their ETH to “work” securing the network and seemingly play a large role in keeping the network running. Validator pools are definitely a bit murkier since the decision is delegated - however even with pools your ETH would still be conducting the work in securing the network (unlike regular investments which are usually converted or exchanged prior to being put to work).

Additionally, a court may also consider whether this has the qualities of a common security. On its face, staking ETH to validate the network and possibly get a reward does not appear to me to be a security. Additionally, from my understanding, you wouldn’t be selling your “validator” to get ETH in return. You would simply unstake your ETH-there is no transaction taking place.

The Investment Contracts and the Howey Test are clearly meant to capture investments beyond the standard stock, bond, etc. However, I think Validator deposits being a security is likely a stretch and is very different from the various ICOs selling stake in their companies or products.

---

**louie-louie** (2017-12-15):

Would it be possible to consider running your own validator node and participating in a validator pool as separate cases? Is there any benefit in doing so?

I agree with what you’ve said when it comes to validator nodes and the murkiness of validator pools concerns me. As a validator node I can lose money through my own actions, and that strengthens the case against #4. I also think someone could make the case that when a person makes a deposit to a validator pool their effort lessens.

When we apply the Howey Test who do consider the entity in question? The Ethereum Network or the Validator Nodes themselves?

---

**AFDudley** (2017-12-25):

I spend a lot of time talking to lawyers about the Howey Test, but I am not a lawyer and this is not legal advice.

Validators are running and maintaining hardware, their surety bonds (non-blockchain term for it) is clearly not a security.

If you have delegated stake, which will almost surely be required in any production PoS system, those delegation contracts are almost surely some type of security, depending on the conditions.

---

**varna** (2017-12-28):

I am more of a finance person - I.e not a lawyer but IMO:

- validators  are blocking an assst to guarantee their diligent performance of predefined work/tasks
- they may withdraw their asset from custody at any time given their proper performance
- they may lose part or in full their blocked asset if they did not perform the work/task properly or in full
- they may receive an incentive for performing their work/task which incentive is not guaranteed and may vary in amount, the incentive is in a form of an asset, there might be a third party dynamic calculator of such an incentive
- the asset of the guarantee and the asset of the incentive are not construed as a security or financial instrument themselves
Thus I believe the PoS validation structure is yet far away from securities laws or bank deposits laws.
Of course it much depends in what words or phrases it gets described and by whom - I.e is there an entity that may be viewed as an issuer or as a deposit gathering institution or as an agent of such.

---

**djrtwo** (2018-01-02):

I think that there is a worthwhile distinction between a pool and running your own validator node, especially if the pool is issuing some token related to the pool. ETH in that context might not be a security whereas the pool token (depending on the setup) could be.

