---
source: magicians
topic_id: 9965
title: "ERC721 Lease: allowing owner to rent NFT to other"
author: wighawag
date: "2022-07-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc721-lease-allowing-owner-to-rent-nft-to-other/9965
views: 1456
likes: 5
posts_count: 1
---

# ERC721 Lease: allowing owner to rent NFT to other

Hi everybody, I have been working for some time on a system to allow NFT owners to rent the NFT to others without requiring the owner to lose ownership while the renting / uses take place.

This proposal works for all ERC721, past, present or future.

It does not require any modification to the existing ERC721 to work.

It is also designed to be fully flexible and every owner/user pair can have their own agreement’s rules.: The system will ensure such rules are enforced while allowing any kind of rules to be implemented (agreements are smart contracts).

The proposal was created a while ago but has been left to dust for some time. It shares some resemblance to existing proposals like [EIP-4907](https://ethereum-magicians.org/t/eip4907-erc-721-user-and-expires-extension/8572) but from what I hope to explain, proposals like EIP-4907 fall short compared to the system proposed here and I thus thought it was time to bring the idea back to life.

The proposal’s main idea is that of a registry contract that store the rental agreement between an NFT and its “user”.  NFT Owners are the only ones able to initiate such an agreement for the NFT they own but the owner can then freely transfer their token as usual (hence no need to require past ERC721 to change their implementation). Similarly unless specified in the rental agreement, “users” of an NFT are protected by their agreement even when the NFT owner changes.

You can find a draft of the system here: [GitHub - wighawag/erc721-lease: A contract to manage lease of NFT](https://github.com/wighawag/erc721-lease)

The contract in this repo allows anyone to rent their NFT token. As mentioned above, the contract act as a registry for lease. A lease is created as soon as an owner grant one to a “user”.

With a lease, the token owner retains ownership. This allows the owner to continue trading its token, while users are able to use their token in every place that supports such a registry. The obvious use case is off-chain reading for NFT display in a shared virtual world, etc… But this could be potentially used on-chain too for various use cases.

Note that each registration is itself an NFT token representing a lease. They can themselves be sub-leased as they are NFT too.

This allows the owner to

- retain ownership while renting its tokens
- give ownership for a loan (for example) but lease the token to itself beforehand to continue using the token
- have full liberty for lease terms: this is handled through external smart contracts.

This allows users to

- use token
- sub-rent the token (unless prevented by the agreement)
- sell renting right

It is worth pointing out that since “usership” is represented by ERC721 itself, existing infrastructure and tooling can easily be reused, allowing the communities to for example continue to use their token gated mechanism by simply adding the corresponding lease NFT to the list of the authorized membership.

This proposal as implemented in the repo above has one issue though.

Indeed, unless such a standard is adopted across marketplaces, marketplaces would not be able to tell potential buyers that the NFT is currently leased. It could potentially even be leased forever (the contract is fully generic, and the lease’s terms are handled through an external smart contract).

While the marketplace can support it and can thus display the current lease. until adoption kick in, there is a risk a buyer buys an NFT to realise that such NFT is being rented for an infinite time by someone else.

One solution to this problem is to prevent any agreement to last more than a specific amount of time (one year? one month?) but this would limit the genericity of the system: What if a user wanted to use a particular NFT for the rest of its life?

Another solution would be to initially only allow specific agreement contracts to be allowed. This is a more complex case though as we would need some sort of upgradeability and so governance…

Overall I think these solutions are misguided and we should accept the issue that we get with full genericity.

It is important to not benefit one side (NFT owner) or the other (lease owner). We do not want our system to take a political stance. NFT owners and lease owners should have full freedom on the specificity of their agreement. An NFT owner might not want to let the user transfer the lease or the lease owner might want to ensure it keeps its use across sales of the NFT. All of this should be supported by an NFT rental system and this proposal does it,

Furthermore, the issue mentioned above is only present in marketplaces that do not support the standard.

Indeed, the marketplaces aware of such a system can display to the potential buyer the current lease and its terms. As such the issue mentioned above is at worst a temporary one.

Another interesting example to contemplate is the case where you own let’s say a LAND NFT

you decide to collateralize it to get a Loan. In that case, you most likely want to be the “user” while giving ownership of the LAND to the Loan Contract (which needs to ensure the safety of its operation)

With the system proposed, this is fully supported but the Loan contract would have to ensure the LAND owner does not give itself “usership” past the liquidation time (if it arrives). And so the Loan contract will most likely give out a Lease upon collaterazation with the idea that if/when liquidation is performed, “usership” is also removed

It is again a matter of adoption, this time for collaterizable Loan contract, but it is great to see such a use case being possible without any changes needed in the core of the system.
