---
source: magicians
topic_id: 23013
title: wallet_addSubAccount
author: wilsoncusack
date: "2025-02-27"
category: ERCs
tags: [wallet]
url: https://ethereum-magicians.org/t/wallet-addsubaccount/23013
views: 210
likes: 3
posts_count: 2
---

# wallet_addSubAccount

This ERC introduces a new wallet RPC, wallet_addSubAccount, which allows an app to request a wallet to track a smart account that the wallet owns. It also allows apps to request the wallet to provision a new account, owned by the universal wallet with a signer provided by the caller.

Embedded app accounts (onchain accounts specific to a single app) have led to a proliferation of user addresses, which can be difficult for users to keep track of. Many embedded app account users also have a universal wallet, which can be used across apps. With hierarchical ownership–where one smart account can own another–if the embedded app account is a smart account, it could be owned by the user’s universal wallet. This would allow users to be able to control an app account via their universal wallet. However, though hierarchical ownership is already possible today, there is no way for apps to tell universal wallets about embedded app accounts a user may have. The proposed RPC provides a path for this.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/932)














####


      `master` ← `jakeFeldman:hierarchical-accounts-api`




          opened 07:38PM - 27 Feb 25 UTC



          [![](https://avatars.githubusercontent.com/u/25087876?v=4)
            jakeFeldman](https://github.com/jakeFeldman)



          [+230
            -0](https://github.com/ethereum/ERCs/pull/932/files)







This ERC introduces a new wallet RPC, wallet_addSubAccount, which allows an app […](https://github.com/ethereum/ERCs/pull/932)to request a wallet to track a smart account that the wallet owns. It also allows apps to request the wallet to provision a new account, owned by the universal wallet with a signer provided by the caller.

## Replies

**dror** (2025-06-03):

it is unclear to me who own the keys.

from the text, it seems that the caller (the app) is the owner of the keys.

this gives a lot of power to the app - but also adds a threat vector: an account was added into the wallet, and the user might feel this sub-account is as safe as its own… however, the keys of this account are the app’s keys.

missing are security considerations, on how to mitigate this security risk

- limit the sub-accounts to specific app
- warning the user about the safety of such account (namely: if a user moves funds into this sub-account, it is equivalent to sending them to the app-specific contract: good as long as you fully trust the app. The fact it is called “sub-account” of the user and managed through the wallet doesn’t bring it extra security compared to dApp-owned service holding those funds.

