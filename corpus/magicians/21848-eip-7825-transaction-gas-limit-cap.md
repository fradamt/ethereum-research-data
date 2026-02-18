---
source: magicians
topic_id: 21848
title: "EIP-7825: Transaction Gas Limit Cap"
author: Giulio2002
date: "2024-11-25"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7825-transaction-gas-limit-cap/21848
views: 855
likes: 17
posts_count: 24
---

# EIP-7825: Transaction Gas Limit Cap

Discussion topic for EIP-7825

#### Update Log

> Creation

#### External Reviews

#### Outstanding Issues

None as of 2024-11-25.

## Replies

**benaadams** (2025-04-10):

Ideally the value would be lower

---

**jochem-brouwer** (2025-04-24):

This EIP is great and I fully support it.

However, I think the EIP itself could use some clarifcations.

> Transactions specifying gas limits higher than 30 million gas will be rejected with an appropriate error code (e.g., MAX_GAS_LIMIT_EXCEEDED)

This is likely meant in the context of JSON-RPC, where the client would respond with this error code. However this could be confused with other places, like the EVM or block validation.

[@benaadams](/u/benaadams) wants the value to be lower. Also for txpool performance to quickly invalidate transactions, what about a limit of `2^(3*8) - 1`? So the gas limit should be `<= 2^(3*8)-1`. This means that the value (`16_777_215`) fits into a `bytes3`. So we can quickly check when decoding the RLP to figure out if the transaction is valid or not regarding this rule: if it is 4 or more bytes it is invalid.

This will need analysis on-chain what transactions use more gas limit than this to ensure we don’t break anything.

---

**benaadams** (2025-04-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> This is likely meant in the context of JSON-RPC, where the client would respond with this error code. However this could be confused with other places, like the EVM or block validation.

Would also need an error for block validation? As a block builder could include an invalid size transaction regardless of what the tx pool accepts

---

**benaadams** (2025-04-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> This means that the value (16_777_215) fits into a bytes3.

Am ok with this limit ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Though some analysis of larger txs and why they are larger might be needed

---

**jochem-brouwer** (2025-04-24):

Yes the block should definitely be rejected! This was meant in the scope of the EIP, in that specific section it should be made clear that it is about JSON-RPC. Then later on in the EIP it should be made explicit that any block with such transaction is invalid. This thus also implies (but it’s fine to note this in the EIP) that these should be directly thrown out of mempool (we don’t want invalid txs in our mempool)

---

**bbjubjub** (2025-04-24):

One of many potential futures for Ethereum is one where apps and users do not produce traditional L1 transactions but instead ERC-4337 ops. If so, we might end up in a situation that looks like [ULTRA-TX](https://ethresear.ch/t/ultra-tx-programmable-blocks-one-transaction-is-all-you-need-for-a-unified-and-extendable-ethereum/21673), where it is most efficient for the block builder to make one big transaction that takes up 50 to 90% of the block with all of the meta-transactions in it, and fill the rest of the block with traditional transactions. Suppose the gas limit is 300M+: if the per transaction limit is 30M, we are forcing the builder to split up their big transaction into up to ten pieces, forcing them to perform the knapsack algorithm and pay intrinsic gas multiple times. It might still be beneficial to put this limit and remove it later if needed, but this should be considered. We might even hamper the emergence of ULTRA-TX by including this EIP.

---

**wminshew** (2025-04-24):

Shipping a transaction cap feels premature to me atm, but if we were to ship it I think it should be updatable without a full hard fork for future flexibility (same as the gas block limit is, iiuc)

---

**chfast** (2025-04-26):

Another example of expensive transactions are big contract deployments because they pay a lot for the stored code (200 gas per byte). So this limit also puts limit on the code size (~70k by my very quick estimation).

In other words, this EIPs goes against the [EIP-7903: Remove Initcode Size Limit](https://eips.ethereum.org/EIPS/eip-7903), discussed in [EIP-7903: Remove Initcode Size Limit](https://ethereum-magicians.org/t/eip-7903-remove-initcode-size-limit/23066).

---

**duncancmt** (2025-07-24):

I posted this over at [the EIP-7987 discussion](https://ethereum-magicians.org/t/eip-7987-transaction-gas-limit-cap-at-2-24/24746/11), but it’s really important not to make breaking/backwards-incompatible changes. Why set this limit lower than the “conventional” block gas limit of 30M? We already have examples of dApps that this lower limit will break. Don’t squander the goodwill that Ethereum’s stability has engendered. The EVM is such a vibrant developer ecosystem precisely because of Ethereum’s stability. I see this entirely too often in EIPs that affect the execution layer. Linus wouldn’t tolerate this and neither should we.

---

**benaadams** (2025-07-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbjubjub/48/13986_2.png) bbjubjub:

> Suppose the gas limit is 300M+: if the per transaction limit is 30M, we are forcing the builder to split up their big transaction into up to ten pieces, forcing them to perform the knapsack algorithm and pay intrinsic gas multiple times.

Splitting the huge tx into multiple pieces means the tx can be parallelized which means the validators can support the higher gaslimit throughput

Intrinsic gas is 21k; if they had to submit 10x for a 300M fill; that’s 0.07% of their tx gas. Isn’t particularlly a feature?

---

**bbjubjub** (2025-07-28):

I agree that intrinsic gas is negligible in this case. There could however also be issues with transient storage, blob aggregation, and top-of-block guarantees when knapsacking the tx, at least based on my reading of ULTRA-TX. But it’s hard to know since we haven’t seen any implementations. I would also like to invite [@Brechtpd](/u/brechtpd) to opine on this, given what was said in Cannes during the Gwyneth talk.

---

**Brechtpd** (2025-07-31):

Yes it is potentially problematic for ULTRA TX. I have proposed [EIP-7814](https://github.com/ethereum/EIPs/pull/9028) that exposes the transaction trie to the EVM so that the latest state can be calculated at any place in the block efficiently, so top of block is not required and the ULTRA TX can be split over multiple transactions if needed.

---

**3commascapital** (2025-09-24):

Hi all, I am a bit late to this discussion, but I do not think that this is the right way to go about doing this. This pathway prevents the utility of certain decentralized projects that are projected to hit this limit in the next few years. By applying a single transaction gas spend limit, optimizations such as accessing warmed SLOADs become harder to achieve when performing group actions.

Imagine a contract that uses 10m in gas, mostly during SLOADs. After that 10m spend, only ~6m is left for warm accessing, which is much less than the current 20m. I could be for this EIP if the warm SLOAD costs were also reduced substantially, like from 100->20 or something similar or if using EIP2930 were re-jigged to not price the user out up front and pack in risk of not using the loads (main reason why people do not use it imo)

Do we not want people to burn the native token?

Addendum:

If EIP2929 applies across a block, I could be more for this, but that still leaves a lot of risk with the executor of multiple batched transactions.

---

**clydebrown231-web** (2025-09-25):

[@bennypoloven-netizen](/u/bennypoloven-netizen) check this bro

---

**MathisGD** (2025-10-14):

Hello all,

I don’t understand the rationale behind this change. From the EIP itself (which is very short):

> DoS Attacks: A single transaction consuming most or all of the block gas can result in uneven load distribution and impact network stability.

Why couldn’t an attacker just DoS with multiple transactions? Just for the 21,000 initial gas of each transactions?

> State Bloat Risks: High-gas transactions often result in larger state changes, increasing the burden on nodes and exacerbating the Ethereum state growth problem.

Why? Again for the 21,000 gas?

> Validation Overhead: High-gas transactions can lead to longer block verification times, negatively impacting user experience and network decentralization.

Why 1 transaction of 10M gas is harder to verify than 10 transactions of 1M gas (actually my intuition is that it’s the opposite)?

**edit:** (from a chat with [@Giulio2002](/u/giulio2002)) different transactions are (more likely) executable in parallel. Which explains 3.

Also, as stated earlier in the thread, putting a value lower than the current block gas limit is technically a breaking change. How can we know that there aren’t some critical actions in some smart-contracts that take more than 16M gas?

Thanks for the answers.

**edit:** [this thread](https://ethereum-magicians.org/t/eip-7987-transaction-gas-limit-cap-at-2-24/24746/21) contains a lot of info about the rationale behind this EIP and the breaking change.

---

**3commascapital** (2025-10-14):

Hey [@MathisGD](/u/mathisgd) , I would not claim to know what the original poster believes, but how I would answer your question is as follows:

> Why couldn’t an attacker just DoS with multiple transactions? Just for the 21,000 initial gas of each transactions?

I don’t know about all clients, but for erigon there is a spam limit where the node will start dropping transactions intentionally if you get above 16 (check me on that number) transactions in the mempool. I am sure there are other spam reduction measurements in other clients.

> Why? Again for the 21,000 gas?

Usually this is achieved via sstore’s since it is an easy gas operation to create. Just increment a number and write it to a mapping.

> How can we know that there aren’t some critical actions in some smart-contracts that take more than 16M gas?

I agree. There are / will be more often. Check out: [EIP-7825: Transaction Gas Limit Cap - #17 by 3commascapital](https://ethereum-magicians.org/t/eip-7825-transaction-gas-limit-cap/21848/17)

---

**CodeSandwich** (2025-12-01):

This RFC should change the semantics of the GASLIMIT EVM opcode too. It should return the gas limit of a single transaction and not of a whole block.

In the context of a smart contract running inside a transaction GASLIMIT is only useful for assessing how much work can be done in one go, in a single transaction. If work must be done over 2 transactions, it doesn’t matter if the other transaction is executed in the same block or in the block that will be mined 12 seconds later. For a smart contract the gas capacity of a block is a meaningless number.

I’m late to the party, but IMO this is a veto-worthy defect of this RFC. If it’s applied without altering GASLIMIT, it will likely break most contracts using this opcode.

---

**bertkellerman** (2025-12-04):

I wish I knew this was coming in Fusaka as it’s a horrible idea.

Why are we interfering in the gas market? We have a market. Let it work.

If someone wants to use(and pay for) the entire block, why are we not allowing that?  In fact, we aren’t even allowing them to use 28% of the block space for just single brief tiny point in time.

If a large tx is willing to pay the market price for block space and builders agree with that price, who are we to say “no” to that?

Further, if a large tx is willing to pay the market price to be included, is it even “spam”?

As stated before, a true spammer can just create multiple txs.

Is there even a DoS threat of large txs? Is it faster to process 1 60M tx or 60 1M txs?

“By capping individual transactions, the validation of blocks becomes more predictable and uniform.”

This is vague, also.

Is “the predictability and uniformity of blocks” really worth playing god of the gas market and most certainly limiting the use of Ethereum for some valid use cases.

Remember,

“640k ought to be enough for anybody” -Bill Gates

---

**bertkellerman** (2025-12-04):

My apologies for being gruff, but in addition to above concerns, this change directly impacts what I’m building on Ethereum

I’m currently building an immutable protocol on Ethereum that, during a pretty rare state, can theoretically be griefed.  The limiting factor of the effective mitigation(atomic arb) is gas usage of a single tx.

In a perfect world, this griefing vector wouldn’t exist and we would redesign, but I’ve felt ok about it given the low probability of the state happening, the economic incentive. I’ve also been ecstatically observing the gas limit rising in the wild.

However, this new tx limit possibly changes the economics of the attack and we will need to reassess. I’m glad we haven’t deployed already.

Which brings the point. Some protocols might have made assumptions about the L1 they thought were reasonable and this change could break them in some way the EIP designers didn’t imagine. Up until now, I thought a tx using all available gas on the market was one of those safe assumptions.

---

**abcoathup** (2025-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bertkellerman/48/10781_2.png) bertkellerman:

> If a large tx is willing to pay the market price for block space and builders agree with that price, who are we to say “no” to that?



      [x.com](https://x.com/no89thkey/status/1996266248225845698)



    ![image](https://pbs.twimg.com/profile_images/1773613294584250368/Acy-TGFH_200x200.jpg)

####

[@no89thkey](https://x.com/no89thkey/status/1996266248225845698)

  EIP-7825 is one of the most underrated upgrades for the future of ZK proving and 100X Ethereum scaling.

By capping each Ethereum transaction at ~16.78M gas, it removes the risk of a single mega-transaction consuming an entire block. That sounds small, but the implications for

  https://x.com/no89thkey/status/1996266248225845698












      [x.com](https://x.com/VitalikButerin/status/1996599032072790322)



    ![image](https://pbs.twimg.com/profile_images/1895872023944937472/Uoyc5-p8_200x200.jpg)

####

[@VitalikButerin](https://x.com/VitalikButerin/status/1996599032072790322)

  @trent_vanepps @CupOJoseph @BertKellerman If EIP-7825 did not exist, then in the worst case (one tx filling the whole block) BALs would not enable parallel execution, and so we would not be able to raise the gas limit as a result of BALs.

So it's a necessary prerequisite of scaling.

  https://x.com/VitalikButerin/status/1996599032072790322


*(3 more replies not shown)*
