---
source: ethresearch
topic_id: 12315
title: Simplified SSLE
author: vbuterin
date: "2022-04-04"
category: Consensus
tags: [single-secret-leader-election]
url: https://ethresear.ch/t/simplified-ssle/12315
views: 16257
likes: 13
posts_count: 8
---

# Simplified SSLE

This document describes a maximally simple version of single secret leader election (SSLE) that still offers good-enough diffusion of the likely next location of the proposer. It relies on [size-2 blind-and-swap](https://github.com/ethereum/research/blob/8bf89edc88c5abc6f0d68ea1f99b2d3d31553383/blind_and_swap/blind_and_swap.py) as a code primitive. Size-2 blind-and-swap proves that two output commitments `(OL1, OR1), (OL2, OR2)` are re-encryptions of two given input commitments `(IL1, IR1), (IL2, IR2)`, without revealing which is a re-encryption of which. The shuffle protocol uses a large number of these blind-and-swaps to shuffle a large number of commitments. Eventually one of these commitments is picked to be the proposer. The proposer would need to reveal themselves to “claim” this opportunity, but until the moment the block is published, no one knows who the proposer is; simply looking at the shuffle network would lead to hundreds of possible nodes that you need to take down in order to have even a 20% chance of taking down the next proposer.

## Parameters

| Parameter | Recommended value | Notes |
| --- | --- | --- |
| WIDTH | 2048 |  |
| SWAP_TREE_DEPTH | 5 | 2**depth - 1 swaps per slot |

## Construction

We maintain in the state an array of blinded commitments: `blinded_commitments: Vector[BlindedCommitment, WIDTH]`. We also add to the `Validator` struct extra fields that allow a “fresh” (ie. not yet mixed/blinded) `BlindedCommitment` for a given validator to be generated. We initialize the array with fresh commitments from a randomly picked set of validators.

During each slot, we use public randomness from the `randao_reveal` to pick three indices:

- proposer_blinded_index (satisfies 0  List[Pair[uint64, uint64]]:
    output = []
    for i in range(2**depth):
        L = (pivot + offset * i) % WIDTH
        R = (pivot + offset * (i + 2**depth)) % WIDTH
        output.append((L, R))
    return output

def get_swap_positions(state: BeaconState) -> List[Pair[uint64, uint64]]:
    output = []
    for depth in range(SWAP_TREE_DEPTH):
        randao_at_depth = get_randao(state, state.slot - depth - 1)
        proposer_blinded_index = randao_at_depth[:8] % WIDTH
        shuffle_offset = randao_at_depth[8:16] % (WIDTH//2) * 2 + 1
        output.extend(get_swap_positions_at_depth(proposer_blinded_index, shuffle_offset, depth))
    return output
```

### Code specification of verify_and_execute_swaps

```python
def verify_and_execute_swaps(state: BeaconState, swaps: List[Swap]) -> None:
    swap_positions = get_swap_positions(state)
    assert len(swaps) == len(swap_positions)
    for i in range(len(swaps)):
        swap, L, R = swaps[i], swap_positions[i][0], swap_positions[i][1]
        prev_L = state.blinded_commitments[L]
        prev_R = state.blinded_commitments[R]
        assert verify_blind_and_swap_proof(prev_L, prev_R, swap.next_L, swap.next_R, swap.proof)
        state.blinded_commitments[L] = prev_L
        state.blinded_commitments[R] = prev_R
```

Note that `get_swap_positions` may create swaps that overlap with each other. For this reason, it’s important to implement `verify_and_execute_swaps` as above, executing the swaps from first to last in order.

## Simulation results

There is a script [here](https://github.com/ethereum/research/blob/8bf89edc88c5abc6f0d68ea1f99b2d3d31553383/blind_and_swap/swapsim2.py) that can run many rounds of the shuffle tree mechanism, and outputs the *20%-diffusion* of the proposer location. This refers to the number of validators that an attacker would need to take offline (eg. with a targeted DoS attack) to have a 20% chance of taking down the proposer.

Here are some results. The values are given in pairs, where the left value is the average 20%-diffusion and the right value is the probability that the 20%-diffusion equals 1 (meaning that you only need to take down one validator to have more than a 20% chance of taking down the proposer).

|  | Swaps = 7 | 15 | 31 | 63 |
| --- | --- | --- | --- | --- |
| Width = 32 | (2.66, 0.20) | (4.43, 0.12) | (5.07, 0.036) | - |
| 64 | (3.02, 0.118) | (7.08, 0.102) | (9.53, 0.040) | (9.79, 0.028) |
| 128 | (3.13, 0.044) | (10.3, 0.056) | (18.8, 0.024) | (20.0, 0.020) |
| 256 | (3.13, 0.012) | (13.72, 0.046) | (36.0, 0.018) | (42.8, 0.022) |
| 512 | (3.02, 0.014) | (17.26, 0.01) | (65.31, 0.008) | (89.7, 0.004) |
| 1024 | (3.03, 0.009) | (19.23, 0.005) | (114, 0.004) | (177, 0.006) |
| 2048 | (2.98, 0.006) | (20.80, 0.005) | (194, 0.004) | (347, 0.004) |

The cost to increasing the `WIDTH` is relatively low; the main downside of an *extremely* large buffer is that it increases the chance of a missing proposer because by the time a validator is selected they have already left the validator set. Assuming a withdrawal time of 8192 slots (~1 day), this implies **a maximum “reasonably safe” buffer width of around 1024-2048** (2048 would ensure that if a validator exits immediately after being added to the buffer, they would only get a wasted post-exit proposal opportunity less than 2% of the time). 31 swaps seems to be the minimum required to get a large amount of diffusion, and 63 swaps gives *near-perfect* diffusion: the 20%-diffusion set is close to 20% of the `WIDTH`, which is what you would get if you just shuffled the entire buffer in each slot.

Each `Swap` in the `BeaconBlock` takes up 7 elliptic curve points (2x `BlindedCommitment` + 3 curve points in the proof), so 336 bytes. Hence, 31 swaps would take up 10416 bytes. Switching to a 32-byte curve would reduce this to 224 * 31 = 6944 bytes. Verifying a blind-and-swap takes 4 elliptic curve multiplications and 3 size-4 linear combinations. A size-4 linear combination is ~2x more expensive than a multiplication, so this is equivalent to ~10 elliptic curve multiplications. Hence, the total verification complexity is ~310 elliptic curve multiplications (~31 milliseconds).

These facts together drive the choice of `WIDTH = 2048` and `SWAP_TREE_DEPTH = 5` (31 swaps per block).

## Replies

**qizhou** (2022-04-06):

Very interesting idea.  I am still reading and understanding it, but I feel that it should have a wider applications to different consensuses.  I have come up with some questions about the idea, but have more later:

- Any reference document of 1-of-2 Schnorr signature scheme in size-2 blind-and-swap?  Looks like it differs from the one I found from the Internet.
- How to determine factor in size-2 blind-and-swap?  Or it could be a random secret from [1.. p-1], where p is the curve order.
- When swapping two commitments c0, c1 to c2, c3 with a random factor, how would the validator with the secret of one of the commitments know c2 or c3 is the new commitment of the validator?  My understanding is that factor is only known to the swapping validator.
- For proposer_blinded_index, fresh_validator_index, shuffle_offset, could we generate them just using a psudo-random-number generator like H(slot_index || salt)?

---

**vbuterin** (2022-04-06):

> Any reference document of 1-of-2 Schnorr signature scheme in size-2 blind-and-swap? Looks like it differs from the one I found from the Internet.

The signature here has to be a 1-of-2 *ring signature*, so it does not reveal which of the two keys signed.

> How to determine factor in size-2 blind-and-swap? Or it could be a random secret from [1.. p-1], where p is the curve order.

It’s just a random secret.

> When swapping two commitments c0, c1 to c2, c3 with a random factor, how would the validator with the secret of one of the commitments know c2 or c3 is the new commitment of the validator? My understanding is that factor is only known to the swapping validator.

The validator who knows their secret `x` would have to walk through every commitment in the buffer and check if `left * x = right`. Whichever commitment that check passes for is their commitment.

> could we generate them just using a psudo-random-number generator like H(slot_index || salt) ?

I think using the RANDAO is better because it makes proposal responsibilities more reliably unpredictable. We do want to minimize how far in advance you know that you will be the next proposer.

---

**qizhou** (2022-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The validator who knows their secret x would have to walk through every commitment in the buffer and check if left * x = right. Whichever commitment that check passes for is their commitment.

Thanks for the explanation.  I have revised the code a bit to explain this part.   Please check [add secret check for blinded-commitment by qizhou · Pull Request #126 · ethereum/research · GitHub](https://github.com/ethereum/research/pull/126).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think using the RANDAO is better because it makes proposal responsibilities more reliably unpredictable. We do want to minimize how far in advance you know that you will be the next proposer.

I understand RANDAO is better but just curious in the PRNG case, how safe it may be since PRNG is much easier to implement.

---

**asn** (2022-04-06):

Hey! Really sweet proposal!

I like the simplicity and I think the numbers are pretty good as well (and could potentially get even better). I also like the overhead balance of the `width=2048` and `swaps=31` combo.

Some thoughts on the scheme:

#### Anonymity set analysis

While the numbers on the `Simulation Results` table look reasonable, we should also take into account the potential for malicious and offline validators, as well as the fact that the total number of validators [corresponds to a smaller number of P2P nodes](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763#anonymity-set-16).

I hence [modded your simulation script](https://github.com/asn-d6/research/tree/simplified_ssle_offline_vals) to support offline validators: I’m attaching a table (like yours above) but just for the `width=2048/swaps=31` configuration with various percentages of offline shufflers, while also estimating the number of nodes that correspond to that anonymity set ([using a 20%-80% Pareto distribution](https://gist.github.com/asn-d6/1d972421667a23a0635f65cd5d12d0e7)).

|  | Validators | Nodes |
| --- | --- | --- |
| Offline == 0% | 193 | 130 |
| Offline == 5% | 180 | 122 |
| Offline == 10% | 169 | 116 |
| Offline == 15% | 156 | 109 |
| Offline == 20% | 149 | 104 |
| Offline == 25% | 139 | 98 |
| Offline == 30% | 138 | 98 |
| Offline == 35% | 133 | 95 |
| Offline == 40% | 128 | 91 |

From the above we see that even with significant offline percentages, there is still some anonymity set provided by this scheme

#### Strengthening the scheme using a shuffle list

If the anonymity set provided by this scheme is not satisfactory to us, we can strengthen it by separating the list that gets shuffled and the list where proposers get chosen from. That brings us slightly [closer to the Whisk design](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/), without Whisk’s cryptography.

For example, we would still use `blinded_commitments` for shuffling, but after 2048 slots have passed we would copy `blinded_commitments` into another list `shuffled_commitments` and we would pop proposers out of  `shuffled_commitments` (either FIFO or randomized).

This approach allows the maximum amount of shuffles to go through before any index gets chosen as the proposer, and [based on some sloppy analysis](https://github.com/asn-d6/research/commit/b585a6d9ba24bba81b248cd7f18fa24e6f71292c) it quickly converges to optimal results for any reasonable width/swaps combo.

The drawback is that we will need consensus code that [moves the commitments between the two lists](https://github.com/ethereum/consensus-specs/blob/d11245a8bfede151613014cd00c6fff66618c49e/specs/whisk/beacon-chain.md#epoch-processing), and we will also need double the `BeaconState` space.

#### Adversarial analysis

The next step in the security analysis here would be to think of what kind of attacks an adversary could pull off in this setup.

For example, if an adversary controls 10% of the validators, not only she controls 10% of the shuffles, but she can also void another 10% of the shuffles since any 2-shuffle that includes the attacker’s commitment is basically transparent to the attacker (she knows where her token went, and hence also the other token).

I’m also curious about backtracking attacks: When Alice proposes, the adversary immediately learns some paths of her shuffle-tree; since there is only a limited number of 2-shuffle paths that her token could have taken to end up where it did. An adversary could potentially use that knowledge to get bits of information about other future proposers.

There is also various types of RANDAO attacks that could happen in `get_swap_positions()`.

---

Cheers!

---

**dankrad** (2022-04-08):

Looking at the swap proof using Schnorr Ring signatures, I think there may be a problem in the current implementation: Namely, if an attacker knows `A1`, `A2`, `B1` and `B2` with respect to a generator `G`, then they can compute the ring signature for any new commitment – which includes completely new commitments, so they could “swap in and out” their own validators, for example.

I think this cannot happen as long as at least one of the elements is not known with respect to the same basis `G`, so we can prevent this by adding another “random” generator with unknown logarithm with respect to `G` to to the ring signature basis prevent it.

---

**asn** (2022-07-12):

Just mentioning for completeness that this proposal has been further analyzed by Dmitry Khovratovich in the following ethresearch post: [Analysis of Swap-or-Not SSLE proposal](https://ethresear.ch/t/analysis-of-swap-or-not-ssle-proposal/12700)

---

**Sh4d0wBlade** (2023-01-19):

Do these two arguments suppose to be swap.next_L and swap.next_R?

[![image](https://ethresear.ch/uploads/default/optimized/2X/a/a9b66be44c8708cf7de0c721f7582fd7999c1138_2_690x235.png)image1215×414 55.2 KB](https://ethresear.ch/uploads/default/a9b66be44c8708cf7de0c721f7582fd7999c1138)

