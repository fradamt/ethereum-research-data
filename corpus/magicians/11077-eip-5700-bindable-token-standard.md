---
source: magicians
topic_id: 11077
title: "EIP-5700: Bindable Token Standard"
author: leeren
date: "2022-09-27"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5700-bindable-token-standard/11077
views: 2752
likes: 1
posts_count: 6
---

# EIP-5700: Bindable Token Standard

## EIP-5700: Bindable Token Standard

This standard enables tokens to be bound to unique assets. Bound tokens have their ownership and tracking delegated through the assets they are bound to, and may be unbound at any time.

> This thread serves as a concise overview. The full EIP may be found here (currently a PR).

---

## Abstract

The proposed standard defines an interface by which fungible and non-fungible tokens may be bound to arbitrary assets, enabling token ownership and transfer attribution to be proxied through the assets they are bound to.

A bindable token (“bindable”) is an EIP-721 or EIP-1155 token which, when bound, delegates ownership and tracking through its bound asset, remaining locked for direct transfers until it is unbound.

A bound asset (“binder”) has few restrictions on how it is represented, except that it be unique and expose an interface for ownership queries. Binders and bindables form a one-to-many relationship.

Example use-cases:

- NFT-bundled physical assets: microchipped streetwear bundles, digitally-twinned real-estate property
- NFT-bundled digital assets: accessorizable virtual wardrobes, customizable metaverse land

## Motivation

Unlike other standards tackling delegated ownership attribution, which look at composability on the account level, this standard addresses composability on the asset level, with the goal of creating a universal interface for token modularity compatible with existing EIP-721 and EIP-1155 standards.

## Specification

### ERC-721 Bindable

```auto
interface IERC721Bindable /* is IERC721 */ {

    /// @notice Emits when NFT ownership is delegated through an asset.
    /// @dev When minting bound NFTs, `from` MUST be set to the zero address.
    /// @param operator The address calling the bind.
    /// @param from The unbound NFT owner address.
    /// @param to The bound NFT delegate owner address.
    /// @param tokenId The identifier of the NFT being bound.
    /// @param bindId The identifier of the asset being bound to.
    /// @param bindAddress The contract address handling asset ownership.
    event Bind(
        address indexed operator,
        address indexed from,
        address to,
        uint256 tokenId,
        uint256 bindId,
        address indexed bindAddress
      );

    /// @notice Emits when asset-bound NFT ownership delegation is revoked.
    /// @dev When burning bound NFTs, `to` MUST be set to the zero address.
    /// @param operator The address calling the unbind.
    /// @param from The bound asset owner address.
    /// @param to The unbound NFT owner address.
    /// @param tokenId The identifier of the NFT being unbound.
    /// @param bindId The identifier of the asset being unbound from.
    /// @param bindAddress The contract address handling bound asset ownership.
    event Unbind(
        address indexed operator,
        address indexed from,
        address to,
        uint256 tokenId,
        uint256 bindId,
        address indexed bindAddress
    );

    /// @notice Binds NFT `tokenId` owned by `from` to asset `bindId` at
    ///  `bindAddress`, delegating asset-bound ownership to address `to`.
    /// @dev The function MUST throw unless `msg.sender` is the current owner,
    ///  an authorized operator, or the approved address for the NFT. It also
    ///  MUST throw if the NFT is already bound, if `from` is not the NFT owner,
    ///  or if `to` is not `bindAddress` or its asset owner. After binding, the
    ///  function MUST check if `bindAddress` is a valid contract
    ///  (code size > 0), and if so, call `onERC721Bind` on it, throwing if the
    ///  wrong identifier is returned (see "Binding Rules") or if the contract
    ///  is invalid. On bind completion, the function MUST emit `Bind` and
    ///  `Transfer` events to reflect asset-bound ownership delegation.
    /// @param from The unbound NFT owner address.
    /// @param to The bound NFT delegate owner address (SHOULD be `bindAddress`).
    /// @param tokenId The identifier of the NFT being bound.
    /// @param bindId The identifier of the asset being bound to.
    /// @param bindAddress The contract address handling asset ownership.
    /// @param data Additional data sent with the `onERC721Bind` hook.
    function bind(
        address from,
        address to,
        uint256 tokenId,
        uint256 amount,
        uint256 bindId,
        address bindAddress,
        bytes calldata data
    ) external;

    /// @notice Unbinds NFT `tokenId` from asset `bindId` owned by `from` at
    ///  address `bindAddress`, assigning ownership of the unbound NFT to `to`.
   /// @dev The function MUST throw unless `msg.sender` is an approved operator
    ///  or asset owner. It also MUST throw if NFT `tokenId` is not bound, if
    ///  `from` is not the asset owner, or if `to` is the zero address. After
    ///  unbinding, the function MUST check if `bindAddress` is a valid contract
    ///  (code size > 0), and if so, call `onERC721Unbind` on it, throwing if
    ///  the wrong identifier is returned (see "Binding Rules") or if the
    ///  contract is invalid. The function also MUST check if `to` is a valid
    ///  contract, and if so, call `onERC721Received`, throwing if the wrong
    ///  identifier is returned. On unbind completion, the function MUST emit
    ///  `Unbind` and `Transfer` events to reflect delegated ownership change.
    /// @param from The bound asset owner address.
    /// @param to The unbound NFT new owner address.
    /// @param tokenId The identifier of the NFT being unbound.
    /// @param bindId The identifier of the asset being unbound from.
    /// @param bindAddress The contract address handling bound asset ownership.
    /// @param data Additional data sent with the `onERC721Unbind` hook.
    function unbind(
        address from,
        address to,
        uint256 tokenId,
        uint256 bindId,
        address bindAddress,
        bytes calldata data
    ) external;

    /// @notice Gets the asset identifier and address an NFT is bound to.
    /// @param tokenId The identifier of the NFT being queried.
    /// @return The bound asset identifier and contract address.
    function binderOf(uint256 tokenId) external returns (uint256, address);

    /// @notice Counts NFTs bound to asset `bindId` at address `bindAddress`.
    /// @param bindAddress The contract address handling bound asset ownership.
    /// @param bindId The identifier of the bound asset.
    /// @return The total number of NFTs bound to the asset.
    function boundBalanceOf(address bindAddress, uint256 bindId) external returns (uint256);
}
```

```auto
interface IERC721Binder /* is IERC165 */ {

    /// @notice Handles the binding of an IERC721Bindable-compliant NFT.
    /// @dev An IERC721Bindable-compliant smart contract MUST call this function
    ///  at the end of a `bind` after ownership is delegated through an asset.
    ///  The function MUST revert if `to` is not the asset owner or the binder
    ///  address. The function MUST revert if it rejects the bind. If accepting
    ///  the bind, the function MUST return `bytes4(keccak256("onERC721Bind(address,address,address,uint256,uint256,bytes)"))`
    ///  Caller MUST revert the transaction if the above value is not returned.
    /// @param operator The address responsible for initiating the bind.
    /// @param from The unbound NFT original owner address.
    /// @param to The bound NFT delegate owner address.
    /// @param tokenId The identifier of the NFT being bound.
    /// @param bindId The identifier of the asset being bound to.
    /// @param data Additional data sent along with no specified format.
    /// @return `bytes4(keccak256("onERC721Bind(address,address,address,uint256,uint256,bytes)"))`
    function onERC721Bind(
			address operator,
			address from,
			address to,
			uint256 tokenId,
			uint256 bindId,
			bytes calldata data
	) external returns (bytes4);

    /// @notice Handles the unbinding of an IERC721Bindable-compliant NFT.
    /// @dev An IERC721Bindable-compliant smart contract MUST call this function
    ///  at the end of an `unbind` after revoking delegated asset ownership.
    ///  The function MUST revert if `from` is not the asset owner of `bindId`.
    ///  The function MUST revert if it rejects the unbind. If accepting the
    ///  unbind, the function MUST return `bytes4(keccak256("onERC721Unbind(address,address,address,uint256,uint256,bytes)"))`
    ///  Caller MUST revert the transaction if the above value is not returned.
    ///  Note: The contract address of the unbinding NFT is `msg.sender`.
    /// @param from The bound asset owner address.
    /// @param to The unbound NFT new owner address.
    /// @param tokenId The identifier of the NFT being unbound.
    /// @param bindId The identifier of the asset being unbound from.
    /// @param data Additional data with no specified format.
    /// @return `bytes4(keccak256("onERC721Unbind(address,address,address,uint256,uint256,bytes)"))`
    function onERC721Unbind(
			address operator,
			address from,
			address to,
			uint256 tokenId,
			uint256 bindId,
			bytes calldata data
	) external returns (bytes4);

    /// @notice Gets the owner address of the asset represented by id `bindId`.
    /// @dev This function MUST throw for assets assigned to the zero address.
    /// @param bindId The identifier of the asset whose owner is being queried.
    /// @return The address of the owner of the asset.
   function ownerOf(uint256 bindId) external view returns (address);

    /// @notice Checks if an operator can act on behalf of an asset owner.
    /// @param owner The address that owns an asset.
    /// @param operator The address that acts on behalf of owner `owner`.
    /// @return True if `operator` can act on behalf of `owner`, else False.
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}
```

### ERC-1155 Bindable

```auto
interface IERC1155Bindable /* is IERC1155 */ {

	/// @notice The `Bind` event MUST emit when token ownership is delegated
	///  through an asset and when minting tokens bound to an existing asset.
	/// @dev When minting bound tokens, `from` MUST be set to the zero address.
	/// @param operator The address calling the bind (SHOULD be `msg.sender`).
	/// @param from The unbound tokens' original owner address.
	/// @param to The bound tokens' delegate owner address (SHOULD be `bindAddress`).
	/// @param tokenId The identifier of the token type being bound.
	/// @param amount The number of tokens of type `tokenId` being bound.
	/// @param bindId The identifier of the asset being bound to.
	/// @param bindAddress The contract address handling asset ownership.
    event Bind(
        address indexed operator,
        address indexed from,
        address to,
        uint256 tokenId,
        uint256 amount,
        uint256 bindId,
        address indexed bindAddress
    );

	/// @notice The `BindBatch` event MUST emit when token ownership of
	///  different token types are delegated through different assets at once
	///  and when minting multiple token types bound to existing assets at once.
	/// @dev When minting bound tokens, `from` MUST be set to the zero address.
	/// @param operator The address calling the bind (SHOULD be `msg.sender`).
	/// @param from The unbound tokens' original owner address.
	/// @param to The bound tokens' delegate owner address (SHOULD be `bindAddress`).
	/// @param tokenIds The identifiers of the token types being bound.
	/// @param amounts The number of tokens for each token type being bound.
	/// @param bindIds The identifiers of the assets being bound to.
	/// @param bindAddress The contract address handling asset ownership.
    event BindBatch(
        address indexed operator,
        address indexed from,
        address to,
        uint256[] tokenIds,
        uint256[] amounts,
        uint256[] bindIds,
        address indexed bindAddress
    );

    /// @notice The `Unbind` event MUST emit when asset-delegated token
	///  ownership is revoked and when burning tokens bound to existing assets.
	/// @dev When burning bound tokens, `to` MUST be set to the zero address.
	/// @param operator The address calling the unbind (SHOULD be `msg.sender`).
	/// @param from The bound asset owner address.
	/// @param to The unbound tokens' new owner address.
	/// @param tokenId The identifier of the token type being unbound.
	/// @param amount The number of tokens of type `tokenId` being unbound.
	/// @param bindId The identifier of the asset being unbound from.
	/// @param bindAddress The contract address handling bound asset ownership.
    event Unbind(
        address indexed operator,
        address indexed from,
        address to,
        uint256 tokenId,
        uint256 amount,
        uint256 bindId,
        address indexed bindAddress
    );

    /// @notice The `UnbindBatch` event MUST emit when asset-delegated token
	///  ownership is revoked for multiple token types at once and when burning
	///  multiple token types bound to existing assets at once.
	/// @dev When burning bound tokens, `to` MUST be set to the zero address.
	/// @param operator The address calling the unbind (SHOULD be `msg.sender`).
	/// @param from The bound asset owner address.
	/// @param to The unbound tokens' new owner address.
	/// @param tokenIds The identifiers of the token types being unbound.
	/// @param amounts The number of tokens for each token type being unbound.
	/// @param bindIds The identifier of the assets being unbound from.
	/// @param bindAddress The contract address handling bound asset ownership.
    event UnbindBatch(
        address indexed operator,
        address indexed from,
        address to,
        uint256[] tokenIds,
        uint256[] amounts,
        uint256[] bindIds,
        address indexed bindAddress
    );

    /// @notice Binds `amount` tokens of type `tokenId` owned by `from` to asset
    ///  `bindId` at `bindAddress`, delegating token-bound ownership to `to`.
	/// @dev The function MUST throw unless `msg.sender` is an approved operator
    ///  for `from`. The function also MUST throw if `from` owns fewer than
    ///  `amount` tokens, or if `to` is not `bindAddress` or its asset owner.
    ///  After binding, the function MUST check if `bindAddress` is a valid
    ///  contract (code size > 0), and if so, call `onERC1155Bind` on it,
    ///  throwing if the wrong identifier is returned (see "Binding Rules") or
    ///  if the contract is invalid. On bind completion, the function MUST emit
    ///  `Bind` and `TransferSingle` events to reflect ownership binding.
	/// @param from The unbound tokens' original owner address.
	/// @param to The bound tokens' delegate owner address (SHOULD be `bindAddress`).
	/// @param tokenId The identifier of the token type being bound.
	/// @param amount The number of tokens of type `tokenId` being bound.
	/// @param bindId The identifier of the asset being bound to.
	/// @param bindAddress The contract address handling asset ownership.
    /// @param data Additional data sent with the `onERC1155Bind` hook.
    function bind(
        address from,
        address to,
        uint256 tokenId,
        uint256 amount,
        uint256 bindId,
        address bindAddress,
        bytes calldata data
    ) external;

    /// @notice Binds `amounts` tokens of types `tokenIds` owned by `from` to
    ///   assets `bindIds` at `bindAddress`, delegating bound ownership to `to`.
	/// @dev The function MUST throw unless `msg.sender` is an approved operator
	///  for `from`. The function also MUST throw if length of `amounts` is not
    ///  the same as `tokenIds` or `bindIds`, if any balances of `tokenIds` for
    ///  `from` is less than that of `amounts`, or if `to` is not `bindAddress`
    ///  or the asset owner. After delegating ownership, the function MUST check
    ///  if `bindAddress` is a valid contract (code size > 0), and if so, call
    ///  `onERC1155BatchBind` on it, throwing if the wrong identifier is
    ///  returned (see "Binding Rules") or if the contract is invalid. On bind
    ///  completion, the function MUST emit `BindBatch` and `TransferBatch`
    ///  events to reflect ownership binding.
	/// @param from The unbound tokens' original owner address.
	/// @param to The bound tokens' delegate owner address (SHOULD be `bindAddress`).
	/// @param tokenIds The identifiers of the token types being bound.
	/// @param amounts The number of tokens for each token type being bound.
	/// @param bindIds The identifiers of the assets being bound to.
	/// @param bindAddress The contract address handling asset ownership.
    /// @param data Additional data sent with the `onERC1155BatchBind` hook.
    function batchBind(
        address from,
        address to,
        uint256[] calldata tokenIds,
        uint256[] calldata amounts,
        uint256[] calldata bindIds,
        address bindAddress,
        bytes calldata data
    ) external;

    /// @notice Revokes delegated ownership of `amount` tokens of type `tokenId`
	///  owned by `from` bound to `bindId`, assigning ownership to `to`.
	/// @dev The function MUST throw unless `msg.sender` is an approved operator
    ///  or asset owner. It also MUST throw if `from` is not the asset owner, if
    ///  fewer than `amount` tokens are bound to the asset, or if `to` is the
    ///  zero address. Once delegated ownership is revoked, the function MUST
    ///  check if `bindAddress` is a valid contract (code size > 0), and if so,
    ///  call `onERC1155Unbind` on it, throwing if the wrong identifier is
    ///  returned (see "Binding Rules") or if the contract is invalid. The
    ///  function also MUST check if `to` is a contract, and if so, call on it
    ///  `onERC1155Received`, throwing if the wrong identifier is returned. On
    ///  unbind completion, the function MUST emit both `Unbind` and
    ///  `TransferSingle` events to reflect ownership unbinding.
	/// @param from The bound asset owner address.
	/// @param to The unbound tokens' new owner address.
	/// @param tokenId The identifier of the token type being unbound.
	/// @param amount The number of tokens of type `tokenId` being unbound.
	/// @param bindId The identifier of the asset being unbound from.
	/// @param bindAddress The contract address handling bound asset ownership.
    /// @param data Additional data sent with the `onERC1155Unbind` hook.
    function unbind(
        address from,
        address to,
        uint256 tokenId,
        uint256 amount,
		uint256 bindId,
		address bindAddress,
        bytes calldata data
    ) external;

    /// @notice Revokes delegated ownership of `amounts` tokens of `tokenIds`
	///  owned by `from` bound to assets `bindIds`, assigning ownership to `to`.
	/// @dev The function MUST throw unless `msg.sender` is an approved operator
    ///  or owner of all assets. It also MUST throw if the length of `amounts`
    ///  is not the same as `tokenIds` or `bindIds`, if `from` is not the owner
    ///  of all assets, if any balances of `tokenIds` for `from` is less than
    ///  that of `amounts`, or if `to` is the zero address. Once delegated
    ///  ownership is revoked, the function MUST check if `bindAddress` is a
    ///  valid contract (code size >  0), and if so, call onERC1155BatchUnbind`
    ///  on it, throwing if a wrong identifier is returned (see "Binding Rules")
    ///  or if the contract is invalid. The function also MUST check if `to` is
    ///  a valid contract, and if so, call `onERC1155BatchReceived on it`,
    ///  throwing if the wrong identifier is returned. On unbind completion, the
    ///  function MUST emit the `BatchUnbind` and `TransferBatch` events to
    ///  reflect ownership unbinding.
	/// @param from The bound asset owner address.
	/// @param to The unbound tokens' new owner address.
	/// @param tokenIds The identifiers of the token types being unbound.
	/// @param amounts The number of tokens for each token type being unbound.
	/// @param bindIds The identifier of the assets being unbound from.
	/// @param bindAddress The contract address handling bound asset ownership.
    /// @param data Additional data sent with the `onERC1155BatchUnbind` hook.
    function batchUnbind(
        address from,
        address to,
        uint256[] calldata tokenIds,
        uint256[] calldata amounts,
		uint256[] calldata bindIds,
		address bindAddress,
        bytes calldata data
    ) external;

    /// @notice Gets the balance of bound tokens of type `tokenId` bound to the
    ///  asset `bindId` at address `bindAddress`.
    /// @param bindAddress The contract address handling bound asset ownership.
    /// @param bindId The identifier of the bound asset.
	/// @param tokenId The identifier of the bound token type being counted.
    /// @return The total number of NFTs bound to the asset.
    function boundBalanceOf(
        address bindAddress,
        uint256 bindId,
        uint256 tokenId
    ) external returns (uint256);

    /// @notice Gets the balance of bound tokens for multiple token types given
    ///  by `tokenIds` bound to assets `bindIds` at address `bindAddress`.
    /// @notice Retrieves bound balances of multiple asset / token type pairs.
    /// @param bindAddress The contract address handling bound asset ownership.
    /// @param bindIds List of bound asset identifiers.
	/// @param tokenIds The identifiers of the token type being counted.
    /// @return balances The bound balances for each asset / token type pair.
    function boundBalanceOfBatch(
        address bindAddress,
        uint256[] calldata bindIds,
        uint256[] calldata tokenIds
    ) external returns (uint256[] memory balances);

}

```

```auto
interface IERC1155Binder /* is IERC165 */ {

	/// @notice Handles binding of an IERC1155Bindable-compliant token type.
	/// @dev An IERC1155Bindable-compliant smart contract MUST call this
	///  function at the end of a `bind` after delegating ownership to the asset
	///  owner. The function MUST revert if `to` is not the asset owner or
    ///  binder address. The function MUST revert if it rejects the bind. If
    ///  accepting the bind, the function MUST return `bytes4(keccak256("onERC1155Bind(address,address,address,uint256,uint256,uint256,bytes)"))`
	///  Caller MUST revert the transaction if the above value is not returned.
	///  Note: The contract address of the binding token is `msg.sender`.
	/// @param operator The address responsible for binding.
	/// @param from The unbound tokens' original owner address.
	/// @param to The bound tokens' delegate owner address (SHOULD be `bindAddress`).
	/// @param tokenId The identifier of the token type being bound.
	/// @param bindId The identifier of the asset being bound to.
    /// @param data Additional data sent along with no specified format.
	/// @return `bytes4(keccak256("onERC1155Bind(address,address,address,uint256,uint256,uint256,bytes)"))`
	function onERC1155Bind(
        address operator,
        address from,
        address to,
        uint256 tokenId,
        uint256 amount,
        uint256 bindId,
        bytes calldata data
	) external returns (bytes4);

	/// @notice Handles binding of multiple IERC1155Bindable-compliant tokens
    ///  `tokenIds` to multiple assets `bindIds`.
	/// @dev An IERC1155Bindable-compliant smart contract MUST call this
	///  function at the end of a `batchBind` after delegating ownership of
    ///  multiple token types to the asset owner. The function MUST revert if
    ///  `to` is not the asset owner or binder address. The function MUST revert
    ///  if it rejects the bind. If accepting the bind, the function MUST return
    ///  `bytes4(keccak256("onERC1155BatchBind(address,address,address,uint256[],uint256[],uint256[],bytes)"))`
	///  Caller MUST revert the transaction if the above value is not returned.
	///  Note: The contract address of the binding token is `msg.sender`.
	/// @param operator The address responsible for performing the binds.
	/// @param from The unbound tokens' original owner address.
	/// @param to The bound tokens' delegate owner address (SHOULD be `bindAddress`).
	/// @param tokenIds The list of token types being bound.
	/// @param amounts The number of tokens for each token type being bound.
	/// @param bindIds The identifiers of the assets being bound to.
    /// @param data Additional data sent along with no specified format.
	/// @return `bytes4(keccak256("onERC1155Bind(address,address,address,uint256[],uint256[],uint256[],bytes)"))`
	function onERC1155BatchBind(
        address operator,
        address from,
        address to,
        uint256[] calldata tokenIds,
        uint256[] calldata amounts,
        uint256[] calldata bindIds,
        bytes calldata data
	) external returns (bytes4);

	/// @notice Handles unbinding of an IERC1155Bindable-compliant token type.
	/// @dev An IERC1155Bindable-compliant contract MUST call this function at
	///  the end of an `unbind` after revoking delegated asset ownership. The
	///  function MUST revert if `from` is not the asset owner. The function
    ///  MUST revert if it rejects the unbind. If accepting the unbind, the
    ///  function MUST return `bytes4(keccak256("onERC1155Unbind(address,address,address,uint256,uint256,uint256,bytes)"))`
	///  Caller MUST revert the transaction if the above value is not returned.
	///  Note: The contract address of the unbinding token is `msg.sender`.
	/// @param operator The address responsible for performing the unbind.
	/// @param from The bound asset owner address.
	/// @param to The unbound tokens' new owner address.
	/// @param tokenId The token type being unbound.
	/// @param amount The number of tokens of type `tokenId` being unbound.
	/// @param bindId The identifier of the asset being unbound from.
    /// @param data Additional data sent along with no specified format.
	/// @return `bytes4(keccak256("onERC1155Unbind(address,address,address,uint256,uint256,uint256,bytes)"))`
	function onERC1155Unbind(
        address operator,
        address from,
        address to,
        uint256 tokenId,
        uint256 amount,
        uint256 bindId,
        bytes calldata data
	) external returns (bytes4);

	/// @notice Handles unbinding of multiple IERC1155Bindable-compliant token types.
	/// @dev An IERC1155Bindable-compliant contract MUST call this function at
	///  the end of an `batchUnbind` after revoking delegated asset ownership.
    ///  The function MUST revert if `from` is not the asset owner of `bindId`,
	///  or if `bindId` is not a valid asset. The function MUST revert if it
	///  rejects the unbinds. If accepting the unbinds, the function MUST return
	///  `bytes4(keccak256("onERC1155Unbind(address,address,address,uint256[],uint256[],uint256[],bytes)"))`
	///  Caller MUST revert the transaction if the above value is not returned.
	///  Note: The contract address of the unbinding token is `msg.sender`.
	/// @param operator The address responsible for performing the unbinds.
	/// @param from The bound asset owner address.
	/// @param to The unbound tokens' new owner address.
	/// @param tokenIds The list of token types being unbound.
	/// @param amounts The number of tokens for each token type being unbound.
	/// @param bindIds The identifiers of the assets being unbound from.
    /// @param data Additional data sent along with no specified format.
	/// @return `bytes4(keccak256("onERC1155Unbind(address,address,address,uint256[],uint256[],uint256[],bytes)"))`
	function onERC1155BatchUnbind(
        address operator,
        address from,
        address to,
        uint256[] calldata tokenIds,
        uint256[] calldata amounts,
        uint256[] calldata bindIds,
        bytes calldata data
	) external returns (bytes4);

    /// @notice Gets the owner address of the asset represented by id `bindId`.
	/// @param bindId The identifier of the asset whose owner is being queried.
    /// @return The address of the owner of the asset.
	function ownerOf(uint256 bindId) external view returns (address);

    /// @notice Checks if an operator can act on behalf of an asset owner.
    /// @param owner The address that owns an asset.
    /// @param operator The address that acts on behalf of owner `owner`.
    /// @return True if `operator` can act on behalf of `owner`, else False.
    function isApprovedForAll(address owner, address operator) external view returns (bool);

}

```

### Rules

The standard supports two modes of binding:

- Delegated (RECOMMENDED):

Bindable ownership is delegated to binder (to is bindAddress).
- Bindable ownership queries return the binder address.
- Bindable transfers MUST always throw.

*Legacy (NOT RECOMMENDED):*

- Bindable ownership is delegated to asset owner (to is binder.ownerOf(bindId)).
- Bindable ownership queries return the asset owner address.
- Bindable transfers MUST always throw, except when called during asset transfers.
- Bound assets MUST keep track of bound tokens.
- On transfer, bound assets MUST invoke transfers for bound tokens.

In the “delegated” mode, because ownership is attributed to the bound asset contract, asset ownership modifications are decoupled from bound tokens, making bundled transfers efficient as no state management overhead is imposed. This is the recommended binding mode.

The “legacy” binding mode was included for backwards-compatibility purposes, so that existing NFT applications can display bundled tokens out-of-the-box. Because token ownership is attributed to the bound asset owner, asset ownership modifications are coupled to bound tokens, making bundled transfers inefficient.

Binder and bindable implementations MAY choose to support both modes of binding.

For a more detailed rundown of the rules, please see the full [EIP](https://github.com/ethereum/EIPs/pull/5700).

## Rationale

A backwards-compatible standard for token binding unlocks a new layer of composability for allowing wallets, applications, and protocols to interact with, trade, and display bundled assets. One example use-case of this is at Dopamine, where microchipped streetwear garments may be bundled with NFTs such as music, avatars, or digital-twins of the garments themselves, by linking chips to binder smart contracts capable of accepting token binds.

## Backwards Compatibility

The bindable interface is designed to be compatible with existing EIP-721 and EIP-1155 standards.

## Reference Implementation

An ERC-721 implementation supporting “delegated” and “legacy” binding modes can be found [here](https://github.com/leeren/erc-5700/tree/main/src/erc721).

An ERC-1155 implementation supporting only the “delegated” binding mode can be found [here](https://github.com/leeren/erc-5700/tree/main/src/erc1155).

---

Any feedback would be greatly appreciated!

Thanks,

Leeren

## Replies

**ccamrobertson** (2022-10-04):

Awesome work [@leeren](/u/leeren)!

Can you expand a little bit on how legacy applications would falter if the delegated method was universal? Trying to understand a bit more the rationale through a real world example where a legacy client would fail (I suppose it simple would show a `binder` alone to an `owner` and none of the bound NFTs?)

Also curious regarding the nature of binders given the reference to chips. In the case of chips is the idea that a chip would act directly as a binder (assuming the chip is equivalent to an EOA) or that there would be some intermediary contract which escrows binders on behalf of chips.

Lastly, can you explain why in `bind` you have both `to` and `bindAddress`; does *SHOULD* here indicate the possibility these might be distinct?

---

**pxrv** (2022-10-05):

It might help to have a mechanism to accept binds to your assets. Otherwise dusting would be a massive problem?

---

**leeren** (2022-10-17):

Thank you [@ccamrobertson](/u/ccamrobertson)!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ccamrobertson/48/4534_2.png) ccamrobertson:

> Can you expand a little bit on how legacy applications would falter if the delegated method was universal? Trying to understand a bit more the rationale through a real world example where a legacy client would fail (I suppose it simple would show a binder alone to an owner and none of the bound NFTs?)

The intent of the legacy method is so that wallets and applications can display NFTs bound to a `binder` as part of the `binder` owner’s collected NFTs. With the delegated model, if a wallet or application supports the standard, they would be able to do the same, while being able to distinguish between NFTs owned directly and indirectly (through a `binder`), and with much less storage and computational overhead.

For all intents and purposes, this proposal really revolves around the latter model, with the former only included as a solution to projects wishing to also support delegated ownership out-of-the-box with existing apps.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ccamrobertson/48/4534_2.png) ccamrobertson:

> Also curious regarding the nature of binders given the reference to chips. In the case of chips is the idea that a chip would act directly as a binder (assuming the chip is equivalent to an EOA) or that there would be some intermediary contract which escrows binders on behalf of chips.

Yes, the case here would be that the chips themselves would act as binders directly!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ccamrobertson/48/4534_2.png) ccamrobertson:

> Lastly, can you explain why in bind you have both to and bindAddress; does SHOULD here indicate the possibility these might be distinct?

Great question. For the delegated model, `to` would always be `bindAddress`.  For the legacy model, `to` would be the address of whoever the owner of the `binder` is. The reason this is needed for the legacy flow is so that the appropriate transfer event is emitted to showcase ownership by the `binder` owner rather than the `binder` directly (whereas with the delegated model, ownership attribution would be inferred by the `Bind` event logs or interface).

---

**leeren** (2022-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pxrv/48/7346_2.png) pxrv:

> It might help to have a mechanism to accept binds to your assets. Otherwise dusting would be a massive problem?

Great point. The idea here is that the `binder` can choose whether to impose filtering or not for bind acceptance. The simplest implementation, as detailed in the sample code, is one whose `onERC...Bind()` method always returns its interface id, which means any token or NFT can be bound to it. To put restrictions on this, a `binder` can choose to impose an allow or deny list of any sort for those functions. I will update the repository to include an example like this.

---

**pizzarob** (2023-11-03):

I think we should add a method that would allow for binding external NFTs to the current contract in addition to what currently exists. Then there’s two options for binding 1) NFTs within the current contract can be bound and 2) External NFTs that didn’t implement this standard can be bound to the current contract. It would require an approval to transfer, but I think it would be a nice addition to support even more use cases

```auto
/// Function to transfer ownership of a given NFT to the current NFT contract and bind to the specified NFT represented by token ID
/// Must emit Bind event
/// @param tokenId The ID representing the NFT in the current contract that tokenIdToBind will be bound to
/// @param tokenIdToBind The ID representing an external NFT that will be bound to the nft represented by the tokenId param
/// @param tokenToBindAddress Contract address of tokenIdToBind
/// @param from address of token owner
 function bindExternal(
      address from,
      address tokenToBindAddress,
      uint tokenIdToBind,
      uint tokenId
    ) external;
```

