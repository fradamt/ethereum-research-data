---
source: magicians
topic_id: 25718
title: "ERC-8042: Diamond Storage"
author: mudgen
date: "2025-10-09"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8042-diamond-storage/25718
views: 1031
likes: 33
posts_count: 29
---

# ERC-8042: Diamond Storage

See the full ERC draft of EIP-8042 here: [ERC-8042: Diamond Storage](https://eips.ethereum.org/EIPS/eip-8042)

## Abstract

This standard formalizes the diamond storage pattern originally introduced by [ERC-2535 Diamonds](https://eips.ethereum.org/EIPS/eip-2535) and widely adopted across smart contracts.

Though originally created for proxy contracts, diamond storage can be used to organize storage and data access within *any* smart contract.

Diamond storage defines the location of structs in contract storage using the `keccak256` hash of human-readable identifiers.

[ERC-8042](https://eips.ethereum.org/EIPS/eip-8042) standardizes this simple and production-proven approach, offering a lightweight alternative to [ERC-7201](https://eips.ethereum.org/EIPS/eip-7201) for new and existing projects.

## Replies

**xinbenlv** (2025-10-10):

Can you file a pull request so we editor can assign number?

8035 has been assigned to [Add ERC: MultiTrust Credential (MTC) — Verifiable Reputation Interface (Core) by YutaHoshino · Pull Request #1229 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1229)

---

**mudgen** (2025-10-11):

Thank you!  I made a pull request here: [Add ERC: Diamond Storage by mudgen · Pull Request #1250 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1250)

Since 8035 is taken can I use 8040?

---

**DavidKim** (2025-10-13):

Great to see that Diamond storage pattern is formally getting standardized!

As mentioned in this ERC, this pattern has been frequently used in the implementations of ERC-2535 diamond and has a proven track record for its practicality.

Especially in the context of facet-specific-storage, as Facets need a secure way to differentiate their storage while they share the storage of the Diamond as a whole.

For example, in Trust Wallet’s ERC-4337 based smart wallet [“Barz”](https://github.com/trustwallet/barz/tree/main), we use a human readable string for the preimage of the hash and use that hash for storage, in line with this ERC.

Below is an example.

```auto
    bytes32 constant K1_STORAGE_POSITION =
        keccak256(
            "v0.trustwallet.diamond.storage.Secp256k1VerificationStorage"
        );
    bytes32 constant R1_STORAGE_POSITION =
        keccak256(
            "v0.trustwallet.diamond.storage.Secp256r1VerificationStorage"
        );
    bytes32 constant GUARDIAN_STORAGE_POSITION =
        keccak256("v0.trustwallet.diamond.storage.GuardianStorage");
```

Barz smart contract has been running securely for years and I believe that numerous other Diamond implementations also follow this pattern.

Looking forward to seeing more adoption of this pattern beyond the Diamond implementations and as a considerable general practice/pattern in smart contract engineering.

---

**mihaic195** (2025-10-14):

Great work [@mudgen](/u/mudgen) !

Although the pattern was heavily inspired by the [Diamond Proxy Pattern (ERC2535)](https://eips.ethereum.org/EIPS/eip-2535), the storage strategy can be used in any contract system that uses `DELEGATECALL`. Therefore, I think the term “Diamond Storage” should be renamed to something else to prevent it from being perceived as only for ERC2535 implementations. I’m not inspired right now, as most of my ideas are very close to what ERC7201 uses ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Since this storage strategy can be used for any proxy contract system, maybe the EIP could benefit from a few words on extending storage. We can leverage the already existing docs regarding the diamond storage upgrade. If you want, I can try to create the appropriate wording.

Another topic is reading storage slots off-chain for developer experience. Some examples would be beneficial. I can also provide some wording here.

Finally, although this may seem obvious to some, I believe the EIP could benefit from a small remark mentioning that storage collisions are only possible among contracts that share the same storage context (i.e., code executed via `DELEGATECALL` into a single proxy’s storage). Using the same identifier across different contract addresses or instances doesn’t have this collision problem.

---

**innovinitylabs** (2025-10-14):

Am new to Smart Contract dev and love [Diamond Proxy Pattern (ERC2535)](https://eips.ethereum.org/EIPS/eip-2535) and already using Diamond storage for my onchain gen art project.

I hope this one gets approved soon ![:smiling_face_with_three_hearts:](https://ethereum-magicians.org/images/emoji/twitter/smiling_face_with_three_hearts.png?v=12)

---

**mudgen** (2025-10-15):

[@mihaic195](/u/mihaic195), thank you for this thoughtful feedback.

> Although the pattern was heavily inspired by the Diamond Proxy Pattern (ERC2535), the storage strategy can be used in any contract system that uses DELEGATECALL . Therefore, I think the term “Diamond Storage” should be renamed to something else to prevent it from being perceived as only for ERC2535 implementations. I’m not inspired right now, as most of my ideas are very close to what ERC7201 uses

Yes, this is a good point. However diamond storage has been called diamond storage for 5 years and there is a [lot of documentation and articles using that name](https://www.google.com/search?q=smart+contracts+%22diamond+storage%22). The name “diamond storage” is significantly different than ERC7201’s “namespace storage” which is good so they don’t get confused by people.

Perhaps some text should be added to ERC8042 to make it clear that diamond storage is not specific to ERC-2535 Diamonds.  If there other ways to make it clear that any contract can use it, that would be good.

> Since this storage strategy can be used for any proxy contract system, maybe the EIP could benefit from a few words on extending storage. We can leverage the already existing docs regarding the diamond storage upgrade. If you want, I can try to create the appropriate wording.

Yes, extending structs through upgrades is important, but that is a technical issue I don’t think is necessary to cover in this EIP.

> Another topic is reading storage slots off-chain for developer experience. Some examples would be beneficial. I can also provide some wording here.

That is a good point.  A good reason to have this standard is so tooling can have a standard way to read structs from custom storage locations.

> Finally, although this may seem obvious to some, I believe the EIP could benefit from a small remark mentioning that storage collisions are only possible among contracts that share the same storage context (i.e., code executed via DELEGATECALL into a single proxy’s storage). Using the same identifier across different contract addresses or instances doesn’t have this collision problem.

I’m not sure I really understand this point but it might be covered by some of the points mentioned under the Security Considerations sections.  If not, please elaborate.  Storage collisions are not possible with diamond storage if different diamond storage identifiers are used.

---

**mihaic195** (2025-10-15):

[@mudgen](/u/mudgen),

Thanks for the quick reply!

In the Motivation section, I would propose something like:

> This pattern is called “diamond storage” due to its origin in ERC-2535. However, it is a general-purpose storage pattern applicable to any smart contract system using DELEGATECALL or proxy-based composition.

Regarding my previous remark:

> I’m not sure I really understand this point but it might be covered by some of the points mentioned under the Security Considerations sections. If not, please elaborate. Storage collisions are not possible with diamond storage if different diamond storage identifiers are used.

Yeah, ignore this, I don’t think it’s necessary, as it is implicit by the Security Considerations. My point was to clarify that collision risk exists only when different logic contracts share the same storage context. Two separate contracts, deployed at different addresses, can safely use the same storage identifier without any risk of collision because each contract’s storage is isolated by address.

---

**mudgen** (2025-10-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mihaic195/48/15506_2.png) mihaic195:

> This pattern is called “diamond storage” due to its origin in ERC-2535. However, it is a general-purpose storage pattern applicable to any smart contract system using DELEGATECALL or proxy-based composition.

Thanks for that suggestion. Diamond storage doesn’t just apply to proxy contracts and contracts that use `DELEGATECALL`. Diamond storage can be used in any contract, but the standard does not make that clear.

So I added the following text to the Abstract and to the Rationale:

> Though originally created for proxy contracts, diamond storage can be used to organize storage and data access within any smart contract.

---

**vitali_grabovski** (2025-10-15):

**Hi [@mudgen](/u/mudgen),**

It’s mostly clear and understandable. I have two remarks that might help:

1. After a single reading, it’s not 100% clear whether the use of /// @custom:storage-location erc8042: within this standard is optional or mandatory.
I suggest clarifying that it is mandatory when the storage struct is declared at the contract level. This aligns with ERC-7201: “Structs with this annotation found outside of contracts are not considered to be namespaces for any contract in the source code.”*
2. Since the goal of the standard is to use ascii characters, it might be helpful to enforce ASCII programmatically, especially when the storage struct and, more importantly, the storage slot are declared at the contract level.
The enforcement could be as simple as a helper function that validates ascii. See the following pseudocode:

`// note: declated as free funcntion`

```auto
function validateAsciiAndCalculateSlot(stringValue)
...
  bytes memory b = bytes(stringValue)

  bool isAscii = true;
  // ...
  // loop:
  // note: Reject the exact sequence: '\u' or '\x'
  if (
      b[i] == 0x5C &&             // 0x5C = '\'
      i + 1 < b.length &&         // ensure there's a next byte in array
      (b[i + 1] == 0x75 ||        // 0x75 = 'u'
        b[i + 1] == 0x78)          // 0x78 = 'x'
  ) {
      isAscii = false;
      break;
  }

  require(isAscii, 'not Ascii');

  return keccak256(stringValue)

...
```

`// note: declared at contract level`

```auto
contract SomeFacet {
...
// Storage defined using the ERC-8042 standard
// @custom:storage-location erc8042:diamonds.registry
struct MyDiamondStorage {
  address[] usersList;
  uint256 distribution;
}

bytes32 immutable MY_DIAMOND_INVALI_SLOT_ID = validateAsciiAndCalculateSlot("\ufdfd"); // will fail at deploy time
bytes32 immutable MY_DIAMOND_VALID_SLOT_ID = validateAsciiAndCalculateSlot("diamonds.registry"); // will deploy successfully

...
```

And the usage is:

```auto
// MyDiamondLibrary.getStorageAtSlot(MY_DIAMOND_VALID_SLOT_ID)
```

---

**nxt3d** (2025-10-15):

Just posted the first ERC that depends on ERC-8042.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1260)














####


      `master` ← `nxt3d:contract-metadata-erc`




          opened 11:22AM - 15 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/3857985?v=4)
            nxt3d](https://github.com/nxt3d)



          [+171
            -0](https://github.com/ethereum/ERCs/pull/1260/files)







### Summary

Introduces a standard for storing contract-level metadata onchain[…](https://github.com/ethereum/ERCs/pull/1260) using ERC-8042's Diamond Storage pattern. Extends ERC-7572's concept with onchain storage for cross-chain compatibility and upgradable contracts.

### Key Features

- **Diamond Storage**: Uses ERC-8042 for predictable storage locations
- **Cross-Chain Compatible**: Storage slots remain consistent across deployments
- **ERC-7572 Compatible**: Maintains compatibility with existing contract metadata standards
- **Upgradable Support**: Metadata persists through contract upgrades

### Technical Details

- Diamond Storage pattern for predictable storage locations
- Support for name, description, image, etc.

### Example Use Case

**Contract ENS Naming**: Any contract can store its ENS name using this standard:
- `name`: "MyToken"
- `description`: "A decentralized exchange for trading ERC-20 tokens"
- `ens_name`: "mycontract.eth"

This enables contracts to self-identify with ENS names while maintaining consistent metadata across chains and through upgrades.












### Summary

Introduces a standard for storing contract-level metadata onchain using ERC-8042’s Diamond Storage pattern. Extends ERC-7572’s concept with onchain storage for cross-chain compatibility and upgradable contracts.

### Key Features

- Diamond Storage: Uses ERC-8042 for predictable storage locations
- Cross-Chain Compatible: Storage slots remain consistent across deployments
- ERC-7572 Compatible: Maintains compatibility with existing contract metadata standards
- Upgradable Support: Metadata persists through contract upgrades

### Technical Details

- Diamond Storage pattern for predictable storage locations
- Support for name, description, image, etc.

### Example Use Case

**Contract ENS Naming**: Any contract can store its ENS name using this standard:

- name: “MyToken”
- description: “A decentralized exchange for trading ERC-20 tokens”
- ens_name: “mycontract.eth”

This enables contracts to self-identify with ENS names while maintaining consistent metadata across chains and through upgrades.

---

**mudgen** (2025-10-15):

Awesome! I reviewed the “Contract-Level Metadata with Diamond Storage” EIP and I think it is great.

---

**mudgen** (2025-10-16):

Hi [@vitali_grabovski](/u/vitali_grabovski), I like your function here:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vitali_grabovski/48/15798_2.png) vitali_grabovski:

> validateAsciiAndCalculateSlot

That can certainly be used to validate diamond storage identifiers, and I am glad to see this function and its implementation. However users don’t need to use it. If they want to they can look at the string literals and see if there are any hex or unicode escape sequences in it.

---

**mihaic195** (2025-10-16):

Hey [@mudgen](/u/mudgen),

> Though originally created for proxy contracts, diamond storage can be used to organize storage and data access within any smart contract.

Indeed, you are right, it can be used in any contract. I went through the EIP again, and it reads very well!

On another note, from my experience implementing ERC2535 Diamonds with many facets and their own diamond storage, I faced some challenges in deciding on the proper string format and versioning for the facet storage. It can easily become hard to manage and error-prone, increasing the risk of collision.

While the ERC8042 defines that it should use ASCII-enforced, human-readable, meaningful strings, it doesn’t provide a concrete naming scheme.

Maybe this is a good opportunity to have a concrete naming scheme, inspired by existing software engineering practices, for example:

- Reverse-DNS provides global uniqueness: org.example
- Protocol gives the name of the specific project or protocol: exchange
- Module is the logical sub-component or contract name for the storage: orderbook
- Major version as a suffix inspired by SemVer: v2

Examples:

- org.example.exchange.orderbook.v2
- com.acme.nft.registry.v2
- io.foo.access.roles.v1
etc.

To prevent storage slot churn, you would only bump the major version when you need a completely new storage slot, reorder fields, change field type/size, etc. Otherwise, simply add fields at the end of the struct, as usual.

If you still want to keep minor/patch versioning, you can do it through NatSpec.

Dots read well and mirror what EIPs already use. This could help avoid collisions in large contract systems that use diamond storage heavily, as it introduces a guide on the naming scheme.

What do you think?

---

**vitali_grabovski** (2025-10-16):

okay, but human typo / human error is always a case

---

**mudgen** (2025-10-16):

> okay, but human typo / human error is always a case

That is true!

---

**mudgen** (2025-10-16):

> Indeed, you are right, it can be used in any contract. I went through the EIP again, and it reads very well!

Great!

> On another note, from my experience implementing ERC2535 Diamonds with many facets and their own diamond storage, I faced some challenges in deciding on the proper string format and versioning for the facet storage. It can easily become hard to manage and error-prone, increasing the risk of collision.

Are any of your implementations of ERC2535 with facets deployed onchain with verified source code? Or do you have links to code repositories I could look at? I’d like to look at some of what you have done with ERC2535 and facets.

I myself have not experienced any difficulty or challenge with making human readable, meaningful strings for diamond storage. I would like to understand better and with more detail what challenge you have had with this. Can you give more data and specifics about it?

> Maybe this is a good opportunity to have a concrete naming scheme, inspired by existing software engineering practices, for example:

I think it is great to have naming schemes and rules for diamond storage and I encourage that, and I like the examples and suggestions you made. I think that naming schemes add more meaning to strings, which follows the idea that diamond storage identifiers should be meaningful. However, the EIP as currently written covers diamond storage with restrictions that make it general, workable and secure. Within this EIP I do not want to move beyond its current scope with recommendations, or functionality etc. However I would be *happy* to support new EIPs that recommend naming schemes, more knowledge and information, additional functionality etc. for ERC-8042 diamond storage. They could be new ERCs or Informational EIPs ([see EIP-1 about Informational EIPs](https://eips.ethereum.org/EIPS/eip-1#eip-types)).

---

**Vagabond** (2025-10-16):

Hey [@mudgen](/u/mudgen)

I think it might be better if we had a mechanism to check whether a storage position has already been taken and require another confirmation (like a boolean flag) before reusing that identifier in another library.

Also, I believe storage identifiers should carry some business meaning — for example, reflecting the domain of the selectors that use it, so developers can immediately understand what the storage is for.

Example:

system.diamond.storage

service.authentication.v.0.0.1

service.allowance.v.0.0.1

What do you think?

---

**mudgen** (2025-10-17):

Thanks for your input [@Vagabond](/u/vagabond).

> I think it might be better if we had a mechanism to check whether a storage position has already been taken and require another confirmation (like a boolean flag) before reusing that identifier in another library.

Okay, that could be good. But its outside the scope of this EIP. Each library should ensure they use a diamonds storage identifier naming convention that ensures their diamond storage struct locations are unique, such as `"mylibraryname.erc"` etc.

> Also, I believe storage identifiers should carry some business meaning — for example, reflecting the domain of the selectors that use it, so developers can immediately understand what the storage is for.
> Example:
> system.diamond.storage
> service.authentication.v.0.0.1
> service.allowance.v.0.0.1
> What do you think?

I agree, but they should also be prefixed with the name of the project or company or organization to ensure such identifiers are unique.  I think a new EIP could be made to suggest or recommend naming schemes for diamond storage identifiers.

---

**mihaic195** (2025-10-18):

Hey [@mudgen](/u/mudgen),

I don’t have the full source verified on-chain and the repo is private, but I can outline the architecture.

### Motivation

We needed to create a contract system capable of handling a large number of features for token sales (also known as token presales). The goal was to cleanly separate admin controls from user-facing execution and have a standardized upgrade process. We ended up using a versioned Diamond (ERC-2535).

### Components

#### Diamond (Admin Hub)

- Holds a versioned facet registry (e.g., v0 for admin facets like diamondCut, diamondLoupe, ownership, etc.).
- It maps (version, function selector) → facet address. This is the only storage it keeps.

#### Token Sale Proxies (Execution Logic)

- Each token sale is a proxy with its own isolated storage.
- Every proxy is pinned to an immutable version number, representing the facet version set used at runtime.

#### Logic Facets (Versioned: v1, v2, etc.)

- Each version bundles a feature set for token sale behavior. Different token sales can pick different versions while remaining consistent within a chosen version.

### How It Works

1. A user deploys a new token sale proxy.
2. The proxy owns the token sale-specific storage.
3. A user call hits the proxy with a function selector.
4. The proxy queries the Diamond for the facet address using its immutable version and function selector (version, selector).
5. The Diamond returns the matching facet address from its versioned registry.
6. The proxy then delegatecall to that facet.
7. The facet executes in the proxy’s storage context to read/write the token sale’s state. The Diamond’s storage remains untouched.

### Storage Model

- Diamond storage: facet registry + admin data only.
- Proxy (token sale) storage: isolated libraries laid out using ERC-8042 conventions for clarity and collision avoidance.
- Context preservation: msg.sender, msg.value, and storage context stay with the proxy across delegation.

## Benefits

User-facing logic is upgradeable by version while preserving strict storage isolation between:

- the Diamond (central admin hub for facets) and,
- each proxy deployment (sale state).

### TL;DR

The Diamond’s sole job is routing across versioned facets. It does not execute business logic.

Each token sale proxy declares multiple storage layouts in an ERC-8042 manner, each based on a specific facet’s logic. The facets operate in the proxy’s storage context. Together, those proxy storage libraries create the full token sale storage layout for that version.

### Challenges we faced

- Storage slot management across versioned facets (exactly my point in the suggestion above), increasing the risk of collision.
- Version complexity, i.e., maintaining multiple storage layouts and ensuring compatibility across versions.

---

**mudgen** (2025-10-19):

[@mihaic195](/u/mihaic195) thanks for that data. That helps me understand what you are building and some of the design of it.

But I don’t have enough details to know how these things were a challenge:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mihaic195/48/15506_2.png) mihaic195:

> ### Challenges we faced
>
>
>
> Storage slot management across versioned facets (exactly my point in the suggestion above), increasing the risk of collision.
> Version complexity, i.e., maintaining multiple storage layouts and ensuring compatibility across versions.

Why were these challenges? Can you tell the details of what you ran into exactly which was a challenge?


*(8 more replies not shown)*
