---
source: magicians
topic_id: 23019
title: BLS12-381 Pairing Consensus Issue
author: MariusVanDerWijden
date: "2025-02-28"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/bls12-381-pairing-consensus-issue/23019
views: 1001
likes: 10
posts_count: 1
---

# BLS12-381 Pairing Consensus Issue

# Incident Response

Yesterday 27 Feb. 2025 , during the Pectra issues happening on Holesky,

EF security got a bug report at ~3:45pm CET via the [Pectra Audit Competition](https://cantina.xyz/competitions/pectra) which described a consensus issue between Geth and Nethermind when calling the BLS12-381 Pairing precompile. Magicians thread for EIP-2537 [here](https://ethereum-magicians.org/t/eip-2537-bls12-precompile-discussion-thread/4187/61).

Because I was attending a funeral, I could only start looking into the issue at 4:40pm CET and quickly confirmed that geth might be deviating from the specification described in [EIP-2537](https://eips.ethereum.org/EIPS/eip-2537).

The bug report contained three test cases that showed the issue. Nethermind quickly confirmed that they were passing all three test cases, while geth only passed the first one, thus confirming the consensus issue at 5pm CET, shoutout to Luk from Nethermind for responding so quickly.

All other client teams were quickly informed about the ongoing incident and a group was assembled with Antonio, Gotti, Justin and Kev from the EF cryptography and research teams.

After discussion with the cryptography team, we came to the conclusion at ~5:45pm that the specification is misleading and the spec and the Nethermind implementation should be changed.

The EEST (testing) team meanwhile prepared test vectors to confirm that no other client than Nethermind was affected.

In parallel to these discussions an impact analysis was done to confirm that no L2s or Ethereum forks were already running the BLS precompiles. At 5:50pm we confirmed that the issue was not live on any other network than Holesky.

At 5:50pm CET Nethermind also published their [fix](https://github.com/NethermindEth/nethermind/pull/8277).

At 6:30pm Pawel from the Ypsilon team notified us that this edge case can also happen on the BN256 pairing precompile, but fortunately we had test vectors in `ethereum/tests` that covered that edge case for the BN curve.

In the aftermath more tests were added to [ethereum/bls12-381](https://github.com/ethereum/bls12-381-tests/pull/14), [evmone](https://github.com/ethereum/evmone/pull/1148/files), [the EIP](https://github.com/ethereum/EIPs/pull/9425/files), [EEST](https://github.com/ethereum/execution-spec-tests/pull/1275) and Nethermind cut a [new release](https://github.com/NethermindEth/nethermind/releases/tag/1.31.2).

And finally the misleading sentence was [removed from the EIP](https://github.com/ethereum/EIPs/commit/437d026460d5c6d4f6159533efde6926b72dd324).

Overall it took one hour and ten minutes from when we first confirmed the issue until the fix was implemented and shipped in a client.

Big thanks to everyone who was involved in helping to triage, debug, confirm and fix this issue!

If you are running Nethermind on Holesky, please update to [version v1.31.2](https://github.com/NethermindEth/nethermind/releases/tag/1.31.2).

# Root cause analysis

The BLS12-381 pairing check precompile does the following:

On an input of list of points `{P,Q} ∈ G1 x G2`

it computes the equation `e(P1, Q1) * e(P2, Q2) * ... * e(Pk, Qk) == 1`.

The precompile outputs 1 if the equation holds and 0 otherwise.

The specification for the EIP stated:

```auto
Note:

If any input is the infinity point, pairing result will be 1.
Protocols may want to check and reject infinity points prior to calling the precompile.
```

This explanation can be interpreted in two different ways:

If a pair `{P, Q}` where either `P` or `Q` is infinity on their respective curves, either

(1) the pair may be ignored, but the multi-pairing should be computed¹

(2) the precompile should return 1 and the multi-pairing should not be computed

We confirmed later that the original author intended (1). The note was added to make smart contract developers aware that some use cases of pairing checks such as signature verification may require the caller to check that none of the inputs is the point at infinity prior to calling this ABI. The misleading sentence was later [removed](https://github.com/ethereum/EIPs/commit/437d026460d5c6d4f6159533efde6926b72dd324).

¹ Since `e(P, Q)` will always be 1, thus eliminating `e(P, Q)` from `e(P, Q) * ... * e(Pk, Qk) == 1` will result in `1 * .... * e(Pk, Qk) == 1` which is equivalent.
