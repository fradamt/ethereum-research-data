---
source: ethresearch
topic_id: 20657
title: What happened to our decentralized private new internet?
author: pememoni
date: "2024-10-15"
category: Privacy
tags: [mev]
url: https://ethresear.ch/t/what-happened-to-our-decentralized-private-new-internet/20657
views: 1219
likes: 30
posts_count: 10
---

# What happened to our decentralized private new internet?

**The Selective Disclosure/Compliance Challenge in Web3**

*By [Peyman Momeni](https://x.com/Pememoni), [Fairblock](https://www.fairblock.network/); [Amit Chaudhary](https://x.com/amitchax), [Labyrinth](https://x.com/Labyrinth_HQ); [Muhammad Yusuf](https://x.com/yusufxzy), [Delphi Digital](https://t.co/rJirnhBM5S)

**Why?**

Today, after 16 years, blockchains’ utility is mostly limited to meme coins and circular infrastructure projects. Yes it’s fun, yes a lot of people made millions, but are we still building the new internet? What happened to the idea of our decentralized private new internet?

The most obvious application – transfers– hasn’t yet been fully realised even for basic scenarios. Most businesses can’t use it. They can’t share their payroll with everyone. Vitalik is getting bullied for his onchain donations to science. Businesses don’t want to share their confidential strategies and data publicly, users don’t like the choice between a centralized service or getting sandwiched maximally and begging for a change from middlemen mercenaries.

While the machine is running, we, as a collective, cannot continue this path for another 16 years.

With privacy should come confidentiality to secure your onchain actions, allowing for more useful and impactful applications to be built and for users to reap the benefits of a more expressive blockchain experience. Confidentiality is a standard across Web2, it’s imperative that it become a standard across Web3.

[![](https://ethresear.ch/uploads/default/optimized/3X/5/7/5753c19290978d1767b2eb6b63aa71fc785ce47b_2_439x158.png)1078×386 50.8 KB](https://ethresear.ch/uploads/default/5753c19290978d1767b2eb6b63aa71fc785ce47b)[![](https://ethresear.ch/uploads/default/optimized/3X/6/8/68b00f87394db8a4f28ce7bb18d6c0a8c7797d2f_2_438x200.png)1176×536 55 KB](https://ethresear.ch/uploads/default/68b00f87394db8a4f28ce7bb18d6c0a8c7797d2f)[![](https://ethresear.ch/uploads/default/optimized/3X/9/7/97831183a8c9a297610ef8e0d78adbe14be28403_2_440x250.png)1192×678 84.1 KB](https://ethresear.ch/uploads/default/97831183a8c9a297610ef8e0d78adbe14be28403)

The lack of onchain confidentiality has hindered the growth and adoption of even the most obvious applications. Confidentiality is one of the most misunderstood terms in crypto. On one end of the spectrum it is associated with money laundering and illegal financial activities and on the other, it unlocks high utility use cases such as normal private transfers, dark pools, frontrunning protection, confidential AI, zkTLS, gaming, healthcare and private governance.

Economies function efficiently when there is a balance between confidentiality and transparency. Take financial markets as an example - confidentiality makes information valuable and tradable, but selective disclosure of that information would be helpful in preventing [market abuse]. Many financial activities such as portfolio management, asset trading, payments, and banking require confidentiality with a need to balance data disclosure for compliance and regulation purposes. However, the phenomenon of selective disclosure is not limited to finance and compliance. A recent example is the confidential social media theme, which is currently battling misinformation and hate content, necessitating self-regulation by social media giants through [disclosures](https://www.brookings.edu/articles/transparency-is-essential-for-effective-social-media-regulation/)).

Recent challenges in fake content generation through AI models have raised questions about the value of sharing secrets and the on-demand disclosure of secrets. During the COVID pandemic, vaccine research raised controversy because important stakeholders were kept in the dark about the detailed results. Balancing confidentiality and transparency takes on many shapes, and sometimes regulation and compliance make this the most important problem to tackle. Technology comes to the rescue in finding the balance - the key question being asked is whether we can remove the centralized party in selective disclosure or compliance use cases.

We have confidentiality inside our walls, 95% of the internet, iPhones, bank accounts, elections and even a friendly poker game. Just the other day US slapped TD - [the largest bank in Canada- with $3B fine over cartel money laundering](https://www.cbc.ca/news/business/td-bank-penalties-1.7348819). But no one is going to avoid banks, no one is scared of privacy in other banks or industries, and even TD itself is not going down. An impactful system shouldn’t be vaporized and banned because of a few bad actors. In web3, we shouldn’t overreact to a few bad examples and myths that we’ve seen. We shouldn’t shy away from building the new internet and turn it into short-term distractions. In most cases, we don’t even have a compliance problem. For private transfers, we can build systems that are as compliant as real-world banks, but still more transparent, private and decentralized. More impactful problems are harder to solve, that’s the way it is.

Even if we only care about money, we can’t extract value from memecoins for another 16 years. Now that we have the scalable infrastructure, opportunities are going to be orders of magnitude greater if we have onchain confidentiality and real applications.

**The Elephant in the room**

One of the most pressing challenges of DeFi is the balance between confidentiality and compliance. Maintaining user privacy while ensuring regulatory oversight without centralization requires a delicate approach. This article explores the solution through selective disclosure, enabling privacy and accountability without compromising security or compliance.

So far in web3, we’ve figured out private transfers and know how to transfer and trade assets privately by proving the validity of transactions without leaking our private identities. The open-debated technical and philosophical challenge is how we can make sure that the technology is not used by minority of bad actors at the expense of the majority of active users, how can we have at least the same level of privacy as our current banks?

While the private transfers themselves are enabled by ZKPs, different centralized or decentralized techniques and cryptographic schemes such as MPC can be used for compliance. Some of the current efforts for making compliant private transfers are:

- Pre-transfer proof of legitimate funds (0xbow/Privacy Pools/Railgun): Users can prove non-association with lists of illicit activities or sanctioned addresses before execution of their transfers.
- Post-transfer selective de-anonymization: Balancing blockchain privacy and regulatory compliance by providing accountability using zk and threshold cryptography
- DID and regulatory smart contracts: Programming real-world rules such as the 10K limit, and other conditions by privately sharing information using decentralized identifiers and MPC/FHE.
- ID verification: Users should engage with non-private and centralized long and haphazard processes of KYC for each of the services they are using.
- Geography-specific private compliance: It allows Virtual Asset Service Providers (VASPs) to set up their “zones” with custom KYC/B, allow lists, and transaction limits in accordance with their local laws. Additionally, MPC can be used to add multiple VASPs to govern a zone instead of it being managed by a single entity.

However, none of these approaches are complete by themselves as they fail to address the balance between privacy and regulations. Deposit limits aim to block illicit funds but often result in inconvenience to legitimate users. Sanction lists are slow to update, allowing bad actors to operate before detection, and there’s no recovery for wrongly flagged addresses. Blockchain analysis tools such as Chainalysis, miss illicit activities due to false negatives. “View-only” access relies on user cooperation, failing against malicious actors. The association sets in privacy pools delay the detection of illicit transactions and rely on untrusted set providers. KYC compromises privacy by forcing users to disclose sensitive information on the first step of using privacy applications, without solving the problem of users turning malicious later. Ultimately, these approaches rely on centralized controls, undermining the decentralized nature of Web3.

[![](https://ethresear.ch/uploads/default/original/3X/1/a/1a479b794ea00a59dce82111e6bc90077c3beaf0.png)657×402 54.6 KB](https://ethresear.ch/uploads/default/1a479b794ea00a59dce82111e6bc90077c3beaf0)

**Co-existence of Privacy and Compliance through Decentralized Approaches**

The answer to balancing privacy and compliance lies in a decentralized compliance framework. This approach allows compliance to coexist with privacy by creating systems where compliance measures can be enforced without compromising user anonymity.

There needs to be different levels of decentralized pre-transfer compliance and case-by-case post-execution audibility through selective disclosure. This way, we still achieve common sense privacy for DeFi while allowing authorities to request more information on a rare case-by-case basis. At the very least, this offers an equivalent level of web2 and tradfi privacy with more decentralization and transparency properties.

Dark pools in traditional finance enable trader anonymity while ensuring regulatory post-trade transparency. Recently dark pools and privacy-focused blockchain protocols such as Railgun, Penumbra, and Renegade are gaining attention. However, they’re either non-compliant or only partially compliant. Selective disclosures can address these issues by ensuring that users’ actions are legitimate while preserving anonymity where appropriate. While users can use a mix of methods to prove their legitimate source of funds and identities, threshold networks can ensure post-transaction accountability.

**Post-transaction accountability through MPC/Threshold decryption**

In a threshold network, compliance and accountability are enforced without relying on central authorities. The system is based on independent entities such as Revokers and Guardians:

Accountable Privacy means that users must engage in legitimate activities. Malicious behavior can lead to selective de-anonymization, but only under lawful conditions, ensuring integrity without compromising user privacy unjustly.

Accountable De-Anonymization ensures that de-anonymization requests are public and traceable, requiring cooperation between Revokers and Guardians, thus preventing unauthorized disclosure.

Non-fabrication guarantees that honest users cannot be falsely accused, even if there is collusion. The cryptographic commitments ensure all participants are bound to act transparently, safeguarding user rights.

Here’s a detailed end-to-end flow explaining how transactions are managed, de-anonymization is requested, and the process is carried out in an accountable and publicly verifiable way by users, revokers, and guardians:

*User Transaction (Onchain)*

Users are accountable for doing compliant transactions. Users face de-anonymization if they act maliciously. Misbehavior leads to loss of privacy, but only under lawful conditions. A user initiates an onchain private transaction on the protocol, and encrypted data is included in the transaction payload. This ensures that all transaction details remain private and secure on-chain, preventing unauthorized access to the user’s data.

When creating a valid transaction, a user is constrained to encrypt transaction details (e.g. asset id, value, owner) using a specific encryption key and needs to provide a ZK proof for the same in the transaction payload. Otherwise, onchain ZKP verifier rejects the proof & transaction reverts as a result.

*Suspicious Activity Detection (Off-chain)*

A Revoker such as a DAO, trusted entity, or neutral gatekeeper, monitors the transaction off-chain, which uses monitoring tools to detect any potential illicit activity or suspicious behavior. The Revoker flags the user’s transaction if it appears to violate compliance rules or triggers suspicious activity alerts.

*De-Anonymization Request Submission (Onchain)*

Once the Revoker identifies a suspicious activity, they submit an onchain de-anonymization request on the governance dashboard. This request initiates the de-anonymization process and makes the request publicly verifiable and transparent to all the network participants. The Revoker does not have de-anonymization rights at this stage but is merely flagging the transaction for further review.

*Guardian Review and Voting (Off-chain)*

The request is picked up by a decentralized network of Guardians (trusted entities picked up through the governance process). These Guardians act as decision-makers and are responsible for validating the Revoker’s de-anonymization request. They assess the flagged transaction according to governance policies and determine whether de-anonymization should be allowed. This review process occurs off-chain to ensure the privacy of decision-making and governance.

*Threshold Mechanism (Onchain)*

For the de-anonymization request to proceed, a certain threshold of Guardian approvals must be met (e.g., 6 out of 10 Guardians need to approve). Each Guardian that votes in favor of de-anonymization submits their cryptographic permission onchain, which is aggregated to reach the required threshold. This on-chain submission guarantees transparency and prevents any foul play or unauthorized actions.

*De-Anonymization Execution (Off-chain)*

Once the necessary cryptographic permissions have been granted, the Revoker can decrypt the flagged transaction. This process happens off-chain, and only the specific transaction under investigation is revealed to the Revoker—no other data or transactions are affected or exposed. Importantly, even the Guardians who approved the request do not gain access to the transaction details; only the Revoker can view the decrypted transaction information.

*Post-De-Anonymization (Onchain)*

If further suspicious activity is linked to the decrypted transaction, it will be flagged separately, requiring a new de-anonymization request to be submitted by the revoker and approved by the Guardians. The rest of the user’s transaction history and data remain encrypted and private. This ensures that privacy is maintained for non-flagged transactions while enabling compliant de-anonymization for suspicious activities.

[![](https://ethresear.ch/uploads/default/optimized/3X/c/0/c06c6733354f18254792958d1ccf872057a2fbba_2_566x293.png)1600×831 119 KB](https://ethresear.ch/uploads/default/c06c6733354f18254792958d1ccf872057a2fbba)

*Security*

There’s a trust assumption in the threshold network. A dishonest majority of malicious validators can work together to decrypt transactions - with or without detection depending on the scheme.

It is worth mentioning that the consequence of such an attack is losing confidentiality, and neither the safety of the network, loss of funds nor private information regarding the identities of users. In this case, the system’s confidentiality will downgrade to the current state of public blockchains. The consequence is more limited in the cases where only ephemeral confidentiality is required or confidentiality is leveraged for better execution quality, not the privacy of users e.g. frontrunning protection, and sealed-bid auctions.

However, validators and operators should be incentivized to protect user privacy with respect to the stakes in the game. The solution lies in building robust networks where compliance can be enforced without compromising decentralization. The transition will involve integrating permissionless compliance mechanisms, where incentives are aligned to encourage honest validator behavior. Approaches like Proof of Stake (PoS) and AVS ensure network security, while [cryptographic traitor tracing](https://www.youtube.com/watch?v=OnpCB5TWsGs)and slashing mechanisms deter malicious actors. There are many promising recent works such as [Multimodal Cryptography - Accountable MPC + TEE - HackMD](https://hackmd.io/@Fairblock/rkSiU78TR)

**Threshold MPC and confidentiality beyond compliant transfers**

The use of Threshold MPC extends beyond compliance, finding applications across multiple confidentiality sectors:

- Frontrunning protection and MEV Protection: Preventing manipulative trading practices by hiding transaction data until completion. Replacing centralized relayers in Ethereum’s MEV supply chain. Leaderless and incentive-aligned MEV or preconfirmation auctions.
- PvP GameFi or prediction markets: Ensuring fairness and excitement by concealing actions until necessary. Adding the element of onchain surprise by decrypting values. Decentralize decryption of oracle updates in prediction markets (instead of naive hashes as in UMA)
- Private Governance/Voting: Prevention of manipulation during decision-making processes, coercion resistance, and privacy of voters.
- Access Control and SocialFi: Enhancing privacy in decentralized applications while retaining usability and accountability as well monetization of contents in creator economies.
- Confidential AI: Decentralized and privacy-preserving systems for training, inference and data sharing to unlock access to more players and data and not being limited because of privacy concerns.
- Healthcare: Access to more and better personalized healthcare services by analysis of biological or health data without loss of privacy or trusting centralized parties.

**Path Forward: Seamless Web3 Confidentiality**

The ultimate goal for privacy in Web3 is to make it as seamless as it is in Web2. Encryption in traditional internet applications (e.g., HTTP transitioning to HTTPS) has become so common that users hardly notice it. A similar evolution is required for Web3—Confidentiality should be invisible to the user, seamlessly integrated into their experience. While most confidentiality schemes don’t have compliance challenges in the first place, private transfers can be compliant through multimodal cryptography techniques such as MPC and ZKPs.

## Replies

**MicahZoltu** (2024-10-15):

It would be nice if this post explained what exactly needs to be complied with, and why we should all comply with that specific law (which likely only applies to a very small set of people in the world).

Should we all comply with China’s financial surveillance requirements?  If so, which specific laws/regulations are we trying to comply with?

Much discussion on this topic revolves around complying with imagined laws.  Tornado Cash built their compliance tool around such an imagined law, and the US government just ignored it entirely when they sanctioned the contracts and arrested the developers.  We shouldn’t be building compliance tools targeting imagined regulations/laws because it doesn’t offer any legal protection, and if we do choose a specific target regulation/law to comply with we should recognize that we are reducing privacy for the rest of the world in order to comply with one country’s regulatory regime.

Financial privacy is not a crime.

---

**pememoni** (2024-10-15):

just added this, I think it’s good start for this challenge:

- Geography-specific private compliance: It allows Virtual Asset Service Providers (VASPs) to set up their “zones” with custom KYC/B, allow lists, and transaction limits in accordance with their local laws. Additionally, MPC can be used to add multiple VASPs to govern a zone instead of being managed by a single entity.

---

**MicahZoltu** (2024-10-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/pememoni/48/9476_2.png) pememoni:

> Geography-specific private compliance: It allows Virtual Asset Service Providers (VASPs) to set up their “zones” with custom KYC/B, allow lists, and transaction limits in accordance with their local laws. Additionally, MPC can be used to add multiple VASPs to govern a zone instead of being managed by a single entity.

It feels like such a setup would result in a massive fragmentation of the financial system, and whitelists would mean that all of the people who are denied access to the global financial system (e.g., people who don’t have IDs) would still be denied access to the global financial system.

---

**pememoni** (2024-10-15):

my initial thoughts are

- tradfi is 99% fragmented between west and the rest of the world.
- crypto itself is not used as a payment method in most powerful countries because of compliance risks, but widely used in the rest of the world

so while I agree with you and that’s my ideal as well, I think a nice significant step is making it work for those who want to be compliant with the most serious regulatory blockers (most sanctions and regulatory challenges are coming from the US even in tradfi), showing the path for other regulations, while other countries/parties are not forced to use it (only if they want to work with US entities). Also, this system doesn’t necessarily require traditional IDs, we can have different mechanisms for pre-transaction checks. The article suggests that we should complete that with post-tx accountability as well.

I think this way we can make the financial system less fragmented and more private/transparent/efficient than the current situation AND make crypto payments work in the West as well (I’m not knowledgeable enough about China)

In future, I do want to see the ideal world that uses a decentralized network for IDs (hopefully + ZK), activity history and a global list of banned addresses so we don’t need to design the system in a way that only suits a few of the most powerful countries’ good or bad intentions. However, in the meantime, I think we shouldn’t let DeFi or blockchains die and want to try our best to build the most pragmatic system for everyone and iterate over that to get closer to a fair, decentralized, and private financial system.

Financial privacy is not a crime, but we can’t change how the world works in one step or with 5 startups with 5m dollars in the bank. What we can do is make it work 5 times better and take 5 small steps toward the end goal.

---

**chaudhary-amit** (2024-10-15):

Thanks [@MicahZoltu](/u/micahzoltu) : In addition to our original post, I want to emphasize the complexity of balancing privacy and regulation. There are various approaches to this challenge, each with its own set of advantages and disadvantages below.

> However, none of these approaches are complete by themselves as they fail to address the balance between privacy and regulations. Deposit limits aim to block illicit funds but often result in inconvenience to legitimate users. Sanction lists are slow to update, allowing bad actors to operate before detection, and there’s no recovery for wrongly flagged addresses. Blockchain analysis tools such as Chainalysis, miss illicit activities due to false negatives. “View-only” access relies on user cooperation, failing against malicious actors. The association sets in privacy pools delay the detection of illicit transactions and rely on untrusted set providers. KYC compromises privacy by forcing users to disclose sensitive information on the first step of using privacy applications, without solving the problem of users turning malicious later. Ultimately, these approaches rely on centralized controls, undermining the decentralized nature of Web3.

It’s important to note that removing the central trusted component in many cases is not a simple task.

However, the second part of the post,

> “Co-existence of Privacy and Compliance through Decentralized Approaches,”

provides a more comprehensive explanation. I highly recommend reading it.

Additionally, to your point I agree it is important to acknowledge the intricacy of encoding local laws into a single system or achieving complete knowledge of them. In this context, a multi-party system where both the user and the protocol collectively determine the appropriate way to interact with the entity known as the Revoker holds significant value. The Revoker accumulates knowledge about local laws and ensures that selective de-anonymization occurs in a decentralized manner while adhering to local regulations. The process of encoding laws onto a network is impractical, and delegating this responsibility to a DAO or a knowledge entity represents a more sustainable long-term solution

---

**MicahZoltu** (2024-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/pememoni/48/9476_2.png) pememoni:

> In future, I do want to see the ideal world that uses […] a global list of banned addresses so we don’t need to design the system in a way that only suits a few of the most powerful countries’ good or bad intentions.

I suspect this may be the core of our disagreement.  History has shown that every time some entity is given the power to censor (money, information, media, etc.) it eventually is abused by those who control the power.  Censorship *always* starts out with “only the bad guys” and that is *always* its purported purpose.  The problem lies in who has the power to decide who are “bad guys”.  Even democratic systems of decision making will eventually result in tyranny of the majority where people will vote to censor those they personally dislike (e.g., other races, other religions, people with different medical beliefs, etc.)

![](https://ethresear.ch/user_avatar/ethresear.ch/pememoni/48/9476_2.png) pememoni:

> we can’t change how the world works in one step or with 5 startups with 5m dollars in the bank. What we can do is make it work 5 times better and take 5 small steps toward the end goal.

I am not convinced that creating a compliant financial system is a step in the right direction.  I am of the opinion that it is actually a step in the wrong direction as it takes away development and social movement effort away from true censorship resistance and towards the same financial tyranny that many of us are trying to escape.  If we want compliance, the USD or CNY is a perfectly reasonable choice of currency and you can use SWIFT or similar for sending/receiving money in a compliant way.  No need for the complexity of crypto if that is the end goal.

---

**MicahZoltu** (2024-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/chaudhary-amit/48/17876_2.png) chaudhary-amit:

> The Revoker accumulates knowledge about local laws and ensures that selective de-anonymization occurs in a decentralized manner while adhering to local regulations.

As alluded to in my post above, this cuts to the core of the problem.  Local regulations are very often the exact evil that people would like to avoid with financial privacy.  The Chinese government can and does simply take money from people via the banking system.  The US also actively engages in civil forfeiture on a regular basis.  Most large governments in the world use the banking system as a way to control their population.

In the US, financial privacy was legislated/regulated away via the Bank Secrecy Act (BSA) and the Third Party Doctrine (TPD), despite it being constitutionally protected.  I hope that one day the constitutionality of that combo is challenged at the Supreme Court and they have the political willpower to strike it down, but in the meantime we live in a world where legislators and regulators have worked together to violate what are supposed to be “inalienable rights”.  We should be striving to legally take that power away from them, such as through intermediaryless private transactions (see CoinCenter’s writings on this for why such transactions are not beholden to BSA and TPD) and reclaim the liberty that has been stripped of people around the world.

---

**ethereumpepe** (2024-10-31):

Thanks, [@pememoni](/u/pememoni), for creating this topic. I am one of the contributors of Panther Protocol, and, over the last ~3.5 years, we at Panther Protocol have been building a solution for privacy-preserving DeFi. We are proud of what Panther can support from a compliance perspective. Perhaps most of the Ethereum community is less familiar with what we have been building as Panther is currently in testnet, as opposed to some of the projects named in your posts that are already live.

A few of Panther’s technical highlights:

- Multi-Assets Shielded Pool (MASP) preserves user confidentiality
- UTXO model for assets and mixed model for “zAccounts”
- Unified, append-only Merkle Tree of UTXOs for all assets
- Shared anonymity set across supported networks
- zkSNARK (Groth16) proofs to verify customizable rules

We believe that privacy should be a qualified right. Panther is all about consent and confidentiality. Right now, even traditional finance is more private than DeFi in its current form. Panther’s architecture is an answer to what happened with previous privacy protocols, as there was a lack of compliance tooling to protect the overall infrastructure and its users. Web3 users should not be scared to use privacy technology.

Panthers’ design includes Know Your Customer (KYC) and Know Your Transaction (KYT) attestation mechanisms. These allow users to prove they comply with rules during onboarding while preserving privacy through zero-knowledge proofs! At Panther, we call this ‘’Smart Compliance.’’ Panther also will include capabilities for illicit activity prevention via transaction monitoring and risk analysis at runtime using ZK-proofs. It also allows for selective disclosures, meaning that if desired, it is possible to reveal only the relevant information to the relevant parties involved; maintaining the confidentiality of other parties on the platform.

The protocol is designed so that pre-transaction checks at runtime are preferred over post-transaction checks, and that checks/analyses are based on obfuscated user data and ZKPs, rather than PII and private data.

Panther’s KYC attestation process, in a nutshell, consists of a claim signed by the KYC attester (using a circuit-friendly signature) that a user with the specified Main EoA passed KYC checks according to the stated rules on the specified date. The KYC Attester is a KYC provider that signs KYC/KYT attestations whereas the KYC provider is a specialized entity that performs KYC/KYT checks, resulting in KYC profiles and KYC attestations. The KYC Profile consists of records about a user, including personal identifiable information (PII), maintained by a KYC Provider, linking the user’s Main EoA to their identity. During onboarding, the user proves (through ZK) the correctness of the KYC attester’s signature and the attestation’s conformance to the protocol rules.

A KYT attestation is a claim signed by the KYT attestor (with a circuit-friendly signature) that a transaction (e.g., depositing a predefined token in the stated amount from the predefined blockchain address) is considered by the Attester as having a Risk Score below the required threshold. In every transaction, the user proves (through ZK) the correctness of the KYT attester’s signature and the attestation’s conformance to protocol rules. This includes:

- KYT attestation for deposits and withdrawals from/to external wallets
- KYT attestation on internal transfers also if the receiver is another user
- Special rules for transfers to another Zone

On every transaction made using Panther, the user encrypts private parameters and proves their correctness and proper encryption using ZKPs. We call this the protocol’s Data Escrow. The ciphertext and its commitment are registered (“escrowed”) on-chain. Except for the user who knows the Data Escrow content, other parties need private “Escrow Keys” to decrypt the Data Escrow for a transaction.

When live, Panther’s MASP will have its own “Zones,” with programmable rules for user onboarding and transactions that are obfuscated from external observers. A Panther Zone is a logical partition of the MASP – a sort of a walled garden. Each Zone will be managed by a licensed operator (Zone Manager), who controls the operator’s private key. Because of this, the Zone Manager can define the onboarding settings and transaction requirements aligned with the jurisdiction from which it operates. This includes:

- Applicable KYC and KYT rules
- Transaction limits (e.g., maximum deposit amount, daily limits)
- Allowed Zones for asset transfers into or out of the Zone

Every transaction belongs to a specific Zone and must meet its requirements. We believe that Panther can be the answer to Ethereum’s privacy challenges, as well as those of other chains. Feel free to get in touch if you would like to learn more about what we are doing here. I would encourage everyone who cares about privacy-preserving technology to check out our testnet on Sepolia and Amoy.

---

**cryptskii** (2024-11-27):

Don’t worry I got you. Let’s chat

