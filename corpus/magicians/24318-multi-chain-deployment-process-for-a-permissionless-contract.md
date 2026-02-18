---
source: magicians
topic_id: 24318
title: Multi chain deployment process for a permissionless contract factory
author: rmeissner
date: "2025-05-23"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/multi-chain-deployment-process-for-a-permissionless-contract-factory/24318
views: 837
likes: 34
posts_count: 11
---

# Multi chain deployment process for a permissionless contract factory

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1052)














####


      `master` ← `safe-research:permissionless_factory`




          opened 08:14AM - 23 May 25 UTC



          [![](https://avatars.githubusercontent.com/u/2896048?v=4)
            rmeissner](https://github.com/rmeissner)



          [+330
            -0](https://github.com/ethereum/ERCs/pull/1052/files)













This ERC proposes a permissionless method to deploy a universal CREATE2 factory contract to a deterministic address (`0xC0DE8E984dF1846E6AdE500972641ce0a9669e1b`) across EVM-compatible chains. It leverages EIP-7702 and a publicly known private key to initiate the deployment.

This approach aims to overcome limitations of current methods, specifically the reliance on transactions without EIP-155 replay protection, guarded private keys, or chain-specific preinstalled contracts. This makes the mechanism both more permissionless and error resistant compared to existing CREATE2 factory deployments. However, while it does suffer from potential front-running attacks may cause delays and gas griefing, they cannot permanently prevent the factory’s deployment to the expected address.

The ERC specifies exact parameters for the CREATE2 factory, to ensure a single, universal CREATE2 factory for the community.

Edit:

More information and tooling can be found on the related Safe Research repo: [GitHub - safe-research/permissionless-create2: Permissionless CREATE2 Factory](https://github.com/safe-research/permissionless-create2)

Edit:

Official ERC link is here: [ERC-7955: Permissionless CREATE2 Factory](https://eips.ethereum.org/EIPS/eip-7955)

## Replies

**pcaversaccio** (2025-05-23):

Some caveats coming from the guy who deployed [CreateX](https://github.com/pcaversaccio/createx) on over 150 chains (cannot recommend lol):

- This entire approach hinges on the assumption that the new transaction type 4 will be supported by all target chains. This approach scales well until you go beyond the standard EVM chains; example Linea is still running on london. The rollout of this EIP is probably best if the rollout of EIP-7702 has happened almost everywhere; but even then you probably cannot support more exotic use cases like Filecoin with their own EVM-compatible but not EVM-equivalent engine (I doubt they will upgrade to this tx type, but who knows). The fundamental question is: how much do we care about the exotic world of EVM-compatible but not EVM-equivalent world? I personally care and thus have chosen the “private key as backup” method for CreateX, which is definitely suboptimal.
- You can have scenarios where EVM chains support transaction type 4 but e.g. not PUSH0. So if the CREATE2_FACTORY_INIT_CODE contains not supported opcodes, this can lead to scenarios where you would face contract creation failures.

That being said, I personally like the idea of the ERC overall. Based on my practical experience, I can envision already a couple of practical issues that can break the scalability of this proposal.

---

**frangio** (2025-05-23):

The only issue I see with this scheme is that it stops working in a post-quantum scenario where ECDSA keys are deactivated. However, if you keep the seed private (and safe for however many decades) it could probably just downgrade to the “secret private key” solution (assuming [something like this](https://ethresear.ch/t/how-to-hard-fork-to-save-most-users-funds-in-a-quantum-emergency/18901) is implemented).

Ideally I think multi-chain deployments should be provided as a native feature of the chain, but this is a great solution as long as we don’t have that.

---

**rmeissner** (2025-05-26):

I agree that having a native feature on chains is the preferred way. The Safe team (and also [@pcaversaccio](/u/pcaversaccio)) are trying to get as many of the L2 providers to include them as pre-deployments for now.

> if you keep the seed private

As the private key is publicly known (as part of the ERC) this shouldn’t bee an issue.

> in a post-quantum scenario

Also agree here that with changes introduced to Ethereum related to Quantum Security will most likely trigger a lot of follow up changes. Lets see when this happen ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**nlordell** (2025-05-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> You can have scenarios where EVM chains support transaction type 4 but e.g. not PUSH0. So if the CREATE2_FACTORY_INIT_CODE contains not supported opcodes, this can lead to scenarios where you would face contract creation failures.

Good point. We can use something like the `RETURNDATASIZE` opcode to push a 0 onto the stack to make things more compatible.

---

**nlordell** (2025-05-27):

In the latest version of the ERC, we changed the code to use `RETURNDATASIZE` for pushing 0’s to remove the dependency on EIP-3855 (i.e. `PUSH0`). So it should be more portable now.

---

**SamWilsn** (2025-07-15):

Why not use Nick’s method to create the signature for the delegation? Then you don’t have to worry about a future opcode permanently deploying code to the deployer account.

---

**nlordell** (2025-07-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Why not use Nick’s method to create the signature for the delegation?

You run into a chicken-and-egg problem. Specifically, the delegation signs over `MAGIC || rlp([chain_id, address, nonce])`, so while `MAGIC`, `chain_id` (set to 0 for a chain-agnostic delegation) and `nonce` (set to 0 by nature of Nick’s method) can all trivially set to fixed values, `address` cannot. You would have to have a way to deploy the target “bootstrapping” contract to the same address on all chains, which brings us back to the original problem.

I will add a blurb under the “Rationale” section to clarify this.

**Edit**: added a section to the “Rational” section in the ERC PR to explain this.

---

**SamWilsn** (2025-07-18):

Ah, yep. That makes perfect sense.

---

**nlordell** (2025-08-15):

[@frangio](/u/frangio) - I updated the CREATE2 factory to propagate revert messages in the ERC: [Update ERC-7955: Propagate CREATE2 Reverts by nlordell · Pull Request #1174 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1174)

---

**duncancmt** (2025-12-11):

This trick doesn’t work on Monad because it doesn’t allow delegated EOAs to `CREATE2` [EIP-7702 on Monad | Monad Developer Documentation](https://docs.monad.xyz/developer-essentials/eip-7702#delegated-contract-code-cannot-call-createcreate2)

