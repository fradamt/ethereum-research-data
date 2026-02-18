---
source: magicians
topic_id: 20209
title: Open source alternatives to privy, web3auth and dynamic
author: TimDaub
date: "2024-06-05"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/open-source-alternatives-to-privy-web3auth-and-dynamic/20209
views: 3342
likes: 22
posts_count: 8
---

# Open source alternatives to privy, web3auth and dynamic

gm,

as some of you may know, I’m running a social media website built on the Ethereum stack. For those who don’t, it’s https://kiwinews.xyz

In any case, a core UX concept is that we use temporary keys that we create in the browser, store in local storage, and use for confirmation-less signing when a user upvotes, submits a link, or leaves a comment.

Now, we’ve obviously done that to provide our users with a better UX so that they don’t have to sign each interaction on the side cumbersomely using their custody wallet.

The system works by delegating posting rights from your custody wallet, for example, managed by your Rainbow or Metamask wallet, to this temporary key in your local storage. We use a simple delegation protocol on Optimism. The user has to send a transaction that connects the keys onchain for the Kiwi News nodes to witness the connection.

All this said a problem that has significantly lowered users’ engagement is that they naturally use multiple different browsers and devices. For example, a user may use a mobile and desktop device. Hence, creating multiple local-storage-specific keys is necessary, and leading them to delegate these keys on Optimism is necessary, too. But this is problematic because it is far from a seamless user experience. If we have to lead the user to send multiple transactions on Optimism, even if they’re virtual free in terms of costs, they cost us engagement and churn. Asking users to send transactions is scary to them and a drop-off point, so we try to avoid it.

Hence, a while ago, I actually started to look into solutions that would make the local storage key less perishable, and I also became interested in finding a solution that would somehow easily synchronize keys between a user’s mobile and desktop device.

In fact, with Apple and Google’s campaign to establish Passkeys more, I became really interested in them. I found out that there is the “largeBlob” extension, which allows the developer to store a small payload in iCloud. This payload is only accessible to the user when they authorize themselves with FaceID to Apple using Passkeys. This is useful as it allows me to store a full Ethereum private key in the largeBlob and retrieve it from any Apple device the user has later on.

So I ended up implementing Passkeys into my app, and it is actually fairly usable on Apple devices. The user can back up the temporary key using the largeBlob extension, and then upon “Connecting their Wallet,” they can consider “Connecting with Passkeys,” which essentially prompts them to authenticate themselves and then downloads the Ethereum private key from iCloud using largeBlob.

[![Screenshot 2024-06-05 at 07.30.59](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8b7b2f3d064f8ce22238c9dda7eb47094bc40e60_2_690x489.png)Screenshot 2024-06-05 at 07.30.591476×1048 107 KB](https://ethereum-magicians.org/uploads/default/8b7b2f3d064f8ce22238c9dda7eb47094bc40e60)

Honestly, this was great because I actually don’t have much concerns about storing this temporary key on iCloud:

- The temporary keys in Kiwi News are technically revocable onchain, and so if they ever leak or there are safety concerns, we could ask users to revoke their delegation.
- These keys aren’t meant to hold any funds. Their purpose is strictly to post content on behalf of the custody wallet and so, for a user who’s willing to opt in, I think it’s totally fair to post them to iCloud. That said, Kiwi News can be used entirely with your Ethereum wallet and you never actually have to delegate to a temporary wallet, so using Passkeys is optional as of now.

So, with that out of the way, let me tell you the caveats to using Passkeys:

- Apple and Google are fighting about integrating the “largeBlob” extension. My reading is that Google wants to go forward with PRF instead of “largeBlob,” and so my understanding is that PRF won’t allow developers to store arbitrary data.
- While there seems to be momentum for RIP-7212 for secp256r1, using this curve for Kiwi News (which would be reasonable) would mean that the user still has to authorize themselves pretty frequently using FaceID when signing stuff (which isn’t really a good trade-off for a social media site).
- As of now, the Passkeys integration that we’ve done has terrible browser and OS support. It basically exclusively works for Safari on Mac and iOS devices. Chromium-based browsers don’t seem to work because of Google’s unwillingness to implement them. iOS 16 devices don’t work. And there is a mysterious bug that if users use 1Password on iOS to manage their Passkeys, it breaks our entire flow. That said, it is my assessment that this entire situation will take years and not months to be fixed, too, which may be time that we don’t have as a startup.
- Finally, I think for an Android and Mac user, Passkeys will never seamlessly work as Google and Apple have decided that their respective solutions will only ever work well “in their ecosystem.”

So having found out all of this through integrating with Passkeys, it has made me feel rather pessimistic about their future, so I started looking for alternatives.

To solve this problem for users, recently, I’ve started considering privy another time, and I found that they perfectly solve our use case. For the sake of simplicity, I’m going to refer to the specific solution as privy, although there are also alternatives such as web3auth or dynamic, which, to my knowledge, all provide roughly the same service. My layman’s understanding of its inner workings is that:

- Users can connect their wallets as usual, and privy takes care of sending the signature request, etc.
- But privy also allows to provision so-called “embedded wallets,” which are (on a UX-level) essentially equivalent to the temporary keys that Kiwi News currently stores in the browser’s local storage, except that privy encrypts these keys, stores them on their servers (or in an iframe, I’m not sure how it works exactly), but in any case, this allows a privy-using developer to generate an embedded wallet that can be synced across a user’s multiple devices and browsers.

While privy is often touted as a tool to onboard new users to crypto, I’m actually not interested in allowing a user to, for example, start trying my site with a Google-login or whatever, but, instead, I find it really useful that embedded wallets can be synced across devices!

So, to me, as having already spent months trying to come up with a reasonable solution for my users, and considering that this issue really kills engagement on the site, I find it now quite tempting to integrate with privy. This is because privy, as opposed to other solutions, seems to work independently of whether Apple and Google find a solution to the largeBlob conflict. privy’s embedded wallet synchronization doesn’t rely on browsers finishing to implement new features, it just relies on a user being able to sign through the SIWE process.

Now, this integration, however, obviously comes with a caveat, which is that it will allow privy to hold my users’ keys hostage. What do I mean by that?

If I lead all my users to create an embedded wallet with privy, and so their temporary key is now stored with privy servers, then for my site to function, I will have to continue integrating with privy - and if I ever want to migrate away, I’d have to ask all my users to send a transaction to Optimism to delegate a new key. So logically, this will also allow privy to charge us quite a bit in the future. And it makes us reliant on them to provide a safe and properly functioning service.

In fact, I think, as of now, this entire situation doesn’t even yet warrant writing an Ethereum Magicians post, but I feel like there is a greater pattern at play here where companies try to intentionally capture a user’s keys because they know that this will increase their app’s moat.

Without trying to sound too accusatory, I think you can also see this with Warpcast’s strategy to generate their own Ethereum key in the app, as this is done to lock down the user’s key and hence make it rather unlikely for the user to swap into other clients/apps with that key as importing and exporting of seed phrases isn’t recommended and a scary act. All of this increases the defensibility of building their app. It makes it harder for others to compete as users are being locked into the ecosystem/app.

So, looking at how privy works and that it makes it very unlikely that, with integrating it, I will give my users the capability to “exit” with their embedded wallets, I couldn’t help but wonder what open-source alternatives exist that also address all my concerns above.

It seems to me that, at least for a site like mine, which doesn’t need the keys to hold actual money, there don’t seem to be that many requirements that would complicate an integration.

Additionally, I feel like this use case is integral for anyone building crypto consumer use cases as temporary wallet keys must inevitably somehow be synced across devices and browsers, and since the more financial-minded self-custody wallets (and Google and Apple) don’t seem to be too interested in providing solutions here. Their interest is in locking down the keys and keeping them safe instead.

**Hence I would love to connect and hear other’s thoughts on this!**

I feel like I’m pretty much in the trenches here as I’m one of the few who have attempted to build an actual social consumer use case with the Ethereum wallet stack that doesn’t primarily deal with sending funds around.

So I’d be super happy if this post actually had an impact where it’d change the strategy of some wallet providers in the future, where they start to pay attention to these use cases to help users keep custody of their keys.

Or, in case I haven’t done my research, it’d be helpful if there was something like a privy that I could somehow self-administer so that I’m not giving up control of my users’ keys to give them a better user experience.

## Replies

**voboda** (2024-06-05):

Fun with iframes, eh? Seems like a lot of the behind-the-scenes magic of these auth systems comes from some old-school web standards, like cross-tab/cross-dom communication, that are only now finding their time to shine.  At the same time, these auth services introduce themselves as at least a semi-trusted third-party, and more to the point, they control their roadmap, so can “upgrade” the product in the future to gain more control.

It’s apt to recognize *Enshittification* also applies to web3, and quasi-decentralized but VC-backed orgs – while full of wonderful people – set up an incentive structure where moats are built, fortified and exploited.   So these handy abstractions they offer come at a fairly predictable future cost.

On that note, have you looked into *remotestorage*.io ? It’s a standard that’s tread this path somewhat. It’s a known solution to the problem of distributing user-custodial data across their devices. There’s a small ecosytem of servers and sdks, still maintained, allowing for self-hosting by you and your users.   In some ways, it had the opposite tendency though, towards not-enough abstraction rather than the over-abstraction we see these days with web3 sdks.  But since you’ve already built a system for ephemeral keys, this might be an easy sync layer.

---

**pedrouid** (2024-06-05):

I think the big challenge around Passkeys, Local Keys or any form of “ephemeral” application keys is that regardless of how you design these they will always risk either being unrecoverable or compromised by cross-site scripting (including malicious browser extensions)

The truth is that a seamless embedded wallet experience isn’t going to be solve overnight and it requires large coordination around different stakeholders surrounding the Ethereum ecosystem.

ERC-4337 got us start with the right foot a couple of years ago but still left a lot of unanswered questions when it comes to embedded wallets:

- how can apps format userOperations?
- how can apps interface with paymasters?
- how can apps sign userOperations on the behalf of users?
- how can users manage and revoke app keys (aka session keys)?

There is a lot of moving pieces currently driving this embedded wallet experience to be native to Ethereum without requiring third party services like privy, web3auth, dynamic, etc

For starters we have ERC-5792 which standardizes wallet interfaces between both EOAs and Smart Contract Accounts (SCAs) this way it will facilitate Ethereum libraries to be immediately compatible for both account types

Then we have standards around Paymasters with ERC-7677 and UserOperation building with 7679 and these will already solve the biggest problem with the current fragmentation in the ERC-4337 space.

Additionally we have ERC-7579 which establishes a very generic but minimal modular system for SCAs that will allow several modules around owners, signers and recovery management to be more interoperable.

Finally we have what I believe is the biggest game changer in this whole thread which is ERC-7715 that provides the ability for an app to be granted permissions from a wallet in order to sign on the behalf of the wallet user using a session key with very granular permissions.

Call me optimistic but I’ve never felt more hopeful for the Ethereum ecosystem to eventually have almost-native account abstraction with oustanding wallet experience that can be built with fully open-source alternatives to third-party providers

Especially now that Core Devs are considering both 7702 and 7212 for inclusion in the next hard fork it will really bring to reality that this work is going to impact the majority

WalletConnect is currently working on all of these standards above and laying the ground for the future Wallet UX with better developer tools and infrastructure that optimize for interoperability

---

**TimDaub** (2024-06-05):

Hey [@pedrouid](/u/pedrouid), thanks for answering but in this thread I‘m actually not looking for the same security guarantees that you do with the financial standards you mention.

Our keys aren‘t supposed to hold funds and their application privileges are always revocable onchain. They’re only used for upvoting, submitting links and commenting. So most of the design to keep financial keys safe actually ends up creating all these hurdles that I‘m describing. I‘m actually not going to blame them. We simply started using financial wallets for social apps! But this is why I‘m here explaining what I need ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I just wanted to clarify this right to begin with as to not make this thread move down the wrong path. Sorry if I may have been unclear!

These are keys for posting to social media protocols. They‘re only supposed to be used for publishing signed content. The custody wallet will continue to take care of funds and Kiwi News or Warpcast also still uses it, such that AA etc is still useful.

But we need a simple key exchange for the keys that just sign content, and this is what this thread is for.

---

**pedrouid** (2024-06-06):

That’s good to know! Honestly I’m glad you are setting the scope and expectations very explicitly upfront that it’s not intended for financial purposes

In that case the solution to this would be [EIP-5573](https://eips.ethereum.org/EIPS/eip-5573) (aka ReCaps) which allows you to describe some “capabilities” in the resources of a [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361) (aka SIWE) message that allows you to “bind” a key to act on the behalf of an Ethereum account.

We actually use this in production for our Web3Inbox service where we generate a ed25519 key in local storage that can create, read, update and delete notification subscriptions for our Notify API server without requesting the wallet to sign for every action. (see image below)

[![Screenshot 2024-06-06 at 12.55.27](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c7b821cecfe596e73b52f3b291e95eb1683307c7_2_267x499.jpeg)Screenshot 2024-06-06 at 12.55.27934×1746 238 KB](https://ethereum-magicians.org/uploads/default/c7b821cecfe596e73b52f3b291e95eb1683307c7)

How you actually construct the ReCap for your use-case is up to you… but the ReCap spec is perfect for your use-case and it allow greater user readability and allow you to build your app very flexibly.

All of this is achieved without any Smart Accounts and you can use any algorithm you want for your public keys (secp256k1, p-256, ed25519, etc) using the [did:key](https://w3c-ccg.github.io/did-method-key/) spec.

---

**reisepass** (2024-07-23):

I had all the same ideas.  And build an Embedded wallet fro some hackathon projects  here is one

It is a stupid simple implementation that stores 2 encrypt versions of the users’ private key on the self hosted backend:  1) Encrypt with  device key stored in local storage   2)  Encrypt with user pin/password

When the user logs in they need  to get a magic link from their email then the server will send over the two encrypted versions of the private key.  If they have the device key still in local storage then they are in, if they are on a new device they need to type the pin.  (multi device support needs some extra work but just requires saving the private key with another device key)

(It was important that the user does not need to type a password and a pin   this was important for usability of existing  password management tools in firefox / lastpass etc . )

This is much simpler than what Privy does with the shamir secret share. Not that SSS is hard but just unnecessary.

Anyway I would be happy to contribute to grant funding for this and also requirements definition.

i’m ruben_wolff on discord and tg

---

**HiraSiddiqui** (2024-12-06):

We are building an alternative to this in Plurality Network. We have an embedded wallet as well with MPC TSS in the background (Lit protocol - which is open source) but none of the part of the key is stored on our servers.

For each new application, we create a “Profile” against the wallet address for that particular application. Once logged in, the server gives a session against that profile, and popup-less signing can take place.

Moreover,  the application can store application-specific data in the user’s profile as well, which gets encrypted and stored using the profile keys created through TSS in the network. Only the user with the correct authentication can decrypt it - no one else. In your case, the application state could be something like access to channels, social graph, like, comments, upvotes or anything like that.

The application state and session can be accessed on any other device that the user logs in to - if the user allows.

The wallet part uses MPC-TSS, and the Profile Part uses Verifiable Credentials.

Happy to run you over the solution and see if it fits your needs.

---

**joalavedra** (2025-11-16):

From Openfort, we’ve recently launched a fully self-hostable wallet solution called OpenSigner (opensigner(.)dev). You can plug in any authentication provider you’re already familiar with (Supabase, Better-auth, etc.).

If you’re looking to have passkeys only and minimal dependency, you can check products like passkey-wallet(.)com with the precompile already onchain.

