---
source: magicians
topic_id: 23782
title: "ERC-7950: encoding chain ID + transaction hash"
author: microbecode
date: "2025-04-23"
category: EIPs > EIPs interfaces
tags: [transactions, chain-id]
url: https://ethereum-magicians.org/t/erc-7950-encoding-chain-id-transaction-hash/23782
views: 414
likes: 9
posts_count: 19
---

# ERC-7950: encoding chain ID + transaction hash

I was thinking of a standard that encodes two things into one string:

1. An EVM chain id
2. A transaction hash

Such string could allow users to uniquely know on which network the transaction occurred. Currently it requires extra communication to inform the user which chain the transaction hash happened on.

Does something like this exist already?

There are some similar EIPs, such as:

1. For block explorer API routers: EIP-3091: Block Explorer API Routes
2. Using network names: ERC-3770: Chain-specific addresses

The first one above is not very relevant, but the second one is quite close to what I had in mind. The problems with the second one are, in my mind:

1. It doesn’t allow using testnets
2. Who decides what are the shortnames for each network

If instead of shortnames we utilize a commonly agreed-upon chain id (https://chainlist.org/) , both of the problems are solved.

The new encoding format might be something like “1:0x123” where “1” is the chain id and “0x123” is the transaction hash.

The real end goal would be to also create a website that guides to the right blockchain explorer based on this new string type. So users simply enter the string and they get redirected to the right blockchain explorer. But such website/service is a separate issue.

What do you think?

## Replies

**SirSpudlington** (2025-04-23):

I like this idea it would help with UX across the several L2s (and forks), although, using [chainlist.org](http://chainlist.org) may not be the best of ideas, as it is quite cluttered. I’d avocate for a separate consensus process, e.g. separate ERCs and an initial list.

It may also be a good idea to indicate to the user when a raw chain id is present e.g. `id-1:0x123...ABC` It may make it look more natural as [EIP-155](https://eips.ethereum.org/EIPS/eip-155) chainIDs are not really designed for user facing environments.

Another issue, is that it may cause confusion with [ERC-3770](https://eips.ethereum.org/EIPS/eip-3770) at a first glance, especially with some dApps condensing the middle bytes of tx hashes and transactions to `...`.

---

**microbecode** (2025-04-24):

Thanks for the feedback!

I’m curious, in what way do you consider chainlist ‘cluttered’? Do you consider the list of IDs cluttered or just that website somehow?

I don’t see any problems with the list of IDs. They are, as far as I know, all unique. And, as far as I can tell, the numbers are not spammed to death (somebody for example reserving all numbers within u32). I don’t see a reason to duplicate this effort in a new ERC - I don’t see how the process could be made much better.

I think it’s a good idea to consider adding also some other data to the string. On the other hand, tx hashes are also really not designed for user facing environments - adding something more user un-friendly doesn’t make it much more horrible looking ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) But I don’t have a strong opinion in either direction currently.

Apps can continue truncating the middle of the tx hash. But you are correct that they may need to reconsider which parts to show and which not - but I’m unsure if this standard should consider that aspect at all.

---

**SirSpudlington** (2025-04-24):

It’s just that chainlist has thousands of entries, and they could change them at any time, adding or removing; it would just make it very hard to implement this standard.

---

**microbecode** (2025-04-24):

Well the source should be [GitHub - ethereum-lists/chains: provides metadata for chains](https://github.com/ethereum-lists/chains) (as mentioned in EIP-155). In theory that can also change, but if those are changed the ecosystem will have a lot bigger problems than just directing links to the wrong block explorer.

And, as I said, it’d be hard to create any better, alternative system.

---

**SirSpudlington** (2025-04-24):

Ah, I missed that EIP-155 specifies a list, in that case, that would be absolutely be better, you are right.

---

**microbecode** (2025-04-25):

Currently, I’m especially looking for more feedback and ideas on the following topics:

1. What should be the string format? Here are some variants where “123” is the chain ID and “0x567” is the tx hash:

“123:0x567”. Pros: A typical formatting used for example in ERC-3770: Chain-specific addresses . Cons: parsers may confuse this new EIP format with that old format
2. “123-0x567”: Pros: Less likely to be confused with 3770.
3. “chainid-123-0x567”: Pros: harder to confuse with other formats, makes the use more explicit. Cons: Makes the string longer and parsing a bit less elegant. Also looks a bit confusing.
4. “0x567-123”: Cons: The chain ID is more important and should be first
5. “eip155:123:tx:0x567”: Pros: Makes this relevant also for non-EVM chains, as discussed here. Cons: longer string.
6. Something else, what?
7. Is “Meta EIP” the right category for this?
8. …And most importantly: does some standard already exist for this?

---

**SirSpudlington** (2025-04-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/microbecode/48/15066_2.png) microbecode:

> Is “Meta EIP” the right category for this?

I’d say this would be better as an ERC.

---

**microbecode** (2025-04-26):

Someone pointed me to [CAIPs/CAIPs/caip-10.md at main · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-10.md) . That specifies something similar, but for addresses, and not tied to EVM.

Now the problem becomes if the standard in this Magicians post wants to be compatible with CAIP-10, so this can be later expanded to be non-EVM specific, if wanted. How to distinguish whether the string refers to a transaction hash or to an address? Some ideas:

1. Use a different separator at some point (or in all of the separation points). For example “:” means it refers to an address and “-” means it refers to a tx hash.
2. Add a static string, like “tx” to some point of the string. Probably best at the end so it can be made later non-conflicting with CAIP-10. (Adding the “tx” to the beginning, like tx:123:0x567, would break the syntax of CAIP-10, but at the end it’d just expand CAIP-10)

I’m starting to lean towards syntax “123:0x567:tx”. It’s longer than just “123:0x567” but the longer syntax makes it somewhat compatible with existing standards. The only non-compatible part would be the “:tx” at the end.

---

**microbecode** (2025-04-28):

Fair point!

I mentioned chainlist as an example. Sorry, I should’ve been more explicit: the chain ID should use the IDs listed here (and in the repo linked to in the EIP): [EIP-155: Simple replay attack protection](https://eips.ethereum.org/EIPS/eip-155)

That can get hacked. But the standard I’m proposing doesn’t “care” too much about that. If someone is interacting with chainId 115511 (Sepolia), I doubt they change the number because some EIP/repo gets hacked. The only thing that’d suffer are some direct integrations that utilize that chain ID list directly - no idea which and where. But for this standard, that’s not a big concern.

The worst case scenario, from this standard’s point of view, is that some integration starts handing wrong chain IDs that are used by this standard. But there’s nothing this standard can do about it - there is no verification for the used IDs.

I agree wallets should be checking these things. I have no idea if they do.

---

**microbecode** (2025-04-28):

This standard doesn’t force anyone to remember anything. This just defines the encoding of chain ID and transaction hash put together. It’s up to other parties (wallets, exchanges, explorers, protocols, …) to actually take this into use - I don’t think anyone wants to be forming these strings manually.

And yes, the repo getting hacked is a concern, but not something we should try addressing here. I encourage you to start a new post about it, discussing the options. Let’s try to stick to the topic here.

---

**SirSpudlington** (2025-04-28):

Worst case scenario is that the source repository gets hacked, the result of this is that you’d see a different name in the start of the tx hash, but with the way tx signing works, the odds of having the exact same transaction hash on two different networks are basically zero (even if the transaction is functionally the same due to encoding changes). So the only attack vector here is mildly inconveniencing a user, if they copy the transaction hash. Best case, they just click a link to the block explorer and nothing happens.

---

**u59149403** (2025-05-07):

Draft PR already exists: [new CAIP - Transaction Object Addressing by bumblefudge · Pull Request #221 · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/pull/221) , I think we should iterate on it

---

**microbecode** (2025-05-14):

Interesting, thanks for the reference! Wasn’t aware of such CAIP.

It seems the CAIP is a bit stale. And the encoding scheme looks super complicated - I tried figuring it out but there’s lots of of information missing.

My proposal is more in line with [CAIPs/CAIPs/caip-10.md at main · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-10.md) which is a lot easier and is already finalized.

---

**microbecode** (2025-06-24):

The EIP has now moved to the “Review” status. Please have a look and let’s discuss any proposals to make the EIP better. Thanks for all the feedback so far!



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7950.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7950.md)



```md
---
eip: 7950
title: Encode chain id with transaction hash
description: Way to encode a chain ID and transaction hash into a unique string format
author: Lauri Peltonen (@microbecode)
discussions-to: https://ethereum-magicians.org/t/a-new-standard-for-encoding-chain-id-transaction-hash/23782
status: Review
type: Standards Track
category: Interface
created: 2025-05-22
requires: 155
---

## Abstract

This standard proposes a way to encode the combination of a chain ID and a transaction hash into one string.

## Motivation

Looking up a transaction by its hash always requires the context of the chain - a transaction hash alone is not enough to identify the used chain. If the chain information is included in the string itself, finding the right chain for the transaction is easy.
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7950.md)

---

**microbecode** (2025-09-18):

This is now in “Last Call” status, and moved to ERC side. [ERCs/ERCS/erc-7950.md at master · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7950.md)

---

**mihaic195** (2025-09-19):

Hey [@microbecode](/u/microbecode),

Great work! After reading your proposal, I think your rationale for using the `:tx` suffix to differentiate from addresses and clear any ambiguity makes sense. However, it got me wondering if it would make more sense to generalize it with a dynamic `:type` field?

For example:

- 1:0xc8dA…:tx - transaction (aligns with goal of this EIP, essentially a CAIP-style ID for EVM)
- 1:0x0DA0…:addr - address (aligns with ERC3770)
- 1:0x12..:block - block number
- 1:0xcdd…:msg - signed message

This would make it more extendable for other common use cases that face the same chain-context problem.

I’m just thinking out loud, but what do you think?

---

**microbecode** (2025-09-19):

Thanks for the feedback!

This can definitely be expanded. But I prefer to keep this version simple because I’ve seen quite a few similar standards that try to cover a lot of different stuff, and they have remained stagnant and never gone anywhere. The easier the standard is, the easier it is to get it finalized.

Another standard can be later built on top of this that expands the usage - be it a CAIP or an ERC.

---

**microbecode** (2025-10-08):

This ERC has now been finalized. Thanks everyone for the feedback and support!

