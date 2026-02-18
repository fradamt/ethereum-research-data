---
source: magicians
topic_id: 121
title: Let's talk about signed data
author: jpitts
date: "2018-04-09"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/lets-talk-about-signed-data/121
views: 2463
likes: 3
posts_count: 1
---

# Let's talk about signed data

The following discussion took place on the ethereum/EIPs gitter channel. It relates to geth’s approach to signed data in eth_sign, and eth_personalSign and the closed [EIP 191](https://github.com/ethereum/eips/issues/191) specification for how to handle signed data in Ethereum contracts.

Many interesting points are made and subtopics explored, including perceived vs. actual safety of signing, the principle of least surprise in the mind of developers, and whether an agreed-upon signing format warrants standardization.

> Micah Zoltu @MicahZoltu 02:29
> Where does one go to discuss EIPs now (like 191)? Previously, it happened in a PR which was kind of terrible, but now I am not sure where to go. Do I just submit a PR with the change I think should be made and debate its merits there?
>
>
> Nick Johnson @Arachnid 02:30
> Wherever the discussions-to URL on the EIP says you should go
> And yes, you can do that too - tag the authors of the draft.
>
>
> Micah Zoltu @MicahZoltu 02:30
> There is no discussion URL.
>
>
> Nick Johnson @Arachnid 02:30
> Perhaps you should send in a PR adding one
>
>
> Sumant Manne @dpyro 02:30
> check the issues tab on github
> there’s more discussion there i believe
>
>
> Micah Zoltu @MicahZoltu 02:30
> I want to do my monthly “get rid of the 0x19 prefix because it is pointless” argument but I don’t know where is best to piss into the wind.
>
>
> Nick Johnson @Arachnid 02:32
> @MicahZoltu I don’t think I’ve heard that argument before.
> You could post it to the Ethereum Magicians board, referencing the relevant EIP(s)
>
>
> Sumant Manne @dpyro 02:32
> if there’s not one, i don’t see why you cant start an issue
>
>
> Micah Zoltu @MicahZoltu 02:32
> The TL;DR: is that the 0x19 prefix doesn’t solve any real problems and it creates a false sense of security that have caused many (smart) people to screw up.
>
>
> Nick Johnson @Arachnid 02:33
> There’s the original #191: ethereum/eips#191
>
>
> Sumant Manne @dpyro 02:33
> ethereum/EIPs#191 ?
>
>
> Nick Johnson @Arachnid 02:33
> @MicahZoltu Really? Without some kind of prefix, what prevents something being valid transaction data?
>
>
> Micah Zoltu @MicahZoltu 02:33
> Yeah, but that one is closed which means it won’t get any visibility.
>
>
> Nick Johnson @Arachnid 02:33
> I’d open a thread on Ethereum Magicians, and maybe send in a PR adding it as the discussions-to URL
>
>
> Sumant Manne @dpyro 02:33
> oh, if you think there’s something useful to talk about, why not just open an issue based on it?
>
>
> Micah Zoltu @MicahZoltu 02:33
> @Arachnid Nothing. The issue is that preventing them from being real transactions doesn’t actually fully solve a real problem, it solves half a problem and lulls people into thinking the whole problem is solved (when it isn’t).
>
>
> Nick Johnson @Arachnid 02:33
> Issues don’t have great visibility and aren’t a great way of holding general discussions either.
>
>
> Sumant Manne @dpyro 02:34
> you can still comment on it but its just one avenue of discussion
>
>
> Micah Zoltu @MicahZoltu 02:34
> I can open an issue, or a topic on Magicians. Just wasn’t sure where the best place to go was and I want to be a good citizen on where I go to argue in futility.
>
>
> Nick Johnson @Arachnid 02:34
> @MicahZoltu I don’t really follow. Having a prefix that’s not a valid RLP solves a problem that would otherwise exist (tricking people into signing away all their money), no?
>
>
> Sumant Manne @dpyro 02:34
> i dunno if theres an authoritative forum
> well if its not obvious where to discuss these things
>
>
> Micah Zoltu @MicahZoltu 02:34
> @Arachnid It only solves a full problem IFF you assume that the only things that one can sign that have financial value are transactions.
>
>
> Sumant Manne @dpyro 02:34
> i think that’s an issue in itself
>
>
> Nick Johnson @Arachnid 02:35
> @MicahZoltu I’m not sure what you mean by “a full problem”. Closing off one avenue of attack still seems valuable even if it doesn’t fix everything.
>
>
> Micah Zoltu @MicahZoltu 02:35
> State/payment channel updates are a great example where signing something could cause just as much or more damage than signing a transaction, and the prefix doesn’t protect at all against that.
>
>
> Nick Johnson @Arachnid 02:35
> I don’t think anyone’s claiming just adding \x19 to the start makes it magically safe to sign any message.
>
>
> Sumant Manne @dpyro 02:36
> i sign DEX orders all the time and that has financial consquences in totality
>
>
> Micah Zoltu @MicahZoltu 02:36
> @Arachnid The problem is that people think, “Oh, it is now safe to sign anything with eth_personalSign because it has a prefix” when it 100% is NOT safe to sign untrusted data.
> And I have seen a lot of engineers believe that is safe because of the prefix.
>
>
> Nick Johnson @Arachnid 02:36
> Okay; that seems like a communications problem. Removing the \x19 prefix wouldn’t fix that.
> It would just add extra ways signing untrusted data is unsafe.
>
>
> Micah Zoltu @MicahZoltu 02:36
> In the #191 discussion for example, almost every engineer thought signing with the prefix was “safe and no one could do significant harm”.
> I had to argue for like 3 days before I convinced some of them that it is not safe to sign untrusted messages that are prefixed.
>
>
> Nick Johnson @Arachnid 02:37
> Like I said, I don’t see how removing the prefix would accomplish anything there except make it even worse to sign untrusted data.
>
>
> Micah Zoltu @MicahZoltu 02:38
> @Arachnid Any security measure that protects the user fully (like informed signing protocols we have discussed in the past) would also protect users from RLP attacks. Therefore one of two things is true:
> The user is already protected via some other mechanism, and the 0x19 prefix doesn’t add value.
> The user is not protected via some other mechanism, and the 0x19 prefix makes people think they are protected when they aren’t.
> I argue that if you are in situation (2) you are already screwed.
>
>
> Nick Johnson @Arachnid 02:39
> I don’t think that’s true - I can conceive of an application concocting a message format that they can explain as a safe way to sign something and also happens to be a valid RLP encoded transaction that sends them all your money.
>
>
> Micah Zoltu @MicahZoltu 02:39
> Removing it solves two problems:
> A. It removes the false sense of security.
> B. It makes it so one can actually verify messages signed with an Ethereum client using an off-the-shelf keccak256 tool.
> @Arachnid I would be curious to see an example of that (I’ll accept some medium level of contrivedness).
>
>
> Nick Johnson @Arachnid 02:40
> There’s no reason that a standard that provides a standard way to encode data for signing would have no collisions with valid transactions unless it’s specifically designed for that.
>
>
> Micah Zoltu @MicahZoltu 02:41
> When I first got into Ethereum it took me like a week (this was quite a while ago, before there was much resources/documentation) to figure out how to validate a transaction signed by Geth.
>
>
> Nick Johnson @Arachnid 02:42
> I’m not sure how removing a 1-byte prefix would fix that, either?
>
>
> Micah Zoltu @MicahZoltu 02:43
> That problem was specifically for Geth signing APIs which signs “\x19Ethereum Signed Message:\n” + len(message) + message.
>
>
> Nick Johnson @Arachnid 02:43
> RE an example - the most obvious way would be to say “our signed messages are encoded using RLP”, then just lie about what each of the fields are for.
> Sure, I agree that whole text prefix plus length thing is stupid. But I don’t think a simple precaution to ensure no signed message collides with a valid transaction is.
>
>
> Micah Zoltu @MicahZoltu 02:44
> I agree, right now informed signing is really bad in Ethereum, someone should champion ethereum/EIPs#719.
> If we had something like , would you still argue for prefixing signed messages?
>
>
> Nick Johnson @Arachnid 02:45
> Yes - because again, there’s nothing that guarantees ‘informed signing’ can’t generate a message that is also a valid RLP encoded transaction.
> Unless you explicitly take care to ensure it’s not - such as by applying a prefix that’s not valid RLP.
>
>
> Micah Zoltu @MicahZoltu 02:45
> I would prefer such a limitation be applied to #719, rather than eth_sign.
>
>
> Nick Johnson @Arachnid 02:46
> Is there a reason that eth_sign should be able to sign transactions?
>
>
> Micah Zoltu @MicahZoltu 02:46
> Principle of least surprise.
>
>
> Nick Johnson @Arachnid 02:46
> I would be surprised if that RPC let me sign a transaction.
> Very surprised, even.
>
>
> ligi @ligi 02:46
> me too
>
>
> Micah Zoltu @MicahZoltu 02:47
> As a user, when I call eth_sign(‘hello’), I expect the result to be a signature for the string hello. I do not expect the result to be a signature for a different string.
>
>
> ligi @ligi 02:47
> I also think this is quite dangerous
>
>
> Nick Johnson @Arachnid 02:48
> @MicahZoltu I assume when you say “as a user”, you mean “as someone who’s just come across eth_sign for the first time”, and I would argue that you wouldn’t know anything about the signature format until you looked it up. You certainly can’t expect to be able to verify signatures generated using it without ever reading the documentation for that function, regardless of what method it uses.
>
>
> Micah Zoltu @MicahZoltu 02:48
> That is exactly what I tried to do the first time.
>
>
> Nick Johnson @Arachnid 02:49
> Adding a simple fixed prefix is an easy protection against an actual attack, with very little downside. I don’t think there is a compelling reason to remove it, least of all “someone might be surprised”.
> Especially when that surprise can be alleviated with a paragraph of documentation associated with the RPC call.
>
>
> Micah Zoltu @MicahZoltu 02:49
> Someone on Reddit or something made a claim and signed something as proof. I went to validate and the first thing I did was google what Ethereum uses for signing, which gave me secp256k1. Then I went online and found a tool that verifies secp256k1 signatures and the validation failed.
> This was surprising to me and caused me to believe the Reddit poster was lying.
>
>
> Nick Johnson @Arachnid 02:50
> Validated keccak256 signatures?
> Do you mean hashes?
>
>
> Micah Zoltu @MicahZoltu 02:50
> Sorry, secp256k1.
>
>
> Nick Johnson @Arachnid 02:51
> So it sounds like you’re arguing that it’s important for eth_sign to be compatible with that one random web-based tool you googled.
> Since that tool has made a bunch of choices too - hash, signature scheme, address encoding, etc.
>
>
> Micah Zoltu @MicahZoltu 02:51
> With every tool for validating secp256k1 signatures.
>
>
> Nick Johnson @Arachnid 02:51
> How many tools are there that validate secp256k1 signatures of keccak256 hashes and produce Ethereum addresses as outputs?
>
>
> Micah Zoltu @MicahZoltu 02:52
> Ah, you are arguing that the string → keccak256(string) → secp256k1(keccak256(string)) is already enough steps that a user has to “read the docs”?
>
>
> Nick Johnson @Arachnid 02:52
> You found a tool that implemented a very specific signing scheme, in a manner contrary to what another common tool was using.
>
>
> Micah Zoltu @MicahZoltu 02:53
> The tool I found was literally just a secp256 verifier (I don’t even remember where it was anymore).
>
>
> Nick Johnson @Arachnid 02:53
> I’m arguing that reasonable users shouldn’t have a firm expectation of the exact steps used by eth_sign without reading the docs. I’m also arguing that there’s no big global standard for us to conform to here.
>
>
> Micah Zoltu @MicahZoltu 02:54
> To confirm my memory, secp256k1(keccak256(string)) is what it does right?
>
>
> Nick Johnson @Arachnid 02:54
> What output did the secp256k1 verifier have? If it wasn’t Ethereum-specific, it seems unlikely it would have used kecck256, and it certainly wouldn’t have output an Ethereum address; how would you have used it even if it had worked?
> eth_sign does, roughly, sign(keccak256(prefix + message), private_key). If you’re verifying it against the address of the signer, you need to do keccak256(ecrecover(keccak256(prefix+message), signature))[64:] - which as I’m trying to point out is not a ‘standard’ procedure.
>
>
> Micah Zoltu @MicahZoltu 02:57
> This is the most reasonable argument I have heard so far against the “least surprise” argument.
>
>
> Nick Johnson @Arachnid 02:57
> Glad to hear it
>
>
> Micah Zoltu @MicahZoltu 02:58
> In fact, I think you have convinced me that the “least surprise” argument isn’t really valid. I still maintain that the false sense of security introduced is pretty bad.
>
>
> Nick Johnson @Arachnid 02:58
> The ultimate question in my mind is whether eth_sign is supposed to be ‘porcelain’ or ‘plumbing’. In my mind, it’s porcelain, and nodes shouldn’t expose dangerous low-level ‘plumbing’ operations on your private keys.
> I would be onboard with abolishing eth_sign in favor of something more restrictive and safer, if we can come up with something that fits those criteria
>
>
> Micah Zoltu @MicahZoltu 02:59
> As in, I have come across maybe 1-2 people total (out of dozens) that intuitively understand it is unsafe to sign untrusted data with eth_sign since the addition of the prefix.
> They all seem to think, “the prefix protects me”.
>
>
> Nick Johnson @Arachnid 03:00
> I certainly agree we need to improve communication. 191 tries to make it another step safer by requiring messages be prefixed by the address of the recipient. If apps supported that restriction, it’d be harder to trick someone into signing something for app B from inside app A.
>
>
> Micah Zoltu @MicahZoltu 03:01
> I’m a fan of deleting eth_sign (and eth_personalSign).
>
>
> Nick Johnson @Arachnid 03:02
> Fine with me; they’re such a mess of incompatible implementations anyway.
>
>
> ligi @ligi 03:02
> @Arachnid as far as I understand 191 does not require this - only when version==0
> would also be happy about deprecating eth_sign
>
>
> Nick Johnson @Arachnid 03:03
> Right - but 191 only really defines version 0 so far.
>
>
> ligi @ligi 03:03
> and ‘E’ ^^-)
>
>
> Nick Johnson @Arachnid 03:04
> Yes, true
>
>
> Micah Zoltu @MicahZoltu 03:04
> It feels like validator address isn’t enough? What if someone has a multisig wallet that doesn’t use unique contracts per wallet and instead has a single contract that stores all of the wallets internally (e.g., to reduce new-wallet gas costs)?
>
>
> ligi @ligi 03:05
> on a side-note: kind of unhappy that this is called ‘version’ there - should be called data_layout_id or something like this IMHO
>
>
> Nick Johnson @Arachnid 03:05
> The idea, intuitively, is that a UI should only let “that contract” propose messages to be signed with its own prefix.
>
>
> Micah Zoltu @MicahZoltu 03:05
> It feels like it should be “validator nonce” or something along those lines, which is to say the validator provides some piece of data that is unique to your specific wallet. Would be an address in the naive case, but could be address+offset for a shared contract wallet.
>
>
> Nick Johnson @Arachnid 03:05
> For instance, you could call a constant function with the arguments you want encoded and it would return the message to sign.
> The UI doesn’t necessarily have to understand the contents of the signed message (though that would be a further improvement), but it can at least prevent “cross-domain” signing.
>
>
> Micah Zoltu @MicahZoltu 03:06
> Hmm, I don’t see that specified in version 0?
> Or are you thinking that this is a further enhancement to 191 (not yet discussed)?
>
>
> Nick Johnson @Arachnid 03:07
> Not explicitly, no, I’m extrapolating. Strictly speaking #191 says “everything after the address is determined by the app”, which means it can add whatever it wants there, including nonces etc.
>
>
> Micah Zoltu @MicahZoltu 03:07
> What you are describing though (I think) is action taken by the signer, which requires standardization.
>
>
> Nick Johnson @Arachnid 03:07
> It’s more in the vein of an “implementation note” for 191. The standard doesn’t specify how UIs should implement signing, just the format of messages.
>
>
> ligi @ligi 03:07
> @MicahZoltu btw. the header info is missing for 191 here ERC-191: Signed Data Standard
>
>
> Nick Johnson @Arachnid 03:07
> It doesn’t strictly require standardisation; it’s interoperable even if we only agree on the format.
> @ligi Good catch, I’ll look into that
>
>
> Micah Zoltu @MicahZoltu 03:08
> As the author of a signer (MetaMask, Geth, Parity, etc.) if I follow the standard my tool will sign anything anyone gives me as long as they provide a validator address and some data.
>
>
> Nick Johnson @Arachnid 03:09
> The standard doesn’t say anything about how you should approve signing requests, just what the format of signed data should be.
>
>
> Micah Zoltu @MicahZoltu 03:09
> Ah, I think I see what you are saying. You aren’t suggesting that the signer would lookup the user nonce or something, you are saying that the contract could expect it and the dapp providing data to the signer would provide it.
>
>
> Nick Johnson @Arachnid 03:10
> @ligi Fixed.
>
>
> Micah Zoltu @MicahZoltu 03:10
> In that case, couldn’t one argue that the standard isn’t necessary at all? Apps can include 20-byte address or not, no need to standardize.
>
>
> Nick Johnson @Arachnid 03:10
> @MicahZoltu Right. I’m saying that a good UI should only sign #191 format data (if it understands it) if it can verify the data was provided “by” the app somehow. How it does that is up to it.
>
>
> Micah Zoltu @MicahZoltu 03:11
> Since there is no shared UI across multiple signing tools.
>
>
> Nick Johnson @Arachnid 03:11
> No, because you can develop libraries for encoding and verifying #191 signed data.
> UI isn’t the only consideration here.
> It’s also useful as a best practice for contracts.
>
>
> Micah Zoltu @MicahZoltu 03:11
> Ah, I’m generally against the whole “best practices” thing in the EIPs repo.
> Best practices evolve out of experimentation over time and many successes and failures, and people in Ethereum love to create “Best Practices” EIPs that they just made up and have never tested in the wild.
> Now that I realize that 191 is just another “best practices” EIP I’ll drop my arguments against it and instead continue to press against eth_sign.
>
>
> Nick Johnson @Arachnid 03:13
> I don’t think I understand the distinction. What did you think EIP191 said that it doesn’t?
> It never prescribed any changes to eth_sign.
> And, writing a standard has to start somewhere. You can’t expect people to just coincidentally implement compatible interfaces and then formalise it later.
>
>
> Micah Zoltu @MicahZoltu 03:14
> I think I actually got 191 confused with another EIP that was trying to add a JSON-RPC endpoint for signing.
>
>
> Nick Johnson @Arachnid 03:14
> You’re probably thinking of signTypedData.
>
>
> Micah Zoltu @MicahZoltu 03:14
> Yeah, that is the one.
>
>
> Nick Johnson @Arachnid 03:14
> That EIP, ironically, is no longer much about the RPC call but instead mostly about the data format (which is a good one, now)
> (And also solves very real data-format-related security issues)
>
>
> Micah Zoltu @MicahZoltu 03:15
> Does it actually protect users from signing malicious data now?
>
>
> Nick Johnson @Arachnid 03:16
> It provides a standard way of encoding structured data that protects against malleability issues.
> (Eg, preventing cases where “foo” + “bar” can be interpreted as “fo” + “obar”)
>
>
> Micah Zoltu @MicahZoltu 03:21
> I still argue that eth_signTypedData having the prefix introduces a false sense of security, but I already argued pretty extensively in that issue about it.
> I think eth_signTypedData is otherwise protected from signing transactions, so the prefix seems redundent, though I haven’t actually verified that is true and someone couldn’t cleverly craft a method call that is really a transaction in disguise.
>
>
> ligi @ligi 03:35
> @Arachnid speaking of 191 - noticed this: ethereum/EIPs#989
>
>
> Nick Johnson @Arachnid 04:22
> Thanks
