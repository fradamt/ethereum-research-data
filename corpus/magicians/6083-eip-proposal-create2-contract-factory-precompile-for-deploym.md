---
source: magicians
topic_id: 6083
title: "EIP Proposal: CREATE2 contract factory precompile for deployment at consistent addresses across networks"
author: spalladino
date: "2021-04-23"
category: EIPs > EIPs core
tags: [precompile]
url: https://ethereum-magicians.org/t/eip-proposal-create2-contract-factory-precompile-for-deployment-at-consistent-addresses-across-networks/6083
views: 4004
likes: 24
posts_count: 29
---

# EIP Proposal: CREATE2 contract factory precompile for deployment at consistent addresses across networks

*Moving here a conversation [started on Twitter](https://twitter.com/smpalladino/status/1385382794310955008) to further discuss before going into opening an EIP.*

The idea behind this EIP is adding a precompile that executes a CREATE2 with whatever data is sent to it and a fixed salt. The rationale for it being a precompile is not performance, but rather being available at the same address across all networks. This allows any contract deployed through this factory to also have the same address across all networks where it’s deployed.

The aim is to provide a more robust alternative to [Nick’s method](https://eips.ethereum.org/EIPS/eip-1820#single-use-registry-deployment-account), used for example in the deployment of the 1820 registry. Nick’s method requires hardcoding the gas price of the deployment tx, which may be reasonable for a chain at a certain time, but not so much in other chains which use a different currency altogether.

With the proliferation of EVM-compatible sidechains and L2s, it’s critical to have consistent addresses across chains for well-known contracts that provide global services, such as EIP3074 invoker contracts.

I’m curious to hear others’ thoughts about this idea, before turning it into a full-fledged EIP.

## Replies

**matt** (2021-04-23):

That is a good point that gas price is hard coded in, that certainly complicates things. I’m not sure if there is bandwidth for something like this atm, but it does seem like a reasonable proposal.

---

**wjmelements** (2021-05-05):

Individual projects are already capable of doing this without a precompile, so I’m opposed.

Nick’s method can be expanded by signing additional transactions with different gas prices. It won’t matter which confirms but you can use whichever according to how much you use to fund the deployer address. I recommend powers of 10: 1 wei, 10 wei, 100 wei, etc.

---

**spalladino** (2021-05-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Nick’s method can be expanded by signing additional transactions with different gas prices. It won’t matter which confirms

But don’t you get different deployment addresses? The whole goal of this is getting consistent addresses across chains.

---

**wjmelements** (2021-05-05):

If I understand it correctly, you shouldn’t get a different address. The result address of a creation is only based on sender and nonce, so it is easy to duplicate addresses across chains. If they only sign the deployer contract deployment transactions (intentionally without replay protection), it should be secure and permissionless to deploy that standard anywhere.

---

**spalladino** (2021-05-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> The result address of a creation is only based on sender and nonce

The problem is having a trustless sender. Nick’s method works by *not* knowing the private key of the sender, but rather setting up a random signature and deriving the sender address from that, so any change on the signed tx payload (such as gas price) yields a different sender, and thus a different address.

The alternative is having someone in control of the private key used for signing the deployment, who can sign deployment txs with multiple gas prices as you say, but there are no guarantees that that someone won’t send another tx with the same key that takes up the deployment nonce and hence the address.

---

**wjmelements** (2021-05-06):

> The alternative is having someone in control of the private key used for signing the deployment, who can sign deployment txs with multiple gas prices as you say, but there are no guarantees that that someone won’t send another tx with the same key that takes up the deployment nonce and hence the address.

I see the limitation of Nick’s method now; I didn’t previously see how the signature was generated.

To sign with a private key of similar security you can do a “trusted setup” similar to EY Nightfall where the private key is generated and destroyed in some docker image live on some streaming platform for everyone to verify the steps and the cleanup, It should be possible to verify the process was live by pulling some data that could not have been known in advance, while showing the hashes of every program and library used as well perhaps as the entire system image, e.g. Docker.

Even then, it is possible that the private key was recorded by some emulator enveloping the whole charade, so I am not sure how to guarantee security on the key, except that whoever was generating the signatures probably had no motivation to exploit, and as soon as funds needed to deploy such a contract (likely minimal in value) were stolen on one network the process would need to be repeated by someone who was not now living in disgrace. So I suspect a complete trustless setup might not be necessary from a cost-benefit analysis, though posterity would appreciate whatever diligence we can engineer.

Separately, if EIP-1820 is no-good due to your gas price observation, this provides an opportunity to optimize the deployment contract by rewriting it in assembly and scrapping the features it does not truly need, such as support for ERC-165.

---

**spalladino** (2021-09-01):

Looping back on this: we found a chain (Celo) which [enforces EIP155-like replay protection](https://github.com/celo-org/celo-proposals/blob/master/CIPs/cip-0035.md) for security reasons. This breaks Nick’s method there, since the pre-signed tx is network-independent by design.

---

**axic** (2021-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spalladino/48/36_2.png) spalladino:

> The rationale for it being a precompile is not performance, but rather being available at the same address across all networks

But cannot this proxy be just deployed on all the networks via the same `CREATE2` method to achieve the same address? ![:nerd_face:](https://ethereum-magicians.org/images/emoji/twitter/nerd_face.png?v=12)

---

**spalladino** (2021-09-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> But cannot this proxy be just deployed on all the networks via the same CREATE2 method to achieve the same address?

Maybe I’m missing something, but an EOA cannot do a CREATE2, only a regular CREATE, so we’re stuck with Nick’s method for this which is a bit unreliable.

---

**axic** (2021-09-08):

You can still deploy a create2 proxy contract on any chain and re-deploy the same via it to a deterministic address.

---

**spalladino** (2021-09-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> You can still deploy a create2 proxy contract on any chain and re-deploy the same via it to a deterministic address.

But doesn’t the address determined by CREATE2 depend on the deployer, which would be this proxy contract in question?

---

**axic** (2021-09-08):

Yes, but you could use the same EOA for it on multiple chains. Can’t you?

---

**spalladino** (2021-09-09):

True, but that doesn’t work for a “public” contract, like the [EIP1820 registry](https://eips.ethereum.org/EIPS/eip-1820#deployment-method).

---

**rmeissner** (2022-09-28):

Seems like this didn’t receive any attention for a long time. But I would like to pick this up again as this would be valuable for counterfactual deployment across multiple chains. Are any of the original posters still active on this?

---

**spalladino** (2022-09-28):

I’m active, though not on this. Happy to help in pushing it forward if there’s more people interested, I still think it’s valuable. However, I’m afraid a problem in incentives here may be that this is an EIP to be adopted by Ethereum devs to benefit all chains that are not Ethereum.

---

**MicahZoltu** (2022-09-29):

These are both deployed to Ethereum mainnet, and anyone on any other EVM chain should be able to deploy them to their blockchain without any permission or special access.  I think some chains have manually deployed them as part of an irregular state chain in some cases as well.

Without salt: [GitHub - Zoltu/deterministic-deployment-proxy: An Ethereum proxy contract that can be used for deploying contracts to a deterministic address on any chain.](https://github.com/Zoltu/deterministic-deployment-proxy/)

With salt: [GitHub - Arachnid/deterministic-deployment-proxy: An Ethereum proxy contract that can be used for deploying contracts to a deterministic address on any chain.](https://github.com/Arachnid/deterministic-deployment-proxy/)

---

**spalladino** (2022-10-20):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> anyone on any other EVM chain should be able to deploy them to their blockchain without any permission or special access

Problem is with chains that require the chainId to be part of the signature (EIP155 states `should`, but some chains have implemented it as a must), so that pre-signed tx is no good. It also breaks with chains for which 100 gwei is not a valid gas price, and have no PBS-like structure to sneak in the tx anyway.

---

**MicahZoltu** (2022-10-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spalladino/48/36_2.png) spalladino:

> Problem is with chains that require the chainId to be part of the signature (EIP155 states should, but some chains have implemented it as a must), so that pre-signed tx is no good. It also breaks with chains for which 100 gwei is not a valid gas price, and have no PBS-like structure to sneak in the tx anyway.

For those chains, a precompile or irregular state change can get them deployed so they maintain EVM compatibility.

---

**rmeissner** (2022-11-01):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> For those chains, an precompile or irregular state change can get them deployed so they maintain EVM compatibility.

Still would make sense to somehow agree on the factory and an address to use. If it is not defined as a “standard” it is unlikely that any “derivative” chain would do an “irregular state change” or custom precompile.

---

**MicahZoltu** (2022-11-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> If it is not defined as a “standard” it is unlikely that any “derivative” chain would do an “irregular state change” or custom precompile.

I forget which (maybe it was Optimism) but at least one EVM compatible change already did this, so I think we can assert it isn’t out of the question at least.  I’m hesitant to bake this into Ethereum when it can be baked into other chains as needed instead.  At the same time, I appreciate your desire to have all of the chains standardize on one of the many implementations.

Would it make sense to create an ERC around one of the existing Ethereum deployments (mine or Nick’s or both, depending on whether you want deployment transaction compatibility or salt support) and then Ethereum (and several other chains) can defacto support it because those contracts are already deployed there, and other chains can have something to rally around?


*(8 more replies not shown)*
