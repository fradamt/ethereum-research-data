---
source: magicians
topic_id: 4382
title: EIP for disabling SELFDESTRUCT opcode
author: AlexeyAkhunov
date: "2020-06-25"
category: EIPs
tags: [evm]
url: https://ethereum-magicians.org/t/eip-for-disabling-selfdestruct-opcode/4382
views: 4247
likes: 24
posts_count: 19
---

# EIP for disabling SELFDESTRUCT opcode

Mandatory post for EIP discussion

---

[@jpitts](/u/jpitts)  Adding additional information here:

The content of the proposal: https://github.com/ethereum/EIPs/pull/2751/files

Pull request w/ some initial comments: https://github.com/ethereum/EIPs/pull/2751

Twitter thread: https://twitter.com/realLedgerwatch/status/1276239221037072390

## Replies

**matt** (2020-06-25):

How exciting!

Under security considerations, another class of contracts that might be worth mentioning (which you alluded earlier in the EIP as “polymorphic contracts”), is [@ricmoo](/u/ricmoo)’s [Wisps](https://blog.ricmoo.com/wisps-the-magical-world-of-create2-5c2177027604).

Also, [this paper](https://arxiv.org/abs/2005.07908) provides an interesting discussion on the current usage of `SELFDESTRUCT` and surveyed contract developers to gain insight into their feeling toward the opcode.

---

**chfast** (2020-06-25):

I would very much welcome such change, but I expect it will be very difficult to roll it out on mainnet because of huge “existing contracts breaking” potential.

However, there is a way not to break Wisps. The `SELFDESTRUCT` should continue to work as before if the contract has been created in the same transaction.

---

**matt** (2020-06-25):

> Polymorphic contracts are limited in their use, because changing the bytecode via SELFDESTRUCT + CREATE2 clears all the contract storage, making contract lose all its data, and making it unsuitable to replace Proxy Pattern as a technique for upgradable contracts.

Wouldn’t it be possible to `DELEGATECALL` into the polymorphic contract and use that as a technique for upgradable contracts?

---

**JayeHarrill** (2020-06-26):

Happy to see movement forward on this issue.

---

**JayeHarrill** (2020-06-26):

Could there be some context here?

---

**jpitts** (2020-06-26):

[@JayeHarrill](/u/jayeharrill), I updated [@AlexeyAkhunov](/u/alexeyakhunov)’s original post with more details.

---

**axe** (2020-06-27):

Hey,

This EIP is center on GASTokens and SELFDESTRUCT is not needed to run that type of tokens. We should not try to block gas tokens. That will be just a lost battle as people can make others types of refund schemes.

The question is more about complexity and if we want to have smart contract that can change behaviour and stay in the same address.

The incentive of SELFDESTRUCT is miss placed, why should i remove a smart contract of chain if in the end i will save max 50% of that transaction? Is just more racional to keep it on chain and forget about it. There is some cases when is important to remove that smart contract, but my intuition points that the major situation we end up in the “forget about it” case.

Removing the SELFDESTRUCT opcode touch other areas of research like storage renting. I feel that we still need one explicitly way of removing a smart contract from chain.

**Why not maintain SELFDESTRUCT, changing the behaviour so that will leave some code (the same of each delete smart contract) avoiding a new deploy to that address?**

---

**AlexeyAkhunov** (2020-06-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axe/48/14450_2.png) axe:

> This EIP is center on GASTokens and SELFDESTRUCT is not needed to run that type of tokens

Sorry I did not make it clear, but the main motivation for this EIP was not to block GasToken. It was mostly about complexity that SELFDESTRUCT introduces into the implementation of EVM.

---

**wjmelements** (2020-07-03):

Polymorphic contracts are the superior upgrade model. If you have thousands of token balances and allowances it’s much cheaper to upgrade the code in-place than to migrate to a new contract. If it’s too much work for the evm to ensure all of the storage slots are cleared, just don’t do it; it would save me the trouble of resetting all contract state. Most self-destructs are for contracts without state; very few contracts self-destruct with remaining state.

Instead you could incentivize other contracts to clear it out of the trie manually. A new opcode could point out external storage corresponding to an account without code and clear it for a gas refund.

---

**AlexeyAkhunov** (2020-07-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> If it’s too much work for the evm to ensure all of the storage slots are cleared, just don’t do it

Ha, ha, if only I designed Ethereum from scratch ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**Amxx** (2020-07-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> If it’s too much work for the evm to ensure all of the storage slots are cleared, just don’t do it; it would save me the trouble of resetting all contract state. Most self-destructs are for contracts without state; very few contracts self-destruct with remaining state.

Well, this is a real issue for these few contracts, as there security depends on an assumption that might not hold.

I wrote some of those, not for production use, but as a proof of concept. The idea was to use create2 + selfdestruct to provide a upgradeability pattern that would clean up a proxy’s the memory state before redeploying the proxy (with a new logic target).

The assumption was strong that the new proxy would start up with a fresh memory state. Clients not doing the cleanup would, at best create security flaw in my contracts, at worst cause a network split.

A few weeks ago I would have been against removing this opcode, because despite the fact that it is dangerous, and that it is a pain for clients to work with, it as some nice usecases … but if these usescases are party broken because the expectation for the smart contracts developpers are not what is actually happening on the client side … then I’d rather remove it then continue using something potentially borken.

---

**wjmelements** (2020-07-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> wjmelements:
>
>
> If it’s too much work for the evm to ensure all of the storage slots are cleared, just don’t do it; it would save me the trouble of resetting all contract state. Most self-destructs are for contracts without state; very few contracts self-destruct with remaining state.

Well, this is a real issue for these few contracts, as there security depends on an assumption that might not hold.

I believe my aforementioned opcode proposal addresses that issue.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Clients not doing the cleanup would, at best create security flaw in my contracts, at worst cause a network split.

Better to not clear the state then, to avoid such an issue. Strictly fewer contracts depend on being reincarnated with a clean slate than on the self-destruct opcode functioning properly.

---

**axe** (2020-07-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Polymorphic contracts are the superior upgrade model

Technically yes, but we are creating a opaque system to the user.

Please see [GitHub - 0age/HomeWork: HomeWork is an autonomous utility for finding, sharing and reusing home addresses for contracts.](https://github.com/0age/HomeWork)

Don’t think that changing the SELFDESTRUCT opcode will have impact on the majority of smart contracts. I also don’t think that simply removing the opcode is a solution, as stated before we need a way of removing code onchain. Not that “as is” today we have an incentive to do so. I’m more in favor of changing the behavior of SELFDESTRUCT to stop redeploys.

Until proven other wise using create2 as an upgradability mechanism is a poor design choose from the user perspective. We are just adding complexity.

Also note that is important discuss the incentive of removing code on chain. The incentive today does a poor job in that regard.

---

**wjmelements** (2020-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axe/48/14450_2.png) axe:

> we are creating a opaque system to the user

Opacity is the fault of current tooling, not a problem with the EVM. I’ve asked Etherscan to improve their “ReInit” UI, and I [contributed](https://github.com/etherscan/writecontract/pull/16) their original delegatecall proxy support. Each upgrade model has its opacity issues; it’s our job to help the users with it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axe/48/14450_2.png) axe:

> Until proven other wise using create2 as an upgradability mechanism is a poor design choose from the user perspective. We are just adding complexity.

That’s not how burden of proof works ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) End-users are generally unaware of upgrade mechanisms because they work with a GUI. Application-level programmers have no problem abstracting reincarnation, as you linked. It’s less gas for the EVM to not need to SLOAD and DELEGATECALL the implementation because the verification time is lower. It’s easier for users with a generalized “write contract” interface to interact with the current ABI than with a delegatecall proxy.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axe/48/14450_2.png) axe:

> Also note that is important discuss the incentive of removing code on chain. The incentive today does a poor job in that regard.

Perhaps the refund should be partially proportional to the codesize, like CREATE.

---

**wjmelements** (2020-09-04):

I wrote up my aforementioned proposal: [EIP 2936](https://github.com/ethereum/EIPs/pull/2936)

---

**axe** (2020-09-07):

Just to reference: [EIP-2937: SET_INDESTRUCTIBLE opcode](https://ethereum-magicians.org/t/eip-2937-set-indestructible-opcode/4571)

---

**akolotov** (2020-10-06):

```auto
After certain block number, the semantics of SELFDESTRUCT becomes the
same as the combination of POP, followed by transferring remaining ETH
to the address popped from the stack, followed by STOP.
```

It is necessary to note that the current `SELFDESTRUCT` behavior allows to send remaining ETH unconditionally. In other words, even if the recipient is a contract without the payable fallback, the funds will be added to the balance of this contract anyway. Sometimes, it is used to avoid attacks to imbalance the sender. Will this functionality be preserved by the construction described in the EIP?

---

**adompeldorius** (2021-08-26):

Hi, I am one of the participants in the [Ethereum Core Developer Apprenticeship program](https://github.com/ethereum-cdap/cohort-zero), and have performed some chain analysis on current usages of `SELFDESTRUCT` [here](https://nbviewer.jupyter.org/github/adompeldorius/selfdestruct-analysis/blob/4647fef99e2aa0a2031b997f3166f07dfa68d7cb/analysis.ipynb).

In the analysis, I discovered that there is an issue with the current proposal to disable or neuter the `SELFDESTRUCT` opcode, in that it opens a security risk to uninformed users of the Pine Finance contract. In short, users of this contract send tokens to an predetermined address called a *vault*. Relayers then trigger a function in the PineCore contract to create a new contract at this predetermined address using `CREATE2`, which executes a trade and then self destructs. Under the current behaviour, it is possible for a user to use the same vault several times. If `SELFDESTRUCT` is neutered, however, this would no longer be possible. In fact, if a user then tried to send tokens to a used vault, anyone could steal the tokens in the vault.

The possible options I see are:

1. Continue with the current proposal of neutering SELFDESTRUCT, but inform Pine Finance so they have time to deploy a new contract that doesn’t suffer from the same risks, in addition to informing their users about the risks of the existing contract. There could perhaps be other contracts that will be exposed to the same risk.
2. Come up with a proposal that does not create the security risk above. This can be done by either
 a) Implement the full functionality of SELFDESTRUCT, but in a way that does not require changing an arbitrary large part of the state. @vbuterin has suggested a couple of ways to do this, essentially changing which address in the state tree stores the contract state each time the contract is self destructed.
 b) Allowing SELFDESTRUCT if the contract was created in the same transaction. This solves the issue in Pine Finance, and also gives us the invariant that deployed contracts are immutable. This may also be less complex to implement than 2a). The disadvantage is that it may be more complicated to reason about this behaviour where SELFDESTRUCT is sometimes allowed, compared to allowing SELFDESTRUCT in all cases. Also, while this solution solves the Pine Finance case, there may be other cases that break, so further analysis should be done to find out what else might break.

What would be the best way to proceed from here? Should I do more chain analysis to help make a decision?

