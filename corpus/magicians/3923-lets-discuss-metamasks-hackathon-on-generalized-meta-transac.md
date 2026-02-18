---
source: magicians
topic_id: 3923
title: Lets discuss Metamask's hackathon on generalized meta transactions
author: Amxx
date: "2020-01-11"
category: Magicians > Primordial Soup
tags: [meta-transactions, meta-tx]
url: https://ethereum-magicians.org/t/lets-discuss-metamasks-hackathon-on-generalized-meta-transactions/3923
views: 3689
likes: 14
posts_count: 47
---

# Lets discuss Metamask's hackathon on generalized meta transactions

As many amount you may know, Metamask recently published a [post](https://medium.com/metamask/announcing-a-generalized-metatransaction-contest-abd4f321470b) and bounty for a new meta-transaction standard.

Unlike previous work that relied on account/proxy smart contracts (see ERC725, UniversalLogin, Gnosis, Authereum …) this targets meta-transactions directly supported by the app. They are quoting Dai’s permit function as an example.

While I think this is a really interresting move from metamask, I also think this should not be a competition but rather a collaboration between members of this community.

Starting a collaboration on twitter is difficult, and [Dmitry Palchun](https://twitter.com/Ethernian) made a good point that we should discuss that here, as it will most likelly end up being the cause of multiple ERC proposals.

Anyone interested to contribute to collaborating is welcome to answer here. Reviewer, hackers, protocol designers are more than welcome to give their opinion!

On my side, I’ve been pretty busy in the past few days and I have a working demo that I believe would be a good start:

- repo: https://github.com/Amxx/GMTX
- GMTXReceier contract: https://github.com/Amxx/GMTX/blob/master/core/contracts/GMTXReceiver.sol
- Showcase dapp contract: https://github.com/Amxx/GMTX/blob/master/core/contracts/utils/MessageHub.sol
- Showcase dapp frontend: https://gmtx.app.hadriencroubois.com/

## Replies

**Ethernian** (2020-01-11):

Thank you, [@Amxx](/u/amxx) for starting this discussion and for your decision to cooperate instead of to compete.

I had not have a look into your code yet.

I have an implementation idea, may be wrong and not verified yet, that I would just drop here.

a quickly dropped idea:

It was possible to just add any trailing bytes after encoded solidity call. These bytes were just ignored and the call went through without exception.  May be we could add the MetaTx signature to the calldata just to the end and evaluate in receiving contract?

If it already obvious - sorry.

---

**Amxx** (2020-01-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> It was possible to just add any trailing bytes after encoded solidity call.

This is how I pass the sender (origin of the meta transaction) after relaying the call (received by a generic receiver).

If you idea is to call the targeted function directly, with extra data being processed only if available … well I don’t see how to process it but it sounds interresting

---

**Ethernian** (2020-01-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> I don’t see how to process it but it sounds interresting

Solidity call dispatcher could take care about this trailing extra data, verify the signature and make the `msg.signer` available to the rest of the contract in some predefined variable together with the `msg.sender`.

I have one question:

what do we mean by generic approach? Do we assume the forward or backward form of it (or both)?

---

**Ethernian** (2020-01-11):

**Philosophical:**

To be honest, I think we are trying to work around EVM limitations that should be lifted not in this way but in some EVM HardFork Upgrade.

There is a damn old [Account Abstraction](https://ethresear.ch/t/a-recap-of-where-we-are-at-on-account-abstraction/1721) proposal, that is aimed to solve all problems like this.

If there are still hard problems preventing implementation, probably a smaller upgrade separating the message signer and the gas spender could be possible?

Ethereum gave up the Bitcoin-level immutability for the ability to make breaking protocol upgrades for high speed development - and doesn’t use it. That’s bad!

---

**Amxx** (2020-01-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> There is a damn old Account Abstraction proposal, that is aimed to solve all problems like this.
>
>
> If there are still hard problems preventing implementation, probably a smaller upgrade separating the message signer and the gas spender could be possible?

Thats a really good point. We might be trying to build a dirty ERC that badly solves something that an EIP could do much better.

---

**Amxx** (2020-01-11):

Well, this is really similar to what I do. I have an entry point that receives meta-transaction as struct, which then calls itself with the calldata included in the meta-tx AND appends the sender at the end of the calldata.

From other function you just run as usual, except that if the calls comes from yourself you overwrite the msg.sender with the 20 last bytes of the calldata. If calling yourself is something you do under normal operation then you just use a mirror to distinguish relayed calls from “normal” self calls.

---

**wighawag** (2020-01-12):

Hey [@Amxx](/u/amxx) thanks for bringing the discussion here and focusing on collaboration.

I have actually proposed an EIP for native meta transaction a while ago but for some reason it there was not much attention to it

Have a look here: https://github.com/ethereum/EIPs/issues/1776

It is actualy already live in sandbox.game but we did not enabled our relayer yet.

It solves many of the intricacies of metattx while remaining flexible: it can be used per token or in a general processor.

I am focusing for the Hackathon on the later.

It solves the msg.sender thing in a very simple manner, the first parameter is ensures to be the metattx signer.this make it compatible with many erc that have from function (erc20, erc721, erc1155)

Once I find some time I ll have a look at what you did.

Really looking forward to the outcome of this!

---

**wighawag** (2020-01-20):

Hi all,

I made a new implementation of EIP-1776 for the hackathon and you can play with it on Gorli or Rinkeby) here : https://metatx.eth.link

it is also obviously accessible via **metatx.eth** but because metamask will try to resolve ENS name on the network it is connected to (and that I did not register the name on Rinkeby or Gorli) it will fails to resolve it unless you go first on the mainnet.

The implementation is a Singleton proxy contract that implement all the meta-tx intricacies, including relayer repayment and forward the call to the destination. It is compatible with [EIP-1776](https://github.com/ethereum/EIPs/issues/1776) (which I modified slightly for some improvements).

As a result, the requirement for metatx recipient is just kept to a very minimum. They simply need to check msg.sender to be the address of the singleton. No much need for a base class, except maybe for modifiers.

You can find the code here : https://github.com/wighawag/singleton-1776-meta-transaction

[@Amxx](/u/amxx) I had a look at your proposal, I like the fact that it explores another method of implementation, that of the recipient being the meta-tx processor. What you call, a “no-proxy” implementation.

I have thus found at least 4 dimensions on which different meta-tx implementation differentiate themselves.

### A) Type of implementation

First of all, It seems we have thus so far the following type of meta-tx implementation

1. Account-contract Based (a la Gnosis Safe, etc…) where recipient do not need any modification but that require user to get a deployed account contract.
2. Singleton Proxy where the recipient simply need to check for the singleton address and where all the logic of metatx is implemented in the singleton. It can support charging with tokens and even provide token payments
3. Token Proxy where the recipient simply need to check for the token address and where all the logic of metatx is implemented in the token. This is the approach originally taken by @austingriffith in “Native Meta Transaction”. It is usually limited to be used for meta-tx to be paid in the specific token. Relayer would then need to trust each token for repayment.
4. No Proxy where the recipient is the meta-tx processor and where all the logic get implemented. While it can support relayer repayment, relayer would have to somehow trust each recipient implementation.
5. Create2 based?  I personally did not explore these much but this could be used to provide a mechanism by which user are still using EOA to sign metatx (same like account-contract based) but have an account-contract created on-demand (maybe when the first metatx is executed, in which case the relayer could be paying the cost in ether in exchange of some tokens).

Note that EIP-1776 is agnostic to the type of implementation.

### B) Relayer refund

Another differentiation is the ability of relayer to get paid.

In my opinion, It is such an important feature for relayers that we should ensure it is at least possible to implement it on top, if not already present.

In that regard one thing that becomes important as soon as a relayer get paid, is that there is a mechanism to ensure the relayer cannot make the meta-tx fails. hence the need for `txGas` in EIP-1776.

Another important EIP that would help here is [EIP-1930](https://github.com/wighawag/singleton-1776-meta-transaction)

### C) Token Transfer / Approval

While relayer-refund can be on its own, I found that it is trivial to also add the ability for meta-transaction processors to support transfering tokens to recipient.

This is a very powerful feature as it remove the need to pre-approve recipient, if they already support meta-tx.

### D) MetaTx Signer Verification

Finally, another differentation possible for non-account based metatx is how the signer is being picked up by the recipient.

In EIP-1776 it assumes that recipient can easily add a from field to their functions as this is already a common practise in many standard.

in [@Amxx](/u/amxx) and GSN version, the signer is appended to the data of the call.

I would be happy to update EIP-1776 to use this method if that is objectively better. For now, I feel the “first param” is simpler and can fulfil the same purpose, While it can in some case, requires recipient contracts to add, otherwise unecessary, extra function, most EIP, like EIP-20, EIP-721 and EIP-1155, have already functions that take the `from` as first parameter.

---

**3esmit** (2020-01-20):

I am aiming into an integrated solution for Proof-of-Stake Ethereum.

I’ve proposed a soft fork to enable miners (and in future stakers/validators) to be relayers (just like they do with regular transactions), see https://github.com/ethereum/EIPs/pull/2473

This changes can be done to geth/others, without a consensus change, and then smart contracts can then always forward gas payment to `block.coinbase` and stop having to deal with a separate ecosystem for relayers, instead the same gas market gets extended for other tokens.

For the use-case of EIP-2473 become more efficient, I proposed EIP-2474, which allows `block.coinbase`  to make calls, see. https://github.com/ethereum/EIPs/pull/2474

In regards of EIP-2473, it mentions EIP-1077, but we could support multiple standards if needed.

I’ve also updated, and is still WIP into a new EIP-1077 interface which encodes only gas payment stuff, leaving the rest to be evaluated by the wallet/account contract, and considering the `gasBase` to enable the refund of the gas payment to relayer.

---

**Amxx** (2020-01-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> You can find the code here : GitHub - wighawag/singleton-1776-meta-transaction: A Singleton MetaTx Processor using EIP-1776 that support all ERC20 tokens

Your ERC712 `domain` does not include the chainId. I think this is really dangerous has it opens the door to replay between chains if contracts are deployed at the same address.

---

**Amxx** (2020-01-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> No Proxy where the recipient is the meta-tx processor and where all the logic get implemented. While it can support relayer repayment, relayer would have to somehow trust each recipient implementation.

My idea with the no-proxy model is to separate the meta-transaction validation by the recipient form the relayer repayment. In that sens the recipient should not deal with relayer repayment. Relayer repayment is either perform by an additional on-chain layer (such as GSN) or left to off-chain accounting (including non decentralized payment in fiat).

---

**3esmit** (2020-01-20):

> Your ERC712 domain does not include the chainId. I think this is really dangerous has it opens the door to replay between chains if contracts are deployed at the same address.

This go even far deep. In case of a chain split, the chainID inside the domain separator wont work. See the discussion I opened at GnosisSafe: [Add EIP-1344 chainid opcode to signed messages composition · Issue #170 · safe-global/safe-smart-account · GitHub](https://github.com/gnosis/safe-contracts/issues/170)

---

**Amxx** (2020-01-20):

It won’t work if the domain separator is only computed in the constructor, but it’s easy to add an unrestricted public function that recomputes it at any time using the value given by the chainId opcode. I’ve done that in a few contracts were I want to avoid recomputing the domain hash everytime.

```auto
function initialize(/* params */)
external onlyOwner()
{
	require(EIP712DOMAIN_SEPARATOR == bytes32(0), "already-configured");
	EIP712DOMAIN_SEPARATOR = _domain().hash();
	// extra stuff
}
function updateDomainSeparator()
external
{
	require(EIP712DOMAIN_SEPARATOR != bytes32(0), "not-configured");
	EIP712DOMAIN_SEPARATOR = _domain().hash();
}
function _chainId()
internal pure returns (uint256 id)
{
	assembly { id := chainid() }
}
function _domain()
internal view returns (IexecODBLibOrders_v4.EIP712Domain memory)
{
	return IexecODBLibOrders_v4.EIP712Domain({
		name:              "iExecODB",
		version:           "3.0-alpha",
		chainId:           _chainId(),
		verifyingContract: address(this)
	});
}
```

---

**3esmit** (2020-01-20):

Yeah, I suggested that, if gnosis safe wants to use EIP712, they have to compute the domainhash every transaction…

The best would be to update EIP712, or use EIP191 with EIP1344 in the application data.

---

**wighawag** (2020-01-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Your ERC712 domain does not include the chainId. I think this is really dangerous has it opens the door to replay between chains if contracts are deployed at the same address.

I am aware of it ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) you can find my reasoning about the current chainId opcode in this forum (I proposed an alternative opcode that was safe under minority fork and did not require any caching but unfortunately got rejected, see EIP-1965) and I agree that chainId is important but require more complex handling that simply injecting in the constructor (or even the chainId opcode as it is  currently exposed) hence why I decided to not included it here.

But let’s not focus on that for the discussion here as this is just the domain separator. In that we can deal with that, once we agree on the rest ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Let’s discuss the important potentially incompatible difference between our perspective and figure out the best of each

---

**wighawag** (2020-01-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> My idea with the no-proxy model is to separate the meta-transaction validation by the recipient form the relayer repayment. In that sens the recipient should not deal with relayer repayment. Relayer repayment is either perform by an additional on-chain layer (such as GSN) or left to off-chain accounting (including non decentralized payment in fiat).

This is not about no-proxy vs proxy. In both case it can be dealt with outside contract.

It is about B) and if a repaymemt is supported, the signer would always need to be in control, hence why I think it is important it is part of the message standard, and not yet another.

That is why one of the goal of EIP-1776 is to be implementation independent so wallet can still process different implementation

---

**Amxx** (2020-01-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> It is about B) and if a repaymemt is supported, the signer would always need to be in control, hence why I think it is important it is part of the message standard, and not yet another.

This is assuming the message signer will be the repayer.

I believe the original idea with metatransactions was about separating the user and the transaction sender, by moving the gas cost in eth away from the user to the relayer. If you require the user to repay the relayer you are bringing back some of the original issue.

I believe that user, relayer, and repayer should be 3 separate entities. In some case 2 of those might be the same (user and repayer) but I think it would be great if as a project I can repay for some of my user meta-transactions while not being in charge of the relaying infrastructure myself.

My proposal is about allowing the receiver to process the user meta-transaction without any repayment support, and In front of that I would have any relaying mechanism, including some where there is a on-chain repayment mechanism.

---

**wighawag** (2020-01-21):

My proposal do not require the user to pay, it allows the user to pay.

The thing though that is important in all case is that if someone else than a relayer is going to pay, there need to be checks in place (txgas among them) that ensure the relayer can’t get the reward while not ensuring the metatx get submitted as intended

---

**wighawag** (2020-01-21):

As for having a repayer being different than the relayer this can be done by whatever relay system is in place.

This does not remove the need to ensure the signer is in total control of how its metatx get included.

---

**Amxx** (2020-01-21):

IMHO:

- A meta-transaction should not be considered as executed (nonce increase, …) unless the included call succeded. There is either enough gas, and the meta-tx succeded or not enough and then it fails and can be replayed
- If the meta-tx targets a contract that has try-catch behaviour, it’s up to this contract to check that the try has enough gas and revert otherwize.
- The only personne that needs to protect itself against reverted transaction is the relayer. It wants to ensure the repayer pay regardless of the outcome.
- It’s up to the relayer to say how much gas he wants the relayer to include in the transaction.

Therefore, I believe gas is an agreement between relayer and repayer and part of the relaying infrastructure. I believe it is not par of the generic meta-tx format.

If the relayer and repayer uses on-chain repayment, then they have to nest meta-tx and include gas settings in the body of the wrapping meta-tx


*(26 more replies not shown)*
