---
source: ethresearch
topic_id: 22115
title: "Ethereum Privacy: The Road to Self-Sovereignty"
author: pcaversaccio
date: "2025-04-09"
category: Privacy
tags: [transaction-privacy]
url: https://ethresear.ch/t/ethereum-privacy-the-road-to-self-sovereignty/22115
views: 4290
likes: 64
posts_count: 15
---

# Ethereum Privacy: The Road to Self-Sovereignty

Ethereum must provide privacy **unconditionally**, without forcing users to prove their innocence.

[This roadmap](https://hackmd.io/@pcaversaccio/ethereum-privacy-the-road-to-self-sovereignty) outlines the necessary steps to transform Ethereum into a **maximally private** and **self-sovereign** financial system. Privacy must not be an optional feature that users must consciously enable — it must be the **default state** of the network. Ethereum’s architecture must be designed to ensure that users are private by default, not by exception.

Today, Ethereum operates in a partial, opt-in privacy model, where users must take deliberate steps to conceal their financial activities — often at the cost of usability, accessibility, and even effectiveness. This paradigm must shift. Privacy-preserving technologies should be deeply integrated at the protocol level, allowing transactions, smart contracts, and network interactions to be inherently confidential. A system that treats privacy as suspicious by default is fundamentally flawed. **Ethereum must empower users with unconditional privacy** — making self-sovereignty a guarantee, not a privilege.

---

Building a truly privacy-first Ethereum needs all our insights! Please share your feedback, ideas, and any concerns here so we can actively co-create this path forward together.

## Replies

**ameensol** (2025-04-09):

> Ethereum must provide privacy unconditionally , without forcing users to prove their innocence.

> This roadmap outlines the necessary steps to transform Ethereum into a maximally private and self-sovereign financial system. Privacy must not be an optional feature that users must consciously enable — it must be the default state of the network.

Presumably the *proof-of-innocence* refers to the first [demo implementation](https://proofofinnocence.com/) of the Privacy Pools paper Vitalik and I wrote, so I’ll chime in here.

I think privacy by default at the L1 is a bad idea—unless we also build tools that allow (not force) users to dissociate from other users. If we don’t, then we are actually the ones *forcing* users to provide privacy to other users (including DeFi hackers, terrorists, and in the case of North Korea: both) just to access privacy themselves.

Being able to disscociate from other users actually increases my **sovereignty**, it does not decrease it. Sovereignty is about choice.

I have had this argument about 100 times since the Privacy Pools paper came out, many times with people who are triggered by the *proof-of-innocence* meme, and you can see these arguments on Twitter by searching the keyword “dissociation” on my account (ameensol): https://x.com/search?lang=en&q=dissociation%20(from%3Aameensol).

It’s also a fallacy to compare anonymous money to encryption (and personally, I wish this wasn’t true but it is). In the case of encryption, I don’t need participation from anyone else to get the benefits of being able to keep secrets. But in the case of anonymous money, if I am the only one using the anon money system, it’s pretty obvious who I am. So value I get from the anon money system is actually *socially derived* from the participation of other users, and thus the *quality* of my anonymity set matters, not just the *quantity*. If I am in the anon set that also includes North Korean hackers, I will have a much harder time getting my funds from the anon money system accepted anywhere else (and rightfully so).

[![Screenshot 2025-04-09 at 7.13.37 AM](https://ethresear.ch/uploads/default/optimized/3X/e/1/e1bb3689e4375c26771d90a79a61d365ed41d2a5_2_524x500.png)Screenshot 2025-04-09 at 7.13.37 AM1198×1142 154 KB](https://ethresear.ch/uploads/default/e1bb3689e4375c26771d90a79a61d365ed41d2a5)

source: https://x.com/delete_shitcoin/status/1521461832266956803

Being able to prove *the funds are legit* is an important part of helping combat the ability of criminals to launder money through our anon money systems. Tornado Cash & ZCash have *view keys*, where users can selectively reveal their transactions to an authority if desired. Before they both joined Vitalik and I on the Privacy Pools paper, Fabian Schar and Matthias Nadler wrote the best paper on Tornado Cash that I have seen, in which they 1) argue for the importance of privacy and 2) provide a potential regulatory framework for it: anonymous money system should be *legal*, but users should still be required to reveal their transaction history to a financial authority in order to legally access them.

I know it’s difficult, but if you can bring yourself to empathize with a regulator, the problem you face is: how do I tell the good money apart from the bad money? One solution is the above: require all anon money system users to reveal their tx history to a financial authority, and in the backend, create a data-sharing system by which we know the sum of all users that have complied with this requirement, and thus by process of elimination, we know that the rest of the money is (probably) the bad money. However, this still creates a government-owned honeypot of all the tx history which itself can be leaked or abused, and is thus not an ideal solution.

The reason Vitalik, Matthias, Fabian and I got together and wrote the Privacy Pools paper is because Vitalik thought of a potentially better way: what if we can prove in public which deposits we are *not*, allowing users to publicly dissociate from known *bad money*, and thus create a more useful separating criteria for regulators, and critically, potentially avoiding the need for a centralized honeypot of all the tx history in the first place. If I was a regulator, I would be OK with this solution. Financial institutions, if desired, could still demand the specific tx history from their users, but at least the funds are known to not be from known illicit sources, based on their public dissociation proofs.

In conclusion, I encourage any technological development we do on enhancing base layer privacy to proceed in lockstep with tools that allow public dissociation proofs, which would serve to enhance user sovereignty by allowing users to choose for themselves who they are willing to associate with.

---

**EmperorOrokuSaki** (2025-04-09):

Thank you for this thoughtful roadmap. It is encouraging to see privacy being discussed more openly within the Ethereum community. In my view, privacy is not only a foundational value but also a key limiting factor in **Ethereum’s broader adoption**.

I completely agree with [@ameensol](/u/ameensol) on the importance of selective disclosure and strong support for on-chain privacy. These ideas enable more flexible forms of interaction, which are essential as Ethereum matures into a general-purpose coordination layer.

However, the term *privacy* often serves as a catch-all. It is frequently used interchangeably to describe very different concerns: anonymity, tool usage privacy, interaction privacy, and more. Without sharper distinctions, important nuances get lost in conversation.

Right now, Ethereum’s full transparency creates a significant obstacle for everyday users. Most people do not want everyone they know to have complete visibility into their financial activity and on-chain behavior. This issue becomes more pressing as Ethereum evolves into a platform for more than just financial transactions.

Much of the current focus is on asset transfers. But Ethereum is becoming more expressive, and privacy in nonfinancial contexts like DAO governance, coordination, and social identity will become just as essential. In these cases, it is not realistic to expect every application to build and maintain complex privacy infrastructure. There is a strong case for shared infrastructure that can support these needs.

While the roadmap rightly emphasizes changes to the core protocol, it is also worth considering paths forward that do not depend on protocol-level consensus. For example, probabilistic privacy systems can offer meaningful guarantees with more flexibility and less infrastructure dependency than deterministic systems. Some ongoing efforts, including the one I am contributing to (Mirage), explore this design space. These systems enable anonymous interactions without requiring strict unlinkability, and they are not limited to token transfers. This opens the door to more private DeFi usage, salary disbursement, and other common activities.

In addition, network-level anonymity and traffic obfuscation can be developed today. These are precisely the kinds of approaches that can provide immediate relief while remaining compatible with Ethereum. Mirage focuses on this layer, exploring how probabilistic techniques and network-level strategies can improve privacy without requiring changes to the base protocol. These approaches may not solve everything, but they can address urgent privacy needs while the community works on deeper protocol changes.

In summary, I fully support the direction of this roadmap. Core upgrades are essential. But privacy is **a present concern**, not just a future goal. We should explore and support **adjacent** systems that improve the privacy of Ethereum users today without waiting for long protocol processes or consensus decisions.

The ongoing community calls and public discussions are important, and I support them. At the same time, I worry that a roadmap like this risks being sidelined as attention shifts to more immediate or politically easier priorities, something that has happened to privacy proposals time and again. We should not let that happen anymore.

---

**z0r0z** (2025-04-09):

like cash, privacy by default is lindy. I would welcome this as part of Ethereum’s credible neutrality pitch for fair settlement of agreements. I can appreciate ameen’s point that disassociation is a powerful tool - but it acknowledges a role of external governance that feels increasingly irrelevant to the challenges of the world and what people, including governments (who increasingly are users) expect of Ethereum. We might see that optionality extended to L2s or other agreements built on top, or other chains, really.

---

**vbuterin** (2025-04-11):

I wrote up my own roadmap:

https://ethereum-magicians.org/t/a-maximally-simple-l1-privacy-roadmap/23459

It’s not meant as a competitor to this; I think there’s value in doing both at the same time.

---

**kladkogex** (2025-04-11):

Hey Vitalik

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/f/9fd66b7fd30588da4b7653f8b81c28289a104f16_2_690x125.png)image1743×317 63.4 KB](https://ethresear.ch/uploads/default/9fd66b7fd30588da4b7653f8b81c28289a104f16)

This is probably going to be too complex for most users. Metamask is already terribly complex.

The more complex it is the more attacks will happen.

You can make it simpler by marking contract calls as accepting transactions from shielded accounts only. Then Metamask can automatically enforce this. Most users do not need—and do not care about—shielded transactions, and most smart contracts do not need them either. There are smart contracts like Uniswap that **do** need them; they can simply mark their contracts as requiring shielded transactions.

If I have a wallet, I should be able to have Metamask generate a private key for me and use it as a temporary “from” address, while using an existing wallet to provide gas. In fact, if Ethereum were designed from scratch, this should be done for every transaction.

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/1/914d539f08fbfbfd2dff7c5344091d18e1715a0b_2_690x164.png)image1859×443 60.3 KB](https://ethresear.ch/uploads/default/914d539f08fbfbfd2dff7c5344091d18e1715a0b)

Big changes are hard to sell to users. This is especially true since many of them frankly do not care so much about making their transaction private.   It’s probably better to discuss how to achieve things through small changes.

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/d/cdb4ea9d39046a631d2117151375e57e439f3ad3_2_690x91.png)image1843×244 49.4 KB](https://ethresear.ch/uploads/default/cdb4ea9d39046a631d2117151375e57e439f3ad3)

We have it already running on our network. Happy to collaborate with any wallets

[![image](https://ethresear.ch/uploads/default/optimized/3X/6/7/67d2292722b04019952b28312eadd2a684855f23_2_690x51.png)image1864×139 19.4 KB](https://ethresear.ch/uploads/default/67d2292722b04019952b28312eadd2a684855f23)

I don’t frankly think this is a particularly relevant problem at the moment. The computational bottleneck nowadays is state — everything else is fast. You can do many thousands of signature verifications for any signature type. For instance, with ECDSA, you can perform about 100,000 verifications per single thread.

The same is true for ZK verification, since it’s just a few pairings.

The problem about doing lots of things solving a small problem is that it makes the protocol harder to implement by someone else.  In our project for instance, it puts lots of strain on engineering resources since we need to keep up with EVM. Most ETH compatible project today de facto use older versions of Solidity compilers exacftly because it is hard to keep up with all the changes. I think most of the community will say that ETH foundation needs to do more deep analysis on how frequent changes affect the ecosystem.

---

**ml-sudocode** (2025-04-14):

I contribute some user-centric inputs for consideration, to ensure that users aren’t too far behind as we progress on the roadmap.

## 1. Reference mental models

Understanding the who/what/when/where/how of privacy in crypto is Very Complicated.

Is it your real-world identity that is private, your string of transactions, or your IP address? Private from whom – your wallet, the RPC, random snoops? Is it private only now, or even after quantum computing? How do I choose between inclusion lists (Privacy Pools) or exclusion lists (Railgun)?

**We need reference mental models** that help users avoid drowning in complexity. (Recall Tim Berners-Lee’s original vision in the 1990s, that of course everyone would run a personal web server – nope, too hard.)

It’s not just for users’ sanity – clear and widely adopted mental models also help builders avoid using conventional but crypto-fatal mental models like adding telemetry to wallets… that include wallet seed phrases (Slope wallet).

Cryptozombies, Privacy Edition?

## 2. False sense of privacy

In cybersecurity there is a phenomenon called “false sense of security.” ChatGPT describes it:

*“A false sense of security often arises when people adopt several cybersecurity tools—firewalls, antivirus software, VPNs—and assume they’re fully protected. The more tools they use, the safer they feel, even if those tools are misconfigured, outdated, or overlapping ineffectively. This illusion of safety is dangerous because it discourages deeper vigilance. True security requires more than stacking tools; it demands proper setup, regular testing, and a critical mindset.”*

The same will happen when we are trying out privacy at so many different levels. Like the legions of early bitcoin users who mistook pseudonymity for anonymity, many are going to assume they have privacy when they don’t – at least not in the ways that they assumed.

How do we combat this? I imagine this is a task for someone at the 99th percentile of intelligence and memory – i.e. we need an AI-driven solution.

Perhaps it’s an AI agent that asks us what our priorities, fears, and constraints are, and then makes a recommendation on which identity to use with which application, based on the application’s privacy boundaries. Before we sign a transaction, we quiz it for a recommendation on where and how to transact. It monitors new privacy tools as they come live, evaluates them against our personalized criteria, and proposes updates to our design.

It helps us possess a *justified* sense of privacy.

## 3. Privacy is normal, but is it worth it?

Most people want privacy, but are not willing to pay the UX cost. Will the UX overhead in this roadmap be worth it for users?

Recall the transition from physical buttons to touchscreen glass in the evolution of smartphones:

*In the mid-2000s, users were hesitant to switch from physical buttons to full glass touchscreens, associating them with laggy, stylus-dependent experiences. This changed with the 2007 iPhone, which introduced a smooth, finger-friendly capacitive touchscreen, multi-touch gestures, and a sleek design. As app ecosystems grew and large screens enhanced media consumption and navigation, touchscreens became essential. Social trends and minimalist design made button phones feel outdated. Gradually, users embraced the versatility of touchscreens.*

I’ll never forget the pain of losing the ability to type surreptitiously under the table with my Blackberry’s physical keyboard, but the switch eventually became worth it because of the bajillions of apps on the App Store, and because everyone cool was getting an iPhone.

What will make it worth it for people who don’t bother with privacy today, to bother tomorrow? Before we start another round of infra fatigue, what’s our killer app?

## 4. Privacy Parties

Let’s throw privacy day parties: people spend a whole day transferring their assets over to private addresses, contracts, wallets, etc. Like with trusted set up ceremonies, we can harness community and memes to accelerate adoption – while boosting anonymity sets =D

Finally, on that note of pushing adoption – let’s highlight that *privacy IS security*. Privacy alone is too niche, too fraught with simplistic “what about the [insert vulnerable group]” arguments. Security is universally aspirational.

---

**sgrasmann** (2025-04-14):

I totally agree that privacy - especially confidentiality - is one of the key ingredients that Ethereum is missing these days. If introduced naively, it will have bad effects on UX (additional complexity) and scalability (loss of performance due to encryption and rising gas cost). We can’t afford this. It needs proper balancing, but it is urgent.

Confidentiality is not only important from a cypherpunk perspective, but a basic requirement for any serious business that wants to use Ethereum as global settlement layer.

What I am missing from the proposed roadmap is a proper market analysis:

There is a lot of movement in the market on layer 2s (besides Aztec, e.g. Parfin’s approach with Rayls), Kaleido’s Paladin and its client side ideas, Zama’s FHE approach, mempool encryption as proposed by Shutter Network, and - maybe more important: a lot of movement on Solana, see their recent announcements (“Confidential Balances Token Extensions”) or Arcium’s orthogonal approach to bring in privacy through a separate network. Very promising from my perspective.

Ethereum doesn’t have to reinvent the wheel - and shouldn’t. Analysis and potential collaboration with some of these projects, or adoption of their approach should be prio number 1. Some of them bring real-world experience - very much driven from the markets, the users, and sometimes important regulatory aspects.

Look beyond your bubble.

---

**ivanmmurciaua** (2025-04-21):

Hey guys, thanks for bringing up this can of worms about privacy. What do you think about going forward with eip-7503?

---

**pcaversaccio** (2025-04-21):

I mention it in the first phase [here](https://hackmd.io/@pcaversaccio/ethereum-privacy-the-road-to-self-sovereignty#1-Confidential-ETH-Transactions):

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/1/b1d8d48da142de8239f7182359056773ed205daf_2_690x286.png)image1112×462 48.6 KB](https://ethresear.ch/uploads/default/b1d8d48da142de8239f7182359056773ed205daf)

As I say there, I think we first need to think about a more generalised (i.e. future-proof) transaction format. In practice, we could move forward independently, but I think it is worth (and definitely important enough) “patching” the transaction format first (i.e. make it privacy friendly; gas/mana parameters are still leaked for example).

---

**TimDaub** (2025-04-23):

Not trying to be snarky here! How does Ethereum plan to execute on making most of the transaction inclusion pipeline private when that pipeline is currently captured by entities which all have $$$ incentives to not have this pipeline be privacy-friendly?

How are you going to pressure, for example, Farcaster to make all of their mini app traffic encrypted and therefore essentially non-monetizable? Haven’t they raised at a valuation of 1B USD on this idea? No EF-funded or highly-Ethereum-aligned effort is going to build a better app than Farcaster either, right? So how can this be won for most users?

---

**Caerlower** (2025-04-30):

This is such an important conversation. Totally agree privacy shouldn’t be something users have to “earn” or “enable” manually.

While transforming Ethereum at core level into maximally private would be awesome as it will enable privacy by default, right now one project which came to my mind regarding privacy on EVM would be Oasis Protocol which is already pushing for privacy at the protocol level, with confidential smart contracts and data privacy baked in.

Would love to see more of that mindset brought into Ethereum too, as it will enable data protection at greater level.

---

**kladkogex** (2025-05-02):

We are launching **BITE**, a privacy-oriented blockchain that extends EVM and Solidity with support for encrypted transactions and data.

The test net is roughly scheduled for this summer

We’re looking for DApps interested in collaborating with us to test and explore the protocol.

More details here!


      ![](https://ethresear.ch/uploads/default/original/3X/2/3/236cd96fb63737c6399a8bd7087ffba98018629a.png)

      [SKALE Network Forum – 2 May 25](https://forum.skale.network/t/bite-solving-blockchain-privacy-in-four-phases/597/5)



    ![image](https://ethresear.ch/uploads/default/optimized/3X/5/b/5bb3c345cd9175ce8007a33787fd572b63699813_2_500x500.png)



###





          dApp Developers






hey @kladkogex ! thanks for the amazing insights. how do you think each of the features and functionalities you mentioned will impact on transaction throughput and gas costs? it feels like every phase brings more and more heavy mathematical...

---

**ivanmmurciaua** (2025-05-05):

I don’t know how to handle this guys: `https://cointelegraph.com/news/eu-crypto-ban-anonymous-privacy-tokens-2027`

Does the discussion of this news item fit in this post?

I think Ethereum has a great community but crypto is losing Europe (or maybe the other way around) but certainly Ethereum should improve privacy without losing any territory. Such a crazy world can’t end well for cryptousers.

I will continue to defend privacy but Ethereum must consider these types of eventualities IMHO.

---

**kladkogex** (2025-05-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/ivanmmurciaua/48/16020_2.png) ivanmmurciaua:

> ttps://cointelegraph.com/news/eu-crypto-ban-anonymous-privacy-tokens-2027

Governments around the world have made it clear—they’re not fans of true privacy.

Monero, arguably one of the most *useful* cryptocurrencies, has become a target. People use it for real-world needs, like accessing affordable prescription medications on the darknet. But instead of acknowledging its utility, regulators have made Monero nearly impossible to buy—delisting it from exchanges not just in Europe, but globally.

Why? Because the more centralized, surveillance-friendly, and U.S.-based a crypto project is, the more governments seem to embrace it.

Enter Base and the broader rollup ecosystem—an ideal setup for regulators. Now, Base claims to be decentralized because it appointed a “decentralization council”… comprised almost entirely of its own employees. Vitalik even calls Base a “Stage 2” rollup. But if this is Stage 2, has the term lost all meaning? Weren’t rollups *supposed* to be decentralized? Now we’re told it’s fine for them to take *years* to decentralize. Really? How many years did it take Satoshi to decentralize Bitcoin?

Back in the day, everyone criticized EOS for having “only” 21 validators. Meanwhile, Ethereum is now effectively controlled by just three entities: Coinbase, Binance, and Lido—two of which are U.S. corporations.

Something to think about.

