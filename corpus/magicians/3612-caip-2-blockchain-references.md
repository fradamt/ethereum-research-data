---
source: magicians
topic_id: 3612
title: CAIP-2 (Blockchain references)
author: ligi
date: "2019-08-31"
category: Uncategorized
tags: [chain-agnostic, eip-155]
url: https://ethereum-magicians.org/t/caip-2-blockchain-references/3612
views: 5564
likes: 23
posts_count: 27
---

# CAIP-2 (Blockchain references)

Emerged in a discussion here around an EIP by [@loredanacirstea](/u/loredanacirstea) - would love some feedback on CAIP-2 and CAIP in general.

https://github.com/ChainAgnostic/CAIPs/pull/1

## Replies

**MicahZoltu** (2021-08-27):

Note: I cross posed this over at [CAIP-2 (Chain ID): The Ethereum interface · Issue #3 · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/issues/3), but since that issue is closed (despite being the discussions-to link) I am leaving this here to ensure it gets visibility.

I don’t understand why Ethereum addresses are labeled as eip155.  EIP-155 didn’t change the addressing scheme for Ethereum in any way, it only changed the signing scheme and it is opt-in for every transaction and not something that is set per account.  An Ethereum address may sign one transaction without a chain ID and the next with a chain ID and then the next without again.

I think that `ethereum` should be the term used, or maybe `ethereum1` if you want some form of versioning.

---

**ligi** (2021-08-30):

the prefix eip155 is used as we use chainIDs introduced in eip155 to specify the chains. Also ethereum: is already used by ERC681

---

**MicahZoltu** (2021-08-30):

ChainID wasn’t introduced by EIP-155, it has existed since Ethereum launched.  The only thing EIP-155 did was integrate it into signatures (but not all signatures!) which made it part of consensus rather than just part of gossip.

As I mentioned in the linked issue, an account can sign a mix of EIP-155 transactions, pre-155 transactions, type 2 (1559) transactions, etc.  Calling this address a “eip155 address” just doesn’t make sense.  This is different (IIUC) from Bitcoin’ segwit, where addresses were actually backward incompatible (my understanding of Segwit is very limited, so this may be incorrect).

> ethereum: is already used by ERC681

If the intent is to make CAIP-2 compatible with other payment URLs, then it should pick a standard schema prefix (protocol) for everything that clearly delineates that it is a CAIP-2 address.  For example, `caip2:ethereum:0xabcd...` or whatever.  Having a separate schema namespace for every single blockchain out there is untenable because you will eventually run into conflicts.  On the other hand, if the assumption is that someone is pasting an address into a box, I believe that CAIP-2 are compatible with 681 addresses because they both would end up being `ethereum:<address>`, unless you include the chain ID (which I don’t think you should), in which case they would not match each other and you don’t have a problem.

---

**ligi** (2021-08-30):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> ChainID wasn’t introduced by EIP-155, it has existed since Ethereum launched.

interesting - I thought it was introduced with EIP155 - seems to be a common misconception then: [private blockchain - What is a chainID in Ethereum, how is it different than NetworkID, and how is it used? - Ethereum Stack Exchange](https://ethereum.stackexchange.com/a/37571/95)

Do you have any EIP/link where it was actually introduced?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> unless you include the chain ID (which I don’t think you should)

How would you differentiate mainnet and goerli without including the chainID?

---

**MicahZoltu** (2021-08-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> Do you have any EIP/link where it was actually introduced?

I am pretty sure it has always been there and I *think* it is part of the genesis block (though it might be called Network ID in there because early on the two were conflated)?  It is necessary to keep testnetworks and mainnet separate from each other, and then eventually (with the ETC split) to keep ETC separate from ETH.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> How would you differentiate mainnet and goerli without including the chainID?

I meant to say that I think you should just have a separate address prefix for every chain, Goerli should not be called “Ethereum”, it should just be called “Goerli”.  The same as I don’t think Polygon should be called “Ethereum” or Binance Chain should be called “Ethereum”.  When people are talking about Ethereum, they are almost certainly talking about Ethereum Mainnet.  There is a whole spectrum of chains that are *similar* to Ethereum Mainnet ranging from the testnets, to ETC, to side chains, to other blockchains that run the EVM   Trying to draw a clean line is difficult and I don’t think it adds value.  Each chain should have a globally unique name (which they all already do), and we should use that globally unique name as the prefix without trying to group/categorize them.

---

**MicahZoltu** (2021-08-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> I thought it was introduced with EIP155 - seems to be a common misconception then: private blockchain - What is a chainID in Ethereum, how is it different than NetworkID, and how is it used? - Ethereum Stack Exchange

Just read that answer.  I think the source of the confusion is that prior to the Ethereum/Ethereum Classic split, Network ID == Chain ID, so there was functionally a single number.  However, after the split we now had two networks with the same network ID but different chain IDs, so we (community) had to come up with a new name for one of them.  Thus, “Network ID” turned into “Network ID + Chain ID”.  I’ll concede that EIP-155 was perhaps the first place that Chain ID (as a term) came up in any documentation/consensus protocol stuff, so I can appreciate the confusion.  However, the test networks have always had a different “chain ID”, its just that it was called network ID previously because in all cases the two were the same so we didn’t need two names.

---

**ligi** (2021-08-30):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> and we should use that globally unique name as the prefix without trying to group/categorize them.

I think it is better to use the ID. E.g. this way you can craft transactions without needing to lookup the chainID. Also otherwise we might clash with networks outside the etheruem exosystem - I think it will be quite hard to enforce a globally unique name and have no collisions with more and more chains emerging.

---

**MicahZoltu** (2021-08-30):

You already have to do a lookup of the first key.  `bitcoin` needs to be handled differently from `ethereum`.  You can simply have a longer list there, no need for a *separate* lookup mechanism.

---

**ligi** (2021-08-30):

No - I just need to match eip155 and can then deal with all chains in this namepspace - even new ones that the app does not yet know about

---

**MicahZoltu** (2021-08-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> even new ones that the app does not yet know about

Ah, I think this is where we are disagreeing.  I don’t think it is realistic that you’ll be able to send coins/tokens or call contracts on an arbitrary chain that you aren’t familiar with, whether it is Ethereum-like or not.  For every chain (even test networks, Ethereum Classic, etc.) you need a unique client to be able to interact with that chain.

In other words, I don’t think you gain functional value by grouping Ethereum-like chains together into a category.

---

**ligi** (2021-09-01):

Yea - this is where we disagree ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=10)

Imagine a wallet connected to a dapp via WalletConnect (where CAIPS are used heavily in V2) - the only thing the Wallet needs to know for signing and basic functionality is the chainID. Also if you just fast spin up a testnet - you do not need to register that on a global registry to do basic things. And not even speaking about the collision problem that gets harder and harder if you do not group. I see a not of advantages in using grouping and leveraging the chainIDs that should be unique. Even there we had collisions - but it is easy to argue against them as for the replay attack problem.

---

**MicahZoltu** (2021-09-02):

How do you plan on drawing the line between “Ethereum” and “Not Ethereum”?  Does Ethereum Classic fall into the Ethereum namespace?  What about Tron?  Polygon?

Even the Ethereum testnets aren’t always compatible.  As testnets received the London upgrade, they became signature incompatible with Ethereum if you signed using a type 2 transaction.  Similarly, Ethereum Classic slowly drifts away from Ethereum compatibility with time, and some chains migrated to type 2 transactions before Ethereum did, while others are migrating after.

With the introduction of Proof of Stake and eventually state expiry, we may see more and more subtle differences between chains that makes it more and more challenging to maintain a consistent interface that works regardless of what blockchain you are talking to.

Something to keep in mind is that address space extension is currently under research which will likely break this grouping as different chains adopt that feature at different points in time.

---

Circling back to the original topic, if we *do* group by “Ethereum like” then I still think we should prefix the name with `ethereum:<chain_id>:address` or `ethereum:<chain_name>:address`.  `chain_name` is more user friendly, but I don’t think there is a JSON-RPC endpoint that exposes this at the moment.  Even if I concede to grouping (which I don’t), `eip155` as a prefix is wrong and should not be used IMO.

---

**ligi** (2021-09-02):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> How do you plan on drawing the line between “Ethereum” and “Not Ethereum”? Does Ethereum Classic fall into the Ethereum namespace? What about Tron? Polygon?

All the chains in the eip155 namespace can at least do eip155 transactions ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

So that clearly includes Ethereum Classic and Polygon - never looked into this Tron thing - the movie was great though.

---

**axic** (2021-09-02):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> ligi:
>
>
> Do you have any EIP/link where it was actually introduced?

I am pretty sure it has always been there and I *think* it is part of the genesis block (though it might be called Network ID in there because early on the two were conflated)? It is necessary to keep testnetworks and mainnet separate from each other, and then eventually (with the ETC split) to keep ETC separate from ETH.

I do not think it existed from beginning, hence on the Morden testnet, each new account had a starting nonce of `2^20` in order to differentiate transactions from mainnet transactions.

---

**pedrouid** (2021-09-06):

This is why we chose not to use `ethereum` as a namespace but instead we chose `eip155` to be the namespace

A chainId compatible with EIP-155 specification is independent of branding or nomenclature associated with Ethereum

We even discussed renaming to `evm` namespace but then it create ambiguity over what is considered an EVM chain

I can understand if you disagree with these points but these namespaces were chosen to provide the lowest friction point that chains could share in order to be identifiable without conflict

---

**MicahZoltu** (2021-09-06):

EIP-155 support by a particular chain doesn’t imply any sort of compatibility other than signing mechanism for a subset of transactions.  Even now, there are Ethereum spin-off chains that have relatively few EIP-155 transactions submitted, and Ethereum Mainnet has an ever dwindling number of eip-155 transaction signatures.

Using eip-155 as the prefix feels similar to using any other EIP number as the prefix like EIP-2718 or EIP-55.  You can very easily (and we may already at this point) have two Ethereum-like chains that have a chain-id but one of them doesn’t support EIP-155 transactions at all (in fact, there was talk just today about deprecating EIP-155 transactions in Ethereum).

I think the core of my argument here is that the eip155 prefix doesn’t provide any additional value to the user or developer that `ethereum` wouldn’t similarly provide.  I still argue that we should have a prefix per chain rather than trying to draw arbitrary lines around chain groups because that gives you real actionable information, but even if we ignore that and try to do a bucket-prefix, EIP-155 doesn’t tell the reader anything useful that a random number or word would.

---

**ligi** (2021-09-06):

IMHO a prefix per chain is a horrible idea.

We can argue about eip155 as a prefix which depends a bit if chainIDs where introduced with eip155 or have been there earlier.

---

**MicahZoltu** (2021-09-07):

Since this is a standard, we should have very strictly/well defined terms.  What exactly are the requirements for a chain being considered for the “ethereum” (or eip155) group of chains?  If the requirement is just “has implemented eip155”, then many Ethereum compatible chains wouldn’t meet this criteria because they simply launched with chain ID support with no EIP155 hardfork.  Also, any new chains that launch with only type 2 transactions (my recommendation to any new ethereum-like chain) would not qualify.  Similarly, if we eventually deprecate eip-155 transactions (something being explored for Mainnet), then Ethereum itself wouldn’t qualify as an eip155 chain in the future.  Meanwhile, any chain that doesn’t support EIP-155 would still be fully compatible with this specification by using the network ID as the middle delimiter.

I am personally unable to come up with any strong boundaries for what qualifies as an Ethereum-like chain and what qualifies as different enough to warrant its own name, which is why I think we should just have a root name for every blockchain.  I don’t think we have run into any *real* problem with namespace collisions in public blockchain names, and we can create a namespace reserved for private blockchains.

I’m very strongly against drafting a standard that isn’t clearly defined, and right now this `eip155` prefix is not nearly defined well enough to know exactly what it covers.

---

**ligi** (2021-09-07):

The requirement is that the network has a chainID (which was introduced with EIP155)

---

**MicahZoltu** (2021-09-07):

What is the value-add to this specification that we get by segregating by networks that have a field colloquially called “chain ID”?  Networks with a “network ID” (which functions identically to chain ID in this context) don’t count and should get their own top level name (like Morden)?  What about when we have two networks that have a chain ID but collide with each other (there is no guarantee that chain IDs don’t collide, you only need to avoid collisions when you have multiple chains that share a network protocol)?

Could we achieve the same goal by saying “any network that has a numeric identifier”?  This would at least be a bit more consistent and useful, because it allows us to do *some* grouping without having to set such an arbitrary group boundary and ensure that the second field is a number.


*(6 more replies not shown)*
