---
source: magicians
topic_id: 3634
title: Ecrecover should handle chainId
author: rmeissner
date: "2019-09-06"
category: EIPs
tags: [evm, chain-id]
url: https://ethereum-magicians.org/t/ecrecover-should-handle-chainid/3634
views: 2584
likes: 5
posts_count: 12
---

# Ecrecover should handle chainId

This is a follow up to [EIP-1344: Add chain id opcode](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131)

The purpose of EIP-1344 was to improve the security of signatures. Adding to that (or even independently of that) I would like to propose that ecrecover should be adjusted to handle [EIP-155](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md). This would allow even existing contracts to use signatures that cannot be replayed between chains.

Would love to hear your opinions.

cc the EIP-1344 people: [@fubuloubu](/u/fubuloubu) [@wighawag](/u/wighawag) [@fulldecent](/u/fulldecent)

## Replies

**fubuloubu** (2019-09-06):

Great idea! Is the concept to change the Solidity implementation of `ecrecover` here to return a tuple of `(address, chainId)` for further verification?

---

**rmeissner** (2019-09-06):

I think solidity needs to be updated anyways since it should accept something else for v (currently uint8 should probably be uint64)

Side note: changing the return value breaks backwards compatibility, also ecrecover will fail if the signature was created with an invalid chainId (and the current chainId can be checked with EIP-1344 ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) ). But I see your point, that it might be interesting to know if a signature used a chain id.

Second side note: With EIP-1344 new contracts can implement this themselves by checking/adjusting the “v” before handing it over to the ecrecover function. (I would still love it, since it would provide additional security to existing contracts and also outside of EIP-712)

---

**axic** (2019-09-07):

I’m not sure why is there a change needed to the `ecrecover` built in method in Solidity? That is a low-level abstraction working off the precompile.

Handling of the chainid is (and should be) above this, e.g. the best place is high level “ec recover” libraries, such as the example I wrote or the widely used implementation in OpenZeppelin.

---

**axic** (2019-09-07):

And I think this issue may be better to be taken to https://github.com/ethereum/solidity.

---

**fulldecent** (2019-12-01):

`ecrecover` cannot be changed.

Multiple chains is a known issues and frameworks deal with it at the application layer. This is discussed in the recent EIP threads regarding `CHAINID`.

I recommend to close this thread and create a new thread which brings up specific application-level requirements. Or if there is an implementation that is already fleshed out and something isn’t working then it can be discussed on Stack Exchange or similar.

---

**rmeissner** (2019-12-02):

> ecrecover  cannot be changed.

Why can it not be changed?

> frameworks deal with it at the application layer

Also while this is true (this is why [@fubuloubu](/u/fubuloubu) and I got the ChainId EIP into the hardfork) it feels like a hack. Why can we trust the chain id for normal transactions? Because it is enforced by the protocol. If I create a signature I might not want that it is valid on any other chain (same as with transactions). And this should be enforced by the protocol.

It is also not really hard to adjust `ecrecover`. For example you could say that if `v` applies to EIP-155 than you take the `hash` append the `chain-id` and use `keccak` to generate a new hash that is used for recovery. If that is defined in the protocol everybody knows how to generate a signature that includes the chain-id and it also doesn’t break the current signatures.

---

**fubuloubu** (2019-12-02):

I think the low level opcodes we have are fine as is. Basically, that you can recover an ecdsa public key given a signature, a message, and a recovery ID. It is a bit hackish looking, but that is just how ecdsa works since the math makes it not possible to recover a signing public key unless you have the recovery ID.

Now, the Solidity `ecrecover` function just wraps `ecrecover`. That function could be adjusted to have a nicer, higher-level API that could account for chain ID now being a part of the EVM (since it is mixed into the definition via EIP-155), but as [@axic](/u/axic) said this is an “application” level discussion (really compiler discussion) of how to adapt the API to make it more ergonomic and account for new EVM features.

I’m fine with continuing that discussion here, as it would be good to be aligned on this API between different compilers and client-side libraries.

---

**rmeissner** (2019-12-02):

My point is that I would align the behavior of the opcode with the behavior of EIP-155. I do agree that this could (and maybe should) be done on application level, but Ethereum started doing it on protocol level for transactions, so in my opinion the current behavior is inconsistent (message signatures are handled different by the protocol then transaction signature). But again, this might be fine and if it is I would actually not change anything. The biggest advantage in adjusting the opcode behavior would be that even existing contracts could benefit from message signatures with included chain id.

Note: I talk about protocol level when I mean EVM and Node implementations and application level when I mean smart contracts and solidity

---

**fulldecent** (2019-12-03):

The precompile is specified for v ∈ {27, 28}. Changing that will introduce unacceptable backwards incompatibilities. So if a different ECRECOVER function is needed it should go at a different address. That was my only point.

---

**cyrus** (2023-04-19):

I’m doing some work on sepolia and with a chain id of 11155111, ecrecover (with v as a uint8) is broken. Is it time for a new ecrecover155(…) to move forward? Is there an EIP for this?

---

**cyrus** (2023-04-22):

No opinions?

Side question: Will transactions using v = 27 or 28 always be valid on Ethereum mainnet (et al)? EIP-155 transactions are preferred, obviously, but one could still use the old style forever?

