---
source: magicians
topic_id: 13030
title: "ERC-6551: Non-fungible Token Bound Accounts"
author: jay
date: "2023-02-23"
category: ERCs
tags: [nft, token, accounts]
url: https://ethereum-magicians.org/t/erc-6551-non-fungible-token-bound-accounts/13030
views: 20182
likes: 112
posts_count: 219
---

# ERC-6551: Non-fungible Token Bound Accounts

An interface and registry for smart contract accounts owned by ERC-721 tokens.

https://github.com/ethereum/EIPs/pull/6551/files

## Replies

**ccamrobertson** (2023-02-23):

I love the simplicity of this proposal, yet it enables significant capabilities for ERC721 creators and holders.

A few thoughts crop up:

- It seems like there is significant opportunity for bad actors to deploy either duplicate registries or implementations for a given ERC721. Although I see that preventing fraud is outside the scope of this EIP, has there been thought given to providing more information about who calls createAccount? For instance I would likely have far more trust in an account created by the minter of the original account.
- This might not be desirable, but I am trying to work out whether or not it would be possible to have a registry that allows for the broad registration of Account Implementations without targeting specific token IDs until a user needs to take an action with the account. I suppose this might result in something like an impliedAccount from createAccountImplementation that can be read from the contract prior to creation so that assets can be deposited to an entire collection vs. single tokenIds.
- Despite the permissionless nature, is it expected that a canonical registry will (or should) emerge?

Excited to see this in the wild!

---

**jay** (2023-02-25):

These are great questions [@ccamrobertson](/u/ccamrobertson)!

- Yes, this does present an opportunity for fraud. The closest analogue I can think of would be airdropping “scam” NFTs into a wallet, which is quite common. This behavior is harmless to the end user so long as the malicious accounts are not interacted with. Because the address of the created account is tied to the implementation it points to, a holder can trust that an account created using a trusted implementation address is secure, regardless of who calls createAccount. The ability to permissionlessly deploy accounts for tokens that you do not own is desirable in many cases, and I think this functionality should be maintained if possible. One example is NFT creators who wish to deploy token bound accounts on behalf of their holders. Determining whether an account is trustworthy seems like something that should happen off-chain at the client level (as both the caller of createAccount and the implementation address will be queryable via transaction logs), or perhaps via an on-chain registry of trusted implementations (although that seems like a large increase in the scope of this EIP, and may warrant a separate proposal). Would love to hear any suggestions you have for how this type of fraud could be addressed within the scope of this proposal!
- This is definitely an interesting idea to explore. I had considered adding a discoverAccount function which would emit an event registering an account address, but ultimately decided against it because the same data could be queried off-chain at the application level given an implementation address. Depositing assets to an entire collection is definitely an interesting use case, but the logic for this may be better implemented at the asset contract level rather than the within the context of this proposal. It might be interesting to add a registerImplementation function which emits an event notifying listeners that a new implementation is available. However, I fear this may compound the risk of malicious account implementations as it gives them an appearance of legitimacy.
- Since the proposal defines both a registry implementation and a registry address that are permissionless, it is expected that this will become the canonical registry. A single entry point for token bound accounts will make it much easier for the ecosystem to adopt this proposal vs. multiple registries. The proposed registry should be flexible enough to accommodate the majority of token bound account implementations, as the EIP-1167 proxy pattern is very well supported. Of course, anyone is free to deploy their own registry implementation, or to deploy token bound account contracts without using a registry.

---

**scorpion9979** (2023-02-26):

I think this is a great concept that enables a whole new array of use cases and the best thing about it is that it would already work with any existing NFTs. I think it could also give rise to a whole new and unique model of project airdrops.

---

**jay** (2023-02-26):

Thanks [@scorpion9979](/u/scorpion9979)!

This proposal definitely has interesting implications for airdrops. It could eliminate the need for projects to capture point-in-time snapshots of token holders, since the token bound account address for each NFT is static and computable.

Additionally, because each token bound account address can be computed from the token ID of the NFT which owns it, the data required to distribute tokens could potentially be stored in a compressed format on chain. This may significantly reduce the gas cost required to perform airdrops.

---

**william1293** (2023-02-27):

As far as I know, a project called A3S Protocol has implemented a similar function, but I don’t know the difference between its implementation and your proposal.

---

**jay** (2023-02-27):

Thanks for highlighting this project [@william1293](/u/william1293)! I haven’t seen it before. It looks like A3S uses a similar approach, but from a quick glance it seems like there are a few key differences:

- A3S uses a single central NFT collection which it deploys smart contract accounts for. It is not compatible with other NFTs. This proposal gives every NFT the ability to have a smart contract account.
- The A3S factory contract is centrally owned and upgradable by the owner. The registry defined in this proposal is neither owned or upgradable.
- Each A3S account calls back into the central factory to determine ownership of the account, which theoretically gives A3S the ability to modify the owner of an A3S account without the current owner’s permission. This proposal defers ownership checks to the account implementation, allowing fully sovereign account implementations to be developed. The example account implementation defined in this proposal is sovereign by default.

In short, this proposal defines a system that gives every NFT a smart contract account in a decentralized manner. A3S seems to be a for-profit protocol company that creates smart contract accounts for their own NFT collection.

---

**hskang9** (2023-02-28):

That sounds similar to previous standard [EIP-5252](https://eips.ethereum.org/EIPS/eip-5252). I think proxy method to generate account contract would make the gas cost more efficient. I think EIP validators will finalize this one as they could not understand the code and gave up. It is such a shame they need take effort on discovering new primitives but then they are not funded when [@vbuterin](/u/vbuterin) sells eth for $350 million.

---

**hskang9** (2023-02-28):

[@SamWilsn](/u/samwilsn) I volunteer to review this EIP and get it finalized, and hopefully I might find someone interested to finalize my EIP as well?

---

**SamWilsn** (2023-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> I volunteer to review this EIP and get it finalized

Always happy to have more peer reviewers!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> hopefully I might find someone interested to finalize my EIP as well?

[ERC-5252](https://eips.ethereum.org/EIPS/eip-5252)? You can open a pull request to move it to `status: Review` whenever you think it’s ready. Peer review—while recommended—is optional.

---

**RobAnon** (2023-02-28):

Pretty neat, we’ve already done this with Revest FNFTs. Suggest including backwards compatibility in some manner.

---

**jay** (2023-02-28):

[@hskang9](/u/hskang9) I’d love to learn more about the similarities you see between this proposal and ERC-5252. I’ve taken a read through that proposal and I’m not totally clear on how it could provide smart contract accounts for NFTs.

---

**jay** (2023-03-01):

[@RobAnon](/u/robanon) thanks for sharing! From a cursory look, it seems like Revest uses ERC-1155 tokens under the hood. ERC-1155 support was considered during the development of this proposal, but ultimately decided against.

Since ERC-1155 tokens support multiple owners for a given token ID, binding an account to an ERC-1155 token would significantly complicate the ownership model of this proposal. In the case of an account bound to an ERC-1155 token, would each token holder be able to execute arbitrary transactions? Would signatures from all holders be required? Or would signatures only need to be collected from a majority of holders?

Some ERC-1155 tokens (potentially including Revest?) support single account ownership of of a ERC-1155 tokens by limiting the balance of each token ID to 1. The challenge to supporting these tokens is that the ERC-1155 standard doesn’t define a method for querying the total number of tokens in existence for a given token ID. It is therefore impossible to differentiate between ERC-1155 tokens that have multiple owners per token ID and those that have a single owner per token ID without using non-standard interfaces.

Since this proposal purposefully excludes ERC-1155 tokens from its scope, I don’t think Revest tokens can be supported in their current form. However, Revest would be welcome to implement a custom token bound account implementation that uses an alternative ownership scheme if they wish to support this proposal. Another potential solution would be to wrap the existing ERC-1155 tokens in an ERC-721 token, which would then make them compatible with this proposal.

---

**hskang9** (2023-03-01):

That is because you don’t clarify ambuiguity of account using NFT and haven’t even made a contract implementation yet. Your proposal currently have not clarified how much one’s NFT have access to its account contract and how the access will be managed. If you can’t make contract implementation, you don’t know what you are doing. What I look feasible in your proposal is unified interface for operating account bound contracts, and this is the first thing I will review. Other items will be reviewed once the contract for binding logic on each case in the proposal is implemented. Account bound finance(EIP-5252) fits in the case where one NFT manages access one contract bound to its nft owner. EIP-5252 creates account with contract clone method. Backward compatibility may be considered if this EIP tries to implement EIP-5252’s structure.

Also, one question about security considerations, have you considered adding metadata in your NFT registry and make it display in opensea metadata format? Why is this a security concern if a metadata can be retrieved from its registry for account bounding? Do you have the certain metadata format you would propose?

For example, [OpenRarity](https://www.openrarity.dev/) have come up with their metadata to show NFT rarity.

---

**hskang9** (2023-03-01):

It would be actually great if we include each of our cases on clarifying account ambiguity into this eip and try to come up with most unified interface for all in democratic way.

---

**hskang9** (2023-03-01):

It is not true that EIP-1155 cannot be used for account bounding, account bounding can already be done by checking ownership of an EIP-1155 token of sender in account contract. Ids can actually be assigned to EIP-1155 and it is more gas efficient.

---

**jay** (2023-03-01):

[@hskang9](/u/hskang9) a few comments:

> haven’t even made a contract implementation yet

A fully-functional implementation is included in the “Reference Implementation” section.

> If you can’t make contract implementation, you don’t know what you are doing

This seems unnecessarily hostile - let’s try to keep things civil ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> Account bound finance(EIP-5252) fits in the case where one NFT manages access one contract bound to its nft owner

Right - I guess my question is whether ERC-5252 works with all existing NFT contracts? Or does it only work with NFTs that implement the ERC-5252 interface?

> have you considered adding metadata in your NFT registry and make it display in opensea metadata format? Why is this a security concern if a metadata can be retrieved from its registry for account bounding?

This proposal is designed to work with external NFT contracts, especially ones that have already been deployed and already have metadata systems in place. As such, it doesn’t specify any requirements for metadata beyond those set out in EIP-721. This is not a security concern.

> account bounding can already be done by checking ownership of an EIP-1155 token of sender in account contract

Right - you can check that a sender’s balance of an ERC-1155 token is non-zero. My point is that there can be many owners of a single ERC-1155 token with a given token ID. How would you recommend handling account authorization given multiple token holders?

---

**hskang9** (2023-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> A fully-functional implementation is included in the “Reference Implementation” section.

The reference implementation does have a case of account contract being a proxy to interact with another smart contract, but it does not cover all ambiguity such as a case where an account being operated by the rules on smart contract.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> If you can’t make contract implementation, you don’t know what you are doing

Sorry if it hurts you, but it is true that you haven’t covered the case on other previous references where the contract account can have other utilities. The way to use smart contract with NFT as a proxy account is very interesting and has its point enough if it is clarified.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> Right - I guess my question is whether ERC-5252 works with all existing NFT contracts? Or does it only work with NFTs that implement the ERC-5252 interface?

Definitely not. your proposal is something new from what I did. Your proposal is providing a way where a proxy account can be made in EVM blockchain with NFT. Problem is you cover the proposal as if it covers all cases of account bound with NFT.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> This proposal is designed to work with external NFT contracts, especially ones that have already been deployed and already have metadata systems in place. As such, it doesn’t specify any requirements for metadata beyond those set out in EIP-721. This is not a security concern.

I agree as this is rather a specification of a proxy account by owning an nft from the reference implementation for now. The proposal has its value on its generic interface to interact with other contracts, but I think it is currently neglecting the fact on who is reponsible on which and which on connecting account to NFT. However, I believe this has a huge potential when it comes to proxy trade. As you declare there is no security concern, it is clear that this is just used as generic proxy account.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> Right - you can check that a sender’s balance of an ERC-1155 token is non-zero. My point is that there can be many owners of a single ERC-1155 token with a given token ID. How would you recommend handling account authorization given multiple token holders?

ERC-1155 with id can be made with setting asset key as an id (e.g. (“1”, 1), (“2”, 1)). This way one can handle account authorization as same as ERC721.

After looking at the reference implementation, I suggest amending the proposal name from “Non-fungible Token Bound Accounts” into “Non-fungible Token Bound Proxy Accounts”.

---

**hskang9** (2023-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> Right - you can check that a sender’s balance of an ERC-1155 token is non-zero. My point is that there can be many owners of a single ERC-1155 token with a given token ID. How would you recommend handling account authorization given multiple token holders?

[@jay](/u/jay) 's point is fair. You need to specify how you handle this issue.

---

**jay** (2023-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> does not cover all ambiguity such as a case where an account being operated by the rules on smart contract

I can definitely add some test cases to clarify how token bound accounts should function. The example account implementation in the proposal is intentionally simple.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> you haven’t covered the case on other previous references where the contract account can have other utilities

Projects wishing to implement this proposal are welcome to create custom account implementations which add additional functionality to token bound accounts. This proposal defines a minimal interface in order to leave room for diverse implementations.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> Problem is you cover the proposal as if it covers all cases of account bound with NFT

I’d love to hear more about some of the cases that couldn’t be supported by this proposal. EIP-1167 proxies were chosen to maximize the possible cases that can be supported, as they have wide ecosystem support and can support nearly all possible smart contract logic.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> it is currently neglecting the fact on who is reponsible on which and which on connecting account to NFT

I can definitely attempt to make this clearer in the proposal. Anyone can create a token bound account for any NFT, but only the owner of the NFT will be able to utilize the account. This is enforced by checking that a given implementation supports the token bound account interface described in this proposal before deploying the account. Bad actors could deploy malicious account implementations, which is a potential concern. However, much like “spam” NFTs that are airdropped into people’s wallets, there is no risk to the end user so long as they do not interact with accounts whose implementations are untrusted.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> ERC-1155 with id can be made with setting asset key as an id (e.g. (“1”, 1), (“2”, 1)). This way one can handle account authorization as same as ERC721.

This is correct. However, given an external ERC-1155 token contract with no knowledge of its token ID scheme, there is no way (according to the ERC-1155 standard interface) for an account implementation to determine that there is only one owner per token ID. As mentioned above, a custom account implementation could be created which implements the `owner` and `executeCall` functions such that they check `balanceOf` instead of `ownerOf` to allow usage with ERC-1155 tokens. I’m reluctant to specifically include this in the proposal to avoid bloating the specification, but if there is enough interest that can certainly be reconsidered.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> You need to specify how you handle this issue.

This question was actually directed at you [@hskang9](/u/hskang9) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Would love to hear your thoughts on how you would like to see ERC-1155 tokens supported!

---

**hskang9** (2023-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> I can definitely add some test cases to clarify how token bound accounts should function. The example account implementation in the proposal is intentionally simple.

You are missing the point. You claim to have provided a token bound proxy account that enables someone do anything and you limit what it does? It is great to make a test cases, but you just made a token bound proxy account for executing generic transactions with separate contracts. You don’t need to limit what you just make, that is not a standard.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> Projects wishing to implement this proposal are welcome to create custom account implementations which add additional functionality to token bound accounts. This proposal defines a minimal interface in order to leave room for diverse implementations.

Ok, so to leave a room, I think the proposal has to specify three cases where:

1. wallet <> token bound contract <> another contract (proxy account and your reference implementation)
2. wallet <> token bound contract

The question is, how will you securely specify second item as you referred on security concerns in your original proposal? and how will you aggregate all the other cases into one (e.g. FNFT by Revest, etc)?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> I’d love to hear more about some of the cases that couldn’t be supported by this proposal. EIP-1167 proxies were chosen to maximize the possible cases that can be supported, as they have wide ecosystem support and can support nearly all possible smart contract logic.

Obviously the same answer from the previous quote.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> Right - I guess my question is whether ERC-5252 works with all existing NFT contracts? Or does it only work with NFTs that implement the ERC-5252 interface?

ERC721A is subset of ERC721? Is it too hard to understand implementing NFT ownership of a newly created contract from create when you just coded? [EIPs/assets/eip-5252/contracts/ABT.sol at 39fe51429c2295692b351e4e89f7c38cc42d8ae9 · hskang9/EIPs · GitHub](https://github.com/hskang9/EIPs/blob/39fe51429c2295692b351e4e89f7c38cc42d8ae9/assets/eip-5252/contracts/ABT.sol#L11)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> I can definitely attempt to make this clearer in the proposal. Anyone can create a token bound account for any NFT, but only the owner of the NFT will be able to utilize the account. This is enforced by checking that a given implementation supports the token bound account interface described in this proposal before deploying the account. Bad actors could deploy malicious account implementations, which is a potential concern. However, much like “spam” NFTs that are airdropped into people’s wallets, there is no risk to the end user so long as they do not interact with accounts whose implementations are untrusted.

Ok now put that into the proposal without saying account ambiguity. You also forgot how your registry actually verifies NFT and connected account.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> This is correct. However, given an external ERC-1155 token contract with no knowledge of its token ID scheme, there is no way (according to the ERC-1155 standard interface) for an account implementation to determine that there is only one owner per token ID. As mentioned above, a custom account implementation could be created which implements the owner and executeCall functions such that they check balanceOf instead of ownerOf to allow usage with ERC-1155 tokens. I’m reluctant to specifically include this in the proposal to avoid bloating the specification, but if there is enough interest that can certainly be reconsidered.

No, you don’t know how ERC-1155 works. ERC-1155 can have total supply of 1, and this makes the fact that there is only one owner per token ID. Perhaps you could set total supply on 2 and ask why it does not work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jay/48/8502_2.png) jay:

> This question was actually directed at you @hskang9
> Would love to hear your thoughts on how you would like to see ERC-1155 tokens supported!

No thank you. I work on this to make sense of a proposal. I am not joining your peripheral attempt on glorifying the proposal when it is just a proxy account implementation with NFT. You have to pay me first on handling your issue. I only work for free on this after being too afraid of the world where [@vbuterin](/u/vbuterin) says zero knowledge solves everything but cannot code one line on actually shipping the product then cashes out 350 million dollars, Do Kwon saying algo-stablecoin will solve all money out there and make hundreds of people suicide after his scam got revealed. They all boast their knowledge about crypto, but they have zero knowledge in action. Also, I think using emojis doesn’t help on showing that you are seriously thinking to pass this. Are you trying to finalize this proposal or what?

From your answers, it seems you do have knowledge in smart contracts, but it does not look like you have knowledge in action as you haven’t known the EIP-1155 can limit the supply. If your proposal’s name is Non-fungible Token Bound Accounts, you must have knowledge in action on all NFTs, including ERC-1155. Hence, you need to implement the case where EIP-1155 is used too. Otherwise, this has to be limited to ERC-721 token bound accounts.


*(198 more replies not shown)*
