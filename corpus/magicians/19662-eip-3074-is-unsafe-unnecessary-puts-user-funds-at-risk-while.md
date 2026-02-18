---
source: magicians
topic_id: 19662
title: EIP 3074 is unsafe, unnecessary, puts user funds at risk while fragmenting UX, liquidity and the wallet stack
author: MrSilly
date: "2024-04-15"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-3074-is-unsafe-unnecessary-puts-user-funds-at-risk-while-fragmenting-ux-liquidity-and-the-wallet-stack/19662
views: 3432
likes: 24
posts_count: 31
---

# EIP 3074 is unsafe, unnecessary, puts user funds at risk while fragmenting UX, liquidity and the wallet stack

There have been mountains of text written on this forum and elsewhere about EIP 3074, but getting to the signal through the noise can be hard. Here’s a short summary of why EIP 3074 is a bad idea:

- User funds at risk: One signature and you lose everything. Relies on wallets preventing this, and users understanding the new security model. Fragile assumptions. Hardware wallets won’t protect users unless their UX is rehauled
- Dangerous lack of security controls: to enable use cases such as gas abstraction EIP 3074 requires giving full access to all of your assets. EIP 3074 is trust maximized. It is an all or nothing “sudo root” access model. This is unlike  4337’s trust minimized design where paymasters are incapable of stealing your funds
- Confusing security model that’s harder for users to understand: EIP 3074 makes the EOA security model much harder to understand, even for experts, but especially for normal humans. Violates the principle of least surprise (see more below)
- Doesn’t improve UX overall: because losing all of your funds to a scam is not good UX. The benefits EIP 3074 claims to provide can be achieved more safely in other ways
- Other security problems: adds new authorization methods to an EOA while being incapable of revoking the old hardwired EOA key. Many potential problems with breaking dapp assumptions around EOAs. Needs more thorough auditing
- Permissioned innovation:  dapp devs won’t be able to develop their own invokers since all wallets will whitelist them once users start getting scammed.
- Creates two incompatible wallet stacks: This will fragment UX and liquidity even more
- Unnecessary: given that account abstraction (ERC 4337) is already on mainnet and we are on the way to having gas efficient native account abstraction in the protocol and standardized on all the rollups
- Enshrines friction and bloat: Instead of helping us on the path to account abstraction, EIP 3074 enshrines EOAs and adds an ugly layer of cruft to the protocol that we will never be able to get rid of. As soon as it gets in, the campaign for more kludgy EIPs built on top of it will start. Patches to patches to patches, all the way down.
- Incompatible with inclusion lists: which we need to mitigate how easy it is now to censor transactions now with centralized block building
- Strategically bad second order effects: promotes centralized solutions as the path of least resistance (eg centralized meta transaction relays, too big to fail monopoly around Metamask’s invoker contract)
- Credit for these arguments goes to various critics of EIP 3074 including:

Vitalik: “we should be moving beyond EOAs not enshrining them”
- Yoav Weiss, EF security fellow and architect of 4337: “ERC 4337 vs EIP 3074”
- Ansgar @ EF researcher: one of the original EIP 3074 authors
- Charles Guillemet, CTO at Ledger
- Martin Köppelmann Gnosis co-founder
- Itamar Lesuisse: Founder and CEO of the Argent wallet
- Patricio @ Founder at POAP

## Why is it a problem that EIP 3074 violates the principle of least surprise?

The general problem with losing the principle of least surprise is that the user expects a transaction to happen once, now.  With 3074 it becomes “the transaction may happen any number of times now or in the future unless the invoker enforces replay protection”.

In addition there’s the issue of opaqueness (unlike a batching transaction type). From looking at the transaction, it’s impossible to know exactly what it’s going to do.   Maybe the invoker transfers the tokens as you requested but also sets an allowance for someone to withdraw more in the future.  Or maybe it sponsors your gas for some transaction but also delegates your governance tokens in some project to a malicious delegate who will silently collect a lot of voting power by sponsoring people’s transaction in some other protocol.

Users won’t notice since they retain their tokens.  They just delegated their voting power to an attacker but are not affected directly.  Or maybe an invoker is an upgradable proxy that is safe now, but in the future it’ll change its implementation to do something else and reuse your old AUTH.  Easy to come up with scary scenarios.

## Community feedback

[![](https://ethereum-magicians.org/uploads/default/original/2X/6/6b9471d6790a5f71f148598303ce41cad64d0861.jpeg)](https://x.com/P3b7_/status/1778720516959785376)

[![](https://ethereum-magicians.org/uploads/default/original/2X/2/262821f023d2418affeac48255eaf1b0ec67a1c5.png)](https://x.com/ryanberckmans/status/1778814106633372044)

[![](https://ethereum-magicians.org/uploads/default/original/2X/9/99e1a927dd8c1dd252ee22abd457bce094dbb5a1.png)](https://x.com/LefterisJP/status/1778460333478211744)

[![](https://ethereum-magicians.org/uploads/default/original/2X/7/7b50211799c446c743491b592044269ca0c56157.png)](https://x.com/0xCygaar/status/1778522812451586554)

[![](https://ethereum-magicians.org/uploads/default/original/2X/c/ccf59446b8e67a5433539ab5b1ebe087705f113f.png)](https://x.com/koeppelmann/status/1778653049302491499)

[![](https://ethereum-magicians.org/uploads/default/original/2X/6/601cd5d85bf362ed6f5ac16166f14be257cfc3d9.png)](https://x.com/koeppelmann/status/1778807483202457876)

[![](https://ethereum-magicians.org/uploads/default/original/2X/1/161897a7004a5ba6be87cfa4e527e2b7b3e44aa4.jpeg)](https://x.com/0xCygaar/status/1778838614798958776)

[![](https://ethereum-magicians.org/uploads/default/original/2X/e/e2e3c0a9102342fb502126ff0147b8e1fa1d0fd7.jpeg)](https://x.com/P3b7_/status/1778779812498231699)

[![](https://ethereum-magicians.org/uploads/default/original/2X/d/dbc14cfd5148f67ea9cb1849336ba7dea580877b.png)](https://x.com/itamarl/status/1778698669992149393)

[![](https://ethereum-magicians.org/uploads/default/original/2X/6/6ab15443c87d9229630c7c80d0206e1f622afb81.png)](https://x.com/naruto11eth/status/1778825028827840767)

[![](https://ethereum-magicians.org/uploads/default/original/2X/6/608868fd2a95814ab6e5e2fca1eab7f6665d154f.png)](https://x.com/SeanMacAonghais/status/1778709836944875881)

[![](https://ethereum-magicians.org/uploads/default/original/2X/7/758f9c6364ab37ecd0481d9ef0da051c01e2cd66.png)](https://x.com/pcaversaccio/status/1778656545087103265)

[![](https://ethereum-magicians.org/uploads/default/original/2X/4/48a2321d57cde65642c31efffd3482900cca9074.png)](https://x.com/Mudit__Gupta/status/1778666806653456869)

[![](https://ethereum-magicians.org/uploads/default/original/2X/e/e08f5708391e34ca4ede96c857c6d230afdd2347.jpeg)](https://x.com/jadler0/status/1779167896423264437)

[![](https://ethereum-magicians.org/uploads/default/original/2X/a/a94852c02a4dff4a4bd0aff6d79d8eebdcee3d01.png)](https://x.com/koeppelmann/status/1778552021181702303)

## Replies

**335767028Tian** (2024-04-15):

An attack maybe like this, an evil contract that contains auth code pretend to be an normal transaction, actually this contract is an invoker , since the replay protection and the validation are all implemented by invoker, this evil contract can do nothing then it can totally control the assets of the user.

---

**wjmelements** (2024-04-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) Liraz Siri:

> (ERC 4337) is already on mainnet

4337 is garbage and a waste of gas. Many of your criticisms also apply to it.

---

**MrSilly** (2024-04-16):

> garbage and a waste of gas

Very good arguments Sir! I concede

---

**wjmelements** (2024-04-16):

As evidence, less than 10% of “account abstraction” transactions use it. Though I haven’t calculated it, I suspect the number is less than 1%.

---

**MrSilly** (2024-04-16):

Not sure I understand you, but I suspect you may have your own unique definition of “account abstraction”, like maybe all meta transactions that have their gas sponsored? Otherwise, since 4337 is the only account abstraction solution, it would always be getting 100% of AA transactions.

If you’re done with name calling and are interested in understanding what the rest of us mean by account abstraction, please read [ERC 4337 vs 3074: a false dichotomy](https://notes.ethereum.org/@yoav/erc-4337-vs-eip-3074-false-dichotomy#ERC-4337-vs-EIP-3074-False-dichotomy)

---

**wjmelements** (2024-04-16):

4337 proponents have to have a narrow definition for AA because everything else is so superior that 4337 has to exclude them as valid solutions to be promising itself. But the main goal of AA is to move ownership of assets to smart contract accounts so that when quantum computing breaks EOAs our assets are safely held by upgradeable accounts that can discard those keys easily. There are other advantages of smart contract accounts such as batching but gas abstraction is not strictly essential, and doesn’t make sense for many use-cases. I accept many more things to be AA than you do therefore, and by my own standard I have sent over half a million AA transactions.

I agree that 3074 isn’t a step toward account abstraction. The EIP recognizes this: “This approach is also not immediately compatible with account abstraction”. Its accepted form is a rump of its original vision; it used to be replayable but now it has to be signed repeatedly. But the final version is still useful and am looking forward to its application to limit order intents in particular. It can abstract gas which is nice. However, 4337 proponents will be mad because their proposal is becoming even less relevant.

---

**tomteman** (2024-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> gas abstraction is not strictly essential, and doesn’t make sense for many use-cases

That opinion has no basis if you look at the actual onchain data.

About 97% of UserOps use a paymaster, and from speaking with dozens of wallets/SDKs in the space, I can say for a fact that many of them see gas abstraction as a **very** important feature. Some of them even value it so much that they migrate to 4337 by letting their users still manage their key with a “dumb” EOA wallet (e.g metamask), but they can hook it up to a 4337 account they deploy for them, just so they can make use of a paymaster.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> 4337 proponents have to have a narrow definition for AA because everything else is so superior that 4337 has to exclude them as valid solutions to be promising itself.
>
>
> …
>
>
> However, 4337 proponents will be mad because their proposal is becoming even less relevant.

Again with the ad hominem attacks. Please don’t make assumptions about people and their feelings/motivations, let’s focus the discussion on data and technical design.

---

**wjmelements** (2024-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomteman/48/8290_2.png) tomteman:

> That opinion has no basis if you look at the actual onchain data.
>
>
> About 97% of UserOps use a paymaster,

As aforementioned, less than 10% of AA is 4377. But you are missing my point: gas abstraction does not define AA. 4337 proponents like yourself sure seem to think it is mandatory. It is not. You also prove the point I make that you object to as ad-hominem; you are trying to disqualify other more successful forms of AA in order to make 4337 seem more relevant. Indeed it’s so irrelevant that it’s losing to word of mouth non-standardized practices.

---

**MrSilly** (2024-04-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> But the final version is still useful and am looking forward to its application to limit order intents in particular. It can abstract gas which is nice

It can abstract gas if you are willing to trust the invoker to access all of your assets. Invokers will be whitelisted with prejudice by wallets (rightly so) so this won’t be that useful to developers.

---

**MrSilly** (2024-04-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> other more successful forms of AA

Like what? You said EIP 3074 isn’t AA and that 4337 is less than 10%. So what’s the other 90%? And why are you so angry?

---

**dror** (2024-04-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> 4337 is garbage and a waste of gas.

ERC-4337 is an opt-in, no-consensus-change account model.

Yes, being an ERC implies some limitations but keeps a lot of flexibility (including full support on all existing blockchains, almost from day one)

The question is not how gas-inefficient it is, but how usable it is, and how it maps with the endgame account model we want Ethereum to have.

---

**wjmelements** (2024-04-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> ERC-4337 is an opt-in, no-consensus-change

That’s all ERCs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> Like what? You said EIP 3074 isn’t AA and that 4337 is less than 10%. So what’s the other 90%?

The most successful AA implementations are MEV bot contracts. The most successful ones are general-purpose. Check out their 1byte and 2byte ABIs. Compare their gas costs to 4337. They are innovating much faster but also much quieter than 4337. You should take some time to look into their code. You can learn a lot about how user accounts should be written.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> And why are you so angry?

Because 4337 proponents say ridiculous things like this the OP:

> Unnecessary: given that account abstraction (ERC 4337) is already on mainnet and we are on the way to having gas efficient native account abstraction in the protocol and standardized on all the rollups

---

**MrSilly** (2024-04-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> The most successful AA implementations are MEV bot contracts. The most successful ones are general-purpose. Check out their 1byte and 2byte ABIs. Compare their gas costs to 4337. They are innovating much faster but also much quieter than 4337. You should take some time to look into their code. You can learn a lot about how user accounts should be written.

Well, did you compare the scope of functionality and security guarantees provided? If they’re equivalent that would be great. Maybe there can be some cross pollination. I suspect it isn’t apples to apples, you can save a lot of gas by doing more stuff off chain in a way that relaxes security constraints and opens up various attacks vectors. My understanding is ERC 4337 is complex because it was designed by a team that spent a lot energy making sure they didn’t overlook attack vectors.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Unnecessary: given that account abstraction (ERC 4337) is already on mainnet and we are on the way to having gas efficient native account abstraction in the protocol and standardized on all the rollups

Why is that ridiculous? Because you think 4337 consumes too much gas? A couple of things 1) gas is less of a concern on rollups, where most account activity is expected to happen moving forward 2) The team is working on native account abstraction that will save gas costs, but this requires consensus changes, which take time to make.

---

**QEDK** (2024-04-21):

Seems to be making a mountain out of a molehill, OP seems to not understand that EIP-3074 is the only pathway to native AA atm. Now, let’s talk about making consensus, quoting people from Twitter and Vitalik’s posts from 3 (!!) years ago is exactly not the way to go about it, in fact, it should be done based on the merits of EIP-3074 as intended to be put into the protocol **today**.

Having no in-protocol AA solution has been terrible for DX and UX alike, now is it great that ERC-4337 has got us half of the way? Sure - but it still doesn’t let us have a native way for delegating access to a contract, which is exactly what EIP-3074 provides - that is the **crucial** point that OP seems to be missing. And if we’re really taking an all-encompassing view, let’s not forget that there is a myriad of centralized apps and chains, and EIPs such as EIP-712 that have obvious footguns but we don’t go at them with pitchforks in the air because it’s effective at what its purpose is, so this entire post, especially combining with those screenshots screams to be a [logical fallacy](https://en.wikipedia.org/wiki/Argument_from_authority).

---

**yoavw** (2024-04-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qedk/48/5997_2.png) QEDK:

> EIP-3074 is the only pathway to native AA atm.

Let’s split this claim to two parts:

*EIP-3074 being **a** pathway to native AA*

Care to point out how 3074 takes us to native AA?  One that is actually AA, including validation?  How does it enable basic AA features like key rotation, spending-limit enforcement, and in general making the account’s validation logic, well… arbitrary?

*EIP-3074 being **the only** pathway to native AA*

You mean because the geth team will veto anything based on RIP-7560 which actually aims to provide full native AA?

---

**StanislavBreadless** (2024-04-21):

I am not a big fan of this EIP per se (I agree that on its own it is a diversion from the endgoal), but it seems that it would enable cheap migration into EIP4337 for EOA users: an EOA user can grant its EIP4337 “side-account” full access to his funds. Not sure whether this option has been explored yet, but it allows the users to interact within the realm of account abstraction, without having to think about migrating their funds. This is a bad version of EIP-5003, just in case it wont get accepted ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

The drawbacks of this approach are obvious:

- It is not “really” a key rotation, since the private key is still the most important ruler here. If it is stolen, the user is screwed really bad.
- Still the extra gas for the bundler since it is an ERC, etc.

However, if this approach is pushed forward enough, it can open much wider doors towards migration to EIP4337 and to RIP-7560 which is very similar to it in the future. I am not aware on the internal discussions with the geth team, but probably it is a big feature for them, and the main reason why it can not be implemented is because cost / risk ratio is bad (where “risk” are the chances that it won’t get used). Having a gradual approach where EOAs partially migrate to EIP4337 accounts can give more time for wider adoption of the complete AA standards.

---

**QEDK** (2024-04-21):

> You mean because the geth team will veto anything based on RIP-7560 which actually aims to provide full native AA?

Would prefer if you didn’t put words into my mouth, or assume some intent (where none) of core devs, the core question to answer here would be how much enshrinement we want at the protocol level. This is where EIP-3074 strikes a very good balance, where protocol changes are simple, implementable and do not carry  forward to an unmanageable situation. I’m not against **full** native AA, or for that matter, RIP-7560, I just think this is a good measure towards forward-compatible native AA, and superior to the *current* alternatives like ERC-4337.

> How does it enable basic AA features like key rotation, spending-limit enforcement, and in general making the account’s validation logic, well… arbitrary?

Why should Ethereum as a protocol care about some of these factors yet? Isn’t it better to have EIP-3074 in conjunction with a smart contract standard (TBD) that handles it, seems simple enough to do through social coordination, and also to clarify, I’m not against future EIPs that do choose to enshrine some of those factors, where I do definitely disagree is that we need a fully-featured native AA (in particular, spending enforcements and the likes) on the protocol level, if anything, we should have the ideal amount of enhancement on top of EIP-3074 that gets us some of the way towards a RIP like RIP-7560.

---

**yoavw** (2024-04-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qedk/48/5997_2.png) QEDK:

> Would prefer if you didn’t put words into my mouth, or assume some intent (where none) of core devs

I wasn’t putting words in your mouth, nor assuming a nonexistent intent.  The intent has been demonstrated on multiple occasions (specifically re RIP-7560).  But it has nothing to do with 3074 so I’ll leave it at that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qedk/48/5997_2.png) QEDK:

> think this is a good measure towards forward-compatible native AA

Can you briefly describe the roadmap that starts with 3074 and ends with full native AA?  I find it hard to see a clear path there.  3074 significantly improves EOA but it remains an EOA with all its limitations.  Full native AA means that smart accounts are a 1st class citizen and do not depend on an EOA, and further empowering EOA doesn’t seem like a step in that direction.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qedk/48/5997_2.png) QEDK:

> superior to the current alternatives like ERC-4337

“superior” indicates that they try to solve the same problem, and one does it better than the other.  I addressed that misconception in [ERC-4337 vs EIP-3074: False dichotomy - HackMD](https://notes.ethereum.org/@yoav/erc-4337-vs-eip-3074-false-dichotomy)

ERC-4337 aims to be a first step in the direction of full AA (where the entire account is abstracted from the protocol, including validation).  EIP-3074 aims to improve EOA.  They are not comparable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qedk/48/5997_2.png) QEDK:

> Why should Ethereum as a protocol care about some of these factors yet?

The protocol shouldn’t care about any specific feature. It should **abstract** the account and let users build whatever they want on top of that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qedk/48/5997_2.png) QEDK:

> Isn’t it better to have EIP-3074 in conjunction with a smart contract standard (TBD) that handles it

It can’t.  No smart contract can cause the ECDSA key to stop working.  And if you kill the key by using EIP-5003, you end up with a smart contract account like Ethereum had from day 1 - which is a 2nd class citizen that cannot send a transaction and needs the help of another EOA.

In the two examples I gave, how can a smart contract standard work?

- Key rotation - can a smart contract standard replace the EOA’s ECDSA key?
- Spending limits - can a smart contract standard prevent the use of the ECDSA key to drain the EOA?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qedk/48/5997_2.png) QEDK:

> (in particular, spending enforcements and the likes) on the protocol level,

That’s a feature implemented by **users**, not by the protocol.  That’s the whole point.  We need to abstract the account and let users build features.  ERC-4337 and RIP-7560 don’t add any built-in features to accounts.  Not even things like batching.  Instead they abstract everything and let the user build the account.  (It does add gas abstraction outside the account, because that’s a protocol feature rather than account feature).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qedk/48/5997_2.png) QEDK:

> if anything, we should have the ideal amount of enhancement on top of EIP-3074 that gets us some of the way towards a RIP like RIP-7560.

What does this enhancement look like?  Can it look significantly different from RIP-7560 and still fully abstract the account, make it a 1st class citizen (can send transactions), without giving up the permissionless mempool required for censorship resistance (or expose the network to DoS by ignoring the transaction invalidation problem)?

I suspect that an attempt to extend 3074 towards full AA will end up quite similar to 7560 (if not outright using 4337).  Otherwise it’ll give up on important properties such as censorship resistance.

---

**yoavw** (2024-04-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stanislavbreadless/48/5336_2.png) StanislavBreadless:

> Not sure whether this option has been explored yet

See [Can EIP-3074 and ERC-4337 be used together? - HackMD](https://notes.ethereum.org/@yoav/eip-3074-erc-4337-synergy)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stanislavbreadless/48/5336_2.png) StanislavBreadless:

> I am not aware on the internal discussions with the geth team

There isn’t one.  Only what you heard on RollCall and a couple of similar public conversations.  Currently RIP-7560 is being implemented on a geth fork, and the reth team is also looking into implementing it there. The implementation is probably quite similar to what you did at zksync - the distance between that and 7560 is not big, and is getting smaller as we split 7560 and make some parts optional.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stanislavbreadless/48/5336_2.png) StanislavBreadless:

> Having a gradual approach where EOAs partially migrate to EIP4337 accounts can give more time for wider adoption of the complete AA standards

I agree - see my post above.  It can certainly help with the adoption of 4337 by making it free to experiment, and even free to deploy a non-EOA smart account.  From that perspective 3074 will push 4337 forward, but I’m concerned about other implications of 3074 that still make it a step in the wrong direction.

---

**noam** (2024-04-22):

A few (very distant) observations (building on the theme here in terms of security and paths to endgame):

1. Ethereum’s executing a rollup centric roadmap that prioritizes moving end users to L2 and architecting L1 to best support this transition.
2. A key value prop of rollups is that they’re not constrained by innovations on L1. We’re seeing this trend strength with the addition of RollCall and the RIP process and we expect to see innovation on L2+ outpace iteration on L1.
3. Given that, and given that there’s consensus that the best canonical endstate is native AA, it seems like it’s worth at least considering what is the best shot to sprint to native AA (and separately EOA migration) on L2.
4. I think 3074 is useful, but way more so on L1 where the cost benefits and legacy community are both substantial, than L2 where it feels more like a compromise/afterthought versus the best architecture in a vacuum.
5. Points (1) and (4) seem potentially a bit incongruent where Ethereum itself is focusing on supporting end user adoption of rollups but the EIP process in this case prioritizes existing users on Ethereum. This is not necessarily a bad thing, but to some of the points above, I wish there had been a broader discussion on priorities, tradeoffs, and target endgames before an inclusion announcement.
6. Net its not necessarily a bad outcome wrt to 3074 (there are some noted synergies, still thinking about how this should fit in to the evolution of user accounts on rollups in the long term) but something that might be worth flagging as EIPs and RIPs continue to evolve separately with perhaps different focuses.

High level, I think this EIP doesn’t support the core L1 roadmap and signifies a lack of alignment on what L1 Ethereum is trying to compete on. I think the ecosystem-wide answer is, at least currently, as a settlement (I understand there’s some nuance with that term) layer, and with 4844 and the move to full danksharding, a DA layer for rollups. My interpretation of “rollup centric” is that we shouldn’t be optimizing for e.g. user swaps on L1. The customers of L1s are rollups and the featureset of L1 should prioritize exclusively that. None of the features mentioned in the “ideal endstate” really optimize for end user activity at scale. My main concern is because Ethereum is trying to compete on everything, it will end up not doing any one thing as well. This might be controversial, but at this point I think L1 Ethereum should actually actively *dissuade* end user onboarding and actively promote user activity migration to rolllups. The amount of complexity and dependencies being baked into the system is high and split brain between rollup optimization and user optimization won’t help that out (https://www.hyrumslaw.com/). Trying to compete for end users on L1 misses the boat of building *global scale* permissionless byzantine resistant systems. Because of that, I actually think 3074 would have been a lot less controversial as an RIP, but candidly either way, it actually feels premature. There’s almost certainly a lot of throwaway work and a degree of settlement at a local maximum with no clear and viable path towards the desired endgame. Let certain more agile networks differentiate on that and have the market drive that demand (Polygon’s already working on an implementation, why not just see if it works as expected there first?).


*(10 more replies not shown)*
