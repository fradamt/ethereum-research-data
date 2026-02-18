---
source: ethresearch
topic_id: 1734
title: Application-layer account abstraction
author: JustinDrake
date: "2018-04-14"
category: Sharding
tags: []
url: https://ethresear.ch/t/application-layer-account-abstraction/1734
views: 2934
likes: 2
posts_count: 7
---

# Application-layer account abstraction

**TLDR**: We suggest a way to bootstrap accounts into account abstraction schemes at the application layer.

**Construction**

We build an “abstractor” contract to emulate account abstraction at the application layer. The abstractor has “virtual accounts” serving as “virtual entry points” for “virtual transactions”. Each virtual account has a “virtual balance” and “virtual init code”.

To make it to their virtual entry points, virtual transactions are broadcast by users to proposers. Those are executed locally, selected, batched and finally wrapped by proposers in a single “dummy transaction” where:

- The sender address is a fresh ephemeral account with zero balance
- The nonce is set to 0
- The gas price is set to 0
- The gas limit is set to 8,000,000
- The recipient address is set to the abstractor’s address
- The value is set to 0

The EVM unwraps the dummy transaction and sends the virtual transaction batch to the abstractor. Individual virtual transactions are then processed sequentially as expected:

1. They are parsed by the abstractor to extract the associated “virtual sender address”, virtual gas price", “virtual gas limit”, “virtual data”, “virtual recipient address”, virtual signature", “virtual nonce”, etc.
2. The virtual signature and virtual nonce are checked against the virtual init code of the virtual sender account and the abstractor throws if the checks fail.
3. If the virtual balance is less than the virtual gas price times the virtual gas limit the abstractor throws, and the virtual balance is sent to the coinbase.
4. The abstractor calls the contract specified by the virtual recipient address with the virtual data, and a gas limit set to the virtual gas limit.
5. The abstractor rewards the coinbase with the gas used in step 4) times the virtual gas price.

Other details of account abstraction (e.g. init code filling) are similarly handled by the abstractor.

**Discussion**

The default signature and nonce infrastructure is bypassed by using an ephemeral account with 0 gas price and nonce, and a dummy signature. This makes it possible to have alternative transaction entry points (e.g. to support UTXOs, quantum-secure signatures, ERC20 gas) without being burdened by ECDSA signatures and nonces.

Pushing account abstraction to the application layer keeps the protocol layer simple. Simultaneously, different abstraction schemes can compete and evolve organically at the application layer, and explore the gamut of tradeoffs that a one-size-fits-all abstraction scheme may fail to capture.

Going further, we may be able to reuse the above bootstrap strategy on a transaction entry point that is simpler than Ethereum 1.0 accounts to remove enshrined infrastructure such as gas prices, nonces and ECDSA signatures, all without enshrining abstraction-specific infrastructure such as PAYGAS, BREAKPOINT or PANIC opcodes.

## Replies

**3esmit** (2018-04-15):

I’m working in Identity smart contract, which probably does this Application-layer account abstraction.

I already have an adaptor to enable abstraction of gas token, and the keys can be used to sign or multisign transactions, and also a decentralized recovery account.

I will follow this thread to find some ideas to improve my current work.

---

**jamesray1** (2018-04-18):

It’d be great if you could have more categories or tags for each post, e.g. sharding, phase 2, EVM, phase 1, networks, protocol architecture, etc. I see that you can create posts with a subcategory for Casper. At the moment I only care about implementing phase 1, I don’t want to know much about phase 2 or later until I get to a point where such things are ready to be implemented. Then I get a notification for just new posts in phase 1, not all posts in the sharding category.

---

**skilesare** (2018-04-18):

I’d love to see some thing like this in practice. What would a contract that does this looks like?

---

**3esmit** (2018-05-01):

Sorry for the slow response, but here it is:


      [github.com](https://github.com/status-im/contracts/blob/150-gas-abstraction/contracts/identity/IdentityGasRelay.sol)




####

```sol
pragma solidity ^0.4.21;

import "./Identity.sol";
import "../common/MessageSigned.sol";
import "../token/ERC20Token.sol";

/**
 * @title IdentityGasRelay
 * @author Ricardo Guilherme Schmidt (Status Research & Development GmbH)
 * @notice enables economic abstraction for Identity
 */
contract IdentityGasRelay is Identity {

    bytes4 public constant MSG_CALL_PREFIX = bytes4(keccak256("callGasRelay(address,uint256,bytes32,uint256,uint256,address)"));
    bytes4 public constant MSG_DEPLOY_PREFIX = bytes4(keccak256("deployGasRelay(uint256,bytes32,uint256,uint256,address)"));
    bytes4 public constant MSG_APPROVEANDCALL_PREFIX = bytes4(keccak256("approveAndCallGasRelay(address,address,uint256,bytes32,uint256,uint256)"));

    event ExecutedGasRelayed(bytes32 messageHash);
    event ContractDeployed(address deployedAddress);

```

  This file has been truncated. [show original](https://github.com/status-im/contracts/blob/150-gas-abstraction/contracts/identity/IdentityGasRelay.sol)








https://github.com/status-im/contracts/blob/145-identity/contracts/identity/Identity.sol


      [github.com](https://github.com/status-im/swarms/blob/master/ideas/150-gas-abstraction.md)




####

```md
---
id: 150-gas-abstraction
title: Gas Abstraction
status: Draft
created: 2018-02-01
category: core
lead-contributor: 3esmit
contributors:
    - 3esmit
    - richard-ramos
    - iurimatias
    - alexvandesande
exit-criteria: no
success-metrics: yes
clear-roles: yes
future-iterations: no
---

# Gas Abstraction

```

  This file has been truncated. [show original](https://github.com/status-im/swarms/blob/master/ideas/150-gas-abstraction.md)









      [github.com](https://github.com/status-im/swarms/blob/master/ideas/145-identity.md)




####

```md
---
id: 145-identity
title: Self-soverign Identity
status: Draft
created: 2018-05-04
category: core
lead-contributor: 3esmit
contributors:
    - 3esmit
    - richard-ramos
    - alexvandesande
exit-criteria: yes
success-metrics: yes
clear-roles: yes
future-iterations: yes
---

# Self-sovereign Identity

## Preamble
```

  This file has been truncated. [show original](https://github.com/status-im/swarms/blob/master/ideas/145-identity.md)








Note that this still under development.

---

**naterush** (2018-05-02):

One concern is that “2nd layer marketplace” schemes like this make it harder for users to calculate the correct fees to pay for their transactions. In general, I feel like we should make it as easy as possible for users to figure out the fees they have to pay to get their transaction included - as of now, it’s hard enough that users have to trust services like [Eth Gas Station](https://ethgasstation.info/) to figure out what the correct fees to pay are.

In general, I feel like we need to be clear with the desiderata we have for our fee markets. “Easy to find the ‘correct’ fee” seems like an important one, IMO - and there are schemes one can imagine that do a much better job of this than even what we have now.

P.S. I implemented a scheme like this for [uPort](https://www.uport.me/) last summer. For anyone interested, it can be found [here](https://github.com/uport-project/uport-identity/blob/develop/contracts/TxRelay.sol).

---

**3esmit** (2018-05-04):

By using gasPrice and gasLimit instead of fee in the inner transaction makes easier to calculate transaction.

Having known the fixed amount the outer transactions consumes to verify signature and change token storage.

The way GasRelay contract is implemented makes possible to gas relayer actor checking if inner transaction signer account contain funds to pay the fee and how much itself will pay for each token.

Also inner transaction signer actor can know how much tokens it will pay for each gas cost and at up to what limit.

It just reimplements the same techniques used by ethereum but accepting any ERC20Token, or ether stored in the account contact itself.

However, each ERC20Token implementation can have different cost of “transfer”, and the cost is usually different from when “initializing” the address balance for the first time and the second consecutive times.

The main idea is to make keys without ether or tokens be able to control the account that holds the tokens.

Gas relayer actor, as msg.sender in gas relay action, authorizes uses of its own “ether” as gas to “call” the contract, with verified parameters signed by accounts defined in contract storage.

