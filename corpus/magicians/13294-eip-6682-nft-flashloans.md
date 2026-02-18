---
source: magicians
topic_id: 13294
title: "EIP-6682: NFT Flashloans"
author: outdoteth
date: "2023-03-14"
category: EIPs
tags: [nft, defi]
url: https://ethereum-magicians.org/t/eip-6682-nft-flashloans/13294
views: 2463
likes: 6
posts_count: 9
---

# EIP-6682: NFT Flashloans

This standard is an extension of the existing flashloan standard (EIP-3156) to support ERC-721 NFT flashloans. It proposes a way for flashloan providers to lend NFTs to contracts, with the condition that the loan is repaid in the same transaction along with some fee.

The current flashloan standard, EIP-3156, only supports ERC-20 tokens. ERC-721 tokens are sufficiently different from ERC-20 tokens that they require an extension of this existing standard to support them.

I tried quite hard to make this EIP have as minimal additional requirements from EIP-3156 as possible. There are only 2 methods:

```auto
interface IERC6682 {
    /// @dev The address of the token used to pay flash loan fees.
    function flashFeeToken() external view returns (address);

    /// @dev Whether or not the NFT is available for a flash loan.
    /// @param token The address of the NFT contract.
    /// @param tokenId The ID of the NFT.
    function availableForFlashLoan(address token, uint256 tokenId) external view returns (bool);
}
```

Here is the link to the EIP:

https://github.com/ethereum/EIPs/pull/6682

I’ve also created an example implementation here (in addition to the reference implementation in the spec): [GitHub - outdoteth/ERC-6682-example: Example implementation of NFT flashloans](https://github.com/outdoteth/ERC-6682-example)

## Replies

**shazow** (2023-03-18):

Since NFTs are non-fungible, would it make sense to give each token the ability to decide its own willingness to flashloan, its own fee, and its own recipient?

This might be too overloaded for a single function, but maybe something like:

```plaintext
function availableForFlashLoan(address token, uint256 tokenId) external view returns (bool isLoanable, address sendFeeTo, uint256 feeAmount);
```

I’m specifically imagining a scenario where an NFT has native flashloan support, and the owners can set their own settings.

---

**ashhanai** (2023-03-20):

Interesting proposal. Can you elaborate on some use cases for borrowing an NFT and returning it in the same transaction?

---

**outdoteth** (2023-03-23):

The existing `flashFee` method already allows for customising the fee on a per-NFT basis so this proposed addition would only allow for the addition of customising the recipient per NFT. In my opinion, this offers quite a bit of excessive customisation with a non-trivial technical cost in the form of complexity and also the fact that it breaks backwards compatibility with EIP-3156.

---

**outdoteth** (2023-03-23):

A flash loan could be useful in any action where NFT ownership is checked.

For example; claiming airdrops, claiming staking rewards, taking an in-game action such as claiming farmed resources etc.

---

**shazow** (2023-03-23):

Oops you’re right, I didn’t notice that you were overloading `amount` as `tokenId` to stay backwards compatible. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**SamWilsn** (2023-03-27):

In your description, you mention that this is a “minimal interface”. I’d argue that neither `flashFeeToken` or `availableForFlashLoan` are actually required for a truly minimal interface.

The lending contract can simply revert if the correct fee hasn’t been paid, and can similarly revert if a particular token isn’t available for loaning.

Granted these functions make it more pleasant to work with, so maybe the correct solution is to change the `description` field ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

---

`flashFeeToken` seems too limiting. If you want to support paying fees with multiple different tokens, you’d need to deploy several different ERC-6682 contracts, right?

I think you could go with a more flexible interface, replacing `flashFeeToken` and `availableForFlashLoan` with:

```plaintext
function flashFee(address token, uint256 tokenId, address feeToken) public view returns (uint256);
```

where `token` is the NFT contract, `tokenId` is the NFT’s id, and `feeToken` is the token the borrower wants to pay with. Then `flashFee` would return the fee denominated in `feeToken` required to borrow that NFT, or revert if that NFT isn’t available or that fee token isn’t supported.

---

I’m not sure how valuable it is to reuse the [ERC-3156](https://eips.ethereum.org/EIPS/eip-3156) interface here. It seems like they are different enough to just make your own interface instead of extending it. Like `amount` makes no sense for ERC-721 tokens.

---

I’m not super versed in the NFT world, so I might be way off here, but this interface doesn’t seem like it would handle special properties of the NFT. For example, if the lender is the NFT contract itself, it might be willing to mint/loan/burn the tokens on the fly, and not require the tokens exist beforehand. If that is the case, the borrower might want to specify properties (for an art NFT a “special property” might be background colour; for an ENS-like token, it might be the domain name.) This interface doesn’t allow the borrower to specify those properties.

---

**outdoteth** (2023-07-27):

I will address each of these points.

> Granted these functions make it more pleasant to work with, so maybe the correct solution is to change the description field

Agreed, “minimal” is not the correct term here.

> flashFeeToken seems too limiting. If you want to support paying fees with multiple different tokens, you’d need to deploy several different ERC-6682 contracts, right?

This is technically true but quite unlikely in practice I think. If we consider EIP-3156, it also takes a similarly opinionated approach on what the currency fee should be paid in – The loan currency.

The `flashFeeToken` already provides an additional degree of customisability by decoupling the loan asset (NFT) and the payment asset (flashFeeToken). Typically, if there is a pool of NFTs, there is appropriate context on what currency to use for the `flashFeeToken`. For example, a pool of NFTs in an AMM will be paired against a token or a pool of NFTs that is used to perpetually sell call options, will have a notional asset associated with it.

> I’m not sure how valuable it is to reuse the ERC-3156 interface here. It seems like they are different enough to just make your own interface instead of extending it. Like amount makes no sense for ERC-721 tokens.

Within the context of this EIP, `amount` is a placeholder for `tokenId`. Since `amount` is of type `uint256` this can work. The benefit of hooking into ERC-3156 is that it allows for contracts that support ERC20 flashloans to be easily extended to support NFT flashloans too (with minimal code changes). If we have an entirely new interface then the change-set for supporting both NFT flashloans and ERC20 flashloans becomes unnecessarily large.

> If that is the case, the borrower might want to specify properties (for an art NFT a “special property” might be background colour; for an ENS-like token, it might be the domain name.) This interface doesn’t allow the borrower to specify those properties.

I’m not sure I fully understand the use case here. Could you explain a bit more?

---

**SamWilsn** (2023-07-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/outdoteth/48/8851_2.png) outdoteth:

> If that is the case, the borrower might want to specify properties (for an art NFT a “special property” might be background colour; for an ENS-like token, it might be the domain name.) This interface doesn’t allow the borrower to specify those properties.

I’m not sure I fully understand the use case here. Could you explain a bit more?

Sure, so imagine a `DiscoDonut` NFT contract. Each `DiscoDonut` token has a `flavour` attribute.

`DiscoDonut` implements ERC-721 and supports flash loans. Because the contract implements ERC-721 directly, it can *flash mint*, or mint new tokens on demand.

As a user, I want to get into an exclusive party for holders of chocolate sprinkle flavoured `DiscoDonut` tokens. I don’t care which `tokenId` I get from my flash loan, just that it has a `flavour` of “chocolate sprinkle”.

I’m not necessarily suggesting that EIP-6682 be expanded to support this use case. I just wanted to mention it.

