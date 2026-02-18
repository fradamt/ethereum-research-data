---
source: ethresearch
topic_id: 11294
title: Casper FFG with backoff
author: vbuterin
date: "2021-11-18"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/casper-ffg-with-backoff/11294
views: 3219
likes: 4
posts_count: 4
---

# Casper FFG with backoff

### Goal

Preserve the Casper FFG safety and liveness invariants, but allow the distance between consecutive epochs that we attempt to justify to increase to accommodate latency. For example, if epochs 100 and 101 fail to justify, the chain could attempt to justify epochs 102, 104, 108… increasing the spacing so that two consecutive attempted epochs could still succeed and give us finality even under multi-epoch latency.

The challenge arises because different competing chains could have different attempted epochs, causing naive Casper FFG to fail:

[![](https://ethresear.ch/uploads/default/original/2X/9/9974f4f76dad24c0832528a20b2583ad311e7939.png)471×338 13.9 KB](https://ethresear.ch/uploads/default/9974f4f76dad24c0832528a20b2583ad311e7939)

### Rules

Each attestation has three epoch parameters:

- SOURCE: source (epoch and blockhash), same as in FFG
- TARGET: target (epoch and blockhash), same as in FFG
- PREV_TARGET_EPOCH: the eligible epoch before the target epoch in the chain

We have two slashing rules:

- Surround slashing: A1.source_epoch  P and A -> Z
- N.epoch = A.epoch - 1: double vote slash between N -> P and Z -> W
- N.epoch  N and A -> Z

Now, let’s extend this argument to this new version of Casper FFG. The new difference here is that `Z.epoch = A.epoch - 1` is not assured, which is why the counterexample in the diagram above becomes possible. But now we added a new rule: if a supermajority link `A -> Z` is possible, then a valid attestation for `A` must specify `Z.epoch` as its `prev_target_epoch`, and so the attester precludes themselves from using any epoch in `[Z.epoch + 1 ... A.epoch]` as the target in another attestation. Hence, the three cases become:

- Z.epoch  P and A -> Z
- N.epoch = Z.epoch: double vote slash between N -> P and Z -> W
- N.epoch  N and A -> Z

### Liveness argument

The liveness argument is the same as the liveness argument for naive Casper FFG. Eventually the chain reaches an epoch `e` that exceeds all epoch numbers used by all previous attestations. Let `J` be the highest-epoch justified block. Let `M` be a descendant of `J` where `M.epoch = e`. There are no intersection or surround violations from attesting `M -> J`, and then no violations from attesting `N -> M` where `N` directly follows `M`, allowing finalization.

## Replies

**ittaia** (2021-11-20):

Hi Vitalik,

I have a vague feeling we discussed this back in 2018ish. In any case, I am not sure I fully follow your notation so apologies in advance for my misunderstandings.

We now have two types of edges:

1. classic edges (as in classic Casper FFG that don’t set the PREV_TARGET_EPOCH).
2. strong edges (that set the PREV_TARGET_EPOCH).

Define any length one edge as strong.

**Finalization**: you need n-f (or 2/3 in your notation) strong edges for finalization (a length one edge is considered strong so this includes the classic finalization rule).

I’ll call this a *relaxed* rule, several protocols have adopted variants of this approach.

**Attestation**: say you are in epoch A and the most recent justified block (lock) you see is in epoch B:

1. if for every epoch between B and A, you either did not attest or the justified source block you attested for is B, then attest to a strong edge A \Rightarrow B.
2. otherwise (there is an epoch between B and A, say K for which B was not the highest justified you saw at epoch K, in particular, you attested at target epoch K to a source justified block that is < B), then attest to a classic edge A \rightarrow B. (Note that if you do attest a strong edge, then you will get yourself slashed due to target K intersection slashing).

Note that in your argument for liveness, if J is the highest justified, it could still be the case that I did not see J but did see K<J and I attested an edge H \rightarrow K (with J<H). So now I cannot attest to a strong edge M \Rightarrow J because K is a target between M and J. So I can only attest to a classic edge M \rightarrow J. Indeed I did not see block J at epoch J but only sometime after epoch H. As you wrote this is fine because N \Rightarrow M will finalize.

---

**vbuterin** (2021-11-22):

> if you saw B later than epoch B, then send a classic edge attestation A

I think this won’t quite work because an explicit goal of this design is to be able to adapt to very high (>1 epoch) temporary latency. Or am I misunderstanding what you mean by “if you saw B later than epoch B”?

---

**ittaia** (2021-11-23):

I made the definition of when to use a classic edge more precise (assuming I am not misunderstanding your notation). It basically says if you may get slashed from attesting a strong edge, then (obviously) attest to a classic edge instead.

Indeed, using a classic edge will not give you the ability to quickly finalize (when blocks are not consecutive), but you may need to have that option otherwise you may not be live.

> There are no intersection or surround violations from attesting M -> J

Note that your liveness agreement shows a concrete example where you may want to use classic edge. This is in case that you already attested an edge H \rightarrow K (or H \Rightarrow K) with J<H<M and K<J. If you must attest a strong edge for M \Rightarrow J then you will slash yourself (because H is a target in the intersection). If you attest a classic edge M \rightarrow J in this case then liveness will be okay and you can finalize in N \Rightarrow M (say of length one).

