---
source: magicians
topic_id: 21195
title: "EIP-7773: Glamsterdam Network Upgrade Meta Thread"
author: timbeiko
date: "2024-09-26"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/eip-7773-glamsterdam-network-upgrade-meta-thread/21195
views: 2372
likes: 25
posts_count: 14
---

# EIP-7773: Glamsterdam Network Upgrade Meta Thread

## Glamsterdam Scoping Timeline

*updated July 15, 2025*

Following my [recent post](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088), here is how I propose we approach Glamsterdam scoping:

1. [May 26 - June 20] Fork Focus Discussion & Headliner Proposals

During this period, ACD{E|C} calls should focus on discussing Glamsterdam’s high-level goals. Headliner champions should be invited to present their proposals.
2. Headliner champions must open an Ethereum Magicians thread with the glamsterdam tag at least 48 hours before the ACD call on which they wish to present, including relevant information about their proposal (see template below).

Note: While technical readiness is a factor, an EIP is not required at this stage. For instance, a proposal focusing on “reducing disk requirements for nodes” is acceptable even without a specific EIP.
3. The June 19th ACDE call will be the final opportunity to propose new candidate headliners, making June 17th the deadline to share new proposals on Ethereum Magicians.
4. This period should evaluate not only Core Dev preferences for the next upgrade but also broader community preferences. While ACD can provide feedback around which stakeholders should be consulted, headliner champions are responsible for gathering sufficient evidence of support.
5. [July 17 - Aug 21] Headliner Discussion & Finalization

Once candidate headliners are identified, ACD will spend the next month evaluating them, soliciting community feedback, and finalizing decisions on which feature(s) to prioritize for Glamsterdam.
6. The ACD calls from July 31 to August 21 will be used to decide on the fork headliner(s)
7. Client team preferences:

Lighthouse
8. Reth
9. Geth
10. Prysm
11. Once we’ve settled on a headliner, the Glamsterdam Meta EIP should be updated to reflect it and articulate the rationale for the choice.
12. [Oct 30] Non-Headliner EIP Proposals

With the headliner Scheduled for Inclusion, ACD should begin reviewing other EIPs Proposed for Inclusion in Glamsterdam.
13. Like for Fusaka, EIP authors proposing their EIP should submit a PR against the Glamsterdam Meta EIP, following the process detailed in EIP-7723.
14. The deadline for EIPs being PFI’d for Glamsterdam will be when mainnet client releases for the Fusaka upgrade are announced.
15. [Date TBD] Non-Headliner EIP CFI Decisions

After the EIP proposal deadline, use the ACDC and ACDE calls to select which Proposed for Inclusion EIPs should advance to Considered for Inclusion. Remaining PFI EIPs will be Declined for Inclusion.
16. [Date TBD] CFI → SFI EIP Decisions

As Glamsterdam devnets begin, make final decisions regarding which CFI EIPs will be included in the upgrade’s devnet.

---

** Headliner Proposal Template**

### Headliner Proposal Template

While EIPs and Python specifications effectively describe a proposal’s technical details, they aren’t best suited to explain **why** a network upgrade should prioritize a specific proposal or its impact on the entire Ethereum community.

To address this, headliner champions should use the following template in their Ethereum Magicians threads to clearly articulate the proposal’s goals, impacts, risks, and readiness.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)[Community Consensus, Fork Headliners & ACD Working Groups](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088/1)

> Summary (ELI5): Concise, plain-language explanation of the proposal, why it matters, and who directly benefits.
>
>
>
>
> Detailed Justification:
>
>
>
>
> What primary and secondary benefits exist, ideally supported by data or clear rationale?
>
>
>
>
> Clearly articulate “Why now?”—Why prioritize this feature today?
>
>
>
>
> Justify this specific approach compared to alternative solutions (considering lower risks, higher value).
>
>
>
>
>
>
> Stakeholder Impact:
>
>
>
>
> Positive: Identify beneficiaries clearly and document explicit support.
>
>
>
>
> Negative: Identify potential negative impacts, document objections, and describe mitigations or accepted trade-offs.
>
>
>
>
>
>
> Technical Readiness: Assess technical maturity clearly, providing links to specifications, tests, and client implementations.
>
>
>
>
> Security & Open Questions: Document explicitly known security risks, open issues, or unclear aspects. Include threat models, preliminary audit plans, or next steps.

Consider this template as comprehensive but flexible. The goal is providing an optimal overview of each proposal. Champions should also update their threads to link notable community feedback or useful inputs. [Here is a good historical example for EIP-1153](https://ethereum-magicians.org/t/shanghai-cancun-candidate-eip-1153-transient-storage/10784). Another useful format is a “readiness checklist,” such as those used for [The Merge](https://github.com/ethereum/pm/blob/master/Network-Upgrade-Archive/Merge/mainnet-readiness.md) or [EIP-4844](https://github.com/ethereum/pm/blob/master/Network-Upgrade-Archive/Dencun/4844-readiness-checklist.md).

## Replies

**jochem-brouwer** (2024-09-28):

EIP: [EIP-7773: Hardfork Meta - Amsterdam](https://eips.ethereum.org/EIPS/eip-7773)

---

**potuz** (2025-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/potuz/48/8696_2.png)

      [EIP-7732 the case for inclusion in Glamsterdam](https://ethereum-magicians.org/t/eip-7732-the-case-for-inclusion-in-glamsterdam/24306) [EIPs](/c/eips/5)




> ePBS: the case for Glamsterdam.
> This short note follows a template designed by @timbeiko to propose a headliner for a fork inclusion. I will keep it brief and as little technical as possible as I have already made a case for inclusion in Fusaka.
> Summary
> ePBS, as in EIP 7732 stands for execution Payload–Block Separation. It proposes the minimal set of changes to maximally decouple the execution layer from the consensus layer validations. Both in terms of broadcasting and transmitting blocks and …

---

**sorpaas** (2025-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png)

      [Glamsterdam headliner proposal: EVM64](https://ethereum-magicians.org/t/glamsterdam-hardliner-proposal-evm64/24311) [EIPs](/c/eips/5)




> This is a headliner proposal for EVM64 for Glamsterdam.
> Summary
> Headliner proposal for EVM64.
> Option A is EVM64 with prefix opcode 0xC0.
>
> EIP-7937 of EVM64 for endianness-independent arithmetic, comparison, bitwise and flow operations.
> EIP-9819 for EOF support.
> EIP-9821 for little-endian BYTE64, MLOAD64, MSTORE64 and PUSH*64 opcodes.
>
> Option B is “pure” EVM64 via EOF code section.
>
> EIP-9834 which defines an extended version of types_section for EOF.
> EIP-9835 which defines the EVM64 code sect…

---

**mingfei** (2025-05-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mingfei/48/15094_2.png)

      [Glamsterdam headliner proposal: Available Attestation](https://ethereum-magicians.org/t/glamsterdam-headliner-proposal-available-attestation/24377) [EIPs](/c/eips/5)




> This is a headliner proposal for Available Attestation (AA) for Glamsterdam.
> Summary (ELI5)
> Available Attestation (AA) is a proposed security upgrade to Ethereum that prevents malicious validators from reorganizing (reordering) blocks to steal transactions or manipulate the blockchain. Currently, attackers with enough stake can create competing blockchains and force the network to switch between them, causing instability. AA requires that before a new block can be built, it must prove that enou…

---

**etan-status** (2025-06-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png)

      [Glamsterdam headliner proposal: Pureth](https://ethereum-magicians.org/t/glamsterdam-headliner-proposal-pureth/24459) [EIPs](/c/eips/5)




> Summary
> EIP-7919: Pureth bundles a set of improvements to make Ethereum data easier to access and verify without relying on trusted RPC providers or third-party indexers. The improvements achieve this by changing data structures for blocks, transactions, and receipts, so that efficient correctness (i.e., validity) and completion (i.e., nothing omitted) proofs can be added to the RPC responses.
> The ability to verify RPC responses is essential for security. Today, most wallets and dApps consume d…

---

**sorpaas** (2025-06-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png)

      [Glamsterdam headliner proposal: EOF](https://ethereum-magicians.org/t/glamsterdam-headliner-proposal-eof/24464) [EIPs](/c/eips/5)




> This is a headliner proposal for EOF for Glamsterdam. EOF was SFI’d and then DFI’d for Fusaka. This proposal repropose it for Glamsterdam.
> Summary
> Headliner proposal for EOF. Note that compared with Fusaka, this headliner proposal has an additional change of EIP-9834 as a mandatory EIP.
> The following texts are copied from @ipsilon’s document (with the addition of EIP-9834).
> (A) - Complete EOF
> The first option represents the status quo of the current plan - proceed with the version of EOF that…

---

**soispoke** (2025-07-18):

Thought it was important to flag that the rule about “not being able to resubmit a headliner EIP as a vanilla EIP” doesn’t seem fair.

I think it’s great to keep experimenting on new ways to ship forks faster, in a more streamlined way (e.g., the new headliner initiative [EIP-7773: Glamsterdam Network Upgrade Meta Thread](https://ethereum-magicians.org/t/eip-7773-glamsterdam-network-upgrade-meta-thread/21195)). But it turns out [FOCIL](https://eips.ethereum.org/EIPS/eip-7805) is basically the archetype of an EIP that doesn’t neatly fit into the headliner structure because it touches both the EL and the CL, and because it is a “not too big, not too small” upgrade.

To be fair, [@timbeiko](/u/timbeiko) pointed out it was mentioned here: “Once a feature is declined as a potential headliner, it cannot return as a regular EIP within the same fork cycle to prevent back-door reprioritization.”  ([Community Consensus, Fork Headliners & ACD Working Groups](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088#p-58740-converging-towards-headliners-5)). But I think most people were not aware of the rule, and it still doesn’t make sense to me in practice. I also don’t think the risks of back-door reprioritization are real, if people don’t like an EIP they just wouldn’t include it in a fork either way.

A potential worst case scenario that could be considered as capture risk is an EIP that cannot be CFI’d just because it doesn’t fit into the governance process. Fork scope/complexity are both valid arguments but I wouldn’t want the process to just exclude EIPs for the sake of new/experimental rules.

---

**gcolvin** (2025-07-20):

In the present case of EOF, it consists of a number of EIPs, some of which are useful separately and worth introducing.

---

**gballet** (2025-08-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png)

      [The case for including code chunking (EIP-2926) in Glamsterdam](https://ethereum-magicians.org/t/the-case-for-including-eip-2926-in-glamsterdam/25089) [EIPs](/c/eips/5)




> Summary (ELI5)
> Introduces code chunking in the MPT, and adds a gas cost each time execution/code copy accesses a new chunk. This is useful for preventing a nasty “prover killer attack” in zkvms that it’s not currently possible to defend against. It is also useful for removing the code size limit. Last but not least, it’s preparing the way for stateless Ethereum by reducing witness size.
> Detailed Justification
> Benefits
> As part of the “scaling L1” roadmap of Ethereum, this EIP delivers:
>
> removin…

---

**SirSpudlington** (2025-08-29):

To reduce the burden on ACDE calls I have made a Ethereum Magicians post for EIPs 7932 and 7980 inclusion for async review: [The case for EIP-7932 & EIP-7980 inclusion in Glamsterdam](https://ethereum-magicians.org/t/the-case-for-eip-7932-eip-7980-inclusion-in-glamsterdam/25293).

---

**gballet** (2025-09-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png)

      [The case for EIP-8032 in Glamsterdam: Tree-Depth-Based Storage Gas Pricing](https://ethereum-magicians.org/t/the-case-for-eip-8032-in-glamsterdam-tree-depth-based-storage-gas-pricing/25619)




> Summary (ELI5)
> This proposal makes it progressively more expensive to store data in contracts that already have lots of storage. Think of it like a progressive tax on storage: small contracts pay normal fees, but contracts storing massive amounts of data pay exponentially more for each additional storage operation.
> Why it matters: Ethereum’s state is growing unsustainably, making it harder and more expensive to run nodes. This threatens decentralization.
> Who benefits directly: Node operators a…

---

**Millercarter** (2025-10-13):

EIP-7503 is a proposed standard for private transactions on Ethereum, enabling users to burn tokens privately and maintain their anonymity.

and it aims to enhance both privacy and security on the Ethereum network.WORM is a privacy preserving token on Ethereum that leverages Proof of Burn and unlinkability to ensure secure and private transactions.The Proof of Burn tech allows you and i to burn our tokens, making them unusable while maintaining their value and this process ensures that transactions are private and secure.

WORM’s unlinkability feature also ensures that transactions can’t be linked to the user’s identity.

It aligns with Ethereum’s roadmap and has been integrated by few L2s we will look into later on.

It’s also on the 2025 PSE roadmap, making it a bluechip project under the privacy narrative.

---

**CPerezz** (2025-10-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cperezz/48/7945_2.png)
    [EIP-8058: Contract Bytecode Deduplication Discount](https://ethereum-magicians.org/t/eip-8058-contract-bytecode-deduplication-discount/25933) [EIPs](/c/eips/5)



> Discussion topic for EIP-8058 https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8058.md
>
> This proposal introduces a gas discount for contract deployments when the bytecode being deployed already exists in the state. By leveraging EIP-2930 access lists, any contract address included in the access list automatically contributes its code hash to a deduplication check. When the deployed bytecode matches an existing code hash from the access list, the deployment avoids paying GAS_CODE_DEPOSIT * …

