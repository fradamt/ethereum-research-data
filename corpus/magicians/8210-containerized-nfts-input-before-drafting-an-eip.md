---
source: magicians
topic_id: 8210
title: Containerized NFTs - Input before Drafting an EIP
author: GravityCollision
date: "2022-02-04"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/containerized-nfts-input-before-drafting-an-eip/8210
views: 734
likes: 0
posts_count: 2
---

# Containerized NFTs - Input before Drafting an EIP

There are a lot of NFTs.  As NFTs spread, there needs to be an on-chain solution to managing and grouping NFTs.

Let us talk about Containerized NFTs.  Is there a current EIP?  If not, then we will propose the EIP as we are planning to use this in an upcoming project.

I’ll use Car Customization as an example since there is a discussion of NFT entanglement in posts below, and games like Forza already use a similar setup (just not NFT-ized).

When you unlock or buy a car, it mints the Car Container to the Player (Player is Owner).  All other Stock Performance Parts are minted to the Car (Car is Owner).  The structure would look like this:

Player

|

—> Car

|

—> Engine

|       |

|       —> Parts of Engine

|       —> Parts of Engine

|

—> Exhaust System

|        |

|        —> Parts of Exhaust System

|

—> Hood

—> Spoiler

—> More Paaarts…

You get the picture.  In this System, the Player Owns the Car.  The Car Owns the Engine, the Exhaust System, the Hood, Spoiler, etc.  This nesting would allow for NFTs to be completely customizable, as long as you own the Car.

If you attempt to list the Engine on OpenSea, you wouldn’t be able to, you aren’t the Owner.

If you just wanted to sell the Car, you can simply list it on a Marketplace, and the transfer moves the ownerOf property of the CAR, to the new Owner.  The Car Container NFT is still the ownerOf the Engine, Exhaust System, etc.

The only things that would need to be added are the following:

- An ERC that gets assigned at the ERC721 level:

contract ERC721 is ERC165, IERC721, ERC821 (ERC821 is the Container Flag in this example)
- The ERC821.sol would have two functions  containerURI(), a and getChildren() function.  A mapping similar to ERC721Enumerable’s _ownedTokens comes to mind
- Constructor initializes the ERC165 so we know the Flag is set when making calls

Each NFT under the Car, REQUIRES a “require” statement like this in it’s functions:

require(msg.sender == ownerOf(addressOfCar));
Each NFT below the Engine, will have a statement like:

require(msg.sender == ownerOf(addressOfEngine));

Wallets simply need to check for the Container Flag and make these NFTs act like Folders on a File System.  It checks for the flag, adjusts the interface to make the Container full width, grabs and fills the full-width NFT with the containerURI (Like a special jpg or png).

When clicked, open “folder” and display the child NFTs using getChildren().  It pulls in all of the Cars-owned NFTs (it’s children).  You can even mark children as Containers (like an Engine, for example) since it is an NFT itself.

When minting these, you need to start from the bottom up, in terms of assigning.  You (or a Smart Contract) needs to initially own the minted NFT.  You will assign the lowest nested NFT to its parent, and then assign that to its parent, etc, until you get to the Top Container (in this example, Car).

Advantages:

- The biggest one is Gas Fees, and how much this would save when transferring an entire car’s worth of parts.
- NFT organization at the wallet level
- New Projects taking advantage of producing Container PFP’s (to organize your existing NFTs).  An NFT to store your PFPs, or Art, etc.  Container Pictures should look pretty too.

Disadvantages:

Slightly more complex, in having to manage an additional ERC

## Replies

**MidnightLightning** (2022-06-15):

What you’re labeling “containerization” here, seems similar to the ([now abandoned](https://github.com/ethereum/EIPs/issues/998#issuecomment-1012320451)) [EIP998](https://eips.ethereum.org/EIPS/eip-998) proposal (which poses it as a “composability” feature, intending the ownership to be “tree-like” which is what you’ve laid out here too), and the [Charged Particles protocol](https://docs.charged.fi/) (created as “a protocol” rather than “a standard”, such that one central contract on each chain can control the logic of the “contents”, while the NFT collection itself can be just a pointer/identifier that acts as a “key” to gain access to those contents).

