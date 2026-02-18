---
source: ethresearch
topic_id: 13624
title: Soulbound tokens as a solution to ENS fees
author: bruno_f
date: "2022-09-10"
category: Applications
tags: []
url: https://ethresear.ch/t/soulbound-tokens-as-a-solution-to-ens-fees/13624
views: 3028
likes: 5
posts_count: 11
---

# Soulbound tokens as a solution to ENS fees

**TLDR**: “Normal” ERC-721 ENS names pay Harberger taxes. But if you convert your name to a Soulbound NFT (thus losing the ability to sell it on the secondary market), you pay a low fixed recurring fee.

---

Recently both [Vitalik](https://vitalik.ca/general/2022/09/09/ens.html) and [Nick Johnson](https://mirror.xyz/nick.eth/EAH91vsu24WlvIqs3os-ISEpgnqIic0Y3z_asUVtGy4) wrote about ENS fees and the challenges on finding an adequate fee model. If you haven’t read both pieces yet, I highly recommend it.

It seems clear from reading both texts that ENS names fall in two categories:

- Identity-based names. Whether it’s the name of a person, or a nickname, or a company/brand, these names are used to identify some entity.
- Traffic-based names. These are names that seem to be valuable digital real estate because they are generic search terms. A list of the most expensive domain names shows examples as nfts.com, hotels.com, casino.com.

The names in the first category are more valuable to society if they remain with their namesake owners. Clearly it’s better if vitalik.eth remains owned by people named Vitalik, and ideally with the most known Vitalik. The names in the second category don’t need to be tied to any particular entity. No one expects [hotels.com](http://hotels.com) to belong to a particular company/person, they only expect to be able to book an hotel there.

I think that the main issue with ENS fees is that we are trying to apply one fee model to two fundamentally different products. For identity-based names it makes more sense to have negligible recurring fees. The name redcross.eth is probably worth a lot to scammers and requiring Red Cross to pay high fees only protect their users from being scammed seems like a socially sub-optimal result. On the other hand, speculators buy up hundreds of names at a time and then leave them unused until they can sell them at a much higher price. This rent extraction is an economic drag and ideally we would like to apply Harberger taxes on those names to maximize utility and have that value accrue to ENS DAO.

The main insight here is that identity-based names don’t require transferability while traffic-based names do. The name nick.eth is worth the same to Nick Johnson whether he can transfer it or not, while wallet.eth is only worth something to a speculator if he can sell it on the secondary market.

So, here’s my proposal. Names on the primary market are always sold through Vickrey auctions (as was already done for 3 and 4 characters names). Then, after you acquire a name you have two options:

1. Convert your name to a Soulbound NFT. In that case, you’ll pay a small annual fee, like the current 5$. This fee is only to guarantee that lost or forgotten names will eventually return to the market.
2. Keep your NFT as an ERC-721. In that case you’ll be subject to Harberger taxes.

Comments/suggestions are very much welcomed!

## Replies

**MicahZoltu** (2022-09-10):

I’m not personally a fan of account bound tokens, as users should *always* be able to rotate their keys.  However, if you used something like [EIP-5114: Soulbound Badge](https://eips.ethereum.org/EIPS/eip-5114) you would still be able to sell on the secondary market, just in a round about way.  How about just make it so if ownership is entirely burned, then the fees become flat?

---

**bruno_f** (2022-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> How about just make it so if ownership is entirely burned, then the fees become flat?

You mean something setting the registrant account to the null address? It probably wouldn’t work since someone could just set the controller account to a smart contract and then sell control over that smart contract. It would just be another way of selling the domain.

But there might be something there. The registrant can only 1) transfer ownership of the domain and 2) change the controller address. If we disallow ownership transfer and force the registrant address to be an actual public key (we could require a proof of knowledge of secret key) then the owner could not sell the name (at least it would always retain the power to take it back).

My fear is that people would still sell the names and just try to enforce the sale with a legal agreement. For example, you sell me a name by changing the controller address to my wallet and also sign a contract stating that you can’t use your registrant key to take back the name.

The closer solution to what you propose would be setting the registrant and the controller addresses to the null address. This works but would in effect freeze all the records in the name.

---

**bruno_f** (2022-09-10):

The problem is that we still don’t have a good solution for soulbound tokens (AFAIK).

---

**MicahZoltu** (2022-09-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/bruno_f/48/8809_2.png) bruno_f:

> You mean something setting the registrant account to the null address? It probably wouldn’t work since someone could just set the controller account to a smart contract and then sell control over that smart contract. It would just be another way of selling the domain.

The requirement for the “fixed pricing” would be that you set the registrant and the controller both to `0`.  Alternatively, if someone ever builds an official “immutable subdomains” module then setting them to point at an immutable subdomain contract I think should also get you locked in for fixed pricing.

The idea here is that if your name is being used for immutably pointing to an address, or used as an immutable subdomain registry, then even if you change owners you can’t change what the name does/points to.  This makes it basically worthless on the secondary market.  One could argue that if you can successfully turn your name into an immutable subdomain registry maybe you could sell rights to the proceeds from that, but I don’t think that is the scenario we want to protect against as this isn’t squatting but rather building a successful business and then selling it.

---

**bruno_f** (2022-09-11):

What if I use my name to immutably point to a smart contract address and then sell the access to that smart contract address? It seems like I would once again be able to sell that name in a round about way.

I’m leaning more towards devising a solution where the original owner can always take control of the name, and ideally do it in a manner that has plausible deniability (so that people can’t even take you to court over it).

---

**MicahZoltu** (2022-09-13):

While you *could* link to a proxy, you wouldn’t be able to add any other records like IPFS hashes, encryption keys, etc. to it so the resale value I suspect would be quite limited.  For example, if you managed to snag some trademark, point it at a contract, and mark it as immutable so you could keep it cheap, the trademark owner probably wouldn’t want to buy it from you because they can’t actually use it for 90% of the things one would want an ENS name for.

My problem with allowing the original owner to take back control is that it should *always* be possible to rotate your keys if they are compromised, and anything that binds an asset to a specific key makes it so that key cannot be rotated.  If your “recovery key” is compromised in your scenario, then the attacker can (at any point in the future) take the ENS name from you (though you could take it back, but the name would still be functionally attacked).

---

**bruno_f** (2022-09-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> While you could link to a proxy, you wouldn’t be able to add any other records like IPFS hashes, encryption keys, etc. to it so the resale value I suspect would be quite limited.

True, indeed. But what wouldn’t that also decrease the value of the name to me? If I have the bruno.eth name I would probably want to change some records occasionally. Identity-based names are probably quite long-lived, so having to decide on an immutable set of records at the beginning should be quite hard.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If your “recovery key” is compromised in your scenario, then the attacker can (at any point in the future) take the ENS name from you (though you could take it back, but the name would still be functionally attacked).

How about if the attacker cannot take back the name but rather just burn it? If you’re buying a name for yourself, you would just delete that key right after buying the name. But it would be impossible to prove to someone else that you deleted the key, thus decreasing its reselling value.

The more I think about it, the more I realize we don’t need a perfect solution here. We just need to discourage people from buying names on the secondary market enough that they prefer to pay the Harberger taxes on them.

---

**MicahZoltu** (2022-09-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/bruno_f/48/8809_2.png) bruno_f:

> True, indeed. But what wouldn’t that also decrease the value of the name to me? If I have the bruno.eth name I would probably want to change some records occasionally.

Immutable names serve a very specific purpose and it is not for individuals.  It is for writing censorship resistant software.  The idea is that you write a dapp, deploy it to IPFS, and point an ENS name at the IPFS hash permanently.  It cannot be changed by anyone ever, and that is a feature because if the developers are compromised they cannot change or take down the site.  The idea is to make it so this usage of ENS is possible/supported, and it isn’t really possible with fees that can change over time as you cannot pre-purchase indefinitely time in advance.

---

**bruno_f** (2022-09-21):

Ok, but then we are talking about different things. My goal is find an on-chain way to distinguish between identity-based names and traffic-based names and apply different fee schemes to them. Immutable names are cool but serve a very small number of users, we can’t have apply Harberger taxes to all mutable names since that will include almost every case.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The idea is to make it so this usage of ENS is possible/supported, and it isn’t really possible with fees that can change over time as you cannot pre-purchase indefinitely time in advance.

You don’t need to purchase time in advance. ENS allows anyone (not just the registrant/controller) to purchase time for a name. That feature was made specifically for immutable names, I think.

---

**MicahZoltu** (2022-09-22):

I think my argument here is just that there are actually 3 classes of users:

1. Identity names.
2. Traffic names.
3. Immutability names.

An ideal solution would be able to identify and price all 3 in ways that are appropriate for that class of name (this may be 3 separate pricing schemes, or 2 pricing schemes).

