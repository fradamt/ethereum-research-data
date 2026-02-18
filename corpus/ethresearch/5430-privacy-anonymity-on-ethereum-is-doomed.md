---
source: ethresearch
topic_id: 5430
title: Privacy/Anonymity on Ethereum is Doomed
author: HarryR
date: "2019-05-09"
category: Cryptography
tags: [transaction-privacy]
url: https://ethresear.ch/t/privacy-anonymity-on-ethereum-is-doomed/5430
views: 7797
likes: 15
posts_count: 15
---

# Privacy/Anonymity on Ethereum is Doomed

I will be straightforward here, because I think it needs saying.

As a public blockchain, it will be impossible for Ethereum as a platform to deliver any meaningful or realistic guarantees of privacy or anonymity, unless some fundamentals are addressed first. On private blockchains, such as deployed ‘in enterprise’, this is less of problem - iif all participants use the same privacy mechanism and somehow get around the ‘gas payer problem’.

However, the crux of the problem is that if *more than one* ‘privacy solution’ gains traction on Ethereum main-net, the fact that the anonymity pool is split into factions will do nothing more than reduce privacy for *everybody*. In this sense - competition will hurt the ecosystem, aside from in a few specific situations.

---

What do I mean by privacy?

- No previous or future actions can be associated with, or correlated to, a specific actor.

Think of it in the sense of Perfect Forward Secrecy™, that even if my Ethereum account is fully compromised - my secret keys are leaked to the world etc., nobody should be able to see what I did in the past - and no other key holder should be able to see what I do in the future. It is an ideal.

---

Ethereum is fundamentally unable to accomplish any part of this Ideal, especially so in a public blockchain setting, because transactions need to be paid for, and there is a linkable history of the movement of funds between accounts this puts the burden of anonymity on the gas payer - they must somehow fund a one-time account without linking it to any of the other accounts. Good luck with that.

One solution is to have ‘transaction proxies/relays’, where you somehow refund the transaction submitter when they successfully execute your transaction, this introduces three really nasty things:

1. You now have an intermediate with a profit-seeking incentive between you and the miner, who are offering a potentially unreliable service which shouldn’t ever need to exist
2. You have to re-design all of the smart contracts (imo… design them ‘properly’), to handle relayed transactions, this puts 99% of the current Ethereum ecosystem out of reach of transaction relay services due to ‘custodial risk problems’ (e.g. msg.sender being the owner of your funds)
3. Censorship, IP logging, capitalist market capture etc. etc. (hello Infura)

The other solution is to use ‘account abstraction’, where any legitimate transaction will be executed iif it appropriately compensates the miner, this is essentially the same solution as ‘transaction relays’, just replace ‘miner’ with ‘relayer’ - it has the same problems: you need to re-design/re-implement a lot of the current smart contract infrastructure to not give anybody and everybody your funds due to shared `msg.sender`, or to be able to access your funds again (because your previous `msg.sender` isn’t the same as your current one).

---

Many ‘anonymity factions’ are worse than a fundamental fix.

Even if we were to implement account abstraction, and then re-design all of the smart contracts to handle the subtleties, then deal with all of the privacy-breaking bugs in the 1000 different implementations, and make everything stop relying on `msg.sender` as a concept of authorisation/authentication etc.

The reality is that 99% of people would just use transparent transactions, without any anonymity or privacy.

But, an issue which is specific to Ethereum, is that instead of - like with ZCash - the remaining 1% of ‘private transactions’ all use the same technology with a shared anonymity set. Instead - you have many competing and incompatible ‘privacy solutions’ with their own anonymity sets, if there are 10000 users who want privacy, but they are equally spread across 10 different ‘privacy solutions’ - they all have far less privacy than if they stuck with one - and they started with *even less* than they should’ve had because everybody else doesn’t know/care/whatever.

Where is ZCash is now? 99% of the transactions are ‘transparent’, but the majority are traders/exchanges speculating about the value of anonymity and privacy by investing in a ‘privacy coin’ while not using its one and only benefit compared to BitCoin (the irony, it burns…) meanwhile teams of PhDs analyse every ‘private transaction’, with an anonymity set of hundreds, or possibly thousands, compared to the millions that it *could be*.

That is worse than Monero, but both are 10x what Ethereum ever possibly could be without really fundamentally addressing this problem - instead we are doomed to add our wishes to the pyre, which only encourages the flames.

---

TL;DR any privacy technology based on Ethereum, which isn’t used in a strictly controlled enterprise environment, is not only fundamentally dead and floating, but even more than that - trying to compete in ‘privacy on public ethereum’ is causing self inflicted harm and collateral damage.

---

</bitching>

<solutions>

…

## Replies

**Mikerah** (2019-05-09):

I 100% agree with what you have written here and have had conversations in private with people who feel the same way. In order to get any meaningful privacy/anonymity, it would require an overhaul of how Ethereum currently works. This is unfeasible as there are a lot of vested interest in the current chain through DApp developers, core devs and other stakeholders. I have already relented to the fact that only opt-in privacy can be achieved on Ethereum today, unless there’s a change in priorities with regards to privacy/anonymity.

---

**fubuloubu** (2019-05-09):

I think the one assumption is that individual people are supposed to use on-chain privacy directly. To me, it seems obvious that 1) privacy at Layer 2 is a much easier, and 2) scalability, UX, fee economics, etc. are better at Later 2. Unless you are participating in the opt-in economics of Layer 1 composability (DeFi use cases, asset issuance, etc.), you are much better served as an individual user by nearly every single metric with Layer 2 solutions.

Transparency is the default on Layer 1, and as you note, it may not be possible to work around it. But that is not a bad thing, as long as the systems we build are properly built to manage that transparency and protect it from any PII being shared. In my opinion, Ethereum is a base layer for developers and institutions to build on top of and trustlessly coordinate with, and the transparency of that is fundamentally important to ensure it works as well as it needs to.

Too much privacy on the base layer can have significant ramifications, for example the inability to audit economic invariants (also an issue with Zcash and Monero). Insecure smart contracts may lead to loss of certain party’s funds, but opaque privacy-preserving mechanisms that are broken affect *everyone* that uses those systems, and may lead to systemic failure that could spread out to other components of the system and other systems in the ecosystem.

---

Think about if Maker CDPs were privacy-preserving, but had a bug that broke the 150% collateralization invariant (instead allowing 75%, or printing double the DAI). Now compare that with a ZK version of the xDAI chain that was broken (can transfer funds you didn’t have). The former breaks Ethereum and affects a lot of projects; the latter affects a much smaller subset of parties, but wouldn’t print more DAI than the collateral on the main chain can back.

---

**Mikerah** (2019-05-09):

You make good points. However, I think what [@HarryR](/u/harryr) was getting at is that you don’t get much financial privacy as one would get with, say, Monero.  Nobody wants their entire financial transaction history public for the world to see. But, in the context of DApps, this may not be as much of an issue, unless we want completely privacy-preserving smart contracts.

---

**MaverickChow** (2019-05-09):

A system that is 100% public is no good as everyone’s wealth will be known, but an advantage to this is law enforcement can hunt down criminals and reduce crime. Contrary to that, a 100% private system would protect everyone’s privacy but criminal operations would be unstoppable. So I think we need to find a sweet spot between these 2 extremes.

“…they must somehow fund a one-time account without linking it to any of the other accounts. Good luck with that.”

I believe this can actually be easily done, without the need for this one-time account, and still preserve privacy to an extent.

---

**fubuloubu** (2019-05-09):

Many institutions have public reporting requirements, and if open businesses become a thing, it will probably be very helpful to contributors to know what’s going on.

I see a big benefit for businesses that have to report, they might settle out their holdings on a quarterly basis (or faster) and use the “public record” to fulfill their reporting requirement without additional work. 99% of their operations could occur on Layer 2 systems with better privacy (probably a requirement for any business with sensitive financials), but there is definitely a benefit to a public settlement layer at the base of it all (besides proof of auditability of the underlying systems’ economics i.e. not building skyscrapers on sand)

---

**Econymous** (2019-05-17):

Having a batch of keys for access to a particular address state tied to a contract.

Idk, instead of operating from the UI with one private and public key, somehow have a batch associated with the core currency and have that batch of keys change with every transaction. then get another batch of keys (that changes with each transaction) for an interaction with a smart contract. and of course use multiple nodes for pushing every transaction. The UI would have to manage a lot.

Really just talking out of my ass on this one, but kinda sorta just hunching maybe.

The solution may need to be as elaborate as using physical space and autonomous iot systems to “physically” secure privacy.

Something elaborate like this sounds more feasible.

ironically, you’d need to be in a publicly connected area for either of these to even come close to remotely working because you’d need to make sure your request to the network wasn’t being funneled through 1 malicious actor.

[@Mikerah](/u/mikerah)

Mainchain can be public. and mainchain being public may be “the right thing” for the world. Sidechains can be private.ah…yeah. that guy said it

[@fubuloubu](/u/fubuloubu)  ![image](https://ethresear.ch/uploads/default/original/2X/1/1bfbed13ebeed203721910dfd025a6253df01611.png)

ah yeah. yeah. this is key

[@fubuloubu](/u/fubuloubu)  ![image](https://ethresear.ch/uploads/default/original/2X/2/28ba3c28981e08b0b41934c6c22d49db3351c9b0.png)

yeah, that guy gets it

---

**Econymous** (2019-06-09):

I disagree. We don’t need privacy right away. And quite honestly, it’s very dangerous.

Open ledgers are good for a mass re-org of top level entities. The federal reserve, for instance.

People are crafty. And people are evil.

We also have proof of location. Combine that with privacy and I could personally think of a few things that would reck society as we know it.

Terrorism. Sex trafficking, data mining the mass subconscious of the population and weilding that data to isolate them into perception bubbles that run their lives.

You could collect people like marbles. Privacy would be the only true form of power. And if everyone had it, we’d be sent back to the Stone age very fast except this Stone age would have wizards with magical money towers(something close to mining rigs)

They’d be like gods, and everyone else would be like ants.

Is that what you want? You want me to get away with this?

---

**HarryR** (2019-06-10):

> You could collect people like marbles. Privacy would be the only true form of power. And if everyone had it, we’d be sent back to the Stone age very fast except this Stone age would have wizards with magical money towers(something close to mining rigs)

You state it as if isn’t already true…

> What I mean by confidentiality is: yes, your tx input is encrypted but if anyone can see that you’ve sent X amount of Ether to a wallet that’s known for X then one can assume that you’re in a business transaction with that company/individual - that’s not meant for the public to know.

I think there are three arguments here (and in your previous paragraph):

1. Protecting people from exploitation (e.g. via data-mining, freedom of association)
2. Enabling businesses to take risks: you can’t play poker when everybody knows your cards.
3. Ensuring fairness, between the players of risk games, and our individual rights to privacy.

Ideally we want a realistic balance between them, which is compatible with some form of a morally agreeable future (even though it may not be compatible with *current laws*), and which can adapt to overcome our inevitable shortsightedness. The introduction of GDPR reflects a growing concern with the concept of data sovereignty and inadequate operating procedures for those responsible for protecting our data, much as the PCI compliance standards could be seen as the last major industry-affecting introduction of regulations in a similar vain.

Another goal which is crucial to think about is reducing bureaucratic burden of compliance, either as a GDPR subject to request removal of data, or to streamline accounting and financial integrity requirements such as Sarbanes-Oxley without additional work because the data for all reports is public verifiable, continuously running and only accessible to those who are authorised.

There are bubbles of privacy which are achievable on Ethereum, e.g. payment channels between multiple custodial entities making net-settled payments to each other on behalf of others, where the individual payments are hidden but can be proven to have occurred without disclosing any of the details. But that’s still custodial… and only works because it’s essentially offline with only the aggregate movement of funds between the custodians being made public.

But for direct users of Ethereum, without a non-custodial trustless way of making confidential transactions, we see everything from everybody. With privacy preserving smart-contracts we would still be able to see which ones you’re interacting with and the total in/out of funds on a per-transaction basis, but it would solve half the problem - if privacy preserving smart contracts were the default - where nobody could see the result of anything you did with it or how the internal state changed - then everything would be privacy preserving by default (e.g. confidential ERC-20 would come for free).

You would still see that some account made N transactions to M different smart contracts, but maybe we can solve that too?

---

**kladkogex** (2019-06-12):

I think SGX plus some type of a decentralized continuous audit to verify that validators use SGX is where the industry will go in 2020.  This solution is pretty reasonable for most ecommerce solutions imho.

It is easier to implement on a side chain since the number of nodes on the side chain is more or less fixed.

---

**Econymous** (2019-06-17):

Not sure if anyone is aware of these two pieces of work.

Way over my head.

I think they still have the privacy limitations of the privacy coins we know of today. It’s just a smart contract version.

[Zexe: Enabling Decentralized Private Computation](https://eprint.iacr.org/2018/962.pdf)

[Zether: Towards Privacy in a Smart Contract World](https://crypto.stanford.edu/~buenz/papers/zether.pdf)

Because of their limitations I think that true privacy will remain a service.

With enough progress (law and tech), we can [trustlessly assemble privacy centers](https://www.youtube.com/watch?v=Ai3jAsGlej8)

Basically, distributed  ownership of land that is dedicated to privacy and other services.

---

**kladkogex** (2019-08-14):

At SKALE we are working to move the entire EVM into SGX.  This will provide privacy good enough for commercial applications.

---

**kladkogex** (2019-08-16):

Yep - thats what we have at SKALE ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**kladkogex** (2019-08-16):

Jena - Great - message me at [stan.kladko@skalelabs.com](mailto:stan.kladko@skalelabs.com)

---

**mathcrypto** (2019-08-24):

I believe using Intel SGX hardware can be dangerous in some cases. In the computation context, data should be protected from any type of modification or access. However, most of Intel Hardware chips have been found to be vulnerable to some attacks (Meltdown, Spectre and Foreshadow).

The first two attacks (Meltdown, Spectre) allow an attacker to access private data by misleading speculative scouts into a speculative execution attack. Compared to other Intel Hardware chips, the SGX is resilient to speculative attacks but unfortunately, it is vulnerable to another type of attack called Foreshadow. This vulnerability enables an attacker to create a shadow copy of the protected data into a different unprotected location.

Another reason why hardware approaches are not privacy preserving is that data is encrypted on the client side with the public key of the server (which is an untrusted party), instead of being encrypted with the client public key. This system requires data within the enclave to be decrypted before being processed. If an attacker manage to access the enclave, it will then be easy to recover plain text data.

I agree with [@fubuloubu](/u/fubuloubu) on the fact that layer 2 solutions can provide better privacy because we will be able to do off-chain heavy computation and reduce the load on the Ethereum network. The privacy aspect can be added by using tools like ZKP, HE and SMPC.

I also believe we should start thinking how dApps can be GDPR compliant as [@jenababe](/u/jenababe) suggested. The world’s 500 biggest corporations are already on track to spend a combined total of $7.8 billion to comply with GDPR and adopt  privacy by design approach in several industries. This regulation creates an opportunity for different industries like healthcare, financial industry, government and others and if we don’t make Ethereum compliant then we will miss the opportunity of leading the field and will not be able to compete other technologies in what they offer.

