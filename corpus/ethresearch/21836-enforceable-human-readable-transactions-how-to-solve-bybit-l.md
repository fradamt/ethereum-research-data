---
source: ethresearch
topic_id: 21836
title: "Enforceable Human-Readable Transactions: how to solve Bybit-like hacks"
author: GCdePaula
date: "2025-02-26"
category: Security
tags: []
url: https://ethresear.ch/t/enforceable-human-readable-transactions-how-to-solve-bybit-like-hacks/21836
views: 3295
likes: 34
posts_count: 53
---

# Enforceable Human-Readable Transactions: how to solve Bybit-like hacks

*Special thanks to [Augusto Teixeira](https://w3.impa.br/~augusto/) and [Pedro Argento](https://twitter.com/PedroArgento8) for reviewing this piece.*

# Introduction

Ethereum has just suffered the largest theft in cryptocurrency history. It was neither a protocol bug nor a smart contract flaw — everything was working as expected. It was neither a private key leak nor a wallet compromise. It was a social attack: hackers spoofed a front-end, tricking signers into inadvertently transferring $1.5 billion dollars to North Korea.

[![Even Dr Evil was surprised](https://ethresear.ch/uploads/default/original/3X/b/2/b23af2169fcffd61a9c10828a15d5b934f2298d0.png)Even Dr Evil was surprised564×398 184 KB](https://ethresear.ch/uploads/default/b23af2169fcffd61a9c10828a15d5b934f2298d0)

The main issue is that a transaction’s input data is a binary blob, displayed by wallets as an incomprehensible hexadecimal-encoded string. Interpreting this data requires not only that the user has context about the application and knowledge of its implementation but also substantial bit gymnastics, making the process essentially impossible.

In the Bybit hack, the input data was spoofed. Although the compromised front-end UI indicated that the transaction would execute the expected transfer, it instead stole all the funds. The wallet displayed the data correctly — it was the humans who couldn’t read it.

These signers were certainly experienced professionals with robust protective measures against such attacks. That they were fooled signals that Ethereum’s transaction signing process is currently broken. This is not a new assertion — these signing issues have been known for a while. If we don’t address this readability problem, I believe we will see more hacks like the Bybit incident in the future.

In this post, we outline a possible technique to address these issues. Rather than being a protocol-level solution, this approach operates at the application level and must be implemented individually by each application’s developers. We assume that while the front-end is untrusted, the wallet and smart contracts with which the user interacts are trusted.

# First attempt

EIP-712 introduced a new typed data signing standard that leverages Ethereum keys to generate signatures that are both machine-verifiable and human-readable. For more details on its design, see this [2018 thread](https://ethereum-magicians.org/t/eip-712-eth-signtypeddata-as-a-standard-for-machine-verifiable-and-human-readable-typed-data-signing/397).

One of the goals of EIP-712 is to transform the signing experience from one where users blindly approve transactions into one where they can clearly verify the details — turning the left-side experience into the right-side one:

[![EIP-712](https://ethresear.ch/uploads/default/optimized/3X/c/0/c06c8953dce788c4d7f056a8d3b60b0c85b37427_2_690x483.png)EIP-7121600×1121 212 KB](https://ethresear.ch/uploads/default/c06c8953dce788c4d7f056a8d3b60b0c85b37427)

This enables applications to define message schemas with fields that are understandable by humans — a significant improvement over blind signing. However, even with this improvement, the signing process can still be overwhelming. See the image below: it shows a hardware wallet asking the user to verify the 54th field while signing a Gnosis Safe transaction — and that’s not even the last one. No one is realistically going to verify every single field.

[![Too many...](https://ethresear.ch/uploads/default/optimized/3X/6/e/6e247dc813064867f69adf295b3afbf0d13ebb03_2_300x180.jpeg)Too many...1080×651 116 KB](https://ethresear.ch/uploads/default/6e247dc813064867f69adf295b3afbf0d13ebb03)

The consequence is effectively the same as blind signing, which ultimately caused the Bybit hack.

# Proposal

The key idea is to embed an *enforceable*, human-readable description within the signed message, thereby preventing users from inadvertently signing transactions with unwanted side effects. The goal is to achieve this enforceable description without incurring prohibitive data availability overhead.

Consider an application that uses EIP-712 messages as input. These messages may contain an excessive number of fields — some with arcane names and inscrutable hexadecimal-encoded binary data. Ultimately, an EIP-712 message is intended for programs, not humans. While users can’t be expected to understand the entire message, **the target application can understand it perfectly**.

For each application, it is therefore possible to implement a *pure function* that maps the human-unreadable message into a human-readable string. For example, while a Gnosis Safe transaction is internally represented as a cumbersome 54-item tuple — necessary for the application — it is far too detailed for a user. A well-designed *decoder* can transform this tuple into a description that is both more concise and more informative for humans. Because decoders are application-specific, each application must implement its own canonical decoder and integrate it into its smart contracts, making it accessible both externally and internally.

Finally, we extend the message schema by adding a new text field — the *description* — to store the human-readable output produced by a canonical decoder. This field is intended for humans, clearly describing in plain language what the transaction will do once executed.

The outline of the technique is as follows:

1. Before sending the EIP-712 message to the user’s wallet for signing, the UI queries the application’s canonical decoder and populates the description field with the corresponding human-readable string. Note: Since the UI is untrusted, it may potentially set the description incorrectly (e.g. the description says something innocuous, but the input data steals all the funds);
2. The wallet, which is trusted, receives the message for signing and displays both the incomprehensible input data and its human-readable description. The user reads the description and decides whether or not to sign the message;
3. The user signs the message, which includes both the incomprehensible input data and its alleged description;
4. The front-end compresses the message by removing the description field and submits the compressed message to Ethereum. (Alternatively, the front-end sends the message to a sequencer.) The key insight is that data availability for the human-readable description is unnecessary since the smart contract can recover it from the raw input data using the same decoder;
5. Finally, the application receives the signed message and uses its canonical decoder to recover the correct description for the message. It then verifies whether the pair message and signature is correct. If the description is incorrect, the signature verification will fail, and the application will refuse to process the transaction.

# Discussion

By signing both the message and its human-readable description, we can later verify that they match and reject any transaction where they do not. This creates a cryptographic guarantee that makes it impossible to spoof a transaction. Moreover, since the mapping from message to its description is implemented as a pure function, the description itself does not need to be included in data availability.

This technique is possible because it is specialized for each application. This specialization allows developers — whom we assume are trusted and who have deep knowledge of their own systems — to address the issue at the application level. As a result, no Ethereum protocol changes are required.

Although the approach does not incur extra data availability costs, it does introduce additional computational overhead per transaction. This overhead might be prohibitive for certain applications, particularly those on Layer 1. In contrast, L2s are a better fit given their greater blockspace — especially application-specific rollups, which offer even more blockspace per application. My intuition is that the extra processing cost will be minor, and certainly preferable to losing $1.5 billion.

One downside of this technique is that it requires two signatures: one for the application and another for Ethereum. In other words, the user must sign an EIP-712 message (including the human-readable description) and then sign a separate transaction to submit that message to Ethereum. The upcoming Pectra fork may help address this issue through account abstraction, allowing someone else to submit a transaction on the user’s behalf so that only one signature is needed by the user. Alternatively, in non-EVM rollups that could already use an EIP-712 message as their transaction schema, users would only need to sign once before sending the message to a sequencer. Finally, while string manipulation in Solidity can be quite cumbersome, rollups with more robust execution environments offer promising ways to mitigate this challenge.

We believe this technique is an excellent fit for implementation on a [Cartesi](https://cartesi.io) application-specific rollup. An application hosted on a Cartesi rollup benefits from dedicated blockspace. This extra blockspace helps mitigate the additional computational overhead introduced by our proposed technique. Additionally, a Cartesi rollup can already use EIP-712 messages as input, and string manipulation is much easier in this environment.

# Conclusion

By adopting this technique, applications eliminate the need for users to delegate trust to front-ends; the Bybit signers would have either seen a sketchy description and refuse to sign, or received an innocuous description that would ultimately be rejected by the application.

As Alfred North Whitehead observed, “civilization advances by extending the number of important operations which we can perform without thinking about them.” In this context, users no longer need to perform complex bit gymnastics or worry about the trustworthiness of front-ends. Instead, they can benefit from what Josh Stark describes as a [hard cast](https://stark.mirror.xyz/n2UpRqwdf7yjuiPKVICPpGoUNeDhlWxGqjulrlpyYi0).

## Replies

**MicahZoltu** (2025-02-26):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/719)












####



        opened 04:18AM - 22 Sep 17 UTC



          closed 12:43AM - 16 Jan 22 UTC



        [![](https://ethresear.ch/uploads/default/original/3X/e/3/e3b30557f41e276cc8ef99a9213ef76c045762a8.png)
          MicahZoltu](https://github.com/MicahZoltu)





          stale







A lot of debate has been happening around how we can make signing a more secure […]()process for end users.  One of the common arguments is that while all of the proposed solutions may resolve the problem for advanced users (developers, tech savvy users, professionals, etc.) it doesn't address the problem of naive users not understanding what they are signing.  They can often be thought of as the legalese presented to people in contracts: it is better than signing a blank sheet of paper, but to the average person its mostly gibberish.

An idea that @Arachnid and I started batting around in an attempt to come up with a long-term solution to this problem is to provide a mechanism by which things can be signed (ideally transactions and arbitrary messages) such that signer can present the user with informed consent without having to trust the UI.

The general premise is that the actor wanting a signature presents the signing tool with the data they want signed as well as a DSL that describes how the data should be presented to the user.  The signer would then ask the target contract if the DSL is valid, and only prompt the user to sign if the contract asserts that the DSL is in fact valid.

This is quite similar to #712, though it strives to take things a step further than just function name and parameters.

As far as the DSL itself goes, one option would be a text-only DSL that allows for replacement variables.  An example DSL may be something like
```
I would like to create an order offering ${data[0,64] as number} ${(data[64,64] as contract).name()} tokens in exchange for ${data[128,64] as number} ${(data[192,64] as contract).name()} tokens.
```
An untrusted dApp would send that DSL (exactly) to the signer along with the transaction they want signed.  The signer would then ask the `transaction.to` contract whether the hash of the DSL is an approved DSL.  If it is, then the signer would extract data from the `transaction.data` and do an `eth_call` to fetch the `name()` of the two contracts (tokens in this example) and finally generate the string to present to the user.  This solution is very simple and allows for devices with small screens that can only present text (e.g., Ledger) to be able to reasonably present the user with information that the contract author has deemed as enough for informed consent.

Another more feature rich solution (in the extreme) would be to allow the DSL to be some form of constrained layout engine markup (e.g., HTML).  The idea here would be that the signer could verify the DSL was approved just like with the text DSL, but would be able to use a basic UI to present the data to the user like the 0x OTC dApp:
![image](https://user-images.githubusercontent.com/886059/30728433-077329da-9f0d-11e7-80f4-e201230bfd44.png)

For complex contracts, a full UI is much more understandable to an end user than a paragraph or two of madlibs text, and it gives the dApp developer the ability to create a generally better user experience.

The obvious disadvantage to the full GUI DSL is that it can't reasonably be rendered on a text-only display like a watch or hardware key.  With the way this is proposed, a contract could support multiple DSLs so a well written contract may support both text only DSL (for small screens and screen readers) and also a GUI DSL for a better user experience for most users.  This would allow dApp developers to provide high quality signing experiences to users on devices that support it with graceful degradation on devices that don't.  It also allows signers to implement the presumably easier-to-implement madlibs spec fist, then expand towards the full GUI support implementation later.

Open Questions:
* What is does the madlibs DSL look like?
* What does the GUI DSL look like?
* Are the benefits of a GUI DSL over a madlibs DSL worth the additional implementation costs on signing tools?
* Are there existing DSLs that would give us broad support out of the box (e.g., HTML)?
* What datatypes should the signing UI DSL support?
  * timestamp: could present users with a date/time picker on click
  * counter: could have an up-down clicker
  * range: could have a range slider with tick DSL defined tick size
  * others?












If the DSL hash is signed over (function parameter), then a fully offline hardware wallet can trustlessly present the human readable transaction to you.

---

**GCdePaula** (2025-02-26):

Wow, a lot of similarities! Thank you for sharing this. I think the key takeaways are the same: have the user sign both the unreadable input data and some sort of readable description, that can later be enforced to match onchain.

A cool insight is that there’s no need to give data availability on the description, since it can be recovered during onchain verification.

To split hairs, I’ll list a few differences between your DSL approach (using the offline thing) and the approach described in the OP.

The DSL approach is easier on onchain compute since the smart contracts don’t need to eval the DSL, only the wallet. This is in contrast with the OP that has this added compute cost of reconstructing the description onchain.

The OP approach does not require wallets to implement anything (besides EIP-712), nor any sort of standardization. It’s an application-side technique that could be implemented today.

---

How do you see these techniques today, and their possible adoption?

---

**MicahZoltu** (2025-02-27):

IIUC, the fundamental difference between the two approaches is summarized as follows?

> Contract receives signed hash of the evaluated DSL and internally evaluates the DSL and compares the hash.  Signing tool doesn’t need to evaluate the DSL (UI can).

vs

> Contract receives signed hash of the un-evaluated DSL and compares it against known good un-evaluated DSLs.  Signing tool needs to evaluate the DSL.

If so, the question is whether we want the DSL evaluation to occur in the contract (high replication factor makes computation a scarce resource), or do we want the DSL evaluation to occur in the signing tool (small form factor makes computation a scarce resource).

I think I lean towards having the logic live on the signing tool, rather than the hardware device because I suspect that in most cases the DSL can be simple enough that any device can evaluate it pretty reasonably.  Contract authors can also be encouraged to provide both “simple” and “advanced” DSLs where the simple one is easier to evaluate on a device while the advanced one has more details but is perhaps more computationally expensive to evaluate.  This could be on top of having both a graphical and a textual representation.

---

One other pretty major difference between the proposed solutions I suppose is that the DSL doesn’t need to be shared between contracts with your proposal, but with 719 everything must use the same DSL.  This is a pretty massive advantage and may swing me towards your proposal.  ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

---

**GCdePaula** (2025-02-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> IIUC, the fundamental difference between the two approaches is summarized as follows?

At a high level, I believe so! But there are some interesting details to expand on.

On my proposal there’s no need of a DSL exactly. The smart contract can use its own turing-complete language to build the description. Think of a read method (e.g. `eth_call`), implemented as a pure function, that receives the transaction itself and returns a description. It might be convenient to have a DSL, but it’s not necessary.

Furthermore, if the contract receives the message and its signature (say, a rollup receiving a list of EIP-712 messages plus signature), I believe we can even omit the “hash of the evaluated DSL”, because the smart contract can recover this hash. Let me give more details. Consider that the user signs the tuple (message, alleged description). They can omit the description, submitting to the blockchain the tuple (signature, message). The smart contract finally recovers the *correct* description, rebuilds the tuple (message, description), and verifies whether the signature matches.

But at a high level, I believe the differences you listed are correct, and the rest is implementation details.

---

I think another consideration is where these techniques would be used. In L1, I believe the added costs of my proposal may be prohibitive. I believe 719 has this advantage. But in L2/L3, specially app-specific ones (since the application has the entire blockspace for itself), the added cost could be minor.

---

**MicahZoltu** (2025-02-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/gcdepaula/48/19223_2.png) GCdePaula:

> Furthermore, if the contract receives the message and its signature (say, a rollup receiving a list of EIP-712 messages plus signature), I believe we can even omit the “hash of the evaluated DSL”, because the smart contract can recover this hash. Let me give more details. Consider that the user signs the tuple (message, alleged description). They can omit the description, submitting to the blockchain the tuple (signature, message). The smart contract finally recovers the correct description, rebuilds the tuple (message, description), and verifies whether the signature matches.

Unless I’m misunderstanding, I don’t think this is the case.  The contract needs the signature to be over either the description provided to the user, the DSL used to generate the description provided to the user, or the hash of either.  If you only sign over method + parameters, the contract has no way of knowing what human readable thing was presented to the user to sign.

---

**GCdePaula** (2025-02-27):

Yes, you are correct. The user needs to sign the (hash of the) description or evaluated DSL. But once signed, I believe it is possible, as an optimization, to compress the transaction by removing this description or evaluated DSL, because it can be recovered by the smart contract.

---

**MicahZoltu** (2025-02-27):

Ah, I see what you are saying.  Clever.  This assumes that there is only one canonical representation that is signed over though, it doesn’t work if there are multiple possible representations (e.g., a graphical presentation and a textual presentation, or presentation in multiple languages, etc.).  Is there any benefit to standardizing how such metadata is provided by the signer, or should that just be left up to the app?

---

**GCdePaula** (2025-02-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Is there any benefit to standardizing how such metadata is provided by the signer, or should that just be left up to the app?

That’s a good question, I’m not sure ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

I think what could end up happening is that, if this idea gains traction, tools and libraries will begin to emerge and be adopted by apps, and these in a way become multiple *de facto* standards.

Maybe tooling is better than standards. I don’t know.

---

**Phle-bas** (2025-03-01):

But how can this really be secure if you assume the developers of the contract are trusted? If hackers can create a malicious contract with the same description as the legitimate one, how will the user notice this in their hardware wallet?

---

**MicahZoltu** (2025-03-02):

Contracts can only modify their own state and call out to other contracts as themselves.  They cannot take any actions on behalf of the user.  This means that a malicious contract can only be malicious regarding its own state.

Of course, this doesn’t solve the scam problem where someone convinces a user to give them their money, but you don’t even need a contract for that as it is entirely social engineering.

---

**Phle-bas** (2025-03-02):

Yes, this proposal solves some issues, but trusting a developer-assigned description at the application level with $1.5 billion still seems unwise. Social engineering attacks and hacks at the application level remain an ongoing concern. This needs to be implemented at the protocol level, just like in Bitcoin—the only layer you can truly trust. Preferably, it should be even more secure than Bitcoin, but at the very least, it should have multisig, which is the bare minimum.

---

**MicahZoltu** (2025-03-02):

Users already need to trust the contracts they are interacting with.  This trust is scoped only to the contract and any assets you give to the contract.  Something like proposed here gives contract developers a way to make it so users can know what sort of interaction they are about to take with the contract without needing the user to trust the web application they are interacting with.

---

**Phle-bas** (2025-03-03):

Well, not by choice, users are **forced to trust** these SAFE contracts because EOAs do not support multisig.

ETH is money, whether it likes it or not. It shouldn’t rely on external contracts for core functionality. Ethereum needs to step up its game and make security a first-class citizen. What good is this entire blockchain concept, with billions staked to protect Ethereum and multiple implementations in different programming languages, if a simple transfer of funds ultimately depends on the security of an external contract and its developer?

This is an existential risk, and some developer-assigned description field isn’t going to be enough to stop these Bybit-like hacks. The attack surface needs to be reduced, not increased.

---

**GCdePaula** (2025-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/phle-bas/48/19296_2.png) Phle-bas:

> forced to trust

Not really, they chose to (i) use a multisig and (ii) use that specific implementation of it, but this is besides the point — as far as I know, no smart contract nor wallet were hacked. It was a front-end hack, which is exactly what this proposal (and previous similar proposals) solve.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/phle-bas/48/19296_2.png) Phle-bas:

> some developer-assigned description field isn’t going to be enough to stop these Bybit-like hacks

I believe this specific proposal would solve this specific hack, yes. It seems you disagree with this point, can you elaborate?

---

![](https://ethresear.ch/user_avatar/ethresear.ch/phle-bas/48/19296_2.png) Phle-bas:

> The attack surface needs to be reduced, not increased.

Delegation of trust needs to be reduced, I agree. This proposal greatly reduces the need to trust front ends.

---

**Phle-bas** (2025-03-05):

Some final thoughts:

They can choose different implementations, but this is not a benefit since all are contracts and inherit the same issues. Yes, they can add external security measures and stick with EOA for now, but I wouldn’t recommend that either. Ethereum is pushing the responsibility for secure fund transfers onto the user. There are no good choices if you simply want to make a secure fund transfer on Ethereum. I just hope the next hack isn’t one of those ETFs.

This description field actually increases the attack surface because it can also be exploited and makes maintaining the code even more complicated. It’s not a bad idea, but I wouldn’t trust it with $1.5 billion.  It may have stopped this specific hack, but it could cause the next one.

Security Concerns:

- False Sense of Security: Fake or buggy contracts can more easily trick users if they rely only on the description.
- Hidden External Calls: Complex contracts frequently call other contracts; an innocent-sounding summary can ignore those calls, leading to unexpected fund flows.
- Over-Simplification: A short description can’t capture every detail of Turing-complete code. Attackers exploit blind spots and edge cases.
- Translation Traps: How will you handle translations into different languages? Translation errors/hacks could mislead users.

---

**GCdePaula** (2025-03-05):

There’s no technology (that I know of) that can protect users that signed something they shouldn’t have.

The GPTfied security concerns make no sense, sorry. (Except the last item about translation, which is fair, but isn’t sufficient to make the idea unsuitable.)

---

**MicahZoltu** (2025-03-06):

I think you may not fully understand how the EVM works.  I have tried to help clarify some pieces below.

![](https://ethresear.ch/user_avatar/ethresear.ch/phle-bas/48/19296_2.png) Phle-bas:

> False Sense of Security: Fake or buggy contracts can more easily trick users if they rely only on the description.
>
>
>
>
> Hidden External Calls: Complex contracts frequently call other contracts; an innocent-sounding summary can ignore those calls, leading to unexpected fund flows.

A contract can only modify its own state.  If you sign a transaction that interacts with some contract, it cannot take actions on another contract on your behalf.

![](https://ethresear.ch/user_avatar/ethresear.ch/phle-bas/48/19296_2.png) Phle-bas:

> Over-Simplification: A short description can’t capture every detail of Turing-complete code. Attackers exploit blind spots and edge cases.

The goal is for the contract you are interacting with to be able to express a human language summary of what is happening to the user.  It is not meant to give an explicit specification, that requires audits and whatnot which is a separate problem (what the contract actually does vs what the contract is supposed to do).

![](https://ethresear.ch/user_avatar/ethresear.ch/phle-bas/48/19296_2.png) Phle-bas:

> Translation Traps: How will you handle translations into different languages? Translation errors/hacks could mislead users.

The solution proposed in this thread would allow a developer to support descriptions in multiple languages if they wanted.  Depending on the device rendering the transaction description, you may also be able to handle translation there instead.

---

**Phle-bas** (2025-03-07):

Ok, you lured me back by accusing me of not knowing how EVM works—that wasn’t very nice ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Why would it be impossible to trick users into opening a fake SAFE account by hacking the SAFE website? The description field would make the fake more convincing than it would be without it.

You suggest description translations on device? Why do you need a description field then? Might as well translate EIP 712 call data into a nice description on the Ledger device. In fact, I don’t understand why they don’t do this, especially with newer devices with more processing power.

I really hope you’re not suggesting implementing a website to handle the translations, like they do with SAFE for verifying transactions. That was—and still is—a crazy idea. But probably, because SAFE is actively promoted by Vitalik, the CEO of a huge exchange felt comfortable doing so.

---

**MicahZoltu** (2025-03-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/phle-bas/48/19296_2.png) Phle-bas:

> Why would it be impossible to trick users into opening a fake SAFE account by hacking the SAFE website?

If you can trick someone into sending all of their assets to a malicious address, then you have already won.  What is being proposed here does not try to solve that attack generally, it just tries to solve the subset of that attack where they trick you into interacting with a *trusted* contract in a way that results in you unintentionally sending away your assets.  This could be tricking you into signing the wrong SAFE transaction, or signing a Uniswap swap & send transaction with them as the recipient.  In both cases, you are interacting with a contract that you trust, but in a way that you do not intend.

![](https://ethresear.ch/user_avatar/ethresear.ch/phle-bas/48/19296_2.png) Phle-bas:

> You suggest description translations on device? Why do you need a description field then? Might as well translate EIP 712 call data into a nice description on the Ledger device. In fact, I don’t understand why they don’t do this, especially with newer devices with more processing power.

Translation on device only works for high power devices.  Good translation tools these days are generally LLMs, and while we can run small translation models on mobile devices these days, you definitely cannot run it on a Ledger (I doubt it is even theoretically possible).  Also, translating between languages is a possible problem, while turning an EIP-712 call into a description of what the function *does* is impossible (there isn’t enough information present in the call details).  For example, knowing what `foo(uint256 x, uint256 y) returns uint256` does is impossible.  It could add two numbers, it could multiply them, it could initiate a swap of two hard coded assets, etc.  You can try to use the function name to *guess* what a function does, but even then translating `swap(uint256 x, uint256 y)` into human language isn’t possible because you still don’t know if it swaps X => Y or Y => X or if it has side effects.  Also keep in mind that most transactions are not EIP-712 signatures, and signature 4-bytes are incredibly lossy.

---

**Phle-bas** (2025-03-08):

1° That was not my point. My point was that creating a malicious contract that a user might trust is now easier than before with your description. Since the description would be correct, the underlying code could, of course, do something else.

2° I looked it up, and Ledger actually has such a system already. They call it clear signing with EIP-712. It works similarly to what I suggested—no guesswork needed. However, I think they use a central database to query on the fly to save space on the device. If they stored it entirely on the device for some high-stakes contracts, it could work fine along with some contract address whitelisting, even with the correct translation for the user.

www ledger com / blog / securing-message-signing

Probably, the lack of standards, frequent upgrades, and extensibility for these existential use cases has prevented hardware manufacturers from implementing this correctly. Which was my point all along—if you read my previous posts—that these existential use cases should be standardized.


*(32 more replies not shown)*
