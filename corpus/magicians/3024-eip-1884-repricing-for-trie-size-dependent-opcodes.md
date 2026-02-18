---
source: magicians
topic_id: 3024
title: "EIP 1884: Repricing for trie-size-dependent opcodes"
author: holiman
date: "2019-03-29"
category: EIPs
tags: [evm, opcodes, gas, core-eips, eip-1884]
url: https://ethereum-magicians.org/t/eip-1884-repricing-for-trie-size-dependent-opcodes/3024
views: 11317
likes: 39
posts_count: 69
---

# EIP 1884: Repricing for trie-size-dependent opcodes

This is the discussion for an EIP to reprice certain opcodes (`BALANCE`, `SLOAD`) and introduce a new opcode {`SELFBALANCE`) for the next hardfork.

- EIP 1884
- Link to the PR

## Replies

**tawaren** (2019-03-29):

I assume the reason for these opcodes getting more expensive is that the state tree grows and thus they have to traverse more nodes to find the value. If this assumption is correct would it mean that the opcodes gas cost has to be increased on a periodical basis or do you suggest to overprice it to ensure that their is a big enough buffer to account for future increases?

---

**veox** (2019-03-29):

Outdated, skip.

---

Some trivial fixes: https://github.com/holiman/EIPs/pull/1

---

**holiman** (2019-03-29):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/b77776/48.png) tawaren:

> that the opcodes gas cost has to be increased on a periodical basis or do you suggest to overprice it to ensure that their is a big enough buffer to account for future increases?

Yes, very likely. However, the rate of that repricing is difficult to tell, since there are other initiatives aimed at slowing down or reversing the state growth for the 1.x. The suggested number should last for a while, but I can’t really say how long.

---

**jochem-brouwer** (2019-05-10):

I don’t see why the new opcode for `SELFBALANCE` should be introduced. This also seems unfair to me. Contracts using the (solidity) code `address(this).balance` have compiled to (of course) getting the `BALANCE` of the current `ADDRESS`. It seems unfair to me that this will get a higher price (400 -> 700) while if they would use `SELFBALANCE` it would only cost 5 gas.

Per another EIP proposed for Istanbul, [EIP 1380](https://eips.ethereum.org/EIPS/eip-1380) (reprice gas cost of calls to self) I think it is much more in line to check that if the `BALANCE` opcode is invoked on the current `ADDRESS` it should burn the proposed 5 gas instead of the 700 gas. (Unless I have missed something here that the balance is not loaded when you call a contract and should be read from the trie - but then still, if `SELFBALANCE` can cost 5 gas and it is unknown beforehand if this opcode is going to be used it does not make sense if the balance is not loaded at the moment the contract is invoked).

The second thing I am worried about is the 4x gas increase of `SLOAD`. I agree that it should increase once the trie increases (it would be nice to see some actual numbers on it - a graph for trie size VS avg. SLOAD time would be great!), but I can imagine this will lead to problems with existing contracts on the chain. For example (in solidity) when people loop over a storage array they often write:

```auto
uint[] test;

function doSomething() public {
  for(uint i = 0; i < test.length; i++) {
    // do something
  }
}
```

This compiles to a for loop which `SLOAD`s `test.length` every time the check expression is invoked.

I am pretty sure there will be contracts which have hardcoded `call.gas(x)(calldata)`. With this 4x increase in gas this might hence, maximally, cost 4x more gas. This might lead to problems. Of course we have to check the chain if these situations exist, although it will be hard to detect those.

This also leads to the question if we should explicitly let developers know that they cannot rely on gas costs. I don’t think this is something even an experienced developer would think of. It should be explicitly stated so that developers can create a built-in function which can change this constant gas in their contracts.

If a contract is found which is susceptible to above situation I am not sure how this should be handled.

---

**axic** (2019-05-10):

Great observation! When EIP-1380 was proposed and discussed initially on ACD#46 ([notes here](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2046.md#eip-1380-reduced-gas-cost-for-call-to-self)) it was noted that it could be generalized so that any state access to “hot data” (aka. something which was accessed in the current transaction context) should/could be reduced.

If this were the case, `SEFLBALANCE` may have less of a point. However it was not pursued further due to the potential of wide ranging implications.

---

**jochem-brouwer** (2019-05-10):

I think the generalized discussion about this is really interesting (I think this is what V (Vitalik?) meant with

> Going as far as saying, gas cost for accessing an account already accessed in same block goes down from 700 to 40, potential to do this in the long term

in the [core call 46](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2046.md#eip-1380-reduced-gas-cost-for-call-to-self))

I mean, this sits, if you think about it in a slightly abstract way in the same category as [EIP 1283](http://eips.ethereum.org/EIPS/eip-1283) (Net gas metering for SSTORE without dirty maps, which caused the Constantinople delay) and of course the “calls to self” EIP. The generalized version of this all would be that any slot which is already dirty is cheaper in gas (of course taking into account a fix for the re-entrancy bug) to write to - but it should also be cheaper to read from if it is already read from / written to (cause you can cache this value). Same goes for calling contracts which have been called in the entire transaction (code is already loaded) and other variables like the balance.

Of course all this is too much to fit inside a single EIP but I think a generalized discussion about this would be great, especially with node implementers, since they can tell exactly in what (general) situations the “constant” gas price is overpriced. This would also give developers a great incentive to optimize things which would use these caches and would increase the amount of computational operations we can do in a single block.

---

**veox** (2019-05-13):

Somewhat tangent: [this recent paper](https://arxiv.org/abs/1905.00553v1) analyses `aleth`'s performance, and finds a possible mispricing for `BLOCKHASH`, `SLOAD`, `BALANCE`, `EXTCODESIZE`; and also `SDIV`, `SGT` and `SLT` (maybe due to `aleth` using `512`-bit numbers to implement these?..).

If anything, it’s interesting to compare these numbers to `geth`.

---

**holiman** (2019-05-14):

I also saw that paper, but it seems a bit strange. Although the paper is pretty recent, the data seems to be old. The statement about `BLOCKHASH` being implemented as a smart contract is not true – it was like that in a PR which was never activated. That same PR also contained a mis-pricing of blockhash: https://github.com/ethereum/aleth/issues/5313

[@jochem-brouwer](/u/jochem-brouwer) I agree it might be ‘unfair’. But I think it’s more correct. Also, the opcodes that are priced low are statically charged. What you are proposing would make it dynamically charged, since we’d have to inspect the topmost stack element and compare with the context in order to determine the cost. That means (I think) that it couldn’t be priced at `5`, but would have to go up a bit more. I’m not dead set on this, however.

In the general sense, I don’t particularly like it when evm gas pricing assume certain caching behaviour, since caches are unreliable. If we price something based on the assumption that a cache exists, then someone will try to make an attack that exhausts that cache, and once the cache is exhausted, we’re in trouble.

Regarding assumptions made on gas costs, I agree there aswell. This *may* break things, but it has IMO long been considered bad practice to hard code gas limits like that. I don’t think we can maintain current gas limits for the sake of badly written contracts, that will make the evm unusable.

---

**k06a** (2019-05-20):

I afraid increasing `SLOAD` opcode gas cost may break some existing deployed smart contracts. They can perform implicit limited gas external calls, which will stop being succed after this change.

---

**axic** (2019-06-21):

[@holiman](/u/holiman) can you include “EIP-1884” in the title as well as link to https://eips.ethereum.org/EIPS/eip-1884 in the intro?

---

**holiman** (2019-06-23):

I just tried to, but I don’t seem to be able to edit the first post, for some reason ![:man_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/man_shrugging.png?v=9)

---

**jpitts** (2019-06-24):

[@holiman](/u/holiman), I have modified the topic to be a “wiki”, this should allow you to modify the first post…

---

**axic** (2019-06-28):

[@holiman](/u/holiman) was there any progress in this EIP? What is left to do? What are the blockers/needs?

---

**holiman** (2019-06-28):

Well, it’s finished from my perspective. There are two PRs for it, original one is https://github.com/ethereum/go-ethereum/pull/19572 and then I made a second one here: https://github.com/ethereum/go-ethereum/pull/19743 . The second one is based on a refactor that would allow geth to execute statetests with the networks set as e.g. `CONSTANTINOPLE+1884`.

Apart from that, it conflicts a bit with one EIP from [@AlexeyAkhunov](/u/alexeyakhunov), so I think that’s the main reason it has not been accepted for Istanbul. As far as I can tell, it’s not sustainable to *not* increase `SLOAD` for istanbul – other than that, I don’t particularly care if it’s done within his eip or mine.

---

**axic** (2019-06-28):

Which EIP from [@AlexeyAkhunov](/u/alexeyakhunov) is this conflicting with?

Would it make sense to introduce `SELFBALANCE` independently of this? Without the repricing that still gives a 400 -> 5 gas reduction for users of the new opcode.

---

**axic** (2019-06-28):

Looking at the gas table in your second PR:

```auto
		ExtcodeSize:     700,
		ExtcodeCopy:     700,
		ExtcodeHash:     400,
		Balance:         700, // Increase from 400 to 700
```

Why wouldn’t the increase apply to `EXTCODEHASH`? It should have the same cost as `EXTCODESIZE` and `(EXT)BALANCE`.

---

**holiman** (2019-07-04):

So the EIP does not touch upon `EXTCODEHASH`. I guess it was not used sufficiently (it’s a new opcode) to show up on my metrics. I wonder why it was introduced at `400` and not `700`. It totally makes sense to me to increase it to `700` aswell…

Do you think we should add it aswell?

---

**axic** (2019-07-04):

According to [EIP-1052](https://eips.ethereum.org/EIPS/eip-1052):

> The gas cost is the same as the gas cost for the BALANCE opcode because the execution of the EXTCODEHASH requires the same account lookup as in BALANCE .

---

**holiman** (2019-07-05):

Totally makes sense. Here’s a PR to update 1884: https://github.com/ethereum/EIPs/pull/2175

---

**holiman** (2019-07-07):

I’ve made another update now, to move the opcode for `SELFBALANCE` to not collide with `CHAINID`, in case both gets accepted


*(48 more replies not shown)*
