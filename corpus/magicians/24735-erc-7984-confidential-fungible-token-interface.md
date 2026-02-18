---
source: magicians
topic_id: 24735
title: "ERC-7984: Confidential Fungible Token Interface"
author: ernestognw
date: "2025-07-04"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7984-confidential-fungible-token-interface/24735
views: 921
likes: 7
posts_count: 15
---

# ERC-7984: Confidential Fungible Token Interface

**Summary**

The team is proposing an specification for confidential fungible tokens that uses pointer-based amounts to maintain transaction privacy while enabling DeFi integration. This standard addresses the growing need for privacy-preserving token transfers on Ethereum without prescribing specific cryptographic implementations.

**Key Features**

The proposed standard introduces several novel concepts:

- Pointer-based amounts: All token amounts are represented as bytes32 pointers rather than plaintext values, allowing implementation flexibility across various privacy mechanisms (FHE, zero-knowledge proofs, secure enclaves, etc.)
- Time-limited operators: Instead of traditional approvals with specific amounts, the standard uses time-bounded operator permissions that expire automatically, reducing external system overhead and providing natural permission expiration
- Comprehensive callback system: Transfer functions include andCall variants that enable rich smart contract interactions while maintaining confidentiality
- Technology-agnostic design: The standard accommodates current and future privacy technologies without being tied to specific cryptographic assumptions



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1113#pullrequestreview-2987904707)














####


      `master` ← `arr00:add-confidential-tokens-erc`




          opened 01:33AM - 04 Jul 25 UTC



          [![](https://avatars.githubusercontent.com/u/13561405?v=4)
            arr00](https://github.com/arr00)



          [+291
            -0](https://github.com/ethereum/ERCs/pull/1113/files)







This PR adds a new ERC standard for a Confidential Fungible Token via pointers. […](https://github.com/ethereum/ERCs/pull/1113)Pointers are implementation specific; some examples include FHE cyphertexts, values stored confidentially in a TEE, and plain text stored offchain.

## Replies

**MASDXI** (2025-07-08):

Should ERC clarify that confidential assets are not entirely private? This is because the address is exposed in the calldata.

---

**Andriian** (2025-07-10):

How the amount of tokens is expected to be disclosed to work with DeFi protocols?

---

**Ivshti** (2025-07-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> andCall

Callbacks generally come with quite a few security implications like reentrancy and gas griefing. This should be addressed in the Scurity section

---

**arr00** (2025-07-29):

Confidential tokens can be utilized by DeFi protocols by executing arithmetic operations on the related coprocessor.

---

**arr00** (2025-07-29):

We can mention these in the security section.

---

**drllau** (2025-08-09):

These are just high-level thoughts as the draft (at least the version I could find) seems more preamble rather than specific design tradeoffs. There seems to be 3 generic approaches to “confidentiality” within the security  <confidentiality, integrity, availablity> triangle.

- holomorphic encryption - keep the number in place but change the mathematical/logic operators to use the transformed number
- interposer layer - basically this pointer is an indirection to a supposedly more protected enclave
- steganographic approaches where create noise to reduce likelihood of pinpointing real transaction

So using a pointer (or other indirection) is trying to push the 2nd approach letting access control gating who can traverse the pointer. My concern is more on the integrity side, how can you mathematically ensure that operations work correctly? The access controls as in who is permitted to view/operate/overwrite is yet another layer to prevent say man-in-middle attacks. There was a case of VC where hacker switched out the bank a/c number at last minute whilst passing thru everything else. Faults can come from anywhere, even in the compiler/instruction set. So what confidence is there that the operators are not fiddled with or that the functions are bijective (meaning pointers don’t reference info outside enclave).

---

**SuperDevFavour** (2025-08-10):

How are defi protocols expected to interact with this ERC?

---

**ernestognw** (2025-08-15):

Hi [@drllau](/u/drllau), thanks for the feedback!

I agree that the current draft feels more like a preamble than a specification with concrete design choices. This is somewhat intentional as we’re trying to establish interface compatibility across different privacy implementations, but I would expect the ERC to evolve to either:

1. Incorporate these design tradeoffs as the ecosystem matures, or
2. Spawn additional informational ERCs that document implementation patterns

In principle, the 3 approaches you suggest seem exhaustive enough. I think the ERC would benefit from acknowledging the `bytes32` argument could be used for both holomorphic arithmetic and steganography.

Right now, the reference implementation the ERC is based on is the [OpenZeppelin Confidential Contracts](https://github.com/OpenZeppelin/openzeppelin-confidential-contracts/blob/master/contracts/token/ConfidentialFungibleToken.sol) implementation, which gave us enough knowledge to document the pointer based variant so far. Before attempting to make the ERC more exhaustive we might discuss tradeoffs with other approaches. Are there fungible token implementations of approaches 1 and 3?

On the integrity side, I also share the concern. In theory, the external system pointers reference should be verifiable and auditable. I remember [@arr00](/u/arr00) mentioned this is not possible for FHE, so I think he can provide better feedback here.

> How are defi protocols expected to interact with this ERC?

Formally, the ERC suggests the operator for DeFi integrations. But in practice the end goal of the standard is that the ERC and semantics become decently defined so that DeFi protocols could rely on them for designing integrations.

---

**arr00** (2025-08-19):

This ERC aims to provide a standard interface for confidential tokens utilizing offchain systems to provide this confidentiality. The ERC views the offchain system as black boxes and does not attempt to guarantee or specify anything about them. That said, we have been initially building with the Zama FHEVM in mind and I believe they are working on a way to have some sort of zkproofs testifying the soundness of their offchain FHE calculations.

By no means do I think this is the only way to provide confidentiality onchain, but I do believe that attempting to group all types of confidentiality into one token interface would be a mistake. This is just a first attempt at producing a token interface for privacy systems utilizing an interposer layers.

---

**arr00** (2025-09-18):

I’m looking into switching the URI function from `tokenURI` to `contractURI`. This seems like a better choice give that the token is non-fungible. It also follows the precedent set by ERC7572.

---

**jat** (2025-10-30):

Hello,

I was wondering what was the rationale to not include the confidential analog of `approve` function in your confidential token standard and instead replace it by a time-based `setOperator(operator, deadline)` function? It might seem more risky since with this design all approvals are unlimited in amount.

I see how his could potentially save some gas, for eg in the ZAMA-based implementation. However there is a major downside of this, if the account you give approval for is malicious, he might steal all your balance (even if using a deadline in same block, you can get back-runned).

For me it would make sense to offer both options, otherwise I fear potentially catastrophic loss of whole balance when interacting with new defi apps.

---

**drllau** (2025-12-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> I think the ERC would benefit from acknowledging the bytes32 argument could be used for both holomorphic arithmetic and steganography.

I’m a certified legal engineer so I always look at issues from a (legal) risk perspective. I know ERCs are supposed to be broad generic interfaces but homorphic & indirection seems to be address 2 orthogonal problem spaces

1. where basically the meta data (when transaction occur or parties temporal consistency checked) needs to be public but precise state (internal amounts) are commercial-in-confidence. This addresses regulatory requires which require say trade data to be public (compilation of aggregate stats) but you don’t want competitors (or speculators) putting your day-2-day business activities under microscope
2. indirection is really a way to enforce surjective and injective mappings (google the maths), reducing the transaction space to chunks/partitions which allows for say role-based access control.
3. stenography is more for obfuscation or furfitive … hiding in noise or a crowd so we can ignore this for now (touches on anti-money-laundering and you don’t want to go there).

> All token amounts are represented as bytes32 pointers rather than plaintext values, allowing implementation flexibility across various privacy mechanisms (FHE, zero-knowledge proofs, secure enclaves, etc.)

The space of RBAC is where (doubly) indirection might create novel use-cases. You can prove that all the data is covered (bijective mapping) but the tax component (eg GST) is compiled quarterly and totals unlocked with special keys so the tax authorities can verify the amounts due or refundable without going down to granular receipts. This can be seen in the worrying announcements that certain govts are combining tax and address databases. You want to be honest but you don’t want masked thugs busting down door in night,

I note that the OpenZep ref implementation is going down the homomorphic route using a tightly controlled EVM … this is to ensure that the hidden amounts stay hidden at the device level. With pointer indirection, the attack surface is more man-in-middle … how do you ensure **full integrity** from the JSON down to EVM dereferencing?

---

**arr00** (2025-12-09):

The reasons for using exclusively time-based approvals instead of amount-based approvals:

1. Reduced complexity - When operating on handles, branching at execution time is not possible. This means we can’t revert or terminate early due to insufficient approval amounts. Having approvals be ciphertexts adds significant complexity to the execution flow, another SSTORE on every transfer, and makes it harder for users to understand why transfers fail.
2. Reduce load on external services handling operations off-chain.
3. Historic Approval Trends - historically, most ERC-20 approvals have been infinite or for the total balance–this flow is an improvement on that. If used properly, there is no concept of revoking old approvals or having to worry about a protocol used years ago getting hacked.

If a user plans to use a malicious protocol, they can use a burner wallet and only transfer what they are willing to lose.

---

**arr00** (2026-01-30):

There are two new topics I’d like feedback on here.

1. Removal of unnecessary transfer functions: Transfer functions with solely a bytes32 input and not a bytes array as well are somewhat superfluous. The only practical role they have is allowing for slight gas improvements when transferring without the need for the bytes array. Should these be removed in favor of simplicity and deployment costs?
2. Amount-based approvals: There have been a significant number of requests for amount-based approvals. Should these be added in addition to time-bound operators? The operator can be checked first with the amount-based approvals as a fallback.

