---
source: magicians
topic_id: 9010
title: "EIP-5027: Unlimit contract code size"
author: qizhou
date: "2022-04-21"
category: EIPs
tags: [shanghai-candidate, size-limit]
url: https://ethereum-magicians.org/t/eip-5027-unlimit-contract-code-size/9010
views: 3156
likes: 4
posts_count: 12
---

# EIP-5027: Unlimit contract code size

---

## eip: 5027
title: Unlimit contract code size
author: Qi Zhou
discussions-to: TBD
status: Draft
type: Standards
Track category: Core
created: 2022-04-21
requires: EIP-170

## Abstract

Unlimit the contract code size so that users can deploy a large-code contract without worrying about splitting the contract into several sub-contracts.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5027)














####


      `master` ← `qizhou:qizhou-code-size`




          opened 07:33PM - 21 Apr 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/e/ec489df73b8873547715c8a2f21986ca2b83d33c.jpeg)
            qizhou](https://github.com/qizhou)



          [+319
            -0](https://github.com/ethereum/EIPs/pull/5027/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/5027)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**SamWilsn** (2022-04-29):

I think you’re going to get a ton of pushback from core devs on this. I’d recommend bringing this up in the Eth R&D discord to gather some consensus before going forward with standardization.

---

**ramvi** (2022-04-30):

This is not an argument against your proposal, just a note for any developer wanting to deploy large-code contracts:

Aribtrum allows for unlimited contract code size.

You can get the Ethereum security (Arbitrum is a Layer 2) with an inifite contracted size **today**.

---

**qizhou** (2022-05-02):

Glad to know that Arbitrum has already enabled this.  Out of curiosity, I am wondering if Arbritum has a customized `solc` to support this feature.  I know that current `solc` will stop compilation if the contract size exceeds 24KB.

---

**qizhou** (2022-05-02):

Thanks for the suggestion.  Just joined!

---

**shemnon** (2022-05-27):

Because the EIP does not give any considerations to the security rational explained in [EIP-170](https://eips.ethereum.org/EIPS/eip-170) (where the restriction was imposed) nor explanation for why those concerns are either mitigated or no longer valid I feel it should be tabled until such details are added and accepted.

---

**qizhou** (2022-05-30):

Thanks for the comment.  Introducing proper gas metering adjustment to avoid possible attacks in EIP-5027 is to address the issue found in EIP-170, especially

> O(n) cost in terms of reading the code from disk, preprocessing the code for VM execution.

The basic idea of gas metering is to treat calling a contract with size > 24K as that of calling multiple contracts with size <= 24K.  E.g., calling a contract with size 24K + 1 will charge the gas as calling two contracts (2 * 700 gas).

Further, to avoid DoS attack, EIP-5027 recommends implementing a mapping from codehash => codesize at the client side, so that EVM can pre-charge the gas of calling a potentially-large contract with `O(1)` KV get cost.  This should eliminate the DoS attack considered in EIP-170 without changing the current Ethereum state structure.

All of above will be presented to AllCoreDev meeting.  Free to let me know if you have further comments.

---

**shemnon** (2022-05-30):

(a) this rationale belongs in the EIP.

(b) “preprocessing the code for VM execution” is a separate concern from “reading the code from disk.”  This needs separate exposition as the attacks are unique to EVM preprocessing.

---

**qizhou** (2022-05-30):

(a) We are collecting the feedback from ACD to complete the Rationale and Security Consideration subsections, but the current rationale should be a minimal version to illustrate the idea.

(b) Preprocessing is basically the JUMPDEST-analysis of the EVM code, which is part of the 700 call gas to my understanding.

However, looks like the current JUMPDEST-analysis of the EVM code is not correctly metered, and EIP-3860 is tracking that ([EIP-3860: Limit and meter initcode](https://eips.ethereum.org/EIPS/eip-3860)).

---

**shemnon** (2022-05-30):

My weakly held position is that any adjustments to how contracts are costed and sized for creation should be done in conjunction with the other EOF related changes and should require a contract in an EOF container.  Legacy code deployment should remain unadjusted.

Increased contract size would be a nice incentive for developers to switch over to EOF containers.

---

**k06a** (2022-06-21):

Strongly support this idea

---

**axic** (2024-12-02):

FYI the EIP was merged as [EIP-5027: Remove the limit on contract code size](https://eips.ethereum.org/EIPS/eip-5027)

