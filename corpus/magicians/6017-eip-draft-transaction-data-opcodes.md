---
source: magicians
topic_id: 6017
title: "EIP Draft: Transaction Data Opcodes"
author: alex-ppg
date: "2021-04-16"
category: EIPs
tags: [evm, opcodes, core-eips]
url: https://ethereum-magicians.org/t/eip-draft-transaction-data-opcodes/6017
views: 2757
likes: 5
posts_count: 15
---

# EIP Draft: Transaction Data Opcodes

Hello everyone,

Given the inclusion ever-growing for smart contracts to be inter-connected, I wanted to come up with an idea to aid developers in building “smarter” multi-contract systems by being able to apply introspection to the entrypoint of a blockchain transaction.

I have already filled out the necessary EIP data under my fork, however, before submitting a formal PR I would like to get validation on whether this is something that the community feels would be useful. I have briefly voiced the idea in Ethereum security channels with positive feedback, hence the conception of the EIP.

Put briefly, I have introduced four EVM instructions that permit introspection to be applied to the original transaction data by being able to access the original `data` payload as well as the original recipient of the transaction, the `to` address. This would primarily allow more complex types of “basic” contracts to be created, such as ERC-20 tokens that are aware of exactly what type of action (i.e. “buy” or “sell”) is performed on a DEX like Uniswap.

As a side-effect, it would counter-act the breaking change of EIP-3074 with regards to the `ORIGIN` opcode by allowing a more granular level of introspection to be performed on the original transaction context, i.e. in pseudo-code the `ORIGIN() == CALLER()` can be replaced by `ADDRESS() == ENTRYPOINT()`.

Let me know your thoughts.

EDIT: This EIP has been split into two separate ones given that the optimizational benefit of the `ORIGINDATA*` opcodes was properly argued. The main point of the EIP is to provide an optimized way of transmission for large data payloads rather than introspection; that purpose is suited for the new EIP 3520.

## Replies

**matt** (2021-04-16):

Nice, thanks for writing this. Do you have a PR against the EIP repo I can review?

---

**alex-ppg** (2021-04-16):

Hello Matt, I haven’t performed a PR yet as the EIP guidelines state that some community validation should happen on this forum first, I thought it would be wise to do that after getting a few comments here.

---

**matt** (2021-04-16):

Thank you following the EIP guidelines, not many people seek community validation first ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) I will say that I am confident this has enough interest to go ahead and make a draft. I am aware that Optimism relies on `msg.sender == tx.origin` so have tx data opcodes would likely be preferable to them.

---

**alex-ppg** (2021-04-16):

Thanks for the feedback, I will also edit the original post as `ADDRESS() == ENTRYPOINT()` alone should be sufficient to guarantee `ORIGIN() == CALLER()`. Here’s the PR: [Transaction Data Opcodes EIP Inclusion by alex-ppg · Pull Request #3508 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/3508)

I believe I selected the wrong PR type though and it should have been a draft PR?

---

**MicahZoltu** (2021-04-17):

Contracts should not be discriminating by caller as that leads to certain classes of wallets, particularly high security wallets like multisigs, timed recovery wallets, social recovery wallets, etc. being unable to interact with applications on Ethereum.  This leads to poor operation security for users because they now have to choose between “have an enhanced security wallet” and “be able to use dapps” (and most choose the option of “use more dapps”).

Because of this, I’m fairly strongly against any change that enshrines the ability to discriminate by caller and I am fairly strongly in favor of any change that breaks contract ability to discriminate by caller.  Contracts that need discrimination should find alternative solutions to their problems, rather than discrimination.

---

**alex-ppg** (2021-04-17):

Hey Micah,

Thanks a lot for the feedback. The EIP’s **main purpose is not to discriminate callers**, it is to provide **a new way of introspection** for transactions. The `ENTRYPOINT` instruction is **necessary** because without it, the input signature and arguments can easily be spoofed by a malicious contract.

Implementation wise, I do not believe it is possible to restrict what the community wants to do. They can already prohibit such wallets by evaluating the `extcodehash` of an address (note: this will not prevent malicious contracts, only wallets that have already been deployed).

Ultimately, I think the benefit of such introspection outweighs the potential of one or two projects producing an ill-advised implementation which they can already apply using the aforementioned check, unless the intention is to strip that ability entirely.

I would like to stress this again, **caller discrimination is not the main point of the EIP** and is a side-effect of `ENTRYPOINT`, however, I do not believe there is any non-spoof-able way to associate the `to` address of a transaction with the original `data` argument. Ofcourse, this is completely up to debate.

---

**MicahZoltu** (2021-04-17):

What is the use case you envision where you want to do introspection of the initial call frame and you *don’t* want to use that information to discriminate by caller (EOA vs contract caller)?

---

**MicahZoltu** (2021-04-17):

It is also worth noting that EOA vs Contract caller discrimination is only possible with `require(msg.sender == tx.origin)`, which will probably break with EIP-3074.  So if that lands, discrimination will not be possible and this will be *introducing* discrimination back into the system.

---

**alex-ppg** (2021-04-17):

A real-world use case here would be the FEI protocol which wants to identify whether a sell or a buy occured via the Uniswap Router. Although it does indirectly discriminate callers, its actual purpose is to accurately track a buy vs a sell order on a DeFi exchange. In general, this would open up new pathways of introspection whereby an intermediate asset (i.e. an ERC20 token) can detect as which part of an overall system workflow it is being transacted for and perform smart actions.

---

**alex-ppg** (2021-04-17):

As I stressed earlier, the discrimination introduced is a *side-effect*. I am very open to other ideas to tackle `tx.data` association with `tx.to` without relying on an opcode that makes the `to` address of a transaction available.

---

**MicahZoltu** (2021-04-17):

IIUC, you want path dependent code in your ERC20 contract so you can have behavior that discriminates on the call path that lead up to the transfer?  In the example case, if your token’s transfer function is called by a contract you are familiar with, you want to know what function is calling you, or possibly what function called that function.  You are saying that you can *derive* that information for the case of an EOA calling into a well known code path because you can deduce from the calldata what the call path looks like?

---

**alex-ppg** (2021-04-17):

Exactly, this can open up quite a lot of new ways to interface with existing smart contract systems especially in the DeFi ecosystem. This is not something I am personally developing on, but I can see the potential it can bring. The `ENTRYPOINT` instruction did not even exist in the first version of the EIP I ideated, it came to be as a solution to the inherent insecurity that solely relying on `ORIGINDATA` can cause as it can easily be spoofed by first interacting with a malicious contract.

---

**fedealconada** (2022-06-13):

Just sharing [this](https://ethresear.ch/t/access-to-calldata-of-non-current-call-frames-and-alternative-methods-of-token-use-authorization/11962/4) interesting post from ethresear.ch which is related to this EIP.

---

**alex-ppg** (2022-06-13):

Thanks for sharing that! I will reach out to the author of that post in case they wish to take up the 3508 & 3520 EIPs and move them forward with me. Regrettably, these EIPs are something I did not focus on due to lack of time but if there is interest I will pursue them more ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

