---
source: magicians
topic_id: 8710
title: "EIP-4758: Deactivate selfdestruct"
author: dankrad
date: "2022-03-25"
category: EIPs > EIPs core
tags: [evm, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-4758-deactivate-selfdestruct/8710
views: 13145
likes: 34
posts_count: 40
---

# EIP-4758: Deactivate selfdestruct

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4758)














####


      `master` ← `dankrad:deactivate-selfdestruct`




          opened 08:25PM - 03 Feb 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/c/cc63c5d10a473c2079ea4ee24ce896c0942d6825.jpeg)
            dankrad](https://github.com/dankrad)



          [+49
            -0](https://github.com/ethereum/EIPs/pull/4758/files)







This EIP deactivates the `SELFDESTRUCT` opcode, and instead renames it to `SENDA[…](https://github.com/ethereum/EIPs/pull/4758)LL`, with the only renaming functionality being to move all funds to the caller.

## Replies

**dankrad** (2022-03-25):

Complete verkle trie construction for motivation: [HackMD - Collaborative Markdown Knowledge Base](https://notes.ethereum.org/5HDhQXstTaKtVqVbS7S9yw)

Analysis on applications that would be affected by this change: [Impact Analysis of Neutering SELFDESTRUCT - Dev Update #2 - HackMD](https://hackmd.io/@albus/rkAbjAsWF)

---

**gumb0** (2022-03-31):

Abstract says:

> The new functionality will be only to send all Ether in the account to the caller.

I believe you intended to say it sends to a beneficiary (instruction input address) and not the caller.

---

**gumb0** (2022-03-31):

Also I’ll paste [@chfast](/u/chfast)’s comment from draft PR here:

> You forgot to mention that SENDALL still terminates execution.

---

**gumb0** (2022-03-31):

Should it be repriced, as it’s now only updating balance?

---

**chfast** (2022-04-06):

The `SELFDESTRUCT` has one additional quirk not handled here: when the beneficiary is the selfdestructing address itself the balance is burned instead of being transferred.

---

**jwasinger** (2022-04-07):

Agreed that it should be mentioned explicitly in the EIP: [EIP-4758: Deactivate selfdestruct by dankrad · Pull Request #4758 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4758#discussion_r807728834).

But the new behavior can also be inferred from the EIP:  the account removal doesn’t happen so a `SENDALL` with self as beneficiary is basically a no-op that just terminates execution of the current frame.

---

**jwasinger** (2022-04-07):

[GitHub - jwasinger/eth-selfdestruct-analysis](https://github.com/jwasinger/eth-selfdestruct-analysis) .  This is an updated impact analysis which looks at usage of `SELFDESTRUCT` after the London hard fork and identifies contracts with large holdings that could be affected by the changes in EIP-4758

---

**jochem-brouwer** (2022-04-12):

~~As mentioned by [@chfast](/u/chfast) `SELFDESTRUCT` can be used to burn ETH by ‘selfdestructing’ to the current address. There is another quirk however which is changed by this EIP:~~

~~`SELFDESTRUCT` does not immediately destroy code and send the balance. This is done after all call frames are done and thus every opcode of the transaction has been executed. Only then are the following steps executed:~~

~~1. Send all ETH of the contract to the beneficiary

2. Destroy the contract (code = empty, balance = empty, nonce = 0, balance = 0)~~

~~Due to this order it is thus possible to destroy ETH. Also, notice that it is possible to do “multiple” selfdestructs by calling the selfdestruct from another contract multiple times. It is possible to first `SELFDESTRUCT` to address `A` and then `SELFDESTRUCT` to address `B`. In this case, the beneficiary is `B`, not `A`. If this changes, it should be specified on the EIP. It now seems that `SENDALL` sends all ETH of the current contract to the beneficiary and immediately exits the current call frame - which I guess is fine, but the EIP also states that it “renames” `SELFDESTRUCT` to `SENDALL` which is due to these quirks not really the case.~~

---

**chfast** (2022-04-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Only then are the following steps executed:
>
>
> Send all ETH of the contract to the beneficiary

I don’t believe this is correct. The ETH is sent immediately. [@gumb0](/u/gumb0) has double-checked this.

---

**jochem-brouwer** (2022-04-12):

Oops, you are right, have semi-deleted my post.

---

**wjmelements** (2022-04-13):

I am a consumer of the reincarnation upgrade pattern. I built an NFT contract ownership system (`0x000000000000c57CF0A1f923d44527e703F1ad70` on every chain) to facilitate this pattern. It helps us upgrade our contract without needing to re-approve and migrate every token for every protocol. Our storage footprint on the protocol would be much larger without `SELFDESTRUCT`. The `SLOAD`+`DELEGATECALL` pattern, especially after Berlin, costs way too much for practical use in gas-denominated auctions, so we cannot use it.

I am willing to pay millions in gas to facilitate code changes. I do not see why code must be immutable but not storage. Perhaps there is a fair way to price a code change, and we could introduce a replacement opcode like `SETCODE`.

The main drawback of `SELFDESTRUCT` right now from an engineering perspective is that it doesn’t take place until the end of the transaction, so I need two separate transactions to do the upgrade. This has prevented wider adoption, as you could not safely upgrade a token, for example, without risking being sandwiched.

---

**RobAnon** (2022-06-28):

Our production system heavily utilizes the [CREATE2 and SELFDESTRUCT loop](https://revestfinance.medium.com/revest-finance-innovates-with-strongest-security-in-defi-3d46d5c49a2). We have a few million dollars of TVL, with more expected to arrive in the near future. The system wasn’t designed to be modified once deployed and this EIP would fully brick our value-storage system, rendering funds inaccessible for users.

As a result, I’m very opposed to this EIP. It breaks a system that allows us to deploy and undeploy smart contract proxies within the same block, which is good not only for gas costs and allowing lower storage utilization, but also for security. By never having code deployed on those contracts outside of very predetermined periods, we reduce our attack surface area significantly. It is frustrating to be punished for being at the forefront of security in smart contract development, and we strongly request that this EIP be reconsidered or modified in some way.

Perhaps a change to CREATE2 could be considered in concert with this, such that it checks for existing byte-code and quietly fails rather than reverting. That would allow our system to continue to function unimpeded by the implementation of this proposal.

---

**WONSUNGJUN** (2022-08-30):

Is there any progress on this EIP-4758??

---

**k06a** (2022-09-06):

What do you think on repricing CREATE and CREATE2 when constructor returns zero size? Nothing will be deployed, only constructor code will be executed from new address. Now this costs 32k

---

**purplehat** (2022-10-11):

I have no strong opinions on this EIP and whether or not it is the right path forward.

Did want to flag for visibility though as part of this conversation, that this has impact on [the BytecodeStorage.sol library](https://github.com/ArtBlocks/artblocks-contracts/blob/main/contracts/libs/0.8.x/BytecodeStorage.sol) that we introduced in our ERC721-conforming “CoreContract” at [Art Blocks](https://www.artblocks.io/) here: [Contract bytecode for script storage by ryley-o · Pull Request #299 · ArtBlocks/artblocks-contracts · GitHub](https://github.com/ArtBlocks/artblocks-contracts/pull/299).

This would not be a *breaking change* perse, so if this EIP were approved+implemented it wouldn’t be a dramatic concern point for our team by any means.

That said, a meaningful part of our rationale for adding this functionality in the first place was the intention to be mindful custodians of our impact on state bloat (see [Allow for cleanup of unused contract bytecode for script storage by jakerockland · Pull Request #304 · ArtBlocks/artblocks-contracts · GitHub](https://github.com/ArtBlocks/artblocks-contracts/pull/304) for context).

It sounds like this rationale of ours may not hold water vs. the concerns around the state management complexity that comes with `SELFDESTRUCT` which is totally valid and again not a matter that we have a strong opinion on.

tl;dr, we’re making use of `SELFDESTRUCT` at Art Blocks, but it is in a way that is not dramatically impacted by this EIP in a way that we have strong concern about–I am sharing all of this for additional context/visibility and not because we have a strong opinion on the matter.

---

**purplehat** (2022-10-12):

Not sure if this actually fully solves the problem that this EIP intends to capture, and again I definitely do not have a strong horse in this race, but has the approach of *functionality limiting* the amount of state change caused by a given usage of SELFDESTRUCT, by way of changing the op-code pricing for the opcode in order to more directly bound state change to the current gas limit, an approach that has been considered?

Could definitely understand that this type of approach would be impractical with regards to the client complexity it would add to calculate gas costs in a way that fits the state-change-bounding constraints that are driving this PR, but figured I would ask! ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)![:purple_heart:](https://ethereum-magicians.org/images/emoji/twitter/purple_heart.png?v=12)

---

**wjmelements** (2022-10-14):

Related discussion regarding Shanghai inclusion: [Shanghai Core EIP Consideration - #35 by wjmelements](https://ethereum-magicians.org/t/shanghai-core-eip-consideration/10777/35)

---

**SamWilsn** (2022-10-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/robanon/48/9341_2.png) RobAnon:

> Perhaps a change to CREATE2 could be considered in concert with this, such that it checks for existing byte-code and quietly fails rather than reverting.

That is an interesting idea. You could probably set it up so that `CREATE2` will allow you to deploy the exact same bytecode to the same address, but fail for all other code.

I’d be concerned about the case where someone expects `SELFDESTRUCT` followed by a `CREATE2` to clear storage, which wouldn’t happen.

---

**SamWilsn** (2022-10-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/robanon/48/9341_2.png) RobAnon:

> rendering funds inaccessible for users.

Could you elaborate?

---

**RobAnon** (2022-10-18):

Basically, our system uses ERC-1155 to represent Financial NFTs, which are backed by tokens. Say an NFT is worth 10 tokens each, it has ID=10, and a supply of 15. 10 copies of ID=10 are owned by User1 and 5 copies of ID=10 are owned by User2

The code our system uses is as follows:

```auto
                address smartWallAdd = Clones.cloneDeterministic(TEMPLATE, keccak256(abi.encode(fnftId)));
                RevestSmartWallet wallet = RevestSmartWallet(smartWallAdd);
                amountToWithdraw = quantity * IERC20(asset).balanceOf(smartWallAdd) / supplyBefore;
                wallet.withdraw(amountToWithdraw, asset, user);
```

The OpenZeppelin method follows:

```auto
    /**
     * @dev Deploys and returns the address of a clone that mimics the behaviour of `implementation`.
     *
     * This function uses the create2 opcode and a `salt` to deterministically deploy
     * the clone. Using the same `implementation` and `salt` multiple time will revert, since
     * the clones cannot be deployed twice at the same address.
     */
    function cloneDeterministic(address implementation, bytes32 salt) internal returns (address instance) {
        assembly {
            let ptr := mload(0x40)
            mstore(ptr, 0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000000000000000000000)
            mstore(add(ptr, 0x14), shl(0x60, implementation))
            mstore(add(ptr, 0x28), 0x5af43d82803e903d91602b57fd5bf30000000000000000000000000000000000)
            instance := create2(0, ptr, 0x37, salt)
        }
        require(instance != address(0), "ERC1167: create2 failed");
    }
```

So if User1 withdraws all of his FNFTs, then User2 will find that his are permanently inaccessible because the contract already exists, as the self_destruct that would have occurred at the end of withdraw was never triggered


*(19 more replies not shown)*
