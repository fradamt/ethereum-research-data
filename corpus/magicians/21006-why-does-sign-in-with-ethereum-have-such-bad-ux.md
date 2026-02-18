---
source: magicians
topic_id: 21006
title: Why does Sign in With Ethereum have such bad UX?
author: TimDaub
date: "2024-09-09"
category: Web > Wallets
tags: []
url: https://ethereum-magicians.org/t/why-does-sign-in-with-ethereum-have-such-bad-ux/21006
views: 431
likes: 9
posts_count: 6
---

# Why does Sign in With Ethereum have such bad UX?

On the weekend I hacked at ETHWarsaw and we used the “Sign in with Farcaster” to build an app. Today, knowing the difficulties of signing in with Ethereum, I’m wondering why Ethereum wallets are so much worse: What’s stopping us to reaching parity?

Just for those who are unfamiliar, here’s an example






My naive understanding is that the Sign in with Farcaster flow just authenticates with the app that this is me who is signing in. But that’s the same for SIWE, right? Does SIWE give any extended information about the user that Farcaster doesn’t that would justify the SIWE dialogues to be THAT MUCH worse than sign in with Farcaster?

For comparison, here is the completely awful flow using Ethereum. This is a huge point of churn. It makes me furious that this hasn’t notably improved over the last year despite many dapp builders very vocally complaining about this:






And this is only slightly better when using a different wallet, I consider Rainbow to be one of the best ones, yet it is still really bad. Notice how, for example, I had to look for the SIWE request in the notifications tab as it didn’t open by default. Other wallets have this and other issues too. It is not isolated to Rainbow. But the real question is why Connect Wallet and SIWE are even split into two actions.

A few things that I don’t understand:

- Why can’t we combine “Connect Wallet” and “SIWE” in one dialogue?
- Why can’t we automate the SIWE flow?
- Why can’t we parse the SIWE flow and make it look pretty instead of signing an unformatted string that looks sketchy as hell to a consumer?
- Are there security concerns for auto-signing SIWE? And if so, why don’t these security concerns apply to Warpcast? If there are security concerns, can we maybe have a two pronged approach of “Sign in with Ethereum” and “Step: 2: Allow the dapp to spend money after the user has signed in?”
- Why is Connect Wallet always so much worse than whatever Warpcast is doing here? It feels way more laggy somehow, why?

I’m a dapp builder so I don’t really have any meaningful power to change these things through building on my platform, so this is mostly a call to action for wallet providers etc. What’s stopping us here to get to parity? If we don’t get to parity then Ethereum wallets will simply not be the developer’s choice when it comes to consumer dapps. I don’t think we want all consumer dapps to be logged in through Warpcast, a closed source app, do we?

Sorry if this is rage bait for you but I’m in rage when I see this. I have complained about this for months and nothing ever changes. We really need to get our shit together here otherwise we won’t be able to compete. Thanks for reading

## Replies

**SamWilsn** (2024-09-10):

There’s nothing technically difficult about SIWE that makes it that clunky. If you use a pure [EIP-1193](https://eips.ethereum.org/EIPS/eip-1193) wallet, you get two dialogs: `eth_requestAccounts` and `personal_sign`.

It’s all the wallet-specific SDKs, WalletConnect dialogs, Web3Modal, etc. that makes this so ugly.

---

**bumblefudge** (2024-09-11):

I can say that the on the original community feedback calls, the designers were intending (and many wallets attending the calls did seem to be intending as well) for SIWE messages to be *detected* by wallets by ABNF validation and displayed *differently*/natively, turning all those ugly technical details into an expandable `<details>Technical details</details>` carrot, for example.  Very few wallets ever did this (and a surprisingly small portion of major dapps even conformantly implemented that ABNF in the first place, so many SIWE msgs would’ve still been garbled).

FWIW Metamask detects those messages and displays them in a more trust-inspiring way than most.  Works fine most places it’s implemented conformantly by the dapp, in my experience


      ![image](https://docs.metamask.io/img/metamask-fox.svg)

      [docs.metamask.io](https://docs.metamask.io/wallet/how-to/sign-data/siwe/)





###



Enable your users to sign in with Ethereum.

---

**frangio** (2024-09-11):

Is there an open source parser for SIWE messages?

**Edit:** Yeah I see parsing is handled by all the libraries.

---

**TimDaub** (2024-12-16):

I’ve recently come across this proposal that wants to combine connecting wallet and SIWE into one dialogue: [Onchain Login with User Info - HackMD](https://hackmd.io/@ilikesymmetry/onchain-login)

---

**sbacha** (2024-12-16):

SIWE is less than ideal because in practice it should have been wallet connect but with Oauth2 like functionality baked in.

instead you, well you see it

