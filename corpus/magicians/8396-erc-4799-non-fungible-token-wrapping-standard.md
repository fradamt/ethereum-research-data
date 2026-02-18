---
source: magicians
topic_id: 8396
title: "ERC-4799: Non-Fungible Token Wrapping Standard"
author: davidbuckman
date: "2022-02-23"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-4799-non-fungible-token-wrapping-standard/8396
views: 2453
likes: 2
posts_count: 4
---

# ERC-4799: Non-Fungible Token Wrapping Standard

for discussion re: https://github.com/ethereum/EIPs/pull/4800

```auto
interface IERCX is IERC165, IERCXNFT {
    /// @dev This event emits when an NFT is wrapped by this contract.
    /// It also emits when the wrapping NFT that represents a particular
    /// wrapped NFT changes.
    event Wrap(
        address indexed wrappedContract,
        uint256 indexed wrappedTokenId,
        uint256 indexed tokenId
    );
    /// @notice Find the tokenId of a wrapped NFT's wrapping NFT
    /// @param wrappedContract The contract address of a wrapped NFT
    /// @param wrappedTokenId The tokenId of a wrapped NFT
    /// @return The tokenId of the wrapping NFT
    function tokenIdOf(IERCXNFT wrappedContract, uint256 wrappedTokenId)
        external
        view
        returns (uint256);
}
```

## Replies

**SamWilsn** (2022-02-28):

Couple of less EIP-process related comments:

- Since EIP-1155 is slowly gaining momentum, how does this standard interact with it? Would it be worthwhile to explicitly support it?
- Should there be a standardized unwrap function?
- What happens if the two contracts get out of sync (ex. the wrapped contract has an alternate way of transferring ownership)?
- Is the @dev comment about ownerOf throwing if owner == address(0) mandatory? If not, it should be removed.

---

**davidbuckman** (2022-03-01):

Hi - great questions, we actually have had discussions internally about all of these points!

> Since EIP-1155 is slowly gaining momentum, how does this standard interact with it? Would it be worthwhile to explicitly support it?

This standard is not compatible with EIP-1155, and we don’t think it would be worth supporting. We created the IERCXNFT interface to codify a pure definition of the abstract idea of an “NFT”: a mapping from `tokenId` to exactly one `owner`. EIP-1155 does not adhere to this interface - NFTs are NFTs in EIP-1155 only if the contract refuses to allow more than one to exist. It is not discernable from the interface, and a client querying a standard EIP-1155 has no way to tell if a token is fungible or not. You could imagine an implementation that adheres to EIP-1155 and also implements IERCXNFT, by keeping track of which `tokenIds` are NFTs in the contract state, which would then be compatible with this standard.

> Should there be a standardized unwrap function?
> What happens if the two contracts get out of sync (ex. the wrapped contract has an alternate way of transferring ownership)?

These two questions have similar answers, the crux of which is the fact that the authenticity of a wrapping NFT is conferred by the wrapped NFT’s original contract listing the ERCX contract its owner.

A standardized `unwrap` function declaration would not be very meaningful, because the power to unwrap an NFT lies with the original contract, not with the wrapping contract. In our reference implementation for an ERC-721 wrapper, you can see that we don’t even include an `unwrap` function - rather, we `approve` the original owner, and they can unwrap the NFT at their leisure by transferring it away from the ERCX contract that is wrapping it.

And this is always the case - regardless of any unwrapping function that may or may not be called on the ERCX, a token is unwrapped when chain of ownership from the original contract is broken, whether the wrapping contract likes it or not. So the idea of contracts getting “out of sync” is not one we have to worry about. The original contract decides if your wrapping NFT is authentic - the wrapping contract not knowing about or disagreeing with this is of no consequence, as any client looking for the owner will follow the chain of ownership and wind up wherever the original contract points. The owner of the NFT from the “out of sync” wrapping contract owns an NFT that represents nothing, and clients will recognize that as such.

> Is the @dev comment about ownerOf throwing if owner == address(0) mandatory? If not, it should be removed.

This was taken directly from [EIP-721](https://eips.ethereum.org/EIPS/eip-721). We don’t really have a strong opinion on whether or not it should stay as a property of the core definition of an NFT. My understanding of this requirement is that it makes implementation easier, since uninitialized memory is 0 by default, and this way the contract is not required to manually keep track of which NFTs “exist” yet and which are “burned” - if this understanding is correct, I would weakly be in favor of removing it from this standard, since that doesn’t seem particularly principled and would prefer to leave that decision up to a contract’s discretion. Seems to me like a contract should be permitted to use the zero address as a destination for “no one has access to this currently” even as the NFT continues to exist and may be returned to a usable wallet at some point. If my understanding is not correct, I would love to learn the real justification for why this was put in the ERC-721 specification!

---

**leeren** (2022-08-16):

Three questions:

1. Is the intention always for wrappers contracts to implement the IERC4799 interface?
2. What would the standard be for figuring out the designated owner from the NFT itself? Getting its contract owner, checking if it implements the IERC4799 interface, and then querying tokenIdOf and otherwise falling back to the standard ownerOf?
3. Have you checked out EIP-4987? The designs are somewhat similar in terms of trying to solve the problem of delegated ownership attribution through the owner contracts themselves. Curious if you see this as sharing the same goal.

