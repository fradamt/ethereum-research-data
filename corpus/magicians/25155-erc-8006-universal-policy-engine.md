---
source: magicians
topic_id: 25155
title: "ERC-8006: Universal Policy Engine"
author: vitali_grabovski
date: "2025-08-19"
category: ERCs
tags: [erc, compliance, policy, rule, policy-engine]
url: https://ethereum-magicians.org/t/erc-8006-universal-policy-engine/25155
views: 602
likes: 30
posts_count: 9
---

# ERC-8006: Universal Policy Engine

[ERC-8006](https://github.com/GuardianLabs/ERCs/blob/universal-policy-engine/ERCS/erc-8006.md)

DApps keep re-implementing ad-hoc validation and compliance rules (roles, kyc, allowlists, limits, workflows, and other legally required validatons). It’s brittle to upgrade, hard to audit, and not reusable across projects.This ERC standardizes a **Universal Policy Engine**:

1. Each rule is packaged in small contract called artifact
2. Each artifact contract can be reused by other policies and has to expose minimal interface (init, exec) and self-descriptors
3. A policy handler bundles/orchestrates them as a Directed Acyclic Graph so apps can compose complex policies from simple building blocks and update them incrementally (swap/append artifacts instead of redeploying app logic)
4. All parameters flow as bytes for uniform on/off-chain integration; variables can be introspected for tooling.

It’s universal by design – applicable across data domains and attachable to any contract as method-level hooks (pre/post) to gate calls and chain validations. Reference implementation in [ERC assets](https://github.com/GuardianLabs/ERCs/tree/universal-policy-engine/assets/erc-8006/contracts).

**General and simplified yet precise view of how it works**

[![simple_policy_bird_eye_view 2](https://ethereum-magicians.org/uploads/default/optimized/2X/4/44ec70a8db64be9830a64a6546a655c73707a844_2_297x500.jpeg)simple_policy_bird_eye_view 21920×3223 238 KB](https://ethereum-magicians.org/uploads/default/44ec70a8db64be9830a64a6546a655c73707a844)

ERC Authors list:

[@Vlad](https://ethereum-magicians.org/u/vpriadko), [@Vitali](https://ethereum-magicians.org/u/vitali_grabovski)

## Replies

**DoroshinAnton** (2025-08-21):

An excellent story for gamification processes. You can build custom complex systems resembling MPORG, conditionally WoW. Artifacts can be ers721/1155, and their improvements are coordinated by high-level policies (for example, physics from Oracle). I like your approach. Thank you.

Sorry for my English, translated from Russian.

---

**DoroshinAnton** (2025-08-21):

The mechanic looks particularly interesting for social DAOs, where actors/delegates/conditional guilds or factions can be endowed with a life cycle through artifacts and, for example, have “research trees.” But for such a system, a certain general primitive of Web3 generation experience must be built up, accessible to all interested parties. It is only necessary to take into account sibyl scams (for example, using a quadratic approach when improving levels), BUT then all these Leyer3, Galaxies, and other systems can be brought to conditional common denominators through policies.

---

**vpriadko** (2025-08-26):

Hey, thanks for your interest!

1. Yep, improvements/role escalations (or any other action) can be constrained by policies
2. The artifacts themselves though are not originally intended to be tokens, cause the “fungibleness” is not the same here as “interoperability” and “reusability” in this case. It is rather a reverse story, policy and its artifacts can constrain erc20, erc721’s transfer method (or other hook, whatever)
3. So, artifacts can be reused, and they not obligatory should be token-like (while technically it’s possible). The only obligation for artfact is to implement IArbitraryDataArtifact interface

---

**vpriadko** (2025-08-29):

Hey! I think there’s a small misunderstanding — ‘artifacts’ here aren’t ‘game artifacts.’

The term ‘artifact’ is used in the sense of ‘a unit intended for a specific function,’ not as ‘a unique collectible item.’ These are just functional components — like addition, subtraction, price queries, etc. So they don’t have much in common with NFTs or other game-fi artifacts.

Regarding DAO policies — while they’re not typically used to store data, I do get your point about what you were aiming to achieve with them!

You can absolutely design a policy system that evaluates a participant’s *current* level using some standardized inputs. Of course, the evaluation strategy can be arbitrary — say, a quadratic model. In that case, the policy effectively becomes an authorization guard.

---

**denniswon** (2025-11-10):

Great observation — and excellent work on ERC-8006.

The [Newton Protocol](https://newt.foundation) is tackling a very similar challenge, but from a complementary angle. In Newton, policy evaluation occurs off-chain through a decentralized network of **Newton Operators**, each capable of verifying rules against **verifiable data sources** (via MPC, TEE, and ZK-based proofs). The result of each policy evaluation produces an **on-chain Proof-of-Compliance**, emitted as a verifiable by-product of the network’s consensus process.

This architecture aims to make compliance and rule enforcement composable, verifiable, and chain-agnostic — allowing developers to plug in any policy engine or attach proofs directly to transactions or intents.

I’d love to hear your thoughts on potential alignment between ERC-8006 and Newton’s approach, and explore whether our initiatives could converge or interoperate. It seems like there’s strong synergy between ERC-8006’s on-chain modularity and Newton’s off-chain verifiability layer.

Looking forward to continuing the conversation.

---

**vitali_grabovski** (2025-11-11):

Hi Dennis, and thank you!

I’m gonna deep dive into the litepaper – the on-chain policy engine is a rare thing, and I think we and any other policy builder should learn from each other and discuss this topic endlessly, especially if it’s open source.

---

Regarding privacy (or onchain verificaion): any logic that can be coded as a smart contract can be converted to a policy artifact. I just need to find time to create an example using verifiable credentials – the same standard that Privado.id is built on top. This should give zero friction and work smoothly. like a clockwork.

__

[@denniswon](/u/denniswon) Do you have any specific questions about the standard?

---

**HenryRoo** (2025-12-02):

If you have could you share your estimates of how using ERC-8006 affects the `gasUsed` of a typical transaction compared to an equivalent inline implementation of the same checks using regular `require` statements/modifiers?

For GameFi (or MMO RPG mentioned above) or high-frequency trading scenarios on DEXes, even a small increase in `gasUsed` per operation (on the order of a few thousand gas) can significantly impact unit economics/revenue, especially for dApps on L1.

Am I correct in understanding that, in exchange for reducing complexity and risks when updating compliance logic (by outsourcing it to a universal Policy Handler and artifacts), we effectively shift additional `gasUsed` overhead onto each user transaction?

Do you have any benchmarks or profiling results for the reference implementation (for example, for policies with 3 to 5 artifacts in the DAG) that you could share? And do you consider this overhead acceptable for high-throughput scenarios?

---

**mudgen** (2025-12-14):

Hi [@vitali_grabovski](/u/vitali_grabovski),

I reviewed ERC-8006.

I like the structure and flexibility this standard provides for sets of compliance rules.

I was enlightened by your All-Bytes approach in `IArbitraryDataArtifact`. I really like the flexibility that provides.

I had the thought that perhaps an `function artifactURI() external pure returns (string memory desc);`  function could be useful in `IArbitraryDataArtifact`.

This function could return a URI, such as a URL to additional information and documentation about an artifact. This is in case the description is not enough.  If the description is already enough then ` artifactURI()` could just return an empty string.  But I am not familiar enough with artifacts in reality to know if a `artifactURI()` function would be useful enough to add.

