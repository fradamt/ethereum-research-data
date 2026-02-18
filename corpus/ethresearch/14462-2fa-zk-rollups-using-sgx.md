---
source: ethresearch
topic_id: 14462
title: 2FA zk-rollups using SGX
author: JustinDrake
date: "2022-12-21"
category: zk-s[nt]arks
tags: [zk-roll-up]
url: https://ethresear.ch/t/2fa-zk-rollups-using-sgx/14462
views: 14136
likes: 100
posts_count: 29
---

# 2FA zk-rollups using SGX

**TLDR**: We suggest using SGX as a pragmatic hedge against zk-rollup SNARK vulnerabilities.

*Thanks you for the feedback, some anonymous, to an early draft. Special thanks to the Flashbots and Puffer teams for their insights.*

**Construction**

Require two state transition proofs to advance the on-chain zk-rollup state root:

1. cryptographic proof: a SNARK
2. 2FA: an additional SGX proof

SGX proofs are generated in two steps:

1. one-time registration: An SGX program first generates an Ethereum (pubkey, privkey) pair. This keypair is tied to a specific SGX enclave, and only signs valid state transitions (pre_state_root, post_state_root, block_root). The pubkey is registered on-chain by verifying an SGX remote attestation which attests to the pubkey being correctly generated.
2. proving: After registration the SGX program runs the rollup state transition function to sign messages of the form (pre_state_root, post_state_root, block_root). These SGX proofs are verified on-chain by checking signatures against the registered pubkey.

**Context**

Early zk-rollups are prone to SNARK soundness vulnerabilities from circuit or proof system bugs. This is concerning because:

1. complexity: The engineering of zk-rollups is particularly complex. Even bridges, an order of magnitude less complex than rollups, are routinely hacked.
2. value secured: The value secured by leading zk-rollups is expected to become significantly higher than that of today’s bridges. These large bounties may be a systemic risk for Ethereum.
3. competition: The zk-rollup landscape is competitive, with first-mover advantages. This encourages zk-rollups to launch early, e.g. without multi-proofs. (See Vitalik’s presentation and slides on multi-proofs.)

**Discussion**

SGX 2FA is particularly attractive:

- safety: There is no loss of safety to the zk-rollup—the additional requirement for SGX proofs is a strict safety improvement. Notice that the SGX enclaves do not handle application secrets (unlike, say, the Secret Network).
- liveness: There is almost no loss of liveness. The registration step does require Intel to sign an SGX remote attestation but:

a) The specific SGX application Intel is providing a remote attestation for can be hidden from Intel. Intel would have to stop providing remote attestations for multiple customers to deny remote attestations for a targetted zk-rollup.
- b) Hundreds of SGX enclaves can register a pubkey prior to the rollup launch. The currently registered pubkeys can generate SGX proofs even if Intel completely stops producing remote attestations for new registrations.
- c) If required, rollup governance can remove the SGX 2FA.

**gas efficiency**: The gas overhead of verifying an SGX proof is minimal since only an Ethereum ECDSA signature is being verified on-chain (other than the one-time cost of verifying remote attestations).

**latency**: There is no additional proof latency—producing SGX proofs is faster than producing SNARKs. Notice that SGX 2FA provides little value to optimistic rollups which have multi-day settlement and can use governance to fix fraud proof vulnerabilities.

**throughput**: There is no loss of throughput. The Flashbots team has shown Geth can run at over 100M gas per second on a single SGX enclave. If necessary multiple SGX enclaves can work in parallel, with their proofs aggregated.

**computational resources**: The SGX computational resources can be minimal. When the state transition is run statelessly (e.g. see [minigeth](https://github.com/ethereum-optimism/minigeth)) there is no need for an encrypted disk and minimal encrypted RAM is required.

**simplicity**: The engineering of SGX is easy relative to SNARK engineering. Geth can be compiled for Gramine with [an 11-line diff](https://github.com/flashbots/geth-sgx-gramine/tree/main/gramine-compatibility). The [Puffer](https://www.puffer.fi/) team is working on a Solidity verifier for SGX remote attestations, supported by an Ethereum Foundation grant.

**auditability**: Auditing the 2FA should be relatively straightforward. The SGX proof verification logic is contained and the incremental smart contract risk from introducing SGX 2FA is minimal.

**flexibility**: Enclaves from non-Intel vendors (e.g. [AMD SEV](https://developer.amd.com/sev/)) can replace or be used in parallel to SGX enclaves.

**bootstrapping**: 2FA can be used alone—without SNARK verification—to bootstrap an incremental rollup deployment. (This would be similar to Optimism launching without fraud proofs.)

**upgradability**: The SGX proof verification logic is upgraded similarly to the SNARK verification logic. Previously registered pubkeys are invalidated and the definition of what constitutes a valid pubkey is changed by upgrading the remote attestation verification logic.

**deactivation**: SGX 2FA is removable even without governance. For example, the 2FA could automatically deactivate after 1559 days.

There are also downsides to SGX 2FA:

- memetics: SGX has a bad reputation, especially within the blockchain space. Association with the technology may be memetically suboptimal.
- false sense of security: Easily-broken SGX 2FA (e.g. if the privkey is easily extractable) may provide a false sense of security.
- novelty: No Ethereum application that verifies SGX remote attestations on-chain could be found.

## Replies

**spacetractor** (2022-12-23):

Avoid dependency on SGX at all costs, it have been breached before, it will be breached in the future.  As you mentioned, it has a very bad reputation in the space for obvious reasons

---

**pepesza** (2022-12-23):

Following assumes that attacks against SGX can steal bits of private key, but only at rate of few bits per `privkey` access. And `privkey` is accessed only to produce signatures.

Consider rotating the keypair with every attestation. Add pubkey of the new keypair to the tuple signed on every attestation: `(pre_state_root, post_state_root, block_root, new_pubkey)`. Smart contract will update 2FA key with `new_pubkey`.

This increases gas cost - one more SSTORE per state transition.

---

**MicahZoltu** (2022-12-23):

If there was a critical failure of SGX (worst case scenario you can imagine, including Intel being actively malicious), what bad things would happen?  Assuming the ZK stuff was not broken then would nothing bad happen at all?  Is the bad scenario *only* when both SGX and ZK stuff are broken?

One disadvantage of this is that you don’t get the benefit of an escalating “bug bounty” over time as the system attracts capital.  The set of attackers who can exploit a bug in the ZK stuff is limited to state actors, Intel, and maybe some hardware manufacturers involved in the chip production process.  This means everything seems to be fine right up until it catastrophically fails and that could be a long way off.  If the ZK is exposed directly, it is more likely to be attacked early before too much capital moves in.

---

**JustinDrake** (2022-12-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/pepesza/48/628_2.png) pepesza:

> Consider rotating the keypair with every attestation.

Oh, great suggestion! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/spacetractor/48/7203_2.png) spacetractor:

> Avoid dependency on SGX […] it will be breached in the future.

There is no dependency on SGX—that’s the point. When SGX is breached safety falls back to a “vanilla” zk-rollup. SNARKs plus SGX is a strict safety improvement over just SNARKs.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Assuming the ZK stuff was not broken then would nothing bad happen at all? Is the bad scenario only when both SGX and ZK stuff are broken?

Yes to both questions.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> One disadvantage of this is that you don’t get the benefit of an escalating “bug bounty” over time as the system attracts capital.

In addition to the “organic” bug bounty for simultaneously breaking both the SNARK and SGX, one could design a “synthetic” escalating bug bounty for breaking either the SNARK or SGX. The synthetic bounty could escalate by, say, 10 ETH per day.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> everything seems to be fine right up until it catastrophically fails

The endgame for zk-rollups is that SNARKs are sufficient for security thanks to multi-proofs (see links in the post) and formal verification. You can think of SGX security-in-depth as a way to buy time to achieve this endgame and reduce the risk of ever failing catastrophically.

---

**jannikluhn** (2023-01-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Notice that SGX 2FA provides little value to optimistic rollups which have multi-day settlement and can use governance to fix fraud proof vulnerabilities.

ORs often get criticized for this ability because arguably it means that users have to trust the governance mechanism first and foremost and the fraud proofs are not much more than decoration. Wouldn’t SGX 2FA be a great tool for ORs to minimize the power of governance? Emergency updates would only be allowed if there’s disagreement between the two factors. Other updates would require a notice period of about one month, giving everyone ample time to exit if they disagree.

---

**nvmmonkey** (2023-01-05):

Setup a 2FA Network/Layer:  this should verify the 2FA proofs required by the protocol. The nodes could be run on low-cost hardware (e.g. Raspberry Pis) and could be distributed geographically to ensure redundancy and resilience.

Aaggregated Proof: Also, the protocol could use proof aggregation techniques to minimize the overhead of generating and verifying 2FA proofs. This involves grouping multiple proofs together and creating a single, aggregated proof that can be verified more efficiently. Certainly, this will need to be designed to secure and resist attack.

---

**lead4good** (2023-02-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The pubkey is registered on-chain by verifying an SGX remote attestation which attests to the pubkey being correctly generated.

What if we would move the remote attestation off-chain? Do you see any scenarios where it would make rollups less secure?

The rollup could serve the remote attestation via a different channel upon request, allowing any user interested in interacting with the rollup to verify its attestation (and that it is the owner of `privkey`). Since the smart contract verifies signatures generated by SGX, full trust is established.

Even key rotation could be implemented by the rollup, by just creating and storing the remote attestation of every key used.

---

**jvranek** (2023-03-01):

This will certainly reduce gas costs, but I can see some tradeoffs:

1. Since this involves safeguarding privkey, this approach is vulnerable if SGX’s confidentiality is broken and privkey is ever extracted and used to sign bad state roots. Instead, verifying an SGX remote attestation on-chain per state root requires breaking SGX’s integrity to produce a bad state root (but also requires way more gas).
2. This approach seems to lend itself better to a permissioned rollup, where the sequencer controls which (key, remote attestation) pairs are whitelisted by the contract. The verify-before-use idea breaks down if we want > 1 sequencer per rollup.
3. More burden on the users - they could join a nefarious rollup if they are lazy and skip the off-chain verification.

---

**jiayaoqijia** (2023-03-06):

It’s a quite nice use case of SGX for fair execution not for storing private keys. With guaranteed execution, it helps both Optimistic and ZK rollups for verification.

---

**lead4good** (2023-03-27):

I believe we can combine both approaches.

1. a sequencer introduces itself to the contract with a remote attestation that also attests it and its private key have been created very recently (i.e. add latest known block hash before priv key generation to attestation quote)
2. the sequencer will publish new state roots and regenerate its private key every now and then (as per @pepesza 's suggestion)
3. if the delta between two private key switches is to big, the contract will dismiss sequencer submissions
4. A new sequencer can be introduced as per step 1

This reduces gas costs as we’re only attesting during sequencer registration, But at the same time it should allow > 1 sequencer per rollup - as per your definition.

---

**jvranek** (2023-03-27):

I believe this can be taken even further and we can do a remote attestation (RA) + key-rotation per state root while only paying L2 gas fees!

- The sequencer performs RA, committing to a fresh ETH public key and the last block hash.
- The sequencer verifies the RA as part of the batched rollup txs (paying only L2 gas fees for on-chain RA verification). The ETH  public key becomes whitelisted, assuming the RA was valid and the committed last block hash is sufficiently fresh.
- The L1 contract will only accept the state root if it was signed with the enclave’s corresponding ETH private key, otherwise it will revert (this relies on the rollup’s data being immediately available to the L1).

---

**lead4good** (2023-03-28):

Interesting approach!

- if RA is not trivial to implement in vanilla EVM, zkEVM’s might have more implementation issues and zk-rollups which do not have EVM compatibility will likely have even more issues doing RA?
- if we have a setup where the rollup uses the TEE block transition proof as the only source of truth, then the enclave providing the RA would be the one verifying it’s correctness, which brings no gain (TEE only rollups have not really been discussed so far but are an interesting topic nonetheless)
- in addition to that - if the zk proof can be faked I think the RA can be faked as well, so we would be loosing the 2FA guarantees

---

**haraldh** (2023-06-22):

> The pubkey is registered on-chain by verifying an SGX remote attestation which attests to the pubkey being correctly generated.

This step would interest me the most on how this would be (is?) implemented in detail…

Where is the attestation report + collateral stored for later verification by 3rd parties?

I guess the attestation report_data will contain the hash of the `pubkey`.

I doubt EVM could do a full attestation verification with all the TCB state verification and certificate revocation lists involved, but prove me wrong ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**JustinDrake** (2023-06-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/haraldh/48/12505_2.png) haraldh:

> I doubt EVM could do a full attestation verification

It turns out I was wrong! Verifying the SGX remote attestation can be done offchain by users ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) This makes SGX 2FA easy to implement.

---

**haraldh** (2023-06-22):

Where is the attestation report + collateral stored for later verification by 3rd parties, then?

---

**JustinDrake** (2023-06-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/haraldh/48/12505_2.png) haraldh:

> Where is the attestation report […] stored

The SGX attestation can be hosted anywhere (e.g. on a traditional website, on IPFS, even on-chain).

![](https://ethresear.ch/user_avatar/ethresear.ch/haraldh/48/12505_2.png) haraldh:

> Where is the […] collateral stored

Not sure what collateral you are referring to. The scheme described doesn’t have collateral.

---

**haraldh** (2023-06-23):

> The scheme described doesn’t have collateral.

To completely verify an attestation report you need additional data from [api.trustedservices.intel.com](http://api.trustedservices.intel.com) (see [Documentation - Intel® SGX and Intel® TDX services - Production environment](https://api.portal.trustedservices.intel.com/documentation)).

So a report with the collateral downloaded at the time of attestation, you need (bytes from an example report + collateral from this week):

- the report itsself (4730 bytes)
- collateral.pck_crl (3653 bytes)
- collateral.pck_crl_issuer_chain (1905 bytes)
- collateral.tcb_info (4291 bytes)
- collateral.tcb_info_issuer_chain (1893 bytes)
- collateral.qe_identity (1381 bytes)
- collateral.qe_identity_issuer_chain (1893 bytes)
- collateral.root_ca_crl (448 bytes)

Which would sum up to: report 4730 bytes + collateral 15464 bytes = 20194 bytes for one of my TEEs as of this week.

Then you have to define and record somewhere what TCB status is still acceptable, like “SWHardeningNeeded” and which advisory Ids the SGX software mitigates like “INTEL-SA-00615”.

---

**ameya-deshmukh** (2023-06-26):

[@JustinDrake](/u/justindrake) this seems like a really cool idea for a thesis/paper, would love to pursue it if possible. What’s the best place to contact you?

---

**JustinDrake** (2023-06-26):

Oh I see, “collateral” is some subset of the attestation data ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) (For me “collateral” usually means financial collateral.)

To answer your question: the attestation data (report + collateral) can be stored anywhere—that’s an implementation detail. It just needs to be downloadable by prospective users.

---

**nanaknihal** (2023-09-02):

This point is very interesting, and to expand on it I think a multisig or TSS involving multiple enclave vendors could add an additional layer of security, arguably even 3FA.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> flexibility: Enclaves from non-Intel vendors (e.g. AMD SEV) can replace or be used in parallel to SGX enclaves.

Especially combined with this, I imagine it is significantly difficult or at least prohibitively expensive to attack multiple architectures and in the span of a single transaction.

![](https://ethresear.ch/user_avatar/ethresear.ch/pepesza/48/628_2.png) pepesza:

> Consider rotating the keypair with every attestation. Add pubkey of the new keypair to the tuple signed on every attestation: (pre_state_root, post_state_root, block_root, new_pubkey). Smart contract will update 2FA key with new_pubkey.

There are attacks which can fake attestations of bad enclaves, so I don’t think key rotation alone would prevent those on a single architecture, but I’m not sure how easy it is to perform such attacks on multiple enclave architectures at once before one patches it.

This seems strictly better than a SNARK alone, especially with

- enclaves from multiple vendors in a multisig
- rotating keys every transaction


*(8 more replies not shown)*
