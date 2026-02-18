---
source: ethresearch
topic_id: 20920
title: Censorable Tornado Cash
author: Mirror
date: "2024-11-03"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/censorable-tornado-cash/20920
views: 788
likes: 3
posts_count: 8
---

# Censorable Tornado Cash

I’m currently researching Tornado Cash, mainly because I believe it’s a proven application of ZK technology and has broad privacy-oriented uses for community members. I’ve created this thread to discuss it with everyone.

**Tornado Cash** (also stylized as **TornadoCash** ) is an [open source](https://en.wikipedia.org/wiki/Open_source), [non-custodial](https://en.wikipedia.org/wiki/Custodian_bank), fully [decentralized](https://en.wikipedia.org/wiki/Decentralised_system) [cryptocurrency tumbler](https://en.wikipedia.org/wiki/Cryptocurrency_tumbler) that runs on [Ethereum Virtual Machine](https://en.wikipedia.org/wiki/Ethereum_Virtual_Machine)-compatible networks. It offers a service that mixes potentially identifiable or “tainted” cryptocurrency funds with others, so as to obscure the trail back to the fund’s original source. This is a privacy tool used in EVM networks where all transactions are public by default.



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Tornado_Cash)





###

 Tornado Cash (also stylized as TornadoCash) is an open source, non-custodial, fully decentralized cryptocurrency tumbler that runs on Ethereum Virtual Machine-compatible networks. It offers a service that mixes potentially identifiable or "tainted" cryptocurrency funds with others, so as to obscure the trail back to the fund's original source. This is a privacy tool used in EVM networks where all transactions are public by default.
 In August 2022, the U.S. Department of the Treasury blacklist...










Nocturne is a protocol enabling private accounts on Ethereum. Imagine a conventional Ethereum account but with built-in asset privacy. Nocturne allows users to deposit or receive funds to private, stealth addresses within the Nocturne contracts. Then, in the future, a user can prove ownership of assets in zero knowledge for use in arbitrary transactions or confidential transfers.It is currently abandoned.

https://nocturne-xyz.gitbook.io/nocturne

## The Privacy-Audit Dilemma Facing Privacy Coins

#### How Tornado Cash Achieves Privacy Protection

At the core of Tornado Cash’s privacy capability is ZK technology, which enables proof of ownership without revealing user identities or transaction details. Tornado Cash’s main contracts, known as pools, are designed for deposit and withdrawal operations. Users deposit funds into a pool contract and receive an anonymous proof to use later for withdrawal, thereby obscuring the original source of funds.

#### How Privacy Protections Can Facilitate Illicit Activities

This anonymity makes Tornado Cash a favored tool for money laundering. Several documented cases illustrate how malicious actors have leveraged Tornado Cash’s anonymity to launder stolen funds, often evading regulatory scrutiny. Criminals have effectively obscured the money trail, making it difficult for law enforcement to track illicit transactions.

#### The U.S. Treasury Sanctions on Tornado Cash

In August 2022, the U.S. Treasury’s Office of Foreign Assets Control (OFAC) sanctioned Tornado Cash, adding its associated USDC and ETH addresses to the Specially Designated Nationals (SDN) list, barring U.S. residents from using the service. The Treasury cited Tornado Cash’s role in numerous decentralized finance (DeFi) hacks, where individuals and groups allegedly laundered over $7 billion worth of cryptocurrency through the platform since its inception in 2019.

### Future Evolution of Privacy Transactions: Selective Auditing as a Path Forward

As privacy solutions evolve, selective auditing features may become standard, enabling both anonymity for users and transparency for regulators. For example, Japan’s recent crackdown on a Monero laundering operation involving over 100 million yen highlights the global regulatory push for compliance in privacy-preserving systems.

### Balancing Anonymity and Auditability

#### The Role of Zero-Knowledge Technology

Zero-knowledge proofs (ZKPs) are central to maintaining anonymity in the cryptocurrency space. By proving information without revealing it, ZKPs provide a basis for private transactions. However, purely anonymous systems can pose regulatory challenges. Recent innovations in ZK technology, like “partially decryptable zero-knowledge proofs” or Selectively Auditable Zero-Knowledge Proofs (SA-ZKPs), offer a promising balance between privacy and auditability.

#### The SA-ZKP Algorithm

The SA-ZKP algorithm comprises the following components:

1. Commitment Scheme C=(CKeygen,Commit,COpen)C = (CKeygen, Commit, COpen)C=(CKeygen,Commit,COpen): Establishes a commitment to private data, allowing it to be used in proofs without revealing it.
2. Zero-Knowledge Proof Σ=(K,P,V)\Sigma = (K, P, V)Σ=(K,P,V): Allows verifiable proof of commitment without disclosing the committed data.
3. Trapdoor Generation: Creates a cryptographic “trapdoor” to enable selective auditability.
4. Selective Decryption Process: Allows authorized entities to selectively decrypt committed data for regulatory auditing.

### Regulated Tornado Cash Workflow with SA-ZKP

Applying the SA-ZKP algorithm to a regulated version of Tornado Cash could create a privacy-compliant framework with selective auditability:

1. Regulator Registration (Trapdoor Generation): Regulators register with the network to gain access to audit permissions through a cryptographic trapdoor.
2. Transaction Flow: Users deposit funds anonymously, with cryptographic commitments created for auditing if necessary.
3. Audit Process (Selective Decryption): In cases of suspicious activity, regulators can selectively decrypt transaction data to investigate without compromising the privacy of all users.

By integrating SA-ZKP with Tornado Cash’s core operations, we can achieve a dual objective: respecting user privacy while empowering regulatory authorities with necessary oversight capabilities.

**If I were to launch a new version of a mixer, where I would decrypt specific transaction proofs for law enforcement using a trapdoor key when requested, would you still use this mixer? Why or why not?**

## Replies

**MicahZoltu** (2024-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/mirror/48/13378_2.png) Mirror:

> Tornado Cash (also stylized as TornadoCash ) is an open source, non-custodial, fully decentralized cryptocurrency tumbler that runs on Ethereum Virtual Machine-compatible networks. It offers a service that mixes potentially identifiable or “tainted” cryptocurrency funds with others, so as to obscure the trail back to the fund’s original source. This is a privacy tool used in EVM networks where all transactions are public by default.

I don’t recommend using Wikipedia’s definition, it is worded specifically to make Tornado Cash sound like a criminal tool rather than a privacy tool.  It is a tool that lets you deposit assets from one account and withdraw from another account without the two accounts being linkable to each other.

![](https://ethresear.ch/user_avatar/ethresear.ch/mirror/48/13378_2.png) Mirror:

> As privacy solutions evolve, selective auditing features may become standard, enabling both anonymity for users and transparency for regulators. For example, Japan’s recent crackdown on a Monero laundering operation involving over 100 million yen highlights the global regulatory push for compliance in privacy-preserving systems.

Tornado Cash already has this ability.  Unfortunately, the US government doesn’t care and it didn’t stop them from taking the actions they took.  There is no evidence that adding auditability to a tool will placate the government, they want nothing short of completely un-mitigated transparency into everyone’s personal finances, despite the constitution protecting such things.

A privacy tool with a backdoor isn’t a privacy tool.  It is like buying a camera in your house that “select actors” can gain access to without your permission.

![](https://ethresear.ch/user_avatar/ethresear.ch/mirror/48/13378_2.png) Mirror:

> In cases of suspicious activity, regulators can selectively decrypt transaction data to investigate without compromising the privacy of all users.

It seems quite unrealistic to believe that the state would restrain its usage of such a tool at its disposal.  They already have similar tools with traditional finance that they use without warrant to spy on innocent people.

---

**Mirror** (2024-11-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I don’t recommend using Wikipedia’s definition, it is worded specifically to make Tornado Cash sound like a criminal tool rather than a privacy tool. It is a tool that lets you deposit assets from one account and withdraw from another account without the two accounts being linkable to each other.

I completely agree with your viewpoint; it’s a misconception to consider Tornado Cash as a criminal tool. Since the Tornado Cash website is offline, I selected a more objective and widely recognized media source for its introduction.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Tornado Cash already has this ability. Unfortunately, the US government doesn’t care and it didn’t stop them from taking the actions they took. There is no evidence that adding auditability to a tool will placate the government, they want nothing short of completely un-mitigated transparency into everyone’s personal finances, despite the constitution protecting such things.
>
>
> A privacy tool with a backdoor isn’t a privacy tool. It is like buying a camera in your house that “select actors” can gain access to without your permission.

Tornado Cash doesn’t have the capability to enable criminal activities, nor does the subsequent mixing pool, Nocturne, as both employ AAML (Advanced Anti-Money Laundering) identification techniques. These technical methods can only assess the past behavior of addresses but cannot prevent ongoing crimes. As a result, these projects are often marked with a tombstone.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> It seems quite unrealistic to believe that the state would restrain its usage of such a tool at its disposal. They already have similar tools with traditional finance that they use without warrant to spy on innocent people.

Granting power to the government will inevitably lead to abuse, which we all know is bound to happen. Therefore, I’m considering a collaborative approach via public documentation rather than directly giving the government surveillance rights. I’m currently exploring holding decryption keys for specific transactions in a decryptable multi-signature format with INTERPOL. This is mainly to ensure the continuity of the mixer and prevent me from spending the rest of my life in prison, unable to continue serving the community. I hope this approach can help the community achieve a certain degree of privacy.

---

**MicahZoltu** (2024-11-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/mirror/48/13378_2.png) Mirror:

> Since the Tornado Cash website is offline

Tornado Cash website is still available from multiple places, including IPFS ipfs://bafybeicu2anhh7cxbeeakzqjfy3pisok2nakyiemm3jxd66ng35ib6y5ri.  It is just code, so anyone can serve it and many people do.  https://tornado.cash was just a convenient way to make it available to people, it isn’t at all required or critical to its operation (despite what the Treasury’s lawyers try to claim).  I personally have it available at https://bafybeicu2anhh7cxbeeakzqjfy3pisok2nakyiemm3jxd66ng35ib6y5ri.ipfs.zoltu.io, though I encourage people to access it through their own IPFS gateway rather than mine.  Also, there is a newer version that has been updated since the sanctions.  The last build I audited was back in April last year: ipfs://bafybeiezldbnvyjgwevp4cdpu44xwsxxas56jz763jmicojsa6hm3l3rum

![](https://ethresear.ch/user_avatar/ethresear.ch/mirror/48/13378_2.png) Mirror:

> As a result, these projects are often marked with a tombstone.

A project being unable to censor people’s access is only a “tombstone marker” if you believe that the world cannot have or does not desire financial privacy.  This is the crux of the disagreement between many people and the state, as the state has a strong dislike of financial privacy, while many people believe that financial privacy is a right that all people should have.

![](https://ethresear.ch/user_avatar/ethresear.ch/mirror/48/13378_2.png) Mirror:

> Granting power to the government will inevitably lead to abuse […] I’m currently exploring holding decryption keys for specific transactions in a decryptable multi-signature format with INTERPOL.

INTERPOL is not incapable of abuse.  No human nor group should have a backdoor around financial privacy, because *any* actor with such power will inevitably be captured and abuse that power.

![](https://ethresear.ch/user_avatar/ethresear.ch/mirror/48/13378_2.png) Mirror:

> This is mainly to ensure the continuity of the mixer and prevent me from spending the rest of my life in prison, unable to continue serving the community. I hope this approach can help the community achieve a certain degree of privacy.

If building privacy software has you fearful of prison, then I recommend waiting for Roman’s case in the US to resolve, and if necessary get challenged up to SCOTUS.  I am strongly of the opinion that he did not commit any crime and the treasury is reaching way too far in arresting him.  Especially with Chevron recently overturned by SCOTUS, I don’t think the state has a real case here.  It *should* have been dismissed as no crime was committed, but unfortunately the Judge wants it to go to trial.

Building censorable financial tools doesn’t leave us in any better of a situation than the current TradFi situation.  Blockchains specifically provide censorship resistance and that comes at great cost.  If you *want* censorship, then I think using a blockchain is just a huge amount of complexity and overhead for no gain.

---

**cryptskii** (2024-11-09):

for another POV on things may I draw your attention to [GitHub - Tonnel-Network/core: First ZK project built on TON blockchain, based on 🌪 Cash](https://github.com/Tonnel-Network/core) I personally I enjoy, and sometimes gain perspective I wouldn’t have if not assessing other derivatives such as this one here. Just thought I’d bring it to your attention. Hopefully it helps. Also, I could mention that the project I am focussed on and implementing from all the posts I’ve shared is censorship immune by design. fully auditable, verifiable yet private I believe it checks all these boxes. I’ve only skimmed your post here very quickly prior to making this comment. I will reread and edit if needed when I have more time. You bated me with tornado ahah.

---

**Halva777** (2024-11-16):

How might the introduction of Selectively Auditable Zero-Knowledge Proofs (SA-ZKPs) influence future regulatory frameworks for privacy-preserving technologies?

---

**doner66** (2024-11-17):

In a world where privacy and regulatory compliance seem to be at odds, how can we design cryptographic systems that maintain true decentralization while providing selective transparency without creating centralized points of failure?

---

**71104** (2025-06-03):

Besides seconding everything that MicahZoltu said, how do you decide who is a qualified “regulator” and who is not? You wrote this:

> Regulator Registration (Trapdoor Generation): Regulators register with the network to gain access to audit permissions through a cryptographic trapdoor.

Can *anyone* “register with the network”? If not, who approves these regulators and trapdoors? If they are chosen democratically by voting in a DAO, would there be a way to remove them should they start abusing their powers?

PS: to answer your final question directly: no, I wouldn’t use such a system.

