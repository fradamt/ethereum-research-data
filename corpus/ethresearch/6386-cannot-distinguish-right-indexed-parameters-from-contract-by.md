---
source: ethresearch
topic_id: 6386
title: Cannot distinguish right indexed parameters from contract bytecode
author: JChoy
date: "2019-10-29"
category: EVM
tags: []
url: https://ethresear.ch/t/cannot-distinguish-right-indexed-parameters-from-contract-bytecode/6386
views: 2263
likes: 0
posts_count: 6
---

# Cannot distinguish right indexed parameters from contract bytecode

These two codes are example contract sources(below example is Solidity, but Vyper has same issue):

```auto
contract A {
    event Transfer(address indexed a, address b, uint256 indexed c);

    function transfer() public {
        emit Transfer(address(0x776), address(0x777), 256);
    }
}

contract B {
    event Transfer(address a, address indexed b, uint256 indexed c);

    function transfer() public {
        emit Transfer(address(0x777), address(0x776), 256);
    }
}
```

Above two contracts are different at the place of the indexed parameter. However, they’re compiled bytecodes(with v0.5.11) are same as below(except code hash obviously):

`6080604052348015600f57600080fd5b5060a98061001e6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80638a4068dd14602d575b600080fd5b60336035565b005b604080516107778152905161010091610776917fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef9181900360200190a356fea265627a7a72315820${32_byte_code_hash}64736f6c634300050b0032`

So, it means those two different events in each contracts emit the same events and we cannot distinguish the orders of parameters without **EXACT** ABI.

The problem is at the ERCs like ERC20 and ERC721.

At [ERC20](https://github.com/ethereum/EIPs/blob/ac1a50936cd3b5b22943a8354ce31912191d1c34/EIPS/eip-20.md), the official event format for `Transfer` is:

```auto
event Transfer(address indexed _from, address indexed _to, uint256 _value)
```

Guess if someone deployed a contract has `Transfer` as below:

```auto
event Transfer(address indexed _from, address _to, uint256 indexed _value)
// or
event Transfer(address _from, address indexed _to, uint256 indexed _value)
```

Is that code ERC20?

- If so, is there any way to distinguish the parameters from event logs without the code’s ABI?

If not, let’s take a look with [ERC721](https://github.com/ethereum/EIPs/blob/ac1a50936cd3b5b22943a8354ce31912191d1c34/EIPS/eip-721.md) and [CryptoKitties source code](https://etherscan.io/address/0x06012c8cf97bead5deae237070f9587f8e7a266d#code).

The official `Transfer` event at EIP721 is:

```auto
event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
```

However, the CryptoKitties implementation is:

```auto
event Transfer(address from, address to, uint256 tokenId);
```

Can we call the Cryptokitties ERC721, then?

So the main question is:

***"Is there any ways to distinguish the place of the indexed parameters just with bytecode?"***

The question about ERCs is incidental curiosity.

Please let me know if I am wrong.

## Replies

**hjorthjort** (2019-11-04):

I’m new to how the Solidity compiler generates Wasm. Could you post the full bytecode generated? I want to have a look at it bby using `wasm2wat` and read the wasm generated. I’m curious how (and if at all) the `indexed` keyword is handled.

---

**dankrad** (2019-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/jchoy/48/1270_2.png) JChoy:

> Above two contracts are different at the place of the indexed parameter. However, they’re compiled bytecodes(with v0.5.11) are same as below(except code hash obviously)

If you look at the [ABI specification](https://solidity.readthedocs.io/en/v0.5.12/abi-spec.html), it does seem like the two events you defined in contract A and contract B are exactly the same type, as the indexed and non-indexed parameters are listed separately.

![](https://ethresear.ch/user_avatar/ethresear.ch/jchoy/48/1270_2.png) JChoy:

> Can we call the Cryptokitties ERC721, then?

It would appear that it is not binary compatible. In fact the [EIP 721](https://github.com/ethereum/EIPs/blob/361c33c62a6277f8a13e3861bb14422424c50ce9/EIPS/eip-721.md) includes a reference to that: “CryptoKitties – Compatible with an earlier version of this standard.”

---

**JChoy** (2019-11-15):

Yup

For the contract A : `0x6080604052348015600f57600080fd5b5060a98061001e6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80638a4068dd14602d575b600080fd5b60336035565b005b604080516107778152905161010091610776917fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef9181900360200190a356fea265627a7a72315820f1fb868f6466c739db25d5180d2e3aad5de6229fa9f94201f8ea9fde7bc8624364736f6c634300050b0032`

For the contract B: `0x6080604052348015600f57600080fd5b5060a98061001e6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80638a4068dd14602d575b600080fd5b60336035565b005b604080516107778152905161010091610776917fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef9181900360200190a356fea265627a7a72315820183916728e1679f1337e395629f61bc231f1b11e22aa488890af62fd31cb7df264736f6c634300050b0032`

---

**JChoy** (2019-11-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> If you look at the ABI specification, it does seem like the two events you defined in contract A and contract B are exactly the same type, as the indexed and non-indexed parameters are listed separately.

Yes, the indexed and non-indexed parameters are separated during compile. The problem is, if we parse the event logs of the contract B with contract A’s ABI, that we cannot realize the problem easily.

So, if someone wants to parse random ERC20 events just with the standard ABI, his code does not parse properly with some cases which has different indexed parameters.

I think it is impossible to find out if an anonymous contract(we only know about the bytecode) implements the standard events form.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> It would appear that it is not binary compatible. In fact the EIP 721 includes a reference to that: “CryptoKitties – Compatible with an earlier version of this standard.”

Got it, you’re right!

---

**JoyCood** (2021-06-14):

i meet the same issue, did you  fight it out now?

