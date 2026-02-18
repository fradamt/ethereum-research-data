---
source: magicians
topic_id: 14989
title: Proposal to allow arbitrary ENV vars per tx
author: blakewest
date: "2023-07-07"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/proposal-to-allow-arbitrary-env-vars-per-tx/14989
views: 532
likes: 3
posts_count: 2
---

# Proposal to allow arbitrary ENV vars per tx

Hey all, Blake West here. I’m the cofounder and CTO of Goldfinch (https://goldfinch.finance).

For a while I’ve been interested in the idea of smart contracts being able to set environment variables that would be accessible by other smart contracts only for the duration of a transaction. I think of this as creating a space for “ENV vars” within ETH transactions.

At a very high level, this ENV var space idea would greatly reduce the coordination costs, and increases the design space of multi-contract transactions, which I think will become the default case over the coming year or two.

The use cases for this have increased recently to the point where I thought I’d raise the idea. So let me start with the basic idea, and then I’ll give some motivations and use cases for it.

### TL;DR

For any given transaction, I propose that any smart contract would be able to set and get arbitrary data that would be 1.) Guaranteed to only live in memory for the duration of that transaction (hence never any storage costs, and wouldn’t have any effect on whether a function is `view` or default), and 2.) would be available globally, just like `msg.sender` or `block.timestamp`.

This would be analogous to user controlled ENV variables that exist in virtually all other computing environments.

Some pseudo code to demonstrate:

```auto
contract MyContract {
  function doSomething() public {
    // Here we are setting msg.sender into the ENV space
    tx.env.addresses[userAddress] = msg.sender
    someOtherFunction()
  }

  function someOtherFunction() public {
    // Now we call out to some entirely other contract, which changes msg.sender
    SomeOtherContract.doOtherThing();
  }
}
```

And then way over in SomeOtherContract, we can read it back…

```auto
contract SomeOtherContract {
  function doOtherThing() public {
    // Here we simply read form the ENV space to retrieve the original msg.sender
    address userAddress = tx.env.addresses[userAddress]
  }
}
```

So what we have is two different contracts being able to communicate with one another without having to pass information between one another explicitly, even though they could be separated by multiple function calls and even multiple smart contracts. Pretty cool.

### Use Cases and Motivation

Would this actually be valuable? Well I would say that the fact that global ENV variables have existed for decades in basically every computing environment is a strong signal that they can be useful in onchain programming as well. But to get more specific with onchain use cases where this could be valuable, let me pose three.

#### 1.) Support more complex, multi-contract dapp architectures

As dapps continue to get more complex, it becomes valuable to split up logic and responsibilities amongst more contracts. Once you do this though, `msg.sender` loses it’s semantics across contract boundaries, which has significant downstream implications for this architecture. I know because we tried this at Goldfinch, and ran into this very issue.

As a simple example, imagine you want to have some top level “Router” contract, which takes a transaction, and then dispatches to some more specific logic contract (eg. an NFT). Now imagine you are calling the standard `transferFrom`, which [requires msg.sender](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L155) to be the owner, approver or operator. If it’s coming from the Router contract, then the Router will be msg.sender, and the check will break.

Worse, if you wanted to implement a view function that relies on msg.sender under this architecture, then you are forced to pass it through as a param, which is gross and feels like incidental complexity because not having to do that is exactly what `msg.sender` is there fore.

#### 2.) Support Account Abstraction

With the coming era of account abstraction, the `msg.sender` semantics will again become very broken, as it will generally be the relayer, and not the EOA. Allowing developers of AA wallets to set the signer to an ENV var, which downstream contracts can trust as the “real” `msg.sender` will be very beneficial.

#### 3.) Supporting Ethereum Attestation Service

The Ethereum Attestation Service (EAS) is an awesome public good that can help increase trust onchain by allowing for anyone to attest to anything with any schema. To save on gas costs of constantly attesting to everything onchain, some (probably most) indexers would like to give front-ends some kind of `attestation_id` which can be passed to a smart contract and verified computationally, rather than through a storage read. Again, it would suck to have to pass that attestation ID all the way through any number of contracts. Being able to set it up front into some kind of ENV var would be extremely helpful.

4.) **Removing `v,r,s` or other auth/sig info from function params**

Right now, there are a lot of functions that, when the tx sender is different from the signer, have to verify authentication and authorization with things like `v,r,s` or `expirationTime` right in the function params. If you think about it, this is weird and it conflates auth with function logic. Plus it requires every function to have to be aware of and handle it’s own auth logic. With an ENV var setup, we could clean this up. The auth could be in the ENV vars, while the downstream function would be agnostic to the auth. Or could simply trust an “auth service” contract to do this verification logic for it.

### Alternatives

If you didn’t want to create an ENV var system, then the alternatives are…

- Pass ID’s all the way down the chain → For example, the AA wallet could call whatever function and also hand in the signer’s address as a param to the receiving function. This is possible but requires sync’d coordination between the caller and receiver, and is very technically unappealing since there is no guarantee that the first recipient is the one that actually needs the information, and if someone later on down the chain needs the info, then multiple functions would have to be changed.
- Use some kind of centralized “Config” contract → In this alternative (which several protocols, including Goldfinch, have done) you create a dedicated contract to handle state vars that many different contracts need (eg. Config.set(someVar) and Config.get(someVar). From an API perspective, this is basically identical to what this proposal suggests. The big difference though, is that a Config contract approach necessarily makes it incompatible with view functions since it requires a write to the Config, and it also incurs full storage gas costs. It’s also not globally available to all contracts, which means it requires more specific coordination between the contracts.

### Getting a little philosophical

In the beginning, Ethereum made the smart contract the atomic unit, with a general underlying assumption that they are fully self contained, handling all their own data and logic in a single place. But as Ethereum development has grown in complexity, this is just not the reality. In reality, transactions and protocols are webs of inter-connected contracts, and we see consistent evidence of devs pushing against the “one contract” paradigm. For example, you have the “diamond pattern” (allowing one contract to delegate call out to N other contracts), you have Config contracts (mentioned above), you have people demanding bigger contract size limits, and demanding smart contract wallets, etc.

To accommodate this reality, Ethereum needs better tools to facilitate multi-contract architectures and transactions. I think an ENV var space would be a big step in the right direction. Plus, there’s good reason devs are pushing into that realm. It maps onto the idea of contracts being like classes, and adhering to the single responsibility principle.

### Other details

There definitely are other questions to answer, but for the sake of brevity, I am avoiding technical details in this post, like who can set what, does it work with all data types, are there size limits, is it mutable within a transaction, etc. etc. We can figure all that out once there’s some traction behind putting in the effort.

### Next Steps

I would love to get feedback on the following questions…

1. Any feedback/thoughts on the idea?
2. Has there been prior discussions about this that I should read up on?
3. Would you want to help?

In general, I’m new to the process of creating EIPs, but excited to contribute! Thanks!

## Replies

**blakewest** (2023-07-08):

I’ll also add that this proposal is very adjacent to [Transient Storage](https://ethereum-magicians.org/t/eip-1153-transient-storage-opcodes/553), which is going into Cancun. I [actually asked](https://ethereum-magicians.org/t/eip-1153-transient-storage-opcodes/553/121) about this general idea on the Transient Storage thread a couple months ago.

The only real issue is that storing anything with Transient Storage triggers a function to become default (state changing) status, rather than remaining as a `view` function. I think if that issue was addressed, then Transient Storage would basically solve for what I’m talking about.

So the upshot is that maybe implementing this won’t be that hard. Or maybe it turns into just a small improvement/variation on the Transient Storage upgrade.

