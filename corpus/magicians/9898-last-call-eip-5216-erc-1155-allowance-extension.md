---
source: magicians
topic_id: 9898
title: "[Last Call] EIP-5216: ERC-1155 Allowance Extension"
author: ivanmmurcia
date: "2022-07-11"
category: EIPs
tags: [erc1155, pr-review]
url: https://ethereum-magicians.org/t/last-call-eip-5216-erc-1155-allowance-extension/9898
views: 3497
likes: 6
posts_count: 13
---

# [Last Call] EIP-5216: ERC-1155 Allowance Extension

Hi everyone,

After been discussed in this forum, I created an EIP PR for the initial idea of my draft (https://ethereum-magicians.org/t/working-draft-new-extension-for-erc1155).

I open this topic to discuss here said PR.

In case that I missed some step, feel free to comment and I’ll change it.

Thank you very much.

PR: https://github.com/ethereum/EIPs/pull/5216

## Replies

**ivanmmurcia** (2022-09-05):

UPDATE: This EIP is now in Last Call.

I need the help of the community so feel free to check it, test the code and find bugs. Let’s discuss about the implementation and move it forward.

Thank you in advance!

EDIT.- This is the EIP: [EIPs/eip-5216.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-5216.md)

---

**xinbenlv** (2022-11-03):

Hi [@ivanmmurcia](/u/ivanmmurcia) thanks for the EIP-5216

QQ: why is `approve` disallowing the caller to be the operator?

---

**ivanmmurcia** (2022-11-05):

Hi [@xinbenlv](/u/xinbenlv), thanks for your feedback.

I have realized that reversing a call because of this check is silly, and also reviewing the OZ’s ERC-20 `_approve` function implementation, I have seen that what I should check instead, is that neither the owner nor the operator are zero address:

```auto
require(owner != address(0), "ERC20: approve from the zero address");
require(spender != address(0), "ERC20: approve to the zero address");
```

What do you think?

---

**xinbenlv** (2022-11-08):

That sounds good. Can you create a new PR to update the spec accordingly?

---

**ivanmmurcia** (2022-11-11):

Of course, I’m on my way. Thanks dude!

EDIT: [Update EIP-5216 with zero address control in _approve function like EIP-20 by ivanmmurciaua · Pull Request #5917 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5917) here is the PR ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**joestakey** (2022-11-12):

Hi [@ivanmmurcia](/u/ivanmmurcia) , love this EIP, the lack of a proper approval pattern is a big problem with ERC-1155, this EIP will definitely help to make it a more robust standard.

A couple things regarding the reference implementation:

1-The proposal states `safeTransferFrom` *MUST Subtract the transferred amount of tokens from the approved amount if msg.sender is not approved with setApprovalForAll*

But in the reference implementation, the allowance is decremented in all cases. In the case of an operator being `approvedForAll`, this means `_allowances[from][msg.sender][id]` can underflow and lead to an allowance being silently inflated.

You can add a check before decrementing:

```diff
        require(
            from == msg.sender || isApprovedForAll(from, msg.sender) || allowance(from, msg.sender, id) >= amount,
            "ERC1155: caller is not owner nor approved nor approved for amount"
        );
+       if (from != msg.sender && !isApprovedForAll(from, msg.sender)) {
        unchecked {
            _allowances[from][msg.sender][id] -= amount;
        }
+       }
        _safeTransferFrom(from, to, id, amount, data);
```

2-There is a tiny logic issue in `safeBatchTransferFrom`: The error string line 89 in `safeBatchTransferFrom` will never be reached, because`_checkApprovalForBatch` never returns false, it either returns true or reverts line 111 if one of the ids to be transferred does not have sufficient allowance.

You can amend the `_checkApprovalForBatch` so that it returns false instead of reverting if the allowance is not enough.

```diff
-            require(allowance(from, to, ids[i]) >= amounts[i], "ERC1155ApprovalByAmount: operator is not approved for that id or amount");
+           if (allowance(from, to, ids[i]) < amounts[i]) {
+               return false;
+           }
            unchecked {
                _allowances[from][to][ids[i]] -= amounts[i];
                ++i;
            }
```

---

**ivanmmurcia** (2022-11-14):

Hey [@joestakey](/u/joestakey), thanks for the great feedback.

1- Yes totally, and I’ve detected this but in my defense I have to say that I wrote the reference implementation and the testing suite in 0.8.15, i.e the compiler avoids the underflow you’ve said… however, this EIP could be implementated in any version of Solidity, so I’ll change.

2- Was my mistake, I only checked that everything worked fine and reverted with the appropiate message but was a tiny logic issue, changed ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

Cheers!

---

**dcota** (2023-12-16):

What is the latest status on this EIP?

Can the title be simplified to `ERC1155Allowance`.

Imo it would be less verbose than `ApprovalByAmount`.

Anyone who knows the 1155 spec will know this is an extension for granular allowance.

---

**ivanmmurcia** (2024-01-07):

Hi [@dcota](/u/dcota). This EIP has last call status. LGTM this title change, I could make a new PR to wake up the editors.

Thanks for your feedback.

EDIT: Official name changed: [ERC-5216: ERC-1155 Allowance Extension](https://eips.ethereum.org/EIPS/eip-5216)

---

**SanLeo461** (2024-01-15):

Has adding ERC20Permit style approvals been considered?

If you (very understandably) don’t want to include it in the base spec, it could also be added as an extension to the spec similar to ERC1155/ERC1155Metadata.

---

**ivanmmurcia** (2024-01-16):

Hi [@SanLeo461](/u/sanleo461) thanks for your idea.

Maybe you can check this [ERC-4494: Permit for ERC-721 NFTs](https://eips.ethereum.org/EIPS/eip-4494) to move forward your proposal. Would be interesting a permit extension for ERC-1155 but in this EIP we’re not going to implement it.

---

**calvbore** (2024-01-27):

Conversation for permit style approvals can be found [here](https://ethereum-magicians.org/t/proposal-for-a-new-eip-erc-2612-style-permits-for-erc1155-nfts/15504), would love to hear your thoughts! Just started a PR for it

