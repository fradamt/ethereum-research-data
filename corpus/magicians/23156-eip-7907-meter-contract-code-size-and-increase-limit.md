---
source: magicians
topic_id: 23156
title: "EIP-7907: Meter Contract Code Size And Increase Limit"
author: charles-cooper
date: "2025-03-14"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7907-meter-contract-code-size-and-increase-limit/23156
views: 1050
likes: 39
posts_count: 45
---

# EIP-7907: Meter Contract Code Size And Increase Limit

discussions-to for [EIP-7907: Meter Contract Code Size And Increase Limit](https://eips.ethereum.org/EIPS/eip-7907)

(original PR: [Add EIP: Meter Contract Code Size And Increase Limit by charles-cooper · Pull Request #9483 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9483))

## Replies

**charles-cooper** (2025-03-15):

I performed jumpdest analysis benchmarks for eip 7903, which are relevant here.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png)
    [EIP-7903: Remove Initcode Size Limit](https://ethereum-magicians.org/t/eip-7903-remove-initcode-size-limit/23066/3) [EIPs core](/c/eips/eips-core/35)



> benchmarks (tl;dr: jumpdest analysis shows a strong linear correlation to initcodesize, at sizes ranging from 128 bytes to 15MB):

---

**radek** (2025-04-25):

Twitter is cheering up.

But this incentivises tha lazy inclusion of libraries and goes against the principle of maximum reuse of what is already deployed on chain.

Ofc, the question is whether there is even **a common agreement on such a principle of deployed code reusability**.

---

**benaadams** (2025-04-27):

> If the account is warm, no change to the gas schedule occurs.

The account being warm doesn’t mean the code is loaded:

- Access Lists: account will be warm if added to access list but no code is pre-loaded just the account (including codehash).
- EXTCODEHASH also warms the account but doesn’t load the code

Other actions loading the code are not included in the pricing:

- EXTCODESIZE loads the code
- Basic tx calling a contract also loads code, but isn’t in the pricing

Do you need to add all these to pricing, or add as second “warm” list that records if code is loaded?

---

**charles-cooper** (2025-04-27):

Hmm, interesting. What do you think is the cleanest way in the spec to specify that the cost is only incurred on the first load of the code?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png) benaadams:

> EXTCODESIZE loads the code

It doesn’t have to btw, the EIP specifies that clients should keep an out-of-band index for codesize –

> Clients should add an efficient way to determine the code size without loading the entire code, e.g. storing it in a separate table keyed by code hash. This way, they can charge for the access cost before physically loading the code. Otherwise, a client may load a contract, even when there is not enough gas left to pay for the code load.

---

**benaadams** (2025-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> e.g. storing it in a separate table keyed by code hash. This way, they can charge for the access cost before physically loading the code.

So should loading from this new table incur the cost of an SLOAD?

Making `EXTCODESIZE` cost `warm account` (get hasd) + `2100`gas (get data) rather than `20` gas?

---

**benaadams** (2025-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> clients should keep an out-of-band index for codesize

How does this work for statelessness and zk; since it is an unwitnessed data with no root, how is it proved to be correct?

---

**charles-cooper** (2025-04-27):

It’s witnessed by codehash, but I’m not sure where and when in the protocol the proof would be provided.

Actually I’m checking go-ethereum and calling `EXTCODESIZE` triggers addition of the full code to the witness. Suggesting that yes, EXTCODESIZE should also trigger the per-byte cost in the EIP.

[![Screenshot from 2025-04-27 22-16-23](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a4b93cd5d61897de6d68b70fc8d9e27693731005_2_690x250.png)Screenshot from 2025-04-27 22-16-23977×355 46 KB](https://ethereum-magicians.org/uploads/default/a4b93cd5d61897de6d68b70fc8d9e27693731005)

---

**qizhou** (2025-04-29):

Nice catch!  I think we should introduce an additional warm state for the code so that

- account warm but code cold.  This applies to optional access lists in EIP-2930.  Calling such a contract will enjoy WARM_STORAGE_READ_COST = 100 vs 2600 for the first 24KB of the code.  If the code size > 24KB, then we charge 2 gas per byte as in EIP-7907 and put the account as code warm;
- account warm and code warm, where calling such a contract will take WARM_STORAGE_READ_COST = 100 gas.

---

**charles-cooper** (2025-04-29):

Yes, this makes sense to me. It looks inelegant at first to have two different warm states, but it makes sense bc code is stored in an auxiliary table separate from accounts.

---

**benaadams** (2025-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> It looks inelegant at first to have two different warm states, but it makes sense bc code is stored in an auxiliary table separate from accounts.

Yeah is a bit ugly; but `EXTCODESIZE` etc has been a pain point in many scenarios; so it is a pragmatic fix

---

**charles-cooper** (2025-04-29):

I spoke a bit about the `EXTCODESIZE` issue offline with [@matt](/u/matt), and here are my thoughts –

As a *user* of the EVM, it’s a bit of a gotcha for EXTCODESIZE to be priced differently from other account querying opcodes, e.g. EXTCODEHASH. It is also uniquely determined by codehash (up to hash collision resistance), so if there are any tricks that the implementation can pull to make this happen, I think it would be good for users.

However, I recognize this might not be copacetic with how implementations actually work. For example, for stateless clients, they probably need the full code in order to prove codesize, even though it is “witnessed” (uniquely determined) by codehash.

I think there are basically three options:

1. Apply the code load cost from this EIP to EXTCODESIZE as well
2. Make it the same as EXTCODEHASH
3. Add @benaadams’ proposed 2100 gas as a separate cost for EXTCODESIZE

I prefer 2, 1 and then 3, in that order. I don’t think an additional cost needs to be added for the codesize query on top of account loading cost, since it can be prefetched in parallel with the other account data (or simply added into the db entry for an account, just without affecting the state root).

All that being said, this issue probably doesn’t matter too much in the big picture, since EXTCODESIZE *usually* happens near a CALL as part of the contract existence check. So the code is typically going to be loaded, anyways!

Meanwhile, option 1 seems most friendly for stateless clients. I think it would also be fine to ship option 1 instead of option 2, and figure out how to bring the gas cost down for EXTCODESIZE down later (since intuitively it looks like it should be cheap).

Paging [@matt](/u/matt), [@qizhou](/u/qizhou), [@jochem-brouwer](/u/jochem-brouwer) as well who have also been very helpful with feedback to see what their thoughts are here. I’d also like everybody to be on the same page so there aren’t surprise disagreements in the spec later.

---

**qizhou** (2025-04-29):

My preference order is also 2,1,3.  My argument is that the gas pricing for stateful, statelessness, and zk may be completely different - not only for EXTCODESIZE but almost all other OP codes and precompiles.  For example, statelessness needs full code to prove codesize, while zk can prove the relationship between codehash => codesize with a much smaller prove size.  Given our priority is for the current stateful EVM upgrade in Fukasa, I would choose 2 considering the negligible cost of the parallel lookup of codehash => codesize in stateful DB as Charles explained.

---

**benaadams** (2025-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> All that being said, this issue probably doesn’t matter too much in the big picture, since EXTCODESIZE usually happens near a CALL as part of the contract existence check. So the code is typically going to be loaded, anyways!

One of the Shanghai DoS attacks was `EXTCODESIZE`,`POP`; so while this is a fair assumption for well meaning code; it isn’t for intentional attacks

---

**charles-cooper** (2025-04-29):

Ah, I meant for the user – as in the typical user won’t experience a large change in pricing depending on the two schemes.

---

**qizhou** (2025-04-30):

An early draft implementing EIP-7907 in Geth can be found here [add EIP-7903 by qizhou · Pull Request #1 · qizhou/go-ethereum · GitHub](https://github.com/qizhou/go-ethereum/pull/1/files)

---

**gurukamath** (2025-05-09):

The EIP does not reference 7702 delegations. Might be a good idea to explicitly clarify the access costs for delegated accounts.

---

**gurukamath** (2025-05-19):

> Change the gas schedule for opcodes which load code. Specifically, the CALL, STATICCALL, DELEGATECALL, CALLCODE and EXTCODECOPY opcodes are modified so that ceil32(excess_contract_size) * 2 // 32 gas is added to the cold access cost, where excess_contract_size = max(0, contract_size - 0x6000). (Cf. initcode metering: EELS). If the account is warm, no change to the gas schedule occurs.

It is a bit unclear if the value of 2 used in the formula `ceil32(excess_contract_size) * 2 // 32` is the same as the `INITCODE_WORD_COST` that is defined in EIP-3860 or if this EIP wishes to define a new constant with the same value. Explicitly clarifying this will help avoid ambiguity in case of future changes/updates.

---

**charles-cooper** (2025-05-19):

Good point. It should be the same as `INITCODE_WORD_COST`. I’ll update the EIP

---

**charles-cooper** (2025-05-19):

[@gurukamath](/u/gurukamath) please check: [clarify that 2 == GAS_INIT_CODE_WORD_COST by charles-cooper · Pull Request #9793 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9793)

---

**jochem-brouwer** (2025-05-20):

I believe this EIP needs more updates, I think we discussed this, but it needs to track which code is loaded and which is not. One could “warm” an address without incurring the extra costs by calling `BALANCE` on them for example, thus not paying for the `ceil32(excess_contract_size) * 2 // 32` (but with the overhead of the `BALANCE` opcode in gas which I think is 100. This is rather small and it would already be net positive if the to-be-called contract exceeds the original limit of `100 * 2 * 32 = 640` bytes)

Also note that we can warm accounts by adding them to the EIP-2930 access lists. This will thus not incur the extra `ceil32(excess_contract_size) * 2 // 32` costs. Since adding the cold items touched to the access list is already a net benefit, this bonus is now thus larger (for large contracts).

I have no direct solution for this but calling the largest contract would cost `(256 * 1024) * 2 // 32 = 16384` gas which is rather expensive (although the JUMPDEST analysis should be accounted for ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12) )


*(24 more replies not shown)*
