---
source: ethresearch
topic_id: 17125
title: Booster rollups - scaling L1 directly
author: Brecht
date: "2023-10-18"
category: Layer 2
tags: []
url: https://ethresear.ch/t/booster-rollups-scaling-l1-directly/17125
views: 6640
likes: 24
posts_count: 10
---

# Booster rollups - scaling L1 directly

# Definition

Booster rollups are rollups that execute transactions as if they are executed on L1, having access to all the L1 state, but they also have their own storage. This way, both execution and storage are scaled on L2, with the L1 environment as a shared base. Put another way, each L2 is a reflection of the L1, where the L2 directly extends the blockspace of the L1 for all applications deployed on L1 by sharding the execution of transactions and the storage.

# What

Rollups are commonly seen as their own separate chain, being almost completely independent from their host chain and their peer rollups. Designs have been [proposed](https://ethresear.ch/t/cross-layer-communication-trivially-provable-and-efficient-read-access-to-the-parent-chain/15396) to bring L1 data to the rollup in an easy way, but on its own that still fails to create a uniform environment that can scale Ethereum in a convenient way. If the future demands hundreds or even thousands of rollups to adequately scale Ethereum, having each rollup function as an isolated unit, with its own set of smart contracts and rules, is not ideal. Developers would have to copy-paste their code onto each rollup. Instead, a rollup could directly add extra blockspace to all dapps deployed on L1. Deploying a rollup could be something like adding extra CPU cores and an extra SSD to a computer, with applications capable of taking advantage of these automatically doing so. Similar to multi-threaded applications, the dapp does need to be aware of this to be able to take full advantage of this multi-rollup world.

# Advantages

- increases scalability in a transparent way: Similar to adding extra servers to a server farm, the only thing required is adding an extra rollup and all applications can take advantage of the increased scalability, no extra steps required.
- uniform: L1 and all L2s look and feel exactly the same for users. All smart contracts automatically have the same address across L1 and all booster rollups.
- easy for developers: No need to deploy to all L2s that need support for the dapp. Just deploy your smart contracts to L1 and you’re done. Each dapp is multi-rollup out of the box. Rolling out updates can now also be done in a single place, with for example all L2s automatically following the the latest version on L1.
- easy for users: A single address everywhere, automatically, no matter if it’s an EOA or smart wallet. Each smart wallet is automatically an L1 and multi-rollup smart wallet that the user can use to transact on L1 and on all L2s.
- easy for rollups: No need to try and get app developers to deploy their dapp on your rollup. All dapps are automatically there (though it still requires to get developers to do some minimal offchain work to make it easily accessible to users, like UI things and changing RPC URLs). The goal now shifts to getting developers on board to write their dapps in the best way to take advantage of multi-rollups.
- stackable: Combine a booster rollup with a based rollup and a way to do atomic cross-rollup transactions between all L2s in this booster network, and we’re doing some serious Ethereum native scaling which I like to unironically call The Singularity and you can’t stop me. This combination should get very close to the feeling of a single scalable chain for users. Not all L2s in this shared network need to be booster rollups, they can be combined with non-booster rollups as well.
- sovereignty: No need for rollup specific wrapper contracts for things like tokens, each smart contract runs on L2 exactly the same way on L1 in all cases, the original developer remains fully in control.
- security: No more rollup specific implementations to bridge functionality over from L1 also means no single point of failure anymore (like bridges with a shared codebase where a single hack can be catastrophic). The security is now per dapp.
- simple: For rollups that are Ethereum equivalent, the only additional functionality to be a booster rollup is to support what the L1CALL/L1DELEGATECALL precompiles do in some way.

# Disadvantages

- contract deployments need to be disabled on L2: It needs to be ensured that the L2 keeps mirroring the L1 in all cases (so SELFDESTRUCT is also a no-go, but that is already going away). For that to be true, contracts can only be deployed on L1, which also makes sure all L2s have access to it. Note that this is not really a big limitation because this doesn’t mean that each L2 needs to be behave exactly the same everywhere. It’s perfectly possible for smart contracts to behave differently depending on which L1/L2 the user is interacting; it just needs to be done in a data driven way. For example, the address of the smart contract being called by another smart contract could be stored in storage. Because storage can be different between L1/L2s, the behavior of this smart contract can vary depending on which chain it is being executed on.
- contract code and shared state is still on L1: The L1 is still used for the shared data, and so there is no direct increase in scalability for this. But that seems like an inherit limitation of any scalable system, it’s up to app developers to minimize this as much as possible.
- not all dapps are parallelizable: Similar to normal applications, not all of them are easily parallelizable in which case they cannot take full advantage of the shared/seperate storage model. But that’s okay, smart contracts like this still scale on all the different L2s separately which is the status quo. And there’s still the big advantage of the smart contract being available on all L2s automatically. This is also why it’s still very important that users can seamlessly do transactions with smart contracts on any of the L2s in the network, no matter where the transaction originates, because e.g. some dapps may run their main instance on a specific L2, or have the most liquidity available there (like the uniswap pool for a specific trading pair).
- L1 and L2 nodes have to run in sync, with low latency communication: Booster rollups basically are the L1 chain, they just execute different transactions and have some additional storage of their own. A possible implementation could be to actually run both L1 and the L2 in the exact same node with just a switch deciding to use either the shared L1 storage or the L2 specific storage while executing the transactions.

# How

All accounts on a booster rollup would have a fixed smart contract predeployed to them:

```auto
contract L2Account {
   fallback() external {
       // Check here if the smart contracts implements the expected interface.
       // If not, default to parallelize everything.
       // Check if the function being called supports parallelization
       if (address(this).l1call(isParallel(msg.sig)) {
           // Execute the call with the L2 state
           address(this).l1delegatecall(msg.data);
       } else {
           // Execute the call with the L1 state
           address(this).l1call(msg.data);
       }
   }
}
```

(Note that EOAs are not handled in this code)

Each smart contract decides for itself (using the code deployed on L1, which optionally implements a very easy interface, otherwise it falls back to using the L2 state exclusively so the dapp runs completely on L2) which parts of its code need to be run with the state stored on L1 (L1CALL) which need to run with the state stored on L2 (L1DELEGATECALL). The state stored on L1 is the shared state, the state stored on L2 is the state that can be parallelized (e.g. token balances or specific uniswap pools).

Handling EOAs correctly here is challenging without additional precompile magic. Using this implementation using standard smart contracts also changes the gas cost of the execution compared to L1, so it is not ideal. In practice this logic would probably not be done in a smart contract, but would be built into the logic of the rollup instead so that it can be made fully transparent.

A simple example to make sense of this: for a token contract, the total balance would be stored on L1, but all user balances and transfers would be done in parallel on L1 and all L2s.

# Booster enabled rollups

Any non-booster rollup that supports the L1CALL/L1DELEGATECALL precompiles also supports boosting, but that now requires deploying this smart contract to each L2 manually per dapp.

## Replies

**Perseverance** (2023-10-18):

Neat idea that extends on the `L1CALL` concept you’ve proposed recently. I can see a lot of benefits in this one. Here are the two things that would worry me the most.

Firstly, this pattern is quite similar to the `ThinProxy` upgradability patterns for smart contracts. In here the L1 contract is the implementation logic, each L2 is the storage proxy and the two communicate via `L1CALL` instead of `delegatecall`.

In many cases with this pattern, there is a need to set up some “creation time” parameters - circumventing the lack of a constructor. I can see the sam being applicable here. This means that any contract deployed on L1 would need to trigger an init-like function on L2. This function becomes an additional dependency to be supported by the smart contracts developers.

Furthermore, this init-like behavior might open up a massive attack vector, where malicious attackers monitor L1 and trigger the init of every contract in L2. The issue gets exacerbated the more booster rollups there are. Take for example a wildly popular DEX supporting such parallelism. As soon as someone launches a new booster rollup, the DEX developers need to go and trigger init before anyone else does.

Fighting this, you can do some magic in the L2 where for some parts of the logic you use the L1 state and for others the L2 state. This, however, requires a quite significant rewrite of the app in order to provide these indications to the booster rollup.

My second worry is around the practicality of requesting existing dapps to include the new interface indicating parallelization. A similar need and assumption existed back when the meta-transactions/gas-abstraction initiative was started (2018. I’m old now LOL). Multiple prominent teams built a thing called GSN - Gas Station Network in order to make meta transactions work. All that was required by dapps was to add a single solidity modifier in order to enable smart wallets and meta transactions. In practice, very few dapps did so. This initiative is the predecessor of the current Account Abstraction initiative, that is now specifically designing around the need to change existing and future dapps. My point is - it is an uphill battle to persuade dapps to include an interface.

Overall Im very bullish on the concept of L1CALL for type 1 rollups, however I think the booster rollups concept needs further refinement and flexibility in order to account for practical issues.

---

**Brecht** (2023-10-18):

Thanks for the feedback!

Certainly agree that this will not work for all smart contracts out of the box, but I think that should be okay. For smart contracts that don’t signal support in some way it could even be disabled on L2 to prevent anything from going wrong.

For the first point, it does need some taking into account for developers. But the way to tackle this should be quite straightforward depending on what kind of data needs to be set (though of course current smart contracts may need some updating to correctly support this):

- Ideally the init state is indeed just read from the L1 smart contract, and so either the init function doesn’t have to be called on L2, or it can be called by anyone and the function just uses the L1 data to set the same initial data on L2.
- If for some reason no automatic method can be applied because it requires L2 specific data, then some address can be hard-coded/stored on L1, and only that address is allowed to call the init function.

The additional interface that ideally is implemented, I agree it will be challenging. Though it is optional and should be very easy to do, developers would need to take into account how this setup works to make the most of it, and there could be issues like the ones described in your first point. But the main argument would be that the alternative would be worse. Developers may not initially have wanted to write applications for a multi-core CPU, hoping that a single core would keep getting faster and faster, in practice though that didn’t work out. As long as it’s very easy to define the rules that makes things at least compatible, and developers see the benefit of this design (it should save them work), I have some hope.

With some additional proxy magic, support for already deployed dapps on L1 could be added by any developer without needing to update the already deployed smart contract on L1, which would then be the contract used on all L2s.

---

**charlieflipside** (2023-10-20):

> If for some reason no automatic method can be applied because it requires L2 specific data, then some address can be hard-coded/stored on L1, and only that address is allowed to call the init function.

At a high level, this could simply be the Deploying EOA? which is already going to match across all EVM L2s.

Small thing that isn’t clicking for me is Factory contracts. A booster rollup sounds great for de-fragmenting liquidity. But it doesn’t really work for example for liquidity pools where the same canonical tokens aren’t given the same address across instances (e.g., USDC). (Repeat Perseverance’s point on init-like behavior).

If the L1 state needs to be updated, where are the cost reductions for the booster roll-up (L2 is cheaper explicitly b/c it is fragmented)?

---

**Brecht** (2023-10-20):

> At a high level, this could simply be the Deploying EOA? which is already going to match across all EVM L2s.

You could indeed do some tricks to figure out who could be authorized to initialize the smart contract on L2 on some historical L1 data, which could work very well for some standard contract deployment configurations. But it seems tricky to find something that would really work in all cases I think.

> Small thing that isn’t clicking for me is Factory contracts. A booster rollup sounds great for de-fragmenting liquidity. But it doesn’t really work for example for liquidity pools where the same canonical tokens aren’t given the same address across instances (e.g., USDC). (Repeat Perseverance’s point on init-like behavior).

For pure booster rollups, transactions that deploy smart contracts will fail because smart contract deployments aren’t allowed. So you can only use factory contracts on L1, and so automatically on L2 they are the same because they are inherited from L1. Which does mean that the deploying of smart contracts doesn’t scale more than just L1, but all the actual activity on those smart contracts can move to any of the booster rollups. If a rollup wants to also scale smart contract deployments, it will have to do so in a non-booster rollup and use manually boosting where wanted.

> If the L1 state needs to be updated, where are the cost reductions for the booster roll-up (L2 is cheaper explicitly b/c it is fragmented)?

The L1 is the shared data, so booster rollups, and I guess just in general, cannot scale that data because that data needs to be available everywhere. The cost reductions on L1 come from all the non-shared activity moving to the L2s.

---

**charlieflipside** (2023-10-20):

Gotcha, so I guess I’m asking for a practical example to scope the benefits. An ETH-USDC 0.05% wouldn’t exist on the Booster (no SC deployment). The L1 ETH-USDC 0.05% pool wouldn’t have cheaper state updates (i.e. trades).

But you could for example have a trustless binary options market that uses the L1 price data as a pure on-chain feed, where settlement (price above X at timestamp) happens in the segmented booster storage.

Is that the right way to think about it?

---

**Brecht** (2023-10-20):

If the L1 ETH-USDC pool exists on L1, it automatically also exists on the booster rollup right? Unless I’m missing the point  you’re trying to make here.

Because AMMs themselves are not easily scalable, I would see all the liquidity for a certain pool moving to one of the booster rollups. So the work for AMMs would be spread across the L2s organically based on where the most liquidity is for a specific trading pair, but in theory all the pools could be used on any of the booster rollups because the necessary smart contracts are there for all of them.

More complex parallelization methods would need to be done on an app by app level. For AMMs specifically there have been some [efforts](https://ethresear.ch/t/damm-an-l2-powered-amm/10352).

---

**0xapriori** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/brecht/48/4820_2.png) Brecht:

> sovereignty: No need for rollup specific wrapper contracts for things like tokens, each smart contract runs on L2 exactly the same way on L1 in all cases, the original developer remains fully in control

good write-up, thanks.

do you anticipate rollup community formation to change in the singularity; e.g., communities forming around booster/stacked booster rollups vs. the socially sovereign communities which comprise part of the rollup landscape today - Optimism or Arbitrum dao for example?

---

**Brecht** (2023-12-02):

Hard for me to predict. I think in L2 communities there’s already a focus on both the L1 and L2, perhaps with direct L1 scaling solutions the focus will shift even more to the L1 part instead of the L2 specific part. Perhaps similar to linux distributions where things are mostly up to the preference of users which distribution they use, and they could easily switch between which flavor one use, because the linux part is the main thing. For linux the differences between the distributions are still significant enough to build strong communities around them, I would think the same would be true for different rollups.

---

**jaguard2021** (2024-01-31):

The challenge of deciding which parts of smart contract code should be executed on L1 or L2 requires a deep understanding of how smart contracts function and efficient implementation. It also necessitates significant changes to existing smart contracts.

