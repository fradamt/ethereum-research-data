---
source: magicians
topic_id: 16025
title: Keyless contract deployment with CREATE3
author: SKYBITDev3
date: "2023-10-08"
category: Magicians > Primordial Soup
tags: [contract-deployment]
url: https://ethereum-magicians.org/t/keyless-contract-deployment-with-create3/16025
views: 2089
likes: 2
posts_count: 8
---

# Keyless contract deployment with CREATE3

I’ve created a GitHub repository that explores the pros and cons of various ways to achieve the goal of getting the same address on different blockchains for a contract. My conclusion is that the best way to do it is to deploy the contract using a **keylessly-deployed CREATE3 factory**.

I’m now sharing my findings to the community, so check it out at: [GitHub - SKYBITDev3/SKYBIT-Keyless-Deployment: Deploy your smart contract to the same address on many blockchains (with fewer pitfalls)](https://github.com/SKYBITDev3/SKYBIT-Keyless-Deployment)

With the CREATE3 method, **contract code doesn’t affect the deployed contract’s address**. The address depends on:

- The factory’s contract address
- A user-provided salt

CREATE3 factories usually also factor in the deploying account’s address to prevent contract address clashing / front-running.

The way CREATE3 method works is that first `CREATE2` is used to deploy a new CREATE factory (so nonce is `1`) which then deploys your contract.

Keyless deployment eliminates:

- dependency on the owner of the account who deployed the factory contract
- account nonce synchronization on multiple blockchains

There have been a few CREATE3 factories out there for a while (e.g. ZeframLou’s), but I think that my pure Yul one is the most gas-efficient:

```auto
object "SKYBITCREATE3FactoryLite" {
    code { // Constructor code of the contract
        datacopy(0, dataoffset("runtime"), datasize("runtime")) // Deploy the contract
        return (0, datasize("runtime"))
    }

    object "runtime" {
        code { // Executable code of the object
            mstore(0, caller()) // 32 bytes. The user's address.
            mstore(0x20, calldataload(0)) // 32 bytes. User-provided salt.
            let callerAndSaltHash := keccak256(0x0c, 0x34) // Hash caller with salt to help ensure unique address, prevent front-running. 12 0s skipped as addresses are only 20 bytes. Store result on stack.

            datacopy(0, dataoffset("CREATEFactory"), datasize("CREATEFactory")) // Write CREATEFactory bytecode to memory position 0, overwriting previous data. Data is on left of slot, 0-padded on right.
            let createFactoryAddress := create2(0, 0, datasize("CREATEFactory"), callerAndSaltHash) // Deploy the CREATE factory via CREATE2, store its address on the stack.

            if iszero(createFactoryAddress) {
                mstore8(0, 1) // An error code made up to help identify where it failed
                revert(0, 1) // Return the error code so that it appears for user
            }

            mstore(0, 0) // make first slot 0 to reserve for address from call output

            let creationCodeSize := sub(calldatasize(), 32) // Store creation code size on stack. Skipping first 32 bytes of calldata which is salt.
            calldatacopy(0x20, 32, creationCodeSize) // Overwrite memory from position 0x20 with incoming contract creation code. We take full control of memory because it won't return to Solidity code.

            if iszero(
                call( // Use the deployed CREATEFactory to deploy the user's contract. Returns 0 on error (eg. out of gas) and 1 on success.
                    gas(), // Gas remaining
                    createFactoryAddress,
                    0, // Native currency value to send
                    0x20, // Start of contract creation code
                    creationCodeSize, // Length of contract creation code
                    0, // Offset of output. Resulting address of deployed user's contract starts here. If call fails then whatever was here may remain, so we left it empty beforehand.
                    20 // Length of output (address is 20 bytes)
                )
            ) {
                mstore8(0, 2) // An error code made up to help identify where it failed
                revert(0, 1)
            }

            if iszero(mload(0)) { // Call output was 0 or not received
                mstore8(0, 3) // An error code made up to help identify where it failed
                revert(0, 1)
            }

            return (0, 20) // Return the call output, which is the address (20 bytes) of the contract that was deployed via CREATEFactory
        }

        object "CREATEFactory" {
            code {
                datacopy(0, dataoffset("runtime"), datasize("runtime"))
                return (0, datasize("runtime"))
            }

            object "runtime" {
                code {
                    calldatacopy(0x20, 0, calldatasize())
                    mstore(0, create(0, 0x20, calldatasize())) // Create returns 0 if error

                    return (12, 20) // Addresses are only 20 bytes, so skip the first 12 bytes
                }
            }
        }
    }
}
```

## Replies

**Mani-T** (2023-10-09):

This is really an awesome idea.

---

**kumaryash90** (2023-10-17):

Pretty cool!

I think both create2 and create3 deployments are quite useful if the main requirement is deterministic addresses. When it comes to deploying on a large number of chains, using keyless factories is somehow the only reliable option, giving you a deterministic (if not same) address everywhere.

At thirdweb we use a Create2 factory method (nick’s method, keyless deployment) for deployment of prebuilt contracts.

Have described the architecture as well as challenges faced, in this blog here: [Permissionless infrastructure deployments on 900+ EVM chains — Joaquim Verges](https://mirror.xyz/joenrv.eth/fCVv65jhMdhKajmSnuhFQ7xQPXbFvCaWQmrNwPgWIJk)

---

**SKYBITDev3** (2023-10-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kumaryash90/48/10723_2.png) kumaryash90:

> When it comes to deploying on a large number of chains, using keyless factories is somehow the only reliable option

Yes, that’s my view after having checked and thought about the various options.

I’ve looked at how other projects have tried to have same addresses across multiple blockchains and most simply try to synchronize account nonce, but eventually one or more goes out of sync and they can no longer get the same address on one or more new blockchains. It’s such an unreliable way to try to maintain same addresses across blockchains.

One problem in our way is the transaction replay ban which I’ve written about in:



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png)
    [Transaction replay blanket ban is wrong - needed for keyless contract deployment](https://ethereum-magicians.org/t/transaction-replay-blanket-ban-is-wrong-needed-for-keyless-contract-deployment/15497) [Primordial Soup](/c/primordial-soup/9)



> We need a good way to deploy contracts to the same address on multiple blockchains.
> The best practice is the keyless method as offered by @MicahZoltu and @Arachnid in deterministic deployment proxy - broadcast a replayable deployment transaction that’s already signed by a manual signature from an account whose address is derived from that signature and transaction information.
> The transaction data contains chainId: 0. We can’t write in the actual chainId of the blockchain that we want to deplo…

Maybe there can be a way to allow transaction replay for the deployment needs of developers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kumaryash90/48/10723_2.png) kumaryash90:

> we use a Create2 factory method (nick’s method, keyless deployment) for deployment of prebuilt contracts

If you’re using Nick’s [Deterministic Deployment Proxy](https://github.com/Arachnid/deterministic-deployment-proxy#deterministic-deployment-proxy) from 4y ago that has been deployed to `0x4e59b44847b379578588920ca78fbf26c0b4956c` on many blockchains, then there is front-running vulnerability - if a contract was deployed using the factory then someone else could deploy the same contract to the same address on other EVM-based blockchains (by using the same salt). So I made an update that eliminates that vulnerability:



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png)
    [Updated MicahZoltu's / Arachnid's Deterministic Deployment Proxy](https://ethereum-magicians.org/t/updated-micahzoltus-arachnids-deterministic-deployment-proxy/15947) [Primordial Soup](/c/primordial-soup/9)



> I felt that the great work 4y ago by @MicahZoltu / @Arachnid with the popular CREATE2 factory “Deterministic Deployment Proxy” needed an update. Many other new blockchains have been appearing and gaining traction, so protection from front-running risk is needed.
> In my updated version I’ve hashed caller() with the user-provided salt so that there won’t be an address clash if different accounts deploy a contract with the same user-provided salt:
>
> I’ve also updated dependencies e.g. Solidity vers…

---

**radek** (2023-10-21):

Great public good. But, is it already deployed somewhere besides Sepolia?

---

**SKYBITDev3** (2023-10-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> is it already deployed somewhere besides Sepolia?

Anyone can deploy any of the offered factories to their chosen blockchains if nobody has done so yet to those blockchains. To deploy a factory just edit (e.g. to choose which factory and EVM version) and run [SKYBIT-Keyless-Deployment/scripts/deployKeylessly-Create3Factory.js at main · SKYBITDev3/SKYBIT-Keyless-Deployment · GitHub](https://github.com/SKYBITDev3/SKYBIT-Keyless-Deployment/blob/main/scripts/deployKeylessly-Create3Factory.js).

---

**Lohann** (2024-09-26):

Hello, I work building bridges between various blockchains, and is being quite challenge, because not all EVMs works equally or supports the same set of features, and **Keyless Deployment** requires the exact same bytecode to work on all blockchains (btw not all of them supports pre-eip155 transactions).

Another issue with most `CREATE3` factories is that they actually aren’t an replacement for the `CREATE3` opcode because `msg.sender` is the proxy address, not the actual sender, and the issue is that most of those factories doesn’t provide an way to know who is the actual sender.

---

**Lohann** (2024-09-26):

Also the `CREATE3` is not good an good replacement for **Keyless Deployment**,   if we want anyone to deploy a common good cross-chain contract (such as the [EIP-1820](https://eips.ethereum.org/EIPS/eip-1820)), we must allow anyone to deploy it’s bytecode at an deterministic address, without the expenses of the **Keyless Deployment**.

To accomplish that I implemented this Factory contract, that supports both `CREATE3` and `CREATE2` methods, with an additional feature that allow you to provide custom arguments to the constructor without influencing the resulting address.



      [github.com](https://github.com/Lohann/universal-factory/blob/main/src/UniversalFactory.sol)





####



```sol
/*
 * Universal Factory Contract
 * This standard defines an universal factory smart contract where any address (contract or regular account) can
 * deploy and reserve deterministic contract addresses in any network.
 *
 * Written in 2024 by Lohann Paterno Coutinho Ferreira.
 *
 * Universal Factory is derived from EIP-2470 and EIP-3171, with an additional feature that allows the contract
 * constructor to read arguments without including it in the bytecode, this way custom arguments can be provided
 * and immutables can be set without influencing the resulting `CREATE2` address.
 * - EIP-2470: https://eips.ethereum.org/EIPS/eip-2470
 * - EIP-3171: https://github.com/ethereum/EIPs/pull/3171
 *
 * This contract is intented to be deployed at the same address on all networks using keyless deployment method.
 * - Keyless Deployment Method: https://weka.medium.com/how-to-send-ether-to-11-440-people-187e332566b7
 *
 *  ██╗   ██╗███╗   ██╗██╗██╗   ██╗███████╗██████╗ ███████╗ █████╗ ██╗
 *  ██║   ██║████╗  ██║██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║
 *  ██║   ██║██╔██╗ ██║██║██║   ██║█████╗  ██████╔╝███████╗███████║██║
 *  ██║   ██║██║╚██╗██║██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══██║██║
```

  This file has been truncated. [show original](https://github.com/Lohann/universal-factory/blob/main/src/UniversalFactory.sol)

