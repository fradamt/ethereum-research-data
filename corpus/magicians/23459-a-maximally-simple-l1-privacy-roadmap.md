---
source: magicians
topic_id: 23459
title: A maximally simple L1 privacy roadmap
author: vbuterin
date: "2025-04-11"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/a-maximally-simple-l1-privacy-roadmap/23459
views: 13427
likes: 69
posts_count: 39
---

# A maximally simple L1 privacy roadmap

*See also: pcaversaccio’s roadmap: [Ethereum Privacy: The Road to Self-Sovereignty - Privacy - Ethereum Research](https://ethresear.ch/t/ethereum-privacy-the-road-to-self-sovereignty/22115)*

These are my current thoughts on how we can practically improve the state of privacy experienced by Ethereum’s users in a way that is very light on Ethereum consensus changes. This covers four primary key forms of privacy:

1. Privacy of onchain payments
2. Partial anonymization of onchain activity inside applications
3. Privacy of reads to the chain, ie. RPC calls
4. Network-level anonymization

This roadmap can be combined with a longer-term roadmap that makes deeper changes to L1, or privacy-preserving application-specific rollups, or other more complex features.

## Roadmap

1. Incorporate privacy tools (eg. Railgun, Privacy Pools) into existing wallets. Wallets should have a notion of a shielded balance, and when you send to someone else, there should be a “send from shielded balance” option, ideally turned on by default. This should all be designed to feel maximally natural from a UX perspective. Users should NOT have to download a separate “privacy wallet”
2. Move the ecosystem toward “one address per application” by default. This is a major step, and it entails significant convenience sacrifices, but IMO this is a bullet that we should bite, because this is the most practical way to remove public links between all of your activity across different applications. Moving toward such a design also works very naturally with in-application wallets, and the new workflows required to make this work look very similar to what is needed already with cross-chain interoperability (eg. depositing funds to a chain from one of multiple sources)
3. Make send-to-self privacy-preserving by default - needed to make (2) work
4. Implement FOCIL and EIP-7701, and make sure to implement a version of FOCIL that is EIP-7701-friendly. Along with EIP 7701’s account abstraction benefits, this allows protocols like PP, Railway, Tornado etc to operate without needing relays / public broadcasters, greatly simplifying the development and maintenance of such protocols. FOCIL greatly improves censorship resistance of all transactions, including privacy-preserving transactions.
5. Incorporate TEE-based RPC privacy into existing wallets, as a short-term mitigation. Automata has a version of this already; this needs to be verified and hardened as much as possible. This allows users to interact with RPC nodes while getting stronger assurances that their private data is not being collected.
6. Replace TEEs with private information retrieval (PIR) once the tech becomes ready. PIR offers cryptographic guarantees, and so is much stronger than TEEs, but it is currently not efficient enough for large datasets. Potentially we can consider hybrid approaches, eg. use TEEs to isolate regions of the state of size 2**20, and use PIR inside of those, shifting the constants up over time as PIR becomes more efficient.
7. Wallets should connect to multiple RPC nodes, optionally through a mixnet, ideally use a different RPC node per dapp. If we also add security armoring to RPC nodes (ie. light client support), it becomes practical for a user to trust a much larger set of RPC servers. This reduces metadata leakage.
8. Work on proof aggregation protocols to allow multiple privacy-protocol transactions to share a single onchain proof. This greatly reduces the gas costs of privacy protocols.
9. Work on privacy-preserving keystore wallets (see more detailed explanations in this post). This allows users to upgrade their account verification logic (algorithm or keys) in one transaction, and have this change be immediately reflected in all private notes that they control (across L1 and all L2s!), without publicly linking those notes.

At the end of this, we will have a world where:

- A large portion of sends are private, and private sends are default in many cases
- Activity inside of each individual application is public, but the link between your activity in application A and your activity in application B is private
- Privacy guarantees hold not just against adversaries passively observing the chain, but also adversaries operating RPC nodes

## Replies

**auryn** (2025-04-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> shifting the constants up over time as PIR becomes more efficient.

What is the gap between current reality and required latency to make PIR RPCs viable?

---

**privacycaviar** (2025-04-11):

Tornado Cash is still the largest privacy pool on Ethereum, and with OFAC sanctions now lifted, I’m curious why it’s not mentioned here. Is it being excluded mainly due to compliance concerns?

---

**Sofianel5** (2025-04-11):

No reason to have compliance concerns anymore, we won the case.

---

**Designer-F** (2025-04-11):

Tornado Cash is a better choice, no censorship, large privacy pool, and free to use if relayers are not needed

---

**NelsonMcKey** (2025-04-11):

> Along with EIP 7701’s account abstraction benefits, this allows protocols like PP, Railway, Tornado etc to operate without needing relays / public broadcasters…

See point four.

---

**TimDaub** (2025-04-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Move the ecosystem toward “one address per application” by default. This is a major step, and it entails significant convenience sacrifices, but IMO this is a bullet that we should bite, because this is the most practical way to remove public links between all of your activity across different applications. Moving toward such a design also works very naturally with in-application wallets, and the new workflows required to make this work look very similar to what is needed already with cross-chain interoperability (eg. depositing funds to a chain from one of multiple sources)

What does this mean for ENS usage? My understanding is that most users currently have one intentionally publicly known address that they use to onboard to apps. And then they have other wallets where they store their wealth, trade, etc. Is an „application“ here: wealth store, trading, public theatre, or is an application: Uniswap, Aave?

---

**vbuterin** (2025-04-11):

Two possible answers:

1. You can have a single address that is your ENS address, but that’s not the address you use for apps by default.
2. Stealth addresses (so, others can use your ENS data to send things to a fresh address that you control, without others being able to publicly link it)

---

**MacBudkowski** (2025-04-11):

> You can have a single address that is your ENS address, but that’s not the address you use for apps by default.

Okay, so if we follow this path, I think we have to think about UX. E.g., we could ask users before connecting to each app if they want to make their actions public.

And also educate them that if they make their actions public, they can build their onchain reputation. So it’s like “sending a DM on Signal” vs. “sending a tweet". One is better for privacy, one is better for building reputation.

If we don’t do it, we will slow down onchain identity by a lot. And this is a thing that differentiates blockchain addresses from e-mails.

If you run web2 social (like Reddit), users send their gmail addresses to create an account. As a company you have to accept all of them because you cannot check if one address is more legit than the other. It makes it pretty easy to astroturf and run bot networks.

If you run onchain social, you can take users’ wallets and check some predefined parameters. E.g., how old is the address, how many txs it did, what are relationship with other potentially problematic addresses and so on. We already been doing that at Kiwi and it’s been very helpful to track these behaviors.

On Farcaster, where every action is public by default (and wouldn’t be impacted since they use their own P2P network), you can even create these forensics graphs [like this one.](https://warpcast.com/geoffgolberg/0xee3cbbea) And of course everyone can do them, which is a big plus.

If - on the other hand - everyone was doing 100% private onchain actions, it’d cripple onchain social defensive capabilities.

PS: We already see onchain identity fragmentation because of in-app wallets, as [I described here](https://x.com/MacBudkowski/status/1863951819296153623) and lately also noted by [nonlinear](https://warpcast.com/nonlinear.eth/0x7763a1e8).

---

**kdenhartog** (2025-04-11):

Number 2 is effectively just recreating 3P cookies if we don’t do it. Web2 has already shown this isn’t a good path forward with everyone except Google having disabled them by default:


      ![image](https://kyledenhartog.com/favicon.png)

      [Kyle Den Hartog](https://kyledenhartog.com/recreating-web3-cross-origin-tracking/)



    ![image](https://kyledenhartog.com/assets/img/profile.jpg)

###



We should expect that when the user shares their address that will act as implied consent for cross-origin tracking in the same way cookie notices act as a prompt for tracking.










As for number 7, [Oblivious HTTPS](https://datatracker.ietf.org/doc/rfc9458/) is another alternative solution so that we don’t face latency tradeoffs. We need RPC services to enable support for it though.

---

**kdenhartog** (2025-04-11):

Option 1 faces the tradeoff that onchain transactions still leak data. This works IfF we also get 1 by default.

---

**Styliann** (2025-04-11):

This is a roadmap for Privacy in the traditional sense - i.e. Anonymity.

How about encrypting balances and amounts, with the ability to selectively reveal them to a third party? Any thoughts on the confidential ERC20 standard?

---

**iAmMichaelConnor** (2025-04-11):

I’m helping design the Aztec privacy rollup, so this is right up my street. We want to make sure we keep pace with Ethereum’s privacy needs. I have some questions / comments.

1. vbuterin:

> This allows users to upgrade their account verification logic (algorithm or keys) in one transaction, and have this change be immediately reflected in all private notes that they control (across L1 and all L2s!), without publicly linking those notes

 A nullifier keypair for a note can’t easily be rotated, because (a) the nullifier for a given note is deterministically* derived from the secret key of the nullifier public key that “owns” the note, and (b) rotation can lead to double-spend bugs.

(a) A nullifier is usually something like hash(hash(note), nullifier_secret_key_1). If you rotate your nullifier keypair, the nullifier for this note still relies on the old nullifier keypair.
2. (b) You could detach the “owner” of the note from the nullifier keypair, by storing the nullifier public key against the “owner” in a keystore registry. The owner could then rotate their nullifier public key  in the registry. But there’s then a risk that the “owner” can spend the note twice: once by deriving a nullifier from the first nullifier secret key; and a second time by rotating their nullifier public key and deriving second nullifier from the second nullifier secret key.
* There’s a way to solve this, but it’s constraint-heavy, and requires proving: when the rotation took place; when the note was created; and that the ‘old’ nullifier hasn’t already been used.
3. vbuterin:

> Move the ecosystem toward “one address per application” by default

 Aren’t there examples of complex defi flows (which compose many smart contract function calls together) which would require the user’s address to be the same across all the different smart contracts?
Even a simple lending contract stores information against a borrower’s address, but also calls separate token contracts to decrement/increment balances of that same borrower’s address.
Consider more crazy complex flows like: take a flash loan; use the borrowed asset to provide liquidity elsewhere; use the LP tokens and stake them somewhere else; use those staked LP tokens as collateral on another protocol to mint a stablecoin; swap the stablecoin for another asset; repay the flash loan.
… For that crazy flow, isn’t it beneficial for the user’s address to be the same across all those smart contracts?
Would it be more fitting to encourage one address per “defi session” (whatever that might be)?
We’re debating this topic at Aztec, currently.
4. vbuterin:

> Users should NOT have to download a separate “privacy wallet”

 Would it be acceptable if these wallets have to generate and track a new set of secrets, as most privacy tools use snark-friendly secrets that are different from a user’s Ethereum private key?
5. vbuterin:

> this allows protocols like PP, Railway, Tornado etc to operate without needing relays / public broadcasters

 How does this work? How do the gas fees get paid?

---

**jimjim.eth** (2025-04-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> “one address per application”

Why cant we just atomically unshield and unshield like how railgun does it with their 0x integration? It would be far more private! It would also be the same UX flow for more endgame privacy like in aztec.

---

**mpeyfuss** (2025-04-11):

This is interesting. Two questions come to mind, from an app developer perspective.

First, having per-app wallets seems to go against the thinking that I can use my wallet across all different applications. Funding those new wallets brings user friction as well. We’ve seen that any additional steps already represent a drop off in user engagement.

Second, what impact would this have on regulation of ETH? I know governments don’t want financial activity hidden from them. Does this pose a threat to users and apps building on Ethereum?

I’m not an expert in privacy so really just asking questions. Cheers!

---

**teddy** (2025-04-11):

On RPC Privacy specifically:

Why choose to move in the direction of TEE->PIR->mixnet instead of focusing on making every wallet be able to run the relevant parts of a node (aka *light client*?) I feel like going for the former means aiming for an Ethereum ecosystem with privacy guarantees resembling tradfi, while moving in the direction of light clients could yield actually better privacy long-term.

---

**h4x3rotab** (2025-04-11):

I can see a lot of space to explore when using TEE. For example:

1. Self hosted light client in TEE. We get a solution that doesn’t rely on any single point of failure, but still can outsource the tedious maintenance tasks to some other providers. We can plug it into almost all the wallets or dapp frontend from the day one. There are people exploring running Helios in TEE [2] to achieve this.
2. Mixnet in TEE. There are also some exploration to run a Tor node in TEE [1]. Since the light client also relies on an upstream RPC provider, it would be a nice addon to redirect all the traffic through a mixnet like Tor to hide the IP address and traffic features.

Links:

1. /github.com/Dstack-TEE/dstack-examples/tree/main/tor-hidden-service
2. /github.com/Dstack-TEE/dstack-examples/tree/main/lightclient

(The forum dislike me to post link directly)

---

**SCBuergel** (2025-04-11):

This list is good but IMO too narrowly RPC-focused when thinking about data-harvesting third party services. That is ok for a typical Ethereum wallet of 2018, but (sadly!) not anymore. Unfortunately, a contemporary Ethereum wallet pings a prospering jungle of centralized servers and services for:

- gas prices
- price feeds
- tx simulation
- scam checkers
- gas-less transactions
- cross-chain balances
- multisigs with off-chain signature services
- a range of indexer data, typically for token balances
- token icons (here’s a fun demo showing why this is much more evil than you think!)

All of them reveal some level of personal data. Minimally that is “IP 1.2.3.4 is doing something with Ethereum right now” but usually it is much more and much more personal. So I’d say that we need a general purpose anonymous transport layer, beyond just anonymizing simple RPC calls.

---

**peersky** (2025-04-13):

Instead of submitting as “*pinnaple-green-swordwish*” many “normal” users want to have notifications in form “*Tim* submitted his proposal” (for those who has been granted notion about account connection to the sender identity) but keep the submission private.

Especially in case of on-chain governance this allows better level of UX and reducing [halo](https://en.wikipedia.org/wiki/Halo_effect).

This  requires reveal only commit and have 3rd party to host pool of proposals that later is batch revealed, ongoing UX goals for [Rankify.it](https://rankify.it) / [Peeramid.network](https://peeramid.network)  looks like this:

```auto
Bot: @Bob sent a proposal. // public commitment & signed by Bob and trusted server holding nullifier
Bot: @Alice sent a proposal.
Bot: @Georg hurry up!
Bot: @Georg sent a proposal.
Bot: New proposals: A;B;C; // Server reveals & nullifies pool of proposals
// Voting phase begins
// Tally, posts proofs of data integrity
Bot: Winning proposal was C, it was sent by @Bob

```

Current plans is to have marketplace for such private pools, enabling users to pick whatever trust guarantees they want (chose between Lit, ICP, TEE, Self hosted MPC etc).

[@vbuterin](/u/vbuterin) Im having hard time to classify that though, does that fit in your categorization under privacy pools  or aggregation?

---

**ying484** (2025-04-13):

I need someone familiar to teach me all this.

---

**undefined** (2025-04-14):

These next-level ambitions are all promising and important to explore. However, I think more people need to start paying attention to the basics when it comes to privacy.

Have you tried passing your wallet/browser through [mitmproxy](https://mitmproxy.org) or burpsuite and checked out just how much information is broadcasted to various endpoints in the cloud? If you use a browser extension wallet, you may be surprised to see traffic that is not visible in Chrome/Firefox developer tools Network tab.

Now see how much you are actually able to prevent leaking by using the wallet settings. Disable any analytics, use your own RPC node, disable optional third-party features, and try again. Compare reality to the privacy policy of the wallet.

The state of privacy in mainstream wallets have gone increasingly worrying over time and I don’t see much talk about that. The features discussed in this thread don’t mean much if balance- and history requests in practice use proprietary unconfigurable vendor servers. Addressing that is not an unsolved technical issue but one where wallet vendors have faced little scrutiny and pushback from the community.

Some deviations and options:

- Konkret Wallet is one budding initiative showing a different approach to the browser wallets.
- Trezor actually provides the option to do self-hosted and private account-indexing via BlockBook (but on the other hand their connector module is idiomatiacally loading from the cloud…)
- TrueBlocks is a great way for expert users with the resources to self-host indexing

All are pretty obscure if not neglected. I think we need to start practice what we preach and addressing the here and now while we consider future possibilities.


*(18 more replies not shown)*
