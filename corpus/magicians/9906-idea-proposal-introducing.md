---
source: magicians
topic_id: 9906
title: "IDEA: Proposal introducing"
author: lucemans
date: "2022-07-11"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/idea-proposal-introducing/9906
views: 922
likes: 3
posts_count: 9
---

# IDEA: Proposal introducing

During URL/URI standard working group #4 ([URL-URI working group meeting #4 · Issue #149 · ethereum-cat-herders/EIPIP · GitHub](https://github.com/ethereum-cat-herders/EIPIP/issues/149)) Trey mentioned compacting URLs as done in ([Bolt-11](https://github.com/lightning/bolts/blob/master/11-payment-encoding.md). This sparked some interest and we are working together on a proposal for parallel URL standards which would propose a more compact solution for use in dApps and QR Codes.

We would love to collect your thoughts and feedback to work on something that is the best of both compactness and readability.

## Replies

**3esmit** (2022-07-11):

I would suggest a binary url (non user readable), having the first byte identification, e.g. 0x01 Transaction Request, 0x02 Transaction Reciept, or similar how communication protocols work.

---

**delbonis3** (2022-07-11):

(Adapted from earlier writeup posted to ECH discord.)

The motivation for this is that I’m questioning how necessary it actually is for the format to be human-readable, especially if we’re working from the basis that these URLs would be either provided directly to wallet extensions in a webapp or scanned from a QR code.  To a lot of “regular” people the information encoded in the URL is nonsense anyways, unlike in a HTTP URL.

The Lightning Network has a similar problem where there’s a lot of binary data that we want to communicate from a receiver to a sender with some optional components and without much obvious structure to it.  In this case, the invoices take the form of a binary blob that’s encoded in bech32, and if a URL is needed we can prepend a `lightning:` scheme.

One advantage of this approach is that it allows us to use the case-insensitive alphanumeric mode QR codes, which means is much more efficient with our use of physical space since each bech32 symbol is only 5 bits. I’m not proposing necessarily using bech32 to encode some binary request format, but it’s convenient for that purpose and might be worth considering.

Something unclear is what kind of scope we should be aiming at with this.  My original focus was on payment request URLs, but there’s others that have a desire for more generic transaction requests.

---

**delbonis3** (2022-07-13):

There’s two sides to the approach I’m imagining.  Since there’s some desire for it, a 1:1 equivalent to ERC-681 is probably a good place to start.  It might be interesting to consider what a binary encoding of function ABIs might look like if hinting is needed there in another optional field.

To copy BOLT-11, I’m imagining tags would include:

- purpose
- expiration/lifetime
- target address OR target ENS name
- chainID hint(s)
- ABI hint
- (repeatable) argument
- some clever floating quantity encoding like zkSync’s 5-byte representation (lightning payments usually only need 4 bytes so that’s what that spec uses, but having 32 bytes is overkill unless we really want it)

The other side of this is some other comments discussed in the call about developing a more abstracted request spec to give wallets more context about the request, beyond “call this function with these arguments”.  While with ERC-681 it is *possible* for a wallet to infer what conditions it needs to satisfy a request, you’d need to apply heuristics to decide if there’s intermediate steps that need to be taken like transferring funds around across bridges between rollups / the main chain.  If you’re trying to figure out what a payment request URL does on a hardware wallet then having to rely on heuristics to figure out what would be necessary to satisfy a payment request would be overly cumbersome.

In BOLT-11, there’s a prelude before the TLV blobs that includes a timestamp that we could add additional “variant” byte to to differentiate which kind of request is being represented, if it’s a 681-style call or something higher level.  And since there’s only 5 bits to store the tag, having different variants allows us to have more sets of interpretations of those tags.

So I’m imagining request types that express requests like this:

- transfer x tokens on network y1, y2, or y3 to address z
- approve contract a to spend quantity b of token contract c on network d
- (same as above two but for 721, 1155, etc)
- vote for option p on question q on governance platform r on network s (if someone wrote a standard for this)

And this more directly gives wallets the information they need to satisfy a request and present a useful UI to the user.  I would expect that specific applications can develop their own extensions that fit into this model.  There was [this prior art](https://github.com/ethereum/EIPs/issues/719) for a similar idea that takes the form of a human-readable-ish DSL and has some other features, but I’m not sure how much research is still being done on that line of work.

One limitation is bech32 blobs as defined in BIP-173 are officially limited to 90 characters (~450 bits minus checksum), but the lightning spec includes a directive to disregard that for decoders, but it does mean strict standard bech32 decoders wouldn’t work with it as far as I’m aware.  This weakens the error correction, which isn’t ideal, but I’m not sure what the priorities around that are.

---

**lucemans** (2022-07-13):

I like the points mentioned and am definitely a fan of the idea of having equivalents of expandability and the ability to have more then just a 681-like “transaction” system. The idea of using the first few bits of data to direct `purpose` sounds benificial.

Regarding hashing and length constraints I am unsure as this is not my area of expertise.

Personally I am more a fan of the low level “function x on contract y with parameters z” approach, and letting the wallet infer whatever it would like from that. Currently for ex metamask infers any function called “transfer” and shows an ERC20 / 721 custom UI for it. Hardware wallets are free to do similar things and use the data on device to be able to show the correct icons and UI presuming they know the contract address.

Depending on bridging etc I think that is far out of the scope of this spec. There are many bridges and ways to move between chains and I don’t think including a per-chain specific field into a url spec would introduce too much ambiguity and work for wallets as opposed to the current situation.

---

**delbonis3** (2022-07-18):

Another benefit of having certain specialized types is that it helps reduce the length of the addresses generated with them, especially using ENS names.  Which I think is pretty valuable since simple payments account for a lot of transactions.

> and letting the wallet infer whatever it would like from that.

This is part of my concern though, different wallets might infer differently and it could be problematic to leave open a lot of space for interpretation.  This seems unlikely in the case of simple token transfers, but it’s foreseeable that someone could write a dapp assuming wallets infer one particular interpretation of a payment request, but a user uses a wallet that does it differently and it breaks an assumption.  So to me it feels like a leaky abstraction.

It’s also less general.  Some rollups may not even have an EVM so it seems weird for a wallet to take apart a request that looks like a call to ERC20 contract and translate it into whatever a transfer tx for that rollup looks like.  Saying at a high level “pay this address” would make writing the code more direct and the addresses more portable.  Like zkSync on mainnet today doesn’t support any EVM contracts, just token transfers (it is in their roadmap, but others in the future might also forego it).  Doing payment requests at a high level makes for a more natural translation to the native transaction logic.

> Depending on bridging etc I think that is far out of the scope of this spec.

I don’t think it’s not worth thinking about.  I don’t think there’s anything a spec needs to accommodate it aside from being aware of multiple networks.  It’s not like it’s saying *bridge using this bridge*, it’s just assuming the wallet can figure out how to use the receiver’s chain (or at least, take apart the relevant data and give it to the user to manage it on their own).

---

**delbonis3** (2022-08-08):

Ok this is a bit later than I intended to submit it, but I think I’ve figured out most of what I would like to see:

# Binary Transaction Request Format

We can use the first byte as a variant and flag byte.  The first 5 bits of a

bech32-encoded message easily correspond to the first char after the `1`, so we

can easily see just by looking it, see what general kind of request might be.

This format, as discussed previously, is informed by BOLT-11 but leaves out a

few Lightning-specific features like message signatures.  Similarly, we

probably must ignore the length limitation that bech32 has (unless we decide to

use a different polynomial for the error correction).

With each variant, we get access to a different set of TLV tags we can use.  Or

it might be such that a variant picks an entirely different representation to

use.  This would be safe since a wallet that doesn’t support a variant wouldn’t

try to parse that not-TLV format at all.

We maintain the similar encoding:

1. type (5 bits)
2. data_length (10 bits, big-endian)
3. data (data_length * 5 bits)

The choices of using 5 bits here is to line up with the bech32 symbols.

## Variant 0 (q prefix)

Variant 0 tries to match directly to EIP-681-style request URLs.

Not all of these TLVs would be required, but we can include:

- a (29) - 20 bytes (32 symbols) - target address (required)
- q (0) - data_length bytes - value [see value encoding]
- f (9) - data_length bytes (trailing padded) - ASCII function signature [see note 1]
- s (16) - 4 bytes (6 symbols, padded) - raw 4 byte function selector
- m (27) - variable bytes (trailing padded) - message call bytes, decodable using function signature
- c (24) - 4 bytes (6 symbols, padded) chain ID
- p (1) - data_length bytes - ASCII purpose or some other message
- l (31) - ? bytes - gas limit
- g (8) - 10 bits (2 symbols) - gas price

If the value field is missing, we can assume it’s 0.  We can specify data to

pass with `m` and only specifying the selector with `s`, but that gives more

work for the wallet to figure out to present a useful UI to the user.  If we

*only* pass a function signature with `f`, then we can provide the user with

options to decide what to do with it (as we could with EIP-681).  We don’t

actually have to include a separate TLV entry for each parameter if we have a

signature to decode the calldata bytes with.

This would of course be useful even with just simple ETH value transfers, and

pretty succinctly.  If we omit the chain ID we can assume it’s referring to the

user’s current chain, as with EIP-681.

We could also add another tag `n` to refer to a target address by ENS name.

## Value encoding

It’s often not necessary to include extremely precise quantities.  Even when we

do, it’s wasteful to waste space on lots of zero bits.  So it makes more sense

to me to encode quantities in an exponent-mantissa form, like floating points

but without the floating points.

Since `10 ** 18` takes 59 bits to represent, if we set aside 10 bits (2

symbols) as an exponent, we get more than we really need (`2 ** (2 ** 10 - 1)`)

but setting aside only 1 symbol isn’t enough.  The following symbols we can

treat as a kind-of mantissa.  This seems complicated, but it’s actually easy to

implement.  We just treat the 3rd and after symbols as a big endian number and

shift it left by the amount of the exponent.  We go the other way by counting

the trailing zeros and working backwards.

// TODO python reference code

This does have a limitation that it’s possible to encode the same number in

different ways, but we are able to decide that the form with the highest

possible exponent (no trailing zeros in the mantissa) is the canonical form.

## Variant 1 (p prefix)

As mentioned before, I think it’s worthwhile to develop a more concise format

for representing common operations like token transfers.  This would let us

more efficiently represent a few parameters and let us further optimize what we

are able to do with this request pattern.  We wouldn’t have to include this in

any initial EIP, but I would like to see it..

- a (29) - 20 bytes (32 symbols) - target address (required)
- q (0) - data_length bytes - value [see value encoding]
- t (31) - 20 or 24 bytes (32 or 39 symbols, padded) - localized token contract address (repeatable)
- k (11) - variable bytes - token identifier
- c (24) - 4 bytes (6 symbols, padded) - chain ID (repeatable)
- p (1) - data_length bytes - ASCII purpose or some other message

The “localized token contract address” param here is a 20-byte contract address

and optionally another 4 bytes to indicate chain ID.  If a receiver has funds

on multiple chains and doesn’t know where the sender has funds, they can

specify a list of these localized tokens to present the sender with a list of

options to choose from if they have the appropriate funds without the receiver

having to produce several payment requests.

Now, this involves some duplication.  If there was a generally-agreed-upon

registry of equivalent token contracts on different ledgers (tokenlists is a

good start to look at), then we could reference that (with `k`) avoid including the full token contract

addresses, and only include the list of chain IDs (with `c`) that we know must have the token

contracts, and look up those addresses locally.  To make this less error prone,

we could add an extra checksum tag or some other tag to ensure that we find the

same list of contracts.  This *also* lets this format more naturally support networks (like

zkSync v1, as previously discussed) that don’t use their own token address

space and inherit it from elsewhere and reference tokens by indexes.

If we borrow the `n` tag from above to refer to a receiver succinctly, then

**it’s possible we can have *really short* payment requests in this model**,

since we don’t include any full addresses that require 32 symbols to encode.

## Notes

1. A binary ABI encoding of what function signatures can look like that matches with general Solidity patterns would be more ideal here, but for the purposes of spec discussion we can assume it’s just a regular textual ABI string.  I’m not sure if it’s worth it trying to do a 1:1 match between textual ABIs or if we can optimize and only include 4 byte selectors, expecting wallets to infer what’s actually happening.

---

**SamWilsn** (2022-08-08):

Probably a dumb question, but why use bech32 encoding at all? If these strings aren’t intended to be typed by a human, can we leave error detection and recovery to the transport (pretty sure QR codes already include error correction.)

---

**delbonis3** (2022-08-09):

QR codes do have error correction of their own.  It’s not meant *strictly* for QR codes, it’s possible users will type them out and having error correction across all fields is a benefit.  Since this fits into the alphanumeric QR mode it still would end up being .

But since there’s a binary encoding in here anyways I wonder what it would look like if we to define the attribs in terms of bytes regularly.  I feel like it would be less efficient.

What do you think would be of most use?

