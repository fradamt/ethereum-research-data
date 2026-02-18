---
source: magicians
topic_id: 4061
title: EIP-2544 ENS Wildcard Resolution
author: 0age
date: "2020-02-28"
category: EIPs
tags: [eip, ens, scaling]
url: https://ethereum-magicians.org/t/eip-2544-ens-wildcard-resolution/4061
views: 4231
likes: 7
posts_count: 7
---

# EIP-2544 ENS Wildcard Resolution

# EIP 2544 (ENS Wildcard Resolution)

author: Nick Johnson ([@arachnid](/u/arachnid)), 0age ([@0age](/u/0age))



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2544)














####


      `master` ← `dharma-eng:master`




          opened 05:55PM - 28 Feb 20 UTC



          [![](https://avatars.githubusercontent.com/u/37939117?v=4)
            0age](https://github.com/0age)



          [+111
            -0](https://github.com/ethereum/EIPs/pull/2544/files)







This EIP proposes a modification to ENS client behavior specified in EIP-137 in […](https://github.com/ethereum/EIPs/pull/2544)order to support "wildcard" resolution for subdomains in a backwards-compatible fashion.












## Simple Summary

EIP-2544 extends ENS client behavior to support “wildcard” resolution of subdomains. This is accomplished by using a parent domain’s resolver if none is set on a given subdomain.

## Abstract

The Ethereum Name Service Specification (EIP-137) establishes a two-step name resolution process. First, an ENS client takes a provided name, performs the namehash algorithm to determine the associated “node”, and supplies that node to the ENS Registry contract to determine the resolver. Then, if a resolver has been set on the Registry, the client supplies that same node to the resolver contract, which will return the associated address or other record.

As currently specified, this process terminates if a resolver is not set on the ENS Registry for a given node. This EIP extends the existing name resolution process by adding an additional step if a resolver is not set for subdomain. This step strips out the leftmost label from the name, derives the node of the new fragment, and supplies that node to the ENS Registry. If a resolver is located for that node, the client supplies the original, complete node to that resolver contract to derive the relevant records.

## Motivation

Many applications such as wallet providers, exchanges, and dapps have expressed a desire to issue ENS names for their users via custom subdomains on a shared parent domain. However, the cost of doing so is currently prohibitive for large user bases, as a distinct record must be set on the ENS Registry for each subdomain.

Furthermore, users cannot immediately utilize these subdomains upon account creation, as the transaction to assign a resolver for the node of the subdomain must first be submitted and mined on-chain. This adds unnecessary friction when onboarding new users, who coincidentally would often benefit greatly from the usability improvements afforded by an ENS name.

Enabling wildcard support allows for the design of more advanced resolvers that deterministically generate addresses and other records for unassigned subdomains. The generated addresses could map to counterfactual contract deployment addresses (i.e. `CREATE2` addresses), to designated “fallback” addresses, or other schemes. Additionally, individual resolvers would still be assignable to any given subdomain, which would supersede the wildcard resolution using the parent resolver.

Another critical motivation with EIP-2544 is to enable wildcard resolution in a backwards-compatible fashion. It does not require modifying the current ENS Registry contract or any assigned resolvers, and continues to support existing ENS records — legacy ENS clients would simply fail to resolve wildcard records.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

EIP-2544-compliant ENS clients MUST perform the following sequence when determining the resolver for a given name:

1. Apply the namehash algorithm to the supplied name as specified in EIP-137 to derive the node.
2. Call the ENS Registry contract, supplying the node as the argument to function resolver(bytes32 node) constant returns (address).
3. If an address other than the null address is returned, the client MUST use the returned address as the resolver.
4. If the null address is returned, the client MUST strip the leftmost label from the name to derive a new name.
5. If the only remaining label is a top-level domain, or if no labels remain, the client MUST refuse to interact with the resolver.
6. Apply the namehash algorithm to the new name as specified in EIP-137 to derive the parentNode.
7. Call the ENS Registry contract, supplying the parent node as the argument to function resolver(bytes32 node) constant returns (address) to determine the resolver.
8. If the null address is returned from this second request, the client MUST refuse to interact with the resolver.

In the event that a non-null resolver is located via this process, the client MUST supply the full, original `node` to the resolver to derive the address or other records. As with EIP-137, clients attempting to resolve an address via `function addr(bytes32 node) constant returns (address)` MUST refuse to interact with the returned address when the null address is returned.

### Pseudocode

```auto
function getNodeAndResolver(name) {
    // 1. Apply the namehash algorithm to supplied name to determine the node.
    const node = namehash(name);

    // 2. Attempt to retrieve a resolver from the ENS Registry using the node.
    let resolver = ENS_REGISTRY.methods.resolver(node).call();

    // 3. Use the resolver if a non-null result is returned from the registry.
    if (resolver != "0x0000000000000000000000000000000000000000") {
        return (node, resolver);
    }

    // 4. Remove the leftmost label from the name.
    const labelsWithoutLeftmost = name.split(".").slice(1);

    // 5. Do not continue if only the top-level domain (or no domain) remains.
    if (labelsWithoutLeftmost.length






####



        opened 09:57AM - 20 Sep 22 UTC



          closed 04:52AM - 25 Jan 23 UTC



        [![](https://avatars.githubusercontent.com/u/27199575?v=4)
          kliyer-ai](https://github.com/kliyer-ai)










![image](https://user-images.githubusercontent.com/27199575/191228113-39c28041-f[…]()132-4b61-b8d5-4e83b1ed40dd.png)

This is my tsconfig:
```json
{
  "compilerOptions": {
    "rootDir": "./src/",
    "outDir": "./dist/",
    "target": "ES6",
    "lib": ["ES6"],
    "esModuleInterop": true,
    "moduleResolution": "node",
    "module": "commonjs",
    "removeComments": true,
    "sourceMap": true,
    "strict": true
  },
  "include": ["./src/**/*"]
}
```












## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**Amxx** (2020-02-29):

I remember discussion this exact mechanism at the ENS meetup in Osaka (just before Devcon 5). An issue that was raised is:

*How is the parent node’s resolver supposed to know what the values for the child node are?*

There also is the issue of who has the right to set these values, considering the node they refer to might not have an owner. A usecase we consider could benefit from wildcard resolution is that of counterfactually deployed wallet accounts, before the deployment actually goes through. We believed in that case, the resolver would need to know the leftmost label + parent’s node. Having the child’s node alone would be very limited.

I’d be curious what usecases could be built with the resolution mechanism. Considering the new ENS registry allows for accelerated setup, just saving the “setResolver” transaction seems not such a great improvement if you still need to create a subnode with the right ownership anyway.

---

**0age** (2020-03-02):

I think these are all valid points, and they certainly merit discussion. The main motivating factor with this EIP is not to work out the ideal structure for wildcard resolution mechanics or ownership rights, but rather to simply enable shared, “fallback” resolvers via a modification that is as straightforward as possible to implement and that does not introduce any new interfaces, algorithms, or other new procedures.

Imagine a dApp where 10,000 users have checked out the frontend and chosen a username, but only 1,000 of those users have actually interacted with the on-chain contracts. If that project wants to support ENS for every user, they would currently need to set a unique resolver for each and every one of their users — this is a pretty extreme cost to bear when you consider that many of those users will never use the name at all.

With even *basic* wildcard resolution, this limitation evaporates. Every single user gets an ENS name right away, **for free**, and a more targeted resolver and owner can be assigned as soon as they’ve used it for the first time (for instance, this setup could happen during contract creation when deploying to the counterfactual address returned for the given subdomain).

The last leg of this process (i.e. what gets passed to the resolver) is a great area for future exploration, but the primary rationale for this EIP is pretty tightly focused on how to locate a resolver for wildcard addresses. There is a prescription for how to proceed once a resolver has been located, but this is mostly just designed to clear up any ambiguity and could be extended in future EIPS:

> In the event that a non-null resolver is located via this process, the client MUST supply the full, original  node  to the resolver to derive the address or other records.

Does an incremental approach like the one outlined here seem reasonable to you, [@Amxx](/u/amxx)?

---

**okwme** (2020-03-03):

Exciting improvement and simple solution. I remember discussion from [@ricmoo](/u/ricmoo) about further utilization of wildcards at the Osaka meetup. It might be out of scope for this topic but would be great to have a reference to it recorded here as well. Was there ever anything formally or informally written about those extensions and what the blockers were?

---

**Arachnid** (2020-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> How is the parent node’s resolver supposed to know what the values for the child node are?

It’s true that the current proposal doesn’t convey that. In my mind there are two compelling reasons to go with the current solution:

- Doing otherwise would require changing every profile (record type) of every resolver in order to support a new parameter for wildcard domains. Even then, resolvers would only get keccak256('label'), not the plaintext label.
- Most uses for the hashed label can also be achieved with the namehash of the whole name. It’s easy to go from plaintext label and parent namehash to the namehash of the child node when looking things up.

---

**briansoule** (2021-10-06):

Posting here to register my interest. Recent trends in the gas market further stress our need for wildcard resolution.

In terms of implementation, what tasks can I help with?

---

**YummyCoin** (2024-06-02):

![:call_me_hand:](https://ethereum-magicians.org/images/emoji/twitter/call_me_hand.png?v=12)Sounds Awesome

Happy Sunday

