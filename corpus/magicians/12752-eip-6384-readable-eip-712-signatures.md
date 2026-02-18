---
source: magicians
topic_id: 12752
title: "EIP-6384: Readable EIP-712 signatures"
author: talbeerysec
date: "2023-01-30"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-6384-readable-eip-712-signatures/12752
views: 4396
likes: 16
posts_count: 33
---

# EIP-6384: Readable EIP-712 signatures

The use case of Web3 off-chain signatures intended to be used within on-chain transaction is gaining traction and being used in multiple leading protocols (e.g. OpenSea) and standards (EIP-2612), mainly as it offers a fee-less experience. Attackers are known to actively and successfully abuse such off-chain signatures, leveraging the fact that users are blindly signing off-chain messages, since they are not humanly readable.

The idea: EIP-712 already formally binds an off-chain signature to a contract, with the “verifyingContract” parameter. We suggest adding a “view” function (“stateMutability”:“view”) to such contracts, that returns a human readable description of the meaning of this specific off-chain buffer.

We are looking to get feedback from the community and especially from Smart Contract implementors, Wallets developers and security practitioners.

## Replies

**SamWilsn** (2023-01-30):

Some non-editorial comments (meaning you’re free to ignore them and your PR will still be merged):

- I’m really not in love with the name evalEIP712Buffer. To me, “eval” implies “evaluate” which is exactly what this function doesn’t do. Maybe something like describeEIP712, or descriptionOf?
- How does this differentiate between two or more functions on the same contract that accept an EIP-712 signature? Imagine an ERC721 token with a permit function (for approval), and a gaslessMint function (so the buyer pays gas fees.)
- Should this interface be exposed with EIP-165?
- What should the implementing contract do if it doesn’t understand the signature? Revert?
- I assume there’s some way to tell if the contract doesn’t implement this EIP? Probably just try to call the function. What if there’s a selector id collision?

---

**talbeerysec** (2023-01-31):

- Good suggestion per name. Let’s leave it open for a period, to collect other people ideas on best name.
- differentiation of two or more functions on the same contract that accept an EIP-712 signature is done by using the primaryType parameter that is passed to the function
- Seems like a good suggestion. we will update the EIP to reflect it
- reverting makes sense. we will update the EIP to reflect it
- We will use EIP-165 as suggested

---

**SamWilsn** (2023-01-31):

As part of our process to encourage peer review, we assign a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@mayowa](/u/mayowa)! Please note that this review **is NOT required** to move your EIP through the process. When you—the authors—feel ready, just open a pull request.

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@mayowa](/u/mayowa) please take a look through [EIP-6384](https://eips.ethereum.org/EIPS/eip-6384) and comment here with any feedback or questions. Thanks!

---

**thebensams** (2023-02-02):

I think it would be a good idea to implement this as an EIP-712 extension where the “localization contract” can be specified explicitly. When the frontend calls `eth_signTypedData`, the address to the localization contract is passed explicitly as an `additionalProperty`, ie:

```auto
[...]
additionalProperties: [
    {
    "name": "EIP-6384-Localization",
    "type": "address",
    "value": "0xdeadbeef"
    }
]
[...]
```

This would benefit the proposal in two ways;

1. The wallet software can determine whether the request is EIP-6384 without sending an RPC request/EIP-165
2. The logic for localization won’t have to live in the same contract as the verifier address. I suspect a lot of protocols would want to update their localization without having to update a core contract or add localization logic to dozens of EIP-6384-compliant contracts. I suspect most implementations would just proxy evalEIP712Buffer requests to a single contract, so using additionalProperty will simplify things for implementers.

---

**talbeerysec** (2023-02-03):

This an option we had considered. But we were worried extending EIP-712 will cause backward compatibility issues in all parties that used to get the older version of EIP-712.

Changing the EIP-712 format will require changing the current `verifyingContract`, as the signature verification will change.

Having said that, your point #1 is definitely an advantage. We are pragmatic and very open to get the implementers’ feedback and if they feel EIP-712 extension is the easier way to go, we will change to that course.

---

**agostbiro** (2023-02-05):

Thanks for submitting this EIP! It addresses a very important problem that doesn’t receive enough attention.

I love the idea being able to get a human readable description of an EIP-712 payload from the verifying contract, but I’m concerned about returning natural language messages from the `evalEIP712Buffer` method. I’d like to propose returning structured data instead of strings, which would have the following advantages:

1. Wallets could build their own display format based on the structured data to ensure consistency for UX and security reasons.
2. Structured data would enable localization (display in different languages) on the wallet side.
3. Receiving token contract addresses and quantities in the structured data would let wallets display balances and dollar values of tokens when approving the signature.

I imagine using the standard token transfer and approval events as the basis of the structured data format. If this is too limiting or too complex to implement, an alternative option could be for the verifying contract to provide a single entry point where all EIP-712 messages can be submitted for execution which would enable running transaction simulation on the payloads.

The transaction simulation approach could make sense, since wallets have to do transaction simulation anyway to learn the outcome of on-chain signature requests, and it might be easier to implement for smart contract developers than the alternatives. As an added benefit, the transaction simulation approach would eliminate the potential for mistakes in mapping EIP-712 payloads to explanations. I’m unsure about the security implications though.

Looking forward to hearing your thoughts!

---

**talbeerysec** (2023-02-06):

Returning structured data is indeed a good idea, for all the reasons mentioned.

We thought about it, but we were worried that would add additional complexity and would make it even harder to adopt by smart contract devs.

If smart contract devs are open to such extra complexity we would love to include it.

BTW, we can make this extensible by adding versioning, setting this to be version “1” and allow future upgrades in a backward compatible manner.

We can also have both: a string as a fallback that includes some data and added structured data, that the wallet can parse and show if the wallet supports it.

As for executing and simulating, I believe it would make the function not a “view” and will also must revert in the end to avoid actually executing (some idea as implemented in EIP-4337), which requires changes to simulation provider logic and might be dangerous if not implemented correctly in smart contract.

---

**rmeissner** (2023-02-07):

Thanks for bringing up this discussion.

I was wondering if a more “off-chain” based solution was considered. Building strings (especially for more complex EIP-712 types) can be quite complex.

It would be possible to include it as part of the ABI/Natspec documentation. Then it could be possible to use it via the “[Sourcify](https://sourcify.dev/)” approach.

Another alternative could be something like the [tokenlist standard](https://uniswap.org/blog/token-lists) where for each primary type you can find a decoding function (i.e. a wasm module). This would also allow to be more flexible in the future for adding multi-language support. Also it would make it possible that a “trusted” party (i.e. like for the tokenlists Uniswap) extends/maintains the list.

---

**auryn** (2023-02-07):

I have a pretty strong preference for the token-list approach, since it’s (1) compatible with all existing contacts using ERC-712 and (2) allows users to choose which list curators they trust.

---

**talbeerysec** (2023-02-07):

The solution is “off-chain” in the sense this is a “view” function that does not need to be executed on chain, but locally on node.

Natspec-like solutions can only give static information (“you are going to list something on OpenSea”), and not actually tell what would the specific message would do (“you are going to list your BAYC #4562 on OpenSea for 0.001 ETH”)

As for curated list by a “trusted” party, sounds like a centralized solution that we’d like to avoid, if possible.

---

**talbeerysec** (2023-02-07):

With our current suggested solution you don’t need to trust anyone except the contract your are signing to, that you already trust. Adding additional “trusted” curators is not helpful and adding another possible point of failure. Also see the reply above.

---

**Michaels** (2023-02-08):

Nice suggestion [@agostbiro](/u/agostbiro)

When using structured data, what if the data to be displayed isn’t necessarily related to token approvals?

I’m assuming wallets will check if the return data is of that type and if not just display the plain string?

---

**rmeissner** (2023-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/talbeerysec/48/8126_2.png) talbeerysec:

> Natspec-like solutions can only give static information (“you are going to list something on OpenSea”), and not actually tell what would the specific message would do (“you are going to list your BAYC #4562 on OpenSea for 0.001 ETH”)

That is not true (see [NatSpec Format — Solidity 0.8.17 documentation](https://docs.soliditylang.org/en/v0.8.17/natspec-format.html#dynamic-expressions)) .

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/talbeerysec/48/8126_2.png) talbeerysec:

> The solution is “off-chain” in the sense this is a “view” function that does not need to be executed on chain, but locally on node.

That is not really off-chain as the whole string building and type conversion is done on evm level (so the logic is stored on chain).

---

**talbeerysec** (2023-02-08):

> (see NatSpec Format — Solidity 0.8.17 documentation ) .

I learned something new about NatSpec today. Thank you for sharing. I am not sure it will be expressive enough for our needs, but I will give it a try.

> That is not really off-chain as the whole string building and type conversion is done on evm level (so the logic is stored on chain).

I assume most of this code already exists in the smart contract as it’s needed for the actual evaluation of the signature. And having the code stored on chain is more of a feature than a bug, in my eyes

---

**auryn** (2023-02-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/talbeerysec/48/8126_2.png) talbeerysec:

> As for curated list by a “trusted” party, sounds like a centralized solution that we’d like to avoid, if possible.

Have you checked out [tokenlists](https://tokenlists.org/)?

I’d say it’s anything but centralized. Rather, it allows anyone to create and curate a list (individuals, organisations, smart contracts, etc) and then it’s up to apps and users to decide which lists they trust and want to use.

---

**Vazi** (2023-02-09):

Hey, I’m looking into Tokenlists, not sure I understand how it can help with the suggested problem, it seems like it aims to curate a ‘Whitelist’ for legit tokens

---

**auryn** (2023-02-09):

If I understand the high-level goal of this EIP, it is to provide canonical, human-readable, descriptions of what a given EIP-712-like signature does, to make it more secure for users to interact with systems requesting these signatures.

Essentially, a user’s wallet needs to be able to display a human-readable interpretation of what a given signature will do on-chain.

As you said, [@Vazi](/u/vazi), Tokenlists is a system for curating lists of tokens. Not just which tokens are legit, but also the correct metadata for each token. [@rmeissner](/u/rmeissner) and I were not proposing to use Tokenlists for this use-case, rather that a tokenlists-like approach could be used to solve for the problem identified.

Essentially, rather than storing this information on-chain in the `verifyingContract`, which is not backward compatible with existing contracts leveraging EIP-712, this information would be independently curated in a similar fashion to how tokenlists works. There would be many competing lists, curated with different mechanisms, and it would be up to each app and user to decide which list of EIP-712 metadata they would like to make signature requests in their wallet more readable.

---

**talbeerysec** (2023-02-09):

With all due respect, these problems are not similar and hence require different solutions.

With tokens the contract cannot attest for itself, as the contract might be malicious (this is the original problem to be solved). Therefore, we must resort to solution in which others should attest to it and in this context tokenlist-like solution makes a lot of sense.

In the case of EIP-712 signatures, the contract is already trusted as it’s the `verifyingContract`. Therefore it is best suited to attest for itself and not require another list that has to be curated and maintained by 3rd parties.

---

**MicahZoltu** (2023-02-15):

I recommend checking out [Trustless Signing UI Protocol · Issue #719 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/719) for additional discussion/ideas on how something like this could be designed.  IIUC, it requires less data on chain than what is proposed here, and is a bit more flexible when it comes to things like localization.

---

**talbeerysec** (2023-02-16):

Thanks. We will look into it. Quite amazing you were thinking about such solutions back in 2017!


*(12 more replies not shown)*
