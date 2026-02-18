---
source: magicians
topic_id: 1131
title: "EIP-1344: Add chain id opcode"
author: rmeissner
date: "2018-08-22"
category: EIPs
tags: [opcodes, chain-id]
url: https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131
views: 15755
likes: 94
posts_count: 118
---

# EIP-1344: Add chain id opcode

https://github.com/ethereum/EIPs/pull/1344 proposes to add an opcode to retrieve the chain id of the chain that the block has been mined on.

This would allow smart contract to validate signatures that use replay protection (as proposed in [EIP-155](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md)).

Currently the only way is to hardcode the chain id into the smart contract. This poses a problem in case of a hardfork.

This opcode would allow multi signature contracts that use signatures to implement better replay protection and increase security.

## Replies

**fubuloubu** (2019-04-01):

This is an excellent proposal, and would be very valuable in EIP-712 applications. EIP-712 [Domain Separator](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-712.md#definition-of-domainseparator) suggests the use of the EIP-155 Chain ID to ensure the user-agent refuses signing if it does not match the currently active chain. This is also valuable in the smart contract use case where full message validation must be done in order to ensure the off-chain message was signed appropriately.

I would suggest that this EIP get a second look for inclusion in Istanbul, as a useful pre-requisite for Layer 2 scaling technologies that may use EIP-712 signing.

---

**shemnon** (2019-04-02):

Would this be better served by a precompiled contract instead of an Opcode?

---

**fubuloubu** (2019-04-02):

I’m not sure what you mean? Chain ID is currently available through RPC, and it’s important as a domain separator to differentiate between off-chain messages meant to be signed for mainnet vs. some testnet with a different ID. Should be no different than looking up other environment variables such as `msg.sender` or `block.timestamp`

---

**rmeissner** (2019-04-02):

I would not do that, this would unnecessarily increase the gas costs from 3 to a couple hundreds. Also precompiles are used for expensive operations that are not often used. Not sure that this would match in this case

---

**ligi** (2019-04-02):

added a issue for this EIP in the geth repo: https://github.com/ethereum/go-ethereum/issues/19368

should be looked at on issue-triage next tuesday

---

**pedrouid** (2019-04-02):

I second everything that [@fubuloubu](/u/fubuloubu) and [@rmeissner](/u/rmeissner) said ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=9)

---

**shemnon** (2019-04-02):

SHA3 is a relatively expensive operation and has an opcode.

The reason I think we should always as the “would a precompiled contact be more appropriate” question is that if we try and keep opcodes to a single byte it is a limited resource that will be exhausted whereas precompiled contracts have a much, much higher limit (theoretically). So this is fine as an opcode, we just need to be sure other options were not better.

---

**fubuloubu** (2019-04-02):

I think `chainId` is a `uint32` parameter, can someone confirm that? What is max `chainId`?

EDIT: It looks like EIP-712 defines it as a `uint256` (one machine word), so that would probably be fine.

---

**shemnon** (2019-04-02):

I view this as an opportunity to nail down what the value of `CHAIN_ID` can be.  It’s not well defined.

The yellow paper defines `v` as 1 byte (Appendix F, v is a member of open bar B sub 1), and per the spurious dragon fork `chain_id` is encoded into v (0x35+CHAIN_ID) which leaves room for only 101 networks.  However EIP-155 where this scheme was introduced defines 1337 as a Geth devnet, which breaks this.

When RLP encoded technically the size is unlimited, so Geth uses a `big.Int` (go library for arbitrary precision).  But Parity uses a `u64` (unsigned 64 int byte) and pantheon uses an `int` (32 bit signed) since none of the known networks have CHAIN_IDs > 4 million… yet.

EIP-712 is still draft so it shouldn’t be authoritative, and can still be updated as well.

Any of the fixed length values sounds fine to me (256, 64, 32), but there should be test cases testing some common known values, values up to the limit, and values over the limit of the chain_id.  We also should look into updating Appendix F of the Yellow Paper with the correct values to give some specification weight to the limit.

---

**fubuloubu** (2019-04-02):

https://chainid.network/ has several over 4 million, but I think you meant 4 billion (`2**32`) which indeed, no one is over that number (according to the website)

---

**shemnon** (2019-04-02):

So signed int, actually 2 billion :(.  But still a large number but not as large as it feels compared to longs and uInt256 numbers.

I think the best choices are uint64 because almost all languages have native support for that, or uint256 which has the added ability to have a chain_id that is a hash output of the hash functions typically used in ethereum.

---

**fubuloubu** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> have a chain_id that is a hash output of the hash functions typically used in ethereum

Yeah, I was thinking about this too. Having a hashed DID that referred to the network configuration would be very valuable for replay protection of txn signing

---

**fulldecent** (2019-04-02):

I am a fan of this proposal and an opponent of certain details EIP-155.

PROPOSAL: The correct chain ID should be `sha3(tar_gz(reference_implementation) || genesis_block)`. If the reference implementation changes to an incompatible version (i.e. a hard fork) then the chain ID is changed.

EIP-155 was created because Ethereum® was originally designed as a single network. Nobody expected that there would be a fork. The community reacted by taking the unfavored fork (Ethereum Classic) and assigning it a separate chain ID. Then mainnet=1 was reserved for Ethereum®.

The problem is that our current process is yet again unprepared for the possibility that another fork comes. Specifically, if a proposed upgrade happens to Ethereum® and the community rejects this upgrade then we will yet again have the situation where chain=1 transactions are being processed on the community-supported “Ethereum” as well as the the Stiftung Ethereum, Zug / Ethereum® networks.

The proposal above solves the problem.

---

**fubuloubu** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> PROPOSAL: The correct chain ID should be sha3(tar_gz(reference_implementation) || genesis_block) . If the reference implementation changes to an incompatible version (i.e. a hard fork) then the chain ID is changed.

What’s the reference implementation?

I was thinking about configurations of core components, such as the EVM, mining algorithm, and state system. That probably has a lot of issues (every wallet would have to change their signing algo on a new release). Maybe I’m mixing in too many things with that idea (I believe Ethereum’s configuration management is poor)

Hash of the Genesis block would be interesting!

---

**fubuloubu** (2019-04-02):

Alright, I think we can all agree that any discussions of what `chainId` *should be* is out of scope for this proposal, but we do need to capture what data type and limits are applicable to the use of `chainId` so we make sure this opcode captures potential nuance.

EDIT: I also think `networkId` is out of scope for an EVM opcode because it describes network interfaces not transaction signing

---

**shemnon** (2019-04-02):

I vote uint256.  It will be more code changes in Pantheon but it opens up the meaning of chain_id to more interesting possibilities.

Note that unless you use a chainID > 64 bits parity won’t notice.  But I think that should be thrown in test cases and noted as such.

---

**ajsutton** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I vote uint256. It will be more code changes in Pantheon but it opens up the meaning of chain_id to more interesting possibilities.

I’d keep it small - 2 billion chains should be enough for anyone.  I haven’t seen any proposals where a hash would be used that make any real sense.  You can’t hash the genesis block because it’s the same for both sides of a fork, hashing the reference implementation has all kinds of issues around centralisation but also breaking the entire chain every time a new release comes out.  Eventually you wind up picking an arbitrary thing to hash and all agreeing on it so why not just pick a number?

---

**fubuloubu** (2019-04-03):

100% and if you REALLY wanted to do a hash, just slice the first or last (or middle???) 8 bytes. Probably enough entropy there to be used as an ID.

---

**drinkcoffee** (2019-04-03):

I agree with [@shemnon](/u/shemnon) - it should be a 256 bit value.

We are looking to use the Chain ID as our Sidechain ID for our ephemeral on-demand permissioned private sidechains technology. Having a 256 bit value means that we can use the id, a public value, in conjunction with private values to derive cryptographic keys, salts and other cryptographic values.  Using a value smaller than 256 bits could open the system up to security issues.

If the value is 256 bits, then if we randomly generate it, it is unlikely to have a collision with an existing sidechain id. If we did have a clash, chances are it is an attack, and we can deal with it assuming it is an attack.

---

**rmeissner** (2019-04-03):

I agree, it is not as simple as “Is it expensive or not”

For me it is a combination of, how much gas would be appropriate for such a call and how often would such a call be used.

Probably an argumentation for this should be added to the EIP. Something like:

Signatures are widely used (e.g. state channels, multi signature wallets and relays) currently all these signatures can not be properly protected against cross-chain replay attacks. As we assume that all these signatures will use this opcode it would be preferred to use an opcode, to be gas efficient.

This might be something else if [EIP-1109: Remove call costs for precompiled contracts](https://ethereum-magicians.org/t/eip-1109-remove-call-costs-for-precompiled-contracts/447) would be part of the next hardfork too


*(97 more replies not shown)*
