---
source: magicians
topic_id: 8388
title: "EIP-4834: Hierarchical Domains Standard"
author: Pandapip1
date: "2022-02-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-4834-hierarchical-domains-standard/8388
views: 3187
likes: 2
posts_count: 15
---

# EIP-4834: Hierarchical Domains Standard

## GitHub Issue

https://github.com/ethereum/EIPs/pull/4835

## Replies

**SamWilsn** (2022-03-14):

Would you mind removing the EIP text from this discussion thread? It’s unnecessary pain for you to have to keep it in sync with the PR.

---

Would it make sense to split the resolver interface from the management interface? I can imagine some use cases that would use a completely different management system but could still benefit from the resolver interface. For example, `4553.some-nft` could always resolve to the owner of `Some NFT #4553`.

---

In `canPointSubdomain`, is the point to prevent yourself being added as a subdomain to a parent you don’t want? If so, what’s to stop a malicious `parent` just skipping this check?

---

**Pandapip1** (2022-03-14):

1. The EIP text is removed.
2. I guess that’s certainly an option. I might do that.
3. That’s a good question. I once thought of a use-case, but  I can’t remember what it is. You’re absolutely right that a malicious parent can circumvent that – maybe I should replace it with an isValidSubdomain that when returns false reverts the name resolution.

---

**SamWilsn** (2022-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> maybe I should replace it with an isValidSubdomain that when returns false reverts the name resolution

Could maybe have the querier pass in the parent address to `getDomain`?

---

**Pandapip1** (2022-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Could maybe have the querier pass in the parent address to getDomain?

If I were to go that route, I would much prefer it to be in `hasDomain`. However, I don’t really see any point in `canPointSubdomain` anymore – I might just remove it. I don’t see any issues with people pointing other peoples’ domains to their own. After all, would the owner of a token care if I set `myfavoritetoken.pandapip1.sometld` to their token? Even if it was `theworldsworsttoken.pandapip1.sometld`, I’m not sure the extra complexity in the spec is worth it.

I’m just going to remove it, and maybe add it as an optional extension.

---

**xinbenlv** (2022-08-16):

[@Pandapip1](/u/pandapip1)  This ERC is going to be greatly useful, kudos!

Two pieces of feedback for its last call

1. Shall we move the “Here is a solidity function that resolves a name:” to the reference implementation instead of spec section?
2. Shall we change all the “must”, “shall” to their upper-case counter part (MUST, SHALL) so to follow RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words which suggest using uppercase to reduce ambiguity

---

**Pandapip1** (2022-08-16):

Definitely #2. I also mostly support #1.

---

**frangio** (2022-09-29):

I don’t think this EIP has had sufficient discussion around it to become Final (seeing that the Last Call deadline is tomorrow).

Although to be frank I am personally not interested in alternatives to ENS at the moment, here are two concerns that I have with this EIP:

- What is the root domain? How do I find it? Without it, no resolution is possible. Without a globally accepted root, a name has no meaning.
- There are no frontrunning mitigations for domain creation.

I’ve seen another alternative to ENS being developed, [dmap](https://dmap.sh), which notably does not have an EIP. This is fine and in my opinion a better approach: standardizing before the system is further developed ossifies a version that has not been tested enough.

---

**Pandapip1** (2022-10-03):

> What is the root domain? How do I find it? Without it, no resolution is possible. Without a globally accepted root, a name has no meaning.

This would be user-provided. The nice thing is that anyone can deploy their own domain and have it work as a root domain. I didn’t notice this wasn’t provided in the EIP, so I will add that.

> There are no frontrunning mitigations for domain creation.

Thank you for pointing that out – I hadn’t considered it. Most of the time, this won’t be an issue. Perhaps a commit/reveal scheme could be recommended when it would be useful.

> Although to be frank I am personally not interested in alternatives to ENS at the moment

The nice thing about this is that this isn’t necessarily an alternative to ENS. It would be perfectly possible to make a “domain” that resolves ENS domains.

> Standardizing before the system is further developed ossifies a version that has not been tested enough

I can be convinced to move this back into review. Do you have any normative suggestions?

---

**frangio** (2022-10-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> Do you have any normative suggestions?

Nothing in particular, my point is rather that I think the interface should be tried “in the field” quite a bit before settling on a final specification, because that could surface issues in it. I mean things like starting to build the various applications, tooling, and libraries around it. I don’t know if that has been done in this case.

---

**Pandapip1** (2022-10-12):

After considering your points I’ve moved it back into review.

---

**jong** (2023-04-04):

There is no any explanation about resolvers in the EIP. Without resolvers, is the use of the domain only that “permits a contract that implements this EIP to be addressable with a more human-friendly name”? Can I create a subdomain with an EOA address or any contract address that does not implement the interface IDomain.

---

**Pandapip1** (2023-04-04):

I’m pretty sure that somewhere it says that the root domain is an implementation detail. This is similar to ENS, whose standard also leaves the root domain as an implementation detail.

---

**jong** (2023-04-11):

I can’t get the point. My question is about a leaf domain instead of a root domain.

---

**Pandapip1** (2023-04-21):

Does the following snippet from the EIP not answer your question?

```plaintext
function resolve(string[] calldata splitName, IDomain root) public view returns (address) {
    IDomain current = root;
    string[] memory path = [];
    for (uint i = splitName.length - 1; i >= 0; i--) {
        // Append to back of list
        path.push(splitName[i]);
        // Require that the current domain has a domain
        require(current.hasDomain(path), "Name resolution failed");
        // Resolve subdomain
        current = current.getDomain(path);
    }
    return current;
}
```



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4834#name-resolution)





###



Extremely generic name resolution

