---
source: ethresearch
topic_id: 19678
title: MagicSpend++ Spend Now, Debit Later
author: vaibhavchellani
date: "2024-05-29"
category: Applications
tags: [rollup, account-abstraction, layer-2]
url: https://ethresear.ch/t/magicspend-spend-now-debit-later/19678
views: 13101
likes: 29
posts_count: 22
---

# MagicSpend++ Spend Now, Debit Later

## Introduction

The current smart wallet experience for users is not suited for transacting in a world with hundreds or thousands of rollups. It forces an average Ethereum user to deal with fragmented assets, forcing them to manage fragments of their assets across 100+ rollups along with complexities like GAS, bridging & RPCs for every transaction.

> For example, today it takes over 30+ clicks in the wallet & over 40+ minutes for a user to use an app on another chain with the swapping, bridging of tokens & GAS, switching RPCs, and other actions involved.

There are several standards today for smart contract wallets. Users send signed UserOps that are bundled together and sent on-chain. It also enables users to pay gas fees using ERC-20 tokens (e.g. USDC) instead of ETH by allowing a third party to sponsor their gas fees.

[![image](https://ethresear.ch/uploads/default/optimized/3X/d/6/d696cf1819e42dfa3424b84e0c8360da38183915_2_690x275.jpeg)image2000×799 75.5 KB](https://ethresear.ch/uploads/default/d696cf1819e42dfa3424b84e0c8360da38183915)

The current smart wallet experience for users is not suited for transacting in a world with hundreds or thousands of rollups. It restricts the extent of abstraction to just one single rollup instead of thousands of rollups. It forces an average Ethereum user to deal with fragmented assets, forcing them to manage fragments of their assets across 100+ rollups along with complexities like bridging & RPCs for every transaction.

### MagicSpend++

We propose MagicSpend++, a framework to allow users to magically spend on any chain instantly, without worrying about which chains their tokens are on.

MagicSpend++ leverages the existing Account Abstraction standard and builds on Coinbase’s work on MagicSpend - an innovative approach to allow users to leverage their assets held on Coinbase Exchange & utilize them on-chain.

MagicSpend++ fundamentally enables users to have a *Chain Abstracted Balance (CAB)* instead of isolated token balances across chains. Users can use their CAB to transact instantly on any chain with a signature. No fragmentation, no bridging, no GAS, no latency.  It’s magic. ![:dizzy:](https://ethresear.ch/images/emoji/facebook_messenger/dizzy.png?v=14)

Smart wallet users with MagicSpend++ get:

- A unified single balance across chains that users can spend anywhere
- Completely gas-less experience
- Instant single chain experience - NO CROSS CHAIN, NO BRIDGING, ZERO LATENCY

### Fundamental Primitive — Time-locked Vaults

In order for tokens to enter the Chain Abstracted Balance, they need to be locked in their smart wallets. Users can withdraw funds back to their **Externally Owned Accounts (EOAs)** after a configurable delay. While locked, the assets remain usable via the smart-account on any chain at any time. **This one-time step required-to onboard as a part of deposit to SCW workflow, it is not required every-time before the assets are used.**

All assets deposited represent the user’s Chain Abstracted Balance (CAB). This chain abstracted balance can now be spent on any-chain via userOps, without bridging, just like how you would spend these assets as if they were on the chain you are acting on.

> Your 100USDC@Optimism, 100USDC@Polygon, 100USDC@Arbitrum, 100USDC@Base, 100 USDC@ethereum all merge together into 400USDC, ready to be spent anywhere.

[![image](https://ethresear.ch/uploads/default/optimized/3X/7/7/77765f9c7d128996817736249125fd859f3710f6_2_690x295.jpeg)image2000×857 113 KB](https://ethresear.ch/uploads/default/77765f9c7d128996817736249125fd859f3710f6)

### Key concept – Spend Now, Debit Later

Conceptually it’s pretty similar to how AA works today with a small difference. User sends UserOp to perform an target chain, just like they would if they had funds on the same chain. Paymasters can now fund the userOp with not just gas but with additional funds to facilitate the on-chain execution of the UserOp. Paymaster then goes and claims it from the chain abstracted balance.

[![image](https://ethresear.ch/uploads/default/optimized/3X/8/5/85d1025c1eb22df5366dedd8449865387901327e_2_690x427.jpeg)image2000×1239 151 KB](https://ethresear.ch/uploads/default/85d1025c1eb22df5366dedd8449865387901327e)

### How it works - high level overview

Say Alice wants to purchase a NFT on BASE using her 1000USDC Chain-Abstracted-Balance:

- Alice sends a signed UserOp to purchase the NFT on BASE
- Paymaster checks(offchain) if there are sufficient funds with Alice in her chain abstracted balance and authorizes usage of paymaster funds via a special_signature
- UserOp is sent to bundler with paymasterAndData containing the special_signature that allows the SCW to pull funds from the paymaster’s pool of liquidity on BASE
- UserOp is normally executed onchain leveraging the paymaster funds, SCW leverages withdrawGasExcess(special_signature) to pull funds from paymaster
- Paymaster can now debit the respective funds from Alice’s chain abstracted balance in custody of smart-wallets (whichever chain or multiple-chains that they are on)

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/d/cdfdad93b81b35b2a546ea19f28e38c2990dd52d_2_690x317.jpeg)image2000×920 130 KB](https://ethresear.ch/uploads/default/cdfdad93b81b35b2a546ea19f28e38c2990dd52d)

### Not Cross-chain but Chain Abstraction

This removes a lot of the pain a user faces today: figure out swap, bridge, buy new gas paying asset and only then will you get to use this new thing. This is dumb and holding back new innovation from taking off. A DEX can be 10x more capital efficient but without liquidity/volume it doesn’t matter.

Chain abstracted wallets provide various 10x improvements for users:

- User asset-balances across chains are combined into one Chain Abstracted Balance
- Balance is instantly usable anywhere, zero bridging latency

This is completely different than any cross-chain implementations where wallets integrate bridges likes Across, Stargate, etc.

Cross-chain implementations are push-based where users start with a fragmented balance on one chain and “push” their tokens to another. On the other hand, MagicSpend++ is pull based where the user simply uses an app and their funds are pulled by the paymaster later. It’s like Spend first, debit later.

This has various implications for the end users.

| Cross-Chain Accounts (push) | Chain Abstracted Balance (pull) |
| --- | --- |
| Asset fragmentation still persists across chains. Users still have to think about fragmented assets on different chains | Single Chain Abstracted Balance |
| Bridging latency-  Users sign a UserOp on the source chain, wait for source chain finality before tx is processed on target chain | Instant finality- User sign a UserOp on the target chain which is fulfilled immediately. No need to wait for finality on source chain. |
| Failure on dest chains - UserOp can fail mid-bridging. Users get stuck with arbitrary funds on target chain in this case | Guaranteed execution - user funds are deducted from the balance only if their transaction is successful |
| Users get tied into trust properties of the bridge for settlement | Users have tighter control over security where they can configure how paymasters can settle |

## Diving Deeper

All we really need to enable this is a new module that creates a vault with configurable withdraw delay such that users can deposit into this vault but only withdraw after a time period, the funds deposited are still usable by the user but in a chain-abstracted fashion. These vaults can be on multiple chains and all the balances will add up and be usable as one.

[![image](https://ethresear.ch/uploads/default/optimized/3X/2/9/299b49a7fa6fbf3619fbdc0c3b6cc846342ec7b9_2_690x376.jpeg)image2000×1091 154 KB](https://ethresear.ch/uploads/default/299b49a7fa6fbf3619fbdc0c3b6cc846342ec7b9)

A good example to start with is Alice wants to mint an NFT on Ethereum worth 100 USDC, lets assume the deposit into the SCW was already done on Base 1000 blocks ago

- Alice goes to the NFT mint site, and wants to insta buy
- Alice clicks mint button the paymaster service checks locked userBalance on all vaults across chains and sends back a special_signature
- paymasterAndData ****will be set to whatever paymaster service application/user opts into just like today, the data however includes the special_signature provided by the paymaster
- This userOp is sent to bundler → entrypoint
- Entrypoint calls validateUserOp() on the SCW and does the usual operations
- When Entrypoint calls validatePaymasterUserOp(…..special_signature)
- Post the usual validations, the paymaster validates the signature and sets a map(address⇒amount) to allow userOp.sender withdraw the amount (which will be the SCW)
- The SCW will then leveraging the withdrawGasExcess method pull funds from the paymaster and execute the userOp that buys the NFT
- In the postOp operation

mapping(address⇒amount) set earlier will be deleted to ensure no double spends
- an execution proof will be sent by the sender contract on L1 to an L2 or multiple L2s via the native-rollup-connections

execution proof is simply a proof to convince chainA of some execution that happened on chainB, think light-client proofs, ZKPs etc

Funds will be then deducted from the userVault and given to paymaster

💡 Interesting thing to note here, while the paymasters are forwarding funds to the user, they are not taking ANY reorg risk since there is no source chain tx for a userOp that is trying to spend, its credit now, debit later

## Limitations and Solutions

While the above mechanism works great and accomplishes the desired goals, the approach has limitations with paymaster availability & settlement flexibility. Smart-Wallets can by-pass these limitations using Socket’s MOFA.

- Single Paymaster Weak: User gets locked into a single paymaster and if paymaster doesn’t have liquidity userOps will not be executed. SCWs can instead delegate paymaster election to Socket’s MOFA to tap into a global network of competing paymasters and sidestep liquidity and efficiency issues. With MOFA, multiple paymasters compete to fulfill incoming UserOps, which means more paymasters, more liquidity & more execution. Single paymaster weak, paymasters together strong.
- Restrictive Settlement Options: Its quite important in the chain-abstracted world for users signing userOps or developers building SCWs to have the ability to expand to new chains quickly, to be able to make their own tradeoffs(security, cost, latency). Standardisation around settlement allows for users and developers to handle both expansion and tradeoff selection in a transparent fashion.

[![image](https://ethresear.ch/uploads/default/optimized/3X/3/5/35964d42692a8fd042edb63452bab73015cbf3c1_2_690x416.jpeg)image2000×1207 147 KB](https://ethresear.ch/uploads/default/35964d42692a8fd042edb63452bab73015cbf3c1)

## Acknowledgements

We think magic-spend++ enables complete chain-abstraction, where users dont have to care where their assets are.

Thank you to the following people for the many discussions, reviews and idea-sharing which lead to the creation of this proposal(in no particular order):

Wilson Cusack, Pierce Harger, Uma(@pumatheuma), Alex Watts, Partha, Ahmed Al-Balaghi, Sachin Tomar, Ivo Georgiev, Theo Gonella, Derek Chiang, Kristof Gazso, Ankit and Stephane, Kakusan, Bapireddy, Aniket Jindal

We are keen to work with existing AA players building bundlers, paymasters and existing solvers/paymasters, wallets, dapps and together be at a place where no one needs to bridge anymore. If anyone is interested in magic-spend++ or chain-abstraction in general we have a public group here to talk about it: [Telegram: Join Group Chat](https://t.me/+QygeBurngS4wODNl)

Account Abstraction → Chain Abstraction journey begins now

## FAQs

- Are paymasters becoming solvers/fillers here?

Solvers/Fillers in cross-chain setting for eg as used in Across, DLN and other intent based protocols are entities that front liquidity and take on reorg risk in return of fees, paymasters in the AA world are not needed to take on reorg risk and here paymasters arent exposed to reorg risk either, so no they arent the same

What risks/trust-assumptions are here for users?

- Users only need to trust the proof-system for security here and there is no additional off-chain security, magic-spend++ can leverage ZKPs, rollup-messengers to have an extremely trust-minimised setup

## Replies

**EugeRe** (2024-05-29):

Very nice work! I would like to further contribute! Also look at my latest blog! I believe there are nice touch points.

---

**irboz** (2024-05-29):

Congrats, really hyped by the development of onchain abstraction

---

**alau1218** (2024-05-30):

Great post! Thanks!

How can you make sure Alice will not double spend? I assume once Alice clicks the mint button and signed the special signature, the SCW would also lock up the funds she spent to buy that NFT? Will the paymaster receive a commitment or proof that the funds will be locked up for that NFT purchase?

If there is a commitment made from the SCW, is this similar to the OneBalance framework proposed by frontier research?

---

**shreyas-londhe** (2024-05-30):

Great post! Really liked the vision for excellent UX for  the users and would definitely help onboard new users.

I have a doubt based on a race condition that might arise and I have not clearly understood the finality for the transactions done using the CAB.

Suppose Alice has a CAB of 100USDC, and she does 3 simultaneous transactions on 3 different chains of 50USDC each. How I imagine the flow is:

Paymasters on each chain query that txn_amount > CAB, and then process the txn further. My doubt is, is there a process which updates the CAB once a paymaster queries? If there is a process to update, I believe the other paymasters will have to wait until the CAB is updated and will lead to increased finality time for the other 2 transactions.

Please correct me if I have understood something incorrectly.

---

**vaibhavchellani** (2024-05-30):

mind linking me the blog you are talking about here? keen to check it out

---

**vaibhavchellani** (2024-05-30):

thanks for checking it out, these are all good questions

> How can you make sure Alice will not double spend?
> So it starts with users locking up their funds in the vault as mentioned in the post, the vault allows user to withdraw only after a say 6hour delay, so unlike intents, onebalance, funds here are committed before everything else

Since funds are committed and paymasters can easily lookup onchain balances the expenditure by the user, paymasters have a consistent view of “available pending balance” that the user can spend and hence are safe from the double-spend

hopefully that helps, but happy to double click if needed

---

**leekt216** (2024-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/vaibhavchellani/48/3716_2.png) vaibhavchellani:

> Since funds are committed and paymasters can easily lookup onchain balances the expenditure by the user, paymasters have a consistent view of “available pending balance” that the user can spend and hence are safe from the double-spend

What if there are multiple userOps in different paymasters that looks for same balance?

Like Alice has 100USDC on source chain and attempts to spend 100USDC on 3 different paymasters and 3 different chains?

---

**vaibhavchellani** (2024-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/shreyas-londhe/48/16529_2.png) shreyas-londhe:

> Paymasters on each chain query that txn_amount > CAB, and then process the txn further. My doubt is, is there a process which updates the CAB once a paymaster queries? If there is a process to update, I believe the other paymasters will have to wait until the CAB is updated and will lead to increased finality time for the other 2 transactions.

thanks for reading the proposal and for the question, I can see where the confusion is stemming from and am happy to help resolve it

basically paymaster needs a consistent view of total available balance for the user to spend, there are 3 pieces of information the paymaster would need for this:

- locked amount in SCWs
- amount spent on-chain but not debited yet (can be tracked onchain)
- amount in pending (can be looked up in bundler mempool for a specific paymaster)

available_balance = lockedAmount - amountSpentButNotDebited - amountInPending

The above information is available real time and is not blocked by anything onchain, hopefully that helps, but please dont hesitate if you have more questions

---

**vaibhavchellani** (2024-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/leekt216/48/4374_2.png) leekt216:

> Like Alice has 100USDC on source chain and attempts to spend 100USDC on 3 different paymasters and 3 different chains?

We have talked about the entire thing with a single paymaster, to have multiple paymasters you want something like Socket MOFA which allows multiple paymasters to have a shared orderbook, so they have consistent view of the pending-pool and can prevent themselves from double spends

SCW module that locks up user funds will be allowed to only spend via 1 single paymaster entity, this paymaster entity can be a single paymaster or multiple-paymasters working together via socket-MOFA

Multiple orderops, multiple chains, multiple paymasters are fine as long as they have a single view of the pending pool

---

**leekt216** (2024-05-30):

thanks for the answer, makes sense to focus on one paymaster atm.

another question, how do you imagine the ux will be when it comes to different token address for different chain?

If address of asset used on chain B(where userOp has been executed), and asset claimed on chain A(where asset is locked) is different, there should be a verification if claimed asset is what Alice has agreed to spend.

should there be a mapping on the paymaster? or should this be verified with paymasterAndData & special_signature?

For mapping, i think this will lead to centralized point, and for verifying on paymasterAndData, it will require Alice to check the asset being claimed(a small pop up like eth_signTypedData i guess?)

---

**vaibhavchellani** (2024-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/leekt216/48/4374_2.png) leekt216:

> For mapping, i think this will lead to centralized point, and for verifying on paymasterAndData, it will require Alice to check the asset being claimed(a small pop up like eth_signTypedData i guess?)

This is a good question, I have not thought too deeply about it, I imagine this information would be part of the userOp being signed or it could be on the SC level or offchain, dont think this is an issue/problem due to magic-spend++ but a problem that spans the entire ecosystem, will think more on this and get back!

---

**vaibhavchellani** (2024-06-04):

![](https://ethresear.ch/uploads/default/original/3X/c/1/c113b489755f57f99ddc09ddf0ee6b7bdfeba4b5.gif)

---

**EugeRe** (2024-06-04):

Sure, You find it here!

https://ethresear.ch/t/unveiling-the-power-of-self-sovereign-identity-and-account-abstraction-for-privacy-preserving-user-operations/19599

---

**himanshuchawla009** (2024-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vaibhavchellani/48/3716_2.png) vaibhavchellani:

> We have talked about the entire thing with a single paymaster, to have multiple paymasters you want something like Socket MOFA which a

Great post, thanks for sharing.

As you mentioned this approach is described in the context of single paymaster , as it can be tricky for multiple paymasters to avoid double spend, i am having difficulty to understand that how it is different from deposit based approach which most paymaster providers are taking currently where user deposits some ERC20 token in paymaster account and receives some universal gas token or offchain credits to claim to pay for other chains.

---

**mikec** (2024-08-01):

Great design, very exciting stuff. a few questions:

1. How is the distribution of repayment across SCWs determined? For example, if user has 100USDC@A and 100USDC@B, and they want to buy a Sloth for 100USDC on C, will paymaster receive repayment 100% on A, 100% on B, 50% on A and B? Would this be determined by front-end when constructing the UserOp or protocol level?
2. If native connections between L1/L2s are used, paymaster has to wait 7 days for repayment on L1 after funding/transmitting UserOp on an L2. Would it be possible for the UserOp itself to define the mechanism for settlement, so a non-native/faster proof could be used?
3. Would settlement in a highly fragmented environment (i.e. 10 USDC on 100 chains, used to buy 1 asset for 1,000USDC) potentially become prohibitively expensive (user has to pay for 100 messages)? Maybe some optimistic mechanism could eliminate the message cost, but even so the paymaster has to withdraw on 100 chains in this scenario

---

**aashidham** (2024-08-01):

Really interesting approach to solve a set of deep problems in the space!

Would the design require Socket to deploy (in a permissioned way) a paymaster on every chain that the user wants to transact on? Or could this be used on a new chain that does not have a paymaster on the Socket MOFA yet? I’m wondering if the design here can be used to bootstrap liquidity and transactions on a new appchain or L3 that doesn’t have a ton of BD or developer traction yet.

What chains does Socket MOFA support currently?

---

**rersozlu** (2024-08-02):

Interesting approach but there needs to be a bit more deeper explanation in my opinion.

1. Smart wallet user will have a separate contract in each chain to perform signatures or hold assets as far as I understand. What about the recovery options and authenticators of these accounts? If user wants to switch their public key pair (authenticator) in Chain A, source chain, how will SCW’s on every other chain that he/she can interact will act?
2. Paymasters on source chain either will be overpowered (able to pull funds from user’s locked assets) or they will need to prove destination transaction to the SCW as mentioned in the post. How is it possible to prove every possible transaction’s output in terms of tokens to the source SCW? Imagine some weird memecoin contract that calls a function, which will allow user to claim 10 USDC after a certain amount of period. You would then need to prove source SCW to pay 10 USDC to paymaster which will be received 10 days later in the destination chain.
3. After a certain transaction, are these assets going to stay at destination chain SCW or will be minted to source synthetically? If prior, see no.1 concern about recovery.

---

**vaibhavchellani** (2024-08-02):

> How is the distribution of repayment across SCWs determined? For example, if user has 100USDC@A and 100USDC@B, and they want to buy a Sloth for 100USDC on C, will paymaster receive repayment 100% on A, 100% on B, 50% on A and B? Would this be determined by front-end when constructing the UserOp or protocol level?

I think about magic-spend++ as a base mechanism and this is a implementation specific, but my current thoughts are, users will basically in their userOp approve repayment positions, paymasters will then construct repayment pathways and we will even see optimisation there, cheaper the repayment pathway, less fees for end user, so yea paymasters will decide repayment pathway at execution time, users will only whitelist locations or just select all.

> If native connections between L1/L2s are used, paymaster has to wait 7 days for repayment on L1 after funding/transmitting UserOp on an L2. Would it be possible for the UserOp itself to define the mechanism for settlement, so a non-native/faster proof could be used?

Yep in the diagram I mentioned that the proof system is modular, thats part of MOFA, and users/paymasters will be able to opt into their choice of proof system

> Would settlement in a highly fragmented environment (i.e. 10 USDC on 100 chains, used to buy 1 asset for 1,000USDC) potentially become prohibitively expensive (user has to pay for 100 messages)? Maybe some optimistic mechanism could eliminate the message cost, but even so the paymaster has to withdraw on 100 chains in this scenario

Yep, this is same as today, if you have highly fragmented balances you will pay for it somehow, this system moves the burden from user to paymaster and allows them to optimise the repayment to reduce the cost, but yes the cost of having your balances on 1000 chains will be higher than 10 for sure, how much, market will decide

---

**vaibhavchellani** (2024-08-02):

> Would the design require Socket to deploy (in a permissioned way) a paymaster on every chain that the user wants to transact on? Or could this be used on a new chain that does not have a paymaster on the Socket MOFA yet? I’m wondering if the design here can be used to bootstrap liquidity and transactions on a new appchain or L3 that doesn’t have a ton of BD or developer traction yet.

Good question, MOFA is going to have no notion of “chains” so it should be able to be available for users/developers regardless of how many chains exist, going to release some more documentation around MOFA soon to make this clearer. Paymasters dont need to be permissioned so you should be able to run a paymaster for your chain easily

---

**vaibhavchellani** (2024-08-02):

> Would the design require Socket to deploy (in a permissioned way) a paymaster on every chain that the user wants to transact on? Or could this be used on a new chain that does not have a paymaster on the Socket MOFA yet? I’m wondering if the design here can be used to bootstrap liquidity and transactions on a new appchain or L3 that doesn’t have a ton of BD or developer traction yet.

I think this is out of scope for the mechanism in itself but its definitely a question a bunch of teams as answering and solving for, for eg light sync, keystore etc

> Paymasters on source chain either will be overpowered (able to pull funds from user’s locked assets) or they will need to prove destination transaction to the SCW as mentioned in the post. How is it possible to prove every possible transaction’s output in terms of tokens to the source SCW? Imagine some weird memecoin contract that calls a function, which will allow user to claim 10 USDC after a certain amount of period. You would then need to prove source SCW to pay 10 USDC to paymaster which will be received 10 days later in the destination chain.

Im not sure I fully understand the question here, but to be clear paymasters dont have access to funds directly, they need to execute the userOp on destination and “prove” to the SCW that the userOp was executed to collect the assets, the proving system is going to be user defined so users only need to trust the proving system which is true for anything operating between chains

> After a certain transaction, are these assets going to stay at destination chain SCW or will be minted to source synthetically? If prior, see no.1 concern about recovery.

There is no minting.


*(1 more replies not shown)*
