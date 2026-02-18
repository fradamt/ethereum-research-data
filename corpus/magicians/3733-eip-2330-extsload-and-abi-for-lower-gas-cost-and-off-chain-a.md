---
source: magicians
topic_id: 3733
title: "EIP-2330: EXTSLOAD and ABI for lower gas cost and off-chain apps"
author: dominic
date: "2019-10-29"
category: EIPs
tags: [opcodes, core-eips]
url: https://ethereum-magicians.org/t/eip-2330-extsload-and-abi-for-lower-gas-cost-and-off-chain-apps/3733
views: 6660
likes: 24
posts_count: 24
---

# EIP-2330: EXTSLOAD and ABI for lower gas cost and off-chain apps

Hi there topic is to discuss EIP-2330.

EIP: [EIP-2330: EXTSLOAD opcode](https://eips.ethereum.org/EIPS/eip-2330)

Connected Solidity issue: [Data Interfaces & EXTSLOAD · Issue #7593 · ethereum/solidity · GitHub](https://github.com/ethereum/solidity/issues/7593)

Aleth Implementation: [[WIP] EIP-2330 EXTSLOAD by dominicletz · Pull Request #5805 · ethereum/aleth · GitHub](https://github.com/ethereum/aleth/pull/5805)

Ping [@davesque](/u/davesque) & [@simon-jentzsch](/u/simon-jentzsch) with both of you I had a short chat in Osaka and I nearly forgot the details. But we discussed the idea for an `EXTSLOAD` instruction and corresponding Solidity ABI for the first time. Would be great if you guys could have a look at the first draft here provide and provide suggestions or comments for improvement.

## Replies

**carver** (2019-10-31):

To align with related opcodes, maybe a rename to `extsload`? (Like `extbalance`)

I don’t think the same gas price as sload makes sense, because sload assumes you have already paid the cost of loading the account from the state trie (via a call). It probably ought to be something like the sum of the gas cost of extbalance (load the account from the trie) and sload (load the slot from the storage trie).

---

**dominic** (2019-10-31):

Yeah, both makes sense. I really like the the name EXTLOAD or EXTSLOAD for this as well. I’m going to add this to the pull request. In fact I think `EXTLOAD` would be the cleanest. Any thought on keeping or dropping the S?

---

**axic** (2019-10-31):

`S` refers to storage and this is about external (account’s) storage load, so `EXTSLOAD` would be more fitting.

---

**dominic** (2019-11-01):

Thanks, I’ve updated both now in the EIP, higher gas cost (1500) and renamed to `EXTSLOAD`.

> Proposal A new EVM instruction EXTSLOAD (0x5c) that works like SLOAD (0x54) with the gas cost of EXTCODE(700) + SLOAD(800) = 1500 and an additional parameter representing the contract that is to be read from.

---

**carver** (2019-11-01):

Maybe you mean `EXTCODEHASH` instead of `EXTCODE`?

---

**dominic** (2019-11-01):

I was referring to the Fee Schedule from the [yellow paper](https://ethereum.github.io/yellowpaper/paper.pdf):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4b54c1a7e561e29327e47e710f2f54a0a6b6cf63_2_690x258.png)image976×366 48.5 KB](https://ethereum-magicians.org/uploads/default/4b54c1a7e561e29327e47e710f2f54a0a6b6cf63)

There it is G_extcode_ = 700 and G_sload_ = 200 – just that EIP-1884 will update G_sload_ to 800 so I referenced that value.

---

**spalladino** (2019-11-04):

Love to see there is interest in this opcode! Please see [this thread](https://ethereum-magicians.org/t/extsload-opcode-proposal/2410) for an earlier discussion about it.

---

**dominic** (2019-11-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png)['EXTSLOAD' opcode proposal](https://ethereum-magicians.org/t/extsload-opcode-proposal/2410/8)

> This implies that you can immediately read other accounts storage. This results in a gigantic attack vector where developers first assumed that you cannot read storage slot X from an external account and now you suddenly can (directly - e.g. without tricks). This is the reason I strongly oppose this addition.

This constant misunderstanding is probably the biggest reason for why we definitely should introduce this new opcode. Any developer who currently codes Solidity assuming non-exposed storage variables are in any way private is creating attack surfaces today. The “private” is an artificial attribute that does not actually exist in any meaningful way and just leads to confusion as some people in fact believe that the data would be protected in some way – while it is not. It’s open today, readable by anyone who cares to. If there is an “attack” transaction that can only be created by knowing the internal storage state of a contract then it can be created today already. `EXTSLOAD` would wipe out this misunderstanding making it clear to every developer  that their contract storage data is always in the open. This would clarify documentation and language around this whole topic.

**meta**

[@anett](/u/anett) is there a way to merge this and [this thread](https://ethereum-magicians.org/t/extsload-opcode-proposal/2410)?

---

**dominic** (2019-11-05):

Btw. I’ve added an Aleth implementation for this opcode https://github.com/ethereum/aleth/pull/5805

---

**anett** (2019-11-05):

[@dominic](/u/dominic) not sure what you mean by “merge threads” but I’m worried that’s not possible to merge thread on discourse ![:confused:](https://ethereum-magicians.org/images/emoji/twitter/confused.png?v=9)

---

**luzius** (2020-12-17):

From a software-engineering perspective, giving access to private members of another object is considered bad design, as it by-passes state encapsulation. This is not about data protection, this is about software design.

For example, when using EXTSLOAD on an OpenZeppeling proxy contract, it might work for a while, but then suddenly brake once the proxy contract is upgraded because the calling contract might have made wrong assumption about the internal state of the proxy contract. When calling methods on other people’s contracts, one should use the official API exposed through the according methods.

If you want to save gas, you should propose lower costs for calls to other contracts in general.

---

**deluca-mike** (2021-11-09):

External clients can already arbitrarily read contract storage slots.

Further, there is a big difference between “giving access to private members of another object is considered bad design” and “accessing private members of another object is considered bad design”.

In other words, giving software developers more tools/functionality is not bad, just because *some* might shoot themselves in the foot. However, shooting yourself in the foot is almost always a bad idea.

---

**zemse** (2021-12-19):

In the proposal it is mentioned cost of the proposed opcode EXTSLOAD = cost of EXTCODE + cost of SLOAD. Since if self contract knows which slot id it wants to read from which target contract, the bytecode of the target contract does not provide any useful information and I think the target contract address and slot id is enough for the geth node (and others) to fetch the slot value from the SSD, so the cost could be simply a cost of a SLOAD.

---

**dominic** (2022-08-24):

Thanks to [@zemse](/u/zemse) this EIP just got updated with in the context of the upcoming EVM changes. Would love to discuss getting this EIP to the next stage at the Magicians meet-up in Berlin next month [ETH Station upcoming event in Berlin [call for action] - #3 by 0xpApaSmURf](https://ethereum-magicians.org/t/eth-station-upcoming-event-in-berlin-call-for-action/10415/3) so let me know if anyone is around then.

---

**PatrickAlphaC** (2022-10-01):

Ah I can’t go to that sadly, but this opcode seems intuitively like something that would be very good. I’m having a fleeting thought (without much testing on it) that some current smart contracts might rely on the fact that others can’t read their state right now?

I wonder if we can come up with an example where adding this opcode gives smart contracts the ability to do damage of some kind that you couldn’t already do off-chain with the sensitive data.

---

**zemse** (2022-11-14):

I came across a [contract](https://github.com/makerdao/curve-lp-oracle/blob/302f5e6966fdbfebe0f7063c9d6f6bc1f6470f28/src/CurveLPOracle.sol#L247) that prevents other contracts from directly reading the state on it. I think the benefit comes from charging money for whitelisting an address, probably to fund gas. Allowing EXTSLOAD would harm the oracle business (which is definitely bad). However, looking at the oracle’s business logic the `read` method loads the slot at location `0x03` which is not recorded in the same block (the `read` function uses `cur` feed and not the `nxt` feed), hence an external untrusted party can provide the oracle feed and proof to a smart contract, which can proceed to utilize the feed for its logic, without paying the oracle maintainer for being whitelisted. But oracles should get funding for gas otherwise it would be a problem. Not sure if it is difficult for open oracles to be economically sustainable through donations or if the whitelist is really worth it.

As a side note, historically an EVM change did hurt businesses e.g. [Gas tokens](https://blog.openzeppelin.com/fundamentals-of-gas-tokens/). However, those changes did come with benefits and interest from the community.

---

**joohhnnn** (2023-04-20):

WOW, Wow, may I ask what stage these proposals have reached now？

---

**RenanSouza2** (2023-04-21):

Here an example of why it is unsafe.

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface Buyer {
  function price() external view returns (uint);
}

contract Shop {
  uint public price = 100;
  bool private isSold;

  function buy() public {
    Buyer _buyer = Buyer(msg.sender);

    if (_buyer.price() >= price && !isSold) {
      isSold = true;
      price = _buyer.price();
    }
  }
}
```

Here is a modified code from ethernaut.

The catch in this level is that originally the isSold field is public and therefore could be used by the Buyer contract to respond different prices in the two different calls.

Here it is private and still the attack could be possible. The merkle tree can be used to proove a storage but only the initial value of it.

With this instruction many attack vectors will be created.

This contract could query buyer only once, but still many other contracts already in the network would become vulnerable

---

**deluca-mike** (2023-07-20):

The last thing we should do is shy away from giving developers options and increasing transparency of contracts because some businesses operating on-chain really on contract-to-contract privacy so they can set up paywalls. Seem antithetical to Ethereum.

---

**dominic** (2023-09-27):

Hey Renan but also [@deluca-mike](/u/deluca-mike) I think there is a misunderstanding here how Ethereum state actually works.

The “public” or “private” field markers are only architectural decorators inside Solidity, but in Ethereum **all storage is always readable**. Please have a look at the documentation and examples of the RPC call `getStorageAt` [JSON-RPC API | ethereum.org](https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_getstorageat)

So in your example of `price` and `isSold` can be fetched using:

price in the first `0x0` position of the contract:

```bash
curl -X POST --data '{"jsonrpc":"2.0", "method": "eth_getStorageAt", "params": ["0x295a70b2de5e3953354a6a8344e616ed314d7251", "0x0000000000000000000000000000000000000000000000000000000000000000", "latest"], "id": 1}' localhost:8545
{"jsonrpc":"2.0","id":1,"result":"0x0000000000000000000000000000000000000000000000000000000000000064"}
```

isSold in the second `0x1` position of the contract:

```bash
curl -X POST --data '{"jsonrpc":"2.0", "method": "eth_getStorageAt", "params": ["0x295a70b2de5e3953354a6a8344e616ed314d7251", "0x0000000000000000000000000000000000000000000000000000000000000001", "latest"], "id": 1}' localhost:8545
{"jsonrpc":"2.0","id":1,"result":"0x0000000000000000000000000000000000000000000000000000000000000000"}
```

So in fact the keyword `private` is a false friend as many developers confuse this with meaning it’s not readable from the outside - when in fact anyone can read it using RPC calls - it is just inside Solidity where it’s impossible to access. This is a restriction in Solidity that you don’t have when writing e.g. a python script using RPC calls from the outside. This EIP-2330 is proposing the addition of EXTSLOAD so that this in-equality is fixed and you get the same powers inside Solidity that you have from the outside already.

Cheers!


*(3 more replies not shown)*
