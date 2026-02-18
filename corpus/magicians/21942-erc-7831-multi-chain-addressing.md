---
source: magicians
topic_id: 21942
title: "ERC-7831: Multi-Chain Addressing"
author: SamWilsn
date: "2024-12-03"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7831-multi-chain-addressing/21942
views: 315
likes: 14
posts_count: 14
---

# ERC-7831: Multi-Chain Addressing

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/749)














####


      `master` ← `SamWilsn:cas`




          opened 01:39PM - 03 Dec 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/2c575027ee1f57338df478738fa0a364bd895e9b.png)
            SamWilsn](https://github.com/SamWilsn)



          [+367
            -0](https://github.com/ethereum/ERCs/pull/749/files)

## Replies

**shemnon** (2024-12-03):

Is there a reason we need this when [CAIP-10](https://chainagnostic.org/CAIPs/caip-10) exists?

I feel that needs to be addressed in the motivation section as well as why this would be superior to CAIP-10 rather than merely just as good as CAIP-10.

---

**SamWilsn** (2024-12-04):

CAIP-10 is off-chain, and doesn’t provide a framework for routing between L2s. This proposal sketches out a framework for wallets to send to L2s they know nothing about (though the specifics are left to future standards.)

I should point out that [ERC-7828](https://github.com/ethereum/ERCs/pull/735) is the more likely candidate for adoption, so you might want to repeat your comment there.

---

**wjmelements** (2024-12-05):

Aww based on the title I was hoping this ERC was recommending the best way to do multichain deterministic deployments.

---

**frangio** (2024-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I should point out that ERC-7828  is the more likely candidate for adoption

What is the difference between 7831 and 7828?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> CAIP-10 is off-chain

Can you expand on this? We’re proposing to use CAIP-10 “on-chain” for [ERC-7786](https://ercs.ethereum.org/ERCS/erc-7786) and it’s one of the points I have stronger doubts about.

---

**SamWilsn** (2024-12-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> SamWilsn:
>
>
> I should point out that ERC-7828  is the more likely candidate for adoption

What is the difference between 7831 and 7828?

The major design difference is that ERC-7828 resolves names of the form `user@l2-name.l1-name` (eg. `sam@optimism.eth` or `bob@arbitrum.sepolia`), while ERC-7831 resolves names of the form `user-ens:l2-name:l1-chainid` where `:l1-chainid` is optional (eg. `sam.eth:optimism` or `bob.eth:arbitrum:11155111`).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> SamWilsn:
>
>
> CAIP-10 is off-chain

Can you expand on this? We’re proposing to use CAIP-10 “on-chain” for [ERC-7786](https://ercs.ethereum.org/ERCS/erc-7786) and it’s one of the points I have stronger doubts about.

I’m not familiar enough with ERC-7786 to have a real opinion here, but both ERC-7831 and ERC-7828 use ENS as the source of truth for L2 metadata.

---

**sbacha** (2024-12-16):

why is ENS enshrined?

---

**SamWilsn** (2024-12-16):

It isn’t enshrined. One could easily write a similar standard for any name service and have it coexist reasonably well with this one.

---

**jaack** (2024-12-17):

While the character `@` is generally overloaded, it provides a more mainstream approach to ‘browsing’ multichain addresses because it mentally connects to another widely used primitive with same approach, i.e. the email.

Chains can be likened to email providers, so just like you @gmail.com, you now @arbitrum.eth. I see zero friction for users for ERC-7828 to be adopted.

---

**jaack** (2024-12-17):

Unfortunately, not all name services use the ENS standard. So if this is done using the ENS implementation, it cannot easily be ported on **any** name service on other L2s.But still, it could be a non-issue.

---

**SamWilsn** (2024-12-17):

That’s kinda the problem with the `@` symbol though. With the email `sam@example.com`, `sam` is bound to the namespace `example.com`. There’s nothing in ENS that restricts a name to the chain it was registered on. For example, `someuser.optimism.eth:base` and `someuser.optimism.eth:optimism` both refer to the same entity, just on different chains. `someuser@gmail.com` and `someuser@hotmail.com` do not share the same relationship.

---

**jaack** (2024-12-19):

mmm OK, maybe I have some confusion about this: I thought that the clean chain name would only be representative of the **target chain** of the transaction, not the **actual** position of the ENS record in the registry.

Meaning:

- I assume that ENS is the only and default name service, so that name resolution can be implicit in some cases (we only look at ENS if there’s a clean name, or if the name starts with 0x, a string that can be reserved so that nobody can take names starting with 0x)
- if I want to send 1 ETH to alice.eth on Arbitrum, there can only be one alice.eth anywhere, just like there is now, so I just use alice@arbitrum.eth, and not because it’s bound, but because that string, in that moment, routes to the specific address of Alice.

This flow works the same way as email on the UX part, but differently on the routing part.

There’s a lot of confusion about chains and names because some L2s and dapps are reserving their chain or dapp name (like Base or Uni) and selling subdomains as identities on the chain (and yes, those are of course bound by the chain name!)

But if a universal multichain address routing goes through, then those subdomains don’t make sense anymore.

I imagine that the routing would be happening at runtime, and not in a predefined record, so that if a chain shuts down, changes name or if a user changes name or its account gets compromised, nothing can break.

Does it make sense?

---

**SamWilsn** (2024-12-20):

I’m not sure I understand this part:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jaack/48/14109_2.png) Routescan:

> I thought that the clean chain name would only be representative of the target chain of the transaction, not the actual position of the ENS record in the registry.

That said, I think we’re saying the same thing: there can only be one `alice.eth`. What differs is that I believe the `@` makes `alice@arbitrum.eth` and `alice@base.eth` look like different entities.

---

**jaack** (2024-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> That said, I think we’re saying the same thing: there can only be one alice.eth. What differs is that I believe the @ makes alice@arbitrum.eth and alice@base.eth look like different entities.

Then yes, I think we’re saying the same thing.

What I meant is that of course it seems like a different entity, but **this** I believe will be easy for users to get accustomed to, because it’s nearer to an ‘avatar’.

They look like different entities because they are, in some way: if you send money to alice on Arbitrum, but she wants them on Base, you made a mistake. It’s not the same mistake you’d make if you send an email to `alice@gmail.com` and instead you wanted to send to `alice@aol.com`. These two email addresses *could* belong to the same person, but maybe they’re not.

With that EIP we’d basically be solving the cross-service name squatting: if you get an ENS, you get it everywhere, and the only issue arises if you want another type of domain name (like .blast, .sonic or whatever L1 or L2 you want to be on).

