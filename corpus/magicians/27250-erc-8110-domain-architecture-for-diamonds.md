---
source: magicians
topic_id: 27250
title: "ERC-8110: Domain Architecture for Diamonds"
author: Vagabond
date: "2025-12-20"
category: ERCs
tags: [diamond]
url: https://ethereum-magicians.org/t/erc-8110-domain-architecture-for-diamonds/27250
views: 303
likes: 21
posts_count: 16
---

# ERC-8110: Domain Architecture for Diamonds

## Introduction

This proposal introduces a domain-based architectural pattern for Diamond

contracts.

In this context, a `domain` represents logical ownership of storage and

responsibility inside a Diamond, following common software architecture

practices.

The core idea is to treat storage as something owned by clearly defined

domains, while facets act as logic interfaces that read or modify that storage.

## Abstract

This EIP introduces a **domain-based architectural pattern** for contracts implementing the Diamond execution model defined by ERC-2535 (Diamond Standard) or

ERC-8109 (Diamond, Simplified), together with the storage identifier mechanism defined by ERC-8042 (Diamond Storage Identifier).

It defines a consistent naming convention for storage identifiers and a directory organization model that **decouples storage management from facet logic**.

This pattern helps reduce storage collisions and human error while enabling better tooling for multi-facet systems.

## Thoughts & Feedback

Any kind of feedback would be appreciated, especially from real-world Diamond implementations.

---

I’m currently refining this ERC based on feedback.

For the latest version, please refer to the draft [here](https://eips.ethereum.org/EIPS/eip-8110).

Ongoing refinements are tracked via PRs [here](https://github.com/ethereum/ERCs/pull/1453).

## Replies

**mudgen** (2025-12-20):

I think this is great!

---

**Vagabond** (2025-12-20):

Thank you! I’m glad you find it helpful.

---

**mihaic195** (2025-12-24):

Hey [@Vagabond](/u/vagabond),

I’m happy someone picked up on the idea that I had [here](https://ethereum-magicians.org/t/erc-8042-diamond-storage/25718/14) in the [ERC-8042: Diamond Storage](https://ethereum-magicians.org/t/erc-8042-diamond-storage) discussion.

I think formalizing this as an architectural pattern makes sense, and I like the direction! I have a few remarks:

1. For clarity and tooling: identifiers MUST be valid ERC-8042 identifiers, and domains MUST declare them via the ERC-8042 NatSpec tag (@custom:storage-location erc8042:) so tooling can reliably discover them. This avoids the need to restate validation rules.
2. On “exactly one storage struct”: it may help to spell this as “one domain maps to one storage slot and one root storage struct.” The root struct MAY contain nested structs/enums/mappings. The key is that the storage entrypoint (slot) is singular per domain.
3. Collisions: Maybe it’s worth emphasizing that collisions matter only when multiple logic modules share the same storage context (e.g., Diamonds/proxies via DELEGATECALL). This prevents newcomers from overgeneralizing collision risk.
4. Naming: to align better with DDD-style organization, consider replacing domain_type with context (inspired by bounded contexts).

{org}.{project}.{context}.{domain_name}.{version}
5. e.g. org.project.access.pausable.v2

What do you think?

---

**Vagabond** (2025-12-25):

Hi [@mihaic195](/u/mihaic195)

Thank you for your input.

My main goal with this proposal is to describe a proper architectural approach for Diamond systems, emphasizing separation of concerns and drawing selective inspiration from DDD.

The focus is on **how to organize a project** so that logic can be split into smaller, well-defined blocks that scale naturally over time, and remain easy to understand, test, and audit as the system evolves.

Regarding your specific points:

> For clarity and tooling: identifiers MUST be valid ERC-8042 identifiers, and domains MUST declare them via the ERC-8042 NatSpec tag (@custom:storage-location erc8042:) so tooling can reliably discover them. This avoids the need to restate validation rules.

Yes, I agree this is a good idea and aligns well with existing tooling. I will update the spec accordingly.

> On “exactly one storage struct”: it may help to spell this as “one domain maps to one storage slot and one root storage struct.” The root struct MAY contain nested structs/enums/mappings. The key is that the storage entrypoint (slot) is singular per domain.

For enums and mappings (including cases like mapping => struct), I agree these are generally safe and natural to use within a storage struct.

For nested structs used directly as fields, there are tradeoffs:

- Technically, inner structs become difficult to evolve, as they cannot be safely extended once deployed.
- Architecturally, this blurs separation of concerns by grouping multiple responsibilities into a single domain.

For these reasons, I think it is preferable to place variables directly in the storage struct, or to define a well-scoped domain with its own storage identifier.

> Collisions: Maybe it’s worth emphasizing that collisions matter only when multiple logic modules share the same storage context (e.g., Diamonds/proxies via DELEGATECALL). This prevents newcomers from overgeneralizing collision risk.

I agree that it is helpful to clarify this.

In practice, storage collisions typically arise from:

- Reusing the same identifier for storage structs with different layouts.
- Modifying variable order or inserting variables in the middle of a storage struct across upgrades (layout-breaking changes).
- Declaring and using state variables directly in facets, including variables originating from libraries, inheritance or shared free variables.

Functions or modules themselves do not directly cause collisions. Collisions stem from how storage is declared and evolved.

Storage collisions are problematic because they can silently mutate storage without triggering immediate failures. For this reason, collision avoidance is treated as a primary architectural concern.

> Naming: to align better with DDD-style organization, consider replacing domain_type with context (inspired by bounded contexts).

I did consider the term `context`, but decided against it, as it can be ambiguous in a smart contract setting where “context” is often associated with runtime data such as msg.sender or msg.data. The term `domain` is intended to emphasize ownership and lifecycle of persistent storage.

I believe the term `domain_type` is sufficiently self-descriptive and conveys its intended meaning clearly.

What do you think?

---

**mudgen** (2025-12-30):

I read this again. I agree with the general idea of separating the domains/storage from facets.

I like the flexibility and guidance the standard provides.

---

**mudgen** (2025-12-30):

I suggest making the name of the standard:  “Domain Architecture for Diamonds”.  I think that reads a bit better.

---

**Vagabond** (2025-12-31):

Thanks for the suggestion, I’ve updated the title to “Domain Architecture for Diamonds.”

---

**mudgen** (2026-01-02):

I think that this standard is a good guide for projects to determine the structure of their storage and application directory layout.

I also think that standards and libraries can determine some of the struct definitions and their storage identifiers. For example I am interested in making a new standard that specifically specifies the struct and storage identifier for diamonds, ERC20, ERC721 and other standards.  For example the standard storage identifier for diamonds might be `erc8109.diamonds` and the standard identifier for ERC20 token transfer functionality might be `erc20.transfer`. Standardizing the storage structs and their locations for standard functionality can promote interoperability and composition of functionality between projects and libraries.

Because of this, I don’t think that the example storage identifiers for diamonds, allowance and pausable in this standard are good examples because these identifiers are likely to be standardized by libraries and/or ERC standards.

I suggest finding or creating application specific examples – things not likely to be standardized by libraries or standards. Perhaps looking at some existing diamond-based smart contract systems can give some ideas. Here is a list of some diamond-based systems that could be looked at:

- ZKsync
- Li.Fi
- Aavegotchi
- Trust Wallet
- Towns Protocol
- Boson Protocol
- Stobox
- Venus Protocol

---

**Vagabond** (2026-01-02):

You’re absolutely right, my examples were not clear enough.

I think it’s important to clarify that this standard is primarily about **how application developers organize their project structure, storage, and application logic**, rather than defining canonical identifiers for libraries, frameworks, or other standards.

Identifiers for standardized functionality (e.g. ERCs or common libraries) are likely better defined by dedicated standards or libraries themselves.

I really appreciate the feedback, thank you for pointing this out.

---

**0xvimer** (2026-01-03):

Thanks for sharing this ERC. Could you clarify how the proposed domain architecture interacts with existing library or ERC standards for storage identifiers? For example, would projects need to rename existing domain structures to adopt ERC-8110? Additionally, how does this standard handle upgrades when new facets are added to a diamond?

Looking forward to your insights!

---

**Vagabond** (2026-01-04):

Hi [@0xvimer](/u/0xvimer)

Thanks for the thoughtful questions!

> how the proposed domain architecture interacts with existing library or ERC standards for storage identifiers?

**About existing libraries or ERC standards:**

ERC-8110 does **not** ask projects to modify, rename, or refactor existing libraries or other ERC standards in order to adopt it.

If a library or standard already follows ERC-2535, ERC-8042, or uses its own established storage identifiers, that code should remain unchanged.

ERC-8110 is intended as an **architectural guideline at the project (application) level**.

It focuses on how a project organizes its own domains, storage ownership, and directory structure, rather than redefining or interfering with shared libraries or standardized components.

> For example, would projects need to rename existing domain structures to adopt ERC-8110?

**For projects that want to adopt ERC-8110:**

Adoption is optional and can be done incrementally.

In most cases, the easiest way to start is at the **application layer**, without touching shared libraries or standardized components.

In practice, teams usually begin by:

- Defining clear domain boundaries
- Organizing directories around domain responsibility
- Grouping facets and their related storage by domain
- Explicitly declaring storage ownership using the ERC-8042 @custom:storage-location annotation

Existing storage identifiers can be treated conceptually as **pre-v1** domains.

Later on, if you need a layout-breaking change or a data migration, you can introduce a new, well-defined versioned identifier (for example `v1`) explicitly, without having to rename or rewrite past identifiers.

**The only thing to be careful about is identifier uniqueness**:

just make sure any new storage identifier you introduce does not duplicate an existing one from either shared libraries or your own project.

---

**Vagabond** (2026-01-04):

> Additionally, how does this standard handle upgrades when new facets are added to a diamond?

**Regarding upgrades and new facets**

Under ERC-8110, upgrade behavior depends on **what the functions inside a facet require**, rather than on the facet itself.

**Case 1: No new storage variables required**

If a facet does **not contain any functions that require new storage variables**:

- The facet can be placed under the appropriate existing domain.
- A regular upgrade is sufficient.
- No storage changes are required.

This is the simplest and safest upgrade path.

**Case 2: Functions introduce a new domain (horizontal upgrade)**

If a facet contains functions that require state which **does not logically belong to any existing domain**:

- This is treated as a horizontal upgrade.
- A new domain must be defined, including:

A dedicated directory
- A new ERC-8042 storage identifier
- A new storage layout

The facet is placed under that domain and added as part of the upgrade.

This allows new features to be introduced without impacting existing domains or storage layouts.

**Case 3: Layout-breaking storage changes**

If a facet contains functions that require a **layout-breaking change** to an existing domain’s storage

*(for example: changing the inner struct of nested structs or struct arrays)*:

- A new, versioned storage identifier must be introduced (for example v2).
- A new storage layout is defined under that identifier.
- Any required data migration must be handled explicitly by the project.

ERC-8110 does not attempt to automate or abstract storage migrations.

The goal is to keep schema changes intentional, visible, and auditable.

**Case 4: New variables added to an existing domain (vertical upgrade)**

If a facet contains functions that require **additional variables** which can be safely appended to the end of an existing storage layout (no layout break), this becomes a design trade-off.

There are two possible approaches, depending on the project and the team:

**Option A — Evolve the existing domain**

- Append new variables to the end of the existing storage struct.
- Add the new facet and selectors.
- This keeps the domain unified and works well for complex or tightly coupled business logic.
- It requires developers to carefully follow storage layout rules.

This approach allows the storage struct to evolve natively together with the domain boundary, preserving a single, cohesive domain over time.

**Option B — Split into a sub-domain**

- Treat the new functionality as a sub-domain of the existing domain.
- If the main domain uses the minimal identifier format:
{project}.{domain}.{version}
- The sub-domain can be defined as:
{project}.{domain}.{version}.{sub-domain}
- The sub-domain storage should contain only the new variables introduced by the new functions, leaving the original domain layout untouched.

This approach is safer and reduces cognitive load, since it avoids relying on strict append-only discipline for the original storage layout.

The trade-off is additional domain entries and higher maintenance overhead.

- This approach can be considered when a layout-breaking change (Case 3) is partial and can be cleanly isolated from the original domain.

Which option to choose depends on the project’s complexity, the team’s discipline, and long-term maintenance goals.

---

**Vagabond** (2026-01-06):

Hey [@mudgen](/u/mudgen), [@0xvimer](/u/0xvimer), [@mihaic195](/u/mihaic195)

I’ve updated the standard based on our discussion.

Would appreciate your thoughts when you have time.

---

**mudgen** (2026-01-07):

[@Vagabond](/u/vagabond) The examples look great.

---

**Vagabond** (2026-01-08):

Thank you for your feedback.

