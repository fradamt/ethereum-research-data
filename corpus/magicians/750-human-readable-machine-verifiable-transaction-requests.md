---
source: magicians
topic_id: 750
title: Human-readable Machine-verifiable Transaction requests
author: pedrouid
date: "2018-07-16"
category: Protocol Calls & happenings > Council Sessions
tags: [eip-681, eip-1138]
url: https://ethereum-magicians.org/t/human-readable-machine-verifiable-transaction-requests/750
views: 2856
likes: 3
posts_count: 10
---

# Human-readable Machine-verifiable Transaction requests

This is a follow up to the discussions about Human-readable Machine-verifiable Transaction requests from FEM Berlin Council from last weekend which are related to the EIP-1138 and ERC-681 and also Radspec implementation.

EIP-1138: Human-Readable Transaction Requests



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png)
    [EIP-1138: Human-Readable Transaction Requests](https://ethereum-magicians.org/t/eip-1138-human-readable-transaction-requests/565) [EIPs](/c/eips/5)



> I wanted to bring up here the discussion for Human-Readable Transaction Requests that Witek Radomski proposed
>
>
> On WalletConnect we have a method to relay a transaction request from the desktop Dapp to the mobile Wallet but currently this simply provides a raw transaction that the Wallet needs to parse in order to display to the user what’s being requested to be signed
> With this EIP it would enable not only to share this information between the Dapp and the Wallet to display to the user but al…

ERC-681: Representing various transactions as URLs



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png)
    [ERC-681: Representing various transactions as URLs](https://ethereum-magicians.org/t/erc-681-representing-various-transactions-as-urls/650) [EIPs](/c/eips/5)



> This is a very useful proposal by @nagydani  that should be getting more attention now that UX (and what I would call “developer UX”) is such a high priority in the community.
> Simple Summary
> A standard way of representing various transactions, especially payment requests in Ethers and ERC #20 tokens as URLs.
> Abstract
> URLs embedded in QR-codes, hyperlinks in web-pages, emails or chat messages provide for robust cross-application signaling between very loosely coupled applications. A standardi…

Radspec is a safe alternative to Ethereum’s natspec

https://github.com/aragon/radspec

The people present at the discussion were:

Pedro Gomes [@pedrouid](/u/pedrouid)

Mikhail Dobrokhvalov [@Dobrokhvalov](/u/dobrokhvalov)

Johann Barbie [@johba](/u/johba)

Remco Bloemen [@Recmo](/u/recmo)

We discussed the use-case for transaction requests describing in more detail what were functions being called without prior knowledge from the wallet of the smart contract.

A lot of the assumptions of the current implementation is for wallets to know the ABI and source code of the Dapp the user is interacting or simply ignoring this all together and not providing any details about the transaction data.

Right now, you simply approve transactions (for example with Metamask) without knowing the exact intent of transaction that is signed.

The proposal for Human-readable Machine-verifiable Transactions requests has the goal to provide enough information to the user to make sure what they are signing is intended but at the same time it has to be machine-verifiable so that it can’t spoofed by a malicious Dapp.

We explored ERC-681 where you are able to use a URI format to explicitly declare the function called and its parameters to best describe the intent of the transaction.

Consequently we looked into Radspec to verify that the function and parameters described were correct and would produce the intented state change.

However we concluded that the ABI isn’t safe enough to verify that it matches the deployed contract and it could be spoofed to mistake the user into approving an unintended state change. Because despite the ABI describes the name and type of the parameters, it’s possible to lie about the name of a parameter because only the type is necessary to execute the transaction hash.

Using the Radspec README example for providing human-readable transaction requests

```auto
const call = {
  abi: [{
    name: 'multiply',
    constant: false,
    type: 'function',
    inputs: [{
      name: 'a',
      type: 'uint256'
    }],
    outputs: [{
      name: 'd',
      type: 'uint256'
    }]
  }],
  transaction: {
    to: '0x8521742d3f456bd237e312d6e30724960f72517a',
    data: '0xc6888fa1000000000000000000000000000000000000000000000000000000000000007a'
  }
}
```

We have a function called `multiply` which takes two parameters `a` and `b` which are both of type `uint256`. Allowing us to describe a function that the transaction request intends to multiply `a` and `b` but the execution for this function only requires us to call it by hashing `multiply(uint256, uint256)` thus a malicious app could spoof the parameters names to deceive the actual intent of the function without compromising its execution. So it could call the parameters `b` and `c` instead deceiving the user from the real execution of these parameters.

The proposed solution for this problem involves building an infrastructure that allows the comparison of the ABI against the source code of the smart contract. This was described as registry on-chain that would link to an IPFS address that would include the data to re-compile the smart-contract and verify the metadata hash with the deployed smart contract.

The data required to store on IPFS would be the source code, compiler version and optimisation settings. This compilation would have to be run off-chain for example using TrueBit protocol. This would allow to verify the ABI provided by the Dapp matches the deployed smart contract using the metadata hash comparison.

This was as far as the discussion evolved. The consesus was clear that exisiting infrastructure wouldn’t allow to make Human-Readable machine-veriable transactions requests without the access to the source code. Etherscan is currently the biggest source for source code for smart contracts but in order to make it decentralized we chose IPFS for hosing this data.

A proposed incentive for smart contracts to upload their source code to IPFS for allowing this verification was that it provide a “seal of approval” or “verified” badge at a Wallet level, giving a bigger assurance to users that this Dapp is confirmed to execute as intended. This was compared to the HTTPS green secure badge used by websites and would be not only a UX feature but a security feature.

## Replies

**boris** (2018-07-16):

Feels like this could learn from / interact with [ERC-1066: Ethereum Status Codes (ESC)](https://ethereum-magicians.org/t/erc-1066-ethereum-status-codes-esc/283), ping [@expede](/u/expede)

---

**tjayrush** (2018-07-16):

Hi [@pedrouid](/u/pedrouid). I’m not sure if you’re aware of this or if it’s of any use: http://solidity.readthedocs.io/en/v0.4.24/metadata.html.  I’m pretty sure it’s related to what you’re talking about above (but I might be missing something). The trouble, of course, is that the developer has to publish the files (but that’s also true elsewhere). Perhaps we can avoid duplication of effort.

I’d have two suggestions: (1) it might be good to promote knowledge of this meta data as it seems it would be helpful in many way, and (2) it would be great if Solidity generated an IPFS hash (in addition? instead of?). Perhaps there’s a feature request for Solidity there.

---

**pedrouid** (2018-07-17):

This is interesting, it’s definitely directely related but using Swarm instead. It’s cool that this was already thought-out as limitation of Solidity. Would be cool to test this and share the proccess.

---

**tjayrush** (2018-07-17):

It does seem Swarm centric. This brings up two points to me: (1) if you move forward with an IPFS centric design (you should), try to keep the data you put on IFPS in sync with this data, and (2) perhaps we can convince the Solidity devs to output an IPFS location as part of this metadata. If the data can be built from the Solidity compiler and an IPFS hash is made available, won’t that solve part of the problem? I don’t know if I’m missing something.

---

**pedrouid** (2018-07-17):

Regardless if it is Swarm or IPFS, it still requires the Dapp developer to upload their source code to a respective location. The core idea is thatboth Wallet and Dapp developers to benefit from both sides. Wallet developers can access to source code verification to provider better user experience and we can facilitate this verification to be seamless. And Dapp developers can gain a larger user traction since users are assured their code is verified.

Given that Swarm implementation is already there I think this is a good way to start. I’m not aware of any significant advantages to IPFS other than it’s more widely used compared to Swarm.

So my proposal is that we use ERC681 as a starting point for Dapp developers to provide better transaction requests. Wallet developers can get the metadata hash from the deployed contract and use it to query Swarm for the source code. If there is no source code available then it’s not verified but if there is then the source code is recompiled it using a protocol like Truebit. Then the metadata hash and ABI can be compared with the transaction request to verify the intent of the transaction request.

The biggest question is the recompilation part that is not clear who is responsible for it and how expensive is it.

---

**tjayrush** (2018-07-17):

The one thing I like about IPFS is that I can run it forever, and if I never ask for a file, no additional hard drive space is taken on my machine (small hard drive space is of high importance to me). With Swarm, I believe that if I run Swarm, some part of my hard drive is devoted to storing Swarm files even if I don’t ask for them.

The main point, I guess, is that the ‘meta-data’ is consistent and created automatically by the compilers (Solidity and others) and the hash locations provided. If the developer chooses to store the ABI and/or code is up to them. (I wish that could be changed, but I doubt that will happen.)

---

**pedrouid** (2018-09-10):

Just learned from [@danfinlay](/u/danfinlay) that Metamask uses Parity on-chain registry for looking up methods from the data payload on a transaction request.

https://www.bokconsulting.com.au/blog/a-quick-look-at-paritys-signature-registry-contract/

There is a javascript library on Github to make this super simple to use.


      ![image](https://github.githubassets.com/favicons/favicon.svg)
      [github.com](https://github.com/MetaMask/eth-method-registry)


    ![image](https://avatars.githubusercontent.com/u/11744586?s=400&amp;v=4)

###



A JS library for getting Solidity method data from a four-byte method signature








This still doesn’t solve the full scope of this issue but is definitely a significant step forward in the right direction! ![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=9)

---

**tjayrush** (2018-09-27):

Don’t know if this is useful, but my friend, Max Galka, from Elementus scraped this database of ABI function definitions. I feel like this data is self-validating (the function interface leads directly to the four-byte codes, so you don’t have to trust anything). I asked him if I could share this and put it into the public domain for anyone to use. He agreed. https://github.com/Great-Hill-Corporation/quickBlocks/tree/develop/src/other/abis

---

**3esmit** (2019-11-26):

After a transaction request is fulfilled, a transaction hash is given to a user. In a scenario of a chat, where one user request transaction to other, the response should be also standardized.

For that I’ve specified the Transaction Receipt URI.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png)
    [EIP-2400 - Transaction Receipt URI](https://ethereum-magicians.org/t/eip-2400-transaction-receipt-uri/3805) [EIPs](/c/eips/5)



> Latest version: https://github.com/status-im/EIPs/blob/tx-hash-uri/EIPS/eip-2400.md

