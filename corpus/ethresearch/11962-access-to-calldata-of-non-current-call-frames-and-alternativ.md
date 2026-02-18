---
source: ethresearch
topic_id: 11962
title: Access to CALLDATA of non-current call frames and alternative methods of token-use authorization
author: wdai
date: "2022-02-07"
category: EVM
tags: []
url: https://ethresear.ch/t/access-to-calldata-of-non-current-call-frames-and-alternative-methods-of-token-use-authorization/11962
views: 3179
likes: 3
posts_count: 5
---

# Access to CALLDATA of non-current call frames and alternative methods of token-use authorization

**Background** In ERC20-based DeFi workflows, users interact with application contracts (e.g. Uniswap) that then invoke token contracts (ERC20) to transfer tokens on users’ behalf. Due to the layer of indirection, an additional `approve` call is required.

There are has been numerous proposals to amend and improve upon ERC20, such as ERC223 and ERC677. [ERC677](https://github.com/ethereum/EIPs/issues/677) proposes `transferAndCall`, which changes the workflows of current ERC20-based protocols, in that users would interact with token contracts instead of application contracts. It also complicate workflows that require multiple input tokens (e.g. liquidity pool deposits).

**A better authorization method via access to CALLDATA of non-current call frames.** This thread is an open discussion around an alternative authentication mechanism via `CALLDATA`. The idea originated in the work of [FLAX](https://eprint.iacr.org/2021/1249) in the context of composable privacy for Ethereuem-style DeFi but can be considered independently.

Below is an initial sketch if access to transaction `CALLDATA` is supported.

1. Add opcodes for accessing CALLDATA of the user transaction in EVM, tentatively ORIGIN_CALLDATA{LOAD,SIZE,COPY}, and provide support for it in Solidity via tx.msg.
2. Standardize authorization message format inside tx.msg. The message will authorize one-time use of a user’s token to a contract. For example, each authorization could include the token address, spender contract address, and amount authorized. And each transaction could include multiple authorizations.
3. Token contracts must verify authorizations in tx.msg inside transferFrom(sender, recipient, amount), which amounts to checking that (1) tx.origin == sender, and (2) tx.msg authorizes recipient to spend amount of this-tokens.
4. Generation and parsing of token-use authorization can be built into wallet implementations, alerting users of the side effects of their transactions.

More generally, the mechanism can also be used to support delegation of token use between contracts if CALLDATA of intermediate call frames are accessible via opcodes. In this scenario, the token contract will check, at step 3 above, that the there *exists* a call frame where `caller` is `sender` and the `CALLDATA` of the frame authorizes the spend.

This proposal require changes to the EVM and its surrounding tooling infrastructure. However, it preserves the current ERC20-based contract logic and can also used to support anonymous token standards as proposed in FLAX.

## Replies

**Mikerah** (2022-02-08):

Isn’t `tx.origin` being deprecated?

You would need to find another way to find the originator of the call.

---

**MicahZoltu** (2022-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> Isn’t tx.origin being deprecated?

I have been lobbying for the removal of it because every time it is used for authorization we break compatibility with contract wallets, which is something we want people to be using as it improves their security.  That being said, there isn’t a concrete proposal to remove `tx.origin` at the moment.

---

**fedealconada** (2022-06-13):

Hey [@wdai](/u/wdai)! I found this very interesting. Wanted to share that there’s an EIP which is related to this ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10) Here’s the link to [EIP-3508](https://eips.ethereum.org/EIPS/eip-3508)

---

**alex-ppg** (2022-06-13):

Greetings [@wdai](/u/wdai), I am the author of EIP-3508 (linked above) and [EIP-3520](https://eips.ethereum.org/EIPS/eip-3520) which I believe coincide with what you are trying to achieve here. Let me know if you would like to move them forward collaboratively as they have already been accepted as drafts in the EIP mono-repo and have had some feedback rounds already incorporated, [see discussions here](https://ethereum-magicians.org/t/eip-draft-transaction-data-opcodes/6017).

