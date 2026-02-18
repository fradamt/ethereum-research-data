---
source: magicians
topic_id: 9951
title: "EIP-5267: Retrieval of EIP-712 domain"
author: frangio
date: "2022-07-15"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5267-retrieval-of-eip-712-domain/9951
views: 5719
likes: 18
posts_count: 42
---

# EIP-5267: Retrieval of EIP-712 domain

Discussion for EIP-5267.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5267)





###



A way to describe and retrieve an EIP-712 domain to securely integrate EIP-712 signatures.










> This EIP complements EIP-712 by standardizing how contracts should publish the fields and values that describe their domain. This enables applications to retrieve this description and generate appropriate domain separators in a general way, and thus integrate EIP-712 signatures securely and scalably.

## Replies

**cylon56** (2022-07-19):

Hi [@frangio](/u/frangio) - This seems a great, common-sense way to standardize EIP-712 domain retrieval.

Couple questions:

1. Are there some specific examples of projects suffering the issues that this EIP will alleviate that you can share? How big do you think the impact would be if this became widely adopted?
2. Are there any existing implementations using this approach in production right now?

*Note: I work with [@frangio](/u/frangio) in a separate team at OpenZeppelin but I thought this question would be better asked in the public forum in case others found it useful.*

---

**frangio** (2022-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cylon56/48/6352_2.png) cylon56:

> Are there some specific examples of projects suffering the issues that this EIP will alleviate that you can share? How big do you think the impact would be if this became widely adopted?

All decentralized ERC20 exchanges that don’t have or only have partial support for permit are suffering from this issue. Currently, the only way to use ERC20 permits is to either hardcode the EIP-712 domain for a subset of tokens, and/or to “guess” the domain and verify that you guessed it correctly with `DOMAIN_SEPARATOR`. The first option is not scalable and the second option is not reliable and not general. Additionally, they don’t help with other EIP-712 usecases: while ERC20 has a `name()` function that can help the guess for permits, other standards or contracts don’t.

A concrete example is 1inch, which has partial support. USDC on Ethereum mainnet has the option to use permit, but permit is not available on 1inch on Arbitrum even though almost all tokens have permit because it’s the default of the bridge. I believe this is a cosequence of having no good general and scalable way to request EIP-712 signatures like permits.

I hesitate to speculate on the potential impact. I don’t think EIP-712 is usable without something like what I’m proposing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cylon56/48/6352_2.png) cylon56:

> Are there any existing implementations using this approach in production right now?

Not yet, that I’m aware of. I’ve discussed this problem with some people before but this is the first solution that has been proposed I think.

---

**ZumZoom** (2022-07-22):

Hi [@frangio](/u/frangio). I agree that permit support is a struggle without standardised way of domain retrieval. I think that better example will be Polygon standard PoS tokens like [USDC](https://polygonscan.com/address/0x2791bca1f2de4661ed88a30c99a7a9449aa84174) or [USDT](https://polygonscan.com/address/0xc2132d05d31c914a87c6611c10748aeb04b58e8f). They all use the domain `EIP712Domain(string name,string version,address verifyingContract,bytes32 salt)` instead of the more widespread `EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)`. The diversity of domains and lack of domain structure exposure makes it difficult to support all the different domains which why only the most widespread ones are supported.

Overall your suggestion seems great and will surely improve the permit support in dapps.

---

**d3mage** (2022-07-26):

Hello. After reading the EIP, I would ask [@frangio](/u/frangio) to add a minor clarification to the section regarding fields. “if and only if **domain** field `i` is present” makes it easier to understand what fields are we talking about.  The only question is why bits are read from least significant to most significant? Wouldn’t it be more convenient to use big-endian notation?

But overall this EIP is a really good one, expecting it to be widespread

---

**frangio** (2022-07-27):

Thanks [@d3mage](/u/d3mage)!

What difference do you see from changing it to “domain field”? It seems the same as the current text to me.

The choice of endianness is a tradeoff. The way it’s specified now it’s really easy to specify and implement the decoding function (see the JS snippet in Reference Implementation). What you suggest might make it easier to write the Solidity part (when writing manually at least), is this the reason you were suggesting the change of endianness?

---

**d3mage** (2022-07-28):

From my personal experience: took me some time to figure out what fields we were talking to. So a small pointer would be sufficient for a reader to pay attention and understand what those fields are.

If I understand it properly, the choice of endianness is driven by the goal of creating a generic backend, compatible with any domain (welp, this is what this standard is about). In such case, I can only agree with you. Thanks for your response ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**philipliao** (2022-08-07):

This is an excellent EIP and solves a true pain point. Right now, determining the EIP-712 domain of contracts is either: guess and check, or digging into the source code.

It could also be nice to deploy a canonical registry contract on each chain that “validates” the EIP-712 Domain. Anyone can attempt to “register” the domain for a given contract, but this will only succeed if the hash of the domain is equivalent to the contract’s `DOMAIN_SEPARATOR`. Might need some consideration for proxy contracts like USDC

Finally, people could look up `function eip712Domain(address target)` in largely the same way that they would if the original contract implemented this EIP (which many immutable contracts cannot). This view function would likely need to recompute the hash and check the `DOMAIN_SEPARATOR` again, in case the proxy implementation has changed its domain

Maybe this registry contract already exists, but would be nice to have for existing tokens that cannot implement this standard (and new tokens that don’t know about this standard)

---

**frangio** (2022-08-07):

Thanks!

And on-chain registry could be useful, but I expect some sort of off chain registry for those contracts anyway. The info could just be embedded in token lists. I think the off chain approach is slightly more powerful in the sense that a human can verify if the domain is immutable (whereas a smart contract registry couldn’t do that).

---

**wighawag** (2022-09-03):

Thanks [@frangio](/u/frangio) for making this proposal, this is indeed much needed for EIP-712 to be truly usable

Couple comments:

- The proposal does not implement EIP-165. I guess this is intentional and would like to see the rationale for it. I suppose this is because if the function throws, then we know the contract does not support this proposal. Technically a minimum gas limit should be specified then to be accurate.
- The proposal uses a function instead of an event. My first impression is that an event should be more than sufficient since the tx signer that needs to make use of EIP-712 will be able to provide the information to the contract. If there is a use-case for on-chain retrieval of the domains that cannot be achieved with the tx signer providing the info, it would be great to see it mentioned in the rationale. If on the other hand, the function is intended to be only called off-chain, one could solve the gas limit requirement mentioned in the previous point by specifying that the block gas limit need to be provided

Actually, while I was writing this last comment I realised a potential rationale for using a function: if the parameters are somehow dynamic, it would not be possible to use events. One particular example is the chainID which in several contracts is made dynamic to support minority forks. (While an event could technically be triggered in such case, it would require an external action to trigger the tx). But maybe  you have more to add here.

---

**TimDaub** (2022-09-03):

Please provide a link to your proposal, now I’m interested how events can solve this.

---

**wighawag** (2022-09-03):

oh, I do not have a proposal, just was thinking an event could be used instead of the function

like

```auto
event EIP712Domain(bytes1 fields,
      string memory name,
      string memory version,
      uint256 chainId,
      address verifyingContract,
      bytes32 salt,
      uint256[] memory extensions);
```

but like I mentioned on dynamic parameter like chainId, this is not as great as the event would have to be triggered

---

**frangio** (2022-09-04):

Thanks for the feedback!

I’ve considered an event but discarded it due to the issue with dynamic domains that you point out, and also that I believe it’s not as simple to fetch an event as it is to query a view function. For example, [Cloudflare’s Ethereum Gateway](https://developers.cloudflare.com/web3/ethereum-gateway/reference/supported-api-methods/) supports `eth_call` but does not support the RPC endpoints related to logs. I don’t know if logs would remain reliable in the future due to pruning.

---

I didn’t really consider ERC-165 but my thinking was as you described, if the function reverts it should be assumed not to be there.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> Technically a minimum gas limit should be specified then to be accurate.

Do you mean a maximum? In order to give clients a minimum gas limit to submit, the EIP would need to specify the maximum gas the function can use.

I can see that technically there’s a problem if there is no maximum in the spec, but in practice `eth_call` runs with a large amount of gas so it wouldn’t run into that problem, and hardcoding gas limits is generally seen as a bad idea nowadays due to possible pricing changes in the future.

---

**wighawag** (2022-09-04):

> I’ve considered an event but discarded it due to the issue with dynamic domains

yes, it indeed makes sense

> Do you mean a maximum? In order to give clients a minimum gas limit to submit, the EIP would need to specify the maximum gas the function can use.

Yes, a maximum for the function to use

> I can see that technically there’s a problem if there is no maximum in the spec, but in practice eth_call runs with a large amount of gas so it wouldn’t run into that problem, and hardcoding gas limits is generally seen as a bad idea nowadays due to possible pricing changes in the future.

If there is no use for any contract to call that function on-chain, then the maximum gas could be the `block gas limit`, this remove the need for hardcoding any specific value. But this would indeed be mostly a technical details as in practise it should never matter.

---

**TimDaub** (2022-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> For example, Cloudflare’s Ethereum Gateway supports eth_call but does not support the RPC endpoints related to logs.

Respectfully, I think Cloudflare’s Ethereum Gateway doesn’t matter for making EIP decisions.

---

**dror** (2022-09-04):

IIRC, the problem is how to map a domain separator of a specific contract to its generating fields, to be included in the `signTypedData` call.

The domain-separator itself is traditionally exposed by contracts as `bytes32 public DOMAIN_SEPARATOR`

While it is possible for contract to expose a public `eip712Domain `, this does not help existing tokens.

My suggestion is to add a registrar for domains: a singleton contract that exposes a method

```auto
function validateDomainSeparator(bytes32 domainSeparator, uint8 fields, string memory name, string memory version, address verifyingContract, bytes32 salt)
```

That validates this domain and register it.

(note that the `uint fields` is a bitmask as in your definition, which also includes “chainId”, which is not passed as a parameter, but has to match the current network’s chainId)

This registrar is permission-less, since only the parameters define the domain, not the caller.

Note that this registrar is not instead of adding an eip712Domain method, but in addition to it.

specifically, such registrar can’t support extensions.

We can also extend this registrar to register actual tokens, as long as they support `DOMAIN_SEPARATOR()` or `getDomainSeparator()` view methods

---

**frangio** (2022-09-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Respectfully, I think Cloudflare’s Ethereum Gateway doesn’t matter for making EIP decisions.

My point is not about this particular service provider but about the availability of logs in general. If a service provider has decided not to make them easily available, there is reason to believe others won’t either.

---

[@dror](/u/dror) My initial intention was for existing tokens to be supported by an *off-chain* registrar. Do you see any use cases where an on-chain registrar like you describe is necessary? Or other reasons why it may be superior?

---

**dror** (2022-09-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> My initial intention was for existing tokens to be supported by an off-chain registrar. Do you see any use cases where an on-chain registrar like you describe is necessary?

I’m trying to get into the root requirement: we want a way to get per-domain the information that wallets need in order to prompt the users.

We don’t want an off chain database, since that has scalability/availability issue.

Your model achieve this by adding a method to each contract that provide the domain.

With my model, instead of an api method per contract, there is a singleton and one method which gets the contract as parameter.

(And I does rely on the contract to expose DOMAIN_SEPARATOR to return the hash)

The major difference, of course, is that your model can support extension fields in the “domain separator”, whereas a central registry is more rigid.

Not that both solve only half the problem, as there is the REQUEST_TYPE, which can’t be generalized, since it differ with each request.

The only need for a domain separator is in cases where the request type itself is too generic, and just by itself can serve different purposes.

---

**hiro** (2022-09-18):

There is an issue with how EIP-5267 is defined: the return parameter list includes parameters named `name` and `version`, and these exactly match two optional but widely-supported functions (public fields) added to ERC20 contracts.

Consequently, when implementing `eip712Domain()` in an ERC20 contract that contains these fields, the compiler gives `Warning: This declaration shadows an existing declaration.`

Renaming the public functions is not an option, since it is part of the ERC20 contract’s (optional extension) API. And there is no Solidity compiler directive for disabling this warning. Therefore, if you want a clean build (no warnings), only the return values from `eip712Domain()` can be renamed.

However, renaming the return params by adding underscores or similar is not only ugly, but it will create incompatibilities (code breakage) if the return values are being read by a Javascript Web3 library like Ethers that pulls the return parameter names from the API:

```auto
function eip712Domain() external view
returns (bytes1 fields, string memory _name, string memory _version, uint256 chainId,
            address verifyingContract, bytes32 salt, uint256[] memory extensions)
```

Therefore, probably in the EIP-5267 spec, these parameter names should be renamed to something like `tokenName` and `tokenVersion`.

---

**frangio** (2022-09-19):

Interesting find. However, I don’t think this is true:

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/b5ac83/48.png) hiro:

> it will create incompatibilities (code breakage) if the return values are being read by a Javascript Web3 library like Ethers that pulls the return parameter names from the API

The client (e.g. the JS code) would interact with the contract using a fixed ABI spec that defines return value names that are independent of the contract source code. The contract can use any names it wants in its source code without affecting compatibility with that client.

Additionally, the return value names in the EIP are non-normative (i.e. a compliant implementation can use different names; this should be implicitly understood), and since this is due to Solidity idiosyncrasies and limitations, I would not change the EIP based on this problem.

Note that `tokenName` and `tokenVersion` are not good options because EIP-712 is relevant beyond tokens.

---

**hiro** (2022-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> The client (e.g. the JS code) would interact with the contract using a fixed ABI spec that defines return value names that are independent of the contract source code. The contract can use any names it wants in its source code without affecting compatibility with that client.

Currently, in order to instantiate a web3 `Contract` object, libraries like Ethers require the user to submit a minimum of the contract address and the contract ABI (in either human-readable string form or JSON). The ABI is output by Solidity. It would be very annoying if the user had to go in and manually edit the ABI file to manually change these parameter names every time a new version of the contract is built and deployed, from the versions that were built (e.g. `_name` and `_version`) to the versions that the user wants to use in the JS API (e.g. `name` and `version`).

The creator of Ethers is considering pulling the ABI directly from Etherscan, so that to instantiate a Contract object, you would only have to specify the address of an Etherscan-verified contract. At that point, whatever is built by Solidity, and deployed, is what will be automatically exposed in Javascript.

So yes, names exposed in Solidity do in fact matter in Javascript code.


*(21 more replies not shown)*
