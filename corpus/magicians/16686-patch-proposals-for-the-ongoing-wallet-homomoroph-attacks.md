---
source: magicians
topic_id: 16686
title: Patch Proposals For The Ongoing Wallet Homomoroph Attacks
author: rook
date: "2023-11-18"
category: Working Groups > Security Ring
tags: [opcodes, security]
url: https://ethereum-magicians.org/t/patch-proposals-for-the-ongoing-wallet-homomoroph-attacks/16686
views: 1840
likes: 11
posts_count: 26
---

# Patch Proposals For The Ongoing Wallet Homomoroph Attacks

Losses from homomorph walles has suprassed $60m: https://gbhackers.com/create2-bypass-wallet-security-alerts/

(edit) The above article is mistaken, this has noting to do with the create2 opcode, and rather a shortcut in wallet germination making it easier to search the wallet keyspace for viable wallets to use in this attack.

Even today I made a transaction, and noticed that a contract was deployed with a wallet that looks very similar to my own. So, clearly there is some shortcut here that allows the attacker to very cheaply generate similar looking wallets.

There is no question that this is a serious problem, how do we fix it?

## Replies

**shemnon** (2023-11-20):

CREATE2 isn’t what makes the attack possible.  It’s what makes it efficient and reliable.  The same “empty address” trick could be used with regular CREATE addresses as well as transaction created addresses.  The difficulty comes from the fact they are a function of the nonce, and the nonce increases one at at time.  So instead of calculating thousands of possible addresses and retrieving the one address where someone took the bait an attacker would need to create all wallets prior to the “bait” address.

Nerfing CREATE2 like this would, in a word, destroy DeFi.  Uniswap depends on this feature to calculate pool addresses that are a function of the two involved token adresses.   Any patch to make “create2 always returns the same wallet address until it is claimed” would be in effect removing the opcode.

Even if this were done scammers would change their tactics to a database of EOA addresses instead of CREATE2 contracts.

A better solution would be at the wallet UX layer, any send to an address with an empty account could either be prohibited or placed behind a scary “this is how people get scammed” dialog.

---

**rook** (2023-11-20):

(Edit: Parts of this post is just wrong, I based this post on reading the article - after some research i realized that i’m wrong. I’m leaving this post up for documentation - but skip ahead)

The calculation used by Create2 is useful in these attacks because it is a significant shortcut.   Let me explain why this patch is needed in more detail.

In the world of cryptography - cost is everything, and create2 is used in this attack because it makes it cheaper.  While it is entirely possible conduct homomorphic attacks using CPU time to find a key-pair that produces a designed wallet, this **very** expensive to conduct en-masse.  Without the create2 shortcut, the alternative is to spend *days* to find the right key-pair which produces a desired homomorph. This attack is likely more expensive than sha2-based bitcoin mining because I do not believe ECC key-generation can be easily accelerated by an FPGA or GPU due to the size of the calculation not being able to fit in the registries - forcing each loop to access slower ram thereby obviating the hardware acceleration. The computational-shortcut introduced by create2 in the generation homomophs needs to be fixed because $60m is a lot to loose.  In cryptography, shortcuts are never a good thing to keep lying around, especially shortcuts which are actively exploited for financial gain.

This proposed change to create2 was specially crafted such that it will have no adverse affects on legitimate scripts, I’m not sure why are unable to see the solution here. In my proposed change, once the contract is claimed then create2 will produce a new address (similar to popping an address off of a queue) - therefore no existing script should even notice or skip a beat.  If you can provide a legitimate script that will error out, I will be happy to design a new patch, but as it stands I do not believe any legitimate script could be affected.

I’m not sure that I understand how a UX patch would be deployed or could be standardized. Seeing as every wallet in existence is affected, fixing every wallet doesn’t sound like a reasonable patch to me.

---

**shemnon** (2023-11-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png) rook:

> Create2 is used in these attacks because it is a significant shortcut.

It’s a very good shortcut for sure, but the fact it’s a shortcut indicates it is not instrumental in the attack. “patching” CREATE2 in the way you propose

> Let me explain why this patch is needed in more detail.
>
>
> In the world of cryptography - cost is everything, and create2 is used in this attack because it makes it cheaper. While it is entirely possible conduct homomorphic attacks using CPU time to find a key-pair that produces a designed wallet, this very expensive to conduct en-masse. Without the create2 shortcut, the alternative is to spend days to find the right key-pair which produces a desired homomorph. This attack is likely more expensive than sha2-based bitcoin mining because I do not believe ECC key-generation can be easily accelerated by an FPGA or GPU due to the size of the calculation not being able to fit in the registries - forcing each loop to access slower ram thereby obviating the hardware acceleration. The computational-shortcut introduced by create2 in the generation homomophs needs to be fixed because $60m is a lot to loose. In cryptography, shortcuts are never a good thing to keep lying around, especially shortcuts which are actively exploited for financial gain.

This is more of a UX problem than anything.  This is typosquatting of a different flavour.  The real solution is to only trust the entire key, like code does at the lowest level.  Perhaps wallets should reduce the number of hex digits they elide, or adopt custom images that checksum addresses, or highlighting your address when asking to verify signed data.

Just because it’s more computationally efficient via one path does not mean cutting that off makes the world safe from the attack.

> This proposed change to create2 was specially crafted such that it will have no adverse affects on legitimate scripts, I’m not sure why are unable to see the solution here. In my proposed change, once the contract is claimed then create2 will produce a new address (similar to popping an address off of a queue) - therefore no existing script should even notice or skip a beat. If you can provide a legitimate script that will error out, I will be happy to design a new patch, but as it stands I do not believe any legitimate script could be affected.

Can you, technically, describe how the patch would be done?  Remember that CREATE2 calculates address from a set of inputs, how would that be chained within the EVM?  How would it impact prior contracts?  What the storage cost of tracking a wallet address until it is “claimed” - and what does “claimed” mean?  Is it a balance?  (attackers will just send a balance to the address as part of the attack)  Is it an external call (again, attackers will call it).

> I’m not sure that I understand how a UX patch would be deployed or could be standardized. Seeing as every wallet in existence is affected, fixing every wallet doesn’t sound like a reasonable patch to me.

Changing the fundamental math of how the CREATE2 operation works is a less reasonable patch than expecting wallets to up their UX game.

My biggest issue is that it is not attacking the core of the attack: relying on users only validating part of the address.  Instead it proposes ecosystem breaking changes on one operation that can be replaced with different (possibly less efficient) techniques.  Address typosquatting would just then move to a different technique.

---

**kdenhartog** (2023-11-20):

Good idea in terms of warning at wallet UX. I’m thinking transaction simulation services adding this feature would get it deployed more widely but I’ll see if we might be able to add this to the UI as well in the interim if the transaction simulation services don’t do it.

---

**rook** (2023-11-20):

Hey Shemnon,

This vulnerably is really screwed up, and it needs to be fixed. (edit.)

---

**rook** (2023-11-20):

I have thought about this a bit more, and removing attacker control over the *_salt* value I believe is the strongest patch here.  Legitimate code won’t care what the ultimate hash value is, and by removing the attacker’s ability to influence the hash value we will stop seeing this attack.  The salt is still needed, but it only needs to be a network-controlled nonce.

… Or if we want to keep the same call convention - we allow the salt value to be attacker controlled, and just XOR it with a Pepper value that is generated by a CSPRNG and is unique to each block.  (Pepper is the name given to a salt value that is unknown to the attacker.)

---

**wjmelements** (2023-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png) rook:

> I am one of top 10 cryptographers on StackOverflow.

Noted. I will disregard stack overflow “cryptographers” in the future. As for my credentials, I authored GPU software that makes it easier to generate addresses that match arbitrary criteria, and I have no doubt my development empowers these attackers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png) rook:

> a vulnerability is being actively exploited to steal tens of millions of dollars

There is no vulnerability. No funds are being “stolen”. “homomorphism” as you call it is intrinsic to similar addresses looking similar, and no address generation scheme is going to fix this. Enough computational work will be able to generate similar addresses, whether they are derived from EOA, `CREATE`, `CREATE2`, or some new scheme.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png) rook:

> Another way of looking at this, is that a feature in the core is making it much more difficult for the real-world to verify addresses

No it is not.

---

**wjmelements** (2023-11-21):

Another way to think about why there is no fix for this is to assume user behavior isn’t going to change. They are only going to eyeball the first 4 hexcharacters of an address. No matter the scheme, if there are more than `2**16` accounts, the system is no-longer idiot proof. This makes no assumptions about how the addresses are generated; there will be collisions.

Wallets can prevent users from doing dumb stuff but this is not the role of the EVM.

---

**rook** (2023-11-21):

Hey WJ,

Secure software takes effort, this is not something that happens by accident.  In the real world when people fall off of a banister and hurt themselves, they sue you - and the issue is fixed.  Well how is this any different?  The only difference I see is that usually when someone takes a tumble - they don’t loose $60,000,000.00 USD.  This isn’t just isn’t one person that made a mistake, and we all know that people keep making this mistake because it is a patchable software defect, and leaving bugs unpatched reflects badly upon all of us.

This pre-computation attack is only possible because of how contract address are generated. The patch is really quite simple - but convincing the community that we deserve secure software maybe more difficult than I anticipated.

---

**rook** (2023-11-21):

`Another way to think about why there is no fix for this is to assume user behavior isn’t going to change.`

If an attacker can no longer generate homomorph wallets, then people will stop sending their coins to look-alikes.  I will do absolutely everything in my power to make sure this vulnerability is patched.

But that being said. I need you start treating others with respect.  I have worked very hard to be where I am, and I am here to help others.  Flinging personal attacks someone for trying to help isn’t going to help us make a more secure network.

---

**wjmelements** (2023-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png) rook:

> This pre-computation attack is only possible because of how contract address are generated.

No, I have already proven that it is independent of how the addresses are generated.

---

**wjmelements** (2023-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png) rook:

> The only difference I see is that usually when someone takes a tumble - they don’t loose $60,000,000.00 USD

I recommend you check out some of my proposed solutions to the “finality problem”, such as EIP-3455 and EIP-6810.

---

**wjmelements** (2023-11-21):

[@rook](/u/rook) I hope you are able to understand why homomorphism is just as possible with `CREATE` and EOA as with `CREATE2`, and that your insistence that `CREATE2` makes it easier is way out of proportion. I hope you will re-read the UX proposals mentioned by everyone else in this thread because they are the solution. Scams are a cat and mouse game though; the scammers will adopt a new strategy once Metamask patches this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png) rook:

> But that being said. I need you start treating others with respect. I have worked very hard to be where I am, and I am here to help others.

I am not as patient as shemnon. My patience with you was over when you brought your cReDeNtIaLs to a technical discussion as a response to why you were wrong and tried monologuing to *us* about the importance of security. I thought that was disrespectful but I am glad you have since edited it out of your post.

---

**rook** (2023-11-21):

I am thinking about how you two are thinking about this problem in more detail. My concern is that you are intending to punish everyday users for not using “the correct software” or “not being careful enough” - when really the majority of people aren’t well versed in this topic - and just want to use a currency.

The best analogy for this argument is “You shouldn’t have clicked on that link” vs well maybe “We shouldn’t have XSS to begin with”…   and please keep an open mind in this discussion - everyone on this tread wants our users to be safe as possible and to build the very best network - I know that.  Math is the universal language after all, and I think it can help us all reason about this issue.

**Is using keccak() alone for wallet generation more of a concern than than keccak(secp256k1)?**

Is this a shortcut useful to anyone?

Let’s start of with keccak() - which is more commonly known as SHA3.  This is hash function is very interesting, it is one of the few hash functions created [specifically to be accelerated on 64bit architectures](https://keccak.team/2017/is_sha3_slow.html) and in fact we are seeing phenomenal hash-rates from [hardware acceleration](https://www.inesc-id.pt/ficheiros/publicacoes/13121.pdf).  Keyword being *accelerated*, which is the exact opposite of the bcrypt(), and PBKDF2() key-derivation functions.

Let’s assume the attacker is modifying the salt with an O(1) operation.  Now let’s assume the hacker has a modern 64bit machine at their disposal.  The address is calculated as follows:

`contract address=keccak(concatenate(sender address,nonce,code hash,salt))`

So this is a sha3() hash of 1024bits.  We will assume that the attacker isn’t using string-concatenation, but rather bit flipping the last 256bits of the message to search the key-space.  Looking up the performance we can see keccakc256treed2 takes [roughly 40 cycles per byte](https://bench.cr.yp.to/results-sha3.html) in order to calculate this hash.

That gives us:

`40 cycles * 64 bytes = 2560 cycles per hash`

Now lets assume our hackers are poor, and they purchased a used-server from eBay for a few thousand dollars.  For the purposes of this lets say the attacker with with an AMD Epyc with 64 cores at 2.66ghz.

So that gives us

`2.66 billion cycles * 64 cores = 170,240,000,000 cycles/second`

Thus yielding a theoretical maximum of:

`66,500,000 hashes per second`

Now keep in mind - the same hardware that is used in Bitcoin mining, will have a higher hashrate using keccak/sha3. This is because the sha3 hash function was created to be accelerated by hardware - where as sha2 wasn’t.

That allows for an attacker to search a very large key-space without a lot of resources.  Yes, of course this poor AMD chip isn’t going to hit its maximum today - but hardware only gets faster over time.  So this calculation will be a low-ball estimate in just a few years.

Now the fun part!  ECC key generation isn’t something that can be easily accelerated because the numbers are too large to fit in the CPU’s registries, which is an important feature of a KDF. So even if a manufacturer decided to make a hardware accelerated secp256k1, no processor has ever been created which can accelerate this calculation, where as sha3 was specifically designed to be accelerated.  This means ECC-key generation isn’t cycle-bound - its **memory-bound** - and we can see this this limit affects the calculation times.

There is another curve-ball here: secp256k1 keys are harder to generate, in fact the link below claims that it is 10 times slower on average than some of the more performant curves used in TLS. The benchmark didn’t think to test secp256k1… but we can choose some other Weierstraß curve which should have very similar performance characteristics.  By looking at the [real-world benchmarks  for ECC key generation](https://bench.cr.yp.to/results-dh.html).  For the purposes of this calculation we will use the data from ecfp256h which is also 256bit Weierstraß curve.

So if it takes roughly 31,738 cycles to generate a single key - we still to calculate the sha3() hash for 32-bytes of data:

`31,738 cycles + 40 cycles * 32 bytes`

Yielding:

`33,018 cycles per key`

Meaning that we can at most generate 5,365,197.07 keys in a second…   But wait, we know that this is wrong because no has ever generated 5 million secp256k1 keys in a second on any chip, thats impossible because this calculation **memory-bound** and not CPU-bound - which is a very useful feature to have in a KDF.

In practice, if you where to benchmark an AMD Epyc system today - I think you would get only around 40k ECC keys per second - making it 3,000 times slower than sha3() alone.

But you don’t have to take my word for it, this is all easily verifiable.  In fact, here is a wonderful discussion between cryptographers about the performance differences between SHA2 and secp256k1 key generation:



      [crypto.stackexchange.com](https://crypto.stackexchange.com/questions/29885/can-a-billion-elliptic-curve-keys-be-generated-on-a-laptop-in-less-than-an-hour)



      [![Thomas Von Panom](https://ethereum-magicians.org/uploads/default/original/2X/1/1183856a0da6f26486384b5a8b4fc627c8794dc2.png)](https://crypto.stackexchange.com/users/28406/thomas-von-panom)

####

  **elliptic-curves, keys, openssl, performance**

  asked by

  [Thomas Von Panom](https://crypto.stackexchange.com/users/28406/thomas-von-panom)
  on [01:25PM - 16 Oct 15 UTC](https://crypto.stackexchange.com/questions/29885/can-a-billion-elliptic-curve-keys-be-generated-on-a-laptop-in-less-than-an-hour)










In some sense you could think of this vulnerability as a KDF bypass, that allows the attacker to search the keyspace thousands of times faster.   If we added some value that made the contract’s hash unpredictable (otherwise known as a ‘pepper’) - then the attacker would have to search this keyspace using secp256k1 key generation instead of simple addition or string concatenation.

Using a formal memory-hard KDF like bcrypt() would also make it more difficult to search this keyspace using any method.

A reasonable patch is as follows:

`keccak(concatenate(sender address, nonce, code hash, salt ⊕ pepper))`

One could make the argument that BLOCK_HASH is a suitable nonce for this purpose because it cannot be known by the attacker when the transaction is formed - and should not be influenced in a MEV-style attack because PoS validators are no longer responsible for block assembly.

Correct me if i’m wrong with any of this, I like being wrong because it gives me a opportunity to improve.

---

**sullof** (2023-11-21):

Modifying CREATE2 in Ethereum could have far-reaching implications, as it’s pivotal for ensuring predictable smart contract addresses—a feature heavily relied upon by numerous systems. Altering it might arguably fix certain aspects, but it risks breaking existing protocols and introducing more significant issues.

On another note, setting up a local Ethereum node is indeed a viable solution for deploying contracts cost-effectively. By mimicking the mainnet environment, you can deploy and test your contracts without spending a dime, achieving the same end result. Am I wrong?

---

**rook** (2023-11-21):

[@sullof](/u/sullof)

After digging into this issue a little more, I think the article is mistaken.  It looks like it is primarily an off-chain pre-computation attack.

While, it nice to know the contract address ahead of time, this “feature” has become very useful in crime.   Knowing what I know now, I would make this calculation strictly on-chain, and emit some kind of event to notify the developer of contract’s wallet.  This is a much more straight-forward UX change then what has been proposed thus far.   Adding the BLOCK_HASH would prevent the value from being computed off-chain with virtually zero overhead… but this decision is above of my pay grade.

You bring up a really good point - developers have become accustomed to predictable addressing, and that still leaves us with a few solutions.  Using an official KDF like bcrypt() would dramatically reduce the rate by which homomorophs can be generated - without introducing too much overhead.   Legitimate blockchain operations only use this method a handful of times, where as an attacker needs to execute it many millions of times before it becomes viable in an attack.   This asymmetry in computability is very useful.

KDFs are commonly used in authentication and identity, so why not here?  Hindsight is 2020, and I don’t think anyone could have predicted the fallout from this feature. Swapping out sha3() for bcrypt() when calculating the wallet would be the solution where we can have our cake and eat it too, and by all accounts we will see a measurable impact in the rate by which funds are lost.

---

**sullof** (2023-11-21):

I built the first Host-proof Hosting password manager in 2006, and a file-system-like secret manager in 2020, and I used iterations anywhere it made sense. So, I agree with the general principle. But here we are talking of blockchain, and things are very different. The opcode must consume as little gas as possible. Implementing something like bcrypt would consume so much gas that it would make create2 unusable. Often, we must choose the best possible compromise.

---

**rook** (2023-11-22):

Correct me if I’m wrong, but I believe contract creation would be the only time this method would be used. This would have to be a new opcode, so we are the ones that set its gas consumption.

If that is the case, the gas costs could be the same cost, or be pretty similar without breaking the bank - keep in mind the major benefit is being memory-hard, not CPU hard - And “memory hard” here is just enough to knock out FPGAs GPUs taking up even 0.5kb of memory would be more than enough to obviate specialized mining-hardware, I think most KDFs don’t even use that much - but we can tune it to something that makes sense.

We would have to run some tests, but you could use a moderate number of iterations and still make a measurable impact.

---

**wjmelements** (2023-11-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png) rook:

> Is using keccak() alone for wallet generation more of a concern than than keccak(secp256k1)?

I have measured the advantage, on a `NVIDIA GeForce GTX 1050` GPU, using `profanity` and `ERADICATE2`, both by johguse. For `CREATE` I get 5.3 MH/s, and for `CREATE2` I get 182 MH/s. This is a multiplier of ~34x, which corresponds to a gain of between one and two matching hexcharacters for similar work. I don’t think this makes a huge difference, especially compared to other approaches.

Your estimate of 3000x, almost 3 hexcharacters of advantage, was based on some CPU analysis. Do you have an explanation for this discrepancy between your theory and practice?

Even if the advantage was a full 3 hexcharacters, I don’t think it’s worth slowing the EVM. The responsibility of keeping user funds safe belongs to wallets. Fool-proofing is not generally possible.

---

**rook** (2023-11-22):

[@wjmelements](/u/wjmelements)

As was mentioned prior, the article that detailed this attack is mistaken and this issue has nothing to do with create vs create2.  The create opcode does not calculate a secp256k1 key, so I’m not sure what your benchmarks are trying to prove.

We are comparing the time it takes to `sha3(1024 bits)` key vs `sha3(unique secp256k1 key)`. You are free to calculate the difference between these two, and by all accounts this should be more than a factor of 1,000, which is why its being used in this ongoing attack on the network.

I’m not sure why [@sullof](/u/sullof) and [@shemnon](/u/shemnon) liked this benchmark…

Sorry that my calculations weren’t clear, but yes - what i’m saying is that calculating a secp256k1 key is hard to do in an accelerated mode, because it is memory-hard calculation, which is common in KDF construction.  I think we all know hash functions are fast.


*(5 more replies not shown)*
