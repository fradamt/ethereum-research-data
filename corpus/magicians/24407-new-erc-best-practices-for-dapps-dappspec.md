---
source: magicians
topic_id: 24407
title: "New ERC: Best Practices for Dapps (dappspec)"
author: oed
date: "2025-06-02"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/new-erc-best-practices-for-dapps-dappspec/24407
views: 525
likes: 34
posts_count: 21
---

# New ERC: Best Practices for Dapps (dappspec)

## Abstract

This ERC aims to standardize design choices for decentralized applications (dapps) in order to enhance censorship resistance across the ecosystem. At the core of the specification is a set of requirements and recommendations around how the dapp is hosted and distributed, as well as a set of extensions to the [Web Application Manifest](https://www.w3.org/TR/appmanifest/) W3C spec.

## Motivation

The decentralized web aims to provide applications that are resilient against censorship and single points of failure. However, many “decentralized” applications still depend on centralized infrastructure, creating vulnerabilities. This ERC addresses this by:

1. Making dependency information explicit and machine-readable
2. Providing redundancy options for critical services
3. Making critical services reusable across dapps
4. Standardizing how dapps interact with blockchain infrastructure

By following this specification, dapp developers can create applications that are more resilient, and users gain access to tools that can help bypass potential censorship.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Naming and Distribution

This section deals with how to package, publish, and distribute your dapp.

#### ENS domain

Dapps conforming to this specification MUST use an ENS domain (ERC-137) as their primary identifier. The [contenthash](https://docs.ens.domains/ensip/7) of the given ENS domain SHOULD be set to an IPFS CID (content identifier).

#### Name governance

Updating of the ENS *contenthash* for the dapp SHOULD be controlled by a multisig. The exact structure of this multisig is important, but will vary from a case to case basis, so is considered out of scope for this spec.

#### Immutable subdomains

Use of immutable ENS subdomains where `<version>.example.eth` points to a specific version of the dapp is RECOMMENDED. The version subdomain *contenthash* MUST NOT be possible to change or update after it’s set once. The version name MAY be an incremental number, e.g. `v1.example.eth`, or use semantic versioning, e.g. `v1-2-5.example.eth`.

#### Distribution Packaging

The dapp MUST be a static webpage, meaning no server is needed to access or run it. This allows it to be hosted on decentralized storage like IPFS or served from any static hosting platform.

#### Resource integrity

IPFS is the RECOMMENDED way of distributing the content, e.g. set the ENS contenthash to a CID.

IPNS is NOT RECOMMENDED.

All static resources SHOULD be contained within the directory enclosed by the aforementioned *contenthash*. This means that all media and scripts transitively loaded from loading `index.html`, or any other page MUST be contained in the content referred to by the *contenthash*.

All static resources SHOULD include a [Subresource integrity](https://www.w3.org/TR/sri/) hash where possible, e.g. on `<script>` and `<link>` tags.

### Endpoint Priority

This section describes how a dapp should prioritize different endpoints for accessing blockchain state and submitting UserOperations.

#### Ethereum RPC

The ethereum RPC is used to access blockchain state on the L1 or other EVM compatible networks (specified with chain-id). The method of access MUST be prioritized in the order defined below.

##### 1. Query Parameter Override

Dapps MUST support overriding the ethereum rpc endpoint for any chain-id using query parameters in the following format: `?ds-rpc-<CHAIN_ID>=<url>`. When provided, the dapp frontend MUST parse the URL and prioritize it over any other method of accessing chain state for the given chain-id. Note that the user may provide overrides for one or multiple chain-ids at the same time.

For example, a user may specify an endpoint for mainnet as follows:

`example.eth?ds-rpc-1=https%3A%2F%2Fmainnet.infura.io%2Fv3%2FYOUR-API-KEY`

##### 2. Injected provider

If an injected provided, i.e. `window.ethereum` is present it MUST be prioritized over all alternatives options, except the query parameter override.

##### 3. Browser based light clients

Although not widely available today, browser based light clients might become a viable alternative in the future. For now they MUST be prioritized after the injected provider, if supported by the dapp, but security and privacy implications are not well known so this might need to be adjusted in the future.

##### 4. Hardcoded RPC endpoints

Dapps MAY provide additional RPC endpoints. It is RECOMMENDED that they include multiple URLs from different providers to provide redundancy.

#### 4337 Bundlers

4337 bundlers also provides a json-rpc endpoint per chain-id. The different methods of accesing these RPCs MUST be prioritized as follows.

##### 1. Query Parameter Override

Dapps MUST support overriding bundler rpc endpoints for any chain-id using query parameters in the following format: `?ds-rpc-<CHAIN_ID>=<url>`. When provided, the dapp frontend MUST parse the URL and prioritize it over any other method of interacting with a bundler for the given chain-id. Note that the user may provide overrides for one or multiple chain-ids at the same time.

For example, a user may specify an endpoint for mainnet as follows:

`example.eth?ds-bundler-1=https%3A%2F%2Fbundler.example.com`

##### 2. P2P browser based mempool

Although no current implementation exists, in theory it could be supported by the bundler mempool p2p network. If a dapp implements such a protocol, it MUST be prioritized after the query parameter.

##### 3. Hardcoded Bundler Endpoints

Dapps MAY provide additional bundler endpoints. It is RECOMMENDED that they include multiple URLs from different providers to provide redundancy.

### Use of Web Application Manifest

Your dapp MUST have a [Web Application Manifest](https://www.w3.org/TR/appmanifest/). Just as the W3C spec [recommends](https://www.w3.org/TR/appmanifest/#using-a-link-element-to-link-to-a-manifest), use a `link` element to link to your `manifest.webmanifest` file.

#### Required Members

Fields in the web app manifest is referred to as “members”. A dapp should consider the following:

- A name member is REQUIRED
- At least one item in the icon member is REQUIRED
- A description member (as defined in the Application Info spec) is RECOMMENDED
- A screenshots member (as defined in the Application Info spec) is RECOMMENDED

#### Code Repository Extension

A dapp MUST add a `dapp_repository` member. It MUST contain a `url` pointing to the source code of the dapp. Ideally both frontend code, and any backend/indexing service if relevant.

#### History Preservation Extension

A dapp MAY add a `dapp_preserve_history` member. If present it MUST contain an integer. This value indicates how many historical versions pinning services should maintain. A value of `-1` means all historical versions should be preserved. The default value if not present is assumed to be `0`, e.g. only the current version is pinned.

A *version* here means a unique update to the *contenthash* field on the dapps ENS name, i.e. every time the *contenthash* is updated it is considered a new version. Although pinning services SHOULD follow the value specified here, there is no guarantee that they won’t store historical versions for longer.

#### Dapp Service Extension

A dapp MAY add a `dapp_service` member. If present it MUST contain an array of `urls`.

A dapp service, or dservice for short, is a backend service that provides the dapp with specialized functionality beyond what is provided through ethereum RPCs and bundlers. Each dapp MAY implement one dservice (it MUST NOT implement more than one) and it is RECOMMENDED to provide multiple endpoints for this service that are hosted on independent infrastructure (these urls are to be provided in the `dapp_service` member).

##### DService Requirements

1. MUST only rely on indexed data from blockchains (Ethereum L1/L2s) or content-addressed data
2. MUST be deterministic - all DService nodes given the same input should produce the same state
3. MUST be open source so that anyone can run their own instance
4. Dapps SHOULD provide multiple endpoints for redundancy
5. Each endpoint MUST be listed in the $dservices.self array

##### Query Parameter Overrides

If the dapp is using a dservice it MUST provide the ability to override the service endpoint with the following query parameter: `?ds-self=<url>`.

#### External Dapp Services Extension

A dapp MAY add a `dapp_external_services` member. If present it MUST contain an array of ENS domain names.

If a dapp consumes the dservice of one or multiple other dapps it MUST list the ENS names of the DServices it consumes.

For example, if dappA consumes the the dservice of dappB, it MUST list `dappB.eth` in the `dapp_external_services` array. This SHOULD be implemented in dappA by first fetching the Web Application Manifest from `dappB.eth` to get the latest endpoints for its dservice, then query those endpoints directly.

##### Query Parameter Overrides

If the dapp is using external dservices, it MUST provide the ability to override each of them using the following query parameter: `?ds-<ens-name>=<url>`

#### Auxiliary Services Extension

If a dapp is using any additional endpoints besides RPCs, Bundlers, or DServices, they MUST be listed in the `dapp_auxiliary_services` member. If present it MUST contain an array of objects, with the following schema:

```typescript
interface Auxiliary {
  /*
   * A description of what this service is used for
   */
  motivation: string;

  /*
   * A list of domains required to make use of the functionality described
   */
  domains: string[];
}
```

The `dapp_auxiliary_services` array lists domains for non-essential services that the dapp uses but aren’t critical to its core functionality:

- Analytics platforms
- WalletConnect, or similar wallet connectivity approach
- Monitoring services
- Feature flagging services
- Non-critical API integrations

The dapp MUST list all auxiliary service domains it utilizes.

#### Contracts Extension

A dapp MAY add a `dapp_contracts` member. If present it MUST contain the chain-id and addresses of contracts which the dapp supports interacting with. The `dapp_contracts` must be an array of objects with the following schema:

```typescript
interface Contract {
  /*
   * The chain id for the blockchain which the contract is deployed on.
   */
  chain_id: string;

  /*
   * The address of the smart contract.
   */
  address: string;
}
```

#### Example manifest.webmanifest

To get a sense of what a manifest file might look like, here’s an example:

```json
{
  "name": "ExampleDapp",
  "description": "Just a simple example dapp",
  "icons": [
    {
      "src": "favicon.webp",
      "sizes": "any",
      "type": "image/webp"
    }
  ],
  "screenshots": [{
    "src": "images/screenshot.png",
    "sizes": "800x600",
    "form_factor": "wide",
    "label": "With ExampleDapp you can try many different decentralized things"
  }],
  "dapp_repository": "https://github.com/example-org/example-dapp",
  "dapp_preserve_history": -1,
  "dapp_service": ["https://example.com", "https://example.org"],
  "dapp_external_services": ["other-example.eth"],
  "dapp_auxiliary_services": [{
    "motivation": "Required by the token search widget to display token names, prices and icons",
    "domains": ["live.crypto-prices.com", "token-icons.com"]
  }],
  "dapp_contracts": [{
    "chain_id": 1,
    "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
  }]
}
```

## Rationale

This specification is designed to highlight design choices necessary to build truly resilient applications.

### Naming and Distribution Recommendations

While ENS supports other protocols. IPFS is recommended because:

- It has wide adoption
- Can be run locally and well packaged dapps can be persisted completely offline
- Has no token dependencies
- Standardizing on one protocol simplifies ecosystem tooling

IPNS is not recommended because:

- Content can change at any time at the key holder’s discretion
- There is no persistent log of changes, unlike publishing CIDs directly on-chain
- There is no simple way to create stronger governance mechanism around updating the CID

Containing all static resources within the contenthash is necessary because any resource loaded from a third party server poses a privacy or even security risk.

Subresource integrity checks are recommended because ENS gateways (such as eth.limo / link / sucks / ac) could in theory serve malicious content since IPFS hashes of subresources are not verified by these gateways (note that this is not the case for the in browser IPFS gateway at [inbrowser.link](https://inbrowser.link/))

The ENS contenthash updates that happens onchain should ideally be controlled by as strict of a governance process as possible. The exact approach will vary on a case to case basis. This ERC recommends using a multisig to provide a baseline. Ideally approaches where permanent versions of dapps are hosted on subdomains, e.g. `<version>.mydapp.eth` is used as well.

### RPC and Bundler Priority

By specifying a priority for Eth RPCs and Bundler endpoints dapps can provide users with both redundancy in case underlaying services go down, but also a way to increase privacy by letting users specify their own custom endpoints. User might run their own nodes, or trust certain providers to not exploit their data. By prioritizing `window.ethereum` the choice of rpc gets outsourced to the browser or wallet, which is a choice the user already has made and in general should be better than the arbitrary choice of provider that the dapp makes.

### Web Application Manifest Members

The `name` and `icon` are necessary if you want to enable the dapp to be installed as a PWA (Progressive Web Application). Additionally the `description` and `screenshots` provide useful information to dapp explorers or wallets that want to show more information about the app to the user before they decide to open it. The same is true for `dapp_repository` as it can be used to build trust between the user and developer.

The `dapp_preserve_history` is useful to help dapp pinning services to know how to persist old versions of your dapp. Currently most IPFS pinning services have no way of dealing with this.

#### Why are DServices needed?

The introduction of the *dservice* concept is an acknowledgement that most applications need to rely on some sort of indexer to access blockchain data. The ethereum rpc api is simply not sophisticated enough for advanced query functionality. Unfortunately most applications simply build a backend indexer and call it a day. If their endpoint goes down the application goes down with it, losing the benefit of distributing the frontend over ENS and IPFS in the first place. DServices mitigates this by allowing apps to specify multiple backups. Additionally since the dapp is required to support the dservice fallback query param, even if all provided endpoints go down, users can run their own indexer as a last resort.

Another benefit of dservices is that they can become a canonical way for dapps to expose backend apis. By allowing dapps to define other ENS names as `$dservices.external`, infrastructure can be shared across multiple dapps. For example, `dappA.eth` can expose a dservice with three backing endpoints, `dappB.eth` can now consume the dservice of Dapp A by resovling `dappA.eth/.well-known/dappspec.json` and using the resolved urls to make requests. Dapps could even implement payment or subscription services where they charge other dapps to consume the default endpoints.

#### Auxiliary services

By default dapp browsers, or browser extensions may choose to block any requests made to arbitrary services in order to improve security and user privacy. By listing domains of auxiliary services the dapp uses along with a description, browsers could give users the ability to selectively approve certain services.

#### Contracts

While listing the addresses of smart contract your dapp interacts with is by no means necessary, it could provide users with additional information if the dapp is listed in some sort of dapp explorer. For example, a user might want to search for apps that affords them to interact with a certain contract.

## Backwards Compatibility

Adding a `dappspec.json` or following the requirements provided by this ERC should be completely backwards compatible with existing dapps.

## Reference Implementation

```txt
TODO - this section is out of date
```

These two applications conform to the specification in the ERC:

- dapprank.eth - manifest.webmanifest
- justw.eth - manifest.json (there’s currently a bug in Safe where it doesn’t accept manifest.webmanifest, or read manifest from the link tag)

Additionally [dapprank.eth](https://dapprank.eth.link) benchmarks applications based on how well they follow this specification (as well as further in depth, per dapp analysis).

## Security Considerations

Even though a dapp provides a valid `manifest.webmanifest` file doesn’t mean its implementation actually provides the functionality it claims. Browsers or extensions that wish to utilize this ERC needs to take this into consideration. It’s also possible for third party evaluation tools to analyze the claims made by a dapp in its `manifest.webmanifest` and how well it conforms to this spec in general.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**adamstallard** (2025-06-05):

A couple of typos I spotted: ingegrity should be integrity, and loosing should be losing.

---

**devanoneth** (2025-06-07):

This is awesome [@oed](/u/oed), thanks for proposing this. Gathering some feedback below, based on my experience building Eternal Safe (link removed because I cannot post links apparently).

1. In the Typescript interface for the Manifest Schema, you’ve left out $dservices.serviceWorker.
2. $chains.contracts: I’m curious how you see this working with factory contracts which deploy contracts that the Dapp may ultimately interact with. e.g. a unique Safe Wallet or a Uniswap Pair. Obviously, not all of these contracts could be known / listed. The Dapp could load these from factories, but really I’m not sure how helpful this manifest section would be when a lot of onchain interactions can happen with contracts which are dynamically provided / retrieved.
3. With regards to the DService concept, I’m worried that it could be a very easy way to start to reintroduce centralized components into otherwise decentralized apps. I think even just a decentralized frontend is already a step in the right direction, but with Eternal Safe, I’ve been extremely careful to not include any backend services (often at the cost of UX). I don’t think we should prescribe any one solution, but I have been working on a Safe Subgraph (link removed because I cannot post links apparently) which, in theory, would allow for better querying of onchain data via The Graph Network. I guess here I’m really ranting that there is no ubiquitous solution for this, that’s really Ethereum native, but The Graph is close. Maybe we could in future work on a DService standard which covers probably 80% of what is needed without leaking into centralized solutions.
4. Fallbacks: I think query parameter fallbacks are a great idea for the overrides, but should just always be supported, and not optional in the manifest, rather a requirement of all dappspec-following dapps. i.e. if they are set, they are used.
5. Completely agree regarding IPNS being NOT RECOMMENDED.
6. I think versioning subdomains should be RECOMMENDED, and follow a standard. With Eternal Safe, I’ve set two subdomains ((link removed because I cannot post links apparently),  v0 and v1. I think v followed by a simple auto-incrementing integer for each released / decentralized deployment is very efficient, scalable and readable. It works well with domain names and is immediately obvious to humans.

Thanks again for the work on this, happy to help where I can! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**oed** (2025-06-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/devanoneth/48/15399_2.png) devanoneth:

> $chains.contracts: I’m curious how you see this working with factory contracts which deploy contracts that the Dapp may ultimately interact with. e.g. a unique Safe Wallet or a Uniswap Pair. Obviously, not all of these contracts could be known / listed. The Dapp could load these from factories, but really I’m not sure how helpful this manifest section would be when a lot of onchain interactions can happen with contracts which are dynamically provided / retrieved.

Good point. Is it possible to know if a contract was created by a specific factory? I assume that would be non-trivial. Maybe this section should be made entirely optional then? Or maybe allow for specifying the abi interface used to interact with contracts?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/devanoneth/48/15399_2.png) devanoneth:

> With regards to the DService concept, I’m worried that it could be a very easy way to start to reintroduce centralized components into otherwise decentralized apps. I think even just a decentralized frontend is already a step in the right direction, but with Eternal Safe, I’ve been extremely careful to not include any backend services (often at the cost of UX). I don’t think we should prescribe any one solution, but I have been working on a Safe Subgraph (link removed because I cannot post links apparently) which, in theory, would allow for better querying of onchain data via The Graph Network. I guess here I’m really ranting that there is no ubiquitous solution for this, that’s really Ethereum native, but The Graph is close. Maybe we could in future work on a DService standard which covers probably 80% of what is needed without leaking into centralized solutions.

Thanks for this feedback, DServices is indeed the most novel concept introduced here. Correct me if I’m wrong, but The Graph actually could be seen as a centralization vector as well because it’s not trivial to run your own node / gateway?

The reason I wanted to include DServices was that it seems fairly common that a dapp needs customized indexing. For example, one dapp I’ve been working on recently require IPFS synchronization of data in the background, while another requires vector embeddings over on-chain data.

So I do think there is a worthwhile compromize to allow dapps to introduce these sort of services, as long as:

1. It’s open source and freely available
2. It’s deterministic (e.g. eventually consistent) based on on-chain data and content-addressed data

Note that in this light The Graph could potentially be considered a DService that you could use in your dapp.

Also consider that DServices could be further decentralized using re-staking services once they become more mature.

Finally, ofc the use of DServices is by no means required!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/devanoneth/48/15399_2.png) devanoneth:

> Fallbacks: I think query parameter fallbacks are a great idea for the overrides, but should just always be supported, and not optional in the manifest, rather a requirement of all dappspec-following dapps. i.e. if they are set, they are used.

Great point, not sure why I didn’t consider this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/devanoneth/48/15399_2.png) devanoneth:

> I think versioning subdomains should be RECOMMENDED, and follow a standard. With Eternal Safe, I’ve set two subdomains ((link removed because I cannot post links apparently), v0 and v1. I think v followed by a simple auto-incrementing integer for each released / decentralized deployment is very efficient, scalable and readable. It works well with domain names and is immediately obvious to humans.

Makes sense to make it RECOMMENDED. About enforcing a version scheme, I wonder if this could be a bit too descriptive? I could imagine someone wanting to use semantic versioning for example. I see how slowly incrementing numbers makes a lot of sense for Eternal Safe because it’s not deployed very frequently. In dapps with more frequent updates like WalletBeat or DappRank, this makes a bit less sense.

---

**polymutex** (2025-06-08):

First, thanks for working on this, I think such a standard is a necessary step

towards establishing a standardized ecosystem for secure frontends.

As meta-feedback, I suggest writing the comments inline on top of each field

of the TypeScript-ish `interface`. Much easier to follow than to have to

look back and forth between the explanation for each field and the structure

of the `interface`. It would also be helpful to link to a working example for

a full-featured dapp frontend that has an IPFS version with dependencies,

like Eternal Safe or Uniswap.

A few pieces of feedback.

- It seems to me like dappspec files should be onchain, not part of the
frontend files themselves. Since dapps already have an ENS name, and
onchain data (like ENS records) are verifiable via light clients, it
would be very useful to be able to also verify the integrity of a
dapp’s dappspec manifest by retrieving it onchain. As a possible
implementation, the dappspec can be posted onchain as an ERC-5219
contract, and the dapp’s ENS name can have a dappspec custom record
that points to the address of that ERC-5219 contract.
I agree that if the app is on IPFS and the ENS record points to an
immutable CID, then the dappspec file’s integrity is already preserved;
but putting the manifest onchain still means you get other things for
free, such as observable version history, data availability of the
manifest itself, and censorship-resistant updates.
- Putting the manifest onchain may also have interesting composability
uses, whereby you could have an onchain manifest refer to other dapps’
onchain-versioned manifests as dependencies, instead of referring to
them via ENS names (which are mutable). For example, dapp1.eth
version A could depend on dapp2.eth’s version A, and whoever owns
the dapp2.eth name can’t rug dapp1.eth users by releasing a
compromised version B of dapp2.eth.
- preserveHistory doesn’t make a lot of sense unless the manifest itself
is onchain. This is because there won’t necessarily be an event that
can reliably make all participants notice that a new version of a dapp
has been released. So a “number of historical versions” means different
things to different observers. I suggest instead that with onchain
dappspec files, preserveHistory can be expressed more precisely as a
rotating set of block numbers (or block hashes), where each dapp update
adds one and prunes another from this list.
- Representing chain dependencies as strings and RPC provider URLs
(which are presumably centralized) seems like a centralizing force, and
remove end user control from this decision. I feel like this could just
be a list of registered chain IDs. Let the wallet handle the decision of
what RPC provider to use for that chain.
- Query parameter fallbacks seem incompatible with immutable frontends on
IPFS, where there is no server that can dynamically change the served
content of the page (which is presumably how such endpoint overrides would
come into play). This means that the dapp would either not support
overwritability of its RPCs/bundlers/etc endpoint if running in immutable
mode, or that there would need to be JavaScript code that parses the URL
and adjusts its chain client configuration accordingly. This seems
error-prone (easy for implementations to accidentally miss). It also means
that sharing URLs to dapps now also bears security implications, because
you could be clicking on a dapp URL that you trust the ENS name of but for
which the overwritten RPC URLs are compromised versions (via
typosquatting). I’d recommend simply not letting dapps be able to specify
or contact chain RPC providers at all. They can simply use the browser
wallet provider instead, which the user is in control of, which the user
can configure to have a light client, to go through proxies to control
metadata privacy leaks, etc.
- If query parameter for setting provider URLs are to be implemented, I
believe they should be required, not “fallbacks” or optional. To use
the dapp-“default” provider URLs should be explicit and obvious to the
user, such as by requiring a URL parameter like
?use-default-ds-rpc-=true.
- URLs as strings is rather restrictive and verbose. I would suggest replacing
them with domain names only. This also makes it easier to present to the
user, for example by asking “do you want to allow this dapp to reach out to
crypto-prices dot com (claimed purpose: fetching price data)?” yes/no.
This is easier for the user to understand than “do you want to
allow this dapp to reach out to
https://cryptoprices.com/api/v1/fetch?from=0xaddress1&to=0xaddress2?”.
There could also be multiple domains for a single purpose, so that users
can approve them as a unit. For example, for a frontend like Uniswap:

```auto
{
    auxiliary: [
        {
            motivation: 'Required by the token search widget to display token names, prices and icons',
            domains: ['live.crypto-prices.com', 'token-icons.com'],
        },
        {
            motivation: 'Required to fetch historical crypto prices and display them on a chart',
            domains: ['history.crypto-prices.com'],
        },
    ],
}
```

---

**Ankita.eth** (2025-06-09):

I’ve been reviewing the proposed DappSpec ERC and appreciate its intent to make dapps more resilient and decentralized using the `dappspec.json` manifest format. I have a few questions and suggestions to clarify parts of the spec and explore implementation challenges. Hoping to gather feedback from other developers, spec authors, and infrastructure teams.

---

**1. Best Practices for DService Scalability**

How can developers ensure DServices remain deterministic, performant, and scalable across multiple independently hosted endpoints, especially for complex data indexing? Are there recommended frameworks (e.g., based on The Graph, IPFS, or custom solutions) to simplify implementation?

**2. Security of Query Parameter Fallbacks**

What are the best practices to validate and secure query parameter-based fallbacks (e.g., `?ds-rpc-1=https...`) against malicious injections or phishing risks? Could the spec recommend signature validation, domain allowlists, or other protections?

**3. Ecosystem Tooling & Adoption**

Are there plans for developer tooling (e.g., schema validators, dappspec.json generators, CI integrations) to support adoption? Also, could wallet providers and dapp browsers leverage the manifest to improve privacy, trust, or endpoint control?

**4. Suggestion: Decentralized DService Registry**

Could the DappSpec standard consider supporting a decentralized registry or marketplace for DServices? This would help dapps discover reusable external services (listed in `dservices.external`) and reduce redundant infrastructure across the ecosystem.

**5. User Experience of Fallback Mechanisms**

Fallbacks via query parameters and `window.ethereum` support are great for resilience, but can be complex for users. Are there any recommended UI/UX patterns or helper libraries to surface these options safely and intuitively to end-users?

**6. IPFS/ENS Performance and Governance**

Fetching `dappspec.json` via ENS and IPFS could introduce latency. Are caching strategies or resolver optimizations being considered? Also, could the spec include a template for managing ENS contenthash rotation via multisig or subdomain versioning?

---

**oed** (2025-06-09):

Thanks for the thoughful feedback [@polymutex](/u/polymutex). Going to update the interface based on your suggestion.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polymutex/48/13290_2.png) polymutex:

> I agree that if the app is on IPFS and the ENS record points to an
> immutable CID, then the dappspec file’s integrity is already preserved;
> but putting the manifest onchain still means you get other things for
> free, such as observable version history, data availability of the
> manifest itself, and censorship-resistant updates.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polymutex/48/13290_2.png) polymutex:

> Putting the manifest onchain may also have interesting composability
> uses, whereby you could have an onchain manifest refer to other dapps’
> onchain-versioned manifests as dependencies, instead of referring to
> them via ENS names (which are mutable).

I actually considered putting the dappspec content on-chain before I landed on the `.well-known/dappspec.json` approach. You can actually get all properties you mentioned above (except data availability) with ENS + IPFS:

1. Observable version history - through the history of your ENS record
2. Censorship resistance - IPFS has proven itself to be quite censorship resistant in real-world scensarios
3. Immutable onchain-versioned manifests - you get this if you are doing immutable version subdomains, e.g. v1.mydapp.eth, which @devanoneth rightly suggested should be RECOMMENDED

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polymutex/48/13290_2.png) polymutex:

> preserveHistory doesn’t make a lot of sense unless the manifest itself
> is onchain. This is because there won’t necessarily be an event that
> can reliably make all participants notice that a new version of a dapp
> has been released. So a “number of historical versions” means different
> things to different observers.

Ah, yes this is for sure underspecified. My intention here is that each update to the *contenthash* ENS record is a “version”. So it should be trivial for a pinning service to index ENS contracts and see the version history.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polymutex/48/13290_2.png) polymutex:

> If query parameter for setting provider URLs are to be implemented, I
> believe they should be required, not “fallbacks” or optional.

Yeah, I’m thinking the change should be something like this:

1. Query param rpc/bundler MUST be used and prioritized
2. window.ethereum MUST be used and prioritized if present (although (1) still takes priority above it).

Btw, you are correct in that the query params needs to be handled by frontend javascript code.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polymutex/48/13290_2.png) polymutex:

> Representing chain dependencies as strings and RPC provider URLs
> (which are presumably centralized) seems like a centralizing force, and
> remove end user control from this decision. I feel like this could just
> be a list of registered chain IDs. Let the wallet handle the decision of
> what RPC provider to use for that chain.

Hm, a few things to consider here:

1. I believe window.ethereum only serves one chain-id at a time?
2. Dapps need to have some RPC connection if there isn’t a window.ethereum object
3. Wallet connection isn’t initialized, e.g. if wallet is on different network, a network switch request pops open a wallet modal

However, similar to the discussion on contracts from above I’m not sure listing RPC urls actually provides much value. Maybe listing only domains similar to what you suggested for the auxiliary endpoints could make sense as well?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polymutex/48/13290_2.png) polymutex:

> I would suggest replacing
> them with domain names only.

Yup, this makes sense!

---

**oed** (2025-06-09):

Updated the OP based on the feedback from [@devanoneth](/u/devanoneth) and [@polymutex](/u/polymutex):

Main changes:

- Made priority of RPC/Bundler endpoints more prevalent up front
- Removed the chains section as it’s value proposition was unclear

---

**oed** (2025-06-09):

Upon further analysis it might make sense to merge what is now in `.well-known/dappspec.json` into the more general [Web Application Manifest](https://www.w3.org/TR/appmanifest/), since it already supports [extensions](https://www.w3.org/TR/appmanifest/#extensibility).

Furthermore, having a webapp manifest is likely something that should be a requirement for dapps anyway.

---

**oed** (2025-06-10):

Update the OP to use [Web Application Manifest](https://www.w3.org/TR/appmanifest/). Items unique to this spec is now listed as top level “members” in this manifest using the `dapp_*` prefix.

Added back the contract section, since I still think it could be helpful (see rationale).

---

**polymutex** (2025-06-12):

I am rethinking the usefulness and drawbacks of the RPC URL provider overrides via URL parameters. Consider the following scenario:

- A dapp’s default RPC provider is down one day
- Someone complains about it on some social website
- Someone else responds with a URL that has a ?ds-rpc-1=... with an alternate RPC that works, say https://mydapp.eth?ds-rpc-1=https%3A%2F%2Fmy-ethereum-node.tld. The link is shortened as “mydapp.eth?ds-rpc-1=https%3A...” on the social media site, because social media sites hate links (lol)
- The link spreads around because it does fix the issue for people.
- Over time, the practice of clicking on such links becomes normalized.
- Time passes. Attacker registers the domain my-ethereum-n0d3.tld.
- Attacker starts posting links to https://mydapp.eth?ds-rpc-1=https%3A%2F%2Fmy-ethereum-n0d3.tld, which get shortened to the same thing (“mydapp.eth?ds-rpc-1=https%3A...”).
- Attacker eventually switches the behavior of my-ethereum-n0d3.tld to return malicious answers because it knows mydapp.eth doesn’t implement an in-browser light client.
- People are tricked into signing transactions with unintended effects, etc.

Basically my larger point is that the ability of RPC URL overrides via URL parameters, especially if they are prioritized above injected providers, creates a new security exploit vector via either typosquatting or simply by user inattention, for a user to be browsing a legitimate `mydapp.eth` yet still be tricked into using a malicious RPC endpoint.

Is there a good use-case for allowing such overrides that is worth adding this risk?

And if so, should these overrides still be prioritized over injected providers?

---

**oed** (2025-06-12):

I’m open to potentially making the injected provider the top priority. Don’t yet feel strongly here.

Can you explain a bit more how a malicious RPC endpoint could cause any more problems than leak users privacy? I’m not really sure how it could trick the user into signing something malicious?

Btw, would love your thoughts on how Helios might be useful here?

---

**polymutex** (2025-06-12):

A malicious endpoint can lie about chain state, which can be used to trick the dapp to display incorrect information, which then leads the user into signing something that, when broadcast onto the actual chain, has unintended effects.

Simple example: NFT marketplace dapp. The malicious endpoint lies about the prices that an NFT collection has recently been selling for. The dapp, none the wiser, displays these low prices. The user has an NFT from this collection they want to sell. So they see these prices and list their NFT for sale at a price way below actual market prices, and then their NFT gets sniped for peanuts. Attacker then resells the NFT for actual market prices, and pockets the difference.

Even without maliciousness, the endpoint also has first dibs on orderflow and MEV extraction as well in case it is used for transaction simulation/broadcast (which would probably be the case if the dapp uses an embedded wallet). So that incentivizes folks to spread around dapp URLs with their specific endpoints as URL parameters, so that they can extract more.

> how Helios might be useful here?

Light clients solve the “lying about chain state” problem, so definitely worth encouraging, but they don’t solve the privacy/MEV problems.

---

**oed** (2025-06-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polymutex/48/13290_2.png) polymutex:

> Light clients solve the “lying about chain state” problem, so definitely worth encouraging, but they don’t solve the privacy/MEV problems.

So how about this priority?

#### Eth RPC

1. Injected provider
2. P2P browser light client
3. Query parameter
4. Hardcoded endpoints

Here (3) and (4) are ideally verified w/ helios or similar light-clientish.

#### 4337 bundlers

1. P2P browser based mempool
2. Query parameter
3. Hardcoded endpoints

---

Another possible requirement that could be added is that dapps must display some sort of warning modal when a query param is provided.

---

**willscott** (2025-06-16):

# Re: Resource integrity

> All static resources SHOULD include a Subresource integrity hash where possible, e.g. on  and  tags.

if the resource is relative to the page / also distributed within or via a content addressed envelope, then this additional complexity seems to be a temporary security issue that should be handled by upgrading the gateways, rather than a burden that should be placed on the dapps

# Re: Etherum RPC

> If an injected provider, i.e. window.ethereum is present it MUST be prioritized over all alternatives options

I think options like Rainbow that detect the injection provider, but allow the user to connect via that or wallet connect or other options rather than directly prioritizing that provider still seem to have widespread acceptance. There’s probably a slightly amended wording here of ‘it needs to be at least as high priority’.

# Re: Code Repository Extension

If there isn’t a standard or validation / reproducibility from the code it’ll be pretty hard to ensure this part of the standard is met. It might be useful to have at least a recommendation of a best practice here if any are emerging for reproducibility of the dapp from the source.

# Re: Dservice

What do we get by having the declarative manifest of the services? is the intention that it provides a space for browsers to fail over to alternative providers? Having a clear description of “what is being achieved” through the standard will help here, and i had trouble infering it from the ERC.

---

**polymutex** (2025-06-19):

Makes sense to me!

Agreed that applications should display some sort of warning when using a query param; I think they would want to do that anyway as a sort of disclaimer (“[dapp] is not responsible for [thing] that may happen as a result of using [overridden provider]…”)

---

**oed** (2025-06-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polymutex/48/13290_2.png) polymutex:

> It seems to me like dappspec files should be onchain, not part of the
> frontend files themselves.

I’ve been thinking over this as I’ve been prototyping an application that uses the DService of another ENS domain. For convenience I think that the DService urls in particular SHOULD be stored as a ENS text record. This means that DServices could be standardized independently as an ENSIP, similar to [ENSIP-12: Avatar Text Records | ENS Docs](https://docs.ens.domains/ensip/12).

The reason for this is that in practice it’s easier to fetch a record from an ENS record for another app, than to also fetch the IPFS content under that ENS name.

**In the case of dservice urls in manifest.webmanifest:**

1. Call ENS universal-resolver to get contenthash from example.eth
2. Fetch index.html from IPFS and find the manifest header property
3. Fetch the manifest file from IPFS

Here the question of how we would fetch data from IPFS arises. We could use [Helia verified fetch](https://github.com/ipfs-examples/helia-browser-verified-fetch), but it introduces certain centralization vectors into your app.

Another approach would be to fetch the manifest file with a single https request to one of the ENS mirrors, e.g. *.eth.limo*, but this is another obvious centralization vector.

**In the case of dservice urls in a ENS text record:**

1. Call ENS universal-resolver to get dservice text record

This is obviously much better since we already have an assumption that we are using an ethereum rpc in either case.

---

Besides DServices however, I still think using the already existing webmanifest standard makes more sense.

---

**oed** (2025-06-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/willscott/48/15442_2.png) willscott:

> if the resource is relative to the page / also distributed within or via a content addressed envelope, then this additional complexity seems to be a temporary security issue that should be handled by upgrading the gateways, rather than a burden that should be placed on the dapps

Can you elaborate on this? It is more of a security precaution in case one existing gateway gets compromised in some way. No one in the ecosystem can’t have control over all gateways.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/willscott/48/15442_2.png) willscott:

> I think options like Rainbow that detect the injection provider, but allow the user to connect via that or wallet connect or other options rather than directly prioritizing that provider still seem to have widespread acceptance. There’s probably a slightly amended wording here of ‘it needs to be at least as high priority’.

To be clear, what we are talking about here is more the part of the RPC that is used to access chain state, i.e. read data. Which RPC is used for making transactions obviously has to use the order you mentioned above.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/willscott/48/15442_2.png) willscott:

> If there isn’t a standard or validation / reproducibility from the code it’ll be pretty hard to ensure this part of the standard is met. It might be useful to have at least a recommendation of a best practice here if any are emerging for reproducibility of the dapp from the source.

I would love for something like this to exist ![:smirk:](https://ethereum-magicians.org/images/emoji/twitter/smirk.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/willscott/48/15442_2.png) willscott:

> What do we get by having the declarative manifest of the services? is the intention that it provides a space for browsers to fail over to alternative providers? Having a clear description of “what is being achieved” through the standard will help here, and i had trouble infering it from the ERC.

It’s more of an architectural design that encourages developers to not lock their users into a particular backend deployment. But it also enables apps to leverage backend/indexing systems of other apps (also see my previous post above).

---

**willscott** (2025-07-01):

regarding the case of relative resources:

The case I’m referring to is an HTML file including ‘./script.js’, and that directory is then packaged as the content addressed object. The top level page would be referenced, when loaded through a content addressed setup as `bafy.....dweb.link/index.html` or `ipfs.io/ipfs/bafy.../index.html`. In both cases, the relative reference to the resource will be within that same directory-level content addressed bundle, which will do the same work as the sub-resource integrity. I don’t see what would case the sub-resource in this type of loading to be fetched from a different gateway than the index.html, and so the protection here could always be subverted by the malicious gateway changing the html page to remove the sub-resource integrity / script link.

regarding manifest:

Having some consumers of the manifest is probably useful as a step in making this feel more natural as a standard, and to have it feel like it meets real-world usage / expectations.

---

**oed** (2025-07-25):

I’ve just proposed a [DService ENSIP](https://github.com/ensdomains/ensips/pull/43). As mentioned with reasoning in a post above. I think this better aligns with what you had in mind with suggesting an onchain approach [@polymutex](/u/polymutex)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/willscott/48/15442_2.png) willscott:

> I don’t see what would case the sub-resource in this type of loading to be fetched from a different gateway than the index.html, and so the protection here could always be subverted by the malicious gateway changing the html page to remove the sub-resource integrity / script link.

[@polymutex](/u/polymutex) would love to hear your thoughts on this since you originally suggested the use of subresource ingrity checks.

---

**polymutex** (2025-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> I’ve just proposed a DService ENSIP. As mentioned with reasoning in a post above. I think this better aligns with what you had in mind with suggesting an onchain approach

Yes, I think that’s a step in the right direction to put this data onchain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/willscott/48/15442_2.png) willscott:

> I don’t see what would case the sub-resource in this type of loading to be fetched from a different gateway than the index.html, and so the protection here could always be subverted by the malicious gateway changing the html page to remove the sub-resource integrity / script link.

This is true in isolation. However subresource integrity is enforced by browsers at the whole-page level (through [the Content-Security-Policy header](https://devdoc.net/web/developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/require-sri-for.html)). So for the purpose of having the browser enforce the use of SRI, it is beneficial to require that dapps provide SRI hashes for all resources (including relative ones), despite this being technically redundant in the context of the IPFS bundle.

“What if the gateway is compromised and just strips the `Content-Security-Policy` HTTP header?” Valid objection. I still think the *ability* for gateways to set a strict `Content-Security-Policy` header is good defense-in-depth. It is also likely that browsers and CSP will extend SRI to make it more useful, for example by allowing CSP pinning on a per-domain basis.

Lastly, on a more practical level, ~all implementations of SRI I have seen in practice rely on automated website bundle generators which take care of SRI-ing everything, so requiring relative resources to be SRI’d doesn’t seem like a large additional burden to ask of dapps that would already need to provide such hashes for external resources. That said, I do agree that a reasonable carve-out might be something like “if the dapp is self-contained to its own bundle and has no external resources, it is not required to provide SRI hashes”.

