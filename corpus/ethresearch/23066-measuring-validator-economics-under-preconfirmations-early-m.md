---
source: ethresearch
topic_id: 23066
title: "Measuring Validator Economics Under Preconfirmations: Early Mainnet Evidence"
author: murat
date: "2025-09-15"
category: Economics
tags: [mev, preconfirmations]
url: https://ethresear.ch/t/measuring-validator-economics-under-preconfirmations-early-mainnet-evidence/23066
views: 383
likes: 4
posts_count: 1
---

# Measuring Validator Economics Under Preconfirmations: Early Mainnet Evidence

**Context**

We stitched together the **first mainnet view** that compares block mev rewards across large operators (Kiln, Everstake, Network) and smaller preconfirmation cohorts (Primev validators, Kiln‑Primev, and Kiln‑EthGas cross‑cuts).

The goal: find out **whether preconfirmations are already adding value** to the **typical** validator block and what to do next.

**TL;DR**

- On typical blocks (75th percentile), mev-commit was observed to deliver blocks with higher value than Kiln validators when the two are directly compared.
- The Kiln‑Primev source shows the highest typical value across comparable sources; consistent with 8,090 preconfirmations settled in August.
- Big datasets tend to have higher averages not because their baseline is better, but because more blocks = more chances at rare, very big blocks. We show this with std dev and variance comparisons across data sets.
- August 2025 is the core focus as it’s the most recent full month with wide relay/builder adoption and release of FAST RPC, though Aug 20 ATH (11.33% of mainnet blocks had mev-commit preconfs) could not be depicted due to lack of data from comparable sources on that day
- What it means: We observe that blocks opted in to mev-commit are already tracking network‑wide mev and adding value on typical blocks. To make this statistically conclusive, we need more validators opted in and more data shared from operators and protocols.

---

Special thanks to **Kiln** and **Everstake** for sharing operator data.

## Background

Primev has developed mev-commit, a credible commitment protocol used for preconfirmations (preconfs) and other novel types of mev, featuring a high performance encrypted mempool and the only live solution to [the fair exchange problem.](https://ethresear.ch/t/preconfirmation-fair-exchange/21891#p-53230-mev-commit-15) The protocol works by [leveraging a leaderless auction for preconfirmations among blockbuilders](https://docs.primev.xyz/v1.2.x/concepts/what-is-mev-commit), and uses validator opt-ins backed by stake to add credibility to commitments. It has [a hybrid model between blockbuilders and validators](https://mirror.xyz/preconf.eth/sgcuSbd1jgaRXj9odSJW-_OlWIg6jcDREw1hUJnXtgI), allowing it to project preconfs into mainnet blocks even when the validator isn’t opted in.

Large validator operators are very sensitive to economic rewards for staking, and we’ve spent considerable efforts to ensure the network can deliver execution rewards equal to or greater than a standard validators’, ultimately increasing the security of Ethereum. Mev-commit has ~1% of Ethereum validators actively opted in on mainnet, has settled 18,000+ preconfs to-date, and [consistently delivers preconfs in milliseconds in over 5% of Ethereum blocks](https://www.mev-commit.xyz/) in a 24-hr span, with August 20th showing an all time high at 11.33% of mainnet blocks covered with at least 1 preconf. mev-commit is being progressively decentralized.

[![11.33% preconf coverage ATH on Aug 20th](https://ethresear.ch/uploads/default/optimized/3X/a/c/acab679e8ba331f8c620395a024768a359558284_2_690x331.png)11.33% preconf coverage ATH on Aug 20th1307×627 59.2 KB](https://ethresear.ch/uploads/default/acab679e8ba331f8c620395a024768a359558284)

## The Story

### The Setup: a worrying first read

**What we heard first:** Preconfirmation cohorts had lower average execution rewards based on charts shared by Kiln. This was puzzling, so we asked for the underlying data and we quickly realized that it was comparing daily rewards but it was including days with 0 proposals and counting them as 0 rewards, thus significantly lowering cohort averages.

### Second read: compare like with like

We started aggregating this data with other sources, and only compared days where different sources **actually proposed blocks**. We depict Network as averages Ethereum wide, Kiln and Everstake as average across all respective operator validators, Primev as all validators opted into mev-commit, Kiln-Primev and Kiln-ethGAS as Kiln validators opted into the respective preconfirmation methods. The numbers began reflecting **rewards per opportunity**, not “opportunities you didn’t have”.

[![All Sources charted comparing large and small datasets](https://ethresear.ch/uploads/default/optimized/3X/3/3/33347289d14df6cf91ca57f8c60812b50ebab503_2_690x331.png)All Sources charted comparing large and small datasets1625×780 36.4 KB](https://ethresear.ch/uploads/default/33347289d14df6cf91ca57f8c60812b50ebab503)

[![line chart with daily data detail](https://ethresear.ch/uploads/default/optimized/3X/f/6/f617080fbb390e913c90100227944b8c40b35716_2_690x341.png)line chart with daily data detail1980×980 149 KB](https://ethresear.ch/uploads/default/f617080fbb390e913c90100227944b8c40b35716)

We did the same to observe Kiln sources only (Kiln, Kiln-Primev, Kiln-ethGAS), we started seeing interesting results:

[![Common days across Kiln sources only](https://ethresear.ch/uploads/default/optimized/3X/0/f/0f9396a219f667e361bd598da1d962e5179310cd_2_690x351.png)Common days across Kiln sources only2073×1057 91.9 KB](https://ethresear.ch/uploads/default/0f9396a219f667e361bd598da1d962e5179310cd)

While this was aligned closer with our expectations being aware of network activity in August, the sample size for the common day intersection of the 3 sources was still too small to derive statistically significant results, and Kiln could’ve had a bad luck of the draw for the common dates. To get as granular accuracy as possible and control for mev spikes, we intersected exact UTC hours across Kiln, Network, Primev, and Kiln‑Primev.

**What we learned:** Blocks with preconfs already mirror network‑wide mev surges, indicating validators maintain the same baseline exposure to mev rewards while opted in.

[![mev-commit blocks track the same spikes as the network.](https://ethresear.ch/uploads/default/optimized/3X/3/9/390e0430e29097be849032387602383b916b7f17_2_690x284.png)mev-commit blocks track the same spikes as the network.2379×980 195 KB](https://ethresear.ch/uploads/default/390e0430e29097be849032387602383b916b7f17)

But these charts still didn’t tell an accurate story on reward averages, as comparing samples with tens of thousands of data points (Kiln, Everstake, Network) exposed them to much higher rates of receiving outlier blocks, which greatly skew averages. When we only looked at Kiln and Kiln-Primev, we saw that Kiln-Primev blocks typically hovered higher, but Kiln’s large exposure to outlier blocks with 33,000+ blocks proposed heavily skewed its total average.

Typical Kiln-Primev blocks hovered above Kiln in value, but a single outlier skewed the average

[![kiln-primev typically hovers above, single outlier disrupts avg](https://ethresear.ch/uploads/default/optimized/3X/f/3/f340cdc04b98560ad61f6f17d877d4595bec6ed2_2_690x395.png)kiln-primev typically hovers above, single outlier disrupts avg1922×1101 132 KB](https://ethresear.ch/uploads/default/f340cdc04b98560ad61f6f17d877d4595bec6ed2)

When we removed the August 14 outlier from the Kiln set across its common days with Kiln-Primev, we saw a major difference in mev rewards for the typical block.

[![Results w/ outlier exclusion kiln v kiln-primev](https://ethresear.ch/uploads/default/optimized/3X/8/3/834e7baec94f12fa8021e196fd2221dad2d566a5_2_690x292.png)Results w/ outlier exclusion kiln v kiln-primev2127×903 53.6 KB](https://ethresear.ch/uploads/default/834e7baec94f12fa8021e196fd2221dad2d566a5)

To depict this statistically we computed the standard deviation and variance across them and observed a meaningful difference in datasets:

| Pair | Std Dev (ETH) | Variance (ETH²) | Read |
| --- | --- | --- | --- |
| Kiln | 0.1525 | 0.0233 | Bigger set → more rare big blocks |
| Kiln‑Primev | 0.0219 | 0.0005 | Smaller set → fewer rare big blocks |

[![stddev depicting discrepancies within datasets](https://ethresear.ch/uploads/default/optimized/3X/1/6/16e1c86b09c81cc377064142a7d7798e5c3c4dcc_2_690x271.png)stddev depicting discrepancies within datasets1979×780 73.3 KB](https://ethresear.ch/uploads/default/16e1c86b09c81cc377064142a7d7798e5c3c4dcc)

The Kiln-Primev source simply didn’t have enough chances at an outlier block reward with 17 data points in August.

---

### The Reveal: dial to typical blocks

Averages get pulled around by rare giant blocks. To ask, “What do I usually earn per block?” we looked at the 75th percentile (p75), the top end of typical blocks without outliers. We took the p75 sample for each source with common hours to see if there would be a difference. The results were drastically different:

[![kiln-primev-network common hours controlled for p75](https://ethresear.ch/uploads/default/optimized/3X/8/7/87b7391d1831da302d56c4b7a182ccf174fe6f90_2_690x350.png)kiln-primev-network common hours controlled for p751535×780 35.7 KB](https://ethresear.ch/uploads/default/87b7391d1831da302d56c4b7a182ccf174fe6f90)

This made sense given the 8090 preconfs settled in August, and Kiln-Primev blocks having a minimum of 1 extra transaction through mev-commit. However this is an indication and we still need more data to make the results statistically significant.

**Takeaway:** **1–2 preconfirmed txs per block** are already **adding to block value** in day‑to‑day conditions.

Based on the sample sizes, we estimate that Kiln gets an outlier block reward every ~300 blocks. The Kiln-Primev set should have about 300 records in a month (~624 keys) to match average calculations without normalization, and ~800 records (4000+ keys) to display a tight mean between Kiln and Kiln-Primev in a statistically significant manner to make the analysis conclusive.

---

### The Trend: three months in, lines are crossing

What the broader window shows (June–Aug):

- Kiln/Network trending down toward broader network parity (partly ETH‑USD price effects when mev is dollar valued).
- mev-commit trending up with network upgrades, coverage, and adoption, leading to more settled preconfs.
- Where we are now: mev-commit has effectively “caught up” to the network (see August 16th trend crossline) and should track broad patterns while keeping an incremental edge as preconfirmation coverage grows.

[![summer trend of mev rewards](https://ethresear.ch/uploads/default/optimized/3X/8/c/8c29e16b2a8210cdf63803db56953bc7bda2cc49_2_690x284.png)summer trend of mev rewards2379×980 173 KB](https://ethresear.ch/uploads/default/8c29e16b2a8210cdf63803db56953bc7bda2cc49)

---

## What this means for validators

- Expectation setting: If you opt in, your block’s reward pattern should look like the network’s, you’ll have exposure to the same mev waves.
- Day‑to‑day uplift: Preconfirmed txs (often 1–2 per block) are already showing additive value on typical blocks.
- Don’t chase averages blindly: Big operators’ higher means mainly reflect more chances at rare big blocks, not a guaranteed higher baseline per block.
- Design note: mev-commit’s leaderless auction means preconfs stack on top of existing block value; they don’t replace it.
- Outlook: As coverage expands in September and beyond, measurement should improve and the uplift from preconfs should stabilize.

---

## Data, scope, and guardrails

- Focus: August 2025 (most recent full month widespread RPC/relay/builder adoption).
- Fair comparisons:

Common days (drop “proposals = 0” days for small cohorts).
- Common hours (everyone sees the same hourly mev spikes).
- p75 (the top end of typical; filters out rare giants).

**Cross‑cuts included:** Kiln, Network, Everstake (large); Primev, Kiln‑Primev, Kiln‑EthGas (small).
**Subsidies:** Early‑August preconfirmation subsidies existed on mev-commit. Data indicates it was taken more by blockbuilders than passed to validators; across‑Ethereum builder subsidies are pseudo‑random at over 30 ETH/week and hard to attribute source‑by‑source. We analyze observed execution rewards as‑is.
**Not included:** Protocol rewards/points (e.g., mev‑commit points, Symbiotic, $eigen, $SSV, $Obol) could be **additional economic upside** not visible in the execution reward lens.

---

## In order to make results conclusive, we request:

- Validators:

Opt-in to mev-commit, increase economic upside and make Ethereum FAST.
- Share operator data (daily + hourly) so we can enrich the comparison set.

Preconfirmation methods:

- Publish or share timestamped per‑block rewards to allow more apples‑to‑apples comparisons.

Target sample sizes:

- 300–800 monthly records for preconfirmation methods → tight confidence and fair large block tail exposure vs large operators.

Thank you for reading, we’re excited to follow up in the coming months with a statistically conclusive analysis
