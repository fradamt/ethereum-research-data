---
source: ethresearch
topic_id: 22005
title: Update Credentials Without Mnemonic (UCWM)
author: maverickandy
date: "2025-03-25"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/update-credentials-without-mnemonic-ucwm/22005
views: 595
likes: 13
posts_count: 11
---

# Update Credentials Without Mnemonic (UCWM)

## Abstract

This draft EIP introduces a mechanism for Ethereum validators with BLS (0x00) withdrawal credentials who have lost access to their withdrawal mnemonic to securely update their credentials to execution-layer (0x01) credentials. The mechanism, inspired by the Consensus Layer Withdrawal Proposal (CLWP) concept, uses cryptographic proofs of validator control and deposit origin. Additionally, it defines a pathway for validators operated by custodial stake pools to achieve the same update through cooperative validation, enabling recovery for a wide range of affected participants.

---

Motivation (Updated)

After Ethereum’s transition to proof-of-stake, validators registered with BLS-based (0x00) withdrawal credentials must migrate to execution-layer (0x01) credentials to access and withdraw their staked ETH. However, many validators have not completed this migration — and some have lost access to the mnemonic needed to authorize the credential change, leaving their ETH effectively locked.

This proposal enables such validators to recover access in a secure, verifiable way using cryptographic proofs of control over both:

- The validator signing key, and
- The original deposit address.

Additionally, a large number of validators are operated through custodial staking providers (stake pools), where the validator signing key is held by the provider. This proposal outlines a controlled, consent-based process where the depositor can initiate the recovery, and the stake pool cooperates by producing the required validator signature — but only with explicit depositor authorization.

Long-Term Motivation: BLS Deprecation & Quantum Risk

BLS withdrawal credentials (0x00) rely on BLS12-381 elliptic curve cryptography, which is not quantum-safe. In the presence of a sufficiently powerful quantum computer, it would be possible to derive private keys from public keys using Shor’s algorithm, making BLS credentials vulnerable to theft.

In contrast, execution-layer credentials (0x01) leverage Ethereum account-based cryptography, which can more easily migrate to quantum-resistant schemes as part of future protocol upgrades.

As a result, the Ethereum ecosystem will likely need to deprecate BLS credentials entirely in the future. This proposal serves as important pre work for that transition by:

- Establishing a robust recovery mechanism for currently inaccessible 0x00 validators.
- Defining a standard pattern for validator credential updates outside of the original mnemonic flow.
- Preparing the validator set for future migrations to post-quantum withdrawal formats.

This ensures that Ethereum can maintain a healthy validator set, prevent permanent ETH loss, and reduce the eventual coordination burden of a network-wide BLS deprecation.

---

## Specification

### Scope

This mechanism applies only to:

- Validators with 0x00 BLS withdrawal credentials.
- Validators that have not exited or withdrawn their funds.
- Cases where the mnemonic (withdrawal key) is lost or inaccessible.

---

## 1. Non-Custodial Validators (Self-Operated)

### Proof-of-Ownership Flow

A validator can request a credential update by submitting two cryptographic signatures. This process is outlined onhttps://github.com/eth-educators/update-credentials-without-mnemonic and https://ucwm.xyz

1. Validator Key Store Signature
The validator creates a key store signature by using their validator key and the Ethereum deposit-cli.
2. Deposit Address Signature
The original deposit address (the address that funded the validator via the deposit contract) signs a message through Beaconcha.in.

These signatures, along with metadata (validator index, target execution address), are submitted to an on-chain credential update contract or recognized off-chain protocol.

### Verification and Update

- Both signatures are verified against the list of validators with BLS credentials and the deposit address is also validated manually.
- A challenge period (e.g., XX-XX months) allows the community to dispute any fraudulent claim.
- If successful, the validator’s withdrawal credentials are updated from 0x00 to 0x01, with the specified execution address.
- These validators will be added to the exit queue, adhering to the existing exit rate limits to avoid destabilizing the network.

---

## 2. Custodial Stake Pool Validators

### Problem Context

For validators run via custodial staking providers, the validator private key is held by the stake pool, not the depositor. This makes it impossible for the depositor to produce the validator key signature themselves.

### Proposed Custodial Flow

1. Depositor Declaration (On-Chain Intent)
The depositor (owner of the funding address) signs a message through Beaconcha.in and submits it on-chain, stating:

- Their control over a specific validator (by index or public key).
- Their request to update withdrawal credentials.
- Their target execution address.

1. Operator Review & Stake Pool Coordination

- A trusted multisig, DAO, or ETH Staker community body reviews the declaration.
- They verify the deposit origin and validator status.
- They contact the stake pool to confirm the depositor’s relationship.

1. Stake Pool Signature
The stake pool, upon verification, follows the same process as above to create a validator key store signature.
2. Final Submission and Challenge Period

- The pool’s validator signature, linked to the depositor’s on-chain declaration, is submitted.
- Challenge period begins.
- Upon approval, withdrawal credentials are updated.
- Lastly, these validators are added to the exit queue.

---

## Rationale

- Minimizes ETH loss: Enables recovery for validators whose funds are otherwise permanently locked.
- Dual-authentication: Using both the validator key and deposit key ensures strong identity guarantees.
- Stake pool path: Provides a collaborative, secure, and consent-driven path for custodial validators.

This proposal can be seen as an homage to the great work that [@jgm](/u/jgm) / [@benjaminchodroff](/u/benjaminchodroff) have done on CLWP. I would very much appreciate your thoughts on this.



      [ucwm.xyz](https://ucwm.xyz/)





###



Proposal to help Ethereum validators that are stuck on BLS credentials and have no way to update withdrawal credentials to 0x01

## Replies

**maverickandy** (2025-03-25):

There are currently 13,394 validators with BLS credentials. Full analysis can be found on the website here:



      [ucwm.xyz](https://ucwm.xyz/analysis.html)





###



Analysis of Ethereum validators with BLS credentials

---

**potuz** (2025-03-25):

Why the restriction to non exited validators? If I were in this situation I would exit my validators immediately and still want to recover my ETH

---

**potuz** (2025-03-26):

I assume  some (most?) validators on BLS addresses aren’t lost but rather don’t care about withdrawals or don’t want to trigger taxable events. At any rate I’d expect the participation to be much less than the full BLS set. I support this idea, specially if it’s done over a very long period of time (say 24 months for example) to give time for any dispute

---

**benjaminchodroff** (2025-03-26):

There are large risks in this EIP because in the “Proposed Custodial Flow” it is bypassing the agreed existing consensus layer protocol handling for 0x00 to 0x01 set withdrawal address by using a third party to validate a list of agreed changes and asking the community to input these changes into a hard fork. I have sympathy for those with lost validator mnemonics, but it is unlikely the Ethereum community is going to support this centralized execution risk and complexity.

I am not going to be able to fully solve this in a comment or be able to endorse this project, but here are some brainstorming ideas to consider.

A simpler and more decentralized approach may be to just agree that after migrating away from BLS to a new PQC algorithm in the CL, any remaining 0x00 validators could be considered “eligible for EL migration” and allow the first EL deposit address associated to the validator to make an EL function call to set a 0x01 withdrawal address. Even this has risks, but if described early enough, those wishing to avoid this risk should either set their own 0x01 address using the agreed CL protocol, or consider using the new PQC algorithm which could set new states (“0x02”) showcasing they are no longer using BLS and still have adopted the PQC signature but still wish to have no EL withdrawal address set. If they “do nothing” and leave the validator controlled by BLS with a 0x00 it is showcasing a risk that a quantum computer could equally take over their validator. This proposal would give any remaining “lost” 0x00 validator an opportunity to set 0x01 from the EL layer using their first deposit address (if they used an exchange or third party protocol, there is no way to help…) or those who have legitimate reasons to continue operating without a withdrawal address a safe migration to PQC without setting an EL withdrawal address.

---

**philrx31** (2025-03-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminchodroff/48/8085_2.png) benjaminchodroff:

> A simpler and more decentralized approach may be to just agree that after migrating away from BLS to a new PQC algorithm in the CL, any remaining 0x00 validators could be considered “eligible for EL migration” and allow the first EL deposit address associated to the validator to make an EL function call to set a 0x01 withdrawal address.

I fully agree with this approach—it appears to be a viable solution. I have previously advocated for this alternative strategy in case the community was not inclined to adopt the UCWM method.

Based on the initial feedback, this longer-term plan seems to be gaining more traction. However, I do have one question:

If we migrate the remaining 0x00 validators to a 0x01 withdrawal credential using the deposit address, validators who have lost access to their mnemonic would still need a way to exit the CL. Could you provide insights into the best approach for them to proceed after successfully updating their withdrawal credentials?

---

**benjaminchodroff** (2025-03-26):

The EL function allowing the initial EL deposit address to request setting the validator 0x01 address could also trigger the CL exit. This idea is a change to consensus and requires a hard fork, but if you are presenting that the PQC signature replacing BLS is already available in the CL and validators who wanted to move to “0x02” to avoid setting a withdrawal address had ample time… there is at least an argument to made that either a quantum computer is going to eventually crack the remaining 0x00 BLS validators and steal the locked funds, or you can rightfully allow the initial depositor (assuming they control this mnemonic) to rescue their lost validator. While this rescue idea isn’t going to happen for many years, I’d be in favor of it because it both reduces the risk of nation states using their quantum computer to attack unprotected ETH 0x00 validators and helps the right people in our community get their funds back at the right time – when it becomes absolutely necessary to move away from BLS.

---

**philrx31** (2025-03-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminchodroff/48/8085_2.png) benjaminchodroff:

> While this rescue idea isn’t going to happen for many years, I’d be in favor of it because it both reduces the risk of nation states using their quantum computer to attack unprotected ETH 0x00 validators and helps the right people in our community get their funds back

Once again, your insight and wisdom are truly commendable—there’s little to add to your statement.

In the meantime, do you believe we should still pursue the goal of collecting dual signatures from validators who have lost access to their mnemonics and attempt to move forward with this EIP, or would this effort be essentially futile?

Alternatively, do you see another path worth exploring that we may not have considered yet?

---

**benjaminchodroff** (2025-03-27):

Don’t lose hope, and stay up to date with the PQC efforts in Ethereum being made. Many are now realizing the recommended timeline for implementing PQC has shrunk from “decades” to “years.”

I personally think trying to collect dual signatures and review them in a DAO is challenging and not going to help. It may distract the developers from just encouraging the right outcome when they start to make a post-quantum replacement for BLS. I would revise the proposal that exclusively uses on-chain data in a simple, fair and entirely decentralized process. I would highlight the risk that validators protected by BLS alone are not quantum resistant, and may eventually be stolen by a quantum computer. Therefore, the right approach may be to help provide a new EL option allowing the first deposit address to set a withdrawal address and exit these validators once a PQC CL signature method has been made available. It is a reasonable request to at least consider when they hardfork away from BLS, but there are likely other edge cases that must be carefully considered.

---

**maverickandy** (2025-03-27):

Very much appreciate your time and inputs (both [@potuz](/u/potuz) and [@benjaminchodroff](/u/benjaminchodroff)).

We will rewrite the proposal and include exited validators, lose the signatures aspect and focus on the decentralized approach outlined above.

[@potuz](/u/potuz): What are your thoughts on the process that [@benjaminchodroff](/u/benjaminchodroff) ? Anything else we should consider or focus on? Potential edge cases?

---

**maverickandy** (2025-05-08):

This topic has evolved into a new post. Would love to get your inputs/thoughts on it:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/maverickandy/48/11806_2.png)
    [Deprecating BLS: Post-Quantum Recovery via Deposit Address](https://ethresear.ch/t/deprecating-bls-post-quantum-recovery-via-deposit-address/22285) [Proof-of-Stake](/c/proof-of-stake/5)



> Abstract
> Proposal to deprecate BLS-based (0x00) withdrawal credentials in Ethereum due to their vulnerability to quantum computing attacks. It establishes a simple Execution Layer recovery where validators that remain on 0x00 after a post-quantum cryptographic (PQC) signature method becomes available may be recovered via their original deposit address. It also introduces a new optional withdrawal credential (0x03) secured by a post-quantum cryptographic key. A hard fork is required to implement …

