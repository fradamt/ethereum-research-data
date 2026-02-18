---
source: ethresearch
topic_id: 13115
title: Privacy Enabled Cross-Chain Automated Market Maker
author: themandalore
date: "2022-07-21"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/privacy-enabled-cross-chain-automated-market-maker/13115
views: 1535
likes: 1
posts_count: 1
---

# Privacy Enabled Cross-Chain Automated Market Maker

Hey ETHresearch, made a new whitepaper and would love your thoughts.  TLDR, the idea is a cross chain AMM / mixer

**charon - a privacy enabled cross-chain amm**

Charon is a privacy enabled cross-chain automated market maker (PECCAMM). It achieves privacy by breaking the link between deposits on one chain and withdrawals on another.  Charon works by having AMMs on multiple chains, with one of the assets on each AMM being the charon dollar (CHD), a free-floating token created by deposits on an alternate chain and then a withdrawal via a zero-knowledge proof . To achieve this cross-chain functionality, charon utilizes an oracle to pass commitments (proof of deposits) between chains.

**design**

Charon can be broken down into three parts:

- an automated market maker (AMM) structure allowing deposits to other chains
- a bridge which passes deposit commitments to other chains
- a mixer structure that mints CHD on the destination chain

**the charon AMM**

The AMM structure used by charon is a standard two token AMM with single side withdrawals / LP deposits on the CHD side, very similar in many aspects to uniswap  or balancer    The tokens traded are defined as a “base” token (e.g., native chain asset) and then the charon dollar, a newly minted token created by privacy-enabled deposits from another chain.  CHD is a synthetic asset that represents deposits on alternate chains. CHD is burned either when a trade happens for the base asset (CHD is burned rather than added to the pool) or when CHD is deposited as a commitment to the other chain. The only way to add CHD to the AMM is through depositing as an LP, either directly with CHD (single side LP) or with both assets in equal proportions (traditional LP deposit). Since deposits to alternate chains are denominated in constant terms (e.g., 1000 CHD, based on the current AMM price), the newly minted CHD will be roughly stable, tracking external demand for CHD with spreads built in for oracle variability and time constraints due to the lock time of the bridging process.

**the bridge**

Charon utilizes an oracle to get information about other chains.  Either a native oracle (e.g. the Polygon data bridge ) or another decentralized oracle structure (e.g. tellor ) can be used to pass deposit information from one chain to another.  The oracle mechanism is a key point in security as the oracle alone can deposit valid commitments to mint CHD on the destination chain.  To achieve security regarding chain finality and allowing time for oracle disputes, users must wait twelve hours before withdrawing CHD on an alternate chain.

**the mixer**

Charon achieves mixer functionality due to the anonymous nature of withdrawals on alternate chains.  This is similar to a standard mixer (e.g. tornado cash ), where a user deposits on one address but withdraws with another.  The unique aspect of charon is that deposits are made on one chain (commitment generated using destination chain logic (the destination chain is part of the secret)), the commitment is passed to many chains, and then the withdrawal happens on the destination chains.  Since the commitment is passed to many chains, assuming other deposits and commitments, anonymity is achieved since there is no way to prove which chain is the destination or which withdrawal on the destination chain corresponds to a given deposit.

**asset pricing across chains**

In order to allow deposits of multiple different currencies on multiple different chains, the AMM itself is used to price the amount of the deposit (e.g.1000 CHD of ETH).  This allows the withdrawal on the destination chain to simply mint 1000 CHD regardless of which currency the deposit came in the form of (e.g. 1000 CHD deposit of ETH on Ethereum or 1000 CHD deposit of MATIC will result in the same withdrawal of 1000 CHD on Optimism (assuming these chains are in the system)).  Arbitrage across chains should force the price of CHD to be even on each chain, and if set up properly, should act as a stable medium of exchange across the assets in the system.  Due to the long delay between deposit and withdrawal however, parties should be incentivized to keep reserves of CHD and/or leave open withdrawals for quick arbitrage should prices diverge.  This arbitrage incentive will help further increase liquidity and anonymity of the system.

**flow**

There are three sets of users for the charon system: LP’s, bridge/mixer users, and traders.  The flow for each user is as follows:

*bridge/mixer usage*

- deposit on chain1 with commitment (created for withdraw on chain3)
- oracle passes commitment to chain2, chain3, chain4 (if anonymity desired)
- user waits to add anonymity then withdraws CHD on chain3 using a proof
- The CHD is then traded as a market order on the chain3 AMM

*trader*

- same as bridge/mixer user, however, will likely not focus or wait for anonymity
- the arbitrage trader will likely sit in the “to withdraw stage” if incentivized but will hold CHD if not.

*LP base asset (e.g. chain1 base asset (e.g. ETH))*

- user acquires equal amounts of base asset and CHD (via an exchange or cross-chain deposit)
- deposit chain1 base asset and CHD for pool tokens
- withdraw both assets at pair rate when finished

*LP CHD (e.g., on chain2)*

- deposit on chain1 with commitment (created for withdraw on chain2)
- oracle passes commitment to chain2, chain3, chain4 (if anonymity desired)
- user waits to add anonymity then withdraws CHD on chain2 using a proof
- CHD are deposited in single side LP on the chain2 AMM

**circuit and cryptographic function constructions**

The cryptographic functions for off-chain use are implemented in the circomlib  library. Much of the mixer structure and solidity implantation of the Merkle Trees are taken from tornado cash, specifically Poseidon-tornado , a fork with a more efficient hashing algorithm. The Solidity implementation of the Poseidon hasher is created by Iden3 . The SNARK keypair and the Solidity verifier code are generated by the authors using SnarkJS, a tool also made by Iden3.

**further considerations**

*oracle methodology*

The security of the system relies completely on the oracle mechanism.  If the oracle mechanism was broken, false deposits could be created, and the pool could be drained.  Due to the potential regulatory issues of charon, the oracle must also be completely trustless and censorship resistant.  For this reason, and other aspects, systems such as native data bridges or Tellor will be used as the trustless bridge.  For the specific implementation, the use of longer delays for validation can be used to create a safer system.  Long delays allow users to see that Tellor (or another oracle) is being attacked, and then can dispute the malicious value to protect the charon deposits.  In the worst-case scenario that the oracle is completely compromised (their dispute voting mechanism is overtaken), the delay also enables current exposed users a window to withdraw funds, leaving the attacker with nothing.

An initial implemenation can be found here:  [GitHub - themandalore/charon: Privacy Enabled Cross-Chain Automated Market Maker](https://github.com/themandalore/charon)

**References:**

zero-knowledge proof - [Zero-knowledge proof - Wikipedia](https://en.wikipedia.org/wiki/Zero-knowledge_proof)

uniswap - https://uniswap.org/

balancer - [GitHub - balancer/balancer-core: Balancer on the EVM](https://github.com/balancer-labs/balancer-core)

polygon data bridge - [404 - Not found](https://docs.polygon.technology/docs/pos/state-sync/state-sync/)

tellor – [www.tellor.io](http://www.tellor.io)

tornado cash - [Tornado Cash · GitHub](https://github.com/tornadocash)

circomlib - [GitHub - iden3/circomlib: Library of basic circuits for circom](https://github.com/iden3/circomlib)

poseidon-torndao - [GitHub - ChihChengLiang/poseidon-tornado](https://github.com/ChihChengLiang/poseidon-tornado)

iden3 - [iden3 · GitHub](https://github.com/iden3)

[![CharonDiagram](https://ethresear.ch/uploads/default/optimized/2X/1/182f619576df13fabe562e427e1a9a21650237d6_2_690x430.png)CharonDiagram926×578 45.9 KB](https://ethresear.ch/uploads/default/182f619576df13fabe562e427e1a9a21650237d6)

a.	chain 1

b.	chain 2

c.	charon AMM on chain 1

d.	charon AMM on chain 2

e.	user

1. base token or chd deposit on chain 1
2. commitment sent with deposit
f.	oracle passes commitment to chain 2
g.	chd is minted when user presents zk proof of ownership over commitment
h.	user (likely same user, but anonymous)
