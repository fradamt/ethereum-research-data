---
source: magicians
topic_id: 13898
title: "EIP-6913: SETCODE instruction"
author: wjmelements
date: "2023-04-19"
category: EIPs > EIPs core
tags: [cancun-candidate, selfdestruct]
url: https://ethereum-magicians.org/t/eip-6913-setcode-instruction/13898
views: 3883
likes: 13
posts_count: 31
---

# EIP-6913: SETCODE instruction

SETCODE allows accounts to replace their code without clearing their state.

I hope this is adopted before, else when, `SELFDESTRUCT` is broken, to preserve the ability of accounts to replace their code.

PR: [Add EIP: SETCODE instruction by wjmelements · Pull Request #6913 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6913)

## Replies

**wjmelements** (2023-04-19):

Tentative EVM assembler support: [SETCODE by wjmelements · Pull Request #15 · wjmelements/evm · GitHub](https://github.com/wjmelements/evm/pull/15)

---

**joeblogg801** (2023-05-05):

In my opinion, it would be best if SETCODE and the removal of SELFDESTRUCT were implemented in the same fork. We’ve seen this scenario before when call and sload/store were repriced, which ended up breaking contracts. Although the issue was later resolved with a type 1 transaction, repeating the same mistake could be avoided by implementing both changes in the same fork.

---

**wjmelements** (2023-05-24):

This is my response to the Dedaub report, reiterating my advocacy for SETCODE.



      [docs.google.com](https://docs.google.com/document/d/16Gk5KjqLrDC65hEFDu28DgEQLpIOfWcYFdFdv61f9Jk/edit?usp=sharing)



    https://docs.google.com/document/d/16Gk5KjqLrDC65hEFDu28DgEQLpIOfWcYFdFdv61f9Jk/edit?usp=sharing

###

The report skims over MEV but doesn't speculate why this upgrade pattern is common among MEV bots who wrote their contracts in assembly. The reason is broader than MEV, and applies to normal DEX trading. Indeed any actor trying to get competitive...

---

**wjmelements** (2023-05-25):

I’ve made the following changes today:

- Changed opcode from 0x49 to 0xfc
- Disable within DELEGATECALL

Disabling within `DELEGATECALL` has the advantage that mutable code will be easier to identify in static analysis.

---

**joeblogg801** (2023-05-26):

Consider the following contracts (this is a pseudo code, not a valid solidity)

```auto
contract Child {
   external killMe() {
       selfdestruct(...)
   }
   external setCode(code) {
       setcode(code)
   }
}

contract Driver {
   Child child
   external run() {
       child.killMe()
       child.setCode(...)
   }
}
```

In order to provide a more precise definition of the expected behavior, it is suggested to further clarify the mechanism related to selfdestruct and setcode operations. The current specification states that selfdestruct clears the pending setcode, but it should be noted that in this example, setcode is executed after selfdestruct. The effect of selfdestruct is not observable until the end of the transaction, allowing for the possibility of reentering the selfdestructed contract and executing setcode on it.

To address this, it is proposed to introduce a more explicit definition, leveraging the language used in the yellow paper’s description of substate. Section 6.1 of the yellow paper defines substate as follows:

“Throughout transaction execution, we accrue certain information that is acted upon immediately following the transaction.”

Building upon this concept, it is recommended to introduce an additional element in the substate, referred to as ‘setcode set.’ This set would consist of accounts with associated pending code that need to be updated following the completion of the transaction.

Upon completion of the transaction, accounts included in the ‘selfdestruct set’ would be removed from the ‘setcode set.’ The remaining ‘setcode set’ would then be processed, and the associated code would be updated accordingly.

By adopting this refined definition, several benefits can be achieved. First, it clearly demonstrates how selfdestruct and setcode operations work together, highlighting the preference of selfdestruct. Second, it explicitly states that the result of the ‘setcode’ operation is not observable until the transaction is fully completed, providing a clearer understanding of the expected behavior.

---

**wjmelements** (2023-05-26):

Pending the meeting yesterday `SELFDESTRUCT` is likely to be disabled on mainnet before `SETCODE` is adopted. But suppose on some alternative chain they both coexisted.

Because `SETCODE` as currently defined takes effect after its call scope returns (as opposed to the end of transaction), the well-defined behavior for the code you provided would work as follows:

- The Child contract is marked for deletion by selfdestruct
- The Child contract’s code is updated by setcode
- After the transaction, the Child account is cleared by the selfdestruct

You are proposing to move `SETCODE` to the end of the transaction. I do not want this behavior because I want the parent contexts to be able to run validations (like EXTCODESIZE) on the result and revert if unexpected behavior occurred.

---

**joeblogg801** (2023-05-26):

In this case, it would be beneficial for `SETCODE` to function similarly to `RETURN` in the `CREATE` and `CREATE2` contexts. In other words, `SETCODE` should immediately conclude the execution and update the contract code. Allowing the execution to continue after calling `SETCODE` introduces the risk of undesired behavior, whereas an immediate return is a well-established behavior of `CREATE` calls, thus minimizing the risk of undesired behavior.

By adhering to the immediate return behavior of `CREATE` calls, the risk of unintended consequences and the need for extensive analysis to identify and resolve potential issues associated with executing additional calls or delegate calls after `SETCODE` is significantly reduced.

Might as well allow `SETCODE` in `CREATE` and `CREATE2` as another way to finish contract creation instead of using `RETURN`

---

**joeblogg801** (2023-05-26):

To ensure comprehensive coverage of the SETCODE behavior, it is important to consider the scenarios involving STATICCALL and CALLCODE opcodes:

SETCODE calls in a static context created by STATICCALL should indeed fail. Therefore, it is recommended that all SETCODE calls within a static context, established by the use of STATICCALL, be disallowed.

When it comes to SETCODE inside a CALLCODE opcode, it is suggested that its behavior align with that of DELEGATECALL. This means that SETCODE inside CALLCODE should have the same effect as executing SETCODE inside DELEGATECALL. This ensures consistency and expected behavior across opcode variations.

---

**wjmelements** (2023-05-27):

Returning early, as you suggest, does not simplify the issue because parent contexts may also be executing code from the modified account.

Executing with code different than the code of the current account is well-defined already due to the specification of `DELEGATECALL`. So it is not necessary to return immediately as you suggest. Matching the behavior of `DELEGATECALL` post-update should simplify analysis.

For the same reason, it’s also not necessary to defer the code update to the end of the current scope. So I will be updating the EIP to remove the deferral. It will simplify the specification. It will also allow the update to validate itself with `EXTCODESIZE` and `EXTCODECOPY`, rather than relying on a parent context.

---

**wjmelements** (2023-05-27):

Thanks. Though we agree the rule is obvious it is important for the specification to say so explicitly to minimize ambiguity. I will add these clarifications to the EIP today.

---

**wjmelements** (2023-05-27):

Updated: [Update EIP-6913: Remove Deferral and Clarify Staticcall by wjmelements · Pull Request #7081 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7081)

---

**joeblogg801** (2023-05-27):

Thanks for updating the spec

Just to clarify the expected behavior, assume the following scenario

Contract A currently executes a code belonging to the contract A account

Contract A calls SETCODE and the change is applied immediately

As a result of SETCODE Contract A no longer executes a code belonging to the contract A account, it is an orphaned code

Contract A continues the execution and calls SETCODE again

Do you expect failure or success?

If success then the ability to execute SETCODE should be established at the start of message call and preserved until the message call is finished

---

**joeblogg801** (2023-05-27):

Please forgive me for banging on about the same thing again and again. But the current definition of “the currently executing code that does not belong to the executing account” is not well defined for making an allow/fail decision for SETCODE.

Consider the following scenarios:

1. Contract A performs a delegatecall to itself, followed by a SETCODE operation.
2. Contract A performs a delegatecall to Contract B, which has the same code as Contract A, and then calls SETCODE.

In the second scenario, where Contract A delegatecalls to Contract B with identical code, it becomes challenging for the contract itself to distinguish between the two cases. The executing contract is unaware of the source of the code it is currently running.

One could argue that SETCODE in the second scenario should be allowed as well since the code being executed is the same.

Additionally, as previously mentioned, one could argue that after the first SETCODE operation, the remaining execution is not running the code belonging to the executing account. This distinction can be easily verified by comparing CODECOPY to EXTCODECOPY.

To address these concerns, I suggest to redefine the decision criteria in terms of how the message call was entered:

When in a STATICCALL context:

```
SETCODE should be disallowed (FORBID).
```

When in a non-STATICCALL context:

```
SETCODE should be allowed if the current message call was entered via a CALL operation or if it is the first call from an externally owned account (EOA) to an existing contract (excluding the initial contract creation call).
SETCODE should be disallowed (FORBID) in all other cases, covering variations of DELEGATECALL, CALLCODE, CREATE, CREATE2, and non-STATICCALL contexts other than CALL or first call from EOA to an existing contract.
```

By redefining the decision criteria in this manner, the specification becomes easier to understand and helps address numerous corner cases. It ensures that SETCODE behavior aligns with the context of the message call, resulting in a more coherent and predictable execution model.

---

**wjmelements** (2023-05-31):

> If success then the ability to execute SETCODE should be established at the start of message call and preserved until the message call is finished

Yes this is a better way to define it if we want to allow multiple `SETCODE` in the same scope. I wonder though if there is a security advantage to disallowing a second modification within the same scope.

Suppose some on-chain static analysis could be used to validate code. It could be used by another contract to validate that likely-immutable accounts are indeed immutable. Assuming `SLOAD` is much cheaper than on-chain static analysis, a set-once registry could be useful. Such a registry would benefit from the assumption that `SETCODE` cannot succeed twice in the same call-scope, as otherwise you could set the code to be immutable, register, and then set it to a mutable implementation. I suspect mutli-`SETCODE` makes on-chain validation that code remains immutable impossible.

The high gas cost of `SETCODE` should make multiple-`SETCODE` unlikely to be the optimal way to do anything, especially while `DELEGATECALL` remains available. `REVERT` is the best way to abort an upgrade. I don’t expect any iterative algorithm to be able to use less gas than alternative approaches.

So I am planning to remove multi-`SETCODE` unless we can think of a good reason to keep it. Removal of multi-`SETCODE` improves static analysis. With this `belongs-to` specification:

1. An account with immutable code cannot later have mutable code.
2. Mutable code can only be made immutable by invoking SETCODE
3. A context successfully invoking SETCODE prevents itself or any parent contexts from running SETCODE on the same account, unless REVERT or abort undoes the change.
4. The cascading behavior of Revert/Abort would also modify any state modifications conditioned upon reverted code changes.
5. A contract that performs a mutation after verifying some non-empty account’s code was immutable can be confident the code will remain immutable.

---

**joeblogg801** (2023-05-31):

Consider this

```auto
contract Decoy {
    external killMe() {
        selfdestruct(...)
    }
}

contract Mutable {
    external setCode(code) {
        setcode(...)
    }
}

contract Deployer {
    external registerAsImmutable() {
        decoy = create2_metamorphic(Decoy)
        // decoy does not contain setcode therefore it will be registered as immutable
        // it does contain selfdestruct but since selfdestruct is largely immutable now it passes the check
        registry.registerAsImmutable(decoy)
        decoy.killMe()
    }
    external deployMutable() {
        create2_metamorphic(Mutable)
    }
}
```

The attacker first calls registerAsImmutable to register the address as immutable, and then calls deployMutable to deploy a mutable version of contract.

This attack relies on changes to selfdestruct opcode behaviour to bypass the registry verification. It is reasonable that registry will consider the selfdestruct as acceptable for immutable contracts.

The safest option for this sort of registry is probably `require(caller = origin)`

---

**joeblogg801** (2023-05-31):

I assume the following still possible with new rules

```auto
contract Boostrap {
    // method called setContractCode
    external setContractCode(code) {
        setcode(code) // evm opcode
    }
}

contract ComplexSetup {
    // method called setContractCode
    external setContractCode(code) {
        setcode(code) // evm opcode
    }
    external setup(parameters) {
       // set state using sload, sstore etc
    }
}

contract FinalContract {
    // ... some useful methods
    // might have setContractCode(code) to support upgradability
}

contract Deployer {
    external deploy() {
        contract = create2(Bootstrap) // or create
        // contract has setContractCode method
        // I assume I am allowed to call setcode right after create?
        contract.setContractCode(ComplexSetup)
        // at this point contract has setContractCode and setup methods
        contract.setup(whatever)
        // I am still allowed to call this method since there are no parents that called setcode
        contract.setContractCode(FinalContract)
    }
}
```

The more I contemplate the proposal to propagate the invocation of setcode to parent message call frames, the less enthusiastic I become about it. The rules involved seem quite intricate, and I’m struggling to envision how they can be effectively implemented. It appears that this approach necessitates maintaining a significant amount of internal state to accommodate the rules. Since restrictions are not propagated to children frames the contract can call setcode again as soon as a new message call is entered. This fact further complicates the matter.Upon exiting the message call, the ability to call setcode for the contract should either be restored to its previous state or kept disabled.

In my opinion, the rules are overly complex and provide only marginal benefits. Therefore, I advocate for allowing multiple SETCODE calls instead. If someone needs to verify whether a contract meets specific requirements, they should perform this verification from the trusted entry point. In other words, ensuring that the verification call is the first one in the transaction would serve that purpose.

---

**wjmelements** (2023-05-31):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/j/aeb1de/48.png) joeblogg801:

> This attack relies on changes to selfdestruct opcode behaviour to bypass the registry verification.

I’m designing the `SETCODE` specification with the assumption that eip 6780 will be accepted.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/j/aeb1de/48.png) joeblogg801:

> The more I contemplate the proposal to propagate the invocation of setcode to parent message call frames, the less enthusiastic I become about it. The rules involved seem quite intricate

I don’t know what you mean here. The `belongs-to` rule is simple: you can only `SETCODE` if you are executing the code belonging to the account. The enumeration I made in my prior post are good properties of this rule, not more rules. All of those properties are violated by multi-`SETCODE`.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/j/aeb1de/48.png) joeblogg801:

> Since restrictions are not propagated to children frames the contract can call setcode again as soon as a new message call is entered.

That is desirable, and consistent with what you would expect, as such child frames would be using the updated code.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/j/aeb1de/48.png) joeblogg801:

> In other words, ensuring that the verification call is the first one in the transaction would serve that purpose.

I don’t wish to constrain security in this way. It would mean more accounts would need to assert that their `CALLER` is the `ORIGIN`, which would prevent various kinds of account abstraction.

---

**joeblogg801** (2023-05-31):

I was thinking about how to implement restrictions on the number of `setcode` operations, we can introduce a new field called `msgCallIndex` associated with each message call. The first message call in a transaction will have `msgCallIndex` equal to 1. Subsequent message calls created by operations like CREATE, CREATE2, STATICCALL, DELEGATECALL, CALL, or CALLCODE will receive an index from a monotonically increasing sequence. For example, the second message call will have `msgCallIndex` equal to 2, the third will have 3, and so on. We use a 64-bit field to store `msgCallIndex`, which provides more than enough space. Querying the `msgCallIndex` has a cost similar to querying other message call information like the address, which is 2. `msgCallIndex` is not an new opcode, it is an internal field maintained by vm for each message call.

Additionally, we add a non-persistent mapping to each transaction state called setcodeLastMsgCallIndexes and defined like this `mapping(address => uint64) setcodeLastMsgCallIndexes`. This mapping stores the last msgCallIndex value at which setcode was called for each address. The structure of this mapping is similar to how TLOAD/TSTORE is implemented and incurs a cost of 100 to read and 100 to update. setcodeLastMsgCallIndexes is an internal structure maintained by vm during a transaction execution.

The implementation of `setcode` after the usual checks (e.g., current message call is the first one or entered via CALL code, non-static message call) can be effectively done as follows:

```auto
// the cost is 100 to query the mapping + 2 for address + 2 for msgCallIndex
// check that this message call did not call setcode yet
// also check that there were no children message calls that called setcode
// since children will set mapping to a higher value than the current msgCallIndex
require(setcodeLastMsgCallIndexes[address] < msgCallIndex)

// the cost is 100 to set the mapping + 2 for address + 2 for msgCallIndex
// this line will prevent parents from calling setcode since parent message calls have lower msgCallIndex
// it will also prevent this message call from calling setcode again
setcodeLastMsgCallIndexes[address] = msgCallIndex

theRestOfSetCodeImplementation(...)
```

The revert mechanism can be implemented similarly to TLOAD/TSTORE. The log is maintained, and it is applied to setcodeLastMsgCallIndexes to restore the previous state if needed.

---

**Philogy** (2023-11-29):

Why have execution revert if `SETCODE` is used from within a `DELEGATECALL` context? I think semantics of `DELEGATECALL` should be retained in the sense that anything done in a delegate context is the same as a normal context except it’s applied to the delegatee account.

---

**wjmelements** (2023-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philogy/48/4714_2.png) Philogy:

> Why have execution revert if SETCODE is used from within a DELEGATECALL context?

Allowing during `DELEGATECALL` was the original specification. I’m open to either way. But the benefit is for static analysis to be able to detect whether an account has mutable code, whereas it is a much harder question when you can `SETCODE` within `DELEGATECALL`. The current specification, which I am calling `belongs-to` in this forum thread, would have another benefit that any code observed within an unreverted context to be immutable will always be immutable, allowing on-chain static analysis.


*(10 more replies not shown)*
