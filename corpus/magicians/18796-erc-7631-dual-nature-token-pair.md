---
source: magicians
topic_id: 18796
title: "ERC-7631: Dual Nature Token Pair"
author: Vectorized
date: "2024-02-20"
category: ERCs
tags: [erc, erc-721, erc20]
url: https://ethereum-magicians.org/t/erc-7631-dual-nature-token-pair/18796
views: 7346
likes: 86
posts_count: 35
---

# ERC-7631: Dual Nature Token Pair

# Dual Nature Token Pair

requires: ERC-20, ERC-721

## Abstract

A fungible ERC-20 token contract and non-fungible ERC-721 token contract can be interlinked, allowing actions performed on one contract to be reflected on the other. This proposal defines how the relationship between the two token contracts can be queried. It also enables accounts to configure if ERC-721 mints and transfers should be skipped during ERC-20 to ERC-721 synchronization.

## Motivation

The ERC-20 fungible and ERC-721 non-fungible token standards offer sufficient flexibility for a co-joined, dual nature token pair. Transfers on the ERC-20 token can automatically trigger transfers on the ERC-721 token, and vice-versa. This enables applications such as native ERC-721 fractionalization, wherein purchasing ERC-20 tokens leads to the automatic issuance of ERC-721 tokens, proportional to the ERC-20 holdings.

Dual nature token pairs maintain full compliance with both ERC-20 and ERC-721 token standards. This proposal aims to enhance the functionality of dual nature token pairs.

To facilitate querying the relationship between the tokens, extension interfaces are proposed for the ERC-20 and ERC-721 tokens respectively. This enables various quality of life improvements such as allowing decentralized exchanges and NFT marketplaces to display the relationship between the tokens.

Additionally, users can configure if they want to skip ERC-721 mints and transfers during ERC-20 to ERC-721 synchronization.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Overview

A dual nature token pair comprises of an ERC-20 contract and an ERC-721 contract.

For convention, the ERC-20 contract is designated as the base contract, and the ERC-721 contract is designated as the mirror contract.

### ERC-20 Extension Interface

The ERC-20 contract MUST implement the following interface.

```solidity
interface IERC7631Base {
    /// @dev Returns the address of the mirror ERC-721 contract.
    ///
    /// This method MAY revert or return the zero address
    /// to denote that a mirror ERC-721 contract has not been linked.
    ///
    /// If a non-zero address is returned, the returned address MUST
    /// implement `IERC7631Mirror` and its `baseERC20()` method MUST
    /// return the address of this contract.
    ///
    /// Once a non-zero address has been returned, this method
    /// MUST NOT revert and the returned value MUST NOT change.
    function mirrorERC721() external view returns (address);
}
```

The ERC-20 contract MAY implement the following interface.

```solidity
interface IERC7631BaseNFTSkippable {
    /// @dev Emitted when the skip NFT status of `owner` is changed by
    /// any mechanism.
    ///
    /// This initial skip NFT status for `owner` can be dynamically chosen to
    /// be true or false, but any changes to it MUST emit this event.
    event SkipNFTSet(address indexed owner, bool status);

    /// @dev Returns true if ERC-721 mints and transfers to `owner` SHOULD be
    /// skipped during ERC-20 to ERC-721 synchronization. Otherwise false.
    ///
    /// This method MAY revert
    /// (e.g. contract not initialized, method not supported).
    ///
    /// If this method reverts:
    /// - Interacting code SHOULD interpret `setSkipNFT` functionality as
    ///   unavailable (and hide any functionality to call `setSkipNFT`).
    /// - The skip NFT status for `owner` SHOULD be interpreted as undefined.
    ///
    /// Once a true or false value has been returned for a given `owner`,
    /// this method MUST NOT revert for the given `owner`.
    function getSkipNFT(address owner) external view returns (bool);

    /// @dev Sets the caller's skip NFT status.
    ///
    /// This method MAY revert
    /// (e.g. insufficient permissions, method not supported).
    ///
    /// Emits a {SkipNFTSet} event.
    function setSkipNFT(bool status) external;
}
```

### ERC-721 Extension Interface

The ERC-721 contract MUST implement the following interface.

```solidity
interface IERC7631Mirror {
    /// @dev Returns the address of the base ERC-20 contract.
    ///
    /// This method MAY revert or return the zero address
    /// to denote that a base ERC-20 contract has not been linked.
    ///
    /// If a non-zero address is returned, the returned address MUST
    /// implement `IERC7631Base` and its `mirrorERC721()` method MUST
    /// return the address of this contract.
    ///
    /// Once a non-zero address has been returned, this method
    /// MUST NOT revert and the returned value MUST NOT change.
    function baseERC20() external view returns (address);
}
```

## Rationale

### Implementation Detection

The `mirrorERC721` and `baseERC20` methods returning non-zero addresses suffice to signal that the contracts implement the required interfaces. As such, ERC-165 is not required.

The `getSkipNFT` and `setSkipNFT` methods MAY revert. As contracts compiled with Solidity or Vyper inherently revert on calls to undefined methods, a typical `IERC7631Base` implementation lacking explicit `getSkipNFT` and `setSkipNFT` definitions still complies with `IERC7631BaseNFTSkippable`.

### NFT Skipping

A useful pattern is to make `getSkipNFT` return true by default if `owner` is a smart contract. This allows ERC-20 liquidity pools to avoid having ERC-721 tokens automatically minted to it by default whenever there is an ERC-20 transfer.

The choice of `getSkipNFT` returning a boolean value is for simplicity. If more complex behavior is needed, developers may add in extra methods of their own.

### Implementation Conventions

The ERC-20 contract is designated as the base contract for convention, as a typical implementation can conveniently derive ERC-721 balances from the ERC-20 balances. This does not prohibit one from implementing most of the logic in the ERC-721 contract if required.

This proposal does not cover the token synchronization logic. This is to leave flexibility for various implementation patterns and novel use cases (e.g. automatically rebased tokens).

### Linking Mechanism

The linking process omitted for flexibility purposes. Developers can use any desired mechanism (e.g. linking in constructor, initializer, or via custom admin-only public methods on the two contracts). The only restriction is that the pairing must be immutable once established (to simplify indexing logic).

## Backwards Compatibility

No backward compatibility issues found.

## Security Considerations

### Synchronization Access Guards

External methods for synchronization logic must be guarded such that only the other contract is authorized to call them.

### Rare NFT Sniping

For dual nature collections that offer ERC-721 tokens with differing rarity levels, the ERC-721 metadata should be revealed in a way that is not easily gameable with metadata scraping and ERC-20 token transfers. A recommendation is to require that an ERC-721 token is held by the same account for some time before revealing its metadata.

### Out-of-gas Denial of Service

ERC-20 transfers can automatically trigger multiple ERC-721 tokens to be minted, transferred or burned. This can incur O(n) gas costs instead of the typical O(1) gas costs for ERC-20 tokens transfers. Logic for selecting ERC-721 token IDs can also incur additional gas costs. Synchronization logic must consider ERC-721 related gas costs to prevent out-of-gas denial of service issues.

## Implementations



      [github.com](https://github.com/Vectorized/dn404)




  ![image](https://opengraph.githubassets.com/de27a07a33afde5bed101e9cd95ba031/Vectorized/dn404)



###



Implementation of a co-joined ERC20 and ERC721 pair.

## Replies

**Philogy** (2024-02-21):

What’s the point of the non-fungible paired ERC721 if it’s actually fungible? Seems like a lot of unnecessary complexity and attack surface for not much benefit.

---

**Vectorized** (2024-02-21):

Gachapon game mechanics. Most NFTs are emotional products, so it’s hard to rationalize.

Given the market demand, we would like to develop flexible and safe ways for people to use such mechanisms.

---

**brrito** (2024-02-21):

Speaking as a long-time NFT fractionalization skeptic who’s trying to understand why “ERC404” is so popular right now: the main benefit IMO is defragmenting liquidity and attention. ERC721s which were previously only traded on Blur and OpenSea can also be traded on CEXes like Binance and Coinbase (in ERC20 form), and vice versa.

Seems to make sense and is valuable in the short-medium term, since NFTs are mostly used for speculating at the moment, but agree that making non-fungible assets fungible defeats the purpose.

---

**Tsubasa** (2024-02-21):

the market seems to have a very positive reaction to this new hybrid type of nature. Mainly increased flexibility on the collectors side and additional game theory methods to how traditionally supply and demand behaviors of users would change and reflect on primary and secondary markets.

It is definitely an exciting experiment and especially when initial implementations like the "erc"404 caused a lot of inefficiency resulting in gas spikes in the past few weeks, this implementation by the ‘avengers’ is a great product birth by adversity and a good step towards ‘optimization to market needs’.

Kudos to the authors.

---

**Tsubasa** (2024-02-21):

Good point!

In regards to ‘making non-fungible, fungible’, it is likely a response to the nature of how the NFTs landscape has been transforming over the years, since the 2021 era, and the introduction of blur, have shown that more fungible versions of art or one with a hybrid nature would have its own niche and could potentially become a large segment in future. When we also consider what this does to collecting art and reveal mechanisms it also brings an interesting conversation to the table.

---

**tba** (2024-02-21):

Big benefit of this proposal is the seamless synchronization between ERC-20 and ERC-721 contracts. you can basically establishing a dynamic relationship between these tokens and users can experience unparalleled flexibility and efficiency in managing their assets. tx’s initiated on the ERC-20 contract automatically trigger corresponding actions on the ERC-721 contract, and vice versa, facilitating effortless token management and enhancing user experience.

Furthermore (as already mentioned by brrito) the proposal allows not only trading on NFT marketplaces, but also on decentralized and centralized exchanges which brings a lot more attention to it. By bridging the gap between fungible and non-fungible tokens, it opens even more doors to a world of possibilities for creators, investors, and enthusiasts alike. With fractionalized buying it also brings more opportunities for investors to gain exposure.

---

**JesseBTC** (2024-02-22):

There are two discussions around this proposal that need to be had. One is purely subjective and centered around, why combine the to aspects of ERC721 and ERC20 into one contract when they both serve the original purpose of providing fungibility and non fungibility separately. There are clear advantages to this for both NFT projects and the wider industry. One such advantage being, the opportunity to have fractional exposure to the NFT if the price of said non fungible asset is unattainable. People can own a divisible amount of an NFT or scale into ownership of a full token to unlock an NFT.

Another benefit is the game theory dynamics and novel use cases that can come from utilising the core dynamics of DN404 to create novel ways of interacting with both the token and the NFT which have not yet been available to developers. There could be countless opportunities for new innovation with this standard.

But this part of the discussion is purely subjective, some will see value in it and some will not. Neither are wrong it is an independent opinion.

The core part of the discussion that needs to be had is objective. Objectively is the standard being proposed safe, is the codes logic sound, and does it bring any inherent risk to users of this experimental standard. Does it pass the test in terms of code quality and engineering to receive an official ERC title. This is what should be reviewed, without our subjective opinion of if it is valuable. The subjective opinion on NFTs and the usage of ERC721 can also be called into question. Many use cases of ERC721 could quite easily exist with no need for any on chain token representation, for example gated token communities. This is subjective to whether it actually adds value by being on chain or off chain.

Let’s be objective here and focus on the code, the quality of the engineering and the security of the standard and allow experimenters to prove value of the ERC standard being proposed once we accept that it is at least safe for experimentation and further development.

---

**Vectorized** (2024-02-22):

Would re-emphasize that dual nature token pairs are entirely feasible with ERC-20 and ERC-721 alone, with full standard compliance.

The goal of this proposal is to standardize an interface for signalling (like ERC-2981, ERC-5185) and permissionless configuration of ERC-20 to ERC-721 syncing behavior.

---

**I3artwork** (2024-02-22):

Fractionalizing NFTs has benefits for the smaller fish in sea. Inscreased **accessibility**. People who would normally be prized out can now participate by purchasing a smaller portion of the NFT. This also means people can **diversify** their NFT portofolio.

Also the big fish can benefit because of the increased **liquidity** this technology brings with it.

---

**MichaelWinczuk** (2024-02-22):

There are multiple types of traders and enthusiasts in this space. Some trade tokens, Some trade NFTs, some hunt for rares, and DN 404 affords an interesting investment opportunity to everyone. I am curious to see what sort of utilities come from this standard. Cheers to the brilliant minds behind it. Bravo

---

**0xth0mas** (2024-02-22):

As one of the original contributors to the DN404 implementation, I think it’s important to reiterate what [@Vectorized](/u/vectorized) mentioned above: the structure used in DN404 allows the tokens to seamlessly integrate into existing protocols that are currently built for ERC20 or ERC721 with zero security issues or integration changes.

The benefit of an ERC for DN404 is that protocols that want to support specific features - such as knowing the paired ERC20 of the ERC721 or vice-versa and toggling of the skip NFT feature - of DN404 will have a standard interface for handling them.

Enshrining the “skip NFT” concept in the token standard where an account defaults to skipping the NFT mint if it is a contract account and defaults to NOT skipping the NFT mint if it is an EOA, with the account being able to change its default behavior with `setSkipNFT` allows for better gas efficiency in a more decentralized/ownerless manner when new AMMs, token routers and smart wallets are sending and receiving the ERC20 tokens.

---

**0xMillz** (2024-02-25):

It used to be that you couldn’t even buy 0.1 shares of Amazon stock if you only had 505 USD in your brokerage account, when the market price for AMZ was $1200/share. This was before Robinhood, et al. But for certain systems, both in Ethereum and the accompanying Universe, 1 exact unit is only equal to 1 exact unit. If I was only born with one hand I can still cast one whole ballot.

Scraping together Bitcoin satoshi after satoshi just to have a wallet that exactly reads 1.00000000 is not uncommon, even though that chain has no concept of exactly that amount being anything special.

The same way one can own a piece of a condo “timeshare” in Aspen (free lunch included). The point is there is this use case for x amounts of fungible *widgets*, semi-useless alone, but when combined as puzzle pieces in the predetermined standard amount make 1 non-fungible whole.

My first post here, but I’ve read a lot of the history. Fractional NFTs like this have already been inspired, debated, and forgotten- many years ago. Some senior wizards had good perspectives, it’s good to try a simple forum search and give credit where it’s due.

---

**Tsubasa** (2024-02-26):

wow i really like this perspective. nice thought!

---

**fomo-protocol** (2024-03-02):

IMO, ERC20 and ERC721 is already enough. The relationship between them are developers’ decision. We don’t need to standardardized how they would interact with each other.

There could be a lot of ways that they can interact with each other, and we can’t possible included all of them in a ERC nor should we.

---

**xinbenlv** (2024-03-02):

First of all, thanks for submitting a ERC proposal.

The draft LGTM editorial for a status of DRAFT so I merged it.

Technical feedback / question

Q1: choice of `bool`

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vectorized/48/7129_2.png) Vectorized:

> event SkipNFTSet(address indexed owner, bool status);

The status is `bool`, have you thought of using something that’s better than bool,

1. avoid mistaken implementation, similar to rationale of ERC-165’s choice return value instead of bool they use a 6bytes
2. allow future expansion. same rationale as ERC-5269: ERC Detection and Discovery choosing the status to be a bytes32 as hash of a string so

That apply to the parameters and return values of

- function setSkipNFT(bool status) external;
- function getSkipNFT(address owner) external view returns (bool);

Etc.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vectorized/48/7129_2.png) Vectorized:

> ```auto
> interface IERC7631Mirror {
>     /// @dev Returns the address of the mirror NFT contract.
>     /// This method MAY revert or return the zero address
>     /// to denote that a base ERC-20 contract has not been linked.
>     ///
>     /// If a non-zero address is returned, the returned address MUST
>     /// implement `IERC7631Base` and its `mirrorERC721()` method MUST
>     /// return the address of this contract.
>     ///
>     /// Once a non-zero address has been returned, this method
>     /// MUST NOT revert and the returned value MUST NOT change.
>     function baseERC20() external view returns (address);
> }
> ```

Q2: Do you wanna specify recommented function that sets the addresses of ERC-20 and ERC-721 binding?

---

**Vectorized** (2024-03-02):

I agree that just ERC-20 and ERC-721 alone suffice for the accounting logic.

This ERC is foremost a signalling ERC (similar to ERC-4906). It informs dApps about the link between the two tokens, to aid indexing, and to enhance the experience for end-users. It does not impose any other restrictions on how the two tokens should interact.

We understand that a standard cannot encompass all possible use cases – it’s a careful balance of imposing restrictions and leaving flexibility.

The `setSkipNFT` and `getSkipNFT` methods may be omitted, as they are allowed to revert by default. A contract that does not implement these methods in Solidity will essentially revert when called with their function selectors, which is functionally the same as a contract that implements these methods and reverts in them.

---

**Vectorized** (2024-03-02):

1. The choice of bool is for simplicity. In the case where more complex behavior is needed and can benefit from standardized interpretation, an extension standard can be proposed.
2. The linking process can use any desired mechanism (e.g. linking in constructor, initializer, or via custom admin-only public methods on the two contracts). The only restriction is that the pairing must be immutable once established (to simplify indexing logic).

I think we can clarify in the rationale on the choice for `bool`, and why the mechanism for linking the contracts is omitted.

---

**Vectorized** (2024-03-02):

Might be better if we specify that `getSkipNFT` reverting SHOULD be interpreted by dApps that the `setSkipNFT` function should not be displayed in the front-end.

I understand that not all implementations will want the skip NFT status to be configurable.

The `getSkipNFT` and `setSkipNFT` methods can be left unimplemented in Solidity, which is functionally equivalent to implementing these methods and reverting in them.

---

**xinbenlv** (2024-03-03):

Another question: I am wondering why does it need the skipping methods? Can they be MAY instead of MUST?

---

**Vectorized** (2024-03-03):

The skipping methods MAY be implemented. We will clarify.


*(14 more replies not shown)*
