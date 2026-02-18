---
source: magicians
topic_id: 19741
title: Expanding EIP 4399 PREVRANDAO with RANDAO(n)
author: alexbabits
date: "2024-04-21"
category: EIPs > EIPs core
tags: [eip-4399]
url: https://ethereum-magicians.org/t/expanding-eip-4399-prevrandao-with-randao-n/19741
views: 1670
likes: 8
posts_count: 12
---

# Expanding EIP 4399 PREVRANDAO with RANDAO(n)

**Do people want a RANDAO(n) Function?**

I am looking to revive the discussion around the potential for a RANDAO(n) function, where n is the `block.number` or `slot`. This opcode would return the `randao` value for a specified block/slot. (It could also be something like PREVRANDAO(n) to keep consistency).

I read through the EIP, articles, and this discussion here: [EIP-4399: Supplant DIFFICULTY opcode with RANDOM](https://ethereum-magicians.org/t/eip-4399-supplant-difficulty-opcode-with-random/7368). This lead me to think that many people wanted this extended functionality of `prevrandao` to be able to input a specific block.

**Is this feasible?**

If so, I think it could serve a purpose for smaller protocols to finally have secure on-chain randomness without any oracle integration. Larger protocols may continue to want off chain oracles, because there does appear to be relatively cheap attacks (block reward opportunity cost) to refuse to publish a block, or get 2^n bits/attempts per proposer that a malicious actor owns.

**Why is it needed**

I’ve written an opinion piece [here](https://medium.com/@alexbabits/why-block-prevrandao-is-a-useless-dangerous-trap-and-how-to-fix-it-5367ed3c6dfc) discussing the current failure of the `prevrandao` use case, and a potential fix with `RANDAO(n)`.

In short, `block.prevrandao` has minimal use cases because the value it uses must be from a block that already exists. There is no way to “delay” the request for randomness to a later unknown time in the future when the randomness production should be revealed. The return value it uses must be from a block that already exists, and it’s `randao` value is determined by the immediate previous block that the transaction was finalized in. Using `block.prevrandao` can be taken advantage of in a simple manner. A malicious function can call the target protocol’s `getRandomness` type of function, which uses `block.prevrandao` as the powerhouse to generate it’s random number for users. This malicious function can revert if the generated random number is unfavorable, and only choose to execute when the number generated is favorable (see medium post).

In contrast, if we had `RANDAO(n)`, this appears to be a step forward in achieving more secure on chain randomness. I’ve built a coin flip game to demonstrate the use case for `RANDAO(n)`.

```js
// This doesn't compile because randao(n) doesn't exist.
// DO NOT USE IN PRODUCTION

mapping(address => uint256) public usersBlockNumber;

error FailedEthTransfer();
error IncorrectPayment();
error AlreadyHasBlockNumber();
error NotMatured();

function setUsersBlockNumber() public payable {
    // User must not have a block number.
    if (usersBlockNumber[msg.sender] != 0) revert AlreadyHasBlockNumber();

    // User must pay in advance (0.01 ETH to play).
    if (msg.value != 1e16) revert IncorrectPayment();

    // Let the users block number be 4 epochs after this call.
    usersBlockNumber[msg.sender] = block.number + 128;
}

function generateAndUseRandomness() public payable {
    // Get user's block number.
    uint256 usersBlock = usersBlockNumber[msg.sender];

    // Must have a matured and valid block number associated with user.
    if (usersBlock  50) {
        (bool success,) = msg.sender.call{value: 2e16}("");
        if (!success) revert FailedEthTransfer();
    }

    // Always set users block back to 0 after using randomness.
    delete usersBlockNumber[msg.sender];
}
```

Notice now the user has no way of manipulating the outcome after they have requested that a block be associated with them. The user cannot create a function that reverts when the randomness is unfavorable, because the randomness is not known at time of request, and can never be, because the request always references a block far into the future. At time of execution, the users block associated with them is always X distance away.

We have the same security techniques as requesting a random number from Chainlink VRF, disallowing users to re-request randomness, and freezing any function calls for the user while they have a number associated with them but not yet used. Also, the depth of the request should be at least the maximum re-org depth I would guess. I’m unsure if a full 4 epochs of waiting time would be necessary for “lotteries” with less than the block reward value.

If `RANDAO` were to use the slot instead of block, and the slot was empty, as mentioned in the original EIP-4399 discussion, it would have to look back further in the past to find a non-empty slot, or have some other technique. For this reason using the block number may be superior, even if the timing is not perfectly consistent, always having a valid number feels better?

I am interested by what others have to say about the feasibility and impact or lack thereof for this new opcode that would act as an extension of `PREVRANDAO`.

## Replies

**alexbabits** (2024-04-25):

These people seemed interested in RANDAO(n) potential implementation per the original EIP-4399 discussion.

[@mkalinin](/u/mkalinin)

[@MicahZoltu](/u/micahzoltu)

[@axic](/u/axic)

[@apiscerena](/u/apiscerena)

[@markuswaas](/u/markuswaas)

---

**MicahZoltu** (2024-04-25):

You can get `PREVRANDAO(n)` by verifying block headers.  If you do this naively, the cost of doing this scales linearly with how far back `n` is from head block.  You could, in theory, do it in a ZK system, though IIUC keccak256 isn’t particularly cheap/easy in most current ZK systems which is unfortunate.

---

**alexbabits** (2024-04-25):

Ahh the EVM doesn’t support any kind of `block.xyz(block.number)` because it would need to look at a specified block, which is not what it’s meant to do. It’s duty is to give information about only the immediate latest published block header info, and that is all in this regard. So that would require a major change to the EVM which will likely never happen?

As you mentioned, you could “manually verify/cache” every header’s randao mix value from each block?:

A script calls contract’s `getAndStorePrevrandao()` function that stores the randao value for that block number. Users would only be able to request randomness by associated their address with a future block N blocks into the future. If there is no value for their associated block yet, then revert. (Issues if the script ever misses a block). However, every block’s randao value that you store would cost 20000+ gas, at which point… just use an oracle). On something like polygon this would still be $300/day if you ran it 24/7, lol. Even if you called it once every 10 blocks or something it would still be costly…

A ZK solution sounds like it could work and maybe be cheaper, but I wouldn’t know where to begin.

---

**MicahZoltu** (2024-04-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> If you do this naively, the cost of doing this scales linearly with how far back n is from head block.

This is not true, don’t listen to that guy.  It is constant time for the most recent 256 blocks (IIRC), then scales linearly after that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexbabits/48/12337_2.png) alexbabits:

> Ahh the EVM doesn’t support any kind of block.xyz(block.number)

It does support `blockhash[number]`, but only for the last 256 blocks.  This can be used by a contract to verify the contents (provided as input) of any of the last 256 blocks.  Beyond that you would have to start 256 blocks back and then verify a chain of headers backward (using the parent field to to step backward).

There was a proposal (EIP) to have a system contract that wrote the blockhash of every block into state.  This way you could do `blockhash[number]` back since the fork that added such a feature.  This would come at the cost of state growth increasing by ~32 bytes/block forever.  That proposal hasn’t been implemented, but not because there was agreement it was a bad idea.  It just wasn’t a *good enough* idea.

---

**qizhou** (2024-04-26):

Using `blockhash` opcode, we have implemented a library to look up a historical RANDAO here



      [github.com](https://github.com/ethstorage/storage-contracts-v1/blob/main/contracts/RandaoLib.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./RLPReader.sol";

library RandaoLib {
    using RLPReader for RLPReader.RLPItem;
    using RLPReader for RLPReader.Iterator;
    using RLPReader for bytes;

    function getRandaoFromHeader(RLPReader.RLPItem memory item) pure internal returns (bytes32) {
        RLPReader.Iterator memory iterator = item.iterator();
        // mixDigest is at item 13 (0-base index)
        for (uint256 i = 0; i < 13; i++) {
            iterator.next();
        }

        return bytes32(iterator.next().toUint());
    }

```

  This file has been truncated. [show original](https://github.com/ethstorage/storage-contracts-v1/blob/main/contracts/RandaoLib.sol)










An application of this to verify an off-chain random sampling with RANDAO as the random seed (see [here](https://github.com/ethstorage/storage-contracts-v1/blob/f1c9c17ef16b59c0495388672f11797eeec7848a/contracts/StorageContract.sol#L211))

Note that for L2s, using L2 RANDAO for randomness is broken as the sequencer can easily forge any RANDAO number.  A way to address the issue is to look up L1 RANDAO from L2.  An RIP is proposing to support reading L1 blockhash and thus L1 RANDAO (see [RIP Idea: L1 Blockhash Precompile · Issue #16 · ethereum/RIPs · GitHub](https://github.com/ethereum/RIPs/issues/16)).

---

**alexbabits** (2024-04-26):

Wow that’s really cool!!

The `verifyHistoricalRandao()` returns the randao value from a historical block, which is what `RANDAO(n)` would hypothetically do.

I realized this process cannot be done on chain entirely, which is unfortunate. We are not able to generate `headerRlpBytes` argument on chain because we only have access to some of the block header data, and not ALL of the block header data.

Without all of the block header data, we cannot generate a proper RLP-encoded block header. We need a full RLP-encoded block header so that we can verify it by comparing the actual known block hash to the `rlpBytesKeccak256()` hash of our `headerRlpBytes` item. Without this verification step we cannot properly verify and use a real and secure randao value.

We can get all the block header data and RLP-encode it easily off chain though, which is nice, as shown by qizhou’s test file [here](https://github.com/ethstorage/storage-contracts-v1/blob/f1c9c17ef16b59c0495388672f11797eeec7848a/test/randao-test.js#L7) and another repo test [here](https://github.com/hamdiallam/Solidity-RLP/blob/0212f8e754471da67fc5387df7855f47f944f925/test/basic-tests.js#L17).

I found an on chain [RLP-encoder](https://github.com/bakaoh/solidity-rlp-encode) library, which complements the [RLP-decoder](https://github.com/hamdiallam/Solidity-RLP/blob/master/contracts/RLPReader.sol) library nicely… But even if we can do all the encoding and decoding on chain… We still cannot make secure randomness fetching happen entirely on chain because we would need all of the block header data? (Also, RLP-encoding looks gas intensive on chain).

---

**MicahZoltu** (2024-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexbabits/48/12337_2.png) alexbabits:

> I found an on chain RLP-encoder library, which complements the RLP-decoder library nicely… But even if we can do all the encoding and decoding on chain… We still cannot make secure randomness fetching happen entirely on chain because we would need all of the block header data? (Also, RLP-encoding looks gas intensive on chain).

You can verify RANDAO(n) for any `n` within the last 256 blocks with code like this:



      [github.com](https://github.com/Keydonix/uniswap-oracle/blob/master/contracts/source/BlockVerifier.sol)





####



```sol
pragma solidity 0.6.8;

library BlockVerifier {
	function extractStateRootAndTimestamp(bytes memory rlpBytes) internal view returns (bytes32 stateRoot, uint256 blockTimestamp, uint256 blockNumber) {
		assembly {
			function revertWithReason(message, length) {
				mstore(0, 0x08c379a000000000000000000000000000000000000000000000000000000000)
				mstore(4, 0x20)
				mstore(0x24, length)
				mstore(0x44, message)
				revert(0, add(0x44, length))
			}

			function readDynamic(prefixPointer) -> dataPointer, dataLength {
				let value := byte(0, mload(prefixPointer))
				switch lt(value, 0x80)
				case 1 {
					dataPointer := prefixPointer
					dataLength := 1
				}
```

  This file has been truncated. [show original](https://github.com/Keydonix/uniswap-oracle/blob/master/contracts/source/BlockVerifier.sol)










You cannot get RANDO for *current* block, but that usually isn’t necessary.

---

**qizhou** (2024-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexbabits/48/12337_2.png) alexbabits:

> We still cannot make secure randomness fetching happen entirely on chain because we would need all of the block header data? (Also, RLP-encoding looks gas intensive on chain)

That is why it is better just to pass the RLP-encoded header in calldata and use on-chain verifier to check.  The RLP-decoder cost is not that much, but the calldata may be a bit expensive - especially [EIP-7623: Increase calldata cost](https://eips.ethereum.org/EIPS/eip-7623) will increase the non-zero-per-byte cost to 48 gas.

---

**alexbabits** (2024-04-28):

Is this as far as we could go in terms of using randao of a specific block for randomness on chain? We must have an off chain service to provide the fully encoded block header so we can verify and extract the randao value from it.

User wants to flip a coin on chain. They need a secure random number. Process is similar to Chainlink VRF.

1. User calls initiateCoinFlip() which associates a future block.number with their address.
2. Wait until the user’s block has been validated, and then the user can successfully call requestRandomness(), and the user gets a request ID associated with them. An event like request(blockNumber) would be emitted, and listened to by an off-chain oracle. The off chain service does RLP-encode for that block’s header, and then calls the callback fulfillRandomness() providing the RLP-encoded block header back to the request ID corresponding to the user. The randomness value is now associated with the user.
3. User can call flipCoin(), which verifies the users RLP-encoded block header from the oracle matches the correct block hash for the users block, and then extracts the RANDAO value from the encoded header through an on-chain RLP-decode library. It uses the extracted randao value to flip the coin and pay the user if they won.

That would be a 1 random word for 1 user. You could allow for multiple random words by associating an array of fixed length for the block numbers with the user, and then request randomness takes in the array. (This would only succeed if the block number that is furthest into the future has already passed). The fulfillment would give the array of RLP-encoded headers, and then you can verify and extract each headers RANDAO value.

There is the same centralization problem with the off chain service… If the oracle doesn’t provide a response or invalid responses… Then you simply don’t get your random number(s) and it’s all ruined.

- Benefit vs Chainlink VRF: Because we are using the inherit randomness from the block header’s RANDAO value, instead of going through a whole process to verify that the oracle provided random number was not tampered with, all we need to do is verify that the provided RLP-encoded block header from the oracle does indeed match the block hash for the block number for the user on chain. We already know the RANDAO value from the block header is a non-tampered random number with respect to fetching it, but not with respect to the proposer’s potential to maliciously alter it.
- Drawback vs Chainlink VRF: Cannot be used on L2 because sequencer can easily forge any RANDAO number (qizhou). And on L1, malicious proposers have some ability to manipulate randao mix?

I haven’t understood the relationship between the cost for a proposer to execute an attack and how much dominion they would have over trying to alter the randao value. It seems like waiting 128 blocks (4 epochs) makes it impossible/useless for proposers to tamper the randao value? I don’t really understand this side of the problem. Waiting 128 blocks is not ideal if randomness is needed quickly and often because of Ethereum block times and gas fees.

---

**MicahZoltu** (2024-04-29):

As a reminder: The proposer of slot `n` which contains block `m` (where block `m` is the block that the roll will occur in) can pick between two options.  If a proposer (or coalition of proposers) produces two blocks in a row they get 4 possibilities to choose from.  If you control 3 blocks in a row, you get 8 possibilities, etc.  When a proposer executes an attack like this they need to pass up on proposing one or more blocks.  This means they will be out the block production reward for one or more blocks (depending on the roll they want), so one needs to be careful that there isn’t *too* much incentive to get “rerolls”.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexbabits/48/12337_2.png) alexbabits:

> Drawback vs Chainlink VRF: Cannot be used on L2 because sequencer can easily forge any RANDAO number (qizhou). And on L1, malicious proposers have some ability to manipulate randao mix?

One could argue that the ability for a party to manipulate the RANDAO is *lower* than all other proposed options.  Last time I looked into ChainLink, it *appeared* to be a centrally trusted service.  Maybe things have changed, but I wouldn’t personally trust it without a lot of diligence.

---

**alexbabits** (2024-05-14):

I made an oracle that can be run on Sepolia using the techniques talked about. I think it might have potential. It’s kind of clunky, but maybe it can be smoothed out. For anyone interested who wants to talk more or help get the ball rolling:

https://github.com/alexbabits/entropy-oracle

“RANDAO(n) oracle built without complex proofs. Randomness secured by using multiple future block randao values per single random word. Requires every proposer to be malicious. Can couple this with waiting 4+ epochs for nearly perfect security.”

