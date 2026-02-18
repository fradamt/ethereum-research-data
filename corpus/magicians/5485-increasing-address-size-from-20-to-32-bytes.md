---
source: magicians
topic_id: 5485
title: Increasing address size from 20 to 32 bytes
author: vbuterin
date: "2021-03-06"
category: Working Groups > Ethereum 1.x Ring
tags: [opcodes, address-space]
url: https://ethereum-magicians.org/t/increasing-address-size-from-20-to-32-bytes/5485
views: 20333
likes: 38
posts_count: 50
---

# Increasing address size from 20 to 32 bytes

# Why increase the address size?

At some point, perhaps soon, we are going to have to increase the address size from 20 bytes to 32 bytes. Some reasons for this include:

1. Adding an address space ID if we use a state expiry scheme that requires it
2. Adding a shard ID if we have multiple EVM-capable execution shards
3. Security: 20 bytes is not secure enough

To elaborate on (3), current 20 byte (160 bit) addresses only provide 80 bits of collision resistance, meaning that someone can spend `2**80` computing work to generate two pieces of contract init code (or (sender, ID) pairs, or one piece of contract code and one EOA private key) that have the same address. `2**80` will soon be within reach of sophisticated attackers; the bitcoin blockchain has already made more than `2**90` hashes.

This possibility of attack means that if someone gives you an address that is not yet on-chain, and claims that the address has some property, they cannot prove that the address actually has that property, because they could have some second way of accessing that account. The properties of addresses become more complicated: you can trust an address if either (i) it is on chain, or (ii) you personally created it; for example, an organization cannot safely receive funds at a multisig unless that multisig has already been published on-chain, because whoever was the last to provide their public key could have chosen their private key in such a way as to make the address also a valid EOA controlled by themselves.

These problems can be eliminated if we go up to 32 byte addresses, increasing the hash length and simultaneously adding shard and epoch data and a version number to add forward compatibility for the future. The challenge, however, is that existing contracts are designed to accept 20 byte addresses. Solidity type-checks addresses to verify that they are in range, and byte-packs addresses to save storage space. This document attempts to give some proposals for how this can be done reasonably backwards-compatibly.

# Proposal

We make a new address schema as follows:

```auto
Byte 0    : Version byte (must be 1 for now)
Byte 1-2  : Must be zero (could be shard number in the future)
Byte 3-5  : Epoch number (0  ALICE_LONG to the translation table). AUCTIONEER confirms that Alice’s bid is higher than any existing one, and saves Alice’s bid, using ALICE_SHORT as her identity.
2. Bob calls AUCTIONEER with a 6 ETH bid. AUCTIONEER confirms that Bob’s bid is higher, and needs to refund Alice her bid as her bid is now losing. AUCTIONEER uses CALL passing along ALICE_SHORT as an argument. The CALL opcode looks up ALICE_SHORT in the translation table, gets ALICE_LONG as a result, and so correctly sends Alice’s 5 ETH back to ALICE_LONG.

## Alternatives

**It’s worth noting that we don’t *have to* do this if we are okay with unpublished addresses requiring the creator to be trusted**. If we are okay with this weaker security property, then we could instead just move to a scheme where the hash *decreases* to 15 bytes (still 120 bits of preimage security) and the remaining 5 bytes get used for version/shard/epoch, though this would instead require somehow invalidating existing addresses that collide with the new schema.

## Replies

**esaulpaugh** (2021-03-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Solidity and other langs would be expected to treat the output as a BigAddress type which would be an alias for bytes32 instead of bytes20

The current ABI spec treats `address` as `uint160`, not `bytes20` though

https://docs.soliditylang.org/en/latest/abi-spec.html

---

**anono1618** (2021-03-06):

Can we reserve a nibble for a checksum, even if it is optional and only used by front ends?

Perhaps have addresses start with checksum c and an “E” to mean Ethereum, so addresses would look like

cE01000001060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F

c being a checksum

“E” denoting ethereum

01 Version Number

000001 Epoch

060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F being the hash (but counting byte number).

---

**greg7mdp** (2021-03-06):

vbuterin on reddit> The amount of computing power needed to break a key or hash goes up exponentially with the length, so we really can be sure that 32 bytes is sufficient for the foreseeable future.

Isn’t the hash length really 26 bytes not 32 in the proposal? Shouldn’t we increase the hash part to 32 bytes in case of quantum surprises? Maybe we could go to 40 byte addresses, and in the spirit of anono1618’s suggestion starting with oxE (for Ethereum) followed by a 12 bit checksum to catch typos.

---

**vbuterin** (2021-03-06):

26 bytes is enough in a post-quantum context too. If we really want, we could later on switch around the addressing scheme again to increase the hash portion to 28 bytes.

> Can we reserve a nibble for a checksum, even if it is optional and only used by front ends?

What properties are you trying to get that [Ethereum’s existing mixed-case checksum scheme](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md) doesn’t already provide?

---

**greg7mdp** (2021-03-07):

I didn’t know about [Ethereum’s existing mixed-case checksum scheme](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md). So now the addresses will be case-sensitive?

> 26 bytes is enough in a post-quantum context too

Do we know that for a fact? Unless this is proven somehow, I think going a bit longer on the addresses may make people feel better and alleviate (possibly irrational) fears. Considering what is at stake, it is better to err on the side of too much rather than not enough when it comes to wallet security.

---

**greg7mdp** (2021-03-07):

Also a byte seems wasteful for a version number. A nibble would be plenty, and if we ever reach version 15 we can increase the version size to one byte in that version.

And why start at version 1? 0 is just as good, isn’t it?

---

**greg7mdp** (2021-03-07):

It is not very clear to me why 3 bytes are reserved for the epoch (what will this epoch embedded within addresses be used for?).

---

**vbuterin** (2021-03-07):

We could do 2 bytes for the epoch as well; I suppose having 108 bits of collision resistance instead of 104 (from adding an extra byte to the hash, making it 27) is more urgent for future-proofness than having epoch space to last 16777216 years instead of a mere 65536.

> Also a byte seems wasteful for a version number

Partial bytes just make code ugly imo ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**vbuterin** (2021-03-07):

> So now the addresses will be case-sensitive?

Theoretically, we could make addresses case-sensitive today. There just hasn’t been enough of a community effort to force adoption of the checksum scheme. But we could actually try putting our minds to making it mandatory! (even before any address size change)

---

**greg7mdp** (2021-03-07):

If changing the address size, it seems much cleaner to set aside a byte for the checksum, rather than encode it using a upper/lowercase scheme. It seems to me that the checksum is really needed when entering addresses by hand, so making such entry more difficult and error prone to enter by making the addresses cases sensitive is a step backward imo.

I still don’t understand the planned use of the epoch. I naively thought it was in eth2 epoch units of ~6.4 minutes. If it is a number of years then yes three bytes is wildly excessive. IMO 1 byte allowing for 256 years would be plenty.

It might well be that there is some benefit of have “must be zero” bytes reserved for future uses, in the hope that the address length will not have to change again, so maybe that could be an argument for longer addresses (40 bytes?) with a longer ultra secure (even to wildly paranoid types)  hash (32 bytes?) and mbz fields.

> Partial bytes just make code ugly imo

Then at least make the first version be 224 instead of one, so that all ethereum addresses will start with 0xE.

Actually, on second thought, maybe it would be nice to start at version 226, so that eth addresses would start with 0xE2 which could be read as Ethereum 2.0.

---

**greg7mdp** (2021-03-07):

Also, the Mixed-case checksum scheme is useful only to catch input errors. Is it possible that an address could get corrupted while sending a transaction or executing contract code? If that is the case, having a checksum allowing to validate that a 32 or 40 byte string is indeed a valid address might be good to have.

---

**vbuterin** (2021-03-07):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/g/ebca7d/48.png) greg7mdp:

> it seems much cleaner to set aside a byte for the checksum, rather than encode it using a upper/lowercase scheme.

How so? Remember that there’s no need for a checksum *within* the EVM; the checksum is a user-interface-level convenience. So it should be part of the representation format (as the mixed-case-hex thing is), and not part of the raw address format.

> making such entry more difficult and error prone to enter by making the addresses cases sensitive

The mixed-case checksums don’t have this risk. If you get the uppercase/lowercase wrong, that can ONLY lead to a “bad checksum” error, NEVER to you accidentally typing in a different but valid address.

> Is it possible that an address could get corrupted while sending a transaction or executing contract code?

I can’t possibly imagine what could cause such a thing to happen.

> so maybe that could be an argument for longer addresses (40 bytes?)

Addresses longer than 32 bytes are extra-problematic because there are 32 byte limits everywhere in ethereum: storage slot keys, storage slot values, ABI bytes32 values, SSZ chunk sizes… so IMO better to just stick to 32.

> Actually, on second thought, maybe it would be nice to start at version 226, so that eth addresses would start with 0xE2 which could be read as Ethereum 2.0.

I’m ok with this if people want it!

---

**greg7mdp** (2021-03-07):

> If you get the uppercase/lowercase wrong, that can ONLY lead to a “bad checksum” error, NEVER to you accidentally typing in a different but valid address

I get that, but it may still get frustrating and not user friendly. Suppose someone trying to send a large amount to a paper wallet. He enters the address, but we just made this entry more difficult because the letters are now case-sensitive. He clicks “send” and gets an error that the address is incorrect. He now totally freaks out.

I think most users would rather type case-insensitive addresses with an additional checksum byte, than having to worry about upper and lower case letters in addresses.

I would describe your argument as saying: “It is OK if I make your task more difficult, because I can guarantee that I will let you know if you fail it, and therefore it won’t have terrible consequences”.

There could also be a benefit to be able to check whether addresses are valid in program databases (beacon nodes, etc.). Maybe?

---

**zamicol** (2021-03-07):

Yes please!  At least a nibble, if not four bytes like Bitcoin.  Two bytes would allow 1/65536 mistakes to get through.  A nibble 1/16 mistakes would get through.

Another point: It’s not just users that [bit flip](https://en.wikipedia.org/wiki/RAM_parity).  It’s not just for user interfaces.  This is a real issue, for computers as well.

[See my post on Reddit.](https://old.reddit.com/r/ethfinance/comments/lzkhqn/daily_general_discussion_march_7_2021/gq2nupd/)

---

**zamicol** (2021-03-07):

EIP-55 addresses are just regular addresses on chain.  There’s no checksum on chain.

EIP-55 addresses are also optional.  What I’m asking for is mandatory checksums.

Thank goodness applications like Metamask use checksums by default.  But then again, it’s only ~15 bits *on average*.

But that’s another problem in of itself.  The checksum strength is not guaranteed, it’s only “an average” value.  **It could be very few bits actually in the checksum.  It totally depends on how many alpha characters the original address has.**

Ethereum addresses are 42 characters long with (when checksummed) a base 22 character set.

If they were efficient (which they are not) they [could hold 179 bits of data](https://convert.zamicol.com/?in=0xffffffffffffffffffffffffffffffffffffffff&inAlpha=0123456789ABCDEFabcdef&outAlpha=01&pad=false).

[For a 42 string length in “base 66”, you can store 242 bits](https://convert.zamicol.com/?in=..........................................&inAlpha=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_%7E.&outAlpha=01&pad=false).  Which is enough room to do everything Vitalik is suggesting to do and have enough bits left over to add checksums.

If using Bitcoin’s base 58, you’d need 44 characters.

---

**vbuterin** (2021-03-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zamicol/48/3425_2.png) zamicol:

> Another point: It’s not just users that bit flip . It’s not just for user interfaces. This is a real issue, for computers as well.

It’s worth noting that in bitcoin, the checksum is also purely a user convenience, not an in-protocol thing; the bitcoin protocol treats addresses purely as a 20-byte hash with no redundancy or error detection of any kind. So as far as I can tell, that is the industry standard way of doing it. And if there are bit flips, they’re far more likely to happen in the much larger parts of the protocol that are *not* addresses.

---

**greg7mdp** (2021-03-07):

Even if it had no technical value (a fact that I am not quite convinced is true), having a checksum is a very potent bragging claim (even better if bitcoin doesn’t have it).

It allows us to say:

> Ethereum has an built in way to validate that addresses are indeed valid addresses, and not just any random string of bits. Before any token transfer, addresses are validated against the embedded checksum and any inconsistency will cause the transaction to be aborted.

Sadly, marketing is important, even for things which make little technical sense.

---

**John-Status** (2021-03-07):

# Proposal: any new address schema should support encoding multiple shard and L2 rollup chain IDs in a single address

The shard and L2 rollup chain IDs that are encoded in the address would represent the destination chains into which the address owner is happy to receive tokens e.g. If an address includes the IDs for say the Ethereum L1, Optimism L2 and ZKSync L2 chains, this would signal that the owner of the address is happy for tokens sent to this address to be sent on the Ethereum L1, Optimism L2 and ZKSync L2 chains.

In a world with multiple rollups, encoding multiple chain IDs in the address would enable wallets to automatically know which L2 rollup chains are valid destinations (for that address) without requiring any additional user input.

Without this change, when (in a world with multiple rollups) a user wishes to make a token transfer, the user would need to know the name of the destination chain in addition to the destination address.  This is much worse than the token transfer user experience on Ethereum today!

Requiring users to enter a destination chain name (in addition to a destination address) introduces the following UX regressions:

- significantly increases scope for user error (e.g. user sends tokens to the correct address but on the wrong chain)
- Adds another concept (the fact there are multiple chains with different names) for users to learn, hindering adoption.  For mainstream adoption we need to make Ethereum easier to use, not harder.
- Because in reality most users would only enter/select a single destination chain, in many cases the routing of these cross chain transactions would be suboptimal, increasing the transaction cost the user has to pay, decreasing the transaction speed, and increasing the number of transactions that need to be performed which needlessly places additional load on the network. Many to many chain routing is better than many to one chain routing.

If multiple chain IDs are encoded in Ethereum addresses, all these problems go away and the token transfer user experience in a world with multiple rollups is just as good as the token transfer user experience today.

### How it would work:

Let’s say Alice has funds associated with her address on rollups A, B and C.  She wants to send funds to Bob who uses his address on rollups B, C and D.  Bob sends his address to Alice, and in the address it is encoded that Bob is happy to receive funds to that address on rollups B, C and D.

Alice has 30 ETH associated with her address in total, and this is split equally across rollups A, B and C (10 ETH on each).  Alice wants to send Bob 20 ETH.  Because Bob’s address has told Alice’s wallet that he is happy to accept funds to rollups B, C and D, Allice’s wallet automatically works out that the quickest and cheapest way to send 20 ETH to Bob is to send 10 ETH from her address to his address on rollup B and another 10 ETH from her address to his address on rollup C.  This means that this transfer doesn’t have to cross any rollup boundaries therefore avoiding the latency and cost of moving funds between rollups.

In terms of the routing of payments, the above is one of the simplest possible examples.  In reality different L2s will have different bridge costs and delays, and the sender’s funds will frequently be spread across multiple rollups in a way that won’t match up so neatly with the rollups on which a recipient is happy to receive funds.  And when L2 to L2 transfers become feasible there will also be different costs when moving funds between different L2’s adding another layer of routing complexity.  It’s unreasonable to expect users to understand and manually work out the best answer to these complex routing problems each time they want to make a token transfer.

Encoding multiple chain IDs in ethereum addresses provides wallets with the information they require to compute the quickest and cheapest way of transferring funds (that are assigned to the same address across multiple rollups) to a recipient whose address is also used across multiple rollups.

### Assumptions around token UX in a in a world with multiple rollups

- In the future, wallets will include simultaneous support for multiple rollup chains (in addition to Ethereum L1)
- When this happens, wallets will display the token balance for a given address across both Ethereum L1 and all the rollup chains that the wallet supports.
- Token bridges will be built into wallets, so when a user wishes to transfer tokens across chains, they will be able to do this directly in their wallet without needing to navigate to a token bridge DApp.

See this rough visual mockup which illustrates these UX assumptions and shows how a token transfer flow could work in a world of multiple rollups if multiple chain IDs can be encoded in an address.

[![Mockup_of_sending_tokens_to_multiple_L2s_with_destination_chain_IDs_encoded_in_address3](https://ethereum-magicians.org/uploads/default/optimized/2X/3/315d5b084d5b2957ff890541832900a50e2669ce_2_690x445.png)Mockup_of_sending_tokens_to_multiple_L2s_with_destination_chain_IDs_encoded_in_address33193×2061 552 KB](https://ethereum-magicians.org/uploads/default/315d5b084d5b2957ff890541832900a50e2669ce)

### Benefits of being able to encode multiple chain IDs in an address in a world with multiple rollups:

- The user sending tokens only needs to know the destination address (just like when using Ethereum today).  Without this change, in a world with multiple rollups, a simple user to user token transfer requires the user to know both the destination address and the destination chain name.
- Less scope for user error e.g. the user doesn’t have the opportunity to mistakenly enter the name of the wrong destination chain.  Follows the UX principle that “when possible, the best way of handling errors is to remove the possibility of the user making the error in the first place!”
- Lower transaction fees, faster transactions and reduced number of transactions.. Wallets would be able to automatically calculate the most efficient routing to transfer X tokens from account A to account B when (for example) account A holds X tokens across rollup A, rollup B and rollup C, and where account B is happy to receive tokens on rollup B, rollup C and rollup D.
- Requiring the user to manually enter the destination chain for a transaction makes the UX of transferring tokens more complex.  By having the ability to encode multiple chain IDs in an address, Ethereum doesn’t get harder to use than it is today in a multi-rollup world.

### Open questions:

- What is the max number of chain IDs we would allow to be encoded in a single address?  The cost of allowing a greater number of chain IDs to be encoded in a single address is increased address length.  Could allowing a max of say 8 or 16 chain IDs to be encoded in a single address be a sensible number?
- What is the global max number of chain IDs that would be available for use in the future?  The cost of having a greater global max number of chain IDs is increased address length.  On the flip side, the greater the number of chain IDs supported the more future proof this format would be.  Perhaps aim to support a total of 32k or 64k chain IDs in total??
- A table of which chain IDs map to which chains would have to live somewhere

### Other thoughts

- Encoding Chain IDs in addresses should be optional e.g. an address should be valid even if no Chain IDs are encoded in it.
- I’m +1 on adding native support for checksums to any future address format.
- We’ve been looking into how we can encode multiple chain IDs into Ethereum’s current address format using mixed case encoding (EIP-55’s checksum encoding mechanism), but it’s not possible to use mixed case encoding for both multiple chain IDs and a checksum at the same time.  Natively supporting multiple chain IDs in a new address format would resolve this issue.

### IMHO the ability to encode multiple chain IDs in ethereum addresses is highly desirable from a user experience perspective!

---

**zamicol** (2021-03-07):

That sounds like a fair compromise.  I would ask to enforce checksums for user interfaces.

---

**greg7mdp** (2021-03-07):

I’m wondering if, instead of deciding on one address format which has hardcoded support for shards/L2 chains addressing, it might not be getter to have optional address extensions.

So in the base 32 byte address, there could be a byte stating whether the address is followed by a second 32 byte extended address. If the byte is 0, there is no extended address information. If the byte is not 0, its value would specify the type of the address extension that follows in the next 32 bytes. Any address extension would be optional, but as you described providing it might be a way to optimize transfers.


*(29 more replies not shown)*
