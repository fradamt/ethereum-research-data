---
source: magicians
topic_id: 21639
title: "ERC-7811: Wallet Asset Discovery"
author: lukaisailovic
date: "2024-11-09"
category: ERCs
tags: [erc, evm, wallet]
url: https://ethereum-magicians.org/t/erc-7811-wallet-asset-discovery/21639
views: 981
likes: 10
posts_count: 16
---

# ERC-7811: Wallet Asset Discovery

JSON-RPC method for wallets to share a user’s complete asset list with Dapps, including assets not easily discoverable through on-chain information alone.

https://github.com/ethereum/ERCs/pull/709

## Replies

**SamWilsn** (2024-12-09):

> requiredAssets is an optional field that specifies only the assets Dapp cares about on the specific chains. If it is provided, the response from the wallet SHOULD include those assets.

The name `requiredAssets` paired with a “SHOULD” requirement is a little weird.

---

**lukaisailovic** (2024-12-14):

[@SamWilsn](/u/samwilsn) The use case is that if the dapp only needs a certain few assets, the wallet shouldn’t return everything it has. However, if dapp requested the asset and user doesn’t have it (wallet has nothing to return), it still shouldn’t fail the request.

What do you think, is there a better way to handle it?

---

**SamWilsn** (2024-12-16):

I would just name it differently in that case. Something like `onlyAssets` or `assetsFilter` maybe? My complaint is only about the name, and not the functionality.

---

**lukaisailovic** (2024-12-16):

Thanks a good point, I’ll update the name!

---

**montycheese** (2025-01-14):

What’s the expected behavior if requiredAssets is not provided? As an app developer I’d likely want a way to fetch all of the assets contained within the wallet (that the wallet is aware of)

---

**montycheese** (2025-01-14):

Also what if this allowed requesting assets for multiple wallet accounts in the same call to save on number of confirmation screens?

e.g.

```auto
type WalletGetAssetsRequest = {
  params: [{
    account: Hex;
    requiredAssets?: Record;
   }]
};
```

---

**ajhodges** (2025-01-15):

Hey! Wanted to chime in with some feedback after a review of the current proposal:

Some concerns:

- it’s not paginated, this asset list could get extremely long
- the filter isn’t very powerful; i.e. if I only care about ERC20s, there’s no way to request only erc20s (if you dont care about NFTs)
- we might also want an optional spam filter (i.e. a wallet would filter spam assets by default, but the caller could request an unfiltered list)
- the NFT balances aren’t aggregated by collection, which can put a lot of work on the client to attempt to go through and aggregate them for display purposes

---

**lukaisailovic** (2025-01-16):

Good point! Added clarification in the spec

---

**lukaisailovic** (2025-01-16):

> Also what if this allowed requesting assets for multiple wallet accounts in the same call to save on number of confirmation screens?

[@montycheese](/u/montycheese) batching is something that can be added to basically any RPC call out there atm. I think the batching should be solved at the top level and should work with any call, not in the call itself.

> Hey! Wanted to chime in with some feedback after a review of the current proposal:
>
>
> Some concerns:
>
>
> it’s not paginated, this asset list could get extremely long
> the filter isn’t very powerful; i.e. if I only care about ERC20s, there’s no way to request only erc20s (if you dont care about NFTs)
> we might also want an optional spam filter (i.e. a wallet would filter spam assets by default, but the caller could request an unfiltered list)
> the NFT balances aren’t aggregated by collection, which can put a lot of work on the client to attempt to go through and aggregate them for display purposes

[@ajhodges](/u/ajhodges)

Agree regarding the pagination. We’ve been discussing this for some time now and none of the solutions feel pretty. Still will probably need to be solved.

For other stuff, I don’t think it needs to be solved at the RPC level. You can just filter/group on the client side. It seems pretty simple. Would be curious to hear your take on why do you think wallet should do it rather than the client

---

**ajhodges** (2025-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lukaisailovic/48/12558_2.png) lukaisailovic:

> Agree regarding the pagination. We’ve been discussing this for some time now and none of the solutions feel pretty. Still will probably need to be solved.
>
>
> For other stuff, I don’t think it needs to be solved at the RPC level. You can just filter/group on the client side. It seems pretty simple. Would be curious to hear your take on why do you think wallet should do it rather than the client

I’m thinking of use cases beyond the typical browser extension wallet → browser app. i.e. a server-based wallet. Loading thousands of token balances in a single request is likely going to be very slow/unreliable. Think of a worst-case scenario wallet like vitalik.eth that has hundreds of legit tokens in it and thousands more spam tokens. This is what we should design for. IMHO this means the request should have flexible filters and pagination.

---

**lukaisailovic** (2025-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajhodges/48/10747_2.png) ajhodges:

> I’m thinking of use cases beyond the typical browser extension wallet → browser app. i.e. a server-based wallet. Loading thousands of token balances in a single request is likely going to be very slow/unreliable. Think of a worst-case scenario wallet like vitalik.eth that has hundreds of legit tokens in it and thousands more spam tokens. This is what we should design for. IMHO this means the request should have flexible filters and pagination.

Agree regarding pagination, that’s a must-have. It will be added.

Curious how would you solve the filtering issue? For example, it can also be assumed that the wallet would filter the spam tokens anyways and would not send them back to the client.

There are two options IMO:

1. Define a few filters like, onlyTokens, onlyNFTs, noSpam etc and wallet MUST implement them when indicating support for 7811
2. Have something more open-ended like capabilities, but then say if the filter is provided wallet SHOULD reflect that in the response.

Also keep in mind that this will probably not be used directly by the client. It will be wrapped in a library/SDK first, like we don’t use any RPCs directly today really.

Would love to hear your thoughts

---

**ajhodges** (2025-01-22):

I think I lean towards having some sane filters defined in the spec vs leaning on a capability approach. I would think a capability-per-filter would lead to fragmented support and diminish the overall usefulness of filters in general.

The assets filter is one example that’s already defined in the spec. I could also see a ‘assetType’ filter, ‘spam’ filter, ‘chain’ filter

i.e.

```auto
{
  "account": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "assetFilter": {
    "0x1": ["0x456", "native"]
  },
  "assetTypeFilter": ["ERC20", "native"],
  "chainFilter": ["0x1"],
  "spamFilter": true
}
```

Maybe spam filter could be an optional one? Though I feel like most wallets have spam filtering in place these days

> For example, it can also be assumed that the wallet would filter the spam tokens anyways and would not send them back to the client.

I 100% expect wallets to filter spam by default, I am just thinking of the case where a dapp may want to request unfiltered asset ownerships to avoid wallets flagging false positives. Maybe this isn’t a thing though

---

**lukaisailovic** (2025-01-22):

I think we should drop the spam filter. I can’t see a use case where the dapp would want spam tokens.

Aligned on the other stuff!

Currently we have this in the spec

> If the assetFilter field is provided and the assets array is empty, the wallet MUST restrict results to the requested chains and SHOULD return all assets on those chains.

Kinda like `chainFilter`, but having explicit field for that is much cleaner.

edit: actually even the statement in the spec is incomplete, its missing the part where the client should provide the key (chainId) but can leave out the asset array

---

**lukaisailovic** (2025-01-26):

[@ajhodges](/u/ajhodges) Updated the spec with included filters. Let me know what do you think

---

**kdenhartog** (2025-08-05):

I’m late to the party, so might be too late to offer suggestions.

Sharing this information will produce another vector of Web fingerprinting beyond the ability to track users via their wallet address. Was there any thought put into the mitigations to prevent this fingerprinting surface from being introduced or is there a way that we could think through avoiding this issue?

I guess I’m not exactly certain what the key use cases for this RPC is, so want to understand that first before I offer changes to how we mitigate fingerprinting so we can actually still address them first and foremost while still addressing privacy.

For example, a simple privacy consideration would be to allow the user to self select which assets they share via this API. It’s a bit cumbersome in UX so there’s a tradeoff there, but at least allows the user to control how much they can be fingerprinted by this API.

