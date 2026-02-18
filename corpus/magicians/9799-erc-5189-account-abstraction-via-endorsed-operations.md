---
source: magicians
topic_id: 9799
title: "ERC-5189: Account abstraction via Endorsed Operations"
author: Agusx1211
date: "2022-06-29"
category: ERCs
tags: [account-abstraction]
url: https://ethereum-magicians.org/t/erc-5189-account-abstraction-via-endorsed-operations/9799
views: 3301
likes: 5
posts_count: 14
---

# ERC-5189: Account abstraction via Endorsed Operations

This is an account abstraction proposal that avoids consensus-layer protocol changes while maintaining compatibility with almost all currently deployed smart contract wallets.

It attempts to solve the same challenges as EIP-4337 but proposing a less restrictive framework.

Instead of tasking the wallets with implementing `simulateValidation` this proposal adds an `endorser` figure that (i) does not need to exist in the same address of the wallet (ii) it has no opcodes/storage access restrictions, and (iii) is never called on-chain.

https://github.com/ethereum/EIPs/pull/5189

## Replies

**MicahZoltu** (2022-06-30):

I feel like compatibility with existing wallets isn’t something we should be targeting.  I would like to see us (Ethereum community) targeting a future where it is worth making breaking changes today in order to have better things in the future.  The primary multisig that people use right now is Gnosis, which is upgradable by the user so if the thing we build requires changes to contracts that is OK for them, and users of other contract wallets can migrate to a new wallet without *too* much difficulty in most cases.

If we get backward compatibility for free then that is fine, but I don’t think we should target it.

---

**Agusx1211** (2022-06-30):

Is not only backwards compatibility with existing wallets, is also about flexibility in design.

If EIP-5189 is compatible with existing contracts it means it can also be compatible with a wider variety of smart contract wallet approaches, EIP-4337 has some limitations in that sense:

- No access to other contracts during signature validation.
- No mutability of state during validation (may be useful if the current wallet set of signers depends on something else, like a bridge message or presigned transactions).
- Built-in nonce that may be redundant or even conflict with other replay-protection ideas.
- Built-in deployment logic that may also be redundant, or conflict with other ways of deploying a wallet.

Some of these restrictions may not seem problematic now if we apply them to the current wallet implementations, but I think having a more open framework can help building better things long term (just like smart contracts are better than 30 different “blockchain modules”).

The tradeoff that I can see here is that bundlers may require a bit more work to include these transactions (because dependencies may include other addresses), but is not that far from EIP-4337 and it pales with the kind of work MEV extractors do on a regular basis. So maybe we aren’t paying a big price for a general-purpose solution.

---

**yoavw** (2022-07-06):

OK, this is going to be a long essay ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

In this post I’m going to

- demonstrate some security issues that arise due to removing ERC 4337 restrictions.  A comprehensive list would be too long but I’ll try to give a taste.
- argue that backwards compatibility and future development both turn out to be easier with ERC 4337 in practice.
- address the comparison and clear some misconceptions about ERC 4337 (e.g. the nonce and deployment methods are convenience methods not enforced by the protocol and shouldn’t conflict with other logic).

**DoS attacks against bundlers and the mempool**

Endorsers are only banned if they change their readiness decision without the dependencies changing. There’s no throttling on the endorser, just dropping the operation. It’s essentially free to keep sending more ops that will be simulated `MAX_OPERATION_REEVALS` times and dropped (or infinite times if the `optional rules` are not applied).  Eve creates an endorser that always wastes `MAX_ENDORSER_GAS` and returns `ready` along with a dependency on the Uniswap price of a high-volume token, or the nonce of an EOA used by some price oracle or rollup sequencer (hereafter an *ever-changing dependency*).  Then, repeatedly send ops with the minimum accepted gas price (below current market price but still mempool-acceptable).  Bundlers will keep reevaluating it until hitting `MAX_OPERATION_REEVALS`, and once the operation is dropped, Eve will resend it.  She will do this concurrently with as many wallets as the mempool is willing to accept with that dependency, and with multiple such dependencies - there are plenty of ever-changing slots and EOAs out there.  No throttling, so it keeps mempool clients constantly busy.

Not banning environment opcodes also makes it easy to attack the mempool despite the dependencies, by combining these opcodes with an *ever-changing dependency* as described above.  Eve creates an endorser and a wallet that checks the current block number, but also has an *ever-changing dependency*.  Each operation is simulated and accepted to mempool because it works for the current block number. Then it is reevaluated and becomes `ready==false` as the block number increased, but the endorser is not banned because a dependency also changed.  These operations can set a very high gas price since they are never included.  Therefore they will always be evaluated first, keeping the bundlers from simulating valid operations.  In ERC 4337 this attack would be prohibitively expensive since Eve would have to constantly change on-chain state in the wallet, but in ERC 5189 this attack is free and scales well.

In fact an endorser can get away with any behavior as long as the ops specify an *ever-changing dependency*.  It can perform any validation logic it wants, specifying an endorser that doesn’t even check which wallet calls it, but returns an *ever-changing dependency*.  The operations would only survive `MAX_OPERATION_REEVALS` blocks in mempool, so the user will have to rebroadcast the operation if it hasn’t been included yet (or use a rebroadcasting server).  But now this wallet can do anything it wants because the endorser can never get banned.  It’s equivalent to having no endorser and just requiring a rebroadcast every number of blocks.

The same trick can be used to evade the 12% replacement rule when changing an operation.  The endorser would set an *ever-changing dependency* but also check the block number in `isOperationReady()`. The user will keep resending the operation after every block if not included yet, and can keep changing it until it’s included.  The mempool clients will simulate every such operation twice (once when it’s valid and once in the next block where it’s no longer valid). The endorser never gets banned because the dependency always changes when the operation becomes “not ready”.

**Censorship vectors and attacks against endorsers**

If a wallet opens an attack vectors (e.g. mistakenly uses an environment opcode, and a malicious user deploys such a wallet and exploits it to cause a readiness change), its endorser gets banned.  What happens to existing instances of that wallet?  Bundlers stop serving its endorser and it doesn’t make sense to deploy a new one because it’ll be similarly exploited.  Users are effectively censored until they upgrade the wallet (by a direct transaction since bundlers won’t even let them call `upgrade`).

Another censorship vector arises from the limit on the number of times a dependency could be in the mempool at the same time.  Alice has a wallet with a proper endorser, which checks Alice’s nonce - a storage slot in her wallet.  Bob deploys another endorser that always returns the storage slot of Alice’s nonce as a dependency, and constantly floods the mempool with ops to that endorser. The mempool is filled with operations that depend on Alice’s nonce.  Alice is unable to add an op to the mempool even if she offers a higher gas price.

Yet another way to get an endorser banned and censor its users, is that the user could change the wallet’s behavior.  How does the endorser determine that the once-trusted wallet is still trusted to pay?  Inspecting the codehash is not enough since wallets can have complex configurations.  Consider Gnosis Safe for example.  Suppose an Eve deployed a valid GnosisSafe and the  GnosisSafeEndorser recognizes its code.  Eve then adds a new `guard` to the wallet, with a `checkTransaction` function that reverts in odd blocks but returns `true` in even ones.  Eve sends transactions to mempool during odd blocks and their readiness changes in the next block without a dependency change, causing bundlers to ban GnosisSafeEndorser and effectively censoring all GnosisSafe users.  The endorser could keep a whitelist of known guards, but that degrades Gnosis Safe’s functionality and prevents users from implementing new guards.  ERC 4337, in contrast, wouldn’t break this functionality.  It doesn’t care about the guard’s logic as long as it doesn’t do funky things like accessing the block number, which the guard has little reason to do.

The lack of separation between validation, execution, and post-operation, also makes it hard for an endorser to make sure the wallet can pay, which is another way to get an endorser banned.  The wallet can’t pay the max in advance because it has no way to trigger a refund at the end.  Therefore it has to pay at the end of the operation.  Consider a PayWithTokens wallet endorsed by PayWithTokensEndorser.  Eve deploys such a wallet and sends an operation paid with USDC.  The operation includes a signed `permit` to a 3rd party contract, and calls that contract to trigger a `transferFrom` of the entire balance.  When it’s time to pay, the payment fails.  The endorser had no way to detect this through dependencies or by looking at calldata.  The balance was still ok when `isOperationReady` was called, and there was no allowance to anyone.  The calldata isn’t a simple `transfer` that the endorser could parse.  It’s just a call to some arbitrary function in an arbitrary contract, which will get an allowance through the `permit` message and withdraw the balance.  The endorser would then get banned due to the failed payment, and all PayWithTokens wallet users will be censored.

**Difficulty of building profitable blocks**

Since there are cross-dependencies between operations, the proposal suggests that during block construction the endorser will be queried after simulating all the prior transactions in the block.  Suppose an operation pays enough to be included as the 100th transaction, but the 99th transaction (paying slightly more) invalidates its readiness.  The optimal block would change the order of these two transactions and get both fees, but simulating the block with many permutations is too expensive. More likely, the bundler would only collect the fee for the 99th operation and drop the 100th, which could have been included if the order was reversed.  In ERC 4337 the operations cannot affect each other’s validity (which means they’ll all pay the bundler) because all the validations happen before any operation. The bundler doesn’t need to worry about the order.  This enables more efficient and profitable building strategies.

To use the popular shipping-container analogy, setting certain restrictions on the shape and size of shipping containers made the entire cargo shipping industry more flexible.  Allowing containers of all sizes and shapes would significantly reduce the cargo ship’s capacity and may even put it at risk.

**Difficulty of implementation**

The proposal doesn’t make a distinction between the validation phase and the execution phase.  How will an endorser determine that a wallet is going to pay and not revert, based only on dependencies it knew about at the time of deployment and on observing `(entrypoint,data,gas)`?  The wallet would have to be written in a way that guarantees non-reversion and payment, regardless of the call outcome.  Current contract wallets are not compatible with this requirement, so it’ll be trivial to get their endorsers banned by causing a transaction to revert.  The endorser doesn’t have an insight into 3rd party contracts called by the transaction, only the wallet implementation and the contracts it is aware of.

Writing an endorser for a wallet with non-trivial dependencies is quite difficult. Consider a wallet that allows the user to pay gas with ERC20 tokens.  The endorser needs to have dependencies on the user’s balance in whatever ERC20 contract is being used for gas payment, as well as a DEX contract (e.g. Uniswap) to determine the price of that token in eth in order to properly compensate the bundler.  The latter may be a highly volatile dependency (e.g. the eth price in USDC) so the dependency will require constant reevaluation.  It also won’t be able to support arbitrary tokens, only ones whose contract is known to the endorser.  Otherwise there is no way for the endorser to find the right storage slots in these contracts.  The endorser won’t be future-proof and will need to be upgraded every time a new token is added.  That makes it a high-maintenance wallet.

Even with a known contract, how does the endorser find the slots for mappings that differ between wallet instances?  E.g. you write an endorser for Gnosis Safe and its `isOperationReady` calls `GnosisSafe.checkSignatures`.  The dependencies need to be the threshold (a permanent slot) and the mapping slots for all the owners.  The owners differ between wallets and the dependencies must cover all these slots but there’s no easy way to find their addresses on chain. `GnosisSafe.checkSignatures()` will access them during readiness check, but if an owner is removed while the operation is already in mempool, causing `checkSignatures()` to fail, how will your endorser set dependencies to catch it?

**Backwards Compatibility**

Adding ERC 5189 support to an existing wallet like Gnosis Safe seems more complicated than adding ERC 4337 support to the same wallet.  Wallets are not typically built with a non-reversion guarantee in the top level and with an ability to ensure payment for failed operations, which is the minimum requirement for supporting ERC 5189.  But they do all have clear validation logic (e.g. a signature check and a replay protection), which is the minimum requirement for supporting ERC 4337.

Furthermore, supporting complex wallet functionality such as Gnosis Safe `guards` is made difficult by ERC 5189’s flexibility, whereas the ERC 4337 model supports such extensions quite readily in most cases.

Therefore, wrapping an existing wallet with a 4337 wrapper will often be easier than modifying it to ensure the guarantees needed by ERC 5189.

**Addressing the comparison to ERC 4337 (now changed to “alternative proposals”)**

1. Indeed ERC 4337 imposes some limitations during validation, but not during execution. As I demonstrate above, it’s hard to protect the mempool without these limitations. As it turns out, these limitations are not a major issue for existing wallets. To use the Gnosis Safe example (since it’s the most common contract wallet afaik), the wallet doesn’t seem to call forbidden opcodes during its checkSignatures() call or nonce check. It can therefore be wrapped with an ERC 4337 compliant validation function without changing its logic. In fact I find it hard to imagine a real use case where a wallet would need to check the block number during validation.
2. ERC 4337 does not enforce any particular replay protection. The UserOperation.nonce field is not parsed by the protocol, only by the wallet’s validation function. Supporting different replay protections (e.g. parallelization through 2D nonces) is a part of the requirements.
3. ERC 4337 does not impose a particular deployment logic. EntryPoint offers a deployment method but it’s a convenience method. You could deploy an ERC 4337 wallet without going through EntryPoint at all, or you could implement a 3rd party deployer combined with a paymaster, performing different deployment logic in the context of a UserOperation.
4. Trusting EntryPoint is indeed a requirement in ERC 4337. EntryPoint is key to ensuring bundler and mempool safety, which is hard to achieve otherwise as I demonstrated above.
5. ERC 4337 does distinguish between execution and signature. Without this distinction it is hard to efficiently construct batches/blocks due to cross-effects between operations. I demonstrated this above in the “Difficulty of implementation” section above.

**Future improvements of ERC 4337 will bring much of the same flexibility without the added risk**

ERC 4337 tried give wallets the maximum flexibility, but turns out that writing a wallet that doesn’t live within certain restrictions and is still mempool-safe, is quite challenging.

We therefore decided to start with a set of restrictions that prevents all the vectors we, the community contributors, and our auditors at OpenZeppelin could think of.

However, we’ve been working to extend the functionality of staked components beyond just paying for gas.  The next iteration of ERC 4337 will use this modular approach to give wallets more flexibility during validation, while keeping risk exposure under control.  More on that soon…

---

**Agusx1211** (2022-07-06):

Thanks for this detailed analysis, I appreciate it.

I’m going to try to address the brought-up issues one by one:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> DoS attacks against bundlers and the mempool

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> There’s no throttling on the endorser, just dropping the operation. It’s essentially free to keep sending more ops that will be simulated MAX_OPERATION_REEVALS times and dropped (or infinite times if the optional rules are not applied).

This can be mitigated by using a sufficiently low `MAX_OPERATION_REEVALS`; genuine operations should not trigger many reevaluations anyway (since dependencies aren’t intended to be used for Uniswap/Chainlink etc. but nonces/configurations/implementations instead).

About `eve will resend it`, I think you may be right that some throttling is needed when an operation is dropped for lawful reasons. I don’t think the whole endorser has to be trotted, throttling individual storage slots from being dependencies should be enough.

I do not want to make these rules *mandatory*, because powerful bundlers with spare computational power *could* keep these in the mempool without harm. These operations may still become valid, or they could even be executed at a loss if the bundler can detect some other source of income (like mev extraction).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Not banning environment opcodes also makes it easy to attack the mempool despite the dependencies, by combining these opcodes with an ever-changing dependency as described above.

This departs from the assumption that you can construct an `endorser/operation` combo with the following properties:

1. It has a “fake” dependency that constantly changes.
2. It uses it to “hide” an actual dependency (opcode).
3. It can not be detected and thus can not be banned.

I argue that (3) is incorrect; the `endorser` can still be detected and banned.

It is correct that any `endorser` can include any dependency, including ever-changing storage slots (Uniswap, Chainlink, etc.). However, it is important to notice that the `endorser` is banned if it ever changes **readiness** without any of its dependencies changing beforehand. The fact that these dependencies can change later in the block is independent and should not affect the evaluation.

Knowing this, these scenarios would blow the whistle on the `endorser`:

1. Calling isOperationReady in isolation (as the first transaction on the block), as no other transaction can trigger the dependency change.
2. Including the operation as the first transaction in a block, as no other transaction can trigger the dependency change.
3. The operation should remain valid as long as the returned dependencies remain the same; this allows the mempool operator to “play” and evaluate isOperationReady using different future basefee, block_number, coinbase, etc. (This is not on the EIP yet).

(1) and (2) may happen by chance or because the mempool operator has a policy of including operations in a block before their respective dependencies are touched, (3) can be added as mitigation against this particular attack.

If the `operation` becomes invalid in any of those scenarios, then the mempool operator has proof that an unlawful readiness change occurred or **can** occur.

I guess the endorser could wait and only trigger the attack if the `dependency` changed, but then I would argue the ever-changing dependency is an **actual dependency** and can be treated as such.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Censorship vectors and attacks against endorsers

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> If a wallet opens an attack vectors (e.g. mistakenly uses an environment opcode, and a malicious user deploys such a wallet and exploits it to cause a readiness change), its endorser gets banned. What happens to existing instances of that wallet?

They need to deploy and use a patched `endorser`, because wallets don’t specify a single endorser; it should not be a problem.

If the endorser *can not* be patched (because the team is no longer available, or the wallet uses a top-level env opcode in a non-signed way), then the user can still recover the wallet by bypassing this mempool.

I consider such an event the exploit of a vulnerability, something that developers/users must watch out for the same way they do for correctness on the signature validation.

I also expect events of endorsers not being able to be patched to be very rare because this would require a wallet with transaction malleability, and this should be a vector of attack anyway even today. In contrast, if the bad behavior has to be explicitly signed by the user, then the endorser can decode, validate and filter it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Alice has a wallet with a proper endorser, which checks Alice’s nonce - a storage slot in her wallet. Bob deploys another endorser that always returns the storage slot of Alice’s nonce as a dependency, and constantly floods the mempool with ops to that endorser. The mempool is filled with operations that depend on Alice’s nonce. Alice is unable to add an op to the mempool even if she offers a higher gas price.

This is incorrect, for the replacement to happen the `operation` must also use the same `endorser`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Yet another way to get an endorser banned and censor its users, is that the user could change the wallet’s behavior. How does the endorser determine that the once-trusted wallet is still trusted to pay? Inspecting the codehash is not enough since wallets can have complex configurations.

The endorser **must** perform exhaustive validation; this includes inspecting the codehash, proxy pointers, configuration, etc. It must validate everything that may result in a transaction changing readiness.

In the gnosis example, the endorser must validate what (if any) guards are being used and if these guards are safe (or have safe payloads).

Keep in mind nothing is stopping a team from making an upgradeable `endorser`, so there is no technical reason to deploy an entirely new one when a new guard is released.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Consider a PayWithTokens wallet endorsed by PayWithTokensEndorser. Eve deploys such a wallet and sends an operation paid with USDC. The operation includes a signed permit to a 3rd party contract, and calls that contract to trigger a transferFrom of the entire balance. When it’s time to pay, the payment fails. The endorser had no way to detect this through dependencies or by looking at calldata. The balance was still ok when isOperationReady was called, and there was no allowance to anyone. The calldata isn’t a simple transfer that the endorser could parse. It’s just a call to some arbitrary function in an arbitrary contract, which will get an allowance through the permit message and withdraw the balance. The endorser would then get banned due to the failed payment, and all PayWithTokens wallet users will be censored.

This seems to be a poorly coded `PayWithTokensEndorser`; there are alternative designs that would allow the `endorser` to detect and validate the payment contract:

- Use an entrypoint that governs both calls.
- Make PayWithTokensEndorser be the entrypoint contract.
- Use a PayWithTokensEndorser that sends the funds directly to the bundler.
- Make the PayWithTokensEndorser permit only work if redeemed from the wallet, and the endorser can validate the wallet never redeems the permit.

This is not an exhaustive list, and I am sure there are more possible implementations.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Difficulty of building profitable blocks

This is 100% true; building profitable blocks becomes more complicated than using ERC-4337. I would argue this is not an issue for the following reasons:

- Block producers simulate a lot more transactions today during mev extraction or when including flashbot bundles, compared to what would be required for ERC-5189.
- Block producers are becoming specialized actors with far more resources than regular mempool operators.
- It incentives wallet developers to avoid operations that affect each other’s readiness.
- Worst-case-scenario operation inclusion is not optimal, but the leftover space can be filled with transactions from the regular mempool too.

The shipping container analogy is interesting, but I do not think it applies. Simulation capacity is far greater when building a block, and block building will never benefit from complete standardization (like containers) because some components will never comply with it (like MeV extraction).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Difficulty of implementation

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> The wallet would have to be written in a way that guarantees non-reversion and payment, regardless of the call outcome. Current contract wallets are not compatible with this requirement, so it’ll be trivial to get their endorsers banned by causing a transaction to revert.

Not necessarily; the `operation` can use an entrypoint that enforces these guarantees, for example, an entrypoint could use two signed transactions with the same nonce (one does everything, the other pays the entrypoint). If the call fails, the entrypoint reverts (only the first call) and uses the second transaction to get the funds to pay the bundler.

Then the `endorser` can validate a given `entrypoint` is being used, in a particular manner.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> The endorser doesn’t have an insight into 3rd party contracts called by the transaction, only the wallet implementation and the contracts it is aware of.

For most cases this will be true (the endorser will ignore 3rd party contract calls), but it must be noted that there is no technical limitation stopping the `endorser` from parsing the transactions and making decisions based on these 3rd party contracts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> The endorser needs to have dependencies on the user’s balance in whatever ERC20 contract is being used for gas payment, as well as a DEX contract (e.g. Uniswap) to determine the price of that token in eth in order to properly compensate the bundler. The latter may be a highly volatile dependency (e.g. the eth price in USDC) so the dependency will require constant reevaluation.

I think that making an `operation` depend on a DEX trade is quite dangerous; a sharp price movement can leave the bundler with an empty mempool. A good design would add some “guarantee” that the transaction will succeed independently from the DEX, and the endorser can validate such a guarantee directly (ignoring the DEX trade).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> It also won’t be able to support arbitrary tokens, only ones whose contract is known to the endorser. Otherwise there is no way for the endorser to find the right storage slots in these contracts. The endorser won’t be future-proof and will need to be upgraded every time a new token is added.

This is incorrect; mappings are deterministic, and nothing stops the endorser from replicating the formulas used for the storage key computation, thus including these storage keys as dependencies.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Even with a known contract, how does the endorser find the slots for mappings that differ between wallet instances?

The endorser would need to compute these keys, but I agree, right now there aren’t good tools for doing so (although it is still possible).

A Solidity library could be helpful, which can be used to derive the storage keys used by any Solidity mapping. In the future native support by Solidity (and other languages) should also be possible.

Remember that the `endorser` should already validate the wallet’s codehash; thus, it is working under the assumptions that it knows the wallet implementation code.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Backwards Compatibility

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Wallets are not typically built with a non-reversion guarantee in the top level and with an ability to ensure payment for failed operations, which is the minimum requirement for supporting ERC 5189.

The `entrypoint` does not necessarily have to be the wallet, so the `non-reversion` guarantee does not have to exist directly on the wallet. Existing wallets can be made compatible using an `entrypoint` that implements such guarantee.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> But they do all have clear validation logic (e.g. a signature check and a replay protection), which is the minimum requirement for supporting ERC 4337.

All wallets have validation logic, but not all wallets have a **pure** enough validation logic for ERC 4337. Wallets may need to *access 3rd party contracts* or even *modify contract state* during verification.

Some wallets **may** be able to adapt (sacrificing functionality and/or efficiency); but even these wallets would need to be upgraded to a new implementation (and if not proxies, a new instance will have to be deployed).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Addressing the comparison to ERC 4337 (now changed to “alternative proposals”)

1. I don’t think benchmarking these EIPs using similarity with the most common current smart contract wallet is a useful thing; because no current wallet represents the entire design space. Both proposals are compatible with gnosis wallet, so it should not pose a problem.
2. But then EIP-4337 assumes a nonce is what a wallet uses for replay protection; this is a typical implementation but not the only possible one.
3. The wallet deployment logic is “optional”, but the alternative is having to implement a paymaster that must run on-chain (making the whole process more expensive). I don’t see the benefit of having a protocol-defined deployment logic; it seems too costly for a convenience method.
4. .(see 5)
5. I agree both of these things make building blocks easier. I think the most significant tradeoff of EIP-5189 is that it requires more work when building a block; in exchange, it gets less on-chain overhead and higher compatibility.

---

**Agusx1211** (2022-07-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> The operation should remain valid as long as the returned dependencies remain the same; this allows the mempool operator to “play” and evaluate isOperationReady using different future basefee, block_number, coinbase, etc. (This is not on the EIP yet).

This may not even be necessary. The bundler can detect any “fake dependency” operation by re-running readiness after detecting that inclusion in a block will fail.

This re-run can be done with all the *old dependencies* but the *new evm globals*. If the `readiness` returns `true` then the `endorser` is banned because it’s lying on the readiness, and if it returns `false` then it’s banned for changing readiness outside the dependencies (the usual rules).

---

**yoavw** (2022-07-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> This can be mitigated by using a sufficiently low MAX_OPERATION_REEVALS

Even if we set it to 1, there’s no cost to rebroadcasting it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> About eve will resend it, I think you may be right that some throttling is needed when an operation is dropped for lawful reasons. I don’t think the whole endorser has to be trotted, throttling individual storage slots from being dependencies should be enough.

I’m afraid it’s not.  Endorsers are sybil-resistant due to the burned eth, so they can be effectively throttled (like paymasters in ERC 4337).  Wallets and dependencies are not.  There are plenty of ever-changing slots/nonces/balances.  A single endorser could use any number of them since they don’t need to be hardcoded.  Eve deploys a permissioned ensorser that returns `ready` for any operation she signs, and returns a dependency she provided as part of the operation.  She keeps sending operations with different `ever-changing dependencies` and keeps the mempool busy.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> powerful bundlers with spare computational power could keep these in the mempool without harm

They could, but should they?  Their CPU doesn’t just sit idle, they’re block builders competing on MEV.

Mempool maintenance competes against the resources they use for MEV searching and they’ll do whatever is most profitable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> The fact that these dependencies can change later in the block is independent and should not affect the evaluation.

It doesn’t need to change later in the block. It can change beforehand. The operations can pay enough gas to be considered, but less than other transactions in the pool which are going to change the dependencies.  E.g. rollup sequencers pay high fees, so Eve’s endorser has a dependency on the sequencer’s nonce and bids slightly below the sequencer.  The way reevaluation happens in the proposal, this will guarantee that the dependency changes before the `isOperationReady` call.

Eve has the benefit of being able to look at the mempool before sending the operation, so she can always pick a dependency that will change earlier in the block.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> Calling isOperationReady in isolation (as the first transaction on the block), as no other transaction can trigger the dependency change.

This would be a good addition to the proposal.  It adds one additional call per operation, but mitigates certain attacks.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> Including the operation as the first transaction in a block, as no other transaction can trigger the dependency change.

This one is less practical.  There are many operations so they can’t all be first.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> The operation should remain valid as long as the returned dependencies remain the same; this allows the mempool operator to “play” and evaluate isOperationReady using different future basefee, block_number, coinbase, etc. (This is not on the EIP yet).

This can become quite a cat & mouse game.  Bundlers add more checks, attackers observe their github (assuming they’re opensource) and change dependencies to keep up with them.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> (1) and (2) may happen by chance or because the mempool operator has a policy of including operations in a block before their respective dependencies are touched

This policy bypasses sort-by-fee policies?  I thought block builders will still prefer putting high fee transactions ahead of low fee ones.  At best they could put one transaction ahead of the others.  But testing 1 explicitly regardless of transaction placement is a good start.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> I guess the endorser could wait and only trigger the attack if the dependency changed, but then I would argue the ever-changing dependency is an actual dependency and can be treated as such.

The endorser can change dependencies based on calldata - see the malicious endorser I suggested above.  Eve could use it to frontrun the bundler’s checks so even 1 above wouldn’t mitigate it.  She monitors the mempool for high paying transactions that are very likely to be included in the next block.  She then sends an operation that depends on the nonce of that transaction’s sender, with a lower fee.  The mempool accepts her operation because it is evaluated against the current state (before the high-fee transaction).  When the 1 check is applied, `isOperationReady` still reports `ready` because the change hasn’t happened.  Then the high fee transaction is included early in the block, and when Even’s operation is reevaluated in mid block, it is no longer ready.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> They need to deploy and use a patched endorser, because wallets don’t specify a single endorser; it should not be a problem.

If the bug is in the wallet, the new endorser will be exploited immediately the same way.  E.g. if Eve finds a way to cause her wallet to revert in the top level, she will use it to ban every endorser.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> the user can still recover the wallet by bypassing this mempool.

Of course.  That’s always possible.  It just means the user must keep some eth in an EOA to be able to upgrade the wallet in such occasion.  But until the wallet maintainer releases a patch for the wallet (not the endorser), the user will have to keep bypassing the mempool for every transaction.  Kinda negates the benefit of switching to AA.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> I consider such an event the exploit of a vulnerability, something that developers/users must watch out for the same way they do for correctness on the signature validation.

True, except that such bugs will be much more common.  Failing to validate a signature correctly is a fairly obvious bug.  Failing to prevent any and all possible reverts in a contract, is a different story.  Formal verification can achieve this, but most contract developers are not proficient in writing K specs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> I also expect events of endorsers not being able to be patched to be very rare because this would require a wallet with transaction malleability, and this should be a vector of attack anyway even today. In contrast, if the bad behavior has to be explicitly signed by the user, then the endorser can decode, validate and filter it.

Why would this require a wallet with transaction malleability?  Suppose there’s a bug in the wallet that enables it not to pay the bundler.  E.g. the balance withdrawal attack I described in my previous post.  The wallet doesn’t pay, the endorser gets banned.  How do you patch the endorser in this case?  The wallet could make an arbitrary call that withdraws the funds through a different contract with different args each time, so you can’t decode it.  As long as the wallet has a non-paying or a reverting flow, endorsers will keep getting banned.  You can’t fix a wallet bug from the endorser, and I think it won’t be trivial to write wallets with the required guarantees.  Runtime Verification or Certora could ensure such guarantees, but with a 7 figures price that most wallet devs can’t afford.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> This is incorrect, for the replacement to happen the operation must also use the same endorser.

I wasn’t talking about replacement.  Read the attack again.  Alice’s operation is not replaced.  It is simply not accepted to the mempool because Bob filled it with other operations that have Alice’s nonce as a dependency.  It triggers the `Limit the number of operations in the mempool that depend on the same dependency slots` rule from the ERC, so Alice’s operation always gets rejected.  (The ERC makes this rule optional but I already argued that it can’t be optional because not enforcing it, makes mempool DoS very easy).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> In the gnosis example, the endorser must validate what (if any) guards are being used and if these guards are safe (or have safe payloads).
>
>
> Keep in mind nothing is stopping a team from making an upgradeable endorser, so there is no technical reason to deploy an entirely new one when a new guard is released.

This assumes that the Gnosis Safe teams are the only ones who implement guards.  But the whole point with guards was to make the safe modular and allow users to extend it.  If the endorser must know about the guard, then any user who deploys a guard will also have to fork and deploy the endorser, and burn eth for it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> This is not an exhaustive list, and I am sure there are more possible implementations.

Yes, there are many ways to solve this specific case.  The simplest is probably to use the endorser as an escrow that behaves like the ERC 4337 EntryPoint - collects the max fee at the beginning, pays the bundler and refunds the wallet at the end.  But my point is that it’ll be hard for wallet and endorser devs to cover all the possible ways the transaction could revert or not pay.  And the price of error is relatively high - the wallet not getting service from mempool until it is patched.  Why not outsource this logic to a single well built EntryPoint that guarantees payment?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> Block producers simulate a lot more transactions today during mev extraction or when including flashbot bundles, compared to what would be required for ERC-5189.

But it’s not instead.  It adds up.  The block producer will still perform the same mev work, and in addition, create ERC 5189 bundles.  If it’s more expensive to extract the same value when supporting ERC 5189, block producers just won’t do it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> The shipping container analogy is interesting, but I do not think it applies. Simulation capacity is far greater when building a block, and block building will never benefit from complete standardization (like containers) because some components will never comply with it (like MeV extraction).

Simulation capacity is high, but fully utilized for mev extraction.  Making it more streamlined by enforcing some structure will increase the block producer’s profitability.  The longer it takes to simulate and optimally include an average operation, the less profitable it becomes.  Very much like the shipping container analogy, where if the ship allowed different sizes and shapes of containers, loading it optimally would become a complex optimization game.  Therefore I think the analogy is quite accurate here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> Not necessarily; the operation can use an entrypoint that enforces these guarantees, for example, an entrypoint could use two signed transactions with the same nonce (one does everything, the other pays the entrypoint). If the call fails, the entrypoint reverts (only the first call) and uses the second transaction to get the funds to pay the bundler.

1. Signing two transactions for every operation would work but would be a hassle, especially when using a hardware wallet like Ledger.
2. This prevents reverts, but not balance withdrawals.  The entrypoint would also have to act as an escrow, ensure that the wallet paid in the first transaction, and revert the first transaction to apply the second one if it hasn’t paid.  That’s what the ERC 4337 EntryPoint does, except that the user doesn’t need to sign two transactions because it’s handled by the protocol.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> For most cases this will be true (the endorser will ignore 3rd party contract calls), but it must be noted that there is no technical limitation stopping the endorser from parsing the transactions and making decisions based on these 3rd party contracts.

How can it make decisions based on 3rd party contracts it wasn’t aware of at deployment time?  It can’t trace execution to find storage slots, and it would be too expensive to load the code of these contracts (recursively) and statically analyze it in solidity.  A static analyzer in solidity would be a fun exercise but probably not practical.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> I think that making an operation depend on a DEX trade is quite dangerous; a sharp price movement can leave the bundler with an empty mempool. A good design would add some “guarantee” that the transaction will succeed independently from the DEX, and the endorser can validate such a guarantee directly (ignoring the DEX trade).

But it’s not a DEX trade.  It’s a way to determine the ratio between the token price and eth.  The bundler pays for the block space in eth, so if it is compensated with a token, the wallet needs to calculate the conversion rate.  If the price is not a dependency, then it won’t compensate the bundler correctly.  And if it *is* a dependency then we have a dependency that changes in every block.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> This is incorrect; mappings are deterministic, and nothing stops the endorser from replicating the formulas used for the storage key computation, thus including these storage keys as dependencies.

I beg to differ.  Mapping is deterministic, but you only know it for contracts you’ve seen.  My comment was about supporting new ERC20 tokens for gas payment.  Ones that were deployed *after* the endorser was deployed.  Maybe they have the `balances` mapping rooted in slot 6, or maybe it’s in slot 13, and that results in different mapping addresses for each balance.  There’s no way to analyze this on chain, hence you’d need to upgrade the endorser every time a new token is added.  A good PayWithTokens wallet would be able to pay with any traded token without maintaining an ever changing whitelist.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> A Solidity library could be helpful, which can be used to derive the storage keys used by any Solidity mapping. In the future native support by Solidity (and other languages) should also be possible.

I already wrote such functions to calculate the addresses of mappings, arrays, mappings in arrays, arrays in mappings, etc. It’s not hard.  But this again assumes that you only interact with contracts you knew about at the time of deployment.  The endorser can’t calculate these things for a newly deployed token because it has no way to translate `balanceOf(address)` to a storage slot.  If it knew where the mapping is rooted, it could.  But this information is missing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> Remember that the endorser should already validate the wallet’s codehash; thus, it is working under the assumptions that it knows the wallet implementation code.

It knows the wallet’s code, but if readiness depends on other contracts, as in the case of paying gas with tokens, that’s not sufficient.  The endorser needs to know the storage structure of every contract that might affect readiness.  In practice it reduces the functionality quite a bit.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> The entrypoint does not necessarily have to be the wallet, so the non-reversion guarantee does not have to exist directly on the wallet. Existing wallets can be made compatible using an entrypoint that implements such guarantee.

Which is what the ERC 4337 EntryPoint does.  It provides the needed guarantees while abstracting it away from the wallet and the bundler.  The difference is that the ERC 4337 wallet needs to be aware and implement a single `validateUserOp` function, and in exchange we don’t annoy the user by asking for things like signing two transactions for every operation to guarantee payments.

Imagine a 4-of-6 Gnosis Safe multisig wrapped with a 2-transactions entrypoint.  Four different users need to sign two transactions instead of one. Worse yet, if the wallet as not aware and the users sign two messages with the same nonce, the wallet can be censored by a frontrunner who immediately sends the 2nd transaction, making the wallet pay without performing the requested operation.

There could be different EntryPoint models but they’re orthogonal to wallets and I don’t think wallet developers should have to design them.  Mempool safety is a different skillset from wallet development and we shouldn’t force wallet devs to become mempool experts if we can avoid it.  Enforcing mempool safety at the protocol level makes it easier to develop a safe wallet.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> All wallets have validation logic, but not all wallets have a pure enough validation logic for ERC 4337. Wallets may need to access 3rd party contracts or even modify contract state during verification.

True, in some cases they’ll need to separate the validation logic if it is tightly integrated with the actual operation.  In practice none of the contract wallets I’ve seen does that.  It sounds like poor coding practice, to mix validation logic with other things.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> Some wallets may be able to adapt (sacrificing functionality and/or efficiency); but even these wallets would need to be upgraded to a new implementation (and if not proxies, a new instance will have to be deployed).

Not necessarily.  Gnosis Safe for example could be upgraded to support ERC 4337 without upgrading it, by adding a module and a fallback handler to an existing safe.  If the wallet is written in a modular way (like Gnosis did), it will often be easy to add support without redeploying.  Not that it matters so much since there aren’t many contract wallets yet, and new ones would hopefully implement a `validateUserOp` function in order to benefit from the new mempool.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> I don’t think benchmarking these EIPs using similarity with the most common current smart contract wallet is a useful thing; because no current wallet represents the entire design space. Both proposals are compatible with gnosis wallet, so it should not pose a problem.

I agree the criteria shouldn’t be existing wallets.  Both standards can support Gnosis Safe.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> But then EIP-4337 assumes a nonce is what a wallet uses for replay protection; this is a typical implementation but not the only possible one.

The EIP doesn’t make assumptions about the nonce.  The wallet may keep the nonce field empty and use something else if it wants.  But it should implement some sort of replay protection in `validateUserOp` since a validated op is guaranteed to pay the bundler.  If it doesn’t prevent replay at this point, it’ll be griefed by replaying operations even if they later revert.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> The wallet deployment logic is “optional”, but the alternative is having to implement a paymaster that must run on-chain (making the whole process more expensive). I don’t see the benefit of having a protocol-defined deployment logic; it seems too costly for a convenience method.

The paymaster is also a convenience method.  What stops you from deploying an ERC 4337 wallet through any other process?  As long as your wallet knows EntryPoint and implements `validateUserOp`, it’s fine.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> I agree both of these things make building blocks easier. I think the most significant tradeoff of EIP-5189 is that it requires more work when building a block; in exchange, it gets less on-chain overhead and higher compatibility.

It does have less on-chain overhead (though not higher compatibility).  But less on-chain overhead only matters if bundlers are actually willing to put your operation on-chain and if mempool participants are willing to relay it to them.  ERC 4337 offers safety guarantees to bundlers and mempool participants, making it easy for them to participate.  A proposal that offers less safety guarantees and occasionally results in DoS against them, will probably lose their support after 1-2 such attacks.

---

**Agusx1211** (2022-07-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Even if we set it to 1, there’s no cost to rebroadcasting it.

If the storage slot is already throttled then the mempool operator can reject the operation right away.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> I’m afraid it’s not. Endorsers are sybil-resistant due to the burned eth, so they can be effectively throttled (like paymasters in ERC 4337). Wallets and dependencies are not. There are plenty of ever-changing slots/nonces/balances.

It’s true there are plenty of ever-changing possible dependencies, but the list is not **infinite**. So if throttling is persistent/aggressive enough it should be possible to protect against most of the common ever-changing dependencies.

Another thing to consider is that the mempool operators don’t need to add the `operation` to the mempool before applying throttling, we could add a rule that states:

- mempool operators must take the dependency list and validate how often these dependencies have changed in the last X blocks

If the operation fee is below `basefee` and dependencies previously changed too frequently, then the dependency can be throttled right away and the operation dropped.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> They could, but should they? Their CPU doesn’t just sit idle, they’re block builders competing on MEV.

This is true, but fees are still a kind of MEV, and a bundle of multiple operations can be a good enough payout.

I know it’s anecdotical but I’ve seen bots extracting MEV for ridiculously low amounts while dealing with non standard ERC-20 tokens.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> It doesn’t need to change later in the block. It can change beforehand. The operations can pay enough gas to be considered, but less than other transactions in the pool which are going to change the dependencies.

Bundlers should monitor for storage changes when constructing a block, and must re-evaluate (or invalidate) the readiness of an `operation` even if a dependency changes mid-block.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> She monitors the mempool for high paying transactions that are very likely to be included in the next block. She then sends an operation that depends on the nonce of that transaction’s sender, with a lower fee.

Ohh I think I see the attack now, so Eve is forcing the mempool operator to process an operation (for 1 block), while knowing this operation will get invalidated and thus it has zero cost for Eve, and Eve can use the existing mempool txs as a source of one-off changing dependencies (without having to send txs herself).

This wouldn’t be covered by the “evaluating against previous blocks approach”, because these could be dependencies that change sporadically, I imagine using balances would be the simplest way to attack using this method.

One possible mitigation is running `isOperationReady` against the next block candidate, but I don’t expect this to be enough since the transaction that changes the dependency may not be candidate for the next block, and yet still have higher priority than the `operation`.

Maybe this is an issue that has to be addressed with better `endorser` scoring/throttling, I think it’s possible to build a good endorser in such a way that you can’t force it to perform this attack (and thus force it to be throttled), if so then mempool operators should be able to filter the endorsers by scoring how many times a transaction is received and then invalidated quickly.

Another “last-resort” solution is to make mempool operators reject `operations` with fee below the current basefee.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> How do you patch the endorser in this case?

You can deploy a new `endorser` and also a new `entrypoint`, if the vulnerability is so severe that it can’t be patched by a “smarter” endorser then developers can always wrap the transaction execution in an `entrypoint` that restricts it even further (the two signed transactions example).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> It is simply not accepted to the mempool because Bob filled it with other operations that have Alice’s nonce as a dependency.

Isn’t it a similar case? The mempool operator could enforce the limit of `number of operations in the mempool that depend on a single storage slot` in a per-endorser basis.

It’s more risky since an attacker can use multiple endorsers to generate `operations` and invalidate them all at the same time. But this attack would be expensive to execute in a big enough scale, since the attacker would need to register and stake N endorsers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> This assumes that the Gnosis Safe teams are the only ones who implement guards. But the whole point with guards was to make the safe modular and allow users to extend it.

This is an interesting scenario, because someone must guarantee the guard will behave correctly in some way.

How does EIP-4337 solves it? `validateUserOp` can’t validate the guard because it can’t access third party contracts, and if implemented as a `paymaster` then the gnosis team paymaster doesn’t have a way of enforcing the guard contract isn’t going to call any forbidden opcodes either. So it seems to be a similar situation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Why not outsource this logic to a single well built EntryPoint that guarantees payment?

Biggest motivation is allowing for better flexibility and reducing overhead. Using an `entrypoint` contract is possible to make the any old wallet compatible with this new EIP, but an optimally developed smart contract wallet would implement this functionality directly.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> But it’s not instead. It adds up. The block producer will still perform the same mev work, and in addition, create ERC 5189 bundles.

Yes I agree this is adds more simulation cost (as any other mev extraction channel). I think this is one of the inherent tradeoffs of the proposal compared to EIP-4337.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Signing two transactions for every operation would work but would be a hassle, especially when using a hardware wallet like Ledger.

I don’t see the “two transactions” approach the ideal scenario, it’s a method to make *any* smart contract wallet compatible with the EIP, but a wallet designed from the ground-up should be able to provide the guarantees natively.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> This prevents reverts, but not balance withdrawals.

Yes I was talking about an entrypoint that looks like this, indeed very similar to what EIP-4337 does:

```auto
- Entrypoint
- - Entrypoint (self external call with try-catch)
- - - Wallet
- - - - Withdraw balance
- - Entrypoint (detects lack of balance/payment, reverts)
- Entrypoint (back to initial state, funds back in the wallet)
```

The difference is that this is only used for non-optimal wallets that don’t natively support fee payment guarantees, the happy path has a lot less overhead.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> How can it make decisions based on 3rd party contracts it wasn’t aware of at deployment time?

Yes, it’s true the 3rd party contract code must be known when the endorser is coded.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> But it’s not a DEX trade. It’s a way to determine the ratio between the token price and eth. The bundler pays for the block space in eth, so if it is compensated with a token, the wallet needs to calculate the conversion rate.

Isn’t this the same scenario? the price spikes and many transactions move outside the bounds of `maxSpend` or even the available balance when sending these tokens, thus making all of them invalid at once.

Additionally I don’t think this EIP is meant to add support for native payment in tokens (without on-chain ETH conversion), this would require a lot more work since the bundler has to hold, trade and price these tokens when building the block.

Another important thing is that both the `endorser` and the wallet can access this price feed, what the `endorser` can’t do is making this price feed a `dependency`.

So lets imagine a “EndorserPaymaster” in ERC-5189, the `endorser` can validate that:

1. The wallet will use an oracle to determine how much the endorser must be reimbursed.
2. The wallet has enough tokens to reimburse it (at a fixed rate, not using the oracle).
3. The wallet will reimburse the endorser.

The endorser is taking some risk (the wallet may not have enough tokens to reimburse the endorser if the oracle moves sharply), but as a mitigation it can ask for a higher margin when evaluating (2).

In exchange the bundler does not need to worry about the oracle, token or trade. Because the endorser is the one guaranteeing the payment.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> My comment was about supporting new ERC20 tokens for gas payment. Ones that were deployed after the endorser was deployed.

This is true, future-proofing and adding support for all future ERC20 tokens would be next to impossible, but the `endorser` can still be updated to add support for them.

Also endorsers/paymasters who support *any* token as payment would be super tricky to implement anyway, because if the `endorser` does not know the token then it must validate that such token is traded for `eth` before paying the bundler, this trade inevitably leads to a dex trade, and a shared dependency.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Imagine a 4-of-6 Gnosis Safe multisig wrapped with a 2-transactions entrypoint. Four different users need to sign two transactions instead of one. Worse yet, if the wallet as not aware and the users sign two messages with the same nonce, the wallet can be censored by a frontrunner who immediately sends the 2nd transaction, making the wallet pay without performing the requested operation.

This assumes gnosis wallets won’t update/extend to natively provide guarantees.

Also the “two signed transactions” is not the only possible solution, depending on the specific gnosis implementation something like the `transaction builder` could be used to enforce fee payment.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> who immediately sends the 2nd transaction, making the wallet pay without performing the requested operation.

This can be safely mitigated by making the `entrypoint` reject the payment unless the 1st transaction already failed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Mempool safety is a different skillset from wallet development and we shouldn’t force wallet devs to become mempool experts if we can avoid it.

I don’t think this EIP asks wallet developers to learn about mempool safety, in theory (if the rules are defined correctly) wallet developers just need to provide “tools for validating readiness of their transactions” using the endorser, and that should be enough.

The wallet development team should be able to write a good endorser since such endorser is practically executing the same logic as the wallet itself.

But it’s true that developers would need to account for the good practices to avoid their transactions from being throttled or dropped.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Not necessarily. Gnosis Safe for example could be upgraded to support ERC 4337 without upgrading it, by adding a module and a fallback handler to an existing safe.

This requires sending an on-chain transaction that adds a codepath to the wallet, I think it falls under the definition of “being upgraded”.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> The EIP doesn’t make assumptions about the nonce. The wallet may keep the nonce field empty and use something else if it wants.

It’s possible, but it adds even more overhead for EIP-4337, because now it also includes an empty field.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> The paymaster is also a convenience method. What stops you from deploying an ERC 4337 wallet through any other process? As long as your wallet knows EntryPoint and implements validateUserOp, it’s fine.

Then it would require accessing the traditional mempool, or a relayer. Ideally the EIP should be able to deploy *any* kind of wallet, in the most efficient way possible.

---

**dror** (2022-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> How does EIP-4337 solves it? validateUserOp can’t validate the guard because it can’t access third party contracts,

It doesn’t have to.

Guards are used during execution. validateUserOp only validates authorization and replay.

If the owners of the safe sign a tx that would fail by a guard, the safe will pay for its inclusion.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> It’s possible, but it adds even more overhead for EIP-4337, because now it also includes an empty field

A wallet is expected to use some extra data to provide replay (otherwise, sending the same transaction twice would be considered a relay). In 4337, we call this “nonce”, but don’t mandate anything and its usage, only that it is 32 bytes long.

---

**MilkyTaste** (2023-10-16):

Some wallet providers are building time based access control to their AA wallets. This EIP doesn’t have a way to define when `block.<property>` affects the readiness of a transaction.

Could we add something like:

```auto
struct BlockDependency {
  uint256 maxNumber; // readiness inclusive
  uint256 maxTimestamp; // readiness inclusive
}
```

to the Endorser’s `isOperationReady` returns to account for these use cases? Otherwise an endorser will be unable to support these features, as there is no defined limit for holding an operation in the mempool.

---

**Agusx1211** (2023-10-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/milkytaste/48/7946_2.png) MilkyTaste:

> Some wallet providers are building time-based access control for their AA wallets. This EIP doesn’t have a way to define when block.

 affects the readiness of a transaction.

I think adding it to the return of `isOperationReady` is a good idea; exceeding either `block.number` or `block.timestamp` would trigger a re-evaluation. If a transaction doesn’t expire, then the endorser can return `max(uint256)`.

---

Another thing we should add to the `Dependency` struct is a way to mark that all storage slots of an address should be considered dependencies. This would make it easier to mimic the behavior of 4337 wallets, in the sense that the endorser can simply return “if anything changes for address X, revalidate.”

With these changes, the interface would look like this:

```solidity
struct BlockDependency {
  uint256 maxNumber; // readiness inclusive
  uint256 maxTimestamp; // readiness inclusive
}

struct Dependency {
  address addr;
  bool balance;
  bool code;
  bool nonce;
  bool allSlots;
  bytes32[] slots;
}

function isOperationReady(
  address _entrypoint,
  bytes calldata _data,
  uint256 _gasLimit,
  uint256 _maxFeePerGas,
  uint256 _maxPriorityFeePerGas
) external view returns (
  bool readiness,
  BlockDependency memory blockDependency,
  Dependency[] memory dependencies
);
```

---

**Agusx1211** (2023-10-16):

I also think we should consider extending the `Operation` structure. Currently, if a wallet wants to transact using a non-native token, it’s expected to first convert those tokens into the native currency before forwarding them to the bundler.

The problem with this is twofold: First, the conversion step adds extra gas costs to the transaction. Second, it can create a bottleneck if multiple transactions are using the same conversion method—especially if they’re relying on an AMM to swap tokens.

An alternative would be to allow the wallet to send tokens directly to the bundler. Bundlers could then decide which tokens they’re willing to accept for payment. To enable this, we could simply add a `feeToken` field to the `Operation` struct. If `feeToken` is set to `address(0)`, it would mean that the fee should be paid in the native currency. Otherwise, it could specify the address of an ERC20 token.

The conversion rate could then be determined by the `priorityFeePerGas` and `maxFeePerGas` fields. Essentially, these fields would now map `gas` to `feeToken`.

---

Another thing we should add is some `endorserCalldata` to the `Operation`. The rationale is that the endorser might need extra information to determine whether the transaction is sound, even though this information isn’t necessary for executing the transaction itself.

For instance, the wallet could be in a non-deployed state. To determine whether the wallet conforms to one of the formats understood by the endorser, the endorser needs to access its code. However, this code isn’t directly available. While the endorser could attempt to decode the transaction to find the deploy data, it would be much simpler (and require less computation) if the preimage of the counterfactual wallet were passed directly to the endorser.

I presume there will be additional use-cases for this “endorser-only” data.

---

**MilkyTaste** (2023-10-16):

Is there a vulnerability around `endorserCalldata`? If the client is sending inaccurate `endorserCalldata` causing readiness to be calculated inaccurately, it’s the endorser that gets punished. If the endorser needs to validate the `endorserCalldata` for accuracy, it doesn’t add value.

`feeToken` is a great idea.

---

**Agusx1211** (2023-10-16):

Yes the `endorser` will need to validate the accuracy of the `endorserCalldata` (like the rest of the operation). It does add value because some things are far easier to validate than to compute (reverse mappings, sorted lists, etc).

In most cases the endorser would have all necessary information on the `data` itself, but it could be hard to access (due to multiple layers of nested encoding).

It could also allow for a wider variety of endorsers, like an endorser that validates if an operation is healthy purely offchain and provider a proof in the form of a signature.

