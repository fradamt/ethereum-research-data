---
source: magicians
topic_id: 12134
title: EIP-6123 - Smart Derivative Contract - frictionless processing of financial derivatives
author: pekola
date: "2022-12-13"
category: EIPs
tags: [erc, erc20]
url: https://ethereum-magicians.org/t/eip-6123-smart-derivative-contract-frictionless-processing-of-financial-derivatives/12134
views: 3988
likes: 8
posts_count: 27
---

# EIP-6123 - Smart Derivative Contract - frictionless processing of financial derivatives

# Smart Derivative Contract

We propose a deterministic decentralized post-trade process protocol for financial derivative contracts - known as Smart Derivative Contract. Counterparty credit risk is removed by construction. This protocol can make use of ERC20 token standard to guarantee frictionless and deterministic post-trade processing. Interface specification and reference implementation please see gitrepo below, for documentation see EIP-markdown-file.

## Abstract

The Smart Derivative Contract is a deterministic protocol to trade and process

financial derivative contracts frictionless and scalable in a complete automated way. Counterparty credit risk ís removed. Known operational risks and complexities in post-trade processing are removed by construction as all process states are fully specified and are known to the counterparties.

## Motivation

### Rethinking Financial Derivatives

By their very nature so-called “over-the-counter (OTC)” financial contracts are bilateral contractual agreements on the exchange of long-dated cash flow schedules. Since these contracts change their intrinsic market value due to changing market environments they are subject to counterparty credit risk when one counterparty is subject to default.The initial white paper describes the concept of a Smart Derivative Contract with the central aim to detach bilateral financial transactions from counterparty credit risk and to remove complexities in bilateral post-trade processing by a complete redesign.

### Concept of a Smart Derivative Contract

A Smart Derivative Contract is a deterministic settlement protocol which has the same economical behaviour as a collateralized OTC Derivative. Every process state is specified and therefore the entire post-trade process is known in advance. A Smart Derivative Contract (SDC) settles outstanding net present value of the underlying financial contract on a frequent basis. With each settlement cycle net present value of the underlying contract is exchanged and the value of the contract is reset to zero. Pre-Agreed margin buffers are locked at the beginning of each settlement cycle such that settlement will be guaranteed up to a certain amount.

In case a counterparty fails to obey contract rules, e.g. not provide sufficient prefunding, SDC will terminate automatically with the guaranteed transfer of a termination fee by the causing party.

These features enable two counterparties to process their financial contract fully decentralized without relying on a third central intermediary agent.

Process logic of SDC can be implemented as a finite state machine on solidity. ERC20 token standard can be used for frictionless decentralized settlement - see reference implementation.

Combined with an appropriate external market data and valuation oracle which calculates net present values, each known OTC derivative contract is able to be processed using this standard protocol.

## Rationale

The interface design and reference implementation is based on following considerations:

- A SDC protocol is supposed to be used by two counterparties and enables them to initiate and process a derivative transaction in a bilateral and digital manner.
- Therefore contract interface specification is supposed to completely reflect the trade livecycle.
- The interface specification is generic enough to handle the case that two counterparties process one or even multiple transactions (on a netted base)
- Usually the valuation of an OTC trade will require complex valuation methodology. Therefore the concept will in most cases rely on external market data and valuation algorithms
- A pull-based valuation based oracle pattern is specified by a simple callback pattern (methods: initiateSettlement, performSettlement)
- The reference implementation SDC.sol is based on a state-machine pattern where the states also serve as guards (via modifiers) to check which method is allowed to be called at a particular given process and trade state

## EIP markdown file

- Please see eip-6123.md

## Further information

For further information on the concept please visit:

https://www.finmath.net/finmath-smart-derivative-contract/

## Replies

**cfries** (2022-12-16):

I believe the PR looks fine now. Is there anything that needs to be done on our side?

---

**cfries** (2023-08-09):

[@pekola](/u/pekola) : Given that we have some new use cases that would require some (small?) changes/improvement to this interface, I wonder: can we still modify the current EIP-6123 or should we keep it as is and create a new one?

---

**pekola** (2023-08-09):

Hi [@cfries](/u/cfries). The enhanced interface proposal could cover more use cases / implementations. In my opinion a new EIP proposal for such an enhanced SDC would be hard to separate from 6123. Wondering, what is common practice regarding changing the interface of ERC-EIPs which are in Draft Mode?

[@Pandapip1](/u/pandapip1) - could you help out on this question. Thanks

---

**Pandapip1** (2023-09-01):

In Draft? Feel free to make whatever changes you want!

---

**cfries** (2023-10-16):

We made some updates. The interface has been slightly extend and modify to better support different implementation variants and different financial products (smart financial contracts). More examples using EIP-6123 will follow.

The reference implementation has been updated accordingly. As well as the documentation and unit tests.

See [Update EIP-6123: Move to Draft by cfries · Pull Request #7857 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7857)

---

**cfries** (2023-10-16):

**Note:**

The new interface is available via `@finmath.net/sdc@0.3.0`

The old interface is available via `@finmath.net/sdc@0.2.3`

See [@finmath.net/sdc - npm](https://www.npmjs.com/package/@finmath.net/sdc)

([@pekola](/u/pekola) @kourouta )

---

**cfries** (2023-10-26):

I have moved the EIP to the new ERC repository. I have added the package.json and hardhat-config files.

The new version is pushed as 0.3.1 to npm:

https://www.npmjs.com/package/@finmath.net/sdc

---

**cfries** (2023-11-03):

Dear All.

As EIP-6123 may have relevance for the European Central Bank’s “exploratory phase for central bank money settlement of wholesale financial transactions” we would like to make some small changes.

However, there are a few PRs in the pipeline. I saw that PR of EIP-6123 (move to draft) is not on the list for the office hours. Will there be longer delays, e.g., given the ERC/EIP split? [@Pandapip1](/u/pandapip1)

https://github.com/ethereum/ERCs/pull/25

[@Kourouta](/u/kourouta) [@pekola](/u/pekola)

---

**Julius278** (2024-07-01):

Dear all,

as the whole applications evolves, I recognized a possible improvement in ISDC.sol / TradeSettlementRequest event.

As in the TradeIncepted event, we should add a initiator (address) to the event like:

`event TradeSettlementRequest(address initiator, string tradeData, string lastSettlementData);`

So if the event gets intercepted, you are directly able to recognize if you should perform the settlement or wait for the counterparty. That would also prevent one of the counterparties from getting an error cause being a bit later than the other one (TradeState is already changed, settlement aready performed), so one counterparty is able to skip this step.

Best regards,

Julius

[@cfries](/u/cfries) [@pekola](/u/pekola)

---

**pekola** (2024-07-01):

Nice and important improvement. Having an off-chain oracle in place and adding the address to the ValuationRequestEvent we then can perform a check on the eligibility of the party calling “initiateSettlement” by just listening to the event log and then check if a valuation can be performed. Correct [@Julius278](/u/julius278) ?

---

**Julius278** (2024-07-01):

Thats correct [@pekola](/u/pekola).

Also as we’re talking about eligibility, the `TradeSettlementPhase` should get the same additional parameter. So both parties are able to understand the relevant transactions of the other party and whether this is authorized.

Irrespective of the fact that it must of course also be checked in the actual contract.

---

**Julius278** (2024-07-01):

For some reason I can not post links here, so this is the reference to my pull request:

ethereum/ERCs/pull/515

[@pekola](/u/pekola) [@cfries](/u/cfries)

---

**cfries** (2024-07-01):

Julius. This is a good addition. I already added that one. Thank you!

---

**Julius278** (2024-07-02):

Hi Christian,

thanks for adding the initiator to the the TradeSettlementRequest event.

I guess it would also make sense in the settlement phase event which is emitted after “performSettlement”:

event TradeSettlementPhase(address initiator);

As described above, this would help both parties to recognize who exactly did which step.

Or if there is a third monitoring / supervising / … party or authority.

Best regards,

Julius

---

**Julius278** (2024-07-02):

oh, forgot to mention you in my last comment [@cfries](/u/cfries)

---

**Anais** (2024-07-02):

Dear [@cfries](/u/cfries), [@pekola](/u/pekola) ,  few items to consider:

- Netting: The EIP states “The interface specification is generic enough to handle the case that parties process one or even multiple financial transactions (on a netted base),” but the current interface does not explicitly specify how. Maybe standardizing this could be valuable.
- Batch operations: To reduce gas costs, could it be interesting to add methods that allow for batching multiple operations into a single transaction? Or should it be left to implementers?
- Upgradability: This is more for the reference implementation, but I think it could be worthwhile to address upgradability explicitly so that ERC-6123 implementers consider best practices, particularly when implementing long-term derivative contracts.

Kind regards,

Anaïs

---

**cfries** (2024-07-11):

Dear Anais.

I have added the two method to perform a cancelation of an open request (which you suggested at another place). I believe this is a very good addition.

For netting and batch operations: I believe this could be an implementation detail. But maybe I have think about this a bit more.

Christian

---

**Julius278** (2024-07-11):

Hi [@cfries](/u/cfries),

as I discussed today with Peter, wouldnt it be nice to have a event called “PaymentTriggered”

```auto
/**
     * @dev Emitted during Settlement phase in case an offchain settlement is needed
     * @param _hash - checksum
     * @param sdcAddress - address of the sdc trade
     * @param _fromId - payer ID for offchain system
     * @param _toId - receiver ID for offchain system
     * @param _amount - payment amount
     * @param _fromAddress - payer onchain address
     * @param _toAddress - receiver onchain address
     */
    event PaymentTriggered(string _hash, address sdcAddress, string _fromId, string _toId, uint256 _amount, address _fromAddress, address _toAddress);
```

and a function like:

```auto
/**
     * @dev Performs the initialization of a party, stores an onchain address associated with an offchain ID
     * @param partyAddress - onchain address
     * @param partyId - ID for offchain system
     */
    function initParty(address partyAddress, string memory partyId) external;
```

in the IERC20Settlement.sol interface, especially for offchain settlements.

In this case an offchain system which listens to onchain events could initiate a (e.g. real money) payment.

You could also create a new interface like

```auto
interface IOffchainERC20Settlement is IERC20Settlement {.....}
```

and at first only include these two elements (event and function from last reply) but I’m not quite sure if this is needed at the moment.

Best regards,

Julius

[@pekola](/u/pekola) fyi

---

**cfries** (2024-07-11):

I have to think about this a bit. But a quick reflex is that the IERC20Settlement.sol is part of the reference implementation but not part of the ERC 6123 (at least, in the strict sense, as I see it). …   on the other hand, the IERC20Settlement.sol is part of the npm package.

---

**Julius278** (2024-07-12):

Hi [@cfries](/u/cfries),

two additions again (sorry ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)) for SDC.sol:

1. I would suggest to remove the overwriting of tradeID variable
tradeID = Strings.toString(transactionHash);
the transactionHash is not really unique as a new trade could have the same setup.
You could consider doing a check if the tradeId is already set and only if not then set to a random one. For the random one you could, for example, add the blocknumber to the hash which would provide more uniqueness.
2. please add a getter function for the mutuallyTerminated variable like:

```auto
    function isMutuallyTerminated() public view returns (bool) {
        return mutuallyTerminated;
    }
```

it will show if a trade was terminated mutually or by an error.

Kind regards,

Julius


*(6 more replies not shown)*
