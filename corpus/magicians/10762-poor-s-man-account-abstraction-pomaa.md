---
source: magicians
topic_id: 10762
title: Poor’s Man Account Abstraction (POMAA)
author: sergio_lerner
date: "2022-09-09"
category: EIPs > EIPs core
tags: [account-abstraction]
url: https://ethereum-magicians.org/t/poor-s-man-account-abstraction-pomaa/10762
views: 1323
likes: 5
posts_count: 7
---

# Poor’s Man Account Abstraction (POMAA)

This is a proposal to provide Account Abstraction (AA) to the Ethereum platform without a hard-fork, and without adding a new role (i.e. bundlers). It requires a low amount of changes to the mempool code and miner’s code.

We’ will describe 4 methods, the last one being the most efficient in terms of consumed gas.

Let G be the base elliptic curve point uses by ECDSA. Let T be a transaction with T.nonce==0 (other nonces are not accepted).

Let T.r be the r value of the ECDSA signature of the transaction.

An account F(r,t) is defined as the one related to private key privKey(F(r,t))=H(r|t), where H() is a crypto hash function. Therefore pubKey(F(r,t))=H(r|t)*G. This is a one-time address, and a one-time private key, but the private key is forwarded inside the signature itself. The value t is defined as H(T) (the hash of a transaction for signing).

The procedure to sign the transaction T is as follows:

1. The signature value r is chosen.
2. The value t=H(T) is computed
3. The EOA F(r,t) is derived from F, r and t.
4. The signature value s is computed for the transaction T signed by the EOA F(r,t).

This enables the creation of uniformly random distributed EOAs whose private keys are known by the receiver of the transaction, and whose senders depend both on r and on the transaction itself. We call these transactions public.

To detect if a transaction X is a public transaction, the following procedure is executed:

- Perform a public key recovery on X to get pubKey(X).
- If pubKey(x) == H(T.r | H(T))*G, then X is public.

**MemPool**

Let T be a public transaction (originating from F(T.r,t)) with T.nonce==0.

Let U = (T.gasPrice*T.gasLimit+T.value) .

Each node performs the following steps:

- setBalance(F(r,t),U)
- Execute T
- Let Z =U+T.value+actualGasConsumed(T)*T.gasPrice.
- Check that getBalance(F(r,t)) >= Z.

If this is valid, the transaction is broadcast.

**Typical payload of T**

The transaction T must contain a payload(T) that represents a call to the user’s smart wallet.

The smart wallet should:

- Verify that the payload is signed.
- Check and increment a nonce given.
- Execute the transaction payload
- pay back to msg.sender the amount Z.

This adds certain overhead. Assuming the signature scheme used by the smart wallet is also ECDSA, the additional cost is not less than 3000+5000=8000.

**Method 1: Miner**

The miner executes the transaction T by creating a sandwich: in the first transaction (Pre), it provides T with the funds to execute. The second transaction is T. In the third transaction (Post), the miner transfers the full balance of T to its own account.

Construction of a block template by the miner using method 1:

1. Transaction Pre: transfer(Miner,F(T.r,t), U)
2. Execute T
3. Transaction Post: transfer(Miner,getBalance(F(T.r,t))),U)

The cost of executing T is increased by 42000 gas (pre and post transactions) plus the overhead of the smart wallet (8000) is 50000.

**Method 2**

The gas consumption can be optimized if the transaction T at the last step calls a fixed contract payBack.reimburse(). Then the transactions required are only 2. Here is our method 2:

1. Transaction Pre:

- Call payBack.deposit(F(T.r,t), minerAccount) from the miner’s account, transferring the value U.
- payBack transfers U to account F(T.r,t).

1. Execute T

- Calls payBack.reimburse() transferring the value U
- CallBack transfers U to the registered minerAccount.

The gas overhead is approximately 21000+9700+9700+9700+8000 = 58100. It seems that we have made things worse!

**Method 3**

If the miner has enough funds to pay in advance all fees he plans to collect, we can perform a single deposit in payBack, and let payBack perform multiple calls.

Now the miner performs the following packing of transactions. Here is our method 3:

1. Transaction Pre:

- Call payBack.deposit(F(T1.r,t1), U1, F(T2.r,t2), U2, …. , F(Tn.r,tn), Un, minerAccount) from the miner’s account, transferring the value U= sum(U1, U2, … ,Un).
- payBack transfers U(i) to account F(T(i).r,t(i)).

1. Execute T(i) for i=1..n

- Calls payBack.reimburse() transferring the value U(i)

1. Transaction Post:

- Call payBack.collectReimbursements()
- CallBack transfers U to the registered minerAccount.

Now most of the additional cost is amortized over the n transaction. The extra constant cost per transaction is approximately 17700.

**Method 4**

What is more interesting, if the contract called by T is known not to check the msg.sender and no contract checks the msg.origin, then the miner can unbundle all the payloads and move them to his own account.

While we don’t need to standardize the signature scheme nor how the nonce is handled not how it is transferred in payload(T), we do define the 3 minimum elements in the payload to allow batching: payload(T).target and payload(T).data.

Therefore a single transaction B needs to be added to the block. The transaction B originates in an EOA with at least U coins. We show our final method 4:

1. Single transaction “bundle” B:

- Call Payload(Ti).target with data payload(Ti).data, gasCost Ti.gasCost and gasLimit Ti.gasLimit for i=1..n
- Each transaction Ti, in its final step, calls: payBack.reimburse() transferring the value U(i).
- Call payBack.collectReimbursements(). This method pays all the balance to msg.sender.

Now not only is there no overhead, but we’ve made the transactions T cheaper. Each transaction T(i) cost 8000 plus the cost of smart wallet signature, nonce, and destination fields. At 16 gas per byte, the total cost results in 9408.

Ethereum has become cheaper.

**Security**

This AA scheme is not subject to denial of service attacks because the source account F(r,t) is chosen based both on r and on the transaction payload itself.  To avoid conflicting public transaction in the mempool, the client code must detect if two transactions call the same smart wallet and keep only one of them. If two transactions compete, the client will keep only the one with higher gas price.

A second type of attack is the inclusion of another transaction that calls the smart wallet, and either changes the user’s nonce or in some way makes the transaction T that exists in the mempool, invalid. Therefore the user never pays the price for the network to forward T.

To avoid this attack, without prohibiting other contracts to call the smart wallet, a set of standard templates for signature verification schemes (from Schnorr to multisigs) are defined as library authentication contract proxies (ACP). The authentication contract, is, as the name indicates, a proxy: it receives the payload, the real user’s smart wallet address, the signature and the nonce and then its verifies that the transaction is correctly signed and that the nonce is the correct one. Afterward the ACP forwards all data to the real user’s smart wallet to perform any other call on behalf of the user.

Nodes in the network will only forward public transactions whose destination is one of the predefined addresses of ACPs. The ACPs are designed so they only change the nonce or reduce the balance by the method used by AA. Therefore the network clients can invalidate public transactions in the mempool only if another public transaction is received that refers to the same user’s wallet address in the payload and pays a higher gas price.

All invalidations are explicit and simple to detect.

Anyone can create a new ACP, deploy it on the blockchain and publish its source code as an EIP and if the community considers it secure (only condition is to isolate nonce and balance from external calls) then its address is added to the network clients. There is no need to hard-fork.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9b9f1d46c4b78dd6de67b2bce536014465a99322_2_345x191.png)image1052×584 16 KB](https://ethereum-magicians.org/uploads/default/9b9f1d46c4b78dd6de67b2bce536014465a99322)

A drawback of POMAA is that hardware wallets need to be updated to support the creation of one-time derived addresses on-the-fly.

## Replies

**koeppelmann** (2022-09-09):

Thanks for this proposal.

One comment:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sergio_lerner/48/1759_2.png) sergio_lerner:

> Nodes in the network will only forward public transactions whose destination is one of the predefined addresses of ACPs. The ACPs are designed so they only change the nonce or reduce the balance by the method used by AA. Therefore the network clients can invalidate public transactions in the mempool only if another public transaction is received that refers to the same user’s wallet address in the payload and pays a higher gas price.
> All invalidations are explicit and simple to detect.

Those requirements unfortunately don’t hold true for the currently most popular smart contract wallet: Gnosis Safe. Most Safes are deployed as proxies and they allow to have modules. A module can introduce arbitrary access rights and can trigger arbitrary changes.

---

**sergio_lerner** (2022-09-09):

True. The only way to make the proposal compatible with Gnosis Safe is to standarize the wallet code via EIP, and the same for each module that participates in authentication. Painful.

---

**koeppelmann** (2022-09-09):

Though I am not a client developer but I think as long as it costs “on-chain gas” to invalidate a previous valid (meta)transaction it should be *ok* for clients that they rarely learn during block building that a transaction became “invalid” and they need to kick it out.

---

**sergio_lerner** (2022-09-09):

But there is some asymmetry, because the on-chain cost can be 21k gas, while the mempool tx has a 2M gas limit and a 128 Kbytes a data payload that the network had to forward.

---

**sergio_lerner** (2022-09-09):

I think the only really novel thing here is encapsulating the “useroperation” in a standard-looking tx and re-using the standard mempool. The rest is more or less a mixture of ideas that have been previously discussed ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**dcposch** (2023-06-26):

I think this thread would benefit from a concise comparison to 4337. 4337 has significant momentum and infrastructure at this point, so any other AA needs a great 1-line justification for why/where it’s significantly better.

