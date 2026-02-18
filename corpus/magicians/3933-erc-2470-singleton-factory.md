---
source: magicians
topic_id: 3933
title: "ERC-2470: Singleton Factory"
author: 3esmit
date: "2020-01-15"
category: ERCs
tags: [create2, erc-2470]
url: https://ethereum-magicians.org/t/erc-2470-singleton-factory/3933
views: 7457
likes: 15
posts_count: 52
---

# ERC-2470: Singleton Factory

[github.com](https://github.com/status-im/EIPs/blob/singleton-factory/EIPS/eip-2470.md)





####



```md
---
eip: 2470
title: Singleton Factory
author: Ricardo Guilherme Schmidt (@3esmit)
discussions-to: https://ethereum-magicians.org/t/erc-2470-singleton-factory/3933
status: Draft
type: Standards Track
category: ERC
created: 15-01-2020
requires: 1014
---

## Simple Summary

Some DApps needs one, and only one, instance of an contract, which have the same address on any chain.

A permissionless factory for deploy of keyless deterministic contracts addresses based on its bytecode.

## Abstract

```

  This file has been truncated. [show original](https://github.com/status-im/EIPs/blob/singleton-factory/EIPS/eip-2470.md)










I am writing a project that needs a singleton, I seen that there was no standard about it so I am creating one.

The idea is that a factory can create one deterministic address per byte-code, so everyone knows what to use and it can be deployed in any chain.

This factory would be using also nick’s method, so it would also be deployable in any chain, which then would always generate the same addresses for that bytecode, regardless of chain.

Any suggestions?

## Replies

**Amxx** (2020-01-16):

This already exist:

factory.kistune-wallet.eth (on mainnet)

0xFaC100450Af66d838250EA25a389D8Cd09062629 (on all networks)

Available on mainnet, ropsten, rinkeby, goerli, kovan, lukso, …

---

**Amxx** (2020-01-16):

Salt is needed for people to deploy multiple instance of a contract that is only differenciated through initialisation (like proxies)

---

**Amxx** (2020-01-16):

Also, have a look at my code, the `callback` mechanism is really important for some contracts. For example, ownable contracts will be owned by the factory, an we need the user to tell the factory to transfer ownership to him.

---

**3esmit** (2020-01-16):

Hi, thanks for the interest in this EIP. I presume you want to join this effort?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> This already exist:

Does it exists as an EIP/ERC? I searched it there and didnt founded any standarization on that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> factory.kistune-wallet.eth (on mainnet)
> 0xFaC100450Af66d838250EA25a389D8Cd09062629 (on all networks)

I noticed that you hold the private key of the address that deploys `0xFaC100450Af66d838250EA25a389D8Cd09062629`, which is not ideal, for 2470 we want to use keyless.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Salt is needed for people to deploy multiple instance of a contract that is only differenciated through initialisation (like proxies)

I think that if the instance is being deployed, the unique address would be obtained by the constructor parameters.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Also, have a look at my code, the callback mechanism is really important for some contracts. For example, ownable contracts will be owned by the factory, an we need the user to tell the factory to transfer ownership to him.

That would work, but IMO this is not ideal, because is possible to encode the correct behavior into the constructor. If the contract is intended to be deployed and have its owner to the factory caller, it should be handled by the initialization data.

if you use this design, it won’t be deterministic anymore based only on initialization condition.

Contracts that are constructed by the Singleton Factory MUST not use `msg.sender` as `Owner` or `Controller`, instead they MUST be designed to accept the “Controller” or “Owner” address into it’s constructor, so their initialization data (including constructor data) defines the deterministic address, not salt. Otherwise, if the factory allowed to send a message to the created contract as part of initialization, but without changing the resulting address, the same address could be initialized with different initialization state, therefore not guaranteeing the “Singleton” Property.

---

**3esmit** (2020-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> ownable contracts will be owned by the factory, an we need the user to tell the factory to transfer ownership to him.

For example, using this is not correct:

```solidity
contract BadSingletonExample {
    address public owner = msg.sender;

    function setOwner(address _owner) external {
        owner = _owner;
    }
}
```

If in the case we use GenericFactory.sol to create the above contract, I could deploy it on different chains the same address with different owner. Thats why I am against this for the “SingletonFactory” EIP.

The equivalent version would be this:

```solidity
contract SingletonExample {
    address public owner;

    constructor(address _owner) public {
        owner = _owner;
    }

    function setOwner(address _owner) external {
        owner = _owner;
    }
}
```

and the intended owner would be encoded in the initialization code (not in the `msg.sender`).

Some contracts wont work in SingletonFactory, and this is intended by design, using msg.sender in contract constructor should only be used to read the factory address (if this have any use).

However they just need to do a small change (replace msg.sender in constructor by parameter) and it would work better.

If you really need to use msg.sender with SingletonFactory to decide the owner, you could wrap another factory around and use `SingletonFactory.deploy(abi.encode(Contract.creationCode, msg.sender), _salt);`

---

**Amxx** (2020-01-16):

I never thought it was worth being an ERC. It’s just a small hack I made one night (took me less then 30min) … But if that is what it takes to have people be aware of it and not reinvent the weel then so be it.

Your approach is only focussed on singleton, so you it makes sens to you to have a fixed salt. I wanted to support any contract. My first objective was to help developper deploy any contract at the same address on multiple blockchain… And if you want singletons, then just use my approach with salt = 0. You could even build a singleton deployer that, given the contract code, calls my factory with salt = 0. And you could deploy the singleton deployer using my factory (and salt = 0) to make sure it has the same address on all blockchain.

Same goes for the callback mechanism. I understand that if you want to singleton, you should not use it, and you should build your contract in a way that prevents that. But some people could just want to use a “standard” contract that inherits from openZeppelin’s ownable, without having to modify and recompile the code, and deploy it on multiple blockchain at the same address. It’s just more flexible.

→ Now that I think about it, I could have used `keccak256(encode.packed(_salt, _callback)` as a salt. Would have ensure singleton even with callbacks. I’m putting that in the v2

It’s true that I own the private key. I was thinking that if I gave the private key away, trools could do useless transaction with it on some blockchain, preventing the factory from ever being deployed at the right address to these blockchain. I’m thinking about what would be the best way to give signed transaction for any chainid, without disclosing the private key.

---

**3esmit** (2020-01-17):

Hey,

It needs to be an ERC for properly being reused in other ERCs.

I added salt to help deploy of vanity addresses, I did this because it is fairly easy to change a bit in comments and it changes the hash included in the bytecode, so why not make things easier, then harder, when there is no reason for.

Salt keeps singleton, as is fixed behavior, after deploy, nothing is done, no variables, all fixed - if the same address - the same (initial) behavior.

- I don’t understand why I want to deploy it on chainId 2470? Why not using pre EIP-155, so its valid on any chain?
- If you want to be really generic on your contract you should use msg.value at create2 value, instead of 0, and obviously also marking the deploy function as payable.
- You should not give the private key, you should have used a keyless method, which not even you have the key. Learn more here https://medium.com/@weka/how-to-send-ether-to-11-440-people-187e332566b7 Nick helped with DAO rescue where he neede to proof he didnt owned the private key of the addresses, but still deploy a contract from there. So he did that. This was used as basis for EIP-2470, EIP-1820 and EIP-820. So I need that keyless deploy for EIP-2429, but then instead of making it once just for that, I made EIP-2470 for using in EIP-2429 or any other EIPs, all will inherit the keyless property of 2470 (anyone can deploy on anychain and noone knows the private key).

If you see, in ERC2470 the r,s of EC deploy signature are both `0x247000...0002470`… Impossible for me to know what PK creates a signature to deploy that content with this `r`,`s` values…

---

**Amxx** (2020-01-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> I don’t understand why I want to deploy it on chainId 2470? Why not using pre EIP-155, so its valid on any chain?

Sorry I missunderstood your past question. I’ll have to check pre EIP-155 has I am not familiar with it

> If you want to be really generic on your contract you should use msg.value at create2 value, instead of 0, and obviously also marking the deploy function as payable.

That is a really big no! The origin of this factoryis the deployment of musisig wallets/proxys. I wanted to make sure you can have the same multisig at the same address on multiple network to avoid the issue of funds sent to a adress that is valid on another network but not on this. If you put msg.sender you either:

- prevent semone else to deploy a wallet at an address were funds have already been sent to from deploying it when he needs to interact with.
- Trust someone will do the deployment and give it the possibility of sensoring the deployment.

The payable part if a really good idea!

> You should not give the private key, you should have used a keyless method, which not even you have the key. Learn more here How to send Ether to 11,440 people | by Nick Johnson | Medium Nick helped with DAO rescue where he neede to proof he didnt owned the private key of the addresses, but still deploy a contract from there. So he did that. This was used as basis for EIP-2470, EIP-1820 and EIP-820. So I need that keyless deploy for EIP-2429, but then instead of making it once just for that, I made EIP-2470 for using in EIP-2429 or any other EIPs, all will inherit the keyless property of 2470 (anyone can deploy on anychain and noone knows the private key).

I’ll have to check that out. The only method I know is to prepare the transaction, and then put a random value in the signature, resulting in a random sender that you have to fund to do the deployment. This is great for a single blockchain, but I don’t know how to apply that method in a way that will produce the same address on all blockchains. I’ll definitelly check that out.

---

**3esmit** (2020-01-18):

> That is a really big no!

What?

> I wanted to make sure you can have the same multisig at the same address on multiple network to avoid the issue of funds sent to a adress that is valid on another network but not on this.

GerenricFactory allows Bob to initialize and set themsselves as owners of the wallet at chain 1, and allows Alice to initialize and set themselves as owners of the same wallet of Bob, but at chain id 2.

Isn’t this bad?

> The payable part if a really good idea!

Maybe for Generic Factory, but not for Singleton Factory, as the msg.value can interfere on how the contract is initialized.

> This is great for a single blockchain, but I don’t know how to apply that method in a way that will produce the same address on all blockchains.

I can assure it work in all blockchains, with the exact same signature, see:

https://ropsten.etherscan.io/address/0x247087a9061f30de86a9E63B68B4e7d8ebf4A51a

https://rinkeby.etherscan.io/address/0x247087a9061f30de86a9E63B68B4e7d8ebf4A51a

---

**Amxx** (2020-01-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> GerenricFactory allows Bob to initialize and set themsselves as owners of the wallet at chain 1, and allows Alice to initialize and set themselves as owners of the same wallet of Bob, but at chain id 2.
> Isn’t this bad?

This is bad. And it’s not possible if the initialisation is part of the constructor (which it is for my multisigs). It can only happen if the owner selection is part of the callback, which I’ve corrected in version 2 : https://etherscan.io/address/0xfac2006166c5b88a9e0a320e933a75813ccc7ecd#code

> Maybe for Generic Factory, but not for Singleton Factory, as the msg.value can interfere on how the contract is initialized.

If you include the msg.value in the way the salt is generate then there is no risk. Also, ether can be sent to the address BEFORE the contract is created, so this kind of interferance will always be possible.

I’m still convinced a well designed generic factory is much more powerfull then a singleton factory.

> I can assure it work in all blockchains, with the exact same signature, see:

I’ve just read about EIP155, I didn’t know there was something before that. I though I had read the yellowpaper carefully but I must have missed it.

It there any tooling for creating this kind of transaction?

I think this kind of deployment is really cool, but it means the sender address (and thus the factory address) is directly link to the deploy bytecode:

- We should really focus on one exact code for the factory + on exact compiler version to fix the transaction once and for all.
- Knowing this is possible, do we need singleton factory at all? The approach used to deploy the factory sounds easy enough that it can be used for any singleton.

---

**3esmit** (2020-01-19):

First of all, you should stop calling this “callback”, because its not a callback, is an “additional call” to the freshly created contract.

I don’t think that the design you suggest is good, because the constructor is the “embedded additional call” of ethereum while creating a smart contract.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> But some people could just want to use a “standard” contract that inherits from openZeppelin’s ownable, without having to modify and recompile the code, and deploy it on multiple blockchain at the same address. It’s just more flexible.

The account contracts that you mention uses msg.sender in constructor to set owner, are therefore not designed for factories in general. OpenZeppelin should provide contracts for being used with factories, not using additional calls, this is bad design.

If a developer want to use EIP2470, they must be aware of what they are coding.

Also, you don’t want to give the responsibility to users that have no idea of solidity to deploy their own account contracts - this is clear to go wrong. Users would be scared away of having to decide in account contracts and factories and standards,

I don’t see the use case for that, seems like you pushing forward a legacy support for nonexistent use case?

So I am against adding additional complexity in this standard to support smart contract not designed to be used with factory, the additional complexity don’t bring any benefit and this is not a Backwards Compatibility issue, so including this would not be an improvement, as its only giving option to developers keep using a bad design.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> It’s just more flexible.

If you give me an use case that is not possible to use the constructor, then I would reconsider it for this EIP.

---

**3esmit** (2020-01-19):

BTW, your GenericFactory is a type of Singleton, so you can use EIP-2470 to inherit the keyless property. if you want a GenericFactory that always have the same address in any ethereum chain possible and no one controls the keys to this process (becoming part of ethereum infra), you can simply say the bytecode of its deploy and then point it to EIP-2470.

Or you could follow Nick method and go to all this effort yourself…

---

**Amxx** (2020-01-19):

You are saying openzeppelin’s contract are bad by design, and dev should not use them and rather implement something of their own with the right pattern. This is something have been fighting for years. Feature duplication is causing bugs that this community cannot afford.

The “construct then initialize” pattern is an old one that has been working long before solidity was even here. Sure it’s not perfect. Sure we would rather not have to rely on it. But i’ll rather make sure to include the possibility then dictate how people should refactor their code.

I’ve been pushing for [“initialized through constructor” proxies](https://github.com/Amxx/KitsuneWallet-ERC1836/blob/master/kitsune-contracts/contracts/proxy/KitsuneProxy.sol) but most people use the regular zos proxies that are initialized after the fact. Upgradeability is (IMO) a great feature and making the most used framework for it not compatible would (again IMO) not be the way to go.

And yes, solidity developers have to be carefull of what they do. I don’t see it changing anytime soon

---

**Amxx** (2020-01-19):

You can do you very limited singleton factory, and then expect people to use it to deploy more generic factories. And I’ll be the first one to admit that it’s unlikelly we will build the perfect factory on the first try. But I think it’s forth it to try get as much features (that do not compromise security) in the “root” factory.

I also think it would be nice to have additional opinions beside ours.

---

**Amxx** (2020-01-19):

Also, I’m still convinced this doesn’t need to be an ERC. we obviously have different visions of what this could/should be. What usually happens is that a bunch of project build their own solution, use them, share the code/address, and then a some point some actors like openzeppelin makes a mix of all existing solution that answers most people needs and becomes the de-facto standard.

I believe this is a much better process then arguing over potential usecases.

---

**3esmit** (2020-01-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> You are saying openzeppelin’s contract are bad by design,

Not the contract themselves, but using it with factory that then set the owner. This is not a really huge problem, but is inherently a bad design as its waste of gas and there is a better way of doing it.

If they are supposed to be used with a factory, they should have been designed for that.

> But i’ll rather make sure to include the possibility then dictate how people should refactor their code.

That’s the case, I don’t want to include the possibility of doing bad things, and if they want to use a factory, they should refactor it - or use some factory who don’t care.

> You can do you very limited singleton factory, and then expect people to use it to deploy more generic factories.

Yes, that can be a point, as I mentioned, an factory that support msg.value or other behavior might be interesting for you or other. In the case of account contracts, a singleton factory could be used, but might not be the best behavior for it, another factory that controls the deploy based on a signed message would be wiser, so we dont allow anyone init other people accounts…

> still convinced this doesn’t need to be an ERC

I need it as ERC because it will be used in other ERCs.

---

**Amxx** (2020-01-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> still convinced this doesn’t need to be an ERC

I need it as ERC because it will be used in other ERCs.

Fair point!

- I’ve seen you added a salt to the EIP
- The deploy transaction includes 100Gwei. Do we really need such a high value? I get it’s a one-time thing but it still feels unecessarily high.

---

**3esmit** (2020-01-20):

> salt

Yes, I enabled salt because it didn’t made sense to hide it, as it was very easy to switch one insignificant bit (such the ones in the source hash) on the initCode. Salt can be used as wanted by project, but for Singleton the only use I see is “vanity address”.

> 100gwei

This is to ensure that it will be deployed on any chain no matter the gas cost. Its 100gwei and with the gas used it costs 0.027 to deploy. With 10gwei I might not have a deploy in some cases, and it would cost 0.0027 ETH.

I also hate to waste my precious gas to leave it there in a keyless address, but is not much, and this will save ETH in my other projects that also need keyless deploy (and are singletons), where the contracts are much bigger and using 100gwei would cost a lot. These singletons will use  any gas price ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) so we have to waste only a high amount in the Singleton Factory deploy.

This 100gwei value decisions was copied from ERC-820 and ERC-1820, which I found were plausible, instead of making everything very tight “gasLimit exactly the cost of deploy” and “gasPrice at a low price”, but then it wont be guaranteed to work in every situation.

For example, I don’t plan to deploy this on ETC, simply because I don’t own any ETC, but it might happen in future that some DApp gets ported to there and uses this ERC, so it will be guaranteed to work in ETC, even if they changed opcode costs and the gas market is competitive.

---

**Amxx** (2020-01-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> For example, I don’t plan to deploy this on ETC, simply because I don’t own any ETC, but it might happen in future that some DApp gets ported to there and uses this ERC, so it will be guaranteed to work in ETC, even if they changed opcode costs and the gas market is competitive.

Completelly unrellated, but does ETC have create2?

---

**3esmit** (2020-01-20):

> but does ETC have create2

I have no idea, the only blockchain I know about is Ethereum.


*(31 more replies not shown)*
