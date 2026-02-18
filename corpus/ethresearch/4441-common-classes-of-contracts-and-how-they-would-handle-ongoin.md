---
source: ethresearch
topic_id: 4441
title: Common classes of contracts and how they would handle ongoing storage maintenance fees ("rent")
author: vbuterin
date: "2018-12-01"
category: Economics
tags: [storage-fee-rent]
url: https://ethresear.ch/t/common-classes-of-contracts-and-how-they-would-handle-ongoing-storage-maintenance-fees-rent/4441
views: 9404
likes: 18
posts_count: 31
---

# Common classes of contracts and how they would handle ongoing storage maintenance fees ("rent")

Here are some common categories of contracts that exist currently on mainnet or will soon exist, and an attempt to analyze how they fare under the introduction of storage maintenance fees (“rent”) in their present form, and how they could be modified to survive the adoption thereof. This list is intended to be useful for evaluating both concrete proposals for storage maintenance fees and proposals for high-level languages that target blockchains with storage maintenance fees.

Anyone is welcome to suggest more examples!

### Tokens (ERC20)

**Effect of rent** - vulnerable to griefing attacks: anyone can send 1 wei (or equivalent) to an unlimited number of accounts, causing the token contract to incur permanent ongoing costs.

**Solution I** - store the balance associated with each user in a contract made with CREATE2 using the user’s address as a seed. Require the user to keep these contracts topped up. Note that for efficiency this can be combined across many applications by creating a generic `UserStorageFactory` contract, where a contract C can, with permission of user U, add an entry at a contract with a CREATE2 address made with sha3(C, U) as a seed.

**Solution II** - store a Merkle root of the balances, and require the user to provide a Merkle branch to spend coins. To mitigate “collisions” (Merkle branches failing due to 2 people trying to spend at the same time), the contract can also store a history of the last, say, 100 Merkle tree nodes added/removed, and can combine that data with branches based on old data to generate valid branches (see [The Stateless Client Concept](https://ethresear.ch/t/the-stateless-client-concept/172) for more discussion).

### Cryptokitties

**Effect of rent** - vulnerable to griefing attacks: anyone can keep breeding kitties, which continually add to the contract’s ongoing storage expenditure.

**Solution** - every kitty becomes a separate contract, owner responsible for upkeep.

### Multisig wallets

**Effect of rent** - in many present designs, in a M of N multisig wallet, any one of the N participants can create an unlimited number of deposit requests, and there is no way to delete these requests. The Ethereum Foundation wallet seems to be **not** vulnerable to this, because 4 of 7 participants can simply keep revoking transactions. However, the Gnosis multisig (code [here](https://github.com/ethereum/dapp-bin/blob/644690dfb8afe31b0b21c7c73c917cf629b4d156/crowdfund/crowdfund.se)). seems to be vulnerable.

**Solution** - store each pending transaction as a contract, with a short TTL (as there’s no particular reason for long TTLs in any case)

### Stateless multisig wallets

**Effect of rent** - some classes of multisig wallets do not store state except for a list of owners and a sequence number (eg. [this Vyper multisig](https://github.com/ethereum/vyper/blob/master/examples/wallet/wallet.vy)). These are not vulnerable to attacks because they have O(1) storage.

### ENS

**Effect of rent** - vulnerable to griefing attacks: anyone can register an unlimited number of domains, and the `_entries` mapping in [the code](https://etherscan.io/address/0x6090a6e47849629b7245dfa1ca21d94cd15878ef#code) will store all of their addresses forever.

**Solution** - because ENS is contract-based already, this is easier than the others: just switch to CREATE2-based addresses, using the domain as a seed, allowing the contract address for any given domain to be generated in real-time.

### On-chain order books

**Effect of rent** - vulnerable to griefing attacks: anyone can make an unlimited number of orders with arbitrarily unfavorable terms, and these orders will stay in the state forever (eg. see [Oasisdex code](https://etherscan.io/address/0x14fbca95be7e99c15cc2996c6c9d841e54b79425#code))

**Solution I** - open orders become contracts.

**Solution II** - orders are stored in a Merkle priority queue; accepting an order involves simply providing Merkle proofs of the `pop` operation. Note that this also solves the on-chain sorting problem.

### Smart contracts representing agreements

**Effect of rent** - some implementations of smart contracts representing agreements (eg. crowdfunds, escrows, CFDs…) for efficiency reasons put all agreements into the same contract (eg. see this [very old implementation of crowdfunds in Serpent](https://github.com/ethereum/dapp-bin/blob/master/crowdfund/crowdfund.se)). These would be vulnerable to griefing attacks. However, designs where a separate contract is used for each agreement are *not* vulnerable to griefing attacks.

**Solution** - switch to a design where a separate contract is used for each agreement.

### Privacy-preserving contracts (mixers, anonymous voting, etc)

**Effect of rent** - some classes of privacy-preserving mixers work using the following mechanism. Anyone can join the mechanism by providing 1 coin along with a commitment c. They can then withdraw the coin at any time by providing a value I such that f1(x) = c and f2(x) = y for some f1 and f2 where x is a secret. Because of cryptographic machinery, there is only one possible I for each c, and using x it’s possible to prove that some given I corresponds to *one* of the commitments that has been published, without revealing which one. I values need to be stored so that they cannot be double-spent. This theoretically includes ring signatures and many kinds of ZK-SNARK schemes. With storage maintenance fees, each I value stored leads to an ongoing expense on chain, leading to griefing vulnerabilities.

**Solution I** - put commitments into “buckets”, each bucket corresponding to eg. the c values submitted within one specific month, and for each I value submitted require the prover to make a proof based on a specific bucket. Store the bucket ID. Run a background process that deletes I values that are too old.

**Solution II** - put commitments and I values into a Merkle tree.

**Solution III** - put used I values into an accumulator which allows succinct proofs of non-membership, eg. a [STARK-based accumulator](https://ethresear.ch/t/a-sketch-for-a-stark-based-accumulator/4382) if one wants a purely hash-based construction.

## Replies

**mkoeppelmann** (2018-12-01):

I think I have a different proposal for a rent mechanism that does not suffer from “tragedy of the commons” or “griefing”

The 3 sentence version:

Contracts don’t pay rent at all. Instead - when you access any particular storage slot during a call the gas cost is a decreasing function based on the time difference since the last storage access (and thus last payment). After a specific time/ costs limit full nodes can prune storage slots. If a call will access those slots the call will fail unless it provides (stateless style) the required proofs for that data in the payload.

One option to think about would voluntary payments to make sure that a future call will not have to deal with that.

So with the design the token contract does not care about an individual tiny balance. If no one will access this data it will not create future costs and will just be pruned at some point.

---

**AlexeyAkhunov** (2018-12-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> Contracts don’t pay rent at all. Instead - when you access any particular storage slot during a call the gas cost is a decreasing function based on the time difference since the last storage access (and thus last payment). After a specific time/ costs limit full nodes can prune storage slots. If a call will access those slots the call will fail unless it provides (stateless style) the required proofs for that data in the payload.
> One option to think about would voluntary payments to make sure that a future call will not have to deal with that.

this is very similar to what Roostrock seems to be going with at the moment ([RSKIPs/IPs/RSKIP61.md at 5920b0fa44f5b2d690cef24fdedd7b0b9f18de8c · rsksmart/RSKIPs · GitHub](https://github.com/rsksmart/RSKIPs/blob/5920b0fa44f5b2d690cef24fdedd7b0b9f18de8c/IPs/RSKIP61.md)). I reviewed this and found that, for the existing contract architectures, it is still vulnerable to griefing attacks. Here, instead of bankrupting the contract directly, the attacker would efficiently penalise all users of the contracts, because the cost of calls needs to depend on the contract size, like in this line: [rskj/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java at 37e18f6d41b20eae353a7fab0e3a7c9479520bb4 · rsksmart/rskj · GitHub](https://github.com/rsksmart/rskj/blob/37e18f6d41b20eae353a7fab0e3a7c9479520bb4/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L678)

In order to solve that, one would need to introduce separate timestamps for all storage items, which now becomes similar to solutions proposed in the original post. To prevent extra transaction churn (or what Sergio calls “the problem that rent payments are micro-transactions”), in the Rootstock solution, the rent payment is waived if the contract has been last touched less than 10’000 seconds ago (for reading) or 1000 seconds ago (for writing). This, however, would mean that someone would try to ensure that the contract is read or modified every 1000 seconds. If the context of individual timestamps for storage items, this could invite a lot of extra transactions just to maintain the status-quo (one of the critiques to my rent proposals which I managed to solve, I think).

---

**vbuterin** (2018-12-01):

> Here, instead of bankrupting the contract directly, the attacker would efficiently penalise all users of the contracts, because the cost of calls needs to depend on the contract size

If the gas cost is logarithmic in storage slot count (which seems reasonable as that’s the proof length), then the logarithm is *basically* capped at ~80, so that’s manageable.

I do like the proposal as it is much more backward-compatible. The one issue that is does have is that once a contract’s storage stops being available, if the contract makes dynamic storage accesses it becomes difficult to use (though not impossible, especially if the contract is only touched once per block). The main use case of dynamic storage access that I can see is adding to a list, and priority queues as in on-chain order books, but it’s not that big a loss if those become infeasible.

---

**AlexeyAkhunov** (2018-12-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If the gas cost is logarithmic in storage slot count (which seems reasonable as that’s the proof length), then the logarithm is basically capped at ~80, so that’s manageable.

Sorry, I don’t understand why proof length is relevant here. The gas cost is linear to the number of the storage slots because this is how much state anyone will need to download if they want to sync

---

**vbuterin** (2018-12-01):

Wait, the gas cost for editing one storage slot in RSK is linear in the number of existing storage slots? So quadratic total cost for N slots? This seems extreme and unnecessary…

If a contract gets too big, then fast-sync clients should just avoid syncing its state.

---

**AlexeyAkhunov** (2018-12-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Wait, the gas cost for editing one storage slot in RSK is linear in the number of existing storage slots?

Well, that is my point earlier - if you want to make not linear in the number of existing storage slots, and still keep time-based cost - you would need to have timestamps for each storage slot separately, not just for the contract itself. Which brings us closer to your proposals above and LCCS

---

**vbuterin** (2018-12-01):

Right, agree. I personally am inclined to say don’t bother with time-based cost on a per-slot basis, and instead simply have two “modes” for the contract, one where enough rent is paid to cover all slots and the other where it is not, and in the latter case add a high fixed gas cost per access (eg. by requiring witnesses to be in transaction data and charging 68 gas/byte for them).

---

**antoineherzog** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Solution I - store the balance associated with each user in a contract made with CREATE2 using the user’s address as a seed. Require the user to keep these contracts topped up. Note that for efficiency this can be combined across many applications by creating a generic UserStorageFactory contract, where a contract C can, with permission of user U, add an entry at a contract with a CREATE2 address made with sha3(C, U) as a seed.

This solution means the user will pay for the rent and brings the question of the chicken or the egg causality dilemma? Let’s say i am a new user. I generate a public/private key. Someone wants to send to me some REP. How can I pay my rent as I don’t have any ETH?

Compare to the existing solution, it increases the complexity for new user to join the blockchain world which is not good. I believe sometimes, the end-user is totally forgotten of the equation ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=12)

Should our goal be to think about the end-user first? (if we really want to get to mass-adoption for the Internet of Values)

---

**AlexeyAkhunov** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> This solution means the user will pay for the rent and brings the question of the chicken or the egg causality dilemma? Let’s say i am a new user. I generate a public/private key. Someone wants to send to me some REP. How can I pay my rent as I don’t have any ETH?
>
>
> Compare to the existing solution, it increases the complexity for new user to join the blockchain world which is not good. I believe sometimes, the end-user is totally forgotten of the equation

I think solution with CREATE2 above is a valuable direction to explore. It tries to solve griefing and free-rider problem that were described in the State rent proposal. I am going to explore it a bit more before commenting further, to see what is the difference between this and LCCS.

Receiving tokens like REP without having any ETH could still be achieved under rent regime, but indirectly. End-users are not forgotten, but they will need to do more work to receive and keep their assets, because a platform subsiding all of that seems to be un-sustainable.

The goal here is to prioritise the survival of the platform. Without platform, there will be no end-users.

---

**prateek** (2018-12-02):

> In order to solve that, one would need to introduce separate timestamps for all storage items, which now becomes similar to solutions proposed in the original post.

Instead of maintaining the timestamps of all storage items individually, can we collect the storage rent in epochs(common expiry date). Any user who wants to store some data on a contract can pay for rest of the current epoch and next epoch(optional). At the end of the epoch, if the data is not paid for the next epoch then it is removed from state in which case, witness has to be provided for reviving the removed data.

PS: I have written a model for rent collection based on epochs [here](https://ethresear.ch/t/improving-ux-for-storage-rent/3994).

---

**AlexeyAkhunov** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/prateek/48/1837_2.png) prateek:

> Any user who wants to store some data on a contract can pay for rest of the current epoch and next epoch(optional). At the end of the epoch, if the data is not paid for the next epoch then it is removed from state in which case, witness has to be provided for reviving the removed data.

This implies that data within a contract can be selectively removed and revived, rather than the entire contract removed/revived. Which can be decomposed into Cross-Contract storage, or schemes with CREATE2 owner’s contracts that Vitalik mentioned above

---

**AlexeyAkhunov** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Solution I - store the balance associated with each user in a contract made with CREATE2 using the user’s address as a seed. Require the user to keep these contracts topped up. Note that for efficiency this can be combined across many applications by creating a generic UserStorageFactory contract, where a contract C can, with permission of user U, add an entry at a contract with a CREATE2 address made with sha3(C, U) as a seed.

This is a great idea, thanks for this contribution - I have been thinking about it today, and it seems to me that this could be a suitable alternative to LCCS, provided that we solve eviction notification, which is not too difficult.

I am going to try three things next:

1. Implement an example of ERC-20 contract and a corresponding token holder contract (which could be made to support multiple tokens, I think), and see if it works.
2. Use heuristic and automation to gather more accurate data (I had to use manual inspection before) about the share of ERC-20 tokens in the current state
3. If (1) works out, I will look into comparative efficiency of this scheme and LCCS, and modify State rent proposal accordingly, adding modification to the eviction notification.

---

**jvluso** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> This solution means the user will pay for the rent and brings the question of the chicken or the egg causality dilemma? Let’s say i am a new user. I generate a public/private key. Someone wants to send to me some REP. How can I pay my rent as I don’t have any ETH?

You wouldn’t. The contract would quickly get evicted, and if you later wanted to spend it, you could recover it and spend the REP by proving that the contract previously existed.

---

**AlexeyAkhunov** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/jvluso/48/1490_2.png) jvluso:

> if you later wanted to spend it, you could recover it and spend the REP by proving that the contract previously existed

This just made me realise, that at least for token contracts, eviction notifications might not be as important as I thought - since the evicted holders can be brought back, technically, those tokens are still part of the supply - so the totalSupply does not need to be reduced when the token holders get evicted. This could make things even simpler. Thank you for that thought!

---

**antoineherzog** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> Implement an example of ERC-20 contract and a corresponding token holder contract (which could be made to support multiple tokens, I think), and see if it works.

I would be very interest to see this implementation! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**veox** (2018-12-03):

Thanks for starting this!

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> ### ENS
>
>
>
> Effect of rent - vulnerable to griefing attacks: anyone can register an unlimited number of domains, and the _entries mapping in the code will store all of their addresses forever.
> Solution - because ENS is contract-based already, this is easier than the others: just switch to CREATE2-based addresses, using the domain as a seed, allowing the contract address for any given domain to be generated in real-time.

May I highlight that the `.eth` Registrar (for forward name->address resolution) is just one piece of the ENS system.

There is the Registry, which is currently much more susceptible to griefing, as “higher-level domains” are “free”. (Quotes here, since the Registry is actually oblivious of the concept of names/domains, operating on hashes only.)

This is proportional in the Public Resolver, probably the most popular resolver (as it’s “free for use of public” and requires no personalised deployment); and the Reverse Registrar/Resolver dual-purpose contract - perhaps to a lesser extent, as there’s only one entry possible per account address, instead of an entry for any conceivable name (as in the case of the “forward” resolver).

Then there are the Deed contracts, a copy for every auction entry; but their impact on storage bloat (and rent) is proportional to that of the `.eth` Registrar, which you’ve mentioned.

---

~~(Sorry for not linking all these mentioned contracts just yet - in a bit of a hurry. Ping to remind me to do this.)~~

See [@nickjohnson’s reply](https://ethresear.ch/t/common-classes-of-contracts-and-how-they-would-handle-ongoing-storage-maintenance-fees-rent/4441/22) with actual links.

---

**jvluso** (2018-12-03):

I made an implementation of an ERC20 token that stores its state in separate contracts over the weekend. I’m not sure if it works - the tests aren’t using Constantinople. It’s at https://github.com/jvluso/openzeppelin-solidity/blob/c683a5bca151f1e10b6ff9dd247b575c9914415a/contracts/token/ERC20/ERC20.sol .

---

**AlexeyAkhunov** (2018-12-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/jvluso/48/1490_2.png) jvluso:

> I made an implementation of an ERC20 token that stores its state in separate contracts over the weekend

Thank you for that! I am trying to do the same, and I will definitely use some of the ideas from your code. I am going to be doing Constantinople uint tests too. Will post here in couple of days when I have the first version

---

**AlexeyAkhunov** (2018-12-04):

So I have some data on ERC20 tokens. I used successful invocation of “transfer” function to detect ERC20 contracts. By successful I mean either returning zero-length output (earlier version of the standard), or non-zero output 32 bytes long.

At block 6813760, which is 2nd of December, there were 149’746’097 storage items in total, spilt across 7’014’024 contracts. Note that there are also zero-storage contracts (like the ones created by GasToken2), these are not counted into this number. In fact, 4’619’309 contracts have a single item in their storage.

ERC20 heuristics identified 71139 ERC20 contracts. That includes CryptoKitties_Core, because it is both ERC20 and ERC721. And these 71139 contracts collectively occupy 80’504’952, which is about 53.7%

It would be easier to identify all ERC721 contracts, because the standard demands that Transfer event is to be issued on any transfers. But the strategy for further data analysis is to remove all ERC20 contracts from the dataset and see what seems to be the largest category now.

---

**AlexeyAkhunov** (2018-12-04):

I have also started on my implementation of ERC20. Have not tested anything yet, but the general idea is to try to have a holder contract being able to hold arbitrary number of tokens, instead of having one holder contract per (token, owner) pair. I might also do data analysis on what is current number of these pairs.

Code is here, but tests will come later: https://github.com/ledgerwatch/eth_state/tree/master/erc20


*(10 more replies not shown)*
