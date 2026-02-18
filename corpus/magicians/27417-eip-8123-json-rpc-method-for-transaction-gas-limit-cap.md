---
source: magicians
topic_id: 27417
title: "EIP-8123: JSON-RPC Method for Transaction Gas Limit Cap"
author: PaulRBerg
date: "2026-01-11"
category: EIPs > EIPs interfaces
tags: []
url: https://ethereum-magicians.org/t/eip-8123-json-rpc-method-for-transaction-gas-limit-cap/27417
views: 141
likes: 4
posts_count: 4
---

# EIP-8123: JSON-RPC Method for Transaction Gas Limit Cap

Discussion topic for EIP-8123

EIP-8123 introduces a new JSON-RPC method called `eth_txLimitGasCap` for querying the EIP-7825 tx gas limit cap. See the full EIP details in the GitHub PR:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/11061)














####


      `master` ← `PaulRBerg:json-rpc-tx-gas-limit-cap`




          opened 12:30PM - 11 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/8782666?v=4)
            PaulRBerg](https://github.com/PaulRBerg)



          [+135
            -0](https://github.com/ethereum/EIPs/pull/11061/files)







Discussions in https://ethereum-magicians.org/t/eip-8123-json-rpc-method-for-tra[…](https://github.com/ethereum/EIPs/pull/11061)nsaction-gas-limit-cap/27417












#### Update Log

- 2026-01-11: initial draft

#### External Reviews

None as of 2026-01-11.

#### Outstanding Issues

None as of 2026-01-11.

## Replies

**dicethedev** (2026-01-13):

Great proposal! Quick question about implementation: should clients return the

cap even if EIP-7825 isn’t active yet on that chain, or should they return null

until the fork activates? Also curious how this would work for chains that

haven’t implemented 7825 at all.

---

**PaulRBerg** (2026-01-13):

Thanks [@dicethedev](/u/dicethedev)! If EIP-7825 isn’t active, the chain should return `null`, indeed. With one exception - even if the chain hasn’t upgraded to Fusaka yet, if they enforce a custom policy for tx gas limits, they should return that value. For example, Base enforces a [25M cap](https://docs.base.org/base-chain/network-information/block-building?utm_source=chatgpt.com#per-transaction-gas-maximum)today (and they haven’t upgraded to Fusaka yet).

I wrote a piece of pseudocode in the EIP on GitHub, cross-sharing here for visibility:

```plaintext
if protocol has finite tx gas cap at head:
  protocolCap = that value
else:
  protocolCap = +infinity

if protocol has policy cap:
  policyCap = that value
else:
  policyCap = +infinity

cap = min(protocolCap, policyCap)

if cap is finite:
  return cap
else:
  return null
```

---

**dicethedev** (2026-01-13):

[@PaulRBerg](/u/paulrberg)  Got it, thanks! So policy caps take precedence when stricter than protocol caps, and null only when there’s truly no limit. The Base example makes it clear. Looking forward to this being adopted!

