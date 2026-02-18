---
source: magicians
topic_id: 12043
title: "EIP-6093: Custom errors for commonly-used tokens"
author: ernestognw
date: "2022-12-06"
category: EIPs
tags: [token, errors]
url: https://ethereum-magicians.org/t/eip-6093-custom-errors-for-commonly-used-tokens/12043
views: 4906
likes: 18
posts_count: 21
---

# EIP-6093: Custom errors for commonly-used tokens

Hello community,

Since the introduction [custom errors](https://blog.soliditylang.org/2021/04/21/custom-errors/) in Solidity in v0.8.4, there’s now a more expressive and gas-efficient way of reverting changes during a transaction.

Given this new addition, we’re proposing a list of standard errors to be used for the standard tokens (ERC20, ERC721, and ERC1155), so the clients and implementers can expect an insightful and structured way from a transaction error.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6093)





###



Lists custom errors for common token implementations

## Replies

**dcota** (2022-12-26):

This is a very good initiative. For the curious out here, it will be interesting to have a reference of the bytecode savings for switching from old revert strings (for example in ERC20) to error messages.

In the Rationale section for *domain*; perhaps the contract name itself could be suggested to help with the compiler *DeclarationError* in situations where the *ErrorPrefix* and *Subject* are the same.

---

**ernestognw** (2022-12-27):

> This is a very good initiative. For the curious out here, it will be interesting to have a reference of the bytecode savings for switching from old revert strings (for example in ERC20) to error messages.

Thanks for your comments! Actually, I just made a quick repo test for comparing the gas savings.

You can find them [here](https://github.com/ernestognw/EIP-6093-benchmarks/tree/main/reports).

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b3a347cd09dcd24f81107f4131a6a228d3bc1a94_2_672x500.jpeg)image1680×1250 257 KB](https://ethereum-magicians.org/uploads/default/b3a347cd09dcd24f81107f4131a6a228d3bc1a94)

*Look at the differences between custom errors and short strings vs long strings, which are the majority of the cases*

TLDR is that EIP-6093’s custom errors are better in gas usage than general revert strings unless for reverts with empty strings.

> In the Rationale section for domain ; perhaps the contract name itself could be suggested to help with the compiler DeclarationError in situations where the ErrorPrefix and Subject are the same.

I see what you mean. Although it can solve the DeclarationError, it’ll also change the error selector depending on the contract name, and that might affect standardization overall (eg. Metamask would need to know the contract name just to calculate the selector and show a proper error message in the UI).

What do you think?

---

**dcota** (2023-02-03):

Very nice report on the gas savings.

In my opinion, the change to custom errors should become the norm on new deployments of these common token implementations.

Assuming this makes its way to an OpenZeppelin implementation, would this change be implemented directly in the existing token contracts, for instance: [ERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol), or would it be within the ./extensions folder?

---

**ernestognw** (2023-02-03):

We aim to implement these changes in OpenZeppelin Contracts for the next 5.0 version, so yes, it’s expected to make into OZ’s ERC20 implementation.

Also, the same rationale is going to be used for other errors, [see this discussion](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/2839).

---

**PaulRBerg** (2023-02-05):

I am wholeheartedly in favor of this, this is an awesome proposal. After reading the entire EIP, this is my feedback:

## Must or Must Not?

I am a bit confused by this statement in the “Specification” section:

> This EIP defines standard errors that may be used by implementations in certain scenarios, but does not specify whether implementations should revert in those scenarios

But then you go on and say something like this underneath each error:

> MUST be used when …

I might be getting the wrong end of the stick when it comes to what “MUST” means in this context, but don’t the statements above contradict one another?

## Prefix Underscores

Happy to see my [proposal](https://twitter.com/PaulRBerg/status/1510584043028500492) to use the name of the contract (in this case, the EIP number) as a custom error prefix. However, I like it better when the prefix is separated by an underscore, so that the contract name gets separated from the rest of the custom error name. Underscores in Solidity have become popular with the advent of Foundry (see the references to test naming [here](https://book.getfoundry.sh/tutorials/best-practices))

Here’s an example for what I mean:

```solidity
error ERC20_InsufficientBalance(address sender, uint256 balance, uint256 needed);
error ERC20_InvalidSender(address sender);
error ERC20_InvalidReceiver(address receiver);
error ERC20_InsufficientAllowance(address spender, uint256 allowance, uint256 needed);
error ERC20_InvalidApprover(address approver);
error ERC20_InvalidSpender(address spender);
```

## Zero Address

I wonder if it isn’t a bit too restrictive to demand that implementors MUST revert when the subject is the zero address (e.g. `ERC721InvalidSender`)? I personally never had a need for allowing transfers to and from the zero address, but I also can’t think of any good reason why this should be prevented at the EIP level (besides maybe preventing fat-finger errors?).

## Closing

Besides the points above and a few minor wording suggestions I left in this [PR](https://github.com/ethereum/EIPs/pull/6444), the EIP looks great to me. I can’t wait for OpenZeppelin v5 to be out.

---

**ernestognw** (2023-02-05):

Thanks for your feedback [@PaulRBerg](/u/paulrberg), I’m glad the proposal makes sense to you.

Let me answer your comments:

> but don’t the statements above contradict one another?

In a sense, yes. We discussed this internally and realized there’s no way of making every previous token implementation use these errors always (backwards compatibility), so we can’t say **MUST** since it’s not even possible.

Still, we put **MUST** to highlight the absolute requirement of using one of the standard errors when its characteristics are those of an EIP-6093 error.

What do you think would be the most accurate approach?

> Underscores in Solidity have become popular with the advent of Foundry (see the references to test naming here)

I think the test reference is becoming popular when it comes to testing, I haven’t seen many verified contracts adopting the mix between PascalCase and snake_case (I’ve seen double `__`, tho).

I searched for a reference, and the Solidity docs guide doesn’t include such a case.

https://docs.soliditylang.org/en/v0.8.17/style-guide.html#naming-styles

It also adds reasons to turn off [Solhint](https://protofire.github.io/solhint/docs/rules/naming/func-name-mixedcase.html), which may be dangerous for newbies.

> I wonder if it isn’t a bit too restrictive to demand that implementors MUST revert when the subject is the zero address

This is also related to the ambiguity in the Must vs Must not category. The idea is that errors MAY be added, but when they’re added, they MUST be used for the described cases.

In any case, EIP-712 and EIP-1155 explicitly state zero address reverts, so the idea is to cover those cases in which the original EIP requires them to revert.

We also thought about a `ZeroAddress()` standard error but we think it loses important context information. For example, does `ZeroAddress` means canceling an action?, is the `ZeroAddress` coming from a bad implemented `ecrecover`? etc.

How do you see the zero address case addressed?

> Besides the points above and a few minor wording suggestions I left in this PR

Thanks! I just approved ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**PaulRBerg** (2023-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> What do you think would be the most accurate approach?

Get rid of that statement? It’s super ambiguous. I think that it is an implicit assumption that EIP-6093-compatible token implementations will NOT be backward compatible with older implementations.

Rewrite the language to say something like this:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> It also adds reasons to turn off Solhint, which may be dangerous for newbies.

Fair enough!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> EIP-712 and EIP-1155 explicitly state zero address reverts

Oh, I didn’t know this. Makes sense to also apply this rule to EIP-20, too, then.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> We also thought about a ZeroAddress() standard error but we think it loses important context information.

I agree.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> How do you see the zero address case addressed?

I was just thinking out load. Given your answers, I’m happy to keep it as is.

---

Thanks for your answers and for merging the PR!

---

**rube-de** (2023-04-28):

Any reason this isn’t moved forward?

---

**ernestognw** (2023-05-10):

It’s going to be included in OpenZeppelin Contracts 5.0 next summer’s release, but we want to hear you out if there’s any feedback. Aside from that, the EIP reviewers will eventually peer-review it, but it takes some time.

---

**mattiascaricato** (2023-06-04):

It would be nice also to have custom errors for the commonly-used ERC-2612 “permit” function. The goal is to enhance the error handling and user experience when utilizing the permit function for approving token transfers. ERC-2612, also known as the “permit” function, has gained widespread adoption in Ethereum because of its gas efficiency. Additionally, the OpenZeppelin library provides an ERC20permit extension, to ensure consistency and compatibility across projects, it is essential to define a set of custom errors for the permit functionality. Having custom errors aligned with the standard would greatly benefit developers.

Specification: The proposed custom errors for ERC-2612 are as follows:

1. ERC2612ExpiredDeadline(uint256 deadline, uint256 blockTimestamp):

- Description: Indicates that the provided deadline for the permit has already expired.
- Arguments:

Deadline (what/who): The expiration timestamp specified in the permit.
- Block Timestamp (why): The current block timestamp at the time of verification.

Usage: Must be used when the current block timestamp exceeds the provided deadline.

1. ERC2612InvalidSignature(address owner, address signer):

- Description: Indicates that the signature used for the permit is invalid or does not match the expected signer.
- Arguments:

Owner (what/who): The address of the token owner who initiated the permit.
- Spender (why): The address that should have signed the permit.

Usage: Must be used when the signature verification fails or when the signer address does not match the expected value.

Implementation

```auto
interface ERC2612Errors {
    error ERC2612ExpiredDeadline(uint256 deadline, uint256 blockTimestamp);
    error ERC2612InvalidSignature(address owner, address spender);
}
```

---

**ernestognw** (2023-06-06):

Hey [@mattiascaricato](/u/mattiascaricato), thanks for your feedback!

These are already two considered errors we have on the current custom errors [Pull Request for OpenZeppelin Contracts](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/4261), you’ll see we have:

```plaintext
    /**
     * @dev Permit deadline has expired.
     */
    error ERC2612ExpiredDeadline(uint256 deadline);

    /**
     * @dev Mismatched signature.
     */
    error ERC2612InvalidSignature(address signer, address owner);
```

However, I think we might not want to decide on extensions to the base token implementations since we’re still agreeing on what would be the best way to create a common errors library in which these two errors may fit.

In any case, the criteria we’re using for naming tokens is that if an error is directly derived from an ERC specification, it should be prefixed by `ERC<number>`.

Curious to know, what’s your criteria for including `block.timestamp` as part of the arguments. I think it’ll be implicit in the block, do you see a strong reason to keep it?

---

**ernestognw** (2023-06-17):

The EIP was recently [moved to last-call](https://github.com/ethereum/EIPs/pull/7157) and it’s also implemented in [OpenZeppelin Contracts](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/4261) for the next release around late summer.

The following changes were added to the EIP:

- Renamed the ERC721InvalidOwner(address,uint256,address) to ERC721IncorrectOwner(address,uint256,addres) under the rationale that the error is more about the lack of ownership rather than the validity of the owner.
- Added ERC721InvalidOwner(address owner) according to the ERC721 standard where it’s specified the address 0 is not a valid owner.
- Added ERC721NonExistentToken since ERC721 reverts for queries to not yet minted token ids.
- Renamed ERC1155InufficientApproval(address,uint256) to ERC1155InsufficientApprovalForAll(address,address) because there’s no such thing as an approval by tokenId and amount in ERC1155, just approval for all

---

**vittominacori** (2023-07-17):

Should we not have more detailed error handling?

I mean in OZ implementation by using `ERC721InvalidReceiver` both inside and outside the `_checkOnERC721Received` method, we cannot understand if the call failed because the receiver is not a `IERC721Receiver` implementer or if it returns a wrong value other than the desired selector.

---

**ernestognw** (2023-07-17):

Hey [@vittominacori](/u/vittominacori)

> Should we not have more detailed error handling?

What would you say would provide more details?

We even considered a `library` of common errors, examples like `error ZeroAddress` or `error InsufficientBalance` were candidates but we decided to avoid them in favor of more informative errors (different arguments).

In regards to ERC271InvalidReceiver, this is important feedback because the 5.0 version of the [ERC721 is still in review](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/4377/files#diff-e2836bd953dd43371de037aa4eef3b8dd1981b3833b4def3f228e88668e377d0R448) and we’re merging those two errors you pointed out, which makes me think we’re removing contextual information.

The challenge has been to not overload the standard with errors for every specific use case while still keeping reasonable feedback for both the users and developers. In the case of `ERC721InvalidReceiver` I’d say the actionable is to take a look at the receiver, regardless of why the operation couldn’t be completed, would you name that error differently?

---

**vittominacori** (2023-07-17):

Yes, my doubt is about giving the same error both for an invalid receiver or for a valid receiver returning a wrong value.

I wanted to follow your proposal and I’ve started working on custom errors for [ERC1363](https://github.com/vittominacori/erc1363-payable-token/pull/7/files#diff-18589e888e101b1aacbc93892ae010139abeb240bc3da9a7341d97c38dd345ca). I’m concerning about how to name errors and if I should create an error for each case I had before when using the old `require(condition, string)`.

For instance I’m creating the `ERC1363EOAReceiver` error in `transferAndCall` when the receiver is an EOA address. Should not I care about this detail and return the more generic `ERC1363InvalidReceiver` error? The same with the invalid selector returned.

Giving a string with detailed message was quite simple than add additional code for each error.

---

**ernestognw** (2023-07-18):

Hey, that’s very nice! Thanks [@vittominacori](/u/vittominacori)

We had this conversation for the OZ library implementation because adding custom errors come (imo) with the following pros/cons overall:

Pros

- The gas savings for bytecode size reduction are significant, some of our first metrics show good improvements
- There’s potential for UI benefits from decoding arguments and standardizing error interfaces

Neutral

- Runtime savings are saved mostly in the error path, which is useful if errors happen on chain, which is usually not the case

Bad

- It reduces the specificity of the error

So far my opinion is that reducing the specificity is somewhat the direction where standardization goes. This is why UIs can benefit from it and there are also some Solidity recommendations for [doing this](https://dev.to/george_k/embracing-custom-errors-in-solidity-55p8) (Note I wouldn’t recommend yet because relying on upgradeable contract error interfaces could be dangerous).

Given these reasons, I’d say we value standardization because of the nature of our library. However, the EIP suggests enough flexibility tolerance in the Backwards Compatibility section, and in consumer products, it may be useful to have very different error reasons depending on your business logic.

My personal advice would be to check out if there are important benefits for UIs or significant Smart Contract dependencies before deciding whether to use more specific errors or not.

EDIT: By the way, there are some issues in the solidity repo ([1](https://github.com/ethereum/solidity/issues/13662), [2](https://github.com/ethereum/solidity/issues/14287)) that may improve custom error extensibility so we may want to provide some input

---

**GalaxySciTech** (2023-09-22):

i have a question is that we can not seen the specifics error log  in etherscan if  you use revert error

it will make someone confuse

how to solve this case

---

**ernestognw** (2023-09-26):

An important aspect of this ERC is standardizing these error selectors so that indexers like Etherscan can properly show the values if needed.

Errors don’t usually make it to mainnet (nor Etherscan) because are frequently caught by wallets while estimating the gas for a transaction. In any case, both a wallet or Etherscan will get the error selector.

---

**bogdan** (2025-04-10):

One error that might not be covered by this standard, but is absolutelly necessary for every ERC721 implementation is: `ERC721TokenAlreadyMinted`. What do you think about adding to the standard?

---

**ernestognw** (2025-06-04):

Hi [@bogdan](/u/bogdan), thanks for the feedback. The thing is that “minting” is not formally defined in ERC-721’s spec. The only formal mention of it is the following:

```auto
/// @dev This emits when ownership of any NFT changes by any mechanism.
///  This event emits when NFTs are created (`from` == 0) and destroyed
///  (`to` == 0). Exception: during contract creation, any number of NFTs
///  may be created and assigned without emitting Transfer. At the time of
///  any transfer, the approved address for that NFT (if any) is reset to none.
event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
```

Theoretically, the benefit of this standard is to show better information in wallet UIs by interpreting revert reasons. In practice, this didn’t happen as expected, which is understandable since many popular tokens didn’t follow this standard and aren’t upgradeable.

For those cases, I think identifying an “already minted” error can be done by checking for the `ERC721InvalidSender(...)` error with `address(0)` as the argument. The rationale is that when attempting to mint an already-existing token, the operation typically tries to transfer from `address(0)` (which represents minting), but since the token already has a valid owner, `address(0)` becomes an invalid sender.

As an example, [OpenZeppelin Contracts does this](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/aaf955de5664a23e6180c1887bf363ab24f2054e/contracts/token/ERC721/ERC721.sol#L265).

btw we should finalize this standard soon

