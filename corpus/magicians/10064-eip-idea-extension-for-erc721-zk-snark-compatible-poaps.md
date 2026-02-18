---
source: magicians
topic_id: 10064
title: EIP-IDEA Extension for ERC721 - zk-SNARK compatible POAPs
author: Nerolation
date: "2022-07-23"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-idea-extension-for-erc721-zk-snark-compatible-poaps/10064
views: 1638
likes: 2
posts_count: 9
---

# EIP-IDEA Extension for ERC721 - zk-SNARK compatible POAPs

EDIT: **I have generalised the idea a little bit more under [this thread](https://ethereum-magicians.org/t/eip-0000-erc-721-merkle-provable-ownership-extension/10154).** You will also find the draft of the EIP and its implementation posted there. In this thread, I wanted to quickly discuss the idea and find fellows to collaborate with.

I’m thinking of an extension for the ERC-721 standard which would add a zk-SNARK interface to it.

The rational behind the idea is enabling the receivers of POAPs to proof their ownership without revealing the owners identity. As mentioned by Vitalik in a post on Soulbound tokens, having the option to proof ownerships without revealing identities would be a significant improvement to privacy in general.

Imagine, ETHGlobal wants to give out POAPs to the hackathon attendants, while allowing them to claim their POA without revealing their identities. At registration, attendants would provide their hashes (commitments). These consist of of a) a secrets and b) a nullifiers; both are private. After the event, the organizers would create a merkle tree, incorporating all the secrets of participating attendants. Attendants could then claim their POAPs to a fresh address and even after they were claimed, participants can still verify their participation using zk-proofs.

Merkle trees are commonly used by related privacy-preserving applications such as [Tornado Cash](https://github.com/tornadocash/tornado-core/tree/23543683f3af71783f8036c16fe9ad21369dc3dc) or [StealthDrop](https://github.com/nalinbhardwaj/stealthdrop) to generate zk merkle proofs that can be used to proof that a certain value is included in the merkle tree, without revealing its exact position. Therefore, I think the proposed implementation may be as minimalistic as possible but still providing a generalisable interface for similar applications.

As an extension, I propose to add 4 state variables to the ERC721 standard:

- root - representing the merkle tree root
- verifier - interface to the zk verifier contract (created with zksnark)
- nullifierHashes - array with known/claimed nullifiers
- tokenId - counter

Furthermore, this requires the following two functions:

- verify(…) - calls Verifier to verify proof
- root() - view function to get the root

After quickly drafting it out, it looks like the following:

```nohighlight
pragma solidity 0.8.8;

...

contract zkExtension is ERC721 {
    bytes32 public _root;
    Verifier public _verifier;
    mapping(bytes32 => bool) public _nullifierHashes;
    uint256 private _tokenId;

	constructor(
        string memory name_,
        string memory symbol_,
        bytes32 root_,
        Verifier verifier_
        )
        ERC721(name_, symbol_)
    {
      _root = root_;
      _verifier = verifier_;
    }

  function root() public view virtual returns (bytes32) {
    return _root;
  }

  // @notice mints POA to address if nullifierHash is unknown
  // Returns true for valid proofs
  function verify(uint[2] memory a_,
            uint[2][2] memory b_,
            uint[2] memory c_,
            uint[1] memory input_,
            bytes32 root_,
            bytes32 nullifierHash_,
            address recipient_) public returns (bool valid)
    {
      // Check if right tree
      require(root_ == _root, "Wrong root");
      if (_verifier.verifyProof(a_,b_,c_,input_)) {
          if (!_nullifierHashes[nullifierHash_]) {
            _nullifierHashes[nullifierHash_] = true;
            _mint(recipient_, _tokenId);
            _tokenId += 1;
          }
          return true;
      }
      return false;
    }
}
```

**I don’t have conrete plans yet to propose an EIP. I’m still at the beginning with zk-SNARKS and the gerneral Ethereum development process. I first wanted to invite the zk-SNARK community to provide me with some feedback on the idea in general and if its appropriate for an EIP. If someone with more experience on EIPs and SNARKS would like to join - perfect, I am open to collaborate!**

*Note, building on top of ERC721 would include transfer functionality. As soon as a valid standard for Soulbound tokens exists, it can be adapted. Anyways, proofs would be valid even when tokens were transfered.*

**EDIT:** Storing the recipient addresses in another merkle tree and implementing a PrivToAddr circuit may enable to prove ownership after claiming. This would result in two merkle trees, one for claiming and one for the ownership structure after the claiming. The merkle tree could be the same that is used at TornadoCash. It would live on-chain and provide users with root + branches to prove their ownership/leaf.

## Replies

**stars** (2022-07-30):

Is there a reason for hashing a `secret` with the nullifier? How do you plan to generate this secret value for the attendees? Is it going to be a random value that the attendees would come up with and save it somewhere with them?

Assuming the nullifier would be the attendee’s actual public address for uniqueness, wouldn’t having a random secret hashed with the public address allow the attendee to commit multiple attendance?

---

**Nerolation** (2022-07-30):

Thanks for the question!

**First, I have generalised the idea a little bit more under [this thread](https://ethereum-magicians.org/t/eip-0000-erc-721-merkle-provable-ownership-extension/10154).** You will also find the draft of the EIP and its implementation. Here, I wanted to quickly discuss the idea and find fellows to collaborate with, however, my post was not-well described and lacks of a well-formated EIP doc.

Regarding your question, `the secret` and the `nullifier` may both represent private values that are hashed together by the users, provided to the event organiser and added to a leaf in the merkle tree. The nullifierHash is used to prevent double-claiming/spending. Therefore, the nullifierhash must be unveiled during the claiming. The claimer is then not able to generate another claim with the same secret and a slightly different nullifier, because he has no chance of producing a proof with another different nullfier (would require a totally different merkle tree). By storing nullifiers, we kind of store Utxos, in broader sense.

Let me link the tornado cash docs. They did a great job in explaining the rational of using secret+nullifier.

https://docs.tornado.cash/general/how-does-tornado.cash-work

I also wrote a medium article, explaining the idea:

https://medium.com/p/4fddabedfddb#b14b-694312d3d705

The secret value would be created at the users end, the proof by the issuer (trusted setup) of the ERC721 (like Tornado Cash).

---

**stars** (2022-07-30):

Thanks for getting back to my question. It’s a pretty good idea and I thought it will be interesting to see how this can used too.

Regarding the secret and nullifier, I’m aware you have a similar setup as tornado cash. But there is a little part I’m not sure about in this proposal. The user will provide the nullifier and secret. The nullifier I believe will be the user’s own address which is unique to himself. The secret is a random value the user generates and he saves it somewhere to remember it. The commitment is based on these two values and then registered  into the merkle tree. However, since the user is generating the random secret himself, could a user make multiple commitments?

For example, `0xabcd` + `randomSecret1`, that’s the first commitment `0xabcd` made for his attendance. Then the same user `0xabcd` registers another time with `0xabcd` + `randomSecret2`. This will be a different commitment made by the same person but this can get registered into the merkle tree as another entry without issues because the commitment hash is different but it’s actually from the same person. Now this user has just made 2 commitments for his single attendance, wouldn’t he? Would this person get to prove his attendance twice?

I believe in Tornado’s case, they have no problem for users to make multiple commitments since each commitment is essentially a deposit. Users are free to make multiple deposits. So perhaps the addition of a secret to the nullifier is justifiable for Tornado so that multiple commitments by a same user is possible?

---

**Nerolation** (2022-07-30):

> For example, 0xabcd + randomSecret1 , that’s the first commitment 0xabcd made for his attendance. Then the same user 0xabcd registers another time with 0xabcd + randomSecret2 .

The user then tricked the registration process itself and consequently the whole system yeah. I more think about something like EthGlobal where you register, stake some eth, register again on-site, participate, officially submit a project and based on that your commitment will be included into the merkle tree. The registration itself, should in general not be enough to receive an “attendance” token, i’d say.

Notably, it’s not possible to claim the token multiple times since only one commitment per user is registered in the merkle tree, so that each user can only have one secret. Every other secret will not be able to produce the right merkle tree root, when being hashed with the nullifier.

Happy to answer your questions!

---

**stars** (2022-07-30):

So it sounds like there is a need for an external measure such as staking or others to ensure the “claim only once” mechanism at this point?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> Notably, it’s not possible to claim the token multiple times since only one commitment per user is registered in the merkle tree, so that each user can only have one secret.

But, internally within this EIP without external measures or processes to check the users at registration, it will still be possible for an address to claim multiple tokens if the user manages to register multiple times with different secrets during the registration phase, doesn’t it? The contract tracks the nullifier hash but not whether an address has collected before or not (which it can’t or it exposes the original address). So it seems anyone with multiple commitments can still claim multiple tokens.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> The user then tricked the registration process itself and consequently the whole system yeah

To avoid the user tricking the registration process, why not just exclude and don’t use the secret at all and simply use the nullifier only which can be the user’s address? This way, there is no way each address can trick his attendance at the registration with multiple commitments.

Pardon my questions as I’m trying to see how this could be applicable in the implementations.

---

**Nerolation** (2022-07-30):

> if the user manages to register multiple times with different secrets during the registration phase

Again, this is what is supposted to happen. No problem in that. If the event organiser wants to strictly avoid users from having multiple registrations then he must ensure that at the event. (let every human only submit one commitment on-site); no on-chain logic required. If a team of two people have 2 commitments, they are allowed to bundle their tokens on one address, of course.

I’d recommend you to check out the other thread i “pinned” at the top. Expanding the idea to NFTs in general seemed more interesting to me and based on what I read from your side, you might like it too.

Happy to answer questions!

---

**stars** (2022-07-30):

Have you considered just excluding and don’t use the `secret` at all and simply only use the nullifier which can then be the user’s address? This way, there is no way each address can trick his attendance at the registration with multiple commitments?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> If a team of two people have 2 commitments, they are allowed to bundle their tokens on one address, of course.

Oh… I’m not sure if I understood correctly, but how would 2 people of 2 different addresses ended up with tokens on a same address? What would be a use case for something like this?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> I’d recommend you to check out the other thread i “pinned” at the top.

Sure, I will check out that thread too.

---

**Nerolation** (2022-07-31):

> This way, there is no way each address can trick his attendance at the registration with multiple commitments?

There is no way to trick the registration on-chain, already. Every commitment in the merkle tree can be redeemed and is afterwards invalid - thats what it must do and nothing more. If EthGlobal writes two of your commitments into their merkle tree, then the qu. is how you did that with only one real-life name to participate (just as an example). The nullifier hash is unveiled to ensure no double-claiming. The secret is used together with the nullifier to create a commitment that can later only be redeemed by the person that satisfies the merkle proof. When claiming the token, the user decides where the token should go, just like tornado cash.

