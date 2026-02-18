---
source: ethresearch
topic_id: 16199
title: Cross-Chain Unified Smart Contract Account without Preset Keystore
author: Leo
date: "2023-07-27"
category: Applications
tags: [account-abstraction]
url: https://ethresear.ch/t/cross-chain-unified-smart-contract-account-without-preset-keystore/16199
views: 3633
likes: 8
posts_count: 12
---

# Cross-Chain Unified Smart Contract Account without Preset Keystore

### TLDR:

We present a new design for cross-chain unified smart contract accounts. In the [design](https://vitalik.ca/general/2023/06/20/deeperdive.html) proposed by Vitalik, a preset keystore contract is needed and is used for wallet’s verification information. User links differenet wallet instances on different chains to the keystore. We propose a new structure where the need of a preset keystore is eliminated. User can simply create a wallet instance on a chain and then get another wallet instance on another chain with the same address, as long as he can prove his ownership of the original wallet.

## Definition

A smart contract account is considered cross-chain unified if it satisfies the following properties:

1. You can have multiple wallet instances on different chains with the same address.
2. Others cannot create a wallet instance with the same address as yours without stealing your account.
3. You can sync the state of the wallet between different instances on different chains at ease, e.g. the guardians of that wallet.

## Solution

The third property of a cross-chain unified account is ensured similarly to the light version mentioned in [Vitalik’s post](https://vitalik.ca/general/2023/06/20/deeperdive.html): each wallet instance has an information stored on the chain at which the instance is located, and syncs through ZK or KZG proofs once an instance changes its state.

In this article we will focus on how to ensure the first and second property is accomplished.

First we have a wallet factory instance with the same address on different chains. This can be done via [EIP-2470](https://eips.ethereum.org/EIPS/eip-2470) (aka Nick’s method). When user wants to simply create a wallet, the wallet factory would take in the InitData, nonce (unique) and chainId to calculate a salt, e.g. *salt = keccak256(encode(initData, nonce, chainId))*. The chainId is to prevent replay attack on another chain. This part is equivalent to creation of a normal account abstraction wallet. User can start to use it now and set different validation rules to the wallet (for example, in [our wallet](https://github.com/VersaLab/versa-contract/tree/main) you can set different validator).

When the user wishes to use his wallet on another chain but remains his unique address, he then calles the `CreateAccountOnTargetChain` function in his wallet. The wallet verifies his identity (with any kind of verification methods), and then passes the CreateAccountGiveSalt function call to bridge, with the salt that originally generated his first wallet. Any bridge can relay this message to the factory on a desired chain, and the factory would create a wallet instance with this salt using `CreateAccountGivenSalt`, acquiring the same address. So the first property holds.

To ensure property 2 is accomplished, the wallet could verify the message when calling `CreateAccountGivenSalt` and require the call is from the Bridge. In other words, users have to verify their ownership on one chain to create a new instance with the same address on another chain.

If one is concerned about the security of the bridge (like Vitalik said in his post), the bridge can be easily replaced by any low-level proofs such as ZK or KZG proofs, as long as thoe chosen method can relay verified messages.

The workflow is as illustrated in the following diagram:

[![](https://ethresear.ch/uploads/default/optimized/2X/6/65405722097e326e0bd0661c05b8ba6f2d7e5603_2_690x444.jpeg)1808×1166 265 KB](https://ethresear.ch/uploads/default/65405722097e326e0bd0661c05b8ba6f2d7e5603)

## Pros

There are several advantages of this implementation in comparison to the keystore solution:

- User experience. Users do not have to deploy a keystore contract first and then link his wallet instance. Users can simply begin their journey on one chain, and transfer their identities (addresses) to another chain whenever they wish to.
- Backward compatibility. User of the existing account abstraction wallet can simply upgrade his/her factory and does not have to change its wallet instance. Where the keystore solution requires an upgrade of the wallet instance.
- Gas efficiency. If user decides to only use his / her account on one specific L2, he / she would never have to prove any cross-chain message. Where the keystore solution always require a keystore contract (which is normally on L1).

## Cons

- State sync. The sync process can only be implemented as the light version in Vitalik’s proposal. You have to sync between all the networks, whereas the keystore solution (heavy version) allows you to upgrade in just one place, where the keystore contract resides.
- Harder to maintain privacy. The wallet’s verification information is always on the same chain with its instance, making private guardians harder to be implemented. In contrast, the keystore method can use ZK-based proofs to ensure privacy.

#### One more word on state syncing

The light version of cross-chain state syncing where you bridge the change of verification method change to each chain is quite burdensome. It actually would be more viable through a cross-chain paymaster and a chain-agnostic signature, i.e. you let your guardian sign a chain-agnostic signature to change your verification information. This signature could be replayed on different chains, by anyone. When you submit the transaction on one chain, using a cross-chain paymaster, the paymaster would submit the signature on all desired chains and deduct gas fee from the one chain you have asset on. This may look naive at first, but currently provide much better UX, gas efficiency and security than cross-chain syncing.

## Replies

**Leo** (2023-08-11):

We’ve implemented a demo at [Versa Omni Wallet Demo](https://versawallet.io/omni-demo-interface/), where you can create wallet and change guardian and still able to create wallet in another chain in the same address. Feel free to try that out

---

**maniou-T** (2023-08-12):

The way you’re suggesting to eliminate the need for a preset keystore and allowing seamless wallet creation on different chains sounds like a practical and user-friendly solution. Nice.

---

**zetsuboii** (2023-08-12):

First of all, good job on the Omni Wallet, it looks great.

Few questions:

- If I understand correctly, when I am on Polygon and want to create a wallet on Optimism, I have to call CreateAccountOnTargetChain where target chain is Optimism and provide a salt that is same as my wallet on Polygon. I couldn’t understand how this is better than connecting to Optimism and calling a account creation function with the same salt.
- Most SCA’s have a mechanism to modify keys that can control that account, like adding a new public key. How does this structure allow us to sync those keys so that if I can add a new key on Polygon and use it on Optimism? I don’t think using a crosschain guard and offchain signatures to handle those keys is the solution here because as Vitalik pointed out in his article, it is a critical part of the infrastructure and should be 100% trustless.
- Some chains don’t have the same address derivation method (e.g Starknet and ZKSync to my knowledge have different logic for it). How this method work in those cases? Does it assume EVM equivalence or would it work? From what I understand, as long as we have a way to use an equivalent of CREATE2 which both Starknet and ZKSync have, it should satisfy property 2, even though property 1 is not possible.

Again, really love the idea, very excited about the innovations on AA ground lately, keep up the good work ![:confetti_ball:](https://ethresear.ch/images/emoji/facebook_messenger/confetti_ball.png?v=12)

---

**Leo** (2023-08-14):

Thanks for the reply!

1. You can’t call CreateAccountGivenSalt and pass a certain salt to create account on Optimism directly (otherwise you can simply use others’ salt). The only way to create an account with a specific salt is through the cross-rollup messenger. The only account creation function you can directly call instead uses the salt = keccak256(encode(initData, nonce, chainId)) formation. Because there’s chainId in the salt, you won’t be able to get the same address if you try to replay on other chain. This ensures that others cannot get your address in Optimism either. If you want to get a specific address that has been deployed on other chain, you must proof your ownership on that chain and use remoteCreate.
2. Agreed. You can use any state-syncing method like KZG and SNARKS to sync your controlling key. We use layerzero to directly syncing those state changing in our demo. This proposal is more focused on ensuring the address consistency. State-syncing of controlling key is not even enfored here at wallet creation(because CreateAccountGivenSalt allows you to pass Initdata).
3. I think as long as there’s an equivalent of CREATE2 on that chain you will be able to use that method because it only rely on the property of CREATE2.

I’ll add more specification and implementation detail in the post for better understanding, thanks again for the reply!

---

**Leo** (2023-08-14):

This is the interface of the factory under the proposed structure

```auto
mapping(address wallet => bytes32 salt) internal _walletSalts;

function createAccount(bytes initData, uint256 nonce) public returns(address) {
	// 1. Use hash(initData, nonce, chainId) as the create2 salt.
	//    Including chainId information is to prevent malicious users from replaying the deploy transaction without permission.
	// 2. After the wallet is created, store the salt in the _walletSalts mapping.
}

// msg.sender is the wallet. Retrieve the wallet's salt from the mapping.
// An implicit condition here is that this UserOP has been verified by the validator of wallet.
function createAccountOnRemoteChains(
	bytes[] memory initDataOnRemoteChains,
	uint256[] chainIds
) public payable {
	// checks that salt == _walletSalts[msg.sender]
	// this insures ownership
	// loop: _createAccountOnRemoteChain()
}

function _createAccountOnRemoteChain(
	bytes memory initDataOnRemoteChain,
	uint256 chainId
) public {
	// Send cross chain message
}

// Receive cross-chain wallet creation information from cross-chain messanger.
function _createAccountGivenSalt(
	bytes memory salt,
	bytes memory initData
) internal returns(address proxy) {
	// requires only call from cross-chain messanger
	// 1. Create a wallet using the salt.
	// 2. After creation, call wallet.initialize(initData) to initialize.
}
```

---

**zetsuboii** (2023-08-15):

Thanks for the answers,

About the first answer, I think adding the `msg.sender` to the hash function instead of the `block.chainid` should be enough to make sure `CreateAccountOnTargetChain` doesn’t create the same account for different users in case they use the same salt while ensuring users can call the same function on different chains themselves.

So that I can create the account on optimism with hash Salt = Hash(Data, Nonce, Address) and someone else can’t replay the same transaction as `msg.sender` would be different. But I can connect my wallet to polygon and give the same (initData, nonce) combination to create the same wallet, as long as my private key is same.

---

**Leo** (2023-08-15):

Yeah if you have an EOA that would be a go-to solution. This proposal focus on SCW under ERC-4337, where user don’t have an EOA and the msg.sender is always the bunder. In this case you cannot use msg.sender to differentiate identity.

---

**Chaz** (2023-08-15):

When user generates the wallet on the first chain, the salt is public already. How do you prevent someone from taking the salt and front-run the contract deployment on the second chain? The attacker can call the factory on the second chain directly

---

**Leo** (2023-08-16):

Yes, the salt is public.

1. the salt contains chainId information in it so it cannot be replayed on other chain.
2. If the attacker try to front-run the transaction from the mempool in the first chain, because the salt contains InitData, the wallet’s initiation config would be the same as what you specify. In other word, the attack is deploying a wallet for you. He would create a wallet using your config (which means you have the key to manage this wallet).

---

**pyk** (2023-08-16):

> How do you prevent someone from taking the salt and front-run the contract deployment on the second chain?

One of the solution is to use `msg.sender` as salt, for example:

```auto
function create(bytes memory publicSalt) external {
     bytes32 salt = keccak256(abi.encodePacked(msg.sender, publicSalt));
     ...
}
```

so even tho `publicSalt` is public, only `msg.sender` can create the same `salt` on other chain.

---

**Leo** (2023-08-16):

Yes indeed. As I previously replied

> If you have an EOA that would be a go-to solution. This proposal focus on SCW under ERC-4337, where user don’t have an EOA and the msg.sender is always the bunder. In this case you cannot use msg.sender to differentiate identity.

Basically in 4337 all msg.sender is bundler. So you cannot use msg.sender to differentiate.

