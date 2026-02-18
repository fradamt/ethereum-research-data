---
source: ethresearch
topic_id: 19557
title: Introducing OneBalance
author: thegostep
date: "2024-05-15"
category: Applications
tags: [mev, zk-roll-up, rollup]
url: https://ethresear.ch/t/introducing-onebalance/19557
views: 15170
likes: 38
posts_count: 21
---

# Introducing OneBalance

By [Stephane Gosselin](https://twitter.com/thegostep) and [Ankit Chiplunkar](https://twitter.com/ankitchiplunkar) on behalf of Frontier Research

*For most recent information about OneBalance, please visit [frontier.tech](https://frontier.tech/onebalance).*

*See Research Day 2024 [slides](https://docs.google.com/presentation/d/1sOuDB-HUiOyxiX3qrmGRfOm7NyxsIxLzBIDqRi0xJdU/edit?usp=sharing) and [recording](https://www.youtube.com/watch?v=okDSIm7PE6I).*

# Motivation

Web3 and the crypto ecosystem more broadly has historically had a chain centric worldview. We believe this is an outdated framework originating from a perceived scarcity in blockspace due to the bundling of credible commitment machines with global consensus.

We believe an ecosystem wide transition towards an account centric worldview which bundles accounts with credible commitment machines is both necessary and inevitable in order to consolidated a fragmented user experience.

We propose a new account model called “*Credible Accounts*” and introduce a framework called “*OneBalance”* for creating and managing these accounts. With this proposal, we hope to provide a missing component of the web3 stack that will help onboard the first billion humans onto crypto.

# TLDR

OneBalance is a framework for creating and managing accounts on credible commitment machines. We call these Credible Accounts.

Each account can thought of as an rollup which allows users to conveniently manage their state and reliably request state transitions on any chain.

This is achieved through the introduction of two key concepts:

1. Accounts on credible commitment machines, and
2. Resource locks

A credible commitment machine is responsible for securing the account, issuing resource locks over the state it holds, and validating the fulfillment of such locks.

By introducing Credible Accounts, we hope to accelerate the transition of the ecosystem from EOAs, the JSON-RPC API, and the transaction supply chain, towards an architecture built around message passing of resource locks and fulfillment proofs.

**A Credible Account on OneBalance can:**

- Combine token balances from every chain
- Abstract gas on any chain
- Swap and send tokens to and from any chain
- Issue complex permissions over any subset of user state
- Incentivize and enforce atomic asynchronous composability across multiple chains
- Authenticate user using modern methods such as passkey, session keys, FIDO
- Fast confirmations through separation of fulfillment from settlement

Many use cases are unlocked with these new capabilities. Users can spend any token to pay for state transitions. They can aggregate liquidity that lives both on-chain and off-chain. They even have the building blocks to build a decentralized Fireblocks, or a non-custodial Binance.

[![OneBalance Account Framework](https://ethresear.ch/uploads/default/optimized/3X/b/9/b9c28cc78642455ccebc698c9de49bf17f43d00a_2_690x388.png)OneBalance Account Framework2666×1500 481 KB](https://ethresear.ch/uploads/default/b9c28cc78642455ccebc698c9de49bf17f43d00a)

# Wallet 1.0 - Externally Owned Accounts

The web3 market structure equilibrium, as defined by Ethereum, is the use of public-private key-pair, aka, Externally Owned Account (EOA) to manage all aspects of a user’s state.

Since EOAs sit outside the blockchain, the chain has no view over what message have been signed. The chain relies on the use of nonces to sequence user state transaction requests, often called transactions.

Here, we simplify down a smart contract blockchain such as Ethereum to a Credible Commitment Machine bundled with Global Consensus.

[![Externally Owned Accounts](https://ethresear.ch/uploads/default/optimized/3X/9/6/9699fa9c1bf230afc00d597a1fc098f5ba09a076_2_448x159.png)Externally Owned Accounts3345×1195 157 KB](https://ethresear.ch/uploads/default/9699fa9c1bf230afc00d597a1fc098f5ba09a076)

### Credible Commitment Machines

[Thomas Schelling’s](https://en.wikipedia.org/wiki/Thomas_Schelling) 1960 ***The Strategy of Conflict*** famously introduced the game theory concept of “focal point” better known as his name sake “Schelling point” .

A lesser know contribution of this work was the introduction of “credible commitments” which he describes as “a promise or threat believable to others by creating a situation where the costs of reneging on the commitment are higher than the benefits”.

According to Schelling, a credible commitment must provide:

1. Irrevocability: Making the commitment in such a way that it cannot be easily reversed. This might involve physical actions or formal agreements that lock the party into their commitment.
2. Increased Costs: Ensuring that backing out of the commitment imposes significant costs, either financially, reputationally, or strategically.
3. Observable Commitment: The commitment must be visible and understandable to other parties, ensuring they believe in the credibility of the commitment.

The concept was further refined by [Nick Szabo in 1997](https://www.fon.hum.uva.nl/rob/Courses/InformationInSpeech/CDROM/Literature/LOTwinterschool2006/szabo.best.vwh.net/idea.html) with the introduction of the concept of smart contracts as software enforced contracts, which was further explored by [Mark S. Miller and Marc Stiegler in 2003](https://papers.agoric.com/assets/pdf/papers/digital-path.pdf).

These investigations lead to the [Ethereum Whitepaper](https://ethereum.org/content/whitepaper/whitepaper-pdf/Ethereum_Whitepaper_-_Buterin_2014.pdf) published by Vitalik Buterin in 2014 proposing Ethereum as the first smart contract blockchain capable of creating and enforcing arbitrary credible commitments.

Many important contributions to the topic followed with a noteworthy contribution by [Mohammad Akbarpour and Shengwu Li in 2019](https://web.stanford.edu/~mohamwad/CredibleMechanisms.pdf) providing a formal definition to Credible Mechanisms and introducing the auction trilemma.

Loosely defined, we refer to a Credible Commitment Machine as a secure computer able to programmatically issue and enforce commitments such that they are believable or “credible” to a third party observer.

### EOAs and Request Equivocation

EOAs are not credible commitment machines. Since the chain has no view over what the user has signed, it must consider any transaction signed with the same nonce as valid. This means that at any time, a user can equivocate their state transition request by signing and submit a new transaction which overwrites their nonce.

This makes EOAs, and the transaction supply chain more broadly, incapable of providing credible commitments as they violate the principle of irrevocability. ****Downstream parties in the transaction supply chain such as solvers are unable to rely on the commitments made by EOAs as they may be equivocated at any time.

To date, every system looking to protect against request equivocation have relied on locking funds in a deposit smart contract. This is the approach used by all types of bridges (L2, intent, POA, IBC, ZK). All implementations of secure cross chain interactions rely on the transfer of assets to a smart contract as a request which cannot be equivocated.

The class of networks based on HTLCs such as the Interledger Protocol all use timelocked requests as a form of credible commitment for security passing economic messages between ledgers.

# Wallet 2.0 - Smart Contract Accounts

Smart Contract Accounts (SCAs) solve the request equivocation problem by bringing the signer on chain. This allows the account to leverage the chain’s credible commitment machine and global consensus to timestamp and sequence each state transition requests issued by the user thereby preventing equivocation.

[![Smart Contract Accounts](https://ethresear.ch/uploads/default/optimized/3X/8/6/860b98a163a541999228b08fc63ef52bccda7155_2_448x159.png)Smart Contract Accounts3345×1195 150 KB](https://ethresear.ch/uploads/default/860b98a163a541999228b08fc63ef52bccda7155)

Vitalik has long been a proponent of smart contract wallets as these offer great UX features broadly referred to as account abstraction which includes gas abstraction, social recovery, permissions policies, and modern authentication methods.

Despite addressing the equivocation problem, smart contract accounts deployed to chains with global consensus like Ethereum are prohibitively expensive and slow. This is because virtual machines such as the EVM require the sequential execution of global locks over all user accounts for every state transition request. This is equivalent to forming a single global queue of all users waiting to do something on chain.

### The Account Dilemma

We observe a tradeoff between EOAs and SCAs. On one side we have EOAs which are fast and cheap, but cannot make credible commitments due to request equivocation. On the other side we have SCAs which can make credible commitments, but are slow and expensive due to global consensus. We call this tradeoff the Account Dilemma.

[![The Account Dilemma](https://ethresear.ch/uploads/default/optimized/3X/3/8/388e6f420274cdb504f0e98be46be09230a816dc_2_448x292.jpeg)The Account Dilemma2476×1615 141 KB](https://ethresear.ch/uploads/default/388e6f420274cdb504f0e98be46be09230a816dc)

# Wallet 3.0 - Credible Accounts

We propose a new account model called Credible Accounts which aims to solve the Account Dilemma. Credible Accounts live in a secure computer of the users choice that can make credible commitments about what messages it will and won’t sign.

By unbundling global consensus from the Smart Contract Account model, we are able to keep the speed and cost advantage of EOAs while retaining the UX improvements and non-equivocation guarantees of SCAs.

[![Credible Accounts](https://ethresear.ch/uploads/default/optimized/3X/8/3/837f659d705ce4c043148cb3ae81b8324adc5686_2_448x159.png)Credible Accounts3345×1195 149 KB](https://ethresear.ch/uploads/default/837f659d705ce4c043148cb3ae81b8324adc5686)

### OneBalance: a framework for Credible Accounts

Each OneBalance account can be thought of as its own rollup. The account wraps individual user state from all chains and replicates it in a virtual environment. This virtual environment issues state transition requests as “resource locks” and fulfills those state transitions through cross-chain execution proofs. This virtual environment is secured by a credible commitment machine.

Since a OneBalance account provides the same guarantees as a SCA, it comes with all the same UX benefits of account abstraction, such as gas abstraction, social recovery, permission policies, and modern authentication methods.

A OneBalance account can create an arbitrary number of sub accounts across any number of chains and manage any state present on those chains. It is backwards compatible with all chains, smart contracts, and assets including Ethereum, Solana, Bitcoin, ERC20s, NFTs, DAOs, multisigs, defi protocols, and deposits or points programs. This multi-ecosystem compatibility is not possible with other current account model.

| Capability | EOAs | SCAs | OneBs |
| --- | --- | --- | --- |
| Fast & Cheap |  |  |  |
| UX features |  |  |  |
| Equivocation protection |  |  |  |
| Multi-ecosystem compatibility |  |  |  |

The OneBalance framework for Credible Accounts is implemented in a modular way using standards developed by the [CAKE Working Group](https://frontier.tech/cake-working-group) to allow users / apps / wallets to pick an choose any component of the [CAKE Framework](https://frontier.tech/the-cake-framework) needed for their use case.

[![OneBalance Framework](https://ethresear.ch/uploads/default/optimized/3X/b/9/b9c28cc78642455ccebc698c9de49bf17f43d00a_2_690x388.png)OneBalance Framework2666×1500 481 KB](https://ethresear.ch/uploads/default/b9c28cc78642455ccebc698c9de49bf17f43d00a)

## Resource Locks

A resource lock is a credible commitment made by a user to escrow some state conditional on particular conditions fulfilled, or an expiry time.

An example could be a cross-chain request to purchase an NFT on Solana using USDC deposited in the OneBalance account from Ethereum.

```json
resource_lock: {
	lock: 1500 USDC,
	fulfill: DeGods #12345,
	expiry: Solana block 245547084
}
```

Resource locks are necessary to prevent solvers from being griefed by a user through double spending or equivocating their request during execution.

Since the user makes a commitment not to overwrite their request within a time window, it removes the uncertainty solvers typically incur between a transaction being signed and the finalized chain state.

A lock is analogous to depositing funds in a smart contract, or issuing an ERC20 approval, but without spending gas or waiting for on-chain finality since it is done within the account itself.

The lock expiry needs to be of long enough duration to provide solvers the chance to execute the requested state transition on the destination chain and submit a proof of fulfillment to the fulfillment engine.

Crucially, this introduces a separation between fulfillment time and settlement time. Since the account provides local assurance of the lock, solvers can bring a requested state transition on a destination chain without waiting for finality on the origin chain.

This allows users to buy SOL with ETH at the speed of Solana without being constrained by the speed of Ethereum. This fulfillment speed can be extended to execution of any state transition such as sniping an NFT, sending money to your grandmother, or anything else users do on blockchains.

Resource locks can implement constraints which sit anywhere along the spectrum of permissions.

[![Permission Spectrum](https://ethresear.ch/uploads/default/optimized/3X/c/3/c3a8e48441d80f71c6492fdfd765b4c80ba01467_2_690x228.png)Permission Spectrum3474×1151 201 KB](https://ethresear.ch/uploads/default/c3a8e48441d80f71c6492fdfd765b4c80ba01467)

Permissions could be stateful or stateless. For example:

- Scoped session keys: a stateless permission for an app like a Telegram bot to take arbitrary actions on subsets of a user’s token balances
- Circuit breaker: a stateful permission to sell all open positions if there is no account activity or market volatility above a predefined threshold
- Limit order: a stateful permission to post an order if a pair reaches a certain price on a DEX
- MFA: a stateless permission to post a transaction if two valid authentication methods are provided

## Credible Commitment Machine

A credible commitment machine is a secure computer on which the account lives and is trusted to provide assurances over the valid issuance of resource locks and the validation of their fulfillment.

We present here four possible architectures of credible commitment machines which provide for secure issuance and enforcement of locks: Trusted Execution Environments (TEEs), Multi-Party Computation / chain signatures (MPC), Smart Contract Accounts (SCAs), and in protocol virtual machine changes.

These mechanisms are being developed and refined as we speak, it is likely that the ideal architecture today will look vastly different than the one five years from now.

This is why a OneBalance account allows users to migrate between CCMs over time as they look for better properties.

[![Credible Commitment Machine](https://ethresear.ch/uploads/default/optimized/3X/8/a/8abeab85e3de0dc9203c0882c3d468e7c31ddcc9_2_690x467.png)Credible Commitment Machine2430×1645 232 KB](https://ethresear.ch/uploads/default/8abeab85e3de0dc9203c0882c3d468e7c31ddcc9)

# Roadmap

OneBalance v1:

- add support for transactions and swaps of any token on any chain
- add support for session keys for trusted applications
- add support for user rage quit through exit hatch

OneBalance v2:

- add support for stateless policies
- add support for arbitrary transactions
- add support for authentication modules

OneBalance v3:

- add support for stateful policies

OneBalance v4:

- add liveness guarantees through account replication

|  | EOA | OneBalance v1 | OneBalance v2 | OneBalance v3 | OneBalance v4 |
| --- | --- | --- | --- | --- | --- |
| self-custody |  |  |  |  |  |
| transfers |  |  |  |  |  |
| swaps |  |  |  |  |  |
| session keys |  |  |  |  |  |
| transactions |  |  |  |  |  |
| stateless policies |  |  |  |  |  |
| auth modules |  |  |  |  |  |
| stateful policies |  |  |  |  |  |
| liveness guarantees |  |  |  |  |  |

---

## Acknowledgements

Thank you to the collective consciousness of the crypto ecosystem for fostering a fertile ground for innovation.

In no particular order, thank you to the following collaborators for the many stimulating discussions which lead to the creation of this proposal:

Murat Akdeniz, Ahmed Al-Balaghi, Viktor Bunin, Jonah Burian, Vitalik Buterin, Philippe Castonguay, Vaibhav Chellani, Valery Cherepanov, Jasper De Gooijer, Nicolas Della Penna, Justin Drake, Brendan Farmer, Ben Fisch, Mattia Gagliardi, Johnny Gannon, Matt Garnett, Ivo Georgiev, Christopher Goes, Pedro Gomes, Mason Hall, Sam Hart, Connor Howe, Sreeram Kannan, Hart Lambur, Zaki Manian, Robert Miller, Alex Obadia, Puja Ohlhaver, Anatolii Padenko, Nick Pai, Illia Polosukhin, Karthik Senthil, Tomasz Stanczak, Henri Stern, Alex Stokes, Caleb Tebbe, Dror Tirosh, Dean Tribble, Drew Van der Werff, Alex Watts, Yoav Weiss, Nathan Worsley, Evgeny Yurtae, Philipp Zentner, Noah Zinsmeister, apriori, jxom, awkweb.

## Discussion

### Why are you doing this?

Our mission is to help the web3 ecosystem to transition to an account centric worldview in order to bring web3 to the first 1 billion people.

We believe non-coercive credible commitment machines are essential for human coordination in the digital age.

We believe the chain centric worldview is an outdated framework originating from the historical scarcity in blockspace. ([sorry Joel](https://www.usv.com/writing/2016/08/fat-protocols/))

Much like the shift from the Geocentric worldview to the Heliocentric worldview unlocked a wealth of discoveries, we believe the shift from a chain centric worldview to an account centric worldview will unlock the full potential of web3.

### What does this mean from a user perspective?

Users don’t need to care about which chains they are interacting with + can get close to instant fulfillment.

Lets take a complex, yet common example:

> User wants to buy an NFT traded on Solana with a price of 10 SOL, but only has USDC on Ethereum.

This state transition request requires the following sequential operations to take place:

1. Generate: Create a new Ed25519 keypair in a solana wallet
2. Swap: USDC for ETH to pay for gas on Ethereum
3. Bridge: Send USDC to bridge contract on Ethereum and get USDC minted on Solana
4. Swap: USDC for SOL to pay for gas on Solana
5. Swap: USDC for SOL to purchase NFT
6. Execute: Execute calldata on marketplace to purchase the NFT

Today, users are required to manually perform each of these actions and wait for the previous one to be settled or finalized before performing the following one. Some of these operations are even technically impossible in a non-custodial way using EOAs without chain level gas abstraction.

The critical path of execution here requires waiting for the settlement of two Ethereum transactions and two Solana transactions + waiting for the finality of Ethereum. With Ethereum’s current block finality time, we are looking at a minimum of 15min to complete execution.

Lets look at the equivalent using a OneBalance account:

> User wants to buy an NFT traded on Solana with a price of 10 SOL, but only has USDC on OneBalance.

This state transition request requires the following sequential operations to take place:

1. Create a resource lock on OneBalance as follows:

```json
resource_lock: {
	lock: 1500 USDC,
	fulfill: DeGods #12345,
	expiry: Solana block 245547084
}
```

There are no additional steps for the user to take.

Behind the scenes, a solver purchases the NFT and credits it to the OneBalance proxy account of the user on Solana, and claims the resources in the lock.

Since a OneBalance account separates fulfillment from settlement, the user gets execution at the speed of transaction execution on their destination network, in this case Solana. The user can perform any operation on any chain using any token they hold in their OneBalance account.

### Show me some sequence diagrams.

Ok.

Lets walkthrough a few examples on how interoperability is achieved under different conditions:

1. The user has EOA account and wants to do a cross-chain contract call while not having gas on target chain

The user signs two transactions using their EOA, the first transfers gas amount from the origin chain to the solver escrow address and the second calls the contract on the target chain.
2. As soon as the solver simulates these two transactions, they have a guarantee that the user will pay them the correct gas amount (user’s commitment is enforced).
3. The solver instantly funds user’s EOA account on the target chain, and executes the contract call transaction without waiting for settlement or finality of first transaction.
4. The solver can include the first transaction (gas payment) within the expiry window of commitment.

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/3/13a5cb8d20d6ab799b12095e82e6bbed0147e295_2_517x265.jpeg)image2788×1434 258 KB](https://ethresear.ch/uploads/default/13a5cb8d20d6ab799b12095e82e6bbed0147e295)

1. The user has Smart Contract account and wants to do a cross-chain swap while not having gas on target chain.

The user signs a UserOp authenticating the transfer of required tokens to the solvers escrow address.
2. As soon as the solver simulates the transaction, they have a guarantee that the user will pay them the required tokens (user’s commitment is enforced).
3. The solver procures the required tokens on the target chain and deposits them into the users account on the target chain without waiting for settlement or finality.
4. The solver can include the UserOp (token deposit in escrow) eventually.

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/6/4620414fdd10e1da61a13fb84436b2daa33a49c2_2_517x260.png)image2817×1419 319 KB](https://ethresear.ch/uploads/default/4620414fdd10e1da61a13fb84436b2daa33a49c2)

As we can see in the above examples a user commitment via nonce lock is same as delegating eventual state update to solvers. This reduces latency introduced by finality especially in a cross-chain setting.

### How does this relate to account abstraction and 4337?

Account abstraction and 4337 are often associated with Smart Contract Accounts and refer to both the set of UX improvements offered by an SCA (account abstraction) and a specific standard for implementation of these UX improvements (EIP-4337).

The OneBalance account model provides the same UX improvements as SCAs and is backwards compatible with using 4337 for settlement of locks on chain as user ops.

However, since OneBalance is a general framework for the creation of credible accounts, it is not limited to chains where account abstraction and 4337 are actively being used.

OneBalance is supportive of chains and proxy accounts which opt for using dos resistant user ops like 4337.

### How do you guarantee atomic asynchronous execution across chains?

We can’t. But we can incentivize it.

Accounts can enforce two types of constraints:

- Constraints over what states of the world it requires in order to issue a lock
- Constraints over what states of the world it requires in order to fulfill a lock

OneBalance can *incentivize* atomicity, but it cannot guarantee it.

- For example: Take a lock that requests sequencing of state transitions across chain A and chain B, with a desired atomicity such that B is executed if and only if A is executed. If the lock is public and the only condition on inclusion of B is the existence of a valid signature from the requesting account, then B could be included regardless of A if it exposes sufficient MEV to compensate its inclusion.

However! Since executing B without A invalidates the fulfillment conditions of the lock, then the solver cannot extract any value from the lock. This means that from the user perspective, atomicity is maintained. Some people refer to this as “economic atomicity”. For locks with complex multi chain atomicity requirements, Solvers take on the risk of non-execution.

This “lock leaking” due to MEV problem can be resolved at the routing layer by routing the state transition request through a secure OFA that prevents information leakage.

Novel mechanisms are being developed at the settlement layer to help solvers manage their settlement risk using things like pre-confirmations or proof aggregation. Importantly, these help manage solver execution risk and therefore help minimize non-execution risk for users of a OneBalance account, but the OneBalance account already has economic atomicity guarantees.

### Is OneBalance just HTLCs for Ethereum?

I prefer to call it turbo HTLCs ![:grinning_face_with_smiling_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face_with_smiling_eyes.png?v=14)

The design of intent bridges work similarly to HTLCs in that they lock user funds on the originating chain until a proof is provided of the completion of a state transition on the destination chain.

Instead of being constrained by the speed of the originating chains, OneBalance accounts are constrained by the speed of the credible commitment engine in generating these locks. This means that on a TEE architecture, locks can be issued at clock speed of a single server, hence turbo HTLCs!

### How does this thing scale to one billion concurrent users?

OneBalance accounts create “local” locks, whereas regular accounts can only create “global” locks. Global locks require locking the state of all accounts in the execution environment during sequencing, whereas local locks only require locking the state of accounts which are party to the lock.

Unlike global locks, local locks provide the opportunity for lock sequencing to be parallelized on distinct machines.

### Where does the account live?

The account lives in a secure computer of the users choice that can make credible commitments about what messages it will and won’t sign.

The four architectures for credible commitment enforcement presented above provide such environments, but each have their tradeoffs. OneBalance accounts are not opinionated to the type of credible commitment enforcement mechanism used.

Crucially, as the sophistication of these architectures evolve over time, the tradeoff space will change and so will user preferences. As such, OneBalance accounts must remain flexible to supporting different architectures.

### Is OneBalance a standard?

No.

OneBalance is a framework for building accounts on top of credible commitment machines. OneBalance will use the standards developed by the [CAKE Working Group](https://frontier.tech/cake-working-group) plug and play with all components of the CAKE stack.

### Are you providing pre-confirmations?

No. OneBalance provides resource locks.

Lets explore the difference between the two.

Pre-confirmations is a mechanism being actively developed by several teams in the ecosystem to offer better inclusion guarantees for entities sending transactions to the blockchain.

Resource locks is a mechanism for offering guarantees to solvers that a user cannot double spend or equivocate on their state transition request.

Both mechanisms are aimed at reducing the execution risk of solvers, pre-confirmations are guarantees provided by proposers, resource locks are guarantees provided by users.

Both pre-confirmations and resource locks can be enforced by the same credible commitment mechanism.

For example: If Ethereum validators were to deposit their staked ETH in a OneBalance account, they could create resource locks which specify slashing rules if certain transaction inclusion commitments are invalidated. This could be implemented with a restaking contract like eigenlayer.

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/c/4c3e7151fe217186184497d8a2de952f5383661d_2_345x107.png)image3587×1114 138 KB](https://ethresear.ch/uploads/default/4c3e7151fe217186184497d8a2de952f5383661d)

### How does a lock turn into a state transition on chain?

OneBalance accounts are responsible for issuing and enforcing resource locks over state transition requests.

Routing of the request in order to provide fulfillment is a downstream module which the upstream app / user must define. For certain kinds of requests, it may be beneficial to route directly to a chain’s transaction pool, other requests may benefit from using a solver network or orderflow auction, and others from specifying an exclusive solver.

OneBalance is unopinionated about the routing mechanism.

### Is OneBalance a competitor to (insert my bags here)?

Probably not.

OneBalance is providing a framework for orchestration of stateful accounts. Our goal is to displace the industry wide reliance on imperative state transition requests issued by user managed EOAs. OneBalance is not opinionated on the architecture of the stateful accounts or the credible commitment mechanisms used to secure them.

OneBalance uses a modular architecture that allows for the following components to be integrated:

1. Orderflow sources: wallets / apps / tg bots / waas
2. Fulfillment engines: orderflow auctions / solvers / solver networks / market makers / intent networks / bridges
3. Settlement engines: any L1 or L2 (yes, even BTC)

The design for OneBalance emerged from our work with members of the [CAKE working group](https://frontier.tech/cake-working-group).

Looking at the CAKE framework, OneBalance sits between the permissioning layer and the solver layer and is compatible with all the other necessary components of the cake.

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/4/44ee9a1604244965ad249dee7879f0b982740679_2_291x375.jpeg)image1763×2267 143 KB](https://ethresear.ch/uploads/default/44ee9a1604244965ad249dee7879f0b982740679)

### Are OneBalance accounts custodial?

No.

All OneBalance accounts are issued withdrawal receipts which allow them to permissionlessly exit their assets back to the settlement chain where the assets originate.

This means at any point, a user is able to “rage quit” and recover their assets on the source chain.

This mechanism is implemented differently depending on the accounting engine used, but essentially boils down to the same outcome: users can withdraw their funds by submitting withdrawal receipts to their proxy accounts on origination chains.

I firmly believe freedom of exit is an essential characteristic of non-oppressive human coordination system design. I have never and will never design a system without freedom of exit.

### Are OneBalance accounts really compatible with any chain?

Kinda.

All chains are supported, but the capabilities differ based on the VM used and the fulfillment speed differs based on the consensus. More details on this in the future.

### Are OneBalance accounts vulnerable to vampire attacks?

Yes. This is a good thing.

If someone can build a system which delivers higher combined utility (functionality + economic incentive) to users than OneBalance accounts, users should be able to exit. This is necessary to avoid anti-competitive monopolies that censor innovation.

To whoever wants to try, I say bring it on.

### Is this a ?

No.

As they are defined today, a keystore rollup solves the problem of having a central source of truth for account permissions, across all chains. It doesn’t offer cross-chain guarantees to solvers. A OneBalance account does not need a keystore rollup since on chain keys don’t change.

If a Keystore Rollup was to attempt to issue locks, they could only be communicated at L1 finality speed.

### What is the trust model?

Instead of requiring mutual trust between users and solvers, the OneBalance model requires each party to trust the credible commitment mechanism used to issue and enforce resource locks.

### Does OneBalance remove the need for bridges?

No.

Bridges are necessary mechanisms to provide fulfillment of locks and settlement of inventory outside of the critical path of user request execution.

### What is the relationship between Frontier Research, OneBalance, and the CAKE Working Group?

[Frontier Research](https://frontier.tech) is and remains an independent research and advisory group formed to bridge the gap between fundamental research and commercial products.

Frontier founded the [CAKE Working Group](https://frontier.tech/cake-working-group) along with other collaborators such as Anoma, Across, and Ethereum Foundation members to foster conversation around common interfaces and language to accelerate the development of chain abstraction technology.

Frontier is spinning out OneBalance as an independent project to accelerate the transition of an account centric worldview for web3.

All three groups of humans will continue to follow their individual missions moving forward.

### What are the latency and consistency guarantees of this account model?

wip

### How do you prevent sequencer DOS?

wip

### How does a OneBalance account recover from a fault in an underlying chain?

wip

### How quickly can lock resolution take place?

wip

### Is this a new kind of blockchain?

wip

### What are the benefits and drawbacks of using a OneBalance account vs a Smart Contract Account?

wip

### Can you build complex applications like a dex on top of resource locks?

wip

## Replies

**amanraj1608** (2024-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegostep/48/7751_2.png) thegostep:

> If a Keystore Rollup was to attempt to issue locks, they could only be communicated at L1 finality speed.

Let’s say if the commitment machine is SCA, Isn’t the best design for resource lock is similar to(can be achieved with) minimal keystore rollup approach? How would the commitment make sure to hold the funds on ETH without finality on ETH and solver buy on Solana?

Relying on soft commits can be a security concern here.

---

**jgcogsystematictradi** (2024-05-15):

How do TEEs provide the best DOS resistance?

---

**tomarsachin2271** (2024-05-16):

> A credible commitment machine is a secure computer on which the account lives

Does the private key of EOA is stored on this ‘commitment machine’ and who’ll be running this secure computer?

Is it correct that all the state changes on this One Balance account has to go through this secure computer?

Is it also correct to imagine this commitment machine as a new chain where you create your account and deposit funds from different chains and then issue locks to certain solver and then trust this machine that it’ll given permission to solver to take the funds only if the commitment is fulfilled on destination chain and then release the lock?

---

**AhmedBalaghi** (2024-05-16):

Assuming this commitment machine can’t just be a blockchain (as we have today). Would the Credible Commitment Machine interact with or be a completely new execution environment that has these locking mechanism implemented and has ability to have granular locks on individual assets?

Where are these resource locks essentially made?

---

**zincoshine** (2024-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegostep/48/7751_2.png) thegostep:

> Each OneBalance account can be thought of as its own rollup. The account wraps individual user state from all chains and replicates it in a virtual environment.

Do you recommend storing the user’s state across all chains as a verkle trees?

Also, in theory, the credible commitment machine can be a micro-rollup, no?

---

**thegostep** (2024-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/zincoshine/48/16293_2.png) zincoshine:

> Do you recommend storing the user’s state across all chains as a verkle trees?

Can you share advantages of doing this vs regular merkle trees for this particular use case?

![](https://ethresear.ch/user_avatar/ethresear.ch/zincoshine/48/16293_2.png) zincoshine:

> the credible commitment machine can be a micro-rollup, no?

Yes ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**thegostep** (2024-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/tomarsachin2271/48/16287_2.png) tomarsachin2271:

> Does the private key of EOA is stored on this ‘commitment machine’ and who’ll be running this secure computer?
> Is it correct that all the state changes on this One Balance account has to go through this secure computer?

Yes, the key of the user needs to be hosted on this commitment machine and the user cannot bypass it except to rage quit from the system. This is necessary in order to maintain the credible properties of the system. We propose four different architectures for running this secure computer.

---

**zincoshine** (2024-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegostep/48/7751_2.png) thegostep:

> Can you share advantages of doing this vs regular merkle trees for this particular use case?

I am no expert. However, the best reason I can think of, is smaller proof size.

---

**EugeRe** (2024-05-17):

Great research, I am doing a lot of research in the identity space and in the sequencing network! I would like to be in touch.

---

**kanthgithub** (2024-05-18):

Question-1:

Is this similar to the DWN (Decentralised Wallet Network) where the key pair is generated by the nodes (delegated MPC signers) in the network and the tokens of the user are to be held in that account?

through this approach , User is prevented from spending the tokens which are resource locked?

Question-2:

What is the OneBalance Proxy account on each chain?

referring to the use case mentioned where it says

> Behind the scenes, a solver purchases the NFT and credits it to the OneBalance proxy account of the user on Solana, and claims the resources in the lock.

---

**jdetychey** (2024-05-21):

Exciting stuff, the Cometh team would love to join the CAKE working group ([ref documentation of our SDK](https://docs.cometh.io/connect)). We did a lot of contributions on passkey signers and more recently on storage proofs that could be leverage in the proof of fulfillment.

---

**EugeRe** (2024-05-21):

Which is the best way to connect with Frontier Research or CAKE community? I’d like to contribute.

---

**rahul-kothari** (2024-05-22):

How do you think about solver decentralization? In most dapps that use solvers today,t hey are all whitelisted due to trust assumptions. Do you see onebalance v1 start with whitelisted solvers and eventually move to permissionless? Or do you see them as keeper nodes?

---

**yosui** (2024-05-22):

I’m Yosui, the Co-founder of Mycel, an Account Transfer Protocol. I agree that the Chain-centric worldview doesn’t match the era of millions of rollups. I believe that an approach that allows users to interact without being conscious of finality is extremely important, assuming that it will bring a billion users into the Ethereum ecosystem.

With a similar awareness of the issue, we have taken an approach inspired by Anoma’s Anoma Resource Model, which involves exchanging encrypted secret keys. We are building a project that realizes small-scale accounts called Fragmented accounts, which are like checks from the original account, using ZKP and TSS. By swapping the owners of these Fragmented accounts, we enable the exchange of value on any on-chain platform without being conscious of the finality of each chain.

I felt that the OneBalance model and Mycel’s Fragmented account approach have a similar worldview in terms of truly pursuing user convenience, seeking methods that do not depend on finality, and focusing on accounts.

The Fragmented approach is positioned in the Settlement layer of the CAKE Framework. I thought that by using the OneBalance model and abstracting the gas costs incurred when swapping account owners of Fragmented accounts, it could be used for this purpose.

Also, since Mycel’s Fragmented account approach swaps secret keys containing already settled tokens, it might be a solution for providing Atomicity to the OneBalance model when desired.

---

**tirtha4** (2024-05-22):

Are the solvers an offchain entity or a smart contract as well?

Is there any proof that needs to be generated to verify that the simulation of transactions witnessed/validated by the solver is genuine?

---

**thegostep** (2024-05-23):

Great question. We describe some of the tradeoffs between different approaches to solver selection in our research posts [Frontier Research: The Orderflow Auction Design Space](https://frontier.tech/the-orderflow-auction-design-space) and [Frontier Research: Introducing the CAKE Framework](https://frontier.tech/the-cake-framework).

The TLDR is that information leakage and non-execution risk leads to a need for whitelisting solvers in order to provide a good user experience.

I expect resource locks and credible accounts more generally to open up a design space for solver selection mechanisms which do not rely on IRL legal agreements.

---

**tomarsachin2271** (2024-05-23):

How does this commitment machine ensure that the user’s intent has been fulfilled by any solver (Eg how to prove the the solver actually bought the NFT to user’s address)?

Can commitment machine just query the other chain while the execution is taking place on this commitment engine while the funds are locked? Or solver will need to submit any cross chain proof that they fulfilled the commitment?

---

**thegostep** (2024-05-23):

When issuing a resource lock, the user must specify the fulfillment conditions. This include the oracle / proof mechanism used to validate the necessary state transition has taken place on the destination chain.

---

**k06a** (2024-05-29):

Anyone considered efficient EVM implementation?

---

**otrsk** (2025-03-20):

How are resource locks compatible with vanilla ERC-20s for anti-equivocation on the source chain?

