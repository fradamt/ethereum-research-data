---
source: ethresearch
topic_id: 13843
title: EIP-3541 locks my ETH in contract forever. What should I do?
author: 0x7d7
date: "2022-10-04"
category: EVM
tags: []
url: https://ethresear.ch/t/eip-3541-locks-my-eth-in-contract-forever-what-should-i-do/13843
views: 5175
likes: 12
posts_count: 7
---

# EIP-3541 locks my ETH in contract forever. What should I do?

I’m sorry if this is the wrong place to post this, but I can’t find a better place to explain my situation.

I have been using Ethereum since 2016 and was doing MEV even before the word MEV exists. Today I was going to withdraw my ETH and Tokens from an old contract deployed by myself years ago. The withdrawing transaction simulation always failed so I did some tracing to find out the reason, which made me really really surprised.

Here is what happened. For gas optimization, that contract uses CREATE and EXTCODECOPY to read and write persistent data, instead of SSTORE and SLOAD. During the withdraw process, the contract needs to change its state so it tries to CREATE a new contract with bytecode starts with the byte 0xEF. EIP-3541 made this impossible. I have read through my old contract code (written in Yul) and I’m sure that there’s no way to work around this issue. For privacy reasons, I don’t want to share my contract address and the source code.

These ETH and Tokens are not small money for me and I really need them now.

I’m really surprised that this EIP doesn’t care about backward compatibility at all. It only cares about  executable contracts while just leaving these non-executable contracts ignored. I’m not the only one to store raw data in contract bytecodes, like in this article published in 2019 [On Efficient Ethereum Storage. As you make headway in the quest to… | by 0age | Coinmonks | Medium](https://medium.com/coinmonks/on-efficient-ethereum-storage-c76869591add)

I’m so depressed and don’t know what to do next. Should I propose a new EIP just for my case? Is this acceptable? Will this kind of issue happen again to somebody else? Do the Ethereum core devs really care about this kind of edge cases? What should Ethereum users like me do to prevent this from happening again? What sort of contract code is guaranteed to work in the future and what sort of contract code is not? How do I trust Ethereum to protect my money?

I believe in decentralization and really love the Ethereum ecosystem. However, I can’t trust it anymore. If I can’t get my ETH back, I only hope this will never happen to others again.

## Replies

**high_byte** (2022-10-04):

The EIP states:

`Analysis in May 2021, on `18084433`contracts in state, showed that there are 0 existing contracts starting with the`0xEF`byte, as opposed to 1, 4, and 12 starting with`0xFD`,`0xFE`, and`0xFF` , respectively.`

I’m afraid without sharing your contract it’s impossible to say for sure.

If you want another pair of eyes on your contract feel free to dm.

---

**cairo** (2022-10-04):

Interesting analysis yet it makes sense there are 0 existing contracts starting with the `0xEF` byte (in this case) because maybe OP hasn’t tried to withdraw funds before May 2021 so the the contract didn’t need to change its state by creating a new contract with starting 0xEF bytecode.

I agree that without the source code its impossible to work around this issue. In a best case, there is a vulnerability in the code which would allow to retrieve the funds.

---

**MicahZoltu** (2022-10-04):

Would you be comfortable with sharing your address with someone from the Ethereum security community or core EVM community?  Getting a trusted dev to validate (privately) the contents of your contract behave as you say they do would go a long way to getting this issue taken seriously and addressed.

The reason for wanting to do this validation is because fixing this is likely non-trivial and we need confidence that you aren’t just someone trying to derail development.

Edit: It is worth noting that the solution to this problem may require making your address public (for example, if we wanted to do an irregular state change), and even if we found a workaround for reading, someone could monitor the chain for such a read and identify your address.

---

**wschwab** (2022-11-01):

[@MicahZoltu](/u/micahzoltu) 's proposal of getting some researchers to privately look over the contract seems like the most reasonable way forward to me personally. fwiw, I’d be happy to try facilitating something. (I’m more than happy to discuss details with you - I’m wschwab on tg and wschwab_ on Twitter.) I shouldn’t even need to know the address myself.

The EIP route does not seem promising to me. Either famously or infamously, there was an EIP around Parity having north of $150m of ETH bricked that explored ways of making an irregular state change to get it back which generated a lot of controversy at the time, and was never implemented.

I do think there is a cautionary tale here for the future, that when implementing new opcodes and the like, simply scanning addresses may not be enough to detect collisions.

Lastly, I assume you’ve thought of this, but if your contract has a `SELFDESTRUCT`, that would transfer out the ETH. Similarly, if your contract has the ability to `DELEGATECALL` an arbitrary contract, you could deploy a contract with `SELFDESTRUCT` and delegatecall in. (I assume the latter is true, but have not actually prototyped to make sure.)

---

**Pandapip1** (2022-11-01):

I can confirm the selfdesruct by delegatecall does work – there have been some spectacular instances where contracts have been maliciously destroyed using that trick.

---

**adietrichs** (2022-11-24):

Given that [EIP-3540](https://eips.ethereum.org/EIPS/eip-3540) ended up having to use a 2-byte magic prefix (`0xEF00`) anyway, I would be in favor of reducing the scope of the prefix ban to that 2-byte prefix as part of the EOF upgrade. [@0x7d7](/u/0x7d7) it would be helpful if you could confirm that the code your contract tries to deploy does not have a `0x00` second byte?

