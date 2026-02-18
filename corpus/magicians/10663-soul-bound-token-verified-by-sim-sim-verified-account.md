---
source: magicians
topic_id: 10663
title: Soul Bound Token verified by SIM -- SIM Verified Account
author: Kapu
date: "2022-09-04"
category: EIPs
tags: [web3]
url: https://ethereum-magicians.org/t/soul-bound-token-verified-by-sim-sim-verified-account/10663
views: 857
likes: 16
posts_count: 5
---

# Soul Bound Token verified by SIM -- SIM Verified Account

Web3 dapps have been flourishing with developers and starups, however, when user authentication is involved it has to fall back to web2. I would like to propose a web3 native authentication system based on SBT (Soul Bound Token) verified by the SIM and Ethereum network. The mobile cellular networks (2G+3G+4G+5G) built by the Mobile Network Operators (MNOs) actually serve much larger population than the internet, including those who use dumb phones or feature phones.

The SIM can be designed as the secure element for wallet, a low cost and universal hardware wallet, provided with an applet (an application running over the operating system of the SIM) for producing the digital fingerprint by hash functions over the IMSI (International Mobile Identity Subscriber Identity, an unique identity of the mobile phone user). User privacy is assured since the hash function is performed based on confidential computing withing the hardware boundary of the SIM hardware chip.

IMSI includes 3 parts:

MCC: Mobile Country Code

MNC: Mobile Network Code

MSIN: The serial number assigned by the network operator

MCC for respective countries and MNC for licensed network operators within the countries are public information and can be included as parameters for verifying a valid SIM user in the contract to facilitate the autonomous attestation.

The fingerprint can be categorized by MCC and MNC and verified by the smart contracts for its validity. When a fingerprint is validated by the contract for the first time, a SBT called SIM Verified Account (SVA) will be available for airdrop to the associated wallet address of the SIM.

For smart phones, the fingerprint is transmitted to the blockchain gateway through BIP protocol (a mobile specification supported by most of the smart phones for end to end communication between the SIM and websites), which interact with the smart contract. BIP can only be triggered by the SIM when the SIM is authorized by the MNO who issue the SIM. When the fingerprint is further verified by the Ethereum contract with it’s uniqueness, SVA will be available for the wallet address. The BIP connectivity ensures the SIM is active as authenticated by the MNO.

For feature phones, the fingerprint is transmitted through SMS to the blockchain gateway, which connect to the contract. The drawback is that the phone number is disclosed to the blockchain gateway. With major use cases for features phones like mobile money in African countries where mobile money are driven by mobile numbers as identity, the privacy issue can be mitigated by offchain solutions which are commonly accepted and regulated.

With matured standardization of the global mobile cellular network as well as the massively distributed SIMs in place, they become an autonomous attestation platform for SVA to bootstrap the native web3 ecosystem. The assumption is the trust to the existing licensed MNOs who issue the SIM with proper KYC in place, for which most of the countries have implemented properly. For countries where KYC may not be facilitated, the SBT can be issued with moderated credit scores.

Feedback, discussions, and comments are welcome.

## Replies

**kdenhartog** (2022-09-04):

Hey, I like the thinking that you’re heading towards here by looking to build on another established and mature network to achieve sybil resistance for SBTs. While there’s benefits to building on top of the phone networks, there’s some legitimate drawbacks that need to be considered here.

1. These networks are not flawless in terms of identity checks and can be subverted quite easily for sybil attacks. For example, prepaid SIMs are a common way to achieve this, even in countries where strong identity checks are required for receiving a SIM, because many network providers don’t set a limitation on the number of SIM cards that can be purchased per person. This means that you’ve introduced an economic limiting sybil attack. As a shot in the dark (no evidence to back this up right now) I’d venture to guess that SIM card based identity fraud sits around 5 - 20% levels depending on the economic value that is gated by it. Is that an acceptable level of fraud for SBTs?
2. Attaching on chain accounts, which are global identifiers, are hardly ever used as Pairwise pseudonymous identifiers. This means that we’re creating a way for the majority of users to have their on chain assets correlated to their real life identity. This is a privacy nightmare waiting to happen, so privacy really needs to be considered here as priority.
3. By setting a barrier of entry being that people need to have a phone number we also introduce a set of shaky foundation problems. Things to consider are: What happens if someone is unable to afford a a phone or phone number? What happens when a phone number is changed? What about if it’s lost or stolen via a SIM swap attack?

If we want to achieve Sybil resistance (I agree with this goal), I don’t believe that building on phone networks is the right way to do this long term. It may be useful in the short term, but we’re going to inevitably limit the value that can be associated with an identity because of the fraud levels. It’s too easy to subvert these checks today. Instead, I’d suggest looking at using [mDLs](https://www.mdlconnection.com/mobile-drivers-license-faq/) which have the advantage of being government issued which expands access and also reduces (but does not eliminate) the ability to receive many mDLs to conduct a sybil attack.

However, for point 2 I don’t have much to offer at this point. There’s probably ways that you could limit this with some sort of anonymous credential scheme and some off-chain checks, but that likely creates centralization points which is a big issue with identity systems.

Finally, here’s a last question to guide this discussion a bit: How much fraud do we consider is acceptable for an initial implementation that would allow SBTs to become a useful primitive in the ecosystem?

---

**Kapu** (2022-09-06):

Thank you Kyle for the questions so that I can elaborate more about my idea.

The SIM that is residing in your mobile phone is actually a crypto processor that can play all the magics to resolve your concerns. The SIM is a smart card which is not only capable to authenticate with the network for telecom services, but also providing more memory space and creation of security domains for building up applications such as:

1. Native construct for a wallet:
In this case users can create their own wallets (an universal, low cost hardware wallet and convenience for accessibility within the mobile devices) natively, without dependencies on any 3rd party software/hardware platforms.
2. Native construct for a web3 ID:
By associating the universal identifier programmed in the SIM like IMSI (SUCI/SUPI for 5G) with hash functions based on confidential computing secured by the hardware boundary, the SIM can produce the unique fingerprint to construct an universal Identity without compromising user privacy. The universal identity may be used to bootstrap a global SSI system, for SSI issuers to issuer Verifiable Credentials to the SIM holder. In this topic we are discussing about creating an autonomous attestation by the mobile network and smart contracts on the chain, in order to verify the fingerprint identity for granting a soul bound token called “SIM Verified Account” by checking the liveness and uniqueness of the SIM. In essence we want to replace the function like SMS OTP authentication in web2, which is subject to privacy/centralization issue due to phone number data disclosure/aggregation and SIM swap issues.

To answer Kyle’s questions:

1. Acceptable fraud for SBTs?
Assuming you’re right about the 5-20% of none KYC SIMs or KYC SIMs that are being used purposely for Sybil attack, I would consider this could be acceptable number, if we were to give a “Universal Basic Reputation” by granting a SIM Verified SBT to the wallet, which can be further enriched by other SBTs for its reputation. With the IMSI fingerprint, the country code is available to downgrade the score of the token for countries where KYC is not enforced. In this case we have significantly remove the cost for Anarchy in the first place. Furthermore, I guess this number is being moderated in more and more countries for facilitating KYC of SIM issuance with stronger policy enforcement, and the numbers of SIM one person can purchase are limited. And of course the economic barrier for limiting Sybil attack is a bonus point to this idea.

Actually, if a SIM is issued with additional functions like mobile money, KYC is definitely taken care seriously by relevant regulations, such as M-Pesa SIM in Africa which serve more than 40 million people. For a SIM that may support the blockchain to drive similar services, offline KYC is likely to be facilitate by the SIM issuers.

1. Privacy issue?
IMSI (International Mobile Subscriber Identity) is implicitly coded inside the SIM chip. Our idea is to leverage the SIM chip capability for producing the fingerprint by hash functions based on the IMSI. Similar to what has been defined in 5G standard for IMSI encryption for producing the SUCI that is transmitted to the radio network, the MSIN is used to produce the fingerprint for chain verification. Therefore, no privacy information is revealed outside the SIM chip. And all these process does not involve the phone number, which is the one paired to the real world identity.
2. Shaky foundation?

- Affordability?
For this point I share different view with you. The mobile network is the major distribution for internet in recent years. It reaches out even to the villages in African countries. In developed countries the SIM ownership is even higher than their populations. My concern over affordability is about those who can not afford a smart phone or the fee for data connectivity. There are nearly 2 billion people who stay unconnected with internet, but they do have a phone with SIM for calling and SMS. For most of those people, quick money transfer is viable to prevent them from hunger and danger, especially when there is a disaster. A SIM based blockchain inclusion is significant to those population. In the centralized web2 internet we failed but for blockchain driven web3 we should consider all necessary efforts to onboard those people.
- What happens when a phone number is changed?
When you change your phone number, you receive a new SIM. Like all the wallet, you simply import the Backup Phrase for wallet recovery with the new SIM, then you get back everything in your wallet.
- SIM swap?
SIM swap is not an issue in this design, because the wallet is not bound to the phone numbers but the SIM. If someone managed to swap your SIM, your wallet would not be transferred to the other SIM. You would see your phone lose signal but your wallet would be still safe.

This topic actually implies a proposal for the convergence in between the internet with the mobile network. In web2, the mobile operators has gone through a tough time since the arise of OTTs (Over The Top) internet service providers who took free ride and grow over the mobile internet built by mobile operators. Centralized ISPs took everything for granted and turn the whole internet to an advertising ecosystem. They even took the phone number for granted to authenticate their user with SMS OTP. When there is a SIM swap attack and lost of property, the victims sued the mobile operators for compensations…

In web3, we are looking forward to a brand new ecosystem, where blockchain shall embrace the mobile network, who provided the infrastructure for Sybil resistance, legal compliance and huge user base. I do believe the mobile industry player are also eagerly to participate in building the new web3 internet.

Starting with the SIM Verified Account SBT, for connecting the mobile infrastructure, there are quite a few items that we need to discuss including:

- SIM channels for communication between the SIM and chain including SMS/BIP/smart phone api…
- SIM fingerprints as an meta-identity for Ethereum network including production/transmissions/management…
- An industrial auditing system such as EMV for banking smart card and SAS for SIM card supply chain management to ensure the universal certification of hardware wallet

Any feedback and comments are welcome.

---

**Kapu** (2022-09-07):

Regarding [mDL](https://www.mdlconnection.com/mobile-drivers-license-faq/), a government issued identity or eID or mID, there are issues for implementation:

1. Global Interoperability：
There is no global Interoperability system in place for authenticating those IDs if you’re in different countries. For SIM card, the IMSI range is managed by GSMA so that you can do roaming even you’re in foreign countries.
2. For authenticating a ID like mDL(mobile Driver License), there is no standard technical interface to facilitate an autonomous attestation. Human check or system integration for each of the countries will involve centralization issues and tremendous workload to make it a global resource for  building up the web3 identity system.

---

**Evonne** (2022-09-09):

Hi, we are proposing the SIM channel between smart phone APPs and the SIM to make your idea happen. We are trying a new EIP to specify how we make it.

