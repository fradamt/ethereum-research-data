---
source: magicians
topic_id: 4340
title: EIP ? - CallWithSigner as a potential fix for the msg.sender problem
author: stonecoldpat
date: "2020-06-04"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-callwithsigner-as-a-potential-fix-for-the-msg-sender-problem/4340
views: 1836
likes: 4
posts_count: 8
---

# EIP ? - CallWithSigner as a potential fix for the msg.sender problem

Hi all,

We have been working on a non-custodial relayer (e.g. proxy bidder) called any.sender. Bob can send any.sender a transaction via the API and any.sender gradually bumps the fee until it gets in. Its a pretty useful service as products can focus on actually building their product and not boring/very tedious transaction infrastructure.

We came across the msg.sender problem while we were building any.sender. To quickly summarise, if your contract relies on msg.sender to authenticate the caller and Bob has registered his EOA with the contract, then it is impossible for Alice to send a transaction on behalf of Bob. This is because an Ethereum Transaction intertwines who is paying the gas (Alice) and who wants to execute a smart contract (Bob).

There are several smart contract solutions to mitigate the problem including msgSender() and the adoption of wallet contracts. However, both solutions do not come for free and I’ve listed several problems in the write-up. So please check there for more information.

I believe  we should solve this problem at the platform / EVM-level, so non-custodial third party relay infrastructure can become a native citizen of Ethereum (alongside various other use-cases).

I have a detailed write up here on a potential solution to help kick-start the discussion:


      [github.com](https://github.com/anydotcrypto/metatransactions/blob/12fcf12b29def78fc46a8c02eb47bf549f6148c4/docs/EIP-proposal.md)




####

```md
---
eip:
title: CallWithSigner - A new CALL opcode to replace msg.sender with the signer's address
author: Patrick McCorry (@stonecoldpat) & Chris Buckland (@yahgwai)
discussions-to:
status: draft
type: Standards Track
category: Core
created: 2020-05-11
---

## Simple Summary

Ethereum transactions intertwine the identity of who paid for the transaction (tx.gaspayer) and who wants to execute a command (msg.sender). As a result, it is not straightforward for Alice to pay the gas fee on behalf of Bob who wants to execute a command in a smart contract. If this issue can be fixed, then it allows Bob, without any significant hurdles, to outsource his transaction infrastructure to Alice in a non-custodial manner. This EIP aims to alleviate the issue by introducing a new opcode, `callWithSigner()`, in the EVM.

## Abstract

It is common practice to authenticate the immediate caller of a contract using msg.sender. An immediate caller can be the externally owned account that signed the Ethereum Transaction or another smart contract. We propose a third option, `callWithSigner()`, that checks if an externally owned account has authorised the command (alongside relevant replay protection) before calling the target contract. If the checks pass, then the target contract is invoked and externally owned account is assigned as msg.sender.

## Motivation
```

  This file has been truncated. [show original](https://github.com/anydotcrypto/metatransactions/blob/12fcf12b29def78fc46a8c02eb47bf549f6148c4/docs/EIP-proposal.md)








Given my quirky academic background it is a bit long, but in essence it proposes a new opcode/precompile:

```auto
targetContract.callWithSigner(callData, value, replayProtection, signature,  signer)
```

It is similar in style to CALL, DELEGATECALL, etc. The precompile verifies:

- The user has signed the target contract + function call
- The user’s replay protection is valid (e.g. unique transaction)

If successful, it swaps msg.sender == the signer’s address and executes the target contract with the desired data.

There are several other ways to solve the problem, most notably to modify the Ethereum Transaction format. I believe a new precompile/opcode is probably the best approach as it is the least intrusive e.g. it doesn’t change any existing infrastructure / client tooling.

It would be great if others are happy to read the proposal and help me kick-start a discussion here. While I think it is a nifty way to solve the problem, there may be superior ways to do it (e.g. full-fledged account abstraction) - so let’s start working it out together.

By the way - this impacts anyone working on meta-transaction infrastructure that includes:

- any.sender
- gas station network
- authereum
- 0x
- Gnosis safe
- Pillar wallet
-… so on

## Replies

**matt** (2020-06-05):

I agree with the sentiment here that this is a **platform** problem and should not be solved by smart contracts. However, I am concerned with how this proposal would affect transaction validation logic.

There is currently an invariant in mempools that essentially says “if a transaction from an account is determined to be valid, it will continue to be valid until a new block is received that invalidates it.” This EIP would violate this invariant because *any* new transaction could invalidate *any* pending transaction. Furthermore, it would be impossible to know if that is the case before fully executing each transaction. We should better understand how important it is to maintain this behavior and explore if this exposes new attack vectors.

Right now I prefer extending the transaction object to support an additional `sponsor` signature. Although `CallWithSigner` seems to offer more flexibility in the near-term (payments to a relayer can be processed within the same transaction) there is an [increased desire](https://ethresear.ch/t/meta-transactions-oil-and-karma-megathread/7472) to remove the observability of gas during execution. This would likely make untrusted `*CALL`s unreliable, because reverts would cascade up and therefore would not be catchable in the parent frame.

> there may be superior ways to do it (e.g. full-fledged account abstraction)

I believe AA could potentially provide a [one-time breakpoint](https://ethresear.ch/t/oil-adding-a-second-fuel-source-to-the-evm-pre-eip-v1-1/7425/2) for performing the accounting that currently takes advantage of gas observability. This is an area that has been underexplored. A fairly analogous idea to `CallWithSigner` in AA might be a `PAYGASFROM` opcode which takes the normal parameters of `PAYGAS` plus an `sponsor` signature. I believe this approach is preferable to `CallWithSigner` because it i) puts a bound on how much computation per transaction must be done to *know* if other transactions will become invalid and ii) this bound is configurable by clients.

This is important problem, I’m glad it’s being discussed.

---

**sergio_lerner** (2020-06-08):

I have a couple of issues with  the proposal, and I’m inclined for an approach of having an additional sponsor signer of the transaction. I’ll explain here.

1. minor: The multi-queue adds a SSTORE gas cost to the call. This cost would vary between 5000 (updating the nonce of a queue that does exists to 20000 for creating a new queue). A sponsor-signature added to the transaction also needs to update its nonce, but the lookup of the account node has already been done, so the cost is actually lower.
2. Main: Signatures used in CallWithSigner get embedded in transaction arguments, and are not segregated. Therefore they cannot be later batched, or pruned, which is something Ethereum could do in the future using SNARKs. If Ethereum implemented SNARK proofs of batched signatures,  the senders must still be stored, because they are included in the signatures via public-key-recovery, so the space savings would be about 40% for simple transactions, yet it’s an important saving. I think signatures should always be segregated to increase the chances that future improvements in SNARKs allow compression of signatures via a single proof.
3. Implementation: You’re not committing to the amount of gas to pass the callee with the signature.
Sign(keccak256(targetContract, callData, value, replayProtection, chainid))
Therefore a front-running attack can be to execute the call the minimum gas (2300) and prevent any other execution future execution. The call should also commit to a minimum amount of gas to pass (or the the exact amount). In RSK the call should also commit to the minimum stack depth.

Regards!

---

**stonecoldpat** (2020-06-15):

> There is currently an invariant in mempools that essentially says “if a transaction from an account is determined to be valid, it will continue to be valid until a new block is received that invalidates it.” This EIP would violate this invariant because any new transaction could invalidate any pending transaction. Furthermore, it would be impossible to know if that is the case before fully executing each transaction. We should better understand how important it is to maintain this behavior and explore if this exposes new attack vectors.

I just updated the EIP to better reflect this point. So one alternative proposal was to use the existing account system for the replay protection. But as you mention, this will break the txpool invariant (e.g. was a nonce already used)

In the EIP, the preferred approach is for the new opcode/recompile to take care of the replay protection directly. So it will storing a mapping of addresses => nonces. The pros/cons:

Pro:

- We can have better replay protection such as MultiNonce. e.g. support up to N concurrent and out-of-order transactions (good if you want to process 1000s of withdrawals, order does not matter)
- It is independent of the account system. So it does not impact already pending transactions. It would just fail the same way as a normal CALL().

Con:

- I don’t know of another precompile that maintains state. Might be problems around that.
- Ethereum maintains two different replay protections. One for the account system, one for the opcode. It might be a nice way to eventually transition away from the account system.

---

**stonecoldpat** (2020-06-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sergio_lerner/48/1759_2.png) sergio_lerner:

> I have a couple of issues with the proposal, and I’m inclined for an approach of having an additional sponsor signer of the transaction. I’ll explain here.
>
>
> minor: The multi-queue adds a SSTORE gas cost to the call. This cost would vary between 5000 (updating the nonce of a queue that does exists to 20000 for creating a new queue). A sponsor-signature added to the transaction also needs to update its nonce, but the lookup of the account node has already been done, so the cost is actually lower.
> Main: Signatures used in CallWithSigner get embedded in transaction arguments, and are not segregated. Therefore they cannot be later batched, or pruned, which is something Ethereum could do in the future using SNARKs. If Ethereum implemented SNARK proofs of batched signatures, the senders must still be stored, because they are included in the signatures via public-key-recovery, so the space savings would be about 40% for simple transactions, yet it’s an important saving. I think signatures should always be segregated to increase the chances that future improvements in SNARKs allow compression of signatures via a single proof.
> Implementation: You’re not committing to the amount of gas to pass the callee with the signature.
> Sign(keccak256(targetContract, callData, value, replayProtection, chainid))
> Therefore a front-running attack can be to execute the call the minimum gas (2300) and prevent any other execution future execution. The call should also commit to a minimum amount of gas to pass (or the the exact amount). In RSK the call should also commit to the minimum stack depth.
>
>
> Regards!

1. Yeah, it should add extra storing costs. e.g. the extra SSTORE. Since its a precompile, it might be possible to make it slightly cheaper?
2. You can put the opcode in a batching contract. So then you can send several transactions via the batch contract (although it does require an additional signature check each time). Since its in the calldata, I don’t think it helps with a snark in the transaction. But possibly in the future, it would be SNARKED at the contract-layer. e.g. I can prove this contract executed correctly. Or be useful in an ORU setup.

1. Nice catch. I updated the EIP to sign the gas limit too!

---

**stonecoldpat** (2020-06-15):

I can’t seem to edit the main post, so I updated EIP here:


      [github.com](https://github.com/anydotcrypto/metatransactions/blob/60a34c36c687553eb8a10426382144fdf1edae66/docs/EIP-proposal.md)




####

```md
---
eip:
title: CallWithSigner - A new CALL opcode to replace msg.sender with the signer's address
author: Patrick McCorry (@stonecoldpat) & Chris Buckland (@yahgwai)
discussions-to:
status: draft
type: Standards Track
category: Core
created: 2020-05-11
---

## Simple Summary

Ethereum transactions intertwine the identity of who paid for the transaction (tx.gaspayer) and who wants to execute a command (msg.sender). As a result, it is not straightforward for Alice to pay the gas fee on behalf of Bob who wants to execute a command in a smart contract. If this issue can be fixed, then it allows Bob, without any significant hurdles, to outsource his transaction infrastructure to Alice in a non-custodial manner. This EIP aims to alleviate the issue by introducing a new opcode, `callWithSigner()`, in the EVM.

## Abstract

It is common practice to authenticate the immediate caller of a contract using msg.sender. An immediate caller can be the externally owned account that signed the Ethereum Transaction or another smart contract. We propose a third option, `callWithSigner()`, that checks if an externally owned account has authorised the command (alongside relevant replay protection) before calling the target contract. If the checks pass, then the target contract is invoked and externally owned account is assigned as msg.sender.

## Motivation
```

  This file has been truncated. [show original](https://github.com/anydotcrypto/metatransactions/blob/60a34c36c687553eb8a10426382144fdf1edae66/docs/EIP-proposal.md)

---

**matt** (2020-06-16):

[@stonecoldpat](/u/stonecoldpat), would EIP-2711 sponsored transactions (+ tx batching) support your needs? How would it affect your use cases if batching wasn’t possible?

---

**stonecoldpat** (2020-06-16):

For any.sender we assume the gas is paid up front, so the sponsored transaction approach works OK for us in the long-term.

The batching is useful if you want to combine relay payment on-demand with the relayed transaction:

- Accept payment from the user / refund the relay keys for the transaction.
- Execute the user’s transaction

The relayer is only paid the the user’s transaction is executed. This is what we do now:

```auto
  // @param _relayTx A relay tx containing the job to execute
    // @param _gasRefund Whether the relayer requires a gas refund
    // @dev Only authorised relayer can execute relay jobs and they are refunded gas at the end of the call.
    //      Critically, if the relay job fails, we can simply catch exception and continue to record the log.
    function execute(RelayTx memory _relayTx, bool _gasRefund) public {
        uint gasStarted = gasleft();

        // The msg.sender check protects against two problems:
        // - Replay attacks across chains (chainid in transaction)
        // - Re-entrancy attacks back into .execute() (signer required)
        require(relayers[msg.sender], "Relayer must call this function.");
        require(_relayTx.relay == address(this), "Relay tx MUST be for this relay contract.");

        bytes32 relayTxId = computeRelayTxId(_relayTx);

        // Only record log if a compensation is required
        if(_relayTx.compensation != 0) {
            // Record a log of executing the job, Each shard only records the first job since the first job has the
            // earliest timestamp.
            setRecord(relayTxId, block.number);
        }

        // We do not require the customer to sign the relay tx.
        // Why? If relayer submits wrong relay tx, it wont have the correct RelayTxId.
        // So the RelayTxId won't be recorded and the customer can easily prove
        // the correct relay tx was never submitted for execution.

        // In the worst case, the contract will only send 63/64 of the transaction's
        // remaining gas due to https://eips.ethereum.org/EIPS/eip-150
        // But this is problematic as outlined in https://eips.ethereum.org/EIPS/eip-1930
        // so to fix... we need to make sure we supply 64/63 * gasLimit.
        // Assumption: Underlying contract called did not have a minimum gas required check
        // We add 1000 to cover the cost of calculating new gas limit - this should be a lot more than
        // is required - measuring shows cost of 58
        require(gasleft() > (_relayTx.gasLimit + _relayTx.gasLimit / 63) + 1000, "Not enough gas supplied.");

        // execute the actual call
        (bool success,) = _relayTx.to.call.gas(_relayTx.gasLimit)(_relayTx.data);

        // we add some gas using hard coded opcode pricing for computation that we could measure
        uint gasUsed = gasStarted - gasleft() + // execute cost
                            (msg.data.length * 16) + // data input cost (add 1 for gasRefund bool)
                            2355 + // cost of RelayExecuted event - 375 + 375 + 375 + (160 * 8)
                            21000; // transaction cost

        if(_gasRefund) {
            gasUsed += (9000 + 1000); // refund cost, send + change for calculations
            if(!msg.sender.send(gasUsed*tx.gasprice)) {
                // Notify admin we need to provide more refund to this contract
                emit OutOfCoins();
            }
        }

        emit RelayExecuted(relayTxId, success, _relayTx.from, _relayTx.to, gasUsed, tx.gasprice);
    }
```

GSN does something similar here to charge the pay master after executing the call:


      [github.com](https://github.com/opengsn/gsn/blob/master/contracts/RelayHub.sol#L220)




####

```sol

1. workerToManager[msg.sender],
2. relayRequest.relayData.paymaster,
3. relayRequest.relayData.senderAddress,
4. relayRequest.target,
5. msg.sender,
6. vars.functionSelector,
7. revertReason);
8. return (vars.success, revertReason);
9. }
10.
11. // From this point on, this transaction will not revert nor run out of gas, and the paymaster will be charged
12. // for the gas spent.
13.
14. {
15. //How much gas to pass down to innerRelayCall. must be lower than the default 63/64
16. // actually, min(gasleft*63/64, gasleft-GAS_RESERVE) might be enough.
17. uint innerGasLimit = gasleft()*63/64-GAS_RESERVE;
18.
19. // Calls to the recipient are performed atomically inside an inner transaction which may revert in case of
20. // errors in the recipient. In either case (revert or regular execution) the return data encodes the
21. // RelayCallStatus value.

```








My motivation for the opcode is that it is very easy to plug it into the existing relay contracts without impacting most of the wider infrastructure.

Note; plenty of wallet providers are going this route including Gnosis, Argent, etc. Their relayers are refunded via the contract.

