---
source: magicians
topic_id: 4332
title: EIP2666 (global precompiles repricing and many more) discussion thread
author: shamatar
date: "2020-06-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip2666-global-precompiles-repricing-and-many-more-discussion-thread/4332
views: 2366
likes: 1
posts_count: 2
---

# EIP2666 (global precompiles repricing and many more) discussion thread

This is a discussion thread for [EIP-2666](https://github.com/ethereum/EIPs/pull/2666).

## Replies

**shamatar** (2020-08-21):

Necessary benchmarks for EIP 2666 were provided by the clients and raw form is assembled in [here](https://docs.google.com/spreadsheets/d/1aCQnk7prrp3Mbcf011BE5zZnkbc3Iw7QAixn6mLbKS0/edit?usp=sharing)

Besu [benchmarks](https://gist.github.com/shemnon/0ddba91be501fa23291bdec9107fe99a)

Short summary:

- BNADD

|  |  | Gas |
| --- | --- | --- |
| Geth |  | 350 |
| OE |  | 225 |
| Besu |  | 165 |
| Nethermind |  | 120 |

BNADD cost will need to be adjusted when EIP 2046 is accepted

- BNMUL

|  |  | Gas |
| --- | --- | --- |
| Geth |  | 3000 |
| OE |  | 6250 |
| Besu |  | 19109 |
| Nethermind |  | 5250 |

Besu result is surprising (I was told that some Rust lib is used, and addition looks fast, but multiplication is very slow). Only little repricing will be necessary when EIP 2046 is accepted

- SHA256 precompile

Currently it’s 60 gas + 12 gas per 32 byte word. Proposed formula is `A * ((len(input) + 8) / 64 + 1) + B`, with coefficients below

|  |  | A | B |
| --- | --- | --- | --- |
| Geth |  | 5 | 3 |
| OE |  | 9 | 4 |
| Besu |  | 5 | 10 |
| Nethermind |  | 10 | 5 |

EIP 2666 proposes A = 9, B = 5. Besu implementation is Java built-in, so I doubt it can be improved, so it would be better to set A = 9, B = 10 that largely fits everyone. There are no large one-off costs in this precompile, so it’s EIP 2046 - safe.

- RIPEMD precompile

Currently it’s 600 gas + 120 gas per 32 byte word. Proposed formula is `A * ((len(input) + 8) / 64 + 1) + B`, with coefficients below

|  |  | A | B |
| --- | --- | --- | --- |
| Geth |  | 12 | 6 |
| OE |  | 8 | 2 |
| Besu |  | 29 | 16 |
| Nethermind |  | 10 | 6 |

EIP 2666 proposes A = 12, B = 6. There are no large one-off costs in this precompile, so it’s EIP 2046 - safe. Besu expects to have performance improvements by the end of the year

- Keccak256 performance

Currently it’s 30 gas + 6 gas per 32 byte word. Proposed formula is `A * (len(input) / 136 + 1) + B`, with coefficients below

|  |  | A | B |
| --- | --- | --- | --- |
| Geth |  | 13 | 13 |
| OE |  | 15 | 2 |
| Besu |  | 19 | 28 |
| Nethermind |  | 16 | 3 |

EIP 2666 proposes A = 15, B = 13. There are no large one-off costs in this precompile, so it’s EIP 2046 - safe. Besu expects to have performance improvements by the end of the year

