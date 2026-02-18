---
source: magicians
topic_id: 10913
title: "ERC-5679: Mint and Burn Tokens"
author: xinbenlv
date: "2022-09-18"
category: ERCs
tags: [erc, token, erc-721, erc-20, erc1155]
url: https://ethereum-magicians.org/t/erc-5679-mint-and-burn-tokens/10913
views: 4086
likes: 13
posts_count: 21
---

# ERC-5679: Mint and Burn Tokens

Hi all, I am proposing a new ERC to extend the ERC-20, ERC-721 and ERC-1155 with ability to Mint and Burn.

See the ERC here [ERC-5679: Token Minting and Burning](https://eips.ethereum.org/EIPS/eip-5679)

Your feedback is appreciated.

Reference Implementations Version 0x1002

https://goerli.etherscan.io/address/0x72D9c2D49F5A2915D7A3c23B1FD5d645dFe492ac#code

https://goerli.etherscan.io/address/0x8965B739DF91eB621D9FF06af4A48198f711BbD9#code

https://goerli.etherscan.io/address/0xE45072F6ee31cBE07FC232f61c61C6Bd000d9ea2#code

## Replies

**TimDaub** (2022-09-29):

I find this proposal very applaudable, especially as I had been calling out not standardizing mint and burn in a previous post on this forum: [EIP-4973 - Account-bound Tokens - #129 by TimDaub](https://ethereum-magicians.org/t/eip-4973-account-bound-tokens/8825/129)

However, I think the proposal would be stronger if it rigorously created separate documents for EIP-721, EIP-1155, and EIP-20’s mint functions. E.g., I have no knowledge whatsoever about EIP-1155 and only very limited knowledge about EIP-20. Hence, although I’d like to help you review and improve the document, my knowledge is mainly in EIP-721 - but I don’t feel like being able to make suggestions for the lack of the other standard document’s inclusion.

Still, thanks for taking this on, I think it’s an important step in the right direction!

---

**xinbenlv** (2022-09-29):

Thank you for the feedback [@TimDaub](/u/timdaub)

I was thinking of the same thing. I hesitate because there is also ways to devide this EIP to more finegrain, e.g. by EIP-20Mint EIP-20Burn, EIP-721Mint, EIP-721Burn etc. And it seems harder for implementers to understand they actually are the same standard and shall follow the same behavior. So, while I am open or even weakly lean towards agreeing with you, let’s wait for other community members to see what they think, WDYT?

In the meanwhile, it’d be great if you could start reviewing it it from EIP-721 perspective

---

**xinbenlv** (2022-10-04):

[@fulldecent](/u/fulldecent) I think this EIP is a perfect example of what you describe in the [What kinds of things should be standardized? – William Entriken Blog](https://blog.phor.net/2022/09/30/What-kinds-of-things-should-be-standardized.html) which adoptions has come before. Love to hear what you think

---

**fulldecent** (2022-10-04):

Here is the key quote:

> A standard only deserves to be written if multiple people adhere to it and people depend on its surface area.

The missing part in the justification for ERC-5679 (DRAFT) is I don’t see any software that depends on performing an ERC-721 mint across any arbitrary contract.

Minting is nearly always attached to payment, randomness, referral fees, auctions, and other complicated mechanisms. This is why every NFT project has its own website to onboard the customers and charge money in a way that is appropriate for that project.

Conceptually, ERC-5679 (DRAFT) is saying that it should be valuable for somebody (who?) to make a website called MINT NFT where you can paste in any Ethereum address and if that address is a compliant ERC-5679 (DRAFT) contract then it will mint you that token. Such a website does not strike me as feasible, much less current best practice. Therefore this surface area is not worth standardizing.

---

**xinbenlv** (2022-10-04):

> Minting is nearly always attached to payment, randomness, referral fees, auctions, and other complicated mechanisms. This is why every NFT project has its own website to onboard the customers and charge money in a way that is appropriate for that project.
> Conceptually, ERC-5679 (DRAFT) is saying that it should be valuable for somebody (who?) to make a website called MINT NFT where you can paste in any Ethereum address and if that address is a compliant ERC-5679 (DRAFT) contract then it will mint you that token. Such a website does not strike me as feasible, much less current best practice.

Just curious, with the same argument the recently finalized [ERC-5313: Light Contract Ownership](https://eips.ethereum.org/EIPS/eip-5313), is conceptually arguing that somebody (who?) would like to check owner of a given contract. Does that happen very often when owner is not the specific project? At least for now owner checking is as specialized as minting and burning as far as I can see.

I am not questing that EIP-5313 shall not be finalized. I am questioning that by your own standard, EIP-5313 doesn’t seem to pass.

The standardization act for the purpose of drive consensus, and sometimes that consensus need to happen before people can start using it.

---

**fulldecent** (2022-10-04):

Yes, this is a good one to review.

EIP-5313: Light Contract Ownership is related to a tool checking the ownership of any arbitrary compliant NFT contract—and where the tool requires those compliant contracts to work in a specific way.

Such a tool does exist and is widely used. OpenSea is one of them. OpenSea interrogates every NFT contract using EIP-5313 to find who the owner is and then grant them permissions to administer where royalties are paid to. Other marketplaces use this information as well.

OpenSea has been using the mechanism documented in EIP-5313 for years before I wrote EIP-5313.

---

**xinbenlv** (2022-10-04):

Given the EIP-5313 is a subset of EIP-173, one could argue that OpenSea is just using EIP-173.

Otherwise, if the argument (that OpenSea is using EIP-5313) holds, the same apply to arbitrary subset of existing widely adopted EIPs. Maybe one should go ahead and create “Light Transfer” for just one single method `transfer...`

I am not saying EIP-5313 is not valuable. I am just saying author of EIP-5313 has to proof that EIP-5313 has merit despite that EIP-173 exists, in which by your article that [What kinds of things should be standardized? – William Entriken Blog](https://blog.phor.net/2022/09/30/What-kinds-of-things-should-be-standardized.html) it should test that a wide interest exists to *ONLY* use owner() but NOTHING else in the EIP-173. But I fail to see any discussion in EIP-5313 addressed that.

I wouldn’t be surprised that once EIP-5313 is proposed, new clients might lean to adopt it and only care about `owner()` method an nothing else, but in this case it would be **adoption *after* standardization**.

---

**fulldecent** (2022-10-04):

OpenSea has documented that it was required to use ERC-173 to have your contract automatically validated. Actually worse, they used confusing language about what might be required and then just linked to an implementation in OpenZeppelin.

OpenSea is the largest and most notable consumer of ERC-173/ERC-5313 data.

Unfortunately, using ERC-173 has the side effect of restricting types of contract ownership, such as where it is dynamically looked up (since dynamic lookup cannot emit an event.

I reviewed with OS documentation engineers, performed experiments and confirmed that the only surface area that is used or required was ERC-5313 and the existing documentation about requiring ERC-173 was wrong… that was my motivation to write ERC-5313. The ERC-5313 discussion *does* note OpenSea’s existing well-known implementation as the primary motivation for ERC-5313.

You are right, there is only mention of another implementation, this is Light.art, a deployed sold out NFT series, that benefits from the smaller surface area not possible with ERC-173. Other implementations of the owner() exist in the wild and we failed to bring these up in discussion (sadly only looking at the whale in the room, OS).

---

Of course, once anything is standardized (or not!) it can be copied and implemented elsewhere.

---

**xinbenlv** (2022-10-04):

For this thread, I think we have drift off a bit from the original goal to get feedback about Mint and Burn token interfaces whether that EIP, specifically the specs shall be revised in anyway.

I’d be more than happy to continue the conversation and friendly debate with you.

I think our discussion in the past a few days are mainly now about whether the criteria of “what should be standardized”. Can I suggest that we create a separate post in the FEM to get feedback of “what should be standardized”. Let’s continue the debate about the article in a new thread, and keep this thread focusing on the ERC-5679?

---

**xinbenlv** (2022-10-05):

Hi [@TimDaub](/u/timdaub) thanks for reaching out. Do you have further feedback for the EIP?

---

**TimDaub** (2022-10-05):

Regarding the previous discussion, while I can see the issue of nobody wanting to have a mint-open EIP721 token because today it’s obvious that this functionality has to be permissioned, I’d ask commenters to refrain from discouragement. In case it is truly useless to have a document standardizing minting and burning, I guess this work will simply be irrelevant and forgotten - but won’t do any harm.

Still, as I’ve already mentioned in [EIP-4973 - Account-bound Tokens - #129 by TimDaub](https://ethereum-magicians.org/t/eip-4973-account-bound-tokens/8825/129), I’m skeptical of both mint and burn not being canonically (at least optionally) available. I’d see this effort as explorative programming. In my own experience, merely expressing one self can spawn new ideas elsewhere, so I can only encourage you to continue working on this.

IMO a problem that is potentially solveable is this: When everybody can call mint as much as they want, how can EIP-721 tokens have value?

---

**xinbenlv** (2022-10-06):

That’s very good question and concern. And I think I am confident to also give you a good answer:

There is multiple ways to do permission. Centralized admin-role based permission is only one way.

here are other ways

1. Allowing auto-sale via native ETHs or exchange of other ERC721 / ERC20

```nohighlight
contract SomeNFT {
const uint256 CHARGE = ...;
fallback() {
  require(msg.value > CHARGE);
  mint(nextId, ...);
  // increase nextId etc;
}
}

```

In this contract above, anyone who send a native ETH of that evm chain above the `CHARGE` will be minted one NFT, no admin permission is involved.

1b. Variant of 1, auto-sale via receiving ERC20*/ERC721/ERC1155. assuming the name of token is called “GoldToken”

contract SomeNFT is ERC1155TokenReceiver {

function OnERC1155TokenReceived(

address operator, address from, address to, uint256 tokenId, uint256 amount, bytes calldata data) {

require(operator == intendedAddressOfGoldToken);

require(amount >= CHARGE);

mint(…);

}

}

1. Authorized Minting via a Smart Proposal(EIP-5247)

```nohighlight
struct Proposal {
  uint256 id;
  address contract;
  bytes memory txForMint;
}

contract SomeDAO {
  function execute(Proposal proposal) public onlyPassed  {
    require(_isProposalPassedAndLocked(proposal.id));
    address erc721 = proposal.contract;
    erc721.call(txForMint);
  }
}
```

In this contract, a DAO can agree to mint one or many tokens but based on a Smart Proposal which can be voted upon.

1. Allow a mint but endorsed by Admin via Smart Endorsement(EIP-5453)

```nohighlight
contract SomeNFT {
  function mint(...) public onlyEndorsedByAdmin() {
    ...
  }
}
```

In this contract, an admin can sign an offchain endorsement message but the claimer will actually create the transaction TX.

1. Mint NFT via auctions

```nohighlight
contract SomeNFT {
  function commit() {
    ...
  }
  function bid(tokenId) { }

  function mint(...) public onlyWonAuction() {
    ...
  }
  modifier onlyWonAuction {
    // Code logic for msg.sender has valid committed bid price
    // Code logic for msg.sender has bid highest price within the a deadline
  }
}
```

---

**xtools-at** (2023-02-23):

hey, i think i’ve spotted a typo in the spec, could anyone confirm please?

so all interface methods have this input param

```auto
bytes calldata _data
```

all but {IERC5679Ext1155-burn} which takes

```auto
bytes[] calldata _data
->
function burn(address _from, uint256 _id, uint256 _amount, bytes[] calldata _data) external;
```

it doesn’t make sense to me to have a different data type for this particular case, anyone know more?

---

**radek** (2023-02-27):

Can [@xinbenlv](/u/xinbenlv) elaborate why bytes calldata _data is mandatory? For ERC20 mint/burn?

When you look on OZ implementation: [openzeppelin-contracts/ERC20.sol at master · OpenZeppelin/openzeppelin-contracts · GitHub](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol)

mint and burn just have (address account, uint256 amount).

I assume most ERC20 will have that.

---

**xinbenlv** (2023-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xtools-at/48/8358_2.png) xtools-at:

> hey, i think i’ve spotted a typo in the spec, could anyone confirm please?
>
>
> so all interface methods have this input param
>
>
>
> ```auto
> bytes calldata _data
> ```
>
>
>
> all but {IERC5679Ext1155-burn} which takes
>
>
>
> ```auto
> bytes[] calldata _data
> ```
>
>
>
> it doesn’t make sense to me to have a different data type for this particular case, anyone know more?

Hi, [@xtools-at](/u/xtools-at)

This is a good finding!

It shall actually be `bytes` instead of `bytes[]`. That’s a typo. Let me fix it and update the ERC draft.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> Can @xinbenlv elaborate why bytes calldata _data is mandatory? For ERC20 mint/burn?

Yes, this is a convention started by ERC721 and followed by ERC1155 and many others. By adding a `bytes _extraData` field it allows extension. For more details you could see [ERC-5750: General Extensibility for Method Behaviors](https://eips.ethereum.org/EIPS/eip-5750) for the motivation and rationale sections.

---

**radek** (2023-03-01):

I understand the convention for extensibility. My point is whether for ERC20 the calldata _data param must be mandatory.

Since most ERC20 tokens have mint / burn without this.

So my proposal is to make that optional within the standard for ERC20 and to have declared 2 kinds of interfaces.

---

**xinbenlv** (2023-03-01):

Could you share some of these contracts’s deployed address that you mentioned?

---

**radek** (2023-03-03):

Example: USDC: https://etherscan.io/address/0xa2327a938febf5fec13bacfb16ae10ecbc4cbdcf#code

line: 697 `function mint(address _to, uint256 _amount)`

Not having the overall chain statistics here, but since this is the outcome of the OZ ERC20 wizard:

`    function mint(address to, uint256 amount) public onlyOwner {         _mint(to, amount);     }`

I really assume most existing  ERC20 will have it just like that.

Note to others - this is only discussing ERC20 - I am not discussing 721 or 1155.

---

**radek** (2023-03-15):

For the future reference - conclusions related to ERC20: [Option for ERC20 reflecting common no calldata approach by radeksvarz · Pull Request #6685 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6685)

> This EIP is in the Final state, and may only be modified to correct errata. I would recommend standardizing this interface in its own EIP if you feel it can stand alone.

This means ERC20 with common mint/burn functions having `(address account, uint256 amount)` MUST NOT declare being compatible with [ERC-5679: Mint and Burn Tokens](https://ethereum-magicians.org/t/erc-5679-mint-and-burn-tokens/10913).

I assume there is no demand to have the additional EIP for common `mint/burn (address account, uint256 amount)` as the PR comment suggested.

---

**xtools-at** (2023-03-31):

it seems the erc still includes the wrong param. not sure if it being final is a problem, i think errata should still be possible. let me know if i can do anything to help

