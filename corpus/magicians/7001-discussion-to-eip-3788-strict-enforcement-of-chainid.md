---
source: magicians
topic_id: 7001
title: "Discussion to EIP-3788: Strict enforcement of ChainId"
author: greg
date: "2021-09-03"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/discussion-to-eip-3788-strict-enforcement-of-chainid/7001
views: 3766
likes: 7
posts_count: 20
---

# Discussion to EIP-3788: Strict enforcement of ChainId

Link to [EIP](https://github.com/ethereum/EIPs/pull/3788).

## Replies

**MicahZoltu** (2021-09-03):

I don’t think this change is a good idea because it doesn’t add value to the protocol and it breaks backward compatibility. Any wallet/signing tool that wants this can easily add it and we don’t benefit from adding it to the core protocol in ways that we cannot achieve by just convincing wallets/signers to add it.

In general, anything that can be solved at a higher layer than the core protocol I believe should be solved at a higher layer than the core protocol, and the core protocol should be as permissive as possible when given a choice between permissive and restrictive.

---

**ligi** (2021-09-03):

I also think this is a bad idea. Also FYI some backlash we got in the geth repo after blocking pre EIP-155 transactions by default: https://github.com/ethereum/go-ethereum/issues/23152

In our case people can work around it via `--rpc.allow-unprotected-txs` but when this EIP gets accepted which I do not hope it will - then this really breaks it and should for sure be in the Backward compatibility section of the EIP.

---

**greg** (2021-09-03):

> Also FYI some backlash we got in the geth repo after blocking pre EIP-155 transactions by default: https://github.com/ethereum/go-ethereum/issues/23152

This was actually one of my main motivations (FWII, we were one of the parties affected, although no one was griefed) because geth is already blocking these transactions be default. We were using geth’s signing package to sign transactions on other chains, when we realized that geth was not respecting the chainId we were adding to transactions. It’s specifically for that reason that I’m proposing this, as we cannot assume or trust that the next million developers who start developing tooling and applications will understand the ramifications of L1/L2 interactions. Ultimately I find it to be completely unsafe. To also comment on the actual feedback that was raised, the notion of repayable transactions may have been quite useful in certain situations, but I believe it to be one of those situations where we created a design flaw by trying to be clever.

> I don’t think this change is a good idea because it doesn’t add value to the protocol and it breaks backward compatibility.

I mean, it does add safety, its my main motivation behind this. I would be curious to know how many transactions are being submitted with a chainId of 0, I’ll see if I can get something created on DuneAnalytics.

> […] and the core protocol should be as permissive as possible when given a choice between permissive and restrictive.

This resonates with me quite a bit and I completely understand that. I’d like to hear some other people’s feedback regardless, alternatively I could also perhaps open a PR to the wallet `interface` or `informational` section for wallets.

---

**sak** (2021-09-03):

> In general, anything that can be solved at a higher layer than the core protocol I believe should be solved at a higher layer than the core protocol, and the core protocol should be as permissive as possible when given a choice between permissive and restrictive.

maybe this can be viewed as complete/incomplete info (instead of permissive/restrictive) ?

I mean, if the chainId is explicit (!=0), the info is complete, incomplete otherwise.

---

**MicahZoltu** (2021-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sak/48/4334_2.png) sak:

> maybe this can be viewed as complete/incomplete info (instead of permissive/restrictive) ?
>
>
> I mean, if the chainId is explicit (!=0), the info is complete, incomplete otherwise.

A pre-155 transaction is not incomplete, it is complete, just a different transaction type.  Ethereum Mainnet currently has 4 transaction types:

Legacy: This is the pre-155 transaction type.

Legacy-155: This is post-155 transaction type.

1: EIP-2930 transaction type

2: EIP-1559 transaction type

None of these are more complete than any other, though some are *newer* than others.  There are valid reasons for submitting pre-155 transactions, and post 155 transactions, and 2930 transactions, and 1559 transactions.  Arguably, 2930 is the least valuable as very few people use it and there is no functionality it provides that cannot be provided by 1559.  After that is 155 transactions which are incredibly widely used but provide no additional value beyond 1559 transactions.  The last one to deprecate IMO is pre-155, because its functionality is not currently available anywhere else.

[@greg](/u/greg) I wonder if you have interest in creating an EIP that introduces a new transaction type that is like type 2 transactions (including supporting access lists), but explicitly skips the chain ID check?  With that, I would be more in favor of a long-term EOL policy and process for pre-155 transactions.

---

**MicahZoltu** (2021-09-04):

Another option would be an EIP that introduces something like https://github.com/Zoltu/deterministic-deployment-proxy as a pre-compile or as a new deployment transaction type.  This would ensure that the ability to deploy code to deterministic addresses is conserved across future Ethereum testnets, forks, and mainnet which would give us a clean path to deprecating pre-155 transactions.

---

**greg** (2021-09-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> @greg I wonder if you have interest in creating an EIP that introduces a new transaction type that is like type 2 transactions (including supporting access lists), but explicitly skips the chain ID check? With that, I would be more in favor of a long-term EOL policy and process for pre-155 transactions.

This is actually quite interesting, I could get behind this as a better way to “ease” it out. Also this would allow us to potential deprecate legacy based transactions (signing libs can just bump legacy to type 0x3 or whatever).

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Another option would be an EIP that introduces something like https://github.com/Zoltu/deterministic-deployment-proxy  as a pre-compile or as a new deployment transaction type. This would ensure that the ability to deploy code to deterministic addresses is conserved across future Ethereum testnets, forks, and mainnet which would give us a clean path to deprecating pre-155 transactions.

Why would you need this as a pre-compile, it works perfectly fine the way it is?

---

**MicahZoltu** (2021-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greg/48/1603_2.png) greg:

> Why would you need this as a pre-compile, it works perfectly fine the way it is?

The primary legitimate use case for transactions that can be replayed across chains is for deterministic addresses of contracts deployed on multiple blockchains.  Deterministic Deployment Proxy works and has been deployed to all existing public test networks and Mainnet, as well as several L2 chains and side chains.  However, if we were to deprecate L1 support for replayable transactions, you would be unable to deploy the proxy to any new chains (like future public testnets or private testnets) created after such a change went live.

By providing users a way to reliably do deterministic address deploys to all future Ethereum-like chains (particularly testnets), we will remove the one legitimate use case for replayable transactions, and I would no longer argue against removing support for them from the protocol (which would mean setting up an EoL schedule for pre-155 transactions).

---

**MicahZoltu** (2021-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greg/48/1603_2.png) greg:

> Also this would allow us to potential deprecate legacy based transactions (signing libs can just bump legacy to type 0x3 or whatever).

Deprecating legacy transactions is going to be an uphill battle, but one that someone needs to undertake at some point in time.  The difficulty is that someone with an offline wallet, pre-signed transaction, or un-upgradable hardware wallet will no longer be able to sign transactions.  We have been very loath to make such a breaking change in the past because we don’t know how many (if any) people might be in such a situation.

One potential workaround for this would be to create a pre-compile that can be called with a signature that would execute a legacy signed transaction.  This way it could be removed from the bulk of the protocol and the complexity for handling legacy transactions can live in a fairly well isolated location within the EVM as a precompile.

If you do decide to take on this project, I encourage and support you doing so!  Just be aware that it is going to be a big project.

---

**greg** (2021-09-06):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> If you do decide to take on this project, I encourage and support you doing so! Just be aware that it is going to be a big project.

Been scheming it with lightclient for some time now, using a pre-compile  is something I didn’t think of before to ease the transition.

---

**spalladino** (2021-09-07):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Another option would be an EIP that introduces something like https://github.com/Zoltu/deterministic-deployment-proxy  as a pre-compile or as a new deployment transaction type. This would ensure that the ability to deploy code to deterministic addresses is conserved across future Ethereum testnets, forks, and mainnet which would give us a clean path to deprecating pre-155 transactions.

FWIW there was a proposal and discussion for such a precompile here: [EIP Proposal: CREATE2 contract factory precompile for deployment at consistent addresses across networks](https://ethereum-magicians.org/t/eip-proposal-create2-contract-factory-precompile-for-deployment-at-consistent-addresses-across-networks/6083)

---

**SKYBITDev3** (2023-08-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greg/48/1603_2.png) greg:

> This is actually quite interesting, I could get behind this as a better way to “ease” it out.

So you wrote this EIP before realizing that there are good use cases for replayable transactions.

I think you should now help us do something about the inability to replay transactions for contract deployments because of chain ID enforcement.

---

**greg** (2023-08-21):

This EIP is not live.

I still believe replayable transactions are not healthy for the ecosystem. If you want to maintain addresses across chains, just use the same nonce and deployer address. This EIP doesn’t prevent that.

---

**SKYBITDev3** (2023-08-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greg/48/1603_2.png) greg:

> just use the same nonce and deployer address

I’ve just mentioned in [Transaction replay blanket ban is wrong - needed for keyless contract deployment - #5 by SKYBITDev3](https://ethereum-magicians.org/t/transaction-replay-blanket-ban-is-wrong/15497/5) that that is what some of the big multi-blockchain projects tried before but failed. Trying to synchronize nonce is precarious as there are many ways for synchronization to be lost (e.g. transaction failure, unexpected transaction by others e.g. self-transfer by bridge (as had occured here: [🥹 Base Mainnet Deployment; EDIT: As of `xdeployer` `v3.0.0`, `baseMain` Deployments Are Possible 🍻! · Issue #164 · pcaversaccio/xdeployer · GitHub](https://github.com/pcaversaccio/xdeployer/issues/164))).

The best way to maintain same addresses across blockchains is by using CREATE2 or CREATE3 factories that have been deployed keylessly. Keyless deployment makes maintaining same addresses more future-proof (as factory deployment can then be done by anyone) but requires replay of a deployment transaction.

---

**loupiote2** (2024-03-04):

Greg, you need to realize how terrible this proposal would be:

This proposal would be locking out many unfortunate people who hold funds on the Ethereum chain, that are secured by an old hardware wallet (only capable of signing pre-EIP-155 Txs), and who have unfortunately lost their recovery seed phrase, but still have a working hardware device (e.g. an old ledger) and their unlocking PIN, allowing to use the device for signing ETH transactions with their private key.

For example, the guy who’s story is told here would have lost a real life-changing fortune:

https://www.reddit.com/r/ledgerwallet/comments/1af8ei9/nano_s_with_firmware_12_539_eth_recovered/

This guy would have permanently lost access to their 539 ETH (more than 1.5 million dollar at today’s valuation) if your proposal had been enacted. And it’s not the only case like this, I have seen many similar ones, and I see some every month, when people dig their old pre-EIP-155 ledgers and realize they lost their seed phrase when they moved between multiple houses.

The current situation is much better, where ETH nodes (like geth) now by default do not accept those legacy Tx’s (pre EIP-155, i.e. with no ChainID), but where it is still possible to create a specially configured ETH node that can accept legacy transactions (e.g. with geth, using the flag --rpc.allow-unprotected-txs).

So please, withdraw this very problematic proposal, or document why it would have the effect of causing a number of unlucky people to permanently lose access to their (possibly very large) ETH funds, but losing backward compatibility with legacy signed-Tx format.

It is critical that ETH Nodes will always be able to process those legacy Tx’s and there should always be a configuration option to allow a node to accept those legacy Tx’s. And yes, it is a good thing that they are now rejected by default.

---

**loupiote2** (2024-03-04):

see my comment above.

---

**greg** (2024-03-04):

This has gone stale, and as you mentioned, the more optimal conclusion that we came to (myself and Geth) was to block pre-155 at the node level, but not make it strict.

This is a three year old proposal.

---

**loupiote2** (2024-03-04):

I know that this proposal is stall and 3y old, but I still wanted to voice my opinion about it, given the number of people I know who would have been very negatively impacted by it (or any similar proposal in the future) that would break compatibility with legacy signed Tx’s.

---

**xinbenlv** (2024-03-25):

I just like to mention there is another stalled EIP that could be related



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-2294)





###



Adds a maximum value to the Chain ID parameter to avoid potential encoding issues that may occur when using large values of the parameter.

