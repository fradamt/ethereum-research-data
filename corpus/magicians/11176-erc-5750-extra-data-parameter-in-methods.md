---
source: magicians
topic_id: 11176
title: ERC-5750 Extra Data Parameter in Methods
author: xinbenlv
date: "2022-10-04"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-5750-extra-data-parameter-in-methods/11176
views: 3060
likes: 1
posts_count: 20
---

# ERC-5750 Extra Data Parameter in Methods

Hi all, I am proposing an EIP-5750 to denote and designate the last parameters method as extra data.

Here is the pull request: [Add EIP-5750: Method with Extra Data by xinbenlv · Pull Request #5750 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5750/files)

To save you a click away, I add a snapshot here

---

## eip: 5750
title: Extra Data Parameter in Methods
description: This EIP that defines an extra data parameter in methods.
author: Zainan Victor Zhou ()
discussions-to:
status: Review
type: Standards Track
category: ERC
created: 2022-10-04

## Abstract

This EIP that defines an extra data parameter in methods, denoted as `methodName(... bytes calldata _data)`. Compliant method of compliant contract

can use the extra data in structural way to introduce extended behaviors.

## Motivation

The general purpose of having a standard for extra data in a method is to allow further extensions for a existing method interface. For example, the `safeTransferFrom` already

1. At the very least, Methods complying with this EIP, such as transfer and vote can add reasons in extra data, just like how GovernorBravo’s improvement over GovernorAlpha
2. In addition, existing EIPs that has exported methods compliant with this EIP can be extended for behaviors such as using the extra data for endorsements or salt, nonce, commitments for reveal commit.
3. Allowing one method to carry arbitrary calldata for forwarding a function call to another method.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

1. Any compliant contract’s compliant method MUST have a bytes(dynamic size) as its LAST parameter of the method.

```solidity
function methodName(type1 param1, type2, param2 ... bytes calldata data);
```

## Rationale

1. Having a dynamic sized bytes allow for maximum flexibility for arbitrary additional payload
2. Having the bytes specified in the last naturally compatible with the calldata layout of solidity.

## Backwards Compatibility

Many of the existing EIPs already have compliant method and all compliant contracts of such EIPs are already compliant.

Here are an incomplete list

1. In the EIP-721 the following methods are already compliant:

- function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data) external payable; is already compliant

1. In the EIP-1155 the following methods are already compliant

- function safeTransferFrom(address _from, address _to, uint256 _id, uint256 _value, bytes calldata _data) external;
- function safeBatchTransferFrom(address _from, address _to, uint256[] calldata _ids, uint256[] calldata _values, bytes calldata _data) external;

1. In the EIP-777 the following methods are already compliant

- function burn(uint256 amount, bytes calldata data) external;
- function send(address to, uint256 amount, bytes calldata data) external;

1. In the EIP-2535 the following methods are already compliant

```solidity
function diamondCut(
        FacetCut[] calldata _diamondCut,
        address _init,
        bytes calldata _calldata
    ) external;
```

1. In the EIP-1271 the following methods are already compliant:

```solidity
  function isValidSignature(
    bytes32 _hash,
    bytes memory _signature)
    public
    view
    returns (bytes4 magicValue);
```

## Security Considerations

1. If using the extra data for extended behavior, such as supplying signature for onchain verification, or supplying commitments in a commit-reveal scheme, the security best practice shall be followed for that particular extended behaviors.
2. Compliant contract shall also take into consideration the information of extra data will be shared in public and circulate around mempool, so specific caution shall be paid for replay-attack, front-run/back-run/sandwich attacks.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**xinbenlv** (2022-10-31):

Posting some good questions from [@SamWilsn](/u/samwilsn)  from the EIPs PR



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5785/files)














####


      `master` ← `xinbenlv:ed`




          opened 05:54PM - 15 Oct 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/7/79e3637a5e42046bea894d923808ca0765bd7dee.png)
            xinbenlv](https://github.com/xinbenlv)



          [+28
            -5](https://github.com/ethereum/EIPs/pull/5785/files)







A relatively straightforward












[@SamWilsn](/u/samwilsn)

> Why does this EIP need to exist? I think this is a great recommendation, but we don’t want the EIPs repository to become a catalogue of Solidity best practices. You need to make the case in your Motivation for why this pattern needs its own standard.

[@Pandapip1](/u/pandapip1)

> I see no reason why best practices shouldn’t be standards. I could see the type being changed to informational, though.

Here is author answer

> Just to be clear, this EIP is not a “recommendation” or “best practice”. EIP intend to serve as a a protocol/standard specifying format of method and their behavior. Unlike a lot of other ERCs that specifying the name and all parameters, this EIP specifies only the last data and its format, which makes it maximally compatible, both future and backward.
>
>
> It could be confusing, so let me make a metaphor here:
>
>
> If someone says: “I’d recommend you drive your car on the right side of the road because it has benefit of we bump into each other less” it’s an informational EIP.
> If someone says, “For all standard-compliant road, let’s designate its right side of the road to be reserved for forward traffic, so we can future agree to which side to build traffic lights, ramps, lightings, fire stations…”, it’s an ERC EIP
>
>
> This EIP serves for the standardizing purpose: There are a thousand ways to extend methods, but this EIP ask to designate certain place and format for extending behaviors. EIPs like EIP-5453(#5453) and EIP-5732(#5732) can all benefit from this EIP if they can rely on that a parameter in a given method is being designated for extending behavior.

---

**frangio** (2022-11-28):

Can you elaborate on this part of the EIP?

> Having the bytes specified as the last parameter makes this EIP compatible with the calldata layout of solidity.

---

**xinbenlv** (2022-11-30):

[@frangio](/u/frangio)  thank you for the question

The Solidity language structure the calldata layout as follows, as documented in [1](https://docs.soliditylang.org/en/v0.8.13/internals/layout_in_calldata.html), [2](https://docs.soliditylang.org/en/v0.8.13/abi-spec.html#function-selector-and-argument-encoding):

> All in all, a call to the function f with parameters a_1, ..., a_n is encoded as
>
>
>
> function_selector(f) enc((a_1, ..., a_n))

Thus, if we choose the bytes that will be designated for extension to locate in the *last one* of all parameters of a function, then we can use that in nesting data, we will be able to assume the same location of data in all methods that conform this rule.

But if we don’t designate the last bytes to be extaData, but alternatively choose the *second from last field as a standard*, then this is what could happen

One of standard’s implementation choose to put a string field after extraData

```auto
function foo(uint8 param1, bytes calldata extraData, string param2);
```

another of standard’s implementation choose to put a uint8 after extraData

```auto
function bar(uint8 param1, bytes calldata extraData, uint8 param2);
```

Then it’s not very easy nor gas efficient to figure out where extraData locates in such scenario.

But if we choose the last one, both implementations will have to be

```auto
function foo(uint8 param1, string param2, bytes calldata extraData);
```

```auto
function bar(uint8 param1, uint8 param2, bytes calldata extraData);
```

Then we can reliably always know the last parameter (meaning, zero from ending byte), are the `extraData` field.

One more real world example is for “EIP Endorsement”, we could choose to say: if this last 32 bytes is keccak256(“SOME_MAGIC_WORD”), we will interpret the extending data as endorsement and try to parse it, see EIP-5453 Endorsement (WIP)

It also helps when we try to do nested calls, e.g.

```auto
SomeERC721 is ERC5679MintAndBurn {

  function burn(from, extraData) {
    // send a call to another function via parsing extraData
    // then
    _burn(from, []);
  }
}
```

Hope these descriptions and helps me explain myself more clearer, if not I will create some more deployable contract examples soon and get back with those examples

---

**devinaconley** (2022-12-01):

Interesting proposal [@xinbenlv](/u/xinbenlv)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> ```auto
> function methodName(type1 param1, type2, param2 ... bytes calldata data);
> ```

Functionally, is the requirement that any implementing contract must treat the `bytes` parameter as optional and non-critical?

---

**xinbenlv** (2022-12-01):

[@devinaconley](/u/devinaconley) not necessarily,

When a contract.method has last bytes and use the first N bytes, the remaining of `bytes` after Nth are always optional and non-critical.

For example, in one of the Commit-Reveal implementation, this particular line



      [github.com](https://github.com/ercref/ercref-contracts/blob/e833633a65de5910ed34e98681278b931993d1b8/ERCs/eip-5732/contracts/CommitableERC721.sol#L43)





####



```sol


1. {
2. return super.supportsInterface(interfaceId);
3. }
4.
5. function safeMint(
6. address _to,
7. uint256 _tokenId,
8. bytes calldata _extraData
9. )   onlyCommited(
10. abi.encodePacked(_to, _tokenId),
11. bytes32(_extraData[0:32]), // The first 32bytes of safeMint._extraData is being used as salt
12. MANDATORY_BLOCKNUM_GAP
13. )
14. external {
15. _safeMint(_to, _tokenId); // ignoring _extraData in this simple reference implementation.
16. }
17.
18. function get165Core() external pure returns (bytes4) {
19. return type(IERC_COMMIT_CORE).interfaceId;
20. }
21.


```










uses first 0-32 bytes for `salt`, the the remaining bytes after 32th byte could be used for extension behavior.

---

**frangio** (2022-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Then we can reliably always know the last parameter (meaning, zero from ending byte), are the extraData field.

Given a function `foo(uint x, string s, bytes extraData)` there is no guarantee that `extraData` will be the last thing in calldata. More generally, if there are multiple dynamic types there is no guarantee of their ordering in calldata. Do you agree with this? See [Use of Dynamic Types](https://docs.soliditylang.org/en/v0.8.9/abi-spec.html?highlight=indexed#use-of-dynamic-types) in the Solidity docs on ABI encoding.

---

**xinbenlv** (2022-12-02):

I am not sure if I follow your word here:

> Given a function foo(uint x, string s, bytes extraData) there is no guarantee that extraData will be the last thing in calldata.

Based on solidity’s calldata (in the context of `calldata` vs `storage`, not to be confused with other meaning of calldata) the structure of

```auto
foo(uint x, string s, bytes extraData);
```

based on the encoding rule: `function_selector(f) enc((a_1, ..., a_n))`

will be a concatenation of

- d1. method selector = keccak256("foo(uint256,string,bytes)")[0:3]
- d2. encoded uint x which is x
- offsetOfD3 for location of d3
- offsetOfD4 for location of d4
- d3. encoded string s which is padded32(length(s)) || uint256 of each bytes of s's content
- d4 encoded bytes extraData which is extraData's length per 32bytes || content of extraData padded last one to full 32bytes

The overall becomes `d1 || d2 || offsetOfD3 || offsetOfD4 || d3 || d4`.

(Updated with frangio’s correction.)

---

**frangio** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> The overall becomes d1 || d2 || d3 || d4.

This is not correct. In the simplest case, the encoding will be:

```auto
d1 || d2 || X || Y || d3 || d4
                      ^X    ^Y
```

With `X` and `Y` the offsets where `d3` and `d4` respectively start.

Although this is the canonical encoding that Solidity will produce, the decoding routines support other non-canonical encodings such as:

```auto
d1 || d2 || X || Y || d4 || d3
                      ^Y    ^X
```

As a consequence, it is not possible to predict the location of a dynamic `bytes` type in calldata.

---

**xinbenlv** (2022-12-02):

[@frangio](/u/frangio)

Oh, you are right. Thanks for the correction, yes there are offset X and Y to indicate place of such dynamic types in tail parts.

You made a very good point that I didn’t think of when drafting this EIP, which is with non-canonical encoding, it’s possible to even have reverse location of bytes, or some trick in having overlaps for different data fields (maybe, due to malicious TX or for saving gas cost maybe?). So there is no guarantee of last bytes being physically last one.

This fact you point out did weaken one of the rationales for mandating `extraData` as *last* one so the remaining rationale is majorly due to conventions.

For non-canonical encoded contract this could be even a potential security issue if interacting clients/contract assumes so. An action item for me is to think of how to add this as a security considerations. I will send a PR.

I appreciate your feedback and let me know if there are other advice.

---

**frangio** (2022-12-02):

Given this, I think the justification for this ERC has lost a lot of weight. I’m not sure that I see the point in standardizing this.

---

**xinbenlv** (2022-12-02):

[@frangio](/u/frangio) If there is no value of this standard, this EIP could just get ignored and quietly stay in the corner.

I hold the views that there are still many features that could utilize EIP-5750 and demonstrating having an extension field have a lot of benefits. I am working on a few ideas that actually requires EIP-5750 and will invite/notify you to review when those are ready for reviews.

---

**xinbenlv** (2022-12-15):

[@frangio](/u/frangio)

EIP-5453 is an example why I think this EIP-5750 is useful

See reference implementation


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/ercref/ercref-contracts/tree/main/ERCs/eip-5453)





###



[main/ERCs/eip-5453](https://github.com/ercref/ercref-contracts/tree/main/ERCs/eip-5453)



ERC Reference Implementations. Contribute to ercref/ercref-contracts development by creating an account on GitHub.

---

**xinbenlv** (2023-01-04):

[@frangio](/u/frangio)

EIP-5750 opens up all sorts of extensionability, e.g.

1. Supplying salt with EIP-5732 Commit Service for Commit-Reveal scheme
2. Supplying endorsement for same-TX permit using EIP-5453, or in separate TX by ERC-2612 or ERC-4494
3. Avoid the limitation of EIP-1271 which is being solved by Add EIP-6066: Signature Validation Method for NFTs by boyuanx · Pull Request #6066 · ethereum/EIPs · GitHub
4. Avoid the limitation of original domain separator lacking “extensions” in EIP-712 being addressed by EIP-5267: Retrieval of EIP-712 domain which is proposing an uint256[] extensions

Let’s continue the discussion on EIP-5750.

---

**frangio** (2023-01-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Avoid the limitation of original domain separator lacking “extensions” in EIP-712 being addressed by EIP-5267: Retrieval of EIP-712 domain which is proposing an uint256[] extensions

I think you misinterpreted this. EIP-712 is already extensible. It says:

> Future extensions to this standard can add new fields with new user-agent behaviour constraints. User-agents are free to use the provided information to inform/warn users or refuse signing. Dapp implementers should not add private fields, new fields should be proposed through the EIP process.

The `uint[] extensions` in EIP-5267 is just a manifestation of this existing bit of the spec.

I think this serves to exemplify why I think this EIP’s approach to extensibility doesn’t work. EIP-712 and EIP-5267 are extensible through the `extensions` array, but the difference is that the EIP gives the array a specific semantics. It says “for each integer *N* in the array there will be additional fields defined in EIP-*N*, which is expected to specify how to retrieve their values”.

Note that, from the outset, users of EIP-5267 know what to do with the `extensions` array, even if only to recognize that there is some unimplemented behavior that should result in an error.



      [github.com/frangio/eip712domains](https://github.com/frangio/eip712domains/blob/7413ee18bbdcbb893154e100b550827a0319b3ca/app/src/lib/eip-5267.ts#L36-L38)





####

  [7413ee18b](https://github.com/frangio/eip712domains/blob/7413ee18bbdcbb893154e100b550827a0319b3ca/app/src/lib/eip-5267.ts#L36-L38)



```ts


1. if (extensions.length > 0) {
2. throw Error("extensions not implemented");
3. }


```










Similarly, implementors of EIP-5267 know exactly what it means to include a number in the `extensions` array.

The problem that I see in all of the examples you provide is that there are no semantics given to these `bytes extraData` arguments. For example, in EIP-6066, what should a contract do if it receives non-empty extraData? How does a user know that the contract is interpreting the extraData correctly?

Standards are about coordination, and as far as I can tell adding `bytes extraData` is not helping coordinate, and may even be leading to coordination problems if different users/implementors don’t agree on how to use it.

---

**xinbenlv** (2023-01-10):

Thank you for your continued effort in discussing with me, [@frangio](/u/frangio). Considering you are the main author of OZ, your opinion carry a lot of weight in my heart both because of my respect to your work in creating the wonderful OZ but also the experience and expertise you earn and demonstrate in that creation.

But I do respectfully share quite different views with you on a few things you write up there.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> I think you misinterpreted this. EIP-712 is already extensible. It says:
>
>
>
> Future extensions to this standard can add new fields with new user-agent behaviour constraints.

The `uint[] extensions` in EIP-5267 is just a manifestation of this existing bit of the spec.

…

I think I didn’t misinterpret this. EIP-712 already is (or claim to be) extensible. I think you misinterpret EIP-5750.

When EIP-712 says it’s extensible, people wasn’t sure how it can be extended. For example “can add new fields”, there are unanswered question open for interpretation: Add such new field *at where*, *in for format*?  This is exactly why EIP-5267 tries to specify. In EIP-5267 you answered: (1) it should be “uint256” and (2) it should be added to the last of the param list, and (3) it should refer to EIP-number.  Those are actually *design choices you made in EIP-5267*.

Now, combing back to EIP-5750, it’s trying to solve the unanswered problem *like this*, and *at certain level of clarity and flexiblity* once-for-all: it says it there should be (1) last param, (2) bytes, and amongst other implied decision, (3) it didn’t require it to be EIP number or anything, leaving it to be open for interpretation. And I do ask you the same question on EIP-5267 whether it has to be EIP-number, or whether you are open it to be other format.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> I think this serves to exemplify why I think this EIP’s approach to extensibility doesn’t work. EIP-712 and EIP-5267 are extensible through the extensions array, but the difference is that the EIP gives the array a specific semantics. It says “for each integer N in the array there will be additional fields defined in EIP-N, which is expected to specify how to retrieve their values”.

I could understand if you want something more restrictive being specified in EIP-5750, but *that’s a choice*. Just like EIP-712 says “you can add fields” and then open up for flexibility for future EIP / impl to decide how to add fields and what those fields means, EIP-5750 *also* make some choices and intentionally leave some choices for flexibility.

Now one could be as much restrictive as they want, but they also needs to be questioned: why so restrictive?

IMHO this is the main difference of mindset between “standard designing” vs “implementation designing”:

- Implementation designing mindset prioritize restrictiveness over flexibility
- standard designing mindset prioritize flexibility over restrictiveness.

I was using EIP-5267 as one of the example to speak the same language with you as you are author of that EIP and it may come to be more obvious such decision were (probably) unmade in EIP-712 and you needs to make it in EIP-5267, hoping you could easily wear the same hat such need will occur in other EIPs and thus see the value of EIP-5750 that makes *some design choices* for all functions.

But if you don’t think using EIP-5267 helps me explain my position and motivation of EIP-5750, that’s fine too, here are other examples…

---

Let’s use some other examples: EIP-5732 Commit Interface using *any function* with a EIP-5750 compatible field for supplying secret salt, or EIP-5453 Endorsement Interface to allow any function to be endorsible if they comply with EIP-5750. I think they provide a much better angle of why EIP-5750 provides a overall value for the whole ERC/application layer.

Please note, some of the choice in EIP-5750 were *intentionally flexible* so it can be maximally useful.

---

Footnote: Just like *any ERCs*, any dApp/Smart Contract/user-client builders could ignore any ERCs, people could feel absolutely free to ignore EIP-5750. But at the end of the day, design question like “how to extend EIP-712, exactly?” comes up every once a while, and hopefully EIP-5750 provides some inspiration, and drive some consensus, of how to answer such design choice for ERC community as a whole

---

**frangio** (2023-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> design question like “how to extend EIP-712, exactly?” comes up every once a while, and hopefully EIP-5750 provides some inspiration, and drive some consensus, of how to answer such design choice for ERC community as a whole

I can agree with this. But I think the extensibility mechanism proposed in this EIP is not helpful and may lead to bad results.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> standard designing mindset prioritize flexibility over restrictiveness.

Standards should be somewhat flexible, but also need to be unambiguously specified. If there is a “bytes” value as a function argument with no meaning given by the standard at all, no one can possibly know how to use this value: users can’t assume what values an implementation would accept or expect, and implementors can’t assume that users would pass in the expected values. There needs to be a way to coordinate users and implementors in the meaning of the bytes value. Generally the standards spec is the coordination mechanism, but when there is an extensibility mechanism there is a need to define a separate coordination mechanism about the extensions being used.

---

**xinbenlv** (2023-01-10):

> no one can possibly know how to use this value

That’s true for “what data will the last param be”, and leaving to EIPs like EIP-5732 and EIP-5453 to specify.

One of things that “one does know” in EIP-5750 is that a compliant function shall add *one last param*. Which also mean any callers shall take into the account for an existence of such last param.

This is entirely what this EIP is about.

---

And I am unsure if you are

- (1) questioning if there is even any value to specify the existence, location or datatype of a param, or
- (2) questioning if there is value when only such existence, location and datatype last param is specified but content of datatype is unspecified.

My take is that

- There is value in specifying the existence, location or datatype of a param.
- As author of EIP-5750 I intentionally made a design choice to leave content unspecified to leave ways for EIP-5732, EIP-5453 and other future EIP authors.

---

**frangio** (2023-01-10):

I think there can be value in documenting a design pattern for extensibility.

I do think the contents of this extensible argument are very important. In EIP-5267, you may disagree with the choice to use EIP numbers (and you make some good points about that!), but the content of the argument and its interpretation are unambiguously defined.

Taking [EIP-6066](https://github.com/ethereum/EIPs/pull/6066/files) as an example, there is a `data` argument that has no meaning whatsoever given to it. Each particular EIP-6066 implementer might give it a specific interpretation, but the EIP makes no provisions for communicating what that is.

In the Governor contracts in OpenZeppelin there is a similar situation that we tried to address. The `castVote` functions have two arguments that are generic and extensible: `uint8 support`, and also `bytes params`. “Support” is the value that encodes For/Against/Abstain, but it could also encode completely different values in other Governor instances with custom behavior. It’s very important to communicate to a user (or application) how to use that argument. The way we do that is with the [COUNTING_MODE()](https://docs.openzeppelin.com/contracts/4.x/api/governance#IGovernor-COUNTING_MODE--) getter, which returns a string that describes how `support` and `params` should be used.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e52ac578ea83cf197de800e7b0b45ca756d6883d_2_587x500.png)image740×630 86.8 KB](https://ethereum-magicians.org/uploads/default/e52ac578ea83cf197de800e7b0b45ca756d6883d)

Hope this example helps understand where I think this pattern is lacking.

---

**xinbenlv** (2023-01-11):

> you make some good points about that!

Thanks for recognizing, [@frangio](/u/frangio) !

> but the content of the argument and its interpretation are unambiguously defined.

Yeah, that was intentional, as I reiterated above.

> Taking EIP-6066 as an example, there is a data argument that has no meaning whatsoever given to it.

Yes, as an EIP that adopts EIP-5750, the EIP-6066 has that data argument, which is just as the same as the EIP-721

```auto
    /// @notice Transfers the ownership of an NFT from one address to another address
    /// ...
    /// @param data Additional data with no specified format, sent in call to `_to`
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data) external payable;
```

In which it reads `data: Additional data with no specified format`

---

I do understand that you disagree the technical design decision that such `data` being unspecified. But we increasingly see such pattern being adopted, so that was the rationale of EIP-5750 choose to be content agnostic but only to advocate for the same pattern.

Such pattern is adopted by not only EIP-721, but also EIP-1155 and many more, such as

- ERC-3668: CCIP Read: Secure offchain data retrieval
- ERC-3234: Batch Flash Loans
- ERC-4341: Ordered NFT Batch Standard

Just to name a few.

Not to mention those other EIPs who have a last param and already assign a meaning.

In fact, if you would entertain an idea that there will be a use-case for `minorEIPIdentifier` in [ERC-5269: ERC Detection and Discovery](https://eips.ethereum.org/EIPS/eip-5269), I’d suggest the [ERC-5267: Retrieval of EIP-712 domain](https://eips.ethereum.org/EIPS/eip-5267) to consider a minor EIP/behavior identifier to provide flexibility for granularity of future use case not just at the whole-EIP level.

