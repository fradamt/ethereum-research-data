---
source: magicians
topic_id: 1056
title: JSON UTC Version 4
author: ligi
date: "2018-08-14"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/json-utc-version-4/1056
views: 3238
likes: 10
posts_count: 19
---

# JSON UTC Version 4

I am currently implementing mnemonic support in [WallETH](https://walleth.org) - The importing part was easy (and also solved my main pain point as I wanted to import from a Ether-Card at dAppcon and had to use a different wallet for it at this time)

The problem arises when exporting. Currently I am using a key-store as used by geth. Basically a directory with JSON UTC files. Unfortunately you cannot export the mnemonic from a JSON-UTC file as the key is already derived and for exporting a mnemonic you would need the root entropy.

So the idea would be to introduce a JSON UTC file format version 4 where instead of the address field that contains a string with the address - we introduce the option of an “addresses” field that contains a list of json objects that map derivation paths to addresses.

Unfortunately it looks like JSON UTC was never really standardized (when I am wrong here - which would be great - please point me to the location where it was standardized)  - So I think the first step would be to properly standardize it (Question here: do versions 0…2 play a role somewhere still?) - and then add the new feature.

What do you think? Feedback/Ideas very much appreciated!

## Replies

**ligi** (2018-08-28):

Digging a bit deeper into this rabbit hole:

- The address was part of version 1 but was deprecated afterwards (see: https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition#alterations-from-version-1)
- Unfortunately it is still present in most files - even worse some implementations fail to import when it is missing - e.g. Trust wallet:

[![20180828_132353](https://ethereum-magicians.org/uploads/default/optimized/1X/13a26220309de52a52af723a92de2a9227afa932_2_281x500.jpg)20180828_1323531152×2048 546 KB](https://ethereum-magicians.org/uploads/default/13a26220309de52a52af723a92de2a9227afa932)

Unfortunately for some cases the address is even needed. E.g. geth needs to know about the address before the user enters the password. The problem is in the end that this file format now fulfills 2 purposes:

1. key storage inside a node/wallet (e.g. geth or WallETH)
2. key exchange format to pass on keys between different wallets

I think for case 1 it makes sense to have the address (or with the idea of v4 -multiple addresses) inside the file. For case 2 the address should not really be in there - and for sure not be mandatory. Really unsure where to go from there now. Would really like some input here from other members of the wallet ring. One direction I could imagine is to (properly) define a new format for the exchange of keys.

We should also think about removing the uuid - was talking with fjl from the geth team about it - and it is really just baggage without a clear use-case. In geth it is just generated but never really used. In WallETH I am also not using it. If you have a real use-case for the uuid here please speak up!

---

**alejandro-isaza** (2018-08-28):

The address is useful to have so that you don’t have to decode the private key to show the list of wallets.

I agree that the best way forward would be to define a new format.

---

**subtly** (2018-09-02):

[@ligi](/u/ligi) The key file is the root entropy. Anything like bip32/bip44 is out of scope. The KDF is used to turn the user’s password into a key for AES. A randomly generated seed is also used for the KDF to ensure the same password for two different keys doesn’t produce the same encryption key. Notably, the ethereum clients weren’t intended to double as software for key stores and transaction signing – it just ended up this way.

As such, if you want to export a mnemonic, then export the output of decrypting the json-utc file. Storage and tracking of addresses should be handled by your application.

Its not practical for bitcoin nor ethereum clients to store/encrypt more than that in the keystore because the chain itself is canonical for the nonce and not the file. If device A and B have the same key and device B submits a transaction, then without referencing the chain, device A will not be able to successfully create the next transaction. A perfect example of this can be seen with bitcoin: if you create a bitcoin address and create more than 20 transactions, you won’t be able to see your balance when you restore from a mnemonic because bip44 clients only look ahead 20 transactions to see if you’ve used it before. By BIP44’s standards, BTC hodlers should never spend more than 20 outputs ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) In the case of etheruem, it’d be really expensive to spend all of your funds to a new address every time you perform a transaction.

---

**ligi** (2018-09-02):

> As such, if you want to export a mnemonic, then export the output of decrypting the json-utc file.

Unfortunately this will not work as far as I see. Because if the mnemonic generated from this export will be imported in some other wallet than the user will not end up with the same address. This will be horrible UX.

> If device A and B have the same key and device B submits a transaction, then without referencing the chain, device A will not be able to successfully create the next transaction.

You always need to reference the chain anyway. You also need to do this anyway to create the transaction with EIP-155. Don’t really see your point here.

---

**subtly** (2018-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> Unfortunately this will not work as far as I see. Because if the mnemonic generated from this export will be imported in some other wallet than the user will not end up with the same address. This will be horrible UX.

If they import the seed output from the mnemonic then the Ethereum client will get the same exact address. I don’t understand. How does this happen (address being different)?

> You always need to reference the chain anyway. You also need to do this anyway to create the transaction with EIP-155. Don’t really see your point here.

Exactly my point. Apps have no way of determining the user’s previous addresses and pertinent activities, no matter how entropy is stored. Additional information needs to be retained and managed by the user.

---

**ligi** (2018-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/subtly/48/1425_2.png) subtly:

> If they import the seed output from the mnemonic then the Ethereum client will get the same exact address. I don’t understand. How does this happen (address being different)?

Because they do a BIP44 derivation …

---

**subtly** (2018-09-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> Because they do a BIP44 derivation …

So there’s the problem. I don’t think any of the main Ethereum clients use BIP44. To this day, I still don’t understand why all the wallets look at Ethereum like it is Bitcoin (it is not; the only shared aspect is secp256k1).

We decided not to use BIP44 and there a long list of reasons why. Foremost is that it adds a lot of complexity and injects a standard which is specific to Bitcoin. BIP44 is a layer on top of and strongly bound to secp256k1 and Bitcoin’s UTXO model. And, at the time we developed “JSON-UTC”, BIP44 was optional for Bitcoin and not yet the default. That de facto makes BIP44 optional. BIP32/44 were at an early-stage when we were going through audits and the only non-standard parts of Bitcoin’s cryptography that had gone through a thorough audit was secp256k1 (thanks to Pieter Wuille who also created BIP32).

What information might be missing here, and with all wallets, is that BIP32 is very specific to Bitcoin and it has a lot of sharp edges which are counterintuitive. In the context of Ethereum, BIP32’s functionality is redundant and perhaps *misleading*. BIP32 was *NOT* created for supporting multiple accounts – it is for creating multiple *LINKED* accounts for use *with* a UTXO model, specifically such that every transaction can be linked to every other transaction. This is juxtaposed to Ethereum’s account and transaction model and poses a risk to privacy. Ethereum could use an HD KDF for accounts, but if we did that, its not clear what happens if future releases support curves other than secp256k1 (in such cases, BIP32s linkability wouldn’t work, rendering it as useless vs. an ordinary HKDF). This wasn’t postulation, as metropolis and serenity were already being considered (both of which hypothetically support non-secp256k1 curves via account abstraction).

With BIP44, there’s no reliable way to figure out the user’s current address, which addresses they have balances on and which addresses they don’t – it is literally a brute-force process. That’s not fun at all. And since Ethereum has nonces and doesn’t use UTXO, BIP32 is redundant and adds unnecessary complexity vs. a normal HKDF.

So its simple to support both. When someone restores a mnemonic, you check both. Preferably, a wallet would not ask someone to extract their native Ethereum private key into a mnemonic. I also firmly believe there are safer ways of handling this.

Needless to say, I wish I had more time and cycles to work on this. Just not there yet! ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**ligi** (2018-09-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/subtly/48/1425_2.png) subtly:

> I don’t think any of the main Ethereum clients use BIP44.

As far as I see all clients that support mnemonic use BIP44 - unfortunately it seems this already established as a standard - it just filled a void. Now we have to deal with the reality out there.

So as far as I see Metamask is using it - TREZOR is using it - MyCrypto is using it - MEW is using it - Trust wallet is using it  - Ethercards is using it - basically everything I tried is using it. And going away from it means becoming incompatible. If you know a wallet that supports mnemonics and does not use BIP44 - please let me know!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/subtly/48/1425_2.png) subtly:

> So its simple to support both. When someone restores a mnemonic, you check both.

How would I check both? Let’s say there are no funds on either address - no transaction yet. But e.g. by the ethercard where the mnemonic is printed on also has the public key printed on it (which uses BIP44) - as a wallet I have no chance to know this …

What we could do: define a Ethereum specific mnemonic standard that uses different words so wallets can detect what standard is being used. We might even have to change the amount of words as some implementations are not actually checking against the words in the list when importing AFAIK. This one then would not be based on BIP44. I would like and support that actually - but we still have to deal with the current reality - so I would still progress with the current plan. I do not see a blocker in your line of arguments - Sure it is not super nice - but we now have to deal with the reality out there …

---

**subtly** (2018-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> If you know a wallet that supports mnemonics and does not use BIP44 - please let me know!

cpp-ethereum, geth, parity, some custom custody systems and I’m sure there are others. I, and a lot of other people use these clients for signing transactions because they’ve been battle tested. I can also move around accounts from one to the other in complete confidence. I couldn’t sleep at night if I had to use mnemonics to manage my accounts.

> the public key printed on it (which uses BIP44) - as a wallet I have no chance to know this

If the user is recovering from a mnemonic, something wrong has happened. Objectively, there is no way to know which of the possible accounts they need to restore. As a recovery operation which requires the user to enter a plaintext secret, it’s can be assumed that the account is compromised. So a solution would be for the wallet to offer to restore all the accounts and flag them as “restored !” with a noticeable warning. A sophisticated user will be able to handle the situation.

Its important to point out here that, with **non**-BIP32 address you will always absolutely know the address. With BIP44 addresses, you have no way of knowing. Further, there are different varieties of BIP44 for Ethereum as not all wallets use the same BIP44 path and some may use different words!

> I would like and support that actually - but we still have to deal with the current reality - so I would still progress with the current plan.

Sadly, this is how we got here. Everyone said the same thing and opted to use Bitcoin BIP32 because that was the current reality. The reality is compromising privacy and simplicity for convenience which is completely counter to the purpose of cryptography. Everyone changed from non-BIP32 to BIP32. Just as well, there is nothing blocking the path to building a better and more thought-out standard.

I’d really like to see through rebuilding new standards. Plus, we need to sort out how to handle things like encryption, digital signatures, M of N schemes and supporting other cryptography. Doing that will net more traction than wallet usability and will necessarily require deprecating the idea that bip32 is mandatory.

> so I would still progress with the current plan

What is the current plan? ![:sunny:](https://ethereum-magicians.org/images/emoji/twitter/sunny.png?v=12)

---

**ligi** (2018-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/subtly/48/1425_2.png) subtly:

> If you know a wallet that supports mnemonics and does not use BIP44 - please let me know!

cpp-ethereum, geth, parity, some custom custody systems and I’m sure there are others. I, and a lot of other people use these clients for signing transactions because they’ve been battle tested. I can also move around accounts from one to the other in complete confidence. I couldn’t sleep at night if I had to use mnemonics to manage my accounts.

geth for sure does not support mnemonics. I am also pretty sure cpp-ethereum does not support mnemonics. Not sure about parity though ( [@5chdn](/u/5chdn) can you help here?)

Actual users out there use mnemonics - if you like it or not - we really have to deal with this …

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/subtly/48/1425_2.png) subtly:

> the public key printed on it (which uses BIP44) - as a wallet I have no chance to know this

If the user is recovering from a mnemonic, something wrong has happened.

What would be the purpose of mnemonics then if not recovering an account from it. People actually use this to backup accounts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/subtly/48/1425_2.png) subtly:

> What is the current plan?

what I was writing in the initial post here

---

**MicahZoltu** (2018-09-07):

Parity wallet UI supported mnemonics, but the Parity wallet UI has been deprecated (no longer officially supported by Parity).

---

**MicahZoltu** (2018-09-07):

I recommend everyone involved in the discussion about BIP44 read these threads:

https://github.com/ethereum/EIPs/issues/84

https://github.com/ethereum/EIPs/issues/85

It is long, but if you want some quick summaries (by yours truly):

https://github.com/ethereum/EIPs/issues/84#issuecomment-292324521

https://github.com/ethereum/EIPs/issues/84#issuecomment-292402851

https://github.com/ethereum/EIPs/issues/85#issuecomment-406811458

---

**brunobar79** (2018-09-07):

I think this is somehow relevant to this conversation: https://github.com/MetaMask/eth-ledger-bridge-keyring/issues/7

Long story short: Per [BIP 44 spec](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki),  the derivation of accounts should stop at first account without transaction.

AFAIK, That is a problem because there is no easy way in Ethereum to look at all transactions that are relevant to a given account

cc: [@danfinlay](/u/danfinlay)

---

**ligi** (2018-09-07):

Thanks for the links [@brunobar79](/u/brunobar79) and [@MicahZoltu](/u/micahzoltu)  - will read deeply after ETHBerlin. But skimming them shallowly (and was aware of some already) reinforces my belief BIP44 plays a role in Ethereum and I am not fully on the wrong path here.

---

**5chdn** (2018-09-19):

Hi [@ligi](/u/ligi)

```auto
curl --data '{"method":"parity_newAccountFromPhrase","params":["stylus outing overhand dime radial seducing harmless uselessly evasive tastiness eradicate imperfect","hunter2"],"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST localhost:8545
```

https://wiki.parity.io/JSONRPC-parity_accounts-module#parity_newaccountfromphrase

---

**ligi** (2018-09-19):

Thanks. When I look at this documentation correctly you can import but not export - on an API level this does not look so bad - but I really miss this in apps then. Also IMHO has some nasty UX traps.

---

**axic** (2018-09-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> JSON UTC

Btw, where does this name comes from? From the fact that the filename usually is an UTC timestamp + address?

How about giving it a proper name? ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**ligi** (2018-09-24):

I am all for renaming or giving it a name in the first place ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

Currently leaning a bit towards completely discarding the old standard and creating a completely new one. The old “standard” carries some baggage we really do not have to carry. For the new one we can even make some automatic check to see if a file complies to the standard so the past do not repeat …

Any good ideas for names?

