---
source: magicians
topic_id: 9901
title: "EIP-1972: ERC-721 Lending Oracle"
author: MakC-Ukr
date: "2022-07-11"
category: EIPs
tags: [nft, lending]
url: https://ethereum-magicians.org/t/eip-1972-erc-721-lending-oracle/9901
views: 1382
likes: 1
posts_count: 7
---

# EIP-1972: ERC-721 Lending Oracle

Hi,

In today’s gaming ecosystem on the blockchain, a considerable amount of time is wasted by the game developers to integrate NFTs into their games. Since many games have already been deployed, so are their contracts. Hence they can’t be amended. However, many games and applications can increase their reach to users by implementing lending of their ERC721 or ERC1155 tokens.

I have thought of an ERC standard of Lending Oracles that will hold the information about lending (leasing) agreements between ERC721 token owners and borrowers in a mapping. If the ERC standard gets adopted, multiple lending oracles could be built in the ecosystem that would allow the game developers to call the standard functions and understand if the ERC721 token is lent out to someone.

Please take a look:

## Abstract

The implementation for this contract allows an owner of a NFT contract to transfer his NFT to the “oracle” contract address by calling `safeTransfer` (or `safeTransferFrom`) and sending relevant information in the ‘bytes’ parameter as calldata. The contract holds this information in mappings and also stores the deadlines until which a lending contract is valid. The relevant functions `isCurrentlyRented` , `extendAgreement`, `claimNftBack`, `realOwner` allow the mentioned functionality. The game contracts and the games’ frontends can read data off the “oracle” and know about the lending agreements.

Furthermore, the current contract can be deployed only once for different ERC721 contracts since the lending agreements also hold the information about the contract address of ERC721.

## Motivation

The current specification is a suggested interface for a lending oracle to be implemented on chain. Currently, blockchain games utilize ERC721 tokens to represent a hero in the game or other in-game assets. In order to implement possibility for lending, the ERC721 contract has to be amended (which is not so convenient). The current specification allows the game devs to deploy a lending “oracle” contract on chain which keeps record of completed lending agreements without changing the core ERC721 contract of the game asset NFTs.

### NOTES:

- The boolean false MUST be handled if returned by the isCurrentlyRented function.
- A lending agreement MUST be created only when an ERC721 is transferred to this Lending Oracle to prevent users from double-lending their NFTs to multiple Lending Oracles

### Functions

##### isCurrentlyRented

Returns whether a certain ERC721 contract is currently rented, and returns who is the renter if True.

`function isCurrentlyRented(address _contractAddress, uint _tokenId) public view returns(bool, address)`

##### onERC721Received

Returns The functions selector of `onERC721Received`

SHOULD handle the logic of creating lending agreements whenever an ERC721 is transferred using `safeTransferFrom`

`function onERC721Received(address, address from, uint256 tokenId, bytes calldata data ) public override returns (bytes4)`

##### extendAgreement

Returns the new deadline for the mentioned non fungible’s lending agreement.

OPTIONAL - Should extend the lending agreement. MUST be called only by an the actual owner of the ERC721 (tokenLord).

`function extendAgreement(address _contractAddress, uint _tokenId, uint _blocksExtended) public  returns (uint)`

##### realOwner

Returns the address of the actual owner (tokenLord) of a rented ERC721. MUST make sure that the ERC721 is currently rented.

`function realOwner(address _contractAddress, uint _tokenId) public  view  returns(address currOwner)`

##### currentRenter

Returns the address of the renter of a rented ERC721. MUST make sure that the ERC721 is currently rented.

`function currentRenter(address _contractAddress, uint _tokenId) public  view  returns(address currRenter)`

##### dataEncoder

Returns the byte representation of the data that must be sent to the current contract with the `safeTransferFrom` function. Each contract may have its on implementation of the same. The data may include the information about the deadline of the lending agreement, the address which is renting the token.

`function dataEncoder(address _contractAddress, address _tokenRenter, uint _lendForBlocks) public pure returns(bytes memory)`

##### isLendingOracle

Returns the selector of the isLendingOracle function itself. Will be used by the gaming contract in order to confirm if the owner of an NFT is a lending oracle.

`function isLendingOracle() external pure virtual returns (bytes4)`

##### claimBack

If the lending agreement has ended past the deadline, the *real owner* SHOULD be able to claim his ERC721 token back.

`function claimBack(address _contractAddress, uint _tokenId) public`

## Rationale

The design of the interface was motivated by the requirement of lending agreements to be made possible for ERC721-standard tokens without having to change the code of the Non-fungible Tokens themselves and having cross-contract interoperability of lending protocols. Many ERC721 tokens today have their own lending systems implemented but they lack the generalised approach to solving the problem of lending and borrowing. The current implementation ensures that previously deployed games/applications can allow their users to lend/borrow ERC721’s by simply tweaking the code in the frontend of the game/application (to check if the owner of the ERC721 is a “Lending Oracle” and take appropriate actions if yes).

A diagram on working of an example interaction structure can be found [here](https://ibb.co/72RwX5c)

## Backwards Compatibility

The ERC standard that we propose does not require the ERC721 standard to implement any new functions. The `safeTransfer` and `safeTransferFrom` functions were present in the standard implementation put forward by EIP721 in January 2018. The current lending protocol would be compatible with all the ERC721’s written as per the standard.

In use case of gaming especially the issue of backwards compatibility may be benign. Many blockchain-based games have systems of ERC20 token emissions as prizes (incentives) for playing the game. With the added logic of an ERC721 being rented it may be unclear of how the distribution of the ERC20 tokens must be handled. In the Reference Implementation section, we also propose a standard way fo handling ERC20 token rewards, however that method needs to tweak the smart contract of the ERC20 utility (reward) token. If the same is not possible, the games should explicitly discourage users from lending out their ERC721 to some other user using the “Lending oracles” currently being put forward.

## Security Considerations

- The ERC721 tokens should be transferred to the contract only with the safeTransferFrom function as implemented in EIP721.
- When transferring the token, the bytes argument passed in calldata must be ensured to be in a correct format (as specified by the “oracle” contract to which the ERC721 is being transferred). Note: the dataEncoder funciton (if implemented) may be used for a more clear understanding.

P.S. I am not sure how EIP number is supposed to be chosen, so please let me know if there is a conflict with the one I chose.

## Replies

**thetrainman** (2022-07-24):

Interesting idea and I can see the benefit.

Games require the NFT to be in the gamers wallet to play (so it can’t remain inside the lending oracle contract and therefore it’s not “owned” by the lending oracle during a lease). The Gamer is the Renter and therefore the NFT is in their wallet, after the lending period is over - how does the lending oracle take back and send the NFT back to the original Owner. The oracle contract is NOT the current owner so it can’t do this right?

Am I missing something here.

---

**MakC-Ukr** (2022-07-24):

So the idea is that that the owner of the NFT is the contract itself, not the user taking the loan and playing. The function `isLendingOracle` is supposed to return specific `bytes4` (the selector of the `isLendingOracle` function) value which signifies that the owner of the NFT is a contract of type “lending oracle”. It is up to the games then to call the `isCurrentlyRented` function to check who is the NFT rented to and it must coincide with the address claiming to have rented the ERC721 token.

So, obviously there is some minimal actions needed to be done from the games’ side in order to implement this system as well. The process would go on something like this:

1. Address Anne rents an ERC721 from the lending oracle from Bob
2. Anne opens the game frontend and presses “Play with a rented NFT”
3. Anne enters the tokenId of the rented ERC721
4. The game reads the on-chain data, and finds the address X of the renter of the mentioned tokenId
5. Annes signs a signature to verify that she owns wallet X
6. The game allows Anne to play

(In case of any  rewards in form of ERC20 the game can transfer them to the *lending oracle* and Anne can later withdraw her part of the rewards and Bob can get his shares. This implementation for token rewards can be implemented, however, I have not added the details to this EIP in order to avoid complication).

Also, do note the there is no kind of centralisation around the lending oracle since any project can implement the current EIP and a game would be able to write a generalised code for all such oracles.

---

**thetrainman** (2022-07-25):

Ok got it. Tnx for the clarification

1. Comment: “no centralization” - yes makes sense. The owner of the NFT collection is the owner of the lending oracle for that collection. So the lending oracle is game specific infrastructure.
2. Comment: given the game is the owner of the lending contract, it then makes sense for the split ERC20 payouts to be coupled within the lending oracle… or else, it might be better to stay independent so the lending oracle is purely a generic NFT leasing solution. Also, an argument can be made to decouple the lending oracle from holding ERC20 so it remains less of a target for attacks as it holds only the bare minimum it needs (NFTs) to provide the leasing functionality.
3. Question: How would this work in the instance that the game airdrops extra NFTs to the NFT holder (game Character upgrades, mystery boxes etc) - basically rewards tied to the gamer playing with the NFT. Do these also need to be sent to the lending oracle and split up between Owner and Renter? Similar to the ERC20 payouts. How do you split the NFT token rewards?
4. Comment: Would you say that this is more of a “lending service” than a oracle? As it’s a service that coordinates NFT lending… to me oracles are decoupled from specific services or verticals like gaming and provide generic distributed consensus of real world data state. This is my opinion.
5. Question: who’s responsibility is it to end the leasing period and send back the NFT after the timeframe ends? Eg Alice is the owner, Alice leases it for 1 month and Bob rents it. At the end of the 1 month, does Alice explicitly need to self claim the NFT from the oracle contract back into her personal wallet? Or is there anyway for the oracle to self execute the “end lease” logic and distribute the rewards and NFTs back to their respective owners. Also - this brings up some other questions around what happens if the lease ends and the NFT has a new owner but the game does not check frequently enough and continues to rewards the old renter…

---

**MakC-Ukr** (2022-07-25):

Thanks for the really good questions, that allow me to describe the protocol even in more detail. So , here we go

1. Agreed
2. Agreed. This is the reason we have not added this functionality for now, since it is probably safer to add the proposals that do one thing good enough rather than multiple things but not perfectly.
3. Let’s imagine that the game wishes to airdrop some tokens to their users who were using the product. There are 2 versions of this:

- the game believes it to be fair to airdrop the users who own the game’s NFTs. In this case, almost always the current owner of the game-specific ERC721 token is rewarded. This is what I have experienced till now , and believe this to be fair enough.
- the game believes it to be fair to reward the users who had played their game at some point in the past. Now, since this would anyways be handled at the frontend (the games would anyways have data about which game was played when). On the frontend side the game can also easily get the list of addresses that played the game in a specified period of time. The benefit of this oracle is that all the history of lending agreement is on chain and confirmed. This helps the gamers to also build their history in the game and proof of their obedience (which could potentially be used for undercollateralized lending in the future as well)

1. Yes, this allows some sort of leasing of ERC721 tokens. However, the reason we propose it to be called an oracle so that it underlines the working of the protocol. It is only an on-chain system that has the information about the lending agreements put in place and their details (for e.g. deadline). Since it holds the information and doesn’t specifically transfer the ERC721 to the renter (and hence doesn’t fulfil one of the requirements of a leasing agreement as we know it). The intention was to avoid this potential confusion. However, this is debatable and I would like to hear your thoughts on it (and others’).
2. This point should be left open since different oracles (or leasing services) could implement this on their own. One possible implementation is to leave it to the real owner of the NFT to call function claimBack(address _contractAddress, uint _tokenId) public and claim their token back. Simultaneously, the lender can return the ERC721 back to the owner by calling the transaction. The contract cannot “self execute the ‘end lease’ logic and distribute the rewards and NFTs back to their respective owners” since a transaction can only be initiated by an EOA on EVM. However, if the oracle service wishes to, they can use a relayer for that which would return the NFT.

I had missed the `claimBack` function in the original post and have added it now.

---

**MakC-Ukr** (2022-08-06):

Here is an example implementation of the EIP: [GitHub - MakC-Ukr/erc721-lending-oracle: EIP1972: Lending oracle for ERC721's implementations. Link for submitter EIP in README](https://github.com/MakC-Ukr/erc721-lending-oracle)

---

**thetrainman** (2022-08-27):

Thanks for the explanation and sorry about the delay in response. Covid got me.

Let me go over your example implementation on Github.

I also work on [itheum.io](http://itheum.io) and we have been looking at NFT Lending for Data Licensing… this is why your EIP caught my eye as we were looking at building a custom contract that handled it. We also work heavily with gaming data and are influenced by web3 NFT game designs so there is overlap in that vertical as well.

1. Question: Have you done much research on how existing NFT lending solutions work?  We had been looking at aavegotchi’s lending solution (How to Lend Your Aavegotchi NFT | The Curve). Do you know if there any any EIP/ERC standards already established and used by projects like aavegotchi?

