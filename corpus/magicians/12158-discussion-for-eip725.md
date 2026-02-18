---
source: magicians
topic_id: 12158
title: Discussion for EIP725
author: YamenMerhi
date: "2022-12-15"
category: EIPs
tags: [accounts]
url: https://ethereum-magicians.org/t/discussion-for-eip725/12158
views: 2470
likes: 2
posts_count: 4
---

# Discussion for EIP725

The original discussion of EIP725 is here: [EIP-725 · Issue #725 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/725).

A discussion thread was created here because EIPs now require EIP discussions to occur on Fellowship of Ethereum Magicians and EIP pull requests no longer work without a discussion link that points here.

Discuss EIP725 here.

The standard is here: [EIP-725](https://eips.ethereum.org/EIPS/eip-725)

The main ERC725 reference implementation is in ERC725Alliance Github Repo.

## Replies

**xinbenlv** (2022-12-15):

Glad to see EIP-725 moving forward.

How would 725 authors describe its competitive advantagr with 4337?

---

**YamenMerhi** (2023-01-03):

[@xinbenlv](/u/xinbenlv) I guess the author [@frozeman](/u/frozeman) can answer this question.

But from my point of view, ERC725 is just a generic executor and a generic data-key value store that **can** be used in different forms of vaults, wallets, and accounts that could be AA compatible (4337).

ERC725 by itself is not an account that can compete with 4337 because an account needs much more functionalities than just executing and storing data, (Signature related, token callbacks, etc …).

For example, [LSP0-ERC725Account](https://github.com/lukso-network/LIPs/blob/main/LSPs/LSP-0-ERC725Account.md) uses ERC725 and other different components (ERC1271, LSP1, LSP14, LSP17) that form a blockchain based-account that can support 4337.

On the other side, [LSP7-DigitalAsset](https://github.com/lukso-network/LIPs/blob/main/LSPs/LSP-7-DigitalAsset.md) and LSP8-IdentifiableDigitalAsset, uses ERC725Y to store unlimited meta-data for the token contract and different tokenIds.

So, ERC725 is not restricted to being used or competing with accounts, it can be useful in different types of smart contracts.

---

**frozeman** (2023-01-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yamenmerhi/48/8052_2.png) YamenMerhi:

> can support 4337.

Like Yamen wrote ERC725 X and Y is not a account standard, but could be used as such, as we do in [LSP0-ERC725Account](https://docs.lukso.tech/standards/universal-profile/lsp0-erc725account). [LSP6-KeyManager](https://docs.lukso.tech/standards/universal-profile/lsp6-key-manager) is more comparable to ERC 4337, but it doesnt require any protocol changes. ERC 4337 can also be used in conjunction with LSP6 and LSP0 to make the account abstraction memory pool based, rather the pure transaction relay services. But this would require adding a function into LSP6 to support that (which is fairly easy todo)

