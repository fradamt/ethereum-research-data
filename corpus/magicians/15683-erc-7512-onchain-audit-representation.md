---
source: magicians
topic_id: 15683
title: "ERC-7512: Onchain Audit Representation"
author: rmeissner
date: "2023-09-05"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7512-onchain-audit-representation/15683
views: 6454
likes: 24
posts_count: 29
---

# ERC-7512: Onchain Audit Representation

Discussion for [Add EIP: Onchain Representation for Audits by rmeissner · Pull Request #7652 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7652/files)

The purpose of the ERC is to propose a standard to represent audits onchain. Any discussion related to this can be facilitated here.

## Replies

**Dexaran** (2023-09-06):

The idea of having on-chain audits is useful. However the implementation proposed in this ERC is overcomplicated significantly.

The goal of having on-chain audit registry is to allow contracts to verify if a contract is secure or nobody ever reviewed it (the fact that it was reviewed and assigned a “secure” label does not automatically mean that it is really secure however).

Taking this into account lets review audit properties:

- Auditor - Do we need it at all?

name - well, there are better ways of recognizing auditors. For example just keep a track of auditors addresses in an open registry and let contracts match the issuer of the on-chain report against one of the auditors publicly available addresses.
- uri - it doesn’t tell contract anything. A human can follow the link and read whatever is written there but not the contract.
- authors - it doesn’t tell contract anything.

Audit

- auditor - ok
- contract - ok, chainID and address are useful.
- issuedAt - may be
- ercs - why is it important at all? I don’t think that a contract may want to conduct this type of standard recognition via audit reports instead of ERC-165 for example. Also, USDT is not compliant with ERC-20 spec, do you expect some auditor like OpenZeppelin or CertiK to say “USDT is not a ERC-20 token”?
- auditHash - ok
- auditUri - ok

### Auditor Verification

Why would someone need such a complex system of auditor verification if that same task can be accomplished in a much easier way - just let auditors submit audit reports from a publicly known address and match addresses to the name of the auditing company.

Like `0x111111` is OpenZeppelin

`0x222222` is CertiK

`0x333333` is Callisto Audits

etc.

You don’t need such a complex structure and the whole load of processes for signing / verifying if it can be done in a way that would allow even a technically inexperienced user to verify who is the auditor.

### The current ERC does not have any mentions of the findings of an audits.

This is the most crucial part honestly. There can be multiple audit reports for one contract and if **at least one** indicates a problem with the contract - it is more important than all other reports that do not indicate any problems with this exact contract.

**If you have 3 auditors who have reviewed one contract, two of them found nothing and the third found a critical vulnerability - it’s much more logical to indicate that “the contract might have a critical vulnerability”** rather than resort to an assumption “if there is at least one audit report that doesn’t indicate any problems then the contract is most likely safe”.

I think that a system that does not allow for findings specification and independent audits submissions for multiple different auditors - will not work or even worse it will deceive users into thinking that some contract is secure while in fact there are problems with it.

---

**Dexaran** (2023-09-06):

I would propose an alternative structure for on-chain audits.

Create a “registry” contract that will allow anyone (or a select group of addresses) to issue an “audit report” for another address. This “audit report” should act as a Soulbound Token with configurable properties.

I have proposed this type of NFTs in the past (it is easy to turn into SBT by simply removing transferring features):



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png)
    [ERC CallistoNFT standard](https://ethereum-magicians.org/t/erc-callistonft-standard/8399) [Tokens](/c/tokens/18)



> ERC - CallistoNFT
> Preamble
> EIP:
> Title: Non-fungible Container Token Standard
> Author: Dexaran
> Type: Standard
> Category: ERC
> Status: Draft
> Created: 2022-22-02
>
> Simple Summary
> An interface for non-fungible tokens and minor behavior logic standardisation.
> Abstract
> This standard allows for the implementation of a standard API for non-fungible tokens (henceforth referred to as “NFTs”) within smart contracts. This standard introdu…

The SBT must contain the following properties:

1. Issuer - the address of the auditor or an auditing company
2. Critical findings: number
3. High severity findings: number
4. Medium severity findings: number
5. Low severity findings: number
6. Audit hash
7. Audit report link
8. Chain ID

It is possible to leave severity assignment to auditors I think.

In this way it would be possible to ask one contract (registry) and get a list of audits if there are multiple. At the same time if there is already one audit report that says “everything is fine with the contract” but in fact the contract has security problems - there will be a way for other auditors to submit reports that point out security problems of the contract.

---

**rmeissner** (2023-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> Create a “registry” contract that will allow anyone

The purpose of the ERC is not to define the registry, but rather a format in which audits can be represented on chain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> type of standard recognition via audit reports instead of ERC-165

The security implications are quite different if a contract can self proclaim what they support and if you get an external party “verify” that they follow a standard. Also not all ERCs are interface standards.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> do you expect some auditor like OpenZeppelin or CertiK to say “USDT is not a ERC-20 token”

Yes that would be the correct way and is actually critical for implementations building on top of such standard. Some tokens that claim to be ERC-20 compatible, but because of different behavior of their `transfer` function require contracts building on top to implement special handling just for these contracts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> Auditor - Do we need it at all?

That is a good question and it should be considered. The `authors` fields was meant to provide a indicator which auditor was actually auditing the contracts (as there are differences within audit companies), but there are alternative ways to represent this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> The current ERC does not have any mentions of the findings of an audits.

This has been discussed with some auditors before and it would be indeed very helpful, but there are some challenges on how to align on the definition for the severity. To not make the ERC more complicated leaving it out would be a first step.

I agree that leaving this classification up to the auditors is also a solution. I would rely on the impact of the auditors for this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> just let auditors submit audit reports from a publicly known address and match addresses to the name of the auditing company.

As the ERC aims to only create a representation of an audit and not define how it is handled on chain, the definition of the verification scheme make it possible to use them independently of specific chain allowing a verification of the representation offchain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> Medium severity findings: number
> Low severity findings: number

How useful are these? Normally medium and low severity findings are not security critical and the usage of the auditors of these states might differ.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> This “audit report” should act as a Soulbound Token with configurable properties.

In my opinion this would be an application of an onchain audit representation. I.e. auditors would create the representation, sign it and then anyone could submit it to create a SBT based on it that can be used onchain.

---

**PatrickAlphaC** (2023-09-11):

I’ve thought a decent bit about this, and every time, I conclude: “What would this accomplish?”

At the end of the day, audits (henceforth, “security reviews”) are for the protocols, not the community. Having a security review hosted on-chain suggests, “You can trust this code because there is a security review here.”

However, the security review was paid for, scoped by, and conducted by the protocol. It’s meant for the protocol. In the context of feedback for the protocol.

At the same time, if a project wanted to show off its audits for people to learn and grow from, that seems fine. But I’m just nervous that this is a standard for projects to say “Look, we are safe. You can see our on-chain security review” when the security review wasn’t done with the community in mind.

My main question is, “Why would we even care to have this standard?”

---

**lukasschor** (2023-09-15):

Not sure security reviews are in practice used „for the protocol“. Pretty much every landing page features security reviews as a signal to the community that there has been some measures being taken and that there is a baseline of security focus in the project. Yet the connection of these PDFs on a landing page and the actual smart contract code is very loose. So this ERC is at least an incremental improvement by bringing security reviews closer to the actual code they were covering.

Ideally it‘s also going to be the basis of much more significant improvements such as reputation systems being built on top of this standard or new incentive mechanisms where it‘s actually not the protocol team scoping and paying for the security review.

---

**chendatony31** (2023-09-19):

I have discussed this issue with some security companies before, and the solution is similar to [@Dexaran](/u/dexaran)’s. Security companies can issue audit SBT to their audited contracts. which means that each security company or person has their own corresponding SBT contract. We can verify whether the contract belongs to this company by using the url metadata of the contract and the /.well-know/contract.json file of the official company domain name

As a wallet (or an explorer), you can enumerate these contracts to display which people/companies have audited the contracts that your user is interacting with and whether they are relatively secure.

---

**thezluf** (2023-09-20):

As [@rmeissner](/u/rmeissner) mentioned, this ERC focuses on standardizing what auditors should sign, rather than defining the registry. The goal is to ensure consistent verification across the ecosystem.

---

**blackbigswan** (2023-09-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/patrickalphac/48/7343_2.png) PatrickAlphaC:

> I’ve thought a decent bit about this, and every time, I conclude: “What would this accomplish?”

I totally get where you’re coming from as I share same sentiment. That said, there’s a solid reason to standardize the data format for posting audits on-chain, and it aligns with the SEC’s recent thinking. While the SEC is primarily concerned with reliable financial information, you could argue that audits indirectly fall under this umbrella. Take a look at this document:

[![F5bvlrbWgAEVC0m](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1a6cd1ed040c45b28387177514addf8b8ba51c5c_2_350x500.jpeg)F5bvlrbWgAEVC0m630×900 169 KB](https://ethereum-magicians.org/uploads/default/1a6cd1ed040c45b28387177514addf8b8ba51c5c)

Notice: *[…] in practice the source code implemented on blockchains are in machine-readable format, may not conform to public descriptions of the code*

So, creating a standardized, public, and immutable registry for audits of a given protocol makes sense. But a standard is only as good as the infrastructure built around it (gh2source2bytecode compare, documentation2implementation compare, does audit audit actual bytecode or github etc.). That’s mostly going to be off-chain though. Personally I call it “GenslerProtocol”. So yeah, this EIP does have value, especially since there’s at least one clear use case that would benefit from a robust data format.

---

**lefuncq** (2023-09-20):

Many people suggest going with a registry instead of the current proposed implementation. That’s precisely what we’ve been working on for the past couple of years at [Trustblock](https://trustblock.run).

Compared to what we’ve built, the current proposal has its strengths and weaknesses.

The main problems I see so far:

- Expect protocols to add this to their codebase, which is far from trivial
- Synchronicity? Auditors have to submit audits upon each request, which is very limiting in terms of usage
- Handling upgrades
- Findings are missing but still valuable information for protocols to act upon.

---

**rmeissner** (2023-09-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lefuncq/48/10530_2.png) lefuncq:

> Expect protocols to add this to their codebase, which is far from trivial

I would be interested how this problem is differently handled by the 2 approaches.

The current ERC proposes a way that could be used in any registry and without any onchain interaction necessary.

The challenge we see with registries is that it is still a very centralized approach (which has its benefits). Therefore the ERC aims to create a building block to make audit information available and verifiable onchain, not to build such registries itself.

> Synchronicity? Auditors have to submit audits upon each request, which is very limiting in terms of usage

Overhead wise the ERC aims to keep it minimal. Many auditors are already signing their audits as part of the process and the additional overhead to create and sign the onchain representation should be quite low (would be interesting where you see this becoming a blocker).

When it comes to publishing the representation and pushing it onchain, then this can be done by anyone. Auditors could upload this side-by-side with their audit files (similar how checksums are published) and anyone could make use of these. This way the overhead to interact with any 3rd party is not required.

---

**Angler** (2023-09-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lefuncq/48/10530_2.png) lefuncq:

> Many people suggest going with a registry instead of the current proposed implementation.

The benefit of the representation over a registry IMO is that we can have many different registries that utilize the audit representation. This has multiple benefits.

1. No single entity is in control over the audit representations
2. The user can select from different registries one that matches his needs. E.g. the user might select a registry for smart contracts that are audited only by specific auditors.
3. The registry can combine the representation with other criteria

---

**thebensams** (2023-09-20):

How does this work for upgradable contracts?

---

**lefuncq** (2023-09-20):

> I would be interested how this problem is differently handled by the 2 approaches.

In our case, we have one registry per chain, and these registries contain auditors’ wallet addresses that are allowed to publish audits. We whitelist wallets for now, but the best would be to have governance voting auditors on and off.

> Therefore the ERC aims to create a building block to make audit information available and verifiable onchain, not to build such registries itself

I agree with you it’s clearly out of scope for this EIP, but I think it’d still be interesting to actually work together on an audit registry ERC that we could also integrate on Trustblock. The main reason for a registry is that it will create many more use cases for audits on-chain, according to our research through these couple of years, than if the verification has to be made synchronously with the auditor. With the data being directly accessible, protocols can be used for various composability purposes. Moreover, storing on-chain also guarantees the immutability of audits.

> The challenge we see with registries is that it is still a very centralized approach (which has its benefits).

Audits are delivered by a single entity, so they will always be centralized by nature, right? However, if you meant that registries would be controlled by a single entity (like us for example), then I think it depends on the registry functioning, for example in our case only auditors can publish audits so we don’t control the data.

Overall

1. Per my knowledge and seeing how many auditors work, I have not seen many auditors sign their audits (not sure exactly what you meant there) nor keep track of contract addresses they have audited. So, if they want to support this, they must change how they do their business. I believe specifying exactly which contract addresses audited is the right thing, but that isn’t the reality right now

If they want to upload old reports, they must find the exact addresses they audited. When they do new ones, they have to ask for deployed contract addresses after an audit, verify them, and add them to the report
2. Preparing audit representation and signing. Depending on the tooling used, it can be automated or simplified. Still, it is an additional step
3. Display their wallet addresses or public keys so that others can verify audits
So they should have the right incentive behind it. I know it is not exactly the scope of this EIP, but that’s the practical aspect of it.
4. If protocols want to support this and accept only, let’s say, tokens with audits into their system, they have to:

Pre-select auditors they trust. It means that they have to get their wallet addresses/public keys to verify the signature belongs to the auditor they trust
5. Implement verifier either on-chain or off-chain

---

**lefuncq** (2023-09-20):

I agree with you. The way you would implement registries is very interesting and different from the way we implemented them in our system so far.

In our case, we have one registry per chain, and protocols can preselect which authorized auditors they want to get audits’ data from.

Another significant advantage in favor of registries is that if the audits were to be stored on-chain, we could make them immutable, which is super helpful to balance trust relations further between users, auditors & protocols.

---

**srw** (2023-09-20):

We just published our opinion at [ERC-7512: A Solution to the Centralization of Security Audits Data?](https://www.coinfabrik.com/blog/erc7512-security-audit-centralization/).

The TLDR is that solves the issue with sites such as CoinMarketCap, Etherscan, CoinGecko, etc because they don’t publish accurate data about auditors even when you follow all their forms. Hence, they are a point of centralization that filters real information. On the other hand, we think that this problem should not be limited to audits and a way to add metadata in general could be interesting.

---

**Dexaran** (2023-09-21):

The main problem with this ERC is that it only allows for “positive” audits that say the contract is secure.

I own a security auditing company (https://audits.callisto.network/), I’m an auditor myself and in many cases it is really important to say “Warning! This contract is not secure” while others are saying it is secure.

It is not secure to pretend “if at least one company said that the contract is secure = we label it as secure” .

Also audit records must not be immutable by any means. Imagine a contract was audited, then a vulnerability is discovered but there is already a signed audit report that states that the contract is fine. Anything can happen or be discovered AFTER the audit report so this needs to be accounted.

---

**JakubLipinski** (2023-09-22):

Just for the sake of reference: I tried (and failed) to create an on-chain registry of smart contract audits in 2008 as a part of SolidStamp service. Some of my learnings and ideas are still available at:

https://medium.com/@SolidStamp/solidstamp-putting-skin-in-the-blockchain-game-6c061cd33c6

https://medium.com/@SolidStamp/solidstamp-a-flight-recorder-for-the-ethereum-ecosystem-7a6247947733

Good luck this time.

---

**Hans** (2023-09-23):

After all, the proposal seems to be to see if a protocol was audited.

We can achieve that more simply, in fact:

- Auditors (personal or firm, whatever) create NFT to represent the audit information. Additional information like the issued date and a report link can be included in ERC721Metadata.
- Maintain an address registry of auditors on-chain.

What else do we need?

---

**rmeissner** (2023-09-23):

You need an agreement of the auditors on this metadata and how to issue that nft.

What you described is not the purpose of the nft the purpose is to create a basis that allows you to create such nfts. I.e. could you say that you have a nft contract where you can submit an erc-7512 object which will mint the nft with some basic information (like auditor). This then can be used in different protocol to perform security check (or other logic based on the audits).

---

**rube-de** (2023-09-25):

Shouldn’t this support also erc-1271? As audit company it would make sense to have a smart account, instead of an EOA.


*(8 more replies not shown)*
