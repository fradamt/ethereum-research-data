---
source: magicians
topic_id: 1491
title: ERC-1456 - Address Metadata JSON Schema
author: pedrouid
date: "2018-09-28"
category: EIPs
tags: [metadata, erc-1456]
url: https://ethereum-magicians.org/t/erc-1456-address-metadata-json-schema/1491
views: 3422
likes: 12
posts_count: 9
---

# ERC-1456 - Address Metadata JSON Schema

A EIP for JSON schema for storing metadata associated to Ethereum addresses.

Ethereum addresses have related information (metadata) useful to users and developers. This metadata is captured by third parties and not accessible through an on-chain mechanism.

The Registry makes address metadata available to applications and users through a registry contract that maps the addres to a JSON file stored on IPFS.

A working prototype is available at: [https://ethregistry.org](https://ethregistry.org/).


      [github.com](https://github.com/eth-registry/EIPs/blob/EIP-1357-Address-Metadata/EIPS/eip-1456.md)




####

```md
---
eip: 1456
title: Address Metadata JSON Schema
authors: Alexander Mangel , Pedro Gomes

type: Standards Track
category: ERC
status: Draft
created: 2018-09-17
discussions-to: https://ethereum-magicians.org/t/erc-1456-address-metadata-json-schema/1491
---

## Address Metadata JSON Schema

## Summary

A standard JSON specification for metadata associated to Ethereum addresses.

## Abstract

Ethereum addresses have related information (metadata) useful to users and developers. This metadata is captured by third parties and not accessible through an on-chain mechanism.
```

  This file has been truncated. [show original](https://github.com/eth-registry/EIPs/blob/EIP-1357-Address-Metadata/EIPS/eip-1456.md)








This EIP allows us to not rely on third-party services to query metadata about a smart contract and also verify the smart contract ABI and Source Code that would be provided by the Dapp developer through an on-chain registry to be submitted on IPFS

PR: https://github.com/ethereum/EIPs/pull/1456

## Replies

**jpitts** (2018-09-28):

Really great idea [@pedrouid](/u/pedrouid), it is important that this key data is available! Once this kind of metadata is present and commonly used, then new layers will be made possible. Currently, contracts and addresses are in data silos.

A question: would you be open to adopting the JSON-LD format for this?

This approach would enable the format to be more easily defined and validated by present tools. Secondly, it encourages [data modeling](http://www.markus-lanthaler.com/research/model-your-application-domain-not-your-json-structures.pdf). And possibly most important of all, JSON-LD is designed to extend and be extended, enabling implementers to easily interconnect / reference other JSON-LD files stored on IPFS.

[JSON-LD project website](https://json-ld.org/)

[Wikipedia article on JSON-LD](https://en.wikipedia.org/wiki/JSON-LD)

---

**pedrouid** (2018-09-28):

Thanks [@jpitts](/u/jpitts), huge props to [@Cygnusfear](/u/cygnusfear) to get this initiative started when we are discussing solutions for WalletConnect as he came across this issue with his own project Ethtective

I think [@pelle](/u/pelle) mentioned JSON-LD when we last spoke about this EIP, I think that we could we easily adapt the schema.

Also curious to hear from everyone who gave their input on the previous thread I discussed something similar as I think this correlates greatly. cc [@Dobrokhvalov](/u/dobrokhvalov) [@johba](/u/johba) [@Recmo](/u/recmo) [@tjayrush](/u/tjayrush) [@boris](/u/boris)



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png)
    [Human-readable Machine-verifiable Transaction requests](https://ethereum-magicians.org/t/human-readable-machine-verifiable-transaction-requests/750) [Council Sessions](/c/protocol-calls/council-sessions/15)



> This is a follow up to the discussions about Human-readable Machine-verifiable Transaction requests from FEM Berlin Council from last weekend which are related to the EIP-1138 and ERC-681 and also Radspec implementation.
> EIP-1138: Human-Readable Transaction Requests
> https://ethereum-magicians.org/t/eip-1138-human-readable-transaction-requests/565
> ERC-681: Representing various transactions as URLs
> https://ethereum-magicians.org/t/erc-681-representing-various-transactions-as-urls/650
> Radspec …

---

**boris** (2018-09-28):

+1 to JSON-LD — we need to be careful to not get trapped on “Ethereum Island”.

---

**tjayrush** (2018-09-28):

I think this is a good idea, but I have a comment or two.

This is probably related to your idea: https://solidity.readthedocs.io/en/v0.4.25/metadata.html?highlight=swarm. Is that what the ‘swarm’ address is in the `contract` data struct?

Also, I wonder if it’s a good idea to duplicate data such as decimals under the ERC20 section of standards. Totally understand why you would need that info, but if you have the contract address, can’t you just ask the contract directly for its ticker and decimals?

Also, this EIP (https://github.com/ethereum/EIPs/issues/820) might give you what you need from the ‘standards’ section. Again, probably better to point to that capability as opposed to duplicating the data.

Two reasons to not duplicate the data: (1) Ethereum data is already really big, (2) duplicated data is harder to keep accurate.

---

**Cygnusfear** (2018-10-04):

Hi everyone!! Thanks for the great responses. It would be awesome to be able to access this type of information without having to depend on API silos.

I am looking into JSON-LD. When I try the examples in the playground (https://json-ld.org/playground/ > recipe) the @context in the example leads me to a dead link for the schema. Is it possible to avoid such a situation by hosting the JSON-LD context as a separate file on IPFS and link to that in @context? If anyone is more familiar with the LD specification it would be great to have some guidance and support drafting up the context document [@jpitts](/u/jpitts) [@boris](/u/boris).

[@tjayrush](/u/tjayrush) I agree ERC820/165 is superior for getting contract interface implementations, where implemented. I am assuming superior ways of retrieving which interfaces are implemented or other new ERCs will be preferred over manually submitting data, thus over the course of time superseding parts of the spec.

This is why I added the ‘standard specific data’. In ERC20 `decimals()` and `symbol()` are both optional functions. The referenced metadata repositories (ie https://github.com/MetaMask/eth-contract-metadata/blob/master/contract-map.json) inspired me to allow contracts to supplement missing interface implementations/data.

Sometimes this is information that is supplemented in hindsight. Another example would be the ‘logo’, which is something that Tokens may want to make available but not part of the specification.

---

**jpitts** (2018-10-04):

A key weakness in JSON-LD (and the Semantic Web and Web in general) is that a link to a schema or other critical resource can become broken! This encourages centralization of schema definitions in order to better guarantee continued access (by way of aggregating stakeholders who would raise hell should something like https://schema.org make moves to shut down).

We do need a resource w/ an ENS domain name for Ethereum dapp-related schemas in order to address the uncertainty about broken links to dependencies. I had considered this last year, thankfully now we’re here and can better coordinate ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=9)

I’ll keep bringing a resource for JSON-LD schemas up as the Data Ring organizes (perhaps eventually that conversation will become a Metadata Ring).

---

**ligi** (2018-10-23):

[@tjayrush](/u/tjayrush) usually I agree that data should not be duplicated. But in this case it makes sense. Sometimes you just do not have access to the chain. E.g. hardware wallets, offline signers, …

---

**TrevorJTClarke** (2018-11-16):

[@pedrouid](/u/pedrouid) Looks like I’m a little late to the party!

I really like the thought and direction on this! So here are a few thoughts:

(Apologize in advance for formatting ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) )

1. Is there a need for cataloging/allowing blockchain specific data? Couple use cases:
– When a client requests meta for an address, they may not know which blockchain or network it belongs to, if there was some way to signify it would all the client to respond with a better initial connection for the user. Ex: User is connected to mainnet ethereum, navigates to an address that only exists on rinkeby, which would return rinkeby related meta. The client could then change its connection to rinkeby.
– Second idea: If/when there is better inter-blockchain support, there should be a way to allow linking/extending of meta. This would enable games or other types of clients to quickly service different types of connections at once. Ex: User is connected to mainnet ethereum where all the core transactions and Ether/Tokens are held for their wallet, upon interaction with a sidechain user transmits some type of game-specific token to be accounted for on both chains. Related meta would then need to supplement which sidechain and which token bridge/swap mechanism is possible. I realize this one is a bit farther down the line, however I think the context of extensibility is key to capture early.
–Lastly, I think there could be a new section under “reputation” where blockchain specifics could be linked or described
2. We chatted about images & image standards (thanks again for that!) Here’s a few ideas where meta could map:
– Under “metadata” looks like a simplified “logo” key exists. I think this is probably a little oversimplified and would get quickly outgrown. Maybe there could be something like “icons” which would allow for other web-spec icons or logos to exist?
– Another Idea: We talked about adding asset definitions within each of the standards, allowing for a standard url schema. This is something I am more specifically thinking about creating a new EIP for, just exploring the data model locally. If all ERC or etc mapped to an “AssetSchema”, it could standardize the way image assets (or really any media) get represented which would simplify implementation and use across wallets & dapps.
3. Questions about reputation:
– Where do the tags come from? Are they simply user created or is there a standard updatable list? My first reaction was it would be awesome if that could reference something like etherscamdb for instance.
– Reputation in general feels like a larger spec, it could be its own module of sorts, or another linked reference schema.

