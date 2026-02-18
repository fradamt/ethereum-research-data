---
source: magicians
topic_id: 3271
title: Any funding/interest available for EIP-689 (Address Collision) and EIP1829 (Eliptic Curve)
author: MadeofTin
date: "2019-05-14"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/any-funding-interest-available-for-eip-689-address-collision-and-eip1829-eliptic-curve/3271
views: 744
likes: 0
posts_count: 5
---

# Any funding/interest available for EIP-689 (Address Collision) and EIP1829 (Eliptic Curve)

Went through this list and there is 2 more EIPs currently looking for Champions.


      [github.com](https://github.com/ethereum-cat-herders/PM/blob/master/Hard%20Fork%20Planning%20and%20Coordination/IstanbulHFEIPs.md)




####

```md
 # Istanbul Hardfork EIPs

[EIP 1679](https://eips.ethereum.org/EIPS/eip-1679) is created as the **Istanbul Hardfork** tracking **Meta EIP** .

Below is the list of EIPs proposed so far. We are going to update its status from "Proposed" -->  "Under Consideration" --> "Accepted" or "Rejected" for the Istanbul upgrade based on the decision taken by the Core Devs.


 №  | EIP  |	Description	| Status |	Client Implementation |	Testnet |	Include in Istanbul HF |
|---| -----|--------------|------- | -----------------------| --------|----------------------- |
| 1 |[EIP 1829](https://eips.ethereum.org/EIPS/eip-1829)| Precompile for Elliptic Curve Linear Combinations| Under consideration - Need champion to work on it. | NA|NA|NA|
| 2 |[EIP 615](https://eips.ethereum.org/EIPS/eip-615) | Static Jumps and Subroutines (part of EVM Evolution discussion)| Under consideration - Discuss in next ACD  | NA|NA|NA|
| 3 |[EIP 1057](https://eips.ethereum.org/EIPS/eip-1057) | ProgPoW, a Programmatic Proof-of-Work| Accepted - Client implementation recomended. | NA|NA|NA|
| 4 |[EIP 1559](https://github.com/ethereum/EIPs/issues/1559) | Fee market change.  |Under consideration - Discuss in next ACD, participate in discussion at https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783  | NA|NA|NA|
| 5 |[EIP 1884](https://github.com/holiman/EIPs/blob/reprice/EIPS/eip-1884.md) | Opcode repricing for trie-size-dependent opcodes | Under consideration, participate in discussion at https://ethereum-magicians.org/t/opcode-repricing/3024 | NA|NA|NA|
| 6 |[EIP 665](https://eips.ethereum.org/EIPS/eip-665) | Add precompiled contract for Ed25519 signature verification | Under consideration, one of two (EIP 665 or EIP1829) will go forward. | NA|NA|NA|
| 7 |[EIP 152](https://github.com/ethereum/EIPs/issues/152) | BLAKE2b `F` Compression Function Precompile  |Under consideration - [champion needed](https://github.com/ethereum-cat-herders/PM/issues/64) | NA|NA|NA|
| 8 |[EIP 1344](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1344.md) | ChainID opcode | Accepted | NA|NA|NA|
| 9 |[EIP 1890](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1890.md) | Commitment to Sustainable Ecosystem Funding | Proposed | NA|NA|NA|
| 10 |[EIP 1352](https://eips.ethereum.org/EIPS/eip-1352) | Specify restricted address range for precompiles/system contracts | Accepted | NA|NA|NA|
| 11 |[EIP 689](https://eips.ethereum.org/EIPS/eip-689) |  Address Collision of Contract Address Causes Exceptional Halt | Proposed - need champion | NA|NA|NA|
```

  This file has been truncated. [show original](https://github.com/ethereum-cat-herders/PM/blob/master/Hard%20Fork%20Planning%20and%20Coordination/IstanbulHFEIPs.md)








## 689 - Address Collision of Contract Address Causes Exceptional Halt


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-689)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.








## 1829 - Precompile for Elliptic Curve Linear Combinations


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-1829)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.








I just submitted to shepherd Blake2b. I would consider shepherding those two a well as long as there is interest. I spend most of my time in the ETH1.X world these days so it wouldn’t be too much for my plate right now.

## Replies

**MadeofTin** (2019-05-14):

The later I believe is the one that [@AlexeyAkhunov](/u/alexeyakhunov) mentioned has a team already working on it.

---

**MadeofTin** (2019-05-14):

Yep - I found it in the notes.

> EIP 1829 will be championed by Alexander Vlasov who has been working on this implementation already for quite a while.

https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2060.md

---

**jochem-brouwer** (2019-05-14):

I like 689. Even though this should be practically impossible, it would be great to have an extra layer of security in the protocol itself. Some conversations I had were about, for instance, discovering private keys. While this EIP does not solve this “problem”, it is close to this problem. If you can show to a person that you cannot “guess” private key sets to create a contract (e.g. find two accounts which deploy to the same address), because it fails on protocol level that would be great.

Since this is already the case for `CREATE2`, I think that `CREATE` should not be treated on a different foot. In `CREATE2` it is obvious to create hash collissions (by providing the same seed and the same init code hash) in `CREATE` this is less obvious but should be treated on the same foot anyways. I would love to see this pushed to Constantinople.

---

**MadeofTin** (2019-05-14):

[@jochem-brouwer](/u/jochem-brouwer) You have the Bandwith to tackle the development side/tests/reference implementations? I am happy to run with the rest.

