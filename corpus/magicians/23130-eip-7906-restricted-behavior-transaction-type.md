---
source: magicians
topic_id: 23130
title: "EIP-7906: Restricted Behavior Transaction Type"
author: alex-forshtat-tbk
date: "2025-03-12"
category: EIPs > EIPs core
tags: [account-abstraction, transactions]
url: https://ethereum-magicians.org/t/eip-7906-restricted-behavior-transaction-type/23130
views: 342
likes: 7
posts_count: 13
---

# EIP-7906: Restricted Behavior Transaction Type

Discussion topic for EIP-7906:


      ![image](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7906)





###



A transaction type that provides a way for senders to restrict the outcomes of their execution










(Upd: new link to the EIPs website)

The point of this EIP is to provide the mechanism for wallets to actually restrict the outcomes of transactions the users are signing. This is just a building block on top of which a truly secure wallet UI can be build.

## Replies

**odysseas_eth** (2025-03-13):

[@alex-forshtat-tbk](/u/alex-forshtat-tbk) I love this proposal.

It’s very similar to the concept of [Assertions](https://x.com/phylaxsystems/status/1877732226739442149) that we have been developing for a while at Phylax as part of a wider [protocol](https://collective.flashbots.net/t/credible-blocks-security-guarantees-in-block-building/4089). Essentially, taking a more liberal approach of running some user defined solidity after every state transition, which evaluates whether it should be a valid state transition or not.

I have been ideating on a wallet/user-facing integration of the above concept, with wallets being able to offer “pre-defined” assertions for users to enable. One big difference is that we intend to integrate at the network level with enforcement being done by block builders.

Would love to collaborate on this. How are you thinking the support for EIP-7906? A modified full-node that makes the checks at the RPC level?

---

**alex-forshtat-tbk** (2025-03-13):

Hello [@odysseas_eth](/u/odysseas_eth), thank you for your feedback!

Regarding the Solidity defined Assertions, I think this is a great idea which gives a remarkable flexibility in defining the restrictions for a transaction. This is something that, unfortunately, will never be possible with a pre-determined set of restrictions like in EIP-7906.

It is not very clear if this approach of using full-fledged Solidity code for restrictions is practical for the Ethereum mainnet, but it may be worth it to think about having some minimal scripting support for restrictions in EIP-7906.

> I have been ideating on a wallet/user-facing integration of the above concept, with wallets being able to offer “pre-defined” assertions for users to enable.

Yes, in general I would hope that it becomes a common practice for smart contract developers and dapps to provide the transactions’ restrictions in the same way they currently provide raw calldata, and for the wallets to have a list of “pre-defined” restrictions for all major known contract types.

For instance, an ERC-20 token transfer will have a very simple “pre-defined” restriction saying “your balance goes down by X, another balance goes up by X, nothing else happens anywhere”, and this restriction is basically “hard-coded” in the wallet’s immutable code.

And for a transaction to a contract that is unknown to the wallet, the dApp would provide a restriction to the wallet saying “writes slots X,Y,Z in contract A and writes any slot in contract B and nothing else happens anywhere”.

There is already a set of RPC APIs around EIP-2930 access lists that could be used to prepare the restrictions.

The wallet will need to present this information to the user in a somewhat human-readable way. And in an “advanced” mode users should be able to get involved and modify the proposed restrictions, for example adding an extra ban on moving some especially valuable asset.

> How are you thinking the support for EIP-7906? A modified full-node that makes the checks at the RPC level?

With this being an “EIP”, if this proposal were to be accepted all full nodes in Ethereum would be modified in order to support the restrictions. We may require some modifications to the RPC methods but in general once the transaction is broadcast through the `eth_sendRawTransaction` RPC method there is no difference with other transactions, and the receipt will just state that the transaction reverted on-chain if the restrictions are violated.

> Would love to collaborate on this.

Sure, that would be great! Please feel free to share any feedback on the proposal itself and if there are any additional details about the assertions mechanism you have built, I would be happy to learn more.

---

**odysseas_eth** (2025-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-forshtat-tbk/48/1453_2.png) alex-forshtat-tbk:

> Regarding the Solidity defined Assertions, I think this is a great idea which gives a remarkable flexibility in defining the restrictions for a transaction. This is something that, unfortunately, will never be possible with a pre-determined set of restrictions like in EIP-7906.
> It is not very clear if this approach of using full-fledged Solidity code for restrictions is practical for the Ethereum mainnet, but it may be worth it to think about having some minimal scripting support for restrictions in EIP-7906.

Well, following the same philosophy of the EIP, we could send the EVM bytecode as part of the request, communicating that the EVM bytecode must not revert if executed after the transaction is applied to the state.

One thing that I like with the EIP is that because of the restricted nature of what constraints can be expressed, it doesn’t need to handle the complexity of adding a turing-complete user-defined computation at the end of a state transition.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-forshtat-tbk/48/1453_2.png) alex-forshtat-tbk:

> For instance, an ERC-20 token transfer will have a very simple “pre-defined” restriction saying “your balance goes down by X, another balance goes up by X, nothing else happens anywhere”, and this restriction is basically “hard-coded” in the wallet’s immutable code.

Yes, I have the exact same concept in mind.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-forshtat-tbk/48/1453_2.png) alex-forshtat-tbk:

> With this being an “EIP”, if this proposal were to be accepted all full nodes in Ethereum would be modified in order to support the restrictions. We may require some modifications to the RPC methods but in general once the transaction is broadcast through the eth_sendRawTransaction RPC method there is no difference with other transactions, and the receipt will just state that the transaction reverted on-chain if the restrictions are violated.

To be honest, I don’t see why we should be limited by the EIP process here. This feature we are describing here, either via EIP-7006 restrictions or the more turing-complete script version that I described with Assertions, could be unilaterally implemented as an experimental RPC path. Getting Infura/Metamask on-board for their default RPC endpoints would probably deliver more than 80% of the value. Instead of the transaction reverting on-chain, it would be instead dropped by the RPC node and then communicated to the user/wallet.

Of-course handling that at the RPC level introduces the risk of an attack which would modify the state inside the block in such a way that the transaction would actually violate the predicates when it’s executed inside the block. That would have been missed at the RPC level, since by necessity it can only check the transaction against the latest finalised state of the blockchain and not against the state on top of which the transaction will be executed when it’s added to the new block.

Will circle back with more comments as I reflect on this EIP.

---

**alex-forshtat-tbk** (2025-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/odysseas_eth/48/6410_2.png) odysseas_eth:

> We could send the EVM bytecode as part of the request, communicating that the EVM bytecode must not revert if executed after the transaction is applied to the state.

Right, however in order to support all features of restrictions this bytecode will probably need to have a mechanism to access private slots of contracts, so it can’t be achieved with a pure  EVM code.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/odysseas_eth/48/6410_2.png) odysseas_eth:

> Getting Infura/Metamask on-board for their default RPC endpoints would probably deliver more than 80% of the value.

My biggest concern with this approach is establishing a false sense of security, which is the worst possible outcome. It is more or less trivial for an attacker to extract the signed transaction from the user’s communication with Infura/Metamask and broadcast it to a non-compliant RPC endpoint.

However, the users may trust the wallet’s message saying that the transaction does not modify any important storage state and sign the transaction on a very shady front-end dapp.

This is a threat in addition to the one you described where the transaction changes its behaviour once it is included on-chain, which can be achieved in many different ways by an attacker.

---

**dror** (2025-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/odysseas_eth/48/6410_2.png) odysseas_eth:

> Instead of the transaction reverting on-chain, it would be instead dropped by the RPC node and then communicated to the user/wallet.

This is a great idea, and I think there are “RPC security proxy” services like this: validating a transaction before forwarding it to the actual blockchain.

But this solution is a completely centralized service: the user **trusts** the RPC service to perform this validation.

We want the user’s assertion to be enforced by the user (that is, signed by the wallet) and that no party afterwards can bypass this assertion.

Can you think of any other way to achieve this goal ?

---

**SamWilsn** (2025-04-01):

Now that we have 7702, can we emulate this without a protocol change? Just revert the whole transaction if certain properties no longer hold at the end of execution.

---

**alex-forshtat-tbk** (2025-04-01):

Well, some checks can indeed be performed fully on-chain by smart accounts but, in my opinion, one of the most powerful features of protocol-level restrictions is their ability to specify a rule that sounds roughly as “these things are allowed, **and absolutely nothing else is guaranteed to happen as part of this transaction**”.

Such a rule is simply impossible to check from inside the EVM. For example, the account could theoretically check that all balances of ERC-20 tokens it holds did not change, but it does not seem possible to check that there was no change in allowances. Checking that there were no ERC-721 token transfers during the transaction would require an ownership check for each held token.

Additionally, the on-chain checks would have to rely on the view functions of the contracts involved to provide all the necessary data, which may not always be sufficient. Private fields of smart contracts may also hold information critical for users’ security. For example, an `implementation` address of an upgradeable contract might be `private`, and therefore it cannot be checked by an EIP-7702 account.

But, if this upgradeable contract is trusted by the user, unexpected change to the `implementation` value may be as dangerous as a token transfer.

For me the whole point of EIP-7906 is to explicitly force the protocol change that provides a higher-level control mechanism on top of what can be achieved on-chain, kind of the last line of defence for the users.

---

**Jlm** (2025-11-17):

Hello Gents,

Thanks for the thoughtful discussion. Many of the points raised resonate with the work we’ve been doing on blind signing and transaction unpredictability. For context, we have been researching and addressing a new class of phishing attacks called **Transaction Simulation Spoofing (TSP)**, as well as broader TOCTOU-style issues.

I discovered this EIP a bit later than I would have liked, but *better late than never*. And I hope some of our observations can be helpful to the discussion. Below are a few reflections we’ve developed that may support the design space.

---

## 1. Verification Approach

TL;DR:

- It is extremely difficult on-chain to prove that nothing else happened.
- Slot- or access-list-based verification tends to be fragile under real market conditions.
- Focusing on semantic outcomes (what happened) instead of technical mechanics (how it happened) seems more robust.
- Events offer a natural substrate for representing these outcomes.
- Comparing the transaction outcome at Time of Check with the outcome at Time of Use could be a more reliable approach.

### 1.1 The “negative space” limitation

We strongly agree with Alex’s point:

from within the EVM, it is practically impossible to guarantee that **no unintended effect occurred**.

This is also something we observed in TSP.

For example, verifying the absence of unexpected approvals would require comparing pre- and post-state allowances for every asset and every address, which is computationally unfeasible.

For this reason, relying on the **7702 batching capability** to evaluate the final outcome of a transaction is likely insufficient: it can confirm that certain intended effects occurred, but it cannot prove that *no additional or harmful effects* happened alongside them.

### 1.2. Why access lists / slot diffs may not scale

DEX aggregators can adapt their routing dynamically depending on real-time conditions; tick intervals or liquidity can shift between the moment of signing and the moment of inclusion.

As a consequence:

- storage slots touched may differ
- contracts interacted with may differ

Even in *legitimate* use cases.

Therefore, validating technical details (slot sets, touched contracts, execution paths) may fail despite the transaction being *semantically* correct.

Validating technical mechanics does not always reflect the user’s expectations or the intended financial effect of the transaction.

### 1.3. Users reason in functional outcomes

Users think in terms of:

- “I give A, I receive B.”
- “I withdraw X.”
- “I stake Y.”

To improve UX and reduce blind signing, it seems fundamental to **abstract internal mechanics** and validate the **functional outcome**, not the specific implementation details.

### 1.4. Why events might be a better semantic surface

Although we do not yet have a strict standard for event usage, they are widely considered **best practice**:

- they log the functional evolution of dApps
- they are evaluated during audits
- they allow indexers to aggregate data cleanly

From our experience, events encode **user-visible actions** much more reliably than storage diffs.

So comparing **what happened** rather than **how it happened** feels like a more stable approach.

### 1.5 Intent-based semantic equivalence

This is why we have been leaning toward modeling expected outcomes as **intents**, and comparing executions through **semantic equivalence**, not bytecode reproduction.

For example, two different routes that swap the same two assets for approximately the same amount should be considered equivalent, even if the internal execution path diverges.

## 2. Ensuring Transaction Fidelity through Transaction Contractualization

Another angle we have been exploring is what we call **transaction contractualization**. We create a "contract” between the user and the chain to ensure that the user gets something *similar to what they signed for* at signing time. In other words, a practical form of **“what you see is what you get.”**

The idea is that users should be given:

- a clear, understandable representation of the transaction’s expected outcome
- the ability to control their tolerances (slippage, risk bounds, asset restrictions)
- enough context to decide whether the simulated outcome matches their intent

From a UX perspective, users naturally treat the simulation outcome as a form of agreement:

> “If I sign this, I expect this to happen.”

To capture this, the expected outcome (with user-defined tolerances) can be expressed in a structured **Intent** that accompanies the transaction payload.

This creates a **contract** between the Time-of-Check (simulation) and Time-of-Use (execution).

Validation then becomes a comparison between:

- the user-signed intent blueprint, and
- the actual executed outcome,

ensuring similarity within user-approved boundaries and helping guarantee transaction fidelity.

# 3. Protocol-Level Enforcement

**TL;DR:**

- Off-chain checks can be bypassed or altered, creating false confidence.
- Protocol-level enforcement seems necessary for predictable guarantees.
- Block execution provides the final, authoritative outcome.

### 3.1 Why protocol-level matters

RPC-level or client-side checks can help but cannot offer strong guarantees:

- the transaction can be intercepted and rebroadcast to nodes or builders that do not perform any validation
- ordering and final state may differ from simulation
- the verification environment may not match the final execution environment

Protocol-level enforcement appears much stronger because:

- ordering is final at this level
- final effects are known precisely
- results are stored on-chain, making them transparent, auditable, and consensual

Given these factors, we have been leaning toward the idea that **protocol-level enforcement is the only reliable place to ensure predictable and robust guarantees for users transactions outcome**.

### 3.2. User-centric validation

We believe users should be able to express:

- expected outcomes
- tolerances / slippage
- asset restrictions
- intended beneficiaries

And wallets should display this in **clear and accessible language**, reducing ambiguity and blind signing.

### 3.3. dApp-provided validation logic

We really like the idea of dApps helping specify how to evaluate transactions interacting with their protocols, they know their systems best.

However, we also see some considerations:

- malicious dApps may provide permissive or misleading rules
- legitimate dApps may unintentionally miss edge cases
- incomplete or incorrect rules can weaken security

So some form of standardization, validation, or templating may be useful to ensure consistency and safety.

### 3.4 TSP and TOCTOU in practice

In TSP attacks, we observed:

1. The simulation appears safe.
2. The dApp front-runs the user.
3. Execution diverges from simulation.
4. With 7702 batching, multiple assets can be drained in a single tx.

This is a classic **TOCTOU gap**. The state at signing differs from the state at execution.

Binding the transaction to the expected outcome and validating it directly against the *executed* effects seems to significantly prevent this class of risks.

## 4. Closing Thought

Really appreciate this EIP. It addresses several deep structural issues we’ve also been exploring.

Our current intuition points toward combining:

- semantic, event-based outcome evaluation
- user-defined tolerances
- intent-based contractualization
- protocol-level enforcement
- clear UX for expected results

We’ve been documenting some of these ideas in a draft we call the Transaction Fidelity Standard (TFS-1). It’s still a work in progress, but sharing it here in case any parts of it are relevant to this conversation: [link](https://github.com/IPSProtocol/IntentGuard/blob/main/TFS-1.md)

Happy to continue contributing ideas, test cases, or empirical findings.

Thanks again for opening this important conversation.

---

**aina** (2025-11-19):

it is greate, Looking forward to seeing it adopted more widely.

---

**alex-forshtat-tbk** (2025-11-20):

Hello and thank you [@jlm](/u/jlm) for the deep and thorough feedback!

First, I agree that scaling slot diffs may be a very challenging task.

In its final form it will require taking the “source verification” feature to the next level, where wallets have an understanding of the storage accessed by users’ transactions, applied to all smart contracts used in production.

However, even understanding and verifying the storage rules for, say, top 100 tokens and dapps can be extremely helpful, and this is a relatively easy task.

I don’t have the data but intuitivley it seems that the purely dynamically routed transactions represent a small share of transaction. These transactions can still benefit from the restricted behaviour rules in my opinion, but will not be able to benefit from the “and all other changes are not allowed” type of rules, of course.

Second, regarding events as the expression of user intents, while I do like the idea think they can be a great addition to the restriction rules, but we probably cannot rely on events exclusively.

There are many ways a contract’s state can be altered with potentially catastrophic consequences without any event being emitted, and on contrary an event may be triggered without a corresponding state change.

In a hypothetical example, an attack where a Vault is tricked to make a ‘delegatecall’ to a malicious contract and injects malicious co-signers can not be prevented with purely event-based rules.

I do like the idea of using events for the welll-known actions on well-known contracts, like token transfers and approvals, and will propose adding these to the EIP.

Third, regarding the tolerances, the EIP tries to provide some support for this feature, and it would be great to look for better ways to express these in a concise and efficient way.

Regarding the clear and accessible language, I believe that as long as the restrictions language is in fact concise and efficient, it will be easy for the wallets’ GUI to express it in a human-readable way using simple text and graphics.

This is true for both events-based and storage-based transaction rules.

Very strongly agree that no off-chain or RPC-level checks can come close to providing the level of security needed for this feature. We will look closer into Transaction Fidelity Standard and looking forward to collaborating on this EIP!

---

**ArikG** (2025-11-22):

It’s not just that RPC and off-chain level checks can’t get to the same level of verification (which is true), it is also that we already have those checks implemented in many wallets anyway. The ecosystem is full of security companies providing transaction security analysis and they are widely used. The thing we are looking for is complete assurance of some end-condition that can’t be bypassed and that can only happen if two things align:

1. We know how to define those conditions for the operation at hand
2. We have the onchain structure to execute these conditions properly

---

**Jlm** (2025-12-08):

Thank you [@alex-forshtat-tbk](/u/alex-forshtat-tbk) for the thoughtful reply. This is extremely useful, and I fully agree that focusing on storage slots for the most common protocols can deliver a quick win. As you pointed out, verifying a restricted subset of storage rules (erc20 tokens, simple dApps) is tractable and would already catch a meaningful portion of undesirable behaviors.

At the same time, we have observed that dynamic routing or dynamic slot access may be more frequent than we might think, particularly in protocols whose internal state evolves during the block:

- Uniswap v3/v4 (tick movement)
- DEX aggregators (1inch, Paraswap, etc.)
- Liquidity-management strategies
- Any protocol where routing depends on on-chain conditions

To better calibrate this, it would be valuable to gather:

- A list of protocols whose execution involves dynamic slot access as it is an implementation design.
- The percentage of monthly transactions interacting with them directly or indirectly

## Dynamic slot verification and gas predictability

Even if we accept slot verification as a baseline, the verification itself may done in a dynamic format to reflect real-world protocol behavior. This raises a design question: dynamic verification logic must remain stable.

If the gas required for slot verification varies significantly depending on which slots end up being touched, we risk:

- legitimate user transactions reverting during post-execution verification

Gas predictability becomes as important as correctness. Otherwise, a transaction that is semantically valid may still fail simply because the verification logic consumed more gas than anticipated.

This constraint between the “correctness” and “predictable cost” becomes fundamental to prevent failed transactions and lost gas, and worth addressing early.

## Delegatecall security as a separate class

Regarding the delegatecall examples you provided: I fully agree that this class of attacks cannot be captured purely through event-based validation. I also believe this sits outside the intended scope of this EIP, because delegatecall issues are structural to the proxy pattern itself.

Delegatecall is, essentially, remote code execution. In Web2 security terms, it is analogous to enabling JavaScript eval() without sanitization. something no production system would allow under OWASP best practices.

Imho, the most robust approach should be preventive rather than reactive: delegatecalls should only be allowed toward contracts explicitly whitelisted by the proxy owner.

This is the approach I implemented after the Bybit hack for Safe users, implementating a DelegateCall Security Guard:

https://github.com/theexoticman/zodiac-delegatecall-guard

Since both AA and 7702 adopt Safe-like proxy architectures for module composability, it seems important that the ecosystem eventually reevaluate this aspect.

If this guarantee is ensured, then a proxy-level event emitted before executing the delegatecall could provide a useful technical signal for post-transaction assertions, together with a whitelist check and an EXTCODEHASH match. We view this type of event as distinct from the financial or functional events emitted by dApp smart contracts; instead, it serves a structural, EVM-level purpose.

Even if this does not fit directly into the current EIP discussion, I am happy to continue this conversation.

[@ArikG](/u/arikg) Thank you for your input. On the definition side, I believe dApps are the best entities to express what must be verified. They understand their invariants, intended effects, and edge cases far better than any external analysis layer. A standard that allows dApps (and optionally wallets) to articulate expected outcomes or user invariants would give much more precise guarantees than generic risk heuristics.

On the enforcement side, I believe the verification phase whould suggest a slightly extended transaction lifecycle. After the normal execution of the business logic (regular transaction), but before committing the final state, the node would perform a verification phase that checks the declared or signed conditions. If these checks fail, the transaction reverts before touching the world state. Conceptually:

- Execute business logic
- Verify expected outcome
- Commit state changes

This insertion point, just before the state transition is finalized, is where protocol-level enforcement becomes meaningful in preventing unwanted outcomes.

Given the architectural implications, it would be valuable to hear insights from the Geth team on where such a verification step could live within the execution pipeline, how it could be standardized safely, and what the correct verification environment should be.

