---
source: magicians
topic_id: 13539
title: "EIP-6780: Deactivate SELFDESTRUCT, except where it occurs in the same transaction in which a contract was created"
author: dankrad
date: "2023-03-25"
category: EIPs > EIPs core
tags: [evm, opcodes, cancun-candidate]
url: https://ethereum-magicians.org/t/eip-6780-deactivate-selfdestruct-except-where-it-occurs-in-the-same-transaction-in-which-a-contract-was-created/13539
views: 6892
likes: 27
posts_count: 20
---

# EIP-6780: Deactivate SELFDESTRUCT, except where it occurs in the same transaction in which a contract was created

This thread is to discuss [EIP-6780](https://github.com/ethereum/EIPs/pull/6780), which is another attempt at getting rid of the `SELFDESTRUCT` opcode in order to pave the road for statelessness.

This particular EIP preserves the opcode when `SELFDESTRUCT` is executed in the same transaction that a contract was deployed. This is possible because all the created storage can be held in memory during that time, so the problem of not knowing which storage to delete when it is dispersed as described in the current verkle implementation does not occur.

The reason for this is that contracts exist on mainnet that currently use `SELFDESTRUCT` to limit who can initiate a transaction with a contract – by destroying the contract in the same transaction so nobody has a chance to call it (one example of such a usage is [Pine finance](https://ethereum-magicians.org/t/eip-for-disabling-selfdestruct-opcode/4382/20). This can be preserved using EIP-6780.

A previous attempt to preserve more functionality was EIP-6046, which however is deemed unsafe because it does not clear storage on `SELFDESTRUCT` and some contracts [do depend on it](https://ethereum-magicians.org/t/almost-self-destructing-selfdestruct-deactivate/11886/14). There is also EIP-6190, which implements full `SELFDESTRUCT` functionality in a stateless-compatible way using contract versioning. However, it is currently judged to be more complex to implement then the variant proposed here.

## Replies

**jochem-brouwer** (2023-03-31):

EthereumJS implementation: [PR](https://github.com/ethereumjs/ethereumjs-monorepo/pull/2612).

---

**gumb0** (2023-03-31):

Does it stop execution or not?

---

**leonardoalt** (2023-04-07):

Just bumping the question above: can you clarify what happens to termination?

---

**leonardoalt** (2023-04-28):

Regardless of the “does it halt execution?” bit missing in the spec, I just wanted to say that imho the proposed solution feels extremely hacky, and although relevant for discussions I don’t think it should be added into production code.

---

**vaibhavchellani** (2023-04-29):

Hey!

Just want to point out, we use SELFDESTRUCT as well for our contracts at Socket.tech. We built a gas-efficient immutable proxy using it. We use self-destruct to essentially “pause” contracts if there is a need.

Using this method of pausing combined with create2 allows us to create a proxy which doesnt do any storage lookups.

While we were well aware of SELF-DESTRUCT going away while building this we went for this route for short-term gas-optimisation, we plan to pause the contracts before SELF-DESTRUCT goes away.

Just wanted to chime in here to share how we use it.

---

**wjmelements** (2023-05-01):

EIP-6046 and EIP-6190 have the advantage that create2 reincarnations aren’t permanently broken.

An example where this could be very bad is quoted below:

[![Screen Shot 2023-05-01 at 5.50.05 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9c3c8fcf082db4b82f4857d2cd30432b8d60ef16_2_690x86.png)Screen Shot 2023-05-01 at 5.50.05 PM1910×240 42.5 KB](https://ethereum-magicians.org/uploads/default/9c3c8fcf082db4b82f4857d2cd30432b8d60ef16)

Contracts meant to upgrade in this way are not intended to be final. Finalizing them with a hard fork can freeze assets. Their assumption that they can replace their code later should not be violated.

---

**timbeiko** (2023-05-25):

Dedaub have performed an impact analysis of this EIP, which can be found [here](https://docs.google.com/document/d/1HDbym5YOoYj63xswMAwvt5Psh4JaI0biY06b6ZvYV2s/edit), along with [summary slides](https://docs.google.com/presentation/d/1_sUneROCVIs0hi9sDCErDrd-tQW7nwJVdFmdvIce5wM/edit#slide=id.p)

Some concerns with the report, by [@wjmelements](/u/wjmelements): [Include SETCODE when you remove SELFDESTRUCT - Google Docs](https://docs.google.com/document/d/16Gk5KjqLrDC65hEFDu28DgEQLpIOfWcYFdFdv61f9Jk/edit)

and a response to it by [@yoavw](/u/yoavw): [SETCODE (EIP-6913) security considerations - HackMD](https://notes.ethereum.org/@yoav/SETCODE-security-considerations)

---

**jochem-brouwer** (2023-05-27):

From the EIP

> Note that when verkle tries are implemented on Ethereum, the cleared storage will be marked as having been written before but empty. This leads to no observable differences in EVM execution, but a contract having been created and deleted will lead to different state roots compared to the action not happening.

I am an absolute novice in verkle tries. What happens if we do a pattern where we redeploy these contracts (like a CREATE2 → Selfdestruct → CREATE2 pattern) and at some point we actually /do/ create the contract (also with storage). Would this lead to problems in the verkle trie?

---

**fckverkle** (2023-05-28):

This eip is not “improving” but worsening ethereum, it’s just breaking stuff

```auto
The SELFDESTRUCT opcode requires large changes to the state of an account, in particular removing all code and storage. This will not be possible in the future with Verkle trees: Each account will be stored in many different account keys, which will not be obviously connected to the root account.
```

If it’s not possible with the fking Verkle tree, it should not be implemented on mainnet at all, why not just start a new layer 1 and implement it, instead of just breaking old contracts

Smart contracts are expected to be immutable, and now you guys are arbitrarily changing how smart contracts with selfdestruct behave, that warning for deprecation of selfdestruct previously is useless, many smart contract has already deployed before that and it can’t be changed anymore

Also, it breaks upgradability to the same address, what if some contracts need it and breaking it may cause users losing their funds, even it support that within the same transaction, it still break contracts that need upgradability to the same address in different transaction, and could potentially result in users losing their funds.

This also create inconsistency between other evm compatible chain, and the same evm code can behaves differently on different evm compatible chain, just like the previous PUSH0, many evm chains aren’t going to support it but at least that’s not gonna break stuff, but this eip is even worse and it’s going to break shit and causing users losing their funds

This eip is potentially causing users losing their funds and you motherfkers are just saying “I don’t fking care if others lose their funds, as long as I don’t lose my fund and I’m not affected then it’s fine”

If this is implemented, in the future, people will just think all opcodes can be modified anytime and smart contracts on ethereum can suddenly break in a change and they can potentially lose their fund, it’s nothing more than harming ethereum’s reputation and user base

---

**wjmelements** (2023-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> What happens if we do a pattern where we redeploy these contracts (like a CREATE2 → Selfdestruct → CREATE2 pattern) and at some point we actually /do/ create the contract (also with storage). Would this lead to problems in the verkle trie?

This solution was discussed but they were worried that existing patterns may rely on the storage removal. A new opcode such as `SETCODE` is the better way forward.

---

**jwasinger** (2023-06-08):

There is a PR for EIP-6780 in Geth [here](https://github.com/ethereum/go-ethereum/pull/27189).

I am also working on adding state test coverage: execution spec tests PR [here](https://github.com/ethereum/go-ethereum/pull/27189) .

---

**adriandev** (2023-06-11):

**PLEASE DO NOT DO THIS PLEASE**

Our project utilizes our own version of GasToken (similar to 1inch CHI Token) to save gas fees for our users. Although GasToken no longer saves gas, it still performs CREATE2 and SELFDESTRUCT operations in our contract logic. Our GasToken maintains an offset, consistently executing CREATE2 or SELFDESTRUCT at this offset. After this update, CREATE2 will fail if the current offset has not been properly SELFDESTRUCTed.

**Our contracts are non-upgradable.** After this update, most of our contract functions will revert, and user funds in our contracts, as well as liquidity in other DeFi projects, will be locked indefinitely.

**We believe that making such breaking changes is highly unacceptable.** We opted for non-upgradable contracts to maintain decentralization. Introducing breaking changes like this introduces significant uncertainty for developers and **promotes the use of centralized, upgradable contracts** in the Ethereum ecosystem.

---

**joeblogg801** (2023-06-12):

Could you kindly provide a link to the contract, if available?

---

**david** (2023-07-05):

Gas refunds for SELFDESTRUCT [were previously removed in EIP-3529](https://ethereum-magicians.org/t/eip-3529-reduction-in-refunds-alternative-to-eip-3298-and-3403-that-better-preserves-existing-clearing-incentives/6097).

However, in practice this makes ephemeral, counterfactual contracts infeasible (since there’s no gas saving to self-destructing the contract). [@geoknee](/u/geoknee) outlined some benefits of this pattern [in this post](https://ethereum-magicians.org/t/eip-3529-reduction-in-refunds-alternative-to-eip-3298-and-3403-that-better-preserves-existing-clearing-incentives/6097/8).

Given that this EIP explicitly maintains the functionality for SELFDESTRUCT when used in the same transaction as construction, would this be an appropriate time to re-introduce the gas refund for SELFDESTRUCT?

---

**shemnon** (2023-07-10):

Two updates are needed in the EIP.  Where it lands I care not, just that it lands.

1. Pre EIP you could vanish ether by self destructing to the same beneficiary.  Geth’s implementation) reverses this.  This can be argued from the text because there is no “set balance to 0” step for the case of a pre-existing contract.
2. Is account creation and contract creation the same event or two different events?  i.e. if I send ether to an address in one TX, then in another TX create a contract, and then SELFDESTRUCTS that account.  Should the account be deleted?  Geth goes one way and Besu currently goes another way.  Which way is correct?

Consider that the account is likely never an EOA (hash collision required) and even if a collision were found and the stub was left, it would have a non-zero nonce.

Hence it will not be an “empty” account and cleaned up automaticallt
3. Note that EIP-3607 checks codes, not zero nonces, for valid EOA transactions
4. If Step 2 were repeated then the nonce would continually increase.

My mild preference is for 1. to be a notation in the spec, saying that self-destruct to the operating address will leave the balance and will result in the account *not* being deleted, but what happens to the nonce and storage needs to be called out.

My preference for 2. is to spell it out.  It is easiest to say that contract creation and account creation are two separate steps and contracts are created via a contract create transaction, CREATE/CREATE2 and future CREATE style operations.  Existing pre-transaction and in-transaction account state is not considered, even if a non-zero nonce or contract storage were to somehow be part of the pre-exiting account (currently there is no way to induce this).

---

**0xTraub** (2023-07-31):

What is the consensus about using the `Create2`/`SelfDestruct` pattern in the future going forward? The EIP explicitly states that it is discouraged, but there are clear benefits to its use. As far as I am aware, there are no further reasons the `selfdestruct` opcode would be removed or modified in the future but we don’t want to utilize functionality that may be removed. Is this intended as a transitional EIP to ease the burden on protocols using it now or will this be an intended as a permanent fixture of the EVM?

---

**shemnon** (2023-08-21):

EIP-6049 is still in effect and discourages it’s use and indicates breaking changes are forthcoming.  I doubt this is the last breaking change and at one point I expect SELFDESTRUCT will no longer destroy contracts.

Apart from transient storage (which has a new facility in EIP-1153 in the TLOAD/TSTORE operations) what are the use cases for CREATE2/SEFDESTRUCT within the same transaction?

---

**0xTraub** (2023-08-24):

The main reasons for utilizing this pattern is that it creates extra security for the contract itself. Since no code exists between transactions an attacker would need to identify a vulnerability in the deployer contract as well as the implementation to be able to exfiltrate any funds. We’ve had several discussions on [erc-6551](/tag/erc-6551) about potential implementations involving what we call “ephemeral contracts” and come to the conclusion that it can be a useful design pattern for some cases. [@RobAnon](/u/robanon) can speak to the benefits of this pattern more as well.

---

**poojaranjan** (2023-08-25):

[PEEPanEIP #115: EIP-6780-SELFDESTRUCT only in same transaction with @gballet](https://youtu.be/s7fm6Zz_G0I)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/0a8ad919970c251a0645a54db5bc071b74d23d0f.jpeg)](https://www.youtube.com/watch?v=s7fm6Zz_G0I)

