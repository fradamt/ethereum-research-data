---
source: ethresearch
topic_id: 22285
title: "Deprecating BLS: Post-Quantum Recovery via Deposit Address"
author: maverickandy
date: "2025-05-08"
category: Proof-of-Stake
tags: [security, post-quantum, consensus]
url: https://ethresear.ch/t/deprecating-bls-post-quantum-recovery-via-deposit-address/22285
views: 961
likes: 5
posts_count: 10
---

# Deprecating BLS: Post-Quantum Recovery via Deposit Address

### Abstract

Proposal to deprecate BLS-based (0x00) withdrawal credentials in Ethereum due to their vulnerability to quantum computing attacks. It establishes a simple Execution Layer recovery where validators that remain on 0x00 after a post-quantum cryptographic (PQC) signature method becomes available may be recovered via their original deposit address. It also introduces a new optional withdrawal credential (0x03) secured by a post-quantum cryptographic key. A hard fork is required to implement these changes.

---

### Motivation

- Quantum Risk: BLS public keys are exposed at deposit and could be broken by future quantum computers.
- Lost Keys: Validators with lost BLS keys (e.g., lost mnemonic) cannot update withdrawal credentials or exit, leaving funds permanently locked. These validators are at risk of being attacked by nation states using their quantum computers. It also helps the right people in our community get their funds back at the right time.
- Community Need: A decentralized, trustless recovery method for lost validators is required to protect the Ethereum ecosystem without introducing social or custodial interventions.
- Current Analysis: As of January 2025, approximately 13,394 validators are still on BLS credentials, representing 1.15% of active validators. A large portion shows no transaction activity since deposit, indicating high risk of key loss. It also includes 1172 validators of Stakehound that are permanently locked when their third-party security provider lost access to private keys in 2021.

---

### Implementation

Following the future introduction of post-quantum cryptographic (PQC) signatures in the consensus layer, any validator that remains using a 0x00 withdrawal credential will become eligible for execution-layer (EL) recovery.

- Overview of Execution-Layer Recovery:

The first deposit address associated with the validator will be authorized to submit an EL transaction to update the validator’s withdrawal credentials.
- The deposit address can then:

Set a new 0x01 execution-layer withdrawal address.
- Once they set a withdrawal address, they can use that withdrawal address to trigger an exit. Exits can be EL triggered from the withdrawal address from Pectra

Fallback and Fairness:

- Validators wishing to avoid this fallback must update their credentials themselves, either setting a 0x01 or 0x02 address or adopting a 0x03 PQC credential.
- Validators who do not act after ample warning and transition windows are signaling acceptance of the fallback mechanism.

Edge Cases and Caution:

- Some validators deposited via custodial services may not control the deposit address; such validators may not be recoverable through this method.
- Edge cases involving shared or misattributed deposit addresses must be carefully reviewed during implementation.

Third-Party Stakeholder Support:

- The three staking providers with the most validators still on 0x00 (Stakehound, Stakefish, and Staked.us: combined total of 2907 validators) support this EIP and will assist their affected customers accordingly.

---

### Specification

Withdrawal Credentials

- 0x00 - BLS Credential (Deprecated): Publicly exposed and quantum-vulnerable.
- 0x01 - Execution Address Credential: Withdrawal to an Ethereum execution address.
- 0x02 - Compounding Credential (EIP-7251): Supports higher effective balances.
- 0x03 - Post-Quantum Credential (Optional): Withdrawal protected by a post-quantum cryptographic signature.

Credential Update Mechanism (in Support of Migration Framework)

- A new EL function will allow the first deposit address to:

function requestCredentialUpdate(uint64 validatorIndex, bytes32 newCredential) payable

- Only the recorded DepositOrigin can call this function.
- A challenge period (~27 hours) ensures that a valid BLS key can override the deposit-origin update if still available.

Hard Fork Requirements

- The fallback recovery mechanism is activated only after a hard fork that deprecates 0x00 credentials and enables PQC credential usage.
- No new validators using 0x00 credentials will be accepted post-fork.

---

### Rationale

- Fairness and Decentralization:

The original depositor is on-chain and verifiable without introducing custodians.
- Validators had fair warning and multiple avenues to protect themselves.

Security and Risk Mitigation:

- Prevents mass validator loss in a future quantum attack.
- Rescues locked funds without complex social recovery or subjective interventions.

Edge Case Awareness:

- Special caution is noted for validators funded through shared deposit mechanisms.

---

### Security Considerations

- Quantum Resistance: Migration to 0x01, 0x02 or 0x03 prevents reliance on quantum-vulnerable cryptography.
- Key Compromise: Emphasizes urgency for validators to secure or migrate their credentials.
- Validator Recovery: Safeguards both network security and individual validator funds.

### Community Support

This EIP incorporates feedback received from the ETHStaker community (Valefar, Yorick Downe), Ethereum core developers (Potuz, Benjamin Chodroff), and major staking providers (Stakehound, Stakefish, [Staked.us](http://Staked.us)). Their guidance helped refine the fallback recovery model and validate its fairness.

---

### Security Considerations

The Execution-Layer Recovery, combined with post-quantum credential options, ensures Ethereum’s validator set remains secure, decentralized, and resilient against quantum threats. The proposed changes allow Ethereum to gracefully deprecate BLS withdrawal credentials and recover lost validators fairly, requiring a consensus-layer hard fork.

---

### References

- EIP-7002: Action Initiation from the Execution Layer to the Consensus Layer
- EIP-7804: Withdrawal Credential Update Functions
- EIP-4736: Consensus Layer Withdrawal Protection

## Replies

**vshvsh** (2025-05-08):

My impression here is this proposal is mostly motivated by lost keys, not quantum risk. Proposal in the same vein as has been pushed by what seems to be Stakehound or Fireblocks’ associated people previously.

Quantum risk can be mitigated by the same way it’s probably going to be mitigated on execution layer - by not allowing validation or fund recovery without proof of having mnemonics for the BLS key. Which is really bad for people who lost mnemonics but is probably inevitable for execution layer’s lost or dormant funds, so making in exception for stakers has to have additional motivation, IMO.

I’d be in favor of this larger stakers with lost credentials (e.g. Stakehound’s and maybe Stakewise/Staked clients?) would pitch in to help transition to quantum resistance, not piggyback on it.

---

**benjaminion** (2025-05-08):

Could you elaborate on why BLS withdrawal credentials are considered vulnerable to quantum computing attacks?

The only public commitment is the hash of the withdrawal public key, rather than the public key itself. Afaik this is enough to prevent useful quantum attacks.

I am not an expert in QC, however; it is a genuine question. Nevertheless, I think we will have much more significant problems than this if/when quantum computers can break BLS cryptography.

---

**vshvsh** (2025-05-08):

Also a good point; they become vulnerable when there’s a message to rotate the credentials to 0x01 which means lost credentials are not a quantum risk unless there exists a message signed by them when they were not yet lost. This is very unlikely for regular staker, but pretty likely for advanced threshold BLS setup a-la Stakehounds’ - they had to test the setup, after all.

---

**maverickandy** (2025-05-08):

Thanks for your time and thoughts - much appreciated!

For the record: I’m not affiliated to Stakehound/Stakefish/Staked.us; merely a pre-genesis staker (9213, 9219, 9226, 9228) that was foolish enough to write down the testnet mnemonics instead of the mainnet mnemonics. Very stupid, yes. And yes, this is also motivated by lost keys.

However, when the hardfork to PQC signatures happens in the future, this would provide a once-in-a-lifetime opportunity to help the right people in our community get their funds back AND preemptively reduce the network’s quantum attack surface.

These are people that started staking when everything was still very experimental and have supported Ethereum for long periods of time. With little to no risk involved, is this then not the ideal time and solution?

---

**maverickandy** (2025-05-08):

Thanks for your time and thoughts as well - much appreciated!

You are right. Shor’s algorithm requires the actual exposed public key to compute the private key. Also appreciate that there are more significant problems to solve however as mentioned above: this might be the only opportunity left for validators that have lost their mnemonics. The hardfork will have to happen nonetheless.

Rough estimate is that there are 2000-2500 validators with lost mnemonics. Many of whom are solo stakers.

---

**kladkogex** (2025-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickandy/48/11806_2.png) maverickandy:

> Quantum Risk: BLS public keys are exposed at deposit and could be broken by future quantum computers.

Well, we may need wait  hundreds of years until the attacks a feasible

---

**cadillion** (2025-05-30):

FWIW, there are already post-quantum smart accounts on Ethereum mainnet (eg Quip Network, Anchor Wallet), one could easily designate such a smart account as the withdrawal address without requiring a hard fork.

Obviously this does not solve the key recovery issue or validator griefing attacks that attest malicious chain histories or DoS the validator, but it would be a workable solution that’s available today without any fork.

For example, the Quip Network hash library uses WOTS+ built on keccak, and the ethereum-sdk library handles swapping out one-time signatures and synchronizing your local hashchains with the onchain state. If a quantum attacker stole your validator key and withdrew to the Quip account, they would not have the Winternitz signature required to exfiltrate the funds to a new address.

---

**smart511** (2025-11-03):

As a solo validator who lost his ability to set 0x01 from 0x00 i’m looking at this with a lot of interest.

Meanwhile, I guess the validator needs to keep running to avoid it going to 0 eth?

---

**maverickandy** (2025-11-19):

I’ve put together a public dashboard that tracks the progress of deprecating BLS withdrawal credentials, including an overview of the ecosystem state and a proposed recovery mechanism for affected validators.

You can check it out here: **[deprecatebls.com](http://deprecatebls.com)**

Creating your signature and adding it to the dash would be very helpful. Other feedback is very welcome.

