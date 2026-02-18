---
source: magicians
topic_id: 8038
title: "Idea: NFT entanglement"
author: cyrus
date: "2022-01-19"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/idea-nft-entanglement/8038
views: 2194
likes: 1
posts_count: 7
---

# Idea: NFT entanglement

When you buy a car, you don’t buy the hood, and then the steering wheel and then the rear axle… you buy it all together as one piece.

In Ethereum NFT land, there’s no option to bundle things together permanently. NFTs that should go together have to be transferred 1-by-1, which is messy, expensive and limiting.

This idea is to create “NFT Entanglement” where a new NFT can be minted but instead of having normal transfer mechanisms, it is immediately and permanently wedded to some existing NFT, specified at mint time.

Anytime the underlying NFT changes owners, the network would enforce that this new entangled NFT immediately *and atomically* does as well, possibly by simply sharing the same memory slot on the chain that holds the owner address.

I’m an application-level guy, mostly (see: Etheria, https://etheria.world), and am seeking feedback/assistance in formalizing this EIP proposal from folks more familiar with lower-level workings.

Questions:

- If the new NFT is to be linked to the memory slot holding the owner address of the existing NFT, by what mechanism should that linkage made?
- Above, I described an NFT type that is linked permanently at creation time, but maybe the spec should allow for creation, then permanent linkage at some later time?
- Is it possible to create two-way entanglement such that the EOA owning the old NFT could authorize the new NFT to manage ownership of the old NFT (i.e. in the reverse direction)?

Background

The need for this comes from my desire to add new features to the existing NFTs in the project I manage, specifically to direct royalties to the old NFT owners via 1155 token mechanics. I could create a new NFT “emblem” (as I call it) inside the 1155 where the normal transfer mechanisms are disabled and replaced with a “touch()” function that always sets the new NFT owner to the underlying owner address. Anytime the set of NFT ownership is out of sync (via sale or transfer), *anyone* can call “touch()” to sync one or more of the “emblem” NFTs to the correct address.

But obviously this is (a) hacky, (b) non-atomic, (c) expensive and probably issues (d-z) I can’t even imagine immediately.

Thoughts and assistance greatly appreciated!

## Replies

**omaraflak** (2022-02-01):

When you say NFTs with an “s”, am I right to assume you’re talking about different `tokenId`s in one same contract ?

Also, what happens if two different persons own “entangled” NFTs, and then one is sold ? The one that did not sell will lose his NFT ?

---

**cyrus** (2022-02-01):

I think the best way to do this is to have a “source” 721 NFT and then any entangled NTT would be permanently wedded to it at mint time.

So the entangled NTTs would not be directly transferrable. They would always go wherever the linked NFT goes. This is doable now: make an NFT, remove the transferability and make getOwner() simply return getOwner() of the source NFT.

Question is how to codify this? Should it be included in the NTT discussion?

On the source NFT side, could there be a 721 extension that is aware of its entangled NFT add-ons? Does the source 721 get a choice as to whether tokens can be entangled to it? Can the source NFT detach add-ons?

Clear as mud, right? Does this help at all?

---

**earizon** (2022-02-04):

This is a very good point from my point of view in terms of UX / usability.

Maybe a “dependency tree” of ownership could be more practical than entanglement.

I am thinking about the scenario when a real-state property is tokenized. Initially it contains an NFT with a house, a “child” swimming pool as well as a two “children” garages. When changing ownership of the house all children tokens must change ownership atomically, but original owner can be interested in changing ownership of just one garage (that will vanish from the tree).

Entanglement will correspond to the addition of an NFT as child of a parent (and potentially grand parents).

Children will need to contain a pointer to their parents, (maybe codified in some compact form) so that in a complex ownership-tree changing a node parent will automatically change ownership of children, grand children, … for free. Only when the pointer has some sort of special value ( ~keccak256(“root_of_ownership”))  the real owner will be used. A tree like structure also means that  complexity of search-for-ownership given a child would be LOG_y(N), with N being the number of “entangled” NFTs and y the average children per parent, in normal scenarios (N in the case corner scenarios of a linear-like tree from root to leaf).

This also helps in other use cases. For example I want to organize my NFT collection into folders with the idea of reselling / atomically swapping a subset of them atomically. For example I have some NFT related to some video-game and I want to swap them for some other collection of NFT from a new video-game with  another user.

My two cents!

---

**cyrus** (2022-02-06):

Ultimately, I think what we’re talking about is **codifying NFT relationships in some way**, transferable or otherwise, and I agree that parent-child is the correct direction for our thought processes.

**The base case** is a transferable NFT parent (~721) and children tokens that become permanently and non-destructively attached at mint time. (My original need, basically.) This is very easy to handle; getOwner() of the child is just getOwner() of the parent and each token gets a concise pointer to the other (an append-only array of children in the parent and a single “parent” variable in the child).

After that, though, it gets *much* more complicated:

- Children tokens that can be attached or detached
- Grandparent (etc) relationships
- Children tokens that can be created, transferred, but when attached, are permanently attached
- Children tokens that are permanently attached unless some condition is met
- Children tokens that are destroyed if some condition is met

These additional cases come with the additional variables of transferability, permanence, and multiple levels of hierarchy. And I can imagine gas determination would become challenging.

So I think the question is what is the real, immediate need and what is realistic to get adopted in short order? Could the base case be codified and added first in such a way that the later needs could be added later?

---

**poria-cat** (2022-02-09):

It looks like I’ve done something relevant, At this [EIP-4786](https://github.com/ethereum/EIPs/pull/4786), One interesting thing I did was to connect/combine different NFTs to each other, and of course to connect the ERC20/ERC1155 to the NFT.

Of course it can also be discussed here: [EIP-4786: Link Common Token to ERC-721](https://ethereum-magicians.org/t/eip-4786-link-common-token-to-erc-721/8245)

---

**earizon** (2022-03-20):

I’m just thinking that a different approach is a degree of indirection between NFTs owner address and NFT ownership that will allow different relationship (entangled, tree, “cherry-pick”, related-by-business-logic, …) be implemented outside the hardcoded smart-logic.

By adding this degree of indirection among identity and ownership and creating well-defined identity patterns we can assign a given set of FT/NFT to a given address, and another set of FT/NFT to another given address with all those addresses owned by the same user/identity (nothing new here). Such user  “group” different tokens in different addresses controlled by himself (again, nothing new here). An entagled group of NFT will just be assigned to a given address representing the entanglement, that can be moved at will to a new ownership. This of course is already possible right now, and anyone can do it by just “juggling” with its wallets. The problem is that this “juggling” can be out-of-reach for 99.999% of users and how to do it in with a beautiful and standarized “UX” is also undefined. There are HD standards to define hierarchies of addresses on the wallet “side”, but nothing related to how mapping those HD wallets (or maybe some other sort of future wallet schema) to entanglement or hierarchy trees of tokens.

The effort will then move to create a set of well-defined “best-patterns” for such address-to-identity mechanism in an standard way to simplify token management (standard way == well documented and defined interfaces that everybody agree to). Related token management EIP can then be extended to PROMOTE those “best-patterns”, basically ensuring for example that market places and wallets use the same nomenclature.

Not sure about how those “best-patterns” must look like, but for example it must be easy for a user to define which set of tokens are entangled or related to each other and users’s wallet must help their users to create new sub-addresses by just “guessing” the user intention for the new addresses and the current capabilities of the underlying smart-contract managing the token (querying its ERC165 interface for example). It must be easy for users to see a set of entangled tokens as belonging to the same creator/author as another set of entangled tokens.  SC controlling tokens can impose “quality-assurance” restrictions. For example, a given SC can impose to register a well defined “parent” address for the full set of tokens defined by the same owner, and force to use a new set of “children” addresses for a new subset of  children-and-entangled tokens, and maybe also imposing such addresses to comply with some well defined rules. Transfers that now indicate movements with the (from, to) parameters can force a (from_parent, from_child, to_parent, to_child) instead (with the “from_parent”, “to_parent” being sort of inmutables entities), and differentiating standard transfers from “regroup” transfers using just (parent, from_child, to_child). Wallets aware of the “best-pattern” standard will check that “from_parent”/“from_child” and “to_parent”/“to_child” match some rules or feedback users otherwise aborting any transfer. This can allow for a much better “UX” experience and also increase the security of transactions, considering for example that the immutable “parent” address must be registered first and treated as a mostly immutable entity.

