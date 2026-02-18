---
source: magicians
topic_id: 7263
title: "EIP-4361: Sign-In with Ethereum"
author: wyc
date: "2021-10-14"
category: EIPs
tags: [signatures, identity, siwe]
url: https://ethereum-magicians.org/t/eip-4361-sign-in-with-ethereum/7263
views: 12033
likes: 37
posts_count: 31
---

# EIP-4361: Sign-In with Ethereum

Discussion for [EIP-4361](https://github.com/ethereum/EIPs/pull/4361).

You can find the latest updates on this work including recorded community calls with notes and links to the chat at login.xyz.

## Replies

**wyc** (2021-10-14):

Ferrying some discussions over from the [GitHub thread](https://github.com/ethereum/EIPs/pull/4361).

=============

axic asked

> Why is it preferable to have a new invented language and not some binary format, which is easier to parse (CBOR or even ERC-712)?
>
>
> Is the only reason because the signed message will be “readily” displayed in wallets without implementing support for it? If so, I think hardware wallets may be a big exception to that where some other more easily parsable format is more likely to gain support.

wyc responded

> Hi axic, thanks for your concern. That is indeed the main reason, so that applications may adopt this specification without full buy-in from wallet vendors or significant degradation of their user experiences today. In our proposal response to the RFP, we actually specified EIP-712 as the signing format, but found the user experience across many wallets to be much worse than using EIP-191. Formats like CBOR, EIP-712, protobuf, etc. indeed specify structuring for data, but hardware wallets have spotty support for presentation of EIP-712 requests to the users already (please see ongoing issues Ledger/Trezor). We believe that if adoption of this specification relies on all wallet vendors upgrading how they do signing first, it is far less likely to see success. While pure technical merit is important to consider, adoption depends far more on talking to downstream users and understanding their concerns, what they are likely to truly adopt, etc. We have completed over 30 interviews towards this conclusion. We welcome anyone to let us know of any further user research in support or incongruent with this claim. Hope that helps!

=============

awoie asked

> Since this is still a draft, it is feels a bit weird that folks have already approved this. wyc Is this going to be merged once all issues in the community calls get addressed?

wyc responded

> awoie the PR is indeed in draft state, and therefore can’t be merged right now. I appreciate everyone who signaled their support for it so far! We will discuss pretty important matters in the public community calls and attempt full resolution of any concerns prior to merge, but also we are on a timeline for delivery so this must be balanced too.
>
>
> Full details: login.xyz

=============

---

**rmeissner** (2021-10-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wyc/48/4647_2.png) wyc:

> Discussion for EIP-4361

The mentioned link doesn’t work for me. The correct link would be [Create EIP-4361: Sign-In with Ethereum by wyc · Pull Request #4361 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4361/files)

---

**rmeissner** (2021-10-15):

> hardware wallets have spotty support for presentation of EIP-712 requests

I don’t see how not using EIP-712 improves the situation for hardware wallets. Wouldn’t it make more sense to specify 1 specific EIP-712 struct that is expected? In this case hardware could optimize for this one. The issue for hardware wallets with EIP-712 is that it is fully dynamic and therefore quite complex to implement with limited resources. But if you pick one specific domain+struct it is trivial to implement. This would also allow easy support on contracts (as EIP-712 was designed with smart contract in mind).

---

**MicahZoltu** (2021-11-22):

TL;DR: Private Key != Identity.  Contract == Identity.

I am pretty strongly opposed to this proposal because it doesn’t support contract wallets.  Attaching an identity to a private key means users cannot rotate their private keys, something broadly considered a good security practice.  In general, we should try to minimize the number of situations where a user’s private keys are tightly coupled with some feature.

Instead, we should have a standard for a contract that has a method like, `isAuthorizedTo(signature, permission_set)`.  Then a user would sign *something* (exactly what is up to the contract wallet they are using and not something that needs to be standardized) and the website could then ask the contract wallet associated with the user’s identity if the supplied signature is one that is authorized to do the thing the user is doing (like sign-in to social media accounts with read access).

This system also would support on-demand permission checking.  You could prompt the user for a signature, and then the website could ask the contract “does the signer have permission to do X” each time the user tries to do some new action.  You would probably want some standardized contract method for adding/removing access to a particular private key, but I think that could be in a separate standard (or many standards).

Note: If one does implement a contract-friendly system as outlined above, then a registry like EIP-1820 should be used so that any contract that supports arbitrary method calls can work with it and it doesn’t require every contract wallet to natively support it.

If a user wants to roll their keys, they would only need to update their contract wallet with the new keys and they would not need to roll their keys with every single service they interact with.

---

**wyc** (2021-11-22):

Hi Micah, thanks for your thoughts! I’m happy to report that the spec does indeed support smart contract wallets via EIP-1271. Please see the section titled “Signing and Verifying with Ethereum Accounts”. Hope this helps, please feel free to add anything further.

---

**wyc** (2021-12-09):

To conform with EIP-1, I am pasting the pieces moved out of the spec to here. Thank you to @lightclient for spotting these!

From Motivation:

> This work is sponsored by the Ethereum Foundation and Ethereum Name Service (ENS). It is being developed in the open through a series of recorded community calls and public repositories, and its development is informed by over twenty user interviews with a focus on currently-in-production uses, related prior EIPs, and fits within product roadmaps.

From Requirements:

> RFP

From Additional Resources

> # Additional Resources
>
>
>
> Throughout the development process of this specification, community participation was encouraged and facilitated via weekly calls. This was to ensure coverage on major areas of concern, and accommodate a wide and diverse range of feedback from the Ethereum community.
> Additionally, resources and research were made public both in the form of the community calls, the minutes being published, and blog posts. Those resources can be found at the following locations:
>
>
> Login.xyz - which served as the primary source of specification updates, news, and community call minutes.
> An initial overview of required workflows - which helped inform the initial kickoff and discussions on the specification.
> Research on related EIPs - which helped identify the necessary requirements around necessary EIPs to support.
> A comparison of EIP-191 vs. EIP-712 - which helped lead to the decision to use EIP-191 in the first version of EIP-4361.

From Discussions and Acknowledgements:

### Discussions and Acknowledgements

> @awoie and @rh7 led the discussion on EIP-712 and EIP-191 signing schemes, including the benefits of structured data types and potential for extensions when using EIP-712.
> @awoie surfaced a number of privacy and security considerations related to MITM attacks, replay attacks, relay attacks, and RP-binding.
> @pedrouid suggested a YAML-inspired message format that struck the balance between human and machine readable.
> @Amxx suggested adding the version indicator to allow forwards-compatibility, and also brought up important implications between EIP-1271 and network selection.
> @mhluongo led discussion around i18n support and suggesting several improvements around the message format.
> @oed suggested low-impact changes that could do a lot to enable capabilities-based permissioning models.
> @kdenhartog advised on mitigating/calling out phishing attacks, domain binding security, OIDC models of identity, and examples of using EIP-712 to structure data.
> @SamWilsn made several improvements to the ABNF grammar and additional security guidelines to wallet implementers to prevent phishing attacks.
> @cfelde suggested a minor improvement to the ABNF grammar.

---

**rmeissner** (2021-12-17):

I still don’t understand how it is beneficial to use EIP-191 with an ABNF message that should get a custom interface by the wallet, compared to an EIP-712 struct where you can do the same.

As we can see it takes a long time for wallets to adopt new standards (e.g. EIP-712) creating a new one which is equally hard to support on hardware wallets doesn’t improve this situation (as mentioned before).

Is there any more documented decisions/ discussions on the signing format, as the information on the EIP are quite limited and provides very little details?

---

**holiman** (2021-12-21):

I started implementing this, and found a quirk in the spec. Regarding the optional statement.

```auto
   address LF
    LF
    [ statement LF ]
    LF
    %s"URI: " uri LF
...
statement = *( reserved / unreserved / " " )
```

If I interpret this correctly, it means that the statement itself can be present or not, and also that the statement *may be empty*.

So this is perfectly fine, being a message with a present-but-empty statement:

```auto
service.org wants you to sign in with your Ethereum account:
0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2

URI: https://service.org/login
Version: 1
```

So is this, a message without a statement:

```auto
service.org wants you to sign in with your Ethereum account:
0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2

URI: https://service.org/login
```

This is a bit awkward, making correct parsing more complicated than it needs to be. I’d propose to change it to read like this, to make the statement, if present, contain one of more characters:

```auto
statement = 1*( reserved / unreserved / " " )
```

---

**holiman** (2021-12-21):

There’s also an ambiguity. This message can be interpreted either as a valid message with a statement, or as a malformed message (without statement):

```auto
service.org wants you to sign in with your Ethereum account:
0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2

URI: https://not.the.service.org/its_a_statement

URI: https://service.org/login
Version: 1
Chain ID: 1
Nonce: 32891756
Issued At: 2021-09-30T16:25:24Z
```

I don’t know if there’s anything to do about that, just throwing it out there as an example for parser-writers to be aware of.

EDIT: One thing that would solve both these quirks, would be if the statement was also prefixed, like the other fields:

```auto
   address LF
    LF
    [ %s"Statement: " statement LF ]
    LF
    %s"URI: " uri LF
```

---

**holiman** (2021-12-28):

The reference implementation is not in line with the spec, so changing it is IMO a no-brainer: [Implementation not according to spec · Issue #30 · spruceid/siwe · GitHub](https://github.com/spruceid/siwe/issues/30)

---

**TimDaub** (2022-01-09):

I want to highlight a conflict within the [spec](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-4361.md#abnf-message-format):

> The wallet presents the user with a structured plaintext message or equivalent interface for signing with the EIP-191 signature scheme (string prefixed with \x19Ethereum Signed Message:\n). The message MUST incorporate an Ethereum address, version of the message, uri for scoping, nonce acceptable to the server, and issued-at timestamp.

The section “Specification” mentions that the message MUST incorporate:

- address
- version
- URI
- nonce
- issuedAt

However, the ABNF in the specification, as well as that in the [reference implementation](https://github.com/spruceid/siwe/blob/main/lib/abnf.ts#L4) mandate more than those fields:

- domain
- chainId

So which one is wrong? The ABNFs or the sentence in the EIP document?

---

**wyc** (2022-01-12):

Thanks for addressing this in your PR! I’ve approved it.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4655)














####


      `master` ← `TimDaub:patch-1`




          opened 10:38PM - 09 Jan 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/2670a369d055e8f4aaca6e8dd123fe3b6d01744b.jpeg)
            TimDaub](https://github.com/TimDaub)



          [+1
            -1](https://github.com/ethereum/EIPs/pull/4655/files)







The spec's ABNF and the ABNF in the reference implementation all mandate `domain[…](https://github.com/ethereum/EIPs/pull/4655)` and `chainId` to be required fields in a message, so we add them to the specification text for completeness as well.

Comment on Ethereum Magicians is here: https://ethereum-magicians.org/t/eip-4361-sign-in-with-ethereum/7263/11

---

**sebastiantf** (2022-02-03):

Something that was noticed while working with Gnosis Safe (implements EIP-1271) is that it requires sending an on-chain txn for signing “off-chain” messages with `personal_sign` et al.

EIP-4361 and similar Sign-in with Ethereum workflows recommend using a nonce for each message, to prevent replay attacks.

But using a nonce for each login would require the Gnosis Safe owner to send an on-chain txn spending the gas fees for each login, which is a bad UX.

I think the Gnosis team is working on something for off-chain message signing with Safes, from talking to [@rmeissner](/u/rmeissner)

But, just wanted to share something here that I’d come across, that’s related to EIP-4361

---

**poojaranjan** (2022-02-09):

EIP-4361: Sign-In with Ethereum with [@wyc](/u/wyc)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/b/b06f49a2e8dd5de28b913fe21fe7446b23dafbf0.jpeg)](https://www.youtube.com/watch?v=rpbaxlfIhho)

---

**htekdev** (2022-03-20):

This is way bigger than simply being able to sign in with Ethereum. This could enable “web2.0” architecture’s ability to accept web3.0 user base. Not only that, but it could enable the consolidation of identity leading towards the dream goal of transitioning all data from centralized monopolies to the new decentralized paradigm. Im currently attempting to make a dent in this area with the health care industry (The biggest identity/privacy/centralized data nightmare in existence). I am trying to formulate a proposal that includes several components and one of those is the Trust Framework.

Im guessing that’s why no so recently ENS published their inclusion in the list of DIDs

[ENS names are Decentralized Identifiers (DIDs) | by Oliver Terbu | uPort | Medium](https://medium.com/uport/ens-names-are-decentralized-identifiers-dids-724f0c317e4b)

Im trying to find how this standard fits with our drive-in health care interoperability starting with the consolidation of identity. I have been driving the conversations towards blockchain (Ethereum) and this standard would be the missing link.

**Real question:**

Am I understanding correctly or is any connection to the JWT standard not being included here? If that is true then it makes it difficult to consider EIP-4361 as a true standard (From the eyes of “non web3 organizations”) which would cause difficult justifications for implementation to legacy relying-parties. Especially ones that are not decentralized in nature. Like you said in the video the dream is to have no centralization but in some situations, we must and for the current maturity of Ethereum and its applications, centralization still exists. If we are going to make any dent in this we need to think about how to include centralized-based authentication flows when designing new standards in order to make the transition to new decentralized paradigm smoother.

---

**shobhit** (2022-07-18):

Why do we need to have chain ID as a mandatory field?

Signing in to an application to (say) check my RSS feeds does not need a chain. Same can be said for other use cases where you really don’t need a reference to chain, just need to authenticate the user.

---

**j12t** (2022-07-26):

Is this spec considered “finished” at this point, or is there ongoing work, perhaps for additional related use cases? (Perhaps in other EIPs or outside of the EIP process?) If there is, where would I track this?

---

**MicahZoltu** (2022-07-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wyc/48/4647_2.png) wyc:

> Discussion for EIP-4361 .

Can you please change this link to `https://eips.ethereum.org/EIPS/eip-4361`?

---

**MicahZoltu** (2022-07-27):

I agree with [@shobhit](/u/shobhit) that chain ID shouldn’t be required for EOA verification, but it should be required for contract verification (you need to know what blockchain to do the contract execution against).

---

While the rationale for choosing 191 over 712 is all technically correct, I think it is mostly based on an a premise I disagree with which is that poorly designed wallets should result in using standards that are worse solutions to problems.  We should be pressuring wallets to do better at EIP-712 rendering, rather than just giving up and saying, “well, I guess we’ll never get good 712 rendering so we will use 191 everywhere”.

712 is more computer readable, while 191 is more human readable, and I think this standard should be focusing on computer readability rather than human readability and leaving it up to the presentation layer to present that to users.

---

**unenunciate** (2022-09-15):

Can this be modified so that it is calling its own personal_sign_swie method, probaly not that method name though, so we can both enforce the data structure and so that, from the extension level, the request could be modified to represent the contract wallet if one is in place? (I am helping building an ERC-4337 platform and this would be very helpful personal and generally useful too)


*(10 more replies not shown)*
