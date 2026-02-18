---
source: magicians
topic_id: 24993
title: "ERC-8003: ERC-20 Pre-initialization Extension (Sentinel Storage)"
author: ariutokintumi
date: "2025-08-03"
category: ERCs
tags: [erc-20]
url: https://ethereum-magicians.org/t/erc-8003-erc-20-pre-initialization-extension-sentinel-storage/24993
views: 274
likes: 2
posts_count: 7
---

# ERC-8003: ERC-20 Pre-initialization Extension (Sentinel Storage)

Hello Ethereum Magicians!

I’m excited to open up discussion on a new **optional ERC-20 extension** designed to make gas costs more predictable for ERC-20 users, especially those interacting with new or trending tokens for the first time during periods of high network congestion.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1158)














####


      `master` ← `ariutokintumi:master`




          opened 05:47AM - 10 Aug 25 UTC



          [![](https://avatars.githubusercontent.com/u/8787613?v=4)
            ariutokintumi](https://github.com/ariutokintumi)



          [+147
            -0](https://github.com/ethereum/ERCs/pull/1158/files)







This ERC proposes an **optional ERC-20 extension** that allows token contracts t[…](https://github.com/ethereum/ERCs/pull/1158)o implement a `preInitializeAddress(address)` function. This function lets users or dApps pay the high `SSTORE` gas cost of first-time balance initialization in advance, when gas is low, by writing a sentinel (magic) value to the balance slot.

The balance mapping is stored as `bytes32` internally, and the sentinel is treated as `0` for all ERC-20 reads/writes. When the user later receives tokens, the sentinel is overwritten at the cheaper 5k gas rate instead of the full 20k.

**We use bytes32** because writing zero to a slot does **not** save gas for the first real (nonzero) balance write. EVM only discounts overwrites of already-allocated slots with nonzero value.

This approach mirrors ERC-721A "gas timing" concept but in reverse: **high gas now, low gas later**, giving users more control over when they incur expensive storage writes.

**Discussion thread:** [https://ethereum-magicians.org/t/erc-tbd-erc-20-pre-initialization-extension-sentinel-storage-gas-savings-for-first-time-token-receivers/24993](https://ethereum-magicians.org/t/erc-tbd-erc-20-pre-initialization-extension-sentinel-storage-gas-savings-for-first-time-token-receivers/24993)

**Repository including contracs, testing and tooling:** [https://github.com/ariutokintumi/ERC-20-Pre-initialization](https://github.com/ariutokintumi/ERC-20-Pre-initialization)












### TL;DR

This ERC-20 extension adds a function to **pre-initialize** your balance slot *in advance*, paying the 20k gas “first write” storage cost when gas is cheap. Later, when you actually receive tokens, the cost is only ~5k gas.

The trick: store a unique **sentinel value** (in a `bytes32` mapping) that ERC-20 reads interpret as `0`. First real transfer/mint simply overwrites it. Fully ERC-20 compatible; invisible to wallets, explorers, and integrators.

This is conceptually the reverse of ERC-721A:

- ERC-721A: low gas now / higher gas later (cheap mint, costlier first transfer).
- This EIP: higher gas now / low gas later (pre-pay storage, cheap first receive).

## Background / Motivation

On Ethereum, the first write to a new storage slot costs ~20,000 gas. Setting the slot to `0` early doesn’t help because only a nonzero value marks it as allocated. With this extension, the slot is allocated *without affecting accounting*, letting the user choose when to pay.

While this cost is well understood, it’s become more significant in practice, as users often try to buy into trending tokens right as gas prices spike, resulting in high transaction costs or even failed buys due to underestimated fees.

A common intuition is to “pre-initialize” your token balance slot by setting it to zero early, but (as many have learned) this doesn’t actually help, **the EVM only discounts subsequent writes if the slot has already been set to a nonzero value.**

This is analogous to ERC-721A’s approach of “gas smoothing” but in reverse: instead of low gas now/high gas later (mint/transfer), we enable high gas now/low gas later for ERC-20s, putting the timing choice in the user’s hands.

This ERC offers a safe, fully compatible workaround.

## Proposal

**Key idea:**

Use a `bytes32` mapping for balances, and introduce a contract-wide sentinel (“magic”) value, e.g. `keccak256("preinit")`. A new external function `preInitializeAddress(address user)` lets anyone set their slot to the sentinel (if currently unset).

*All* normal ERC-20 reads/writes (`balanceOf`, `transfer`, etc) continue to interpret the storage value as a `uint256`, treating the sentinel as zero for accounting. When the user later receives tokens, the sentinel is overwritten (at a cheap SSTORE cost), and all functionality is unchanged.

This enables:

- Pre-initializing your address for a token contract when gas is low, making future first buys/claims/transfers much cheaper even if network gas spikes later.
- dApps/wallets to offer this as a service (“optimize my gas for token X”).
- All ERC-20 compatibility and UX preserved, no “phantom” tokens, no risk of broken accounting.

## Specification

ERC-20 contracts implementing this extesion **MUST**:

- Store balances as mapping(address => bytes32).
- Provide a public/external function:

```solidity
/// @notice Pre-initialize an address' balance slot with a sentinel value
/// @param user The address to pre-initialize
function preInitializeAddress(address user) external;
```

- Treat the sentinel as zero in all ERC-20 logic.
- Overwrite sentinel on first real transfer/mint.

## Rationale, code, and live calculator:

- Extension Draft & Rationale
- Reference Implementation (Solidity)
- Conceptual Savings Calculator (live)
- Real Testing Results

## Example Savings

Based on real Sepolia testnet measurements:

- Pre-initialize: 44,221 gas
- First transfer to non-initialized: 52,146 gas
- Transfer to pre-initialized: 35,050 gas

With strategic timing, users can save >30% ETH in high-gas scenarios.

Check this example Pre-initializing with 0.3 gwi and buying the token at 20 gwei using the [Conceptual Savings Calculator (live)](https://erc-20-pre-initialization.tiiny.site/):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9b26c2784bb4dd96a9a5bf449c5c67a4d356b17c_2_690x472.png)image947×648 79 KB](https://ethereum-magicians.org/uploads/default/9b26c2784bb4dd96a9a5bf449c5c67a4d356b17c)

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/85e751830aa19029413afebe349f0034f3a9a78b_2_690x326.png)image910×430 41.8 KB](https://ethereum-magicians.org/uploads/default/85e751830aa19029413afebe349f0034f3a9a78b)

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a7bad68c72c051c1f4e106809ab66d67bf793db5_2_509x500.png)image893×877 108 KB](https://ethereum-magicians.org/uploads/default/a7bad68c72c051c1f4e106809ab66d67bf793db5)

## Use Cases

- Presales, airdrops, major launches: Users prepay SSTORE when gas is low, so when the event starts (and gas spikes), their first buy/claim is much cheaper.
- Pro traders and power users: Batch pre-initialize expected tokens as a cost-saving measure.
- Wallets/bots: Offer “pre-initialize my address” for trending tokens as a value-added feature.

### Relation to ERC-721A and Gas Timing

Some developers may be familiar with ERC-721A (originally from the Azuki team), which reduces minting gas for NFTs by deferring part of the gas cost to the first transfer, effectively betting that “gas will be lower later” (or users prefer to mint cheaply even if transfers are a bit costlier).

**This proposal applies the same philosophy, but in reverse:**

It allows users to optionally “prepay” the storage cost for receiving tokens when gas is low, so their first real transfer (often at a busier time) is much cheaper. Neither approach saves total gas in a fixed-cost world, but both give users more control over *when* they pay expensive storage, helping users and dApps align costs with actual network conditions and their own strategies.

## Compatibility & Security

- 100% ERC-20 interface compatibility (balanceOf always returns uint256).
- The sentinel value is invisible to external callers, never appears as a “phantom” balance.
- No risk of funds loss, overflows, or nonstandard balances.
- Slightly more complex contract logic (all reads/writes check for the sentinel).
- This pattern is opt-in and only affects new contracts.

## Discussion / Feedback Welcome

- Is there a way to further generalize or simplify this pattern?
- Are there other use cases where pre-initialization would provide value?
- Would you consider adopting this in new ERC-20 launches?
- Any security or edge-case scenarios you’d want addressed?

This proposal is not intended as a “must-implement” for all tokens, but as a tool for teams and users who want to minimize gas costs and give power users more options, especially in an era of high volatility and rapid launches.

**Feedback, suggestions, and peer review are very welcome!**

**Thanks for reading!**

- German Maria Abal Bazzano (a.k.a. ariutokintumi)
Contact me @ariutokintumi on X & @llamame on Telegram
Check the full Extension Proposal, code, and tools repo

## Replies

**MASDXI** (2025-08-12):

For me Its about the implementation technique not actually a standard cause not thing changing at interface and behavior is actually same.

What if the balance is back to zero? It’s cold again need re-preintialized?

---

**ariutokintumi** (2025-08-12):

Hello [@MASDXI](/u/masdxi), thanks for taking the time to read and add value here!

> not actually a standard cause not thing changing at interface and behavior is actually same.

Two quick clarifications:

1. There is an interface change. This is proposed as an optional ERC-20 extension that adds a new external function:

```auto
function preInitializeAddress(address user) external;
```

That is why I’m proposing it as a new standard ERC extension (similar to other optional ERC-20 extensions). The storage layout change is internal, the **public interface** adds this method so wallets/dApps can rely on uniform behavior.

1. What if the balance is back to zero? It’s cold again need re-preintialized?
When a holder spends down to zero, the slot is cleared and you get a SSTORE refund (partial costs of the previous write), but after that, the slot is zero again, so the next first non-zero write would be the expensive case. In your words “if you return to zero you’re cold again”,  so yes, you might want to pre-initialize once more later if you expect to receive during a gas spike.

I **did not** auto-write the sentinel when balances hit zero because that would push extra cost onto ordinary transfers and remove the user’s timing choice. Keeping `preInitializeAddress` explicit preserves the idea: *pay now when gas is cheap, save later when it’s expensive*.

Happy to discuss variants and thanks again for the question!

---

**MASDXI** (2025-08-12):

Instead of re-initializing, you can use a magic number (like uint256.max) to act as a “virtual zero.” This way, the balance storage slot stays warm, which slightly increases gas usage for balance validation during each transfer, but is still cheaper than going from cold to warm storage. Most people don’t realize that always keeping 1 wei (or the smallest ERC-20 unit) in an account can save gas.

Or your as put 1 token as warm flag, balanceOf MUST exclude that token from the usable balance i think it more simple and affective

---

**ariutokintumi** (2025-08-12):

[@MASDXI](/u/masdxi) thanks again for sharing your thoughts.

In the ERC draft I take in consideration this points and here is the explanation of why I didn’t choose to use that approaches,

### Why Not Use Other Approaches?

- Transfer(0) or balance=0: Does not allocate the slot; first nonzero write still costs 20,000 gas.
- Dummy balance (e.g. 1 token): Breaks accounting, is unsafe, and not compliant.
- Negative or non-numeric: Not possible in uint256, and not safe in mapping types.

**Sentinel bytes32 value** is the only way to safely allocate the storage slot with zero external effects.

Also I have extended the warnings on using numeeric representations in the Security section:

## Security Considerations

- No risk of funds loss: pre-initialization cannot set balances to nonzero token values or affect accounting.
- The sentinel is never visible or accessible externally. ERC-20 APIs always interpret it as zero.
- Minimal “storage bloat” risk; a slot with sentinel is no worse than a slot initialized via normal transfers.

Thanks again for contributing and please keep posting your ideas to improve it.

---

**xinbenlv** (2025-10-28):

Can you verify the ERC20 token will be able to execute the following transactions

1. Mint to Address of Alice 2 token
2. Preinitialize Address of Bob
3. Alice ERC20.transfer 2 to Bob
4. Bob attempt to ERC20.transfer to 3 to Charlie

Supposedly Step 4 will fail. Can you run these 4 step in your Reference Implementation deployment and show the failure

---

**ariutokintumi** (2025-10-28):

Hello [@xinbenlv](/u/xinbenlv), thaks for your request and taking time to review the proposal.

Here is the test results, direcly made at the contract using Etherscan ([Address: 0x259e1396...1bba5be27 | Etherscan Sepolia](https://sepolia.etherscan.io/address/0x259e139612ab2e6a3c7525585af724a1bba5be27#writeContract)).

For the testing I’m using new addresses without previous interaction with the ERC-8003 implementation.

Alice address: 0x3Ede56f008d7612039617f7dc0e1EAd433CF280E

Bob address: 0xe2743a467309AFEE2E28f728e2876250751c55af

Charlie address: 0x5e994dBBAACaF1c6Dd6246Cd3BD7DAc0C5E23716

**1º Mint to Address of Alice 2 token:** (success as expected) ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15)


      ![](https://sepolia.etherscan.io/images/favicon3.ico)

      [Ethereum (ETH) Blockchain Explorer](https://sepolia.etherscan.io/tx/0xa0ca571e22b73013ca1821548abe87583dd56cbd71d0ad6a2f7949113691dc03)



    ![](https://etherscan.io/images/brandassets/og-preview-sm.jpg)

###



Transfer 0 PINIT to 0x3Ede56f0...433CF280E | Success | Oct-28-2025 04:37:00 PM (UTC)










Alice has received 2 minted tokens and has the balance:

[![image](https://ethereum-magicians.org/uploads/default/original/3X/7/4/742c9868cd2b6c1d066156cb1507832f9d884e7b.png)image338×252 11.2 KB](https://ethereum-magicians.org/uploads/default/742c9868cd2b6c1d066156cb1507832f9d884e7b)

**2º Preinitialize Address of Bob** (success as expected) ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15)


      ![](https://sepolia.etherscan.io/images/favicon3.ico)

      [Ethereum (ETH) Blockchain Explorer](https://sepolia.etherscan.io/tx/0x096549bdd016b171284b47aa982a38a1c847bef0b0978457a234ed4e68feb270)



    ![](https://etherscan.io/images/brandassets/og-preview-sm.jpg)

###



Call Pre Initialize Address Function By 0xe2743a46...0751c55af on 0x259E1396...1bba5Be27 | Success | Oct-28-2025 04:41:36 PM (UTC)










Bob Is preinitialized (numeric balance remainis 0):

[![image](https://ethereum-magicians.org/uploads/default/original/3X/5/5/55e3858af7a6f06c804820cc2c7aae91e0ba531f.png)image383×242 11 KB](https://ethereum-magicians.org/uploads/default/55e3858af7a6f06c804820cc2c7aae91e0ba531f)

**3º Alice ERC20.transfer 2 to Bob** (success as expected) ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15)


      ![](https://sepolia.etherscan.io/images/favicon3.ico)

      [Ethereum (ETH) Blockchain Explorer](https://sepolia.etherscan.io/tx/0x134d5f1c5c865b9d305259efbf572a91a49644595d75cdeaa8aeaf6746dfe08c)



    ![](https://etherscan.io/images/brandassets/og-preview-sm.jpg)

###



Transfer 0 PINIT to 0xe2743a46...0751c55af | Success | Oct-28-2025 04:45:00 PM (UTC)










Alice balance went to 0:

[![image](https://ethereum-magicians.org/uploads/default/original/3X/3/e/3ecf40287cb4b3e59aaf9cc468933c811074cd6d.png)image343×238 11.1 KB](https://ethereum-magicians.org/uploads/default/3ecf40287cb4b3e59aaf9cc468933c811074cd6d)

Bob balance is now 2:

[![image](https://ethereum-magicians.org/uploads/default/original/3X/d/b/dbe5d81691d8422dc4bd6af0c5350f563f183ef8.png)image358×259 11.2 KB](https://ethereum-magicians.org/uploads/default/dbe5d81691d8422dc4bd6af0c5350f563f183ef8)

**4º Bob attempt to ERC20.transfer to 3 to Charlie** (failed as expected) ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15)


      ![](https://sepolia.etherscan.io/images/favicon3.ico)

      [Ethereum (ETH) Blockchain Explorer](https://sepolia.etherscan.io/tx/0xb870a52215541fa251fd300c1fca42c7ea1278757d1d4d360da6a9cd2a2c766c)



    ![](https://etherscan.io/images/brandassets/og-preview-sm.jpg)

###



Call Transfer Function By 0xe2743a46...0751c55af on 0x259E1396...1bba5Be27 | Fail With Error 'Insufficient' | Oct-28-2025 04:51:36 PM (UTC)










Bob to Charlie transfer 3 tokens etherscan output:

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/2/3/23055a67fd41e29f203f1fda3bad07d7e970bccb_2_690x162.png)image1341×316 37.5 KB](https://ethereum-magicians.org/uploads/default/23055a67fd41e29f203f1fda3bad07d7e970bccb)

Bob balance remains 2:

[![image](https://ethereum-magicians.org/uploads/default/original/3X/7/a/7a9bc79414e60b3a8a6636eb223a1beeea39a630.png)image365×241 11.1 KB](https://ethereum-magicians.org/uploads/default/7a9bc79414e60b3a8a6636eb223a1beeea39a630)

Charlie balance remains 0:

[![image](https://ethereum-magicians.org/uploads/default/original/3X/4/a/4ad25d66e0ddc4ea08ecf1b8e55b5b50ecd9c330.png)image369×245 11.5 KB](https://ethereum-magicians.org/uploads/default/4ad25d66e0ddc4ea08ecf1b8e55b5b50ecd9c330)

**Extra Bob attempt to ERC20.transfer to 2 to Charlie** (success as expected) ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15)


      ![](https://sepolia.etherscan.io/images/favicon3.ico)

      [Ethereum (ETH) Blockchain Explorer](https://sepolia.etherscan.io/tx/0x04f73af93633102f0a3bc4bfe8c71a945796bfda26c4eff07f2749514321e5e2)



    ![](https://etherscan.io/images/brandassets/og-preview-sm.jpg)

###



Transfer 0 PINIT to 0x5e994dBB...0C5E23716 | Success | Oct-28-2025 04:56:12 PM (UTC)










Bob balance is now 0:

[![image](https://ethereum-magicians.org/uploads/default/original/3X/4/0/40975160377440a3fe45c785059735e997ba88da.png)image323×246 10.7 KB](https://ethereum-magicians.org/uploads/default/40975160377440a3fe45c785059735e997ba88da)

Charlie balance is now 2:

[![image](https://ethereum-magicians.org/uploads/default/original/3X/d/f/df093da5e145b237bee113dffa04f20341bd7ed0.png)image348×250 11.5 KB](https://ethereum-magicians.org/uploads/default/df093da5e145b237bee113dffa04f20341bd7ed0)

I hope this clarifies the question and looking forward for more comments to move forward.

