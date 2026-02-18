---
source: magicians
topic_id: 13068
title: Hybrid Mode State Expiry
author: asyukii
date: "2023-02-27"
category: EIPs
tags: [state-expiry]
url: https://ethereum-magicians.org/t/hybrid-mode-state-expiry/13068
views: 993
likes: 7
posts_count: 3
---

# Hybrid Mode State Expiry

[Refer to the original proposal for more illustrations](https://forum.bnbchain.org/t/bep-idea-state-expiry-on-bnb-chain/646/5)

**To everyone in the forum**

Storage explosion has always been one of the key issues that we are trying to tackle. In this proposal, we hope to implement state expiry for BNB Chain to solve the problem. We hope that we can get more insights from the community and see how we can move things forward together.

---

# BEP-206: Hybrid Mode State Expiry

## 1.Summary

This BEP proposes a practical solution to address the problem of increasing world state storage on the BNB Smart Chain, by removing expired storage state.

## 2.Motivation

Storage presents a significant challenge for many blockchains, as new blocks are continually generated, and transactions within these blocks could invoke smart contracts that also add more states to the blockchain.

A large storage size can cause several side effects on the chain, such as higher hardware requirements, increased network resources required for downloading and performing p2p sync, and performance degradation due to MPT write amplification.

Due to the high volume of traffic, the storage size on BSC grows very rapidly. As of the end of 2022, a pruned BSC full node snapshot file is approximately 1.6TB in size, compared to approximately 1TB just one year ago.

The 1.6TB storage consists mainly of two parts:

- Block Data (~2/3), which includes the block header, block body, and receipt;
- World State (~1/3), which includes the account state and Key/Value (KV) storage state.
The Ethereum community proposed EIP-4444 to address the first part, which is to prune old block data. However, EIP-4444 does not address the second part, which is more challenging.
There have been many discussions on how to implement state expiry, with one proposed solution involving the removal of EOA accounts, extension of the address space, and the use of Verkle Trees to reduce the witness size. However, implementing such a solution would be a significant undertaking that could have a substantial impact on the ecosystem, and may not be feasible in the short term. As BSC continues to face high traffic volumes, it is essential to develop a short-term solution for state expiry that can be implemented quickly, while still retaining the ability to upgrade to a long-term solution once it becomes available.

## 3.Specification

### 3.1.Hierarchy View

#### a.Current MPT Tree

The current MPT(Merkle Patricia Tries) tree on BSC is a single tree composed of two trie trees, namely the L1 AccountTrie and L2 StorageTrie. The L1 account trie tree stores the account state, which includes the Nonce, Balance, StorageRoot, and Codehash for both EOA and Contract accounts. Each contract account also has its own L2 storage trie tree, which stores its KeyValue (KV) state that is updated by the corresponding smart contract. The world state is accessed through this single-layered MPT tree.

> Please go to the original BEP to view the picture.

#### b.Hybrid MPT Tree

This proposal introduces the concept of an “epoch,” which refers to a period of time with a unit of blocks. The details of the epoch will be explained further later on.

With the epoch concept in mind, this proposal suggests the introduction of a hybrid MPT tree mode, where the L1 account trie tree will remain unchanged, while the L2 storage trie will have a new Shadow Tree which will keep the access record for the MPT tree. In other words, the hybrid MPT tree consists of a single account trie and an epoch-based storage trie, as illustrated in the following diagram.

> Please go to the original BEP to view the picture.

The storage trie in Epoch 0 will stay unchanged, but since Epoch 1 the storage trie will have a new trie node type as its root: RootNode. It consists of 3 elements: EpochIndex, MPT Root and Shadow Root.

EpochIndex: the latest epoch index in which the trie is accessed

MPT Root: same as the current MPT Root, it will pointer to the root trie node.

Shadow Root: the root hash of the shadow tree, which is used to record the access history of the storage trie

> Please go to the original BEP to view the picture.

The RootNode and ShadowTree are very important in this proposal and the details will be revealed later.

### 3.2.The Components

> Please go to the original BEP to view the picture.

#### a.Data Availability

The expired state will be kept by the DA for witness service, allowing users to revive their expired state. The details of data availability will not be covered in this proposal but can be provided by third-party projects such as the BNB Greenfield project.

#### b.New Transaction Type

A new transaction type will be added, which would contain the witness. The EVM will be upgraded to support this new transaction type, along with an appropriate gas metering policy.

There will be another BEP to explain the details.

#### c.Epoch

The epoch period is a key parameter for this proposal, and by default, it could be set to 2/3 years for the BSC mainnet. Given a BlockInterval of 3 seconds, the EpochPeriod would be calculated as follows: EpochPeriod = 365 * (2/3) * 24 * 60 * 60 / 3 = 7,008,000.

#### d. ShadowTree & ShadowNode

Before introducing the new concepts of ShadowTree and ShadowNode, it is important to have a clear understanding of the layout of the classical MPT, which is depicted in the diagram below:

> Please go to the original BEP to view the picture.

There are three types of nodes in the MPT tree: Branch Node, Extension Node and Leaf Node.

As the name suggests, ShadowTree is the shadow version of the MPT tree and is also comprised of three types of ShadowNode:

- ShadowBranchNode
- ShadowExtensionNode
- ShadowLeafNode
The Layout of the ShadowTree can be depicted as the following diagram:

> Please go to the original BEP to view the picture.

Unlike the MPT tree, Shadow Tree is not a patricia tree, it can not be iterated by the Shadow Root. It is a shadow mapping to the MPT tree and can be accessed indirectly by the MPT tree.

The key to of the shadow node can be: ShadowKey =${TrieNodeHash}${suffix}, it is a combination of the corresponding trie node hash and a suffix. The client may need to keep the shadow node update record to support archive node or block rewind.

##### Shadow Leaf Node

The ShadowLeafNode is always nil, since it is the end of the path, no need to keep the metadata of its child.

```auto
type ShadowLeafNode struct {}
```

##### Shadow Extension Node

It has a single element: ShadowHash, which is calculated based on shadow information of its child.

> Please go to the original BEP to view the picture.

```auto
type ShadowExtensionNode struct {
  ShadowHash *common.Hash
}

func (node *ExtensionNode) ShadowNode() ShadowExtensionNode {
  // to calculate the ShadowHash of a ShadowExtensionNode
  var shadowHash *common.Hash
  child := node.child
  if child.isLeafNode() {
    shadowHash = nil
  } else if child.isBranchNode() {
    branch := child.ShadowBranchNode
    shadowHash := Hash(branch.ShadowHash, branch.EpochMap)
  } else {
    // unreachable,
  }
  return ShadowExtensionNode{shadowHash}
}
```

##### Shadow Branch Node

For branch nodes, there would be 16 items corresponding to each of the sixteen possible nibble values ​​of the keys in which they are traversed. And the ShadowBranchNode would have two elements:

ShadowHash: a unique hash value of the following shadow nodes.

EpochMap: a metadata to keep the corresponding item’s last accessed epoch index.

> Please go to the original BEP to view the picture.

```auto
type ShadowBranchNode struct {
    ShadowHash *common.Hash
    EpochMap     []uint16
}

func (node *BranchNode) ShadowNode() ShadowBranchNode {
  // Get the epoch infor of itself
  epochSelf := node.EpochIndex
  // Get the epoch infor of its children
  epochChild := node.EpochChild()

  // to calculate the ShadowHash of a ShadowBranchNode
  var shadowHash *common.Hash
  hashList := []common.Hash{}
  for i, child := range node.children {
    // skip expired node.
    if epochSelf >= epochChild[i] + 2 {
      continue
    }
    if child.isLeafNode() {
        continue
    }
    if child.isExtensionNode() {
        ext := child.ShadowExtensionNode
        hashList = append(hashList, ext.ShadowHash)
        continue
    }
    if child.isBranchNode() {
        br := child.ShadowBranchNode
        brHash := Hash(br.ShadowHash, br.EpochMap)
        hashList = append(hashList, brHash)
        continue
    }
    // unreachable
  }
  if len(hashList) == 0 {
    shadowHash = nil
  } else {
    shadowHash = Hash(hashList)
  }
  return ShadowBranchNode{shadowHash, epochChild}
}
```

Actually, only the ShadowBranchNode will be stored on disk to save IO space, ShadowExtensionNode and ShadowLeafNode will be kept in memory and generated on need.

#### e.RootNode

> Please go to the original BEP to view the picture.

```auto
type RootNode struct {
    Epoch     uint16
    MptRoot   common.Hash
    ShadowRoot common.Hash
}

// to calculate the ShadowRoot
r := rootNode
mRoot := GetMptRootNode(r.MptRoot)
if mRoot.isBranchNode() {
  br:= mRoot.ShadowNode()
  r.ShadowRoot = Hash(br.ShadowHash, br.EpochMap)
} else if mRoot.isExtensionNode() {
  ext:= mRoot.ShadowNode()
  r.ShadowRoot = Hash(ext.ShadowHash)
} else if mRoot.isLeafNode() {
  r.ShadowRoot = Hash(nil)
}

// to calculate the StorageRoot
Account.StorageRoot = Hash(r.Epoch, r.MptRoot, r.ShadowRoot)
```

The storage tries of Epoch 0 do not have the RootNode, if the storage trie is accessed after Epoch 1 then a RootNode will be generated and its hash will be kept in Account.

And the RootNode will never expire.

#### f.Witness Protocol

Witness protocol will define the format of the witness and it will be defined in another BEP.

#### g.State Revive

If the missed state is from the previous epoch, the state revive process will be automatic and will place the state in the current epoch. However, if the missed state is from an even earlier epoch, the user will need to provide a witness to revive it.

### 3.3.General Workflow

#### a.How To Expire

Accounts will not expire, only the L2 storage trie will be subject to expiration, which is used to keep the state of KV slots.

The state expiry is trie node level, the latest epoch index that the trie node was accessed is recorded by its parent, which can be used to determine if the trie node is expired or not. Since we only keep the latest 2 epochs, older trie nodes will not be accessible.

These expired trie nodes can be pruned, but in order to keep the proof generation capability, it is better to only prune the shadow node that is >=2 epochs behind its parent.

#### b.How To Access KV In New Epoch

To access the KV, there would be a path in MPT tree, for each trie node in the path, it has to check its corresponding shadow node first, if it is expired then the transaction would be reverted immediately.

And there are three cases to access the state in the proposal :

1. If the state has already been accessed in the current epoch, it can be returned or updated in the current epoch tree.
2. If the state was last accessed in the previous epoch, the shadow node will be updated, so that it is refreshed.
3. If the state is cold data and has not been accessed in the current or previous epoch tree, it is expired. Trying to access expired state will cause the transaction to revert. To access the expired state, the user needs to revive it first.

#### c.How To Revive State

A new transaction type will be added, which contains witnesses to revive the state.

The full storage trie can be revived through several transactions, and if the witness is too large, partial revival will be supported.

Anyone can restore the data as long as they are willing to pay.

It is optional to revive the corresponding shadow node, if it is not provided or mismatched, then the elements in epoch map will all be reset to 0 and the ShadowHash will be nil.

#### d.Node Sync Mode: Light & Full & Snap

Light & Full sync mode will stay unchanged, but snap sync will need extra work in the world state heal phase. It will have to sync and heal the shadow tree as well.

## 4.Rationale

### 4.1.Why Keep The L1 Account Trie

There are several reasons to keep it:

The size of the L1 account trie is relatively small, constituting only around 4% of the L2 storage trie on BSC as of the end of 2022.

The L1 account trie contains crucial information about user accounts, such as their balance and nonce. If users were required to revive their accounts before accessing their assets, it would significantly impact their experience.

By retaining the L1 account trie, the witness verification process can be much simpler.

### 4.2.Why Not Create A New L2 Storage Trie

In this proposal, the trie skeleton will be kept in a new epoch. There are other approaches which will generate a new trie tree from scratch at the start of a new epoch. Although they provide a comprehensive solution for state expiry, there are still two unsolved issues to address: account resurrection conflict and witness size. Additionally, they would have a significant impact on the ecosystem and rely on other infrastructure, such as address extension and Verkle Tree.

By keeping the skeleton of the trie, it would be much easier to do witness verification and have less impact on the current ecosystem.

### 4.3.Reasonable Epoch Period

The state will expire if it has not been accessed for at least 1 epoch or at most 2 epochs. On average, the expiry period is 1.5 epochs. If we set the epoch period to represent 2/3 of a year, then the average state expiry period would be one year, which seems like a reasonable value.

## 5.Forward Compatibility

### 5.1.Account Abstraction

Account abstraction implementation will be impacted, as these accounts could be stored in the L2 storage trie and could be expired.

### 5.2.L2 Rollup: Optimism & ZK

Rollups could be impacted if the rollup transactions try to access expired storage.

## 6.Backward Compatibility

### 6.1.Transaction Execution

The current transaction types will be supported, but if the transaction tries to access or insert through expired nodes, then it could be reverted.

### 6.2.User Experience

There are several changes that could affect user experience. The behavior of many DApps may change and users will have to pay to revive their expired storage. If the revival size is very large, the cost could be expensive.

### 6.3.Web3 API

Some of the APIs could be impacted, such as: getProof, eth_getStorageAt…

### 6.4.Snap Sync

The snap sync mode will heal the world state after the initial block sync. The procedure of world state healing in snap sync mode will need to be updated.

### 6.5.Archive Node

More storage volume would be needed for the archive node, since more metadata will be generated in each epoch. The increased size could be remarkable, which would make the current archive node reluctant to keep the whole state of BSC mainnet. Archive service may have to be supported in other approaches.

### 6.6.Light Client

The implementation of the light client would be impacted, since the proof of the shadow tree would also be needed.

## 7. License

The content is licensed under CC0

## Replies

**0xbundler** (2023-03-28):

[Refer to the original proposal for more illustrations](https://github.com/bnb-chain/BEPs/pull/215)

# BEP-215: Revive State Transaction with Witness

## 1. Summary

This BEP aims to introduce a state revival transaction type based on [BEP-206](https://github.com/bnb-chain/BEPs/pull/206). In BEP-206, all unaccessed states in the last two epochs will expire.

The new transaction type contains the necessary witness for state revival and partial newly inserted state conflict detection. This transaction is a supplement to the current transaction type, most interaction scenarios can still use the old transaction type.

## 2. Motivation

State inflation is a common problem with blockchain, especially current users who can permanently use blockchain storage for a one-time fee. The current BEP-206 will expire for more than two epochs of unaccessed states, greatly reducing the storage burden of BSC.  All states need to be kept available at a certain cost. Otherwise, only state revival can be used to access them.

Because account trie data does not expire, existing transaction types can satisfy account-related transactions, such as account transfers, contract creation, and access to the contract account’s unexpired states. But accessing any expired node will result in transactions being reverted.

On the basis of BEP-206, this BEP continues to introduce a new transaction type and witness definition, which are used to revive state and prevent newly inserted state conflict, meanwhile transactions can be executed as usual.

## 3. Specification

### 3.1 New Transaction type

To support state revive, this BEP introduces a new transaction type, while the current transaction type can still be used in most scenarios, called `LegacyTx`, the new transaction type in order to maintain compatibility, begin with a single byte `REVIVE_STATE_TX_TYPE` in the RLP format, the complete transaction definition is as follows:

```go
type SignedReviveStateTx struct {
	message: ReviveStateTx
	signature: ECDSASignature
}
type ReviveStateTx struct {
	Nonce    	uint64          // nonce of sender account
	GasPrice 	*big.Int        // wei per gas
	Gas      	uint64          // gas limit
	To       	*common.Address // nil means contract creation
	Value    	*big.Int        // wei amount
	Data     	[]byte          // contract invocation input data
	WitnessList	[]ReviveWitness
}
```

The `ReviveStateTx` structure is similar to `LegacyTx`, with the `StateWitness` array added for batch state revival. `ReviveStateTx` will verify witness and revive state first, and continue to execute transfer, contract calls and other behaviors as normal transactions.

If the user only wants to revive the states of the contract, it is suggested to simply read the contract or guarantee that the transaction can not revert.

### 3.2 Witness format

In BEP-206, the witness scheme is Merkle proof. Specifically, only the witness of the MPT tree is needed for state revival.

> Please go to the original BEP to view the picture.

The diagram above shows an example of an unexpired MPT structure.

> Please go to the original BEP to view the picture.

Given an example of Merkle Proof for value A in the diagram above, the Merkle Proof generated would only contain the nodes wrapped in boxes.

> Please go to the original BEP to view the picture.

Since a Merkle Proof does not require all nodes to be part of the proof elements in the MPT tree, we can revive selected nodes as shown in the diagram above.

The Merkle Proof witness may be provided in the following structure:

```go
type ReviveWitness struct {
	witnessType byte // only support Merkle Proof for now
	address *common.Address // target account address
	proofList []MPTProof // revive multiple slots (same address)
}

type MPTProof struct {
	key []byte // prefix key
	proof [][]byte // list of RLP-encoded nodes
}
```

### 3.3 Gas computation

In the new transaction type, it introduces an additional field of `StateWitness`, this part will define the extra gas cost, whoever revives that state will have to pay for it. It consists of three parts:

1. StateWitness size cost, and the Gas consumption per byte is defined as WITNESS_BYTE_COST;
2. StateWitness verify cost, and the fixed Gas consumption of each branch is defined as WITNESS_MPT_VERIFY_COST;
3. Revive the state cost, same as a sStore opcode cost;

The calculation rules are as follows:

```go
func WitnessIntrinsicGas(wits []StateWitness) uint64 {
	totalGas := 0
	for i:=0; i Please go to the original BEP to view the picture.

This BEP allows the user to revive the state in batch mode. At this time, the trie nodes could be revived layer by layer to the storage MPT, thereby reducing the gas consumption of batch state revival.

The revived trie nodes rebuild the Shadow Nodes to indicate which child have been revived, or which are still expired.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/6/6a61f50fe165ef06af9133a951cbaddcd2c15deb.png)image972×422 19.9 KB](https://ethereum-magicians.org/uploads/default/6a61f50fe165ef06af9133a951cbaddcd2c15deb)

### 3.5 Witness Generation

Typically, generating a witness (i.e. Merkle Proof) contains the complete path from the root to the leaf node. However, there may be a scenario where some nodes in the path have already been revived. This causes a witness conflict and induces unnecessary computation. Therefore, we can simply generate a partial witness to only revive the expired nodes.

First, we need to get the corresponding storage trie given the account address. Then, we would traverse from the root node to the parent node using the prefix key. The parent node represents the parent of the target revive subtree. From the parent node, we can generate a proof down to the leaf node.

```go
func (s *StateDB) GetStorageProof(address common.Address, parentKey []byte, slotKey []byte) ([][]byte, error) {
	var proof proofList
	trie := s.StorageTrie(a)
	if trie == nil {
		return proof, errors.New("storage trie for requested address does not exist")
	}
	err := trie.ProveStorage(parentKey, slotKey, &proof)
	return proof, err
}
```

### 3.6 Revive State

The user revives the state through the new transaction type, and the submitted witness is usually a Merkle Proof, which can prove the validity of the state. Since BEP-206 marks the expired state through an expired node, state revival only needs to provide the Merkle proof from the expired node as the root.

In order to avoid conflicts, the witness will be divided into the smallest proofs, and the partial revival feature is used to revive it sequentially.

```go
func (s *StateDB) ReviveState(wit ReviveWitness) error {
	addr := wit.address
	proofList := wit.proofList
	for i:=0; i<len(proofList); i++ {
		if !verifyWitness(proofList[i]) {
			continue
		}
		// divide into the smallest proofs and revive all valid trie nodes
		proofs := divideWitness(proofList[i])
		index := s.tries[addr].findFirstValidProof(proofs)
		if index < 0 {
			continue
		}
		s.tries[addr].revive(proofs[index:])
	}
	return nil
}
```

When the block is finalized, storage trie will commit all updates to the underlying storage DB.

## 4. Rationale

### 4.1 Insert Conflict Detection

In the BEP-206 scheme, all expired nodes will be pruned, and the common ancestors of expired nodes will also be pruned, which greatly alleviates the problem of state expansion, and leaves expired node and shadow node to mark the sub-trie expired, for state conflict avoidance and state revival.

When it is necessary to insert a new state through an expired node, even if the state has never been created and expired, it must be proved that the state does not conflict with the previous expired state.

At this time, the partial revival method can be perfectly used to support this insert operation. One thing to note is that if the newly inserted state does not through any expired node, it can be directly inserted without any proof.

### 4.2 Revive State Transaction Estimate

Just like the `eth_estimateGas` method, there needs to be an RPC API provided to the user, which can pre-execute and generate the witness required for the transaction and the gas limit required, which will greatly improve the ecological user experience.

### 4.3 Data Availability

There needs to be a state resurrection service to provide the generation of historical expired state witnesses, possibly by BSC’s DA layer, such as the BNB Green Field project.

### 4.4 Witness Data Cost

Witness data in new transaction types can create additional burdens:

1. The user needs to pay additional Gas according to the witness size when reviving the state. Is there a proof of higher efficiency to reduce Gas consumption;
2. Witness data storage will also occupy extra space. To ensure that TPS will inevitably increase the block gas limit, block historical data will also keep expanding;

These discussions beyond this BEP, and other BEPs will further reduce the cost of state resurrection.

## 5. Forward Compatibility

### 5.1 Verkle Tree

Verkle tree is another solution to replace the current MPT with less witness size, but it’s not ready for production, especially for the whole EVM-compatible ecosystem. When the verkle tree is available, this BEP is compatible to support it.

## 6. Backward Compatibility

### 6.1 Other Transaction Types

The new transaction type introduced by this BEP adds the `TransactionType` prefix in the encoded data to distinguish it from the old transaction type, so as to ensure that the old and new transactions can exist and be used normally at the same time.

`TransactionType` is a one-byte-sized data with a value range of `0x00-0x7f`, which can be reasonably allocated to more transaction types in the future to avoid conflicts.

### 6.2 Hard Fork

This BEP requires the introduction of a new hard fork, which takes effect after the epoch2 phase of BEP-206.

## 7. License

All the content is licensed under CC0.

---

**0xbundler** (2023-03-28):

Here are the advantages in state expiry using BEP-206 & BEP-215:

1. Account data cannot expire, it’s data is limited and increase slowly, keep it is worth in ecosystem friendly and user experience;
2. Shadow nodes solve state conflict problems, it using trie node hash and metadata to verify correct expired states and prevent conflict in new states;
3. Shadow nodes greatly reduce witness size, it allows partial witness revival;
4. The design is more friendly to the ecosystem and user, using MPT and shadow node to support state expiry;

