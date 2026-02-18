---
source: magicians
topic_id: 2410
title: "'EXTSLOAD' opcode proposal"
author: spalladino
date: "2019-01-13"
category: Magicians > Primordial Soup
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/extsload-opcode-proposal/2410
views: 2511
likes: 8
posts_count: 11
---

# 'EXTSLOAD' opcode proposal

I wanted to gather feedback around proposing a new `EXTSLOAD` opcode, which would allow a contract to read a storage position from another account.

While I understand that this could be regarded as a Bad Idea ™ since it promotes breaking encapsulation, I think it naturally follows `EXTCODEHASH`. Once you have validated that an account holds a particular kind of contract using `EXTCODEHASH`, you can safely use `EXTSLOAD` to check a storage position from that account, knowing that it will have the semantics you expect.

The gas cost for this operation could be much cheaper than actually performing a call to execute a getter from a contract, since it does not require executing (nor loading!) any code on the queried contract, but just retrieving a single storage location.

As for high-level usage of this opcode, this means that getters for a contract (assuming it will rely on a single implementation) could be implemented as methods from Solidity libraries that use this opcode behind the scenes to check the code hash and subsequently retrieve the value from storage.

```auto
contract Box {
  uint256 value;
  constructor (uint256 _value) public { value = _value; }
}

library BoxReader {
  function getValue(Box target) internal {
    // optionally use extcodehash on Box to validate it matches the code
    // use extsload on Box to retrieve the value
  }
}

contract Reader {
  using BoxReader for Box;

  Box box;
  constructor() { box = new Box(); }

  function readBox() public {
    uint256 value = box.getValue();
    // ...
  }
}
```

Besides gas cost savings, the actual use case that drove me to this opcode was using `EXTCODEHASH` for validating implementation contracts behind `DELEGATECALL` proxy contracts. On a system that relies on this pattern for upgradeability, using `EXTCODEHASH` for checking that a contract has the expected code does not cut it, since it may be a proxy sitting in front of the actual implementation contract. This means that the validation would actually be a 3-step process:

- EXTCODEHASH the target account to check it is indeed a proxy,
- EXTSLOAD to retrieve the implementation contract’s address,
- and then EXTCODEHASH the retrieved implementation address and compare it against the desired one

Given I’m not that familiar with the internals of EVM implementations, I wanted to gather some feedback around this before formally proposing it as an EIP. Thanks in advance for any comments!

## Replies

**jochem-brouwer** (2019-01-14):

This is a bad idea. If a storage is marked as “private” this of course means that you can read it off-chain but it is private for a reason: external contracts are **not allowed** to read any storage. If someone wants to implement reading storage (either for all accounts or for some) they can just implement a function which other accounts can call. This would yield about 700 gas for the call plus 200 gas for the SLOAD and some extra overhead for the function selector / memory expansion.

---

**spalladino** (2019-01-15):

Hey Jochem! I understand that reading storage can be implemented as a getter if the contract wants to expose that value. The point of the proposal is coming up with a cheap way (in terms of gas) to go around getters when dealing within a set of closed and well-known contracts, since it removes the need to set up a new context for the CALL, loading the code, running the function selector, etc.

---

**ajsutton** (2019-01-15):

It’s worth noting that the gas cost for EXTSLOAD would have to be quite high - *much* higher than SLOAD because it requires the target account and it’s storage to be loaded. That’s at least 50% of the cost of performing a call (the remaining being loading the other account’s code and a small amount of time creating a new EVM frame).  So it would become more expensive to use EXTSLOAD by about the second or third value loaded that way.

---

**Ethernian** (2019-01-16):

related:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png)
    [EIP-1153: Transient storage opcodes](https://ethereum-magicians.org/t/eip-transient-storage-opcodes/553/1) [Core EIPs](/c/eips/core-eips/35)



> I have written this EIP after having reviewed EIP-1087 (EIP-1087: Net gas metering for SSTORE operations) and its discussion (EIP-1087: Net storage gas metering for the EVM - #35 by Arachnid).
> I propose an alternative design (which Nick said he also considered at some point), which in my opinion can bring bigger benefits than EIP-1087, at lower cost (by this I mean new opcodes with very simple semantics and gas accounting rules, and keeping the existing gas accounting rules for SSTORE intact)…

may be



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/androlo/48/1228_2.png)
    [Account-bound EVM memory](https://ethereum-magicians.org/t/account-bound-evm-memory/2270) [EIPs](/c/eips/5)



> Withdrew PR to flesh it out a bit more. (https: //github .com/ethereum/EIPs/pull/1666)
> Transient storage repo, related: https://github.com/androlo/tstorage
> Much of this comes from experimenting with transient storage (EIP: Transient storage opcodes).
> There are three types of memory involved here:
>
> EVM-bound memory - protected memory used by the EVM to store things like call-, and returndata. Can be read from contract code.
> Account-bound memory - Lasts throughout an entire transaction and can…

---

**SilentCicero** (2019-05-17):

For reference, I wrote up an EIP which outlines this and did a rough implementation in go-ethereum to map it out:


      [github.com](https://github.com/SilentCicero/MultiSignatureWallet/blob/master/eips/EIP_sloadext.md)




####

```md
Title: Opcode SLOADEXT

## Preamble

Presently, Ethereum developers are limited to reading other contracts storage through the use of calls. In this EIP, I introduce a simple but powerful opcode akin to what is already available through the Ethereum RPC Standard via `eth_getStorageAt` called `SLOADEXT` which allows any contract to read the current state storage of another contract.

## Specification

An opcode to retrieve the storage of another contract.

```
sloadext(address:u160, position:u256) -> result:u256
```

#### OpCode

SLOADEXT

#### Inputs (2)

```

  This file has been truncated. [show original](https://github.com/SilentCicero/MultiSignatureWallet/blob/master/eips/EIP_sloadext.md)








For what it’s worth, it’s generally a bad idea, but it has some nice upsides. I don’t think the gas would actually be substantially higher after looking at it implemented. Go-ethereum is well setup to handle it. The question is, do we break the existing call oriented interface design model which is already well established and going pretty well.

---

**Agusx1211** (2019-11-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> external contracts are not allowed to read any storage

Yes and no, you could still workaround that limitation using a witness, and with that you could read any storage position of any account. Anyway, `EXTSLOAD` could still break the assumptions of some systems, reading a storage slot using a witness has his limitations (front running, witness update, etc), and this opcode would remove all those limitations, maybe opening the door to “game” some smart contracts?

---

**jochem-brouwer** (2019-11-05):

The main problem here is that, in my opinion, a beginning solidity dev learns up to some extent that internal/private variables cannot be read from other accounts. This does not even imply the knowledge of how `CALL`s the other contracts work (e.g. invoking their code, shifting the environment to this storage, etc.) - from a “normal” imperative programming approach (e.g. Java) it is clear that something which is “external” which might be vague in the Ethereum context (in practice this is hence another account/address/contract) and which has private/internal variables (in solidity hence not exposed via internal/private - but this holds form EVM in general) it cannot be read from said account.

Since most developers currently use Solidity (this is an assumption but I am pretty sure it holds) it is strongly implies that external accounts cannot read these internal/private variables. Since variables are non-exposed by default this means a developer has to expose them via public (or in case of a function public/external) to allow other accounts to read this.

Adding `EXTSLOAD` directly violates this assumption. In my opinion this is a much larger issue that “detailed” settings e.g. EIP 1283 where we introduce a re-entrancy in case of a fallback (it is implied a fallback cannot be used to exploit via re-entrancy since it cannot SSTORE). This implies that you can immediately read other accounts storage. This results in a gigantic attack vector where developers first assumed that you cannot read storage slot X from an external account and now you suddenly can (directly - e.g. without tricks). This is the reason I strongly oppose this addition.

Given this reasoning I would love to know the reasoning from [@spalladino](/u/spalladino) knowing where, in practice, this opcode is actually useful, besides basically verifying setups via `CREATE2`. I think by now it is clear that there is a safe way to setup `CREATE2` contracts e.g. in a way where the code is either present or it is selfdestructed (overwriting code is not possible, even if the code would equal the currently deployed code).

---

**zemse** (2021-12-19):

The point from [@jochem-brouwer](/u/jochem-brouwer) about software engineering principles regarding private/internal variables makes sense and I’d agree thinking about that makes EXTSLOAD seems like a bad idea. But I’d also like to point out some more use cases/benefits:

1. If a contract is only interested in reading a particular value from a public function which perform multiple SLOADs (in case of UniswapV3Pool.ticks(tickIndex) it’s 4 SLOADs), directly reading the appropriate storage slot would prevent unnecessary SLOADs.
2. Could potentially reduce contract bytecode by decreasing the number of unnecessary view functions (contracts can keep view functions like totalSupply() for adhering to standards)
3. The EVM would not need to load the bytecode of the contract and process it, in order to read a storage variable, hence CALL cost might not be needed? Probably just an SLOAD cost (I think this is already mentioned in the description).

The use of EXTSLOAD should not be standardised, i.e. ERC20 totalSupply, balanceOf, should remain as external view methods. I mean standards should specify view methods only and not that totalSupply should be in slot 5 (with the exception of proxy contracts which need to have implementation address at a specific slot, for security purposes).

---

**open-contracts** (2021-12-19):

To echo [@jochem-brouwer](/u/jochem-brouwer) and provide some further context, having private variables unaccessible to other contracts can be *crucial* for the business model of certain contracts. Think of an oracle solution which has an off-chain component which signs data and submits it on chain, and an oracle contract which checks the signature against a set of somehow trustworthy publiy keys. The contract can only enforce e.g the reimbursement of the oracle nodes or the usage of a certain token if the pubkeys are actually private. If someone else could create a contract that checks the sigs against the pubkeys in the original one, but doesn’t enforce these things, the whole thing breaks. The result of this proposal is to *reduce* the types of contracts that are possible, starving the ecosystem of valuable solutions. It’s not all about gas costs.

---

**moodysalem** (2022-03-11):

IIUC witnesses/storage proofs are going to be cheaper with Verkle trees, although they still have the other drawbacks Agustin mentioned.

The opcode also allows smart contract developers to move a lot of really complicated logic outside of core contracts, since we can read storage directly without large gas overhead. Imagine a contract that allows you to specify an extension contract address, which allows some additional logic to be implemented in the extension. It is painful to have the overhead of a call and potentially unnecessary SLOADs with each field you need to read.

We also had an issue where the getters generated for NFT Position Manager [structs](https://github.com/Uniswap/v3-periphery/blob/51f8871aaef2263c8e8bbf4f3410880b6162cdea/contracts/NonfungiblePositionManager.sol#L34-L52) cost 20k gas to call, even if you only need to get the value in 1 slot as in [here](https://github.com/Uniswap/v3-staker/blob/4328b957701de8bed83689aa22c32eda7928d5ab/contracts/UniswapV3Staker.sol#L160).

I think this opcode should still be prioritized. ~~I also don’t understand why loading the account code is necessary to get the value of a storage slot. Could someone elaborate on that?~~ Description [here](https://discord.com/channels/595666850260713488/706868829900505180/922630739957260328) from Danno Ferrin

> First the account needs to be fetched, to get the trie root for the storage slot. Then the slot needs to be loaded, to get the slot value. cost of EXTCODE is basically the same operation, just reading a different field from the account object. EXTCODEHASH would be a better equivelance.

