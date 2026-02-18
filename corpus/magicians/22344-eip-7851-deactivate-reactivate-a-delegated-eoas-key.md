---
source: magicians
topic_id: 22344
title: "EIP-7851: Deactivate/Reactivate a Delegated EOA's Key"
author: colinlyguo
date: "2024-12-27"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7851-deactivate-reactivate-a-delegated-eoas-key/22344
views: 459
likes: 17
posts_count: 15
---

# EIP-7851: Deactivate/Reactivate a Delegated EOA's Key

Discussion topic for EIP-7851

#### Update Log

- 2024-12-27: initial draft
- 2025-01-13: multiple fixes and refinements
- 2025-02-01: multiple fixes and refinements
- 2025-02-25: multiple fixes and refinements

#### External Reviews

None as of 2024-12-27.

#### Outstanding Issues

None as of 2024-12-27.

## Replies

**colinlyguo** (2025-01-12):

Strong thanks to [@jochem-brouwer](/u/jochem-brouwer) and [@thegaram33](/u/thegaram33) for the valuable reviews of the draft PR.

Here’s a summary of some open discussions for broader visibility:

1. Extra Storage Read During Transaction Validation
This EIP introduces an account code read during transaction validation when txpool is adding new transactions as noted in this discussion. Alternatives include:

Adding a new Boolean field in the account state.
2. Encoding the “active/deactivated” status into the nonce.
3. Concerns About Reactivation
Concerns (e.g., comment link) that users might not keep their private keys secure after deactivation. Possible solutions:

Users need to keep and back up their private keys as they used to. Nothing changes after they are deactivated since the main purpose is safeguarding the delegated EOA in one chain instead of deactivating the private key globally in a multi-EVM-compatible chains ecosystem.
4. Not supporting private key reactivation.
5. Allowing redelegation through a precompiled contract instead of supporting private key reactivation.
6. Permit Extension
The permit extension concern is mentioned in the relevant section of this EIP and also in this X post. Possible solutions:

Modify ecRecover precompile to check the deactivated status and if the recovered address is deactivated: return a precompile contract error (or, if not adding an error return, return a zero address or a designated magic address).
7. Trace transactions and check if the Permit function is invoked, if so, check the signer’s deactivated status, this solution would like to introduce a heavy check for clients.
8. The contracts upgrade the implementation and deactivate the Permit function. However, some ERC-20 contracts cannot be upgraded.

---

**kopykat** (2025-01-15):

I believe another issue that needs to be addressed is the behavior of `ecrecover`, specifically expected behavior should be that it doesn’t work anymore if the pk is deactivated, right?

---

**colinlyguo** (2025-01-15):

Interesting. also have considered this, This method also sounds promising to address the **Permit Extension** issue listed above. since `Permit` usually utilizes `ecrecover` to verify EOA’s signature. while when I first thought of changing the behavior of `ecrecover`, it may be a bit unintuitive since this precompile does not do a “single job” (signature recovery) anymore. not sure. it’s worth discussing. so you think it’s more natural to consider the “deactivated” status in `ecrecover`? any considerations?

btw, I added the possible solutions in the previous **Permit Extension** issue session.

---

**kopykat** (2025-01-15):

yes I definitely agree on this making `ecrecover` more complex (and stateful). however, to me relying on contracts to implement correct behaviour (ie checking codesize and doing 1271 before `ecrecover`) feels hacky and not like a fully complete solution

---

**jxom** (2025-01-15):

Totally agree with [@kopykat](/u/kopykat) here! Definitely think it would be worthwhile to restrict EOA signatures  as without it, an attacker could work around this EIP.

---

**Arvolear** (2025-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kopykat/48/9235_2.png) kopykat:

> I believe another issue that needs to be addressed is the behavior of ecrecover

I am not sure this has to be addressed. Anyone can implement ECDSA signature verification natively in Solidity. Yes, this would be more expensive, but changing `ecrecover` behavior introduces a leaky abstraction that doesn’t fix the problem completely.

---

Nevertheless, the deactivation concept sounds really cool to me as it relaxes the “god mode” access of delegated multisigs.

---

**kopykat** (2025-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Anyone can implement ECDSA signature verification natively in Solidity.

yes this is a good point. you’re completely right that there’s no way to modify ECDSA to conform to this behavior.

however, I understand this proposal to be about making it possible to activate/deactivate a private key from the perspective of the EVM. currently, this includes mainly transactions (with the exception of addressing permit-based systems), but to me it feels like this change should also address any out-of-the-box features the EVM provides for ECDSA operations, namely `ecrecover`.

---

**Arvolear** (2025-01-16):

You know, `ecrecover` still accepts signatures with `S` values from both halves of the curve, while transaction can only be sent with `S <= N / 2` (EIP-2). So this distinction has already been done before ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12).

---

**colinlyguo** (2025-01-31):

I merged [a new PR](https://github.com/ethereum/EIPs/pull/9302) based on some newly found fixes, recent EIP-7702 updates, and discussions in this thread, summarization of changes is as follows:

- Adding fact fixes in the “Additional Transaction Validation Overhead” section, because due to EIP-3607 and EIP-7702, there is already a code loading operation during transaction validation before executing the transaction, so this EIP introduces no additional code loading in this step. This EIP only introduces an extra code read when the transaction pool is validating a transaction to be added to the pool, narrowing DoS attack vectors.
- Changing PRECOMPILE_GAS_COST from 5000 to 13000, and adding gas cost decomposition of PRECOMPILE_GAS_COST.
- Adding more details and potential solutions in the “Contracts Using ECDSA Secp256k1 Signatures” section, aligning with the discussion in this thread.
- Adding “how a contract can check the deactivation status of private key” as it is now doable without adding a new opcode, based on the latest change of EXTCODESIZE and EXTCODECOPY in EIP-7702.
- Removing “delegating to malicious wallet implementations” related discussions, as it is in the scope of EIP-7702, instead of this EIP.
- Adding “replaying the same authorization” discussions in the “Deactivation and Reactivation Replay” section.
- Rephrases, section restructures and code refactors.

---

**rdubois-crypto** (2025-03-12):

There is a motivation for this EIP in the context of Post Quantum crypto. If one can deactivate its eoA prior to Quantum computing, then 7702 can be used for PQ migration. Otherwise it is possible for the quantum attacker to take control of the account via the EOA. This include the ‘Keyless’ Nicks technique, where quantum computing can recover the private key, which is impossible when ECDLP holds.

We used 7702 delegation to FALCON for testing purpose, but it has no real meaning while 7851 is not enforced.



      [github.com](https://github.com/ZKNoxHQ/ETHFALCON)




  ![image](https://opengraph.githubassets.com/04a65b05ca5543b655127e2b140bc971/ZKNoxHQ/ETHFALCON)



###



Study and implementation for the ETHEREUM ecosystem

---

**ArikG** (2025-03-12):

It solves some of the issues for PQ but not all of them because of the possibility of signing messages using the EOA and using them in any contract that does not check ERC-1271 signatures first. So you are only quantum secure against contracts that also apply a flow that is compatible. Is there an ERC that enforces this mechanism today? If not, then maybe EIP-7851 needs a companion ERC that will do the following flow:

1. If contract code exists, check 1271 signature only
2. Otherwise, check ecRecover on address
With these 2 things you might be able to operate in a pq protected environment by only signing proper 712 messages.

Maybe also something can be done to identify compatible 712 messages using the domain separator or something like that

---

**colinlyguo** (2025-03-26):

Thanks for the feedback from practice. Yeah, that’s one of the motivations of this EIP, will add it explicitly in the next refinement.

---

**colinlyguo** (2025-03-26):

Thanks. It’s a valid concern and good suggestion. From my point of view, no matter the signature types. e.g. EIP-712, ERC-1271, etc. A new ERC can be added to support signature verification based on the EOA private key’s active/inactive statuses (may not be mandatory, but providing compatibility support). e.g., for ERC-1271, when it comes to an ECDSA signature, the contract should check the status of this EOA private key first (EIP-7851 supports on-chain checks by checking EXTCODESIZE of the address), such checks are not mandatory, they can be enabled by a flag in the signer list of the contract, based on the contract’s actual use scenario.

For the off-chain services, this EIP also provides a way to check if the private key is disabled or not. They can also add optional hooks before signature validation based on security considerations.

Another issue is that there are some ERC20 contracts which support [ERC-2612](https://eips.ethereum.org/EIPS/eip-2612), the `permit` function. e.g., DAI. The ERC to support EIP-7851 above cannot add checks in existing contracts (if they cannot be upgraded). One aggressive method is to modify the `ecrecover` precompile to check the private key’s activation status first. Some pushbacks are: (i) this will make this precompile stateful; (ii) this still cannot defend cases where ECDSA signature verification is implemented in other methods, e.g., self-implemented by Solidity. Thus I’m still hesitant if it’s proper to add this change into this EIP.

---

**rdubois-crypto** (2025-12-01):

Yes, and this is better that no contract at all.

For now not having the ability to deactivate means all effort in this direction are meaningless.

