---
source: magicians
topic_id: 12517
title: Minimalistic transferable interface
author: sullof
date: "2023-01-10"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/minimalistic-transferable-interface/12517
views: 6117
likes: 73
posts_count: 120
---

# Minimalistic transferable interface

There are a lot of popular discussions about non-transferable tokens, with a good proposal at [EIP-4973 - Account-bound Tokens](https://ethereum-magicians.org/t/eip-4973-account-bound-tokens/8825)

I have been working recently on a subordinate NFT ([ERC-721 Subordinate](https://ethereum-magicians.org/t/erc721subordinate/12479)), and I realized that before everything else, we must address the problem that an exchange must know if a token is transferable or not.

Before going into so many details (like in the EIP-4973), it is necessary to solve this simple problem.

How can we avoid people spending gas trying to transfer or approve a non-transferable token?

I think we must define a minimalistic interface that tells a caller if a token is not-transferable.

This way, a marketplace can check if an NFT supports the transferability interface.

If not, the caller assumes it is a standard ERC721 token, and it is transferable.

If it supports the interface, the caller executes

```auto
function transferable(uint tokenId) external view returns (bool);
```

to verify if that token is transferable or not. The function is helpful because a token can be locally transferable or transferable under certain circumstances. In a game that can depend of other assets, of the status of the gamer, on other related contracts.

Since a soulbound token is a sub-case of a more general case, an account-bound token like in EIP-4973 can just implement this simple interface and start from that.

It is hard to find a short name to define it in a way that can be applied to token that are always non-transferable and tokens for which the transferability can depend on the context.

I would suggest something like

```auto
interface IERCxxxx {
  function transferable(uint256 tokenId) external view returns (bool);
}
```

Sometimes the most obvious name is the best.

**ADD-ON

January 20th**

As you can see in the discussion below, there are cases where the transferability of a token can be affected by the context, i.e., by its current owner or the possible recipient, but adding all those parameters in the equation over-complicates this proposal.

If a token may be non-transferable because of any internal reason, the function `isTransferable` should return false. This interface must be consumed by external entities (marketplaces, exchanges, pools, etc.), and for them knowing the internal logic that makes a token potentially non-transferable is irrelevant.

**ADD-ON

February 9th**

With [@stoicdev0](/u/stoicdev0) and other people, we proposed a new interface at



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6454)





###



A minimal extension to identify the transferability of Non-Fungible Tokens.










Initially, I had doubts about calling the function `isNotTransferable`, but the naming makes sense because by default an ERC721 is transferrable, so, this interface focus on the case when an NFT may be not transferrable, and the function names follows that. (Still, I like simplicity and I would prefer to call the function `isTransferable`)

## Replies

**stoicdev0** (2023-01-10):

This feels very similar to 5663, in draft state. Only difference I think, is naming (they use soulbound) and that the 5663 includes event.

There’s also 5192, in final state, which calls this locked and has 2 events instead of one.

Having said that. I think events are limiting, I have a use case where the token is locked or not depending on the address having another token. I’m sure there are many other cases in gaming like this. In these use cases, events don’t make sense and you cannot trust the state of a token just by indexing them.

So, I like this one better, but I’d call it something with soulbound since is what everyone is using now.

---

**xinbenlv** (2023-01-10):

[@stoicdev0](/u/stoicdev0) I was thinking the same.

There are quite a few EIPs proposed in addressing the exact same problem. IMHO It’s ok to propose competing EIPs but I’d suggest first get familiar and maybe reach out for potential collaboration and /or discuss why propose a competing EIP and it’s merit in rationale/motivation.

That said, I do enjoy seeing this EIP of which the interface is much simpler than competetors

---

**sullof** (2023-01-11):

Thanks for pointing out to them.

I can’t find the EIP-5663.

[EIP-5192: Minimal Soulbound NFTs](https://eips.ethereum.org/EIPS/eip-5192) solves the issue with trying to transfer something that is locked, but assumes that the contract implements a switch between two states and emits an event when the switch happens.

That is not always the case. It may be true with personal badges and tokens like that, but there can be a token that is observing a contract and decides if the NFT is locked or not based on that. In that case, the state of the token can not be predicted listening to the event. The only reliable way to know if it is locked or not is calling the view.

I am totally fine with the word locked, but I find it a bit risky because a token being locked can mean a lot of things. For example, in ERC721Lockable, a contract we implemented to allow people to stake their NFTs keeping the ownership of them, we use the word lock in a similar way.

I think that a more specific word would be better. Anyway, I will take a look at that discussion.

---

**sullof** (2023-01-11):

I would be happy to participate in other discussion. Sometimes, the only way to discover that there is a conversation in place, is to start a new one and get feedback ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**sullof** (2023-01-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> 5663

I found it [ERC-5633: Composable Soulbound NFT, EIP-1155 Extension](https://eips.ethereum.org/EIPS/eip-5633)

Again, this is very specific on the terminology, and has the same problem and emits an event to say to the world that that token has been bounded to a wallet. But that may not be the case.

I think that a more general naming would be better and it should not emit an event, because the state can change dynamically. In a composable environment like the EVM that should be obvious.

---

**sullof** (2023-01-11):

Maybe it makes sense to add a similar interface for approvals

```plaintext
interface IERCyyyy {

   function isApprovable(uint tokenId) external view returns(boolean);
}
```

because all the combinations can be true:

1. The token is approvable and transferable
2. The token is approvable but not transferable
3. The token is not approvable and not transferable
4. The tokens is transferable but not approvable (i.e., is transferable only by the owner)

Having two separate interfaces, one for transfers and one for approval, is the most flexible.

If the basic interfaces are minimalistic, it is easy and inexpensive to combine them and obtain whatever you like. Complex interfaces create always problems.

Anyway, the transferability is the most relevant, and a wise exchange can avoid trying to approve something that cannot be transferred.

---

**stoicdev0** (2023-01-12):

I’m with you on this. We’re creating an advanced NFT standard which includes 5773, 6059 and 6220 (to be merged) and in our repo we have a soulbound implementation in place which is basically the same you’re proposing, just a different name. We did it this way because of the same reason you mention, events would limit implementations.

So again, I like this one better. Just thought it would be good for you to have the other 2 on the radar. Let me know if we can be of any help.

---

**sullof** (2023-01-13):

I just realized that a function like

```auto
function isTransferable(uint tokenId) external view returns (bool);
```

is not working in all the scenarios and I would like to have your opinion about it.

I will make an example that unfortunately is a bit complex.

In Mobland a user can install a Farm over a Turf, in order to plant Seed and have rewards in Weed tokens. Farm and Turf are NFTs. Seed and Weed are ERC20.

To use, for example, a Farm in the GamePool, the user

- approves the GamePool as a spender
- allows the GamePool to lock the Farm

The result is that the user is still the owner of the Farm token, but they cannot transfer the token as long as it is locked in the GamePool.

In the most common case, the Farm will stay locked until all the Weed has been harvested and the user can unlock the Farm. However, we could have allowed the user to lose the Farm because an attacking team has stolen it. In that case, the GamePool could have transferred the Farm token to the attackers.

Can you see the issue with the current proposals?

That Farm is non-transferable by most wallet, but is transferable by the locker, i.e., the GamePool.

So, a simple function that expects only the tokenId as a parameter will fail.

A more general case, that would cover any possible combination is

```auto
function isTransferable(
  address from,
  address to,
  uint tokenId)
external view returns(bool);
```

What do you think?

---

**sullof** (2023-01-14):

There are in fact more scenarios that a generic interface should cover. Let’s look at the factor that can influence the transferability of an NFT.

**The token id**

I think this is obvious.

**The spender**

As I said above, making the example of the GamePool, some spender may be able to transfer some may not.

**The current owner**

In a game it is possible that someone has to own other assets, or having some balance to be able to transfer an asset.

**The recipient**

Same like for the current owner

Then, to address all the possible scenarios, the function should be

```auto
function isTransferable(
  address sender,
  address from,
  address to,
  uint tokenId
) external view returns(bool);
```

I would say that in this form, it has lost its original simplicity, but a function that covers only single cases, sooner or later, must be amended. Better to have it ready for a long future.

---

**andyscraven** (2023-01-15):

I like this approach and I agree that events cannot be relied upon in such an implementation.

Although this is not as simple as the original idea it is always a balance between simplicity and thinking about what might come down the road.

I think this is a good balance.

---

**sullof** (2023-01-15):

My last iteration may have been overkill and unnecessary.

When transferring a token, there are two primary types of exchanges involved: internal marketplaces (such as those inside a game) and public marketplaces (such as OpenSea). Internal marketplaces do not need to call a view to see if an NFT is transferable or not because they already know all the rules. On the other hand, public marketplaces simply want to know if they can transfer a token or not. This means that we can remove the “spender” from the required parameters and assume that external exchanges (such as marketplaces or pools) need to know if they can transfer the token or not.

However, we still need to consider that the current owner or the recipient can influence the transferability of an NFT. Above, [@stoicdev0](/u/stoicdev0) was pointing out

*a use case where the token is locked or not depending on the address having another token*

Moreover, the NFT knows who is the current owner or approved, so there is no need for it as a parameter and only the recipient is needed.

Therefore, I suggest using the function:

```auto
function transferable(
  address recipient,
  uint tokenId
) external view returns(bool);
```

(The simpler name “transferable” works just as well as “isTransferable” and simplicity is usually best.)

---

**toledoroy** (2023-01-18):

Just brainstorming this a little bit further.

What do you think about instead of having every contract implement all these new functionality and add that little piece of data to its own state, to just have a central contract on each chain to manage all that sort of data (on-chain metadata, so to speak) in one place. Contract as a service sort of thing that would hold arbitrary information for all other contracts on the chain. ![:thought_balloon:](https://ethereum-magicians.org/images/emoji/twitter/thought_balloon.png?v=12)

That could have a huge DRY impact

---

**stoicdev0** (2023-01-19):

> However, we still need to consider that the current owner or the recipient can influence the transferability of an NFT. Above, @stoicdev0 was pointing out
> a use case where the token is locked or not depending on the address having another token

No special need for this beyond not having events since they don’t make sense in this scenario. You can implement whatever logic you want to return the result, that includes calling other contracts.

I don’t like this depending on recipient or anything besides the `tokenId`. It’s too specific IMO for a minimalistic interface.

---

**sullof** (2023-01-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> I don’t like this depending on recipient or anything besides the tokenId. It’s too specific IMO for a minimalistic interface.

I prefer the simplest solution too, but in your specific case, if a token can be transferred depending on the address having another token, I would expect that a similar rule can be applied also to the receiver. So, if you do not specify the receiver, how can you establish if that token is transferable or not?

The tradeoff is between the simplest possible interface and a bit more complex interface that covers all the possible scenarios. If we go with the first case, maybe a partial implementation of ERC5192 is enough.

---

**sullof** (2023-01-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/toledoroy/48/5677_2.png) toledoroy:

> What do you think about instead of having every contract implement all these new functionality and add that little piece of data to its own state, to just have a central contract on each chain to manage all that sort of data (on-chain metadata, so to speak) in one place

That is an interesting approach, but how can that central contract know all the rules applicable to the NFT in different games, defi, etc.? It would require that the game, somehow, tells the registry how to manage the single case. It seems not feasible. Much easier that everyone manages its own stuff and there is a simple way to tell others what is going on.

---

**toledoroy** (2023-01-19):

Yeah, well, the contract has to explicitly declare that either way. And either way, we’d need to add some code to write that data. It would make it simpler to read, find and index. Well, I guess you could call it an index contract.

It just seems that looking at the crypto space as a community of microservices, and especially when limited to 24k, it might make more sense to have a central service that handles all similar things everyone needs. Like arbitrary identifying data, such as this, contractURI, etc’

Maybe some kind of an arbitrary data protocol for taking out all of these birds and future birds with one stone.

It would also maybe offer some relief to the spaghetti and lack of backward compatibility issue that each of these standard changes introduces.

… just a thought ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)

---

**yuki-js** (2023-01-20):

I recently submitted the “Untransferability Indicator” EIP. Currently it is for EIP-1155 tokens, but eventually I want to implement untransferability for any token specification.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yuki-js/48/8029_2.png)
    [EIP-6268: UNTransferability Indicator for EIP-1155](https://ethereum-magicians.org/t/eip-6268-untransferability-indicator-for-eip-1155/12182) [EIPs](/c/eips/5)



> I submitted an EIP, that is inspired by EIP-5172 and have a similar simple interface.
> This is something like EIP-5172 for EIP-1155.

I support your idea if it can be applied to ERC-20 token.

IMO, any tokens have transferability by default. Untransferable tokens is the specific case of them. So, I think it’s better “Untransferability Indicator” or “Untransferability Interface” than “Transferable Interface”

---

**sullof** (2023-01-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/toledoroy/48/5677_2.png) toledoroy:

> It would also maybe offer some relief to the spaghetti and lack of backward compatibility issue that each of these standard changes introduces.

That is a big problem. For Everdragons2 we are building a contract-as-a-service system to generate subordinate contracts and I am very sensitive to that issue. The problem is that a service like that, to be reliable, should index the entire blockchain. Some kind of Google for EVM. It would be fantastic, if we had something like that. I am sure that can be done, but composability, for now, is what we have and we take advantage of it.

---

**sullof** (2023-01-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> No special need for this beyond not having events since they don’t make sense in this scenario. You can implement whatever logic you want to return the result, that includes calling other contracts.

I think you are right. Let’s go back to the initial formulation. A minimalistic case where it just says if a tokenId is transferable or not. In the end, that is needed by external entities, like marketplaces, the internal marketplace does not need to call the view because it knows what to do.

I think the discussion has been very productive.

**A question for the moderators**

In general, is it better to update the initial post or is it better to link an updated document? I may create a simple repo for it.

---

**sullof** (2023-01-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yuki-js/48/8029_2.png) yuki-js:

> I support your idea if it can be applied to ERC-20 token.

Since an ERC20 is fungible, it can be either transferable or not transferable, if this interface would be applied.

If that is not the case, for example a token can be vested and there can be cases where the owner cannot transfer it or the recipient cannot receive it, this interface doesn’t work.

We need a more complex function, like the one I proposed a few comments above:

```auto
function isTransferable(
  address from,
  address to,
  uint tokenIdOrAmount)
external view returns(bool);
```

This would support also ERC20 and any other asset that is transferable between two addresses. The problem here is if to keep the interface minimalistic and simple, or make it capable of managing any possible scenario. It looks like the tendency is towards the first case.


*(99 more replies not shown)*
