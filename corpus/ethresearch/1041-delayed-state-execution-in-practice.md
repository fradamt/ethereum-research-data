---
source: ethresearch
topic_id: 1041
title: Delayed state execution in practice
author: vbuterin
date: "2018-02-10"
category: Sharding
tags: [execution, state-execution-separation]
url: https://ethresear.ch/t/delayed-state-execution-in-practice/1041
views: 8212
likes: 6
posts_count: 17
---

# Delayed state execution in practice

Prerequisite: [Delayed state execution, finality and cross-chain operations](https://ethresear.ch/t/delayed-state-execution-finality-and-cross-chain-operations/987)

---

If we are to go with a model where state execution is a separate process that trails behind collation selection, then the next question is: how *do* clients figure out what the state is? Super-full nodes can always execute every collation, but every other type of node needs some kind of light client protocol.

Here is one simple proposal. Allow anyone with ETH in any shard to deposit their ETH (with a 4 month lockup period), and at certain points (eg. once every Casper epoch) give depositors the ability to make claims about the state at some given height. These claims can be published into the blockchain. The claims would be of the form `[height, shard, state_root, signature]`. From the point of view of a node executing the state, a correct claim is given some reward proportional to the deposit (eg. corresponding to an interest rate of 5%), and a false claim means the claimer is penalized.

This is the simple “cryptoeconomic light client” design; anyone who sees a claim knows that either (i) the claim is true, or (ii) in the *real state*, the depositor that made the false claim loses their deposit. It could be potentially used as a light client design even for Ethereum 1.0 today, though with a layer of indirection as the EVM only has access to block hashes, and so the state root would need to be confirmed by including the block header, checking its hash, and then extracting the state root.

However, when used with sharding it has a flaw: if too few nodes are super-full nodes (ie. nodes with O(c2) computing power that process the entire chain), then if a 51% attack on the state calculation layer takes place (which is quite feasible, since every shard has separate state calculation deposits), then it may not *matter* what happens to the deposits in the real state, because no one will know what the real state is (or at least there will be so few actors that do that they [could collude](https://vitalik.ca/general/2017/05/08/coordination_problems.html) to pretend it’s something other than what it actually is).

### Interactive verification

Hence, what we actually need is something like an interactive verification protocol, where if any substantial disagreement at any particular point takes place the client calculates the state transition at that point themselves, so that even in the presence of a 90% attack on any single shard a client can still figure out the correct state. The following is a proposal for doing that.

We will start off by making a series of changes to the above cryptoeconomic light client protocol that we introduced above. First, we switch from claims being `[height, shard, state_root, signature]` to `[height, collation_hash, shard, state_root, signature]`. A claim that specifies the wrong collation_hash for a given height does not receive any reward or penalty; only a claim with the *correct hash* but the *wrong state root* is penalized. This has three effects:

1. It means that it’s the client’s responsibility to determine what the correct chain is. The chain of reasoning for a client would be “my chain selection process tells me that the collation at height H is 0x1234, and I have 357000 ETH worth of claims showing that if the collation at height H is 0x1234 then the state root is 0x5678, and so I believe that the state root at height H is 0x5678”.
2. It means that state executors do not have to assume “reorg risk”; because their claims are now conditional on a particular history, and state execution is a deterministic process, they can only lose money if they deliberately provide the wrong state root.
3. As a consequence of (2), it becomes safe to have very harsh penalties for claimers giving bad answers. Specifically, we can make the penalty be the entire deposit, or follow the Casper approach where if the portion of claimers that make incorrect claims is p, then the claimer loses portion 12 * p of their deposit, or 100% if p >= 1/12.

Now, we change the claims to `[height, shard, prev_state_root, collation_hash, post_state)_root, signature]` - making claims also dependent on the *previous* state root.  Clients can then make estimates of the state by treating claims as a graph, where states are vertices, collation hashes are edges and the total deposit size of claims is the weight; to evaluate the correct state, clients would start at the genesis, with the head state being the genesis state, and then follow a GHOST-like protocol where at each stage, clients select the child state root with the most claims staked on it, conditional on the prev state root being the current head state.

That is, clients would follow a chain of reasoning like:

- I know the pre-state root at height 0 is 0x1234 because that’s the genesis state, which is the protocol params
- I know the block hashes at heights 0, 1 and 3 are 0xabcd, 0xabce and 0xabcf.
- There’s 520000 ETH staked on the claim that if the pre-state root is 0x1234 and the block hash at height 0 is 0xabcd, then the state root at height 0 is 0x5678
- There’s 437000 ETH staked on the claim that if the post-state root at height 0 is 0x5678, and the block hash at height 1 is 0xabce, then the post-state root at height 1 is 0x9012.
- There’s 619000 ETH staked on the claim that if the post-state root at height 1 is 0x9012, and the block hash at height 2 is 0xabcf, then the post-state root at height 2 is 0x3456.
- Hence, I know that either (i) the post-state root at height 2 actually is 0x3456, or (ii) at least 437000 ETH will be lost.

The purpose of this is to make state claims “bite-sized”, in the sense that the correctness of any individual claim can be evaluated by re-checking the execution of only one block.

We now add the interactivity. If a client sees that, for some given (shard, prev state root, collation hash) there are two or more conflicting answers being given, with more than some threshold if disagreement (say, 10%), it doesn’t believe *any* claim until it receives a proof of execution - the full collation data plus witnesses, which the client can re-execute to determine what the *actual* post-state root of the execution, conditional on the prev state, is. The client software can treat the proof of execution as being like a conditional bet, but with a weight of infinity.

### Cross-shard communication

We now add asynchronous cross shard communication. Now, the execution of a collation depends not just on the prev state and the collation, but also on receipts from CROSS_SHARD_DELAY (eg. 5) blocks ago. Receipts are generated by execution, and so we can simplify by assuming that receipts are part of the state. Hence, calculating the state of any shard at height H requires knowing the state root of every shard at height H-5. In order to preserve the “zero external risk” property of honest state execution claiming, we thus need to make the claims be conditional on the prior state of *every* shard. We do this by creating an implicit `meta_state_root`, which is the root hash of a Merkle tree of all the state roots; the claims become `[height, shard, prev_state_root, prior_meta_state_root, collation_hash, post_state_root, signature]`.

Here is a sample code for how a client could run in this paradigm:

```python
from ethereum.utils import sha3
NUM_SHARDS = 64
CROSS_SHARD_DELAY = 5
GENESIS_STATE = b'\x00' * 32

# Database mock
class EphemDB():
    self.kv = {}

    def get(self, k):
        assert isinstance(k, bytes)
        return self.kv[k] if k in self.kv else None

    def put(self, k, v):
        assert isinstance(k, bytes)
        if isinstance(v, int): v = str(v)
        if ininstance(v, str): v = v.encode('utf-8')
        self.kv[k] = v

# Set the block hash of the given block height and shard
def set_blockindex(db, height, shard, blkhash):
    # Put hash
    db.put(b'block:%d-%d' % (height, shard), blkhash)
    # Set max score calc *for this shard*
    existing_max = int(db.get(b'max_score_calc:%d' % shard))
    db.put(b'max_score_calc:%d' % shard,
           min(existing_max, height - 1))
    # Set max height
    existing_max = int(db.get(b'max_height:%d' % shard))
    db.set(b'max_height:%d' % shard, max(existing_max, height))

# Get the block hash of the given block height and shard
def get_blockindex(db, height, shard):
    return db.get(b'block:%d-%d' % (height, shard))

# Get the meta state root
def get_metastate_root(db, height):
    return db.get(b'merkle:%d-%d' % (height, 1))

# Add a bet of the form `prev state, blockhash, root -> post_state`
# with some given size
# Note: an execution proof is a bet of infinite size
def add_bet(prev_state, blockhash, root, shard, post_state, size):
    # Add to the score for the post-state in this context
    bethash = sha3(prev_state + blockhash + root + post_state)
    cur_score = int(db.get(b'score:' + bethash)) or 0
    db.put(b'score:' + bethash, cur_score + size)
    # Check the max score for this context; if the score for
    # the given post-state is higher, change the child pointer
    position_hash = sha3(prev_state + blockhash + root)
    cur_max_score = int(db.get(b'score:' + position_hash)) or 0
    if cur_score + size > cur_max_score:
        db.put(b'score:' + position_hash, cur_score + size)
        db.put(b'winner:' + position_hash, post_state)
        existing_max = int(db.get(b'max_score_calc:%d' % shard))
        db.put(b'max_score_calc:%d' % shard,
               min(existing_max, height + CROSS_SHARD_DELAY))

# Assuming the state for height H-1 has been estimated, estimates
# the state for height H
def calc_candidate_child(height, shard):
    prev_state = db.get(b'state:%d-%d' % (height - 1, shard)) \
        if height else GENESIS_STATE
    blockhash = get_blockindex(height, shard)
    root = get_root(height - CROSS_SHARD_DELAY) \
        if height >= CROSS_SHARD_DELAY else b'\x00' * 32
    position_hash = sha3(prev_state + blockhash + root)
    old_state = db.get(b'state:%d-%d' % (height, shard))
    new_state = db.get(b'winner:' + position_hash)
    if old_state != new_state:
        db.put(b'state:%d-%d' % (height, shard), new_state)
        db.put(b'merkle:%d-%d' % (height, NUM_SHARDS + shard), new_state)
        # Update a Merkle tree of state roots to compute the meta-state root
        i = (NUM_SHARDS + shard) // 2
        while i:
            L = db.get(b'merkle:%d-%d' % (height, i*2)) or b'\x00' * 32
            R = db.get(b'merkle:%d-%d' % (height, i*2+1)) or b'\x00' * 32
            db.set(b'merkle:%d-%d' % (height, i), sha3(L + R))
            i //= 2
        # Annul all scores more than CROSS_SHARD_DELAY after this height
        existing_max = int(db.get(b'max_score_calc'))
        db.put(b'max_score_calc', min(existing_max, height + CROSS_SHARD_DELAY))

# Recalculates state for the given shard for the appropriate range
def recalc_states(shard):
    range_start = min(int(db.get(b'max_score_calc')),
                       int(db.get(b'max_score_calc:%d' % shard)))
    range_end = db.get(b'max_height:%d' % shard)
    for h in range(range_start, range_end):
        calc_candidate_child(h, shard)
    db.set(b'max_score_calc:%d' % shard, range_end)

```

---

2018.03.12 addendum:

The protocol as written may be inefficient, because if there is a very large number of executors on each shard, then there will be a very large number of messages that the chain needs to process every block. We can reduce this inefficiency in two ways:

1. Randomly sample, so only a specific 1% (or whatever other percentage; perhaps a fixed number, like 50) of validators are allowed to make a claim during each block. Have clients execute the collation themselves if >10% of the validators that vote disagree with the majority.
2. Have individual claims be over a few consecutive epochs, rather than a single epoch; this allows signatures to be reused.

Note that because claims are included in the chain as raw signed objects, a client can get the complete set of claims by just scanning the chain; additionally, note that a client can get claims about the state of block B from inside blocks that are descendants of B, even without knowing the state of those blocks yet, because the client can find the claims simply by scanning the chain.

## Replies

**JustinDrake** (2018-02-16):

I love the idea of fork choice rules for execution. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) The portfolio of strategies for minimised onchain execution keeps expanding:

- Fraud proof execution

User-collaterised (e.g. cryptoeconomic accumulators)
- Executor-collaterised (e.g. interactive verification execution)

Cryptographic execution

- SNARKs/STARKs verified onchain
- Executor-collaterised SNARKs/STARKs (to avoid onchain proof verification)
- Eventually-cryptographic execution (to address prover latency)

Fork choice rule execution

I’ve written your fork choice rule scheme below in my own words (skipping the cross-shard communication section for discussion in another post). It took me quite some time to digest your post and fill in detail that made sense to me. Did I get anything wrong below?

**Construction**

We have an Executor Manager Contract (EMC) in each child shard. The EMC is a “black box” contract where execution of the EMC is done via externally enshrined fork choice rules. The EMC mints ETH to reward executors.

The EMC has the following methods (mirroring [those of the VMC](https://github.com/ethereum/sharding/blob/develop/docs/doc.md#validator-manager-contract-vmc)):

- deposit: Immediately adds an executor to the executor set and issues an ExecutorAdded log.
- withdraw: Immediately removes an executor from the executor set and issues an ExecutorRemoved log. After a 4 months lock period the initial deposit plus rewards minus slashing is released.
- addClaim: Takes a claim of the form [height, shard, prev_state_root, collation_hash, post_state_root, signature] and issues a ClaimAdded log. If the claim is valid and truthful then an ExecutorRewarded log is issued. If the claim is valid and untruthful then an ExecutorSlashed log is issued.

(Having logs is not strictly necessarily but helps the discussion below. It also helps light clients efficiently search for EMC events using the Bloom filter indexing of logs.)

A claim is valid if:

1. The shard number matches that of the EMC.
2. The collation_hash matches the collation header at the specified height.
3. The signature is a valid signature from the executor set.

A claim is truthful if `prev_state_root` and `post_state_root` are the real state roots corresponding to the collation with hash `collation_hash`.

The EMC does not gate the submission of claims (`addClaim` always returns `True`) and has no notion of real state. Instead honest executors calculate the real state through offchain execution and use it to check the truthfulness of claims.

The valid (but not necessarily truthful) claims naturally form a directed and weighted graph, called the “claims graph”. The vertices are the state roots included in valid claims, and there’s a directed edge from `prev_state_root` to `post_state_root` with weight the sum of the corresponding claims. If all valid claims are also truthful then the claims graph forms a “claims chain” pointing from genesis to the real state root. If not, at least one of the depositors gets slashed and the real state is correspondingly updated.

Slashing happens as a fork choice rule by executors (*not* validators) within the EMC. So we have three nested fork choice rules:

- miners choose block headers in the main shard
- validators choose collation headers in the VMC
- executors choose claims in the EMCs

Light clients can guess the real state following a GHOST-like protocol on the claims graph. For that they need to:

1. filter out invalid claims, i.e. check the shard, height, collation_hash and signature of every claim
2. know the weight of executors to apply the correct weighting to the claims graph

Filtering out invalid claims is the easy part. It assumes the availability of `ExecutorAdded`, `ExecutorRemoved` and `ClaimAdded` logs. These three logs readily derive from transactions that call the `deposit`, `withdraw` or `addClaim` method of the EMC.

Knowing the weight of executors is harder. First of all, the issuance of `ExecutorRewarded` versus `ExecutorSlashed` logs depends on `prev_state_root` and `post_state_root` matching the real state which light clients are trying to guess. Second, if slashing does occur then the claims graph needs to be retrospectively re-weighted, which itself affects the guessing process.

To address the inherent uncertainty around the issuance of `ExecutorRewarded` versus `ExecutorSlashed` logs, light clients use heuristics. They settle disagreements among executors at a vertex of the claims graph as follows:

1. If the disagreement is over 10%, all claims are ignored until a valid proof of execution is verified, in which case the known-truthful claims are given a weight of infinity and the executors with known-untruthful claims are slashed.
2. If there is no disagreement, or the disagreement is under 10%, light clients follow an optimistic strategy where they don’t do any slashing.

**Initial questions and remarks**

1. Is the above description of the scheme correct?
2. For light clients it seems the scheme depends on the historical availability of transactions that call the EMC, or at least the availability of the ExecutorAdded, ExecutorRemoved and ClaimAdded logs to filter out invalid claims. Is that right?
3. For executors it seems that the EMC has “black box” state. Indeed, the EMC has implicit state (namely, the set of depositors and their weight) which is reflected in the state roots but never made explicit. It cannot be made explicit because the state transitions of the EMC for ExecutorRewarded and ExecutorSlashed logs is done with fork choice rules without explicit witness-bearing transactions. Does this bar new executors from joining the EMC without historical availability of the transactions (see the above point)? Maybe we can isolate the EMC’s state from the rest of the shard’s state somehow.
4. Not only do light clients need to download and evaluate the ExecutorAdded, ExecutorRemoved and ClaimAdded logs, they also need to keep these in memory in order to allow for retrospective re-weighting if the optimistic strategy turns out to be wrong. Is that correct?

---

**vbuterin** (2018-02-16):

It’s important here to really philosophically grasp what state execution processes are and what they can do. The EMC is itself part of the state of each shard; hence, the EMC only “exists” in so far as it is being instantiated by state execution processes. State execution processes have the following properties:

1. The real post-state of block Bn, with ancestry chain [B0, B1, B2, B3 ..... Bn], can be computed via stf(stf(stf(...stf(GENESIS_STATE, B0) .... B(n-2)), B(n-1), Bn), or more intuitively: GENESIS_STATE --(B0)--> S0 --(B1)--> S1 --(B2)--> S2 -- .... --> S(n-1) --(Bn)--> Sn.
2. The real post-state of some block is a mathematical function, and so it is a thing, like a kind of Platonic ideal, that exists independently of whether or not anyone ever actually correctly computes it.
3. However, in reality we of course want and expect users to employ various strategies to either directly, or cryptographically (ie. snarks) or cryptoeconomically (ie. fraud proofs) to successfully determine the correct recent state of the canonical chain.
4. The state is aware of its own previous state roots. For example, this could be done by giving the EVM a “current state root” opcode, and then having a block post-processing function that pushes this value into some storage key of some contract.

So IMO saying that “the EMC … has no notion of real state” is not really correct because the EMC only exists in so far as it is being executed as part of the state transition function, and so the execution of the EMC is fully aware of the state at the time, and is also fully aware of the “actual” value of past state roots. So when you say “if not, at least one of the depositors gets slashed and the real state is correspondingly updated”, keep in mind that this would be done *by the `addClaim` function of the EMC*, so the function affects state instead of just issuing logs.

Well, kinda - there is one other way to do it. And that is that the EMC doesn’t actually store any depositor balances; that’s all done on the main shard. And the *main shard* EMC has logic which processes logs created inside the EMC of any shard in order to take away deposits, though we do not introduce this at first (this would only get introduced once we add shard-to-main-chain transactions).

> Knowing the weight of executors is harder. First of all, the issuance of ExecutorRewarded versus ExecutorSlashed logs depends on prev_state_root and post_state_root matching the real state which light clients are trying to guess. Second, if slashing does occur then the claims graph needs to be retrospectively re-weighted, which itself affects the guessing process.

I would actually recommend not bothering with this, and keeping it super-simple. Assume clients know the state 2 months ago, and the EMC has a withdrawal period of 4 months (a long withdrawal period is crucial). They then use that state to determine the weight of claims.

> For light clients it seems the scheme depends on the historical availability of transactions that call the EMC, or at least the availability of the ExecutorAdded, ExecutorRemoved and ClaimAdded logs to filter out invalid claims. Is that right?

In my model, it requires light clients to know the state 2 months ago. I suppose you could also do it with ExecutorAdded logs, as any ExecutorAdded log that’s less than 4 months old corresponds to an active validator, but then you’d need to keep logging online-ness of validators that don’t log out, so state is really a more suitable tool for the job.

> ClaimAdded logs to filter out invalid claims

No need for ClaimAdded logs. Light clients would just download and verify claims, as in the signed messages, directly.

> It cannot be made explicit because the state transitions of the EMC for ExecutorRewarded and ExecutorSlashed logs is done with fork choice rules without explicit witness-bearing transactions.

???

The state can totally be made explicit. The key insight as I mentioned above is that the entire state transition execution is itself already done client-side with various algorithms, and the state at height N is aware of previous state roots.

---

**JustinDrake** (2018-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Light clients would just download and verify claims, as in the signed messages, directly.

For light clients to remain “light” both verification and download need to be cheap:

- Verification:

What about complex and expensive transactions that make obfuscated addClaim calls? We can’t expect light clients to execute those addClaims. One solution is for the EMC to somehow enforce “simple claims”, i.e. transactions that only directly call addClaim and provide the raw claim data directly in the transaction data.
* How do light clients know whether the caller of simple claims can afford the gas? (Without enough gas, a simple claim executes as a no-op.) In the stateful paradigm we cannot expect light clients to keep track of every account balance. In the stateless paradigm, light clients would not immediately know whether the state root for the caller’s account witness is real. One solution is for the EMC to enforce gas-free simple claims. To maintain incentives, proposers/validators could get rewarded by the EMC by drawing from executor deposits instead of caller accounts.

**Download**: How can light clients know they have downloaded *all* claims without downloading full collation bodies? One solution is to Merklelise all gas-free simple claims and include a “claims root” in the header, with the additional consensus rule that collations are only valid if the claims root was constructed properly.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In my model, it requires light clients to know the state 2 months ago.

That’s a significant simplification ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

1. What is the source of the state 2 months ago? Is it a trusted or trustless source, and how do light clients know they get the real state (assuming no snarks)?
2. If the state used to run the GHOST-like protocol is stale by 2 months then a large adversarial executor may be able to fool light clients for up to 2 months with a single slashing.
3. Do light clients periodically refresh the 2 months old state, e.g. once a day? If so, should light clients be encouraged to sync up to the same daily checkpoint otherwise different light clients may come to different conclusions from running the GHOST-like protocol?

---

**vbuterin** (2018-02-18):

`addClaim` would take as input a signed object containing the claim, and it would for convenience emit an exact copy of the object as a receipt. Separately from their inclusion in the blockchain, these claims would be broadcasted around the network, and could be downloaded by light clients. A light client receiving the claim would know that either the claim has been included in the chain, or if not, that it soon would be, especially if it’s an incorrect claim (like in Casper FFG, we can add a rule that 4% of the slashed deposit goes to the submitter as a bounty).

> One solution is for the EMC to enforce gas-free simple claims.

This would make it identical to how Casper FFG works with votes; I’d support that.

> How can light clients know they have downloaded all claims without downloading full collation bodies?

Is it really that necessary that they do know this? Even downloading a partial set of claims gives you a pretty strong cryptoeconomic assurance.

> One solution is to Merklelise all gas-free simple claims and include a “claims root” in the header, with the additional consensus rule that collations are only valid if the claims root was constructed properly.

Yeah, I suppose that can help.

> What is the source of the state 2 months ago? Is it a trusted or trustless source, and how do light clients know they get the real state (assuming no snarks)?

If a client hasn’t been online for a full withdrawal period, then it would need to get the updated state from a trusted source, although Casper FFG already has this property so it doesn’t weaken the security model.

> Do light clients periodically refresh the 2 months old state, e.g. once a day?

They should refresh whenever they’re online.

> If so, should light clients be encouraged to sync up to the same daily checkpoint otherwise different light clients may come to different conclusions from running the GHOST-like protocol?

Remember that state execution is not a consensus game; there really is only one correct answer. So if two different light clients come to different conclusions, that implies that a lot of people lost a really huge amount of ETH. In fact, it should not even be possible for two different light clients to come to different conclusions, unless there is a really successful attempt to censor evidence for at least one side. The reason is that if at any particular branch point there’s anything less than a 90% consensus in favor of one side, then that triggers the “download the full proof and check it yourself” rule, which all light clients would execute in the same way.

---

**JustinDrake** (2018-02-19):

Thanks for all the clarifications ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> addClaim would take as input a signed object containing the claim, and it would for convenience emit an exact copy of the object as a receipt

In case it wasn’t clear, that’s what I intended for the `ClaimAdded` (receipt) log. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> state execution is not a consensus game

I want to push back a bit on this philosophical point as it has practical implications. State execution can be modelled as a Platonic ideal, and in such a model not be a consensus game. In reality state execution is arguably a consensus game (see also “Background on consensus” in [this post](https://ethresear.ch/t/fork-free-sharding/1058)) for several reasons:

1. Higher-level consensus: There is a higher-level consensus game in choosing which execution rules to run in the first place, e.g. Ethereum vs Ethereum Classic or Byzantium vs Constantinople.
2. Specification ambiguity: Even if all clients intend to run the same execution rules, the act of specifying the rules (e.g. in EIPs, yellow paper, etc.) is generally ambiguous. Edge cases will be unspecified or over-specified (i.e. contradictorily specified), and different clients will handle some cases differently.
3. Implementation bugs: Even if all clients intend to run the same execution rules, and the rules are perfectly specified, implementations will have bugs. See for example Consensus bug in geth v1.4.19 and v1.5.2.
4. Censorship: This execution scheme emphasises another notion of locality to execution, namely that light clients may come to different conclusions when evidence is censored.

Points 2) and 3) are bad for executors because it can lead to a significant portion of deposits to be slashed. Execution risk being financially borne by executors via slashing may deter some executors from participating in the first place.

---

**vbuterin** (2018-02-20):

Agree that we need to think more deeply about (2) and (3); *any* interactive verification game is going to be tricky when there are risks of bugs in the executor. The only approach that I can think of, other than recommending clients to run multiple implementations and not make any claims if they disagree, is to reduce the penalties to make them more moderate at first.

---

**kladkogex** (2018-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If we are to go with a model where state execution is a separate process that trails behind collation selection,

As a suggestion - since collators see all blocks anyway, and since running EVM without any Merkle state root calculations is easy (?), collators could run a light version of the EVM without doing any state root calculations, so collators would be an additional aware of the state.

Then if there is a discrepancy (which is supposed to be a rare event) you could ask collators to actually calculate the state root and serve as judges

In this case one would not need to implement EVM in the light client.

Another benefit of this would be to speed up confirmations - if I want to confirm the value of a particular variable X, I could simply ask a large number of collators and if all of them return the same number I would accept this as a confirmation.

---

**vbuterin** (2018-03-01):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> and since running EVM without any Merkle state root calculations is easy (?)

The cost of state execution is mostly IO. That technically could be reduced greatly by storing a state in a different format where you can access accounts directly instead of walking down the Patricia tree, but that’s something that clients really should do anyway; even if they do that they can still maintain the Patricia tree separately with relatively low additional cost.

---

**nate** (2018-03-02):

Very cool! The application to cross-shard transactions is very exciting ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

If claims are free to create, it seems like there’s a fairly trivial DOS attack where some executors generate a large number of claims on randomly generated `collation_hash`es, thus receiving no penalty. In the case of gas-free claims, this is especially bad, as there’s essentially no cost to getting a huge number of claims on-chain/to clients.

Two possible solutions are a) requiring that some small fee is paid for each claim is submitted (but then it’s pretty much gas, and we have the issue [@JustinDrake](/u/justindrake) describes), or b) requiring a small amount of PoW with each claim. There are probably more complexities with the second one as well, though (difficulty adjustments? global difficulty?).

---

**nate** (2018-03-02):

Also, it seems like there might be another DOS vector, whereby a validator can cause a large number of claims to be generated by causing a reorg on a shard. For example, let’s say a validator causes a reorg of `reorg_length` > `CROSS_SHARD_DELAY`. In this case, all previous claims on all other shards would be worthless (as the `prior_meta_state_root` is incorrect). Thus, all executors on all shards need to make new claims on these blocks.

As new claims would have to be generated for each block, it seems like this would result in `num_shards * (reorg_length - CROSS_SHARD_DELAY) * num_executors_per_shard` new messages being generated, which seems like quite a lot for a reorg. We can make the `CROSS_SHARD_DELAY` really high (or wait for finality), but then we’re in the same situation we were before delayed state execution.

I might be missing something here that makes this a non-issue, but the best I’ve been able to figure out in terms of “solutions” would be somehow making it so executors only need to commit to the past state roots on relevant shards. For example, the `prior_meta_state_root` of a claim on `shard_a` only commits to the state root of shards that generated receipts for `shard_a`. This isn’t really a solution to the attack, as an attacker can make a transaction that generates a receipt for a bunch of other shards, but may improve things in the event of a regular reorg.

---

In the same line of thinking, wouldn’t it be quite easy for a bribing attacker to cause some amount of chaos for relatively cheap? Essentially, imagine if an attacker committed to giving each executor some amount greater than the reward for proper execution if they don’t make a claim on some block for some large delay.

Because there isn’t an “increasing amount of punishment” that occurs when executors don’t make claims on some specific blocks (really, just lost rewards), it seems that each executor has an incentive to wait on making a claim on this specific block. As with your forkchoice example, a block’s state root is only committed to with the minimum of the commitments to the blocks in its history (if that makes sense), and thus all claims on future blocks (even if they are finalized) are worth nothing. Might be missing something here as well.

---

**vbuterin** (2018-03-03):

Yeah, bribing attackers can definitely cause some degree of chaos unless CROSS_SHARD_DELAY >= finality time. I don’t think that’s avoidable. Though I think that setting CROSS_SHARD_DELAY to equal some point where reorging the chain is hard for non-economic reasons (eg. it’s passed a few random sampling checks, so forking would require a violation of honest majority) is fine; it will almost never happen in practice, and even if it does, the only harm is that it adds overhead to the chain.

Also, I actually am fine with claims having to pay for gas. It discourages making claims too quickly, or making claims for chains that are not likely to be canonical.

---

**nate** (2018-03-17):

It seems like this adds considerable overhead compared to a [simple casper light client](https://ethresear.ch/t/simple-casper-light-client/828).

To find the current state root, light clients must download claims for each block starting from the last state root they are sure of. Else, as claims are conditional on the previous state root, if there is a “break” in the chain somewhere, claims after the break are worth nothing. This makes light client sync proportional to the number of blocks they were offline, rather than constant (as the light client linked above).

Also - what’s the impact on weak subjectivity? If a client is coming online for the first time and just has a recent block hash, unless they start from the genesis and work their way to the current state root on that block, any claims on this block’s state root are worthless to them (again, because there could be a break in the chain somewhere that they have to check for). A simple solution to this is including the state root in the weak subjectivity format.

Adding unconditional claims about state roots (similar to what the simple light client w/ finalized blocks) would seemingly address both of these concerns for a bit more complexity.

---

**vbuterin** (2018-03-17):

> It seems like this adds considerable overhead compared to a simple casper light client.

Correct, but it has the benefit that it can survive 51% attacks on the execution layer, which is very important here as the execution layer is shard-specific and so 51% attacks can very feasibly happen.

> If a client is coming online for the first time and just has a recent block hash

We extend the assumption - we expect clients to have both a recent block hash and a recent state root.

---

**kladkogex** (2018-06-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Here is one simple proposal. Allow anyone with ETH in any shard to deposit their ETH (with a 4 month lockup period), and at certain points (eg. once every Casper epoch) give depositors the ability to make claims about the state at some given height. These claims can be published into the blockchain. The claims would be of the form [height, shard, state_root, signature] . From the point of view of a node executing the state, a correct claim is given some reward proportional to the deposit (eg. corresponding to an interest rate of 5%), and a false claim means the claimer is penalized.

Which mechanism will be used to prevent front running ?(someone can make a deposit, do zero work, repost the state root from an honest executor, and then claim the reward).

---

**daniel** (2018-11-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Which mechanism will be used to prevent front running ?(someone can make a deposit, do zero work, repost the state root from an honest executor, and then claim the reward).

I think this might be covered by the risk of “betting” on a wrong state root and losing the deposit as opposed to the relatively minor inconvenience of actually doing the execution. But I do think this might be a problem, do you have any suggestions for improvement?

However, I see a different issue with the combination of delayed state execution and stateless validators as in the current Ethereum 2.0 spec. If the proposer and the committee are randomly sampled from beacon chain validators, then the proposer does not know the current state of the shard and has to guess/randomly include transactions into the proposed block.

This seems like a DoS vector to me, since an attacker could just spam a shard with invalid transactions from empty accounts, and if the amount of spam transactions significantly outsize the amount of honest transactions, basically stall the entire shard forever at very little cost.

Am I missing something in the approach / has the idea matured in the meantime?

Otherwise, my suggestion would be to use executors, which are randomly sampled from a pool of collateralized executors on the beacon chain (similar to validators, just with slower reshuffeling, e.g. reshuffle half of the executors every week) as a “filter”. The executors would receive transactions from users and store them in a transaction pool, filtering out all spam/invalid transactions.

Then, every shard block, we would have a different committee from which one proposer randomly samples transactions from the shard-local set of executors. The committee then attests to this block and then the described delayed state execution process is executed. The executors would be incentivized to throw out spam, since they would not earn any reward on these transactions later if they get included in the chain while censoring from executors could (probably) be prevented by randomly sampling the transactions from multiple executors.

---

**vbuterin** (2018-11-04):

Proposers are only re-sampled once every ~2 weeks, so they have plenty of time to reload the state of the new shard.

