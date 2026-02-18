---
source: magicians
topic_id: 3045
title: Removing or Increasing the Contract Size Limit
author: maxsam4
date: "2019-03-31"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/removing-or-increasing-the-contract-size-limit/3045
views: 13276
likes: 35
posts_count: 28
---

# Removing or Increasing the Contract Size Limit

**Abstract**

A contract size limit of 24KB was introduced by [EIP #170](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-170.md) to solve the problem:

“When a contract is called, even though the call takes a constant amount of gas, the call can trigger O(n) cost in terms of reading the code from disk, preprocessing the code for VM execution, and also adding O(n) data to the Merkle proof for the block’s proof-of-validity”.

I think we can solve this problem in a way that allows contract size to be higher than 24KB. Complex dApps require complex smart contracts. I have seen many dApp developers struggle with this. A few people have provided their feedback on [this GitHub Issue](https://github.com/ethereum/EIPs/issues/1662), and I know many more that are struggling with this. When this limit was introduced, It was not a big Issue, but since then, many things have changed like:

1. More complex dApps are now being built on top of Ethereum, and after Serenity upgrade is complete, Ethereum will be able to support even more complex dApps.
2. EIP 838 Allows adding reason strings to reverts which makes it much easier to debug smart contracts. However, the reason strings take up a lot of contract size. Although the EIP is not finalised, most clients already support this, and it is actively used.
3. Newer versions of Solidity have more type checks that Increased the size of contracts. Often, you’ll find that a contract that was working fine with an old version of solidity is no longer deployable with newer versions of Solidity.

**Current Solution**

Delegate call proxy patterns and Libraries: Using delegate calls, you can store the code of your smart contract in parts in different contracts and have a “dispatcher” contract that calls the actual contract using delegate calls. Please refer to [ZeppelinOS’s upgradability contracts](https://github.com/zeppelinos/zos/tree/master/packages/lib/contracts/upgradeability) and [EIP #1538](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1538.md). If you are interested in understanding how this works, I wrote a [blog post that you can read](https://hackernoon.com/how-to-make-smart-contracts-upgradable-2612e771d5a2). Libraries also use delegate call under the hood. If you want to learn more about Libraries, I recommend [this blog post by Aragon](https://blog.aragon.org/library-driven-development-in-solidity-2bebcaf88736/).

**Limitations of the current solution**

1. It adds extra unnecessary code.
2. Proxy patterns add another attack vector.
3. Proxy patterns make calls to contracts a lot more expensive as the Proxy has to copy the parameters make an external delegate call every time.
4. Proxy patterns like EIP 1538 also make inter-logic contract call a lot more expensive. We have to make an expensive external call to the proxy that in turns make a similar call to the other logic if we had to access a function that is in the other logic contract. If the contract size was larger, both these functions could have been in the same contract, and we would have had to make only an internal call which is almost free.
5. Proxy patterns hurt readability for the end user. The actual contract code/ABI of the proxy is different from the one we need to access the contract behind the proxy. Like it or not but most people can barely use the read/write features in etherscan, they can’t load a custom ABI and make web3 calls.
6. Proxies make smart contract development slightly more complex.
7. Proxies make it harder to verify the actual code and hence reduce trust.
8. Loading a large contract will be sequential read while loading multiple small ones will be random read. Sequential read is way faster than random reads.

**Possible Solutions**

1. Increase contract size limit to 32,768 (2**15, also happens to be exactly the size of two 16k I/O blocks) as it was proposed by @gavofyork in the EIP 170 discussion. This change will give dApp developers a 50% more code size to work with which will be able to accommodate the reason strings and other Solidity changes. This is the easiest solution to implement. If required, relevant opcodes like CALL can have their cost increased by a bit through EIP #1838.
2. Allow infinite contract size and make the cost of OPCODES like CALL dynamic to allow for this change. Code size will still be limited by block gas limit. This is a moderate difficulty change but makes a lot of sense IMO. More on this later.
3. Allow infinite contract size by Implementing paging of contract code as suggested by @SergioDemianLerner in EIP #170 discussion: Make contracts a vector of 24 Kbytes pages. The first page is loaded for free when a CALL is received while jumping or running into another page pays a fee (500 gas) because the page must be fetched from disk. This is an interesting approach but as Vitalik said, “In the long term, we could do pagination, but doing that properly would require changing the hash algorithm used to store contract code - specifically, making it a Patricia tree rather than a simple sha3 hash - and that would increase protocol complexity, so I’m not sure that would actually create significant improvements on top of the delegatecall approach.”

**Making the cost of OPCODES like CALL dynamic**

**Method**

1. The ethereum account array in state trie saves another element codeSize apart from existing 4: [nonce,balance,storageRoot,codeHash]
2. Whenever a new contract is deployed, its size is stored in codeSize of the account object.
3. If a contract is destructed, the codeSize should also be reset.
4. opcodes like CALL, DELEGATECALL, CALLCODE etc should charge additional X(3?) gas per extra word if the contract code size is greater than 24KB.

**Rationale**

The only reason why the contract size was limited was to prevent people from exploiting the fixed costs. We can overcome this by making the costs variable. The codeSize element will help in calculating call cost before reading the whole contract and eventually throwing OOG. Merkle proofs will also be generated at a fixed cost as we won’t have to load whole contracts from disk first. The codeSize should be enough for generating Merkle proofs of calls that are going to be OOG due to contract size.

**Backwards Compatibility**

All the existing accounts have less than 24KB of code, so no extra cost has to be charged from calls being sent to them. We can assume words to charge extra gas for = 0 if it’s not available. Alternatively, we can refactor existing DB to include proper codeSize of every contract so that we can use this variable in other things. The hashes before FORK_BLOCK will be generated as if there was no such field and hashes after the FORK_BLOCK will contain this field.

## Replies

**gcolvin** (2019-03-31):

I’m favor of this.  The current limit is ridiculously small.

---

**fubuloubu** (2019-03-31):

Can confirm. I’ve written a simple Plasma contract, and it takes 90% of the the storage limit, which does not bode well for others to implement similar complexity things.

---

**atoulme** (2019-03-31):

Sounds like a good idea to at least make it possible to configure this for private chains.

See https://github.com/ethereum/EIPs/issues/659 for a recent discussion on this as well.

---

**amiromayer** (2019-03-31):

Agree. The only solution I could come up with to solve this issue was by splitting contract to several small ones and connect them using ERC1538. And I’ve faced this contract size limit issue in several projects already. Its really annoying.

---

**lukas-berlin** (2019-03-31):

I also agree. As I recall EIP170 was quickly created shortly after the Shanghai attack. I ran into this problem myself and saw a lot of questions about this on gitter. More and more devs are starting to run into this limit. 50% increase would be an improvement. Perhaps we can just let the blockgaslimit take care of this.

When EIP170 was accepted the block gas limit was below 4700000 and the limit couldn’t be reached.

> The maximum size has been set to 24576 bytes, which is larger than any currently deployed contract.

With the current block gas limit, the limit for code deposit would be 39735. (8000000-53000)/200

So to me EIP170 looks like a quick fix. Perhaps there could be a discussion in the core devs meeting if this EIP is still needed.

---

**vbuterin** (2019-03-31):

Personally I’d oppose this, and in fact the proposal in serenity is to make the code size cap *even smaller* (~12kb for code+storage combined). Anything that you can do with a single contract you can do with a system of connected contracts, you just need the right high level language to take care of it. The problem with allowing individual contract code to get big is that (i) fixed costs associated with compiling/preprocessing the contract get big, and (ii) Merkle proofs for the contract get big. You can solve (ii) by adding a “tree inside a tree” mechanism like we do for storage, but then that’s exactly the kind of complexity that we’re trying to move away from.

How could we improve HLLs to make this a non-issue? Maybe delegatecall contraptions where each function definition is stored in a separate contract? That could actually be really good for code redundancy.

---

**fubuloubu** (2019-03-31):

It also extremely complicates the protocol, increases the attack surface, and makes work on execution layer improvements more difficult.

Why not find a way to work with it instead of against it?

---

**gcolvin** (2019-03-31):

A big motivation for eWasm is to allow for a large number of HLLs to target Ethereum contracts, and that is a goal of the EVM Evolution project as well.  So counting on better HLLs isn’t going to help.

And moving to even smaller contract sizes is going to make migrating code from the existing blockchain to Serenity shards even more difficult, as many EVM programs are not going to fit when transpiled to eWasm.

---

**maxsam4** (2019-04-01):

First of all, Thanks for your feedback. Please Allow me to address some of your concerns.

> fixed costs associated with compiling/preprocessing the contract get big

1. There are no costs attached with compiling as contracts are compiled by the user and not the nodes.
2. I am proposing to make the fixed costs of preprocessing/loading the smart contracts variable. Please refer to the first post for details.

> Merkle proofs for the contract get big. You can solve (ii) by adding a “tree inside a tree” mechanism like we do for storage

As I understand, trees for the storage are required because the storage can change in every transaction and hence Merkle proofs are required to be generated every time. However, contract code is fixed and hence the Merkle proof needs to be generated only while deployment of the contract. As the cost of deployment goes up with contract size, I don’t think this is an Issue. (I am not entirely sure if we need to generate fresh merkle proof of contract code with every tx or not. It doesn’t sound like something we’ll need to do but I am not sure.)

> How could we improve HLLs to make this a non-issue? Maybe delegatecall contraptions where each function definition is stored in a separate contract? That could actually be really good for code redundancy.

Please refer to the limitations of Delegate call in my first post. It basically makes everything much more expensive for the nodes and the callers. Also, as [@gcolvin](/u/gcolvin) mentioned,  “A big motivation for eWasm is to allow for a large number of HLLs to target Ethereum contracts, and that is a goal of the EVM Evolution project as well. So counting on better HLLs isn’t going to help.”

> the proposal in serenity is to make the code size cap  even smaller  (~12kb for code+storage combined)

This is going to be a deal breaker for a lot of dApp developers. Have you talked to people actually building on top of Ethereum about this? All major dApps will break.

12KB isn’t enough to even make a dispatcher that stores (many) contract addresses to call against function selectors, parse incoming call to detect the function selector, delegatecall to the relevant address. You also need space for the actual storage.

---

**vbuterin** (2019-04-01):

> However, contract code is fixed and hence the Merkle proof needs to be generated only while deployment of the contract.

False. Because the crosslink committee that is verifying a block does not have the state ahead of time, it will need to generate a fresh Merkle proof, effectively meaning that every time a contract is called translates to a significant amount of bandwidth, including the entire contract code.

> 12KB isn’t enough to even make a dispatcher that stores (many) contract addresses to call against function selectors, parse incoming call to detect the function selector, delegatecall to the relevant address. You also need space for the actual storage.

It’s definitely enough in EVM! And if EVM can do this in 1 KB (which I’m confident it can; it’s just a simple matter of `mstore(28, calldataload(0)); if mload(0) == 0x12345678: call(foo); if mload(0) == 0x9abcdef0: call(bar)....`) and EWASM somehow can’t, then to me that would be evidence that the EWASM plan should just be scrapped in its entirety and we should just adopt a modified version of EVM that uses 64 bits as its base stack value size with other improvements like maybe SIMD and banning dynamic jumps.

> Proxy patterns make calls to contracts a lot more expensive as the Proxy has to copy the parameters make an external delegate call every time.

How is copying parameters expensive? It’s only maybe ~100 gas. In practice, the gas consumption of function calls is tiny compared to the gas consumed for tx data, SSTORE, SLOAD, LOG, ETH send and similar operations.

---

**maxsam4** (2019-04-01):

> False. Because the crosslink committee that is verifying a block does not have the state ahead of time

I admit that I haven’t kept up with the 2.0 specs and all my statements are based on eth 1.x. Consider this a proposal for eth 1.x. I don’t believe there is anything like crosslink committee in eth 1.x.

> it’s just a simple matter of  mstore(28, calldataload(0)); if mload(0) == 0x12345678: call(foo); if mload(0) == 0x9abcdef0: call(bar).... )

It’s not… call won’t work. We’ll need to use delegate calls and handle the parameters (return and function parameters). Address of the contracts will need to be hardcoded which will take space. An average contract can have ~50 functions (including internal functions). Storing full address for each function will require a decent amount of space. As you are suggesting that 12KB will be limit for storage + code, that will leave a lot less space available for storage and contracts will just break. Even ERC20 tokens with a lot of holders won’t fit in the remaining space. Also, please refer to other drawbacks of delegatecall methods that I mentioned in the first post.

> How is copying parameters expensive?

Copying the parameters is not the main concern here. Needing to make an extra external call (delegatecall) is. It will increase the cost of an average erc20 transfer by 5-10% (~2500 gas).

---

**vbuterin** (2019-04-01):

The addresses can be dynamically generated if you use CREATE2. An O(1) fowarder would just look like: `delegatecall(hash(0xff + self + mload(0) + hash(init_code)))`.

> An average contract can have ~50 functions (including internal functions)

You don’t necessarily need one contract per function; if you want to save on contract count, then you can group functions as well. The point is that this would be HLL-level pagination, and regardless of the page size the forwarder can be made to be O(1).

> Even ERC20 tokens with a lot of holders won’t fit in the remaining space.

The goal is that per-user storage (or really any storage that is not O(1)) would live in separate contracts (see eg. the examples here: [Common classes of contracts and how they would handle ongoing storage maintenance fees ("rent") - Economics - Ethereum Research](https://ethresear.ch/t/common-classes-of-contracts-and-how-they-would-handle-ongoing-storage-maintenance-fees-rent/4441)). This is a good idea anyway because it makes rent accounting much cleaner; the storage belonging to a particular beneficiary is stored in a contract that the beneficiary themselves is responsible for paying the ETH to kep up. Rent/hibernation/waking schemes that keep the current monolithic O(N)-sized storage tree model tend to be much more complicated.

> Needing to make an extra external call (delegatecall) is. It will increase the cost of an average erc20 transfer by 5-10% (~2500 gas).

This is an artefact of present-day gas costs, not necessarily a reflection of costs in reality. If you go back to the discussion in 2016 that led to the current 700 gas cost for delegatecall (see eg. [Long-term gas cost changes for IO-heavy operations to mitigate transaction spam attacks · Issue #150 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/150)), one of the competing proposals (option 2) was effectively a gas cost that scales with contract size. If that had been implemented, then modular contract structures would be *favored* because they would not load parts of code that don’t need to be accessed, so the total gas cost of making calls would be lower.

Additionally, delegatecall is expensive in part because of known weaknesses in the current gas cost model (eg. self-calling, and calling a contract that was already called in the same block, are gas-expensive despite being cheap in reality) which should not be taken as a given; if we are making changes to the code these isuses can be remedied.

If eth1.x is going in a stateless client direction then the byte size of contracts becomes a large cost component, and so we should adopt version 2 of EIP 150 as that would more accurately reflect costs, and we should favor contract modularity. If eth1.x is *not* going in a stateless client direction (ie. it’s doing rent), then the cost of loading large amounts of code is lower; I suppose we would ask the experts to determine whether the per-page loading cost is sufficiently high that favoring contract modularity is optimal. If loading any amount of data up until a few dozen kilobytes is basically O(1) and we’re not doing stateless clients, then I would agree that bumping up the max contract size is optimal.

---

**maxsam4** (2019-04-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> The addresses can be dynamically generated if you use CREATE2. An O(1) fowarder would just look like: delegatecall(hash(0xff + self + mload(0) + hash(init_code))) .

Except we don’t have space to store the `init_code`.

> Additionally, delegatecall is expensive in part because of known weaknesses in the current gas cost model (eg. self-calling, and calling a contract that was already called in the same block, are gas-expensive despite being cheap in reality) which should not be taken as a given; if we are making changes to the code these isuses can be remedied.

Agreed. cost for calling the same contract again in a single transaction should be much lower.

The net call cost will still remain higher in paging model than if a bigger contract size was allowed. Imagine a case where the contract size is 30KB. If it is split into two pages + dispatcher, we’ll still have to make at least 2 extra full price delegatecalls (dispatcher to page 1 then dispatcher to page 2) and multiple “cheaper” delegate calls (page to dispatcher and repetitive dispatcher to page calls) which will still be slightly more expensive than internal calls due to parameter copying. If contract size of >24KB was allowed, it will only cost the caller ~1000 extra gas to pay for the extra code size.

Paging is more resource heavy due to random reads than loading a big contract which is sequential read. It’s fair that gas costs reflect this but this begs the question, what’s the advantage of using paging? The stateless client will anyway have to fetch the code of all the loaded pages which will, in fact, be larger because it will contain the paging logic. Paging will only make sense if the functions are independent of each other. Which rarely is the case.

Thanks for pointing towards the resources, I’ll have a read!

---

**vbuterin** (2019-04-02):

> Except we don’t have space to store the init_code .

Only need to store the hash of the init code ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> The net call cost will still remain higher in paging model than if a bigger contract size was allowed. Imagine a case where the contract size is 30KB. If it is split into two pages + dispatcher, we’ll still have to make at least 2 extra full price delegatecalls (dispatcher to page 1 then dispatcher to page 2) and multiple “cheaper” delegate calls (page to dispatcher and repetitive dispatcher to page calls) which will still be slightly more expensive than internal calls due to parameter copying. If contract size of >24KB was allowed, it will only cost the caller ~1000 extra gas to pay for the extra code size.

Are you predicting that the average call will end up executing code from *every* piece of a contract? In an eth2 context, that sounds like a big problem if true! Though I don’t think it’s true; checking Uniswap for example, every call only ends up making maybe 1-2 sub-calls, and there’s a pretty natural pagination between `{small utility functions, big function 1, big function 2 ... }`. Would definitely be interested in seeing a deeper study of this though!

---

**maxsam4** (2019-04-02):

> Only need to store the hash of the init code

We can just store pre-computed address at that point. Doesn’t make sense to compute it on the fly.

> In an eth2 context, that sounds like a big problem if true!

I guess contracts can be re-architectured to overcome this problem. However, In most calls, you’ll need to load at least 3 pages (main dispatcher, utility function page, main function page). That requires 3 random read i/o blocks. If it were a monolithic single contract, It would have required only 1 block read (Most SSD have block size > 512 KB). This means it will be more taxing for the full nodes to process paged contracts.

I agree that for stateless clients, it’s better to have paged contracts if they are architectured properly. I don’t see many people using stateless clients though.

That being said, I don’t see this as a big problem for even stateless clients. If anyone was going to dos stateless clients, they can just create 24KB contracts and call an empty function on each of them. As the cost of CALL is going to increase as the size of contract increase over 24KB, It won’t make a difference if the griefer uses 24KB contracts or 32KB.

The effect of average daily use will be minimal and worth the advantages IMO.

---

**dev1644** (2019-04-02):

Agree with [@maxsam4](/u/maxsam4), current limitation restrict  developers to develop complex logic, usage of multiple contracts increase the number of files which are hard to manage.

---

**gcolvin** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> EVM that uses 64 bits as its base stack value size with other improvements like maybe SIMD

The vector abstraction of SIMD gives you 64 bit (and other powers of 2) stack items as one-element vectors.  I think [@expede](/u/expede) has a more interesting idea of switching the default 256-bit operators to work with natural numbers of unlimited size.

---

**vbuterin** (2019-04-03):

> We can just store pre-computed address at that point. Doesn’t make sense to compute it on the fly.

But if the init code is shared, then it’s O(1). Storing pre-computed addresses would be O(N).

> I agree that for stateless clients, it’s better to have paged contracts if they are architectured properly. I don’t see many people using stateless clients though.

As mentioned, in an eth2 context half of all validation will be done in “stateless” mode, and in the worst case more than half because fraud proofs are stateless. For eth1.x I agree the situation is not the same.

So this does sound to me like paging makes sense for eth2, but doesn’t make sense for eth1.x unless we end up going with the stateless client route for state size control. So that suggests we should wait for [@AlexeyAkhunov](/u/alexeyakhunov)’s proposals and see whether stateless clients or rent or some hybrid work best and go from there?

> I think @expede has a more interesting idea of switching the default 256-bit operators to work with natural numbers of unlimited size.

That sounds cool! In principle, I definitely think that only two types of numbers make sense for a VM to have: 64 bit, and unlimited size. If we have the code for doing fixed-size bigint math, then it seems like the sort of thing that would be easy to adapt to sizes of different powers of two.

---

**maxsam4** (2019-04-03):

> But if the init code is shared, then it’s O(1). Storing pre-computed addresses would be O(N).

Ah so you are talking about the case where pages share the same/similar code and are used for rent distribution. I was thinking more about paging to divide functions into different pages.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> So this does sound to me like paging makes sense for eth2, but doesn’t make sense for eth1.x unless we end up going with the stateless client route for state size control. So that suggests we should wait for @AlexeyAkhunov’s proposals and see whether stateless clients or rent or some hybrid work best and go from there?

I think this should be independent of rent as bigger contract size shouldn’t affect rent calculation. I agree that rent will require re-architecture of a lot of existing smart contracts to divide the rent costs among users but that’s more of a design question and not something that can be forced.

If we increase focus on stateless clients, then I’d agree that their bandwidth requirements will increase a little but I think the increase will be marginal in real and not of much significance. The increase in resource requirements if we increase block gas limit by even 50% will be much more (>5 times by my guess) than the increase caused by this change. I’d argue that this change is worth the minor resource requirements increase.

Tagging [@karalabe](/u/karalabe) for his thoughts as he is working on reducing state size.

---

**AlexeyAkhunov** (2019-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> So that suggests we should wait for @AlexeyAkhunov’s proposals and see whether stateless clients or rent or some hybrid work best and go from there?

I am still wrangling with the data on the stateless client, to complete my [post](https://medium.com/@akhounov/data-from-the-ethereum-stateless-prototype-8c69479c8abc), but I would propose (in the 4th version of State fees/rent proposal) to only introduce stateless clients approach for contract storage items. I am currently missing data on whether size of the block proofs (witnesses) for contract storage eventually overtook the block proof for accounts and for the code size, because at the block 5.4m those 3 components were roughly on par. That is it to say, that byte codes played significant part in the block proof, and increasing contract sizes can push it up even further.

Even if we were to go with the pagination approach, we need still look at the compilers to try to optimise the code so that the code of specific functions are partitioned well (i.e. usual function calls do not end up touching all the pages).

In general, I would approach this proposal with caution, and also in the context of other EIPs that propose to change EVM, most notable EIP-615. I would definitely welcome more research.

For example, it was noted that the code of the contract is inflated by the PUSHx opcodes storing data inline in the code. Perhaps, the solution to this is to use DATA segment approach that has been introduced into EIP-615?

Another point - some of the desire to put lots of code into a single contract stems from the fact that this code wishes to access the same storage, without calling wrapper contracts. Currently, it is very appealing, because reading storage (SLOAD) cots 200 gas, and any call to a wrapper adds an extra cost of 700 gas to that, so it ends up being 900. But the cost of SLOAD is likely to be increased 4x or 5x, because it is overpriced, so the relative win from co-locating the storage would decrease.


*(7 more replies not shown)*
