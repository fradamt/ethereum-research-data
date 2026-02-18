---
source: magicians
topic_id: 2842
title: "EIP-1822: Universal Upgradeable Proxy Standard (UUPS)"
author: pi0neerpat
date: "2019-03-04"
category: EIPs
tags: [proxy-contract, eip-1822]
url: https://ethereum-magicians.org/t/eip-1822-universal-upgradeable-proxy-standard-uups/2842
views: 9505
likes: 22
posts_count: 33
---

# EIP-1822: Universal Upgradeable Proxy Standard (UUPS)

Universal Upgradeable Proxy Standard (UUPS), pronounced “oops,” is similar to existing proxy contracts, in that it creates an escape hatch for upgrading to a new smart contract when a bug or vulnerability is found. Here we introduce an improvement upon proxy contracts which can be used as a holistic lifecycle management tool for smart contracts.

Our motivation for developing UUPS was to reduce contract deployment cost for our onboarding tool, while maintaining universal compatibility and keeping ownership in the hands of the developers.

**View the explainer and simple tutorial**

https://medium.com/terminaldotco/escape-hatch-proxy-efb681de108d

**View the full EIP**



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1822.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1822.md)



```md
---
eip: 1822
category: ERC
status: Moved
---

This file was moved to https://github.com/ethereum/ercs/blob/master/ERCS/erc-1822.md
```










If you have any comments, edits, or suggestions, let us know here!

## Replies

**Amxx** (2019-03-04):

Won’t have any comments until there is something to comment, but as a huge fan of ERC1538 I’m really curious about want you have to propose ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**pi0neerpat** (2019-03-04):

Still waiting on review from an EIP Auditor, but I went ahead and updated the link with the PR. Looking forward to hearing your thoughts!

---

**jess.simpson** (2019-03-08):

I just did the Remix example on the medium article. What a way to explain the EIP, great work there ![:clap:](https://ethereum-magicians.org/images/emoji/twitter/clap.png?v=9)

---

**gbarros** (2019-03-08):

Gabriel here. Anxious to get your feedback and have great discussions!

---

**ali2251** (2019-03-12):

Hi,

I am Ali, author of https://docs.upgradablecontracts.com/ and have been researching in the area of upgradability for a while now.

I maybe missing something there but I cant see any improvements to the proxy contracts and the links you have provided to the Gnosis are OpenZeppelin are way too old, I suggest looking at their contracts in Production (Gnosis Safe) and ZeppelinOS.

To my specific concern.

1. Gnosis Safe contracts in particular do not use the first slot,  they use this: https://github.com/gnosis/safe-contracts/blob/development/contracts/proxies/Proxy.sol#L28
2. How is your pattern different from Zeppelins Unstructured storage? to me they look the same
3. How do you achieve a governance change? (If its such that the owner points to an address which is a contract which handles governance such as a multi-sig, I believe thats been around for a long time)

I am happy to have a chat offline if that helps but cant see the point of the EIP, but very open to being educated!

Best,

Ali

---

**Amxx** (2019-03-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/a/ccd318/48.png) ali2251:

> How do you achieve a governance change? (If its such that the owner points to an address which is a contract which handles governance such as a multi-sig, I believe thats been around for a long time)

I’ve proposed something very similar to ERC1822  with a callback mechanism for initialization of the governance. Proposal isn’t written yet but the code is available [here](https://github.com/Amxx/ERC1836UpgradableIdentityProxy/). In particular, you can check the `test/010_upgrade.js` to see an example

---

**pi0neerpat** (2019-03-16):

Hey I saw this a few weeks ago [on twitter](https://twitter.com/pi0neerpat/status/1105121463747706880?s=19). Excited to finally see the code.

---

**pi0neerpat** (2019-03-16):

Hi Ali, thanks for pointing this out. We weren’t aware of this particular implementation, but will add it to the EIP discussion section.

There are a few differences between ours and the Zeppelin unstructured example. I’ll start by saying that the overall the purpose of this EIP is to create a standard proxy (be it Zeppelin, the one we present, or a combination). By doing so we can improve developer experience across the ecosystem, and make a highly accessible interface rather than fragmented and incompatible implementations.

The following are two examples of common actions we may wish to perfom for many different proxy contracts. The UUPS allows us to avoid writing new code for every different proxy implementation.

1. Verify both the contract source code and initialization code
2. Create your own proxy of an existing deployed contract, using your own initialization parameters.

Another difference is that the storage slot is intentionally choose as “Proxiable”, and not a random string. Again, this helps us standardize the process.

Regarding governance, I think the approach your describing we debunk in the Medium post. Governance is not in an external contract. It can be implemented directly into the Logic Contract itself. This makes it much simpler to design

Happy to answer more questions!

---

**Amxx** (2019-03-16):

To answer your tweet here, I’m discussing that with Fabian from erc725 before proposing a new opposing standard for account proxy. My first objective is not generic upgradable contracts, but identity proxy with upgradable governance.

I’m sure there is a lot in ERC1822 I could benefit from. Feel free to PM me is you want to discuss that.

---

**gbarros** (2019-03-19):

Hey Amxx,

I am also interested in identities and have been playing with 725. Don’t you think this here could be the the smallest possible interface/base for an identity, since it’s (almost) fully upgrade-able, then we could add some very basic functionality for identity abilities ? Kinda the way 725 is already heading.

---

**Amxx** (2019-03-20):

I think your design is missing a mechanism to initialize the memory state of the proxy when the logic contract is updated.

`updateCodeAddress` must include much more then just updating the targeted logic. It potentially needs to reset the memory state of the proxy and configure the new logic. An exmaple is that, if you have an identity proxy that is a simple ownable contract, and you want to update it to a multisig, you should cleanup the owner and set up the multisig persmissions in a single transaction when updating the logic. This is why I include semantics for initilization function, and pass bytes to describe initialization operation.

Without that I’m afraid updating security policy will be either insecure of non user friendly

---

**Amxx** (2019-03-20):

I believe what i’m proposing in ERC1836 is close to the minimal subset of ERC1822 that has the added functionnality needed to manage “identities” through proxy

---

**gbarros** (2019-03-20):

I think the addition of “re-initialization” code is a great suggestion. I wouldn’t go as far as say it’s a reset, but definitely it’s a process that might be needed. Although there is already space for it happen, I agree that it’s not the best user experience not having it in a single tx if possible.

I will think a bit and suggest an implementation for it.

---

**Amxx** (2019-03-20):

I think state reset is needed for 2 reason:

- I might want to upgrade from mutlisig1 to multisig2 or from multisig2 to multisig1. If the 2 were dot designed to be compatible, I one will end up assuming fiels are null when the previous delegate set them. This can be keys or anything else.
- When moving from multisig1 to multisig2 then back to multisig1 I will assume no traces of are left that would break the assumptions of the second usage of multisig1.

That is why I believe some data should formalized by ERC1836 to stay as an invariant — nonce / nonceless replay protection / identity generic data (from ERC725) for example — and everything else should be cleaned up.

We could however see the cleanup as a layer on top of the standard, with the basic `updateDelegate` / `updateCodeAddress` not performing the cleanup and an added cleanup function that would clean then call the upgrade mechanism. That way you have the choice to cleanup before upgrading or not (in a single tx)

---

**gbarros** (2019-03-20):

A reset is something potentially impossible, or at the very least cost prohibitive.

If you are upgrading from `multisig1` to `multisig2`, you are not just randomly pointing to another implementation but rather something more like `fromMultisig1ToMultisig2` implementation/logic contract.

Also, I remember from a conversation with Fabian where his was proposing (when discussing identity) those contract whose address are beacons (not meant to be changed, such as the 725) be managed by some other contract. This came up when talking how, in this particular case, a 725 is often managed by a single owner but in the future might be managed by a multsig. In his view, when it happens you change the owner to a 734 contract. I think that’s the best option for when changes are quite drastic ( although I do see how you could potentially make it happen with a “simpler” upgrade).

---

**Amxx** (2019-03-20):

I believe `multisig1` and `multisig2` cloud be ERC1077 (universal login), gnosis safe, uport, … things that you may want to move from and to in no particular succession.

My issue with having an ERC734 owning an ERC725 is that:

- By calling the ERC725 proxy you would not be able to access info from the multisig (like ERC1271 interfaces) … this can be solved by a fallback in the proxy, which i proposed as a PR to ERC725
- The multisig owns no asset, and therefore cannot easily refund relayer for meta transaction (or the multisig has to be ERC725 specific … which I think isn’t a good idea)
- You end up with a LOT of multisig (one per proxy) which is expensive to deploy and fill the blockchain memory … keep in mind that they will be disposable

---

**gbarros** (2019-03-20):

> You end up with a LOT of multisig (one per proxy) which is expensive to deploy and fill the blockchain memory … keep in mind that they will be disposable

You missed the point of UUPS hahaha. You wouldn’t really deploy the whole 734 every time, just deploy an UPPS and point to it.

> The multisig owns no asset

But it manages a contract that has assets. It *is* able to implement 1077 with no trouble and ask the 725 to issue the repayment. All this while the other systems are completely unaware of what is really going on with the setup (734->725).

> By calling the ERC725 proxy you would not be able to access info from the multisig.

As of now, it’s not part of the ERC725, and for that, I agree that it is not straightforward. But you could have an implementation of 725 that is aware of outside management, meaning another contract.

All this to say, that you really don’t need to resort to “state” resets.

Once a user deploys a contract with a vendor, they will be very limited on migrating it to another vendor’s implementation. Therefore, it makes sense that vendors will keep track (as they have), of their implementations, and when updates/upgrades are available they will have to check for compatibility. We can only try to make this less of a “locked with a vendor” kind of situation. And I think decoupling where possible, as 725 being simple but managed externally is one of those measures.

---

**Amxx** (2019-03-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gbarros/48/1567_2.png) gbarros:

> You missed the point of UUPS hahaha. You wouldn’t really deploy the whole 734 every time, just deploy an UPPS and point to it.

Ok so instead of having potentially millions of abandonned multisigs, you have millions of abandonned ERC1822 … sure it’s better, but still sounds bad to me

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gbarros/48/1567_2.png) gbarros:

> But it manages a contract that has assets. It is able to implement 1077 with no trouble and ask the 725 to issue the repayment. All this while the other systems are completely unaware of what is really going on with the setup (734->725).

But you have 2 different version of the 1077, one for when it’s a standalone, and one for when it’s behind an ERC725

In the end it’s a matter of personal preferences. I see the point of your organisation. It’s less likely to break but is more expensive. I see mine as being more elegant and cheap, but also more complex for SCs developers

---

**gbarros** (2019-03-20):

> millions of abandonned ERC1822

Next iteration will have a [solution for it](https://ethresear.ch/t/improving-the-ux-of-rent-with-a-sleeping-waking-mechanism/1480).

Glad we could talk.

---

**frangio** (2020-06-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pi0neerpat/48/1438_2.png) pi0neerpat:

> Another difference is that the storage slot is intentionally choose as “Proxiable”, and not a random string. Again, this helps us standardize the process.

To improve compatibility of this proxy with existing and future solutions, I think it would be much better to use the slot defined in [EIP-1967: Standard Proxy Storage Slots](https://ethereum-magicians.org/t/eip-1967-standard-proxy-storage-slots/3185). [@pi0neerpat](/u/pi0neerpat) Can you explain the reasons why this was explicitly decided against? We’re trying to move said EIP to Final state and it would be good to have UUPS on board.

We really do like this model and want to provide an implementation of it in OpenZeppelin Contracts but the choice of an incompatible storage slot sticks out as a problem for us. For inclusion in OpenZeppelin it would also be necessary to move this EIP to Final.


*(12 more replies not shown)*
