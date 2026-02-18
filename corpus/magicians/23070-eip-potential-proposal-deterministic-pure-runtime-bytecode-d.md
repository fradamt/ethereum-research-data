---
source: magicians
topic_id: 23070
title: EIP potential proposal - Deterministic pure runtime bytecode deployment
author: radek
date: "2025-03-05"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-potential-proposal-deterministic-pure-runtime-bytecode-deployment/23070
views: 209
likes: 4
posts_count: 10
---

# EIP potential proposal - Deterministic pure runtime bytecode deployment

I propose to align on the following potential EIP that enables etching of the runtime bytecode onto the derived address by anyone.

I have been thinking about this since the creation of the YAC3F CREATE3 factory ( [GitHub - radeksvarz/yac3f: Yet Another CREATE3 Factory](https://github.com/radeksvarz/yac3f) ) and discussion on Pascal’s and Matt’s CreateX ( [📖 Private Key Management of `CreateX` Deployer · pcaversaccio/createx · Discussion #61 · GitHub](https://github.com/pcaversaccio/createx/discussions/61) ) seeing how the deterministic deployment infra must be over complicated and cost ineffective (e.g. multiple passes of bytecode in calldata).

I also wonder why such an uncomplicated improvement was not put on the table with EIP 7702 and other AA, which would benefit from it for its adoption.

Therefore I am inviting at least [@pcaversaccio](/u/pcaversaccio) + [@mds1](/u/mds1) (CreateX deployments), [@PaulRBerg](/u/paulrberg) + [@zerosnacks](/u/zerosnacks) and others (Foundry and Reth), [@holiman](/u/holiman) and others (Geth), [@mudgen](/u/mudgen) (Diamonds), [@yoavw](/u/yoavw) and others (AA) and anyone to give their opinion / co-author and advocate such EIP.

---

## Abstract

This EIP proposes a new precompile that allows contracts to be created at addresses derived directly from their runtime bytecode. This facilitates deterministic deployments based on code content and enhances the capabilities of externally owned accounts (EOAs), in line with the concepts of EIP-7702.

## Motivation

Deterministic deployments: Addresses the challenge of deploying contracts deterministically across different Ethereum Virtual Machine (EVM) compatible chains, especially when specific deployment factories (e.g. CREATE2, CREATE3) are not available.

Trustless and independent deployments: Allows anyone to deploy the same contract to the identical address across compatible EVM chains.

Enhanced EOAs: Supports the adoption of EIP-7702 enhanced EOAs / Smart accounts.

Reduction of the calldata: Eliminates the need to include initcode, reducing calldata size during deployment and multiple calldata passes when using factories

Improved security: Intrinsically linking code to its address can improve security and limit phishing attempts by making it harder to deploy malicious code under a seemingly benign address.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Precompile Address: yet TBD (example: 0x00000000000000000000000000000000000000ee).

Input Parameters: runtimeBytecode: bytes - The runtime bytecode of the contract to be deployed.

Output Parameters: contractAddress: address - The address of the deployed contract.

### Functionality

Address derivation: The contract address is calculated as the rightmost 20 bytes (160 bits) of the Keccak-256 hash of the provided runtimeBytecode.

Contrary to the CREATE opcode, neither msg.sender, nor sender’s nonce is taken into consideration. Contrary to the CREATE2 opcode neither msg.sender, nor initcode, nor salt are taken into account.

Deployment: The runtimeBytecode is deployed to the derived contractAddress.

**Error handling:**

The precompile should handle errors similarly to the CREATE/CREATE2 opcode.

State changes done by the current context are reverted in these cases:

Not enough gas.

Not enough values on the stack.

The current execution context is from a STATICCALL (since Byzantium fork) or an EXTSTATICCALL (since EOF fork).

Provided runtimeBytecode size is greater than the chain’s maximum runtimecode size.

Collisions of resulting address with the sanctioned range.

Sanctioned address range:

0x0 … 0xff

0x0000000000000000000000000000000000000100 and 0x00000000000000000000000000000000000001ff as defined in EIP-7587

In the case the resulting address is calculated within these ranges, the precompile reverts. Authors of the contract are advised to add an arbitrary byte to the runtimebyteCode as a workaround.

### Gas cost:

Similar to the CREATE opcode with modifications, where init code cost and deployment_code_execution_cost are 0 as there is no initialization code to execute.

The new contract address is added to the warm addresses.

## Rationale

### No initcode

Initcode traditionally serves two primary purposes: initializing contract storage and generating runtime bytecode. However, this precompile is designed to bypass both of these steps. The runtime bytecode is directly provided as input, and the intention is to deploy it without any initial storage setup. This design choice is deliberate, aiming to create contracts with immutable bytecode at addresses derived solely from their code content. Consequently, initcode becomes redundant and irrelevant in this context.

### Precompile

The choice to implement this functionality as a precompile, rather than a new opcode:

Precompiles can be used by all contracts, and EOAs directly. This EIP mitigates the problems with the CREATE2 opcode that led to the need for the CREATE2 factory.

Introducing a new opcode increases the complexity of the core EVM. Precompiles, being external to the core execution engine, minimize the impact on the protocol’s complexity.

## Backwards Compatibility

This EIP introduces a new precompile and does not affect existing contracts or functionality.

## Security Considerations

Immutable code:

Any change to the runtime bytecode, would change the address of the contract.

## Replies

**wjmelements** (2025-03-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> especially when specific deployment factories (e.g. CREATE2, CREATE3) are not available.

If the chain doesn’t have CREATE2, it’s even less likely to have your precompile.

There are already deterministic deployment schemes using CREATE2. Which EVM chains don’t have CREATE2?

---

**radek** (2025-03-08):

Thanks for the good point.

At first I would like not to call it “my” precompile ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> There are already deterministic deployment schemes using CREATE2.

Indeed - I also built that CREATE3 factory using CREATE2 opcode. If you mean CREATE2 Nick’s factory - it has a few drawbacks:

a) chaining CREATE2 opcode is passing initcode several times in the calldata (once from EOA, 2nd time from factory to created address)

b) there is the prebuilt transaction, that needs to pass and not fail to deploy the factory - that is a risk (I remember Gnosis does not have one deployment on some chain due to failed transaction - low gas. That impacted nonce of the factory deployer.

c) It does require a non-EIP155 transaction to get deployed. So for EIP155 compliant chains it requires “nonstandard state-change” to deploy this factory (as it was on Base).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Which EVM chains don’t have CREATE2?

If you mean CREATE2 opcode - I am not aware of any not having that. If you mean Nick’s CREATE2 factory - I remember some CREATE3 projects menitoned Nick’s tx is not deployable on certain chains. Unfortunately I do not remember exactly which ones, as that was almost 2 years ago.

### Regarding the precompile

there are also other options - Anvil/Foundry  has the `setCode` RPC method. Any of such options has some negatives:

- Opcode - not callable by EOA
- RPC method - not callable by other contract

In general I might be wrong in the terminology - it is not to be “precompile of the solidity code”. **The general idea is that calling the certain address with bytecode in calldata would etch such bytecode onto the keccak(runtimecode) derived address.**

I hope it makes more sense now.

---

**radek** (2025-03-11):

Regarding the failed tx of CREATE2 factory deployment - here is some related discussion: [Gnosis Safe: Chiado v.1.3.0 - unsupported base contract - Ethereum Stack Exchange](https://ethereum.stackexchange.com/questions/166500/gnosis-safe-chiado-v-1-3-0-unsupported-base-contract)

IMHO this is a huge risk if you need to ensure the same address for your runtime code on every possible chain.

---

**pcaversaccio** (2025-03-12):

We should move away from precompiles IMHO. Both [EIP-7266](https://eips.ethereum.org/EIPS/eip-7266) (`blake2f` removal) and [EIP-7666](https://eips.ethereum.org/EIPS/eip-7666) (EVM-ify identity precompile) make a solid case for it. Some thoughts:

- ZKStack-based EVMs aren’t fully EVM-equivalent when it comes to CREATE and CREATE2. How do we deal with this?
- No more precompiles. If something is truly essential, it should be either deployed as EVM code or made an opcode (at the risk of a consensus bug which is another discussion).
- Multichain rollouts are a nightmare. Instead of trying to standardise precompiles across an increasingly fragmented ecosystem, it’s better to push for factory contracts as predeploys—like how CreateX is a predeploy (they call it preinstall) on OP Stack.

You write:

> Trustless and independent deployments: Allows anyone to deploy the same contract to the identical address across compatible EVM chains.

`CreateX` is now deployed on 137 chains, is completely stateless and trustless at runtime. How many more do we really need?

My overall biggest challenge here is based on practical experience of being the author of `CreateX`: The truth is that EIPs and keyless deployments don’t scale in such a fragmented world. We have sacrificed the beauty of keyless deployment for a fallback option in `CreateX`, particularly to be future-proof and scalable. As a reminder, there are presigned txs available, but e.g. on Filecoin you need to set 120m gaslimit… - the world is dirty out there and no EIP will solve this problem perfectly across all EVM chains as it requires all EVM chains to upgrade.

---

**pcaversaccio** (2025-03-12):

Also, without going into my major concerns regarding EOF, let me link here a relevant EIP

- EIP-7873: EOF - TXCREATE and InitcodeTransaction type

See the section: [Creator Contract](https://eips.ethereum.org/EIPS/eip-7873#creator-contract-1). They plan to introduce a predeployed Creator Contract.

---

**radek** (2025-03-12):

Thx. And related interesting discussion: [Update EIP-7873: Creator Contract - revert reason & magic value by pdobacz · Pull Request #9391 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9391#issuecomment-2678451413)

From which it looks like the similar bootstrapping address is to be existing for EOF deployments.

IMHO still too much complex comparing to just pure etching on keccak(runtimecode).

---

**thogard** (2025-03-12):

How about something like this?



      [github.com](https://github.com/thogard785/Single-Shot-7702-Verifier/blob/main/SingleShot7702Verifier.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

// By Alex Watts (@ThogardPvP) and based off of the Biconomy PREP design (https://blog.biconomy.io/prep-deep-dive/)
// Per EIP-7702 (https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7702.md).
// Rather than using provable randomness, this design uses a complete lack of randomness to allow verification
// of 7702-ness
// This is a sketched concept - it will not work in prod until updated so that the payload is packed properly.

// The purpose is to verify that a 7702-activated address does not have a knowable private key and is therefore
// immutable. The deployer of the 7702-activated address must know this factory address prior to deployment.
contract SingleShot7702Verifier {
    error UnableToGenerateSignature(uint256 maxAttempts);

    // 7702's magic salt
    uint8 public constant MAGIC = 0x05;

    // 7702's salt for authority's codehash
    bytes3 public constant EIP_7702_CODE_HASH_SALT = bytes3(0xef0100);

```

  This file has been truncated. [show original](https://github.com/thogard785/Single-Shot-7702-Verifier/blob/main/SingleShot7702Verifier.sol)










It has a deterministic address and uses 7702 on top of an EOA with a provably-unknown private key in a way that is trustlessly (and cheaply) verifiable on chain.

---

**pdobacz** (2025-04-10):

Just a side note - the predeployed Creator Contract is being dropped from EIP-7873 and the EOF plan for Osaka ([see PR and some discussion on that](https://github.com/ethereum/EIPs/pull/9593), as it is not absolutely necessary to bootstrap EOF. Its spec is planned to be re-added in a separate EIP or ERC, but would become optional to EOF roll-out.

OTOH you could consider leveraging the `InitcodeTransaction` type from EIP-7873, in order to make the design EOF-compatible, i.e. read the `runtimeBytecode` from there, rather than calldata.

---

**radek** (2025-08-04):

Interesting. Will have to make some tests with that concept.

I can see  only 2 limitations now:

a) requires 7702 → limits projects on which chains to deploy - but that would be the problem with other EIP implementations anyway

b) additional delegation gas for each tx

Hopefully a) will diminish in due time.

Thanks!

