---
source: magicians
topic_id: 3302
title: eth_estimateGas and block parameter
author: ligi
date: "2019-05-20"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eth-estimategas-and-block-parameter/3302
views: 1041
likes: 0
posts_count: 2
---

# eth_estimateGas and block parameter

Does anyone have use-case for the block parameter in eth_estimateGas? I just stumbled over an ancient (2016) bug [internal/ethapi: eth_estimateGas should take block number · Issue #2586 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/issues/2586) and not sure yet if it should be changed in the documentation/spec or in geth. But I think we should do something about it to remove this stumbling block.

Also as [@karalabe](/u/karalabe) just pointed out - the documentation is also inconsistent in this regard - this section does not mention estimateGas:


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [GitHub](https://github.com/ethereum/wiki/wiki/JSON-RPC#the-default-block-parameter)



    ![image](https://opengraph.githubassets.com/e8c60b2ee67365b72e3fe574db5923fae70794ae6ee2441f59aafdc7769f94da/ethereum/wiki)

###



The Ethereum Wiki. Contribute to ethereum/wiki development by creating an account on GitHub.

## Replies

**ligi** (2019-05-22):

use-case is found - but in the end the rpc-spec should still be changed to allow also a blockhash and not only a number:

https://github.com/ethereum/go-ethereum/issues/2586#issuecomment-494762902

