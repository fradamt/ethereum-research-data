---
source: magicians
topic_id: 13065
title: Bit Based Permission
author: chiro-hiro
date: "2023-02-27"
category: EIPs
tags: [authorization, permission, role]
url: https://ethereum-magicians.org/t/bit-based-permission/13065
views: 1913
likes: 3
posts_count: 3
---

# Bit Based Permission

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5982)





###



An interface for role-based access control for smart contracts.










Access Control List is a powerful tool to manage roles and permissions, it improved the security and prevent unwanted actors to interactive with smart contracts. But there are many issues that weren’t solved in `eip-5982`, please check the following list:

- Role doesn’t reflect the permissions, a role in eip-5982 represent by a string we don’t know the detail of its rights
- Verification cost is high, to verify a role, we need to perform keccak256 and compare with the value in hashmap, this approach is quite costly when you want to check multiple roles.
- Unable to organize the priority of permissions, there is no standard to compare the important between role/permissions, since all are strings.

What would make **Bit Based Permission** better?.

The basic concept of this proposal is, using `uint256` to store permission since it’s supported natively by the EVM. We can defined up to `256` permissions, each bit of an `uint256` will be represent a permission (1 single permission is power of 2). What do we benefit from this approach?.

- Role reflect permissions, since permissions were defined as power of 2, we can use OR operator to combine new role based on multiple permissions. We know exactly, what a role contains.
- Cheaper verification cost, to verify a role or a subset of permission we just need to do a simple AND operator on a permission bitmask. It’s much more cheaper than keccak256(string).
- Ordering permission by priority, We can use the most significant bit to represent for important permission, the comparison can be done easily since it all are uint256.
- Flexibility, 256 permissions can be combined to create up to 2²⁵⁶ different role. It would be enough for any complex ecosystem.

## Replies

**SamWilsn** (2023-06-08):

With the addition of the metadata extension, I think this is looking great!

If I were working on a wallet, and I wanted to use these permissions, how would I do that? For example, let’s say there’s an [ERC-721](https://eips.ethereum.org/EIPS/eip-721) token that supports `IEIP6617Meta` and has functions like:

```plaintext
function setPermissions(uint256 tokenId, address grantee, uint256 permissions);
function getPermissions(uint256 tokenId, address grantee) returns (uint256);
```

This token might have permissions like:

| Bit | Name | Description |
| --- | --- | --- |
| 0x01 | transfer | can change the owner of the token |
| 0x02 | burn | can destroy the token |
| 0x04 | modify | can change the tokenUri of the token |

Feels like we need:

- some way to indicate which function arguments are permissions, and
- some way to enumerate permissions.

Does that seem reasonable?

---

I’d omit the `setDescription` function from the interface. It feels very similar to `mint`, where only the contract creator would use it and so doesn’t need to be standardized.

---

**chiro-hiro** (2023-09-22):

Hi [@SamWilsn](/u/samwilsn),

I think your suggest is reasonable. I and Victor will have discuss on this.

Regarding to:

> some way to enumerate permissions.

I think It would be the best if it was support at language level [enums with specified values · Issue #4638 · ethereum/solidity · GitHub](https://github.com/ethereum/solidity/issues/4638) but it won’t be supported as a part of Solidity. Define constants are so expensive we still finding a good solution for it.

