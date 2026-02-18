---
source: magicians
topic_id: 8362
title: ERC-4824 Decentralized Autonomous Organizations
author: thelastjosh
date: "2022-02-18"
category: ERCs
tags: [governance, dao, erc-4824]
url: https://ethereum-magicians.org/t/erc-4824-decentralized-autonomous-organizations/8362
views: 8094
likes: 38
posts_count: 50
---

# ERC-4824 Decentralized Autonomous Organizations

| Authors | Joshua Tan (@thelastjosh), Isaac Patka (@ipatka), Ido Gershtein (ido@daostack.io), Eyal Eithcowich (eyal@deepdao.io), Michael Zargham (@mzargham), Sam Furter (@nivida) |
| --- | --- |
| EIP Link | Github |
| Discussions | See  daostar.org, daostar.one, and original thread |
| Status | Draft |
| Type | Standards Track |
| Category | ERC |
| Created | 2022-02-17 |

## Abstract

A standard URI and JSON schema for decentralized autonomous organizations (DAOs), focusing on relating on-chain and off-chain representations of membership and proposals.

## Motivation

DAOs, since being invoked in the Ethereum whitepaper, have been vaguely defined. This has led to a wide range of patterns but little standardization or interoperability between the frameworks and tools that have emerged. Standardization and interoperability are necessary to support a variety of use-cases. In particular, a standard daoURI, similar to tokenURI in [ERC-721](https://eips.ethereum.org/EIPS/eip-721), will enhance DAO search, discoverability, legibility, and proposal simulation. More consistent data across the ecosystem is also a prerequisite for future DAO standards.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Every EIP-4824 compliant contract MUST implement the EIP4824 interface below:

```solidity
pragma solidity ^0.4.20;

/// @title EIP-4824 DAOs
/// @dev See https://eips.ethereum.org/EIPS/eip-4824

interface EIP4824 {
    /// @notice A distinct Uniform Resource Identifier (URI) pointing to a JSON object following the "EIP-4824 DAO JSON-LD Schema". This JSON file splits into four URIs: membersURI, proposalsURI, activityLogURI, and governanceURI. The membersURI should point to a JSON file that conforms to the "EIP-4824 Members JSON-LD Schema". The proposalsURI should point to a JSON file that conforms to the "EIP-4824 Proposals JSON-LD Schema". The activityLogURI should point to a JSON file that conforms to the "EIP-4824 Activity Log JSON-LD Schema". The governanceURI should point to a flatfile, normatively a .md file. Each of the JSON files named above can be statically-hosted or dynamically-generated.
    function daoURI() external view returns (string _daoURI);
}
```

The EIP-4824 DAO JSON-LD Schema mentioned above.

```json
{
	"@context": "http://www.daostar.org/schemas",
	"type": "DAO",
	"name": "",
	"description": "",
	"membersURI": "",
	"proposalsURI": "",
	"activityLogURI": "",
	"governanceURI": ""
}
```

### Members

Members JSON-LD Schema.

```json
{
  "@context": "http://www.daostar.org/schemas",
  "type": "DAO",
  "name": "",
  "members": [
    {
      "type": "EthereumAddress",
      "address": ""
    },
    {
      "type": "EthereumAddress",
      "address": ""
    }
  ]
}
```

### Proposals

Proposals JSON-LD Schema. Every EIP-4824 contract should implement a proposalsURI pointing to a JSON object satisfying this schema.

In particular, any on-chain proposal MUST be associated to an id of the form CAIP10_ADDRESS + “?proposalId=” + PROPOSAL_COUNTER, where CAIP10_ADDRESS is an address following the CAIP-10 standard and PROPOSAL_COUNTER is an arbitrary identifier such as a uint256 counter or a hash that is locally unique per CAIP-10 address. Off-chain proposals MAY use a similar id format where CAIP10_ADDRESS is replaced with an appropriate URI or URL.

```json
{
  "@context": "http://www.daostar.org/schemas",
  "type": "DAO",
  "name": "",
  "proposals": [
    {
      "type": "proposal",
      "id": "

",
      "name": "",
      "contentURI": "",
      "status": "",
      "calls": [
        {
          "type": "CallDataEVM",
          "operation": "",
          "from": "",
          "to": "",
          "value": "",
          "data": ""
        }
      ]
    }
  ]
}
```

### Activity Log

Activity Log JSON-LD Schema.

```json
{
  "@context": "http://www.daostar.org/schemas",
  "type": "DAO",
  "name": "",
  "activities": [
    {
      "id": "",
      "type": "activity",
      "proposal": {
        "id": "

",
        "type": "proposal"
      },
      "member": {
        "type": "EthereumAddress",
        "address": ""
      }
    },
    {
      "id": "",
      "type": "activity",
      "proposal": {
        "id": "

",
        "type": "proposal"
      },
      "member": {
        "type": "EthereumAddress",
        "address": ""
      }
    },
  ]
}
```

## Rationale

In this standard, we assume that all DAOs possess at least two primitives: *membership* and *behavior*. *Membership* is defined by a set of addresses. *Behavior* is defined by a set of possible contract actions, including calls to external contracts and calls to internal functions. *Proposals* relate membership and behavior; they are objects that members can interact with and which, if and when executed, become behaviors of the DAO.

### URIs and off-chain data

DAOs themselves have a number of existing and emerging use-cases. But almost all DAOs need to publish data off-chain for a number of reasons: communicating to and recruiting members, coordinating activities, powering user interfaces and governance applications such as Snapshot or Tally, or enabling search and discovery via platforms like DeepDAO or Messari. Having a standardized schema for this data, akin to an API specification, would strengthen existing use-cases for DAOs, help scale tooling and frameworks across the ecosystem, and build support for additional forms of interoperability.

While we considered standardizing on-chain aspects of DAOs in this standard, particularly on-chain proposal objects and proposal IDs, we felt that this level of standardization was premature given (1) the relative immaturity of use-cases, such as multi-DAO proposals or master-minion contracts, that would benefit from such standardization, (2) the close linkage between proposal systems and governance, which we did not want to standardize (see “governanceURI”, below), and (3) the prevalence of off-chain and L2 voting and proposal systems in DAOs (see “proposalsURI”, below). Further, a standard URI interface is relatively easy to adopt and has been actively demanded by frameworks (see “Community Consensus”, below).

### membersURI

Approaches to membership vary widely in DAOs. Some DAOs and DAO frameworks (e.g. Gnosis Safe, Tribute), maintain an explicit, on-chain set of members, sometimes called owners or stewards. But many DAOs are structured so that membership status is based on the ownership of a token or tokens (e.g. Moloch, Compound, DAOstack, 1Hive Gardens). In these DAOs, computing the list of current members typically requires some form of off-chain indexing of events.

In choosing to ask only for an (off-chain) JSON schema of members, we are trading off some on-chain functionality for more flexibility and efficiency. We expect different DAOs to use membersURI in different ways: to serve a static copy of on-chain membership data, to contextualize the on-chain data (e.g. many Gnosis Safe stewards would not say that they are the only members of the DAO), to serve consistent membership for a DAO composed of multiple contracts, or to point at an external service that computes the list, among many other possibilities. We also expect many DAO frameworks to offer a standard endpoint that computes this JSON file, and we provide a few examples of such endpoints in the implementation section.

We encourage extensions of the Membership JSON-LD Schema, e.g. for DAOs that wish to create a state variable that captures active/inactive status or different membership levels.

### proposalsURI

Proposals have become a standard way for the members of a DAO to trigger on-chain actions, e.g. sending out tokens as part of grant or executing arbitrary code in an external contract. In practice, however, many DAOs are governed by off-chain decision-making systems on platforms such as Discourse, Discord, or Snapshot, where off-chain proposals may function as signaling mechanisms for an administrator or as a prerequisite for a later on-chain vote. (To be clear, on-chain votes may also serve as non-binding signaling mechanisms or as “binding” signals leading to some sort of off-chain execution.) The schema we propose is intended to support both on-chain and off-chain proposals, though DAOs themselves may choose to report only on-chain, only off-chain, or some custom mix of proposal types.

**Proposal ID**. Every unique on-chain proposal MUST be associated to a proposal ID of the form CAIP10_ADDRESS + “?proposalId=” + PROPOSAL_COUNTER, where PROPOSAL_COUNTER is an arbitrary string which is unique per CAIP10_ADDRESS. Note that PROPOSAL_COUNTER may not be the same as the on-chain representation of the proposal; however, each PROPOSAL_COUNTER should be unique per CAIP10_ADDRESS, such that the proposal ID is a globally unique identifier. We endorse the CAIP-10 standard to support multi-chain / layer 2 proposals and the “?proposalId=” query syntax to suggest off-chain usage.

**ContentURI**. In many cases, a proposal will have some (off-chain) content such as a forum post or a description on a voting platform which predates or accompanies the actual proposal.

**Status**. Almost all proposals have a status or state, but the actual status is tied to the governance system, and there is no clear consensus between existing DAOs about what those statuses should be (see table below). Therefore, we have defined a “status” property with a generic, free text description field.

| Project | Proposal Statuses |
| --- | --- |
| Aragon | Not specified |
| Colony | [‘Null’, ‘Staking’, ‘Submit’, ‘Reveal’, ‘Closed’, ‘Finalizable’, ‘Finalized’, ‘Failed’] |
| Compound | [‘Pending’, ‘Active’, ‘Canceled’, ‘Defeated’, ‘Succeeded’, ‘Queued’, ‘Expired’, ‘Executed’] |
| DAOstack/ Alchemy | [‘None’, ‘ExpiredInQueue’, ‘Executed’, ‘Queued’, ‘PreBoosted’, ‘Boosted’, ‘QuietEndingPeriod’] |
| Moloch v2 | [sponsored, processed, didPass, cancelled, whitelist, guildkick] |
| Tribute | [‘EXISTS’, ‘SPONSORED’, ‘PROCESSED’] |

**ExecutionData**. For on-chain proposals with non-empty execution, we include an array field to expose the call data. The main use-case for this data is execution simulation of proposals.

### activityLogURI

The activity log JSON is intended to capture the interplay between a member of a DAO and a given proposal. Examples of activities include the creation/submission of a proposal, voting on a proposal, disputing a proposal, and so on.

*Alternatives we considered: history, interactions*

### governanceURI

Membership, to be meaningful, usually implies rights and affordances of some sort, e.g. the right to vote on proposals, the right to ragequit, the right to veto proposals, and so on. But many rights and affordances of membership are realized off-chain (e.g. right to vote on a Snapshot, gated access to a Discord). Instead of trying to standardize these wide-ranging practices or forcing DAOs to locate descriptions of those rights on-chain, we believe that a flatfile represents the easiest and most widely-acceptable mechanism for communicating what membership means and how proposals work. These flatfiles can then be consumed by services such as Etherscan, supporting DAO discoverability and legibility.

We chose the word “governance” as an appropriate word that reflects (1) the widespread use of the word in the DAO ecosystem and (2) the common practice of emitting a governance.md file in open-source software projects.

*Alternative names considered: description, readme, constitution*

### Why JSON-LD

We chose to use JSON-LD rather than the more widespread and simpler JSON standard because (1) we want to support use-cases where a DAO wants to include members using some other form of identification than their Ethereum address and (2) we want this standard to be compatible with future multi-chain standards. Either use-case would require us to implement a context and type for addresses, which is already implemented in JSON-LD.

Further, given the emergence of patterns such as subDAOs and DAOs of DAOs in large organizations such as Synthetix, as well as L2 and multi-chain use-cases, we expect some organizations will point multiple EIP-4824 DAOs to the same URI, which would then serve as a gateway to data from multiple contracts and services. The choice of JSON-LD allows for easier extension and management of that data.

### Community Consensus

The initial draft standard was developed as part of the DAOstar One roundtable series, which included representatives from all major EVM-based DAO frameworks (Aragon, Compound, DAOstack, Gnosis, Moloch, OpenZeppelin, and Tribute), a wide selection of DAO tooling developers, as well as several major DAOs. Thank you to all the participants of the roundtable, the full list of which can be found [here](https://daostar.one/). We would especially like to thank Auryn Macmillan, Fabien of Snapshot, Selim Imoberdorf, Lucia Korpas, and Mehdi Salehi for their contributions.

In-person events will be held at Schelling Point 2022 and at ETHDenver 2022, where we hope to receive more comments from the community. We also plan to schedule a series of community calls through early 2022.

## Security Considerations

This standard defines the interfaces for the DAO URIs but does not specify the rules under which the URIs are set, or how the data is prepared. Developers implementing this standard should consider how to update this data in a way aligned with the DAO’s governance model, and keep the data fresh in a way that minimizes reliance on centralized service providers.

Indexers that rely on the data returned by the URI should take caution if DAOs return executable code from the URIs. This executable code might be intended to get the freshest information on membership, proposals, and activity log, but it could also be used to run unrelated tasks.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

> edited March 6, 2022: updated to reflect most recent changes to PR

## Replies

**thelastjosh** (2022-02-19):

## Additional references

1. Dilger, W. (1997). Decentralized autonomous organization of the intelligent home according to the principle of the immune system’. 1997 IEEE International Conference on Systems, Man, and Cybernetics. Computational Cybernetics and Simulation, 351–356. https://doi.org/10.1109/ICSMC.1997.625775
2. Buterin, V. (2013a). Ethereum whitepaper: A next-generation smart contract and decentralized application platform [White Paper]. https://blockchainlab.com/pdf/Ethereum_white_paper-a_next_generation_smart_contract_and_decentralized_application_platform-vitalik-buterin.pdf
3. JSON-LD Schema. https://json-ld.org/
4. CAIP-10. https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

---

**toledoroy** (2022-03-16):

Hi,

Great idea! we should definitely add some standards for metadata. Though I think we could generalize this idea a bit and perhaps come up with something that could work for other contracts as well.

First, I think it would probably make more sense to have different types/names for different JSON files, so we can tell them parts

E.g.

```auto
Members
 "type": "members",
```

and

```auto
Proposals
 "type": "proposals",
```

It might be more correct to name that parameter as role, not type, as the type usually represents what a thing is and this represents what it is for (purpose).

If you do that, you could just use the conventional contractURI() which would a JSON of “type”: “DAO” or “role”: “DAO”. Which makes more sense semantically, doesn’t require that you have prior knowledge regarding the contract type, and could be use as a general standard for all other types of contracts as well.

---

**thelastjosh** (2022-03-20):

Hi [@toledoroy](/u/toledoroy) ! First off, thank you for the suggestions ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

**Re: associating types for the different JSON files being returned by `membersURI` and `proposalsURI`**, we didn’t really dig into this during the working group discussions, so maybe now is a good opportunity. My thoughts are:

1. First, notice that each individual member does have a type or typeclass, member, and it might get confusing for member and members to be separate types (e.g. in the schema.org ontology, member supersedes members, so there’s no difference).
2. Perhaps most saliently, the membersURI and proposalsURI are pointing to different JSON objects because we expect some DAOs might want to compute those using different services, and it allows for more modularity. You could imagine them getting replaced by properties members and proposals, and daoURI returning a giant nested JSON with all the metadata, members, proposals, activities, etc. In that case, the type of the JSONs returned by membersURI, proposalsURI, and activityLogURI would just be DAO, since members and proposals are properties intended to be evaluated in the DAO type/context. And you can see this in current type signatures of the JSONs returned by proposalsURI, membersURI, and activityLogURI.
3. If I think about it from a data modeling standpoint, it feels like we should be able to just say that the type of the Members JSON should just be something like List(member) or [member].

Let me know if that makes sense; I’ve tagged some of the other team members to get their thoughts [@mzargham](/u/mzargham) [@nivida](/u/nivida).

**Re: contractURI suggestion**, I think you’re right, but I’m not familiar with uses of contractURI outside of the OpenSea context though for NFTs (essentially replacing/extending tokenURI). Do you see it getting more prominent usage elsewhere / has there been a standard emitted for it? I could see it being really useful to have a generic contractURI for every single contract that the daoURI schema could inherit from.

---

**julesl23** (2022-03-21):

Hi,

I am liking this but something did bother me…

That everything is shuffled off-chain to secondary storage.

I’m thinking that members can be a map of accounts on-chain (so can call member style functions). Proposals can each be an NFT, grounding the truth on-chain. Hence leveraging much more of the Ethereum eco system.

Sure, variables such as descriptions, history logs etc. can be off-chain JSON type files.

I’m all for pushing wider use of NFTs beyond digital art. I see this proposal as an opportunity to do this, forgive me.

What about gas fees might be a reaction? By the time if this goes to final stages, fees will be much lower anyway (hopefully).

---

**thelastjosh** (2022-03-23):

Thanks for the comments [@julesl23](/u/julesl23) ! Re: proposals as NFTs—an idea like this did come up during the WG sessions, I think from [@mzargham](/u/mzargham)! We ended not going there because it’s not a pattern that we currently see in the ecosystem, and we didn’t want this first standard to push the envelope so much as organize and exemplify existing best-practices in observed DAOs and DAO frameworks.

DAOs in other L1s with much lower costs do end up hosting more of their ops and data on-chain (and we’re working to explore/cover those use-cases in a multi-chain working group), but for now that’s not standard in Ethereum use-cases. But even with lower fees, there will always be a use-case for the off-chain data for the legibility and discoverability use-cases we mention.

---

**toledoroy** (2022-03-23):

Loving this!

People are non-fungible too and there’s no reason for each DAO member to have to maintain and update their data on different locations.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/b/bf2d6e9f07f0283343039d56ba487a61a15d154e_2_647x500.jpeg)image1275×984 69.3 KB](https://ethereum-magicians.org/uploads/default/bf2d6e9f07f0283343039d56ba487a61a15d154e)

---

**Asgeir** (2022-03-24):

Great initiative! I love how open it is (even while making the data more easily consumable); it does not force DAOs into some rigid standardization scheme!

One thing that came to mind is that we could perhaps, instead of or in addition to the interface implementation requirement, have an event emitted with the daoURI.

The event could, for instance, be emitted by:

- A common contract with a function that takes a daoURI and emits it in an event, or
- It could be a standard event emitted by any contract, or
- It could use ERC-3722 (Poster) with a standard tag.

The rationale for proposing this:

- The daoURI is not something that is consumable on-chain, and therefore does not need to be part of the chain state.
- It’s easy to propose a transaction that will emit the event to any DAO that can execute arbitrary transactions. It will also be easy for preexisting DAOs to “implement the standard”.
- Implementing a Subgraph for continuously indexing all DAOs that emit the event is trivial.

Basically, this could make it cheaper to implement the standard, make it easier to implement the standard (and in the future update the daoURI), and make it more easily indexable.

---

**julesl23** (2022-03-24):

I second what [@Asgeir](/u/asgeir) says. I was going to say it but forgot as I wrote my other post.

The other thing I noticed was lack of timestamps in any of the JSON files…

Take an example where a DAO has thousands of members and the membership is tokenised with a secondary market so a lot of members joining and leaving. With current proposal it doesn’t define if memberships list has to be up to date. In this use case, a single member leaving/joining and the whole list has to be written out again.

I know there is the blurb on having endpoint to compute this real-time but unless I’m mistaken that requires server and defeats purpose of decentralisation. Is there a way to get this list computed by smart contract directly?

At least with a timestamp and a snapshot of members list, won’t have to keep uploading the most up to date.

On that point, wasn’t clear to me in activates log if member is the proposer of the contract, or members’ snapshot of voting and where would amounts/results go and so on?

---

**thelastjosh** (2022-03-28):

Just wanted to say that I really like this idea. It would make adoption much easier for existing DAOs. One question is which of these methods (contract, event, poster) we should recommend, and/or whether we should support all of them.

Small note, on some level no matter what method you use, daoURI has to be part of the chain state, it just doesn’t have to be defined in the contract.

---

**Asgeir** (2022-03-29):

I like the event method option since it’s the most flexible one. This will allow a more strict and backward-compatible standard to be developed using the contract method later (with additional checks and still emitting the event).

Can we assume that all DAOs can execute arbitrary function calls from the “avatar” address (or the address that represents the DAO)? If so, we could use the message sender as the DAO address (when indexing). Also, if there is a new emit of the event, we can treat it as an overwrite of the old daoURI.

Basically something like this:

```auto
emit ERC4824(string daoUIR); // implicitly the message sender is the DAO
```

Perhaps we should also add an indexed address to the event. That can be useful later if a new standard builds on this one using the contract method (where this address can probably be trusted, which is not the case in this version).

---

**thelastjosh** (2022-03-29):

In the standard we don’t actually assume that every standard has an avatar or canonical contract; in principle multiple contracts (on multiple chains / L2s!) associated to the same DAO can all pass to the same daoURI (~a company operating multiple storefronts or processes). But the event method still makes sense in that context.

How would attaching an indexed address to the event be useful? Are you assuming this would be “avatar” address?

---

**julesl23** (2022-03-29):

Okay, with so little use of the blockchain, what’s stopping a malicious actor pointing e.g. proposalsURI to their centralised storage and changing the proposal before its execution?

Will the community easily understand that this is not a trustless system? Given the context of its use, what are the checks and balances?

---

**julesl23** (2022-03-30):

Having the URI addresses (such as hashes) come from the blockchain would be more secure. Something like this:

emit ERC4824(

string context,

address indexed dao,

string name,

string description,

string membersURI,

string proposalsURI,

string activityLogURI,

string governanceURI

);

---

**Asgeir** (2022-03-30):

Aha, that makes sense.

My thinking was that in the initially proposed solution, using the EIP4824 interface, the daoURI would be associated with the address of the contract implementing it. If we were going to use an event instead, we need another way to associate an address with the daoURI (even if multiple addresses can point to the same daoURI). Also, we need to be able to trust that address (so that not anybody can register daoURIs for any address).

Therefore, looking at it again now, I can’t see how we can get an address that we can trust by only using an event (like I proposed above). I think we will need to use a contract that also emits the message sender (just like Poster does). Or could there be another solution here that I am not aware of?

I think it could make sense to create a new contract almost identical to the Poster contract and deployment process (via singleton). As Poster seems to be intended for social media: “A ridiculously simple general-purpose social media smart contract.”. Also, it will be less resource-intensive to process the events.

---

**julesl23** (2022-03-30):

Yeah, I’m liking it.

Three different versions:

v1

```auto
contract ERC4824v1 {
    event DAOUpdate(
        address indexed sender,
        address[] indexed daos,
        string name,
        string description,
        string membersURI,
        string proposalsURI,
        string activityLogURI,
        string governanceURI
    );

    function dao(
        address[] calldata daos,
        string calldata name,
        string calldata description,
        string calldata membersURI,
        string calldata proposalsURI,
        string calldata activityLogURI,
        string calldata governanceURI
    ) public {
        emit DAOUpdate(
            msg.sender,
            daos,
            name,
            description,
            membersURI,
            proposalsURI,
            activityLogURI,
            governanceURI
        );
    }
}
```

v2

```auto
contract ERC4824v2 {
    event DAOUpdate(address indexed sender, string uri);

    function dao(string calldata uri) public {
        emit DAOUpdate(msg.sender, uri);
    }
}
```

v3

```auto
contract ERC4824v3 {
    event DAOUpdate(address indexed sender, address[] indexed daos, string uri);

    function dao(address[] calldata daos, string calldata uri) public {
        emit DAOUpdate(msg.sender, daos, uri);
    }
}
```

The last one can search by dao(s) address, whilst the second one can’t. Both use less gas than the first. The first has the advantage of the last and the hashes of membersURI, proposalsURI and governanceURI come from the blockchain via events, more secure.

---

**julesl23** (2022-03-31):

I still feel there is a lack of timestamps though.

With events at least can get the block timestamp it was emitted from (to an accuracy between two blocks is probably good enough for most use cases). But anything in JSON-LD files cannot without timestamp fields in them, I feel is needed; considering that most data in these are conceptually snapshots.

---

**thelastjosh** (2022-03-31):

Just wanted to say that [@mzargham](/u/mzargham) and I are working on a response to the event/poster idea; we had a long conversation about it at today’s working group meeting and have some ideas!

---

**thelastjosh** (2022-03-31):

Re timestamps, I think this is more something that people could easily add to the data model / extend the standard with, rather than a truly necessary data field. We’re working to add tooling, e.g. a schema manager / explorer, to allow easier and relatively permisionless extensions of the data model for extended use-cases.

---

**julesl23** (2022-04-01):

That’s a shame [@thelastjosh](/u/thelastjosh) . So we are not able to search for any changes then?

For example, how to filter for new proposals?

---

**julesl23** (2022-04-01):

Also I’m not sure what fields are considered required and which optional?

For some use cases, the Members JSON-LD file is not possible as there is maybe no array list of members held by DAO contract, only total supply of governance tokens. This to save gas and storage, and maybe anonymity/security reasons too.

When proposals are voted for, at that stage can get list of accounts that voted with their governance tokens. So only then can these subset of accounts be recorded in proposals/activity files.


*(29 more replies not shown)*
