---
source: ethresearch
topic_id: 21982
title: Enforceable Descriptive Operation Layer (against Bybit-like hacks)
author: Zergity
date: "2025-03-18"
category: Security
tags: []
url: https://ethresear.ch/t/enforceable-descriptive-operation-layer-against-bybit-like-hacks/21982
views: 300
likes: 3
posts_count: 12
---

# Enforceable Descriptive Operation Layer (against Bybit-like hacks)

*Special thanks to [@GCdePaula](/u/gcdepaula) and [@MicahZoltu](/u/micahzoltu) for preliminary feedback, suggestions, and reviewing this piece.*

I recently read [Enforceable Human-Readable Transactions](https://ethresear.ch/t/enforceable-human-readable-transactions-how-to-solve-bybit-like-hacks/21836) by [@GCdePaula](/u/gcdepaula) and [Trustless Signing UI Protocol](https://github.com/ethereum/EIPs/issues/719) by [@MicahZoltu](/u/micahzoltu), both of which aim to improve the transaction signing user experience (UX) to prevent phishing and malicious backdoor contracts. These approaches effectively secure the input that users sign, but I believe something important is missing. Shouldn’t we also secure the output or effects of the transaction?

While input is hard to trust and even harder to verify, we can more reliably verify the transaction outputs (or effects) like which storage will be changed, which external contract will be called. We can even map each operation to human-readable forms (with different levels of attention) to be displayed on low power devices, like:

- (DANGER!!!) DELEGATE CALL to 0x123…234 with data 0x…
- (CAREFUL) Upgrade this contract to new implementation at 0x123..456.
- (WHAT?) Revoke ownership of 0x234…567.
- Transfer 123 WETH to someone.eth.
- Swap at most 234 USDC for at least 0.01 WETH on Uniswap Pool (0x…).

The goals of this proposal are:

- no chain hard fork, no EVM upgrade required
- works on low-power signing devices
- supports both EIP-712 clear messages and direct function data

[![image](https://ethresear.ch/uploads/default/original/3X/0/e/0e3872a601bca6ab678a49d708e61003efea27f8.png)image1061×751 24.7 KB](https://ethresear.ch/uploads/default/0e3872a601bca6ab678a49d708e61003efea27f8)

By creating an Enforceable Descriptive Operation (EDO) layer, the application contract can have critical operations to clearly signed with descriptive forms. These descriptive data can be displayed effortlessly in low-power devices, and generated/verified by EDO code.

The opDesc is generated from the opData deterministically by the EDO code, and can be simulated by the FE (untrusted) manually or by static calling the contract. The FEs don’t need to be trusted, they can be phishing sites.

The human-readable opDesc texts are displayed in the singing devices, to describe each and every critical operation that can happen in the transaction. Any malicious or ambiguous operation will stand out on the signing device screen.

The EDO code will verify the signed opDesc and opData and record them in transient storage. All registered opData registered can be executed by the transaction and only in that transaction. Any operation request outside the registered opData will revert the transaction, prevent malicious call injections.

How does this fare against front-end phishing attacks like Bybit’s?

## Replies

**MicahZoltu** (2025-03-18):

Are both `opDesc[], opData[]` parameters to the function being called (and thus signed over)?

---

**Zergity** (2025-03-18):

Yes, both of them shoud be tied to a function call.

---

**MicahZoltu** (2025-03-18):

So the idea here is that `string[] opDesc, bytes[] opData` (recommend `{string, bytes}[] operation` instead) parameter can be composed into a set of human readable statements by the signing device, and then the contract validates that the descriptions and the data are all valid and match the function being called?

---

**Zergity** (2025-03-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> validates that the descriptions and the data are all valid and match the function being called?

The EDO code validates each signed opData and its opDesc. And make sure only those signed operations are allowed to execute in the transaction. Any other operation requested will revert the tx.

---

**MicahZoltu** (2025-03-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/zergity/48/5716_2.png) Zergity:

> The EDO code validates each signed opData and its opDesc. And make sure only those signed operations are allowed to execute in the transaction. Any other operation requested will revert the tx.

This is not enforceable by anything nor does the protocol care about it.  Implementations could certainly do that, but for the purpose of making a standard what matters (IIUC your proposal correctly) is that there is a well defined data structure as the last parameter of the function, and the signing library should follow a standard mechanism for turning that datastructure into human readable statements that are presented to the user prior to signing.

I think this is similar to what was proposed by [@GCdePaula](/u/gcdepaula), except in theirs all that is passed to the contract is a hash, and the signing tool doesn’t need to know how to construct the human readable string (only how to hash and compare it).

---

**MicahZoltu** (2025-03-18):

If I am understanding your proposal correctly, a contract could implement the EDO internally with [@GCdePaula](/u/gcdepaula)’s implementation, but there is less presentation flexibility on the signer’s part compared to what you have proposed here.

---

**Zergity** (2025-03-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If I am understanding your proposal correctly, a contract could implement the EDO internally with @GCdePaula’s implementation, but there is less presentation flexibility on the signer’s part compared to what you have proposed here.

It’s the reverse, to be precise.

GCdePaula’s proposal maps each function input to a description and verifies it on function input. So if there are 20 functions, there should be 20 or more descriptions.

This proposal maps each critical operation to its own description and makes sure only those operations can happen in a transaction. So there could be 20 functions, but if the application only needs to enforce a specific storage change, the EDO only needs to map that storage change to a description and ignore the rest. If a function triggers multiple enforced operations, the signing device would need to display and sign all of the descriptions.

This is enforceable in the sense that, if implemented by the application, the front-end or clients must provide the correct descriptive texts for each transaction; otherwise, the function will revert. For the signing device, there are ways to recognize a contract function implementing this by: (1) assigning a special field in the EIP-712 request, and (2) creating a formal standard for function parameters where the descriptive texts can be easily decoded without the function ABI.

---

**MicahZoltu** (2025-03-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/zergity/48/5716_2.png) Zergity:

> This proposal maps each critical operation to its own description and makes sure only those operations can happen in a transaction.

What you are describing is a choice that someone could make when implementing either standard, but it isn’t a requirement or enforced by the standard at all.  All the protocol *actually* requires is that the signer renders and presents the data present in the last `operation` parameter(s) to the user, and the contract verifies (however it wants) that the data in the `operation` parameters is appropriate for the contract call being made.  The standard has no say over what exactly the contract does to validate the provided data, it can only assert that the data was presented to the user according to some presentation protocol.

You can certainly suggest a particular strategy for encoding/presenting data and encourage people to follow it, but people don’t have to follow that part in order to leverage the protocol.

Similarly, people could follow your proposed strategy for contract-side validation when receiving just a hash like GCdePaula proposed.

---

**Zergity** (2025-03-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> What you are describing is a choice that someone could make when implementing either standard, but it isn’t a requirement or enforced by the standard at all.

This choice alone can help mitigate different kinds of phishing attacks, which the application’s devs have a strong incentive to do.

Without a new transaction type or some kind of collective storage management contract, do you have any idea to make it more strictly enforced?

---

**MicahZoltu** (2025-03-21):

I’m notoriously against trying to standardize Good Ideas.  One should create standards where you have a many-to-many interoperability concern that needs to be addressed, but we should not try to create standards that don’t involve interoperability between participants.

In this case, what you are proposing is a Good Idea, but the only part that needs to be standardized is how the signing tool can sign over some human presentable information that is validated by the contract.  Your proposal is one way to achieve that (descriptions + data as last parameter(s)), and a hash of the human readable string is another way to achieve that.

---

**Zergity** (2025-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> In this case, what you are proposing is a Good Idea, but the only part that needs to be standardized is how the signing tool can sign over some human presentable information that is validated by the contract.  Your proposal is one way to achieve that (descriptions + data as last parameter(s)), and a hash of the human readable string is another way to achieve that.

Agree. I wasn’t trying to create a protocol or standard yet; those require a lot of ideas and designs to be battle-tested in the real world first. I was trying to first find a direction for us to discuss.

The deeper issue is that Ethereum (and others) lack certainty for the signer, as they often have to rely on the transaction constructor (front-end), which can easily malfunction or be malicious. If a signer can approve “what can happen in my transaction” instead of “what someone tells me they will do,” a lot of risks can be avoided.

In a perfect world, this should happen at the protocol level — for example, by enforcing a list of EVM logs that can be written in the transaction. Until then, one possibility is a collective storage and operation manager contract (like a single EDO contract shared by all applications), similar to how Permit2 lets users sign an approval of “what can happen to my tokens.”

I’m consulting for a project that uses AI to build transactions from user prompts, which is wildly dangerous — mixing a highly unreliable transaction constructor with a non-descriptive signing system. I believe a robust descriptive-signing process would benefit everyone.

