---
source: magicians
topic_id: 15206
title: "ERC-7390: Vanilla Option Standard"
author: xeway
date: "2023-07-24"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/erc-7390-vanilla-option-standard/15206
views: 2740
likes: 3
posts_count: 15
---

# ERC-7390: Vanilla Option Standard

A standard interface for creating and interacting with vanilla options.

https://github.com/ethereum/ERCs/pull/53

## Replies

**xeway** (2023-07-24):

[You can see an implementation of this ERC here](https://github.com/Xeway/ERC/blob/main/contracts/Option.sol)

---

**mlalma** (2023-08-16):

I went through the EIP as well as the accompanying implementation. Great stuff! I am also interested in bringing different kinds of financial instruments to the blockchain, and vanilla options are a great product to start with.

I have a few comments:

**(1)** Creating a new contract for each option issuance seems a bit sub-optimal. Options are ephemeral by nature, so once the option has expired, the contract just stays on the blockchain and doesn’t do anything. I would propose a change where the parameters of the option are not defined in the contract’s constructor, but instead are given on the create() call, and the create() would return a uint256 id.

The id value would then be passed as a parameter to the buy(), exercise(), retrieveExpiredTokens(), and cancel() function calls to signal which option issuance is the targeted action. Internally, inside the implementing contract, the option issuance data could be saved to a struct, and a mapping (and an incrementing counter) could be used for storing.

In this way, a single contract could hold a large number of option issuances, and in my opinion, it would be a better way to organize the option issuances and reduce fragmentation.

**(2)** When the counterparty pays the premium and takes the other side to buy a call or put, there should be tokens that should be minted for the buyer representing the options. The amount of tokens should be the same as the amount of the underlying asset.

As an example, in the “Concrete Example - Call Option” part, the amount of underlying is 8000000000000000000 LINKs. When the counterparty pays the premium, they should get 8000000000000000000 tokens that represent the amount of LINK tokens that can be bought at the strike price.

Again, due to the ephemeral nature of the options, I don’t think the tokens should be represented by an ERC-20 contract that is created on-the-fly; instead, I would go for ERC-1155 to hold all option tokens in a single contract. Also, when options are represented as tokens, they could be traded independently to other parties.

**(3)** One potential limitation of the current interface design is that on the exercise() method, the buyer must exercise all options. I would suggest that there should be a parameter for the exercise() function to define how many option tokens the buyer wants to exercise. This would make sense, e.g., when the buyer might want to exercise only a portion of the option tokens to hedge and take gains of the currently favorable underlying price while still retaining the other portion to see if the market moves even more in the buyer’s favor (given that buyer still has exercise time left).

When the buyer exercises they need to of course have the amount of option tokens and they need to pay strikePrice * amount of strikeToken to the seller. Anyone who holds option tokens would be able to exercise them during exercise window.

**(4)** For the create method, I would add an array of addresses that are the allowed counterparties to (initially) take the other side. This is the improvement idea mentioned at the end of the ERC, and I think it would make sense to add it. If the array is empty, then it is free-for-all. Now, if suggestions (2) and (3) are taken into account, then there should be no restrictions on who can exercise the underlying as long as they own the tokens that represent the options. If we want to limit this, then there could be an extra boolean parameter for the create() method called “renounceable” that defines if the counterparty can buy/sell the option tokens to other parties as they wish or if those tokens are locked to the counterparty’s address, and only they can exercise them.

**(5)** I would remove from the state variables the type of the option (“european” / “american”). Also I would remove expiration state variable. Instead of these I would define two state variables, exerciseWindowStart and exerciseWindowEnd, which represent when user can start to exercise and when the exercising ends. After exerciseWindowEnd time has passed, seller can call retrieveExpiredTokens() to get the underlying tokens back that have not been exercised.

---

**xeway** (2023-08-16):

Hey, thanks so much for your interest in this EIP!

Here’s my answer for each suggestion:

(1) Yes that’s a really good idea! This would be a change a bit like Uniswap V4 = making a singleton contract. And this would be simpler for users to create a new contract (instead of creating, then calling create() to “enable” the option).

However, I’m not sure this would be a standard (ERC), but rather a “private” protocol on itself (because there would be only one contract on the blockchain). But if this standard is created by every dApp, we should think about how to transfer options between smart contracts.

Maybe another solution to improve gas: make the contract reusable. This mean that after the option is “inactive”, someone (or the same writer), can change all the parameters to create a new option, instead of creating a new smart contract.

(2) So your idea is to create a kind of coupon represented as a token, so that the buyer can “share” his right with multiple people to exercise according to the amount he gave to each of them? It’s really interesting and would brought even more possibilities. But do you think it is more gas efficient to use a system of token (with an ERC-1155), or to simply implement the functionality without token (e.g. a function *shareExercise(uint256 amount, address recipient)* that would store each amount for each address in a map, and when exercising, the contract would verify if msg.sender can exercise)?

(3) Great idea! It would offer more possibilities.

(4) Another great idea, this would (has you said) be the solution to the suggestion written in the EIP ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

(5) Very smart, it would be simpler and probably more gas efficient.

---

**mlalma** (2023-09-01):

Hi,

my (current) proposal for the interface is at the fork that is available on [GitHub - mlalma/ERC-7390: Fork of draft implementation of ERC-7390 spec for hatching out changes to the standard](https://github.com/mlalma/ERC-7390).

I think the key here would be the interface on `IVanillaOption.sol`. It basically is `IOption.sol` with all my prposed changes.

I have updated the `README.md` and documented the interface there. If you could take a look at it, try out the fork and see that the reference implementation (and the related tests) work as expected and then provide some comments back that would be amazing.

For the summary, some of the key changes I would propose are:

- VanillaOptionData struct contains the essential features of a vanilla option in a single struct that is passed to the create() function
- None of the functions return bool stating success / failure. If the function returns, then the action is successful and for any failure an exception is thrown
- There is now ID parameter that needs to be passed around so that single contract can handle multiple option issuances due to the ephemeral nature of the instrument
- Option buyer does not need to buy the whole lot, they can define the amount of options they want to buy (and later on exercise)
- I have added updatePremium() function to enable option seller to change the premium to keep it more in synch

There are probably also other smaller changes, but I think those are the main ones.

-mla

---

**xeway** (2023-10-01):

Hey, sorry for the very late answer.

I looked at your changes and this looks very nice to me!

My only concerns are:

1. in which case data from VanillaOptionData is useful? Do you have any idea or example?
2. in the updatePremium function, shouldn’t we verify that block.timestamp <= issuance[id].data.exerciseWindowEnd?

Thanks a lot for your involvement in this EIP.

---

**mlalma** (2023-10-02):

Hi

Great comments, please find my answers below:

1. My original thinking was that it would be possible to add e.g. access control lists for the addresses that are allowed to buy a particular option issuance or additional parameters for supporting exotic options such as knock-in / knock-out barrier levels.Thinking more of this, maybe any additional data should not be in an extra field on a structure named VanillaOptionData, but any derived contract implementations can handle them as needed. I have removed the data variable from the structure, it didn’t have any effect to the code itself.
2. True - will add the check.

I have done the changes and will open a new pull request for you.

---

**xeway** (2023-10-03):

Hey, thanks for your reply. Sounds good to me, just merged the changes ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**mlalma** (2023-10-09):

Hi,

few proposals for the next things that could be worked on:

(1) (This is your idea ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) ), We could create a separate interface `IERC7390Metadata` for querying contract variables such as `underlyingToken(uint256 id)`, `premium(uint256 id)`, `exerciseWindowStart(uint256 id)` and so forth for providing a defined interface getting the data out of the available option issuances.

(2) I propose adding to the `VanillaOptionData` structure three additional fields: `uint256 underlyingTokenId`, `uint256 strikeTokenId` and `uint256 premiumTokenId`. Reasoning is that right now (only) ERC-20 tokens can be used for underlying, strike and premium. If we added explicit token ids for all these three fields then tokens also from ERC-721 and ERC-1155 standards could be used. If the token is an ERC-20 token then the token id field is simply ignored. This would enable creating e.g. an option where underlying is a (single) ERC-721 token, compound options / options-on-options where underlying token is ERC-1155 from another option issuance or an issuance where option premiums are paid using other options. Lots of possibilities ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Making this change would of course require bunch of changes to reference implementation as it would need to check what is the interface that the given address supports using e.g. ERC-165.

(3) …and that would also lead to my third change proposal, where I would suggest to implement the `supportsInterface()` ERC-165 call on the reference implementation to let other contracts verify that `IERC7390` is implemented.

Any thoughts / comments?

---

**xeway** (2023-10-15):

Hey,

These are really great ideas, especially the second one.

Nothing else to say tbh, except thanks for these improvement ideas.

Let’s go building!

---

**xeway** (2023-10-27):

Hey, just to let you know that the previous PR was closed because they moved ERC-only proposals to another repository. Here’s the new PR: [Add ERC-7390: Vanilla Options by Xeway · Pull Request #53 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/53)

---

**xeway** (2023-11-10):

Hey,

Just made small improvements:

- Instead of adding a brand new IERC7390Metadata interface, I thought it was actually useless to do it since we only want to implement one function (that I called issuance(uint256 id)). Moreover, by looking at OpenZeppelin’s ERC20 contracts, I found that balanceOf (which is similar to issuance in the sense that it returns an element of a map with the key that correspond to the parameter) is not in the metadata extension interface but in the main IERC20 interface. So I guess the best is to copy the rules of OpenZeppelin’s contracts, so we know it’s more formal.
- Speaking of which, still by looking at OZ code, I found that functions are declared external in the interface but are declared as public in the implementation. I’m not sure, but I think this is a tip to be able to call the function externally and internally (public’s property) while being more gas-efficient (external’s property). I’m waiting for OZ developers to confirm it’s right. But I implemented it anyway in ERC7390 code implementation.
- Made attributes private and only accessible with function defined in the interface. issuanceCounter is private but doesn’t have a function to access to, because this is not really an important data for an external entity.

Sorry this isn’t a lot of work, kinda busy these times.

Hope y’all have a great day

---

**zerosnacks** (2023-12-04):

Hi [@xeway](/u/xeway)

You may be interested in using [EIP-6909](https://ethereum-magicians.org/t/eip-6909-multi-token-standard/13891) as a replacement for ERC1155 in the reference implementation.

---

**xeway** (2023-12-27):

Hey, so sorry for the late answer (as always ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)).

Didn’t know about ERC6909, it would way simpler for the current usecase of EIP-7390.

My concern is that ERC6909 is still a Draft, not very famous… so is it worth the risk to implement it?

---

**zerosnacks** (2024-01-09):

I would say it is worth looking into, the spec is quite close to being finalised and already has multiple [implementations](https://github.com/Vectorized/solady/blob/main/src/tokens/ERC6909.sol) and drafts of extensions (like an [ERC4626-like interface](https://github.com/jtriley-eth/ERC-6909/blob/main/src/ERC6909ib.sol)).

