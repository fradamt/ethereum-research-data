---
source: magicians
topic_id: 13935
title: Batch Calls JSON Schema
author: JXRow
date: "2023-04-23"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/batch-calls-json-schema/13935
views: 924
likes: 3
posts_count: 4
---

# Batch Calls JSON Schema

Batch calls we use oftenly, like *Approve* then *Swap*, *Approve* then *TransferFrom*, user needs to confirm twice or more in wallet, we put the calls into a JSON, so that the wallet can deal the calls automatic in just one confirm. Here’s the JSON example:

```javascript
let json = {
        rpc: {
            name: 'Scroll_Alpha',
			url: 'https://alpha-rpc.scroll.io/l2',
			chainId: 534353
		},
        calls: [
            {
                to: '0x67aE69Fd63b4fc8809ADc224A9b82Be976039509',
                value: '0',
                abi: 'function transfer(address to, uint256 amount)', //transfer ERC20
                params: [
                    '0xE44081Ee2D0D4cbaCd10b44e769A14Def065eD4D',
                    '1000000'
                ]
            },
            {
                to: '0xE44081Ee2D0D4cbaCd10b44e769A14Def065eD4D',
                value: '1000000000000000000',
                abi: '', //transfer ETH
                params: []
            }
        ]
    }
```

The *abi* standard is defined in [ethers.js](https://docs.ethers.org/v5/api/utils/abi/interface/), this JSON send from app to wallet, and the wallet’s encode function is:

```javascript
const { BigNumber, utils } = require('ethers')

let interface = new utils.Interface([call.abi])
let funcName = call.abi.slice(9, call.abi.indexOf('('))
let data = interface.encodeFunctionData(funcName, call.params)
```

then sign the *data* with Private key.

In this case, wallet knows each call, the total spend(This’s what user really care about) can be calculated before submit. It’s useful for not only EOA but also SmartContractAccount(like AA).

## Replies

**PureBlack** (2023-04-26):

Have you tried it before? Can you reply to me about the transaction hash of Goerli or other chains? I would like to study it，thank you!!!

---

**JXRow** (2023-04-27):

https://blockscout.scroll.io/tx/0x0abd703a4e19a75c0be62d2d50e0e3b2ab52650a15ab1ae32b004b8dcf026159/internal-transactions

I deployed a Smart Contract Wallet to do the batch, the JS code is :

```javascript
const { BigNumber, utils } = require('ethers')

let swapData = utils.defaultAbiCoder.encode(
    ['address', 'address', 'uint8'],
    [USDC_ADDRESS, WALLET_ADDRESS, 1] // tokenIn, to, withdraw mode
)

let json = {
    rpc: {
        name: 'Scroll_Alpha',
        url: 'https://alpha-rpc.scroll.io/l2',
        chainId: 534353
    },
    calls: [
        {
            to: USDC_ADDRESS,
            value: '0',
            abi: 'function approve(address spender, uint256 amount)',
            params: [
                ROUTER_ADDRESS,
                '1000000'
            ]
        },
        {
            to: ROUTER_ADDRESS,
            value: '0',
            abi: 'function swap(tuple(tuple(address pool, bytes data, address callback, bytes callbackData)[] steps, address tokenIn, uint256 amountIn)[] paths, uint amountOutMin, uint deadline) returns (uint amountOut)',
            params: [
                [{
                    steps: [{
                        pool: POOL_ADDRESS,
                        data: swapData,
                        callback: ZERO_ADDRESS,
                        callbackData: '0x',
                    }],
                    tokenIn: USDC_ADDRESS,
                    amountIn: '1000000',
                }],
                0,
                BigNumber.from(Math.floor(Date.now() / 1000)).add(1800)
            ]
        }
    ]
}

const MachineGunWallet = await ethers.getContractFactory('MachineGunWallet')
const machineGunWallet = await MachineGunWallet.attach(MachineGunWallet_ADDRESS)

let toArr = []
let valueArr = []
let dataArr = []
for (let call of json.calls) {
    toArr.push(call.to)
    valueArr.push(call.value)

    if (call.abi != '') {
        let interface = new utils.Interface([call.abi])
        let funcName = call.abi.slice(9, call.abi.indexOf('('))
        let data = interface.encodeFunctionData(funcName, call.params)
        dataArr.push(data)
    } else {
        dataArr.push('0x')
    }
}

await machineGunWallet.batchCalls(toArr, valueArr, dataArr)
console.log('batchCalls done')
```

MachineGunWallet is the Smart Contract Wallet, I like the name, it works like a machine gun, the EOA wallet works like a pistol.  MachineGunWallet.sol is :

```Solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "hardhat/console.sol";

contract MachineGunWallet is Ownable, ReentrancyGuard {
    using ECDSA for bytes32;

    uint public nonce = 1;

    constructor() {}

    receive() external payable {}

    function call(
        address to,
        uint value,
        bytes calldata data
    ) public onlyOwner {
        (bool success, bytes memory result) = to.call{value: value}(data);
        console.logBytes(result);
        if (!success) {
            assembly {
                revert(add(result, 32), mload(result))
            }
        }
        nonce++;
    }

    function batchCalls(
        address[] calldata toArr,
        uint[] calldata valueArr,
        bytes[] calldata dataArr
    ) public onlyOwner {
        for (uint i = 0; i < toArr.length; i++) {
            (bool success, bytes memory result) = toArr[i].call{
                value: valueArr[i]
            }(dataArr[i]);

            if (!success) {
                assembly {
                    revert(add(result, 32), mload(result))
                }
            }
        }
        nonce++;
    }
}
```

Hope this helps !

---

**PureBlack** (2023-05-04):

OK，thanks you，and i saw that Uniswap has also launched Permit2, and the principle should be partially the same, which is very meaningful and interesting.

Here is his code repository and main network contract

https://github.com/Uniswap/permit2

https://etherscan.io/address/0x000000000022d473030f116ddee9f6b43ac78ba3/advanced#code

