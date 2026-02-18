---
source: magicians
topic_id: 9635
title: "ERC: Rich Site-Proposed Contract Metadata"
author: danfinlay
date: "2022-06-15"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/erc-rich-site-proposed-contract-metadata/9635
views: 1581
likes: 3
posts_count: 10
---

# ERC: Rich Site-Proposed Contract Metadata

---

## eip:
title: Rich Site-Proposed Contract Metadata
description: A protocol for dapps to suggest metadata to wallets related to relevant contracts.
author: Dan Finlay <@danfinlay>
discussions-to:
status: Draft
type: Standards
category: Interface
created: 2022-06-15

## Abstract

Many types of phishing attack today rely on users not knowing what contract they’re interacting with, even when it’s a contract the user has interacted with before. To facilitate in recognizing these interactions in a way that requires no central registry or additioanl services, we propose that wallet methods that may interact with an address should also accept proposed metadata from the site suggesting the transaction, which can be used to enhance the display of future interactions with those contracts.

## Motivation

We’ve got a lot of ways we try to gather the information for confirmations, but it ranges between very complicated, unreliable, centralized, and incomplete, and is not getting the job done.

1. Contract names

- Local address book

Requires user interaction, which adds UX burden, and most users skip.

Centralized registries

- Are perpetually incomplete, and favor the established, not the upstart.

reverse-resolved ENS names

- Attackers can choose familiar-looking names, so these are not a reliable basis of secure review of what you’re looking at unless you entered it yourself.

1. Method information

- Registry lookups (4byte directory, the Parity on-chain registry)

Can be prone to collisions (like At Inversebrah, with trolling increasing)
- Returns ABIs

Has no parameter names, leaving most of the transaction illegible.

Trusting the contract for its own metadata (EIP-719, EIP-4430)

- Requires an active connection to the blockchain.
- Is not widespread (no backwards compatibility)

[Transaction Insights](https://metamask.zendesk.com/hc/en-us/articles/4412543412123-Transaction-Insight)

- Requires an additional fairly heavy-weight process
- Is largely centralized today
- Only works for verified contracts on etherscan (although designed for eventual Sourcify support).

Additionally, this method serves to help populate the wallet with trustworthy information about what it holds. It reduces the need to rely on any central services for indexing (enhancing performance and privacy), and eliminates dangers that come from index-based automatic asset detection, like receiving harrassment, or [Airdrop scams](https://medium.com/metamask/phisher-watch-airdrop-scams-82eea95d9b2a).

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Wallets may integrate the ability to propose names for contracts, methods, and parameters into any method that touches an address, so the wallet can be expanded with this metadata at runtime. These methods include `eth_sendTransaction`, and `eth_signTypedData` (and its variants).

Benefits

- No need for any central server
- No registry with collisions
- Works on all chains
- Includes parameter names as well as method and contract names.
- Could be easily added to any existing dapp
- If every dapp a user touches uses this, then no phishing site could get the user to give up one of those assets without seeing a legible confirmation.
- Can even be implemented on a cold/offline or hardware wallet.

### Implementation

Any method that involves an address MAY include a new OPTIONAL parameter `proposedContracts`, which will include an additional prompt to the user as part of the confirmation flow, asking if they’d like to trust the site for this information.

`contractId` would be some kind of cross chain address format, likely [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md).

`ContractData` would be some kind of type that is enough to render transaction names for methods called.

- Today TX Insight uses a full Truffle Decoder output to render this, which includes lots of compiler info that we would not need here.

```typescript
type TxOptionsEnhancement = {
  proposedContracts: {
    [contractId: CrossChainAddress]: {
      proposedName: string,
      abi?: Abi,
      contractData?: ContractData
    }
  }
}
```

Wallets MUST store the recommending site & time along with this data for forensic purposes.

The user SHOULD be able to adjust the proposed names in the confirmation, to avoid collisions, and help personalize their local context.

Any subsequent confirmations that are displaying the proposed contracts’ names SHOULD show the proposed names.

- A mouse hover may provide the metadata about when this name was proposed.
Any subsequent transaction confirmations that are displaying transactions to the proposed contracts SHOULD use the proposed data to render those transactions as readably as possible.
Additional optional parameters MAY be added to the proposedContracts options object to allow new kinds of enhancement in the future.

## Rationale

- We need a solution that can address two aspects of transaction interaction

What you’re interacting with
- How you’re interacting with it

We want something we can get into production ASAP
We want a solution that is as complete as possible

- If used correctly, it should be able to totally eliminate the un-readability problems of transactions.

If this were adopted widespread, it could also reduce the need to rely on centralized indexes of on-chain assets in general, since users would have more complete local views of their own assets.

## Backwards Compatibility

Since this EIP involves a new optional parameter whose name is not used in any method, it should not have any issues with backwards compatibility.

## Security Considerations

This proposal’s security depends on a user’s first interaction with a contract being from a trustworthy site. If we assume that most of the time that a user is being phished, they are being robbed of an asset they previously acquired, then it should be safe to assume that there was a prior opportunity for the user to be introduced to reliable metadata from the source that they originally acquired the asset (the metadata is as trustworthy as the asset they have is authentic).

Achieving that initial safety would require a widespread push for adoption, but since it’s just about adding a new optional parameter and it keeps a site’s users more resistant to phishing, I think this effort could be effective.

Some users would not be protected by this: Users who acquired their assets previously, and do not have the relevant metadata for the assets they are holding. Those users would be at no greater risk than they are at today. One of these users being phished to a malicious site could be either presented with a malicious transaction or malicious metadata, but for a scammer the current behavior (transfer the asset) is simply fewer steps to success, so it seems unlikely this would be a desireable attack for phishers.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**danfinlay** (2022-06-15):

To Do:

- Finalize cross-chain address format in EIP (probably defaulting to CAIP-10)
- Specify a metadata format that is rich enough to render arrays of nested structs as members of named parameters in functions. Maybe borrowing some schema from EIP-712.

---

**danfinlay** (2022-06-15):

For the `ContractData` type, it could be as complex as a [Truffle Decoding](https://trufflesuite.com/docs/truffle/codec/), but could probably be something simpler. I’ll be enlisting advice of the Truffle team as they’re available.

---

**danfinlay** (2022-06-15):

I could almost see this as part of a larger system of Ðapp-wallet communicating objects and their affordances back and forth. The same way [a Ðapp might want a list of tokens](https://eips.ethereum.org/EIPS/eip-2256), or might want strong typing on the methods they have, they would love to know what the user has to interact with. Would be cool if the same format that makes the tx object readable could allow a site to generate a generic strongly-typed interface from the same info.

---

**danfinlay** (2022-06-15):

Oh, we might want to include `image` and other common identifying params. Maybe try to make this a superset of [EIP-747: wallet_watchAsset.](https://eips.ethereum.org/EIPS/eip-747)

---

**danfinlay** (2022-06-15):

Since this approach does not rely on the contract itself, recommending sites could take it upon themselves to recommend particularly human-readable names for methods & parameters, including localization.

---

**Pandapip1** (2022-06-16):

How about something akin to `watchAsset`, but that provides, as an argument, a superset of the ABI that also contains NatSpec data (whose format would be defined in this EIP)?

---

**danfinlay** (2022-06-16):

I agree. This benefit could also serve well as a standalone method call including this data.

I’ve been starting to refer to this desired type as **ABI+**. It could be utilized in many ways:

- As a standalone method for annotating one address
- As a batchable method for suggesting several address metadatas
- Aggregated into a feed/list that users could subscribe to.
- Incorporated into methods (to minimize method calls), as this EIP suggests.
- Made available by contracts for self-declaring their interfaces.

But I increasingly think the important thing is “we need a standardized superset of the ABI”, and from there we could explore a ton of different ways of making confirmations more comprehensible.

---

**danfinlay** (2022-06-23):

Noting the Grid+ team has a format that may work for this: https://twitter.com/alexmillertech/status/1539764022127591428?s=21&t=kAy-Ok5jX2-i9IiaDhJjAA

---

**kuzdogan** (2022-06-23):

This is a really exciting proposal, thanks for laying it out.

Firstly, about the EIP, some immediate questions:

- Does this include showing a descriptive message when calling a method such as “Sends X tokens to 0x123” as in EIP-4430 or as in a NatSpec @userdoc field? Is the what was meant with: “kind of type that is enough to render transaction names for methods”? In this case this means the dApp developer will be documenting explainers for the methods of the contract which will be sent to the user’s wallet.
- I suppose this metadata will be something that might change over time. The dapp developer may improve the method documentation or correct some mistakes. In that case some versioning might be helpful or another way to resolve conflicting metadata.

I am not sure if I completely understood the implementation of the proposal so apologies if these were already laid out or irrelevant.

Secondly, We at sourcify.dev are working towards a similar goal but our approach has been different. Our’s can be added to the “2. Method information” section which has its own downsides and upsides. We primarily leverage the **Solidity contract metadata** in the following ways:

1. We fully verify contracts using the source file hashes in the metadata file to guarantee a byte-by-byte match of the verified source code with the deployed source code.
2. We maintain a public repository of verified contracts and pin them on IPFS for users/wallets to fetch the metadata file, whose IPFS hash is appended at the end of the contract bytecode. You can see it in action in the playground.
3. As a larger goal, we aim to enable more human-friendly transactions through ABI + NatSpec’s dynamic expressions in the @userdoc and @devdoc fields, found in the metadata file mentioned above. This way the tx parameters can be decoded and users can be shown plain text information marked in the NatSpec.

As I’m relatively new in the space, I wasn’t aware of the EIP-719 and EIP-4430, and learned a lot about the previous efforts in the same direction. For now I gathered them very basically in docs.sourcify.dev’s Additional Resources.

As said, the EIP’s approach and ours seem to be different but I don’t see them mutually exclusive. Now I’m thinking if it would make sense to coordinate these efforts somehow. With downsides and upsides to each of them, and being dependent to contract and dapp developers in one way or another, I feel all of them can be leveraged at the same time. Besides there are additional information to contracts that can help users make more informed decisions when interacting with a contract e.g. how many times a contract is interacted with, if it is audited, when it is deployed etc.

This is a difficult and multi-faceted problem and a working group or some shared resources on human-readable contract interactions would make sense, I believe.

