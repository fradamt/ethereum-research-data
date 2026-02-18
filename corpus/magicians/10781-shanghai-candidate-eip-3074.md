---
source: magicians
topic_id: 10781
title: "Shanghai-candidate: EIP-3074"
author: matt
date: "2022-09-09"
category: EIPs > EIPs core
tags: [account-abstraction, shanghai-candidate]
url: https://ethereum-magicians.org/t/shanghai-candidate-eip-3074/10781
views: 3212
likes: 12
posts_count: 7
---

# Shanghai-candidate: EIP-3074

[![image](https://ethereum-magicians.org/uploads/default/original/2X/a/a8f2dc3c5324d3029c1831e518fc3fc51756b87f.jpeg)image500×500 60.4 KB](https://ethereum-magicians.org/uploads/default/a8f2dc3c5324d3029c1831e518fc3fc51756b87f)

Early last year, I felt there was a real possibility of EIP-3074 being included in the Berlin hardfork. The authors pushed to get the EIP into a stable state, but it was a bit too late and there were still questions around the security of it.

To resolve these security concerns, we had two security audits of the specification [[1](https://leastauthority.com/blog/audit-of-eip-3074-for-ethereum-foundation/), [2](https://dedaub.com/blog/eip-3074-impact)] which both came back clean. We then [reapplied](https://github.com/ethereum/pm/issues/260) the EIP for CFI for London. It was [subsequently rejected](https://www.youtube.com/watch?v=C9hzAYkklQM&t=2403s) to keep London simple, but with the understanding it would again be considered for Shanghai.

Well – Shanghai is finally just around the corner! The EIP has been stable over the last year and there are no additional changes to consider. I would like propose the EIP for Shanghai ([again](https://github.com/ethereum/pm/issues/394))! [There](https://eips.ethereum.org/EIPS/eip-3074) [are](https://blog.mycrypto.com/eip-3074) [many](https://www.youtube.com/watch?v=zToZVpKPW6Q) [resources](https://www.youtube.com/watch?v=pUJlZMXrVEI) [to](https://www.youtube.com/watch?v=eEOb0hlrCLU) [understand](https://www.youtube.com/watch?v=KVrhyTk9_zY) [the](https://twitter.com/search?q=eip-3074) [benefits](https://www.youtube.com/watch?v=pS5asEp6ry8) [of](https://ethereum-magicians.org/t/validation-focused-smart-contract-wallets/6603) [EIP-3074](https://ethereum-magicians.org/t/eip-3074-auth-and-authcall-opcodes/4880), however I want to point out two specific points that are particularly relevant today:

- Despite EIP-4337 existing for over 1 year, I’m not aware of any wallets that support it. For better or worse, core protocol changes are schelling points and EIP-3074 could quickly be adopted by major wallets (many of them support the EIP) and drastically improve UX on Ethereum.
- On a more practical front, smart contracts are still plagued with dealing with two types of ether (eth and weth). EIP-3074 provides the functionality to actually remove this distinction for contracts, which has been a very rough edge for developers.

## Replies

**cyrus** (2022-09-16):

Please note: I’ve requested a small change to this EIP (specifically, how tx.origin is handled in a world where the gas payer and account “doing the thing” are no longer synonymous) and hope that it can be considered and discussed before moving forward. See here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cyrus/48/10140_2.png)
    [EIP-3074: AUTH and AUTHCALL opcodes](https://ethereum-magicians.org/t/eip-3074-auth-and-authcall-opcodes/4880/103) [EIPs](/c/eips/5)



> In the current EVM, tx.origin is the account from which the transaction originates (logically, the account “doing the thing”) as well as the account that pays the gas to execute the tx. They are synonymous.
> With EIP-3074, this is no longer the case; these identities get split up: The logical originating account account “doing the thing” is the AUTH’d account, but the account paying the gas to initiate the transaction is the account making the AUTHCALL to remote control the AUTH’d account into “…

Without this change, 3074 will break the way some of my 2015 smart contracts handle NFT ownership.

---

**Pandapip1** (2022-09-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> image500×500 60.4 KB

We somehow have 4/5 EIP editors in support of this ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=15) - [@gcolvin](/u/gcolvin) is the only person that hasn’t liked your post (yet). Too bad we can’t participate in governance…

EDIT: 5/5 EIP editors

---

**pgebheim** (2022-09-20):

Heya!

I’ve been a bit out of the loop on this over the last year. I’ve got some brass tacks questions that might be easy to answer / point me to the right resource:

1. Which clients already have implementations of 3074? Is the Quilt geth patch still the canonical implementation?
2. Does anyone have a solid lists of tasks that would be helpful in getting this over the finish line?
3. On the high level does everyone here agree with the thread @cyrus linked to earlier?

---

**yoavw** (2022-09-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> To resolve these security concerns, we had two security audits of the specification

I think the audits actually came before the [security concerns](https://ethereum-magicians.org/t/a-case-for-a-simpler-alternative-to-eip-3074/6493/1) I raised.  The audits were finished on the June 14 2021 and May 19 2021, and my post above is from June 16 2021 and mentions risks that are not in the audits, as far as I recall.

I’m glad to see `chainid` was subsequently added to the signed message, which mitigates one of the attacks I demonstrated.  Thanks for adding that!

I still feel that the risk outweighs the benefit, for the reasons I mentioned before.  E.g. no way to revoke a previously signed AUTH.  Revoking is hard to implement, but how about a `deadline` block number, like the one used in [EIP 2612](https://eips.ethereum.org/EIPS/eip-2612)?  It would at least cap the risk to recent approvals.

Even if we had a way to revoke old AUTH or set a `deadline`, attacks like the Governance Hijack I described would still be possible.  (Quick reminder: an invoker that helps users do something useful, but also delegates their voting tokens to an attacker.  Users won’t notice anything since they still have the tokens, but the attacker steals everyone’s voting power).

Another concern is that EIP 3074 enshrines certain things we’re trying to change.  It enshrines ECDSA signatures, which we’re working to abstract away.  At a higher level it [enshrines the EOA model](https://ethereum-magicians.org/t/we-should-be-moving-beyond-eoas-not-enshrining-them-even-further-eip-3074-related/6538) rather than move Ethereum towards a contracts-only model.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Despite EIP-4337 existing for over 1 year, I’m not aware of any wallets that support it.

While EIP 4337 hasn’t been finalized yet, and new features like BLS aggregation are still work in progress, there are several wallets being built around EIP 4337 and a growing community of developers around it.  Building wallets takes time, and they’re doing it while the EIP is undergoing breaking changes.

To name a few, [Stackup](https://www.stackup.sh/) is [ERC-4337 compliant](https://docs.stackup.sh/), [Candide](https://www.candidewallet.com/) is [making progress](https://coda.io/@candide/contributors/progress-1-25), [Soul Wallet](https://docs.google.com/document/d/10JIe6Apirs8KdHGGtFIvs_IFNxLgFNLxOMLynKVgFcY/edit#heading=h.tat6al5f0tw) is [building an 4337 wallet](https://github.com/proofofsoulprotocol/smart-contract-wallet-4337) for soulbound NFTs.  I’m aware of a couple of others who haven’t published yet, and a couple of teams working on ERC 4337 tooling to make wallet integration easier.  You’re welcome to monitor progress on the [Account Abstraction discord](https://discord.gg/UY7HmJxK).

While ERC 4337 is not a protocol change, I think we can build upon it and get all the benefits of EIP 3074 and beyond, without compromising on security.  I hope we can join forces and work on a set of EIPs that will take us there.

---

**matt** (2022-09-26):

> how about a deadline block number, like the one used in EIP 2612? It would at least cap the risk to recent approvals.

We can of course implement this in the EIP, but am generally against ( as you are aware ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) ) because it reduces the flexibility of the mechanism. It is a simple mechanism to implement in the contract, and that is where I believe it belongs. Developers must be able to handle implementing code which is secure, and wallet teams must ensure their users aren’t exposed to insecure invokers.

---

**yoavw** (2022-09-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> as you are aware

Yep. We already agreed to disagree on this philosophy ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

I’m with you on giving developers as much flexibility as possible, but my concern is about the inevitability of bugs (or even maliciously introduced, well disguised “bugs”). On the trade off between making AUTH indefinite or limiting it in time, I’m (a little bit) inclined towards the latter.

But I acknowledge it’s a trade-off so I’ll counter myself and highlight a valid use case that my `deadline` suggestion would prevent.  Session-keys for games, like what ArgentX implements.  Sign an authorization for a game to perform a specific type of actions on your behalf so that you don’t need to sign each one.  Usability is indeed better if you don’t need to re-sign the AUTH every 30 minutes.

It’s possible to support this use case with account abstraction, e.g. an ERC 4337 wallet with a validation function that allows different keys to perform different actions.  And it’s possible with a specialized EIP 3074 invoker that only transacts with the game contract.  But limiting the authorization to a `deadline` breaks it.

Painful trade-off, I agree.

