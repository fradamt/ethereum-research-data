---
source: magicians
topic_id: 14821
title: Progressive precompiles via CREATE2 shadowing
author: dcposch
date: "2023-06-25"
category: EIPs
tags: [precompile, create2]
url: https://ethereum-magicians.org/t/progressive-precompiles-via-create2-shadowing/14821
views: 3685
likes: 27
posts_count: 27
---

# Progressive precompiles via CREATE2 shadowing

## Summary

We can create future precompiles at deterministic `CREATE2` addresses, instead of special low addresses like `0x00...0003`. The precompile shadows a library contract implementing the same function.

This gives us a smoother deployment process. Different L2s and mainnet may ship the precompile at different times, but a user contract can use the same address. It just becomes more gas-efficient once the precompile lands.

## Goals

- Increase cross-chain compatibility. Easier to maintain compatibility across the many L2s and mainnet.
- Support contract accounts. This is especially important for account abstraction. 4337 accounts are themselves CREATE2 contracts which exist on all chains. For the proposed P256 precompile and others meant for wallet use, it’s very useful if the same wallet can work across all chains even when some might not have the precompile yet.
- Make precompiles easier to ship. Mitigates the chicken-and-egg problem of (needing to demonstrate usage and interest to ship a precompile) and (needing the precompile to get more usage).

## Things to standardize

The main prerequisite for CREATE2 shadowing is a well-optimized, well-vetted EVM contract implementing the function that will be precompiled. This, of course, is specific to each function.

There are a few things we could standardize across all functions, including sender and salt. Reasonable defaults might be

- Salt = 0
- Sender = 0x4e59b44847b379578588920cA78FbF26c0B4956C, the default CREATE2 deployer in Foundry

The goal is for the precompile address to be easily computable from just the contract code.

The contract code, in turn, should also be reproducible. Whatever language the contract is written in, the precompile EIP should include a one-step deterministic compilation to produce the exact bytecode that determines the address.

In Solidity, for example, this can be done by including `solc-input.json` bundling both the code and compiler settings.

## Testing

Precompiles always need a comprehensive spec and tests to ensure consistency between client implementations.

For CREATE2 shadowing, these tests additionally need to run against the CREATE2 contract. This ensures that user contracts won’t break once the precompile ships.

–

Idea credits to [@xinbenlv](/u/xinbenlv) and [Nalin](https://twitter.com/nibnalin)

## Replies

**xinbenlv** (2023-06-25):

Thank you [@dcposch](/u/dcposch)

Yes, I value overall idea for allowing a precompile contract to be used as regular contract first, demonstrate the adoption and usefulness and then be migrated to precompile. To give it a name to refer to this approach, I’d call it “Progressive Precompile Contract” just like the “progressive” in “*Progressive Web Apps” .

This could turn into two EIPs:

(1) one EIP for Progressive Precompile Contract (`Information EIP` as a “recommendation” or `Meta EIP` as a formal policy) and

(2) one EIP for the solution of CREATE2 Shadowing (likely to be categorize as an ERC).

The CREATE2 Shadowing and similar approach provides *one of* the solutions.

In particular, using CREATE2 Shadowing allows a cross-chain consistency for precompile contract to stay the same.

*Note this is not the only possible approach to achieve the Progressive Precompile Contract.* This could potentially unblock many Precompiles such as EIP-2537 [EIP-2537: Precompile for BLS12-381 curve operations](https://eips.ethereum.org/EIPS/eip-2537)

Here are the prior discussion on the github and I am cross-posting here for better awareness

---

###

**[dcposch](https://github.com/dcposch)** [2 days ago](https://github.com/ethereum/EIPs/pull/7212#discussion_r1240215378) •

edited

Curious if people are interested in `CREATE2` shadowing.

In short, if we make `PRECOMPILED_ADDRESS` the CREATE2 address of a contract that implements identical functionality–instead of a special low address like `0x00..0019`–then it allows a smoother deployment.

Chains will adopt this EIP at different times; maybe certain L2s are first, others later, and mainnet last. With CREATE2 shadowing, contracts can work on all chains immediately. They just become more gas-efficient once a given chain adds the precompile.

This is especially salient for this particular precompile, since a primary use-case for it is hardware backed wallets. A 4337 account is itself a CREATE2 contract that runs on all chains with identical code.

A related benefit is that it reduces the need for upgradeability in user contracts.

---

###

**[xinbenlv](https://github.com/xinbenlv)** [2 days ago](https://github.com/ethereum/EIPs/pull/7212#discussion_r1240350745) •

edited

[@dcposch](https://github.com/dcposch) I like your idea. I see the biggest merit of what you describe being a route reduce barrier for adding precompile contracts, mitigating the chicken-and-egg problem of “needs to demonstrate usage and interest to convince adding precompile” vs “needs adding the precompile to get more usage”.

I would be happy to collaborate if you want to propose an EIP for Create2 shadowing

---

###

**[ulerdogan](https://github.com/ulerdogan)** [yesterday](https://github.com/ethereum/EIPs/pull/7212#discussion_r1240792308)

The idea looks very interesting. I also would love to follow future plans and integrations about it.

---

###

**[dcposch](https://github.com/dcposch)** [15 hours ago](https://github.com/ethereum/EIPs/pull/7212#discussion_r1241006040) •

edited

[@xinbenlv](https://github.com/xinbenlv) happy to, but does it need an EIP? this is more a general pattern that can be applied to all precompiles that are pure functions

for future pure-function precompiles, CREATE2 shadowing seems like a win/win

---

###

**[xinbenlv](https://github.com/xinbenlv)** [15 hours ago](https://github.com/ethereum/EIPs/pull/7212#discussion_r1241012145) •

edited

I agree with you having a CREATE2 will be a wthat it’s win/win

To answer your question “does it need an EIP”? I’d assume the question being: Do we need to standardize it?

Here is what I think:

When there are many ways and variables (“moving pieces”) to do the same thing, standardization helps people coordinate. An example would be screw driver and screw, the size of screw bing standardize so people can manufacture screw and drivers independently and they will work together.

In the CREATE2 shadowing, I presume there are a few “moving pieces.” that if people make different choices, they will end up with the different sizes of screw, hence there are value to standardize.

1. For the same functionality, ideally everyone use the same contact address generated by CREATE, so that ultimately, with a hard-fork we can change them to precompile and with lower gas cost. We don’t want people generating different contacts deployed at different addresses.
2. How to determine the input of CREATE2? Which sender, which nonce, which bytecode?

- 2.1 Are there going to be a sender that everyone want to use so if nonce and bytecode are also determined it we can all agree upon the contract address generated by CREATE2?
- 2.2 How do we generate nonce? Shall we do something like ERC-600 / ERC-601 or BIP-32?
- 2.3 Should there be any magic in bytecode? E.g. Should bytecode be consistent should there be any additional behavior that caller can expect?

These are a few things I can think of.

To this point, I think the discussion of CREAT2 shadwing seems a bit off topic from this EIP.

If you are open to it, we shall probably make a [ethereum-magician.org](http://ethereum-magician.org) post to discuss, and leave this PR for the Precomiple of secp256r1 Curve support.

---

###

**[dcposch](https://github.com/dcposch)** [11 hours ago](https://github.com/ethereum/EIPs/pull/7212#discussion_r1241062964)

Yeah, fair points. The CREATE2 address would eventually have to be part of the proposed precompile regardless. I agree re: standardizing how it’s created.

Happy to make an ethmagicians post

---

###

**[ulerdogan](https://github.com/ulerdogan)** [5 hours ago](https://github.com/ethereum/EIPs/pull/7212#discussion_r1241179101)

Considering that the solutions that are expected to be presented as precompiled contracts cannot always be implemented as a Solidity smart contract, can we say that this is a downside for the standardization purpose?

---

**dcposch** (2023-06-25):

[@ulerdogan](/u/ulerdogan) oh for sure, this would be an optional standard for precompiles. It applies to pure functions which can be implemented reasonably efficiently in solidity.

That includes all the proposed cryptographic precompiles I’m aware of–P256, Blake3, BLS etc.

It *doesn’t* include precompiles that are not pure functions. For example, Optimism’s [0x4200… series](https://www.evmdiff.com/diff?base=1&target=10) of precompiles are special cross-chain oracles and bridges, and can’t be implemented as a contract.

---

**dcposch** (2023-06-25):

[@xinbenlv](/u/xinbenlv) curious, how would implement a progressive precompile without CREATE2?

---

**xinbenlv** (2023-06-25):

It seems CREATE2 is the best for now. But in theory CREATE could be used if people can agree with sender and always use the same nonce.

Another question, when using CREATE2, which `sender` do we plan to use?

Could there be any security implication when using Foundry default CREATE2 sender?

---

**dcposch** (2023-06-26):

I think it’s a reasonable choice for `sender`. It’s this contract, small and widely used:

https://github.com/Arachnid/deterministic-deployment-proxy

---

**xinbenlv** (2023-06-26):

I think there is a potential complexity of how do we make *all* (today and future) EVM chains and L2s, capable to use the *exactly* same sender. Which is a requirement if we want to make it progressively precompile in the future.

---

**chfast** (2023-06-26):

Seems the other big problem is that we don’t have source code / bytecode for any of precompiles (except Identity).

---

**dror** (2023-06-26):

See a [previous discussion](https://ethereum-magicians.org/t/eip-proposal-create2-contract-factory-precompile-for-deployment-at-consistent-addresses-across-networks/6083/18) about a precompile for CREATE2

To my understanding, there is no need for a precompile: there is no real benefit of creating a new opcode just for this purpose, it is enough to adopt the de-facto deterministic deployer mentioned (`0x4e59b44847b379578588920cA78FbF26c0B4956C`), and only require that chains make it available - it might require a "irregular state " as [@MicahZoltu](/u/micahzoltu)  mentions in the above post.

Note that once deployed, this contract is fully compatible with any EVM chain.

To my knowledge, BASE chain (which is EIP-155 from day one) did do this state-change to deploy the contract

---

**xinbenlv** (2023-06-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> Seems the other big problem is that we don’t have source code / bytecode for any of precompiles (except Identity).

For any contract that wants to petition to become a precompile, they are supposed to share the full transparency of computation and source code so that clients could implement them inside their own client. They need to make it clear mathematically what’s steps expected to be executed and provide test case data, just like all existing precompile proposal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> See a previous discussion  about a precompile for CREATE2
>
>
> To my understanding, there is no need for a precompile: there is no real benefit of creating a new opcode just for this purpose, it is enough to adopt the de-facto deterministic deployer mentioned (0x4e59b44847b379578588920cA78FbF26c0B4956C), and only require that chains make it available - it might require a "irregular state " as @MicahZoltu mentions in the above post.
>
>
> Note that once deployed, this contract is fully compatible with any EVM chain.
>
>
> To my knowledge, BASE chain (which is EIP-155 from day one) did do this state-change to deploy the contract

[@dror](/u/dror): I think that’s a different topic (though it could be a pre-requisite for this EIP to be feasible).

To clarify, the matter of discussion here are about “Can we allow a path for contracts to go from normal contract to precompile contract, whereas specifically the address of this contract’s deployment follow some deterministic provided by CREATE2”

[@dcposch](/u/dcposch) maybe we shall change the topic to “Progressive Path towards Precompile” to avoid confusion?

---

**xinbenlv** (2023-06-26):

Soliciting feedback: [@abdelhamidbakhta](/u/abdelhamidbakhta) (Author of EIP-5988), [@Recmo](/u/recmo) (Author of EIP-1829), [@chris](/u/chris)

And everyone welcome.

---

**xinbenlv** (2023-06-26):

Hi [@spalladino](/u/spalladino), as we are searching a possible route here, we discover you previously proposed a CREATE2 precompile, in which you argue in [this tweet](https://twitter.com/smpalladino/status/1385550147728388097)

> But how can you ensure the generic factory is available at the same address across all networks, so the resulting deployment address is the same?

We agree with you. The topic disucssed here propose a progressive way to make a contract become precompile. One of the dependency is to find the same `sender` across all networks. It shows the usefulness of your idea. We here ask for your feedback about our idea too.

---

**xinbenlv** (2023-06-26):

Cross-posting a technical feedback from Tobias Oberstein author of *EIP-665 introducing Ed25519 signature verification*

> I understand the idea, maybe it would help, I don’t know. What I would
> expect is massive gas cost for such a standard EVM (non-precompile)
> based Ed25519 verify function. The cost will render it practically
> useless on mainnet.
> So if it doesn’t gain traction using a non-precompile, that might then
> be the case since it is not a real solution to Ed25519.

My response:

> Here is how I see it: the way to convince EVM builders to accept a contract worthy of precompile is that: such computations are critically useful and lack alternatives, so much so that people are using their non-compile despite the high cost of gas.
>
>
> An example would be Poseidon Hash which has unique usefulness in the ZK without better alternatives in the existing instructions and precompiles.
> Another example is the alt_bn128 (EIP-196 / 197) which is also critical and lacks alternatives.
>
>
> For Ed25519, the original rationale is that it has a lower cycle. But whether EVM shall support them depends on whether there are wide enough adoptions. For example, if there are many signatures out there signed with Ed25519 that we want to on-chain verify, it shows an usefulness regardless of (currently) high gas cost.
>
>
> We are proposing an approach so authors of precompile can demonstrate they point progressively, that’s the intention of our proposal.

And as you (Tobias Oberstein) mention in the [EIP-665](https://eips.ethereum.org/EIPS/eip-665) which says

> Despite being around only for some years, post-Snowden, these curves have gained wide use quickly in various protocols and systems:
>
>
> TLS / ECDH(E) (session keys)
> TLS / x.509 (client and server certificates)
> DNSSEC (zone signing)
> OpenSSH (user keys)
> GNUPG/OpenPGP (user keys)
> OpenBSD Signify (software signing)

Which mentioned DNSSEC.

One example of possible route for a non-precompile could be that so much people are wanting to verify DNSSEC or OpenSSH on-chain that they end-up using the non-precompile despite its high gas cost, and ultimately gain large enough traction to convince Client Devs to build it as a precompile and reduce gas cost.

---

**dcposch** (2023-06-26):

A few quick thoughts:

### Picking a good sender

I’m open to alternatives.

`0x4e59b44847b379578588920cA78FbF26c0B4956C` is widely used and seems to be available on all popular EVM chains. I’ve checked:

- Mainnet
- Optimism
- Arbitrum
- Polygon
- Goerli
- Sepolia
- Base Goerli

CC [@Arachnid](/u/arachnid) - let me know if `0x4e59...` is a good choice. I’m curious what your level of confidence is that it’ll continue to be deployed to new EVM chains going forward.

Also happy to hear any arguments for a better already-existing CREATE2 deployer contract to use as our `sender`.

**Lastly some context. While we’d like a stable and universal `sender`, it’s not a rigid commitment we’re stuck with.** This proposal is about a clean path to ship new precompiles. Each precompile could use a different sender and nothing would necessarily break; specifying a good universal default is convenient but not essential.

### Re: a precompile for CREATE2 itself

An interesting idea, but seems a ways off and not directly related to this idea. I think we can keep discussion separate–this proposal doesn’t depend on it.

### Proposed precompiles like Ed25519 and gas costs

Even if the contract for a given function is too expensive for mainnet, it can still be valuable for compatibility on rollups. L2 costs are dominated by L1 data availability (calldata/blob data post 4844) – computation gas on L2 is cheap.

---

**xinbenlv** (2023-06-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dcposch/48/6087_2.png) dcposch:

> ### Picking a good sender
>
>
>
> I’m open to alternatives.
>
>
> 0x4e59b44847b379578588920cA78FbF26c0B4956C is widely used and seems to be available on all popular EVM chains. I’ve checked:

I think picking the sender (let’s call it “**Designated Sender**”) will be one of the key problem to make this Progressive approach work.

The ultimate promise is that: All EVM chains (including future EMV chain that don’t exist today) shall be able to deploy with the identical address of Designated Sender.

That means there needs to be a consistent way for that Designated Sender to come into existance in new chains, in all constraints to these chains.

For example, if a chain is designed to be *permissionless*, the Designated Sender needs to come into existence in a *permissionles* way. For example, if the one that you suggested, which is the [Default Foundry Factory 0x4e59…956c](https://etherscan.io/address/0x4e59b44847b379578588920ca78fbf26c0b4956c) that you referred to is created in the [TX](https://etherscan.io/tx/0xeddf9e61fb9d8f5111840daef55e5fde0041f5702856532cdbb5a02998033d26) by [The Wolves of Wall Street: Deployer 0x3fab…5362](https://etherscan.io/address/0x3fab184622dc19b6109349b94811493bf2a45362),

Which means the Wolves of Wall Street Deployer might have to publish they private key so new chain could establish them, which could have security implications.

Therefore, it seems so far, the sender itself needs to be a precompile (or have its own address), as proposed in [the thread](https://ethereum-magicians.org/t/eip-proposal-create2-contract-factory-precompile-for-deployment-at-consistent-addresses-across-networks/6083/18) proposed by [@spalladino](/u/spalladino)

---

**dror** (2023-07-11):

> Which means the Wolves of Wall Street Deployer might have to publish they private key so new chain could establish them, which could have security implications.

That is wrong: the deployment of this deployer’s deployment is completely permissionless.

The deployment transaction is the same on all network, which means the network must accept non-EIP155 transactions and 100wei gas price.

So either the network accepts this conditions always, or it performs a one-time “non-standard state change” to include this transaction.

Note that regardless of how the deployer gets deployed, using it, doesn’t require any non-standard transaction, as it is a normal contract call.

BTW: the [Base (testnet)](https://goerli.basescan.org/tx/0xeddf9e61fb9d8f5111840daef55e5fde0041f5702856532cdbb5a02998033d26) network didn’t have the deployer deployed to begin with, and it has EIP-155 enabled fro day one, so we couldn’t install it ourselves.

We reached them out to deploy it, so that EIP4337 [EntryPoint](https://goerli.basescan.org/address/0x5ff137d4b0fdcd49dca30c7cf57e578a026d2789) could be deployed at the standard address as on other networks.

The deployer’s code (by [@Arachnid](/u/arachnid) ) is [here](https://github.com/Arachnid/deterministic-deployment-proxy):

And an [article](https://yamenmerhi.medium.com/nicks-method-ethereum-keyless-execution-168a6659479c) describing this permissionless deployment method.

---

**dcposch** (2023-07-11):

Makes sense, thank you!

So I think we have a clean way to deploy a contract at a deterministic address.

I’m curious about two other aspects:

- Is there a good reason not to do it this way? In other words, a good reason to keep using low-numbered 0x00..0a, 0x00..0b precompiles.
- What are the implementation challenges? Would love to hear from client developers on how much additional effort it would be to ship, say, the P256 or BLS precompile progressively.

---

**xinbenlv** (2023-07-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> That is wrong: the deployment of this deployer’s deployment is completely permissionless.
> The deployment transaction is the same on all network, which means the network must accept non-EIP155 transactions and 100wei gas price.

[@dror](/u/dror) : thanks for the feedback, but if you mean to use pre-EIP-155 TX to deploy to deterministic address, IMHO, EIP-155 is enabled by default for most new chains that I know of, for the re-play attack exactly demonstrated by the old Nick’s method: Replay the same TX everywhere from any chain disregarding chainId.

Asking those new chains to include legacy Pre-EIP-155 transaction is no different than asking for their permission. If I understand it correctly, that alternatives of using permissionless deterministic deployment requires as strong of consensus as getting a hard-fork in those new chains, yet non-standard each time.

Alternatively, this proposal here provides a standardized way to do so.

---

**dror** (2023-07-14):

The need for a deployer is clear.

It can either be a precompiled contract, which requires developer support on all existing (and future) networks, and it can be done by accepting an already proven solution on [20-some](https://blockscan.com/address/0x4e59b44847b379578588920cA78FbF26c0B4956C) major networks, and thus only OTHER network need to do anything explicitly to support it.

Also, the required change is not any code modification, but nonstandard inclusion of a valid transaction.

Also, do you think you can convince the developers of ethereum, polygon, bsc, optimism, arbitrum, etc, that they need to push an EVM change, when their network already supports that feature ?

---

**dcposch** (2023-07-28):

CC [@matt](/u/matt) ; do you have a sense of relative effort for client developers?

For example, from where we are today, how difficult would it be to put a precompile like BLS or P256 at an existing CREATE2 address vs next sequential?

---

**matt** (2023-07-28):

It is no more difficult to deploy a precompile to an arbitrary address than it is to deploy to the next sequential address. You can see addresses are just hard coded: https://github.com/ethereum/go-ethereum/blob/8f2ae29b8f7743a14760e6f2b458ecddc8bb7d8f/core/vm/contracts.go#L112-L122


*(6 more replies not shown)*
