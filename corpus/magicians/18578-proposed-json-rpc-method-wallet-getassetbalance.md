---
source: magicians
topic_id: 18578
title: "Proposed JSON-RPC method: wallet_getAssetBalance"
author: wilsoncusack
date: "2024-02-09"
category: EIPs > EIPs interfaces
tags: [wallet, json-rpc, intents]
url: https://ethereum-magicians.org/t/proposed-json-rpc-method-wallet-getassetbalance/18578
views: 1874
likes: 15
posts_count: 8
---

# Proposed JSON-RPC method: wallet_getAssetBalance

With intents, multi-chain transactions, and other tools, accounts will increasingly be making use of “just in time” funding when transacting. Apps can no longer rely on calls like `address.balance` or `erc20.balanceOf` to know an account’s spending power.

I propose a new wallet RPC to help, something like `wallet_getAssetBalance(account_address, chainId, asset_address)`.

Very open to feedback. Want to start a conversation. One question I have: should this RPC try to make use of some more universal asset identifier? Or, because most apps care about a specific asset on a specific chain, chain + address is sufficient.

## Replies

**kristofgazso** (2024-02-09):

Feel like this could be a good fit as a [CAIP-25](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-25.md) extension actually.

When it comes to a universal asset identifier, I imagine it might be a bit overkill and could be implemented by the wallet at the library level. Especially with quirks like some tokens having a different amount of decimals on different chains, bridged → native token migrations, etc.

Or how were you imagining it?

---

**wilsoncusack** (2024-02-09):

hmm how do you think as a CAIP-25 extension? Would be part of handshake? Seems like a lot to ask about all possible asset balances. E.g. imagine connecting to Uniswap.

Re universal identifier, maybe the field is just 32 bytes long so that people have some space for extra info. E.g. in the ERC1155 case, you would want to pass both the asset address and the token id.

---

**kristofgazso** (2024-02-10):

Oh no a CAIP extension would not require all the balances to be given at once, it would just mean that the dapp would check during the handshake whether the wallet supports wallet_getAssetBalance (and the wallet would confirm or deny), and the dapp would use that method if supported, otherwise fall back to erc20 getBalance

---

**wilsoncusack** (2024-02-17):

Ah yeah, that’s a good idea.

Also wondering if we could just add a method to viem/wagmi that optimistically tries this Wallet RPC, and falls back to a normal balance change.

Also thinking more about the asset identifier maybe

```auto
{
  type: bytes12 // "ERC20" | "ERC1155" | "..."
  address: Address
}
```

or we could pull chainId into the asset identifier as well

```auto
{
  chainId: uint24
  type: bytes9 // "ERC20" | "ERC1155" | "..."
  address: Address
}
```

Bytes9 might be too constraining for type. Fitting this all into bytes32 is somewhat of an ar

---

**bumblefudge** (2024-02-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kristofgazso/48/3640_2.png) kristofgazso:

> the dapp would check during the handshake whether the wallet supports wallet_getAssetBalance (and the wallet would confirm or deny), and the dapp would use that method if supported, otherwise fall back to erc20 getBalance

the way this is done in today’s CAIP-25 (no new extensions needed) is that a dapp would request an RPC method like `wallet_getAssetBalance` and, (if both wallet and dapp both support the “custom RPC endpoints”), a stable URL where that RPC is defined (i.e., if there is an OpenRPC API dictionary published somewhere that wallet and dapp can defer to for the canonical definition of that API; could be the URL of an EIP, for example).

---

**tomarsachin2271** (2024-06-03):

Just like Uniswap has [token list](https://tokenlists.org/), similarly as asset list could be maintained for other types of assets as well.

You mentioned ‘just in time’ funding of accounts. Can you give an example of this? Like how would this rpc will return a different result as compared to erc20.balanceOf() ?

---

**MUHAMMADIHSANALIKAP** (2024-08-27):

Sir, I really agree with you. Appreciate your efforts.

