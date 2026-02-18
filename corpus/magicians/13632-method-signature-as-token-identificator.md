---
source: magicians
topic_id: 13632
title: Method signature as token identificator
author: peersky
date: "2023-04-01"
category: Magicians > Primordial Soup
tags: [nft, token, semantic, permission, rbac]
url: https://ethereum-magicians.org/t/method-signature-as-token-identificator/13632
views: 1125
likes: 0
posts_count: 6
---

# Method signature as token identificator

Hi everyone, I want to bring up here a discussion for an idea that been out in my head for a while now.

The concept is to use `msg.sig` of an interface being called to calculate NFT `tokenId` that will define interface access permissions.

This is absolutely possible since `msg.sig` number space is `bytes4` while `tokenId` number space is larger that that - `bytes32`

I have written down a proof of concept ([github repo](https://github.com/peersky/NFT_Access)) showing how with a simple proxy such protocol can be used to allow access to certain interfaces only for those who have a token.

I’ve also explored additional use-cases such as using extra number space of token Id to specify different types of an access for a same interface - based on tokenId you either have to simply be owner of it, or proxy might require you to lock/pay/burn this access token.

Im not sure if this idea is ready to be filed as an EIP, but certainly I feel the potential and would love to hear more feedback and bring up the discussion to understand whether it’s worth proceeding further with filing an EIP

I have also more detailed write up about potential of such access pattern in my [blog](https://peersky.xyz/blog/nft-rbac/), article is also readable as md in [github](https://github.com/peersky/daococoa/blob/main/apps/bestofweb/content/nft-rbac.mdx)

Looking forward any feedback from Magicians community here,

Cheers!

## Replies

**JamesB** (2023-04-03):

Hi [@peersky](/u/peersky), we are working on something similar but coming from a different end. I think there’s very much a good usecase here.

Our project is ‘TokenScript’ which defines an external interface for tokens (rather than internal in your case). I like the simplicity of your concept - we have permission rules defined in the script but having them codified into the token itself would be useful and could replace a few of those rules.

For example, we define a script that allows you to use an NFT as a door token; our [EIP-5169](https://ethereum-magicians.org/t/eip-5169-client-script-uri-for-token-contracts/9674/3) provides a link to the script within the token so a wallet or website implementing TokenScript can fetch this, check authentication (you can use IPFS for implicit authentication, although updates are an issue) and then the host can provide the external interface needed to use the token. [Here’s the repo showing our office door code/firmware](https://github.com/AlphaWallet/Web3E-Application/tree/master/New%20Office%20Door).

I usually add a class to my contracts which implement EIP-5169 that allow multiple editors with different permission levels access to different settings, your idea would definitely benefit that:

```auto
abstract contract MultiOwnable is Ownable {
    mapping(address => bool) private _admins;

    /**
     * @dev Initializes the contract setting the deployer as the initial owner.
     */
    constructor() Ownable() {
        _admins[_msgSender()] = true;
    }

    function addAdmin(address newAdmin) public onlyOwner {
        _admins[newAdmin] = true;
    }

    function revokeAdmin(address currentAdmin) public onlyOwner {
        delete _admins[currentAdmin];
    }

    function isAdmin(address sender) public view returns(bool) {
        return _admins[sender];
    }

    /**
     * @dev Throws if called by a non-admin
     */
    modifier onlyAdmins() {
        require(_admins[_msgSender()] == true, "Ownable: caller is not an admin");
        _;
    }
}
```

---

**peersky** (2023-04-03):

Thanks [@JamesB](/u/jamesb) for a feedback. Indeed there are few of similar protocols emerging out from NFT space who are elaborating similar architectures.

They all share in common great interoperability and encapsulation of permission in a form of a sharable token. Your tokenScript is one such.

Another can be referred to moonstream team led by [@zomglings](/u/zomglings) working on [Terminus](https://github.com/bugout-dev/dao/blob/main/docs/terminus.md)

From the feedback I’m getting it seems that my idea actually can accompany such protocols in a way of helping to define a **semantic permission token identification** trough a generalised EIP.

---

**peersky** (2023-04-03):

Based on a feedback I was getting I want to clarify some topics:

**1. Use case of NFT’s as permission token**

By tokenising  access permissions allows to treat access permissions as market liquidity rather than a fixed, non liquid value. That is opening new doors for a technologies where by balancing supply of *permissions* in the market protocols can manage own economy.

Existing NFT marketplaces, bridges and protocols that implement 721/1155 can be reused

**2. Benefits of having semantic permission token id determination**

The NFT provided bonuses can be utilised without semantic token ID calculation.

What THIS brings - is **allows** to be very deterministic and implementation agnostic. It should not matter whether access control is implemented via proxy, directly in permissioned contract or inside the NFT.

Whether TokenScript, Terminus or any other protocol is used behind the scene, **all** what marketplace, or security auditor has to check to understand what tokens are in interested - simply check that target contract supports semantic permission token identification.

For example. This means that one can have full information about which token Ids to look from two items:

1. knowing the fact that contract supports this permissioning
2. Having contract ABI

Which makes it even agnostic from a deployed token addresses and can be already audited and inspected in early development lifecycle

---

**peersky** (2023-04-03):

Another thing to note that current PoC has a possible collision for hashes because tokenId’s being offseted for (0…3) to define different kinds of requirements.

Right now I think that best way around that is to add these offsets in leftmost byte (msb) of the token id. That way exact signature hash match (`msg.sig` casted to `uint256`) can stay the same, but incrementing can be done by simple OR bitewise mask.

---

**peersky** (2023-05-12):

Some updated thoughts on this:

After discussing with peers and validating previous idea of NFT defined Role based Access it is clear that there are many parties already approaching a sacred grail of NFT based permission management. Hence I instead of access management I want to focus attention on most important in this idea - *matching token Id to interface name creates semantical meaning*.Having such semantic definition for token Ids meets a very common metaverse builders issue - there is hard to find common ground between multiple different standards and marketplaces.

## Possible simple implementation

Smart contract supporting such semantic token id matching must implement:

- supportsInterface specific to this standards
- getPermissionTokenContract() public view returns (address)

These two should be sufficient in order to get required checks from external contractsThe implementation of the access logic can be left out of standardizing, it can be up to developer to implement this, the only thing left to standardize is the token ids and related privileges themselves. I.e.:

1. tokenId = msg.sig + 0 → unlimited access for one having that token
2. tokenId = msg.sig + 1 → access by locking token in the contract for time of operation
3. tokenId = msg.sig + 2 → access by burning a token in exchange of calling the interface
4. tokenId = msg.sig + 3 → access by sending a token to target contract

Rest implementations on how the access checks are performed can be left to a particular implementations.

[Original writeup](https://peersky.xyz/blog/token-id-matching-to-msg-sig/)

