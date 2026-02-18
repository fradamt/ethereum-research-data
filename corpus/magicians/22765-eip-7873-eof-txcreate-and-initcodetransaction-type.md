---
source: magicians
topic_id: 22765
title: "EIP-7873: EOF - TXCREATE and InitcodeTransaction type"
author: gumb0
date: "2025-02-04"
category: EIPs > EIPs core
tags: [evm, eof, evm-object-format]
url: https://ethereum-magicians.org/t/eip-7873-eof-txcreate-and-initcodetransaction-type/22765
views: 413
likes: 7
posts_count: 29
---

# EIP-7873: EOF - TXCREATE and InitcodeTransaction type

This is the discussion topic for [EIP-7873: EOF - TXCREATE and InitcodeTransaction type](https://eips.ethereum.org/EIPS/eip-7873)

## Replies

**cameel** (2025-02-05):

There is one thing I’m missing in the EIP’s rationale - what would be the downside to having *both* an EOF creation transaction and `InitcodeTransaction`? An obvious upside I see would be that it would remove the need to have a predeployed creation contract.

Alternatively, an `InitcodeTransaction` transaction with empty `to` could be special-cased to deploy the attached initcontainer, taking salt and constructor arguments from calldata, just like a predeployed contract would, but without the awkwardness of having to assign it an address and deploy it during a network upgrade.

I actually initially expected `InitcodeTransation` to be a such a specialized creation transaction but after reading the EIP I see that it’s more of a generalization of the standard transaction type. It’s not even required to use `TXCREATE` and deploy any of its initcontainers, which means that one could use it for arbitrary calls to EOF contracts. If the requirement to carry at least one initcontainer was relaxed it could be seen simply as an “EOF transaction” with deployment being a special case.

---

**gumb0** (2025-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cameel/48/4949_2.png) cameel:

> Alternatively, an InitcodeTransaction transaction with empty to could be special-cased to deploy the attached initcontainer, taking salt and constructor arguments from calldata, just like a predeployed contract would, but without the awkwardness of having to assign it an address and deploy it during a network upgrade.

This is an interesting idea, the main tradeoff here would be between the complexity of predeployment (done once at fork transition), and complexity of extra feature of the transaction, that has to stay forever, and after transition is actually redundant, because the same can be achieved with non-empty-`to` InitcodeTransaction after Creator Contract is deployed.

Additionaly, with such transaction it still would be required to use “Nick’s method” or similar hacks to deploy the Creator Contract in a cross-chain-safe manner, but one of the goals that EOF deployment design is trying to achieve is make such hacks unnecessary.

---

**pdobacz** (2025-02-20):

> Additionaly, with such transaction it still would be required to use “Nick’s method” or similar hacks to deploy the Creator Contract in a cross-chain-safe manner

I’ll add to this that it was noted in [this comment](https://github.com/ipsilon/eof/issues/162#issuecomment-2538446370), that Nick’s method doesn’t offer cross-chain deployments universally, not only is a hack.

Actually, do I understand correctly that to be cross-chain Nick’s method requires to use a pre-155 tx, thereby is not possible to use an InitcodeTransaction type at all?

---

**jochem-brouwer** (2025-03-27):

We should not use type 0x05 for this transaction type. It is used as MAGIC for signing authorities in [EIP-7702: Set EOA account code](https://eips.ethereum.org/EIPS/eip-7702). (Better be safe than sorry)

Side-note, we should maybe create an informational EIP on all the “magic” first bytes which are used within our ecosystem. There’s also 0x19 [ERC-191: Signed Data Standard](https://eips.ethereum.org/EIPS/eip-191) but it will take some time before we hit that transaction type ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**jochem-brouwer** (2025-03-27):

I am confused by the motivation of this EIP. In the current “Mega EOF” we can create EOF contracts “normally” by providing an EOF container with valid initcode to any tx with `to: null`. It should `RETURNCONTAINER` and then deploy one of the subcontainers in the calldata - right? Why do we need a new tx type? And what features does this bring which we don’t already have? ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

---

**gumb0** (2025-03-28):

No, EOF Creation Transaction is not going to be part of Complete EOF and is removed in devnet-1.

TXCREATE supersedes it, it’s a cleaner solution and provides extra flexibility and features, such as determenistic deployment address (not depending on nonce), and ability for smart contract wallets to deploy contracts from initdata in transaction.

Sorry for the confusion, some adjustments in EIPs are still underway.

---

**jochem-brouwer** (2025-04-01):

I did not realize that the deployments of EOF contracts currently (without TXCREATE) does not allow contract factories, since it cannot read containers from calldata. This is solved by TXCREATE and indeed makes a lot of sense. Thanks! (Would indeed be great if this would be motivated in the EIP such that it is clear what the goal of TXCREATE is → for instance, reading containers from tx “calldata” (but yes now a new field)).

I see that the current EIP has an “irregular state transition” to create the contract factory. Because we did not do this irregular state transition for other system-like contracts I think this will get a pushback. I can understand the reasoning, we have a way to create deterministic contracts on other networks, but this is bound by `gasPrice` so on networks with high gas price (or more accurate: high base fee) it could be impossible to submit this tx. However I think that this is still reasonable, because this deployment is only necessary on live networks, and new networks should “just” put this address in the prestate.

---

**gumb0** (2025-04-01):

The rationale for predeploying Creator Contract is that without EOF Creation Transaction (removed from the spec) there is no other way to deploy the very first EOF contract.

---

**pdobacz** (2025-04-03):

There was a discussion during EOF Implementers call around whether the Creator Contract should be a predeploy or a precompile. Posting takeaways for visibility and record.

Predeploy seems to have lead, pros:

- feels like a cleaner solution, more auditable, common EVM code for all clients
- no need to derive a gas schedule - gas charged according to EVM rules
- can be EXTDELEGATECALLed without exceptions to the rules
- a precompile making a sub-call (to the initcode) would be something new

Cons:

- clients need to find a way to introduce that account into the state at fork transition block

---

**jochem-brouwer** (2025-04-03):

I’m assuming TXCREATE is banned in legacy contracts? I was thinking along the lines “why didn’t we do this predeploy” then also for system contracts as 7002 and 7251, but this case is special since we have to deploy an EOF contract which cannot be done via txs and not be done via CREATE(2). So the choice between using a precompile (which is essentially a predeploy but now of non-EVM code) or predeploy seems rather clear to me: use the predeploy because of native EVM code (we want to move precompiles also to EVM [EIP-7666: EVM-ify the identity precompile](https://eips.ethereum.org/EIPS/eip-7666)).

I would suggest in the EIP to make it very clear how to compile the solidity source code such that it stays reproducible (also in a year or two). For that, also include the resulting bytecode of the compilation (so the EOF container)

---

**pdobacz** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> I’m assuming TXCREATE is banned in legacy contracts?

Wait, maybe I’m missing something, but this is actually a brilliant idea hidden there - allow TXCREATE in legacy contracts. This relieves us from the need for the Creator Contract and seems to have nothing blocking it (no immediates, no code-introspection). The Creator Contract can still be reasonably well deployed to chains using Nick’s method, or CreateX’s method. If desired to be introduced as a predeploy at a distinguished address, that still can be done, but isn’t necessary for EOF to bootstrap.

Let us analyze this possibility.

---

**jochem-brouwer** (2025-04-03):

I assumed that it would be banned in legacy contracts because it could technically change existing contracts, and stuff like `RETURNDATALOAD` is also not included in legacy contracts.

But yeah I guess this solves the “chicken and egg” problem.

Another question, why does `TXCREATE` pop a `tx_initcode_hash` from stack? I thought the idea was that we cannot do code introspection, so we need a new tx type where the tx initcode is now “hidden” from the EVM. But now it technically is not, because I can for instance create a InitcodeTransaction where the calldata equals the initicode at index 0. Now to get the initcodehash I hash the calldata and then perform a TXCREATE. If it succeeds, I know I had the right hash, and therefore I now have access to the initcode?

Why is this hash popped from the stack and not the index of the initcode I want to deploy?

Also, there is this in the abstract:

> EVM Object Format (EOF) removes the possibility to create contracts using creation transactions (with an empty to field), CREATE or CREATE2 instructions.

I read this as when EOF is introduced, it is now not possible to create contracts via `to: null`, `CREATE` or `CREATE2`. I’m assuming this is incorrect and that this only applies to not being able to create EOF contracts? (So in the context of [EIP-3541: Reject new contract code starting with the 0xEF byte](https://eips.ethereum.org/EIPS/eip-3541) ?)

---

**pdobacz** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> EVM Object Format (EOF) removes the possibility to create contracts using creation transactions (with an empty to field), CREATE or CREATE2 instructions.

I read this as when EOF is introduced, it is now not possible to create contracts via `to: null`, `CREATE` or `CREATE2`. I’m assuming this is incorrect and that this only applies to not being able to create EOF contracts?

It is correct, but maybe a tiny bit of an unfortunate wording there. EOF contracts cannot have a CREATE and CREATE2 instruction, so are not able to use these to create EOF or legacy contracts alike. `to: null` transactions with EOF initcode used to fail on 1st byte and after EOF fork transition they will continue to fail (assuming no EIP-7698), so that also makes it impossible for such transactions to create EOF or legacy code (that’s assuming TXCREATE is banned in legacy, ofc).

Maybe the misunderstanding comes from “EOF removes” - this should be read as “EOF contracts do not have the ability to create contracts using CREATE/CREATE2, as banned by 7620, and EOF fork upholds the lack of ability of `to: null` transactions to create EOF contracts, as granted by EIP-3541, or run EOF initcode”. It should not be read as “At EOF fork transition, all contract creation using `to: null`, CREATE, CREATE2 is removed”, which it may sound like.

---

**pdobacz** (2025-04-03):

As a by-product of the above exchange of posts (kudos to Jochem again for sparking an idea), there is a proposal to significantly simplify the EIP: [Update EIP-7873: unban TXCREATE in legacy EVM for bootstrapping by pdobacz · Pull Request #9593 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9593)

---

**pdobacz** (2025-04-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Another question, why does TXCREATE pop a tx_initcode_hash from stack? I thought the idea was that we cannot do code introspection, so we need a new tx type where the tx initcode is now “hidden” from the EVM

Sorry about late reply. Removing code introspection is most important with regards to code which exists on chain. TXCREATE mechanism still doesn’t allow you to modify the code within the EVM. At most you could analyze it and reject it using the approach you listed, or, but that seems prohibitively expensive, supply multiple initcodes, and choose one to deploy based on some EVM logic.

So I suppose TXCREATE “hiding” of initcode could also be realized by, instead of a dedicated tx field, in a way such that initcode was pointed to by an offset and size in tx’s calldata (and a hash for trust-less deterministic setups!), but that’s just an ugly hack (what if TXCREATE happens in a nested CALL? cannot use that call’s calldata, but “origin calldata”, ugh).

Lastly, using `tx_initcode_hash` instead of `tx_initcode_index` is precisely useful for deterministic deployment setups (counterfactual deploys, AA deploys too I guess), so that they can be opt-in rather than default.

---

**frangio** (2025-04-10):

Is there a reason why this restriction shouldn’t be lifted?

> InitcodeTransaction is invalid if the to is nil.

InitcodeTransactions with `to: null` that invoke TXCREATE and don’t deposit any code could be a good way to deploy EOF contracts. In particular, it doesn’t rely on preexisting TXCREATE factories.

We need a standard recommendation for how EOF contracts should be deployed and I don’t think it should rely on ERC factories. As it stands there is no standard deployment procedure, no standard way for tools to fetch the address of deployed contracts (`contractAddress` in tx receipts is no longer useful), I think this is pretty bad.

---

**shemnon** (2025-04-10):

We can look into it for sure.  Some of the deeper TXCREATE work stalled a year ago when TXCREATE and the InitcodeTransaction was removed from pectra scope. I think this was the question we were working on when it was shelved. There are some things to work out however:

- Would we allow only one initcode?
- If we allow multiple initcodes, would only the first be executed?

This would preclued a “all initcode must be ordered by hash” rule, but I feel all we need to avoid that is a reason why order is important, like this.

Entire TX fails if initcode[0] is invalid, otherwise validity of other initcodes doesn’t matter.

- This could be viewed as a natural side effect of attempting to execute it

data will become calldata to an initcode

- This preserves a EIP-7620 behavior where the data after the container became call-data

[@pdobacz](/u/pdobacz) proposed something simple like

```auto
if tx.to is null:
  assert len(initcodes) == 1
  run(initcodes[0])
```

Although I might make the assert >= instead of ==, but weakly held.

---

**pdobacz** (2025-04-10):

`assert len(initcodes) == 1` is just to do away with all the edge cases, especially the need to sort that list. Can be also a tx validity rule, but that needs some consideration. Yes, `tx.data` becomes calldata of the `initcodes[0]` execution. The hashing scheme would be that of legacy creation tx.

Big question then - what about TXCREATE in legacy EVM?

---

**shemnon** (2025-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pdobacz/48/3042_2.png) pdobacz:

> The hashing scheme would be that of legacy creation tx.

Meaning nonce driven address?

```auto
  contract_address = keccak256(rlp.encode([address, nonce]))[-20:]
  increment_account_nonce()
```

---

**pdobacz** (2025-04-10):

Yes, in absence of a non-hacky way to supply `salt`, unless we have an idea


*(8 more replies not shown)*
