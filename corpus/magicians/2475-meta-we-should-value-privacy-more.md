---
source: magicians
topic_id: 2475
title: "Meta: we should value privacy more"
author: vbuterin
date: "2019-01-18"
category: Magicians > Primordial Soup
tags: [privacy]
url: https://ethereum-magicians.org/t/meta-we-should-value-privacy-more/2475
views: 11452
likes: 59
posts_count: 28
---

# Meta: we should value privacy more

Right now, Ethereum privacy is quite lacking. There are two reasons why. First, all of your activity is by default done through a single account, so it is all linkable on-chain. Second, and more insidiously, even if you have multiple accounts that you split your activity between (ideally, the default would be to use a different account for each application), the fact that you need to transfer ETH between accounts to pay for gas on all of them is itself a privacy leak.

This is a situation that could use improvement. Two areas come to mind.

#### Mixers

We can encourage the development of easy-to-use, and importantly decentralized (ie. not just “trustless”, *completely serverless*) mixers targeting privacy-preserving transfer of small amounts of ETH, so if you want to send gas payment to another account you can do so without linking the two.

Note that here, one major challenge with (eg. ringsig or zk snark based) smart contract mixers is that if you want to send funds from A to B, B still needs to have ETH to pay gas to submit the proof to receive their funds, and sending that gas would be a privacy leak; this can be solved with a layer-2 protocol where a user can broadcast their proof (including a commitment to what address they want to receive to and what fee they are willing to pay) over something like Whisper, and a specialized set of nodes could accept these proofs, include them into a transaction and pay for the gas, and collect the fee from the recipient. But this protocol needs to be specced out, standardized and implemented…

#### UX

If we make a default that for every dapp, a user uses a separate account, we have to overcome a few challenges:

- Address generation: It would be nice to keep wallet software stateless, so users can easily export and import their keys between wallets; this implies using some deterministic scheme like privkey_for_dapp = hash(master_key + dapp_id). But then what is the dapp_id? How would that work for multi-contract dapps?
- Dapp interaction: The most common category here is using ERC20 tokens inside another dapp. What is the workflow by which they would do that? To use KNC on Uniswap, would you first transfer KNC from their “Kyber account” to your “Uniswap account” and then do whatever you wanted to do with Uniswap? Something else? Ideally from a UX point of view, it would still feel like the user makes one operation; the UX of dapps that requires users to sign three transactions in a row to do something honestly really sucks.

Have people here thought about these issues more deeply?

## Replies

**AtLeastSignificant** (2019-01-18):

To be clear, the issue with using one account - or transacting between multiple accounts you own, effectively making it a single “profile” - makes it easier to identify people in meaningful ways.

For example, I can look at things like where addresses are getting their ETH/tokens from, which leads to eventually to an exchange.  Exchanges help identify potential attack vectors for spear phishing, but it also reveals some geographic information.  The times that these transactions occur also helps to narrow locale.

I can see what Dapps an entity is using, which helps point me towards where these users may be reachable on social media.

You can even profile what kind of wallet scheme their using.  Whether they have a cold storage address, are just using MetaMask or some other hot wallet, etc.  This helps to know how difficult it would be to attack the user.

There’s a ton of meta information on top of the obvious X sent Y to Z.

This problem becomes exponentially worse when you add it to things like airdrops or giveaways where many people are associating their social media identity with their address.  Anything that can be used to tie an address down to any other identifiable information makes this blockchain meta-information *very* powerful to attackers.

There’s also the concern for big data mining operations / government conspiracies that may not be so far fetched that are applying deep learning algorithms to all of this to pain a bigger picture.

---

The problem with mixers/privacy layers/Dapp support is that they aren’t usually trustless *and* easy.  If possible, I’d rather see privacy built into the base protocol and not be an option for users.  They should have to explicitly prove a transaction, not explicitly hide them.

---

**jochem-brouwer** (2019-01-18):

**Dapp interaction**

This is an idea for `CREATE2` which can be applied in some situations. We use the fact that we can precalculate the `CREATE2` address - which means we can transfer tokens here and we can even supply a salt! It is applied to ERC20 tokens where we try to semi-interact with contracts in a single TX.

The idea is that an user transfers tokens to the address which is precalculated by seeding the address of the user together with the calldata. Knowing these values proves that the user wants to “deposit” the value which is currently the balance of the precalculated address together with the calldata. Hence the seeded data in `CREATE2` is the address of the user and the calldata.

Now let’s say we have an useless dummy contract to show the usage. An user A wants to transfer tokens to B but not directly. This useless `SplitContract` is deployed and we can now calculate the `CREATE2` address where A should deposit: the salt is simply the address of A and B and the init_code simply transfers all tokens at the `CREATE2` address to `SplitContract`. When we created the contract at the address where A deposited to in the `SplitContract` we hence knew the seed so at this point we also know address `B`. We can calculate how many tokens were transferred and now transfer all tokens to B. Note that the `CREATE2` contract can be selfdestructed immediately after we transferred tokens (hence yielding extra used gas of about 11k (~32k contract deployment, 22k refund, ~1k execution cost).

This is of course rather stupid but it can be expanded. Think of a DDEX: here you can match someones trade by transferring tokens to a certain address. The only thing the user now needs to do is to broadcast that these tokens are deposited and either the maker of this order can now take them or the user includes a fee for someone else to ““mine”” this token on-chain which gives them incentive to pay for this gas. (This fee is hence in the `calldata` / salt). If the order is not matched the user can go on-chain to withdraw their tokens by simply providing the supplied calldata and showing that the user wants to cancel the order (to prevent the contract to try to match the order again). (Or the order is fulfilled already).

Notice that in the DDEX cases the contract is also only created and selfdestructed so no code is deposited, yielding a low amount of extra gas. The only downside in the implementation-side is that you can’t selfdestruct, create2 it again, and selfdestruct it again in the same tx which means you have to deposit code if you want to call back into this contract for some reason. When thinking about this I can also see why it would be really nice to have some kind of memory between call frames, something EIP 1283 tries to accomplish.

---

**jpitts** (2019-01-18):

I’m interested also in how this applies to “account contracts”, which are essentially multisigs for a single person but with private keys on different devices + a recovery mechanism.

Account contracts make Ethereum more usable and help safeguard against loss of access to someone’s most important dapps, but they make privacy more challenging due to encouraging users to have a single point of entry to many dapps.

---

**burrrata** (2019-01-18):

[@AtLeastSignificant](/u/atleastsignificant)

I agree that privacy by default is the only real solution. If it’s a choice, there’s always going to be incentives to trade information for access. Trading data for services is the default for major applications on the web today, and it’s what users are accustomed to, so they won’t even question it. Also, if it takes extra effort for developers or users to create privacy, and there are no economic incentives for doing so, then it’s an just an inconvenience at best and a sub optimal game theoretic business decision at worst. Better to have options for privacy than not, but like we see with 2FA and password managers today, they’re the exception and not the norm.

An idea that could help with geographic analysis via IPs and such might be dandelion routing. From what I understand it routes a tx between peers a certain number of times before having that tx broadcast to the network. This way you can’t tell where a tx originated from, but you would still be able to see which address is sending what to whom.

- https://github.com/mimblewimble/grin/blob/master/doc/dandelion/dandelion.md

edit: realized danelion routing would help with network analysis, but not tx analysis.

---

**boris** (2019-01-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> mixers targeting privacy-preserving transfer of small amounts of ETH, so if you want to send gas payment to another account you can do so without linking the two.

This seems like a doable first task. The second part about Whisper etc. etc. seems like there are a lot of rabbit holes to go down. If we get these simple mixers, one can start by having users actually generate multiple accounts and not immediately link them. Still relies on OPSEC of the user, but a good start for simple dApp usage.

On the UX front, this is mainly a middleware and best practices issue. Can we help out wallets / web3 providers succeed at making this easier to set / generate accounts per dapp?

Do we use URL or IPFS hash as dapp identifiers? (think middleware) – or, of course, as you say, the contract address of the dapp.

I think starting with multiple accounts and multiple keys may not be ideal, but all of our single account solutions for securing / generating keys still work.

---

**vbuterin** (2019-01-19):

Privacy by default for everything a la ZEXE would be really nice, but it’s still far away, and not something that could be easily done technologically. What I’m proposing here is some low hanging fruit that can reduce the extent to which users’ activities are all immediately linked to each other. It’s nowhere close to total privacy, but it’s a very significant improvement.

> This seems like a doable first task. The second part about Whisper etc. etc. seems like there are a lot of rabbit holes to go down.

True, but making a mixer that doesn’t have the “deanonymize yourself by paying for gas” issue *requires* a layer 2 messaging protocol for things other than transactions (unless the way we want to solve this is by adding some limited form of base-layer abstraction…)

---

**ligi** (2019-01-21):

Great initiative!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> deterministic scheme like privkey_for_dapp = hash(master_key + dapp_id) .

wonder if we could also use a scheme like [@bitgamma](/u/bitgamma) was once proposing in another context ([Non-wallet usage of keys derived from BIP-32 trees](https://ethereum-magicians.org/t/non-wallet-usage-of-keys-derived-from-bip-32-trees/1817)) - so we would use different BIP-32 paths for each dApp.

This would have the advantage that  we could directly use it with existing hardware wallets. In the above scheme hardware wallets would need to implement a new function to be compatible. The disadvantage would be that the chance of collisions between dapps is higher. But it would still be better than the status quo.

---

**juniset** (2019-01-23):

Hey! This is something that we have started investigating for our smart-contract based wallet Argent. We are working on the mixer but have not yet started tackling the “deanonymize yourself by paying for gas” issue. We were planning on looking at some form or meta-transactions for that which is essentially what you [@vbuterin](/u/vbuterin) are suggesting. Will let you know if we find something even partly satisfactory.

[@jpitts](/u/jpitts)  I agree that “account contracts” pose a challenge for privacy but I also think they are nicely positioned to bring solutions to users.

---

**vbuterin** (2019-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> wonder if we could also use a scheme like @bitgamma was once proposing in another context (Non-wallet usage of keys derived from BIP-32 trees) - so we would use different BIP-32 paths for each dApp.

Yeah, I would definitely support reusing BIP32 for this.

> We were planning on looking at some form or meta-transactions for that which is essentially what you @vbuterin are suggesting

I personally hope there could be a coordinated effort to get meta-transactions or whatever other scheme figured out and made in a way that anyone can use. It’s just too useful. Maybe it requires finally getting something like whisper working well; would be good to have more discussion…

---

**bitgamma** (2019-01-23):

We got a step further with the EIP proposal and it is now [a draft](https://eips.ethereum.org/EIPS/eip-1581)

They way it is currently written would already allow this use case by defining a “dApp” key type (the document defining all key types is still WIP) and then each dApp gets an identifier.

If it is desired to keep a register of dApps, then simply using the key_index already defined would make the job.

Otherwise, for each dApp a 128-bit GUID can be generated and split in 4 32-bit integers which would be used as sublevels of key_type (hierarchy having no specific meaning, but just being used to get longer IDs). 4 bits of this identifier would probably need to be set to a fixed value since they are interpreted as hardened/unhardened derivation, but we would still have enough bits to avoid collisions.

What do you think? Does this cover the use case?

---

**ligi** (2019-01-23):

I think a dapp registry would be nice anyway. But think the GUID version is more practical and we can start without waiting for dApp support.

---

**gravityblast** (2019-01-28):

Could we derive the GUID from the hostname? if a dapp has its own .eth domain it should be ok I think.

---

**ligi** (2019-01-29):

not all dApps have an URL/hostname

---

**gravityblast** (2019-01-29):

yeah it might be a requirement or we can use the swarm/ipfs hash but upgrades would be more  difficult

---

**ligi** (2019-01-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gravityblast/48/1477_2.png) gravityblast:

> yeah it might be a requirement

I would signal we not make this a requirement

---

**bitgamma** (2019-01-30):

I have updated the draft to allow the key_index field to encode larger identifiers, spanning across several derivation levels. It is quite generic to allow any kind of identifier to be used. Additional EIPs can define specific use cases, remaining compatible to the EIP-1581 specs.

The changes are already here: https://eips.ethereum.org/EIPS/eip-1581

Of course further changes can be discussed as needed.

---

**jpitts** (2019-02-26):

[@vbuterin](/u/vbuterin) and others in this thread, this “App Keys” proposal from [@danfinlay](/u/danfinlay) and [@Bunjin](/u/bunjin) addresses some of your concerns here.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bunjin/48/1580_2.png)
    [EIP ERC App Keys: application specific wallet accounts](https://ethereum-magicians.org/t/eip-erc-app-keys-application-specific-wallet-accounts/2742) [EIPs](/c/eips/5)



> Hi everyone,
> Our research at MetaMask has lead us to propose the following EIP and we would very much appreciate if the community gave us feedback such that we can come to an agreement on a standard that would be appropriate both for wallets and applications developers to guarantee cross-compatibility.
>
>
> Simple Summary:
> Among others cryptographic applications, scalability and privacy solutions for ethereum blockchain require that an user performs a significant amount of signing operations. It…



      [github.com](https://github.com/ethereum/EIPs/blob/c0608fbcfa9c541431e6ed2efd1c3160ded49c1a/EIPS/eip-draft-app-keys.md)





####



```md
---
eip:
title: App Keys: application specific wallet accounts
author:
Vincent Eli [Bunjin](https://github.com/Bunjin)
Dan Finlay [DanFinlay](https://github.com/DanFinlay)
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2019-02-20
requires (*optional): BIP32, BIP43, EIP137, EIP165,
replaces (*optional): EIP 1581
---

## Simple Summary

Among others cryptographic applications, scalability and privacy solutions for ethereum blockchain require that an user performs a significant amount of signing operations. It may also require her to watch some state and be ready to sign data automatically (e.g. sign a state or contest a withdraw). The way wallets currently implement accounts poses several obstacles to the development of a complete web3.0 experience both in terms of UX, security and privacy.
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/c0608fbcfa9c541431e6ed2efd1c3160ded49c1a/EIPS/eip-draft-app-keys.md)

---

**danfinlay** (2019-02-26):

Thanks for drawing my attention here, [@jpitts](/u/jpitts)! Hadn’t seen this one yet.

A couple of my answers to the questions by [@vbuterin](/u/vbuterin) that are not addressed in the linked EIP:

> How would that work for multi-contract dapps?

Our current EIP assigns a unique `domain` string to whatever app it connects to, this should be the most secure string we can attribute to the loading site, so public key, site hash, or ideally ENS address is presented as our preferred initial solution.

This allows many keys to be assigned in many ways, and all that is needed to allow multiple domains to then seamlessly integrate is a delegation system for these app keys, which can/will be part of a later proposal.

> Ideally from a UX point of view, it would still feel like the user makes one operation; the UX of dapps that requires users to sign three transactions in a row to do something honestly really sucks.

I totally agree. We are definitely building towards making the initial sign-in increasingly look like a coherent contract that sets terms that allow the app to accomplish the user’s goal with minimal subsequent approvals, while enforcing hard restrictions under the hood based on those terms.

---

**virgil** (2019-02-26):

I suggest back-burning all but the simplest privacy initiatives until we’ve solved our problems.  Ethereum is already such disruptive technology.  And private disruptive tech is even more dangerous.  We want someone else to take the brunt of the privacy.  I suggest we work on other issues (scaling, UX, DevX, economic efficiency, etc.) while letting Zcash et al. lead the privacy charge.  We can look at what they did right/wrong and then play fast follower and not make as many social mistakes as we would if we moved first.

---

**vbuterin** (2019-03-05):

> I suggest back-burning all but the simplest privacy initiatives until we’ve solved our problems. Ethereum is already such disruptive technology. And private disruptive tech is even more dangerous.

I can see where you’re coming from, though OTOH *non-private disruptive tech* is also dangerous (see: recent Facebook scandals etc etc). What we’re suggesting here isn’t full-scale ZEXE, it’s just the minimal simplest level of unlinking needed to ensure that all of a user’s activities, particularly non-financial ones, can’t be trivially publicly linked to each other.


*(7 more replies not shown)*
