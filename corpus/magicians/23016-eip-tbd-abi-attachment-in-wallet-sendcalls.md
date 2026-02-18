---
source: magicians
topic_id: 23016
title: "EIP-TBD: ABI attachment in wallet_sendCalls"
author: frangio
date: "2025-02-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-tbd-abi-attachment-in-wallet-sendcalls/23016
views: 128
likes: 1
posts_count: 5
---

# EIP-TBD: ABI attachment in wallet_sendCalls

Discussion topic for [EIP-TBD](https://github.com/ethereum/EIPs/pull/9422).

> This EIP extends EIP-5792 with a new interfaces capability, whereby an application can attach the contract interface specifications (aka. ABIs) that the wallet needs to reliably decode the calldata in the request.

#### Update Log

- 2025-02-27: Add EIP: ABI attachment in `wallet_sendCalls` by frangio · Pull Request #9422 · ethereum/EIPs · GitHub

#### External Reviews

None as of 2025-02-27.

#### Outstanding Issues

None as of 2025-02-27.

## Replies

**SamWilsn** (2025-02-27):

I am *vehemently* opposed to this idea (though I am not a wallet developer, so my opinion likely carries little weight).

The idea that a random website can supply ABIs that the wallet will use to decode calldata is **flatly unsafe**.

Take, for example, the following contrived example:

```solidity
contract Evil {
    function collate_propagate_storage(bytes16 arg) external { /* ... */ }
}

contract Victim {
    function burn(uint256 arg) external { /* ... */ }
}
```

Both of these functions have the same function selector ([0x42966c68](https://www.4byte.directory/signatures/?bytes4_signature=0x42966c68)), but they clearly have different meanings.

If an attacker were to supply the ABI for `Evil` to the wallet, when `Victim` was actually deployed at that address, the wallet would happily display:

> The dapp is attempting to call collate_propagate_storage(0x00..01)
> Approve Reject

When in reality the attacker would be burning 34028…11456 tokens.

*(Please forgive the slightly imperfect attack sketch here; I’m aware that the encoded lengths will not match, but if I was willing to put in more effort, I could find a better collision.)*

**This is unacceptable behaviour for a wallet. Full stop.**

This proposal *needs* some form of verification. Maybe the contract has a function returning an ABI hash, I don’t know.

---

Even though this proposal is somewhat salvageable, I don’t believe it needs to exist at all. The infrastructure for wallets to decode transaction calldata exists today and just needs implementation. Something like this:

1. Fetch the contract code from the chain.
2. Using the embedded IPFS hash (or a centralized service like Etherscan), retrieve the source code of the contract.
3. Compile the contract.
4. Verify that the compiler output matches the contract code on chain.
5. Use the generated ABI to decode the transaction.

---

**bumblefudge** (2025-02-28):

Dispassionately, I would simply ask how this works (or doesn’t) with an ABI registry like sourcify? Whether or not the capability *needs to exist* or not, it could at least be made safe with some kind of proviso that it is inherently unsafe without double-checking that ABI, at least against a trust registry or service…

---

**frangio** (2025-02-28):

I believe I tried to address these points in the initial draft so I would ask if you could engage with that. From Motivation:

> The wallet can try to use a database of function selectors to try to guess an ABI, but this will fail for new and unknown contracts, and known selectors can be ambiguous due to collisions, including those deliberately introduced by attackers. Alternatively, the wallet can obtain an ABI from a repository of verified source code, with the downside that the main such repository is managed by a centralized party.

This is slightly different from what [@SamWilsn](/u/samwilsn) proposes. I don’t think we can expect a hardware wallet to be able to compile a contract, it likely doesn’t even have access to the code on chain. It’s not even clear to me that a mobile wallet could compile it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bumblefudge/48/7449_2.png) bumblefudge:

> it could at least be made safe with some kind of proviso that it is inherently unsafe without double-checking that ABI, at least against a trust registry or service…

Yes, this is exactly what I was thinking:

> Wallets MAY validate the provided specs against a database of verified or trusted specs.

A wallet could either choose not to use an untrusted spec at all, or use it while warning the user that it’s not able to verify it.

The wallet’s job is to give the user tools. The user can make an informed decision about who or what to trust. If a user trusts an application, why shouldn’t their wallet be able to build on that trust to give them a better (safer!) experience.

The trust may not even be on the application. Imagine that the user has Rabby on their desktop computer connected to a hardware wallet signer, Rabby is able to obtain the ABI without trusting the application (e.g. by fetching and compiling the source code), and is then able to pass on the ABI to the hardware wallet using this capability. Of course there is a risk that Rabby or the computer could be compromised, but what is the alternative… to only sign hex bytestrings on the hardware wallet?

I am not going to say that every wallet should blindly implement this, enable it by default, and trust every random website, as my initial draft already made clear. But I believe this is a tool that absolutely *needs to exist*.

---

**SamWilsn** (2025-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> I don’t think we can expect a hardware wallet to be able to compile a contract

That’s a good point. For low-powered hardware wallets, we probably need a different solution. Maybe some kind of signed message from a centralized authority (eg. GridPlus/Ledger loads Etherscan’s public key on the device, and only accepts ABIs signed by that key).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> it likely doesn’t even have access to the code on chain

Ideally, I’d like to see hardware wallets become light clients, but that’s a long way out (if it ever happens).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> bumblefudge:
>
>
> it could at least be made safe with some kind of proviso that it is inherently unsafe without double-checking that ABI, at least against a trust registry or service…

Yes, this is exactly what I was thinking:

> Wallets MAY validate the provided specs against a database of verified or trusted specs.

If you’re already checking the ABI against a trusted source, why not just use that trusted source?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> A wallet could either choose not to use an untrusted spec at all, or use it while warning the user that it’s not able to verify it.

Imagine the flow:

1. User navigates to a dapp they think they trust.

The dapp has been hacked, or perhaps they mistyped the URL.
2. The user goes about their business on the dapp, constructing a transaction, filling in all the details they want, and submits it to the wallet.
3. The wallet displays a function call containing all the information they entered on the dapp, along with the warning “The following function signature could not be verified”.

What do you think the user is going to do? Are they going to (a) check that the function name and arguments match what they entered in the dapp, or (b) panic and assume the dapp was compromised? I believe the answer is going to be (a). The average user isn’t going to understand exactly how an ABI can be faked, and they aren’t going to take the time to learn.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> The wallet’s job is to give the user tools.

There’s a difference between giving the user a circular saw with proper blade guards and a knife without a handle.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> The user can make an informed decision about who or what to trust. If a user trusts an application, why shouldn’t their wallet be able to build on that trust to give them a better (safer!) experience.

Users trust their wallets. Wallets need to be defensive. I’m not advocating for not decoding calldata. I think decoding calldata is an excellent idea. Using dapp-provided ABIs is just not safe, and there are workable alternatives that are.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> The trust may not even be on the application. Imagine that the user has Rabby on their desktop computer connected to a hardware wallet signer, Rabby is able to obtain the ABI without trusting the application (e.g. by fetching and compiling the source code), and is then able to pass on the ABI to the hardware wallet using this capability. Of course there is a risk that Rabby or the computer could be compromised, but what is the alternative… to only sign hex bytestrings on the hardware wallet?

This is a different problem altogether. The interface between a frontend on your PC and your hardware wallet doesn’t have to match the interface between a dapp and your frontend. Obviously similar concerns apply here (a compromised PC could send a faked ABI to your hw wallet), but this vector is less likely.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> I am not going to say that every wallet should blindly implement this, enable it by default, and trust every random website, as my initial draft already made clear. But I believe this is a tool that absolutely needs to exist.

I think you’re putting the emphasis in the wrong place. The feature “decoding calldata” needs to exist, but this particular implementation does not.

