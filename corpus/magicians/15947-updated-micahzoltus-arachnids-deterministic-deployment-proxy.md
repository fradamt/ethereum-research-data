---
source: magicians
topic_id: 15947
title: Updated MicahZoltu's / Arachnid's Deterministic Deployment Proxy
author: SKYBITDev3
date: "2023-09-29"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/updated-micahzoltus-arachnids-deterministic-deployment-proxy/15947
views: 1985
likes: 3
posts_count: 16
---

# Updated MicahZoltu's / Arachnid's Deterministic Deployment Proxy

I felt that the great work 4y ago by [@MicahZoltu](/u/micahzoltu) / [@Arachnid](/u/arachnid) with the popular CREATE2 factory “Deterministic Deployment Proxy” needed an update. Many other new blockchains have been appearing and gaining traction, so protection from front-running risk is needed.

In my updated version I’ve hashed `caller()` with the user-provided salt so that there won’t be an address clash if different accounts deploy a contract with the same user-provided salt:



      [github.com](https://github.com/SKYBITDev3/deterministic-deployment-proxy/blob/32bfd8755d042a8cec6f771234ab31532669a5b9/source/deterministic-deployment-proxy.yul#L11-L13)





####



```yul


1. mstore(0, caller()) // 32 bytes. The user's address.
2. mstore(0x20, calldataload(0)) // 32 bytes. User-provided salt.
3. let callerAndSaltHash := keccak256(0x0c, 0x34) // Hash caller with salt to help ensure unique address, prevent front-running. 12 0s skipped as addresses are only 20 bytes. Store result on stack.


```










I’ve also updated dependencies e.g. Solidity version from 0.5.8 to 0.8.21 (the latest), and you can set `evmVersion` to `paris` if you need to deploy the factory to any blockchains that don’t yet support `PUSH0` opcode at:



      [github.com](https://github.com/SKYBITDev3/deterministic-deployment-proxy/blob/32bfd8755d042a8cec6f771234ab31532669a5b9/scripts/compile.ts#L51-L52)





####



```ts


1. // compilerInput.settings.evmVersion = 'paris'
2. compilerInput.settings.evmVersion = 'shanghai' // downgrade to `paris` if you encounter 'invalid opcode' error


```

## Replies

**MicahZoltu** (2023-09-29):

The entire point of deterministic deployment proxy is that they can’t be “frontrun”.  If you get frontrun it just means someone else paid the gas for you and saved you some money, but the thing they deployed will be exactly the same as the thing you would have deployed.

---

**SKYBITDev3** (2023-09-29):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> the thing they deployed will be exactly the same as the thing you would have deployed

It’d be an issue if, for example, a contract that someone deployed using the old Deterministic Deployment Proxy has *privileged access*, e.g.

- functions with onlyOwner function modifier, with owner being the account that deployed it;
- functions with onlyRole function modifiers, with roles (particularly default admin) granted to the account that deployed it in the constructor.

---

**MicahZoltu** (2023-09-29):

Any references to `msg.sender` in a deterministically deployed contract’s constructor are functionally *not* deterministically deployed.

If you want a specific address to have special rights and you also want a deterministically address, then you should set the address as an constant in the contract so you get the same address on all chains regardless of who triggers the deployment.  This will also make it more clear in the code what the intent is, rather than relying on a specific deployment procedure to get the code you want on-chain.

---

**SKYBITDev3** (2023-09-30):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Any references to msg.sender in a deterministically deployed contract’s constructor are functionally not deterministically deployed

I’m not sure what you mean.

Though `msg.sender` in a contract’s constructor actually becomes the factory’s address if the contract is deployed via a factory such as the Deterministic Deployment Proxy. A user would realize this when they try it, and then may quickly fix it by replacing `msg.sender` with `tx.origin`.

I’ve just tried to deploy (via Nick’s Deterministic Deployment Proxy) an ERC20 contract that grants admin role to the account doing the deployment with this code in the constructor:

```auto
        _grantRole(DEFAULT_ADMIN_ROLE, tx.origin);
```

Here’s the output if `walletToUse = wallet1`:

```x
Using network: hardhat (31337), account: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 having 10000.0 of native currency, RPC url: undefined
Address of Arachnid's factory deployed keylessly: 0x4e59b44847b379578588920ca78fbf26c0b4956c
expected address using await walletToUse.call(txData): 0xd8d463e3a19f1ea97e8a62670054515f3f38b740
expected address using ethers.getCreate2Address: 0xd8D463e3a19F1eA97E8A62670054515f3f38B740
Now deploying TESTERC20 using Arachnid's factory...
TESTERC20 was deployed by 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Testing deployed contract by getting contract at address 0xd8D463e3a19F1eA97E8A62670054515f3f38B740:
0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 calling contract.point(): 10,5
0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 calling contract.privilegedFunction(): 1
```

Here’s the output if `walletToUse = wallet2`:

```x
Using network: hardhat (31337), account: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 having 10000.0 of native currency, RPC url: undefined
Address of Arachnid's factory deployed keylessly: 0x4e59b44847b379578588920ca78fbf26c0b4956c
expected address using await walletToUse.call(txData): 0xd8d463e3a19f1ea97e8a62670054515f3f38b740
expected address using ethers.getCreate2Address: 0xd8D463e3a19F1eA97E8A62670054515f3f38B740
Now deploying TESTERC20 using Arachnid's factory...
TESTERC20 was deployed by 0x70997970C51812dc3A010C7d01b50e0d17dc79C8
Testing deployed contract by getting contract at address 0xd8D463e3a19F1eA97E8A62670054515f3f38B740:
0x70997970C51812dc3A010C7d01b50e0d17dc79C8 calling contract.point(): 10,5
0x70997970C51812dc3A010C7d01b50e0d17dc79C8 calling contract.privilegedFunction(): 1
```

This shows that 2 *different* accounts were able to deploy the same contract to the same *deterministic* address (obtained before deployment using both `call` and [getCreate2Address](https://docs.ethers.org/v6/api/address/#getCreate2Address)), and each of them got admin privilege in the contract instance that they deployed. In reality, the owner of `wallet2` would have done it on a different blockchain, and the owner of `wallet1` may not have wanted `wallet2` to do the deployment to that same address and gain control of the contract on that other blockchain.

My updated version prevents this.

You can see my script at [Testing https://github.com/Arachnid/deterministic-deployment-proxy · GitHub](https://gist.github.com/SKYBITDev3/943f6389862d1ba68d02ddad72a8c208)

---

**MicahZoltu** (2023-09-30):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> I’m not sure what you mean.

I’m arguing that what you are doing is an anti-pattern.  Ideally, you create immutable contracts with no admin.  If an admin is necessary and you want to ensure it is a specific address no matter the blockchain and no matter who deploys it, then what you *should* be doing is something like this:

```auto
_grantRole(DEFAULT_ADMIN_ROLE, 0x70997970C51812dc3A010C7d01b50e0d17dc79C8)
```

This makes it very clear that the specified address is always the initial admin, regardless of who deploys the contract.  It is less prone to error, much easier to audit, and doesn’t depend on specialized deployment scripts being executed properly to get the desired result.

The idea here is to keep all of the desired functionality in the contract code, and make it impossible to introduce a security vulnerability due to a problem with the deployment scripts.

---

**SKYBITDev3** (2023-09-30):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Ideally, you create immutable contracts with no admin.

Privileged access is often necessary for contracts, depending on use cases. e.g. even a withdraw function to be able to take out tokens that were accidentally sent to the contract requires privileged access, otherwise without a withdraw function the tokens would be permanently stuck which could be very unfortunate for the sender if it was a large amount.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> you want to ensure it is a specific address no matter the blockchain and no matter who deploys it

It shouldn’t be possible for different accounts to deploy to the same address, especially for contracts that are designed with privileged access (e.g. admin).

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> This makes it very clear that the specified address is always the initial admin

Yes, hard-coding the address when granting admin role in the constructor gives clarity and certainty of who the admin will be, making it imposible for some other account to obtain privileged access.

But as the factory is used by the public, we can’t expect all contracts that use it to have addresses hard-coded like that in their constructors.

So my updated version offers protection for when someone uses the factory to deploy a contract that grants admin role to the deploying account. Hashing the deploying account’s address with the salt ensures that the contract addresses will be different for different accounts that deploy with exactly the same contract bytecode and salt.

---

**SKYBITDev3** (2023-10-08):

Here’s my script for testing my updated version: [Testing https://github.com/SKYBITDev3/deterministic-deployment-proxy · GitHub](https://gist.github.com/SKYBITDev3/57a385d1c7a067de22ab6e6a598bca7e#file-deployviafork-testerc20-js)

Here’s the ouput if account is `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266`:

```plaintext
Using network: hardhat (31337), account: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 having 10000.0 of native currency, RPC url: undefined
Address of factory deployed keylessly: 0xaf45f86eb0bbf0536fa770b699b806f22496d875
expected address using await walletToUse.call(txData): 0xe32dcd55a5daee6e5a34b046f759721c76e78291
expected address using ethers.getCreate2Address: 0xE32dcD55a5daEE6E5A34b046F759721C76E78291
Now deploying TESTERC20 using factory...
TESTERC20 was deployed by 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Testing deployed contract by getting contract at address 0xe32dcd55a5daee6e5a34b046f759721c76e78291:
0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 calling contract.point(): 10,5
0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 calling contract.privilegedFunction(): 1
```

Notice that the contract address is deployed to `0xE32dcD55a5daEE6E5A34b046F759721C76E78291`.

Here’s the ouput if account is `0x70997970C51812dc3A010C7d01b50e0d17dc79C8`:

```plaintext
Using network: hardhat (31337), account: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 having 10000.0 of native currency, RPC url: undefined
Address of factory deployed keylessly: 0xaf45f86eb0bbf0536fa770b699b806f22496d875
expected address using await walletToUse.call(txData): 0xbb1070bb427b517cb6ecfc2b1ef08ec413259277
expected address using ethers.getCreate2Address: 0xbb1070bb427B517Cb6Ecfc2B1ef08ec413259277
Now deploying TESTERC20 using factory...
TESTERC20 was deployed by 0x70997970C51812dc3A010C7d01b50e0d17dc79C8
Testing deployed contract by getting contract at address 0xbb1070bb427b517cb6ecfc2b1ef08ec413259277:
0x70997970C51812dc3A010C7d01b50e0d17dc79C8 calling contract.point(): 10,5
0x70997970C51812dc3A010C7d01b50e0d17dc79C8 calling contract.privilegedFunction(): 1
```

Notice that the contract address is deployed to `0xbb1070bb427B517Cb6Ecfc2B1ef08ec413259277`, which is different. This shows that with my updated version, a different account now cannot deploy the same contract with same user-provided salt to the same address.

My updated version hashes deploying account address with the user-provided salt, so the address of the contract can be deterministically calculated using `ethers` like this:

```js
ethers.getCreate2Address(addressOfFactory, ethers.solidityPackedKeccak256([ `address`, `bytes32` ], [ walletToUse.address, salt ]), ethers.keccak256(bytecodeOfContractWithArgs))
```

---

**SKYBITDev3** (2023-10-08):

These days though I’d suggest using the “CREATE3” method of deploying contracts instead of CREATE2, so that contract code no longer matters to the address.

I explore keyless deployment with the CREATE3 method in detail in this repository:



      [github.com](https://github.com/SKYBITDev3/SKYBIT-Keyless-Deployment)




  ![image](https://opengraph.githubassets.com/b03b0d94e8f66391ff41236914ae6331/SKYBITDev3/SKYBIT-Keyless-Deployment)



###



Deploy your smart contract to the same address on many blockchains (with fewer pitfalls)










I’ve also made a thread about it here: [Keyless contract deployment with CREATE3](https://ethereum-magicians.org/t/keyless-contract-deployment-with-create3/16025)

---

**MicahZoltu** (2023-10-09):

If your “owner” is a constructor argument then it will become part of the contract’s code and mean that the contract deployed with that specific owner exists at the same address on every blockchain (if using deterministic deployment proxy).

---

**SKYBITDev3** (2023-10-09):

Yes, with CREATE2, creation code affects deployment address. As constructor arguments are part of the creation code, different constructor arguments therefore lead to different deployment addresses. So there is no problem with front-running in that case. But we don’t have control over what code others have in their contracts.

As I’ve described before, a problematic case is when someone uses the deterministic deployment proxy to deploy a contract whose constructor grants privileged access to `tx.origin`. The original legitimate account that deploys it wouldn’t want other malicious accounts to deploy the same contract to the same address on other blockchains and become admin (by using the same salt, which can be easily found on etherscan etc.). My updated version which factors in the deploying account’s address prevents that.

Though now with the CREATE3 method, it’s even more important to factor in the deploying account’s address, because creation code no longer plays a role in address calculation. Glady, all CREATE3 factories that I’ve seen do so.

---

**MicahZoltu** (2023-10-10):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> a problematic case is when someone uses the deterministic deployment proxy to deploy a contract whose constructor grants privileged access to tx.origin.

The core of our disagreement seems to be on whether this is a ever a good idea.  I am of the belief that you should *never* being doing this.  There is no use case I can think of where it is the right choice compared to using a constructor parameter or hard-coded value.

If you really want, you could do `require(tx.origin == param1)` or something, but even that is a bad idea because anyone who is calling the factory with a contract wallet (e.g., Gnosis SAFE) will *not* want `tx.origin` to be the owner, the SAFE should be the owner (which is an intermediate address in the call chain, not `tx.origin` or `msg.sender`).

---

**SKYBITDev3** (2023-10-10):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> The core of our disagreement seems to be on whether this is a ever a good idea

We’re not disagreeing - I already agreed with you  that it’s much safer to hardcode the admin’s address in the constructor. I also suggested another option - to pass in the admin address into the constructor. So developers like you and I would do these instead.

But the issue isn’t about developers like you and I, it’s about everyone else. Factories like yours / Nick’s are used by the public to deploy their own contracts. As I had said a couple of times in different ways, *we can’t totally stop others* from writing code that grants privileged access to `msg.sender` / `tx.origin` in their own contracts. OpenZeppelin’s contract wizard even output such code that has `msg.sender` being granted admin role, minter role etc. in the constructor.

So as experienced technical professionals in this space, we can be on the other side by protecting others where we can from vulnerabilities in their code that they may not even be aware of. Making our products safer is good for the blockchain/web3/DeFi/crypto ecosystem & community. That’s what I’ve done in my update to your / Nick’s popular deterministic deployment proxy.

---

**dror** (2023-10-26):

I really don’t understand the purpose of hashing the caller: if you want the contract’s address to depend on `caller` + `initcode`, then simply call `CREATE2` …

The whole purpose of the deterministic deployer was to **remove** the dependency on the caller, and make the code depend on solely on the `initcode`

And `tx.origin` should be deprecated by now, and completely avoided. It breaks anything related to contract-based accounts, be it Safe or ERC4337 accounts or anything else.

---

**SKYBITDev3** (2023-10-29):

Hi [@dror](/u/dror), it’s nice to see you here (I’m looking forward to OpenGSN 3 full release).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> I really don’t understand the purpose of hashing the caller

It’s to prevent front-running. Let me explain using variables:

I’ve demonstrated that using Nick’s factory (“Deterministic Deployment Proxy”) (and Zoltu’s which has no salt (it becomes 0)) this happens:

1. Developer D1 uses the factory to deploy contract C using salt S to address A1 onto blockchain B1.
2. If developer D2 then uses the factory to deploy contract C using salt S onto blockchain B2, then the contract will also have address A1 on B2.

This would be a problem if C has code in the constructor that grants privileged access to whatever account did the deployment e.g. using `tx.origin`.

This is “front-running” because D2, who may not be a legitimate actor of the project that has the contract, takes over the address A1 on B2 and possibly taking ownership or control of the contract there, preventing legitimate actor D1 from ever being able to deploy contract C to A1.

By hashing `caller` with salt, this happens:

1. Developer D1 uses the factory to deploy contract C using salt S to address A2 onto blockchain B1.
2. If developer D2 then uses the factory to deploy contract C using salt S onto blockchain B2, then the contract will have address A3 on B2, i.e. an address different from A1.
3. If D1 deploys contract C using salt S onto B2, it will have address A2 as desired, same as on B1.

So front-running by D2 now can’t occur under any circumstance.

If you check other CREATE2 libraries / factories you’ll also find that they hash the caller with the salt. Here are some examples:



      [github.com](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/94697be8a3f0dfcd95dfb13ffbd39b5973f5c65d/contracts/utils/Create2.sol#L90)





####



```sol


1. // | bytecodeHash      |                                                        CCCCCCCCCCCCC...CC |
2. // | salt              |                                      BBBBBBBBBBBBB...BB                   |
3. // | deployer          | 000000...0000AAAAAAAAAAAAAAAAAAA...AA                                     |
4. // | 0xFF              |            FF                                                             |
5. // |-------------------|---------------------------------------------------------------------------|
6. // | memory            | 000000...00FFAAAAAAAAAAAAAAAAAAA...AABBBBBBBBBBBBB...BBCCCCCCCCCCCCC...CC |
7. // | keccak(start, 85) |            ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ |
8.
9. mstore(add(ptr, 0x40), bytecodeHash)
10. mstore(add(ptr, 0x20), salt)
11. mstore(ptr, deployer) // Right-aligned with 12 preceding garbage bytes
12. let start := add(ptr, 0x0b) // The hashed data starts at the final garbage byte which we will set to 0xff
13. mstore8(start, 0xff)
14. addr := keccak256(start, 85)
15. }
16. }
17. }


```












      [github.com](https://github.com/axelarnetwork/axelar-gmp-sdk-solidity/blob/fee271da28500034ad406e11194335c28628ce66/contracts/deploy/Deployer.sol#L35)





####



```sol


1. *
2. * - `bytecode` must not be empty.
3. * - `salt` must have not been used for `bytecode` already by the same `msg.sender`.
4. *
5. * @param bytecode The bytecode of the contract to be deployed
6. * @param salt A salt to influence the contract address
7. * @return deployedAddress_ The address of the deployed contract
8. */
9. // slither-disable-next-line locked-ether
10. function deploy(bytes memory bytecode, bytes32 salt) external payable returns (address deployedAddress_) {
11. bytes32 deploySalt = keccak256(abi.encode(msg.sender, salt));
12. deployedAddress_ = _deployedAddress(bytecode, deploySalt);
13.
14. if (msg.value > 0) {
15. // slither-disable-next-line unused-return
16. deployedAddress_.safeNativeTransfer(msg.value);
17. }
18.
19. deployedAddress_ = _deploy(bytecode, deploySalt);
20.
21. emit Deployed(deployedAddress_, msg.sender, salt, keccak256(bytecode));


```










![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> if you want the contract’s address to depend on caller + initcode, then simply call CREATE2 …

`CREATE2` doesn’t use `caller` to produce an address. It instead uses the address of the contract that calls it (which is the factory). See [Yul — Solidity 0.8.22 documentation](https://docs.soliditylang.org/en/v0.8.22/yul.html?highlight=create2#evm-dialect) where it says the address formula is `keccak256(0xff . this . s . keccak256(mem[p…(p+n)))` where “`this` is the current contract’s address”.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> The whole purpose of the deterministic deployer was to remove the dependency on the caller, and make the code depend on solely on the initcode

It doesn’t say that in [deterministic-deployment-proxy/README.md at master · Arachnid/deterministic-deployment-proxy · GitHub](https://github.com/Arachnid/deterministic-deployment-proxy/blob/master/README.md).

The purpose was to be able to deploy a contract to the same address on any EVM-based blockchain. `CREATE2` made it possible to determine and thus know the address of the contract before it’s deployed, so it was well-suited for that purpose.

So people have been using the factories in order to get the same address for their contracts on multiple blockchains. But they may not be aware of the front-running risk.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> tx.origin should be deprecated by now, and completely avoided. It breaks anything related to contract-based accounts, be it Safe or ERC4337 accounts or anything else.

As these factories are fully available to use by the public, we have no control over what developers write in the contracts that they deploy using these factories. But we should still try to keep them safe when they use our products.

---

**dror** (2023-10-31):

The purpose of CREATE2 was to create a deterministic address, that only depends on the actual deployed code.

It is possible to abuse it, and deploy arbitrary code into an address. It doesn’t mean that CREATE2 is bad - with proper usage, it works just great.

I’d say that using `tx.origin` or even `msg.sender` within a constructor is an abuse of the feature.

I think that if you want the “caller” or “owner” address be part of the target contract address - then you’d better pass it as a constructor parameter.

