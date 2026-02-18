---
source: magicians
topic_id: 6844
title: "ERC-3643 : the T-REX token standard"
author: Joachim-Lebrun
date: "2021-08-12"
category: ERCs
tags: [token, security-token]
url: https://ethereum-magicians.org/t/erc-3643-the-t-rex-token-standard/6844
views: 7221
likes: 10
posts_count: 17
---

# ERC-3643 : the T-REX token standard

This is the discussion topic for [EIP-3643](https://github.com/ethereum/EIPs/pull/3643): T-REX token standard for securities.

This standard is used to tokenize securities and is based on ERC-20, on top of which we added 2 permission layers :

- the first permission layer being linked to the identity of the transaction’s receiver and its eligibility following preset rules defined by the token issuer (using ERC 734/735 for the identities and checking if the required claims are present on the identity and are signed by the trusted claim issuers)
- the second permission layer being based on global restictions applied to the token as such, e.g. maximum amount of token volume per day, maximum amount of token holders, …

## Replies

**wschwab** (2021-08-12):

Hi!

I wanted to ask if you are aware of previous efforts to make a securities-compliant token, and if so, why you decided to go with a new implementation. This isn’t a field I really have much knowledge in, so I’m interested in what goes in to the architecting here.

Cheers!

---

**Joachim-Lebrun** (2021-08-13):

Hello, we are well aware of the existence of the other security token standards, but we decided to have a different approach, as we wanted to have the possibility to process more complex compliance & eligibility checks onchain, that’s why we decided to go for another implementation, including the use of onchain identities and specific compliance contracts tailor-made for each token, but working through a standard interface, as described in ICompliance doc.

It is also important to note that T-REX tokens are used for about 3 years now in the industry and that >8,5 billion € of securities are already tokenized with this token standard, therefore it is not really a new implementation, what is new is the request that we made to add the standard in the EIPs library

cheers!

---

**luzius** (2021-08-13):

(Copied from https://github.com/ethereum/EIPs/pull/3643#issuecomment-898248180)

I believe that this approach is fundamentally broken as it comingles concerns from different legal layer into one big monolithic technical blob. As an adverse side-effect, it makes basic operations like transfers significantly more expensive than a simple ERC-20 token. Furthermore, giving the issuer total control over the issued tokens does not only go against the spirit of decentralization, it might also violate investor protection laws designed to protect token holders from the issuer in case of conflicts of interest.

Here is a concrete example: let’s assume that the founder of a successful company wants to use his tokenized shares in that company as a collateral to get a credit. He won’t be able to use a DAI-style DeFi protocol as they require the ability to take exclusive control over the deposited assets that serve as collateral. So he asks his bank for a credit. The bank would love to provide the credit, but their compliance department is reluctant to approve the collateral because they know that the founder has access to the admin key, enabling the founder to “steal” the collateral at any time. I say “steal” in quotes as such an action would not legally qualify as stealing, because the taken assets still belong to the founder when used as a collateral, so it is not exactly theft. Further, the bank’s cyber insurance says they cannot provide insurance coverage for assets that are not truly under the control of the bank and the regulator is worried about the bank being able to auction off the asset in case of a default of the founder, so they do not recognize the collateral as risk-reducing when calculating capital requirements. All of this could be solved if the token offered the possibility to provide *exclusive control* over the token to the current holder.

As a side note, Swiss law explicitely recognizes the possibility to use crypto securities as a collateral, but it requires that it is technically ensured that the creditor has exclusive control over the crypto securities in case of a default. The reasoning behind this requirement are scenarios like the above.

So what is the correct way out?

The correct way out in my opinion is to depart from the monolithic “one size fits all” approach and to go for a layered design, distinguishing four layers.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/c/c2fa7603e226235e3da975024762e1befc69f0ed.png)](https://user-images.githubusercontent.com/3128389/129317714-affc527d-fb16-4bf2-9f49-bd2c532639e3.png)

The bottommost layer is the **infrastructure layer**. In our case, this would be the Ethereum blockchain, fulfilling basic requirements regarding data integrity, transparency, and so on. On top of that is the **register layer**, which essentially is an ERC-20 token that fulfills all constitutive legal requirements to represent a security token, but none of the circumstancial compliance rules that depend on the token holder, jurisdiction, involved intermediaries, etc. Legally, compliance rules are also added on a different layer than the basic rules that define what a security actually is and what it takes to create one. Also, compliance rules come and go whereas the basic rules about the issuance and transfer of securities last for decades. It makes sense to separate these different legal concerns also in the technical implementation. So the register layer ideally is a minimal ERC-20 contract with a few features added that are strictly necessary to make the tokens legally recognized securities (under Swiss law, the only feature that is missing in the ERC-20 standard is a link to a document called the “registration agreement” that specifies what the token actually represents and other general terms the tokens are subject to). Ideally, this base contract is not upgradable at all, potentially providing the token holders with a very high level security.

On top of the register layer, there is an **administrative layer** that adds all kind of administrative features, for example token recovery in case of a loss of private keys. Ideally, these features are added by wrapping the token and not by extending its functionality, making sure that it is possible to free the basic token on the register layer from all administrative backdoors if necessary, for example under the circumstances described in the example. Also, having this layer separated from the register layer creates a lot of flexibility, for example implementing a different set of rules for one jurisdiction than in another jurisdiction. One should also be careful to not call this layer “compliance” layer as “compliance” is usally used in the context of financial intermediation and AML rules, which in general do not apply directly to issuers. So the administrative layer is really reserved for token administration through the issuer, not for fulfilling the compliance requirements of individual custodians or other financial intermediaries that might hold the tokens at some point in time.

The latter requirements, the compliance rules of individual intermediaries, should be implemented on the **contractual layer**. Often, such rules are defined in the general terms applicable to the relation between an individual token holder and a financial intermediary. Even within jurisdictions, they might differ from intermediary to intermediary, for example requiring different levels of identity verification. All these kind of requirements are implemented on top of the other layers, usually without the involvement of the issuer. Also, this layer might contain smart contracts to automatically enforce shareholder agreements and the like.

It is important to have such a separation to cleanly deal with examples like the following (again coming from Swiss law, not sure how this works in other jurisdictions): assume an employee received tokenized shares from an issuer as part of an employee participation plan. The employee is not allowed to sell the shares according to his employment agreement, but does so anyway. The company refuses to execute the transfer of the tokens, saying that the transfer would violate the employment agreement. The empoyee goes to court and the court orders the company to approve the transfer because the refusal of a share transfer requires an according clause in the articles of association, which the company is lacking. Nonetheless, the employee is liable for violating the employment agreement. This example shows that the legal situation also has different layers, with the contractual agreements on upper layers not being able to supercede the applicable terms on lower layers. Of course, the company could have implemented an additional smart contract on the contractual layer to lock the shares of the employees and to enforce compliance with the employment agreement, but it is in general not allowed to use the terms of the register layer to enforce contractual agreements that have been made on a higher layer.

Let me know if you’d like to know more. The Swiss Blockchain Federation is working on an update to their Circular on Security Tokens, outlining these concerns in more detail.

---

**Joachim-Lebrun** (2021-08-13):

Hi,

As you are probably  expecting, we cannot agree with you. We tried to provide a short and concise answer below to all the incongruences in your post:

- In regards of the law-related remarks, please note that the T-REX standard is already approved in its fundamental approach by all our customers lawyers (including some of the major European banks) and it has already been used to tokenise more than 8,5 billion € of assets across the globe. Also Tokeny Solutions, creator of the T-REX token standard is backed by Euronext who never rose any legal concerns of this kind. In facts what you have to understand is that the fundamental approach of T-REX is coming from years of discussion with the various actors of the industry, as well as decades of experience from our team members in the world of securities (stock exchanges, central banks, major CSDs, etc).
- When it comes to the gas use, we are well aware of the additional costs of such transactions, especially on Ethereum Main Net. The standard might not be cheap to use but if you had a better understanding of our customers (mostly handling private placements) and the traditional financial industry, you would know that it remains a much better options than already existing frameworks for many reasons. Also as it is developed in solidity it can be used on any EVM based blockchain, T-REX tokens are already deployed on the polygon network for instance when dealing with customer targeting retails and facing important number of transactions.
- Last but not least, T-REX is indeed a centralised and permissioned protocol deployed on top of a decentralized infrastructure. If you think it should be fully decentralized, we strongly advise you to DYOR about the legal obligations of issuers and agents of securities In Switzerland (as it seems to be your focus) and everywhere else in the world. Every T-REX token is deployed in parallel with a full legal paperwork describing the issuer and its agents obligations. Such actors are for most of them regulated by their respectives local authorities. They will not “steal” security tokens from investors. We are not in DeFi here. Every actor is identified with a unique ONCHAINID and responsible for what they do, therefore it is not possible to “rugpull” a T-REX token.
Hopes it helps to bring a bit of light in your thoughts

---

**cmartins** (2023-05-17):

Hi there,

Is this standard still valid? If so, why is the eip submission with the “Stagnant” tag in there [ERC-3643: T-REX - Token for Regulated EXchanges](https://eips.ethereum.org/EIPS/eip-3643)?

Whata are the other options for securities standards?

many tks

---

**Joachim-Lebrun** (2023-05-18):

Hi [@cmartins](/u/cmartins)

The EIP is indeed Stagnant, but it will be updated very soon, EIPs are put in stagnant status when there is no change done on the last non-final version of the EIP for a certain period of time (usually 6 months).

The reason we didn’t touch the EIP during that time to move it to the next step towards final status is because there was still some ongoing development on the T-REX standard, which is the main implementation of the EIP. The development is now done, the version 4 of T-REX has been successfully audited by an external auditor company (Hacken) and the code has been released earlier this month.

You can find the code on the following repository : [GitHub - TokenySolutions/T-REX: T-REX is a suite of smart contracts implementing the EIP 3643 and developed by Tokeny to manage and transfer financial assets on EVM blockchains](https://github.com/TokenySolutions/T-REX)

The V4 comes with some breaking changes on the interfaces that need to be translated into the EIP.

We can now propose to the Ethereum community to move the EIP out of the stagnant status and continue the process to get the final status as soon as possible.

In the meantime we also created an association for the standard, you can find more details here : https://www.erc3643.org/

Be assured that the standard is definitely not dead and is more thriving than ever !

If you have any additional questions about the EIP feel free to ask them here

---

**SamWilsn** (2023-10-31):

Hey! I have a few non-Editoral comments that I’d like to raise before you go into last call:

First, in the `IAgentRole` interface, who do you expect to call the `addAgent` and `removeAgent` functions? I would, perhaps naively, assume that these would only be called by the owner of the various contracts implementing this interface. We recommend standardizing only those functions which need to be called from different independent systems. For example, ERC-20 doesn’t standardize `mint`/`burn` because those functions are generally only called by the contract’s owner, who knows what specific API to expect.

I could imagine a scenario where `addAgent` and `removeAgent` are called by some regulatory contract that needs to interact with many different ERC-3643 implementations, but I want to be extra sure that’s what you intend.

Similarly, standardizing `mint` and `burn` here restricts you to use cases where the tokens are minted manually.

At the very least, I’d like to see the reasoning for including these functions in your Rationale section. Could be as simple as something like “mutation functions like `mint`/`burn` are included so that standard admin interfaces can be built to work across all T-REX implementations”.

---

**Joachim-Lebrun** (2023-11-01):

Hello [@SamWilsn](/u/samwilsn) ,

Thank you for taking the time to review the ERC-3643 and for your insightful comments. I’d like to address your concerns regarding the inclusion of certain functions in the interfaces and provide our rationale for their existence:

**1. Basic Implementation Assumption vs. Real-World Security & Flexibility Needs:**

While a basic implementation might see an EOA set as the owner, adding Agents that are also EOAs, we believe this approach might not capture the full potential and flexibility of T-REX tokens. Setting a simple EOA as the owner presents a single point of failure. Should access to the wallet be lost, the consequences could be severe, possibly leading to a token redeployment. Instead, we propose a more secure and flexible setup:

**Owner Role:**

- Security Concerns: Assigning an EOA as the sole owner is a vulnerability. If compromised, it jeopardizes the token’s entire operation.
- Mitigation: Our recommendation is to assign the owner role to smart contract structures, like multisig contracts, with a keen emphasis on role management and compliance. By doing so, the risk of inadvertent actions is minimized as it necessitates multi-party validation.
- Flexibility & Delegation: The owner role in its current form is overly permissive. By using smart contracts, we can achieve a more granular role delegation. For example, restricting certain users to specific owner-scoped functions. An illustration of this approach can be found in our T-REX repository: OwnerManager.sol.

**Agent Role:**

- Operational Necessity: The functions available to agents are mostly operational, encompassing tasks like minting, burning, freezing, etc. While these could be managed through EOAs, it isn’t the most optimal or secure route.
- Use Cases for Smart Contracts: By assigning the agent role to contracts, we open up a wide array of automation and operational possibilities:

Automated Fund Management: Smart contracts can auto-manage open-ended fund subscriptions and redemptions by triggering the mint and burn functions.
- Security Protocols: Freeze functions can be automatically invoked by a dedicated smart contract when a wallet is identified as participating in illicit activities.

*AgentManager for Granularity:* In a similar vein to the OwnerManager, we have developed an [AgentManager contract](https://github.com/TokenySolutions/T-REX/blob/main/contracts/roles/permissioning/agent/AgentManager.sol). This contract adds more granularity to the Agent role, which otherwise is too permissive. It allows for a nuanced approach to managing Agent permissions and actions.

**2. The Standard’s Open-Ended Nature:**

The very essence of ERC-3643 is to provide a framework that’s adaptable to different operational and security needs. By including these functions, we aren’t mandating a specific implementation but rather offering the flexibility to integrate with additional contracts or systems as needed.

In conclusion, the inclusion of functions like `addAgent`, `removeAgent`, `mint`, `burn` and other functions in the interfaces, even though they might seem superfluous at first glance, caters to a broader vision of security and operational adaptability. The ERC-3643, in its entirety, seeks to offer a secure, flexible, and forward-compatible framework for token operations.

Thank you for your understanding, and I appreciate any further feedback you might have.

---

**vittominacori** (2025-03-02):

I would like to explore a use case to see if this could be a security issue.

1. Bob and Alice are both KYCed and verified.
2. Bob has 200 tokens.
3. Bob approves Alice to spend 100 tokens using approve.
4. Bob is frozen for some reason, so Alice cannot get Bob’s token.
5. The agent forces transfers of 100 tokens from Bob to Alice to cover the previous topic.
6. Alice is left with an allowance of 100 tokens from Bob.

What happens if Bob will be unfrozen again?

Alice could `transferFrom` 100 tokens from Bob’s balance.

Is this scenario covered somewhere?

---

**Joachim-Lebrun** (2025-03-03):

Hi [@vittominacori](/u/vittominacori)

The Force transfer should not be used in this case, instead the agent should unfreeze the amount of tokens that bob has to send if this is a legitimate transaction and then Alice can call the transferFrom.

Force Transfer is a function that should never be called except in extreme cases in my opinion, that function bypasses compliance checks and freeze status, it is only to be used when there is no alternative.

If the point is that you want transfers to happen only when it has been approved by the agent (which would explain why you freeze everything and want to use force transfers) there is a way to do it in a cleaner way by using the compliance contracts to only allow transfers that are pre-approved by an agent or the issuer.

Here an example of such compliance feature [T-REX/contracts/compliance/legacy/features/ApproveTransfer.sol at main · TokenySolutions/T-REX · GitHub](https://github.com/TokenySolutions/T-REX/blob/main/contracts/compliance/legacy/features/ApproveTransfer.sol)

---

**vittominacori** (2025-03-04):

Hi [@Joachim-Lebrun](/u/joachim-lebrun), sorry for the late reply.

No, I’m not referring to a must-be approved transfer from agent.

Ok, so in that case, Alice is in charge of completing the `transferFrom` once Bob will be unfrozen.

Anyway this scenario do not cover the above topic, because we may not want to unfrozen Bob for any reason (i.e. could be not compliant anymore).

Obviously not all cases can be covered and must be analyzed according to the initial requirements or specific use cases. Thanks for your time.

---

**Joachim-Lebrun** (2025-03-05):

Yes, i believe this is a general thing about all ERC-20 and extensions of ERC-20 (including ERC-3643), you should always be aware of who you give approval to and you should remove the approvals that are not used or are putting you at risk, ERC-3643 doesn’t modify the main mechanics of ERC-20 in that sense.

---

**tinom9** (2025-04-30):

[@Joachim-Lebrun](/u/joachim-lebrun), what are your thoughts on narrowing the token interface in a different ERC, to allow for simpler implementations?

In very rough terms, identity registry and onchainID could be embedded in the compliance module, and TIR, and CTR could be implemented on top of forced transfers.

On the other hand, I find token permissioning functions very strong and accurate, leading me to believe it would make sense to propose a backwards compatible ERC with a narrower scope that enables minimal T-REX-like deployments:

- Token interface:

Pausable (pause, unpause, isPaused).
- Address freezing (setAddressFrozen, isFrozen).
- Partial token freezing (freezePartialTokens, unfreezePartialTokens, getFrozenTokens).
- Forced transfers (forcedTransfer).
- Minting and burning (mint, burn).
- Agnostic to ownership, versioning, token holder identity, and claims.
- Additional transfer rules through compliance (compliance).

Compliance interface:

- Exposes unique check (canTransfer).
- Modular.
- No token binding.
- Optional stateful hooks (transferred, created, destroyed).

Congrats on your job so far!

---

**xaler** (2025-05-01):

[@tinom9](/u/tinom9) I agree that for a standard, achieving agnosticism, maximize compatibility and composability are the most important things. RWA is a broad spectrum with plenty of functionalities that might or might not be required

---

**Joachim-Lebrun** (2025-05-02):

Hi [@tinom9](/u/tinom9) thanks for the feedback ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

The ERC being in final stage there cannot be any modifications to the interfaces anymore.

What you propose could be done, but it doesn’t really bring additional (missing) features that would make the ERC-3643 standard not usable for specific use cases, it would just simplify a bit the interface but at the same time break the standardization (as dapps developed to manage ERC-3643 would try to call `isVerified()` on the Identity Registry for instance. Therefore i don’t believe it would be desirable to make another standard, as the whole point is to standardize as much as possible. To be clear, the interfaces of ERC-3643 are probably not perfect and could be simplified, but the added value of standardization, i believe, surpasses the desirability of simplification/optimization.

I already had the same thoughts about the fact of making the Identity checks part of a compliance module, it could indeed make sense and be doable, but it would break backwards compatibility with ERC-3643 without adding much added value outside of code simplification.

---

**devender-startengine** (2025-12-23):

Hi @Joachim (and ERC-3643 community),

Congratulations on the $28B+ tokenized through T-REX - that’s impressive real-world validation.

I’m working on ERC-1450, a complementary standard specifically designed for US-regulated securities where SEC rules require a Registered Transfer Agent (RTA) to have exclusive control over all token operations.

How Our Approaches Differ

| Aspect | ERC-3643 (T-REX) | ERC-1450 |
| --- | --- | --- |
| Control Model | Validator system (multiple validators can approve) | RTA-exclusive (single regulated entity controls all operations) |
| Transfer Flow | Automatic if validators approve | Request → RTA Review → Execute |
| Compliance Check | On-chain identity registry + claim validators | Off-chain KYC/AML, RTA makes final decision |
| transfer() behavior | Works if compliant | Always reverts (only RTA can move tokens) |
| Target Jurisdiction | Global / EU MiCA friendly | US SEC regulations (Reg CF, Reg D, Reg A+) |

Why a Separate Standard?

US securities law has a specific requirement: the Registered Transfer Agent (a SEC-registered entity) must maintain exclusive control over the shareholder registry and all transfers. This isn’t just a compliance preference - it’s a legal requirement under the Securities Exchange Act.

ERC-3643’s validator model is elegant for jurisdictions with flexible compliance frameworks, but for US securities:

- The RTA cannot delegate transfer authority to on-chain validators
- Every transfer must go through RTA review (even if automated on their end)
- transfer() and approve() must be disabled to prevent unauthorized movement

Questions for the Community

1. Interoperability: Has anyone explored bridges between validator-controlled (ERC-3643) and controller-controlled (ERC-1450/ERC-1400) security tokens? A US company might issue under ERC-1450 domestically but want ERC-3643 compatibility for EU secondary trading.
2. Claim Issuers: In ERC-3643, claim issuers verify identity. In the US, the RTA performs this function. Could an RTA act as a claim issuer in a hybrid model?
3. Identity Registry: We handle identity entirely off-chain (the RTA’s database). What’s been your experience with on-chain vs off-chain identity for regulatory audits?

Resources

- Discussion: ERC-1450: RTA-Controlled Security Token Standard
- PR: Update ERC-1450: Move to Draft by devender-startengine · Pull Request #1335 · ethereum/ERCs · GitHub
- Reference Implementation: GitHub - StartEngine/erc1450-reference (643 tests, 86%+ coverage, Halborn audit in progress)

We’ve tokenized $1B+ in compliant offerings using this model operationally - now formalizing it as an ERC.

Would love to hear thoughts from those who’ve worked across multiple jurisdictions. Are there patterns from ERC-3643 deployments that could inform cross-standard compatibility?

Best,

Devender

StartEngine

