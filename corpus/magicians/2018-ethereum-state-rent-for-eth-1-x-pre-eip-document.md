---
source: magicians
topic_id: 2018
title: Ethereum State rent for Eth 1.x pre-EIP document
author: AlexeyAkhunov
date: "2018-11-26"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x, storage-rent]
url: https://ethereum-magicians.org/t/ethereum-state-rent-for-eth-1-x-pre-eip-document/2018
views: 5652
likes: 28
posts_count: 39
---

# Ethereum State rent for Eth 1.x pre-EIP document

Here is the document about state rent: https://github.com/ledgerwatch/eth_state/blob/master/State_rent.pdf

Because I wrote most of it, it most probably reflects lots of my opinions, but I tried to incorporate alternative points of view to the extent it would still make description tractable.

## Replies

**Cygnusfear** (2018-11-26):

Thank you for these slides. An idea that comes to mind reading this and https://ethresear.ch/t/ethereum-2-0-data-model-actors-and-assets/4117 is the following:

Account/wallet contracts implement a permissioned storage interface standard (using a sort of ACL).

Instead of ledger-within-ledger token contracts, the user of the wallet grants the token contract permission to write to the user’s own storage. Token balances, NFTs etc are now stored on the user’s account, thus the users are charged rent for their own assets. To decrease rent fees users can remove unwanted assets.

This could be a solution to the dust griefing attack mentioned in the slides.

Users can ‘deny’ tokens from storing data in their contract, reducing the viability of spam tokens. Airdrops can still be performed using a withdraw() scheme.

Token contracts will pay significantly less storage rent. Users are incentivised to pay their ‘account cost’ and be custodians of their own data usage.

(I’m uncertain if I’m reformulating the Step 3 - Linear cross-contract storage here, so please let me know if I whooshed there)

---

**AlexeyAkhunov** (2018-11-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cygnusfear/48/247_2.png) Cygnusfear:

> (I’m uncertain if I’m reformulating the Step 3 - Linear cross-contract storage here, so please let me know if I whooshed there)

Yes, what you are describing is in sprit the linear cross-contract storage from Step 3 ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**boris** (2018-11-26):

Useful thread from Vlad:



      [twitter.com](https://twitter.com/vladzamfir/status/1066979913859616768?s=21)



    ![image](https://pbs.twimg.com/profile_images/1803355295826984961/SX6Bin0F_200x200.jpg)

####

[@VladZamfir](https://twitter.com/vladzamfir/status/1066979913859616768?s=21)

  I know blockchain rent doesn't have a great user experience, but we need to (eventually) bound the size of the EVM state trie or the system will 🔥

  https://twitter.com/vladzamfir/status/1066979913859616768?s=21

---

**hershy** (2018-11-26):

Thank you [@AlexeyAkhunov](/u/alexeyakhunov) . I appreciate that you had some concerns around the blowback that certain teams high up on the ‘Contracts by Storage’ list will/may receive from folks acting in bad faith. And I appreciate those concerns comes from a good and empathetic place. However, this research is excellent and concisely presented and should not have to accomodate the actions of a 'lowest common denominator.

---

**AlexeyAkhunov** (2018-11-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hershy/48/1155_2.png) hershy:

> I appreciate that you had some concerns around the blowback that certain teams high up on the ‘Contracts by Storage’ list will/may receive from folks acting in bad faith

Thank you for the kind words, and I think now that my concerns might be unfounded

---

**cheeselord1** (2018-11-27):

This is really great! I’m wondering if we can split up the rent problem for contracts into two groups:

1. How can we get active contracts that are using lots of storage to pay a rent that more accurately represents the cost of storing that data permanently on-chain over a period of time. As you pointed out, for many contracts (Token contracts) this suffers from the free rider problem. I think the Actor/Asset model (or Linear cross-contract storage as you call it) could be an interesting solution here.
2. How can we clear the state of abandoned contracts that are not being used anymore?  As calling SELFDESTRUCT is not free, most people don’t clear their old contracts when abandoning them (I am guilty of this too).  For this case, maybe we can store an expiration_time for each contract and refresh it to now+12 months on every call to that contract.  Though there may be some types of contracts that are still in-use but called very infrequently (libraries, multi-sig wallets)

#1 would offload a lot of state from large, central contracts to the actual users of the contract where rent could be applied more fairly.  And #2 would help purge any state remaining on the contract itself once abandoned

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/8e8cbc/48.png) cheeselord1:

> How can we clear the state of abandoned contracts that are not being used anymore?

I did not include this into the deck, but as it stands at the moment, abandoned contracts (those not used for the last 12 months) represent only 6% of the state. That is why measures specifically designed to go after them were not in the proposal. And they are also quite easy to neutralise if someone wishes to.

---

**Cygnusfear** (2018-11-27):

Hey Alexey, I would like to second the sentiment shared by [@hershy](/u/hershy) and I’m very happy to be able to ask stupid questions here as well ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=9)

Currently I understand that once a contract is evicted, it’s cross-contract storage is cleared, including the storage (on the owner’s side) that holds for example the tokens of a user. How does this influence actual ownership of assets, something that is specifically the goal of the NFT community and one of the promises of ‘gaming on Ethereum’ (once the servers go down, you still own the assets).

From a user perspective, I’m probably not aware this contract has run out of rent; my point of discovering this is when I’ve lost my assets. Additionally the community would have to rework current token standards to have actual ownership of items.

The rent model is a very elegant solution (not a UX nightmare at all); having an ‘open account’ means you pay a small fee for keeping the account open. If you store your own data, then you can do your own ‘cost’ housekeeping. The above scenario where you can lose your data is scary for a user with regards to ownership. Could you elaborate on why it is necessary to clear the user’s storage to help me understand the reasoning here?

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cygnusfear/48/247_2.png) Cygnusfear:

> Currently I understand that once a contract is evicted, it’s cross-contract storage is cleared, including the storage (on the owner’s side) that holds for example the tokens of a user

No, when contract is evicted, only the storage it owns gets evicted, but not the storage it writes. That means, if an NFT contract suddenly goes away, users will be able to bring it back using resurrection, and all their assets will be intact, as long as they keep paying for them. And, if NFT contract is very lean and popular, it might be able to effectively immortalise itself (because it will accumulate huge rent balance) by using call-fee (page 48).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cygnusfear/48/247_2.png) Cygnusfear:

> Could you elaborate on why it is necessary to clear the user’s storage to help me understand the reasoning here?

Data owners should not be allowed to modify storage written by other contracts. But they should be able to withdraw that write permission, to stop paying for the store. For example, if you sold your tokens, you do not want to pay for number “0” kept in your storage ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**Cygnusfear** (2018-11-27):

Thanks for clearing this up for me. It makes complete sense that you shouldn’t be able to write to the storage other contracts have grown, but should be capable of cleaning it. I was mistakenly assuming it would wipe all storage written to by the `<writer>` when reading the eviction slide (including the user’s). Very grateful for the help.

Probably the last stupid question ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=9)  : It seems this is not very far removed from the actor/asset model if there is a ‘safe’ way to move that storage to another address? And if an asset could be isolated, as currently there would be an issue with the storage being a blob. As a hack for this, I can deploy a contract that won’t pay for its rent but writes to a user’s storage (so the storage is isolated) after deployment? Would an `xmove` and partitioned storage make this actor/asset model possible?

(I like the idea of not needing the original contract for moving my assets, doing an exchange. I don’t need to pay any extra fees to resurrect the inevitable transfer function that is built into every contract. I’m having a hunch that the above isn’t as obvious as it seems and isolating the data storage per asset encapsulates a lot more than that. And this doesn’t work for fungible tokens.)

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cygnusfear/48/247_2.png) Cygnusfear:

> It seems this is not very far removed from the actor/asset model if there is a ‘safe’ way to move that storage to another address?

I am afraid I did not study actor/asset model. Will look into it shortly.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cygnusfear/48/247_2.png) Cygnusfear:

> As a hack for this, I can deploy a contract that won’t pay for its rent but writes to a user’s storage (so the storage is isolated) after deployment? Would an  xmove  and partitioned storage make this actor/asset model possible?

I don’t quite understand, sorry ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Under this proposal, in the end, everything which is deployed, will pay rent, otherwise it will create abuse of primitives.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cygnusfear/48/247_2.png) Cygnusfear:

> I like the idea of not needing the original contract for moving my assets, doing an exchange

It might get quite complicated if you want to start delegating writing rights to other contracts. We are trying to propose something that will be able to curb state growth, but that won’t destroy the ecosystem. Other extensions are possible, but only if they can be added without increasing complexity.

---

**Cygnusfear** (2018-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> I don’t quite understand, sorry  Under this proposal, in the end, everything which is deployed, will pay rent, otherwise it will create abuse of primitives.

Sorry, that was a hamfisted way of explaining what I intended to ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12). I’m intrigued by the fact that the rent proposal *almost* makes it possible for contracts/users (actors) to move/transfer/own their assets (items in storage) without any further interaction with the creating contract. This would allow ‘assets’ to be treated as first class-citizens similarly to a users’ ether balance.

However, I’m admittedly not very proficient in the base layer/evm/assembly level. As I understand it, this comes with a lot of increase in complexity. Moving around storage/memory is more complicated than I make it out to be in the above example.

The described proposal in your state rent document is very elegant without doing so and I really appreciate your patience in answering these questions and helping me understand these things a bit more. ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=12)![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cygnusfear/48/247_2.png) Cygnusfear:

> The described proposal in your state rent document is very elegant without doing so and I really appreciate your patience in answering these questions and helping me understand these things a bit more.

Thank you very much ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**fubuloubu** (2018-11-27):

One other random thought: how we actually pay the rent (specifically using the actor/asset model)

The naive way would be to have whatever ether balance an address has be the rent payment. This makes it easier to collect rent for “large, central contracts” – just send ether to that address and it gets deducted at a rate of storage costs. If it runs out, the storage gets archived, then removed after some period (only the root remains).

However, let’s say you want to hibernate your holdings (meaning you will accept the burden of storing the state tree entry matching the root that remains). Your holdings include some significant amount of ether that you don’t want drained as you go into hibernation. A way to do that in my mind might be to make use of “semi-fungible tokens” (related to ERC 1410) where Ether holdings can be split into 2 holding groups: rent payment balance and free (non-rent) holdings. This would help contracts who are programmed to deal with escrow of Ether not to get their balances mixed with the rent payment balance.

---

**cheeselord1** (2018-11-27):

I’ve noticed some focus on “mitigating GasToken” on other forums like ethresear.ch. Why is that? The point of GasToken is to save state and later clear it to get refunds when gas prices are high, so it’s unlikely to continue growing unbounded compared to other contract types.

> I did not include this into the deck, but as it stands at the moment, abandoned contracts (those not used for the last 12 months) represent only 6% of the state.

Super interesting!  From just eyeballing charts 1 and 2, it looks like total state was ~30% of current size 12 months ago.  Is this right?  So if 6% of current state is abandoned, that means 20% of the total state as of 12 months ago is now abandoned?  That may suggest the 6% number will start growing dramatically in the coming months

> Data owners should not be allowed to modify storage written by other contracts. But they should be able to withdraw that write permission, to stop paying for the store.

I’m guessing we would make a contract’s write permission all-or-nothing? E.g. assume a contract stores user balances and debts. If the user could withdraw permission for the debt-storage field, that would enable them to drain the contract.

But then is there also a token-dusting attack vector if a contract’s write permission is all-or-nothing?  E.g. someone can send me dust from millions of tokens on EtherDelta which would make the rent prohibitively high. Unless we require authorization for each storage field used which seems like really complicated UX

---

**AlexeyAkhunov** (2018-11-27):

Adding another response here

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/8e8cbc/48.png) cheeselord1:

> That may suggest the 6% number will start growing dramatically in the coming months

Main reason not to go specifically after abandoned contract is the fact that a spiteful adversary can easily neutralise such measures, and it will wasted work.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/8e8cbc/48.png) cheeselord1:

> debt-storage field

Debt is not an assert of the debtor, but of the creditor. The creditor is the one who should keep it and pay for it. That way, debtor cannot clear away the debt.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/8e8cbc/48.png) cheeselord1:

> But then is there also a token-dusting attack vector if a contract’s write permission is all-or-nothing?

It is not all-or-nothing. On the page 40, there is opcode XGROW, which owner can use to expand the cell writeable by a particular writer. Owner cannot shrink the cell though, only complete remove it

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> deal with escrow of Ether not to get their balances mixed with the rent payment balance

Interesting line of thought. It might be possible to quite easily achieve that with a wrapped ETH token contract, which under the new model will have a constance storage size and can easily sustain itself by eating into the wrapped ETH it contains, or utilising callfee (page 48).

---

**fubuloubu** (2018-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> wrapped ETH token contract

In other words, “RentToken” lol

---

**jvluso** (2018-11-27):

CallFee and Linear cross-contract storage both seem like powerful abstractions. Are these things that you want to add to the base layer or do you think they can be implemented in the scripting language?

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jvluso/48/836_2.png) jvluso:

> CallFee and Linear cross-contract storage both seem like powerful abstractions. Are these things that you want to add to the base layer or do you think they can be implemented in the scripting language?

To the base layer, as they require new opcodes and new consensus structures


*(18 more replies not shown)*
