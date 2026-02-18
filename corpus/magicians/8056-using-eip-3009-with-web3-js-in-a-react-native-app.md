---
source: magicians
topic_id: 8056
title: Using EIP-3009 with web3.js in a react-native app,
author: omidziaee
date: "2022-01-21"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/using-eip-3009-with-web3-js-in-a-react-native-app/8056
views: 565
likes: 0
posts_count: 1
---

# Using EIP-3009 with web3.js in a react-native app,

We are trying to use EIP-3009 in our application. First step we follow the web3 part in [#3010](https://github.com/ethereum/EIPs/issues/3010)

Following is the selected part of our code:

```auto
const nonce = web3.utils.randomHex(32);
        const data = {
            types: {
              EIP712Domain: [
                { name: "name", type: "string" },
                { name: "version", type: "string" },
                { name: "chainId", type: "uint256" },
                { name: "verifyingContract", type: "address" },
              ],
              TransferWithAuthorization: [
                { name: "from", type: "address" },
                { name: "to", type: "address" },
                { name: "value", type: "uint256" },
                { name: "validAfter", type: "uint256" },
                { name: "validBefore", type: "uint256" },
                { name: "nonce", type: "bytes32" },
              ],
            },
            domain: {
              name: "Coin Test",
              version: "1",
              chainId: "3",
              verifyingContract: "0xd73ce105814e.......76",
            },const nonce = web3.utils.randomHex(32);
        const data = {
            types: {
              EIP712Domain: [
                { name: "name", type: "string" },
                { name: "version", type: "string" },
                { name: "chainId", type: "uint256" },
                { name: "verifyingContract", type: "address" },
              ],
              TransferWithAuthorization: [
                { name: "from", type: "address" },
                { name: "to", type: "address" },
                { name: "value", type: "uint256" },
                { name: "validAfter", type: "uint256" },
                { name: "validBefore", type: "uint256" },
                { name: "nonce", type: "bytes32" },
              ],
            },
            domain: {
              name: "Things Coin Test",
              version: "1",
              chainId: "3",
              verifyingContract: "0xd73ce105.....Be76",
            },
            primaryType: "transferWithAuthorization",
            message: {
              from: this.state.senderAddress,
              to: this.state.receiverAddress,
              value: 100,
              validAfter: 0,
              validBefore: Math.floor(Date.now() / 1000) + 3600, // Valid for an hour
              nonce: nonce,
            },
          };
          const signedMessage = web3.eth.accounts.sign(data, this.state.privateKey)
            primaryType: "transferWithAuthorization",
            message: {
              from: this.state.senderAddress,
              to: this.state.receiverAddress,
              value: 100,
              validAfter: 0,
              validBefore: Math.floor(Date.now() / 1000) + 3600, // Valid for an hour
              nonce: nonce,
            },
          };
          const signedMessage = web3.eth.accounts.sign(data, this.state.privateKey)
```

Following that we use a transaction object and signed it to send to Infura. The walletAddress is the address of the third person who is paying the transaction fee in ether. senderAddress is the address of the person who is sending the erc20 but does not have any ether to pay the fee.

```auto
const rawTransaction = ({
            from: walletAddress,
            to: contractAddress,
            value: web3.utils.toHex('0'),
            gasprice: web3.utils.toHex('1000'),
            gas: web3.utils.toHex("100000"),
            data: TNGContract.methods.transferWithAuthorization(
                this.state.senderAddress,
                this.state.receiverAddress,
                100,
                0,
                MAX_UINT256,
                nonce,
                signedMessage.v,
                signedMessage.r,
                signedMessage.s,
              ).encodeABI(),
        });
        console.log('-----------rawTransaction: ' + JSON.stringify(rawTransaction))
        web3.eth.accounts.signTransaction(rawTransaction, privateKey)
            .then((signedTransaction) => {
                console.log('.-----signedTransaction: ' + JSON.stringify(signedTransaction))
                web3.eth.sendSignedTransaction(signedTransaction.rawTransaction).then((receipt)=>{
                    console.log('.-----receipt: ' + JSON.stringify(receipt))
                }).catch(err => {console.log("the error is----- " + err)})
            }).catch((e) => console.log("the error is: " + e));
```

Problem is we are getting “Fail with error ‘EIP3009: invalid signature’” each time we are sending the transaction. Any help is appricaited.
