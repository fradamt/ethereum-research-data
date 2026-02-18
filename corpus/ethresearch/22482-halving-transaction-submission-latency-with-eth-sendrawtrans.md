---
source: ethresearch
topic_id: 22482
title: Halving transaction submission latency with eth_sendRawTransactionSync
author: 14mp4rd
date: "2025-05-29"
category: UI/UX
tags: []
url: https://ethresear.ch/t/halving-transaction-submission-latency-with-eth-sendrawtransactionsync/22482
views: 882
likes: 19
posts_count: 10
---

# Halving transaction submission latency with eth_sendRawTransactionSync

*By [Sam Battenally](https://x.com/sam_battenally), [Hai Nguyen](https://x.com/hai_rise) and [Thanh Nguyen](https://x.com/nvthnh). Special thanks to [Lin Oshitani](https://x.com/linoscope) and Danilo R for useful feedbacks and comments.*

# Abstract

The traditionally asynchronous transaction submission and confirmation is no longer suitable for blockchains optimized for latency, such as RISE, MegaETH and Flashblocks chains (Unichain, Base). We introduce a simple `eth_sendRawTransactionSync` RPC to address key limitations in traditional Ethereum transaction workflows.

By aligning Web3 API behavior more closely with familiar Web2 request-response patterns, `eth_sendRawTransactionSync` simplifies developer experience, reduces latency, and enhances user responsiveness. This simple RPC is particularly impactful as blockchain architectures evolve toward lower block times and faster responsiveness, bridging the gap between decentralized and traditional application development paradigms.

# Motivation

The conventional transaction flow follows an asynchronous model where clients first broadcast signed transactions via `eth_sendRawTransaction`, then repeatedly poll nodes using `eth_getTransactionReceipt` until non-null receipts are returned.

[![Traditional Polling Mechanism](https://ethresear.ch/uploads/default/optimized/3X/9/6/9639f9b2438727ecab88e836b4a3b1fbf82ac146_2_690x325.jpeg)Traditional Polling Mechanism2048×967 130 KB](https://ethresear.ch/uploads/default/9639f9b2438727ecab88e836b4a3b1fbf82ac146)

In this model, the client submits the transaction and receives a transaction hash immediately, without waiting for the transaction to be included in a block. The client then relies on subsequent polling to determine the transaction’s status. This approach prevents the client from freezing or becoming unresponsive while waiting for the transaction to be mined.

```javascript
async function sendTransactionAndWaitForReceipt(web3, signedTx, pollingInterval = 200, timeoutMs = 30000) {
  try {
    // Send the signed transaction, returns the transaction hash immediately
    const txHash = await web3.eth.sendSignedTransaction(signedTx);
    console.log(`Transaction sent. Hash: ${txHash}`);

    const startTime = Date.now();
    let receipt = null;

    // Poll for the transaction receipt until it is available or timeout occurs
    while (receipt === null) {
      receipt = await web3.eth.getTransactionReceipt(txHash);

      if (receipt !== null) {
        console.log('Transaction receipt received:', receipt);
        return receipt;
      }

      if (Date.now() - startTime > CONFIG_SYNC_TIMEOUT) {
        throw new Error(`Timeout: Receipt not received within ${CONFIG_SYNC_TIMEOUT} ms`);
      }

      await new Promise(resolve => setTimeout(resolve, pollingInterval));
    }
  } catch (error) {
    console.error('Error sending transaction or fetching receipt:', error);
    throw error;
  }
}
```

***Listing**. An example code snippet for sending a transaction and querying its receipt.*

## Problems

- Latency Bottleneck. For chains optimized for latency, users expect near-instant feedback and seamless interactions. The inherent latency due to at least two distinct RPC calls can significant hinder the UX, especially for applications that require real-time feedbacks.
- Developer Experience Challenges. After submitting a transaction via eth_sendRawTransaction, developers must repeatedly call eth_getTransactionReceipt to check if the transaction has been included. This polling loop requires careful timing and error handling.

Developers often have to implement exponential backoff and retry logic to balance trade-offs (e.g, node response and latency).

**Node Performance**. Each `eth_getTransactionReceipt` call triggers lookups in the node’s database. Repeated or concurrent calls to this RPC at high request rates can strain node resources and degrade performance.

## Why Async?

- Long Blocktime. Ethereum’s average block time is around 12 seconds, meaning a transaction is only finalized after it is included in a proposed block. Since proposing and block propagation take time, a synchronous RPC call that waits for finality would block for many seconds, causing poor responsiveness and poor scalability.
- DX & UX Considerations. Early blockchain tooling and wallets were designed around asynchronous workflows to avoid freezing user interfaces and to handle the inherent latency gracefully. Polling receipts asynchronously allows better user feedbacks and error handling without blocking the application thread.

## Latency Factors

Let’s examine which factors contributing to the total latency.

1. Network Propagation. The time it takes for the request to reach the block producer across the P2P network.
2. Mempool Queue. Duration in the pending mempool before being picked into a block.
3. Block Creation. The time it takes for the receipt to be available after mempool queuing.
4. Polling Interval Delay. The delay from periodic receipt polling. This value is upper-bounded the case where the receipt becomes available just after a request.

For (1), we can hardly do anything except having our client to be physically close to the block producer. In general, rollups have less propagation time then the L1 in general since the users can send transactions directly to the sequencer (or its replicas). Therefore, in this post, we consider (1) as the baseline for the latency.

(2) mainly depends on the network utilization. High-performant networks are often under-utilized. That is, transactions are processed as soon as they land to the sequencer’s mempool. Therefore, this factor can literally be reduced to a negligible figure (< 1ms) in most of the cases.

(3) is mainly determined by the underlying blocktime. Ethereum or other EVM blockchains have long blocktime. However, with recent attempts to reduce chain responsiveness, we now have blockchains with a few ms (sub)blocktime (e.g, [RISE’s \mathtt{Shreds}](https://blog.riselabs.xyz/incremental-block-construction/), [MegaETH’s mini-blocks](https://docs.megaeth.com/mini-blocks), [Base’s Flashblocks](https://docs.base.org/chain/flashblocks/apps)), .

(4) is largely depends on the (2), and (3). At the time of submitting a transaction, a client does not know whether the transaction will be included instantly or not. If the polling interval is too short, it overloads the node with failed requests; if too long, it introduces unwanted latency for the client. If we can optimize (2) and (3) to negligible figures, we can certainly remove the need for polling.

# The Sync Transaction RPC

As many blockchains optimize for latency (reducing **(2) Mempool Queuing Time** and **(3) Block Creation** to as low as a few miniseconds) to enable realtime applications, realtime receipts are an important feature.

[![Sync vs Async Transaction Sending](https://ethresear.ch/uploads/default/optimized/3X/2/6/2633f4e5e9f00895055f9acd925f70e07f440d4a_2_690x302.jpeg)Sync vs Async Transaction Sending2048×899 110 KB](https://ethresear.ch/uploads/default/2633f4e5e9f00895055f9acd925f70e07f440d4a)

***Figure**. In a low-latency blockchain, transaction receipts are often available right after the transactions land to the sequencer’s mempool. Requiring an additional RPC call introduces unnecessary latency.*

We propose introducing a new synchronous RPC method `eth_sendRawTransactionSync` that combines `eth_sendRawTransaction` and `eth_getTransactionReceipt` into a single yet efficient RPC.

The code snippet below outlines a near-complete implementation in [reth](https://github.com/paradigmxyz/reth). As you can see, the code overhead is minimal. Holding HTTP ports open for extended periods can be heavy on resourcing so, `TIMEOUT_DURATION` should be set to some reasonable duration, say 2s.

```rust
async fn send_raw_transaction_sync(&self, tx: Bytes) -> RpcResult {
        const TIMEOUT_DURATION: Duration = Duration::from_secs(2);
        const POLL_INTERVAL: Duration = Duration::from_millis(1);

        let hash = self.inner.send_raw_transaction(tx).await?;

        // Continuously poll the receipt from the shred-funded pending block
        let start = Instant::now();
        while start.elapsed() < TIMEOUT_DURATION {
            if let Some(receipt) = self.pending_block.get_receipt(hash) {
                return Ok(receipt);
            }
            tokio::time::sleep(POLL_INTERVAL).await;
        }

        Err(ErrorObject::owned(
            -32002,
            format!(
                "The transaction was added to the mempool but wasn't processed in {TIMEOUT_DURATION:?}."
            ),
            Some(hash),
        ))
    }
```

***Listing**. An example snippet of the `eth_sendRawTransactionSync` logic.*

The `TIMEOUT_DURATION=2s` and `POLL_INTERVAL=1ms` are an implementation references and can be configured differently for different chains, depending on the execution performance.

## The Gains

- Latency. Network latency is reduced by half by removing the unnecessity of the two-RPC call paradigm. Transaction receipts could be available almost immediately after the transaction is sent.
- DX. The new RPC simplifies the entire process and removes the complexities associated with asynchronous programming and manual polling. Developers can write cleaner and more straightforward code, akin to making a standard synchronous API call.
- UX. The instantaneous transaction confirmation provided by the synchronous method in RISE translates directly into a much smoother and more responsive user experience for individuals interacting with decentralized applications built on the network.
- Node Performance. For node operators, implementing eth_sendRawTransactionSync is pretty easy, with just over 20 more lines of code. However, it has impactful effects on performance. By eliminating the need for clients to repeatedly query for transaction receipts using the eth_getTransactionReceipt method, the overall number of RPC calls directed at the nodes can be significantly reduced.

## A Quick Comparison

The following table summarizes the differences between the traditional async approach and the new sync approach to transaction submission.

|  | Async Method | Sync Method |
| --- | --- | --- |
| Latency | High, at least two round-trips | As low as network propagation time |
| UX | Slow responses, laggy UI | More responsive, near-instant feedbacks |
| DX | More complex (asynchronous logics, repeated polling) | Simple (synchronous calls, direct receipts) |
| Node Performance | Higher load, can strain the node | Potentially lower load |
| Network Efficiency | Multiple RPC calls per transaction increase network traffic and latency | Single RPC call per transaction reduces network load |
| Targeted Blockchains | Long blocktime, slow execution, fast consensus | Short blocktime, fast execution, fast consensus |

## Experimental Results

We implemented the `eth_sendRawTransactionSync` with a few lines of code and performed a few benchmarks to illustrate its improvement. In each benchmark, we track the **Total Time,** which indicates the duration between the time a transaction is submitted until its receipt is available at the client side. We configured our client to be in different locations with different RTT to the tested node.

### Baseline Numbers

For each location, we tracked the RPC response time of the benchmarked chains using the `eth_blockNumber` method as the baseline. The extracted numbers are the average and median of calling `eth_blockNumber` 50 times, and are recorded in the following table.

| Location | Average (ms) | Median (ms) |
| --- | --- | --- |
| Location 1 | 253 | 243 |
| Location 2 | 15 | 13 |
| Location 3 | 348 | 332 |
| Location 4 | 88 | 86 |

### Latency Report

We performed a side-by-side comparison between the sync and async methods. For each run, we tracked the **Total Time** when sending 200 sequential raw-transfer transactions. The following charts and table show the much-improved latency of the sync method compared to the async one (time is measured in miliseconds).

| Location | Baseline | Async Avg | Async Med | Sync Avg | Sync Med |
| --- | --- | --- | --- | --- | --- |
| Location 1 | 243 | 498 | 488 | 247 | 246 |
| Location 2 | 13 | 28 | 26 | 15 | 14 |
| Location 3 | 332 | 701 | 664 | 334 | 332 |
| Location 4 | 86 | 184 | 173 | 88 | 87 |

***Table**. Average and median time for async and sync methods on different locations.*

For the async method, the median **Total Time** numbers are approximately two times the RPC baseline time numbers for all locations. This is expected because a transaction typically requires two RPC calls. It suggests that the time for transaction processing and propagation is tiny compared to RPC time. We also observed frequent fluctuations during the test.

[![Time measured with the client in Location 1](https://ethresear.ch/uploads/default/optimized/3X/c/b/cb2d73197c2791f67542539dae9e4a763758b28c_2_690x287.jpeg)Time measured with the client in Location 11152×480 69.3 KB](https://ethresear.ch/uploads/default/cb2d73197c2791f67542539dae9e4a763758b28c)

[![Time measured with the client in Location 2](https://ethresear.ch/uploads/default/optimized/3X/c/7/c78105f8b4c0e510764d5e8b39e0095997abb46d_2_690x287.jpeg)Time measured with the client in Location 21152×480 73.8 KB](https://ethresear.ch/uploads/default/c78105f8b4c0e510764d5e8b39e0095997abb46d)

[![Time measured with the client in Location 3](https://ethresear.ch/uploads/default/optimized/3X/b/e/beaad1a30e41106dd3c913c92b3b6b90df6417bf_2_690x287.jpeg)Time measured with the client in Location 31152×480 75.1 KB](https://ethresear.ch/uploads/default/beaad1a30e41106dd3c913c92b3b6b90df6417bf)

[![Time measured with the client in Location 4](https://ethresear.ch/uploads/default/optimized/3X/c/f/cf0b553dd47e60b09a4f496986f9aaeff3314f97_2_690x287.jpeg)Time measured with the client in Location 41152×480 84.5 KB](https://ethresear.ch/uploads/default/cf0b553dd47e60b09a4f496986f9aaeff3314f97)

Regarding the sync method, the **Total Time** is reduced to closely assemble the time for a single RPC call. The sync method also has a more stable performance compared to the async one. As a result, the sync method allows us to save half the time needed to send a transaction and query its status.

# Conclusion

The `eth_sendRawTransactionSync` RPC represents a significant step forward in blockchain interaction design, predominately for chains optimized for low latency. The experiment results demonstrate clear advantages over conventional async methods, with transaction confirmation times reduced by approximately 50%.

In general, halving latency makes blockchain interactions feel more instantaneous and fluid, closer to the responsiveness users expect from Web2 applications. Removing the latency for receipt retrieval means that chains are left with optimizing other parts of RPC connections (routing, proxy, RPC handler, etc.) to fully deliver the real-time experience that current Web2 giants are providing.

## Replies

**antonydenyer** (2025-06-03):

Nothing is stopping `eth_sendRawTransaction` from blocking currently. The specification offers no indications (and limited flexibility) on what returning a transaction hash means. There is an implicit assumption for eventual consistency.

Currently, most wallets and dApps will continue to work if the transaction hash is not returned immediately in a timely manner. The timeout for a dApp to request something to be signed is huge because the user may be signing with a hardware wallet or something else.

In short, infrastructure providers can offer this today with the current specification. The limiting factor is dealing with concurrent open requests.

---

**SmoothBot** (2025-06-04):

Here we’re proposing to return the transaction receipt rather than the block hash. Modifying `eth_sendRawTransaction` to block and return the receipt would break integrations, wallets in particular.

---

**antonydenyer** (2025-06-04):

Ahh, the way I read it, most of the savings came from the removal of long polling and specifically the mismatch between poll frequency.

I guess in this scenario, you’d be saving the additional request to get the transaction receipt.

---

**thedarkjester** (2025-06-05):

Do you have any benchmarks on memory as well as CPU for the sync method vs. async at volume?

I am imagining a scenario where you have comparable amount of transactions (as the chain enjoys higher tx volume) being submitted and holding onto the signed tx data.

Could there be a spam or OOM attack?

---

**SmoothBot** (2025-06-05):

We honestly haven’t delved that deep yet, but it’s probably worth doing.

It’s live and in use on the RISE testnet without issues, but it needs more testing.

---

**thegaram33** (2025-06-06):

This would be a great addition to low-latency rollups.

Should this be an RIP? Or do you see any chance of L1 adopting this? (I guess no, since the Reth example only waits for 2 seconds).

---

**SmoothBot** (2025-06-07):

I’m no Ethereum governance expert, but given it’s optional, I think it makes sense as an EIP → ERC. In fact, there’s already an issue and PR open for this in [reth](https://github.com/paradigmxyz/reth/issues/16674)

---

**bomanaps** (2025-06-18):

Hello [@14mp4rd](/u/14mp4rd) and [@SmoothBot](/u/smoothbot)  I have some inputs/questions on this, we need to address this following points:

- How this behaves on Ethereum mainnet (12s block times)
- Impact during network congestion
- Behavior during MEV auctions and block building delays
- Interaction with private mempools.
It will be nice if we can create a compatibility matrix showing when this method is beneficial vs. detrimental across different network types.

Instead of aggressive polling, is it possible to use  existing infrastructure:

```auto
// Better approach using existing event systems
async fn send_raw_transaction_sync(&self, tx: Bytes) -> RpcResult {
    let hash = self.inner.send_raw_transaction(tx).await?;

    // Subscribe to block events instead of polling
    let mut block_stream = self.new_block_notifications();
    let timeout = tokio::time::timeout(TIMEOUT_DURATION, async {
        while let Some(_block) = block_stream.next().await {
            if let Some(receipt) = self.get_receipt(hash) {
                return Ok(receipt);
            }
        }
        Err("No receipt found")
    });

    timeout.await??
}
```

1. Adaptive Polling Strategy

```auto
// Smarter polling that adapts to network conditions
async fn adaptive_poll_receipt(&self, hash: TxHash) -> Option {
    let mut interval = Duration::from_millis(10); // Start reasonable
    let max_interval = Duration::from_millis(500);

    loop {
        if let Some(receipt) = self.get_receipt(hash) {
            return Some(receipt);
        }

        tokio::time::sleep(interval).await;
        interval = std::cmp::min(interval * 2, max_interval); // Exponential backoff
    }
}
```

I believe you’d get valuable feedback by bringing this up during the next Ethereum RPC Standard call, usually happens twice a month, and there should be one next monday. It could be a good opportunity to get broader input from client implementers.

---

**14mp4rd** (2025-06-19):

Thank you [@bomanaps](/u/bomanaps) for the comments.

![](https://ethresear.ch/user_avatar/ethresear.ch/bomanaps/48/16719_2.png) bomanaps:

> How this behaves on Ethereum mainnet (12s block times)

This RPC is optional for node implementation and only particularly suitable for blockchain with low latency.

![](https://ethresear.ch/user_avatar/ethresear.ch/bomanaps/48/16719_2.png) bomanaps:

> Impact during network congestion

During network congestion, the RPC will likely to be timed-out and callers must fall back to regular receipt polling technique.

![](https://ethresear.ch/user_avatar/ethresear.ch/bomanaps/48/16719_2.png) bomanaps:

> Behavior during MEV auctions and block building delays
> Interaction with private mempools.

To be honest, we haven’t thought of these but we aim at blockchains whose blocktime is around hundreds of miliseconds.

![](https://ethresear.ch/user_avatar/ethresear.ch/bomanaps/48/16719_2.png) bomanaps:

> Instead of aggressive polling, is it possible to use existing infrastructure:

Detailed implementations vary depending on client implementers. We do not specify a particular implementation for all clients, the code above mainly serves as an illustration of how simple the RPC is.

![](https://ethresear.ch/user_avatar/ethresear.ch/bomanaps/48/16719_2.png) bomanaps:

> I believe you’d get valuable feedback by bringing this up during the next Ethereum RPC Standard call, usually happens twice a month, and there should be one next monday. It could be a good opportunity to get broader input from client implementers.

Thank you for the information.

