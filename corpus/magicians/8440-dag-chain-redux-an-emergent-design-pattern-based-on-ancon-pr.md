---
source: magicians
topic_id: 8440
title: DAG Chain Redux - An emergent design pattern based on Ancon Protocol/DAGs, EIP-3668 and EIP-4337 Account Abstraction
author: molekilla
date: "2022-02-26"
category: Uncategorized
tags: [account-abstraction, eip-4337, eip-3668]
url: https://ethereum-magicians.org/t/dag-chain-redux-an-emergent-design-pattern-based-on-ancon-protocol-dags-eip-3668-and-eip-4337-account-abstraction/8440
views: 1102
likes: 0
posts_count: 1
---

# DAG Chain Redux - An emergent design pattern based on Ancon Protocol/DAGs, EIP-3668 and EIP-4337 Account Abstraction

# DAG Chain Redux

An emergent design pattern based on Ancon Protocol, EIP-3668 and EIP-4337 Account Abstraction

![DAG REDUX](https://user-images.githubusercontent.com/1248071/155858908-13282b5a-6612-4783-b9f3-9c4194f01ef3.svg)

## Abstract

There are already open source indexing tools like The Graph and TrueBlocks, which takes enough care of post processing of onchain events.

[Ancon Protocol](https://github.com/anconprotocol) does support indexing features, but one feature we recently cut off was mutable DAG blocks using PUT, because we required full verifiable signatures. In reimagining the problem from another point of view, if we take onchain events as the ultimate proof of truth, we can mutate DAGs similar to the [previously implemented Rust WASM Contracts](https://github.com/anconprotocol/contracts), but instead, taking cues from [EIP 4337 Account Abstraction](https://github.com/ethereum/EIPs/blob/3fd65b1a782912bfc18cb975c62c55f733c7c96e/EIPS/eip-4337.md), **a relayer gets paid to execute a Javascript smart contract** , these contracts compiled to JEXL or QuickJS WASM Containers.

The result is a signed output, verifiable both offchain and onchain (if used with Ancon Protocol offchain signatures or EIP-3668).

## Use Case

In our flagship NFT Marketplace, the redux flow without DAG Chain Redux looks like:

- POST DAG block to Ancon
- Submit proof to EVM if required
- Wait for transaction
- Listen for Events and sign again mutated block as new POST DAG block

The last action is outside the transaction, which makes it a bad design and very common one. Ideally, listeners or subscribers await web sockets or other messaging mechanism for updates (DISPATCHES) to be made to a DAG Block.

Marketplace needs to keep updated an users NFTs and also the entire most current NFT snapshot. With DAG Chain redux, you can create relayers or INDEXERS in Javascript or inside a WASM engine compatible with QuickJS ([Redirecting...](https://wasmedge.org/book/en/dev/js/quickstart.html)) and execute REDUCERS.

## Summary

A DAG Chain redux is then made of:

- Smart contracts build with security VM isolation using QuickJS and executed in either Javascript or WASM
- Indexers listening for events to dispatch actions
- Which represent a specific reducer, meaning, it takes the current DAG block and reduces it to other data transformation
- Execution by an existing relayer takes care of payment fees, otherwise, an indexer must charge the execution fee directly.
- The state is stored in an Ancon DAG Node, which internal Merkle Tree makes it ICS23 Proof ready, or using an EIP-3668 request response, be available for secure offchain requests.
- Cycles repeats once again

## Alternatives

- Trueblocks
- The Graph
- Do your indexing and merge

## Implementation using JEXL

```typescript
const jexl = require('jexl');

const jexlSmartContract = {
  Transfer: [
    {
      name: 'concatTransactionHash',
   // rule condition
      condition: `(returnValues.from == '0x0000000000000000000000000000000000000000') && (returnValues.to != null)`,
//   rule expression
      expression: `assign(dag, append('txHash', tx.transactionHash))`,
//   fetch DAG block condition
      blockFetchCondition: 'returnValues.to != null',
//   fetch DAG block topic address (where topic is similar to Swarm Feeds)
      blockFetchAddress: 'returnValues.to',
      topicName: '@topic',
    },
]

const transferExample = {
  address: '0xA7D6e6F21D6D5906eEFC2c30601CEC178e2e6743',
  blockNumber: 17190973,
  transactionHash:
    '0xbd7a5fc437f8e58d59a2d56b19d7c174ea1189abe5d09a68afda8b91c2aa1fd7',
  transactionIndex: 0,
  blockHash:
    '0x4a01147f5e3dba3867d3c58dd115060806e6f35a9e39dc1a70fdd30ad58a0fa8',
  logIndex: 4,
  removed: false,
  id: 'log_1192ac7e',
  returnValues: {
    '0': '0x0000000000000000000000000000000000000000',
    '1': '0x32A21c1bB6E7C20F547e930b53dAC57f42cd25F6',
    from: '0x0000000000000000000000000000000000000000',
    to: '0x32A21c1bB6E7C20F547e930b53dAC57f42cd25F6',
  },
  event: 'Transfer',
  signature:
    '0x0a59a585b9550719952b099b96c48342a827bee7469998fdbdfb68477e412931',
  raw: {
    data: '0x0000000000000000000000002f4167f834892fb7f2691883867aec12fc4863710000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000005dc000000000000000000000000000000000000000000000000000000000000002461663634346661352d633161662d343631622d626430352d39383634636165616565663800000000000000000000000000000000000000000000000000000000',
    topics: [
      '0x0a59a585b9550719952b099b96c48342a827bee7469998fdbdfb68477e412931',
    ],
  },
};

const dagAnconExample = {
  commitHash: 'dvI2mjNUQdaiutM/mDtaJjjGYyzsCQyKMkncEV20RVY=',
  contentHash: {
    '/': 'baguqeeracxd7idu7jjxvboym6lm22tlcjssj5xvfreydmntkheipqcbxm24q',
  },
  digest: '0xa33469f7f4eb0213d1f3c897e6d2fe3911ea91511f84ed040a4b0dc68907599b',
  height: 269,
  issuer: '0x32A21c1bB6E7C20F547e930b53dAC57f42cd25F6',
  key: 'YW5jb25wcm90b2NvbC91c2Vycy9kaWQ6ZXRocjpibmJ0OjB4MzJBMjFjMWJCNkU3QzIwRjU0N2U5MzBiNTNkQUM1N2Y0MmNkMjVGNi9iYWd1cWVlcmFjeGQ3aWR1N2pqeHZib3ltNmxtMjJ0bGNqc3NqNXh2ZnJleWRtbnRraGVpcHFjYnhtMjRx',
  lastBlockHash: {
    '/': 'baguqeeranvsy7kickuqzmugxwe3vmxsmz5mdqlst3vvdmv76hq3wumvlruqa',
  },
  network: 'anconprotocol',
  rootKey:
    'YW5jb25wcm90b2NvbC91c2Vycy9kaWQ6ZXRocjpibmJ0OjB4MzJBMjFjMWJCNkU3QzIwRjU0N2U5MzBiNTNkQUM1N2Y0MmNkMjVGNg==',
  signature:
    '0xe181951f189b9f553b946108a96a65be606ec5d730d2fc042f157d0369dd508377d19fa92e0ee5431a8c94d422450535d03057243bb6cb13e469f0c49e27a08b1b',
  timestamp: 1646065832,
  content: {
    blockchainMakeOrderTxHash: '',
    blockchainTokenId: '8',
    blockchainTxHash:
      '0x5965b148a04f3cf27964a0303b086582850a400542298c521a17735e248b1354',
    creator: '0x32A21c1bB6E7C20F547e930b53dAC57f42cd25F6',
    currentOrderHash: '',
    currentOrderTimestamp: '',
    description: 'commetn feb 25',
    fileExtension: 'gif',
    image: 'baguqeerad36yce4lghf7amd7i3e3k5biig54np6hyd6l3o4xztpbqnufclxa',
    name: 'demo 3 feb 25',
    owner: '0x32A21c1bB6E7C20F547e930b53dAC57f42cd25F6',
    price: '',
    sources: [
      'https://tensta.did.pa/v0/file/baguqeerad36yce4lghf7amd7i3e3k5biig54np6hyd6l3o4xztpbqnufclxa/',
    ],
    tags: 'Videogames',
    uuid: 'ebdaf05a-635d-49df-aee7-c690e9adbc9d',
  },
};

const onEvent = async () => {
  // helper functions
  jexl.addFunction('assign', assign);
  jexl.addFunction('append', append);

  // Lookup by event
  const rule = jexlSmartContract;
  const ruleset = rule[transferExample.event];

  // Lookup by condition
  let expectedRules = [];
  expectedRules = await ruleset.filter(async (r) => {
    return await jexl.eval(r.condition, transferExample);
  });

  // Lookup by DAG block condition, note this could be a single liner
  if (expectedRules.length > 0) {
    expectedRules = await expectedRules.filter(async (r) => {
      return (
        (await jexl.eval(r.blockFetchCondition, transferExample)) ===
        true
      );
    });
    expectedRules.map(async (r) => {
      const queryAddress = await jexl.eval(
        r.blockFetchAddress, transferExample,
      );

      // TODO: Fetch topic + queryAddress eg Waku, Swarm Bee or Ancon protocol
      const dagContent = dagExample.content;
      const context = { dag: dagContent, tx: transferExample };
      const result = await jexl.eval(r.expression, context);

      // TODO: Mutate topic + Sign
      return { result: result, rule: r, signedBlock: {} };
    });
  }
};
```

## Authors

Rogelio Morrell, Kendall Kant, for Industrias de Firmas Electronicas SA , 2022.
