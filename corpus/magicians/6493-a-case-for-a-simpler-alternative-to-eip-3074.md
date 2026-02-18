---
source: magicians
topic_id: 6493
title: A case for a simpler alternative to EIP 3074
author: yoavw
date: "2021-06-16"
category: EIPs
tags: [signatures, eip-3074]
url: https://ethereum-magicians.org/t/a-case-for-a-simpler-alternative-to-eip-3074/6493
views: 8125
likes: 33
posts_count: 45
---

# A case for a simpler alternative to EIP 3074

# A case for a simpler alternative to EIP 3074

The `AUTH`/`AUTHCALL` mechanism is very appealing from a developer’s point of view.  It gives anyone the ability to come up with an invoker that can implement different batching strategies (e.g. supporting multiple nonces for better parallelism), gas abstraction models, complex account abstraction methods, etc.

The flexibility comes from being completely unopinionated about how this mechanism is used.  Instead of requiring the developer to conform to a particular pattern, we require the user to sign an invoker-parsed `commit` hash, and let each developer set discretionary restrictions based on the commit.

However, this flexibility comes at an extremely high security cost.  I would like to make a case for a simpler alternative that would get us most of the benefit at a much lower risk.

Why is signing an AUTH `commit` riskier than signing a transaciton to any other buggy/malicious contract?

When signing a transaction to a contract, the user takes a known risk of losing assets controlled by that contract.  The user could sign an approval transaction to an ERC20 contract, approving a malicious DEX contract. The malicious DEX contract could then withdraw the user’s entire balance of that ERC20.  But… it cannot withdraw the user’s tokens from other ERC20 contracts without requiring specific approvals.  Nor can it do anything else on behalf of the user.  The approval is specific.

EIP 3074, on the other hand, requires the user to sign a blank cheque and assume that the invoker is honest and not buggy.  A malicious/buggy invoker could **do anything on behalf of the user** - access any asset owned by the user, vote on behalf of the user, take ownership of any contract owned by the user, etc.

Worse yet, the invoker can do it now and **in the future**, because the nonce implementation is controlled by the invoker.  A buggy/malicious implementation of the nonce logic could allow replaying the user’s past transactions.  Combined with buggy logic of other parts of the `commit` verification, it could be used to perform any future action on behalf of the user.  Even if the bug is discovered, the user has no way to revoke that blank cheque.  The EOA is compromised forever.

Writing a correct invoker is tricky and we are almost certain to get it wrong occasionally.  The [non-exhaustive list of checks/pitfalls/conditions that invokers should be wary of](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3074.md#secure-invokers) at the end of the EIP gives us a glimpse of that.  This list will inevitably grow, possibly through a painful discovery process.

Furthermore, a malicious actor could implement a honest-looking invoker with an intentional subtle bug which will be exploited after a lot of EOAs AUTH that invoker.

The attack may go unnoticed for a long time if it doesn’t steal from the user directly or immediately.

***Governance hijacking example***

- EveSwap, a malicious DEX, implements an invoker for its users.  It sponsors their gas through its airdropped EVE token and batches their approve+transfer transactions.
- EveSwap’s invoker appears honest and never steals user tokens because that would be discovered immediately.
- Users are happy.  Trades are cheap and successful, nothing bad happens for months.
- However, every time someone trades AliceSwap governance tokens, ALI, it self-delegates the user’s AliceSwap voting rights.
- Once delegation crosses a threshold, EveSwap hijacks AliceSwap through a governance proposal.

EveSwap users are unlikely to notice this process because their trades are always successful, but the end result is devastating for AliceSwap.

***Cross-chain replay example***

The EIP rightly suggests that the `commit` should cover `chainid`.  However, this is not enforced by the protocol, just the invoker.  An invoker with the same address on another chain might skip this check (or any check for that matter).

- EveSwap lives on the EVM-compatible BobSpongeChain, which also supports EIP 3074.  It deploys a honest invoker there.
- Users trade on BobSpongeChain using the invoker, and then use a bridge to move their assets to Ethereum.
- EveSwap uses the same deployment key to deploy a different invoker on Ethereum, at the same address.  The Ethereum invoker doesn’t check the commit at all.  It just checks ownerOnly and acts as a generic AUTH/AUTHCALL proxy for its owner.
- EveSwap hijacks the Ethereum EOAs of all its users and gets away with all their assets.

The users never transacted on Ethereum, and the invoker running on BobSpongeChain went through rigorous security audits and was found to be secure.  And yet, everyone lost their assets.

Ethereum prevents this through the replay protection in EIP-155.  AUTHCALL doesn’t.  By delegating all `commit` checks to the invoker, we lose any transaction protections offered by Ethereum.  The attack is possible because protection becomes discretionary.  If this EIP is accepted, the AUTH message must include `chainid` explicitly, not as part of the `commit`.

**What can we do instead?**

My proposal is to implement a more opinionated mechanism that enforces the meaning of the `commit` at the protocol level.  The commit structure will be typed (as in EIP 712) so the wallet will present it in a user-readable format.  The user will know exactly what the transaction will look like, and have confidence that it cannot be replayed later on any chain, without relying on the honesty and competence of an individual developer who implemented the invoker.

A possible implementation:

`AUTH` will replace the `commit` hash with a typed structure containing a list of authorized calls.  For each call, {nonce,to,gas,calldata,value,chainid} will be specified.  The signature will be verified, and the entire list will be saved as `authorized_transactions` instead of the `authorized` address variable.

`AUTHCALL` will get a new arg, `index`, which points to an address in the list created by the last `AUTH`.

The EOA’s nonce will be incremented on each `AUTHCALL`.  Not a nonce stored by the invoker, but the actual account nonce.

Pros:

- User gets full visibility into what’s going on.
- Security is enforced by the protocol.
- Still allows batching and account abstraction.

Cons:

- Opinionated about the nonce implementation and doesn’t support parallelism.
- Transactions of complex invokers become cumbersome because the user has to see and accept a list of all the calls.

A different implementation could support a different nonce scheme.  But whatever mechanism we use, MUST be enforced by the protocol rather than the invoker.

Complex invokers that perform a large number of user calls should arguably be prevented anyway.  Complex operations should be implemented as a normal smart contract rather than attempt to implement an algorithm using multiple EOA calls.

**Alternative: entirely avoid the hard fork**

Another option is to avoid the AUTH mechanism altogether, and solve the account abstraction and batching problems through an alternative mempool as [suggested by @vbuterin](https://notes.ethereum.org/@vbuterin/alt_abstraction)

Pros:

- No need for a hard fork.  The new type is supported through smart contracts and nodes that are aware of them.
- Can be used to implement anything that EIP 3074 could be used for, without introducing additional risk.

Con:

- Not backward compatible with existing EOAs.  Users will need to deploy a contract wallet and move assets to it.

Unless the requirement is to support existing EOAs without migration, this seems to be the safer option.

## Replies

**SamWilsn** (2021-06-16):

# Introduction

Thank you so much for the in-depth review! This is incredibly valuable, and you raise excellent points. I’ve understood a couple different criticisms that I’d like to summarize and discuss separately, before diving into your alternative proposal:

- Principle of Least Privilege: once an invoker has an authorization, it has complete control over the signing account.
- Buggy or Malicious Invokers: invokers may be complex pieces of software, and may contain bugs or even be malicious.
- Eternal Authorizations: once signed, without a cooperating invoker, an authorization lasts forever.
- Chain Id and Clever Contract Creation: an invoker on one chain (testnet, Ethereum fork, etc.) seems secure and checks the chain id, but a malicious invoker is deployed at the same address on another chain which does not check the chain id.

# Criticisms

## Principle of Least Privilege

> Once an invoker has a signed package, it has complete control over the signing account.

This is absolutely a concern shared by all of us authors. At first glance, it might seem like signing an EIP-3074 package is strictly worse than an infinite ERC-20 allowance. Instead of granting access to one token, you’re granting access to all of them, forever. Oh, and it’s irrevocable.

As [@danfinlay](/u/danfinlay) pointed out in his [excellent comment](https://ethereum-magicians.org/t/eip-3074-auth-and-authcall-opcodes/4880/61), many people have compared EIP-3074 to unix’s `sudo` command: signing a 3074 transaction is like giving up complete control over your account.

Both of these comparisons (to ERC-20 allowances, and to `sudo`) are true, to some extent, but they lack a lot of nuance.

An ERC-20 allowance has two components: what address is authorized, and an amount that address has access to (which may be infinite.) The owner has zero control over what the authorized address does with their allotment. A malicious contract could look safe, but when authorized, it transfers all the tokens away. On the other hand, an EIP-3074 authorization can set incredibly specific rules through the invoker for what can be done with the tokens.

To bring this back into the unix analogy, I believe EIP-3074 is a lot more like the [setuid](https://en.wikipedia.org/wiki/Setuid) bit than `sudo` itself. An executable which has the `setuid` permission assumes the identity of its owner rather than the identity of the executing user. Oftentimes, the owner will be `root`, allowing non-`root` users to execute *specific tasks* with elevated permissions.

My central theme here is that while an EIP-3074 authorization grants the invoker full power over the signing account, the fact that the invoker is programmable enables extremely fine-grained control over exactly what can be done with that power.

EIP-3074 is not `sudo`. It’s `setuid`.

## Buggy Invokers

> Invokers may be complex pieces of software, and may contain bugs or even be malicious.

This is unequivocally true. There will be buggy invokers. There will be invokers designed to scam. There will be trojan invokers who try to collect authorizations over time and eventually topple DAOs.

I *still* believe EIP-3074 is worth pursuing in its current flexible form. With UI mitigation, good security messaging, and carefully built code we can keep the majority of people (and their assets) safe.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Why is signing an AUTH commit riskier than signing a transaciton to any other buggy/malicious contract?

This comparison has come up several times while socializing EIP-3074, and I’ll defer once again to [@danfinlay](/u/danfinlay). He summed up why we shouldn’t compare EIP-3074 authorizations to traditional transactions more eloquently than I can in [his comment](https://ethereum-magicians.org/t/eip-3074-auth-and-authcall-opcodes/4880/61). I’ll quickly paraphrase it here:

> EIP-3074 allows a user to delegate full control of their account, and therefore invokers are better understood as part of the wallet’s own code and not as a separate contract.

In other words, we shouldn’t compare signing an EIP-3074 package to a traditional transaction, but to installing an extension for a wallet. Few wallets do this today, and none of them do it lightly. EIP-3074’s security proposition is very similar: install a malicious wallet/extension and get pwned; sign an authorization to a bad/buggy invoker and get pwned.

If I rewrite your paragraph replacing “EIP-3074” with “wallet” (and I mean *zero* disrespect here, I just couldn’t come up with a better way to convey my point), your criticism is equally valid:

> [Using an Ethereum wallet] requires the user to sign a blank cheque and assume that the [wallet] is honest and not buggy. A malicious/buggy [wallet] could do anything on behalf of the user - access any asset owned by the user, vote on behalf of the user, take ownership of any contract owned by the user, etc.

I think, therefore, it’s reasonable to draw the conclusion that invokers have a similar security profile as wallet software.

Wallets are already complex pieces of software, attached to *browsers* as often as not. The fact that they are not compromised on a daily basis gives me a little hope that we can write safe and solid code.

I would be remiss not to point out that wallets never transfer your private key, and EIP-3074 authorizations would necessarily be public, so there is that added risk. I would argue that invokers will be much simpler than wallets in general, so I think that balances out somewhat.

Buggy invokers would have to be *seriously* and *obviously* broken to be compromised to the level you suggest. Obviously the more complex the invoker is, the more opportunity for issues, but we can structure invokers in such a way that the more bug-prone/complex sections happen after the easy-to-verify sections. Essentially, check nonces before running batched transactions.

On-chain replay protection is putting a nonce in the commit, comparing a storage slot, then incrementing it. Screwing that up is difficult (not impossible, of course ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=15).) To change the authorization’s target you’d basically need to omit it from the signed commit, and same with the calldata. Also somewhat difficult to screw up.

I don’t think it’s outside of the realm of possibility for wallets to reject invokers which haven’t been formally verified and extensively audited. Combine that with strong best practices, and an attitude of abundant caution, and I think we can be reasonably certain that even the buggiest of whitelisted invokers won’t allow attackers to obtain permanent access to an account.

Malicious invokers are a completely different beast. Audits and formal verification can only go so far here. Instead we have to rely on social mechanisms, like whitelists and reputation. A huge part of the security proposition of EIP-3074 requires that wallets:

- Ban, generally, any signature which might look like an EIP-3074 authorization; and
- Allow a limited number of “trusted invokers” that have met some acceptance criteria.

Initially, for example, we expect wallets to whitelist their own sponsored transaction invokers. These invokers will likely only allow transactions originating from one of their official sponsor addresses, limiting the damage they can cause.

Further, wallets have extreme pressure to maintain stringent standards for their invoker whitelists. Users are free to move from one wallet to another, so even a *hint* of insecurity could destroy their reputation, and decimate their entire business model.

## Eternal Authorizations

> Once signed, without a cooperating invoker, an authorization lasts forever.

This is certainly a departure from other authorization patterns, like ERC-20 allowances. Similarly to the principle of least authority, however, EIP-3074 gives invokers the ability to define exactly how revocation (or expiry) will work.

At the simplest, an invoker can reuse nonce replacement to implement revocation, which should be simple enough to implement with some confidence. You could also limit validity to specific block number ranges, which is also trivial to implement.

## Chain Id and Clever Contract Creation

We’ve went back and forth on chain id several times, and I think this seals it as necessary. Are you convinced [@MicahZoltu](/u/micahzoltu)?

# Alternatives

## Nested Transactions

This seems pretty similar to other approaches to batched transactions like [EIP-2711](https://eips.ethereum.org/EIPS/eip-2711), or [EIP-3005](https://eips.ethereum.org/EIPS/eip-3005) except with the execution controlled by a contract. It’s actually quite similar to the [original EIP-3074 design](https://github.com/ethereum/EIPs/blob/d89ff42f53f2c3e0d4d44f63a273ab8ccfa4d18b/EIPS/eip-3074.md).

One potential issue with your proposal is that a transaction from the signer’s account can invalidate a sponsored transaction bundle, wasting the sponsor’s funds.

## Do Nothing

There are a couple use cases that EIP-3074 enables, which I don’t think can be implemented without *some* change. Synthetic EOAs, which are useful for state channels, are a really interesting unique feature of EIP-3074.

Contract wallets have a lot of the same issues as EIP-3074 invokers, so I don’t think they’re a better solution.

# The End

Thanks again for your comments, and for catching the issue with chain id! We all really appreciate the thorough review.

---

**yoavw** (2021-06-16):

Thanks for your quick and detailed reply!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> EIP-3074 is not sudo. It’s setuid.

I agree with you 100% on that.  The sudo analogy is wrong, at least the way most people perceive sudo - as shell access rather than a specific command hardcoded in /etc/sudoers.

I’m thinking about EIP 3074 exactly as setuid.  Consider the history of setuid binaries.  I used to audit those binaries in the early days of Linux, and before that on closed-source systems like Sunos/Solaris/Ultrix/Irix.  I found vulnerabilities in almost all of them, usually leading directly to unrestricted root access, and sometimes just as a stepping stone to achieving that (e.g. no direct code execution but can be manipulated to truncate an important file of my choosing, leading to privilege escalation).

In fact, most of the privilege escalation attacks on Unix based systems in the 1990’s and early 2000’s were due to buggy setuids.

It took a couple of decades to weed *most* of these bugs out, and required adding system level restrictions over the years, such as removing setuid support for interpreted executables (anything starting with #! such as shell/perl scripts), because they were almost impossible to secure.  Just recently, [CVE-2021-3156](https://blog.qualys.com/vulnerabilities-threat-research/2021/01/26/cve-2021-3156-heap-based-buffer-overflow-in-sudo-baron-samedit) reported such vulnerability that has been hidden in plain sight for 10 years.

Adding setuid to Ethereum might have similar results.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I still believe EIP-3074 is worth pursuing in its current flexible form. With UI mitigation, good security messaging, and carefully built code we can keep the majority of people (and their assets) safe.

To continue your Unix analogy, Linux eventually became more secure when it largely moved away from setuid executables in favor of an approach that caused much less trouble than setuid executables -  supporting specific privileged operations through system level daemons.  Such daemon typically starts from init, drops all unneeded capabilities, chroot itself to an empty directory if it doesn’t need filesystem access, setreuid/setregid itself to an unprivileged uid/gid, and only then start interacting with users.  For example, if ntpd needs to set the system clock, it doesn’t need to communicate with time-servers while running as root.  Instead, it only retains `CAP_SYS_TIME`, then switches to run as an unprivileged user before opening a network socket.  Therefore the worst that an attacker could do is mess with the time, not execute root level code.

This time-proven approach is what I think Ethereum should adopt if we need a privileged operation.  The alternative I suggested attempts to implement that.  The requirement is to perform an action on behalf of a user, but there is no requirement to allow the invoker perform just any action - only to reflect the user’s intention.  Hence I tried to drop the unlimited capability and replace it with one that is strictly tied to the user’s request.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I think, therefore, it’s reasonable to draw the conclusion that invokers have a similar security profile as wallet software.

Fair comparison.  The invoker becomes a wallet extension.

One major difference though: if a wallet adds support for extensions, it is affects only *that* wallet, and only above a certain version.  EIP-3074 adds extension support to *all* wallets.

Some problems that stem from this difference:

- Old unaware wallets become compromised.  Anyone using a pre-EIP-3074 wallet could be enticed to sign a benign-looking message that actually transfers its control to such extension.  The unaware wallet will not warn the user that it is actually an extension installation rather than a normal transaction.
- Even with EIP-3074-aware wallets that warn the user, many users will be enticed by short term benefits such as a DEX offering sponsored gas for their trades.  Most users won’t realize that they’re signing away full control of their wallet rather than just a trading authorization.  Immediate saving is easy to see, but delayed consequences are hidden.
- For hardware wallets it breaks user expectations.  When I sign a transaction on my hardware wallet I can verify it on the wallet’s screen without relying on the browser-based wallet.  A wallet extension like EIP 3074 breaks that expectation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Buggy invokers would have to be seriously and obviously broken to be compromised to the level you suggest. Obviously the more complex the invoker is, the more opportunity for issues, but we can structure invokers in such a way that the more bug-prone/complex sections happen after the easy-to-verify sections. Essentially, check nonces before running batched transactions.

Challenge accepted ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

If EIP 3074 is merged in its current form, I’ll try to release an invoker with a subtle bug that violates this assumption under a pseudonym and see how long it remains undiscovered.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> On-chain replay protection is putting a nonce in the commit, comparing a storage slot, then incrementing it. Screwing that up is difficult (not impossible, of course .) To change the authorization’s target you’d basically need to omit it from the signed commit, and same with the calldata. Also somewhat difficult to screw up.

At the risk of giving away the kind of subtle bugs I have in mind, consider a complex invoker that performs the nonce check as early as possible and stores it in a mapping.  The audit focuses on this pre-nonce-check code and it seems perfect.  However, deep inside some unrelated post-authentication housekeeping function I introduce a bug that allows me to overwrite arbitrary storage in the contract.  After collecting enough authorizations, I start resetting user nonces and replaying transactions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Ban, generally, any signature which might look like an EIP-3074 authorization; and
> Allow a limited number of “trusted invokers” that have met some acceptance criteria.

EIP-3074 aware wallets can do that, but we’ll be putting legacy users at risk of installing bad extensions without knowing that they even exist.

If we want to require wallets to be aware, then we need a new transaction type, incompatible with old wallets, and only accept the AUTH opcode when triggered from a transaction of the new type.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Further, wallets have extreme pressure to maintain stringent standards for their invoker whitelists. Users are free to move from one wallet to another, so even a hint of insecurity could destroy their reputation, and decimate their entire business model.

Wallet maintainers are not necessarily qualified to identify subtle/malicious bugs in invokers.

To use another OS analogy, Microsoft added drivers-signing many years ago and its reputation relies upon not signing malicious drivers.  Microsoft security engineers are quite capable.  And yet, researchers got them to whitelist malicious drivers.  Apple does that for any iOS app, requiring a signature from Apple itself in order to run an app on your iphone.  Their reputation depends on it.  And yet, malicious apps occasionally make it through and cause some damage until discovered and removed.

When I use a hardware wallet I don’t rely solely on MetaMask for my transaction security, although I’m sure the MetaMask team are among the best experts in the field.  I rely on what I see on the hardware wallet screen, and I know that even if MetaMask is compromised it cannot abuse my EOA, now or in the future.  EIP-3074 takes away that confidence and forces me to rely on MetaMask to audit and whitelist invokers.

On the other hand, it enables a lucrative business model for wallet maintainers ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12).  Most wallets (except MetaMask with the swaps support) don’t make a lot of money, but with EIP 3074 they can directly capitalize on their reputation (once), by robbing all of their users including high-value ones that use hardware wallets for signing anything of value.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> At the simplest, an invoker can reuse nonce replacement to implement revocation, which should be simple enough to implement with some confidence. You could also limit validity to specific block number ranges, which is also trivial to implement.

Yes, an invoker could implement pretty good protection schemes.  But the model is discretionary, not mandatory protocol level protection.  As you explained, it’s equivalent to a setuid executable, where I must trust the implementation of that particular binary rather than kernel level enforcement such as dropping unused capabilities.

Kernel level guarantees are stronger than usermode checks → protocol level guarantees are stronger than contract checks.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> One potential issue with your proposal is that a transaction from the signer’s account can invalidate a sponsored transaction bundle, wasting the sponsor’s funds.

Yes, I’m aware of the issue with changing the actual account state and conflicting with another transaction from that account.  It’s hard to mitigate without maintaining separate nonce storage for invokers.  However it would make sense to maintain this additonal nonce storage at the protocol level and mandate that it is used as part of `AUTHCALL` so that an invoker can’t replay messages even if it is buggy/malicious.

Another possible mitigation is to assume that miners run mev-geth (most of them already do), and have the sponsor pay the miner directly, but only if the nonce check succeeds.  The sponsor is no longer exposed to griefing through invalidation, and neither is the miner because the transaction will never get mined.

I believe my proposal preserves the principle of least privilege, as I explained in the minimally-privileged daemon analogy above.  What do we lose by implementing something like that instead of adding a setuid bit?  It would make sense to list the downsides of such approach compared to EIP 3074, so that we can decide if it is worth the extra risk.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> There are a couple use cases that EIP-3074 enables, which I don’t think can be implemented without some change. Synthetic EOAs, which are useful for state channels, are a really interesting unique feature of EIP-3074.

Does my proposal of adding a mandatory signature check for specific AUTHCALLs hinder state channels support?  I think it can be used the same way as EIP 3074.  The user needs to sign the latest state in any case.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Contract wallets have a lot of the same issues as EIP-3074 invokers, so I don’t think they’re a better solution.

Contract wallets share *some* of the issues but not *all* of them.  The user makes a deliberate choice to move assets to a contract wallet.  With EIP 3074 the user could be tricked to turn the wallet into a contract without moving assets or realizing what’s going on.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Thanks again for your comments, and for catching the issue with chain id! We all really appreciate the thorough review.

Thank you for your detailed reply and insightful analogies.  Always a pleasure to discuss security issues with smart people.

---

**MicahZoltu** (2021-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> We’ve went back and forth on chain id several times, and I think this seals it as necessary. Are you convinced @MicahZoltu?

No, for the same reason as before.  Don’t solve a problem on a lower layer that can be solved by a higher layer, especially when the solution involves restricting possibilities.  The goal is to build a simple and expressive instruction set, and it is up to people *using* those instructions to do so wisely.  As much as I hate it, there is a reason that the lowest level programming languages don’t do even the simplest things like overflow protection.

---

**MicahZoltu** (2021-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Old unaware wallets become compromised. Anyone using a pre-EIP-3074 wallet could be enticed to sign a benign-looking message that actually transfers its control to such extension.

IIRC, there are no popular wallets that allow arbitrary signing without enabling specific advanced features that come with dire warnings.

---

**MicahZoltu** (2021-06-16):

I replied to a bunch of specific things below, but I think you may have a misunderstanding of how most wallets work today and what they allow.  If 3074 launched today, essentially no one would be able to sign a 3074 transaction because no wallet I know of supports signing arbitrary messages, and no wallet knows about 3074 messages.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Even with EIP-3074-aware wallets that warn the user,

I believe that every wallet we have talked to has asserted that they will not be allowing their users to sign arbitrary invokers.  I think they all plan on whitelisting vetted invokers only.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> A wallet extension like EIP 3074 breaks that expectation.

I don’t think any major hardware wallet will let you sign a 3074 transaction.  TBD how exactly hard are wallets will deal with this, but I’m guessing a whitelist just like software wallets.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> If we want to require wallets to be aware, then we need a new transaction type, incompatible with old wallets, and only accept the AUTH opcode when triggered from a transaction of the new type.

See above, this is essentially the case.  No wallet will even prompt a user to sign a 3074 message today.  Wallets will explicitly need to add support.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> I rely on what I see on the hardware wallet screen, and I know that even if MetaMask is compromised it cannot abuse my EOA, now or in the future. EIP-3074 takes away that confidence and forces me to rely on MetaMask to audit and whitelist invokers.

Same as above, your hardware wallet won’t let you sign a 3074 transaction by default.  They will need to update with that functionality, and I would be very surprised if any let you sign arbitrary 3074 messages without going through some advanced configuration.

---

**SamWilsn** (2021-06-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> SamWilsn:
>
>
> We’ve went back and forth on chain id several times, and I think this seals it as necessary. Are you convinced @MicahZoltu?

No, for the same reason as before. Don’t solve a problem on a lower layer that can be solved by a higher layer, especially when the solution involves restricting possibilities. The goal is to build a simple and expressive instruction set, and it is up to people *using* those instructions to do so wisely. As much as I hate it, there is a reason that the lowest level programming languages don’t do even the simplest things like overflow protection.

I think [@yoavw](/u/yoavw) has established that it cannot be safely done at a higher level:

1. I create a thoroughly vetted/audited/perfectly secure contract which checks the chain id, called ContractA.
2. I deploy ContractA on goerli (or ETC, or BobSpongeChain) using a very special CREATE2 deployer, which allows arbitrary code to be deployed at the same address (and yes, this is 100% possible, we did it for fun a while back.)
3. I create a malicious contract, ContractB, and deploy it using the same method on a different chain at the same address. ContractB does not check the chain id.
4. I replay the authorizations given to ContractA against ContractB, gaining complete control of those accounts on the other chain.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> yoavw:
>
>
> Old unaware wallets become compromised. Anyone using a pre-EIP-3074 wallet could be enticed to sign a benign-looking message that actually transfers its control to such extension.

IIRC, there are no popular wallets that allow arbitrary signing without enabling specific advanced features that come with dire warnings.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> No wallet will even prompt a user to sign a 3074 message today. Wallets will explicitly need to add support.

Metamask allows it, without any special configuration:

[![Screenshot from 2021-06-16 15-43-35](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7ffdc3e6f28ca891b329808d06e1dea21a67a3a9_2_281x500.png)Screenshot from 2021-06-16 15-43-35760×1350 88.1 KB](https://ethereum-magicians.org/uploads/default/7ffdc3e6f28ca891b329808d06e1dea21a67a3a9)

I’m not sure if that warning is sufficiently dire.

---

**yoavw** (2021-06-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> No, for the same reason as before. Don’t solve a problem on a lower layer that can be solved by a higher layer, especially when the solution involves restricting possibilities. The goal is to build a simple and expressive instruction set, and it is up to people using those instructions to do so wisely. As much as I hate it, there is a reason that the lowest level programming languages don’t do even the simplest things like overflow protection.

And how would you prevent the cross-chain attack I described above at a higher layer?  The invoker on BobSpongeChain is perfectly secure and yet it can’t do anything about the attack on Ethereum.

In general this argument is incompatible the principle of least privilege.  Would you trust an OS where there are no kernel level protections and everything is delegated to usermode processes?  Or a blockchain where all transactions are accepted into blocks, and clients are expected to detect double-spending transactions and disregard them?  Some things are best done at the infrastructure layer.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> IIRC, there are no popular wallets that allow arbitrary signing without enabling specific advanced features that come with dire warnings.

Hmmm, is Trezor popular enough to be considered?

Let me try that with one of the Trezors I have on my desk here:

```auto
$ trezorctl ethereum sign-message $(printf '\x03some_hash') -n "m/44'/60'/0'/0/0"
Please confirm action on your Trezor device.
message: some_hash
address: 0xB46d902CF5B12B8f00c93A6fe3800CDFA4ca4ef7
signature: 0x21ceb8fdd0c8b07c1721a9d1a48365914ca90d1ded9f125208b06a0731b181e30bdb15b10e17ed3c6da2e0f509d2753c0024a10d7787294b3de6523d67949d211b
```

Well, that worked.  And my Trezor didn’t give me any warning.  Just displayed the message with the \x03 character as a benign “” at the beginning of the message, and let me sign it.

I haven’t tried with a Ledger but I believe it will behave similarly.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I replied to a bunch of specific things below, but I think you may have a misunderstanding of how most wallets work today and what they allow. If 3074 launched today, essentially no one would be able to sign a 3074 transaction because no wallet I know of supports signing arbitrary messages, and no wallet knows about 3074 messages.

Are you sure I’m misunderstanding how wallets work?  Seems that two popular wallets (Trezor and MetaMask) do sign it.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I believe that every wallet we have talked to has asserted that they will not be allowing their users to sign arbitrary invokers. I think they all plan on whitelisting vetted invokers only.

Well, at least some of them currently do.  Even if they block it in their next release, the existing ones are vulnerable.

Furthermore, I don’t want to trust their judgement on vetting invokers.  I trust them to sign transactions and messages.  As for smart contract, I’d rather be vetting them myself.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I don’t think any major hardware wallet will let you sign a 3074 transaction. TBD how exactly hard are wallets will deal with this, but I’m guessing a whitelist just like software wallets.

Well, one of them just did.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> See above, this is essentially the case. No wallet will even prompt a user to sign a 3074 message today. Wallets will explicitly need to add support.

Ditto.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Same as above, your hardware wallet won’t let you sign a 3074 transaction by default. They will need to update with that functionality, and I would be very surprised if any let you sign arbitrary 3074 messages without going through some advanced configuration.

Same as above.

But aside from the legacy-wallet issue which I hope I sufficiently established above, I think you may be disregarding my main point regarding security design and what we can learn from `setuid` vulnerabilities in operating systems in the past 30-40 years.

I believe we all agree that EIP 3074 invokers are equivalent to setuid executables.  Let’s learn from what went wrong with setuid executables and how the problem was mitigated in the last decades.  We don’t need to reinvent security when there’s an equivalent we can learn from.  We have decades of relevant security research, and there are time-proven patterns we can study.

Do you see a good reason to deviate from the established pattern here?

---

**SamWilsn** (2021-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Well, that worked. And my Trezor didn’t give me any warning. Just displayed the message with the \x03 character as a benign “” at the beginning of the message, and let me sign it.

Are we sure it isn’t prepending the `\x18Bitcoin Signed Message:\n` magic prefix? A quick google seems to suggest trezor will do that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> I don’t want to trust their judgement on vetting invokers. I trust them to sign transactions and messages. As for smart contract, I’d rather be vetting them myself.

You should always be free to do additional vetting yourself before signing anything, no?

---

**yoavw** (2021-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Are we sure it isn’t prepending the \x18Bitcoin Signed Message:\n magic prefix? A quick google seems to suggest trezor will do that.

I think that’s what they do for “`trezorctl sign-message`” but not “`trezorctl ethereum sign-message`”.  I haven’t verified it now, but I recall that in the past I signed messages to a proxy contract with trezorctl and didn’t have any issues.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> You should always be free to do additional vetting yourself before signing anything, no?

Yes, but once it is whitelisted most people wouldn’t even know that an invoker is involved.  It will appear just like any other transaction and most users won’t be aware that they’re essentially installing a wallet extension.

---

**SamWilsn** (2021-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> If EIP 3074 is merged in its current form, I’ll try to release an invoker with a subtle bug that violates this assumption under a pseudonym and see how long it remains undiscovered.

Our [testnet](https://github.com/quilt/puxi) should still be running if you want to give it a shot! I’d be curious to see what that would look like.

---

I’m going to take some time to mull over your thoughts. Something akin to capabilities would be extremely interesting to me.

I’m not convinced that enshrining single-use transaction-like packages is the way to go, but I’m certainly more open to alternatives to 3074 than I was a few days ago!

---

**yoavw** (2021-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Our testnet should still be running if you want to give it a shot! I’d be curious to see what that would look like.

heh, doing it that way would miss the point since everyone will know there’s an intentional bug to look for.  The experiment would be more fun when I publish it a bit later as part of a larger project.  ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

But think something like what I described above, with an unrelated post-nonce function that overwrites arbitrary storage cells.  Or more likely, a post-nonce delegatecall to another contract that does that, using a mapping with the same name rather than an obvious asm snippet.  (I know delegatecall doesn’t preserve AUTH but I don’t mean using it for that - just to use it to overwrite some storage cell in the invoker).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I’m not convinced that enshrining single-use transaction-like packages is the way to go, but I’m certainly more open to alternatives to 3074 than I was a few days ago!

I’m glad to hear that.  I think something like 3074 is important for use cases like account abstraction, gas sponsorship and state channels.  I just hope we can find a way to do it securely.  I’ll be happy to discuss more ways to achieve this.

---

**matt** (2021-06-17):

~~[@yoavw](/u/yoavw) I’m quite conflicted on this cross-chain attack. On one hand, what you say sounds plausible. A malicious actor *could* deploy different code to the same address on different chains. But, IMO, you left out that there would be a glaring trail in the initcode and/or the deployment transaction. But at the same time, there doesn’t seem to be any reasonable use case for cross-chain invokers…~~

edit: I made the mistake of forgetting `create` operations are not tied to the hash of the initcode. I was thinking of `create2` ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) in that case you are right, this could be a bad attack. However, if in the “guidelines for safe invokers” we state that invokers should only be deployed via create2 and their initcode should not allow arbitrary code to be loaded, it should be perfectly safe.

–

My philosophy on this is that EIP-3074 has pitfalls and it’s those pitfalls that make it so powerful. We can’t know how people will use these primitives in 5-10 years. The fact that it’s possible to prove, with absolute certainty, that an invoker cannot reach a bad state is a compelling reason for me to overlook the difficulties in creating the proof. I think the cost of proving safety is worth it, because it unlocks a rich set of functionality for EOAs. This cross-chain attack is just another checkbox to check when deciding if an invoker is safe. IMO, it’s probably one of the easiest checkboxes since it just requires looking at the initcode (the HLL code *is* available, right? right…?).

Other than that, I think my main criticism with these Linux comparisons is that *Ethereum isn’t Linux*. The things that work for Linux don’t necessarily work for Ethereum. Supporting specific privileged operations is where EIP-3074 started (and EIP-2711 and EIP-2733). Again and again, we found the burden of the new functionality did not outweigh the gains provided.

As soon as new storage reads or writes are introduced (this is what you’re saying when you say “specific privileged operations” - Ethereum has to check the “disk” to get the permissions) to an EIP, either complexity/storage costs explodes or we’re back to a rigid design whose pros usually don’t outweigh the cons. If we try to reuse things like EOA nonces, we break invariants. If we save a new nonce, we have to figure out how and where. IMO, this* is a non-starter.

*by “this” I mean stateful checks. There are some *stateless* checks that we can do if there is sufficient desire. I am generally against them, but they are possible without significantly modifying EIP-3074. For example:

- we can add a chainid parameter to the AUTH message
- we can add a block_number or epoch to the AUTH message, capping the amount of time a signature is valid
- … probably others!

But again, these are generally against my philosophy of EIP-3074.

---

**danfinlay** (2021-06-17):

This has been a very fun read, thank you to [@yoavw](/u/yoavw) for so many specific examples and even some alternative approaches.

I’ll be very curious to see if Trezor is prepending a prefix if not. If it’s not, that’s pretty bad. I think one of the strongest take-aways from this thread for me is “we should do a formal and systematic review of wallets’ behavior for this type of signature”

I agree the MetaMask signature warning could be more dire (particularly in a 3074 environment), but it does say in red, that this signature risks entire control of the account. And we wrote that before 3074, so I’m going to count it pretty prescient, even though it could be tighter.

> Contract wallets share some of the issues but not all of them. The user makes a deliberate choice to move assets to a contract wallet.

There are now multiple consumer contract wallets that are being promoted to consumers who do not disclaim themselves as having contract bug risk. Vitalik himself promotes contract accounts as a safer alternative to EOAs. We’re already well into the “unspoken account-wide contract risk” era. You could compare that behavior to a wallet signing 3074 messages without mentioning it to the user, for convenience sake. That’s already the wallet environment, so to some degree, I think this argument is trying to prevent a type of risk that is already taken.

That’s a common theme I find when debating delegation: Can we keep people safe, by preventing certain types of delegation? I am of the camp that if a user has the ability to do something, they already have the de-facto ability to delegate it, it might just be inconvenient.

> I don’t want to trust their judgement on vetting invokers. I trust them to sign transactions and messages. As for smart contract, I’d rather be vetting them myself.

I think it’s reasonable for a wallet to help users know when they’re taking on contract risk, and I’d gladly make sure that MetaMask lets users avoid this kind of risk entirely, but like with contract accounts, it’s already common for consumer products to integrate contract risk for their users without really emphasizing or mentioning it.

> I believe we all agree that EIP 3074 invokers are equivalent to setuid executables. Let’s learn from what went wrong with setuid executables and how the problem was mitigated in the last decades. We don’t need to reinvent security when there’s an equivalent we can learn from. We have decades of relevant security research, and there are time-proven patterns we can study.

I’m not that familiar with the setuid executable example, and I’d love some links to the example attacks and mitigations. From the earlier descriptions in this thread, it sounds like when you’re using chroot, for example, you’re still trusting a trusted computing base to restrict the behavior of subsequent programs being executed. In a way, this sounds a lot like a 3074 invoker in its current form: You trust an invoker, so it can attenuate control to other external scripts.

> there doesn’t seem to be any reasonable use case for cross-chain invokers…

One hypothetical could be “I want to delegate this account’s control to this other key, on every network”.

This spectrum between the tradeoffs between user control and safety seems like a very well defined philosophical disagreement. I generally think that the Ethereum platform exists far on the “dangerously free” end of this spectrum, and some of the arguments for “keeping security at the protocol layer” remind me of arguments in favor of per-app blockchains over an application-capable chain like Ethereum. I always figured bugs could exist at the protocol layer, too, so you might as well keep the entire platform more dynamic, but this seems like a distinction that the Ethereum community needs to decide for itself.

Anyways, just sharing my initial thoughts.

I think we should systematically review wallets that sign arbitrary bytes, and for any that do (MetaMask, Trezor?), consider the attack surface (can Ðapps ever propose an arbitrary signature to it? Does it receive a salient warning? How common are users who are willing to paste signature bytes from strangers into outdated signers?)

---

**SamWilsn** (2021-06-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> SamWilsn:
>
>
> Are we sure it isn’t prepending the \x18Bitcoin Signed Message:\n magic prefix? A quick google seems to suggest trezor will do that.

I think that’s what they do for “`trezorctl sign-message`” but not “`trezorctl ethereum sign-message`”. I haven’t verified it now, but I recall that in the past I signed messages to a proxy contract with trezorctl and didn’t have any issues.

So this is far from scientific, but I tried your signature, a signature from `personal_sign`, and a signature with `eth_sign` on [MEW](https://www.myetherwallet.com/interface/verify-message).

Assuming I did all three parts correctly, since MEW validated the trezor signature and the `personal_sign` signature, but not the raw `eth_sign` signature, we can assume the trezor signature includes the magic prefix.

### Trezor

```json
{
    "address": "0xB46d902CF5B12B8f00c93A6fe3800CDFA4ca4ef7",
    "sig": "0x21ceb8fdd0c8b07c1721a9d1a48365914ca90d1ded9f125208b06a0731b181e30bdb15b10e17ed3c6da2e0f509d2753c0024a10d7787294b3de6523d67949d211b",
    "msg": "\u0003some_hash"
}
```

Gives

> 0xB46d902CF5B12B8f00c93A6fe3800CDFA4ca4ef7 did sign the message: some_hash

### personal_sign

```json
{
    "address": "0x285608733D47720B40447b1cC0293A2e4435090e",
    "sig": "0x0112651f89e8eaaf0331db857e23f77fe493249cf7d75f0c06ca1ed5e08581c340f0ba8713873cd65bba1d00c6cbdedb235e32130700a3c8f88d8858022eb90c1b",
    "msg": "\u0003some_hash"
}
```

Gives:

> 0x285608733D47720B40447b1cC0293A2e4435090e did sign the message: some_hash

### eth_sign

```json
{
    "address": "0x285608733D47720B40447b1cC0293A2e4435090e",
    "sig": "0x0667ebe3419e77d411844ab485027580977fa47259ab9780620043bfbaa88a961e188f287ad519fc11d9ac483b79202294ad3bddf2f546474e17ca40d1b43f431b",
    "msg": "\u0003some_hash"
}
```

Gives:

> Signer address is different than the derived address!

To use `eth_sign`, I had to manually hash the message, which came out to `0x2ff859a3a103a3c50abafb36eaf0ff4a80de20f68766573c10397d1199154515`. **This is probably the part I’m most unsure of.**

---

**yoavw** (2021-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> @yoavw I’m quite conflicted on this cross-chain attack. On one hand, what you say sounds plausible. A malicious actor could deploy different code to the same address on different chains. But, IMO, you left out that there would be a glaring trail in the initcode and/or the deployment transaction. But at the same time, there doesn’t seem to be any reasonable use case for cross-chain invokers…

What kind of glaring trail would you expect to find in the deployment?  I don’t think I left anything out.  There shouldn’t be any.

To demonstrate it, I quickly hacked together a couple of invoker-like contracts, one that checks commits to verify the call data and prevent replays, and one that doesn’t.  I deployed the legitimate one [on kovan](https://kovan.etherscan.io/address/0x2f37c1c864932c425be17e73e9f7d3edc28af010#code) and the malicious one [on ropsten](https://ropsten.etherscan.io/address/0x2f37c1c864932c425be17e73e9f7d3edc28af010#code), at the same addresses (0x2f37C1C864932c425Be17E73e9F7d3edc28AF010).  The contracts are available with verified code on etherscan so you can inspect their deployment and transactions:

See anything detectable signs of fraud in the deployment of the legitimate invoker on kovan?

And I sent a couple of transactions to demonstrate the attack.  I know it’s nowhere near a full simulation of EIP 3074 but the EIP3074Simulation contract implements the security checks that matter for this demo.  `authTest(bytes32 commit, uint8 _v, bytes32 _r, bytes32 _s) internal returns(address signer)` verifies that the commit is signed along with the address of the invoker, returns the signer and assigns it to `authorized`.    `function authcallTestAndReset(string memory what) internal returns(bool success)` doesn’t actually call anything but it verifies that `authorized` is set, and performs `what` on behalf of `authorized` (actually just emitting `SuccessfulExecution(address who, string what)`).

Both invokers use that contract without changes, to simulate an EIP 3074 call.  But the contracts themselves are different despite having the same address:

`BenignInvoker` on kovan implements replay protection and ensures that `commit` really represents `what`.  If you look at the first three transactions I sent it, you can see that the first one (0x324d4bc54319334fb92f4cd5efa93ab37d06e2f95f6fd79395777338a2d8c54d - sorry I can’t link as this forum only allows two links per post) succeeded, and if you look at the decoded input you can see that it executed “legitimate call” on behalf of the signer.  The second transaction (0xcf7d3e0154af2acaed3ee9a1b7adfc3d97a0e61b3ca40ea098cb2c1e6568393f) reverted on a replay of the same call, and the third one (0x9869df67fa53fe003265bc09dcc800e2bc08fb75cb0aae189849627404784619) reverted on an attempt to change the `what`.  So this invoker seems legit.

`MaliciousInvoker` deployed on ropsten omits the checks around `commit` (no replay protection, no check to associate `what` with `commit`).  I replayed the commit and signature from the first kovan transaction above, replacing just the `what`, and sent a couple of transactions malicious `what`s.  If you look at one of them, e.g. 0xb331067354431f085ea300cf748df1416a93430f858402f2595303c74c69bcb0, and decode the input, you’ll see that it is identical to the kovan transaction except for having a malicious `what`.

The point of this demo is to show the cross-chain attack I was talking about.  I think it’s impossible to find anything illegitimate on the kovan invoker, and yet I’m able to perform any action on behalf of the signer on ropsten.

I hope this clarifies the attack and shows why it would be impossible to mitigate without checking chainid in AUTH.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I think the cost of proving safety is worth it, because it unlocks a rich set of functionality for EOAs.

I don’t think it’ll be possible to prove safety of an invoker when it is made so powerful.  But the question I keep coming back to, is what functionality do we lose by making it less powerful and have the user actually sign each AUTHCALL?  It clearly makes the invoker less risky, so we should compare the two approaches and see what we lose by taking away some of that power.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> IMO, it’s probably one of the easiest checkboxes since it just requires looking at the initcode (the HLL code is available, right? right…?).

Well, the initcode is available in the contracts I linked above.  I don’t think you can tell that something is wrong by looking at the legitimate one I deployed on kovan.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Other than that, I think my main criticism with these Linux comparisons is that Ethereum isn’t Linux. The things that work for Linux don’t necessarily work for Ethereum.

I used the Linux analogy because Sam described it as setuid (and he’s totally right about it).  Since this is the closest analogy, it made sense to draw conclusions from problems it created and how they were mitigated over the years.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Again and again, we found the burden of the new functionality did not outweigh the gains provided.

I don’t think we ever added something with that level of risk, but perhaps I’m wrong.  In any case my philosophy around Ethereum is that we can add new functionality but need to be much more prudent than most other systems.  This is not a website, so the Facebook approach of “move fast and break things” doesn’t fit.  We should weigh the alternatives and find the least risky way to achieve the goal.  I’m not sure EIP 3074 reaches that bar at the moment, but I do think it could with some changes.  What I’m trying to do is start a public discussion about the pros and cons of various approaches, so that the community can determine the right trade-offs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> *by “this” I mean stateful checks

I’m also talking about stateless checks.  Specifically, check the same things that you already intend to check on a `commit`, but do it at the protocol level rather than the invoker.  Enforce security in the infrastructure, not an individual contract.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> But again, these are generally against my philosophy of EIP-3074.

That’s the crux of the matter.  The specific attacks we’re discussing can all be mitigated one way or another.  The real discussion is about that philosophy.  Whether the protocol should be opinionated and enforce the principle if least privilege, or whether we delegate security to a smart contract.  My preference is the former, yours seems to be the latter.

That’s fine, we don’t have to share the same philosophy.  I highly respect you and the rest of the authors if this EIP, as well as the other commenters in this thread, and I believe we are all working in good faith to make Ethereum better.

The best way to decide is to discuss pros and cons, and let the community decide.  It would be helpful if we list some use cases that break if we enforce at the protocol level instead of the invoker, and then we can discuss whether they justify the increased risk.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I’ll be very curious to see if Trezor is prepending a prefix if not. If it’s not, that’s pretty bad. I think one of the strongest take-aways from this thread for me is “we should do a formal and systematic review of wallets’ behavior for this type of signature”

I haven’t verified, but there’s a good chance it’s actually a message format and not directly signing the transaction (unlike Metamask which does).  Still, we’re diving into specifics (e.g. which wallets currently support such messages).  Any specific case can be mitigated, including the attacks I demonstrated.  The bigger question is whether EIP 3074 really needs to be that powerful, or whether we can achieve much of the same value with a lower risk.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I am of the camp that if a user has the ability to do something, they already have the de-facto ability to delegate it, it might just be inconvenient.

Would it be much more inconvenient to the user if the specific call has to be signed instead of a blank authorization?  The wallet could still hide that from the user, but it wouldn’t be as vulnerable to invoker bugs since replay and modifications will be prevented at the protocol level.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I’m not that familiar with the setuid executable example, and I’d love some links to the example attacks and mitigations.

It would be quite time consuming to come up with a full list, but if you search “setuid” on old bugtraq archives and CVEs, you can see numerous cases.  And then you can see that their frequency starts dropping, as more projects move away from using setuid in favor of daemons that drop privileges.  There was a steep decline in these bug reports when Linux completely banned setuid scripts, which broke many projects until they switched to a different model, but greatly improved security.  It was controversial at the time, but in retrospect it was the right call.  (As an anecdote, you could get root access with such scripts by just setting IFS=/ when invoking them, since it would run “bin” in the current directory as root, instead of /bin/sh, and this worked on almost all Unix based systems for a few years).

I do recall some Usenix Security papers that analyzed the different approaches in the early 2000’s but I haven’t scanned for these old articles.  Personally I’ve been involved in this specific space for the past 30 years so it seems obvious to me, but going through privilege escalation CVEs and seeing how many of them were due to setuid might help everyone realize the risk involved.

Unfortunately even today we haven’t fully gotten rid of this problem.  The CVE I linked earlier in this thread, from Jan 2021, demonstrates an attack against sudo, one of the last remaining setuid binaries.  It’s hard to implement sudo without setuid so it keeps getting hit every couple of years.

As for the mitigation, different approaches were tried, but the prevailing one is daemons that live in a “cage” and only retain the specific capability they need.  This is pretty much the standard.  In the past few years, since Linux added the unshare(2) syscall, containers like docker started also creating separate namespaces that made things even more secure.  We don’t have an equivalent in Ethereum but it’s interesting to think about it.  Ethereum strives to be the world computer, and can benefit from past OS security research.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> you’re still trusting a trusted computing base to restrict the behavior of subsequent programs being execute

Yes, but the TCB in this case is the kernel which enforces the chroot, the mandatory permissions, the capabilities subsystem, selinux rules, etc.  The kernel is verified by more security people than most other parts of the system.  The equivalent here would be Ethereum as the TCB.  Ethereum itself (and EVM specifically) has been verified and is continuously verified by many security people.  Adding 3rd party invokers to the TCB would weaken that model, just like adding a setuid binary weakens the Linux TCB.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> In a way, this sounds a lot like a 3074 invoker in its current form: You trust an invoker, so it can attenuate control to other external scripts.

This is pretty much the definition of setuid (although setuid was banned for scripts by the Linux kernel due to numerous vulnerabilities, and can now only work with compiled binaries).  But since it increases the TCB, it makes sense to consider different approaches that wouldn’t.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> One hypothetical could be “I want to delegate this account’s control to this other key, on every network”.

But then how would you mitigate the attack I demonstrated above?  I don’t think this use-case justifies putting everyone else at such high risk.  It would be almost trivial to exploit this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> remind me of arguments in favor of per-app blockchains over an application-capable chain

Why?  Per-app blockchains are inherently weaker due to having less participants.  Ethereum’s turing-completeness made it attractive enough to become secure.  There’s no conflict.

The fact that Ethereum gives us more freedom doesn’t mean that we should become careless.  Any EIP needs to be scrutinized and considered against the alternatives.  I’d be interested in an analysis of the use-cases that this EIP comes to solve, and whether this is the least risky way to solve them.  So far I haven’t seen a use-case that can’t be solved while still letting the user retain the signatory power over the EOA.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I think we should systematically review wallets that sign arbitrary bytes, and for any that do (MetaMask, Trezor?), consider the attack surface (can Ðapps ever propose an arbitrary signature to it? Does it receive a salient warning? How common are users who are willing to paste signature bytes from strangers into outdated signers?)

As I noted above, I think this is diving into a specific case.  I think we should start from a higher level, document the use cases this EIP aims to solve, and then dive down to mitigating specific issues in specific solutions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> To use eth_sign, I had to manually hash the message, which came out to 0x2ff859a3a103a3c50abafb36eaf0ff4a80de20f68766573c10397d1199154515. This is probably the part I’m most unsure of.

I haven’t researched this beyond the snippet I pasted a few messages ago.  Considering the above, I suspect that Trezor is not signing a raw message.  But since the legacy wallets issue is not the primary issue (just one symptom of possibly giving too much power to the invoker), I think we should focus on the high level first.

Let’s try to get to a design that solves the required use-cases with the lowest risk possible, so that we end up with the most secure version of EIP 3074.  When we achieve that, we can go through specific issues (whichever will be left) and see how significant they are and what can be done about them.  And finally make a decision on the trade-offs around the ones we can’t mitigate.

Right now I think this thread is mostly debating that last part (trade-offs), treating EIP-3074 as a take-it-or-leave-it proposition and assuming that we just need to decide if the risk is worth it.  But I think we should explore improving the design and then maybe we won’t need to debate trade-offs.

---

**matt** (2021-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> What kind of glaring trail would you expect to find in the deployment?

I retracted my above comment on this, I realize I was only thinking of the `create2` case. In the case of `create` you’re right, there is no way to know and we have to just trust the deployer. This of course is not acceptable.

If we add the requirement that invokers must only be deployed via `create2` then that should no longer be an issue. The init code will clearly show if it can sideload code. However, after some more discussion, I think we’re going to put chainid into the `auth` msg. You presented a compelling argument and although we could tell people to only deploy via `create2`, we’ve come up with no use cases for multi-chain messages.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> I’m also talking about stateless checks. Specifically, check the same things that you already intend to check on a commit, but do it at the protocol level rather than the invoker. Enforce security in the infrastructure, not an individual contract.

Things like `chainId` and `blockNumber` can be checked statelessly, because they’re already easily available in the current executing context. There are also no other interpretations of them.

`nonce` is different. There are many different schemes for replay protection. For example, instead of a sequential nonce you could have a map of tx hash to bool. Enshrining specific nonce mechanisms makes it difficult to have new ones. But the main issue is *where* do you even store this data? Can’t use EOA nonces because they’re already used by the tx pool to determine tx validity. You could have special precompile with storage, but this would be the first time that’s been done. This is how this EIP actually started, but then we realized the EIP was unlikely to be accepted if it did something weird like that. Finally you could modify the trie to add a new account type / field. Trie changes are very difficult to pull off and making it a prerequisite for the EIP essentially means it won’t be scheduled anytime soon. Plus, none of these changes are as flexible as just allow invokers do arbitrary things.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> The real discussion is about that philosophy.

IMO Ethereum’s philosophy [has always been](https://blog.ethereum.org/2015/07/05/on-abstraction/) to prefer abstraction over specific implementation when possible.

---

**yoavw** (2021-06-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Things like chainId and blockNumber can be checked statelessly, because they’re already easily available in the current executing context. There are also no other interpretations of them.

So can `to` and `calldata`.  There’s little downside in verifying that they’re signed by the EOA.  That would remove most attack vectors except for replay.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> nonce is different

Right.  That’s the only one where there’s a real downside.  The most secure option is to make it part of the protocol, e.g. by adding to the trie.  But I can see why you want to avoid that for practical reasons.  Another option is to use a very simple smart contract that implements the same nonce protection as the EOA one, using its own storage.  Technically it doesn’t need to be a precompile, although a precompile with storage has been suggested before.  [EIP-2935](https://eips.ethereum.org/EIPS/eip-2935) does that in a way, to save historical block hashes.

While such nonce is the most secure option, it has a clear downside since it is opinionated about the kind of replay protection used, and prevents different protection schemes that would allow better parallelization, more efficient batching, etc.

Another option, less secure but more flexible, is to use multiple storage-based replay protection contracts and whitelist them through EIPs.  The AUTH opcode will get an address of a replay protection scheme and a nonce for it.  AUTH will verify this tuple along with the rest (`to`, `calldata`, `chainid`, etc.) and then each AUTHCALL would call that.

Each such replay protection contract will be audited by the community and approved through an EIP so they’ll have to meet a higher bar than normal contract.  And even if a bug is discovered in one, the implications will be a replay at worst, rather than arbitrary calls on behalf of the EOA.

The least secure option would be the same as above, but without a whitelist.  Let each invoker use its own replay-protection contract.  It is likely that some of them will be buggy, but still less likely than an invoker having a bug, and with less severe implications since it’s just the replay protection rather than the entire invoker.

I’m inclined to suggest the whitelist-through-EIP approach since it’ll enable the same functionality we get with EIP 3074 with as little security risk as possible.

As far as I can tell, an AUTH that checks the signature on everything (including the nonce and the contract that checks it), and ensures that this contract is in the whitelist, would let us achieve anything that EIP 3074 gives us, with a much lower risk.

Anyone will be able to implement an invoker, while leaving the user in control by signing each call.

And anyone would also be able to come up with a new replay protection scheme, but would have to wait for the next fork to whitelist it.

Do you see any important EIP 3074 use-cases that this scheme can’t support?

---

**matt** (2021-06-20):

You’ve laid out 3 options here:

1. Max security, put replay protection info in trie.
2. Medium security, implement replay protection in separate smart contract and allowlist via EIP.
3. Low security, implement replay protection in separate smart contract and use without allowlist.

Like I mentioned, **option 1)** is basically a non-starter. EIP-2935 received similar push back.

**Option 2)** is at odds philosophically with Ethereum. The only time we’ve done something similar to protocol-level allowlisting is with precompiles. This has been a major pain point in core development. Everyone wants *their* precompile in the next hard fork. Admittedly, precompiles are usually difficult to audit since they are usually implementing specific cryptographic primitives. But regardless, there is [significant desire](https://ethereum-magicians.org/t/evm384-feedback-and-discussion/4533) to allow people to write efficient cryptographic primitives without being blocked by hard forks and ACD.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Do you see any important EIP 3074 use-cases that this scheme can’t support?

No, this should be able to support all use-cases. Please note, this will inherently be more expensive due the additional contract call and be more complex to handle the edge cases.

**Option 3)** is really no different functionally than the current proposal of EIP-3074. Yes, the parameters of `AUTH` change slightly, but invoker implementers can just deploy their replay logic into a separate contract.

–

I argue that option 2) is equivalent to how we want EIP-3074 to be used in practice. If wallet developers do allowlist certain “safe” EIP-3074 invokers (like they’ve indicated), then the only invokers people will be able to use are the ones that have been “decided” as safe. I don’t see why forcing core devs to debate and decide on this is better than wallet developers doing the same.

If we don’t trust the developers of the wallet we use to upgrade their software securely, I think we have bigger problems.

---

**yoavw** (2021-06-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Option 2) is at odds philosophically with Ethereum

AFAIK there’s no precedent in Ethereum for anything as powerful as setuid, so it’s hard to draw a philosophy from other precompiles.  EIP 3074 would be the equivalent of adding support for additional signature schemes (e.g. BLS), but instead of baking it into the protocol or into precompiles, allow anyone to deploy a contract that implements a new signature type which would work with any EOA for transacting with unaware contracts.  I doubt that would be within Ethereum philosophy either.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> No, this should be able to support all use-cases. Please note, this will inherently be more expensive due the additional contract call and be more complex to handle the edge cases.

Yes, it adds the extra cost of an additional CALL.  I think it’s worth the significant risk reduction.

As for edge cases, what kind of edge cases would it complicate?  I would actually expect it to simplify things because it decouples replay protection from the rest of the invoker logic.  The replay protection will have a very simple ABI.  It just receives an opaque nonce signed by an EOA (as part of the AUTH message), checks whether this nonce is accepted, and “burn” that nonce.  If it fails for whatever reason (fails the nonce check or runs out of gas) the AUTH call reverts.  There seems to be little room for edge cases.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Option 3) is really no different functionally than the current proposal of EIP-3074.

From security perspective it is different.  EIP-3074 currently gives the invoker a blank check which can be easily abused.  **option 3** only enables replay.  A malicious invoker combined with a malicious replay-verifier could, at worse,  replay a transaction previously signed by the EOA for the same chainid.  Whereas with the current EIP-3074, the invoker could make any transaction on behalf of any EOA that ever signed a message to it.

I’m less keen on **option 3** because it does enable replay attacks by a malicious replay-checker, so I think it should be protected by an “EIP-shield”.  But even without the EIP protection, it’s still much more secure than the current proposal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I argue that option 2) is equivalent to how we want EIP-3074 to be used in practice.

I think it’s not equivalent.  See the explanation above.  With option 2, a malicious/buggy invoker can do much less damage than with EIP 3074.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> If wallet developers do allowlist certain “safe” EIP-3074 invokers (like they’ve indicated), then the only invokers people will be able to use are the ones that have been “decided” as safe.

This moves the power from the community (in the form of the public EIP process) to the wallet maintainers.  The maintainer of a widely used wallet gets the power to set the standard without going through the scrutiny of the EIP process.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I don’t see why forcing core devs to debate and decide on this is better than wallet developers doing the same.

The public process may be inefficient, but it has the advantage of being public.  It’s the community’s way to decide for/against something.

The congress with all its debates is also an inefficient way to set policy, but replacing it with an efficient private company seems too risky.

---

**matt** (2021-06-22):

It seems like we fundamentally disagree on the philosophy of Ethereum. It’s unlikely my position on the topic will change, so we can set aside that disagreement for now.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> As for edge cases, what kind of edge cases would it complicate?

In **option 2)**, if you require `AUTH` perform a call-like operation into a replay protection contract you’ll need to specify the interface, like you said. This complicates the consensus specification, because right now it does not need to be specified at the consensus-level.

The main edge case I have in mind is what happens if someone calls the replay protection precompile/contract independently of `AUTH`? How can you securely pass data to the replay protector from `AUTH`? Do you need to do a second `ecrecover` or do you bind the replay protection to `CALLER` or do you magically shuttle it to the precompile? Could this lead to a sponsor being griefed? Should that even be considered by the protocol?

These aren’t unanswerable questions, but it certainly doesn’t simplify things.

> From security perspective it is different. EIP-3074 currently gives the invoker a blank check which can be easily abused. option 3 only enables replay. A malicious invoker combined with a malicious replay-verifier could, at worse, replay a transaction previously signed by the EOA for the same chainid. Whereas with the current EIP-3074, the invoker could make any transaction on behalf of any EOA that ever signed a message to it.

As you describe **option 3)** above, it is *no different* from EIP-3074 from security perspective. A malicious replay protector can say every nonce is valid. At that point, the malicious invoker again has a “blank check”. There is nothing forcing either the invoker or replay protector to check any part of the `commit`, where the actions are actually specified. So if a user can be forced to interact with a malicious invoker, they are at equal risk as with EIP-3074 as it’s written.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> I think it’s not equivalent. See the explanation above. With option 2, a malicious/buggy invoker can do much less damage than with EIP 3074.

A malicious invoker under **option 2)** has the opportunity of 1 blank check, whereas **option 3)** has N blank checks. After that nonce is burned in **option 2)**, the damage is done.

However, if you can trick a user to signing a tx to a bad invoker, it’s safe to assume you can trick them into signing an arbitrary transaction. I’ve stated on multiple occasions that the argument “but the worst that can happen is one bad tx” is a very weak counter argument to batching. Batching *is* coming. Whether it’s via meta-txs, ERCs, or EIP-3074. When that time comes, one bad signature will be able to empty an EOA.

Even if you disregard the fact that batching is coming, I don’t think “security by diversification” is a strong argument that 1 blank check is acceptable. I [investigated](https://hackmd.io/@matt/BknnAnyNu) this more a while back.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> matt:
>
>
> I don’t see why forcing core devs to debate and decide on this is better than wallet developers doing the same.

The public process may be inefficient, but it has the advantage of being public. It’s the community’s way to decide for/against something.

The congress with all its debates is also an inefficient way to set policy, but replacing it with an efficient private company seems too risky.

This is an unfair comparison. You’re framing it like “wallet developers will hold all the power privately and the community will be helpless”. EIP-3074 allows *permissionless* innovation. If the wallet developers block the adoption of a certain invoker, the community could fork the wallet and add it to the whitelist. Or they could build a new wallet. This is *far* easier than forking Ethereum to bypass the core developers.


*(24 more replies not shown)*
