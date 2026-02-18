---
source: magicians
topic_id: 23266
title: "ERC-7920: Composite EIP-712 Signatures"
author: ogunsakin
date: "2025-03-25"
category: ERCs
tags: [eip-712]
url: https://ethereum-magicians.org/t/erc-7920-composite-eip-712-signatures/23266
views: 203
likes: 4
posts_count: 8
---

# ERC-7920: Composite EIP-712 Signatures

[![erc-7920](https://ethereum-magicians.org/uploads/default/original/2X/0/010d58c821ad87a3b0d9253bf51faf18fe63306d.png)erc-7920577×360 35.9 KB](https://ethereum-magicians.org/uploads/default/010d58c821ad87a3b0d9253bf51faf18fe63306d)

## Pull Request



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/993)














####


      `master` ← `sola92:master`




          opened 05:03PM - 25 Mar 25 UTC



          [![](https://avatars.githubusercontent.com/u/1865667?v=4)
            sola92](https://github.com/sola92)



          [+1076
            -0](https://github.com/ethereum/ERCs/pull/993/files)







This EIP provides a scheme for signing multiple typed-data messages with a singl[…](https://github.com/ethereum/ERCs/pull/993)e signature by encoding them into a Merkle tree. Allowing individual messages to be verified without requiring full knowledge of the others.

![eip-tbd](https://github.com/user-attachments/assets/8b73583d-3416-471c-ae4a-b4ce26176f80)












## Reference Implementation



      [github.com](https://github.com/sola92/composite-712)




  ![image](https://opengraph.githubassets.com/ab32a482986187e4cba0e14f463c2c87/sola92/composite-712)



###



Reference implementation and tests for ERC7920

## Replies

**hellohanchen** (2025-04-01):

Very interesting proposal!

Can the data be composite at multiple layers, like `[[x₁, x₂, ..., xₙ], [y₁, y₂, ..., yₙ]]`?

And what’s the actual gas cost for a specific number of messages (n)?

---

**ogunsakin** (2025-04-01):

[@hellohanchen](/u/hellohanchen) thanks for the review!

Currently the messages must be flattened for signature: `[x₁, x₂, ..., xₙ]`.

Gas cost for verification? Thats a good question I can run a test to find out. Runtime should be `log(n)` number of messages, if the tree is properly constructed.

---

**hellohanchen** (2025-04-01):

Thanks for replying. I currently don’t have a great use case for this but this is interesting. Signature and validation work should become more flexible to prepare for the future use cases.

I do have some use cases that the signatures need to be layered like

```auto
sig1 = sign(message, key_1)
sig2 = sign(sig1, key_2)
```

And both signatures need to be verified.

---

**dror** (2025-05-06):

Nice idea…

I noticed that signTypedData has a “backward compatibility”, to return a single result.

however, the sample solidity code only uses a merkle-proof, and doesn’t work with a single-entry proof returned by signTypedData_v5

---

**ogunsakin** (2025-05-07):

Hi [@dror](/u/dror), thanks for reviewing.

The proposed schema for `signedTypedData_v5` result is:

```typescript
{
  signature: `0x${string}`; // Hex encoded 65 byte signature
  merkleRoot: `0x${string}`; // 32 byte Merkle root as hex string
  proofs: Array>; // Array of Merkle proofs (one for each input message)
}
```

When `N=1`, the derivation path is an empty array as the sole message is root and `signedTypedData_v5` returns:

```typescript
{
  signature: `>`;
  merkleRoot: `>`;
  proofs: [
   []
  ]
}
```

**During verification**

[_verifyMerkleProof(N=1) = root == leaf](https://github.com/ethereum/ERCs/blob/5580d029fc43c7cffb1300788fe5db0bc7f386eb/assets/erc-7920/contracts/ExampleVerifier.sol#L84)

Simplifying check to

```solidity
isVerified = isValidSignature && root == leaf
```

Here is a unit test for this case: [ERCs/assets/erc-7920/test/solidity.test.ts at 5580d029fc43c7cffb1300788fe5db0bc7f386eb · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/blob/5580d029fc43c7cffb1300788fe5db0bc7f386eb/assets/erc-7920/test/solidity.test.ts#L99)

---

**dror** (2025-05-07):

ok, so just to verify:

I can take a “standard” signTypedData result, and pass it as “root” with an empty merkle proof, and it will succeed. right ?

---

**ogunsakin** (2025-05-07):

Hi [@dror](/u/dror), here’s what verification would look like with a `signedTypedData_v4` result

```auto
isVerified = isValidSignature(fullSig) && _verifyMerkleProof(messageHash, [], messageHash)
```

This would always evaluate as `true`

```auto
_verifyMerkleProof(messageHash, [], messageHash)
```

Leaving

```auto
isVerified = isValidSignature(fullSig)
```

