---
source: ethresearch
topic_id: 23315
title: "Zkzkevm: private evm"
author: barryWhiteHat
date: "2025-10-21"
category: Privacy
tags: []
url: https://ethresear.ch/t/zkzkevm-private-evm/23315
views: 1112
likes: 32
posts_count: 11
---

# Zkzkevm: private evm

## Introduction

With the commoditization of zkevms there have emerged interesting opportunities to deliver  private smart contract infrastructure, while maintain evm compatibility. Developers can write solidity and compile it using a version of solidity compiler or some post processing tools. To make private smart contracts.

There are important trade offs around private global state and privacy which stem from the notion that you need to know what you are proving in order to be able to prove it. There for you can’t have a private smart contract with global public state that you don’t know. It follows that you can’t have a private smart contract with global private state. For example uniswap is not possible because the prover needs to know the balance of both pools in order to be able to make a proof a swap has been done correctly. more on that [Why you can't build a private uniswap with ZKPs](https://ethresear.ch/t/why-you-cant-build-a-private-uniswap-with-zkps/7754)

So some of the things we know and love are not possible to implement in a private way, until we have IO, which is why IO is so important. It lets us make a fully private ethereum with exactly the same trust assumptions.

Anyway this post is about how we can add two opcodes to reth pstore and pload , compile it into zkevm and have private smart contracts that have private user state but not private global state.

## How

You have certain contract calls that are private. We do this by leveraging the zkevm code that exists to prove these have been executed correctly but not reveling any information about what the contract actually done. Other than satisfying some requirement, for example that a certain number of tokens have been approved for use from another contract other, but not who’s tokens. We implement two new op codes pstore and pload similar to sload and sstore except the values are private.

## Tool box

We take as our tool chain the zkevm. We will not make any changes to the zkevm itself. We will treat this as a black box. Instead we will make changes to reth. We for reth to add two new trees. The private storage tree (PST) and the private nullifier tree (PNT).

Each leaf in the PST and PNT are published with each update. So anyone can make proof of membership of any leaf. But the values these leaves contain is only known to the user who created them.

### pload

pload is a evm opcode that we add. Its similar to sload. When sload is executed in zkevm the zkzkevm makes a merkle proof that a certin value is in a certin position in the tree.

Similarly for pload we make a proof of membership for that leaf in the tree but we also make a proof that that leaf has not been nullified.

Lets say that we want to pload a value x. So basically we are doing two merkle proofs

1. prove x in PST
2. prove that x.nullifier is not in PNT

Only the user who knows the secret value of that leaf can calculate its nullifier and only such a user can prove that it has not been nullified.

NOTE: sload has a proof of non inclusion implicit because it uses are ordered merkel tree. We can’t use an ordered merkle tree for pload and pstore so we will need to some kind of encoding to ensure that a given leaf has not been created. Such an encoding could be hash (contract, slot, value, nullifier)

NOTE: I think also if you sload an address wiht nothing in it you get 0x0 and that will also need to be considered. Might have to think of a way to handle this in zkzkevm such that the same devex exists. But its hard to prove that a storage slot has not been filled.

### pstore

pstore is going to do the same thing as sstore. But it works a bit differently.

In the zkevm every time an sstore is performed it effectively performs two merkle proofs. The first on proves that the current value of the leaf is x and the second merkle proof calculate the merkle root it the value of x is replaced with y. So you can think of the first proof as getting a summarized proof of all the leaves in the tree and the second proof as replacing just the single leaf (x) with y.

So sstore

1. Prove that a value x is in the tree
2. Replaces it with y

pstore can do the same thing but a bit differently

1. It removes x by getting x.nullifier and adding it to the nullifier tree.
2. It replaces x with y by adding it to the PST.

### Solidity

Solidity compiles to evm opcodes.

Lets say we have the following smart contract

```python3
def transfer(sender, reciver, amount) private:
    bal[sender]= bal[sender] - amount
    bal[reciver] = bal[reciver] + amount
    # this is not adding to the users balance directly. Instead it is kind of input out put thing where the user needs to get the received funds to add to their total balance. This nuance is encapsulated in a receiver address abstraction for now. But needs more work to figure out what is needed on zkzkevm side.
    return(1)
```

The solidity compiler (of some post processor) would see this and replace all the sloads/sstore with ploads/pstores in the bytecode. It would just do this for function that have the private modifier or tag.

## Call chains with some private legs and some public legs

Think of this like a more programmable version of aztec connect. So lets say that we have a private wallet too get that wallet to call uniswap. This can be done but we have to be careful to sanitize message.sender, tx.origin , nonce , gas_price, gas_limit and other meta data leaks. There are a few ways we can do this

1. Create proxy contracts for each call and then rebalance in another tx or at the end of the current tx call stack.
2. Use a global proxy contract

note: tx.origin might need to be sanitized in reth change. But its probably just a bundler so not too bad i think.

## Tradeoffs

This all seems a bit complicated just to make aztec connect. But the power here lies in being able to reuse most of the infrastructure we currently have to be able to enable much more powerful applications.

### Cartel contracts

We talked a bit about private global state and how its impossible to do uniswap and things. But lets say that i want to make a smart contract for me and my friends. I want to keep the source code private publicly but let me and my friends execute it. So this is also possible we just need to relax the data availability guarantees of smart contracts such that the smart contract code does not need to be published.

There is some nuance about data availability guarantees inside the cartel. I suppose we could implement some kind of enforced logging where all data updates are encrypted and published so only cartel members can see.

## Conclusion

It seems that this idea will be immediately useful in two ways

1. Making a private rollup where a monster server makes all the proofs the user gives their data to this server but not everyone else
2. A private rollup where the users makes some of the proofs so their storage accesses are hides from the monster server.

Seems its useful and easy to implement. Requiring no zk knowledge taking the zk as commodity.

## TODO

We need to think more about

1. Should we make EOA’s private by default , it seems possible with some nullifier tricks like getting them to sign “nullifier” and that random string becomes their nullfieir or like nullifier_0 = hash (sign(“nullfiier”) , 0 ) nullifier_1 = hash(sign(“nullifier”,1)) and so on. But to do this we would have to compile all erc20 contracts to use pstore and pload for erc20s. It seems this might break other things. But an manual EOA privacy seems not to include state changes cos mostly people care about erc20 rather then eth.
2. Is it feasible for making a zkevm proof of some relaxed set of things on mobile ? a few ploads
3. If the value you are pstoreing is dynamically generated it better to have a nullifier the monster server can use to store that leaf for you rather than you making the full leaf because of race conditions.
4. How to give out my address such that i can privately receive funds without connecting all my receipts together
5. How can i use logging or other constructs such that i can know if i received funds. Probably as simple as returning a log that includes some kind of encrypted “flag”

## Replies

**Po** (2025-10-22):

Nice post! From my understanding, the preimage of `pstore` is stored in the user’s local database, right? If that’s the case, how can the preimage be recovered if the user loses their local storage.

---

**janmajaya** (2025-10-22):

User can always recover their state with “brute force” trial decryption of all notes in the state tree - but there may exist better methods ( need to think more ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) )

---

**barryWhiteHat** (2025-10-22):

You can derive the preimage from ecdsa signatures so that as long as they have their eth key they are still abe to recover. OR you can encrypt it to that key so tehy can decrypt it later. The only assumption is

1. They are able to keep their eth key (which is the case now)
2. The encypted storage is available to them.

---

**luckyluke21** (2025-10-22):

Nice writeup. The direction makes sense, but I think we can already do better than a zkzkEVM-style approach.

If the goal is to keep execution private while still verifiable, collaborative SNARKs combined with oblivious hashmaps offer a cleaner trust model. Instead of a single proving server that learns the full state, a set of MPC nodes can jointly generate the proof over secret-shared data. Privacy then only depends on a threshold assumption, not on one party staying honest.

This setup effectively replaces the “trusted prover” with a distributed one, while keeping the same verification flow onchain. Oblivious hashmaps (built on MPC-friendly ORAMs) give the private state layer, allowing multiple parties to update shared data without revealing keys or values.

From that perspective, collaborative SNARKs provide a direct path to private shared state (aka private global state) and a weaker trust model than zkzkEVM.

Happy to share more details if this approach seems interesting.

---

**janmajaya** (2025-10-22):

How much does it cost to prove EVM tx execution in co-SNARKs? And, if possible to learn, what are bandwidth requirement per server? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

> Oblivious hashmaps (built on MPC-friendly ORAMs) give the private state layer, allowing multiple parties to update shared data without revealing keys or values.

In this case, do multiple parties trust that distributed set of servers will not collude?

---

**luckyluke21** (2025-10-23):

here are some number for 100k user in the private rollup (defined as in the original post):

- for a write (read is much cheaper) operations (similar as describe in the original post) the cost are sub-cent (that’s all on rather unoptimized code).
- per write the servers need to send ~1MB

every party using this services relies for the privacy on the threshold assumption in the MPC network. important for the correctness of the computation (integrity) there is no trust assumption as they network provides a SNARK

---

**janmajaya** (2025-10-26):

This is amazing!

Just one last question, maybe I missed it. But how many servers do you assume when you quote performance numbers? And how does performance vary with no. of servers? Does it increase or stays consistent?

---

**0xRowan** (2025-11-18):

Is there a corresponding implementation? Where can I try it?

---

**barryWhiteHat** (2025-11-19):

No implementation at the moment.

Please let me know if someone is working on this ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**Caerlower** (2025-11-25):

This is a pretty cool write-up. The pload/pstore idea makes sense for what you’re trying to achieve, private per-user state without pretending we can do fully private global state in a ZK system. The PST/PNT setup is clever, and honestly feels like a practical way to get “ZK-friendly privacy” without blowing up the proving costs or rewriting half the stack.

I have seen that Oasis Protocol has been taking the same kind of approach, but from the opposite direction. Instead of forcing all the privacy guarantees through zero-knowledge proofs, they lean on tees & attested off-chain execution (rofl) and sapphire for private EVM. You get private state, private logic, and verifiability, but through hardware-based isolation instead of proving everything.

These are different trust assumptions, but the end goal is similar, which is to let devs build private smart contract flows without redesigning Ethereum from scratch.

Cool to see both paths being explored, feels like the ecosystem is finally moving past the “one privacy model for everything” mindset.

