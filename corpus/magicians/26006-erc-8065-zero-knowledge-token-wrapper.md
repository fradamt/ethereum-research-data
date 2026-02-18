---
source: magicians
topic_id: 26006
title: "ERC‑8065: Zero Knowledge Token Wrapper"
author: doublespending
date: "2025-10-28"
category: ERCs
tags: [erc, erc-721, erc-20, zkp, erc-1155]
url: https://ethereum-magicians.org/t/erc-8065-zero-knowledge-token-wrapper/26006
views: 897
likes: 41
posts_count: 41
---

# ERC‑8065: Zero Knowledge Token Wrapper

> ZWToken - Make privacy a native feature of all tokens on Ethereum

> NOTE:
>
>
> ERC-8065 has been accepted as a draft ERC: ERC-8065: Zero Knowledge Token Wrapper
> PoC is available at zk.walletaa.com with the github repository.

This ERC defines a standard for the Zero Knowledge Token Wrapper, a wrapper that adds privacy to tokens — including ERC-20, ERC-721, ERC-1155 and ERC-6909 — while preserving all of the tokens’ original properties, such as transferability, tradability, and composability. It specifies EIP-7503-style provable burn-and-remint flows, enabling users to break on-chain traceability and making privacy a native feature of all tokens on Ethereum.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1322)














####


      `master` ← `0xNullLabs:erc-draft-zero-knowledge-token-wrapper`




          opened 04:43PM - 28 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/33960178?v=4)
            doublespending](https://github.com/doublespending)



          [+772
            -0](https://github.com/ethereum/ERCs/pull/1322/files)







This ERC defines a standard for the Zero Knowledge Token Wrapper, a wrapper that[…](https://github.com/ethereum/ERCs/pull/1322) adds privacy to tokens — including ERC-20, ERC-721, and ERC-1155 — while preserving all of the tokens’ original properties, such as transferability, tradability, and composability. It specifies [EIP-7503](https://eips.ethereum.org/EIPS/eip-7503)-style provable burn-and-remint flows, enabling users to break on-chain traceability and making privacy a native feature of all tokens on Ethereum.

NOTE: PoC is available at [zk.walletaa.com](https://zk.walletaa.com/) with the [github repository](https://github.com/0xNullLabs/ZWToken)












## Motivation

Most existing tokens lack native privacy due to regulatory, technical, and issuer-side neglect. Users seeking privacy must rely on dedicated privacy blockchains or privacy-focused dApps, which restrict token usability, reduce composability, limit supported token types, impose whitelists, and constrain privacy schemes.

This ERC takes a different approach by introducing a zero knowledge token wrapper that preserves the underlying token’s properties while adding privacy. Its primary goals are:

- Pluggable privacy: the wrapper preserves all properties of the underlying token while adding privacy.
- Permissionless privacy: any user can wrap any token into a Zero Knowledge Wrapper Token (ZWToken).
- Broad token support: compatible with both fungible tokens (e.g., ETH, ERC-20) and non-fungible tokens (e.g., ERC-721).
- EIP-7503-style privacy: supports provable burn-and-remint flows to achieve high-level privacy.
- Compatibility with multiple EIP-7503 schemes: supports different provable burn address generation methods and commitment schemes (e.g., Ethereum-native MPT state tree or contract-managed commitments).

## Q & A

### 1. Why not New zkERC20

- Hard to gain liquidity and users

Users would rather have a non-private USDC than a niche zkERC20 that only offers privacy.

Major token issuers unlikely to issue due to regulatory constraints

### 2. Why EIP-7503

- Only requires transferability
- Indistinguishable burn

### 3. Why not EIP-7503

- Hard Fork
- Only support ETH
- Unmeasurable ETH supply

## Specification

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Overview

A Zero Knowledge Wrapper Token (ZWToken) is a wrapper token that adds a commitment-based privacy layer to existing tokens, including ERC-20, ERC-721, and ERC-1155. This privacy layer allows private transfers without modifying the underlying token standard, while preserving full composability with existing Ethereum infrastructure.

The commitment mechanism underlying this privacy layer may be implemented using Merkle trees, cryptographic accumulators, or any other verifiable cryptographic structure.

A Zero Knowledge Wrapper Token (ZWToken) provides the following core functionalities:

The ZWToken recipient can be a provable burn address, from which the tokens can later be reminted.

- Deposit: Wraps an existing token and mints the corresponding amount of ZWToken to the specified recipient.
- Transfer: Transfers ZWToken to the specified recipient.
- Remint: Mints new ZWTokens to the specified recipient after verifying a zero-knowledge proof demonstrating ownership of previously burnt tokens, without revealing the link between them.
- Withdraw: Burns ZWTokens to redeem the equivalent amount of the underlying tokens to the specified recipient.

#### Privacy Features by Token Type

For fungible tokens (FTs), e.g., ERC-20:

- This ERC enables breaking the traceability of fund flows through the burn and remint processes.
- The use of provable burn addresses hides the true holder of fungible tokens until the holder performs a withdraw operation of ZWToken.

For non-fungible tokens (NFTs), e.g., ERC-721:

- This ERC cannot break the traceability of fund flows through burn and remint, since each NFT is unique and cannot participate in coin-mixing.
- However, the use of provable burn addresses can still conceal the true holder of the NFT until the holder performs a withdraw operation of ZWToken.

#### ZWToken-aware Workflow

In the ZWToken-aware workflow, both the user and the system explicitly recognize and interact with ZWToken. ZWToken inherits all functional properties of the underlying token.

[![flow1](https://ethereum-magicians.org/uploads/default/optimized/3X/2/0/20d7c825bc7a83aa2240634f7a7a84f45083266e_2_506x499.png)flow11758×1736 146 KB](https://ethereum-magicians.org/uploads/default/20d7c825bc7a83aa2240634f7a7a84f45083266e)

For example, if the underlying token is ERC-20, ZWToken can be traded on DEXs, used for swaps, liquidity provision, or standard transfers. Similar to how holding WETH provides additional benefits over holding ETH directly, users may prefer to hold ZWToken rather than the underlying token.

#### ZWToken-unaware Workflow

This ERC also supports a ZWToken-unaware workflow. In this mode, all transfers are internally handled through ZWToken, but users remain unaware of its existence.

[![flow2](https://ethereum-magicians.org/uploads/default/optimized/3X/f/7/f7c2867110164b034c12c66686313f37fabd8b23_2_685x500.png)flow21792×1308 114 KB](https://ethereum-magicians.org/uploads/default/f7c2867110164b034c12c66686313f37fabd8b23)

ZWToken functions transparently beneath the user interface, reducing the number of required contract interactions and improving overall user experience for those who prefer not to hold ZWToken directly.

#### Alternative Workflows

The two workflows described above represent only a subset of the interaction patterns supported by this ERC. Additional workflows are also possible, including:

- Reminting by the recipient:
Alice may transfer (in the ZWToken-aware workflow) or depositTo (in the ZWToken-unaware workflow) ZWToken to Bob’s provable burn address instead of her own. In this case, the remint operation is initiated and proven by Bob rather than Alice.
- Recursive reminting:
A reminted ZWToken may also be sent to another provable burn address controlled by Bob instead of his public address, allowing the privacy state to persist across multiple remint cycles.

The interface:

```solidity
interface IERC8065 {
    struct RemintData {
        bytes32 commitment;
        bytes32[] nullifiers;
        bytes proverData;
        bytes relayerData;
        bool redeem;
        bytes proof;
    }

    // Optional
    event CommitmentUpdated(uint256 indexed id, bytes32 indexed commitment, address indexed to, uint256 amount);

    event Deposited(address indexed from, address indexed to, uint256 indexed id, uint256 amount);

    event Withdrawn(address indexed from, address indexed to, uint256 indexed id, uint256 amount);

    event Reminted(address indexed from, address indexed to, uint256 indexed id, uint256 amount, bool redeem);

    function deposit(address to, uint256 id, uint256 amount, bytes calldata data) external payable;

    function withdraw(address to, uint256 id, uint256 amount, bytes calldata data) external;

    function remint(
        address to,
        uint256 id,
        uint256 amount,
        RemintData calldata data
    ) external;

    // Optional
    function previewDeposit(address to, uint256 id, uint256 amount, bytes calldata data) external view returns (uint256);

    // Optional
    function previewWithdraw(address to, uint256 id, uint256 amount, bytes calldata data) external view returns (uint256);

    // Optional
    function previewRemint(address to, uint256 id, uint256 amount, RemintData calldata data) external view returns (uint256);

    function getLatestCommitment(uint256 id) external view returns (bytes32);

    function hasCommitment(uint256 id, bytes32 commitment) external view returns (bool);

    // Optional
    function getCommitLeafCount(uint256 id) external view returns (uint256);

    // Optional
    function getCommitLeaves(uint256 id, uint256 startIndex, uint256 length)
    external view returns (bytes32[] memory commitHashes, address[] memory recipients, uint256[] memory amounts);

    function getUnderlying() external view returns (address);
}
```

## Replies

**Miaomi** (2025-10-29):

This means that we can transform any token (USDT, USDC, anything you want) to a private pool.

WITHOUT anyone’s permission!

---

**doublespending** (2025-10-29):

Yeah, ERC-8065 is designed to work with all asset types — fungible (ETH, ERC-20), semi-fungible (ERC-1155, ERC-6909), and non-fungible (ERC-721).

For NFTs, you obviously can’t have a “privacy pool” since each token is unique, but ERC-8065 can still hide the real owner by decoupling ownership from the on-chain address.

---

**0xZPL** (2025-10-30):

Yes. It is permission-less.

For example, we can transform USDC into ZKUSDC, DAI into ZKDAI.

Even if some tokens (USDT) block the pool address, then another pool can be created. If more and more wallets support the pool, it will  be less possibility to be blocked.

---

**stateroot** (2025-10-31):

It looks like each underlying token currently needs its own Zero Knowledge Token Wrapper contract, which feels a bit limited in terms of scalability — you’d have to deploy a new contract and possibly handle different proof generation logic every time.

Would it make sense to leverage something like **ERC-6909** so that a single contract can manage all possible ZWToken combinations instead?

---

**Zach** (2025-10-31):

Absolutely. I am not sure if this is the most optimized way, but absolutely love this. It gives more freedom to old tokens to become private. Yes.

---

**doublespending** (2025-10-31):

We hope the Zero Knowledge Wrapper Token maintains the same characteristics as its underlying token to make integration easier for applications. For example, since USDC is an ERC-20 token, we’d prefer ZWUSDC to also follow ERC-20 rather than ERC-6909.

---

**nuno** (2025-11-02):

Hi, I’ve been developing my own implementation inspired by zk-wormhole, called zERC20. Both the implementation and the proof of concept are now complete.

In zERC20, I’ve built upon the zk-wormhole mechanism and added the following features:

- Batch withdrawals supported by Nova IVC
- On-chain Merkle tree optimization by offloading the Merkle tree computation to off-chain using Nova IVC for improved gas efficiency
- Anonymous cross-chain transfers

HackMD: [zERC20: A Private Token Based on zk-Wormholes - HackMD](https://hackmd.io/zYixSwg2Rtqoz2UpMqVY_w)

GitHub: [GitHub - kbizikav/zERC20](https://github.com/kbizikav/zERC20)

Demo: https://zerc20-demo.vercel.app/

---

**doublespending** (2025-11-02):

Yeah, great work. You’re welcome to build together! I think issuing our own zkERC20 would struggle to gain liquidity and users. Besides, major token issuers are unlikely to issue zkERC20s themselves due to regulatory and other constraints. That’s why a permissionless wrapper could be a practical path toward **making privacy a native feature of all tokens on Ethereum** .

---

**stateroot** (2025-11-02):

Also, does this kind of ERC support *any* type of token? Are there specific tokens that require special handling or extra attention?

---

**doublespending** (2025-11-04):

In theory, any token with a transfer function can be supported, so ERC-8065 does **not** work with non-transferable tokens such as **Soulbound Tokens (SBTs)**. However, there are certain types of tokens that require extra care when implementing the wrapper:

1. Fee-on-Transfer Tokens
2. Rebasing Tokens

BTW, you can avoid the complexity of handling rebasing logic by wrapping the **wrapper** of a rebasing token instead.

---

**ZyraV21** (2025-11-04):

Great work on ERC-8065! This is exactly the kind of permissionless privacy infrastructure Ethereum needs. I’ve been developing a similar concept for several months now, and I’d love to share insights and compare approaches.

I built zkETH on Starknet L2 - a privacy-preserving ETH wrapper that shares your core vision but takes a different technical path optimized for L2 economics and STARK proofs.

## Demo & Code

- Live Demo (Testnet): I can’t publish links since my account is new, created it just to post here.
- GitHub: Private by now, will publish if asked.
- Deployed Contract (Sepolia): 0x079a77a7d82ecb78092deeae6ce971f2499e1cd95cd1121672851f7eccc50108

## Philosophy Alignment

zkETH shares ERC-8065’s fundamental principle: making privacy a native feature of existing tokens without requiring issuer cooperation. Like you said, major token issuers won’t create private versions due to regulatory constraints, so permissionless wrappers are the practical path forward.

## L2 Economics: Practical Privacy

One significant advantage of building on Starknet L2 is the dramatically reduced transaction costs compared to Ethereum L1. While I won’t claim specific numbers (as they fluctuate with gas prices), the cost difference is substantial enough to make privacy viable for everyday transactions, not just large transfers.

On Ethereum L1, complex ZK proof verification can be prohibitively expensive for average users. On Starknet, the same operations are economically feasible for much smaller amounts, making privacy truly accessible.

### Key Architectural Differences

| Aspect | ERC-8065 | zkETH |
| --- | --- | --- |
| Proof System | Generic ZK | STWO Circle STARKs |
| Privacy Model | Burn-and-remint (EIP-7503) | UTXO-style private notes |
| Token Support | Multi-token (ERC-20/721/1155) | ETH-only (specialized) |
| Blockchain | Ethereum L1 | Starknet L2 |
| Amount Privacy | Partial (remint reveals amount) | Full (range proofs + commitments) |

Both projects prove that **privacy doesn’t require permission from token issuers, regulators, or centralized entities**. By building permissionless wrappers, we’re democratizing financial privacy and making it a user choice rather than an institutional decision.

The future of DeFi privacy is multi-chain: different privacy layers optimized for different use cases, all interoperable and user-controlled.

Would love to connect and explore synergies between ERC-8065 and zkETH. Feel free to reach out or ask whatever you need.

Regards, Zyra

---

**ZyraV21** (2025-11-04):

PoC txs (see on starknet blockexplorer, testnet)

Deposit Eth: 0x6ab8fb0c7a5acb9447d21e92c379495ecfa6d93af44cc950939fc8279bb3cbb

Shield Tokens: 0x184c94da5717a14f92b66e51aba6364b0136382eab97d2cbd8a98b5513ca18e

Transfer Private note: 0xfe1aa3d4091cc2a30a74919b2e0e953379a45cf94000df121a150a40a27724

Burn Private note:

0x20080dc0408c547fb4825d74bfcfedda4d40455cab12f07a184ecd63fbcdc13

Unshield: 0x77f0893392947db9432b5f39d7d850f4c4631d3b19dd2cd303b01575d8f19ea

---

**doublespending** (2025-11-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zyrav21/48/16390_2.png) ZyraV21:

> Both projects prove that privacy doesn’t require permission from token issuers, regulators, or centralized entities. By building permissionless wrappers, we’re democratizing financial privacy and making it a user choice rather than an institutional decision.
>
>
> The

Great work! You’re very welcome to build together. We can discuss whether the ERC-8065 interface could be made compatible with your work.

---

**ZyraV21** (2025-11-05):

Thanks for your feedback!!! It really means A LOT for me. It’s been a lot of months doing R&D on my own… glad to see its alive finally! :')))))))))

---

**doublespending** (2025-11-06):

I’ve created a new Telegram group for anyone who wants to discuss things more frequently.

---

**Miaomi** (2025-11-09):

Moreover, I wonder that  whether the DEXes or aggregators will support this wrapped token. and why.

---

**doublespending** (2025-11-10):

That’s actually one of the key benefits of a **token wrapper** — it’s *not* a new token that requires new liquidity. It enables seamless two-way conversion between the **ZWToken** and its **underlying token** at any time.

For DEXes or aggregators:

a. If the **input** is a ZWToken, they can simply call withdraw on the input to get the underlying token (just like converting **WETH → ETH**).

b. If the **output** is a ZWToken, they just need to deposit the underlying token to mint the corresponding ZWToken (just like converting **ETH → WETH**).

There’s also a really interesting use case: if you want to **buy a token without revealing your address**, you can ask the DEX or aggregator to send the **output ZWToken** directly to your **provable burn address**.

---

**ten-io-meta** (2025-11-11):

ZWToken formalizes privacy at the token layer, solving a key missing component in Ethereum: unlinkability without losing composability. There is also an unexplored complementary axis: irreversible, non-remintable burn mechanics with deterministic supply constraints and economic tension, where privacy could operate on top without reintroducing remint of the same supply. Both directions are orthogonal and composable, and together point toward a new category of non-traceable but supply-bounded token primitives

---

**zero** (2025-11-17):

Great proposal — glad to see more conversations around making ERC20 assets privacy-capable.

Our team has been building privacy infrastructure on Base for several months, and we’ve actually fully implemented and deployed a wrapping-based privacy system similar to what’s being proposed here.

(ZeroLayer is currently live on Base Sepolia and supports wrapping ETH and any ERC20 into private assets.)

After building, deploying, and testing this model, we found several important insights that may be useful for this discussion:

1. Wrap-based privacy works, but creates real UX fragmentation

Users end up managing two representations of the same token:

public ERC20

private wrapped version

Even with a smooth UI, users often get confused about:

“Which balance do I actually have?”

“Where is my real supply stored?”

This creates friction for adoption.

1. Supply is still “split” between two contracts

Even with correct supply invariants, the model inherently creates:

ERC20 public supply

wrapped private supply

This complicates accounting and increases the surface for implementation mistakes.

1. DeFi composability becomes indirect

The wrapped form cannot be used directly inside DeFi unless integrations explicitly add support for it.

This pushes additional work to every DeFi protocol instead of giving them a unified standard.

1. These issues eventually motivated us to explore a unified (“dual-mode”) token model

After deploying the wrap approach and observing user feedback, we came to the conclusion that privacy should ideally live inside the token standard itself, not as a wrapper contract.

This led us to draft a proposal for a Dual-Mode Fungible Token, where a single token natively supports:

a public mode (ERC20)

a private mode (ZK commitments)

seamless switching between the two

consistent total supply tracking

Our draft is here for anyone interested in the comparison:



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/z/a88e57/48.png)

      [ERC-8085: Dual-Mode Fungible Tokens](https://ethereum-magicians.org/t/draft-dual-mode-token-standard-single-token-with-public-and-private-modes/26592) [ERCs](/c/ercs/57)




> Discussion topic for ERC-8085:
>
>
>
> Abstract
> This EIP defines an interface for fungible tokens that operate in two modes: transparent mode (fully compatible with ERC-20) and privacy mode (using ERC-8086 privacy primitives). Token holders can convert balances between modes. The transparent mode uses account-based balances, while the privacy mode uses the standardized IZRC20 interface from ERC-8086. Total supply is maintained as the sum of both modes.
> Motivation
> The Privacy Dilemma for New Token P…

1. Wrap-based privacy and dual-mode privacy can coexist

I believe the wrap model is extremely valuable especially for existing tokens that cannot upgrade.

Dual-mode tokens, on the other hand, benefit new tokens that can launch with native privacy built-in.

Both approaches are valid and useful, depending on the context.

Just wanted to share our practical learnings from having a live wrap-privacy implementation — hope this helps the discussion move forward.

Happy to collaborate or share deeper technical details if helpful.

---

**doublespending** (2025-11-17):

Thanks for your interest in ERC-8605 — I’m also excited about the recent surge of related work, including this thread (which is quite similar to what you’re doing): [zERC20 : Cross-Chain Private ERC-20 Based on ZK Proof-of-Burn](https://ethereum-magicians.org/t/zerc20-cross-chain-private-erc-20-based-on-zk-proof-of-burn/26452)

Regarding the UX concerns introduced by wrappers, I think the ZWToken-unaware workflow can significantly improve the situation. Users don’t necessarily need to be aware that a wrapper exists at all.

I still believe that even if new tokens are issued, wrappers remain the only viable path. Asset issuers generally prefer to avoid regulatory exposure (which is essential for the survival of their projects), so privacy inevitably has to be handled by a permissionless wrapper — even if that means we’ll need some additional UX improvements.


*(20 more replies not shown)*
