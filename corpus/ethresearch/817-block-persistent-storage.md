---
source: ethresearch
topic_id: 817
title: Block Persistent Storage
author: skilesare
date: "2018-01-19"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/block-persistent-storage/817
views: 4310
likes: 0
posts_count: 7
---

# Block Persistent Storage

Has there ever been any thought or consideration given to block persistent storage for a contract?

I’m doing some state channel/sharding research and thinking and I’m running across a few situations where I’m limited in what I can do because multiple transactions operating on my contract in the same block can only be reconciled by writing a storage variable.

Example:  Calculating a replacement Merkle root.

Transaction 1:  Comes with a value and a proof.  The transaction operates on the value and adds a new leaf to the current branch of the merkle tree and swaps out the required values up the branch resulting in a new root.

Transaction 2:  Wants to do the same thing on a different branch but can’t because the root has changed.

Current Solution:  Keep track of each replacement hash from transaction 1 in a mapping(block -> mapping(source hash -> replacement hash).  Unfortunately, this is very expensive as it will be at least 20,000 gas for each hash that has been replaced.  If this is a long proof it could get very expensive (not to mention it is eliminating the core reason I was trying to build this contract -> use less gas).

Desired Solution: I only need these values during the current block.  It would be nice to have a much cheaper 0x46 BLOAD and 0x47 BSTORE that could store this mapping during the processing of the block so that my contract can swap out hashes for any additional transactions included in the block.

This storage would need to only be accessible from my contract in order to keep other contracts from trying to manipulate it.

## Replies

**JustinDrake** (2018-01-20):

For the specific problem you put forward (Merkle roots changing), a cool solution is what’s been called “witness auto-update”. I first saw the idea in the [stateless client post](https://ethresear.ch/t/the-stateless-client-concept/172):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[The Stateless Client Concept](https://ethresear.ch/t/the-stateless-client-concept/172/1)

> by the time a transaction propagates through the network, the state of the accounts it accesses, and thus the correct Merkle branches to provide as a witness, may well be different from the correct data when the transaction was created. To solve this, we put the witness outside the signed data in the transaction, and allow the miner that includes the transaction to adjust the witness as needed before including the transaction.

Basically witness updating can be done offchain by validators, and incentives align. See also the post on [auto-updating in the context of account abstraction](https://ethresear.ch/t/account-abstraction-miner-data-and-auto-updating-witnesses/332).

---

**kladkogex** (2018-01-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/skilesare/48/336_2.png) skilesare:

> Desired Solution: I only need these values during the current block.  It would be nice to have a much cheaper 0x46 BLOAD and 0x47 BSTORE that could store this mapping during the processing of the block

Does not seem to me that this can be done securely, since a miner could always include only one of two messages in the block. There is no guarantee that both messages will be in the block.

---

**skilesare** (2018-01-20):

The second message wouldn’t depend on the second. If the second went in the next block it would just fail because the riot would have changed.  The user would need to re issue the second transaction with the now known new root.

There are two things to discuss here 1. How to do this nowish and 2. How to do this to implement sharing.

1. It would be nice to have some system that tracks hashes and swaps out an expected hash for a replacement hash. I had proposed just in one block, but the scenario you mention raises another concern that if you put a low gas price your root will likely be invalid by the time a miner gets to it. The issue it is more restricted to doing something inside the contract.
2. Long term: I love the solution of providing proofs with transaction variables and letting miners keep transitions for x blocks for easy swap ability.

Going back to 1 I’d love to have this operation of putting a var in storage for, x amount of blocks for a much lower gas price.  I know I can later dump the bar to get some gas back, but there isn’t a good way make this happen without issuing a new trx who’s cost outweighs the refund.

---

**denett** (2018-01-22):

An other solution could be to use the Merkle proof of the transaction only to verify its correctness and store the hashes of the original and new hash of the transaction in a verified list.

Once the verified list is big enough a Merkle root update function can be called that inserts all verified transactions in the Merkle tree. (You need to attach the proof that this update is correct)

The extra advantage is that the Merkle root is not updated after each transaction, so it is less likely that new transactions will bounce.

Of course you have to loop over the verified list for every transaction, to make sure the transaction has not yet been updated. If you update a transaction in the verified list, you only have to check the list to see if it is there and it has not yet been updated.

To incentivize users to update the Merkle root once a while, a transaction should also send a small amount of eth to the contract that can be claimed by the user updating the merkle tree. The optimal maximum length of the list depends on the gas saved by updating multiple hashes of the merkle tree at once vs the extra gas cost of looping the list.

---

**skilesare** (2018-02-21):

My concern with this is that I still need some kind of storage to freeze certain things.  Once a particular leaf of my merkle route becomes dirty I need to make sure that it isn’t used again until the hash is updated.  If I use some kind of accumulator as you suggest I can have a broader range of transactions (say if I have 1000 balances, each one could be updated once per update) but I still have to keep track of the dirty ones. Once again I arrive at a place where it would be nice to have some kind of temporary storage with a smaller gas cost.

---

**skilesare** (2018-02-21):

The following contract is an example of a ‘stateless contract’ that is bitcoin like in that each UTXO gets split into a couple of different UTXOs upon each transaction.  The lines that have the comment //todo: check and swap equivalence in block are the place where it would be nice to check some kind of short term storage…maybe it is just during this block, maybe things get stored for a hundred blocks and then dropped.

```
pragma solidity ^0.4.18;

contract StatelessToken1 {

address public owner;
bytes32 public root;
uint256 public totalSupply;

event NewBranch(bytes32 indexed addressFrom, bytes32 amountFrom, bytes32 indexed addressTo, bytes32 amountTo, bytes32 indexed parent);
event SwapLeaf(bytes32 indexed oldLeaf, bytes32 indexed newLeaf);

function StatelessToken1() public{
    owner = msg.sender;
    totalSupply = 1000000 * 10**18;
    root = keccak256(bytes32(msg.sender), bytes32(totalSupply));
    NewBranch(0x0, 0x0, bytes32(msg.sender), bytes32(totalSupply), 0x0);
}

function Transfer(address _to, uint256 _amount, bytes32[] proof){
    require(verifyProof(bytes32(msg.sender), proof[1], proof, root));
    require(_amount  0);

   newLeaf = keccak256(keccak256(_sender, _senderBalance), keccak256(_to,_toBalance));

   bytes32 newHash = newLeaf;

   for(uint thisProof = 0; thisProof < proof.length; thisProof++){
     if(thisProof == 0){
       //do nothing, this is what we are replacing
     } else if(thisProof == 1){
       lastHash = keccak256(proof[0], proof[1]);
       if(lastHash == proof[2]){
        NewBranch(_sender, _senderBalance, _to,_toBalance, proof[2]);
       } else {
           NewBranch(_sender, _senderBalance, _to,_toBalance, proof[3]);
       }

       SwapLeaf(lastHash, newLeaf);
     } else if(thisProof == proof.length -1){
        //do nothing we have newHash
     }
     else{
       if(proof[thisProof] == lastHash){
         lastHash = keccak256(lastHash, proof[thisProof + 1]);
         newHash = keccak256(newHash, proof[thisProof + 1]);
         SwapLeaf(lastHash, newHash);
         //todo: check and swap equivalence in block
         thisProof++;
       } else {
         lastHash = keccak256(proof[thisProof], lastHash);
         newHash = keccak256(proof[thisProof], newHash);
         SwapLeaf(lastHash, newHash);
         //todo: check and swap equivalence in block
         thisProof++;
       }
     }

    }

   return newHash;
 }

 function updateBalance(bytes32 _sender, bytes32 _senderBalance, bytes32[] proof) constant public returns(bytes32){
   bytes32 lastHash;
   bytes32 emptyBytes;
   bytes32 newLeaf;
   bytes32 newHash;

   for(uint thisProof = 0; thisProof < proof.length; thisProof++){
     if(thisProof == 0){
       //do nothing, this is what we are replacing
     } else if(thisProof == 1){
       lastHash = keccak256(proof[0], proof[1]);
       newLeaf = keccak256(_sender, _senderBalance);
       SwapLeaf(lastHash, newLeaf);
     } else if(thisProof == proof.length -1){

        //do nothing we have newHash
     }
     else{
       if(proof[thisProof] == lastHash){
         lastHash = keccak256(lastHash, proof[thisProof + 1]);
         newHash = keccak256(newHash, proof[thisProof + 1]);
         SwapLeaf(lastHash, newHash);
         //todo: check and swap equivalince in block
         thisProof++;
       } else {
         lastHash = keccak256(proof[thisProof], lastHash);
         newHash = keccak256(proof[thisProof], newHash);
         SwapLeaf(lastHash, newHash);
         //todo: check and swap equivalince in block
         thisProof++;
       }
     }
    }
   return newHash;
 }

 //used to clear a 0 balance
 function clearBalance(bytes32[] proof) constant public returns(bytes32){
   bytes32 lastHash;
   bytes32 emptyBytes;
   bytes32 newLeaf;
   bytes32 newHash;

   for(uint thisProof = 0; thisProof < proof.length; thisProof++){
     if(thisProof == 0){
       //do nothing, this is what we are replacing
     } else if(thisProof == 1){
       lastHash = keccak256(proof[0], proof[1]);
     } else if(thisProof == proof.length -1){

        //do nothing we have newHash
     }
     else{
       if(proof[thisProof] == lastHash){
         lastHash = keccak256(lastHash, proof[thisProof + 1]);
         newHash = lastHash;
         SwapLeaf(lastHash, newHash);
         //todo: check and swap equivalince in block
         thisProof++;
       } else {
         lastHash = keccak256(proof[thisProof], lastHash);
         newHash = lastHash;
         SwapLeaf(lastHash, newHash);
         //todo: check and swap equivalince in block
         thisProof++;
       }
     }
    }
   return newHash;
 }

//utility function that can verify merkel proofs
//todo: can be optimized
//todo: move to library
function verifyProof(bytes32 dataPath, bytes32 dataBytes, bytes32[] proof, bytes32 _root) constant public returns(bool){
   bytes32 lastHash;
   bytes32 emptyBytes;

   for(uint thisProof = 0; thisProof < proof.length; thisProof++){
     if(thisProof == 0){
       require(dataPath == proof[thisProof] );
     } else if(thisProof == 1){
       require(dataBytes == proof[thisProof]);
       lastHash = keccak256(dataPath, dataBytes);
     } else if(thisProof == proof.length - 1){
        require(lastHash == proof[thisProof]);
     } else{
       if(proof[thisProof] == lastHash){
         lastHash = keccak256(lastHash, proof[thisProof + 1]);
         thisProof++;
       } else {
         require(proof[thisProof + 1] == lastHash);
         lastHash = keccak256(proof[thisProof], lastHash);
         thisProof++;
       }
     }

    }

   require(lastHash == _root);
   return true;
 }

}
```

