---
source: ethresearch
topic_id: 23437
title: "EIL: Trust minimized cross-L2 interop"
author: yoavw
date: "2025-11-13"
category: Layer 2
tags: []
url: https://ethresear.ch/t/eil-trust-minimized-cross-l2-interop/23437
views: 3054
likes: 50
posts_count: 18
---

# EIL: Trust minimized cross-L2 interop

# EIL: Trust minimized cross-L2 interop

## Executive summary

Ethereum’s rollups brought scale, but fragmented the user experience. Today, each L2 feels like an island with its own gas, bridge, and sometimes even wallet. Moving between them breaks the seamless, trustless UX Ethereum was meant to offer.

There have been many attempts to unify the L2 user experience, but they often compromise on Ethereum’s core values:

- Less censorship resistance - transacting through intermediaries.
- Less security - trusting 3rd parties with funds or state attestation.
- Less privacy - exposing the user’s IP address and/or intention to 3rd parties.
- Less open source - most logic runs on a 3rd party server, often opaque to users.

We want the UX of a single chain, the security and censorship resistance of Ethereum, with the scalability, price, and speed of the L2 ecosystem. This post will talk about the **Ethereum Interop Layer (EIL)**, an interop standard that aims to provide exactly that.

The Ethereum Interop Layer (EIL) makes Ethereum’s rollups feel like a single, unified chain by enabling users to sign once for a cross-chain transaction without adding new trust assumptions. Built on ERC-4337 account abstraction and the principles of the [Trustless Manifesto](https://trustlessness.eth.limo/general/2025/11/11/the-trustless-manifesto.html), users themselves initiate and settle cross-L2 actions directly from their wallets, not through relayers or solvers. EIL preserves Ethereum’s core guarantees of self-custody, censorship resistance, disintermediation, and verifiable onchain execution. This new account-based interoperability layer unifies Ethereum’s fragmented L2 ecosystem under Ethereum’s own security model.

## The vision

### UX: Multichain feels like single chain

Arbitrum Alice wants to send 0.1 ETH to Base Bob. Alice pastes Bob’s address into her wallet and sends 0.1 ETH, her wallet figures everything out and Bob receives the funds within seconds.

We want this kind of clean user experience not just for moving around ETH and ERC20s, but also for more complicated operations (eg. multichain calls, cross-chain swaps). Alice should be able to pay fees in one place using any asset, and sign once per operation, not once per chain. Latency should be as low as possible.

### Security & privacy: Censorship resistance, no trusted intermediaries

Alice and Bob should not have to trust any third party for **liveness**, **safety** or **privacy**. That is:

- There should be no “enshrined” actor that the protocol depends on in order to operate.
- Liquidity providers or other actors should not be able to steal Alice’s funds. Security assumptions should be the same as the underlying chains.
- Liquidity providers or other actors should not even be able to freeze Alice’s funds, even for a short duration. If one liquidity provider disappears halfway through a trade, others should be able to come in and finish the job.
- There should be no server that Alice or Bob (or even liquidity providers) need to ping, leaking their IP address. The only thing that they should need to talk to is RPC nodes of the L1/L2s, and possibly a p2p mempool.
- Liquidity providers should not learn ahead of time details that could allow them to sandwich or otherwise exploit Alice.

## Background

### Why general purpose censorship resistant intents are hard

At first glance, intent solvers seem like an easy path to cross-chain UX. But permissionless and decentralized solvers face structural DoS and griefing risks.

For example:

- Sybil could deploy malicious contracts on the destination chain and send many intents that use them, causing the solver to unexpectedly revert on chain and not get paid for them.  Solvers will have to mitigate by whitelisting contracts. E.g. support only a closed list of known tokens. This happened to MEV searchers: initially they automatically used every ERC-20, then they got salmonella and within hours they all switched to whitelists.
- General purpose intents can be arbitrarily complex and it’s hard to verify their results. Oscar could run malicious solvers that fulfill intents in unintended ways, causing Alice to pay and not get what she wanted. For example a solver could call the requested contract with insufficient (but marginal) gas, causing an inner frame to revert while the rest of the intent succeeds.  Mitigating each such attack is easy, but mitigating all possible attacks for every possible intent is hard.  Protocols might mitigate by whitelisting known-safe intent types.
- Oscar’s solver could decompose a multichain intent, perform the actions on one chain but not on another. The solver doesn’t get paid but the user is stuck in a limbo state which Oscar may benefit from.  Intent protocols might mitigate by whitelisting solvers.

Protocols that whitelist solvers or users are not censorship resistant.

Protocols that whitelist contracts or intent types are not general purpose and require work to support every new use case. The added friction for supporting new use cases might become de-facto gatekeeping.

Since the solver must execute arbitrary logic on untrusted contracts, full censorship resistance and generality are fundamentally in tension.

### Why crosschain privacy is hard: the Privacy/Safety/UX trilemma

Submitting an intent reveals the user’s intended outcome ahead of time - what the user is going to do on each chain.  It often also require interacting with an offchain service, associating the user’s IP address with the intent.  This has privacy implications.

**Example 1:**

Arbitrum Alice wants to donate to a controversial cause on Scroll.  She reaches out to solvers, they reject her, or say ok but not actually deliver.  They do log her IP address and associate her real world identity with the cause.

She could instead separate the donation to two transactions: 1. Send funds to her own Scroll address.  2. Send the donation on Scroll.  She won’t be censored in this case but her IP is still associated with the donation due to 1, and her UX is degraded - she has to sign two transactions for one operation.

**Example 2:**

Base Bob wants to bid at an auction on Arbitrum.  He doesn’t want to associate his IP address with the bid, but also doesn’t want to reveal his intent to bid due to frontrunning safety.

- If he uses an offchain intent protocol and a reputable solver, he’s relatively safe from frontrunning but the solver now knows his IP.
- If he uses an onchain intent protocol to avoid connecting to a solver, his IP stays hidden but gives up safety - his action is revealed to frontrunners.
- If he splits the operation into two transactions, sending funds to Arbitrum and then signing another transaction for the actual bid, he is safe from both risks, but UX is degraded.

This presents a trilemma: **{Privacy, Safety, UX} — pick 2 out of 3**

| Choice (what you optimize for) | Example approach | What you lose |
| --- | --- | --- |
| Privacy + UX | On-chain intent protocols (fully public mempool execution) | Lose front-running safety - transactions can be observed and exploited before inclusion. |
| Safety + UX | Reputable off-chain solver networks (private matching and execution) | Lose privacy - users reveal intent details and metadata like IP address, which can link their blockchain address and real-world identity to a centralized or semi-trusted solver. |
| Safety + Privacy | Split flow: on-chain intents only for transfers, send calls separately | Lose UX - high latency, multiple signatures, and fragmented user flow. |

*Takeaway:* full censorship-resistant, privacy-preserving, safe, and seamless intent execution is currently impossible without introducing some trust assumption or UX degradation.

A well designed crosschain protocol should aim to solve this trilemma:

- Not require offchain server interaction.
- Not require revealing the entire intent ahead of time.
- Good UX: reliability, low latency, one signature per operation.

### This can be solved by putting the user in full control at all times.

If Alice initiates every transaction on every chain without intermediaries transacting on her behalf, no one can censor her, grief her, limit her to specific use cases, or compromise her privacy.  Goal achieved.

But this requires solving some problems:

1. How will Alice transparently use an unknown chain without trusting dapps to add them to her wallet and trusting unknown RPC servers?
2. How will Alice pay for the gas on chains she never used before?
3. How will Alice move assets between chains without trusting bridge operators or using expensive and slow canonical L1 bridges?
4. How will she do all this with just one signature?

## How EIL works

### Multichain calls with ERC-4337

Suppose Alice wants to perform N operations on N different chains. By far the most common case will be: transfer assets to a liquidity provider on chain A, and then perform an action on chain B. But there are other more complex cases as well.

In EIL, users use an ERC-4337 account with logic optimized for multichain use cases.  A wallet generates multiple different UserOps, then signs a single authorization on a Merkle root of all of them.  The validation section of the account on each chain expects (i) a UserOp, (ii) a Merkle branch proving its membership in some tree, and (iii) a signature over the root of the tree.

The main advantage of doing this instead of just signing N times (which a wallet could do with one click from the user) is in order to support hardware wallets, which generally do not support any functionality for simultaneously generating N signatures.

How the wallet uses it:

[![Untitled](https://ethresear.ch/uploads/default/optimized/3X/6/3/6382513a0833be0f540be102d1a42875cf374222_2_256x500.png)Untitled1436×2804 153 KB](https://ethresear.ch/uploads/default/6382513a0833be0f540be102d1a42875cf374222)

[ZeroDev](https://github.com/zerodevapp/kernel/blob/6a098bc8f9a7001fe7ae801368e96a5ee635ddb1/src/validator/MultiChainValidator.sol) and [Biconomy](https://github.com/bcnmy/scw-contracts/blob/d3a2ee85f03d9517e3bd224842cc7a58eaf0f6ac/contracts/smart-account/modules/MultichainECDSAValidator.sol) implemented validation modules that works similarly.

### Token transfers

Token transfers from chain A to chain B are needed for two reasons. First, Alice often wants to move tokens between chains. Second, if Alice wants to do something on chain B, but has no tokens on chain B, she needs to pay gas fees somehow, and this requires moving tokens over from chain A.

Unlike calls, token transfers do require information flow between L2s.  Currently we can’t trustlessly implement fast messaging so the next best thing is Atomic Swaps.

The most widely known method is [HTLC](https://www.investopedia.com/terms/h/hashed-timelock-contract.asp). Each party locks funds in a timelock contract on one of the chains, which can be withdrawn by the other party using a secret which is hashed in the contract.  Both contracts use the same hash so as soon as the party which generated the secret performs a withdrawal, the other party sees the secret and can perform the withdrawal on the other chain.  If the secret is not revealed within the preset time, each party can withdraw their original deposit.  Funds can’t be lost or stolen but the protocol is inefficient.  It requires 1:1 relationship, multiple transactions on both chains, and potentially locks up funds for some time.

Can we do better?  Yes!  We have a tool at our disposal that the typical HTLC implementation doesn’t: We don’t have fast cheap trustless messaging but we do have slow expensive messaging via L1.

This enables optimistic design, removing the need for a secret and reducing the number of transactions to 2 on the source chain (one by each party) and 0 on the destination chain. The withdrawal doesn’t require a dedicated transaction, and happens within the user’s call where the funds are used.  Transfers can be as fast as 1 source chain block + 1 destination chain block, 2 seconds on many current rollups.

#### How it works

We introduce a **CrossChainPaymaster**, an ERC-4337 paymaster for crosschain gas payments as well as a permissionless liquidity hub for ETH and ERC-20 tokens.

**XLPs (Crosschain Liquidity Providers)** register and deposit funds in the CrossChainPaymaster on multiple chains. In addition they lock a stake on L1 in L1CrossChainStakeManager. The unstake delay is 8 days - longer than the max L2 finality time.  If an XLP starts the 8 days unstaking process, it immediately gets unregistered.

Registering & Staking:

[![Untitled (1)](https://ethresear.ch/uploads/default/optimized/3X/2/6/262f6f7c37421abecd5a3908e737fce0413f75b9_2_690x370.png)Untitled (1)1436×772 26.6 KB](https://ethresear.ch/uploads/default/262f6f7c37421abecd5a3908e737fce0413f75b9)

Unregistering & unstaking:

[![Untitled (2)](https://ethresear.ch/uploads/default/optimized/3X/f/1/f148ab83ad113711ea1aa06574405cdb8c96c104_2_690x367.png)Untitled (2)1436×764 26 KB](https://ethresear.ch/uploads/default/f148ab83ad113711ea1aa06574405cdb8c96c104)

The structure and use of the stake is discussed in [EIL: under the hood](https://hackmd.io/@1XHOvXHsQ76QF9ptlCibYQ/Bkz_EqKybl#How-the-stake-is-structured-and-used).

Transacting:

- Alice wants to transact from Chain_A to Chain_B. She finds registered XLPs that operate on both chains
- Alice signs a multichain UserOp. On Chain_A she locks funds in CrossChainPaymaster and requests a matching Chain_B voucher, specifying a list of XLPs she’s willing to use and a fee schedule (detailed below).  The request is short-lived.  If a voucher is not provided promptly, Alice’s funds are unlocked.
- An XLP claims her Chain_A funds by providing a signed voucher - a signed commitment for Chain_B. The same signed voucher that claims funds on Chain_A releases XLP funds on chain B to Alice - forming an atomic swap. The funds on Chain_A remain locked for an hour (to mitigate rugpull attempts - more details in the following section), after which they’re credited to XLP’s deposit.
- Alice appends the XLP’s voucher to her Chain_B UserOp’s signature and submits it to Chain_B.
- Chain_B CrossChainPaymaster verifies voucher, checks that XLP has sufficient funds deposited, pays for the gas and gives Alice the funds.
- Alice’s Chain_B call gets executed and her account uses the funds during this call. Gas is paid out of XLP’s Chain_B balance.

[![Untitled (3)](https://ethresear.ch/uploads/default/optimized/3X/b/5/b5d1c032add426359b2de8266a027616307d1220_2_674x500.png)Untitled (3)1436×1064 41.4 KB](https://ethresear.ch/uploads/default/b5d1c032add426359b2de8266a027616307d1220)

- This flow can continue and traverse any number of L2s using the same signature.
- Each iteration transfers value and performs one or more calls.
- It can also perform a completion call on Chain_A if needed.
- Calls are executed on all chains with one signature. Gas was paid on the source chain.

What could go wrong and what do we do about it?  EIL defines a trustless L1-based dispute mechanism, ensuring that funds cannot be lost or stolen, penalizing XLPs that violate the rules and incentivizing other XLPs to prove any such violation to L1.  See Attacks & mitigations section in [EIL: under the hood](https://hackmd.io/@1XHOvXHsQ76QF9ptlCibYQ/Bkz_EqKybl#Attacks-amp-mitigations).

#### Voucher fee structure

Voucher requests offer a fee to compensate XLPs.  Each request may include one or more assets, e.g. ETH for gas, ERC-20 tokens.  The fee is denominated in the first asset, whether it’s ETH or a token.

Requests specify multiple XLPs that may claim them. The first XLP to provide a voucher receives the fee. This creates competition between XLPs.

Fee discovery uses a reverse Dutch auction.  The request specifies a fee range and a fee increase per second.

- Time T+0: UserOp is still in the mempool. Any listed XLP may provide a voucher and receive the start fee as soon as both the request and the voucher get included onchain.
- Time T+1: If no XLP provided a voucher at T+0, the request may land onchain unfulfilled.  A higher fee is paid to the XLP that provides a voucher.
- The fee keeps increasing every second at the user-specified rate until a voucher is provided or the max fee is reached.
- If the request remains unclaimed, it expires and the funds are released back to the user.

Alice may start with a very low fee and let it increase until an XLP considers it sufficient. However, to minimize latency she should start close to the current market fee.  If she offers the current market fee or higher, she can expect zero-latency fulfillment.  Current market fees can be observed onchain as the paymaster emits an event for each voucher.

This mechanism is an optimization over how gas fees work.  The start fee is equivalent to the current gas price which can be gathered from onchain data.  To avoid signing a new transaction if the price increased, a range is specified.  The reverse dutch auction uses the competition between XLPs to ensure that users transact at the lowest possible fee.

#### Mempool dynamics

An XLP that also runs a bundler and participates in the mempool can bundle the UserOp along with its own UserOp that claims the funds, thus earning the fee before other XLPs get a chance to act. Voucher requests become part of MEV.

In a competitive environment XLPs that don’t do this will usually be 1 block too late and seldom earn fees.

It is therefore expected that most XLPs would join the mempool and compete on fulfilling requests in the same block where users submit them. Users benefit from 1 block crosschain swaps.

### What can we improve when we get trustless crosschain messaging

In the future we expect faster L2 finality as rollups move away from the optimistic model and towards ZK validity proofs. This enables fast trustless cross-L2 messaging and efficient proving of L2 state.

When fast L2 finality becomes available, we’ll build an additional paymaster, CrosschainMessagingPaymaster, which doesn’t use atomic swaps and makes different trade offs. It removes the XLPs and replaces them with passive liquidity providers, much like a Uniswap liquidity pool.

Multichain accounts will be able to send funds on the source chain and use them to complete the transaction on the destination chain as soon as a message is delivered between the paymasters on both chains.

Liquidity providers will earn fees on each chain and be incentivized to rebalance the pool across chains.

It provides better liveness guarantees than CrossChainPaymaster since there’s no risk that a chain has no XLPs running, but higher latency due to L2 finality time on L1 and slightly higher cost due to crosschain messaging overhead.

CrosschainMessagingPaymaster and CrossChainPaymaster may share the same interface so wallets will be able to support both without additional effort. By default they might prefer to use the faster and cheaper CrossChainPaymaster, but can fall back to CrosschainMessagingPaymaster if there’s a protocol liveness issue on a certain chain.

### What can we improve when we get native account abstraction (EIP-7701)

Currently the protocol uses ERC-4337 accounts for multichain operations.  Being an ERC rather than part of the Ethereum protocol, 4337 unavodiably adds a layer on top of transaction.  This comes with certain downsides:

- The AA protocol is implemented as a singleton contract (EntryPoint) which adds some gas overhead.
- The 4337 mempool is a network of bundlers rather than block builders.  Bundlers then interact with block builders, adding a layer of complexity.

EIP-7701 introduces flexible in-protocol account abstraction.  It enables different AA models, including a more efficient variant of ERC-4337 where the EntryPoint contract is replaced by the protocol, and the bundlers logic can be implemented directly by block builders that wish to participate in the AA mempool.

EIL is designed with EIP-7701 in mind.  Chains that implement EIP-7701 will benefit from an EIL implementation with increased efficiency and improved censorship resistance.

## Recap: what are some key UX, security and privacy properties of this mechanism?

### Seamless UX

- Multichain smart accounts and EIP-7702 delegation enable multichain transactions signing once per operation, not separately on each chain.
- You can purchase vouchers for any token on any chain, and use them anywhere.
- You can purchase a gas voucher on one chain, and use it to pay fees on another.
- Minimum latency - as fast as the underlying chains.
- Building interop into the wallet. Vouchers requested and received in the same block, wallets transact directly on all chains, not waiting for a crosschain message.

### Censorship resistance, security, privacy

- EIL uses a permissionless and incentivized mempool. A single honest node is sufficient.
- No trusted intermediaries, calls made directly by the user, funds are swapped atomically, any dispute is resolved directly via L1.
- Privacy aware users can send directly to the p2p mempool. Plausible deniability.
- The pre-transaction-submission steps of reveal token amounts and gas limits. Actual calls not revealed to anyone until the user executes them. Privacy aware users can choose to send direct to builder marketplaces that protect from sandwiching, or use any future solution to the same problem.
- Runs locally on the user’s machine, open source.  Cross-chain liquidity provider only provides gas and liquidity, performs minimal functionality (atomic swaps) and fully verifiable onchain.

## How does this architecture support the most common use cases?

#### Seamless crosschain transfers

Arbitrum Alice wants to send 100 USDC to Base Bob. Alice pastes Bob’s address into her wallet and sends 100 USDC, her wallet figures everything out and Bob receives the funds within seconds.

[![Untitled (4)](https://ethresear.ch/uploads/default/optimized/3X/6/d/6d8cbec610179f503a4a6406e404068ac2308551_2_690x446.png)Untitled (4)1436×930 37.5 KB](https://ethresear.ch/uploads/default/6d8cbec610179f503a4a6406e404068ac2308551)

#### Seamless multichain calls

Alice wants to mint an NFT on Linea. It costs 1 ETH. She never used Linea but has 0.8 ETH on Arbitrum and 0.5 ETH on Scroll. She clicks the “mint” button and signs a single transaction. Her wallet figures everything out, transparently transfers enough ETH from Arbitrum and Scroll, mints the NFT on Linea and verifies that she received it.

[![Untitled (5)](https://ethresear.ch/uploads/default/optimized/3X/2/b/2bbb5ec6b9922c789460a4e5b6764d5bb94b5ac8_2_690x449.png)Untitled (5)1436×936 38.9 KB](https://ethresear.ch/uploads/default/2bbb5ec6b9922c789460a4e5b6764d5bb94b5ac8)

#### Seamless crosschain swaps

Arbitrum Alice wants to swap USDC to RUT (Rarely Used Token). It has little liquidity on Arbitrum but she finds a good price in a DEX in Taiko.  She signs a single transaction, her wallet figures everything out, swaps on Taiko, and she receives the RUT back on Arbitrum within seconds.

[![Untitled (6)](https://ethresear.ch/uploads/default/optimized/3X/c/f/cfc35fed535e02610aa7569f8ca505466a7c8f46_2_641x500.png)Untitled (6)1436×1120 47.2 KB](https://ethresear.ch/uploads/default/cfc35fed535e02610aa7569f8ca505466a7c8f46)

## Differences between EIL and other designs

### EIL is not Intents or Bridges

EIL is account-based interop: the user’s own account directly performs every call on every chain. Liquidity providers only supply gas and assets - they never submit transactions and never see the call targets. This removes the “mid-state” trust dependency that exists in intents and bridges, where a 3rd party solver/relayer transacts on the user’s behalf.

The analogy is buying gas for your car vs. buying a bus ticket:

- If you buy a bus ticket, you’re committed to that bus.

Privacy: the bus company knows where you’re going.
- Censorship resistance: If the bus driver decides to drive elsewhere, or stops the bus halfway and kicks you out, you don’t reach your destination.  There’s a mid-state in which you can’t switch buses.

If you buy gas for your car and then drive to your destination, either the gas station sell you the gas or another station will, but either way your dependency on the gas station ends as soon as you get the gas.

- Privacy: the gas station doesn’t know where you’re going.
- Censorship resistance: Once they sell you the gas they have no way to stop you.  There’s no mid state, the transaction is atomic - you pay, get the gas, and you’re done.

With intents or Bridges, there is this mid state where a 3rd party is supposed to “get you there”, and at that point you’re dependent on them.  EIL does not have this mid state because the calls are made by the user, not a 3rd party.

### EIL is not a crosschain messaging protocol

Trustless crosschain messaging is currently slow.  It depends on L1 block time as well as L2 finality speed.  To improve speed, messaging protocols introduce trust assumptions.  A 3rd party needs to attest for message validity until it gets proven/disproven via L1.

Messaging protocols have different strengthes and weaknesses comapred to EIL:

- Strength: they can achieve something that EIL doesn’t - composability between contracts on multiple chains. EIL is account based, enables the account to combine calls to different contracts, but doesn’t attempt to enable calls from a contract on one chain to another.  For this use case, projects should choose between slow trustless messaging (canonical bridges) and faster messaging protocols.  Good options exist, making different trade offs.
- Weakness: messaging introduces latency.  The less trust it requires, the higher the latency.  EIL does not incur this latency because the calls are from the user to each chain rather than from one chain to another.

EIL does use the canonical bridge for messaging, but only when a fraud proof is required.  Normal user flows do not involve messaging.  Hence it cannot be seen as a messaging based protocol.

In the future, when we have faster finality of both L1 and L2 which enables trustless messaging, it’ll be possible to implement EIL as a messaging based protocol and simplify the protocol.  For now, however, it is not messaging based.

## When to use / not use EIL?

EIL enables trustless execution of calls on multiple chains, and provides liquidity and gas for these calls.

When is EIL a good fit?

- You need to execute calls on multiple chains seamlessly.
- The user doesn’t necessarily have gas funds on each chain.
- Assets scattered on multiple chains, you wish to use them without bridging friction.
- You prefer to only trust your wallet, and not add intermediaries and trust assumptions.

When should you use something else?

- Your dapp only knows what it wants to achieve at a high level, not how to translate it to contract calls.  EIL doesn’t delegate to a 3rd party service so the dapp must specify the calls to execute.

Intents let you delegate to a Solver and let it figure out the calls.  The downsides are that transaction logic is controlled by a 3rd party, and censorship resistance is degraded.

Your action involves offchain counterparties rather than just smart contracts.  For example, offchain orderbook based swaps.  EIL is an onchain protocol.  It can transfer assets across chains but depends on DEXes for swapping one asset to another.

- If a transaction requires coordinating between offchain parties, intents are a better fit.  It comes with the downsides above, plus the information asymmetry risk.

A contract on one chain needs to call a contract on another, without trusting the user.

- EIL lets users transact on multiple chains, but if contracts need to call each other directly, then you need a crosschain messaging protocol.  The downside is either high latency (canonical bridge - 7 days for optimistic rollups), or trusting an offchain oracle to attest for crosschain messages.

### How to use EIL if I’m a …?

#### Wallet dev

- Support ERC-5792 (wallet_sendCalls) with an extension for multichain operations, or use the EIL SDK.

Smart accounts: use the multichain account module we’ll provide or build your own, based on the ERC (WiP).
- EOA wallets: use the multichain 7702 implementation we’ll provide or implement the ERC (WiP)
- Use CrossChainPaymaster for crosschain gas payment and token transfers.

#### dApp dev

- Use ERC-5792 (wallet_sendCalls) for multichain operations by default, or use the EIL SDK.

Only fall back to bridges if the wallet doesn’t support it.

#### User

- Pick a wallet that supports EIL.
- Transact like you would on a single chain, never having to switch networks or bridge funds.

## Replies

**ed** (2025-11-13):

Lovely writeup!  A question about how source chain reorgs are handled:

Alice commits funds on chain A.  An XLP claims these funds and generates a voucher on chain A to be redeemed on chain B.  Alice then uses the voucher to claim funds on chain B.  However, chain A now reorgs to a point before Alice committed her funds!  The XLP that generated the voucher on chain A could monitor this reorg, and then resubmit Alice’s tx to commit funds (perhaps the XLP initially bundled their own voucher creation with Alice’s fund commitment tx in the first place, so this is easy).  The XLP has a full day to land Alice’s transaction on chain A (1 day for force-inclusion on the L1 + 7 days for chain A finality = 8 day dispute period). However, what happens if Alice is able to submit a tx with the same nonce before the XLP is able to do this?  Now the XLP can no longer re-submit Alice’s tx, and loses out on claiming Alice’s funds on chain A, while Alice still claimed the XLP’s funds on chain B.  What am I missing here?

---

**jayden-sudo** (2025-11-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> A wallet generates multiple different UserOps, then signs a single authorization on a Merkle root of all of them.

Hi Yoav,

Thank you for sharing this! The EIL proposal is incredibly detailed and well-thought-out. Cross-L2 interoperability is a critical problem to solve, and this is one of the most practical and comprehensive approaches I’ve seen. Amazing work!

I had one specific point I’d love to get your thoughts on, regarding the multichain account validation mechanism.

Your document states: “A wallet generates multiple different UserOps, then signs a single authorization on a Merkle root of all of them.”

This is a very elegant solution, but I’m thinking about the practical complexities of heterogeneous account setups. As you know, a user’s smart account on one chain might have a different configuration from their account on another. For example:

1. Different Signers/Validation Logic: A user might secure their L1 account with a standard ECDSA key but use a more gas-efficient or novel scheme on an L2, like a P-256 key, a Passkey/WebAuthn signer, or even a social recovery setup.
2. Chain-Specific Implementations: The account implementation on one chain might not be identical to another, especially if they are deployed at different times or on chains with different EVM capabilities.

This leads to my core question: **How does an account on Chain B validate a Merkle root that was signed using the validation logic native to Chain A?**

A naive interpretation would suggest that the account contract on *every* chain would need to contain the validation logic for *all potential signers* from all other chains. This could lead to significant contract bloat and complexity, undermining one of the benefits of chain-specific account optimization.

I imagine you’ve already considered this, so I’m curious about the intended model. Is the underlying assumption that for a user to leverage EIL, their “Multichain Account” must share a single, standardized “master signer” or validation module across all chains specifically for authorizing these Merkle roots? This master signer could coexist with other chain-specific signers for regular, single-chain transactions.

I hope my question is clear! I might be overthinking a detail you’ve already solved, but I wanted to raise it as it seems crucial for the real-world implementation of wallet infrastructure on top of EIL.

Again, fantastic work on this. I’m really impressed and looking forward to hearing your perspective!

Best

---

**alonmuroch** (2025-11-13):

Great write-up!

How are the economics for an LP compare to intents? It seems more expensive because they lock collateral on L1?

---

**yoavw** (2025-11-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/ed/48/13214_2.png) ed:

> Alice commits funds on chain A. An XLP claims these funds and generates a voucher on chain A to be redeemed on chain B. Alice then uses the voucher to claim funds on chain B. However, chain A now reorgs to a point before Alice committed her funds! The XLP that generated the voucher on chain A could monitor this reorg, and then resubmit Alice’s tx to commit funds (perhaps the XLP initially bundled their own voucher creation with Alice’s fund commitment tx in the first place, so this is easy). The XLP has a full day to land Alice’s transaction on chain A (1 day for force-inclusion on the L1 + 7 days for chain A finality = 8 day dispute period). However, what happens if Alice is able to submit a tx with the same nonce before the XLP is able to do this? Now the XLP can no longer re-submit Alice’s tx, and loses out on claiming Alice’s funds on chain A, while Alice still claimed the XLP’s funds on chain B. What am I missing here?

Thank [@ed](/u/ed) , that’s a great question.  We discuss reorgs in the “under the hood” doc, [here](https://hackmd.io/@1XHOvXHsQ76QF9ptlCibYQ/Bkz_EqKybl#Trust-assumptions).

An XLP takes the same risk as intent solvers do.  As you pointed out, one mitigation technique is for the XLP to retain a copy of Alice’s UserOp and resubmit it immediately if it gets reorged out on chain A.  The XLP doesn’t even need to worry if another XLP submits a voucher for the same request since the protocol ensures that only the XLP whose voucher was used ends up getting the chain A funds, as described [here]([EIL under the hood - the gory details - HackMD](https://hackmd.io/@1XHOvXHsQ76QF9ptlCibYQ/Bkz_EqKybl#What-happens-if-a-voucher-was-provided-on-Chain_A-but-a-different-one-was-used-on-Chain_B)).

But as you further noted, Alice could submit a conflicting UserOp during the reorg, so the original request can no longer be replayed.  In that case the XLP ended up providing a chain B voucher and not getting paid on chain A.  However, for this to happen, Alice needs to actually trigger the reorg or at least be aware that it’s going to happen at that exact time, sign two conflicting UserOps and cause the two reorg branches to include these different UserOps.  It’s highly unlikely to happen by accident - that Alice just guessed there’s going to be a reorg, sent two conflicting UserOps and happened to hit a reorg where different UserOps got included.  She can’t just keep sending such UserOps until there’s a reorg since she pays fees for all the cases where there wasn’t one, and locks her capital for the validity time of each voucher.  If Alice is able to somehow control reorgs to that level and doesn’t have to guess blindly that a reorg is coming, then this chain is unsafe and she can probably do worse than stealing a voucher.

XLPs should still take this into account when dealing with particularly large amounts on reorg-prone L2s.  They could wait a few blocks between the request and the voucher to reduce the change of a reorg.  But doing this for small vouchers is a losing strategy because another XLP will provide a voucher before they do.  The early XLP gets the worm ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14).   I assume that solvers already developed strategies for dealing with reorg risks of high value intents.  XLPs should apply similar strategies.

---

**yoavw** (2025-11-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/jayden-sudo/48/19870_2.png) jayden-sudo:

> This is a very elegant solution, but I’m thinking about the practical complexities of heterogeneous account setups. As you know, a user’s smart account on one chain might have a different configuration from their account on another.

Thanks [@jayden-sudo](/u/jayden-sudo) .  The protocol assumes that the user uses the same account implementation on both chains, or at least uses implementations that support the same merkle-based `UserOp.signature` format.  To facilitate this, we should have a standard format for this “signature”.  EIL requires a set of ERCs, and this will be one of them.  We’ll publish a proposal soon and collaborate with account devs to ensure that it fits their multichain needs.

Note that this question applies to smart accounts.  EOA users will use a 7702 delegation, and should just set the same delegation for all chains.  UserOps can be submitted with a 7702 delegation, so the wallet should add the delegation when submitting each of the UserOps if it hasn’t been set previously.

![](https://ethresear.ch/user_avatar/ethresear.ch/jayden-sudo/48/19870_2.png) jayden-sudo:

> Different Signers/Validation Logic: A user might secure their L1 account with a standard ECDSA key but use a more gas-efficient or novel scheme on an L2, like a P-256 key, a Passkey/WebAuthn signer, or even a social recovery setup.

The account is supposed to support this new “signature” scheme in addition to any other signature scheme it supports, and it needs to support it on any chain.  It’s ok to support it in the L1 version as well, since the user never pays for it if not using it.  For example the account can check len(UserOp.signature) and treat short sigs as ECDSA, or add a sig-type header to UserOp.signature.

But this highlights another point: the user must use the same key on all chains, unless the wallet manages per-chain keys (which I don’t think any wallet does).  If you rotated your key on chain A but not on chain B, then validation will fail on one of the chains due to signing the merkle root with the wrong key.  The long term solution to these problems is an L1 keystore.  We’ve already discussed the importance of the keystore in the past, now they’re becoming even more important.  We need L2’s to implement L1SLOAD to make keystores viable.  Without a keystore, a user that started rotating the key has to complete the rotation on both chains before sending a multichain UserOp.

![](https://ethresear.ch/user_avatar/ethresear.ch/jayden-sudo/48/19870_2.png) jayden-sudo:

> Chain-Specific Implementations: The account implementation on one chain might not be identical to another, especially if they are deployed at different times or on chains with different EVM capabilities.

That’s where the above standard plays a role.  Even if the account implementation differs, it should support the same ERC for merkle validation.

![](https://ethresear.ch/user_avatar/ethresear.ch/jayden-sudo/48/19870_2.png) jayden-sudo:

> their “Multichain Account” must share a single, standardized “master signer” or validation module across all chains specifically for authorizing these Merkle roots? This master signer could coexist with other chain-specific signers for regular, single-chain transactions.

Exactly.  The same merkle validation logic should exist on both ends.  Technically it doesn’t need to be standardized as long as the account has the same implementation on both ends, but there’s value in standardizing it so that mixing implementations would still work.  It’s not a “master signer” though, just a standardized merkle proof, and then the root is signed with whatever signature scheme the account already supports.  E.g. if the account uses P256 rather than ECDSA then the merkle root should be signed by that P256 key.  The standard should not force accounts to maintain an ECDSA key.

![](https://ethresear.ch/user_avatar/ethresear.ch/jayden-sudo/48/19870_2.png) jayden-sudo:

> I hope my question is clear! I might be overthinking a detail you’ve already solved, but I wanted to raise it as it seems crucial for the real-world implementation of wallet infrastructure on top of EIL.

You’re not overthinking!  And thanks for asking this question.  We’ve been discussing these things extensively while working on EIL.  Looking forward to collaborate on the required standards.

---

**yoavw** (2025-11-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> How are the economics for an LP compare to intents? It seems more expensive because they lock collateral on L1?

Thanks [@alonmuroch](/u/alonmuroch) .  Capital efficiency is similar to that of some intent protocols.  The L1 stake is O(networks) rather than O(funds) since it’s not used as a collateral to cover funds.  Its goal is to deter behaviors that degrade network efficiency, e.g. delaying XLP funds or delaying a user by causing the need for an alt voucher.   Funds are protected by other means, not repaid by the stake.  Since the stake is not O(funds) it doesn’t materially affect capital efficiency, although in particularly low-volume chains it might play a role: if the traffic is $100,000/month then locking a permanent 1 eth doesn’t matter much, but if traffic is $10/month - it does.

The mechanism staking mechanism that doesn’t require O(funds) is described [here](https://hackmd.io/@1XHOvXHsQ76QF9ptlCibYQ/Bkz_EqKybl#How-the-stake-is-structured-and-used) but I’ll elaborate a bit in this thread:

When someone submits a dispute, they must report it on both src and dst.  On dst they actually prove insolvency, so dst sends a message to L1.  On src they complement it with a claim, which immediately freezes the funds for 8 days unless resolved sooner via L1.  This prevents user funds from ever being lost, so the stake doesn’t need to cover the actual funds.  The disputer is also incentivized (but not forced) to provide an alt voucher to the user, so from the user’s perspective the funds are not even delayed unless the deal is so bad that no one else wants to provide an alt voucher, in which case the funds are only refunded when the dispute settles.  This case is unlikely in a competitive XLP landscape.

The role the stake plays in this flow, is to incentivize other XLPs to send these two transactions (src and dst), and to provide an alt voucher to the user asap (before anyone else does).  When the dispute settles on L1, the malicious XLP’s stake is distributed among those who submitted these two transactions and whoever provided an alt voucher.  The alt voucher also pays a fee just like any other voucher, so the stake adds an extra to compensate for time when the funds are still locked until the dispute settles.

The reason for making the stake O(networks) rather than O(1) is to compensate these callers on any number of networks, in case an XLP is active on many networks and defaults on all of them concurrently.

Another mechanism we introduced is the dispute array.  Disputes and proofs are submitted as arrays rather than each one separately.  This prevents dilution of incentives, where there would be so many disputes against one XLP, that the stake won’t even cover the fees of the dispute transactions.  All the information about valid disputes is available onchain, so there’s no legit reason for a disputer to submit a partial array.  Therefore we record the array length and only compensate those who submitted the longest array for the XLP on each of the chains.

Since you brought up capital efficiency, one thing that actually isn’t O(1) is the funds that are locked for 1 hour at the source chain.  XLP funds remain liquid, except when issuing an actual voucher.  But when an XLP submits a voucher and it gets used at the destination, the funds on the source chain remain locked for 1 hour in case there’s a dispute.  This does introduce some inefficiency, which I believe some other protocols also incur for enabling disputes.  The XLP can’t reuse the funds for an hour if a transfer actually took place.  We need to consider whether the dispute period can be shortened.  1 hour is arbitrary, it just needs to be significantly longer than the validity time of the voucher, and sufficient for another XLP to report a dispute - which the protocol incentivizes to do immediately.  We [proposed](https://hackmd.io/@1XHOvXHsQ76QF9ptlCibYQ/Bkz_EqKybl#Note-on-voucher-expiration-time) voucher expiration of 5 mins, so maybe a dispute period of 10 minutes would be sufficient.  That’s something we need to explore with XLPs.  It also doesn’t need to be identical on all chains, and can be set in the CrosschainPaymaster on each L2.

I hope this answers your question.  If not, happy to discuss more.

---

**alonmuroch** (2025-11-15):

Another thing I find interesting is the UX of signing only once while executing across multiple chains. We actually make use of that as well.

Maybe some standards and broader wallet adoption can go a long way.

---

**yoavw** (2025-11-15):

Right. We intend to standardize this as an ERC soon, so different implementations can be compatible and make things easier for wallet devs.

---

**yoavw** (2025-11-15):

Anyone at devconnect interested to learn more about EIL, we’re going to discuss it extensively at https://trustlessconference.com/

---

**MicahZoltu** (2025-11-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> If Alice is able to somehow control reorgs to that level and doesn’t have to guess blindly that a reorg is coming, then this chain is unsafe and she can probably do worse than stealing a voucher.

What is the worse things Alice can do if she can force a reorg?

Ethereum, and many other blockchains, are designed such that reorgs are costly but not impossible.  Introducing clear autonomous ways to profit from them not only puts the protocol introducing those incentives at risk, it also increases the risk that reorgs actually occur (which causes mild discomfort/annoyance to others on the chain).

If the chain in question has a concept of finality, then you can wait for that before proceeding.  If the chain has no finality then this is always a risk.

---

**k06a** (2025-11-20):

EIL idea sounded promising until I saw ERC-4337 mentioned - which is obviously over-engineering for me.

---

**sissnad** (2025-11-21):

First of all, thank you for the excellent write-up on EIL.

I really appreciate the clarity of the proposal and the focus on improving cross-L2 UX without compromising Ethereum’s trust-minimized properties.

I have one question about large-value transfers that I’m trying to reason through, specifically in scenarios that resemble institutional flows rather than retail-sized bridging.

Consider the following example:

1. A user on chain A initiates an EIL cross-L2 transfer of $100m.
2. An XLP fronts the $100m on chain B via a voucher, so the user receives the funds instantly on B.
3. The user immediately deposits the funds into a vault on chain B.
This deposit becomes final on B’s local state.
4. Hours or days later, an L1 dispute proves that the XLP misbehaved.
The voucher is invalid and the XLP is slashed.

My questions are:

- Since rollups do not support cross-chain reversion, does the user’s $100m deposit on chain B remain untouched and final, regardless of the XLP dispute outcome?
- If the user’s original funds on chain A are refunded or remain unspent due to the invalid voucher, doesn’t this create an economic mismatch (the user effectively ends up with exposure on both A and B)?
- The XLP’s slashed stake may be significantly smaller than the fronted amount (e.g., $10m vs $100m).
How is the remaining discrepancy handled, if at all?
- Is the intended assumption that XLPs will be sufficiently solvent and capitalized to cover very large transfers, or is EIL not intended for institutional-scale settlement where full economic finality is required quickly?

I’m asking to understand the intended guarantees of EIL for high-value transfers, and whether EIL is best suited primarily for retail-sized UX improvements rather than institutional-grade settlement.

---

**yoavw** (2025-11-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/k06a/48/1496_2.png) k06a:

> EIL idea sounded promising until I saw ERC-4337 mentioned - which is obviously over-engineering for me.

Thanks for your feedback.

Trustless interop through self-execution requires abstracting gas payment.  EIL uses ERC-4337 for its gas abstraction, to avoid depending on centralized relayers.  When EIP-7701 gets included, gas abstraction will become a protocol feature and won’t require an additional layer.  EIL will then replace ERC-4337 with that.

To make your criticism more constructive and actionable, it’ll be great if you can propose a simpler alternative that provides the same UX and censorship resistance.

The ecosystem already has plenty of simple interop solutions that introduce trust dependencies.  We believe Ethereum should have at least one option that doesn’t.  We’d love to collaborate on any proposal that improves Ethereum UX without introducing trusted intermediaries.

---

**nerses-asaturyan** (2025-11-23):

This is a very interesting idea. I may have misunderstood part of the flow, so I’d appreciate some clarification on a few points:

1. How does the user verify that the voucher they receive is valid on the destination chain?
What mechanism ensures that the voucher can be safely redeemed without risk of forgery or replay?
2. What prevents the XLP from redeeming the funds on the destination chain themselves?
Is there a specific cryptographic or protocol-level restriction that enforces correct behavior?
3. Are these aspects mainly implementation choices?
(e.g., using signatures, time-locked funds, or another enforcement mechanism)

A bit more detail on these points would help me fully understand the security assumptions and guarantees of the design.

---

**SCBuergel** (2025-11-25):

Thank you for working deeply on this proposal! I have a concern regarding wasteful competition among XLPs.

It seems that best price execution, censorship resistance, and liveness all depend on the user listing multiple XLPs. But doesn’t this recreate the same wasteful competition we see in onchain CLOBs, where all but one taker burn gas on reverted or unfilled transactions at the top of the book?

In practice, I would expect most (all?) XLPs to submit their claims in the same block, since their cost basis for simple transfers is fairly well defined and the fee increases only in coarse, block-sized steps aligned with L1 block times.

---

**xinbenlv** (2025-11-26):

+1 to [@MicahZoltu](/u/micahzoltu) ‘s question about re-org resistance.

I also have a question about **complexity growth and DoS-resilience** in EIL’s multichain model.

EIL lets wallets construct **N UserOps across many chains**, Merkle-ize them, and authorize all of them with one signature, and it allows CrossChainPaymaster flows to traverse **any number of L2s** through sequential voucher-funded hops.

My question is:

**How does complexity scale as the number of cross-chain operations grows, and how resilient is EIL to worst-case or adversarial composition?**

More concretely:

1. Computational & verification cost
As N (number of per-chain UserOps) grows, per-chain validation involves verifying larger Merkle proofs, longer calldata, and more complex account logic.
How does overall computational cost scale with N, and is there a practical limit before validation becomes a DoS vector?
2. Sequential, state-dependent hops
For flows that perform K dependent voucher hops (A→B→C→…→A), where each hop’s validity depends on previous on-chain results,
how does liveness / dispute load / XLP resource usage scale with K, and are deep multi-hop sequences a potential DoS pressure point?
3. System-level resilience
Are there recommended guardrails or assumptions (e.g., bounding N and K) to prevent unbounded user-constructed multichain sequences from overwhelming bundlers, paymasters, or XLPs?

---

**yoavw** (2025-12-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> What is the worse things Alice can do if she can force a reorg?

One obvious example is unbundling MEV sandwiches, then including an alternative block with only one side of the sandwich.  Others include DeFi protocols involving liquidations, etc.  Basically wherever there’s significant MEV, being able to cheaply and predictably cause reorgs where you can selectively replace a transaction, can be highly profitable.

The cost of doing this on Ethereum is too high to be exploited for most purposes.  And in most rollups it’s not feasible at all since they have a single sequencer.

Anyway if Alice can cheaply and predictably cause reorgs where she can replace her own transaction with a conflicting one, she can rugpull bridge operators / solvers / XLPs unless they wait for finality.  For small amounts this protection makes little sense for them, as a less risk averse competitor will end up collecting the fees.  If it does become a problem on some chain, then intent solvers and XLPs will adjust their behavior on that chain and wait longer for finality.

![](https://ethresear.ch/user_avatar/ethresear.ch/sissnad/48/13177_2.png) sissnad:

> First of all, thank you for the excellent write-up on EIL.
> I really appreciate the clarity of the proposal and the focus on improving cross-L2 UX without compromising Ethereum’s trust-minimized properties.

Thank you

![](https://ethresear.ch/user_avatar/ethresear.ch/sissnad/48/13177_2.png) sissnad:

> A user on chain A initiates an EIL cross-L2 transfer of $100m.

Even though the scenario you described isn’t possible (explained below), both EIL and intent protocols are not designed to transfer $100m in a single transaction. The reorg risk (e.g. via a fraud proof in an optimistic rollup) with such amounts is too high and I’d use the rollup’s canonical bridge for that.

![](https://ethresear.ch/user_avatar/ethresear.ch/sissnad/48/13177_2.png) sissnad:

> Hours or days later, an L1 dispute proves that the XLP misbehaved.
> The voucher is invalid and the XLP is slashed.

This can’t happen because the voucher is an atomic swap. The only way for the XLP to misbehave is by issuing a voucher that isn’t solvent.  Once the user successfully redeems the voucher, the funds irrevocably belong to the user.  If you follow the dispute flows, you’ll see that an XLP can be penalized for being insolvent or for attempting to delay another XLP by making wrong claims about its insolvency.  There is no flow in which a voucher was good and later became bad, since it’s atomic.

![](https://ethresear.ch/user_avatar/ethresear.ch/sissnad/48/13177_2.png) sissnad:

> Since rollups do not support cross-chain reversion, does the user’s $100m deposit on chain B remain untouched and final, regardless of the XLP dispute outcome?

The user has the funds because the voucher was valid.  The XLP couldn’t be slashed for it because it was valid, but it’s possible that the XLP was slashed for another offense.  This can’t affect past vouchers, just prevent future ones from being valid since the XLP becomes unregistered as soon as a dispute is proven against it at the destination (and later also at the source when the message gets there).

![](https://ethresear.ch/user_avatar/ethresear.ch/sissnad/48/13177_2.png) sissnad:

> The XLP’s slashed stake may be significantly smaller than the fronted amount (e.g., $10m vs $100m).

I’ll answer this outside the context of the above situation which cannot happen.  The stake is O(1) for each network, not O(liquidity).  The reason is that it never has to cover a loss, just to incentivize disputing and proving.  In a dispute situation (when an XLP has issued a voucher while having insufficient funds at the destination), we need someone to do two things:

1. Prove the insolvency at the destination. This proof is immediate - the paymaster sees the valid voucher and can verify that the XLP who signs it doesn’t have sufficient banace, so it sends a message to L1 via the canonical bridge.
2. Dispute at the source chain. This freezes the sent funds for 8 days unless the dispute is settled sooner via L1.  Once this happens, the funds cannot be stolen by the offending XLP, so the stake is not used to cover them.

The protocol incentivizes making both of these calls, by giving a part of the stake to whoever makes them on the respective chains.

Therefore even if a $100m voucher is insolvent, a stake of 1 ETH is more than enough for defending it.  Someone will be getting hundreds of dollars for just proving and disputing it, and the $100m will get frozen at the source chain until the proof from the destination arrives via L1.

I hope this clarifies why the stake doesn’t need to match the voucher amount.

![](https://ethresear.ch/user_avatar/ethresear.ch/sissnad/48/13177_2.png) sissnad:

> Is the intended assumption that XLPs will be sufficiently solvent and capitalized to cover very large transfers, or is EIL not intended for institutional-scale settlement where full economic finality is required quickly?

EIL is good for institutions in the sense that self custody is preserved due to voucher atomicity - either the user has the funds at the source or at the destination, and the funds are never sent to a 3rd party for bridging. However each individual transfer is expected to be small to medium, not $100m.  As explained above, the reorg risk becomes too great if a single voucher carries such amount.  IMHO for such amounts, institutions shouldn’t use any interop protocol - they should use the canonical bridge.

![](https://ethresear.ch/user_avatar/ethresear.ch/sissnad/48/13177_2.png) sissnad:

> I’m asking to understand the intended guarantees of EIL for high-value transfers, and whether EIL is best suited primarily for retail-sized UX improvements rather than institutional-grade settlement.

Primarily for small/medium sized UX improvements, whether by institutions making frequent transactions, or retail, but not for large settlements.

![](https://ethresear.ch/user_avatar/ethresear.ch/nerses-asaturyan/48/21438_2.png) nerses-asaturyan:

> How does the user verify that the voucher they receive is valid on the destination chain?

The voucher is verified by the source chain contract to be signed by one of the XLPs that the user has whitelisted (after verifying sufficient destination liquidity).  If it satisfies that requirement it’s considered valid.  And at the destination, either it’s valid and can be redeemed immediately, or the XLP has pulled the liquidity (or double spent) and the voucher will be proven insolvent there and disputed at the source.  The user doesn’t verify that the voucher is valid at the destination - the user just uses it immediately.  A voucher cannot be valid at the source and invalid at the destination because it’s the same signed message that applies to both.  At most, it can be valid-but-insolvent, which the mechanism design deters.

![](https://ethresear.ch/user_avatar/ethresear.ch/nerses-asaturyan/48/21438_2.png) nerses-asaturyan:

> What mechanism ensures that the voucher can be safely redeemed without risk of forgery or replay?

The voucher cannot be forged - it’s just a signature from the XLP.  It is used at the source to claim the user’s funds, and the same signature releases XLP funds to the user at the destination. It also cannot be replayed, because each voucher has a nonce that gets burned when redeemed.

![](https://ethresear.ch/user_avatar/ethresear.ch/nerses-asaturyan/48/21438_2.png) nerses-asaturyan:

> What prevents the XLP from redeeming the funds on the destination chain themselves?

The voucher is issued to the requester, and can only be redeemed in a UserOp where `UserOp.sender==requester`.  No one other than the user can spend a voucher.

![](https://ethresear.ch/user_avatar/ethresear.ch/nerses-asaturyan/48/21438_2.png) nerses-asaturyan:

> Are these aspects mainly implementation choices?

It’s just signatures. The protocol requires that the voucher redeemer is the vocuher requester.  And the voucher itself is the XLP’s signature and is identical on both chains.

![](https://ethresear.ch/user_avatar/ethresear.ch/nerses-asaturyan/48/21438_2.png) nerses-asaturyan:

> (e.g., using signatures, time-locked funds, or another enforcement mechanism)

The protocol does use time-locked funds, just not for the above.  Time-lock is used in three places:

1. Very short lock (seconds) set by the user when requesting a voucher.  If no XLP responds, funds are released back to the user.
2. 1 hour time lock (we can probably shorten this significantly) after an XLP provided a voucher to claim user funds.  This is the dispute period in case the voucher was insolvent.
3. 8 days time lock, if a dispute was opened at the source.  The funds will be released when the proof from the destination reaches L1, which settles the dispute at the source.  If this doesn’t happen within 8 days, the funds are released.  8 days is longer than the 7 days fraud proof window in all optimistic rollups so it ensures that the proof will arrive unless there isn’t one.

In practice it’s unlikely that we’ll ever see this happen in real life, due to the incentives.  This is equivalent to a fraud proof on an optimistic rollup, which also never happened to the best of my knowledge.

![](https://ethresear.ch/user_avatar/ethresear.ch/scbuergel/48/7344_2.png) SCBuergel:

> Thank you for working deeply on this proposal! I have a concern regarding wasteful competition among XLPs.

EIL uses ERC-4337 and the competition should normally happen inside the AA mempool.  The voucher fee is essentially a form of MEV.  Efficient XLPs will also be bundlers in the AA mempool.  When an XLP/bundler sees that it’s whitelisted by the user, it knows that it can collect that request’s fee.  If it’s profitable enough, the bundler will bundle the UserOp containing the request with a UserOp containing the voucher.  The bundler obviously won’t also include vouchers from other XLPs - it doesn’t even see them since they also operate similarly and would not be sending their vouchers unless bundled with the request.

A naive XLP that isn’t also a bundler will likely win few deals since it only sees the request onchain, and normally a voucher was already provided in the same block.  But if there’s an unfulfilled request and multiple naive (non-bundler) XLPs then indeed they might compete wastefully onchain.  This seems unlikely in a competitive market due to the above strategy.

We actually could solve it even for naive XLPs by using a 4337 aggregator contract which could ensure that a request can only get included when bundled with exactly one voucher, but I don’t know if it’s worth implementing unless we see that most XLPs are naive despite market efficiency.

![](https://ethresear.ch/user_avatar/ethresear.ch/xinbenlv/48/9201_2.png) xinbenlv:

> How does complexity scale as the number of cross-chain operations grows, and how resilient is EIL to worst-case or adversarial composition?

Complexity lives in the wallet in this model.  The wallet constructs the UserOps, keeps them locally, and sends them to the respective chains in the right order.  Somethings this can happen in parallel when there’s no dependency, and sometimes there’s a dependency graph (e.g. UserOp1 swapped tokens and UserOp2 uses the resulting proceeds).  Adversarial composition won’t happen since the user would be attacking themselves.

![](https://ethresear.ch/user_avatar/ethresear.ch/xinbenlv/48/9201_2.png) xinbenlv:

> How does overall computational cost scale with N, and is there a practical limit before validation becomes a DoS vector?

The user is the one building and orchestrating these UserOps.  If the user includes a very large number of UserOps and ends up with a large merkle proof, the user pays the gas for it.  On the source chain the user may be paying the gas directly, and for other chains it’ll be paid by vouchers - which the user also paid for.  The voucher request says how much gas it needs to spend at the destination, and the XLP considers it when deciding to provide a voucher.  The fee has to be sufficient to pay for that gas, or else no XLP will provide a voucher.  Therefore users can only DoS themselves.  Everyone else gets paid for the validation cost.

![](https://ethresear.ch/user_avatar/ethresear.ch/xinbenlv/48/9201_2.png) xinbenlv:

> how does liveness / dispute load / XLP resource usage scale with K, and are deep multi-hop sequences a potential DoS pressure point?

The user’s wallet has to be online, see when a UserOp was completed, read the voucher it produced on its respective chain, and use it to send the next UserOp on the next chain.  It does not depend on anyone else’s liveness but the wallet itself has to remain online throughout the operation in order to orchestrate it.  If it disconnects in the middle, any vouchers that were given but not used, will get refunded when someone else reports them as unused once they expire (typically after 5 minutes), to collect the unused voucher fee.  So if you disconnect somewhere in the middle, your operation isn’t completed but you don’t lose funds.  For disputes you don’t need to remain online since the incentives ensure that XLPs will dispute each other whenever there’s a disputable condition.  The user can also dispute but that’s a fallback and won’t be needed as long as there are multiple non-colluding XLPs.

For users that don’t want to remain online until the transaction completes, it’s possible to run a service that gets all the UserOps and orchestrates them on behalf of the user as a convenience method.  But this is not part of the EIL protocol and requires trusting that server to orchestrate on your behalf.  Some server providers will probably offer this method but I hope it’ll be used as a fallback rather than the default path.  I.e. “please orchestrate these UserOps for me if the conditions are met and they don’t show up onchain for 2 blocks”.

![](https://ethresear.ch/user_avatar/ethresear.ch/xinbenlv/48/9201_2.png) xinbenlv:

> Are there recommended guardrails or assumptions (e.g., bounding N and K) to prevent unbounded user-constructed multichain sequences from overwhelming bundlers, paymasters, or XLPs?

I don’t think we need to limit it.  The complexity remains in the wallet and doesn’t really affect other parts of the system.  Bundlers receive the UserOps one at a time and only when the UserOp is valid (including a valid voucher if needed).  The paymater is a contract, not a server.  And XLPs issue one voucher per request so they’re unaware of the others.

I hope I answered everyone’s questions here.  If I missed anything, or if there’s anything unclear, feel free to tag me again.

