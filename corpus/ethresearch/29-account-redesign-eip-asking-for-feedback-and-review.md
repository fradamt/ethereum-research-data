---
source: ethresearch
topic_id: 29
title: Account redesign EIP, asking for feedback and review
author: vbuterin_old
date: "2017-08-19"
category: Sharding
tags: []
url: https://ethresear.ch/t/account-redesign-eip-asking-for-feedback-and-review/29
views: 1773
likes: 2
posts_count: 17
---

# Account redesign EIP, asking for feedback and review

https://github.com/ethereum/sharding/blob/master/docs/account_redesign_eip.md

These protocol changes are intended to only be use *within* shards, so that we can make more radical changes to improve efficiency without caring about backwards compatibility. The doc itself describes most of the rationale and some of the interesting properties and ideas that this kind of redesign enables.

## Replies

**tim** (2017-08-19):

@vitalik ^ the url above returns a 404 error ![:disappointed_relieved:](https://ethresear.ch/images/emoji/facebook_messenger/disappointed_relieved.png?v=9)

---

**vbuterin_old** (2017-08-19):

Sorry! All fixed now.

---

**comepradz** (2017-08-21):

Is the “home shard” the same as “main shard” in the doc.md?

---

**vbuterin_old** (2017-08-22):

Yes, “home shard” and “main shard” are the same thing.

---

**djrtwo** (2017-08-22):

Does the account to which the transaction is sent need to be specified in read/write_address_list, or is does it get get that access by default?

---

**vbuterin_old** (2017-08-22):

I would say adding the `to` address to the write address list automatically (ie. not requiring it to be added explicitly) would certainly be a useful optimization.

---

**djrtwo** (2017-08-22):

So is `len(union(read_address_list, write_address_list))` at least 1, where it at least has the `to` address specified?

Specified another way, does a transaction have to pay READ_ADDRESS_GAS to read/write to the `to` address?

---

**vbuterin_old** (2017-08-23):

> Specified another way, does a transaction have to pay READ_ADDRESS_GAS to read/write to the to address?

Yes.

Philosophically speaking though it doesn’t really matter, because you can think of this READ_ADDRESS_GAS as just being part of the base transaction gas cost.

---

**tawarien** (2017-08-23):

I See the costs for SSTORE, but missing the one for SLOAD, I assume it will be cheaper as it is now or it will end up being potetially more expensive then a repeated SSTORE.

Will this proposal have an influence on OP codes accessing other contracts like EXTCODE and all the CALLS in terms of gas? I could imagine that they potentially could become cheaper as the contract loading has already been payed for.

---

**tawarien** (2017-08-23):

If the to contract is just a proxy, that does not write anything to its storage but only checks a certain condition and then forwards to another contract and the write address list entry could have been a read address list entry instead, which is better optimizable.

I can Imagine that an ERC20 contract built for this scheme would have a separate child contract for each address holding tokens and only the contracts for the “from” and “to” addresses in a transfer have to been written to, the Main contract may be read only, which has huge parallelisation opportunities as all token transfer that do not share any address could be run in parallel.

---

**tawarien** (2017-08-23):

By writing the previous post I have noticed that the current proposal give no incentive to add a contract to the read address list instead of the write address list. As the ACCOUNT_EDIT_COST are only charged on an actual SSTORE. The caller has no benefit of adding an address he read to the write instead of the read, except for being lazy or when he does not know if a call will write or only read. But the network has a drawback as writes can not be executed in parallel as well as reads can. What speaks against adding the ACCOUNT_EDIT_COST up front independent of if an actual write will happen or not?

---

**vbuterin_old** (2017-08-24):

I agree that SLOAD and calls could be made much cheaper, though there’s also not too much value in doing so. Use cases which call the same contract many times within one transaction are few and far between. Transactions that loop through account records in contracts won’t work in this model, because each account record would need to be a separate contract. Though perhaps there *is* a rationale in just perfectly equalizing SLOAD and MLOAD to encourage compilers to be simpler and treat the two operations as analogous.

> What speaks against adding the ACCOUNT_EDIT_COST up front independent of if an actual write will happen or not?

There might be a transaction of the form “if X then write to A, otherwise write to B” where X is unknown at submission time.  You need A and B in the writable set, but you don’t want to charge for two edits in this case.

---

**MicahZoltu** (2017-08-24):

> Use cases which call the same contract many times within one transaction are few and far between.

I believe this is the case right now only because there are no non-trivial dApps out yet.  Augur does a *ton* of internal transactions as part of a transactions, both between Augur contracts (because Augur is way too big to fit into a single contract) and within contract.  Often the calls will jump back and foreth between a couple of contracts several times before finally returning out to some originating contract.

---

**vbuterin_old** (2017-08-24):

Ok, fair point. Then reducing the base gas cost for all calls back to 40 seems reasonable.

---

**tawarien** (2017-08-31):

After some thinking about this EIP I found a corner case that is still unclear to me. How are newly created contracts treated concerning the address Lists.

Does the new contract need to be in the write_address_list, the read_address_list or none of them? (Assuming he is never called after creation)

If the new contract is called and does an SSTORE does he need to be in the write_address_list?

Does the contract creating the new contract need to be in the write_address_list or is the read_address_list enough? (assuming the creator itself does not do an SSTORE)

When the initcode of the new contract does an SSTORE who has to be in the write_address_list; The creator, the new contract or none of them?

---

**vbuterin_old** (2017-09-03):

All accounts always exist in some virtual sense. “Creating” an account is just changing the account from an empty state to a nonempty state. So they would work just as before, and any account that gets created would need to be in the write address list.

