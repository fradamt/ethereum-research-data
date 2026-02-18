---
source: ethresearch
topic_id: 11416
title: "Proposal: Minimizing fraudulent transactions in Metamask, e.g via front-end hacks"
author: hiddentao
date: "2021-12-03"
category: Security
tags: []
url: https://ethresear.ch/t/proposal-minimizing-fraudulent-transactions-in-metamask-e-g-via-front-end-hacks/11416
views: 4540
likes: 13
posts_count: 16
---

# Proposal: Minimizing fraudulent transactions in Metamask, e.g via front-end hacks

*This was inspired by the recent front-end attack against BadgerDAO. Though this post focuses solely on securing Metamask and other browser-extension based wallets I’m hopeful that - with some discussion and smart ideas - it can be expanded to cover other types of wallets too.*

For front-end attacks, the root issue at play is that users [do not really know](https://twitter.com/koeppelmann/status/1466410728265498637) whether what they are signing is legit. How the information is presented in the Metamask popup doesn’t really matter since in daily use most users just click through as quickly as they can anyway. Plus, having to double check the information one is seeing would just make for terrible UX.

I propose a simple solution whereby Metamask double-checks the information on behalf of the user. Broadly speaking:

1. Dapp makes a transaction signing request, which goes through to Metamask.
2. Metamask obtains the current browser tab URL. I’m assuming it’s unlikely the user is able to switch to a different tab before the request reaches Metamask.
3. Metamask uses keccak256(URL domain) as a key into an on-chain (chain being whatever chain the tx is for) lookup table which lists the expected contract addresses for that domain.
4. Thus, Metamask is able to confirm whether the address that is being approved as a token spender is the expected one, or whether the contract being called in the tx is the expected one.

*Regarding point (3), the on-chain lookup table would ideally be deployed at the same address on every chain. Multi-chain dapps would need to ensure their lookup data is kept up-to-date on all their supported chains. And perhaps there is some synergy to work with existing lookup table such as ENS, haven’t yet through this through fully.*

Clearly this would be an opt-in system - if Metamask is unable to find any on-chain registry data for the domain then it would inform the user of this whilst still letting the user proceed with the signature.

A dapp author would ideally create an entry for their domain in the lookup table prior to launching their dapp front-end. Only their account would be able to make updates to that domain’s list (and obviously, a change of ownership would be possible at any time). Eventually the existing dev tooling would integrate this as an optional deployment step.

The benefits of this solution are two-fold:

- Prevent front-end attacks in the use-cases where this can be applied
- Enabling automatic verification without user input, thereby not disrupting the existing UX

The effectiveness of this solution relies on 3 assumptions which I think are quite reasonable and realistic:

- Metamask hasn’t been compromised
- The browser hasn’t been compromised
- The dapp developer is able to own the lookup table mapping for their dapp domain

There are obviously issues:

- It only works for Metamask and other browser-extension wallets
- It relies on proprietary browser APIs which can change
- It proposes extra work for Dapp developers
- It requires a bit more engineering though to cover use-cases which involve Dapps that deploy contracts on behalf of users and which then need to send txs involving those newly deployed contracts.

The solution is by no means complete and there are probably pitfalls I haven’t thought of yet.

## Replies

**MicahZoltu** (2021-12-03):

See [Trustless Signing UI Protocol · Issue #719 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/719) for a solution that has been around for a while, but needs a champion.

---

**hiddentao** (2021-12-03):

I remember this one. I think a contract-verified DSL is good but it still wouldn’t prevent a malicious address from being able to get your token approval, unless I’m mistaken.

The underlying transaction signature isn’t based on the DSL but just the raw transaction data.

What’s most important is verifying the actual addresses involved in the transaction, and that’s what this proposal attempts to do.

---

**MicahZoltu** (2021-12-04):

The solution to the approval problem is for contracts to implement a `transferAndCall` or `transferWithCallback` function.  There are a number of proposals out there for such a function, though I haven’t followed them all closely.  Users should not have to do 2-step approve-the-transfer just to interact with a contract, it is a problematic pattern that results in a poor UX and poor security.

I am of the belief that solving the terrible “approval required” problem should be done separately from solving the “trusted signing” problem.

---

**hiddentao** (2021-12-04):

I agree with you. And and even ERC777 - which has been around for a while - would help solve this issue. But the fact remains that people continue to use the legacy ERC-20 standard despite the existence of better solutions, not to mention the existing large collection of tokens using this standard. And not enough people are using smart contract wallets, otherwise we’d be able to solve the problem from that end.

All in all, in the short-to-medium term we still need a solution to this problem.

---

**illuzen** (2021-12-04):

Basically you want to bootstrap onto some existing authentication method like DNS or ENS, and you need some convention for linking. ENS is a good candidate, you could make the convention that both the content hash and an ETH address record need to be set and metamask can check if the contract you’re about to send a tx to is under the same name as the content you’re viewing (implies you’re using ipfs).

---

**hiddentao** (2021-12-05):

Well, most dapps aren’t deployed on IPFS - if they were this would obviously be ideal. That’s why I’m suggesting using the domain name from the URL (and this obviously assumes the browser hasn’t been compromised).

I do the like the thought of using DNS. A TXT entry could contain the address of a smart contract which can be used to verify the transaction parameters. This has the added benefit of allowing for more complex transaction parameter verification beyond the basics.

Thus, a Dapp author would optionally deploy such a contract (and change to new one by simply updating the TXT entry) if they wished to provide added security for their users.

---

**danfinlay** (2021-12-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/hiddentao/48/8003_2.png) hiddentao:

> I do the like the thought of using DNS. A TXT entry could contain the address of a smart contract which can be used to verify the transaction parameters.

This sounds backwards to me. The smart contract is the final authority on its own behavior. If wallets trusted a Ðapp’s pointer to a description of the method behavior, then phishers could mask the transactions they propose and do things related to past sites you’ve used.

I prefer proposals like natspec or eip 719 where the contract author points at descriptions of its own behavior that can be shown regardless of the calling context.

There could also be other ways of sharing descriptions of contracts, but it has to be careful about how it’s trusted, not just the site you’re on.

---

**hiddentao** (2021-12-05):

Fair points. I think EIP 719 is nice though I note that it only involves verifying the DSL and not the actual call values (e.g. the token involved in a swap). And it also wouldn’t prevent a front-end hack involving approving a malicious address as a spender of a user’s tokens.

The idea behind the suggested DNS-based solution is to verify the actual call values. So for example, when a Dapp sends a token approval request to the signer the signer can verify that the `spender` specified is the Dapp’s expected contract address and not some malicious third-party address.

We can’t have the Dapp telling the signer where to get this information verified since that can be spoofed, so the signer needs its own independent method of doing this - and this is where a DNS-based on-chain lookup (building on the browser tab domain) comes in.

I’ll admit it isn’t elegant and is only applicable to extension wallets such as Metamask but that has such a large wallet market share that I think it’s worth it.

---

**meridian** (2021-12-26):

The issue really here is how do we verify that the current application the end user is interacting with is in fact deployed by an authorized person on the team.

- Automated
- Scalable
- Works within current workflow processes

Two concerns:

- Verify that source used is what we want (no malicious supply chain, etc)
- Verify that it was deployed by an authorized process and is correct

### GitHub Deployments for Verify Deployments

TLDR: Metamask can verify that the application its interacting with was deployed by an authorized process. GitHub has such information it can use right now. Here is sushiswap’s information

```json
  {
    "url": "https://api.github.com/repos/sushiswap/sushiswap-interface/deployments/452468601",
    "id": 452468601,
    "node_id": "DE_kwDOFC8osc4a-B95",
    "task": "deploy",
    "original_environment": "Preview",
    "environment": "Preview",
    "description": null,
    "created_at": "2021-11-10T05:48:23Z",
    "updated_at": "2021-11-10T05:56:27Z",
    "statuses_url": "https://api.github.com/repos/sushiswap/sushiswap-interface/deployments/452468601/statuses",
    "repository_url": "https://api.github.com/repos/sushiswap/sushiswap-interface",
    "creator": {
      "login": "vercel[bot]",
      "id": 35613825,
      "node_id": "MDM6Qm90MzU2MTM4MjU=",
      "avatar_url": "https://avatars.githubusercontent.com/in/8329?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/vercel%5Bbot%5D",
      "html_url": "https://github.com/apps/vercel",
      "followers_url": "https://api.github.com/users/vercel%5Bbot%5D/followers",
      "following_url": "https://api.github.com/users/vercel%5Bbot%5D/following{/other_user}",
      "gists_url": "https://api.github.com/users/vercel%5Bbot%5D/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/vercel%5Bbot%5D/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/vercel%5Bbot%5D/subscriptions",
      "organizations_url": "https://api.github.com/users/vercel%5Bbot%5D/orgs",
      "repos_url": "https://api.github.com/users/vercel%5Bbot%5D/repos",
      "events_url": "https://api.github.com/users/vercel%5Bbot%5D/events{/privacy}",
      "received_events_url": "https://api.github.com/users/vercel%5Bbot%5D/received_events",
      "type": "Bot",
      "site_admin": false
    },
    "sha": "cdb7e91e645d9ac9a8c24b27adbe784afaaa66f1",
    "ref": "cdb7e91e645d9ac9a8c24b27adbe784afaaa66f1",
    "payload": {

    },
    "transient_environment": false,
    "production_environment": false,
    "performed_via_github_app": null
  },
```

Get this information by:

```sh
curl -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/sushiswap/sushiswap-interface/deployments
```

By default the `   "description":` field is left `null`. if there is need for inserting some value here for verification, etc.

## Generating a secure hash value

### Git Tag / hash



      [github.com](https://github.com/cgwalters/git-evtag)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/5/0/50e7b15badc6c27f066b94fb7e99b02810227b07_2_690x344.png)



###



Extended verification for git tags










Git EV-TAG provides a secure SHA512 algo for computing a deterministic* secure hash

```rust
fn git_evtag(repo: GitRepo, commitid: String) -> SHA512 {
    let checksum = new SHA512();
    walk_commit(repo, checksum, commitid)
    return checksum
}

fn walk_commit(repo: GitRepo, checksum : SHA512, commitid : String) {
    checksum_object(repo, checksum, commitid)
    let treeid = repo.load_commit(commitid).treeid();
    walk(repo, checksum, treeid)
}

fn checksum_object(repo: GitRepo, checksum: SHA512, objid: String) -> () {
    // This is the canonical header of the object;
    // https://git-scm.com/book/en/v2/Git-Internals-Git-Objects#Object-Storage
    let header : &str = repo.load_object_header(objid);
    // The NUL byte after the header, explicitly included in the checksum
    let nul = [0u8];
    // The remaining raw content of the object as a byte array
    let body : &[u8] = repo.load_object_body(objid);

    checksum.update(header.as_bytes())
    checksum.update(&nul);
    checksum.update(body)
}

fn walk(repo: GitRepo, checksum: SHA512, treeid: String) -> () {
    // First, add the tree object itself
    checksum_object(repo, checksum, treeid);
    let tree = repo.load_tree(treeid);
    for child in tree.children() {
        match childtype {
            Blob(blobid) => checksum_object(repo, checksum, blobid),
            Tree(child_treeid) => walk(repo, checksum, child_treeid),
            Commit(commitid, path) => {
                let child_repo = repo.get_submodule(path)
                walk_commit(child_repo, checksum, commitid)
            }
        }
    }
}
```

## Additional options

### Canary / Deadman switch

- Warrant Canaries  / CanaryTrail

https://github.com/canarytail/client

### Web Standards

**- SRI - subresource integrity**



      [github.com](https://github.com/w3c/webappsec-subresource-integrity)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/a/8/a88f3b0b5da8e53867407ff94f4b27bada60bd5c_2_690x344.png)



###



WebAppSec Subresource Integrity










[discussion for getting this to work with nextjs, a popular framework for javascript](https://github.com/vercel/next.js/discussions/23951)

### The problems with using Git for this



      [mikegerwitz.com](https://mikegerwitz.com/2012/05/a-git-horror-story-repository-integrity-with-signed-commits#automate)





###










---

All in all I think being able to leverage existing workflow output (via GitHub’s deployment records) would make it easy to maintain and for adoption. This is by no means bulletproof but I think its a good start.

Cheers,

Sam

---

**MicahZoltu** (2021-12-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/hiddentao/48/8003_2.png) hiddentao:

> Metamask uses keccak256(URL domain) as a key into an on-chain (chain being whatever chain the tx is for) lookup table which lists the expected contract addresses for that domain.

This breaks censorship resistance.  Take Uniswap for example, if they whitelisted [uniswap.org](http://uniswap.org) then users wouldn’t be able to use http://4-11-1.uniswap-uncensored.eth/, which is a clone of Uniswap that has region restrictions removed (which are present on [uniswap.org](http://uniswap.org)).

IMO, a well designed dapp should be able to be hosted on IPFS, downloaded, hosted on a traditional server, etc. and work in all contexts.  When one domain gets taken down, it should be trivial to spin up a new one by anyone (not only by permissioned actors).

---

**illuzen** (2021-12-28):

Yeah these discussions about censorship resistance are not idle fancy. Dapps need to be hydras, new heads sprouting from every attempt to control.

---

**illuzen** (2021-12-28):

I disagree with the problem description, the proper implementation of the proposed security function should also protect against malicious contracts.

This git workflow stuff is good for security, but it only checks that the frontend you are interacting with was not tampered with.

Many dapps interact with many contracts across the ecosystem, and there should be a simple way to allow people to check the outcome of a proposed transaction.

What if it was something like metamask simulates running the tx and summarizes the state changes, like in the state tab on etherscan? Something like

If you had run this transaction in the last block, you would have

- transferred 1 ETH to 0xblahblah
- received 4000 DAI from 0xblahblah2

It wouldn’t cover more subtle state changes that still might be important, but what we’re talking about is some layer that makes it easier for non-experts to do due diligence before signing a transaction.

---

**ricburton** (2021-12-30):

[![Screenshot 2021-12-30 at 06.10.59](https://ethresear.ch/uploads/default/optimized/2X/d/d803a3caa5f15ddf8227282ae619184159032960_2_494x499.png)Screenshot 2021-12-30 at 06.10.591728×1746 224 KB](https://ethresear.ch/uploads/default/d803a3caa5f15ddf8227282ae619184159032960)

We have been starting to design something around this area called: Safe Send

How else could we adapt this design and think about presenting it to customers?

You can follow our work at: https://discord.gg/safari-wallet

---

**hiddentao** (2022-01-25):

The DNS proposal wouldn’t prevent you from forking the Dapp UI onto new endpoints. A user would still be able to use a decentralized mirror version of Uniswap - they just wouldn’t have the DNS-based verification process in place. But this could be added later for that endpoint.

Ultimately, in order to verify the outcome of a call triggered in a Dapp you need an alternative source of verification that doesn’t rely on any of the code contained within the Dapp.

---

**MicahZoltu** (2022-01-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/hiddentao/48/8003_2.png) hiddentao:

> But this could be added later for that endpoint.

Whoever is in control of adding things to the registry of “acceptable domain names” would be able to decide which sites get a green check and which get a warning.  This is fine if individual users can opt in to different curators, but I don’t think it is a good solution to have an authoritative source for this information.  In particular, it discourages people using *actually* censorship resistant software like IPFS and custom IPFS gateways in favor of using centralized and censorable solutions like legacy DNS.

