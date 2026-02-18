---
source: magicians
topic_id: 15497
title: Transaction replay blanket ban is wrong - needed for keyless contract deployment
author: SKYBITDev3
date: "2023-08-19"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/transaction-replay-blanket-ban-is-wrong-needed-for-keyless-contract-deployment/15497
views: 1749
likes: 7
posts_count: 19
---

# Transaction replay blanket ban is wrong - needed for keyless contract deployment

We need a good way to deploy contracts to the same address on multiple blockchains.

The best practice is the keyless method as offered by [@MicahZoltu](/u/micahzoltu) and [@Arachnid](/u/arachnid) in [deterministic deployment proxy](https://github.com/Arachnid/deterministic-deployment-proxy) - broadcast a replayable deployment transaction that’s already signed by a manual signature from an account whose address is derived from that signature and transaction information.

The transaction data contains `chainId: 0`. We can’t write in the actual chainId of the blockchain that we want to deploy the contract onto because that would result in a different deployment address on each blockchain.

Since the [ChainId enforcement](https://blog.ethereum.org/2021/03/03/geth-v1-10-0#chainid-enforcement) by default in Geth, more node providers have been rejecting such replayable deployment transactions, with error “ProviderError: only replay-protected (EIP-155) transactions allowed over RPC”. Geth offers `--rpc.allow-unprotected-txs` comamnd line option for running the node but they say “this is a temporary mechanism that will be removed long term”.

There should have been acknowledgement that there are valid non-malicious use cases of transaction replay. But it instead they’ve narrow-mindedly done a blanket ban.

We should push back against this. I’ve expressed my arguments in a new issue at go-ethereum: [Allow replay of transactions that are designed to be replayable](https://github.com/ethereum/go-ethereum/issues/27935).

Maybe there could be a chainId that would indicate that the transaction is meant to be replayable so they should be let through, e.g. `-1`. Or maybe introduce a new variable in the transaction data e.g. `replayable: true`. Maybe add the condition that it’s a deployment transaction.

It’s increasingly becoming a multi-blockchain world, so there will be more multi- and cross-chain applications which would benefit from having contracts at the same address on multiple blockchains for simplicity and elegance, reducing coding effort. So this issue is likely to grow in prominence.

What thoughts and ideas do you guys here have?

## Replies

**SKYBITDev3** (2023-08-20):

[EIP-3788](https://eips.ethereum.org/EIPS/eip-3788) says:

> Per EIP-155 a transaction with a chainId = 0 is considered to be a valid transaction. This was a feature to offer developers the ability to sumbit replayable transactions across different chains.

If that’s correct then EIP-3788 is the real cuprit that has blocked transaction replay.

In any case, with chain ID enforcement, EIPs that require contracts to be deployed for public use would no longer be implementable, e.g. singleton contracts in [EIP-1820](https://eips.ethereum.org/EIPS/eip-1820) and [EIP-2429](https://gitlab.com/status-im/docs/EIPs/blob/secret-multisig-recovery/EIPS/eip-2429.md), and factory contract in [EIP-4337](https://eips.ethereum.org/EIPS/eip-4337). EIP-1820 itself outlines the [keyless deployment method](https://eips.ethereum.org/EIPS/eip-1820#deployment-transaction) using an already-signed deployment transaction (with no `chainId` or `chainId: 0`) that would no longer work.

---

**omnus** (2023-08-21):

Does using create2 from a deployer factory offer any hope?

It requires the factory to exist at the same address on multiple chains, but there are examples out there (e.g. the fine ImmutableCreate2Factory from [@0age](/u/0age) `0x0000000000ffe8b47b3e2130213b802212439497`)

---

**SKYBITDev3** (2023-08-21):

But who owns / controls the factory?

If people use a factory that wasn’t deployed via the keyless deployment method then, going forward, they become dependent on the holder of the private key that was used to deploy the factory. e.g. if a new blockchain appears that you want to deploy some contract onto and you want it to have the same address as your contract on the other blockchains, you’d have to ask/beg the original deployer of the factory to get his factory contract onto that new blockchain so that you can use it. He may not even be contactable anymore, or may not agree.

With the keyless deployment method, anyone can replay the transaction as the factory contract will still get the same address, and the factory becomes a true public good / service that nobody owns or controls, like [@Arachnid](/u/arachnid)’s / [@MicahZoltu](/u/micahzoltu)’s CREATE2 deterministic-deployment-proxy.

---

**SKYBITDev3** (2023-08-21):

I’ve checked the contracts of a few multi-blockchain projects: Axelar, OpenGSN, Uniswap

Most of their contracts were deployed on many blockchains using EOAs by trying to synchronizing nonce, but they all eventually failed to maintain same contract addresses, and instead only some contracts have same addresses across blockchains.

Uniswap learned about CREATE2 only this year it appears. They deployed their most recent contract (Permit2) using Arachnid’s CREATE2 factory: [Document deterministic CREATE2 deployments · Issue #782 · foundry-rs/book · GitHub](https://github.com/foundry-rs/book/issues/782#issue-1548824094). Better late than never!

That factory is the best CREATE2 factory for everyone to use because anyone can deploy the factory contract (via keyless deployment) and it’ll end up at the same address as on the other blockchains. It’s now even included in Foundry’s Anvil: [feat(`anvil`): Include `CREATE2` deployer by default on new instances by Evalir · Pull Request #5391 · foundry-rs/foundry · GitHub](https://github.com/foundry-rs/foundry/pull/5391)

But it may no longer be possible to deploy the factory contract onto new blockchains that arise in future because of chainId enforcement, as it has made keyless deployment difficult or impossible.

What options do we have left now to do keyless deployment? Set up our own nodes with `--rpc.allow-unprotected-txs` for every new blockchain that we want to use?

Even though Arachnid’s / Zoltu’s factory contracts are the best CREATE2 factories to use, we may want to create newer versions of factory contracts e.g. that have extra features (e.g. execute `initialze` function), and deploy them keylessly so that anyone else could deploy them onto other blockchains to the same address. So we really need ways to have such replayable deployment transactions accepted.

Please share your ideas, guys.

---

**Mani-T** (2023-08-22):

The suggestion of introducing a new ChainID or a new variable in transaction data to indicate replayable transactions is a potential solution. But I wonder that are there alternatives that could achieve the desired outcome of replayable deployment transactions?

---

**MicahZoltu** (2023-08-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> If that’s correct then EIP-3788 is the real cuprit that has blocked transaction replay.

This EIP is stagnant, it never made it to final.  Essentially it is just a proposal that didn’t get any adoption.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> EIP-3788 says:
>
>
>
> Per EIP-155 a transaction with a chainId = 0 is considered to be a valid transaction. This was a feature to offer developers the ability to sumbit replayable transactions across different chains.

The current EIP-155 text doesn’t mention chain ID 0 anywhere in it.  Someone should dig through the history as I did do a pretty significant rewording of the EIP a while back to make it more readable, and it is possible that the chain ID 0 stuff was lost in what was supposed to be a non-normative change to prose text.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> Even though Arachnid’s / Zoltu’s factory contracts are the best CREATE2 factories to use, we may want to create newer versions of factory contracts e.g. that have extra features (e.g. execute initialze function), and deploy them keylessly so that anyone else could deploy them onto other blockchains to the same address. So we really need ways to have such replayable deployment transactions accepted.

These both execute the constructor like a normal deployment would.  No need to have them *also* call an initialize function (why not just put code in the constructor if you want it called on deployment?).

I’m not sure what you mean by keyless deployment if you aren’t referring to the mechanism by which both of these were deployed.  Both can be deployed to any blockchain that supports replayable transactions and has a gas price under 100 nanoeth/gas.  Some blockchains just deploy these contracts as precompiles, that way they support deterministic contract deployments but they don’t have to support replayable transactions.

Generally speaking though, I do agree that replayable transactions have some value, but most of that value is lost when you have deterministic deployment proxies on the blockchain in question.  Are there other use cases besides deterministic address contract deployment that are only possible with replayable transactions?

---

**SKYBITDev3** (2023-08-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> These both execute the constructor like a normal deployment would. No need to have them also call an initialize function (why not just put code in the constructor if you want it called on deployment?).

There can be reasons for having a separate initialize function, e.g. see Axelar’s CREATE2 factory called [Constant Address Deployer](https://docs.axelar.dev/dev/general-message-passing/solidity-utilities#constant-address-deployer) which has `deployAndInit` “in case you need constructor arguments that are not constant across chains, as different constructor arguments result in different bytecodes”.

But my point was that your CREATE2 factory (“deterministic-deployment-proxy”), although being great work and that it’s now deployed on so many blockchains, *it shouldn’t have to be the only one we can use ever*. You said something similar a few years ago, i.e. users are free to create and use their own or other factory (“deployer”):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png)[ERC-2470: Singleton Factory](https://ethereum-magicians.org/t/erc-2470-singleton-factory/3933/32)

> The reason I didn’t create an EIP is because I don’t think there is significant value in standardizing it. Anyone can deploy with whatever mechanisms they want. I can use my deployer and you can use your deployer and everything works just as well as if we both used the same deployer.

Some may want to create or use some other factory that works differently. But in order to deploy the factory via keyless deployment, they need to replay a deployment transaction. With nodes increasingly forbidding transaction replay, it’s becoming almost impossible.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Some blockchains just deploy these contracts as precompiles

There will be newer factories that people want to get onto a blockchain and start using. Hoping that a blockchain will deploy one as a precompile isn’t realistic.

---

**SKYBITDev3** (2023-08-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Are there other use cases besides deterministic address contract deployment that are only possible with replayable transactions?

Although the best way to have contracts at the same addresses on multiple blockchains is by using a factory (that was deployed keylessly), some may want to skip using a factory (there may not be any CREATE2 or “CREATE3” factory on the blockchain) - they may just have one contract to deploy to the same address on multiple blockchains, and want to use the keyless deployment method because it doesn’t require safeguarding private keys. Keyless deployment requires transaction replay.

---

**SKYBITDev3** (2023-08-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mani-t/48/10103_2.png) Mani-T:

> introducing a new ChainID or a new variable in transaction data to indicate replayable transactions is a potential solution

A new variable in transaction data (e.g. `replayable: true` or `replayable: 1`) would of course be better so that `chainId` is only ever about the blockchain. Wallet apps wouldn’t add `replayable`, so those transactions wouldn’t be replayable, which is OK. Only developers would create transactions that have `replayable`.

But yes, we welcome other ideas in case there could be some better ways.

---

**omnus** (2023-08-31):

The contract in this instance is ownerless, with no privileged roles.

But I get your point! If there are new chains to support you are reliant on the original deployer to come to the party!

---

**MicahZoltu** (2023-09-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> There can be reasons for having a separate initialize function, e.g. see Axelar’s CREATE2 factory called Constant Address Deployer which has deployAndInit “in case you need constructor arguments that are not constant across chains, as different constructor arguments result in different bytecodes”.

I don’t recommend using a deterministic deployer for this sort of thing as someone can front-run your deployment but with different initializer parameters.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> it shouldn’t have to be the only one we can use ever. You said something similar a few years ago, i.e. users are free to create and use their own or other factory (“deployer”):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> Some may want to create or use some other factory that works differently. But in order to deploy the factory via keyless deployment, they need to replay a deployment transaction.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> There will be newer factories that people want to get onto a blockchain and start using.

Any chain that has deterministic-deployment-proxy deployed to it can deploy a new proxy with different features at a deterministic address.  Really, Nick’s proxy *should* have been deployed with my proxy (which was already deployed when he deployed his) rather than using a constructed signature.

---

**SKYBITDev3** (2023-09-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Nick’s proxy should have been deployed with my proxy

If such piggy-backing was the case and someone deployed their contract via Nick’s factory (or “proxy” or “deployer”) to get the same address on a few blockchains, then one day a **new blockchain** comes along that she wants to deploy the same contract onto, in order to get the same address as on the other blockchains these steps would need to occur on the new blockchain:

1. Your factory deployed keylessly
2. Nick’s factory deployed via your factory
3. She deploys her contract via Nick’s factory

So there would have to be an extra step.

I wrote a script to see the addresses if there was such piggy-backing. Here is the output:

```
Using network: hardhat (31337), account: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 having 10000.0 of native currency, RPC url: undefined
Address of Zoltu's factory deployed keylessly: 0x7A0D94F55792C434d74a40883C6ed8545E406D12
Address of Lock deployed via Zoltu's factory: 0x4e39ee0cdb6041dc54bcbe780113e3becee46aae
Attached to Lock at 0x4e39ee0cdb6041dc54bcbe780113e3becee46aae
lock.unlockTime(): 8888888888
Address of Arachnid's factory deployed keylessly: 0x4e59b44847b379578588920ca78fbf26c0b4956c
Address of Lock deployed via Arachnid's factory: 0x3e46d046d9ce3fa2df49732cb6bf2b71b0f89dfc
Attached to Lock at 0x3e46d046d9ce3fa2df49732cb6bf2b71b0f89dfc
lock.unlockTime(): 8888888888
Address of Arachnid's factory deployed via Zoltu's factory: "0x7205927be4d1aea7dee1bfb3332244c8b3d0f438"
Address of Lock deployed via Arachnid's factory that was deployed via Zoltu's factory: 0xb18332386d90004182e40fb6b72ef77650fcae01
Attached to Lock at 0xb18332386d90004182e40fb6b72ef77650fcae01
lock.unlockTime(): 8888888888
Done in 8.98s.
```

See the script code at: [Zoltu's factory vs Arachnid's factory vs Arachnid's factory deployed via Zoltu's factory · GitHub](https://gist.github.com/SKYBITDev3/eb8c5562c05b9011fc96e9fb68daaf1f)

So the piggy-backing resulted in contract address `0xb18332386d90004182e40fb6b72ef77650fcae01`, which is different from the addresses from the other cases.

---

**SKYBITDev3** (2023-09-04):

Also, normally the address of the account that uses a CREATE2 factory affects the deployment address, right? If so, then the same account that deployed Nick’s factory via your factory on the other blockchains would need to do step 2 above on the new blockchain, otherwise addresses would become different.

However, when running my script with a different calling account (`walletToUse = wallet2`, so account address becomes `0x70997970C51812dc3A010C7d01b50e0d17dc79C8`) it didn’t make a difference to the addresses:

```
Using network: hardhat (31337), account: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 having 10000.0 of native currency, RPC url: undefined
Address of Zoltu's factory deployed keylessly: 0x7A0D94F55792C434d74a40883C6ed8545E406D12
Address of Lock deployed via Zoltu's factory: 0x4e39ee0cdb6041dc54bcbe780113e3becee46aae
Attached to Lock at 0x4e39ee0cdb6041dc54bcbe780113e3becee46aae
lock.unlockTime(): 8888888888
Address of Arachnid's factory deployed keylessly: 0x4e59b44847b379578588920ca78fbf26c0b4956c
Address of Lock deployed via Arachnid's factory: 0x3e46d046d9ce3fa2df49732cb6bf2b71b0f89dfc
Attached to Lock at 0x3e46d046d9ce3fa2df49732cb6bf2b71b0f89dfc
lock.unlockTime(): 8888888888
Address of Arachnid's factory deployed via Zoltu's factory: "0x7205927be4d1aea7dee1bfb3332244c8b3d0f438"
Address of Lock deployed via Arachnid's factory that was deployed via Zoltu's factory: 0xb18332386d90004182e40fb6b72ef77650fcae01
Attached to Lock at 0xb18332386d90004182e40fb6b72ef77650fcae01
lock.unlockTime(): 8888888888
Done in 8.32s.
```

If calling account doesn’t affect addresses then wouldn’t there be issues when your factory is used by different people to deploy common contracts like [ERC1967Proxy](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/ERC1967/ERC1967Proxy.sol)? If more than one person tried to deploy the same contract (same source code and compiler settings, therefore having same bytecode) then the target deployment address for each would be the same, and only the first would succeed.

Though at least Nick added a salt variable to his factory, which would make it possible for the different people to get different addresses for the same contract with same compiler settings.

---

**SKYBITDev3** (2023-09-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I don’t recommend using a deterministic deployer for this sort of thing as someone can front-run your deployment but with different initializer parameters.

I was going to say that other people would have different account addresses, resulting in different contract deployment addresses, but it seems with your factory the address of the account using the factory doesn’t affect the deployment address as I’ve described just above. Please confirm if that’s true.

---

**MicahZoltu** (2023-09-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> So the piggy-backing resulted in contract address 0xb18332386d90004182e40fb6b72ef77650fcae01, which is different from the addresses from the other cases.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> Also, normally the address of the account that uses a CREATE2 factory affects the deployment address, right? If so, then the same account that deployed Nick’s factory via your factory on the other blockchains would need to do step 2 above on the new blockchain, otherwise addresses would become different.

Yes, keyless deployment will result in a different address than deterministic-proxy deployment.  This is expected behavior, and not a problem as I see it.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> If calling account doesn’t affect addresses then wouldn’t there be issues when your factory is used by different people to deploy common contracts like ERC1967Proxy? If more than one person tried to deploy the same contract (same source code and compiler settings, therefore having same bytecode) then the target deployment address for each would be the same, and only the first would succeed.
>
>
> Though at least Nick added a salt variable to his factory, which would make it possible for the different people to get different addresses for the same contract with same compiler settings.

The idea with my deterministic deployment proxy is to deploy singletons.  If you have some code and you want to make sure that code exists at the same location on every blockchain, then you would use deterministic deployment proxy.  If you want to be able to deploy multiple copies of that code to multiple well-known addresses, then Nick’s fork of the proxy that adds support for salting would achieve that goal.

If you want to deploy with different parameters, then I don’t think either of our tools nor would keyless deployment work.  The problem is that you may deploy to chain A with some set of parameters, but then a malicious actor would deploy to chain B with *incorrect* parameters at the same address and you cannot fix it.  For deterministic addresses to be meaningful, you need to make it so that the deployment process is identical for every chain so a malicious actor cannot front-run your deployment to a particular chain and do bad things.  This is why the “Deterministic Deploy With Init Function” is a really bad idea, because someone can front-run your initialization call.  It also gives end-users no guarantee that the contract on a particular chain was initialized with the proper values.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/73ab20/48.png) SKYBITDev3:

> I was going to say that other people would have different account addresses, resulting in different contract deployment addresses, but it seems with your factory the address of the account using the factory doesn’t affect the deployment address as I’ve described just above. Please confirm if that’s true.

This is correct.  The address of a contract deployed by Deterministic Deployment Proxy is a function of the code being deployed.  With Nick’s fork, it is a function of the code being deployed and the provided salt.  The deployer’s address doesn’t play any role in the contract’s address.

---

**sbacha** (2023-09-29):

We would be interested in supporting this in the context of a new RPC method meant for deployments.  This would be part of an additional RPC method for recovering from network connection issues, https://github.com/manifoldfinance/eip-proposal-rpc/blob/master/eth_getTransactionBySenderAndNonce.md

Something like this: `eth_sendUncheckedTransaction`

Same as `eth_sendRawTransaction`, but never checks nonce or gas price of the transaction. This can be used to broadcast transactions with faster response. You have to make sure yourself the transaction is valid.

---

**SKYBITDev3** (2023-09-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> never checks nonce or gas price of the transaction

It’s the **chain ID** check that is the issue described in this thread - when we create a transaction that we want to replay on many blockchains, we set chain ID to 0. But many nodes these days reject transactions if chain ID is 0.

---

**SKYBITDev3** (2023-09-29):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> This is why the “Deterministic Deploy With Init Function” is a really bad idea

I agree with you.

Though the point I was trying to make is that there could updated versions of the Deterministic Deployment Proxy (e.g. one that I’ve made) - the old one from 4y ago by you / Nick shouldn’t have to be the only one that ever exists.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> The address of a contract deployed by Deterministic Deployment Proxy is a function of the code being deployed. With Nick’s fork, it is a function of the code being deployed and the provided salt. The deployer’s address doesn’t play any role in the contract’s address.

For general purpose contract deployment, the deployer’s address should be included to prevent front-running by others, so I’ve made an updated version which I’ve described in [Updated MicahZoltu's / Arachnid's Deterministic Deployment Proxy](https://ethereum-magicians.org/t/updated-micahzoltus-arachnids-deterministic-deployment-proxy/15947)

