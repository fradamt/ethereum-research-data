---
source: ethresearch
topic_id: 4202
title: Attributing rent cost
author: clesaege
date: "2018-11-10"
category: Economics
tags: [storage-fee-rent, hibernation]
url: https://ethresear.ch/t/attributing-rent-cost/4202
views: 5241
likes: 14
posts_count: 21
---

# Attributing rent cost

Following [DRAFT: Position paper on resource pricing](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838) here are a few though on rent.

The problem I see with rent is “who should pay for it?”.

Letting anyone pay the rent for a whole contract have the issue that the cost is not attributed to the resource consumer.

For example for a token contract, someone could split its balance into a lot of accounts, taking a large amount of storage, thus increasing the rent which must be paid for the contract.

A potential solution to it would be to have storage affected to an account which should pay for it. In the case of a token contract, the data would be stored in state[token_holder][token_contract]. Only token_contract could write there, but token_holder would have to pay the gas for it. If he doesn’t his balance would become inaccessible and he would have to pay the wake-up cost.

Separating this storage by contract, allows a token holder to choose which rents he want to pay (otherwise we would have the opposite problem, contracts writing to its storage in order to increase the account rent). In term of user experience, this could be done smoothly by putting a rent deposit when the user use the contract.

If the user fails to pay the rent only this user is affected.

In token contracts, the problem looks quite simple, but for more complex contracts, allowing a user to render the storage related to him inacessible by not paying could be problematic (concrete example: in the Kleros contract if a the staking slot of a user is not accessible, the contract would not know which account is drawn and would not be able to penalize the corresponding user for failing to vote).

A solution would be to require users to prefund an “hibernation” fee which would be used to pay the execution cost of an action when storage goes into hibernation (in the case of the Kleros contract, it would be destroy all locked tokens of this account and unstake all remaining tokens).

That would introduce new challenges in smart contract development (having to specify a hibernation procedure and not always being able to rely on storage being available).

## Replies

**vbuterin** (2018-11-11):

I agree this is a challenge, and I’d say it’s the single major challenge remaining in designing rent schemes! Here’s an overview of ideas we have now:

- Require each contract to have a fixed small storage size (eg. <= 4096 bytes). If you need infinite-sized mappings for your application, you can create a new contract for each entry, where the contract’s address would be based on what mapping and what key you are accessing, and the contract’s code would be a simple code that allows the parent contract to read and write the value inside. Mapping read/writes would then turn into contract calls. This allows mapping entries to be separable from each other and individually pay rent, hibernate and wake. Note that ENS is essentially architected this way already.
- Put storage into a Merkle tree, and only store the root inside the contract. Users would have to process historical data to figure out what Merkle branches to use client-side, and the network would only need to bother with O(1) storage. So essentially the stateless client model, but at the contract level.

A major challenge with the first approach is how to handle the following sequence of events (I’ll use an ERC20 for example):

1. Alice sends Zachary 20 tokens. Zachary never had any tokens before, so a contract gets created to record the balance.
2. Zachary contract expires and hibernates.
3. Bob sends Zachary 10 tokens. Zachary does not seem to have an active contract, so a new one gets created to register the 10-token balance.

How do the 10 tokens and 20 tokens get aggregated together? And what if this is a more complex application, where aggregating together states is not a matter of simple addition?

---

**MihailoBjelic** (2018-11-12):

I didn’t put much thoughts into this topic so far, but I was triggered to comment because I fail to see the problem here.

Let me try to elaborate in Layman’s terms:

Behind (I guess) every smart contract there are two entities:

1. The creator (individual or organization)
2. Users

Why wouldn’t contracts simply have “tip jars” where anyone can put ETH to pay the rent? Every contract, i.e. entities behind it should determine who should pay the rent (the decision process can happen on-chain or off-chain).

The reasoning is that there are so many different use cases for contracts, so there can not be a one-size-fits-all solution. In some cases the creator is financially or otherwise benefiting from the contract existence (so she/them would probably be the one paying), in other cases the creator was an altruist and is not benefiting from the contract (so users should be the ones paying), and finally there certainly are many hybrid cases.

I’m probably missing something obvious, does anyone mind explaining what? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**jvluso** (2018-11-13):

From a protocol perspective what makes the most sense is for each contract to be responsible for its own rent. This would run into issues like the one that you mentioned about users mooching storage, but it would also allow smart contract developers to experiment with different ways of solving that problem.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A major challenge with the first approach is how to handle the following sequence of events (I’ll use an ERC20 for example):
>
>
> Alice sends Zachary 20 tokens. Zachary never had any tokens before, so a contract gets created to record the balance.
> Zachary contract expires and hibernates.
> Bob sends Zachary 10 tokens. Zachary does not seem to have an active contract, so a new one gets created to register the 10-token balance.
>
>
> How do the 10 tokens and 20 tokens get aggregated together? And what if this is a more complex application, where aggregating together states is not a matter of simple addition?

Right now, most implementations of ERC20 contracts don’t create a new contract - they would just add a line to their storage, and whoever is footing the bill to maintain the contract would have to pay slightly more for each account with a balance.

This won’t scale well once rent gets added, so a new implementation will need to be created that can hibernate individual user’s gas totals. I think it will use the `CREATE2` opcode. With hibernation, it will need to prove that nothing has been created at the specified address since the creating contract was created. Alice will be able to provide that proof and create the new contract. Bob won’t, and will instead need to wake up the hibernating contract using the logic in the ERC20 implementation.

---

**vbuterin** (2018-11-13):

I fully agree that each contract being responsible for its own rent is optimal. And I fully agree that making a new implementation of ERC20 that creates contracts as balance records is optimal.

The challenge is making a generic programming model that actually allows developers to write contracts with (close to) the same ease that they have today without needing to worry too much about thinking about who pays what rent and what the edge cases are involving different parties not paying.

---

**clesaege** (2018-11-13):

Creating smart contracts for each attributable user storage seems the most elegant method.

For some applications we would need to know when some contracts hibernate (in my Kleros usecase to remove them from the staking data structure, as if we don’t, we’ll draw contracts hibernating and we won’t be able to penalize them for failure to vote).

The solution to this problem would be also have a `hibernate` special function (something similar to the `constructor` special function) which is called when one contract goes to hibernation (here it would call the main Kleros contract to unstake). When the contract wakes up, a `wake` function would be called.

In order not to block hibernation, the hibernation should work even if the `hibernate` function fails. We would probably also need to set up a gas limit in advance in order not to make hibernation calls too expensive. The amount of gas could be specified at contract creation and the minimum deposit could be a function of this gas (if hibernate gas limit is high, your contract will enter in hibernation when reaching a higher deposit threshold).

---

**fubuloubu** (2018-11-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> Creating smart contracts for each attributable user storage seems the most elegant method.

Why is this true? It seems to significantly grow the programming complexity, as mentioned here:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A major challenge with the first approach is how to handle the following sequence of events…

I really think a good solution to this problem has to make the programming model much clearer. I don’t think “emitting separate contracts per contract for interacting as a contract, and then have to figure out how the contracts combine together in the permutation of cases of which contracts are down” is the clearest model.

I have an alternative proposal specified here: [Ethereum 2.0 Data Model: Actors and Assets - #6 by fubuloubu](https://ethresear.ch/t/ethereum-2-0-data-model-actors-and-assets/4117/6)

I think it makes the programming model clearer (per-user storage of assets) which the infinite mapping model typically aligns around in many cases. An addendum to that I just thought of now is deduct storage rent from your Ether holdings, which means your account can’t do anything if it’s unfunded. That’s a clear model with how actual rent works. And this also supports the “tip jar” that [@MihailoBjelic](/u/mihailobjelic) mentioned, just add ETH to the contract!

---

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> The solution to this problem would be also have a hibernate special function… wake special function…

I think this is a really interesting approach, because it makes rent a direct feature you have to plan for if you have custom logic that needs to be handled. It makes this complicated concept much easier to work with and plan for.

Whatever is planned, there would have to be a gradual introduction of these concepts. You could put legacy contracts on a different schedule for rent increases, putting them on a slower path towards what the general case would be, and then eventually making them more expensive in order to convince people to change to the new style. Dropping this all on Serenity doesn’t seem like the best way to have a smooth transition to highly-secure contracts, people need time to play with these concepts because they are quite complicated!

---

**vbuterin** (2018-11-19):

> I have an alternative proposal specified here: Ethereum 2.0 Data Model: Actors and Assets

I have thought of a somewhat similar model myself, where a contract can store objects with a user account, with that user’s permission, which the user would then need to pay rent for. I do increasingly agree that it has advantages; the main one I see is that if a user account does get hibernated, reviving it and all of its associated assets requires only a single set of Merkle branches.

This seems like a promising direction.

---

**clesaege** (2018-11-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> Why is this true? It seems to significantly grow the programming complexity, as mentioned here:

From a programming standpoint, creating smart contracts for each user storage makes sense in the object-oriented paradigm. They would have getters and setters (only available to the parent contract), constructors and “hibernators” (acting as a special kind of destructors).

Note that I’m not hardly advocating for this, just saying it’s a possibility which should be considered. The thoughts in my initial post were more similar to your Actors and Assets proposal which also seems to be an interesting direction.

---

**fubuloubu** (2018-11-19):

In a way, although the object oriented approach of treating everything as an object leads to weird and obscure abstractions, and the inheritance model leads to many insecure practices.

I’ve been a big fan of the actor model because it is just more understandable. This actor has these assets and this internal state. It can receive messages of this type (4 byte signature is a message id, and contracts have a “mailbox”), and responds with messages of this type (external calls, emitting events). It may keep track of things in internal state, but that should be small if it is well designed.

Hibernation and Revival can be message types as well. If the Actor accepts a Hibernation, it will make preparations to enter into “cold storage” like in your staking example (clearing out the staking pool). Similarly for Revival, like it might allow whomever revived it to become it’s owner or something, creating an incentive to pick up something that has been abandoned, or allowing someone to reclaim lost property.

The concurrency attributes of this model are really compelling as well. I think it would work well in Sharding for example. [@expede](/u/expede) and I talked a great deal about this at DevCon.

---

Edit: this abstraction happens mostly under the hood. Contract writers still can write contracts in EVM bytecode in any language they choose, it just affects the execution model a bit. As you hopefully can see, the current contract mental model is pretty compatible with this proposal.

---

**fubuloubu** (2018-11-19):

Hmm, I wonder if this could clean up events a bit? Events can be directed to a given account, and then event storage could become the responsibility of that account, after some period like a month or whatever so light clients can get them.

---

**MihailoBjelic** (2018-11-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> Why is this true? It seems to significantly grow the programming complexity

I would agree (again, I’m not deep into the matter).

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> I have an alternative proposal specified here: Ethereum 2.0 Data Model: Actors and Assets
>
>
> I think it makes the programming model clearer (per-user storage of assets) which the infinite mapping model typically aligns around in many cases. An addendum to that I just thought of now is deduct storage rent from your Ether holdings, which means your account can’t do anything if it’s unfunded. That’s a clear model with how actual rent works. And this also supports the “tip jar” that @MihailoBjelic mentioned, just add ETH to the contract!

This makes sense to me.

If I’m not mistaken, Dfinity is using the actor model? It might be worthwhile to take a look at their work, or chat with someone from the team?

---

**fubuloubu** (2018-11-21):

Not sure about Dfinity, but I know Rchain is. The problem IMO is that they dove into the deep end with the contract language being written in a subset of Erlang (I think?) or some other obscure-ish language that may not be as friendly to developers as JavaScript or Python. But their approach does have a strong concurrency model.

Erlang (actor model VM) was used to build WeChat. The story goes their first iteration supported something like 2m DAUs on a single server before having to add more computers, which was almost trivial to do because that model natively supports a distributed architecture. You just have to load balance between nodes effectively.

---

**vbuterin** (2018-11-21):

Personally I do think keeping the developer experience close to what they’re used to and not adopting weird programming models that require them to completely change their thinking is something that heavily contributed to ethereum’s current success and it would be very valuable to keep it.

But we don’t need to bake the model in deeply into the scripting language, we’re just trying to figure out the permanent storage model, which is a lighter footprint.

---

**fubuloubu** (2018-11-21):

That’s 100% spot on. This is mostly for the data and execution layers to adapt. The programming model actually already reflects this if you think about it (contracts have internal state and interact by passing messages to other contracts)

---

**MihailoBjelic** (2018-11-21):

Didn’t know about Rchain, thanks for the info.

Just checked Dfinity, their actor model is realized through Primea, Dfinity’s communication layer (it’s Martin Becze’s brainchild, if I got it right). It sits between the consensus layer and the data exec layer (Wasm VM), which is in a way along the lines with what [@vbuterin](/u/vbuterin) noticed.

About Primea ([source](https://www.reddit.com/r/dfinity/comments/959pjb/where_can_i_learn_more_about_dfinitys_actor_model/)):

"It enables many things at the inter-contract communications level, in particular contract locality and isolation of contract code, via restricted communications between contracts. This allows for modularity and more easily audited gateway contract patterns, and lends itself very well to concurrency and parallelisation. Primea loosens restrictions on synchronous calling, enabling scalability by allowing for much deeper call stacks (callers are freed so you don’t need to store the entire modified state of the call stack for atomic reversions), you can still make atomic calls if you want to but unlike ethereum this is now optional, it’s a choice made in the contract code and not enforced by the VM.

It also adds to the actor model by making the message scheduling deterministic, using a gas based metric for message queuing. The actor model also prevents attacks that leverage re-entry bugs, which have been the cause of some notable exploits."

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Personally I do think keeping the developer experience close to what they’re used to and not adopting weird programming models that require them to completely change their thinking is something that heavily contributed to ethereum’s current success and it would be very valuable to keep it.

This is so true and important, though.

---

**fubuloubu** (2018-11-21):

Ah, that’s a neat idea. Optional synchronous behavior. There are calls that need to be synchronous (such as authorization logic or data querying), but I think this model gives additional tools to have those calls settle asynchronously with a smart scheme (settle assets iff all calls succeed). Asynchronous calls settle much quicker because you wouldn’t have to do that if specified up front.

---

**expede** (2018-11-23):

This may actually belong over at [Ethereum 2.0 Data Model: Actors and Assets - #6 by fubuloubu](https://ethresear.ch/t/ethereum-2-0-data-model-actors-and-assets/4117/6), but since I’m responding to things in this thread, I’ll put this here for now. Apologies for the categorization error ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

> being written in a subset of Erlang (I think?)

RChain have their own abstraction, called the [Rho Calculus](https://ac.els-cdn.com/S1571066105051893/1-s2.0-S1571066105051893-main.pdf?_tid=445f11f7-0d13-45ac-820d-72252290dc89&acdnat=1542995176_34a15edccf302e44ff583a2603557235) (an extension of Pi Calc) that is essentially formalism for the actor-style concurrency, and have used it as the basis of [RhoLang](https://github.com/rchain/rchain/tree/master/rholang). The primary implementation is in Scala, and yes, has a very “unique” syntax.

> Personally I do think keeping the developer experience close to what they’re used to and not adopting weird programming models that require them to completely change their thinking is something that heavily contributed to ethereum’s current success and it would be very valuable to keep it.

I agree, broadly! Ethereum should be as approachable as possible. There is a balance, though: people are spending a lot of time learning EVM internals and getting bitten by expensive bugs (Turing Tarpit, &c). We’re already seeing the rise of Ethereum-specialist programmers in commercial contexts.

Not necessarily arguing for switching, but just my two cents worth: Erlang’s Prolog-ish syntax looks unfamiliar, but there are others like Scala (widely-used) and Elixir (praised for syntax and ease-of-learning). The actor model is closely related to OO — in fact, essentially the original OO paper is really the actor model. These languages don’t need to seem unfamiliar (see Elixir), and inter-actor calls between actors can looks as simple as the `.call` that we have today.

> @expede and I talked a great deal about this at DevCon.

Indeed; thanks for the fun conversations ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12) To extrapolate a bit, smart contracts today can be modeled as single-threaded actors. Viewing them as through this lens gives the application-layer more *room to grow*, and potentially ways of adding more safer and more powerful constructs over time. That’s a bit off topic of this thread, though. WRT sharding, cold storage, &c, I don’t think that users should have to do the accounting of where something lives. IMO all the of routing, message addressing, &c should happen below the application layer, and should feel like one VM, as it is today.

---

**antoineherzog** (2018-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I have thought of a somewhat similar model myself, where a contract can store objects with a user account, with that user’s permission, which the user would then need to pay rent for. I do increasingly agree that it has advantages; the main one I see is that if a user account does get hibernated, reviving it and all of its associated assets requires only a single set of Merkle branches.
>
>
> This seems like a promising direction.

I disagree. Like in the current ERC20 Token model, in the current world, shares of a company for example are maintained by the issuer, which means the company.

So technically the issuer pays for the bookkeeping  It should be the same in blockchain and the issuer should be responsible to pay for the rent cost.

---

**clesaege** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> I disagree. Like in the current ERC20 Token model, in the current world, shares of a company for example are maintained by the issuer, which means the company.

I don’t think we should try copy previous systems (get inspiration and learn from, for sure, but not copy). We have different problematic.

If the owner of an ERC20 is malicious, he can split his ERC20 tokens on a really high number of accounts. For this, he will only pay a one-time gas fee while the issuer will need to pay a recurrent storage fee. Assuming the tx fee to be constant and the storage fee constant per time unit, this would lead to a O(t)  griefing factor where t is the time elapsed since the attack. This is not acceptable.

We could envision some systems like dust-destruction to remove addresses below some threshold, but this would add significant complexity to smart contracts and likely results to some exploits.

---

**jvluso** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> I have thought of a somewhat similar model myself, where a contract can store objects with a user account, with that user’s permission, which the user would then need to pay rent for. I do increasingly agree that it has advantages; the main one I see is that if a user account does get hibernated, reviving it and all of its associated assets requires only a single set of Merkle branches.
>
>
> This seems like a promising direction.

I disagree. Like in the current ERC20 Token model, in the current world, shares of a company for example are maintained by the issuer, which means the company.

So technically the issuer pays for the bookkeeping It should be the same in blockchain and the issuer should be responsible to pay for the rent cost.

Does the base protocol need to be opinionated about this? If each contract is responsible for its own rent, each contract can set its own rules about who can pay for its rent costs, and multi-contract structures can be used for delegating rent costs.

