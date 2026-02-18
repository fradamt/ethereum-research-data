---
source: magicians
topic_id: 14796
title: "EIP-7201: Namespaced Storage Layout"
author: frangio
date: "2023-06-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7201-namespaced-storage-layout/14796
views: 6969
likes: 22
posts_count: 38
---

# EIP-7201: Namespaced Storage Layout

> We define a formula to derive a location in storage, that is suitable for structs of arbitrary size, from an identifier. The formula is chosen to be safe against collisions with the standard Solidity storage layout. We define a convention to document this location in Solidity source code.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7201)





###



Conventions for the storage location of structs in the namespaced storage pattern.

## Replies

**Ramarti** (2023-07-05):

Decoupling this into a simpler, more self-contained EIP looks like a good idea to me ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

My only comment would be that the reference implementation (which is probably pseudocode) it’s not compiling.

As it is, it would need a `bytes32` casting when calculating MAIN_STORAGE_LOCATION

`bytes32 private immutable MAIN_STORAGE_LOCATION = keccak256(bytes.concat(bytes32(uint256(keccak256("example.main")) - 1)));`

Which then gives us

`TypeError: Assembly access to immutable variables is not supported.`

Changing it to constant (which would need a change from `bytes.concat` to `abi.encode`, since it seems that `bytes.concat` is not considered compile-time constant) still does not work:

`TypeError: Only direct number constants and references to such constants are supported by inline assembly.`

So I would suggest changing the MAIN_STORAGE_LOCATION in the reference implementation to:

```auto
// keccak256(abi.encode(uint256(keccak256("example.main")) - 1))
bytes32 private constant MAIN_STORAGE_LOCATION = 0x183a6125c38840424c4a85fa12bab2ab606c4b6d0e7cc73c0c06ba5300eab5da;
```

For people to play around with it faster.

---

**frangio** (2023-07-06):

Thanks! All true. I’ve pushed the change:

https://github.com/ethereum/EIPs/pull/7287

---

**conner** (2023-08-01):

I’ve been finding similar intuitions in development of upgradeable contracts and appreciate you making an EIP to formalize this!

---

**frangio** (2023-08-24):

We’re proposing one small change to the formula and moving this to Last Call:

https://github.com/ethereum/EIPs/pull/7519

> namespace locations are aligned to 256 as a potential optimization, in anticipation of gas schedule changes after the Verkle state tree migration, which may cause groups of 256 storage slots to become warm all at once.

---

**KaiHiroi** (2023-08-31):

Hello,

I hope you’re doing well! I would like to discuss a point regarding the EIP. I believe that this EIP will become an essential standard for creating modular and upgradeable contracts.

I have a specific question regarding the final sentence of the specification, which reads: “Structs with this annotation found outside of contracts are not considered to be namespaces for any contract in the source code.”

Do Structs need to be located within (storage or proxy) contracts?

Considering the context of the Diamond Standard, where Diamonds and Facets collaborate, and the Proxy acts as the storage layer while Implementations function as the logic layer, it’s common for Structs to exist in Implementations or the libraries they use, rather than in the Proxy contract. In fact, the sample code for the Diamond Standard on GitHub ([GitHub - mudgen/diamond-3-hardhat: EIP-2535 Diamond reference implementation using Hardhat and Solidity 0.8.*](https://github.com/mudgen/diamond-3-hardhat)) follows this approach.

Based on my current understanding, I would actually appreciate it if annotations outside of contracts were also processed, as it aligns with this interpretation.

---

**frangio** (2023-09-01):

Perhaps the phrasing is not clear enough, but it’s not saying that the struct should be defined in the Proxy contract. It’s absolutely expected that there won’t be any namespace structs defined in the Proxy contract.

What we mean is something like this:

```auto
/// @custom:storage-location erc7201:example
struct ExampleStorage {
    uint256 x;
    uint256 y;
}

contract Example {
    ...

    function _getXTimesY() internal view returns (uint256) {
        MainStorage storage $ = _getMainStorage();
        return $.x * $.y;
    }
}
```

Here `MainStorage` is defined outside of `Example`, so it’s not associated to the `Example` contract.

The struct definition has to be inside `Example`. Potentially it might be in some other contract and then inherited, which also brings it into “scope”.

This is just like normal storage variables. You can only define storage variables inside contracts, the compiler will error if you do otherwise.

---

**dror** (2023-09-01):

This is a great proposal.

What is missing is simpler support at the compiler level.

I’d like to suggest adding a solidity `pragma namespace id`

Which changes the current “root” for all further storage references.

Normally, contracts will have a single “namespace”, though a “shell” contract like [SafeStorage](https://github.com/safe-global/safe-contracts/blob/82dfcc8c0cf21c0f76db354d691d668093fe1618/contracts/libraries/SafeStorage.sol#L10) might want reference multiple namespaces.

The above example can be written as:

```js
contract Example {
pragma namespace example;
    uint256 x;
    uint256 y;
    ...

    function _getXTimesY() internal view returns (uint256) {
        return x*y;
    }
}
```

---

**KaiHiroi** (2023-09-04):

Thank you for your response. I have understood the points you’ve made.

To account for inheritance and library usage, how about modifying the final sentence to: “In order to enable this annotation, Structs MUST be defined within the scope of a contract through direct declaration, inheritance, or explicit referencing.” Does this suggestion align well with the intended context?

---

**SamWilsn** (2023-09-05):

I’d very strongly recommend getting feedback from the Solidity team (apologies if any of you are involved there.)

---

**mudgen** (2023-09-15):

The added complication and gas cost of using `- 1) & ~0xff` to create the final hash is unnecessary.  The [Rationale](https://eips.ethereum.org/EIPS/eip-7201#rationale) given about it is irrational because the probability of hash/storage collision is too little to matter. If you don’t believe it then get a statistician to give some data on the probability of collision.

Also keep in mind that Solidity strings, bytes, dynamic arrays and values stored in mappings are stored in random locations in storage using keccak256. Does the Solidity implementation prevent them from being stored in Solidity layout storage locations?  No, because it is unnecessary.

There is another point which is that the [Rational](https://eips.ethereum.org/EIPS/eip-7201#rationale) gives the idea that it is okay to declare state variables outside diamond or namespace storage in upgradeable smart contracts. Doing that should be discouraged because that causes bugs.

---

**frangio** (2023-09-15):

There is no added gas cost from those operations. The storage locations should be constants in bytecode.

Hash collision probability is negligible. That’s definitely not the concern. The concern is “preimage collision”: for example, making sure that a namespace called `"foo"` will not land at the same place as `m["foo"]` for some mapping `m` because of the way the hash preimage is constructed. This may seem trivial but is important to check. Solidity had to answer the same question when designing its storage layout.

---

**mudgen** (2023-09-16):

> There is no added gas cost from those operations. The storage locations should be constants in bytecode.

Yes, I see that you use a constant so there is no gas cost.  That is excellent.

> Hash collision probability is negligible. That’s definitely not the concern. The concern is “preimage collision”: for example, making sure that a namespace called "foo" will not land at the same place as m["foo"] for some mapping m because of the way the hash preimage is constructed. This may seem trivial but is important to check. Solidity had to answer the same question when designing its storage layout.

But it is not true that a namespace called `"foo"` (or any other string with only visible characters) will ever land at the same place as `m["foo"]` (or other mapping) because of the way the hash preimage is constructed. There is no problem to solve here.

If you keccak256 a single string, for example “example.main”, or “foo” and use that as the namespace without doing anything else to it, then a preimage collision with Solidity’s storage layout is not possible. So anything done to prevent that is not needed. If someone disagrees with this then please show a working example of a preimage collision with Solidity storage layout and a keccak256 of a single string containing only visible characters as the namespace for a struct.

---

**frangio** (2023-09-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> But it is not true that a namespace called "foo" (or any other string with only visible characters) will ever land at the same place as m["foo"]

It is definitely possible to find a key `k` such that the slot of a mapping value `m[k]` is a string `s` of 32 printable ASCII characters, and if this is an array then `m[k][0]` will land at `keccak256(s)`. The probability is 1e-14, making it difficult but feasible to mine one, and if we can design namespaces such that the probability is reduced to the same as finding a hash collision (60 orders of magnitude smaller), why wouldn’t we do that…

I find this a weird criticism. It would be fair to say “don’t overthink it”, but we definitely wanted to at least consider it and have a rough idea that it would be ok for arbitrary namespace ids.

---

**mudgen** (2023-09-19):

Let’s look at this example:

```auto
contract Example {

    bytes32 internal constant STORAGE_SLOT = keccak256('example.storage');

    // Any value stored in this mapping is stored at keccak256(abi.encodePacked(string,bytes32(0)))
    // mapping defined at storage slot 0
    mapping(string => uint256) private map;
}
```

In the above example `STORAGE_SLOT` is the namepace that is used to retrieve/write to a struct using diamond/namespace storage.

In the above example the `map` variable is declared at storage slot 0. All mappings use their storage slot position and a key in calculating the location that values are stored in them.

In the above example the storage location of any value put into `map` is calculated with ` keccak256(abi.encodePacked(string,bytes32(0)))`. That is the keccak256 hash of a string key concatenated with 32 bytes of `0` null values. Because the storage slot position of `map` is included in the calculation of where to store values in it, the preimage (inputs of  keccak256) of `map` will never be `example.storage`. So there is no concern of preimage collision.

My point is this: if preimage collisions (same inputs to `keccak256`)  are not possible with the namespace strings that are used and we are not concerned with `keccak256` hash collisions, then why guard against them using `- 1) & ~0xff` to generate a final hash?

If you feel that preimage collisions are possible between mappings and a namespace generated with `keccak256('example.storage')` or other string that would be used and is hashed with `keccak256` then can you please explain exactly how that is possible and/or show an example?

> I find this a weird criticism. It would be fair to say “don’t overthink it”, but we definitely wanted to at least consider it and have a rough idea that it would be ok for arbitrary namespace ids.

I am hard about this point because many people have already been using diamond/namespace storage without the `- 1) & ~0xff` solution. It will cause confusion if this solution is included in the standard and it is not necessary or needed.

---

**mudgen** (2023-09-19):

> It is definitely possible to find a key k such that the slot of a mapping value m[k] is a string s of 32 printable ASCII characters, and if this is an array then m[k][0] will land at keccak256(s). The probability is 1e-14, making it difficult but feasible to mine one, and if we can design namespaces such that the probability is reduced to the same as finding a hash collision (60 orders of magnitude smaller), why wouldn’t we do that…

Perhaps it could be possible to find a key in a mapping that generates a storage slot address that is 32 printable characters. But they would be random characters.  Not something that would match a namespace that was used. The chances of mining a namespace that was used is the same chance of mining other hashes that are used.

I understand that a malicious developer might be able to use a random set of 32 characters (if he/she is able to mine it) as a namespace string in order to intentionally mess up his own contract he is writing or scam users. However there are easier ways to obscure the intentions of a developer such as not verifying source code and using assembly.  Also it is easy to see that a namespace string is 32 random characters and is therefore considered malicious. Even if `- 1) & ~0xff` is included in the standard, malicious developers can still do this scam by not following the standard by not using `- 1) & ~0xff`. Information about this could be included in the security considerations of the standard.

I suggest not doing the ` - 1) & ~0xff` solution because it isn’t needed and because diamond/namespace storage has already been adopted by many projects and people without that solution. Having that solution will create two different versions of namespace/diamond storage and friction and confusion between them.

It would be useful and advantageous for adoption if the standard was written in a way that made the existing implementations of diamond/namespace storage compliant with it.

Just to give some data on this:  The [EIP-2535](https://eips.ethereum.org/EIPS/eip-2535) standard contains within it an example of diamond/namespace storage and a reference implementation that uses diamond/namespace storage.  They don’t use the `- 1) & ~0xff` solution.

Most or all EIP-2535 diamond implementations are using diamond/namespace storage without the solution.

The diamond reference implementations use diamond/namespace storage without the solution.

There is a list of over 85 projects on [Awesome Diamonds](https://github.com/mudgen/awesome-diamonds#projects-using-diamonds) that are using EIP-2535 Diamonds. [Louper.dev](https://louper.dev/) is tracking close to 4000 diamonds deployed across many blockchains.

The [solidstate-solidity](https://github.com/solidstate-network/solidstate-solidity) library extensively uses diamond/namespace storage without the solution. I know it is being used by a number of projects.

[ERC721A-Upgradeable](https://github.com/chiru-labs/ERC721A-Upgradeable) is using diamond/namespace storage without the solution.

It is hard to know the extent that diamond/namespace storage is already being used by various projects.

---

**frangio** (2023-09-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> I am hard about this point because many people have already been using diamond/namespace storage without the - 1) & ~0xff solution.

This is fine and completely compatible with this EIP! We designed the annotation to be forward-compatible with other ways to compute namespace locations.

I’d recommend publishing an EIP that builds on EIP-7201’s `@custom:storage-location` but defines a different storage location function. If this new EIP is called EIP-9999, developers would write `@custom:storage-location eip9999:example.storage` to specify that location is `keccak256("example.storage")`.

You could also write something like `@custom:storage-location keccak256:example.storage`, or reuse EIP-2535 as `@custom:storage-location eip2535:example.storage`, but I wouldn’t recommend either of these options since they wouldn’t be standardized.

For us it was important to make namespace locations as disjoint as possible from the standard Solidity layout because the code we write has to be maximally generic. For others the considerations may be different.

---

**mudgen** (2023-09-22):

> This is fine and completely compatible with this EIP! We designed the annotation to be forward-compatible with other ways to compute namespace locations.

Simply hashing a string is not compatible with the EIP.  The specification specifically says this:

> The storage location for a namespace is defined as ns_loc(id: string) = keccak256(keccak256(id) - 1) & ~0xff.

So just doing `bytes32 internal constant STORAGE_SLOT = keccak256('example.storage');` is not compatible with the EIP because it is doing something else than what the specification says.

The Rationale given in the standard is misleading:

> A requirement for the root is that it shouldn’t overlap with any storage location that would be part of the standard storage tree used by Solidity and Vyper (root = 0), nor should it be part of the storage tree derived from any other namespace (another root). This is so that multiple namespaces may be used alongside each other and alongside the standard storage layout, either deliberately or accidentally, without colliding. The term keccak256(id) - 1 in the formula is chosen as a location that is unused by Solidity, but this is not used as the final location because namespaces can be larger than 1 slot and would extend into keccak256(id) + n, which is potentially used by Solidity. A second hash is added to prevent this and guarantee that namespaces are completely disjoint from standard storage, assuming keccak256 collision resistance and that arrays are not unreasonably large.

It is misleading because any meaningful string that is simply hashed with `keccak256` already meets the requirement "that it shouldn’t overlap with any storage location that would be part of the standard storage tree used by Solidity and Vyper (root = 0), nor should it be part of the storage tree derived from any other namespace (another root). "

Hashing a meaningful string is how people have been doing it. This standard as written invalidates and makes wrong existing documentation and how people have been doing it for the past three years, when there is nothing wrong with how they have been implementing namespace/diamond storage.

I suggest changing the specification to say that a namespace is calculated by hashing a meaningful string with keccak256. That is technically accurate, secure, and is backward compatible with the use of namespace/diamond storage over the past three years.

---

**frangio** (2023-09-22):

I don’t think my last point was understood so I’m going to elaborate.

This EIP defines two things:

1. A NatSpec annotation to document the namespaces in a contract and their storage location.
2. A specific function to compute namespace locations from namespace ids (the part @mudgen disagrees with).

These two things can be decoupled. The NatSpec annotation was designed with a format that can be used with other functions.

If a contract uses the function we define in EIP-7201, the annotation would look like this:

`/// @custom:storage-location **erc7201:**foobar`

Suppose now that ERC-9999 defines a different function `nsloc(id: string) = keccak256(id)` like [@mudgen](/u/mudgen) suggests. A contract that uses ERC-9999 namespaces can write:

`/// @custom:storage-location **erc9999:**foobar`

This is what I mean when I say that it would be compatible with the EIP.

I thought this would be clear from the EIP text but it seems like it isn’t and it should be made explicit.

It might also be worth noting: A contract may use namespaces / diamond storage without using `@custom:storage-location` annotations. This EIP is not monopolizing the pattern, just providing a tool and guidelines that can improve interoperability when the pattern is used.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> any meaningful string that is simply hashed with keccak256 already meets the requirement […]

I already explained why this is not strictly true so I’ll refer to my previous messages. I’ll just re-emphasize this point:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> For us it was important to make namespace locations as disjoint as possible from the standard Solidity layout because the code we write has to be maximally generic. For others the considerations may be different.

---

**frangio** (2023-09-22):

Updated the EIP to make it explicit that different formulas can be used and how:

https://github.com/ethereum/EIPs/pull/7760

---

**mudgen** (2023-09-23):

[@frangio](/u/frangio) Understood about the NatSpec annotation and that’s great.

> I already explained why this is not strictly true so I’ll refer to my previous messages. I’ll just re-emphasize this point:

This is what I am trying to say, *it is strictly true*. Your earlier message said this:

> It is definitely possible to find a key k such that the slot of a mapping value m[k] is a string s of 32 printable ASCII characters, and if this is an array then m[k][0] will land at keccak256(s). The probability is 1e-14, making it difficult but feasible to mine one  and if we can design namespaces such that the probability is reduced to the same as finding a hash collision (60 orders of magnitude smaller),

What your description fails to mention here is that if it was possible to mine such a thing it would generate 32 *random* printable characters. I am proposing to `keccak256` a *meaningful* string. That is different than exactly 32 random characters. To try to mine a specific meaningful string is the same as trying to find a hash collision.

Here is an example of a meaningful namespace string `"openzeppelin.storage.ERC20"`

> For us it was important to make namespace locations as disjoint as possible from the standard Solidity layout because the code we write has to be maximally generic. For others the considerations may be different.

Hashing a meaningful string with `keccak256` is already disjoint from standard Solidity layout. This is no problem about having accidental collisions with Solidity using this simple method. Can you show or explain any problems that could happen with this?

Namespace/diamond storage is not new. It has been in use for years by many projects. If a new standard is going to change how it works I think it should have a good reason for doing so.


*(17 more replies not shown)*
