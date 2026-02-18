---
source: magicians
topic_id: 15999
title: "EIP 7530: EVM Profiles to enable decentralized sequencers for zk Rollups"
author: drinkcoffee
date: "2023-10-05"
category: EIPs
tags: [evm, rollups]
url: https://ethereum-magicians.org/t/eip-7530-evm-profiles-to-enable-decentralized-sequencers-for-zk-rollups/15999
views: 1540
likes: 7
posts_count: 15
---

# EIP 7530: EVM Profiles to enable decentralized sequencers for zk Rollups

From the [draft EIP 7530](https://github.com/ethereum/EIPs/pull/7809):

## Abstract

This EIP defines a set of EVM Profiles. Each profile describes how the Ethereum Virtual Machine (EVM) should operate when configured with the profile. The profile specifies that some EVM opcodes and precompiles should operate in the usual way, whereas other opcodes and precompiles operate differently, for example reverting.

## Motivation

Blockchains that use deterministic finality consensus protocols can be used as decentralized sequencers in zero knowledge rollup systems, as shown in the figure below.

[![architecture](https://ethereum-magicians.org/uploads/default/optimized/2X/5/54b55717e45e41176358548f832faf73ce016b88_2_690x121.png)architecture1602×282 14.5 KB](https://ethereum-magicians.org/uploads/default/54b55717e45e41176358548f832faf73ce016b88)

The L2 blockchain acts as a decentralized sequencer, defining an ordered list of transactions, and the resulting state changes produced by executing those transactions. Finalised transactions and related state changes are consumed by zero knowledge provers. The provers generate proofs that show that executing the transactions results in the state changes. The proofs can be verified in verifier smart contracts on Ethereum.

In the system described in the previous paragraph there are three Ethereum Virtual Machines: the EVM executing in the L2 blockchain clients and the EVM processor in the zk prover, and the EVM in the L1 blockchain (Ethereum). The EVM in the L2 blockchain clients and the EVM in the zk prover must operate in precisely the same way for the proof to be able to be verified in the verifier smart contract.

Several “EVM compatible” zero knowledge proof systems are available at time of writing (October 2023). However, each prover has implemented a slightly different set of opcodes and precompiles, and has different behaviour for opcodes and precompiles that are not supported.

The purpose of this EIP is to define a standard set of opcodes and precompiles must be supported and the behaviour for unsupported opcodes and precompiles. The goal is to allow any blockchain client configured with this profile to be connected to any prover configured with this profile to create a workable zero knowledge rollup system with a decentralised sequencer.

## Replies

**drinkcoffee** (2023-10-05):

I have created two profiles. Profile A matches Type 1 zk rollups and Profile B matches Type 3 zk rollups that have no gas changes.

---

**WhileyDave** (2023-10-05):

Hi Peter, so how did you arrive at these two profiles?  For some reason, I might have expected profiles with more extensive changes.  For example, some which alter the `KECCAK256` bytecode.

---

**WhileyDave** (2023-10-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/drinkcoffee/48/1850_2.png) drinkcoffee:

> The two EVMs must operate in precisely the same way for the proof to be able to be verified in the verifier smart contract.

Not sure I agree this is strictly necessary.  Of course, it would be ideal.  But, the system will work fine if the EVMs differ.  For example, I imagine scenarios where the client EVM is running the latest fork, and the zkEVM is running an older fork.  I definitely agree that its important to be clear what exactly the zkEVM does and does not support.

---

**drinkcoffee** (2023-10-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/whileydave/48/8535_2.png) WhileyDave:

> so how did you arrive at these two profiles?

I had a look at what Polygon zkEVM (Hermez) and ConsenSys Linea said they supported, and used that as a starting point.

---

**drinkcoffee** (2023-10-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/whileydave/48/8535_2.png) WhileyDave:

> I might have expected profiles with more extensive changes. For example, some which alter the KECCAK256 bytecode.

The smaller the number of changes, the better.

For KECCAK256, it is used extensively in EVM code. Within the Solidity language complex data types like mapping use keccak256. Within contracts using Solidity, keccak256 is used to derive id numbers and other such values. It could be imagined that off-chain code could calculate the same number. To ensure these applications don’t need to be re-written when they transition from L1 to L2, the keccak256 opcode needs to operate in the same way.

The reason for the precompiles in Profile B being not supported is that they are rarely used. That is, not never in no contract, but not in the vast majority of contracts. Prover teams have found those precompiles complex to implement. Hence, rather than just have Profile A, Profile B is also offered.

You can think of Profile A matching Type 1 or 2 rollups, and Profile B matching Type 3 rollups that don’t change any gas prices.

---

**drinkcoffee** (2023-10-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/whileydave/48/8535_2.png) WhileyDave:

> But, the system will work fine if the EVMs differ. For example, I imagine scenarios where the client EVM is running the latest fork, and the zkEVM is running an older fork.

If the EVMs were different, the blockchain client would calculate one state root, and the prover would prove that the calculation was wrong. The prover would perceive the state root was wrong because it would be essentially calculating based on a slightly different algorithm; a slightly different EVM.

---

**WhileyDave** (2023-10-06):

> If the EVMs were different, the blockchain client would calculate one state root, and the prover would prove that the calculation was wrong

Right I think its a terminology issue here.  When you say “blockchain client” I assumed you meant the L1 blockchain client.  But, now I think you mean L2 blockchain client and are imagining a scenario where the L2 client and prover use different underlying EVMs.  Is that right?

---

**WhileyDave** (2023-10-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/drinkcoffee/48/1850_2.png) drinkcoffee:

> For KECCAK256, it is used extensively in EVM code. Within the Solidity language complex data types like mapping use keccak256.

Right, I understand that.  Still, I could imagine a zkEVM which uses e.g. the Poseidon hash instead of Keccak256.  Anyway, I’m just trying think about specific instructions which might be implemented differently (for some reason).  For example, [CREATE/CREATE2](https://era.zksync.io/docs/reference/architecture/differences-with-ethereum.html#create-create2) differs on zkSync.  `SELFDESTRUCT` I think is another problematic case.

---

**drinkcoffee** (2023-10-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/whileydave/48/8535_2.png) WhileyDave:

> terminology issue here. When you say “blockchain client” I assumed you meant the L1 blockchain client. But, now I think you mean L2 blockchain client and are imagining a scenario where the L2 client and prover use different underlying EVMs. Is that right?

Correct. L2 blockchain clients agree on consensus, the order of transactions and blocks. This runs an EVM. Prover connects to L2 blockchain client, and runs a proof, which in effect is an EVM. Hence, on L2, you effectively have two EVMs running, one to execute the transactions and one to generate the proof.

---

**drinkcoffee** (2023-10-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/whileydave/48/8535_2.png) WhileyDave:

> Anyway, I’m just trying think about specific instructions which might be implemented differently (for some reason). For example, CREATE/CREATE2 differs on zkSync. SELFDESTRUCT I think is another problematic case.

I am happy for you to propose additional profiles, or recommend alterations to the existing profiles. What do you propose?

---

**WhileyDave** (2023-10-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/drinkcoffee/48/1850_2.png) drinkcoffee:

> I am happy for you to propose additional profiles, or recommend alterations to the existing profiles. What do you propose?

Well, I don’t have any specific suggestions!  Just pondering what other differences are out there.  And, I appreciate that having profiles to suit every possible combination of instruction variations is completely impractical!!!  But, maybe there is a shortlist of “problematic” instructions that’s worth considering?

---

**drinkcoffee** (2023-10-09):

[@WhileyDave](/u/whileydave) and [@hmijail](/u/hmijail) , I have added a diagram and improved the description to more clearly differentiate between the L2 blockchain and Ethereum.

---

**shemnon** (2023-10-12):

Have you considered leveraging EOF for any of this?  With the EOF container the profile can be encoded into extra code sections or EOF version to make it clear the EVM code expects to execute in Profile A, Profile B, or Mainnet profile. Some tweaks would be needed in the EVM parsers and executors to allow reading of these extra fields but that seems no more difficult than tracking revert reasons.

---

**drinkcoffee** (2023-10-13):

[@shemnon](/u/shemnon) , thank you for that great idea. No, I had not thought of that.

