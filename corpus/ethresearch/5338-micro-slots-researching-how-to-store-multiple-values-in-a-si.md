---
source: ethresearch
topic_id: 5338
title: Micro slots - researching how to store multiple values in a single uint256 slot
author: tpmccallum
date: "2019-04-21"
category: Data Science
tags: []
url: https://ethresear.ch/t/micro-slots-researching-how-to-store-multiple-values-in-a-single-uint256-slot/5338
views: 3269
likes: 6
posts_count: 10
---

# Micro slots - researching how to store multiple values in a single uint256 slot

Please find some design patterns (below) which use modulo arithmetic & exponentiation to access and store multiple values inside a single uint256 slot.

**Pseudo code 1 - read one or more digits from a uint256 variable**

```auto
((_value % (10 ** _position)) - (_value % (10 ** (_position - _size)))) / (10 ** (_position - _size));
```

**Solidity**

This has been implemented in Solidity as a pure function

```auto
contract uintTool {
    function getInt(uint256 _value, uint256 _position, uint256 _size) public pure returns(uint256){
        uint256 a = ((_value % (10 ** _position)) - (_value % (10 ** (_position - _size)))) / (10 ** (_position - _size));
        return a;
    }
}
```

**Implementation**

It has also been deployed on the Ropsten test network at the following contract address if you would like to interact with it.

```auto
0x33539788196abf0155e74b80f4d0916e020226f7
```

**Usage**

The above getInt function will return a value of **1234567** if passed the following arguments

```auto
_value 99999991234567999999999999999999999999999999999999999999999999999999999999999
_position 70
_size 7
```

**Thank you**

Thank you for having a super quick chat with me about this at EDCON2019 [@vbuterin](/u/vbuterin), I went ahead and wrote this getInt function in Vyper straight after our quick chat. I appreciate that this is something that you have already thought of/tried; I would like to refine the general idea and formalize it as an [Informational EIP](https://github.com/ethereum/EIPs/blob/08e28dcaeda388fe03d3cb483a30c04bf9f5ef92/EIPS/eip-draft_micro_slots.md).

For more information, and many more examples, please see [this GitHub repository](https://github.com/second-state/micro-slots/blob/master/README.md)

## Replies

**PhABC** (2019-04-23):

We used this approach in our ERC-1155 implementation if you are interested in looking into the [details](https://github.com/horizon-games/multi-token-standard/blob/2b16c20a15a00f77e24927f4528e0c3911831f73/contracts/tokens/ERC1155PackedBalance/ERC1155PackedBalance.sol). I wrote a blog post about it sometime ago as well: https://medium.com/horizongames/going-beyond-erc20-and-erc721-9acebd4ff6ef

---

**tpmccallum** (2019-04-24):

Hi [@PhABC](/u/phabc)

Thank you for your article and code URLs. Very thought provoking!

May I suggest the use of convention for assigning micro slots inside the uint256 data type. For example there are 77 (0-9) digits available. The factors of 77 are 1, 7, 11 and 77. Therefore the following options will explicitly segment the uint256 and ensure that as much of the uint256  is being used.

- 1, 77 digit integer with an individual value between 0 and 99999999999999999999999999999999999999999999999999999999999999999999999999999
- 77, 1 digit integers with an individual value between 0 and 9
- 7, 11 digit integers with an individual value between 0 and 99999999999
- 11, 7 digit integers with an individual value between 0 and 9999999

I have provided some Solidity code below which enforces the last bullet point from above; provides 11 unique slots, each of which can contain a maximum of 7 digits (total value of between 0 and 9999999).

```auto
pragma solidity ^0.5.0;

// The following contract uses a fixed convention which provides 11 unique micro-slots, each with 7 digits between 0 and 9.
// Each of the functions are designed to explicitly return the appropriate slot.
// Warning: This is a prototype for research purposes and it is not to be used to transact real value yet.

contract MicroSlots{

// This variable must be set to 77 digits between 0 and 9
uint256 private value = 76543210000000000000000000000000000000000055555554444444333333322222221111111;

// TODO This contract needs modifiers which will only allow numbers between 1 and 9999999 to be set for each position

// Returns 1111111
function getPosition1() public view returns(uint256){
    return ((value % (10 ** 7)) - (value % (10 ** (7 - 7)))) / (10 ** (7 - 7));
}

// Returns 2222222
function getPosition2() public view returns(uint256){
    return ((value % (10 ** 14)) - (value % (10 ** (14 - 7)))) / (10 ** (14 - 7));
}

// Returns 3333333
function getPosition3() public view returns(uint256){
    return ((value % (10 ** 21)) - (value % (10 ** (21 - 7)))) / (10 ** (21 - 7));
}

//Returns 4444444
function getPosition4() public view returns(uint256){
    return ((value % (10 ** 28)) - (value % (10 ** (28 - 7)))) / (10 ** (28 - 7));
}

// Returns 5555555
function getPosition5() public view returns(uint256){
    return ((value % (10 ** 35)) - (value % (10 ** (35 - 7)))) / (10 ** (35 - 7));
}

// Returns 0000000
function getPosition6() public view returns(uint256){
    return ((value % (10 ** 42)) - (value % (10 ** (42 - 7)))) / (10 ** (42 - 7));
}

// Returns 0000000
function getPosition7() public view returns(uint256){
    return ((value % (10 ** 49)) - (value % (10 ** (49 - 7)))) / (10 ** (49 - 7));
}

// Returns 0000000
function getPosition8() public view returns(uint256){
    return ((value % (10 ** 56)) - (value % (10 ** (56 - 7)))) / (10 ** (56 - 7));
}

// Returns 0000000
function getPosition9() public view returns(uint256){
    return ((value % (10 ** 63)) - (value % (10 ** (63 - 7)))) / (10 ** (63 - 7));
}

// Returns 0000000
function getPosition10() public view returns(uint256){
    return ((value % (10 ** 70)) - (value % (10 ** (70 - 7)))) / (10 ** (70 - 7));
}

// Returns 7654321
function getPosition11() public view returns(uint256){
    return ((value % (10 ** 77)) - (value % (10 ** (77 - 7)))) / (10 ** (77 - 7));
}

}
```

The above contract has been deployed on the Ropsten Testnet at the following address

```auto
0xc7b6ac40d8557de62a33f5bcec6c4dc443fbd0f3
```

The functions are all public view so please feel free to interact with it.

Again, thank you so much for your response!

---

**tpmccallum** (2019-04-24):

I have a way to [zero-out (flush) each micro-slot](https://github.com/second-state/micro-slots/blob/11c942aa0129ac2dfd72bb8f33d20ac88a774d57/README.md#zerooutmanyvalues-output-examples), as well as, individually [update each micro-slot’s](https://github.com/second-state/micro-slots/blob/11c942aa0129ac2dfd72bb8f33d20ac88a774d57/README.md#updatemanyvalues-output-examples) value.

I can provide the Solidity code for this here also if anyone is interested. I feel that this could be a very powerful tool for certain applications. Please let me know if there are any specific use cases and I will go ahead and code up the contract and the modifiers (validate inputs outputs etc.).

Many thanks

Tim

---

**Idiotcards** (2019-05-18):

Awesome work. Very helpful. Thanks. I am interested in the Solidity code for the Zero-out and update each micro-slot. Please do post it here at your convenience. Cheers

---

**quickBlocks** (2019-05-31):

This is interesting from the perspective of the developer (and the user) because it reduces gas costs. That’s an important consideration, to be sure, but I write tools that try to access arbitrary data from any smart contract (permissionless accounting). Generally, we only have the ABI to guide us about what’s going on.

Would there be any way to programmatically understand the storage/input/event data of a smart contract through the ABI? Or would an ‘outsider’ (such as our software) have to know that the uint256 in the ABI interface is actually storing multiple values?

This is obviously a useful and interesting idea, but there may be considerations other than simply gas savings. Have you thought about how this type of storage mechanism might be communicated to tools?

---

**tpmccallum** (2019-06-01):

Hi,

Thank you so much for your response and questions.

**Programmatically understanding the data**

I envisage that the developer would write a smart contract such as [this prototype example](https://github.com/second-state/micro-slots/blob/54e64ff44c32ef13525d9a244b4e2f6d0844be97/eleven_separate_slots_per_uint256.sol) which I have provided. You will notice that the actual uint256 variable is private, however you will also see some pre-written “get” and “set” functions which can access each of the slots.

**Validation (overflow and underflow)**

These pre-written functions could include custom validation etc. The main point is that the pre-written functions will be available in the ABI. Of course the developer might want to give the pre-written functions more meaningful names. I just programmatically churned the pre-written functions out using a for loop in Javascript.

**Events**

Also, I like your point about events. We could absolutely create some events with meaningful names and then emit those events as part of each “get” and “set” function. All in all the combination of the above would allow external tools to instantiate a web3 contract instance and harvest not only the current state (by calling all of the public/view functions) but also harvest and store the event logs for the life of the contract (and even create a watcher for real-time events).

**Compiler support**

I like this Micro slots approach because it **can be implemented in the Vyper programming language** by any developer. It does not require new opcodes.

It is my current understanding that (whilst alternatives to Micro slots such as [Bitwise shifting](https://github.com/ethereum/EIPs/blob/96e8093f6ac1e126dc18eb8485b81e369c9b5538/EIPS/eip-145.md) may be as cheap or cheaper in terms of gas) Bitwise shifting is only supported in the Solidity compiler.

a) I am happy to be wrong about the Vyper support, please correct me if Vyper now supports the Bitwise shift opcodes.

b) I am not sure if Bitwise shifting is actually cheaper than Micro slots in terms of gas. If someone could test and measure this I would be ever so grateful.

**EIP to formalize this design pattern**

In a community spirit, and also to improve safety and prevent duplication of effort, I would like to see the community refine the idea in [this informational EIP](https://github.com/ethereum/EIPs/blob/08e28dcaeda388fe03d3cb483a30c04bf9f5ef92/EIPS/eip-draft_micro_slots.md) so that there is a safe and comprehensive resource (design pattern) for the community to use, if they so desire.

I hope this answers your questions.

Thanks again for the reply, much appreciated.

---

**tpmccallum** (2019-06-01):

Hi,

Sorry, I just re-read this and realized that you specifically asked for the Solidity code to Zero-out and update each micro-slot (as apposed to just zeroing out and updating arbitrary positions in the uint256). Apologies for the delayed response. I have been meaning to write a full smart contract (building on [the previous work here](https://github.com/second-state/micro-slots/blob/54e64ff44c32ef13525d9a244b4e2f6d0844be97/eleven_separate_slots_per_uint256.sol)). I will get back to this and include getters, setters, events and more. I will just need some more time as I am currently very busy. Hold that thought ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**quickBlocks** (2019-06-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/tpmccallum/48/1486_2.png) tpmccallum:

> Thanks again for the reply, much appreciated.

No problem. If you ever deploy something on the mainnet, let me know (by posting to this post), and I will try to use it as a test case in our code.

---

**Idiotcards** (2019-06-08):

Thx. No hurries. Very good resource. I will update you on my progress

