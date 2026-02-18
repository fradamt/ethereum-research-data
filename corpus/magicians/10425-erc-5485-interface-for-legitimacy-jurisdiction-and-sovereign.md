---
source: magicians
topic_id: 10425
title: "ERC-5485: Interface for Legitimacy, Jurisdiction and Sovereignty"
author: xinbenlv
date: "2022-08-18"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-5485-interface-for-legitimacy-jurisdiction-and-sovereignty/10425
views: 2077
likes: 3
posts_count: 11
---

# ERC-5485: Interface for Legitimacy, Jurisdiction and Sovereignty

---

## eip: 5485
title: Jurisdiction, Accreditation, and Enforcement
description: An interface for identifying the sovereignty status, observed jurisdiction, accreditation, and enforcement mechanisms.
author: Zainan Victor Zhou ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-08-17
requires: 5247

## Abstract

Defines a standard interface for smart contracts to declare their sovereignty status, observed jurisdiction, accreditation within that jurisdiction, and the mechanisms by which they may receive and record enforcement actions.

## Motivation

Smart contracts are, in essence, digital agreements whose execution is enforced by network consensus. As their use increasingly expands into domains that mirror real-world legal or institutional relationships, one critical component present in traditional systems is missing on-chain: a structured way to express sovereignty, jurisdiction, accreditation, and enforcement.

Historically, much of the smart-contract ecosystem has emphasized decentralization and self-sovereignty, implicitly assuming that contracts do not rely on any external legal or institutional framework. However, many practical use cases—especially those that interface with real-world regulations, property rights, or compliance regimes—require an explicit identification of the jurisdiction(s) a contract observes, the authority that has accredited it as a valid actor within that jurisdiction, and the mechanisms by which binding decisions may be communicated to it.

This ERC proposes a standardized interface for representing four foundational concepts:

- Sovereignty — whether a contract is self-sovereign or claims allegiance to a higher-order system;
- Jurisdiction — which external authority it chooses to observe;
- Accreditation — whether that authority formally recognizes the contract as a valid participant within its system; and
- Enforcement — how decisions, rulings, or binding actions issued by that authority can be delivered to and acknowledged by the contract.

In many real-world and institutional settings, an entity becomes an actionable participant only after receiving formal accreditation by the relevant authority—whether this is a state chartering a corporation, a school recognizing a student club, a platform onboarding a developer, or a DAO admitting a module into its governance structure. Conversely, some entities explicitly declare their absence of external jurisdictional alignment, operating instead as sovereign actors such as declaration of independence as newly established countries gain their sovereignty, or joining a jurisdictional system as a newly established entity. Representing both modes—subordination and self-sovereignty—is essential for accurately modeling institutional relationships on-chain.

By standardizing how smart contracts declare sovereignty, jurisdiction, accreditation, and enforcement pathways, this ERC enables interoperability between legal systems, regulatory frameworks, institutional hierarchies, and on-chain governance models—bridging a structural gap between real-world systems and their digital counterparts.

### Use Cases (Primary)

The primary use cases address the questions related to the status of a contract themselves.

- Stablecoins (e.g., USDC): Require jurisdiction because reserve custody, redemptions, freezes, and regulatory compliance depend on a specific legal authority.
- Tokenized Stocks / RWAs: Require jurisdiction because securities laws, transfer restrictions, investor rights, and enforcement vary entirely by legal venue.
- Regulated Lending Protocols: Require jurisdiction to define collateral rights, default resolution, licensing requirements, and enforceability of loan agreements.
- Private Company Equity for Qualified Investors: Require jurisdiction to enforce accreditation rules, transfer limits, corporate law, and cap-table validity.

### Use Cases (Secondary)

The secondary use cases address the questions related to the interactions between contracts.

- Jurisdiction Compatibility Checks: Ensuring that interacting contracts operate under compatible or acceptable jurisdictions.
- Regulatory Boundary Enforcement: Gateways, bridges, or marketplaces can restrict integration to contracts meeting specific jurisdictional or accreditation requirements.
- Good-Standing Verification: Validating whether a contract is accredited and in compliance under its declared jurisdiction.
- Jurisdiction-Based Access Control: Allowing or restricting participation based on jurisdiction or accreditation metadata.
- Cross-Contract Legal Cohesion: Ensuring coherent jurisdictional alignment across multi-contract systems, federated DAOs, or hierarchical governance structures.
- Automated Dispute-Path Selection: Determining which arbitration venue, legal process, or enforcement route applies when disputes ar

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

A contract compliant with this ERC MUST implement the interface defined below.

The interface provides standardized primitives for declaring a contract’s accreditation source, its observed jurisdiction, and a mechanism for receiving structured enforcement proposals. When the jurisdiction is absent, a contract is self-sovereign.

### 1. Data Structures

For backward compatibility with existing contracts that implement

ERC-5247, the interface extends

the `IERC5247Executable` and `IERC5247Executables` data structures.

#### IERC5247Executable

Represents a single action that MAY be proposed as part of an enforcement submission.

This structure follows a generic “executable call” pattern: a target address, an optional ETH value, a gas limit, and calldata for invocation.

No guarantees are made regarding execution; implementations MAY ignore or reinterpret these fields.

```solidity
/// @notice A single executable action that MAY be proposed as part of an enforcement.
struct IERC5247Executable {
    /// @notice The target address to be called if this executable is processed.
    address target;

    /// @notice The amount of ETH (in wei) to send along with the call to `target`.
    uint256 value;

    /// @notice The gas limit for the call. Implementations MAY ignore this field.
    uint256 gasLimit;

    /// @notice The calldata to send to `target`.
    bytes data;
}
```

#### IERC5247Executables

A batch of `IERC5247Executable` items representing an ordered enforcement proposal.

```solidity
/// @notice A batch of executable actions forming an enforcement proposal.
struct IERC5247Executables {
    /// @notice Ordered list of executable actions included in this proposal.
    IERC5247Executable[] executables;
}
```

### 2. Interface

#### sourceOfAccreditation()

Returns the address that accredited this contract as a valid participant within some jurisdiction or governance system.

- MUST return the accrediting authority’s address if one exists.
- MUST return address(0) if the contract does not recognize any external accreditation source (e.g., self-sovereign behavior).
- SHOULD remain stable over the contract’s lifetime or change only through a defined governance or upgrade mechanism.

#### jurisdiction()

Returns the primary jurisdiction or system whose rules this contract claims to observe.

- MAY return the same address as sourceOfAccreditation() when a single contract performs both roles.
- MUST return address(0) if the contract claims no external jurisdiction.
- Represents the higher-order system the contract aligns with, independently of accreditation.

#### imposeEnforcement(IERC5247Executables _proposal)

A standardized entry point for submitting an enforcement proposal to the contract.

- Implementations MUST define and document the access control for this function (e.g., restricted to jurisdiction(), sourceOfAccreditation(), or a curated authority list).
- Implementations MAY:

immediately execute some or all proposed actions,
- record the proposal for later deliberation,
- partially honor or completely ignore the proposal based on policy.

Implementations SHOULD emit events or persist state enabling verifiable on-chain acknowledgment that an enforcement attempt occurred.

The function is payable to allow ETH to accompany proposals when executables specify non-zero `value` or when processing fees apply.

### Full Interface

```solidity
interface IERC5485 {
    /// @notice Returns the address that accredited this contract, if any.
    /// @dev MUST return address(0) if the contract does not recognize
    ///      an external accreditation source. SHOULD remain stable or change
    ///      only via defined governance.
    function sourceOfAccreditation() external view returns (address);

    /// @notice Returns the jurisdiction or higher-order system this contract
    ///      observes.
    /// @dev MAY be the same as `sourceOfAccreditation()`. MUST return address(0)
    ///      when the contract claims no external jurisdiction (self-sovereign
    ///      behavior). SHOULD remain stable or change only via defined governance.
    function jurisdiction() external view returns (address);

    /// @notice Submits an enforcement proposal to this contract.
    /// @dev Implementations MUST define access control. Implementations MAY execute,
    ///      schedule, partially honor, reject, or only record `_proposal`.
    /// @dev Implementations SHOULD emit events or store state acknowledging receipt of
    ///      enforcement proposals. Payable to allow ETH forwarding for executables that
    ///      specify non-zero value.
    function imposeEnforcement(IERC5247Executables _proposal) external payable;
}
```

## Rationale

### Separation of Jurisdiction and Accreditation

This ERC separates **jurisdiction** from **accreditation** because

they represent fundamentally different relationships:

- Jurisdiction is voluntary.
A contract may unilaterally declare that it observes the rules or
norms of a particular system.
- Accreditation requires external approval.
Only the authority itself can grant formal recognition that a contract
is an accepted participant within its system.
- Jurisdiction expresses alignment; accreditation expresses acceptance.
Declaring jurisdiction does not imply the authority recognizes the contract.
Accreditation establishes the reciprocal relationship.
- Accreditation enables enforcement.
Authorities typically issue enforcement only to contracts they have
accredited. Jurisdiction alone does not create this binding pathway.

Keeping these concepts distinct reflects how real-world institutions work:

observing a system’s rules is self-declared, but gaining formal standing

within that system requires an explicit action by the authority. This

distinction ensures more accurate modeling of institutional relationships

on-chain.

## Backwards Compatibility

1. The absence of accreditation and jurisdiction is backward compatible with
existing contracts, as it is a superset of the existing behavior. More
explicitly, a contract that does not implement this interface observes no
jurisdiction, by default showing no accreditation and is considered
self-sovereign.
2. Using ERC-5247 as a base interface for enforcement proposals is backward
compatible with existing contracts that implement ERC-5247, such as Multi-Sig
wallets such as treasury of a DAO.

## Security Considerations

Similar to a real world scenario, when observing a jurisdiction

practically gives the contract the ability to enforce rules on the

contract’s behavior. Simlar to “Ownable” (ERC-173) or “AccessControl”,

implementations MUST be aware of the security implications of this: the

security of a contract is compromised if the jurisdiction is compromised.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**sbacha** (2022-08-21):

this is obviously a government psyop, this EIP is not even coherent and should be rejected until an actual specification is met.

Also your title is intentionally inflammatory.

---

**davidc** (2022-08-23):

This is interesting but definitely has to be thought through more. I’m not sure if it’s appropriate for a contract that another gains legitimacy from to be able to issue a selfdestruct.

---

**jademckinley08** (2022-09-13):

Great Stuff, thanks for sharing the information

---

**xinbenlv** (2022-09-28):

selfdestruct is an example of the “most powerful thing” an account (contract) can do onto another account (contract). we can definitely consider other way to mandate. Basically, under jurisdiction means the agreement to obey rules of the jurisdiction and be panelized when not.

---

**xinbenlv** (2025-12-01):

Hi friends who are following ERC-5485’s development, a new version of draft has dropped!

---

**radek** (2025-12-01):

Honestly I cannot imagine interoperability among smart contracts if they needed to take into consideration outputs of such interface.

Wrt design itself - there are more jurisdictions than one - E.g. in EU - in many cases you have both EU level and a national (country) level.  I guess there will be similar cases in US (Federal vs Delaware) and other larger regions.

---

**xinbenlv** (2025-12-02):

Thank you [@radek](/u/radek) for the feedback.

# 1 Interoperability

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> Honestly I cannot imagine interoperability among smart contracts if they needed to take into consideration outputs of such interface.

There are many cases I can think of. Here is one

1. In US, only a qualified investor QI can invest in a company C when QI has proper accreditation such as  QI being a FINRA memeber. They can leverage ERC-5485 to attest the following

a. `C` is a Delaware company, meaning they observe State of Delaware as `jurisdiction()` will return an address representing The Court of State of Delaware, and they are organized in Delaware meaning they will be accredited by the State Department of Delaware. `sourceOfAccreditation()` will return an address of State Department of Delaware. And as you go to State Department of Delaware you will be able to call `hasAccredited()`

TODO add interfaces for `hasAccredited(bytes32 typeOfAccreditation, address entity)` etc.

b. `QI` is a accredited investor accredited by FINRA, they will be able to call `sourceOfAccreditation()` and get an address of FINRA and then call that address with `hasAccredited()` to validate the membership of QI in FINRA.

In this case

When the contract of `QI`’s treasury wants to a investment - in the format of a swap of ERC-20 representing `C`’s equity vs the stablecoins they invest, such `C` will check if `QI` is a member of FINRA - by checking hasAccreditation before proceed. And if `QI`’s own governance require QI to only invest in companies that observes Delaware jurisdition, they can put such check logic that in this swap too.

# 2 Concurrent Jurisdiction

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> Wrt design itself - there are more jurisdictions than one - E.g. in EU - in many cases you have both EU level and a national (country) level. I guess there will be similar cases in US (Federal vs Delaware) and other larger regions.

Indeed multi/concurrent-jurisdiction is a design question we have to face. For simplicity now we are observing only a single jurisdiction like all contracts. In Delaware, the Delaware is a directly observed jurisdiction, and US Federal is a inferred jurisdiction because Delaware observes US Federal as a jurisdiction. Same for countries in EU etc. I can’t think of any countries or states that doesn’t have this kind of tree/single parent relationship when there is an indirect jurisdiction.

That said, I can also think of other kinds of jurisdiction relationships for example a pre-declared forum of arbitration. If more people hope we support concurrent jurisdiction, we will update accordingly.

---

**xinbenlv** (2025-12-08):

A question from [@fulldecent](/u/fulldecent) off Ethereum Magician, let me post it here.

> Thanks for sharing. What I don’t understand right now is how a smart contract itself is able to make declarations. A smart contract itself is not a person under law, and therefore it does not have a jurisdiction or legal enforceability. So really instead declaration is made by an individual (owner of the contract) and the subject of the declaration is the smart contract. In other words, the owner badges the contract.

Answer: Smart contracts, like paper contracts, don’t make declarations themselves. The people or entities who write and sign the smart contract make the declarations.

For example, when a company is formed, its shareholders write and sign a bylaw in which they (the shareholders), through the company, make declarations such as “we together (this company) observe the jurisdiction of Delaware.”

Likewise, when two companies form a contract, they establish a contractual agreement and relationship in which the two companies write and sign a contract that declares a jurisdiction.

> Or the reverse like you have said if the government is going to recognize something Then that is a badge, bestowed by government. Not asserted by the smart contract itself.

Government bestows recognition on a company by allowing it to register. Government by default bestows recognition on a contract if it is physically signed within its territory or sometimes by entities domicile in its territory. In fact, a court could simply decline jurisdiction. [Marbury v. Madison](https://zh.wikipedia.org/wiki/%E9%A9%AC%E4%BC%AF%E5%88%A9%E8%AF%89%E9%BA%A6%E8%BF%AA%E9%80%8A%E6%A1%88) was one of the example that declined jurisdiction of some agreement.

Historically, governments had to pass a charter to formally recognize a company.

- In UK, until Joint Stock Companies Act 1844, which means the UK government relaxes its process of recognizing a company off the burden of a parliament bill.
- Like-wise, in United States. Before 1811, forming a corporation required a special legislative charter; after the 1811 New York general incorporation act, eligible businesses could incorporate simply by meeting statutory requirements and registering, without needing legislative approval.

In some countries, certain types of contracts still need to be bestowed (notarized, as one form) or registered in order to be recognized:

Security interests (like pledges or mortgages) often require formal registration. Many countries require registration in a public registry for the security interest to be effective against third parties.

*What I agree with you is*: such badge should be a badge bestowed by ~~government~~ its Source of Accreditation

---

**xinbenlv** (2025-12-08):

Here are a few pieces of feedback collected by Chase from industry contributors

> Feedback 1: Heyy went through the EIP - I think it’s a pretty strong foundation but there are likely some edge cases and considerations that needs to be solved for. The main thing is on the multi-jurisdiction oversight: What happens for contracts that subscribes to multiple jurisdictions? Do you need to fork the smart contract and then add different addresses to represent another jurisdiction? And then how does those 2 contacts speak to each other when an action is taken against 1.:

The first feedback was also about multi-jurisdiction or concurrent jurisdiction. This is a good question and I addressed in [my reply]([ERC-5485: Interface for Legitimacy, Jurisdiction and Sovereignty - #8 by xinbenlv](https://ethereum-magicians.org/t/erc-5485-interface-for-legitimacy-jurisdiction-and-sovereignty/10425/8)

I also want to point out that when multiple jurisdictions issue conflicting decisions, it becomes a real problem—that’s when things break down and jurisdictions effectively start fighting each other. The good news is that if we simplify the model so that each contract recognizes only one jurisdiction, and that jurisdiction in turn recognizes its own superior jurisdiction, we can still mimic most real-world governance structures.

> Feedback 2: having a public registry interface for the governmant, to observe, not all knows how to use etherscan

This is a good suggestion, but it falls outside the scope of this ERC.

Just like ERC-20 does not specify where a token should be registered, in practice different wallets and exchanges each maintain their own registries. The ERC-20 standard itself does not include any requirement for such a registry.

The same applies here: a public registry could absolutely be built, but it should be implemented at the application layer rather than inside the ERC standard.

> Feedback 3: we need to try some large asset first, for example, debts, which has a time lock, automated cash flows etc…

Yeah, adoption is the key. Starting with large assets would be great, but it’s a chicken-and-egg problem—both tools and assets need to adopt the standard before it creates real value.

That’s why we want a broad group of early adopters participating in the committee, so the ecosystem can develop in parallel on both sides.

---

**fulldecent** (2026-01-04):

The point of jurisdiction in a contract is that the parties agree on a quick way to end private controversy in all places EXCEPT the one specified in the contract.

It will be helpful if this ERC can spell out some specific kinds of controversy that are enforceable under courts and which this ERC will help. And then in further detail, this thread to mention specific course cases where this ERC would help.

