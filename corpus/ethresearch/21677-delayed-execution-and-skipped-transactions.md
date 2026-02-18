---
source: ethresearch
topic_id: 21677
title: Delayed Execution And Skipped Transactions
author: Nero_eth
date: "2025-02-05"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/delayed-execution-and-skipped-transactions/21677
views: 1854
likes: 23
posts_count: 27
---

# Delayed Execution And Skipped Transactions

# Delayed Execution And Skipped Transactions

***Many thanks to [Francesco](https://x.com/fradamt) for feedback, review an collaboration on this!***

Ethereum requires **every block to be fully executed before it’s considered valid**. Each block header commits to a set of execution outputs—like the new state root, receipts, and logs—that result from processing every transaction within that block. This tight coupling means that **validators must run every transaction as soon as they see a new block, making execution an inherent part of the critical path.**

A proposed solution, known as ***Delayed Execution*** (spec’ed by [Francesco](https://x.com/fradamt), [here](https://github.com/fradamt/execution-specs/tree/delayed-execution-simple)), offers an elegant approach by **decoupling block validation from immediate transaction execution**. In this post, I’ll go through how this mechanism works and what it could mean for scaling.

> Also, check out Francesco’s post on delayed execution that explores another potential approach besides the one described in this post.

## Blockchain 1x1

In Ethereum, each block links to its predecessor by including a cryptographic commitment not only to the previous block’s header **but also to the state resulting from all transactions in that block**.

**Here’s what happens:**

- Execution-Dependent Headers: The block header contains fields such as state_root, receipt_root, and logs bloom. These fields are generated only after the transactions have been executed.
- Full Execution: Every validator, upon receiving a new block, must execute all transactions to verify that the header’s commitments are correct. This ensures the block is consistent with the current state but forces nodes to do potentially heavy computation immediately.

[![state transition now](https://ethresear.ch/uploads/default/optimized/3X/5/a/5aacb210a05b8f495da99a9cb4e949d8fc1fa1cf_2_690x239.png)state transition now1241×431 25.1 KB](https://ethresear.ch/uploads/default/5aacb210a05b8f495da99a9cb4e949d8fc1fa1cf)

## The Concept of Delayed Execution

Delayed Execution challenges this paradigm by splitting the block processing into two distinct stages:

1. Static Validation (Pre-Execution): Validators perform minimal checks using only the previous state. Instead of committing to a freshly computed state_root and related fields, the block header defers these execution outputs by referencing values from the parent block.
2. Post-Attestation Execution: The actual execution of transactions is delayed until after the block is initially validated and attested to by the network.

This decoupling means that validators can quickly agree on the block’s validity without having to execute every transaction upfront. In essence, the block is “chained” to its predecessor using minimal data that does not require full execution.

[![state transition with delayed execution](https://ethresear.ch/uploads/default/optimized/3X/5/e/5ea0ee6dacc5c950f7d2f1e4ffa17dc02ffc3504_2_690x211.png)state transition with delayed execution1142×350 24.6 KB](https://ethresear.ch/uploads/default/5ea0ee6dacc5c950f7d2f1e4ffa17dc02ffc3504)

Instead of fully executing the block before attesting, **we can already attest to the block as soon as minimal static validation is done**. This relieves stress from the critical path. The following is a simplified illustration of the efficiency gains. It compares the current situation (*top*) with delayed execution (*bottom*):

[![overtime](https://ethresear.ch/uploads/default/optimized/3X/4/6/467c02fcd8e3727db953d3f575e1e40677b8c498_2_690x407.png)overtime1250×739 162 KB](https://ethresear.ch/uploads/default/467c02fcd8e3727db953d3f575e1e40677b8c498)

The following graph has a (incomplete) list of things we do during a state transition. Only the initial, **static validation phase** (**which relies solely on the previous state**) needs to be executed immediately, while the more complex, **state-changing operations can be safely deferred until after attestation**.

[![state transition function](https://ethresear.ch/uploads/default/optimized/3X/a/9/a98b11aee17de5afceb99d0c78b2c941d8623242_2_608x500.png)state transition function840×690 105 KB](https://ethresear.ch/uploads/default/a98b11aee17de5afceb99d0c78b2c941d8623242)

In theory, this change could boost efficiency by as much as **8x**, assuming blocks arrive at second 3 of the slot, the attestation deadline stays at second 4, and the worst-case execution time is 1 second (based on the 99.9999th percentile). Special thanks to [Marek](https://x.com/M25Marek), [Ben](https://x.com/ben_a_adams), and [Łukasz](https://x.com/URozmej) for providing this figure.

That said, take this estimate with a grain of salt—you might more realistically expect around a **5x** improvement.

## The Role of Skipped Transactions

A novel concept in the delayed execution mechanism is the allowance for ***skipped transactions***. Under the current protocol, a single invalid or underfunded transaction can invalidate an entire block. Delayed execution introduces a more resilient approach:

- Inclusion Without Execution: Transactions are still included in the block’s transaction list but might be marked as “skipped” during execution if they fail certain conditions (e.g., insufficient funds, underpricing, incorrect nonce, or other execution-dependent checks).
- Upfront Fee Payment by Coinbase: To protect the network against the cost of including these transactions, the block proposer’s account (known as the COINBASE) pays an upfront “inclusion cost.” This cost covers basic expenses like the base transaction cost and calldata fees.
- Network Compensation: Even if a transaction is skipped, the network is compensated because the inclusion cost has been pre-paid by the COINBASE. This mechanism eliminates the risk of having transactions that consume resources without paying.

[![delayed execution flow](https://ethresear.ch/uploads/default/original/3X/9/e/9e2b6c9f9fa49053698138194c94656f3e755c4a.png)delayed execution flow1181×331 20.9 KB](https://ethresear.ch/uploads/default/9e2b6c9f9fa49053698138194c94656f3e755c4a)

By allowing invalid transactions to be skipped without invalidating the whole block, the proposal shifts the burden of heavy execution away from the immediate validation process. Similar to [EIP-7732](https://eips.ethereum.org/EIPS/eip-7732) (ePBS), we relieve the critical path from the heavy load of execution and state root validation.

## The Role of COINBASE and Direct Sponsorship (optional)

Delayed execution could create new opportunities for direct sponsorship. Since the coinbase already covers the inclusion cost upfront, it might be reasonable to extend this responsibility to the base fee as well.

**Here’s how it works:**

- COINBASE’s Signature Commitment: The block header comes with a signature from the COINBASE address. This signature is a commitment that the COINBASE is responsible for paying all inclusion costs upfront. In effect, the COINBASE sponsors the execution of transactions that might otherwise be underfunded (=not able to pay for the basefee).
- Flexible Fee Models: With the COINBASE on the hook for initial fees, the protocol can allow transactions that don’t strictly meet the minimum fee requirements. This opens the door to new possibilities such as gasless or sponsored transactions, where the sender might not have enough ETH to pay upfront but is later reimbursed—or the COINBASE recoups the cost—once execution is successful.

Delayed execution and block-level base fee mechanisms are separate topics that should be addressed independently. However, the COINBASE’s commitment to covering the inclusion cost could be extended to also committing to sponsoring the base fee.

For additional details on why block-level markets have the potential to contribute to more efficient resource allocation, check out Barnabé’s post on [Block-level Markets](https://ethresear.ch/t/block-level-fee-markets-four-easy-pieces/21448).

## Under The Hood

Under delayed execution, the way blocks are chained together undergoes a small transformation:

- Deferred Execution Outputs: Header fields such as the state_root, receipt_root, and logs bloom are deferred. Instead of reflecting the immediate execution of the block, these fields hold values from the parent block. This means that the block’s validity can be confirmed without performing all of its computational work. Invalid transactions can be included in blocks.
- Inclusion Cost Calculation: For every transaction, an inclusion cost is computed that typically includes a base cost (e.g., 21,000 gas), calldata fees, and any blob gas fees. This cost is deducted from the COINBASE’s balance before the transactions are executed. If the transaction is skipped, the COINBASE loses the inclusion cost fronted for the transaction. If the transaction executes successfully, the inclusion cost fronted by the COINBASE is refunded by the sender of the transaction.
- Two-Phase Validation: The validation process is split into an initial static check—ensuring that the block is structurally sound and that the COINBASE can cover inclusion costs—and a later execution phase, where transactions are processed or skipped as appropriate.

This design relieves the critical path of execution, allowing blocks to be validated and attested more quickly. It ultimately results in a more scalable and flexible protocol, as the heavy lifting of transaction execution can be handled asynchronously relative to block attestation.

## Advantages and Trade-Offs

**Advantages:**

- Increased Throughput: By taking transaction execution out of the immediate validation path, blocks can be attested to more rapidly.
- Enhanced Flexibility: The model simplifies introducing new fee mechanisms, such as sponsored and gasless transactions, which can make Ethereum more accessible to users.

**Trade-Offs:**

- Liquidity Requirements for Proposer/Builder: The COINBASE address must be sufficiently funded to cover the maximum possible inclusion costs for a block, which may introduce liquidity constraints, especially during periods of high base fee conditions. The maximum inclusion fee equals gas_limit * base_fee, so, with a base_fee of 100 GWEI, we’re at 3 ETH.
- Protocol Complexity: Introducing delayed execution involves substantial changes to Ethereum’s execution layer. However, unlike other delayed execution proposals, this approach avoids modifying the fork-choice function, which keeps the complexity lower. For a closer look at what these changes entail—especially if you’re interested in adding base fee sponsoring—check out the flow chart in the appendix and the EELS specs here.

## Appendix

For flowchart enthusiasts, here is how the described mechanism is currently spec’ed; **this includes the block-basefee feature and skipped transactions**, going through the EELS implementation [here](https://github.com/ethereum/execution-specs/compare/devnets/prague/6...nerolation:execution-specs:delayed-execution-prague):

[![flow chart of complete flow with skipped transactions adn sponsoring](https://ethresear.ch/uploads/default/optimized/3X/c/b/cb10f259905b16b2241f0f375107803eb08814be_2_122x500.jpeg)flow chart of complete flow with skipped transactions adn sponsoring891×3640 285 KB](https://ethresear.ch/uploads/default/cb10f259905b16b2241f0f375107803eb08814be)

^find the uncompressed version of this diagram [here](https://github.com/nerolation/delayed-execution-diagram/blob/5eb1d946e065e796b77f2020c5b04c65010f7257/delayed_exec.pdf).

## Replies

**thegaram33** (2025-02-05):

Excellent writeup!

While it’s not shown on the “State Transition” figure, I assume the *Static Validation* steps would also include:

- Check execution results of parent block (header.pre_state_root, etc.)
- Block and transaction decoding (we at least need to make sure that the block is well-formed).

---

**g11in** (2025-02-05):

we will also need to include execution requests in the deffer-ed outputs

essentially CL can’t use/attest to any outputs from the current payload txs since the actual EL execution might not agree with it. This implies now the requests CL will include/apply in its block will be of parent’s

---

**terence** (2025-02-05):

Expected withdrawals from CL to EL as well

---

**GregTheGreek** (2025-02-05):

I love this, something I’ve been thinking about with Mark lately is whether it even matters to have any failed or “skipped” txs in the blocks at all.

An initial thought was to chuck the failed ones into a blob or a special tx that sits at the 0th index of every block. Rational is its useless state to store, and if we can validate a tx (eg Mev bots racing each other, or nft drops and hat get spammed and fail) we have a chance to decrease the overall load on the network and free up space that’s literally useless.

---

**thogard785** (2025-02-05):

Why skip - is it purely for the disincentivize? If the Coinbase is already paying the cost, why not execute it and let the block builder act as a de facto paymaster?

---

**Nero_eth** (2025-02-06):

This is interesting, and yeah, I agree, the right place for invalid transaction would actually be in a blob, and then being pruned after some days.

I have to think more about this approach and what it would require in changes as we’re currently basically using simple “if not skipped then execute and refund, else skip” logic while putting txs into the trie beforehand. So, we’d need to keep track of skipped txs and then move them over into a blob. 128kib would probably be a little wasteful since we can expect skipped transactions to be a very rare event since local/mevboost builders have a clear incentive to not have skipped txs bc they pay for it. Also, during syncing you’d need to know that those transactions (that still contribute to the previous_state_root of the next block) are now in a blob instead of the block. I still have to get my head around this.

---

**Nero_eth** (2025-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> Why skip - is it purely for the disincentivize? If the Coinbase is already paying the cost, why not execute it and let the block builder act as a de facto paymaster?

For mevboost blocks, the coinbase usually sets its own address into the “coinbase”. So, when a transaction needs to skip execution, it means that the transaction was invalid (underfunded, invalid nonce, etc) and would normally have invalidated the whole block. With the described delayed execution mechanism, we’d pre-charge the coinbase of the block (builder) at the very beginning, taking an “inclusion fee” (21k base cost + calldata + blobs), and refund it in case the tx is not skipped. So, there’s a clear incentive for the builder to not order your transactions in a way that screws you over by suddenly having your transactions “skip”. The builder can still do so but pays for it. So, skipped transactions should be rare bugs and failures at the one that has control over the content of the block.

---

**Nero_eth** (2025-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> While it’s not shown on the “State Transition” figure, I assume the Static Validation steps would also include:
>
>
> Check execution results of parent block (header.pre_state_root, etc.)
> Block and transaction decoding (we at least need to make sure that the block is well-formed).

Yeah, this is correct in case of delayed execution. The transaction (and withdrawal) encoding happens as part of the static checks too, yes. In the diagram I wanted to show the current state transition function, not the one with delayed execution, just to show that static validation is minimal compared to the rest. I have the post-execution header checks as Verification at the end.

This is all done in `validate_header()` in the specs:



      [github.com](https://github.com/fradamt/execution-specs/blob/ae2c77989cb83e5d5e5eb1f51d9da840a337d5b0/src/ethereum/prague/fork.py#L497)





####



```py


1. Bytes, Optional[Union[Bytes, LegacyTransaction]]
2. ] = Trie(secured=False, default=None)
3. withdrawals_trie: Trie[Bytes, Optional[Union[Bytes, Withdrawal]]] = Trie(
4. secured=False, default=None
5. )
6.
7. parent_header = chain.blocks[-1].header
8. validate_header(block.header, parent_header)
9.
10. # validate deferred execution outputs from the parent
11. if block.header.parent_gas_used != chain.last_block_gas_used:
12. raise InvalidBlock
13. if block.header.parent_receipt_root != chain.last_receipt_root:
14. raise InvalidBlock
15. if block.header.parent_bloom != chain.last_block_logs_bloom:
16. raise InvalidBlock
17. if block.header.parent_requests_hash != chain.last_requests_hash:
18. raise InvalidBlock
19. if block.header.pre_state_root != state_root(chain.state):
20. raise InvalidBlock
21.


```

---

**LukaszRozmej** (2025-02-06):

I have mixed feelings, but probably more on the positive side.

I would like to propose to call it an async execution rather than delayed execution. As we are not really delaying it to any next slots, but running it async to attestations and all CL logic, without waiting for result.

As for the proposal: on one hand it probably gives us a lot of wiggle room with execution. On the other hand execution is probably not the main bottleneck, bandwith and state growth are.

I somewhat like skipped transactions, this brings parity with rollups, especially based rollups that can’t control their sequencer thus have to have a similar concept.

My main concerns would be around if this won’t close up some other paths we would like to explore in the future as the design is somewhat a one way ticket and will prevent us from having this execution feedback loop in CL. Not sure if there are already existing EIPs this would make void?

---

**linoscope** (2025-02-06):

Good read and interesting proposal!

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Liquidity Requirements for Proposer/Builder: The COINBASE address must be sufficiently funded to cover the maximum possible inclusion costs for a block, which may introduce liquidity constraints, especially during periods of high base fee conditions. The maximum inclusion fee equals gas_limit * base_fee, so, with a base_fee of 100 GWEI, we’re at 3 ETH.

I am wondering about the impact on self-building solo-stakers here, who may not have such liquidity. Note that even for validators using MEV-Boost, self-building is important for supporting the fallback case for MEV-Boost failure. Is the assumption that we will already have APS so all builders (= execution proposers) are sophisticated? Or maybe there can be an opt-out mechanism to allow for blocks to be proposed without the delayed execution (and consequently the upfront payment), probably with a lower gas limit?

---

**thogard785** (2025-02-06):

I see. So I think my concern would be around EIP-7702:

- If we assume that the block builder does execute the block, I don’t think that the builder would include txs that aren’t profitable for the builder, so I don’t see the need to “skip” txs. If the builder wants to pay for the unfunded txs, imo let them.
- If we assume that the block builder doesn’t execute the entire block, then there is a pretty gnarly attack vector on the builder created by 7702.  For context, EIP-7702 allows for bytecode to be deployed to EOAs.  Currently, in the absence of 7702, a block builder can build a valid block by looking at an EOA’s balance at the end of the last block and then ensuring that balance > (tx.gas + calldata_gas) * tx.gas_price + tx.value.  But this only works because of the invariant “only a tx from an EOA can decrease that EOA’s balance.” If we assume that the builder isn’t executing the txs in a block, 7702 will allow EOAs to frontrun their txs with other txs to arbitrarily drain their balances.  In a PBS-style competitive, permissionless auction, this type of adversarial behavior could be rational to decrease the value / profit of a builder’s block.

In the long term I think that skipping the tx would disincentivize that type of behavior - and incentives do matter - but I worry that presumed-adversarial actors in the MEV supply chain may interact with this mechanism in ways that cause unexpected externalities.

---

**Nero_eth** (2025-02-06):

Yeah, all good points!

![](https://ethresear.ch/user_avatar/ethresear.ch/lukaszrozmej/48/14715_2.png) LukaszRozmej:

> I would like to propose to call it an async execution rather than delayed execution.

Yeah, I can see why this makes sense.

![](https://ethresear.ch/user_avatar/ethresear.ch/lukaszrozmej/48/14715_2.png) LukaszRozmej:

> My main concerns would be around if this won’t close up some other paths we would like to explore in the future as the design is somewhat a one way ticket and will prevent us from having this execution feedback loop in CL. Not sure if there are already existing EIPs this would make void?

This is true. Initially, when considering the interplay between FOCIL ([EIP-7805](https://eips.ethereum.org/EIPS/eip-7805)) and the delayed execution proposal in its current form, it became clear that for FOCIL execution must be carried out before attesting to check whether a transaction—one that is not included in the block but is present on the IL—can be appended.

For other concepts, such as block base fee sponsoring, block-level access lists, or real-time proving, delayed execution offers significant advantages.

---

**Nero_eth** (2025-02-06):

Good questions! The additional liquidity requirement could indeed be a challenge for those who don’t have ~3 ETH on top of their 32 ETH. However, we need to weigh the pros and cons.

If pipelining execution unlocks significant efficiency gains and the only trade-off is monetary assets for “stake,” it might be a worthwhile approach (there are other downsides as outlined in the post). Local builders can still operate under the increased liquidity requirement, ultimately contributing to a more scalable network. For most users, the ~95% who are using MEV-Boost, the liquidity requirements are handled by the block builder.

---

**Nero_eth** (2025-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> So I don’t see the need to “skip” transactions. If the builder wants to pay for the unfunded transactions, IMO let them.

We need to skip transactions because, otherwise, they would invalidate the entire block. The builder pays for their inclusion—not for execution—since these transactions have no execution.

The only incentive for the local builder or MEV-Boost builder is to avoid skipped transactions. For the user, it doesn’t matter whether the builder includes transaction A and B from sender C in one order or the other. If a transaction is skipped due to nonce issues, the builder pays. This is consistent because one could argue that the fault lies with the builder.

---

**thogard785** (2025-02-06):

I think it’s more complex than this - in your inclusion-but-not-execution model you aren’t accounting for the opportunity cost of the transaction.

EDIT: I agree with skipping nonce-invalidated and signature-invalidated and other critical security issues. But specifically for gas cost invalid txs:

If the builder *is* executing the entire block then great, but they won’t include bad txs unless it’s profitable to do so. There’s no opportunity cost but there’s also no bad txs, so just charge the builder for the max execution cost of any invalidated-by-gas-cost transaction (and then execute it). There’s no reason not to do so.

If the builder *isn’t* executing the entire block, that also means the builder has to build the block based on the gas limit of each transaction rather than the execution gas used. This is because they don’t yet know what the execution gas used will be, because they haven’t executed it yet. Validators voting / attesting would similarly have to build the block based on gas limits rather than execution gas used. In this example, you’d still want to charge the builder for the max execution cost because that’s what corresponds with the blockspace that they’re reserving and it’s the opportunity cost to all parties involved for an invalid transaction.

This opens up a real can of worms though around gas costs and their relationship with gas limits. There is a lot of research being done on this area that should help inform on delayed execution strategies. I agree with you that the two are inherently linked and that it’s hard to discuss details of async execution without first clarifying changes to gas cost.

---

**Nero_eth** (2025-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> So just charge the builder for the max execution cost of any invalid transaction (and then execute it). There’s no reason not to do so.

You cannot execute an “invalid” transaction—that’s what makes it invalid. There are only two options:

1. Skip execution.
2. Invalidate the entire block.

If such a transaction were executed, it could “overwrite” a past transaction through nonce reuse.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> If the builder isn’t executing the entire block, that also means the builder has to build the block based on the gas limit of each transaction rather than the execution gas used. This is because they don’t yet know what the execution gas used will be, because they haven’t executed it yet.

This is only partly correct. For each transaction, we check whether its maximum gas usage (the gas limit) still fits within the block. However, after executing the transaction, we only subtract the actual gas used from the block gas limit.

For example, if I include a 21k gas transaction (consumes 21k and has 21k gas limit) in a block, another 21k transaction cannot be added to that block if it specifies a gas limit equal to the block gas limit. Ordering them vice-verca works. This logic remains unchanged with delayed execution.

Importantly, even skipped transactions consume gas—otherwise, this would create a DoS vector. However, they only consume *inclusion gas*, which is fair since the transaction remains available indefinitely and can still be used for DA.

---

**GregTheGreek** (2025-02-11):

That makes sense, I was trying to target failed txs due to races (eg: solvers, or liquidation bots) which we can fully remove from the blocks and state entirely.

We might be able to do both at the same time.

---

**thogard785** (2025-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> You cannot execute an “invalid” transaction—that’s what makes it invalid. There are only two options:
>
>
> Skip execution.
> Invalidate the entire block.
>
>
> If such a transaction were executed, it could “overwrite” a past transaction through nonce reuse.

Apologies for the typo. I was specifically and exclusively referring to transactions “invalidated” post-inclusion due to a gas balance shortfall. But invalidated is probably the wrong word to use if they’re actually executed ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12)  Rewording it, I think the gist of my point was that it’s not clear to me why this new case (gas cost shortfall) should lead to an invalidated transaction if we can make the block builder on the hook for the gas cost anyway. I don’t see the benefit of separating out an inclusion cost from an execution cost - can you elaborate on the motivation and benefits of doing so?

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> This is only partly correct. For each transaction, we check whether its maximum gas usage (the gas limit) still fits within the block. However, after executing the transaction, we only subtract the actual gas used from the block gas limit.

That’s how synchronous execution works.

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> For example, if I include a 21k gas transaction (consumes 21k and has 21k gas limit) in a block, another 21k transaction cannot be added to that block if it specifies a gas limit equal to the block gas limit. Ordering them vice-verca works. This logic remains unchanged with delayed execution.

I must be fundamentally misunderstanding your design because I do no believe that the logic is unchanged with delayed execution. In fact, I believe your example illustrates the difference.

For the two txs in your example:

**BlockGasLimit**:

30,000,000

**Tx A:**

GasLimit: 21,000

GasUsed (in Execution): 21,000

**Tx B:**

GasLimit: 30,000,000

GasUsed (in Execution): 21,000

**Synchronous Execution**, sequence [A, B]:

GasAvailable for the Second Tx =  BlockGasLimit -  GasUsed_A = 29,979,000

GasNeeded for the Second Tx =  GasLimit_B = 30,000,000

Tx B **cannot** be included because GasAvailable < GasNeeded

**Asynchronous Execution**, sequence [A, B]:

GasAvailable for the Second Tx =  BlockGasLimit -  GasLimit_A = 29,979,000

GasNeeded for the Second Tx =  GasLimit_B = 30,000,000

Tx B **cannot** be included because GasAvailable < GasNeeded

Matches so far, but if we flip the sequence:

**Synchronous Execution**, sequence [B, A]:

GasAvailable for the Second Tx =  BlockGasLimit -  GasUsed_B = 29,979,000

GasNeeded for the Second Tx =  GasLimit_A = 21,000

Tx A **CAN** be included because GasAvailable \ge GasNeeded

**Asynchronous Execution**, sequence [B, A]:

*Note that we’d have to execute Tx B to know that it only used 21,000 gas in execution, and executing Tx B is not possible with delayed execution.*

GasAvailable for the Second Tx =  BlockGasLimit -  GasLimit_B = 0

GasNeeded for the Second Tx =  GasLimit_A = 21,000

Tx A **cannot** be included because GasAvailable < GasNeeded

In other words, with asynchronous / delayed execution, we do not know how much gas is used during execution and so the builder *has* to build the block by fitting the sum of each transaction’s gas limit (not gas used) into the block. If it were built any other way, execution would be needed *prior* to validation in order to know how much gas was actually used.

This is also why I emphasize the opportunity cost of the transaction’s gas cost as if it were fully executed - this cost is relevant because the high gas limit is forcing out other transactions that could be executed inside of the same space and earn fees for the proposer (and/or burn for the protocol). The foregone revenue to the proposer / validator would be the full execution cost (+ inclusion if you separate it) of the invalidated tx. If we want to really lean into delayed execution, technically the opportunity cost would be based on the actual gas limit of the tx.

Please let me know if I’m missing something - perhaps there’s an “block overfilling” mechanism? But if so, it’s not clear to me what would happen if all txs used up all of their gas limit and the block itself became invalidated.

---

**Nero_eth** (2025-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> I don’t see the benefit of separating out an inclusion cost from an execution cost - can you elaborate on the motivation and benefits of doing so?

Ah, I see what you mean and there is actually a 3rd part that the coinbase could sponsor:

- Inclusion cost (delayed execution)
- Inclusion cost + base fee (delayed execution + block base fee)
- Inclusion cost + base fee + everything else (with only tx.value remaining)

While directly going to block base fee sponsoring seems intriguing, it definitely brings additional complexity and a smoother rollup of the phases might be better.

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> I think the gist of my point was that it’s not clear to me why this new case (gas cost shortfall) should lead to an invalidated transaction if we can make the block builder on the hook for the gas cost anyway.

This means that even though we COULD make the block’s coinbase base for underfunded transactions at execution, we don’t in the initial design. Besides the complexity it would increase the monetary requirement to local build (which might be fine though).

![](https://ethresear.ch/user_avatar/ethresear.ch/thogard785/48/11683_2.png) thogard785:

> Tx A cannot be included because GasAvailable < GasNeeded

Here, we would just stop executing and start skipping if the actual gas usage raises above the block gas limit during execution. For the inclusion cost is already paid at that point. The builder would lose the inclusion cost for the transaction that went over the block gas limit.

---

**thogard785** (2025-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Here, we would just stop executing and start skipping if the actual gas usage raises above the block gas limit during execution. For the inclusion cost is already paid at that point. The builder would lose the inclusion cost for the transaction that went over the block gas limit.

Right but you can’t stop executing because you haven’t started executing because this scenario is prevented from happening by checks that occur when the block is validated, which happens before the block is executed.

You can’t have the tx gas used go over the block gas limit because:

1. the tx gas reserved can’t go over the remaining block gas limit
2. The tx gas used can’t go over the tx gas reserved.

If either of those conditions did happen (although I don’t believe it does in the example we were looking it), it would invalidate the block… but the second condition is impossible to reach because it requires execution, which would never happen because the first condition would get caught in the validation (before execution) and the block would be invalid anyway and so there’d be nothing to execute.

Edit: or are you saying the block builder could intentionally overpack the block and this would overflow the execution gas used, which would lead to a skip? In which case that would mean you’re removing check 1. (Prior paragraph) from the block validity requirements?


*(6 more replies not shown)*
