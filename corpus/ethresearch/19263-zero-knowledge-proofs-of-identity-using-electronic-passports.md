---
source: ethresearch
topic_id: 19263
title: Zero-knowledge proofs of identity using electronic passports
author: turboblitz
date: "2024-04-09"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/zero-knowledge-proofs-of-identity-using-electronic-passports/19263
views: 8244
likes: 74
posts_count: 24
---

# Zero-knowledge proofs of identity using electronic passports

# Zero-knowledge proofs of identity using electronic passports

[![282155110-514ae671-3c02-434f-ac6a-31ce20eec24d](https://ethresear.ch/uploads/default/optimized/2X/a/ae85fbbbb938d295752b4f8fcb38f3fcab695885_2_690x154.jpeg)282155110-514ae671-3c02-434f-ac6a-31ce20eec24d1792×401 181 KB](https://ethresear.ch/uploads/default/ae85fbbbb938d295752b4f8fcb38f3fcab695885)

Many applications need to verify their user’s identity online, whether it is nationality, age, or simply uniqueness. Today, this is hard. They are stuck between shady heuristics like tracking IP addresses and technologies like Worldcoin that need to deploy their infrastructure widely.

Fortunately, UN countries in association with the International Civil Aviation Organization have built a great tool for us to piggyback on: electronic passports. They are issued by more than 172 countries and include an NFC chip with a signature of the person’s information, including name, date of birth, nationality and gender. Issuing countries make their public keys accessible in online registries, enabling the verification of signatures.

## A circuit for passport verification

For someone to prove their identity using a passport, they will have to do two things. First, read the content of their passport’s chip. This can be done easily with any NFC-enabled phone. Then, show a verifier that their passport has been correctly signed. Instead of sending all of their personal data for the verification to happen, they can generate a zero-knowledge proof that redacts some of their inputs.

Our circuit will have to checks two things:

- The disclosed attributes have been signed correctly
- The corresponding public key is part of the public key registry of UN countries

A simple circuit compliant with the electronic passport specs would look something like this:

  [![image](https://ethresear.ch/uploads/default/optimized/2X/e/e55186294a00f20a4e0fd0cdc8da1172a89d3e3e_2_500x336.png)B1_4A2ZxC.png2483×1669 96.6 KB](https://ethresear.ch/uploads/default/e55186294a00f20a4e0fd0cdc8da1172a89d3e3e)

Here is roughly what happens:

- Each datagroup stored in the passport contains some of the person’s information. The datagroups we are most interested in are the first one (nationality, age, etc) and the second one (photo). The circuit takes them as inputs along with the signing public key.
- Datagroups are hashed, concatenated and hashed again.
- The final result is formatted, hashed and signed by the country authority. We can use the public key to check this signature.

This makes the following attributes disclosable: name, passport number, nationality, issuing state, date of birth, gender, expiry date, photo.

Some countries also provide additional data like place of birth, address, phone number, profession and a person to notify. Biometrics like fingerprint and iris are sometimes included but can’t be retrieved, as they require a special access key.

In practice, we want our circuit to have a few other features:

- Instead of passing the country’s public key directly, we want the user to prove that the public key that signed their passport is part of the registry published by the ICAO. This can be done by passing a merkle proof of inclusion and having only the merkle root as a public input.
- To allow for selective disclosure of any attribute, we pass a bitmap as a public input that will redact some of the attributes.
- We want specific modules for age disclosure and nationality list inclusion. A range check can guarantee someone is above a certain age without disclosing the precise age, and an inclusion check can be done over a set of countries to prove someone is or is not a citizen of any country in a list.
- For applications like minting an SBT or voting, we want to check that the passport is not expired. This can be done by passing the current date and doing a range check over the date in the circuit. We can then check that the current date is correct using the block timestamp in a smart contract or server-side in offchain verification.
- For applications that need sybil-resistance, we want to store a nullifier that prevents using the same passport twice. The simplest approach involves storing a hash of the government’s signature, though this does not render the individual anonymous from the government’s perspective. There are other approaches, see here for a discussion of the tradeoffs.

A map of a more complete circuit can be found [here](https://hackmd.io/_uploads/rk9_ZaZeC.png).

One of the challenges is the [number of signature algorithms used](https://hackmd.io/@TCEn_IDhTDWLjwyItiiBcQ/BJ4LX0m9p). Most countries use common ones like RSA with SHA256, but the ICAO specifications are quite permissive and some countries chose to use hash functions like SHA512 or unusual padding formats. We currently support the most common one and we are working on [adding support for more](https://github.com/zk-passport/proof-of-passport/issues/38).

## Applications

Applications roughly fall into three categories: proof of humanity, selective disclosure and authentication.

Proof of humanity can be used in general for sybil resistance. This includes voting, fair airdrops, quadratic funding and helping social media fight bots. If passports can’t be construed as a general solution today, they can be integrated into wider systems like Gitcoin Passport or Zupass.

Selective disclosure has applications like privacy preserving age check. Some countries restrict buying alcohol, drugs or entering casinos for minors, and zk could help bringing better privacy to those controls.

Another example of selective disclosure is proving one is not a citizen of any country in a set of forbidden countries. This could help creating an intermediate level of compliance between KYC-gated traditional finance and fully permissionless DeFi.

Using passport signatures for authentication, one can build a ERC-4337 recovery module that asks for a proof from a specific passport as one of the conditions for recovery. Some passports also support Active Authentication, meaning they have their own private key and the ability to sign data. This would make them suitable for direct transaction signing, either for small transactions or in a multisig setup with other signers.

## Limitations

The most obvious limitations of using passport signatures are the following:

- The passport does not do any kind of biometric check when the chip is read. Therefore there is no straightforward way to know if the passport has not been borrowed or stolen.
- Most of the world population does not have a passport. Even in the US, only around 50% of the population owns a passport.
- Issuing authorities can create an arbitrary number of passports and cheat in systems that require passports for sybil resistance.
- Passports can be lost or revoked. Some countries allow citizen to keep their previous passport when they are issued a new one. Some people have dual citizenship. All those cases are hard to mitigate, as the signatures stay valid.

Those limitations are all quite fundamental to the way passports work today. They can be addressed by aggregating attestations from multiple sources, which will be covered in a future post.

## Current state

Proof of Passport is [fully open source](https://github.com/zk-passport/proof-of-passport), from mobile app to circuits. If you are interested in contributing, please check [open issues](https://github.com/zk-passport/proof-of-passport/issues).

While performance would have been a bottleneck a few years ago, work from teams like Polygon ID, arkworks and mopro have made client-side proving on smartphones quite fast. Generating a proof with the current circuit takes ~4 seconds on a recent iPhone.

We are currently focused on shipping the mobile app for the first integrations. It allows users to mint an Soulbound Token disclosing [only specific attributes they chose](https://testnets.opensea.io/fr/assets/goerli/0x64bfeff18335e3cac8cf8f8e37ac921371d9c5aa/0), or none at all other than the validity of their passport. [Contact us](https://t.me/FlorentTavernier) to try out the beta release.

Thanks to [Rémi](https://github.com/remicolin), [Andy](https://twitter.com/AndyGuzmanEth), [Aayush](https://twitter.com/yush_g), [Youssef](https://github.com/yssf-io) and [Vivek](https://twitter.com/viv_boop) for contributing ideas and helping build this technology!

## Replies

**parseb** (2024-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/andreevpetr/48/15970_2.png) AndreevPetr:

> It’s challenging to conceive of any request regarding nationality and gender that wouldn’t be discriminatory. Can you?

Are positive measures “to promote diversity and assist minority nations” discriminatory?

Every *body* has membership conditions. Knowing exactly what those are leads to more just outcomes.

Belonging criteria is not discriminatory, but mere preconditions for the existence of organizations.

---

**wooju** (2024-04-11):

Passports must be stored privately, yet there should be a way to publicly verify their validity. How and where passport information is stored?

---

**turboblitz** (2024-04-11):

Good question.

The passport data that is read from the NFC chip is very sensitive information, so I don’t think we want to keep a copy of it in a mobile app. Instead, we can generate a proof of just the information we want, like humanity or nationality and store only this proof. It can still be verified afterwards using the government’s public keys that are accessible online.

---

**AndreevPetr** (2024-04-11):

No, positive measures themselves are not inherently discriminatory. In theory, organizations could apply these measures constructively to foster inclusivity. However, it’s often observed that the nationality listed in passports is used for discriminatory purposes. Ultimately, it’s within an organization’s discretion to either perpetuate discrimination through various classifications and categories, or to uphold the fundamental principles outlined in the Declaration of the United Nations. Article 7 of the Declaration explicitly states that everyone is equal before the law and entitled to equal protection without any discrimination. This includes protection against any discrimination that violates the Declaration and against any incitement to such discrimination. It would be commendable if mechanisms like Ethereum could be utilized to offer anti-discrimination bonuses to minorities, which would be a significant step forward. However, in my opinion, it’s generally better to avoid at all using nationality information in passports

---

**parseb** (2024-04-12):

Understood. Using the tool likely to come with its values.

The source of worry here being the inherent discriminatory character of national identity. At application level this boils down to KYC and respecting the rules and regulations of the jurisdiction in which you operate. Law, be it international, is historically powerless in its affirmative sense. Appeals to law, since states and not individuals are producers of it, is more efficient at upholding discriminatory practice than not.

This is an application. Ethereum is, like the internet, permissionless and credibly-neutral.

---

**aguzmant103** (2024-05-03):

[@AndreevPetr](/u/andreevpetr) tech can be used for good or evil, i don’t think “ignoring” nationality/gender is the way to go

Returning privacy for people to selectively disclose PII is very important

Some positive example use cases:

- Targeted UBI for at-war countries or high levels of poverty (claimable anonymously if you can prove X)
- Private refugee applications
- Anon national forums where civil discussions are taken to improve local or national government

---

**Mirror** (2024-05-04):

This raises another question: why check people’s passports at all? I think a better idea would be to use ZK technology to encrypt citizens’ passport chips, which would be verified when they pass through customs. Passports, including their chips, are easily forged.

---

**Pfed-prog** (2024-05-07):

Please stop the overly zealous moderators banning absolutely everything. We are not in Canada.

For my credentials, skills certification:

I have made a 30 minute presentation on zkPassport and SoulBound NFTs at EthBucharest 2024.

Here are the slides: [EthBucharest 2024 - Google Präsentationen](https://docs.google.com/presentation/d/1OmJJgzk4iFbKexqBw87oU7oh4H9lXlFFh3eas0EF9y8/edit?usp=sharing)

Here is an opinion by inverid, most popular mobile app to read Passports.

> In practice, only a very few organisations such as national border control, police and local governments receive authorization to read the fingerprints from a passport. Especially in an international context, it is very difficult to arrange. Because of this, EAC-TA seems to be used very little. We have already implemented EAC-TA some years ago, and ReadID can support EAC-TA for customers that have received such authorization. This is however currently not a production feature.


      ![](https://ethresear.ch/uploads/default/original/3X/e/d/ed190199422f55682d364bef50537a97a9ea60b3.png)

      [Signicat](https://www.signicat.com/blog/privacy-related-security-mechanisms-for-epassports)



    ![](https://ethresear.ch/uploads/default/optimized/3X/a/7/a730652f6c8abbf995a14b68a9dd6cf52f188a0d_2_690x362.jpeg)

###



In this blog, we zoom in on the security measures used to protect the privacy of the document holder of ePassports and other similar electronic identity…










Here is my slide page 11 from the presentation

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/9/b981371e2f395ccba16d204763037fe635f101f8_2_690x370.jpeg)image1920×1030 134 KB](https://ethresear.ch/uploads/default/b981371e2f395ccba16d204763037fe635f101f8)

---

**Pfed-prog** (2024-05-22):

Further attaching relevant resources on the context perceived discrimination that stem from passports

# The Effects of Perceived Discrimination on Immigrant and Refugee Physical and Mental Health


      ![](https://ethresear.ch/uploads/default/original/3X/3/6/366309b72090843accd886395b8c67de88c17a0c.png)

      [PubMed Central (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6553658/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/1/c/1c2b2fab27273d4bb02dc0a9b2efa3389fa20ffe_2_690x360.jpeg)

###



Discrimination has been identified as a major stressor and influence on immigrant health. This study examined the role of perceived discrimination in relation to other factors, in particular, acculturation, in physical and mental health of ...










# Transgender and Nonbinary People Describe Discrimination, Harassment, and Mistreatment at Aurora Detention Facility in New Civil Rights Complaint

https://www.americanimmigrationcouncil.org/news/transgender-nonbinary-people-abuse-ice-aurora-colorado-detention

# Enforcement at the Airport


      ![](https://ethresear.ch/uploads/default/original/3X/1/8/183cb2dc72fb159c8445b73d742c48dba8c11145.png)

      [American Civil Liberties Union](https://www.aclu.org/know-your-rights/what-do-when-encountering-law-enforcement-airports-and-other-ports-entry-us#what-types-of-law-enforcement-officers-could-i-encounter-when-entering-or-leaving-the-united-states)



    ![](https://ethresear.ch/uploads/default/optimized/3X/5/d/5d62329f7199a5cec993214b4fb844d6db9cb758_2_690x362.png)

###



At the border, you are likely to encounter Customs and Border Protection (CBP) officers, and you may encounter Homeland Security Investigations (HSI) agents. HSI is part of U.S. Immigration and Customs Enforcement (ICE). Know your rights in these...

---

**turboblitz** (2024-05-23):

EAC-TA, which is Terminal authentication, is only meant to be done at airports and requires special access keys. Definitely not something we can or want to do!

---

**0xvon** (2024-07-10):

Thanks for the nice post!

My lab studies Digital Identity and I have studied the signature algorithm used for Verifiable Credential, so I thought this was a very interesting post.

If you don’t mind, can you elaborate on how Selective Disclosure works?

> To allow for selective disclosure of any attribute, we pass a bitmap as a public input that will redact some of the attributes.

Bitmap and circuit diagram are not well connected in my mind. The reason for incorporating that mechanism is to be able to change public input and private input without changing the circuit, right? Can you explain how the flow is different when disclosing only the name and when disclosing only the date of birth?

---

**turboblitz** (2024-07-13):

Hi,

Yes, precisely. By passing a bitmap that selects characters of the MRZ to be revealed, we can have a single circuit for any combination of disclosures, and let users choose what to reveal each time they generate a proof. You can see the code [here](https://github.com/zk-passport/proof-of-passport/blob/0c3d115553d28d3dd1ef4d63d640d775a8e5abbc/circuits/circuits/disclose.circom#L63-L71).

---

**AndreevPetr** (2024-07-29):

Where can I find a list of oracles for ZK passports? Which industries already have them? Is there a complete list available?

---

**turboblitz** (2024-07-29):

If by oracles you mean the public keys of issuing authorities, there are multiple lists, the main one being compiled by the [ICAO](https://download.pkd.icao.int/). [Here is how we parse it](https://github.com/zk-passport/proof-of-passport/tree/main/registry).

---

**EugeRe** (2024-08-02):

Hey [@turboblitz](/u/turboblitz) this is a great use! Have you seen my work on standardizing on chain executions using zk-ID I believe there could be an angle there

[Enabling standardized on chain executions through modular smart accounts](https://ethresear.ch/t/enabling-standardized-on-chain-executions-through-modular-accounts/20127)

---

**huihzhao** (2024-10-13):

ah, this is an interesting use case.

---

**huihzhao** (2024-10-20):

How can applications verify on chain? for example, a DeFi app needs to verify if the user is over 18 years old, after the proof is generated, it must be submitted on chain so that the DeFi app can verify?

---

**voronor** (2024-10-21):

To enable on-chain verification for applications like DeFi, after generating a zero-knowledge proof (ZKP) from an electronic passport verifying that a user is over 18, the proof must be submitted on-chain. The DeFi app can then verify the proof using the blockchain, which acts as a trustless intermediary. This approach ensures that sensitive user data, such as birth date, is kept private, while the app can confirm the age eligibility based on the verified proof.

These are my guesses.

---

**Therecanbeonlyone** (2024-10-21):

The architecture is relatively straightforward and also needs to take into account abstraction.

[Here is a write-up](https://ethresear.ch/t/resolving-the-dichotomy-defi-compliance-under-zero-knowledge/20413) and questions with link to a published whitepaper. There is an ongoing effort on this, if anyone from the DeFi protocols or L2s is interested in contributing, please DM me.

---

**Therecanbeonlyone** (2024-10-21):

[@turboblitz](/u/turboblitz) using the international passport schema is one step. There also needs to be a root of trust that does the passport reading and digital translation. That is a second credential that establishes the legal identity of the passport data reader and attester. So one is not enough.

Generally speaking, to simplify the circuits, one should also use W3C Verifiable Credentials (at a minimum, ideally with W3C DIDs). [Here is a recent write-up](https://ethresear.ch/t/self-sovereign-identity-and-account-abstraction-for-privacy-preserving-cross-chain-user-operations-across-roll-ups/19599/14) on the topic as well as a [link to the whitepaper](https://entethalliance.org/w3cs-did-and-vc-technology-can-help-with-ethereums-three-transitions/) on the topic of identity and standards and key management across chains from the Ethereum Open Community Projects L2 Standards WG.


*(3 more replies not shown)*
