---
source: magicians
topic_id: 10627
title: "EIP-5573: SIWE ReCap"
author: awoie
date: "2022-09-01"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5573-siwe-recap/10627
views: 5539
likes: 18
posts_count: 36
---

# EIP-5573: SIWE ReCap

Discussion on EIP-5573: a mechanism on top of Sign-In With Ethereum for informed consent to delegate capabilities with an extensible scope mechanism.

See more details on EIP-5573 here: [ERC-5573: Sign-In with Ethereum Capabilities, ReCaps](https://eips.ethereum.org/EIPS/eip-5573)

## Replies

**unenunciate** (2022-09-15):

Can this be modified so that it is calling its own personal_sign_swie method, probaly not that method name though, so we can both enforce the data structure and so that, from the extension level, the request could be modified to represent the contract wallet if one is in place?

---

**awoie** (2022-09-15):

Can you elaborate what you mean by “calling its own personal_sign_siwe method”? The spec is fully personal_sign and SIWE compliant which means it uses the same data structure, same JSON RPC signing methods.

---

**unenunciate** (2022-09-15):

Its not about it not being compliant. Its about this being compatible with ERC 4337 account abstraction adding in separate sign where the form is further conscribed would allow for the extension simply modify the request via injecting the correct address for the SIWE request.

---

**cobward** (2022-10-07):

I think that is out of scope for EIP-5573. EIP-5573 is simply describing a common SIWE format that can be used to encode object capabilities. It is not prescriptive on how such a message should be constructed or signed.

If a `personal_sign_siwe` method is needed for SIWE to be compatible with ERC 4337, then that should be addressed in another EIP in my opinion.

---

**unenunciate** (2022-10-08):

It has been why most are against 4361 so it tracks that it will be continually recurring issue and shouldn’t be separated considering the eventual road map that includes the of removing EOAs altogether. Unless I am misunderstanding the meaning of that.

---

**cobward** (2022-10-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/unenunciate/48/7178_2.png) unenunciate:

> it will be continually recurring issue and shouldn’t be separated considering the eventual road map that includes the of removing EOAs altogether

Sorry I’m not sure I understand what you mean by this. What road map are you talking about, and how does this affect 5573?

---

**unenunciate** (2022-10-11):

I am not going to lie this might be either an internal document or something more ethereal in Vitalik’s head either way he has mentioned it several times being on the ‘roadmap’, but I can find no public roadmap that goes out that far.

4337 wallets will become very quickly adopted not only as a better wallet option but also because they provide a better UX. Any SIWE EIP that does not support them will ultimately not be widely adopted.

---

**cobward** (2022-10-12):

EIP-5573 is not concerned with signing or verification of a SIWE message (it simply uses the methods described in EIP-4361), so I would argue there is no need to concern it with the requirements of EIP-4337.

I agree there will need to be work (possibly an extension EIP) to make SIWE compatible with EIP-4337, however that is not a concern for this 5573. From my understanding there are ongoing conversations on how this could be done. 5573 would not disrupt this work, nor make 4361 *less* compatible with 4337.

---

**unenunciate** (2022-10-12):

Any link to those aforementioned conversations?

---

**cobward** (2022-10-12):

I don’t think there’s been anything in the public yet, but the internal conversations will start bringing things up.

---

**danfinlay** (2022-10-15):

Hi there, I’ve lightly reviewed the proposal. I’m a pretty big object capability enthusiast, and there are some things here that I like and some things that I think are going to make it challenging to adopt or expensive to use. Anyways, here are my notes, [syndicated from my Roam graph](https://roamresearch.com/#/app/capabul/page/EIboJH_Jn):

- Aims to provide a [[EIP-4361: Sign in with Ethereum]] extension that allows any cryptographic [[capability]] to also be delegated as part of the same signature.

Uses the terms [[capability]] and [[object capability (ocap)]], unclear if they fulfill [[rich sharing]] criteria.

At the very least, this seems to be more cap than ocap, since the designation is not being conveyed as a programming language object.

Claims to enable “any protocols and APIs that support [[object capability (ocap)]].”

- This is not possible, since a capability format may require additional signatures that are not part of this one.

Uses the term [[delegee]] for the recipient of a [[delegation]]. New to me, appears to be a real word!
Since it overloads [[EIP-4361: Sign in with Ethereum]], it’s building on top of [[personal_sign]]

- This ensures the signature will be somewhat less efficient to parse on chain (string parsing).
- Making the signature challenge human readable will either need to be

Plain text

This appears to be what it does.
- more expensive to parse on chain
- Not multi-lingual
- Uses a URI as the delegate in the signature

Unclear how a URI should be interpreted as the designee of a capability.
- Shows an example with [[DID]]s

So the implementation needs to be able to interpret them. Who is implementing that? Which schemes will be supported?

More dense format

- This may also be used, via the ReCap URI Scheme.

Since there is both a human-readable and “URI Scheme” representation of the delegation, there needs to be some measure to ensure these are the same thing, so the user does not sign one thing that means another.

Would require feature additions of [[wallet]] software.

- Implementation/distribution can be simplified using [[[[MetaMask]] Snaps]]

Will probably not work for [[contract account]]s

- I hope to address this with [[[[Delegatable Eth]] and [[[[EIP]] 4337: [[account abstraction (AA)]] via Entry Point Contract]] synthesis]]

Includes a new [[JSON-RPC API]] method that allows requesting methods.

- Each capability is specified by a sort of resource identifier like my.resource.1.

This is not open ended enough to satisfy the kind of reference passing across domains that really distinguishes true [[rich sharing]] and avoids the [[Confused Deputy]] problem. Ideally capabilities would be represented as objects that could have been granted from other methods/sources.

This isn’t a show stopper. There is still lots of value to having a way of requesting multiple resources from a user, I’m just being very specific about what distinguishes this method from some of the approaches it is borrowing language from.

I’m largely skimming this schema for now.

Does not seem to have an implementation today, which leaves a lot of questions open. I think a lot here is left to the implementers.

- Can the holder of a ReCap also delegate it?
- How is a ReCap used/redeemed?
- Can contract accounts interact with these?

---

**cobward** (2022-10-16):

Thanks for sharing your extensive notes. Hopefully I can address at least some of the issues you raise. I’ll start with the easier ones!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Does not seem to have an implementation today

We have an implementation [here](https://github.com/spruceid/siwe-recap).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Can the holder of a ReCap also delegate it?
> How is a ReCap used/redeemed?

Yes a holder can delegate any of the capabilities in a ReCap, but the ReCap spec doesn’t define a method for how that should be done. If the secondary delegation is also a ReCap, we have an expectation that a link/cid/encoding of the primary delegation would be inserted in `ext` (extra fields).

One of the problems we are trying to solve with ReCap is “How can an ethereum account authorise actions with a system that supports ocaps?”. It’s clearly bad UX if an end-user is required to directly sign a capability invocation message for every action that needs to be performed. We want to use ReCap to delegate capabilities to a session key, which invokes those capabilities on behalf of the ethereum account. ReCap only defines a delegation format. How that delegation is invoked is dependent on the “type” of delegee and the authorisation system that is being interacted with.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Can contract accounts interact with these?

Absolutely, with a caveat. Since ReCap uses SIWE for the signature portion of verification, this is the same problem as “Can contract accounts use SIWE?”. We have been working with Gnosis to provide a method for a Gnosis Safe to sign in with ethereum. In this case the ethereum address in the SIWE message (i.e. the delegator) is the Gnosis Safe, the message is signed with an EOA, and as part of SIWE verification we perform an on-chain lookup to check the binding between the EOA and Gnosis Safe in a “delegation registry”. [Note: I personally haven’t actually worked on this so some of the terminology might be inaccurate].

How this should be done more widely is likely the concern of later work to make SIWE compatible with EIP-4337.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Each capability is specified by a sort of resource identifier like my.resource.1.
>
>
> This is not open ended enough to satisfy the kind of reference passing across domains that really distinguishes true [[rich sharing]] and avoids the [[Confused Deputy]] problem.

Apologies if I’m wrong, but you may have missed that each capabilities are grouped into namespaces. Does that resolves these concerns? If not, what is ReCap lacking?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Since there is both a human-readable and “URI Scheme” representation of the delegation, there needs to be some measure to ensure these are the same thing, so the user does not sign one thing that means another.

Along with SIWE signature verification, to verify a ReCap you must also verify that the human-readable statement is correct. This is done by performing the translation from resources (ReCap URIs) to `recap-transformed-statement`, and checking that the statement is suffixed with `recap-transformed-statement`. This is described in more detail in the algorithm sections.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> This is not possible, since a capability format may require additional signatures that are not part of this one.

I’m not familiar with any such formats, but would it be enough to insert those signatures (plus any other required data) into `ext` (extra fields)? Or could you give an example of such a format?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> At the very least, this seems to be more cap than ocap, since the designation is not being conveyed as a programming language object.

Would you be able to elaborate on this? Is the “designation” the target resource in this context? And what do you mean by it “is not being conveyed as a programming language object”?

---

**cobward** (2022-10-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Uses the term [[delegee]] for the recipient of a [[delegation]]. New to me, appears to be a real word!

We tend to use it to avoid the confusion of using `delegate`, being both a verb and a noun ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**awoie** (2022-10-17):

Thanks a lot for reviewing the article and providing feedback. [@cobward](/u/cobward) commented already on most of your points. But here are some additional comments below.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Includes a new [[JSON-RPC API]] method that allows requesting methods

SIWE ReCap will rely on the same JSON-RPC API as SIWE, therefore strictly speaking there is no new JSON-RCP API needed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Shows an example with [[DID]]s
>
>
> So the implementation needs to be able to interpret them. Who is implementing that? Which schemes will be supported?

The delegate/delegee has to be a URI to be identifiable. DIDs are just examples since they make it easy to authenticate the delegate/delegee but any URI can be used. The documentation of the resource service API has to define what URI schemas are acceptable and that would include DID methods if they even wanted to support DIDs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Includes a new [[JSON-RPC API]] method that allows requesting methods.
>
>
> Each capability is specified by a sort of resource identifier like my.resource.1.
>
> This is not open ended enough to satisfy the kind of reference passing across domains that really distinguishes true [[rich sharing]] and avoids the [[Confused Deputy]] problem. Ideally capabilities would be represented as objects that could have been granted from other methods/sources.

SIWE ReCap capabilities can be represented as objects: SIWE message incl. ReCaps + Signature. We expected people will use CACAOs as their container format for this since CACAOs can already represent SIWE messages + Signatures.

There is no strict requirement that each ReCap has to include a resource identifier. We intentionally made the spec open to cater for systems that don’t have URIs identifying their resources. The proposed EIP also allows untargeted (not tied to a resource identifier) ReCaps as well.

---

**expede** (2022-11-15):

(Wow it’s been a while since I’ve been in a magicians thread ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12))

Hey [@awoie](/u/awoie) ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12) I just got off a CASA call where we’re exploring make UCAN and SIWx/ReCap interop.

I just wanted to quickly shared something that we learned in the UCAN process that may or may not be helpful for ReCap:

```json
      "my.resource.1":[
         "append",
         "delete"
      ],
      "my.resource.2":[
         "append"
      ],
      "my.resource.3":[
         "append"
      ]
```

UCAN resources looked almost *exactly* like this early on. We started in languages that use parsing libraries — this is readable and the parser combinators make this stuff very easy. Once folks using JS & TS started writing libraries, we got a bunch of complaints that it was hard to parse when they’re used to working directly in JSON. This is why we switched to objects:

```json
[
  {
    "with": "my.resource.2",
    "can": "append"
  },
  {
    "with": "my.resource.3",
    "can": "append"
  }
]
```

This is totally isomorphic, just laid out differently. It also reads nicely like an English sentence “with `noun`, you can `verb`”.

Anyhow, I hope that’s helpful! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**oed** (2022-11-16):

I threw together a quick comparison of ReCap and UCAN. I think there are some changes we could make to ReCap to make it more compatible with UCAN.



      [gist.github.com](https://gist.github.com/oed/24207b2de1fb63e05867f1cf45776df8)





####



##### ucan-recap.md



```
Exploreing the differences between how capabilities are represetned between UCAN and ReCap.

## Comparison

|                 | [UCAN](https://github.com/ucan-wg/spec)    | [ReCap](https://eips.ethereum.org/EIPS/eip-5573)   |
| --------------- | ------------------------------------------ | -------------------------------------------------- |
| `$RESOURSE`     | Needs to be a URL                          | Any String                                         |
| `$ABILITY`      | One ability per resource ref               | Any nymber of abilities per resource ref           |
| `$EXTENSION`    | Additional caveats for a specific resource | Additional information, relevant for all resources |
| All resources   | Not possible                               | In `def` property                                  |
```

    This file has been truncated. [show original](https://gist.github.com/oed/24207b2de1fb63e05867f1cf45776df8)

---

**expede** (2022-11-16):

Thanks [@oed](/u/oed) !

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> $RESOURSE     | Needs to be a URL

More specifically it needs to be some kind of URI. We started with “any string”, but Irakli quite rightly pointed out that it makes interop very difficult because the same string can have different meanings

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> All resources   | Not possible

This is possible in UCAN as `{with: "*", can: "*/*"}`. We use it regularly for e.g. device linking

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> Any nymber of abilities per resource ref

We had this at one point, but the complaint was that it’s easier with one per ![:woman_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/woman_shrugging.png?v=12) I guess also if you need extensible fields, they may cross unintentionally

---

The other big difference is that we namespace the `can` field too.

---

**oed** (2022-11-17):

> More specifically it needs to be some kind of URI. We started with “any string”, but Irakli quite rightly pointed out that it makes interop very difficult because the same string can have different meanings

Typo, should have said URI. Updated!

> This is possible in UCAN as {with: "*", can: "*/*"}. We use it regularly for e.g. device linking

Is `*` really a URI? Or is this just a special case.

Either way i think it would make sense for ReCap to use the same approach for the resource string.

> We had this at one point, but the complaint was that it’s easier with one per  I guess also if you need extensible fields, they may cross unintentionally

Easier in what way? Imo it would be better to avoid duplication here. Tooling can abstract the underlaying data structure and make it easier to use.

> The other big difference is that we namespace the can field too.

Oh good point. Updating comparison doc to reflect this.

---

**expede** (2022-11-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> Is * really a URI? Or is this just a special case.

Indeed, good catch: we changed this in 0.9 to be a URI and scoped to a specific DID’s capabilities. This now looks like: `own://did:key:zH3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV/*`

Some folks want to use the DID itself, but I think it’s ambiguous that you’re delegating the rights of things owned by a DID vs rights to update the DID doc itself.

We previously used `my:*` for this to disambiguate especially in chains, but the `own` URI is more general and easier to work with.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> Easier in what way? Imo it would be better to avoid duplication here

It makes the delegation logic more complex because now you have a nested array, but the same capability could still be delegated in another entry. For example, there’s nothing stopping you from writing the following:

```js
"my.resource.1":["append","delete"],
"my.resource.1":["read"]
```

So now you have to deal with the nested array in your code *and* still look at the level above for others caps on the same resource. If you model this as a JSON object, you have to either merge them, or pick which one is valid, or invalidate the entire credential. There’s more that an implementer can mess up, basically.

```javascript
// what do?
{
  "my.resource.1": ["append","delete"],
  "my.resource.1": ["read"]
}
```

If you pick the merge case, then extensible fields get dangerous (easy to mess up what refers to what) unless you reformat them as objects:

```javascript
{
  "my.resource.1": [
    {can: "append", on: "Tuesdays"},  // silly nonsense example
    "delete"
  ],
  "my.resource.1": ["read"]
}
```

In UCAN, we solve for this by allowing for hierarchy (which yes, is a tradeoff). This is desirable for a bunch of reasons, including enabling rights amplification (incl. joining caps from different sources) and letting applications extend other’s semantics, which gives consumers a lot of (safe) flexibility over how they consume and reuse capabilities between apps/services.

Here’s the [diagram from the 0.9 UCAN spec](https://github.com/ucan-wg/spec#52-top):

```auto
                                           ┌───────┐
                                           │       │
                                           │   *   │
                                           │       │
                                           └▲──▲──▲┘
                                            │  │  │
               ┌────────────────────────────┘  │  └────────────────────────────┐
               │                               │                               │
          ┌────┴────┐                     ┌────┴─────┐                     ┌───┴───┐
          │         │                     │          │                     │       │
          │  msg/*  │                     │  crud/*  │                     │  ...  │
          │         │                     │          │                     │       │
          └─▲─────▲─┘                     └─▲──────▲─┘                     └───────┘
            │     │                         │      │
            │     │                         │      │
            │     │                         │      │
┌───────────┴┐ ┌──┴────────────┐ ┌──────────┴──┐ ┌─┴─────────────┐
│            │ │               │ │             │ │               │
│  msg/send  │ │  msg/receive  │ │  crud/read  │ │  crud/mutate  │
│            │ │               │ │             │ │               │
└────────────┘ └───────────────┘ └─────────────┘ └─▲─────▲─────▲─┘
                                                   │     │     │
                                            ┌──────┘     │     └──────┐
                                            │            │            │
                               ┌────────────┴──┐ ┌───────┴───────┐ ┌──┴─────────────┐
                               │               │ │               │ │                │
                               │  crud/create  │ │  crud/update  │ │  crud/destroy  │
                               │               │ │               │ │                │
                               └───────────────┘ └───────────────┘ └────────────────┘
```

Here you can delegate `crud/mutate` and avoid the resource duplication. If you squint, this is the same “shape” as rights amplification, but where no new authority is conferred. It’s also the same relationship as between `*` and `crud/read` (where `read` is a subset of `*`/“everything”). I will highlight that not everyone loves this, but it’s the same idea as being able to attenuate a resource, but on the ability. The open extensibility (I guess really “just” the open-closed principle) of this kind of system means that we can ship a standard library of capabilities and give them really good support in libraries without limiting users to specific use cases.

Phew that was a lot longer than I expected to write ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12) Looking forward to the call next week btw!

---

**oed** (2022-11-20):

Crossposting Irakli’s response and suggestion: [Multiple "can" for a "with" · Issue #123 · ucan-wg/spec · GitHub](https://github.com/ucan-wg/spec/issues/123#issuecomment-1321075931)

An approach like this would be interesting and it solves for the merge approach you outlined above.

---

I think his suggestion also makes sense for ReCap:

**Schema:**

```auto
{
  $RESOURCE: {
    $ABILITY: $EXTENSION,
    ...
  },
  ...
  "prf": [&Link] // OCAP delegations
}
```

**Example:**

```auto
{
  "example://example.com/public/photos/": {
      "crud/delete": {}
  },
  "example://example.com/private/84MZ7aqwKn7sNiMGsSbaxsEa6EPnQLoKYbXByxNBrCEr": {
      "wnfs/append": {}
  },
  "example://example.com/public/documents/": {
    "crud/delete": {
      "matching": "/(?i)(\W|^)(baloney|darn|drat|fooey|gosh\sdarnit|heck)(\W|$)/"
    }
  },
  "mailto:username@example.com": {
    "msg/send": {},
    "msg/receive": {
      "max_count": 5,
      "templates": ["newsletter", "marketing"]
    }
  }
}
```


*(15 more replies not shown)*
