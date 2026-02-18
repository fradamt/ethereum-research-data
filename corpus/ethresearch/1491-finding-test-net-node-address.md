---
source: ethresearch
topic_id: 1491
title: Finding test net Node address
author: radedoc
date: "2018-03-24"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/finding-test-net-node-address/1491
views: 2120
likes: 3
posts_count: 11
---

# Finding test net Node address

Can someone please tell me the address of a reliable Casper Test Net node?  I am trying to connect to one and it appears that all the addresses I find online (including the one here https://hackmd.io/s/Hk6UiFU7z) are not working.

## Replies

**liangcc** (2018-03-25):

hi please try the following ones. Also note that we are doing some update to source code and will launch a new testnet soon.

```auto
"enode://bb017ea59f421392caae4694c96f0590d00a830e78b66dec9c83c814508a3e324f7a09aa7555009384f997a6b1b4726c3b48e7058c7da8fdddbbd599a71fe775@13.93.89.39:30313"
"enode://8d4a6aec3e340f9e859fd72ced95d2a0b49766772ac914810f6888bc2be5f95acf241aa94de8cd47a92dec1e8f96d86f4c052cc020e7c8e5438f6f18211dfeb1@54.226.126.100:30303"
"enode://8cae2ed1214f394ae36d8a737066572c2f45a01b13aca8cc9a42e4425c7d8f8a362674d1b34f9417840e584ddb00eccf7fe53af51f5d1a32c31aab74b6ed423e@34.224.156.160:30303"
```

---

**terry.rossi** (2018-03-25):

If I do not want to run a node but just want to query the casper contract, what IP/Port could I use as an argument to HTTPProvider() call in the “Just taking a look” portion of these instructions: http://notes.ethereum.org/MYEwhswJwMzAtADgCwEYBM9kAYBGJ4wBTETKdGZdXAVmRvUQDYg=?view

---

**radedoc** (2018-03-25):

Hi,  I tried all three addresses on different computers and I keep getting sync fail errors.  Is there something I am doing wrong?

---

**liangcc** (2018-03-26):

Hi, for HTTPProvider please try `curl 54.167.247.63:8545`.

But the pyethapp does not sync well, the service might not be stable.

---

**terry.rossi** (2018-03-26):

This port/IP seem to work, but I am getting an error when I call `casper.get_base_penalty_factor()`. Looks like the decimal type isn’t supported? Is there something I’m doing wrong, or is there some other way I can access this value?

---

**nate** (2018-03-26):

[@djrtwo](/u/djrtwo) any thoughts on if the issue w/ decimal type is what you ran into?

---

**djrtwo** (2018-03-26):

Web3.py does not currently support `decimal10` so yes, this will not work. Not sure if whoever wrote the instructions fully tested the web3.py support. Here is the issue in web3.py’s github.

Not sure if anyone is working on it currently. If you are inspired, drop a line in the issue and pick it up!



      [github.com/ethereum/web3.py](https://github.com/ethereum/web3.py/issues/700)












####



        opened 12:27AM - 16 Mar 18 UTC



          closed 04:57AM - 07 Aug 18 UTC



        [![](https://ethresear.ch/uploads/default/original/3X/e/5/e50d6fb17ee25ef48ab3aa15661970adc0b63671.png)
          djrtwo](https://github.com/djrtwo)










* Version: 4.0.0-beta
* Python: 2.7/3.4/3.5
* OS: osx/linux/win

### What […]()was wrong?
There is currently no support for vyper abi type `decimal10`. Although vyper is in alpha, it is increasingly used by ethereum research team for casper and sharding.

### How can it be fixed?
Add support for `decimal10` abi type :)

---

**liangcc** (2018-03-27):

[@terry.rossi](/u/terry.rossi) Sorry due to the lack of the `decimal10` type support, the `get_base_penalty_factor` is supposed to extracted from a synced node’s console.

```auto
>> from ethereum.tools import tester
>> casper = tester.ABIContract(tester.State(eth.chain.state), casper_abi, '0xbd832b0cd3291c39ef67691858f35c71dfb3bf21')
```

By the way, the `base_penalty_factor`, which is `0.0001`, is initialized [here](https://github.com/karlfloersch/pyethapp/blob/dev_env/pyethapp/eth_service.py#L171) with function signature [here](https://github.com/karlfloersch/pyethereum/blob/develop/ethereum/hybrid_casper/casper_utils.py#L24-L30), and is not changed after initialization.


      [github.com](https://github.com/karlfloersch/pyethereum/blob/develop/ethereum/hybrid_casper/casper_utils.py#L24-L30)




####

```py

1. def make_casper_genesis(alloc, epoch_length, withdrawal_delay, base_interest_factor, base_penalty_factor, genesis_declaration=None, db=None):
2. # The Casper-specific dynamic config declaration
3. config.casper_config['EPOCH_LENGTH'] = epoch_length
4. config.casper_config['WITHDRAWAL_DELAY'] = withdrawal_delay
5. config.casper_config['OWNER'] = a0
6. config.casper_config['BASE_INTEREST_FACTOR'] = base_interest_factor
7. config.casper_config['BASE_PENALTY_FACTOR'] = base_penalty_factor

```








In case you need some historical data, here is the dump I extracted recently


      [github.com](https://github.com/ChihChengLiang/testnet-data-dump/blob/master/data/epoch.json)




####

```json
{"number": 49, "blockhash": "267ad8155fbe6f71468be15a189df566b9003bd5a1ea09471db71a9fe1cdcb88", "timestamp": 1514711380, "difficulty": 8192, "current_epoch": 0, "validators": [{"addr": "0xebdd5b584fb0f1ad7d5da99fbc1153af11163683", "start_dynasty": 2, "end_dynasty": 1000000000000000000000000000000, "deposit": 5000.0}], "lje": 0, "lfe": 0, "votes": {"cur_deposits": 0.0, "prev_deposits": 0.0, "cur_votes": 0.0, "prev_votes": 0.0, "cur_vote_pct": 0, "prev_vote_pct": 0, "last_nonvoter_rescale": 0.0, "last_voter_rescale": 0.0}, "deposit_scale_factor": 10000000000.0, "storage": 18}
{"number": 99, "blockhash": "2a7c7c78a25d7ee6f258371cfbe115d0ff48adee96e26286b854f3fb717fcd72", "timestamp": 1514712465, "difficulty": 8216, "current_epoch": 1, "validators": [{"addr": "0xebdd5b584fb0f1ad7d5da99fbc1153af11163683", "start_dynasty": 2, "end_dynasty": 1000000000000000000000000000000, "deposit": 5000.0}], "lje": 0, "lfe": 0, "votes": {"cur_deposits": 0.0, "prev_deposits": 0.0, "cur_votes": 0.0, "prev_votes": 0.0, "cur_vote_pct": 0, "prev_vote_pct": 0, "last_nonvoter_rescale": 1.0, "last_voter_rescale": 1.0}, "deposit_scale_factor": 10000000000.0, "storage": 25}
{"number": 149, "blockhash": "bdccff6f1ea9e824e2c2742fed836793c1b1a00fa4d75643257ef2ecde0de6e0", "timestamp": 1514713188, "difficulty": 8200, "current_epoch": 2, "validators": [{"addr": "0xebdd5b584fb0f1ad7d5da99fbc1153af11163683", "start_dynasty": 2, "end_dynasty": 1000000000000000000000000000000, "deposit": 5000.0}], "lje": 1, "lfe": 1, "votes": {"cur_deposits": 0.0, "prev_deposits": 0.0, "cur_votes": 0.0, "prev_votes": 0.0, "cur_vote_pct": 0, "prev_vote_pct": 0, "last_nonvoter_rescale": 1.0, "last_voter_rescale": 1.0}, "deposit_scale_factor": 10000000000.0, "storage": 35}
{"number": 199, "blockhash": "f1d25c47ea270592913b53b24580f209eb3fe861b4cb997470c77b69114dd954", "timestamp": 1514713993, "difficulty": 8196, "current_epoch": 3, "validators": [{"addr": "0xebdd5b584fb0f1ad7d5da99fbc1153af11163683", "start_dynasty": 2, "end_dynasty": 1000000000000000000000000000000, "deposit": 5000.0}], "lje": 3, "lfe": 2, "votes": {"cur_deposits": 5000.0, "prev_deposits": 0.0, "cur_votes": 5000.0, "prev_votes": 0.0, "cur_vote_pct": 100.0, "prev_vote_pct": 0, "last_nonvoter_rescale": 1.0, "last_voter_rescale": 1.0}, "deposit_scale_factor": 10000000000.0, "storage": 45}
{"number": 249, "blockhash": "181db4c3e8575fe001a0a90c7013ea122fc49cf685b66a251f98b5c30b610ead", "timestamp": 1514714774, "difficulty": 8192, "current_epoch": 4, "validators": [{"addr": "0xebdd5b584fb0f1ad7d5da99fbc1153af11163683", "start_dynasty": 2, "end_dynasty": 1000000000000000000000000000000, "deposit": 5000.0}], "lje": 4, "lfe": 3, "votes": {"cur_deposits": 5000.0, "prev_deposits": 5000.0, "cur_votes": 5000.0, "prev_votes": 5000.0, "cur_vote_pct": 100.0, "prev_vote_pct": 100.0, "last_nonvoter_rescale": 1.0, "last_voter_rescale": 1.0}, "deposit_scale_factor": 10000000000.0, "storage": 55}
{"number": 299, "blockhash": "21a3f22e5a7012d4556741ecfad61e5e5c8b4c46dd2d140a8d46928b7c29b053", "timestamp": 1514715567, "difficulty": 8204, "current_epoch": 5, "validators": [{"addr": "0xebdd5b584fb0f1ad7d5da99fbc1153af11163683", "start_dynasty": 2, "end_dynasty": 1000000000000000000000000000000, "deposit": 5008.0703605}], "lje": 5, "lfe": 4, "votes": {"cur_deposits": 5008.0703605, "prev_deposits": 5008.0703605, "cur_votes": 5000.0, "prev_votes": 5000.0, "cur_vote_pct": 99.8388528930493, "prev_vote_pct": 99.8388528930493, "last_nonvoter_rescale": 1.0, "last_voter_rescale": 1.0}, "deposit_scale_factor": 10000000000.0, "storage": 65}
{"number": 349, "blockhash": "e39df9477a25c1e33157ee8985f615d92f6fa022d97d240ad0688ed45528dccb", "timestamp": 1514716371, "difficulty": 8196, "current_epoch": 6, "validators": [{"addr": "0xebdd5b584fb0f1ad7d5da99fbc1153af11163683", "start_dynasty": 2, "end_dynasty": 1000000000000000000000000000000, "deposit": 5012.093353428221}], "lje": 6, "lfe": 5, "votes": {"cur_deposits": 5012.093353428221, "prev_deposits": 5012.093353428221, "cur_votes": 5004.022153932233, "prev_votes": 5004.022153932233, "cur_vote_pct": 99.83896549950596, "prev_vote_pct": 99.83896549950596, "last_nonvoter_rescale": 0.9991916634, "last_voter_rescale": 1.0008044307}, "deposit_scale_factor": 9991916634.0, "storage": 74}
{"number": 399, "blockhash": "35fc9b841d9c47657119b34f8e2456156e21ce6cf2939ce523b9ba2988e30f24", "timestamp": 1514717255, "difficulty": 8196, "current_epoch": 7, "validators": [{"addr": "0xebdd5b584fb0f1ad7d5da99fbc1153af11163683", "start_dynasty": 2, "end_dynasty": 1000000000000000000000000000000, "deposit": 5016.119599436375}], "lje": 7, "lfe": 6, "votes": {"cur_deposits": 5016.119599436375, "prev_deposits": 5016.119599436375, "cur_votes": 5008.044735281332, "prev_votes": 5008.044735281332, "cur_vote_pct": 99.8390216980482, "prev_vote_pct": 99.8390216980482, "last_nonvoter_rescale": 0.9991922301, "last_voter_rescale": 1.0008038696}, "deposit_scale_factor": 9983845464.499746, "storage": 83}
{"number": 449, "block
```

  This file has been truncated. [show original](https://github.com/ChihChengLiang/testnet-data-dump/blob/master/data/epoch.json)

---

**toliuyi** (2018-03-28):

Would you please send me 1500 Ether for test? I mined a whole day, only got a little more than 3 ether. My address is 0x146a1a572219Fd5D076bF87f4Ca247567ca76634 .

---

**liangcc** (2018-03-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/toliuyi/48/1040_2.png) toliuyi:

> 0x146a1a572219Fd5D076bF87f4Ca247567ca76634

done. but FYI, due to a bug, currently the contract is not able to take new deposits. we will launch the new testnet soon.

