---
source: magicians
topic_id: 22800
title: "New ERC: Programmatically Derived Addresses (PDAs)"
author: JohnCrunch
date: "2025-02-08"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/new-erc-programmatically-derived-addresses-pdas/22800
views: 182
likes: 8
posts_count: 9
---

# New ERC: Programmatically Derived Addresses (PDAs)

A proposal for programmatically derived addresses, which would drastically improve compute efficiency and storage demands on chain. While we are bound by the iron triangle of decentralization, we can “shrink” the entire triangle with structural improvements, such as PDAs.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/890)














####


      `ethereum:master` ← `JohnCrunch:erc-pda-proposal`




          opened 03:32PM - 08 Feb 25 UTC



          [![JohnCrunch](https://avatars.githubusercontent.com/u/197000207?v=4)
            JohnCrunch](https://github.com/JohnCrunch)



          [+106
            -0](https://github.com/ethereum/ERCs/pull/890/files)







This is a draft ERC proposing Programmatically Derived Addresses (PDAs).

- ER[…](https://github.com/ethereum/ERCs/pull/890)C Number: To be assigned by an editor.
- Discussion Link: TODO create conversation in ethereum magicians with this ERC

### Summary
This ERC introduces a mechanism for generating deterministic, contract-derived addresses without private keys. PDAs enable permissionless, stateless interactions with smart contracts while ensuring security and uniqueness.

Requesting review from ERC editors. Thanks!

## Replies

**shemnon** (2025-02-08):

How do you intend to get contracts at those addresses?  A fully worked out process is needed otherwise this won’t work as intended.

---

**JohnCrunch** (2025-02-08):

My perspective is using CREATE2, which allows deterministic deployment for contracts.

- Process:

1. Derive PDA
2. A contract deployer (e.g., a factory contract) uses CREATE2 to deploy a contract at that PDA address
3. Any user can verify the address by recomputing the PDA and checking that a contract exists at that location.

(Contracts must be deployed before any interactions).

---

**shemnon** (2025-02-08):

I think what you are missing is that CREATE2 doesn’t really get to pick it’s address.  CREATE2 address derivation is

`keccak256( 0xff ++ address ++ salt ++ keccak256(init_code))[12:]` per EIP-1014. Your solidity code is not compatible with what the EVM requires.  You may be able to write a contract that will allow arbitrary code with a fixed init_code and then tweak salt, but that’s not even contemplated upon in this ERC.

---

**marioevz** (2025-02-08):

I think this requires at least a couple of new opcodes to be feasible.

I’m thinking of an opcode that allows to make a call from an address that is derived from the current contract’s address plus a salt, and we can call this address a “contract owned address”, something like:

`OWNEDCALL(address, salt, value)`

- address is the recipient of the call.
- salt is a value that is combined with the address of the contract in the caller context to generate a new address that would become msg.sender on the recipient end.
- value is Eth taken from the calculated address’s balance and included with the message.

We could also have `OWNEDSETCODE` that would do something very similar to set code transactions from 7702, but for the addresses owned by the contract.

---

**JohnCrunch** (2025-02-08):

thank you, yes! I was thinking something like:

```auto
function computeCreate2Address(address deployer, bytes32 salt, bytes memory initCode) public pure returns (address) {
    return address(uint160(uint256(keccak256(abi.encodePacked(
        bytes1(0xff),
        deployer,
        salt,
        keccak256(initCode)
    )))));
}
```

but [@marioevz](/u/marioevz) wrote a much better comment

---

**shemnon** (2025-02-08):

New opcodes for this will be a hard sell, and it would also need to be an EIP instead of an ERC.

That being said, I think a 90% solution may be on the way.  The derivation scheme for EOF’s propsoed TXCREATE (EIP-7873, [still a PR](https://github.com/ethereum/EIPs/pull/9299)) is simply

```auto
keccak256(0xff || sender || salt)[12:]
```

which would allow contracts using a modified PDA to deploy arbitrary contracts to PDAs from it’s address derivation.

The modification would be to have the ERC specify what goes into the salt of the TXCREATE opcode and then let that address derivation occur.  So if one PDA had three seeds and a keccak derivation the effective address derivation would be

```auto
keccak256(0xff || sender || keccak256(seed1 || seed2 || seed3))[12:]
```

And as long as the factory/source contract is wired for it they can have contracts deployed at those addresses per the contract’s own rules.

---

**JohnCrunch** (2025-02-10):

This looks great. Will follow, appreciated

---

**suiiii** (2025-02-14):

Can’t you achieve the same result using create3? For example pcaversaccio/createx on github is deployed on a lot of chains

