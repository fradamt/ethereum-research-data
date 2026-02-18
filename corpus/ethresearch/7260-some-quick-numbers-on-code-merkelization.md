---
source: ethresearch
topic_id: 7260
title: Some quick numbers on code merkelization
author: lithp
date: "2020-04-11"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/some-quick-numbers-on-code-merkelization/7260
views: 3622
likes: 5
posts_count: 4
---

# Some quick numbers on code merkelization

Some key numbers in determining the viability of stateless ethereum are (1) how big the witnesses will be, and (2) what witness size the network can support. (1) must be less than (2). To that end there are a couple different proposals for making witnesses as small as possible, one of them is code merkelization. It would take a while to get perfect numbers on the impact of merkelization so I tried to come up with a quick estimation of the benefits.

I wrote some logic to record which bytes of contract bytecode are accessed during transaction execution, and then ran it over a sampling of recent blocks. I scanned every 50th block, starting with [9375962](https://etherscan.io/block/93759622) and ending with [9775962](https://etherscan.io/block/9775962) (a total of 8001 blocks).

This post is kind of a grab-bag, I don’t have any conclusions but wanted to put this data somewhere public so we can refer to it later. Here are some results which seemed useful:

### Code merkelization could have a large impact:

We all assumed this but it’s nice to put some numbers behind that assumption:

[![bytecode_histogram](https://ethresear.ch/uploads/default/original/2X/a/aca68efe72d05560415920dc9219db4fa15535c4.png)bytecode_histogram580×480 15.5 KB](https://ethresear.ch/uploads/default/aca68efe72d05560415920dc9219db4fa15535c4)

The above histogram bins blocks by the total size of all the contract bytecodes which were executed in that block. The largest block by this metric is [9697612](https://etherscan.io/block/9697612), which executes 1.7MB of contract bytecode. Code merkelization would likely have a massive impact here, as that block only ever executes 220044 (12%) of those bytes. 220044 is near the high end:

[![accessed_bytecode_histogram](https://ethresear.ch/uploads/default/original/2X/d/dc52033cd367e13f83b292e1ecbd1e75ff078157.png)accessed_bytecode_histogram581×480 15.3 KB](https://ethresear.ch/uploads/default/dc52033cd367e13f83b292e1ecbd1e75ff078157)

This histogram bins blocks by the number of contract bytes which are actually accessed during execution. I should note that actually witnessing these bytes requires proving them! These numbers provide an upper bound on the potential savings, no [accumulator](https://ethresear.ch/t/using-polynomial-commitments-to-replace-state-roots/7095) will ever be able to reduce the code witness size of this block by more than 88%.

What does the average block look like?

[![block_savings_histogram](https://ethresear.ch/uploads/default/original/2X/b/b49d327e5421b3146a4c2bf8545bd71bbcd35e0f.png)block_savings_histogram580×480 15 KB](https://ethresear.ch/uploads/default/b49d327e5421b3146a4c2bf8545bd71bbcd35e0f)

There are a few blocks which use a high proportion of the contract bytes but those are tiny blocks which don’t touch many blocks to begin with. Most blocks execute ~15% of the bytes of the contracts they execute.

This is great news! No block that I scanned accessed more than 251403 bytes. That’s not insignificant, but it almost certainly fits into whatever our witness size budget turns out to be. So, we should be able to witness contract bytecode without massively increasing gas costs for existing transactions.

### For the average transaction, gas costs will not greatly increase:

Vitalik [has proposed](https://ethereum-magicians.org/t/protocol-changes-to-bound-witness-size/3885) charging transactions 3 gas per witnessed byte. This would lead to a theoretical maximum block size of under 3.2MB (assuming a 10M block gas limit) which seems too large but let’s stick with that number for now. If transactions were charged 3 gas for each byte of bytecode which they accessed, here’s how gas prices would increase across the set of transactions this scan found:

[![txn_gas_cost_histogram](https://ethresear.ch/uploads/default/original/2X/2/2a4fdfa5859df77e5e530635a8e8b71fceddd09b.png)txn_gas_cost_histogram597×480 14.9 KB](https://ethresear.ch/uploads/default/2a4fdfa5859df77e5e530635a8e8b71fceddd09b)

For most transactions, the impact is minimal. Some transactions would see their gas cost increase by ~30%. Of course, this is an underestimate. For one, I’m not counting the witness bytes required to prove the accessed contract bytes. For another, state accesses also must be witnessed.

### We need to special-case extcodesize

Again, I think everyone already assumed this but it’s nice to be able to back those assumptions up with data. The naive implementation of `extcodesize` just counts the number of bytes in the target contract, and would require witnessing the entire bytecode.

I recorded most calls to `extcodesize` [1] to estimate how much of an impact this would have have on witness size. For block 9697612 this would witness 1.4MB of data, just to prove `extcodesize` calls! 52 of the blocks I scanned (<1%) would use over 1MB of data for `extcodesize`, and 1012 of them (~13%) would use 500KB of data.

`extcodesize` appears to be widely used. Unless we want to break a large proportion of the current transactions we’ll need to provide some way of succinctly proving the codesize [when we rebuild the account trie](https://ethresear.ch/t/overlay-method-for-hex-bin-tree-conversion/7104). This could be an explicit field in the account structure. If we merkelize using fixed-size chunks a proof of the right-most chunk would be enough.

[1] I’m only recording countracts which had extcodesize calls on them, and which were also executed. Contracts which had `extcodesize` called on them but which never executed any bytes are not counted, so the true numbers are even higher than reported here.

### Some additional complications:

- Not all JUMPDEST bytes are valid jumpdests, some of them are part of PUSHDATA and cannot be jumped to. At the beginning of execution geth scans through the entire contract and computes the set of valid JUMPDESTs. Trinity does something which touches fewer bytes, but in order to merkelize bytecode both of them will have to come up with a new strategy. I forget who told me this strategy, I think it was Piper? But if we merkelize bytecode by chunking it up, each chunk could start with an extra byte, the offset of the first valid JUMPDEST in that chunk.
- I’m not counting the initcode of CREATE calls, since the only ways to get an executable initcode are already witnessed.
- In these sums I’m including bytes from contracts which were created in the same block. This makes the numbers larger than they should be, those contract bytes won’t need to be witnessed, but I think correctly handling this edge case would take more work to fix than it improves the results.

## Replies

**sinamahmoodi** (2020-04-14):

The proof overhead was in the order of 20-30% in my [experiment](https://github.com/ewasm/biturbo/pull/64) (witness aggregated the whole block). There the code was divided by [basic blocks](https://medium.com/ewasm/evm-bytecode-merklization-2a8366ab0c90) (instead of fixed-sized) with a chunk min size of 128 bytes. On the other hand the proofs were assuming a hexary trie, so using a binary trie and chunk min size of 32 bytes should yield similar numbers. In the chart the green bars are the touched code chunks and the purple bars the accompanying hashes. `extcodesize` was not counted in, but `extcodehash` was (after Martin pointed it out). But generally good to see that the numbers roughly agree.

[![code-saving-chart](https://ethresear.ch/uploads/default/optimized/2X/4/40be089d88506ff02ad984bdbf850c7252b345e1_2_690x324.png)code-saving-chart1139×536 26.4 KB](https://ethresear.ch/uploads/default/40be089d88506ff02ad984bdbf850c7252b345e1)

Can you please expand on the method you used for the gas estimations?

---

**sinamahmoodi** (2020-06-02):

There exist chunking strategies which take the control flow of a contract into account and are hypothesized to produce leaner proofs but are at the same time more complex. Before we have actual data from these approaches, we can estimate the saving that a hypothetically optimal chunking strategy would yield compared to e.g. the jumpdest-based approach.

To estimate this we can measure chunk utilization, which tells us how much code sent in the chunks were actually necessary for executing a given block. E.g. if for a tx we send one chunk of contract A, and only the first half of the chunk is needed (say there’s a STOP in the middle), then chunk utilization is 50%, the other half is useless code that has been transmitted only due to the overhead of the chunker.

[![Chunk utilization in the basic block merklization approach with a minimum chunk size of 32 bytes](https://ethresear.ch/uploads/default/optimized/2X/7/7e5b982533e63b5479339b3c47dde8464a9729c3_2_690x338.png)Chunk utilization in the basic block merklization approach with a minimum chunk size of 32 bytes1459×716 37.7 KB](https://ethresear.ch/uploads/default/7e5b982533e63b5479339b3c47dde8464a9729c3)

Above you can see average chunk utilization for 50 mainnet blocks is roughly 70% when using the jumpdest-based approach with a minimum chunk size of 32 bytes. That means the optimal chunking strategy could improve the code transmitted by 30%, but that itself is only part of the proof (which includes hashes, keys and encoding overhead). Assuming binary tries cut the hash part by 3x, there might be ~11-15% improvement in total proof size compared to the jumpdest-based approach.

---

**SergioDemianLerner** (2020-06-04):

I have nothing interesting to add to your research.

I just want to mention that RSK has the code size embedded in trie nodes so that EXTCODESIZE does not need to scan the full code. Also RSK uses a binary trie called Unitrie. Works well.

