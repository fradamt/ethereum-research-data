---
source: ethresearch
topic_id: 13237
title: ERC721 Extension for zk-SNARKs
author: Nero_eth
date: "2022-08-04"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/erc721-extension-for-zk-snarks/13237
views: 29053
likes: 47
posts_count: 26
---

# ERC721 Extension for zk-SNARKs

**Hi community,**

**I’ve recently been working on this draft that describes zk-SNARK compatible ERC-721 tokens:**

**https://github.com/Nerolation/EIP-ERC721-zk-SNARK-Extension**

Basically every ERC-721 token gets stored on a Stealth Address that constists of the hash *h* of a user’s address *a*, the token ID *tid* and a secret *s* of the user, such that *stealthAddressBytes* = *h(a,tid,s)*. The *stealthAddressBytes* are inserted into a merkle tree. The root of the merkle tree is maintained on-chain. Tokens are stored at an address that is derived from the user’s leaf in the merkle tree: *stealthAddressBytes* => bytes32ToAddress().

For **transfering** a token, the contract requires a proof that a user can

i) generate a stealth address that is included in the merkle tree

ii) generate the merkle tree after updating the respective leaf

For **minting** a token, the contract requires a proof that a user can

i) generate a stealth address and add it to an empty leaf in the merkle tree

ii) generate the merkle tree after updating the respective leaf

For **burning** a token, the contract requires a proof that a user can

i) generate a stealth address and delete it from a leaf in the merkle tree

ii) generate the merkle tree after updating the respective leaf

**NOTE:** The generation of the stealth address requires to have access to a private key. E.g. a user signs a message, the circuit parses the public key (…and address), hashes the address together with the token ID and a secret value and inserts the result into a leaf of the merkle tree. In the end the circuit compares the calculated and user-provided roots for verification.

For general information, have a look at Vitalik’s short section on private POAPs in [this article](https://vitalik.ca/general/2022/01/26/soulbound.html) on SoulBound tokens.

I think, this EIP is the exact implementation of what Vitalik described.

**This is the current draft of the interface:**

```auto
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.6;
...
interface ERC0001 /* is ERC721, ERC165 */ {

    /// @notice Mints token to a stealth address `stA` if proof is valid. stA is derived from
    ///  stealthAddressBytes which is the MIMC Sponge hash `h` (220 rounds) of the user address `eoa`,
    ///  the token id `tid` and a user-generated secret `s`, such that stA  computePublicKey() => computeStealthAddress() ).
    ///       - prover can generate the merkle root from an empty leaf.
    ///       - prover can generate the merkle root after updating the empty leaf.
    /// @param currentRoot A known (historic) root.
    /// @param newRoot Updated root.
    /// @param stealthAddressBytes Hash of user address, tokenId and secret.
    /// @param tokenId The Id of the token.
    /// @param proof The zk-SNARK.
    function _mint(bytes32 currentRoot, bytes32 newRoot, bytes32 stealthAddressBytes, uint256 tokenId, bytes proof) external;

    /// @notice Burns token with specified Id from stealth address `stA` if proof is valid.
    /// @dev Requires a proof that verifies the following:
    ///       - prover can generate the StealthAddress (e.g. user signs msg => computePublicKey() => computeStealthAddress() )
    ///       - prover can generate the merkle root from an non-empty leaf.
    ///       - prover can generate the merkle root after nullifieing the non-empty leaf.
    /// @param currentRoot A known (historic) root.
    /// @param newRoot Updated root.
    /// @param stealthAddressBytes Hash of user address, tokenId and secret.
    /// @param tokenId The Id of the token.
    /// @param proof The zk-SNARK.
    function _burn(bytes32 currentRoot, bytes32 newRoot, bytes32 stealthAddressBytes, uint256 tokenId, bytes proof) external;

    /// @notice Transfers token with specified Id from current owner to the recipient's
    /// stealth address, if proof is valid.
    /// @dev Requires a proof that verifies the following:
    ///       - prover can generate the StealthAddress (e.g. user signs msg => computePublicKey() => computeStealthAddress() ).
    ///       - prover can generate the merkle root from an non-empty leaf.
    ///       - prover can generate the merkle root after updating the non-empty leaf.
    /// @param currentRoot A known (historic) root.
    /// @param newRoot Updated root.
    /// @param stealthAddressBytes Hash of user address, tokenId and secret.
    /// @param tokenId The Id of the token.
    /// @param proof The zk-SNARK.
    function _transfer(bytes32 currentRoot, bytes32 newRoot, bytes32 stealthAddressBytes, uint256 tokenId, bytes proof) external;

    /// @notice Verifies zk-SNARKs
    /// @dev Forwards the different proofs to the right `Verifier` contracts.
    ///  Different Verifiers are required for each action, because of the merkle-tree logic involved.
    /// @param currentRoot A known (historic) root.
    /// @param newRoot Updated root.
    /// @param stealthAddressBytes Hash of user address, tokenId and secret.
    /// @param tokenId The Id of the token.
    /// @param proof The zk-SNARK.
    /// @return Validity of the provided proof.
    function _verifyProof(bytes32 currentRoot, bytes32 newRoot, bytes32 stealthAddressBytes, uint256 tokenId, bytes proof) external returns (bool);
}
```

This EIP is still in idea stage (no pull-request yet).

Looking for collaborators!

## Replies

**vbuterin** (2022-08-08):

I feel like you can accomplish this with much lighter-weight technology.

Just use regular [stealth addresses](https://hackernoon.com/blockchain-privacy-enhancing-technology-series-stealth-address-i-c8a3eb4e4e43):

- Every user has a private key p (and corresponding public key P = G * p)
- To send to a recipient, first generate a new one-time secret key s (with corresponding public key S = G * s), and publish S
- The sender and the recipient can both compute a shared secret Q = P * s = p * S. They can use this shared secret to generate a new address A = pubtoaddr(P + G * hash(Q)), and the recipient can compute the corresponding private key p + hash(Q). The sender can send their ERC20 to this address.
- The recipient will scan all submitted S values, generate the corresponding address for each S value, and if they find an address containing an ERC721 token they will record the address and key so they can keep track of their ERC721s and send them quickly in the future.

The reason why you don’t need Merkle trees or ZK-SNARK-level privacy is that each ERC721 is unique, so there’s no possibility of creating an “anonymity set” for an ERC721. Rather, you just want to hide the link to the sender and recipient’s highly visible public identity (so, you can send an ERC721 to “vitalik.eth” and I can see it, but no one else can see that vitalik.eth received an ERC721; they will just see that *someone* received an ERC721).

You can generalize this scheme to smart contract wallets by having the smart contract wallet include a method:

`generateStealthAddress(bytes32 key) returns (bytes publishableData, address newAddress)`

which the sender would call locally. The sender would publish `publishableData` and use `newAddress` as the address to send the ERC721 to. The assumption is that the recipient would code `generateStealthAddress` in such a way that they can use `publishableData` and some secret that they personally possess in order to compute a private key that can access ERC721s at `newAddress` (`newAddress` may itself be a CREATE2-based smart contract wallet).

One remaining challenge is figuring out how to pay fees. The best I can come up with is, if you send someone an ERC721 also send along enough ETH to pay fees 5-50 times to send it further. If you get an ERC721 without enough ETH, then you can tornado some ETH in to keep the transfer chain going. That said, maybe there is a better generic solution that involves specialized searchers or block builders somehow.

---

**AbhinavMir** (2022-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> corresponding private key P=G∗p

Possible correction - Public key where G is the base point of ECG

---

**WF9639** (2022-08-08):

是否可支持跨链支付其他的代币呢，因为所有网络都是一个大家庭，覆盖率广，使用率高，效益越好，即流量为王

---

**shugangyao1** (2022-08-08):

Stealth Address (BSAP/ISAP/DKSAP) 只能暂时隐藏吧，一旦接受地址被转账，则发送者->隐藏接收地址-》提取地址 的转账路径还是会出现在 ERC20/NFT 合约的 transfer event 中。

---

**mesquka** (2022-08-08):

Given the pure stealth address are essentially generating fresh ethereum addresses for the purposes of this scenario wouldn’t it make more sense to implement as a wallet level protocol rather than in a token standard?

As [@vbuterin](/u/vbuterin) stated above this would make the most sense in a smart contract wallet, but the problem remains that has needs to be paid in an unlinkable way otherwise the protocol would only delay the construction of a transaction graph by an observer rather than properly prevent it.

I see 2 approaches here assuming our stealth address protocol is smart contract wallet based: A) an out of band payment is made to compensate a gas related, or B) the transaction compensates a gas relayer from a seperate stealth address where stealth addresses. B is the ‘decentralized’ approach, but would only really achieve UTXO levels of privacy, A would be as private as the out of band payment method to the gas relayer and strongly private to everyone else assuming the gas relayer can be trusted to not reveal any data they obtain but this is obviously a fairly centralized approach.

Side note: Using a zk shielded pool with approach B would prevent visibility of the transaction graph which should result in a strongly private protocol, I’m not sure another generalized approach is possible without a significant change to Ethereum’s transaction format.

---

**eigmax** (2022-08-08):

Only Stealth Address is not enough to cut off the linkage between sender and receiver, but combining with a Merkle tree(like Tornado Cash’s), and using the stealth address’s private key as the Merkle tree leaf’s committed value to withdraw the money, can work here. This is how Eigen Network(https://www.eigen.cash) implements its anonymous payment.

---

**wdai** (2022-08-08):

The main difference between a Zcash-style zk-SNARKs + Merkle tree method vs stealth addresses method mentioned by Vitalik above is in terms of **confidentiality vs anonymity**–the token id transacted can be hidden with zk-SNARKs but not with stealth addresses (which only provide anonymity). Note that token ids transacted does represent some information leak. In the particular case of transfers, we can aim for full confidentiality of transactions instead of just anonymity. However, for supporting more complicated smart contract logic taking token type and amount (ERC20 / 1155), then we can only hope to achieve anonymity.

An additional downside to stealth address is that if it is applied to anything beyond 721 (like 20 or 1155), then there is very little privacy added as the chain of transfers can be traced. Whereas a zk-SNARK based method can preserve confidentiality or anonymity completely.

Ideally, L1s should support privacy-preserving tokens that can be used by smart contract applications (anonymity for composable on-chain transactions and confidentiality for P2P swaps / transfers). This can be achieved with known techniques. Effectively, one can take the best part of privacy-focused L2s like Aztec, ZkOpru, Railgun, and Eigen and make the privacy-preserving token accounting default on the L1. This is described in [FLAX](https://eprint.iacr.org/2021/1249). The main problem to have built-in privacy on Ethereum is that we have a fixed gas fee payment mechanism tied to EOAs, making all privacy-preserving token standard moot unless we have a privacy-preserving gas payment method. This is why privacy is currently best done in a separate layer for Ethereum unless privacy-preserving gas payments are possible. A privacy layer also has the added benefit of not needing to change token standards on L1–the smart contract own assets on behalf of its “L2” users on L1.

However, there are ways to salvage this with anonymous gas payments and privacy-preserving ERC20/721/1155s. For gas payments, we can combining a shielded token pool (e.g. Zcash style zk-SNARKs + Merkle tree) into EIP-4337. Composable usage of tokens in these shielded pools require alternative to ERC20 approve that is atomic and stateless (can be done by expanding call stack access as described [here](https://ethresear.ch/t/access-to-calldata-of-non-current-call-frames-and-alternative-methods-of-token-use-authorization/11962/5)). The caveat is that this means we need to change user transaction / ERC20 / Defi ecosystems entirely, and at that point, might as well build a privacy layer on-top of Ethereum.

---

**llllvvuu** (2022-08-09):

Likely this is a better fit for Soulbound Tokens, where we

- don’t necessarily desire anonymity but just unlinkability of nyms
- gas less of an issue / out-of-band gas more viable (DAO can provide gas station for SBT holders to do SBT-related stuff)

If SBTs:

- each go to a fresh stealth address (if the mint is self-serve the user can generate a private key themselves, rather than going through the stealth address generation protocol)
- can optionally be linked
- can be issued/revoked via semaphore/interep proof (there’s a question of whether all-or-nothing sharing is achievable here)
- can be added/removed from semaphore/interep group

This pretty much gets us to DeSoc, except of course you’d need at least one social recovery set per connected component of nyms.

---

**vbuterin** (2022-08-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/mesquka/48/9850_2.png) mesquka:

> Given the pure stealth address are essentially generating fresh ethereum addresses for the purposes of this scenario wouldn’t it make more sense to implement as a wallet level protocol rather than in a token standard?

The reason why this needs to be standardized is that the sender needs the ability to automatically generate an address belonging to the recipient without contacting the recipient.

---

**Nero_eth** (2022-08-09):

I like the idea and it makes full sense to implement it in the way suggested

Removing the zk-SNARK part comes with further simplification, which is great.

Only one thing:

In the case, C representing a contract (going to be) deployed on A through CREATE2, the sender would have to use a different method (using the recipient’s address, salt, bytecode) to generate the address for C, which would destroy privacy, or do I miss something here? How would the recipient be able to have a contract already waiting at A to receive the token? In other words, would the sender have to anticipate a specific CREATE2 call eventually executed by the recipient at address A?

Addressing the remaining challenge mentioned, I’m generally a fan of specialized searchers (as implemented in [Surrogeth](https://github.com/lsankar4033/surrogeth)) implemented in the final app. However, this would require to have some additional functionality for handling related incentives for frontrunners within the standard. Therefore I agree that the “pay for the recipients’ transfers and then tornado-refill” is the better approach.

I’m keen to implement it.

EDIT: Find a minimal poc with stealth addresses [here](https://github.com/Nerolation/EIP-ERC721-zk-SNARK-Extension/blob/main/assets/minimal_poc.ipynb).

---

**Nero_eth** (2022-08-10):

I guess, the approach suggested by [@vbuterin](/u/vbuterin) is the one that we should go for:

I’ve started drafting an EIP [here](https://github.com/Nerolation/EIP-ERC-721-Stealth-Addresses/blob/271a3b4651f73bac9ec32621abb0eb1308a8c79f/eip.md).

Please feel free to provide feedback!

Also, I’m looking for contributors with experience in the EIP process and Crypto/Ethereum in general, to help me implementing it.

---

**vbuterin** (2022-08-11):

> In other words, would the sender have to anticipate a specific CREATE2 call eventually executed by the recipient at address A?

Yes, this is exactly the idea. In general, this is a common pattern for smart contract wallets, which is necessary to replicate the existing functionality where users can receive coins to an address they generate offline without having to spend coins to register that address on-chain first.

---

**vbuterin** (2022-08-11):

[@Nero_eth](/u/nero_eth) now that I think more about this, I am realizing that it doesn’t actually make sense to make this standard *part of* ERC721 per se. There are lots of potential use cases for it. So it probably should be an independent ERC that lets users generate new addresses that belong to other users, and both ERC721 applications and other applications can use that ERC.

Aside from that, my main feedback to the EIP so far is that I do hope that something like the `generateStealthAddress` method idea from my earlier post can be added so that we can support smart contract wallets.

> You can generalize this scheme to smart contract wallets by having the smart contract wallet include a method:
>
>
> generateStealthAddress(bytes32 key) returns (bytes publishableData, address newAddress)
>
>
> which the sender would call locally. The sender would publish publishableData and use newAddress as the address to send the ERC721 to. The assumption is that the recipient would code generateStealthAddress in such a way that they can use publishableData and some secret that they personally possess in order to compute a private key that can access ERC721s at newAddress (newAddress may itself be a CREATE2-based smart contract wallet).

---

**artdgn** (2022-08-14):

How would calculating `p * S` for every S of every potential transfer (of many implementing contracts) work for private keys stored on e.g. hardware wallets / secure elements? Would this mean that this scheme is only tractable for low value assets (since sender cannot assume the receiver ever finds out)?

Maybe only specially designated addresses can be used (e.g. signalling their ability to receive this kind of transfer in some public way) and a special registry will be needed for those. And to have such an address one would use some ephemeral private key generation scheme every time to scan for those transfers and transfer them to some other address (that is controlled by the actual private key, but isn’t public).

---

**Nero_eth** (2022-08-14):

The value `s` represents a secret value and not the senders private key.

Using a random one-time secret, no private information gets leaked.

I think, it’s best to implement the suggested `generateStealthAddress(bytes32 key)`  into a smart contract wallet (see sample implementation [here](https://github.com/Nerolation/EIP-ERC-721-Stealth-Addresses/blob/main/eip.sol)), as outlined above.

There are still some points open for discussion:

1. How would p*S be implemented (at recipient’s side) to not expose the wallet to any security risk?
2. Should P be immutable or updateable? (I’d prefer immutability and using new contracts for changing Ps)
3. Adding CREATE2 functionality to “force” the recipient to create a smart contract wallet to “claim” the transfer or transfers to EOAs.
4. How does the sender publsih S? (Could be done by the smart contract wallet after executing the token transfer)

The current workflow looks like the following:

1. Sender calls recipients smart contract wallet locally to receive publishableData  and a stealthAddress
2. Sender sends to recipient’s stealth address and publishes publishableData
3. Recipient parses all S and checks if some address contains a token

---

**Nero_eth** (2022-08-16):

> see sample implementation here

**I added a quick PoC using Gnosis Safe Modules [here](https://github.com/Nerolation/EIP-ERC-721-Stealth-Addresses/blob/0f0642eed7e21ef3cae7c0d7a167608e818d02ca/gnosisSafeModule.sol).**

Basically, every compatible smart contract wallet would require to have a public key (of the owner) coded into it (might be upgradeable).

The `privateTransfer` Module (check the link above for Gnosis safe example) would broadcast a `PrivateTransfer` Event containing `publishableData` for every transfer using the `privateETHTransfer` function (the same priciples can then be applied to tokens).

This way, the standard can easily be extended.

Addressing, which contract should eventually publish `S`, it would be best to have it in the token contract itself, which would require extensions to the existing standards and some separat implementation for ETH transfers.

In case, all users use the same module, then the module contract may simply broadcast the Event containing `publishableData` (`S`) - probably together with the asset address interacted with for filtering.

---

**vbuterin** (2022-08-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Addressing, which contract should eventually publish S, it would be best to have it in the token contract itself, which would require extensions to the existing standards and some separat implementation for ETH transfers.

I would say you should just have a contract that issues a log containing the `S` value, with the recipient address as a topic. This makes it easy for the recipient to search, as they can just scan through all logs that have their address as a topic, and it keeps the stealth address mechanism separate from the ERC721 mechanism (as I do think that the stealth address mechanism is a general-purpose tool, which could also be used for ERC20 sends and other applications, there’s no need to tie it to one specific application).

---

**Nero_eth** (2022-08-29):

That’s a good idea! Logging the recipient’s stealth address enables the recipient to compare the indexed topic (stealthRecipient) with the address calculated from the shared secret S to check for ownership.

Consequently, no need to ask the chain if the derived (from S) address possesses an asset.

EDIT: This implementation may require a single immutable contract that can take over the role to exclusively emit `PrivateTransfer` events for every kind of asset transfer. This then allows wallets to subscribe to a single contract instead of every other SM wallet.

This is the current draft :

```auto
pragma solidity ^0.8.6;
...
interface ERC-N {

    /// @notice Public Key coordinates of the wallet owner
    /// @dev Is used by other wallets to generate stealth addresses
    ///  on behalf of the wallet owner.
    bytes publicKey;

    /// @notice Generates a stealth address that can be accessed only by the recipient.
    /// @dev Function is executed locally by the sender on the recipient's wallet to
    ///  generate a stealthAddress and publishableData S. The Caller/Sender must select a secret
    ///  value s and compute the stealth address of the wallet owner and the matching public key S
    ///  to the selected secret s.
    /// @param secret A secret value selected by the sender
    function generateStealthAddress(uint256 secret) returns (bytes publishableData, address stealthAddress)

}

interface PubStealthInfoContract {

    /// @noticeImmutable contract that broadcasts an
    ///  event with the address of the stealthRecipient and
    ///  publishableData S for every privateTransfer.
    /// @dev Emits event with private transfer information S and the recipient's address.
    ///  S is generated by the sender and represents the public key to the secret s.
    ///  The sender broadcasts S for every private transfer. Users can use S to check if they were
    ///  the recipients of a respective transfer by comparing it to stealthRecipient.
    /// @param stealthRecipient The address to send the funds to
    /// @param publishableData The public key to the sender's secret
    event PrivateTransfer(address indexed stealthRecipient, bytes publishableData)
}
```

---

**Nero_eth** (2022-09-03):

**Thanks for all the great input so far!**

I tried to summarize the idea and the current status in a blog post.

You can find it here:

https://medium.com/@toni_w/eip-5564-improving-privacy-on-ethereum-through-stealth-address-wallets-fdf3250e81a1

Please feel free to suggest any feedback!

Find the EIP at the following place:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5566)














####


      `master` ← `nerolation:master`




          opened 01:13PM - 31 Aug 22 UTC



          [![](https://ethresear.ch/uploads/default/original/2X/d/d4f2263996da2d20c2cfa6fa7537c3849f106b12.jpeg)
            nerolation](https://github.com/nerolation)



          [+934
            -0](https://github.com/ethereum/EIPs/pull/5566/files)







Stealth Addresses for Smart Contract Wallets

---

**mds1** (2022-09-04):

Admittedly I only skimmed the above EIP, but wanted to mention that we’ve built [Umbra](https://github.com/ScopeLift/umbra-protocol) which has been live for a little over a year and supports ETH/ERC-20 payments to stealth addresses. We never got around to writing up an EIP, but the current implementation should support NFTs and smart contract wallets without many changes (e.g. the `Umbra` contract would need to be modified since it can only transfer ERC-20 tokens). I’d recommend taking a look at our implementation and using that as a starting point for an EIP since I think it may already cover most or all of your goals.

Our [FAQ](https://app.umbra.cash/faq) contains all the details. There’s a single core [Umbra](https://github.com/ScopeLift/umbra-protocol/blob/efa104c21a0658cfa64ede7bae470fe060927c7f/contracts-core/contracts/Umbra.sol) contract, along with a [StealthKeyRegistry](https://github.com/ScopeLift/umbra-protocol/blob/efa104c21a0658cfa64ede7bae470fe060927c7f/contracts-core/contracts/StealthKeyRegistry.sol) which maps an address to the public key to use when computing a stealth address for that recipient. This can support smart contracts wallets and multisigs by having them publish a public key that at least 1 person on the contract wallet has access to.

We’ve also considered supporting things like [view tags](https://github.com/ScopeLift/umbra-protocol/issues/377) to help reduce scanning time. We don’t have plans to implement it yet since it’d require migrating to a new contract, however adding both view tags and NFT support could be sufficient enough to justify the migration.


*(5 more replies not shown)*
