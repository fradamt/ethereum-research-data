---
source: magicians
topic_id: 4558
title: "EIP-2929: Gas cost increases for state access opcodes"
author: vbuterin
date: "2020-09-01"
category: EIPs > EIPs core
tags: [gas, eip-2929]
url: https://ethereum-magicians.org/t/eip-2929-gas-cost-increases-for-state-access-opcodes/4558
views: 70955
likes: 13
posts_count: 57
---

# EIP-2929: Gas cost increases for state access opcodes

As discussed in the calls the last couple of weeks:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2929)














####


      `master` ← `vbuterin-patch-2`




          opened 12:02PM - 01 Sep 20 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/89ac618501d77ed85e1ea0663718f590291e7737.png)
            vbuterin](https://github.com/vbuterin)



          [+165
            -0](https://github.com/ethereum/EIPs/pull/2929/files)







Increase the gas cost of SLOAD to 2100, and the CALL opcode family, BALANCE and […](https://github.com/ethereum/EIPs/pull/2929)the EXT* opcode family to 2600. Exempts (i) precompiles, and (ii) addresses and storage slots that have already been accessed in the same transaction. Additionally reforms SSTORE metering and SELFDESTRUCT to ensure "de-facto storage loads" inherent in those opcodes are priced correctly.

This is done as a short-term security improvement to reduce the effectiveness of what is currently the most effective DoS strategy, reducing the theoretical max processing time of a block by ~3x, and also has the effect of being a stepping stone toward [bounding stateless witness sizes](https://ethereum-magicians.org/t/protocol-changes-to-bound-witness-size/3885).












---

Increase the gas cost of SLOAD to 2100, and the CALL opcode family, BALANCE and the EXT* opcode family to 2600. Exempts (i) precompiles, and (ii) addresses and storage slots that have already been accessed in the same transaction. Additionally reforms SSTORE metering and SELFDESTRUCT to ensure “de-facto storage loads” inherent in those opcodes are priced correctly.

This is done as a short-term security improvement to reduce the effectiveness of what is currently the most effective DoS strategy, reducing the theoretical max processing time of a block by ~3x, and also has the effect of being a stepping stone toward [bounding stateless witness sizes](https://ethereum-magicians.org/t/protocol-changes-to-bound-witness-size/3885).

## Replies

**wjmelements** (2020-09-02):

> If the ETH recipient of a  SELFDESTRUCT  is not in  accessed_addresses  (regardless of whether or not the amount sent is nonzero), charge an additional  COLD_ACCOUNT_ACCESS_COST  on top of the existing gas costs, and add the ETH recipient to the set.

Why is it important to add the recipient to the access list if there is no ETH transferred?

---

**vbuterin** (2020-09-03):

It’s technically not, but it reduces the amount of code and special cases if it is done that way.

---

**ilanDoron** (2020-09-03):

Seems this gas scheme doesn’t take into account reading of storage slots that are already cached by the machine. Example when reading an array from storage.

One would assume cached data should have much cheaper gas cost for storage reads.

---

**vbuterin** (2020-09-03):

> Seems this gas scheme doesn’t take into account reading of storage slots that are already cached by the machine. Example when reading an array from storage.

It does! If a storage slot was already accessed in the transaction, the next access costs 100 less. If you mean sequential access, that wouldn’t actually work because storage keys are all hashed, so the elements of an array map to totally distinct random-looking locations in reality.

---

**ilanDoron** (2020-09-03):

Oh

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> elements of an array map to totally distinct random-looking locations in reality

Is this behaviour essential, could it be modified?

storing an array in memory in a sequential manner and then lowering gas price for sequential access could be very helpful. Especially with current gas price

---

**ilanDoron** (2020-09-07):

if a few different contracts query same storage. like when querying token balance after trade,

or a few contracts query same account balance.

is it considered a warm storage read?

---

**axic** (2020-09-07):

[@vbuterin](/u/vbuterin) [@holiman](/u/holiman) could the functionality of https://eips.ethereum.org/EIPS/eip-1380 be covered by this EIP? At the time EIP-1380 was discussed, the [idea of access list was brought up](https://ethereum-magicians.org/t/eip-1380-reduced-gas-cost-for-call-to-self/1242/12), which it seems to be implemented by EIP-2929.

---

**axic** (2020-09-07):

From the specification:

> When an address is either the target of a ( EXTCODESIZE  ( 0x3B ),  EXTCODECOPY  ( 0x3C ),  EXTCODEHASH  ( 0x3F ) or  BALANCE  ( 0x31 )) opcode or the target of a ( CALL  ( 0xF1 ),  CALLCODE  ( 0xF2 ),  DELEGATECALL  ( 0xF4 ),  STATICCALL  ( 0xFA )) opcode, the gas costs are computed as follows:
>
>
> If the target is not in  accessed_addresses , charge  COLD_ACCOUNT_ACCESS_COST  gas, and add the address to  accessed_addresses .
> Otherwise, charge  WARM_STORAGE_READ_COST  gas.

It is unclear to me whether the above is a cost on top of the current cost or replacing it. For `EXTCODESIZE`, etc. it seems to be replacing, but for `CALL`s I believe it may only be replacing the base cost? Can this be clarified further?

---

**axic** (2020-09-07):

Never mind, ever since I wrote [this blurb](https://hackmd.io/@axic/evm-cost-relationships) my mind has been tainted that we have complex base costs for `CALL*` opcodes, when in fact we do not. We just have a complex set of rules, but the base cost is fixed, and EIP-2929 is changing the base cost.

---

**vbuterin** (2020-09-08):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/i/51bf81/48.png) ilanDoron:

> Is this behaviour essential, could it be modified?

It’s essential because otherwise attackers could place a bunch of accounts or storage keys close to each other so as to massively increase the data costs of accessing the Merkle tree of the storage.

> if a few different contracts query same storage. like when querying token balance after trade,
> or a few contracts query same account balance.

Yes. As long as you’re reading something that was already read in the same transaction, it’s a warm storage read.

> @vbuterin @holiman could the functionality of EIP-1380: Reduced gas cost for call to self be covered by this EIP?

The behavior of EIP-1380 is already automatically a part of this EIP, because if an account is the caller, it must already be in the access list, so a call-to-self would only cost the `WARM_STORAGE_READ_COST`. This EIP also subsumes EIP-2046 (make calls to precompiles cheaper).

---

**ilanDoron** (2020-09-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> costs of accessing the Merkle tree of the storage

Is there a way, as part of this design to enable larger storage slots. Slot size could be aligned to cache sizes of avg. mining machines, so it does not introduce new EVM attack vectors. From reading analysis of loading and calculating state by clients, seems main delaying factor is related to disk reads. For linux default page size for disk reads is 4K. So maybe one solution is creating memory chunks with that size.

The costs of storage reads create great burden on any dapp in the space. Note some dapps took long months to write. The magnitude and pace of changes is quick (we just had Istanbul with x4 cost not long ago).

It seems no development efforts are directed to solve the high costs of storage reads. Hence there are missing solutions for contract designers/writers.

so some support would be appreciated.

---

**axic** (2020-09-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> @vbuterin @holiman could the functionality of EIP-1380: Reduced gas cost for call to self be covered by this EIP?

The behavior of EIP-1380 is already automatically a part of this EIP, because if an account is the caller, it must already be in the access list, so a call-to-self would only cost the `WARM_STORAGE_READ_COST` . This EIP also subsumes EIP-2046 (make calls to precompiles cheaper).

I wonder if the underpricing of `bn128_ecadd/ecmul` discovered during EIP-2046 would not have an effect here? The underpricing is described in [Precompiles and Keccak256 repricing by shamatar · Pull Request #2666 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2666). The cost proposed by 2046 is significantly lower at 40, while 2929 proposes 100, so it may not have such an effect on it, but would be good to have clarity on this.

---

**axic** (2020-09-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/i/51bf81/48.png) ilanDoron:

> vbuterin:
>
>
> costs of accessing the Merkle tree of the storage

Is there a way, as part of this design to enable larger storage slots. Slot size could be aligned to cache sizes of avg. mining machines, so it does not introduce new EVM attack vectors. From reading analysis of loading and calculating state by clients, seems main delaying factor is related to disk reads. For linux default page size for disk reads is 4K. So maybe one solution is creating memory chunks with that size.

The costs of storage reads create great burden on any dapp in the space. Note some dapps took long months to write. The magnitude and pace of changes is quick (we just had Istanbul with x4 cost not long ago).

It seems no development efforts are directed to solve the high costs of storage reads. Hence there are missing solutions for contract designers/writers.

Variable length storage was discussed previously a few times, and as recently as EthCC this year.

Two weeks ago I looked into this again, because my hunch was that at least two major use cases (multisig wallets and decentralised exchanges) would benefit from it. The sources I checked were uniswap, gnosis-multisig, and gnosis-safe.

A comprehensive analysis would mean looking at the generated code to see if subsequent storage locations are used (by subsequent here I do not mean by hash, but rather pre-hash, i.e. the key solidity uses for cases like byte arrays or structs).

While this is not a comprehensive analysis and only checked source codes, what I found is that only the multisig use case would benefit from variable length storage, all the other contracts make heavy use of mappings with value types, so they would not benefit from this. I’m sure it would open the door for new best practices or perhaps these contracts could be rewritten in a manner to benefit from it, but it is not looking as promising as I initially hoped.

That being said I would be interested to collaborate on researching this further, but my time is restricted.

I did come up with some ideas how to represent this nicely in Solidity, but that is besides the point currently.

---

**ilanDoron** (2020-09-10):

Thanks for all details. wasn’t aware.

I am part of Kyber smart contract development.

In our code base we also have excessive usage of mappings. But not always.

Some contracts do use structs and arrays (not mapped).

Adding to that, most of the contracts has a list of configurable addresses and configuration flags (enable / disable), which could benefit from a cheaper storage method. Adding to that, best practices are dynamic and will be modified.

would love to set up a call to farther discuss.

---

**holiman** (2020-09-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> I wonder if the underpricing of bn128_ecadd/ecmul discovered during EIP-2046 would not have an effect here?

Yes, that’s a good point. I’m doing some more benchmarking to check all precompiles under these rules.

---

**mudgen** (2020-09-13):

I am concerned that this EIP increases the gas cost to call external functions on proxy contracts and [diamonds](https://eips.ethereum.org/EIPS/eip-2535).

Currently an external function call on a proxy contract or diamond requires an SLOAD to get a contract address and requires executing DELEGATECALL.  The gas costs is 800 + 700 = 1500

So currently it costs at least 1500 more gas to call an external function on a proxy contract or diamond than on a regular contract.

This EIP would increase the gas cost to 2100 + 2600 = 4700.  So it would cost 4700 more gas to call an external function on a proxy contract or diamond than on a regular contract. This increased gas gap between proxies/diamonds and regular contracts hurts the utility and usefulness of proxy contracts and diamonds.

I understand this EIP is necessary and is temporary and I support it for Ethereum’s long-term health and scalability. But these changes could stay in effect for a year or longer.

I would like to know if it is possible that this EIP also require something in it that can be used to mitigate or reduce the gas costs for calling external functions on proxy contracts and diamonds.

One idea is for this EIP to require [EIP-2936](https://eips.ethereum.org/EIPS/eip-2936), which provides a new way to create proxy contracts and diamonds.

What other solutions and mitigations are possible?  Can [EIP-2930](https://eips.ethereum.org/EIPS/eip-2930) be used to solve the problem?

---

**wjmelements** (2020-09-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> So currently it costs at least 1500 more gas to call an external function on a proxy contract or diamond than on a regular contract.

Gas costs are relative. Patterns that are more burdensome on validation should cost more. Correcting issues with pricing will allow larger gas limits and thereby lower gas prices, making the effective difference comparable to before.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> One idea is for this EIP to require EIP-2936 , which provides a new way to create proxy contracts and diamonds.

As the author of 2936, naturally I support this solution. It reduces the burden on validators for the CREATE2 reincarnation upgrade pattern and makes reincarnation a viable alternative to SLOAD+DELEGATECALL proxies, the current dominant paradigm.

---

**mudgen** (2020-09-13):

[@wjmelements](/u/wjmelements) I understand that gas prices may drop because of this EIP, therefore easing the burden of gas costs for calling external functions on proxy contracts and diamonds.  But what concerns me specifically is the increased gas gap between calling external functions on regular contracts and calling them on proxies/diamonds.  The gas price may be less but the gas gap is still wider than before. It will still cost more gas units to call external functions on proxy contracts and diamonds.

[@wjmelements](/u/wjmelements) What do you mean by larger gas limits?

---

**wjmelements** (2020-09-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> It will still cost more gas units to call external functions on proxy contracts and diamonds.

As it should, because those patterns require more work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> @wjmelements What do you mean by larger gas limits?

Increasing gas costs of these operations would allow higher gas limits for the same uncle rate and state growth rate. A better way to view this change is that every other operation uses less gas, relatively.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/i/51bf81/48.png) ilanDoron:

> Is this behaviour essential, could it be modified?
> storing an array in memory in a sequential manner and then lowering gas price for sequential access could be very helpful.

If you want sequential storage you have to use contract code. You can use EXTCODECOPY to read the data into memory.

---

**ilanDoron** (2020-09-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> If you want sequential storage you have to use contract code. You can use EXTCODECOPY to read the data into memory.

Thanks. a good point.

but this is only for constant data. right?


*(36 more replies not shown)*
