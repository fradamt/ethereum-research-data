---
source: ethresearch
topic_id: 7459
title: "Distaff VM: now with DEEP-FRI"
author: bobbinth
date: "2020-05-23"
category: zk-s[nt]arks
tags: [library]
url: https://ethresear.ch/t/distaff-vm-now-with-deep-fri/7459
views: 2652
likes: 1
posts_count: 8
---

# Distaff VM: now with DEEP-FRI

I have just released a new version of [Distaff VM](https://github.com/GuildOfWeavers/distaff) (for more info see [Introducing Distaff: a STARK-based VM written in Rust](https://ethresear.ch/t/introducing-distaff-a-stark-based-vm-written-in-rust/7318)). The major changes are primarily under the hood. Specifically:

- I’m now using DEEP-FRI methodology for low-degree testing. This had significant impact on proof size (see below).
- Proof “grinding” is now supported. This allows adding extra security while keeping proof size the same (or reducing proof size for the same security) at the expense of increasing proof generation time.
- The primary field for the VM is now a 128-bit prime field. This is about 2x slower than the 64-bit field I used before (and also has higher RAM requirements) - but it comes with better soundness and also has some other future benefits.

### Performance

Similar to the previous post, I benchmarked a simple [Fibonacci calculator](https://github.com/GuildOfWeavers/distaff#fibonacci-calculator) program on the new implementation. The machine is also the same: Intel Core i5-7300U @ 2.60GHz (single thread) with 8 GB of RAM. But unlike in the previous version, the proofs now target 120-bits of security.

| Operation count | Execution time | Execution RAM | Verification time | Proof Size |
| --- | --- | --- | --- | --- |
| 210 | 260 ms | negligible | 2 ms | 76 KB |
| 214 | 2.7 sec | 160 MB | 3 ms | 127 KB |
| 218 | 48 sec | 4.4 GB | 3 ms | 189 KB |

The parameters I used for the proof are as follows:

- Extension (or blow-up) factor: 32
- Number of queries: 50
- Grinding bits: 20

As I mentioned above, it is possible to adjust these parameters in ways that reduce proof size while increase proof time and vice-versa. The table below demonstrates this trade-off on the example of a program with 214 operations from above.

| Security | 3 sec | 5 sec | 9 sec | 18 sec |
| --- | --- | --- | --- | --- |
| 100 bits | 111 KB | 87 KB | 71 KB | 65 KB |
| 120 bits | 128 KB | 97 KB | 84 KB | 76 KB |

Basically, to get a proof at 120-bit security level, you can spend 3 seconds and get a proof size of 128 KB, or you could spend 18 seconds, and the resulting proof size will be 76 KB.

A note on proof times: these times are for a relatively un-optimized implementation running in a single thread. I’d expect that for a heavily-optimized multi-threaded implementation on an 8-core processor, the 18 second proof time will go down to about 1 second.

### 128-bit field

As mentioned above, switching to a 128-bit field has non-negligible negative performance impact. The proof times increase by over 2x and RAM requirements also almost double.

The primary reason for switching over is that getting sufficient bits of security from a 64-bit field is non-trivial, and currently I don’t know how to get 120 (or even 100) bits of security in a 64-bit field. I know that it’s possible though, and it might make sense to switch back to a 64-bit field in the future.

But, 128-bit field also has a couple other benefits:

- It is much easier to construct elliptic curves over a quadratic extension of 128-bit prime fields (e.g. see Microsoft’s  FourQ curve). This means Distaff VM could support elliptic curve operations in the future (though, unfortunately, FourQ curve won’t work).
- Since we now work with 128-bit values, the instruction set for the VM could be a bit more compact and the stack wouldn’t need to grow as much for things like hashing and Merkle proof verification.

### Distaff VM under the hood

I’ve started working on a description of how Distaff VM works under the hood. The primary description is [here](https://github.com/GuildOfWeavers/distaff/tree/master/src/stark) (you might need to refresh the page for math formulas to show up in Github). So far, it focuses on my implementation of STARKs. Any feedback is greatly appreciated!

## Replies

**vbuterin** (2020-05-24):

Great work!

I think your 100-bit numbers are *technically* needlessly over-conservative because you could just truncate your hashes to 25 bytes and so get ~17% savings from that in addition to the savings from reducing query count.

> currently I don’t know how to get 120 (or even 100) bits of security in a 64-bit field

Don’t you just do this by taking multiple samples? In the FRI you would presumably pick two columns, and then continue the next round with a random linear combination of those columns.

---

**bobbinth** (2020-05-24):

Thank you!

Regarding truncating hashes: good point! I didn’t think of this.

Regarding 64-bit fields: my understanding is that as long as size of the prime field is much larger than the evaluation domain, you can estimate FRI soundness as \rho^m, where \rho is the coding rate and m is the number of queries. But, this “much larger” means q > n^4, where q is the size of the field, and n is the size of the evaluation domain.

So, for 64-bit fields this is quite limiting - there aren’t many useful things you can do in evaluation domain with size 2^{16}.

When q > n^4 doesn’t hold, other factors come into play and the number of queries needed to achieve given soundness probably increases (though, I don’t know by how much). I asked Eli, and he recommended to stay with 128-bit fields for now. But I know they are planning to release a paper which will address this topic in the near future.

---

**vbuterin** (2020-05-24):

By the way, do you know if there has been any work on determining if using half-sized hashes (16 bytes for 128-bit security) for STARKs is ok? Intuitively, it feels like being able to generate Merkle trees where some leaves can be opened to two positions (but you still can’t do second-preimage attacks) doesn’t give an attacker *that* much extra degrees of freedom. And it seems like half-sizing hashes would be a very significant size decrease to a STARK.

---

**bobbinth** (2020-05-25):

I’m not aware of any such work - but yeah, if it doesn’t compromise security, it would be very significant for STARKs.

---

**pvienhage** (2020-05-26):

[@vbuterin](/u/vbuterin) are you suggesting that the half sized hash tree would allow doing less query de-commitments because you reveal more points on the reed Solomon encoded polynomial or that the smaller hash sizes reduce the size of the merkle de-commitments because each de-commitment gets smaller? If it’s the second one we have implemented this technique and masked each of our hashes by ~10 bytes and it does help quite a bit with proof size. I’m not sure that the increased efficiency of half sized hashes would be worth it over 20 byte hashes. Also, I would be concerned about the suggestion that pair revealing would reduce the number of overall decommitments because the predictability of the pair commitment structure may mean attackers would commit pairs which are near the same polynomial [in terms of reed soloman encoding distance]. If they did that then each pair revealed may only contribute as much to the proof as a single point in a non-pair de-commitment strategy.

---

**bobbinth** (2020-05-27):

[@pvienhage](/u/pvienhage) Quick question: does masking hashes by 10 bytes mean that you use 22 byte hashes? If so, what security level are you targeting with these?

---

**pvienhage** (2020-05-28):

The hash function is a masked keccak, we take the last 20 bytes of a normal keccak hash of the inputs and use that as the internal hash of our merkle trees. Our security target varies based on application but in general we shoot for 120 bits and the loss of security in the masked hashes is within the conservative range to achieve 120 bits for the whole system.

