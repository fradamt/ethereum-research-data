---
source: magicians
topic_id: 6728
title: "Durin: Secure offchain data retrieval"
author: Arachnid
date: "2021-07-27"
category: EIPs
tags: [data, scaling]
url: https://ethereum-magicians.org/t/durin-secure-offchain-data-retrieval/6728
views: 7299
likes: 15
posts_count: 23
---

# Durin: Secure offchain data retrieval

This is a discussion thread for [EIP 3668 - Durin: Secure offchain data retrieval](https://github.com/Arachnid/EIPs/blob/durin/EIPS/eip-3668.md).

Durin is ENS’s approach to supporting offchain lookups of data without requiring clients to understand how to query each possible data source. It’s capable of being transparently integrated into client libraries such as web3 and Ethers in a way that doesn’t require the application author to care about how queries are executed or where they source their data.

Feedback on the EIP is very much appreciated.

## Replies

**jpitts** (2021-07-29):

[@Arachnid](/u/arachnid), this is a really well-structured proposal!

Is “prefix” intended to be a code which changes per each query to the original contract, or at least unique given the caller and function parameters? The name of this may be confusing to some developers, although perhaps there is ample precedent in other smart contracts? If I understand “prefix”, the concept reminds me of “authorization codes” used in cross-web-app redirects.

---

**Arachnid** (2021-07-29):

Basically, the prefix has to commit to the relevant parts of the query, so that the gateway can’t provide a valid answer to a *different* query.

A concrete example may help. Suppose you’re implementing ERC20’s `balanceOf` function using Durin:

```auto
function balanceOf(address addr) public returns(uint256)
```

Your implementation wants the gateway to go off and get the result, with some proof data, and call this function:

```auto
function balanceOfWithProof(address addr, uint balance, bytes memory proof) returns(uint256)
```

If the prefix specified by the first function were empty, the gateway could return a call to any function at all on the contract, which would be bad.

If the prefix contains just the 4-byte function ID, the gateway would need to return a call to `balanceOfWithProof`, but it could have any arguments at all - meaning it could return a proof of the balance of a different account.

If the prefix contains the function ID and the first argument, the gateway can only return calls with the correct address - so it no longer has the freedom to mislead the caller or the contract.

This can be easily implemented in the contract by making the prefix the result of `abi.encodeWithSelector(balanceOfWithProof, addr)`.

---

**jpitts** (2021-07-29):

Thanks for clarifying! I was off the mark.

---

**molekilla** (2021-08-01):

[@Arachnid](/u/arachnid) I like the specs and I think I can help with, do you think this gateway if using multiformats / ipld can be the proof? More here Explaining XDV Protocol [Explaining XDV Protocol. Here is the XDV Protocol architecture… | by IFESA | Jul, 2021 | Medium](https://ifesa.medium.com/explaining-xdv-protocol-eed7b8516cb3)

---

**Arachnid** (2021-08-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/molekilla/48/4357_2.png) molekilla:

> do you think this gateway if using multiformats / ipld can be the proof?

The proof can be formatted any way that both the gateway and the contract agree on.

---

**juanfranblanco** (2021-08-03):

So when we are executing transactions, we can pass a byte array collection of “functions with Proofs” that can be selected from the input?

`CallData[function balanceOfWithProof(address addr, uint balance, bytes memory proof) returns(uint256)]`

Also, do you envision the `proof` to be a signature that can be recovered?

---

**Arachnid** (2021-08-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/juanfranblanco/48/6519_2.png) juanfranblanco:

> So when we are executing transactions, we can pass a byte array collection of “functions with Proofs” that can be selected from the input?

I’m not sure what you mean by this. The Durin gateway will return the call data for a single call or transaction, formatted to match the expectations of the contract that initiated a Durin call. It won’t return an array of calldatas.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/juanfranblanco/48/6519_2.png) juanfranblanco:

> Also, do you envision the proof to be a signature that can be recovered?

I expect that to be one common way to do things where the trust model permits it, but the proof can be anything - for example, a contract and gateway that connect to Optimism would contain merkle proofs against the Optimism state root on mainnet.

---

**Arachnid** (2022-01-06):

I’ve been working extensively on this EIP in conjunction with the Chainlink team, and I believe it’s ready for use. I’ve asked the editors to move it to Last-Call status.

---

**wighawag** (2022-01-08):

Hi all, as I briefly mentioned on twitter (https://twitter.com/wighawag/status/1478999358968406018)

the spec is currently not fully compatible with IPFS for these reasons:

1. 404 errors won’t be able to be json in case the ipfs url points to a non-existing file
2. ipfs gateway’s current way to handle mime-type seems to be in flux still. the go implementation (GitHub - ipfs/go-ipfs: IPFS implementation in Go) currently uses the following mechanism to detect mime type (as can be seen here : go-ipfs/gateway_handler.go at 7c76118b0b7026fba8357807e5a67b59fc2b684b · ipfs/go-ipfs · GitHub) :

check extension (which cause issues like : MIME type sniffing bug (filename prioritized over content?) · Issue #4543 · ipfs/go-ipfs · GitHub)
3. check for pattern in the content and for that recently switched from golang builtin http package - net/http - pkg.go.dev to GitHub - gabriel-vasile/mimetype: A fast Golang library for media type and file extension detection, based on magic numbers to detect the mime-type from the content of the file. While it supports json, it fill brittle.
There has been some discussion on supporting mime-type as metadata in unixfs but I am not sure what the latest, see : State of UnixFS v2 · Issue #86 · ipfs/go-unixfs · GitHub and ipld/fs.md at master · ipld/ipld · GitHub

Solutions:

For 1. we could simply update the spec to not force the use of json in case of error. client simply look at the HTTP status code

For 2, we could

- A. assume json detection will work without extension needed to be added
- B. add in the spec that url need to finish with .json and assume the file name extension is a valid mechanism for ipfs gateway to detect mime-type (at least for json)
- C. do not force the use of application/json and simply assume the response is json.

---

**Arachnid** (2022-01-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> 404 errors won’t be able to be json in case the ipfs url points to a non-existing file

Thanks - I already updated the spec to not require errors have application/json content-type.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> ipfs gateway’s current way to handle mime-type seems to be in flux still.

A better solution here might be to specify that the URL has a meta-variable that is replaced with the query - much like EIP 1155. I’ll draft a change with this.

---

**serenae-fansubs** (2022-01-11):

I posted this on the ENS discourse as well:

> One example of a valid implementation of balanceOf would thus be:

```auto
function balanceOf(address addr) public view returns(uint balance) {
    revert OffchainLookup(
        address(this),
        [url],
        abi.encodeWithSelector(Gateway.getSignedBalance.selector, addr),
        ContractName.balanceOfWithProof.selector,
        abi.encode(addr)
    );
}
```

> Note that in this example the contract is returning addr in both callData and extraData , because it is required both by the gateway (in order to look up the data) and the callback function (in order to verify it). The contract cannot simply pass it to the gateway and rely on it being returned in the response, as this would give the gateway an opportunity to respond with an answer to a different query than the one that was initially issued.

Doesn’t this open the door for poor/naive implementations where devs will fail to read the full spec and just rely on the correct response being returned? I notice this is pointed out below in the Security Considerations as well, but I’m worried about a hasty implementer missing this. What if the original `callData` was also passed to the callback as well?

`(bytes originalCallData, bytes response, bytes extraData)`

That way the callback is always guaranteed to receive the original data. And then `extraData` can still be used for anything that your callback needs but that you don’t want to send to the gateway (or other arbitrary contextual data).

Or, do you think that would be inappropriate/superfluous for most cases? It seems like it would be helpful for the current `balanceOfWithProof` example at least. But it doesn’t eliminate the problem: If verification is needed, implementers would still need to actually ***do*** that verification against `originalCallData`.

Admittedly this also means that you would probably be passing additional information to the callback function that it wouldn’t ever need, like `Gateway.getSignedBalance.selector` in this case.

So yeah, now that I’ve typed this out I can see the pros and cons, either way the dev is going to need to be aware of the security best practices here, and passing the original calldata might just be more overhead. Curious to hear your thoughts though!

---

**serenae-fansubs** (2022-01-11):

It looks like the link in the initial post still points to the durin branch, and the latest changes [@Arachnid](/u/arachnid) made aren’t merged in there (not sure if they’re meant to be or not).

The latest version of the spec is here I believe:



      [github.com](https://github.com/Arachnid/EIPs/blob/master/EIPS/eip-3668.md)





####



```md
---
eip: 3668
title: "CCIP Read: Secure offchain data retrieval"
description: CCIP Read provides a mechanism to allow a contract to fetch external data.
author: Nick Johnson (@arachnid)
discussions-to: https://ethereum-magicians.org/t/durin-secure-offchain-data-retrieval/6728
status: Review
type: Standards Track
category: ERC
created: 2020-07-19
---

## Abstract
Contracts wishing to support lookup of data from external sources may, instead of returning the data directly, revert using `OffchainLookup(address sender, string[] urls, bytes callData, bytes4 callbackFunction, bytes extraData)`. Clients supporting this specification then make an RPC call to a URL from `urls`, supplying `callData`, and getting back an opaque byte string `response`. Finally, clients call the function specified by `callbackFunction` on the contract, providing `response` and `extraData`. The contract can then decode and verify the returned data using an implementation-specific method.

This mechanism allows for offchain lookups of data in a way that is transparent to clients, and allows contract authors to implement whatever validation is necessary; in many cases this can be provided without any additional trust assumptions over and above those required if data is stored onchain.

## Motivation
Minimising storage and transaction costs on Ethereum has driven contract authors to adopt a variety of techniques for moving data offchain, including hashing, recursive hashing (eg Merkle Trees/Tries) and L2 solutions. While each solution has unique constraints and parameters, they all share in common the fact that enough information is stored onchain to validate the externally stored data when required.

```

  This file has been truncated. [show original](https://github.com/Arachnid/EIPs/blob/master/EIPS/eip-3668.md)












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3668)





###



CCIP Read provides a mechanism to allow a contract to fetch external data.

---

**Krayola** (2022-01-12):

So, in theory, the 3 step process will be only necesary the first time you want to call an offchainlookup related function right? If you called it once already and it returned you the gateway url info, the following times you need to call the original function you could skip step 1 and make a request to the gateway directly right?

Or I am missing something?

---

**Arachnid** (2022-01-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/krayola/48/5206_2.png) Krayola:

> So, in theory, the 3 step process will be only necesary the first time you want to call an offchainlookup related function right? If you called it once already and it returned you the gateway url info, the following times you need to call the original function you could skip step 1 and make a request to the gateway directly right?

The contract determines the input data to the gateway - so you will always need to call the contract first in order to obtain the correct input data.

---

**naomsa** (2022-01-14):

Hi, sorry for the dumb questions, but some things are still unclear to me:

- What does During means?
- Is there any live implementation we could take a look at?
- How can I query reverts and Errors from ethers.js or web3.js?
- When the user requests the off chain data, the call is reverted and then he needs to retrieve the results on another view call, right?

---

**Arachnid** (2022-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/naomsa/48/5230_2.png) naomsa:

> What does During means?

It’s the original codename for this standard.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/naomsa/48/5230_2.png) naomsa:

> Is there any live implementation we could take a look at?

https://github.com/smartcontractkit/ccip-read/tree/rewrite

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/naomsa/48/5230_2.png) naomsa:

> How can I query reverts and Errors from ethers.js or web3.js?

Ethers throws an exception with error information in the exception object. See the ethers provider plugin in the above repository for a way to handle EIP 3668 contracts transparently to the JS code.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/naomsa/48/5230_2.png) naomsa:

> When the user requests the off chain data, the call is reverted and then he needs to retrieve the results on another view call, right?

That’s right. All of this can be handled transparently for the user via the web3 library, however.

---

**poojaranjan** (2022-01-17):

[EIP-3668: CCIP Read: Secure offchain data retrieval](https://youtu.be/y7BDRt0zCJQ) with [@Arachnid](/u/arachnid)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/6/6a5dbaa01089b83b008197d11bae1010bf0cb415.jpeg)](https://www.youtube.com/watch?v=y7BDRt0zCJQ)

---

**frangio** (2022-01-18):

I’m a little confused by the use of `balanceOf` as the example, as if implying that the ERC makes sense in that context. Such a contract would clearly not be ERC-20 compliant, right? Even if it is compliant technically it would simply not interoperate at all with the ERC-20 ecosystem.

Might be worth using a different function for the examples?

---

**Arachnid** (2022-01-20):

There’s really no way to build in validation without requiring it to be in specific formats - which obviates the entire point of the protocol, which is to allow clients (web browsers) to fetch data needed to execute contracts without having to understand the format of the data they’re fetching. Further, doing this wouldn’t really help, as it the proofs would still have to be verified onchain by the contracts receiving the data.

If people want to submit data from offchain insecurely, they can do that today with a simple string field and by first fetching the data in the user’s browser; EIP 3668 doesn’t add anything new here.

I think it would be extremely misguided to reject a generic data-fetching standard because some people may use it badly. There will absolutely be standardised Solidity libraries for validating proofs, and JS libraries for generating them, which will make “doing the right thing” as easy as possible.

---

**Arachnid** (2022-01-20):

hyperbart:

> I think it is more important to think about what programming patterns the feature will allow in the future rather than compatibility with the existing code/protocols (such as Chainlink I assume).

There’s no existing protocol we’re trying to preserve compatibility with; I’m saying that if you try and hardcode the verification mechanism into the protocol, it becomes useless as a general-purpose protocol, which makes it more or less useless full-stop.

 hyperbart:

> If the programming pattern we’re allowing is “fetch anything from a url”, we’re setting ourselves up for a major precedent. I can imagine there would be a StackOverflow question somewhere, with a newcomer asking on how to fetch some data from a REST API in Solidity with someone answering “just use OffchainLookup”, completely missing the point of a permissionless environment.

But a naive developer can do this *right now* without EIP 3668. They can fetch data from a URL and supply it as an argument to a smart contract function.

 hyperbart:

> The input won’t even be shown as an input on Etherscan, it’s a “hidden” input that you need to look for in the source code.

If you’re sending a transaction using EIP 3668, it will show up as input on Etherscan.


*(2 more replies not shown)*
