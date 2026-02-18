---
source: ethresearch
topic_id: 4513
title: Layer 2 gas payment abstraction
author: vbuterin
date: "2018-12-08"
category: Economics
tags: [account-abstraction, gas-abstraction]
url: https://ethresear.ch/t/layer-2-gas-payment-abstraction/4513
views: 7699
likes: 10
posts_count: 16
---

# Layer 2 gas payment abstraction

Suppose that a user wants to make an ERC20 token transfer, but pay transaction fees in that ERC20, instead of ether. We can do that without modifying the base layer protocol by extending the ERC20 protocol as follows. We add a function `submitSignedPayments({to: address, value: uint256, fee: uint256, deadline: uint256, seq: uint256, sig: bytes[65]}[])`, which works as follows. For each submitted payment:

- Let sender = ecrecover(hash(to, value, fee, seq, deadline, self), sig)
- Verify that balances[sender] >= value + fee
- Verify that seqs[sender] == seq
- Verify that block.number <= deadline
- Set balances[sender] -= value + fee
- Set balances[to] += value
- Set balances[msg.sender] += fee
- Set seqs[sender] += 1

Users wishing to send ERC20 tokens could publish offchain messages offering a fee, and then simply wait until someone includes their message in a transaction.

Note that the 21000 gas overhead of a publishing transaction can be shared between multiple ERC20 contracts, by creating a central routing contract that accepts a list of signed payment objects and then calls `submitSignedPayments` of each ERC20 contract with its associated signed payment as needed.

---

We can abstract this much further if we combine it together with an account abstraction scheme. Consider an abstraction scheme where user accounts are contracts, and transactions are calls to accounts, with the `msg.sender` set to the `block.coinbase`. We assume also that with account abstraction, users can create transactions that queue up multiple operations. However, user accounts can’t just be called by transactions, you can also have another contract call the user account as part of a transaction.

A user can send a transaction with two operations: (i) send the `msg.sender` some tokens of some ERC20, (ii) perform some other task. A series of transactions of this type can then be put into a wrapper transaction which pays ETH fees, which can then get published on chain. The publisher of the wrapper transaction would collect the tokens.

## Replies

**jtremback** (2018-12-10):

Coincidentally, the first part of this is exactly what we considered doing for Althea. Our ERC20 could mint tokens 1-1 from DAI, wrapping it. In addition to the gasless transfers it would also have gasless payment channel operations, plus an extra reward for “bounty hunting” by preventing an old update attack.

---

**austingriffith** (2018-12-10):

Yes! I love this kind of stuff. I did the first part for one of my weekly R&D pieces a couple weeks ago! I totally missed the deadline part but that would be important.

It seems like we should be integrating signed message recovery into all of our newly deployed contracts just to provide for better UX in the future.

Here is the repo with a screencast:

https://github.com/austintgriffith/native-meta-transactions

Here is the article:

https://medium.com/gitcoin/native-meta-transactions-e509d91a8482

As for batched signed messages, I like George at LimeChain’s:



      [github.com/LimeChain/batched-transactions](https://github.com/LimeChain/batched-transactions/blob/4198d8c1b46e6f8dc3cffefb9f0b2e165d576e50/contracts/MetaBatchProxy.sol#L40)





####

  [4198d8c1b](https://github.com/LimeChain/batched-transactions/blob/4198d8c1b46e6f8dc3cffefb9f0b2e165d576e50/contracts/MetaBatchProxy.sol#L40)



```sol


1.
2. /**
3. * @dev executes a transaction only if it is formatted and signed by the owner of this. Anyone can call execute. Nonce introduced as anti replay attack mechanism.
4. *
5. * @param target - the contract to be called
6. * @param value - the value to be sent to the target
7. * @param data - the data to be sent to be target
8. * @param dataHashSignature - signed bytes of the keccak256 of target, nonce, value and data keccak256(target, nonce, value, data)
9. */
10.
11. function execute(address[] target, uint256[] value, bytes[] data, bytes[] dataHashSignature) public onlyValidSignature(target, value, data, dataHashSignature) returns (bool) {
12. // solium-disable-next-line security/no-call-value
13. for(uint i=0; i< target.length; i++) {
14. require(target[i].call.value(value[i])(data[i]), 'unsuccesful call');
15. }
16. return true;
17. }
18.
19. }


```










The last part about account abstraction is out of my wheelhouse and I’ll have to read more. I’m assuming we aren’t just talking delegated execution through an identity contract.

---

**yoavweiss** (2018-12-10):

I recently submitted [ERC draft 1613](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1613.md) that supports similar operations, but extends to any dapp rather than specifically for tokens.

Basically it’s a protocol for adding “reverse charge” calls to contracts, using a central contract (RelayHub), through which multiple trustless relayers can “mine” transactions.  Adding a token-based payment mechanism on top of that EIP can be done in the recipient’s `map_relay()` function.

One primary difference from [@vbuterin](/u/vbuterin) 's suggestion above is that the user gets immediate guarantee that the transaction has been handled, without waiting for someone to pick the transaction from the pool.  The user selects the relayer from RelayHub’s registrar, interacts with the relayer, and gets a signed transaction that acts as a “performance bond”, ensuring that the relay will submit the transaction, or would be penalized otherwise.  Misbehaving relayers can be detected immediately without causing delays or malfunctions.

Trust is placed in the singleton contract (RelayHub) so the rest of the system is decentralized, with proper incentives to all actors to ensure that the system remains robust and fair.  The different actors in the system (relays, users, contracts) don’t need to trust each other, as behaviors are enforced by RelayHub.

Got some good feedback for the draft above from community members.  I’d love to get more.

Initial implementation available [here](https://github.com/tabookey-dev/tabookey-gasless).

---

**jtremback** (2018-12-10):

Thanks! I will look very closely at that medium article!

---

**PhABC** (2018-12-10):

This proposal is very similar to [ERC-865](https://github.com/ethereum/EIPs/issues/865), worth taking a look if you have time.

![](https://ethresear.ch/user_avatar/ethresear.ch/austingriffith/48/2947_2.png) austingriffith:

> The last part about account abstraction is out of my wheelhouse and I’ll have to read more. I’m assuming we aren’t just talking delegated execution through an identity contract.

A simplification of account abstraction would be to say that account abstraction is making all accounts *smart wallets* by default. For L2 account abstraction, Gnosis Safe is probably the best model that I know of.

---

**3esmit** (2018-12-11):

if `block.coinbase` is used instead of `msg.sender` and `msg.gasPrice == 0` then we could remove the transaction publisher signature verification, as it would be only bloating the processing and no represent no state change over publisher balance.

I posted this suggestion here [Gas Abstraction: Non signed "block validator"-only procedures](https://ethresear.ch/t/gas-abstraction-non-signed-block-validator-only-procedures/4388)

This is not necessary for the implementation of gas abstraction but nodes would benefit from less processing.

---

**3esmit** (2018-12-11):

I’m also working into a payment channel for paying the gas of transaction, where instead of the relayed transaction moving tokens it would simply kick a nonce in the payment channel, which would be necessary for payout using the sender signature.

This function is called by the Account Contract after the execution is complete:


      [github.com](https://github.com/status-im/snt-gas-relay/blob/8cc3479e2de1ca71623598e1d0f9db84ddeba20f/test-dapp/contracts/gasrelay/SimpleGasChannel.sol#L110)




####

```sol

1. _gasChannel
2. )
3. ),
4. _signature
5. ),
6. ERR_BAD_SIGNER
7. );
8.
9. _execute(_to, _value, _data);
10.
11. authorizeChannel(_gasChannel);
12. }
13.
14. /**
15. * @notice deploys contract in return of authorizing channel payout in an offchain agreement
16. * @param _value call value (ether) to be sent to newly created contract
17. * @param _data contract code data
18. * @param _gasLimit maximum gas of this transacton
19. * @param _gasChannel kicked NonceChannel which will charge for the execution
20. * @param _signature rsv concatenated ethereum signed message signatures required
21. */

```








That ends up in:


      [github.com](https://github.com/status-im/snt-gas-relay/blob/8cc3479e2de1ca71623598e1d0f9db84ddeba20f/test-dapp/contracts/payment/NonceChannel.sol#L68)




####

```sol

1. _signature
2. )
3. );
4. paid = _nonce;
5. process(_amount);
6. }
7.
8. /**
9. * @notice allows recipient to claim payout
10. */
11. function incrementNonce()
12. external
13. onlyController
14. {
15. nonce++;
16. }
17.
18. /**
19. * @notice extends channel sender withdraw lock
20. * @param _newExpiration timestamp of new expiration
21. */

```








Which is required here:


      [github.com](https://github.com/status-im/snt-gas-relay/blob/8cc3479e2de1ca71623598e1d0f9db84ddeba20f/test-dapp/contracts/payment/NonceChannel.sol#L51)




####

```sol

1. * @param _signature signer payoutHash signed
2. */
3. function payout(
4. uint256 _nonce,
5. uint256 _amount,
6. bytes calldata _signature
7. )
8. external
9. {
10. require(msg.sender == recipient, "Only recipient allowed");
11. require(_nonce  paid);
13. require(
14. signer == recoverAddress(
15. getSignHash(
16. getPayoutHash(_nonce, _amount)
17. ),
18. _signature
19. )
20. );
21. paid = _nonce;

```

---

**vbuterin** (2018-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavweiss/48/3050_2.png) yoavweiss:

> One primary difference from @vbuterin 's suggestion above is that the user gets immediate guarantee that the transaction has been handled, without waiting for someone to pick the transaction from the pool. The user selects the relayer from RelayHub’s registrar, interacts with the relayer, and gets a signed transaction that acts as a “performance bond”, ensuring that the relay will submit the transaction, or would be penalized otherwise. Misbehaving relayers can be detected immediately without causing delays or malfunctions.

What’s the point of this? The recipient gets no guarantee, because the sender could just double-spend by cooperating with a *different* relayer that uses a higher gasprice to move all their coins out.

---

**yoavweiss** (2018-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What’s the point of this? The recipient gets no guarantee, because the sender could just double-spend by cooperating with a different relayer that uses a higher gasprice to move all their coins out.

The guarantee is not for the tokens recipient. The recipient still needs to see the transaction mined on-chain. This is not a layer 2 network, but a way to transact on layer 1 without having ETH for gas. The guarantee is for the sender, that the relayer will actually relay it to the blockchain in a timely manner, with the parameters and gas price set by the sender.

The point is to avoid the need for an additional off-chain transaction pool, and guarantee that the transaction ends up in the mining pool. The sender selects a single relayer from the RelayHub registrar and talks to it (through web API or a similar channel) rather than submitting the transaction to a global relaying pool. Therefore the sender needs to know immediately whether the relayer relayed the transaction, and not wait for mining. Otherwise a group of malicious relayers could censor transactions by just stalling. If the relayer is misbehaving, the sender knows it immediately and connects to a different relayer, so the delay is measured in seconds rather than minutes. No way for a relayer to stall the sender from getting to the blockchain.

The motivation to talk to a single relayer from a decentralized relayers-pool, rather than a transaction pool, is to:

1. Not add delay, in addition to that of the Ethereum mining process. Gasless transactions take the same amount of time as normal transactions, and are as secure as normal trasactions.
2. Not require the use of a P2P protocol, since a similar level of censorship-resistance can be achieved through “standard” protocols. We’re trying to make Ethereum accessible to etherless users running mobile apps, possibly in restricted environments (e.g. enterprise/gov networks). As long as the user can open an http connection (even proxied), the user can transact on Ethereum. This removes two of the biggest technical obstacles for Ethereum adoption in such environments - the need for users to have ETH, and the requirement to use non-http protocols. Currently, mobile apps rely on centralized nodes (e.g. Infura) to communicate with the blockchain. This protocol decentralizes it while remaining practical for mobile apps and enterprise environments.

As for why this protocol achieves the desired level of censorship resistance, see “Attacks and mitigations” section under [EIPs/EIPS/eip-1613.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1613.md#rationale)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Users wishing to send ERC20 tokens could publish offchain messages offering a fee, and then simply wait until someone includes their message in a transaction.

What we’re doing here, is removing the `wait` and the `someone` from it.

The user is in control. The user selects a relayer to publish the transaction, agrees on the fee, and gets a service guarantee. At that point, the transaction is guaranteed to end up in the transaction pool with all other Ethereum transactions.

---

**hkalodner** (2018-12-11):

In the original proposal, assuming that there’s profit to be made from relaying transactions, the market should make sure that someone is willing to do so. There shouldn’t be any delay in this occurring since there will be race to earn what is essentially free money.

That actually points to an issue which is that there is a significant coordination problem. It’s likely that a large number of people will all attempt to submit the transaction assuming that there is a profit to be made. All of the transactions except for the first will fail and cost the submitter gas without any reward.

Selecting a particular relayer eliminates this issue.

---

**yoavweiss** (2018-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/hkalodner/48/2466_2.png) hkalodner:

> Selecting a particular relayer eliminates this issue.

Exactly. That’s part of what we were aiming to solve. The sender is the one most incentivized to get the transaction to the blockchain, so we leave it to the sender to find a relayer and negotiate the fee (and we give the sender the tools to do that, with on-chain information).

The sender and the contract are both incentivized to get the transaction delivered, so the system is focused on incentivizing relayers to provide the service, and lets the users and dapp owners decide who to work with, how much to pay, etc. Prices will be determined by the market, with rates published by relayers through RelayHub.

---

**jtremback** (2019-01-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/hkalodner/48/2466_2.png) hkalodner:

> That actually points to an issue which is that there is a significant coordination problem. It’s likely that a large number of people will all attempt to submit the transaction assuming that there is a profit to be made. All of the transactions except for the first will fail and cost the submitter gas without any reward.

Is this actually a problem? Sounds pretty similar to PoW which has worked so far.

Miners acting as relayers could include transactions which pay “gasless gas fees” to them in blocks they mine. If they get the block, they get the fees. If they don’t get the block, they don’t spend the gas.

---

**yoavweiss** (2019-01-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/jtremback/48/2634_2.png) jtremback:

> Is this actually a problem? Sounds pretty similar to PoW which has worked so far.
>
>
> Miners acting as relayers could include transactions which pay “gasless gas fees” to them in blocks they mine. If they get the block, they get the fees. If they don’t get the block, they don’t spend the gas.

Miners could be *part* of the solution (see below what they can’t provide). However, there may be a chicken and egg problem with starting from the miners:

- To support gasless transactions, miners need to agree to a soft-fork. No blockchain changes, but certainly mining code changes. They’re likely to accept the changes if there are enough dapps accepting relay calls and paying for them.
- Dapps owners need to modify their solidity code to accept relay calls and pay for them. They’re likely to do that if there’s a functioning network of relays, so they can actually benefit from it.

Who goes first? Miners accepting a soft-fork that complicates things and initially doesn’t make more money, or dapp owners adding “dead code” into their contract and hoping that miners will follow? Or maybe both sides will take a wait-and-see approach?

For such solution to work, it has to be implemented by the majority of miners. If only 10% of the miners enable gasless transactions, then a gasless transaction will take, on average, 10 times longer than a normal transaction. Usability will be poor, which defeats the whole purpose here - improving the onboarding process for etherless users. The solution won’t have any real value until it is widely adopted, and it may not be widely adopted until it provides real value.

[EIP 1613](https://github.com/ethereum/EIPs/blob/3beee14440508fe187b82f44d419c2cd22b1e2cf/EIPS/eip-1613.md) takes a practical approach. No network changes, no soft-fork, usable immediately and scales as needed. Once there are enough dapps implementing EIP 1613 to compensate relays, it is very likely that miners will accept the soft-fork and start mining gasless transactions, since this activity will become profitable immediately. EIP 1613 can break the tie above and become the path towards a miners-based solution.

Now let’s consider what’s required from a decentralized relays network, and see what miners can or cannot help us with:

1. Get transactions from etherless users.
2. Deliver the transactions to dapps.
3. Compensate relays/miners for the transactions, by means other than gas.
4. Dapps need to know the real sender, since msg.sender is now the relay/miner.
5. Dapps need to be able to decide which transactions they’re going to accept and pay for, based on the real sender or any other parameters of the transaction.

The miners based solution takes care of #1 and #2 (getting the transaction to the blockchain), which EIP 1613 currently handles by selecting a single relay and sending transactions via http.

It may seem as though #3 and #5 are unnecessary if you only consider ERC20 token contracts. The user can pay the miner with tokens as part of the transaction, as [@vbuterin](/u/vbuterin) suggested in this post. However… Ethereum is **not** ERC20.

Ethereum provides value to applications well beyond tokens, or at least that’s where we’re trying to take it by solving its UX challenges. Consider applications where transactions don’t transfer value and the user doesn’t hold any tokens. E.g. voting in a DAO or making a move in a game. What motivates the miner to relay such transaction?

To solve this for all dapps rather than just ERC20 contracts, #3 and #5 require a trustless mechanism for dapps to compensate the relay node, whether it’s a miner or an independent relay. Miners can’t just take ether from the dapp.  EIP 1613 compliant dapps take care of that by delegating trust to the central RelayHub contract and implementing the accept_relayed_call() function. A relay node (or a miner) only gets compensated for transactions accepted by the dapp, and therefore it will refuse to deliver calls that will be rejected (and therefore not compensated).

#4 requires telling the dapp who the real sender was. The relay node (or miner) cannot be trusted to deliver this information, as it could abuse it and perform unauthorized actions in the dapp. EIP 1613 takes care of that by having the central RelayHub contract extract the real sender address from the signature and delivering it to the dapp. The dapp replaces all calls with get_sender() which always returns the real sender, regardless of whether the transaction was gasless or normal. Unlike miners or relay nodes, RelayHub is an on-chain contract that can be trusted not to cheat.

Most of the EIP 1613 components (e.g. accept_relayed_call, get_sender, RelayHub) are still needed, regardless of whether the relay node is a miner or an independent node. The initial comm part (relay selection and http communication) is just one piece of the puzzle, meant to solve the problem **now** without waiting for miners to change their behavior. We can (and should) solve Ethereum’s UX challenges today, not in some future release.

The miners-based solution is an elegant long term solution, but it’ll be easier to pass the required soft-fork after there are already dapps implementing the protocol and paying for relay services. EIP 1613 is a practical way to get there.

---

**HarryR** (2019-01-02):

I keep coming back to an idea which could allow for transaction/payment abstraction and some interesting other things: **contingency payments**. I previously implemented this as part of a Plasma-style prototype, but I think it deserves some more attention.

Modifying the signature of the function to:

```auto
submitSignedPayments({to: address, value: uint256, fee: uint256, deadline: uint256, seq: uint256, dependencies: bytes32[], sig: bytes[65]}[])
```

Note the addition of a new parameter:

- dependencies: bytes32[]

Each payment can be contingent upon 0 or more other payments being submitted **within the same batch**. Where the dependency is the hash of every parameter (excluding the dependencies, and signature). The motivation for this is to allow for atomic swaps and complex multi-step transactions (like, possibly arbitrage)

Three examples:

- Atomic swap
- Pay for transactions using ERC-20 tokens
- Arbitrage (á la Loopring)

**However, the `nonce` (or `seq`) field hinders the ability for traders to make multiple speculative offers**, I can’t offer an exchange to two people using the same account with the same `seq` value, nor can I make an offer with a linear sequence as if the previous transaction isn’t submitted no subsequent transactions will be valid due to the `nonce` mismatch.

Ideally we want transaction parallelism in a way which allows speculative transactions to be negotiated but potentially never submitted to the chain. Two ways it could be achieved are:

- In addition to the seq field there is a batch/group ID for every account, any transaction which matches the batch ID is allowed. However, the owner of the account must also submit a separate signature which increments the sequence (to keep linearity, discard old transactions etc.) which changes the batch ID to an arbitrary new value (or even, leaves it the same)
- Transactions are only valid for one block, signed against the previous block hash.

**I think transaction parallelism is a problem, we need to overcome the limitations of a sequential nonce to allow speculative deals to be made off-chain, but only in conjunction with contingency payments or dependent transactions**

## Atomic Swaps

Two payments have each other as dependencies, Bob pays Alice 50 DERP, Alice pays Bob 100 LOLS. Either both are executed or neither are.

- Alice -> Bob depends on Bob -> Alice
- Bob -> Alice depends on Alice -> Bob

## Gas Payment using ERC-20

To submit one ERC-20 transaction from A \to B I really need 3 transactions:

1. A \to B
2. A \to TokenExchanger
3. TokenExchanger \to TransactionSubmitter

Yay badly formatted graphs:

1

1

2

2

1->2

A pays B

3

3

2->3

A exchanges token for ETH

3->1

ETH pays for Gas

I communicate with TokenExchanger off-line to negotiate a payment to a special address (for whoever the transaction submitter is) in return for sending them a number of tokens. The special address could be `0x0` or something similar - which is translated to `msg.sender` upon execution.

## Arbitrage

While LoopRing™® does something similar, I don’t like that it’s tokenised and it could be much more generic using this contingency / payment dependency mechanism.

The idea is: I find an arbitrage route, however I need funds that I don’t have to execute the deal.

On an open market I can solicit funding, I offer 100 DERP in return for 250 LOLS (above market rate). The parties involved know that this is a good deal and sign their parts of the transaction, but they don’t know how I’m able to provide the 250 LOLS.

I can then construct a chain of transactions which results in more than 250 LOLS being deposited to me, and I pocket the difference.

---

**3esmit** (2019-01-04):

Interesting.

Checking a transaction hash to be able to withdraw a payment was my first idea for “gas channel”, however right now EVM does not support loading a past transaction data by providing the transaction hash.

Instead of that I did “ping a payment channel” to allow the payout of gas, and the value of gas is agreed offchain.

Seems like you will need a PoS or something like that to allow this payments, as you will need an external source of trust to check if a dependent transaction was indeed included inchain for that one become invalid.

Or your implementing this architecture inside cryptographic proofs of a plasma contract?

