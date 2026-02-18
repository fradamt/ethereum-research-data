---
source: magicians
topic_id: 6044
title: "EIP-3340: NFT Editions Standard Extension"
author: nginnever
date: "2021-04-20"
category: EIPs
tags: [nft, feedback-wanted]
url: https://ethereum-magicians.org/t/eip-3340-nft-editions-standard-extension/6044
views: 3985
likes: 4
posts_count: 10
---

# EIP-3340: NFT Editions Standard Extension

This is a simple extension with the intent of improving provenance in ERC-721 tokens representing works of digital art.

As NFTs evolve further into representing digital art, there is a need to strengthen the link between a token and the digital work itself. With the current standard, a symbolic URI is the only information present linking the art to the blockchain. The URIs may become lost over time and the link may be lost. Hashing the digital art is a good link but pre-images may be lost. This standard focuses on allowing the artist to store a signature for each NFT, and allows the artist to designate an original and limited printed editions in a trustless way that does not rely entirely on the metadata.

Links:

Issue: [Discussion for EIP-3440 · Issue #3519 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/3519)

PR: [EIP-3440: NFT Editions Standard by nginnever · Pull Request #3518 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/3518)

Cheers

## Replies

**Shymaa-Arafat** (2021-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nginnever/48/4143_2.png) nginnever:

> With the current standard, a symbolic URI is the only information present linking the art to the blockchain. The URIs may become lost over time and the link may be lost. Hashing the digital art is a good link but pre-images may be lost.

What do u mean?I haven’t read much about NFT in Ethereum, but the whole point was the unique ID and talks all over the net about using it for 3D objects specially in ancient pieces ( whether art or monuments) the point it can, MUST, distinguish original from copy otherwise it’s useless!!!

.

I noticed one thing from the Daily Show

and started to ask people since I’m no expert in NFT is he joking or if this is true there is a major danger

https://mobile.twitter.com/sasamilic33/status/1396684410850738181

.

I expected they’re using an accumulated hash of all the small pics in something similar to a Merkle Tree/Trie/… whatever (since this is probably fixed) and they just missed ( have a little bug u may say) of not checking the hash of every small piece before issuing a new NFT. I emphasized on the danger of this happening to a museum pieces ( while the one paid for Beeple may joke about it or consider it a gift to the Daily Show, a country paid a fortune for NFTing it’s museums will go to Court for this.

.

Now u r saying the situation is even much worse than I expected???

---

**nginnever** (2021-05-29):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f0a364/48.png) Shymaa-Arafat:

> Now u r saying the situation is even much worse than I expected???

To clarify this extension does not claim that NFTs are currently cryptographically less verifiable than any media coverage may portray them as, or that there is not a strong crypto graphic link in the protocol. This comments on the implementation details and only offers a minimally extended option to continue the provenance story over time, perhaps slightly improving the link between artist and digital work.

The current links between artist and digital work are…

1. The original ECDSA signature on the initial transaction that “created the NFT”. A contract may be deployed from an artist’s EOA or a minting transaction may be executed to an already deployed NFT from the artist’s EOA (Opensea,rarible,foundation,superrare etc…)
2. The metadata is stored with the NFT ID mapping space with an additional URI extension. This metadata is usually an IPFS content hash containing a nested link (IPLD) to the media. This content addressing ensure that the blockchain immutably stores sha256 image of the media.

You will notice that as long as an artist retains and deploys the nft themselves there is a pretty easy link to verify. However there aren’t any easy ways for the artist to show they still have that key or that they value it (to my knowledge). This extension simply lets them sign the NFTs and then sign messages over time, post those messages on out of band networks like twitter, and let NFT owners verifiably show that the artists signatures match the ones on their NFT. This is more for an over time improvement to provenance, if however minimal.

---

**Shymaa-Arafat** (2021-05-30):

Oh yes, I’ve done some reading in the 3 days before u replied; however my Motivating Q is still the same.

I know there’s a Cryptographic hash (u just added it’s SHA256), the points r:

1-The degree of security depends on the object kind and to what limit it could be uniquely identified, ie I still see u can’t just sell they’re all the same level of security.

Ex.

-if u sign a real estate contract with say SHA256, then ur ownership is as secure as SHA256

-but if u used it to sign a photo or even a DNA, u should add to ur calculations the accuracy of ur presentation of the image(the way u uniquely identity it), or the accuracy of DNA (I know DNA is like 0.9999…9 accurate)

.

2- For this specific case of the Beeple pic, as it includes smaller images inside it, I’m asking what exactly did they hash?

*If they hashed every small image, howcome one of the smaller ones got a new NFT?

*If they did not, do u think the owner who paid 69m$ is aware of that?or thinks he bought them all?

---

**MaxFlowO2** (2022-01-04):

Still game to have this in full production on NFT contracts?

Was diving through the EIPs and came across this, and was wondering if you have used this before or not? I believe you can tweak this a bit between the different styles of NFT minting contracts as well… say a public minter like OpenSea, PFP’s, and game “characters” would all be different implementations of this.

Give me a week and I’ll fire up my repo of what I think and would like to add to the EIP.

---

**nginnever** (2022-01-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/76d3ee/48.png) MaxFlowO2:

> was wondering if you have used this before or not?

Thanks for taking a look. I have implemented this and used it in tests but I haven’t worked it into anything production. I do still think it’s a cool idea to extend signing meaningfully.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/76d3ee/48.png) MaxFlowO2:

> I believe you can tweak this a bit between the different styles of NFT minting contracts as well

Yeah, I think if done cleverly this could be used for something like opensea. In general I think it would be nice to see creators given more power to mark their works when their NFTs are bundled in with many other creators NFTs like opensea type minting.

---

**MaxFlowO2** (2022-01-04):

Yeah, let’s link up and make this happen outside of testnets…

At a minimum, heard nothing but people saying this is a good idea, may want to change some of the parameters (like _setTokenURI()) but i bet you within the week we can have this is production of a few of my contracts… I happen to launch these PFP’s on chain id 250 all the time, and wanted a new way to “digitally sign” this. even if the signature is an ipfs link and that being signed with abi.encodepacked().

One thing I ask, can I be added to this as an author as well if we happen to get this working?

---

**MaxFlowO2** (2022-01-04):

Don’t mind me, making the bots that call this inactive, active so watch me comment on all the threads.

---

**MaxFlowO2** (2022-01-05):

Might have a decent re-write, plugging EIP 1271’s isValidSignature() into this just to set this into more adoption of this standard…

This would rewrite isSigned() a bit to isValidSignature() but adding the parameter of tokenID to the mix, making the new “Magic Number” other than 0x1626ba7e… but think this could be the ticket.

Also dropping an interface on this to make all variables private with custom getters (more gas effective).

First Edition will be like how I did ERC2981’s:

Collection (think PFP’s via hashlips or whatever) - One signature to prove them all

Mass Minter (think one OpenSea’s pubic minter) - One signature per token

Plus tossing a throwback to ERC165 in there for “backwards compatibility”

Also with ERC721 being the normal, dropping ERC721URIStorage for ERC721 straight up, since there’s a few cases where not using _setTokenURI() is a way better option, say those collection (aka PFP) contracts

---

**MaxFlowO2** (2022-01-05):

also want to do an access control measure like onlyArtist()? cold be super simple to rewrite that (have done in the past for onlyDev())…

