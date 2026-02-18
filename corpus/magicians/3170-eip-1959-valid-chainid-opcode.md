---
source: magicians
topic_id: 3170
title: EIP-1959 Valid ChainID opcode
author: wighawag
date: "2019-04-21"
category: EIPs
tags: [chain-id]
url: https://ethereum-magicians.org/t/eip-1959-valid-chainid-opcode/3170
views: 5054
likes: 1
posts_count: 13
---

# EIP-1959 Valid ChainID opcode

https://github.com/ethereum/EIPs/pull/1959 proposes to add an opcode to check if specific chainID is part of the history of the chainID of the current chain.

This would allow smart contract to validate signatures that use replay protection (as proposed in [EIP-155](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md)) without running the risk of contract checking only the latest chainID like [EIP-1344](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131) propose by default.

It was proposed as part of [the discussion of EIP-1344](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131/39) but the authors there thought better to have [2 separate EIP](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131/64) since both opcode could be implemented.

My point of view is that EIP-1344 is dangerous and require a contract based caching solution (as mentioned in the rationale) and does not explicitly state any use case not achievable by the opcode proposed here, at least in relation to the goal (shared between the two solutions) of protecting users of off-chain messages.

## Replies

**fubuloubu** (2019-04-21):

I have a few questions, but first I need to clarify something:

It seems this proposal *requires* that both sides of a contentious fork adopt different values from what occurred before the fork in order to be considered safe. Failure to do so would break the replay protection in at least one direction. Since there is currently no process for changing chain ID after a fork (such as the one [@fulldecent](/u/fulldecent) suggested), such process cannot be assumed to occur, and thus this proposal is not safe by itself without additional application-level considerations (similar to EIP 1344). I think this should be made more clear under Rationale.

Anyways, here are my questions:

1. How do you protect against a new message signed against an older chain ID? (Signed after the fork occurred)
2. What kinds of application-level effects might occur if all chain IDs in the history are considered valid with differentiating based on time?
3. Would it make more sense to emit what block height the chain ID fork occurred at for time-ordering of messages where chain ID update occurred?
4. If the opcode returned a block height instead of a boolean, what happens when an invalid chain ID value is given? Does it throw? Return 0? Etc.
5. If the opcode throws on invalid values, wouldn’t we need to add a new exception to the VM context? Wouldn’t it be easier in that scenario to use a standardize contract in this scenario? (Maybe a pre-compile)
6. If the block height returns 0 for invalid values, then what does the current chain ID return for block height? Is it the height of when it started? When it finished being valid?
7. If the current block height returns when it was valid from, what does chain ID 1 return? Implementation fork height of EIP 155? What about for other chain IDs for other chains?
8. If the opcode returns the block height of when it finished being valid, what does the current block height return? The current block? How do we know that it’s the tip of the history of chain ID values?

I think this series of questioning summarizes my current concerns. I think they could largely be dealt with, but it requires a lot of nuanced thinking to get correct to implement this opcode contrary to EIP-1344, which requires only that the user of such an opcode be aware of and implement a simple strategy to handle many of these scenarios (if required by their application).

---

**wighawag** (2019-04-22):

> It seems this proposal requires that both sides of a contentious fork adopt different values from what occurred before the fork in order to be considered safe. Failure to do so would break the replay protection in at least one direction. Since there is currently no process for changing chain ID after a fork (such as the one @fulldecent suggested), such process cannot be assumed to occur, and thus this proposal is not safe by itself without additional application-level considerations (similar to EIP 1344). I think this should be made more clear under Rationale.

This is not a situation specific to the particular solution provided here but simply a consequence of the requirement to support older message (signed before the hardfork). This situation is present as soon as a contract need to accept message signed with an older chainID, which as both rationale concur, is a must-have. This is thus also present in the solution presented as part of EIP-1344 rationale to deal with that.

But again, there is no need for any established process. Similarly to how a chain will change its chainID to not have its transaction replayed on another, we can assume that the community that disagree with the changes made as part of an hardfork, will make their own hardfork that simply change the chainID.

I have a paragraph on that situation but I ll see what I can add to the rationale to make this more clear.

> Anyways, here are my questions:
> How do you protect against a new message signed against an older chain ID? (Signed after the fork occurred)

We don’t do that at the contract level. This is the responsibility of wallets to only sign message that use the latest chainID. this is similar to how this is their responsibility today to use the proper chainID for the chain in question.  As such the behaviour of wallet do not need to change : they should reject message attempting to be signed with a different value than the current chainID.

But again here, this is not a situation unique to that opcode, it is simply a consequence of requiring smart contract to support messages with older chainID for the obvious reason mentioned in both rationale (EIP-1344, EIP-1959).

> What kinds of application-level effects might occur if all chain IDs in the history are considered valid with differentiating based on time?

There is no extra effects except for the inability for contract to reject messages because they were signed before a hardfork. Assuming wallet do their job, replay protection is guaranteed.

> Would it make more sense to emit what block height the chain ID fork occurred at for time-ordering of messages where chain ID update occurred?

We could indeed return the block number at which the chainID was introduced but it does not bring any benefit for the goal of protecting users of off-chain messages against replay attacks.

> contrary to EIP-1344, which requires only that the user of such an opcode be aware of and implement a simple strategy to handle many of these scenarios (if required by their application).

As mentioned, your concerns (except for EIP-1959 return values which can stay to be true or false) apply to EIP-1344 too. The important differences is that EIP-1344 can be easily misused and require a contract based solution to be used correctly.

---

**fubuloubu** (2019-04-22):

There are two big assumptions here:

1. Both sides of the fork will upgrade because both communities will (rationally) see the value in doing so… People, especially crypto communities, aren’t rational!
2. Application-level faults won’t occur due to the ability of a malicious attacker to sign a newer message with an older chain ID (this can happen outside of wallet software)

Both of these assumptions show the need for a time-based solution of handling chain ID, which is probably best done in user code because of the difficulties of implementing this opcode with block numbers instead of booleans. The one caveat is that if you have access to the current chain ID, then you can implement a block number-based solution easily (the opcode returns the block height after which the chain ID is no longer valid, or 0 if it is invalid, delegating the `assert` to user code)

---

**wighawag** (2019-04-22):

> Both sides of the fork will upgrade because both communities will (rationally) see the value in doing so… People, especially crypto communities, aren’t rational!

By the same argument, any chainID solution would not work, since you could always have a community that decide to use the same chainID as another one.

Realistically though, there are 2 possible situations :

1. The majority decide to make an hardfork but a minority disagree with it. The fork is planned for block X. If the majority is not taking any action to automate the process of assigning a different chainID for both, the minority has plenty of time to plan for a chainID upgrade to happen at that same block. Now if they do not do it, their users will face the problem that their messages will be replayable on the majority chain (Note that this is not true the other way around). As such there is no reason that they’ll leave it that way,
2. A minority decide to create an hardfork that the majority disagree with. Now, the same as above can happen but since we are talking about a  minority there is a chance that the majority do not care about the minority. In that case, there would be no incentive for the majority to upgrade the chainID. If after all, the minority chain gets traction, the majority might change their mind and upgrade the chainID. At that point, users of the majority might be disapointed that a subset of their messages were replayed on the minority fork while they were not paying attention. This could be at the detriment of the minority as it would reduce its traction.

In that second case, you are right, the use of block height would indeed be useful, and as you said, we could return the block height at which a chainID become invalid. This way the minority chain can prevent replays from the majority chain, but this requires 2 things (not present in EIP-712 for example):

- messages need include both a chainID and the block height representing the time at which it was signed
- contract need to check that validChainID(message's chainID) > message's Block Height

where validChainID return 0 when invalid (not part of the history), 2^256-1 when the latest, and the blockHeight at which it was replaced for past chainIds.

It might be better to use time rather than block height though. This would provide a nicer user experience and do not tie the off-chain world to the on-chain one. At the same time, fork transition handling might be ticker to deal with since it is unknown what time it will be until the fork activate.

> Application-level faults won’t occur due to the ability of a malicious attacker to sign a newer message with an older chain ID (this can happen outside of wallet software)

There is not malicious attacker scenario here. User can sign a new message with an old chainID if they desire to do so. Maybe they want their message to be replayed on all the fork sharing that chainID.

> The one caveat is that if you have access to the current chain ID, then you can implement a block number-based solution easily (the opcode returns the block height after which the chain ID is no longer valid, or 0 if it is invalid, delegating the assert to user code)

There would be no need to access current chain ID. The issue mentioned here about a minority-led hardfork can be solved by `VALID_CHAINID` return the time/blockHeight at which a chainID become invalid.

I ll update the spec in that regard and that should be all we need. Do you agree?

---

**wighawag** (2019-04-22):

I’d like to note that the issue mentioned here about a minority-led fork will not be without problem (even if fully solved as described). Simply because as soon as the majority disregard the minority fork when it happen, there will be lots of application issue as users do not submit messages there.

In other words, it might be too far-fetched to consider it as a valid scenario and the original spec might well be sufficient.

Also would EIP-712 consider to add a timestamp as part of its message format based on this possible scenario?

Anyway, since the change is minimal, I ll add it to the spec

---

**fubuloubu** (2019-04-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> Also would EIP-712 consider to add a timestamp as part of its message format based on this possible scenario?

It should not be required, but many use cases would typically make use of a timestamp or block height in their messages. Plasma for example references the previously submitted (Plasma) block, to ensure proper ordering of transactions in-protocol in order to be used on settlement. Note that this is application-specific, so I wouldn’t make it a requirement.

---

**fubuloubu** (2019-04-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> I’d like to note that the issue mentioned here about a minority-led fork will not be without problem (even if fully solved as described). Simply because as soon as the majority disregard the minority fork when it happen, there will be lots of application issue as users do not submit messages there.
>
>
> In other words, it might be too far-fetched to consider it as a valid scenario and the original spec might well be sufficient.

Potentially, but we are also building something with this opcode for a scenario that hasn’t actually occurred yet. EIP-155 was not implemented when the DAO fork occurred. We are making our best guess at what would happen and should give developers the proper tools to use in all relevant scenarios if we are creating an opcode to handle these situations.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> validChainID return 0 when invalid (not part of the history), 2^256-1 when the latest, and the blockHeight at which it was replaced for past chainIds.

Definitely one solution, but I don’t like adding tons of context-specific behavior.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> I’ll update the spec in that regard and that should be all we need. Do you agree?

Potentially. One thing I do not like about the current proposal is that it is a little long-winded in it’s analysis against EIP-1344. It would be awkward if this proposal was adopted and that one was not. I would remove those sections, and maybe add your analysis separately, in the GitHub issue or here.

---

**wighawag** (2019-04-23):

I updated the PR

> It should not be required, but many use cases would typically make use of a timestamp or block height in their messages. Plasma for example references the previously submitted (Plasma) block, to ensure proper ordering of transactions in-protocol in order to be used on settlement. Note that this is application-specific, so I wouldn’t make it a requirement.

As the analysis shows, this is not application specific. In order for a chain to have **none** of its new message (post fork) to be replayed on a unknown minority-led fork, all applications need to perform that block number check and wallet need to be able to protect users by ensuring the block number signed is not a past one (else it will be replayable on the minority chain). That is why it needs to be part of EIP-712 spec.

Of course, applications could decide that the issue mentioned about minority-led hardfork is not going to happen (something I am still on the fence). In that case we could make the blockNumber optional, like chainID is optional. In other words : optional but if present, enforceable by wallets.

In other words, if we believe the minority-led hardfork scenario is likely, EIP-712 must update its spec to protect signers from that scenario.

> Potentially. One thing I do not like about the current proposal is that it is a little long-winded in it’s analysis against EIP-1344… I would remove those sections, and maybe add your analysis separately, in the GitHub issue or here.

Why? the reasoning about EIP-1344 still stand. accessing the latest chainID is not sufficient and a contract based solution would be far less elegant than EIP-1959. Plus, the minority-led hardfork situation is worse for EIP-1344 since the caching system can’t ensure that the correct blockNumber is recorded. It will be off by few blocks, more if nobody updates it after a while.

As such the proposal still stand as a better alternative to EIP-1344 and it is important to explain why in the EIP so the community can chose which one to use.

> It would be awkward if this proposal was adopted and that one was not.

I am not sure what you mean, but I can add you as a co-author if you wish. After all, our conversation played a role in establishing the current spec.

---

**wighawag** (2019-04-23):

Actually I think we should decide as a community if we want to protect minority-led hardfork replay protection now.

After all it suffice one important application to not follow the practise of using both chainID and blockNumber to make the life of the minority fork harder. In other words, we should either assume minority-led harfork are not protected from replay or enforce that they are.

So if we think it is worthwhile to protect minority-led hardfork we should have the following opcode:

`VALID_CHAINID(uint256 chainID, uint256 blockNumber) returns (bool valid)`

Else we should go with

`VALID_CHAINID(uint256 chainID) returns (bool valid)`

since returning the blockNumber at which the chainID became invalid will allow some application to have their message replayable on a minority-led hardfork. And as said, it suffice one of these application to be important for the minority-led hardfork to be at a disadvantage.

---

**fubuloubu** (2019-04-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> As the analysis shows, this is not application specific

The overall need mostly isn’t (meta transactions are the exception, as they can be resigned if they miss the boat on the update without adverse affect), but how it’s handled is application-specific. My plasma example is a good one because they do create an application-level chain of Plasma block numbers that is referenced in protocol messages and serves the same behavior in this scenario as what is needed to protect against chain ID updates. It’s actually a good example where 1344 gets you by quite well:

1. On every block submission, do the cache check.
2. If changed, set the new domain separator.
3. All messages before or in the block submission must use previous chain ID, all the ones after must use the latter.
4. Clients can trustlessly query domain separator from contract vs. signing library and ensure a match.

In this scenario it’s actually preferable to cache in the application because it ensures the messages move in lockstep with the block submissions (which are done asynchronously), so there are no issues during the short period of update.

---

**fubuloubu** (2019-04-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> It would be awkward if this proposal was adopted and that one was not.

I am not sure what you mean, but I can add you as a co-author if you wish. After all, our conversation played a role in establishing the current spec.

What I mean is you should write proposals as if other proposals didn’t exist, unless there is a dependency.

---

**wighawag** (2019-04-24):

I reverted the change because as mentioned, to properly protect minority-led fork, the check need to be done by all applications interested in chainID based replay-protection. It suffice one important application to be put the minority-led fork at a disadvantage.

So now EIP-1959 assume that no protection will be put in place for minority-led hardfork. I added some info in the rationale.

Instead I also created a new [EIP-1965](https://github.com/ethereum/EIPs/pull/1965) that deal with the issue. It would be the solution I would vote for.

Discussion here : [EIP-1965 Valid ChainID For Specific BlockNumber : protect all forks](https://ethereum-magicians.org/t/eip-1965-valid-chainid-for-specific-blocknumber-protect-all-forks/3181)

