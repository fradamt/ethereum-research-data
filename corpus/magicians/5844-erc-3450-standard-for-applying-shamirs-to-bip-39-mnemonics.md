---
source: magicians
topic_id: 5844
title: "ERC-3450: Standard for Applying Shamir's to BIP-39 Mnemonics"
author: dstreit
date: "2021-03-29"
category: EIPs
tags: [cryptography]
url: https://ethereum-magicians.org/t/erc-3450-standard-for-applying-shamirs-to-bip-39-mnemonics/5844
views: 5907
likes: 8
posts_count: 31
---

# ERC-3450: Standard for Applying Shamir's to BIP-39 Mnemonics

A proposal for a standardized algorithm for applying Shamir’s Secret Sharing Scheme to BIP-39 mnemonics, where the shares are also BIP-39 mnemonics.

Pull request: [Draft: Shamir + BIP-39 by danielstreit · Pull Request #3450 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/3450) (Updated to apply feedback from below)

Reference implementation: [GitHub - danielstreit/shamir-bip39: Applies Shamir's Secret Sharing Scheme to BIP39 mnemonics](https://github.com/danielstreit/shamir-bip39)

Any and all feedback is appreciated!

Thanks,

Dan

## Replies

**vbuterin** (2021-03-29):

What’s the polynomial modulus that you are using? Although the various 256-element fields are all isomorphic, I think you still need to pick one to get consistent answers.

---

**dstreit** (2021-03-29):

1.

I was under the impression this was implied by the 256-element field, but I may be mistaken on that and can update the spec to clarify this.

---

**vbuterin** (2021-03-29):

29, meaning $x^8 + x^4 + x^3 + x^2 + 1$?

Yeah, it matters because multiplications that wrap around degree 8 will give different concrete answers.

---

**dstreit** (2021-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> What’s the polynomial modulus that you are using? Although the various 256-element fields are all isomorphic, I think you still need to pick one to get consistent answers.

Yes, I believe that is correct.

A little background: This started as a UI-focused project to make it easier to interact with existing implementations of Shamir’s. I got two pieces of feedback on the initial prototype:

- Ideally, the shares would be mnemonics (they were hex strings initially)
- Ideally, the algorithm would follow a known standard, to ensure recovery some point down the road

While I was able to find related standards (like SLIP-0039), I wasn’t able to find something that would work for this case exactly (though I’m open to suggestions and may have missed something obvious), so went about drafting a new standard.

I’ve been following several implementations closely in this, but am probably a bit over my head in math notation and finite field arithmetic, so any feedback on how to specify it more accurately is greatly appreciated ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12).

---

**vbuterin** (2021-03-29):

One option might be to switch to GF(2048) as your field, so you can secret share over the mnemonics directly?

---

**dstreit** (2021-03-29):

Yeah, that’s an interesting point.

I started with existing implementations of Shamir’s operating on hex values and used the hex representation of the mnemonic for them. But, maybe that really isn’t necessary anymore, now that I’m not using an existing implementation. Could go from mnemonic to mnemonic with no hex in between ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=9)

It does lean into the aspect of the project that I’m lease experienced with tho. But, maybe I can find someone to work with me on it.

---

**dstreit** (2021-03-30):

Okay, I think I see how to do this better with GF(2048). I’m going to give it a shot.

---

**dstreit** (2021-03-30):

I’ve updated the spec and implementation to use GF(2048) with primitive polynomial x^11 + x^2 + 1.

See https://github.com/ethereum/EIPs/pull/3450 (new MR)

And https://github.com/danielstreit/shamir-bip39 (same location as before)

---

**dstreit** (2021-04-01):

In my haste, I neglected that, originally, the shares were also valid BIP-39 mnemonics. By naively converting the mnemonic to shares, word for word, the shares would no longer be valid BIP-39’s ![:man_facepalming:](https://ethereum-magicians.org/images/emoji/twitter/man_facepalming.png?v=9). They wouldn’t have valid checksums.

We could instead convert the entropy portion of the mnemonic to shares and calculate the checksum from for each share to recreate a valid BIP-39. But, at that point, we’d need to convert the share mnemonic to hex to calculate the SHA256 to get the checksum.

So, did we gain anything by using GF(2048)? We’d still need to convert to hex at some point to create a valid BIP-39. Maybe then, the original solution where the initial BIP-39 is first converted to entropy is better? I might be missing something here, please correct me if I’m wrong.

Alternatively, if we decided that we didn’t really care that the shares were valid BIP-39 mnemonics, we could use the space where the checksum is to store the share id, avoiding the need to store any data outside the mnemonic.

I don’t really like this later idea. I think it is important that the shares are valid BIP-39 mnemonics, indistinguishable from any others, to hide the fact that there may be something greater behind it.

---

**dstreit** (2021-04-02):

Summarizing current state and open questions:

Thanks for looking! Any and all feedback is greatly appreciated :).

Background: As an Ethereum user, I’m concerned that the BIP-39 mnemonic backup of my wallet is a single point of failure. I’d like to use Shamir’s Secret Sharing Scheme to split it into shares that I can distribute for storage and later use to recover my original mnemonic.

I’d like each of the shares to also be a standard, BIP-39 mnemonic, so that if one is found/lost, the finder would not necessarily know that it was only one of a larger scheme.

So far, I’ve been primarily focused on building the UI for this using an existing implementation of Shamir’s scheme. But, I’ve gotten some feedback that in order to make this tool more broadly useful, and ensure recovery at some arbitrary point in the future when tooling may have changed, that I should use a standardized implementation of Shamir’s. Or, since that doesn’t exist as far as I’m aware, create one.

So, I’ve gone down the route of creating an EIP to specify a standardized approach for splitting a BIP-39 mnemonic into shares that are also BIP-39 mnemonics. Although this isn’t my core domain, I think I’ve gotten a good start and am hoping to get some feedback here :).

Questions:

- What’s a good choice for a Galois Field for this?

My spec originally converted the mnemonic to hex entropy and applied Shamir’s to the hex values using GF(256). The resulting hex shares were then converted to valid BIP-39 mnemonics.

[Earlier in this thread](https://ethereum-magicians.org/t/erc-3450-standard-for-applying-shamirs-to-bip-39-mnemonics/5844/6), it was suggested that I could use GF(2048) instead so we could apply Shamir’s directly to the mnemonic. The problem I see with this is that the resulting shares would not be valid BIP-39 mnemonics. (Unless we jumped through some hoops, only converting the entropy section of the mnemonic and calculating the checksum from there for each share. Doable, but then, what’s the advantage of using GF(2048) here?)

Would there be any advantage to using GF(16)? Or any other field? GF(256) seems like the most common in the wild, but not sure there are other considerations I should be thinking about in choosing the field.

- Does the choice of a primitive polynomial matter?

Other than being included in the specification and consistent across implementations, does the actual choice matter?

I’ve been following various reference implementations and using the lowest primitive polynomial. For GF(256), I used 29 (`$x^8 + x^4 + x^3 + x^2 + 1$`). For GF(2048), I used 5 (`$x^11 + x^2 + 1$`).

Are there any arguments for using a different primitive polynomial here?

Thanks for reading!

Links:

- Draft: Shamir + BIP-39 by danielstreit · Pull Request #3450 · ethereum/EIPs · GitHub (Note that the current state uses GF(2048), but does NOT output valid BIP-39s for shares. I’m planning on updating this based on feedback here.)

---

**nicolas** (2021-04-03):

The advantage of using GF(2048) is that you can map every shamir share to a valid mnemonic word. Since you are using BIP-39 you have 2048 words.

---

**dstreit** (2021-04-04):

Thanks for taking a look Nicolas!

Although this approach would result in shares with “valid mnemonic words”, the shares would not be valid BIP-39 mnemonics.

BIP-39 mnemonics have two components: entropy and a checksum (which is the first few bits of the SHA256 of the entropy). And, to make it more complicated, the divide between the two components is not between words. For example, a 12 word mnemonic has 132 bits total (11 x 12), including 128 bits of entropy and 4 bits of checksum.

So, this feels like it gets pretty dirty. We’d need to extract out the entropy bits from the generated shares, calculate the checksum and then create a different mnemonic, with the valid checksum. And then, we’d repeat this dance going the other direction.

Instead, if we convert the mnemonic to bytes of entropy before sharing, apply Shamir’s to those bytes, and then convert the resulting shares to BIP-39 mnemonics (ie using the shares as the entropy bytes, calculating the checksum, and converting to words), I believe we get a valid BIP-39 with less hassle than applying Shamir’s to the words directly. And, that would imply using GF(256) instead of GF(2048).

There is still a bit of a dance, from mnemonic to bytes, but it seems more straight forward to me. What do you think?

---

**nicolas** (2021-04-06):

I agree with you about the niceness of having shares be valid BIP-39s. Therefore, I agree that you need to secret share the first 128 bit and not the full 132 bits. However, I would go for GF(2^128) instead of GF(256). There is a chance where some people would want verifiable secret sharing (computational hardness). In that scenario, you won’t be able to use GF(256) the Field is small and discrete log is not hard. However, Discrete log is hard in GF(2^128) and GF(2^256). Verifiable secret sharing is needed where share holders want to verify that they got good consistent shares. A private key holder can distribute shares to individuals and each individual can check that his share is correct against a commitment to the polynomial holding the initial secret. Another place where having valid secret shares (GF(2^128) and GF(2^256)) is nice is with threshold signatures. Share holders can sign together a transaction.

---

**dstreit** (2021-04-07):

One of the primary goals of this project is to make it easy for non-technical users to store their keys safely. That means a user interface is mandatory. A CLI is not sufficient. To me, that means we need an implementation in JavaScript.

See, for example AirGap Vault. Its social recovery feature creates mnemonic shares using Shamir’s scheme, but it doesn’t follow a standard. Their code is currently written in TypeScript. It would be great if they adopt a standard like the one proposed here.

Similarly, I’m working on a UI that will make it easy for non-technical users to split their mnemonics in order to keep them safer. My project is also written in TypeScript.

And, if it becomes a standard, maybe others will adopt it for similar workflows in their own apps as well.

The point here is that it needs to be easy to implement correctly, even in a language like JavaScript. The max number in JavaScript is 2^53 - 1. So, to use a field larger than the max number would really complicate the implementation. GF(256) on the other hand is very easy to implement in JavaScript.

One additional complication of a field like GF(2^128) is that we’d need a different field for each supported strength of mnemonic. BIP-39 supports 128, 160, 192, 224, and 256. While not a big deal, supporting five different fields does add complexity to the implementation.

For a more articulate rationale for GF(256), written by folks with a lot more experience than me, see [slips/slip-0039.md at master · satoshilabs/slips · GitHub](https://github.com/satoshilabs/slips/blob/master/slip-0039.md#FiniteField). The use case is very similar to this one. Key differences are: this one focuses on interoperability with BIP-39. SLIP-39 adds a variety of additional features to facilitate sharing.

Regarding:

> Verifiable secret sharing is needed where share holders want to verify that they got good consistent shares.

> Another place where having valid secret shares (GF(2^128) and GF(2^256)) is nice is with threshold signatures. Share holders can sign together a transaction.

Both of these features sound very interesting. I had not considered them in the initial feature set for this, but am interested in learning more. Can you point me to any resources on this? What would it take to support these features in this spec?

I feel like additional implementation complexity could be justified if it supports additional, useful features.

Thanks again for digging into this spec with me! I really appreciate the feedback you’ve given and have learned a lot from it.

---

**danfinlay** (2021-04-07):

Curious if you’d considered Ian Coleman’s approach? His also results in mnemonics.

https://iancoleman.io/shamir39/

---

**nicolas** (2021-04-07):

Working in GF(2^256) can be done in Javascript. You just have to use a library to store the big (128-256 bits) numbers (and do arithmetic operations on those numbers). Metamask (written in javascript) signs your transactions on the browser (this is done in a field size of approx 2^256).

When working in applied cryptography, working in “big fields” is the norm (digital signatures, public key encryption, commitments… all require attackers no to be able to go through all the field in polynomial time (they would break discrete log, prime factorization …)). For debugging purposes, you would start in a small field and then make it bigger.

Supporting 5 different fields shouldn’t be hard, the same functions would work in all 5 (Lagrange interpolation, computing inverses…). I can even write the library in JavaScript and share it with you (if you want).

I am convinced that working in GF(256) is easier than the bigger fields. Easier: in the sense that you will be able to fit all the numbers you have in the regular variable of JavaScript. However, you will be doing multiple parallel secret sharings. You are effectively secret sharing smaller pieces of the secret and not the secret itself. In general, by doing that you loose two things: the ability to compute multi party computation on the secret shares directly, and any computational hardness that you can leverage in the big field (commitments).

Now whether someone can leverage those to build something useful, I don’t know(we have shares of a seed that generates sk/pk pairs, it would have been definitely useful if we have shares of sk direclty). But we are removing the ability for someone in the future to use them.

Look at how polynomial commitments work (you commit to the polynomial that you use to generate the shares). Maybe start with [Feldman’s scheme](https://en.wikipedia.org/wiki/Verifiable_secret_sharing#Feldman.E2.80.99s_scheme).

For threshold signatures maybe start with the basics [threshold signatures](https://www.unboundsecurity.com/blog/threshold-signatures/) and then look at why threshold signatures is easy with https~removeMe~://medium.com/bitbees/what-the-heck-is-schnorr-52ef5dba289f.

Also feel free to reach out on discord I will be happy to help.

---

**dstreit** (2021-04-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Curious if you’d considered Ian Coleman’s approach? His also results in mnemonics.
>
>
> https://iancoleman.io/shamir39/

Yeah! This was actually the project that inspired me to work on this.

It has a couple of deficiencies that I’m hoping to address.

The resulting share mnemonics aren’t valid BIP-39 shares. See open issue here: [Consider making shamir mnemonics BIP39 compatible on their own · Issue #1 · iancoleman/shamir39 · GitHub](https://github.com/iancoleman/shamir39/issues/1). The shares generated by this EIP are.

There is a cost to making the shares valid BIP-39s - the share id is not encoded in the mnemonic, so the user needs to store an additional piece of data. I discuss some alternatives and justification for this in the EIP. Would definitely be interested in other’s thoughts on this.

Ian Coleman’s approach lacks standardization. He is very clear about this. In the UI in large red font he writes, " There are no alternative implementations, meaning you are *totally dependent on this tool* if you use it. That is a dangerous situation to be in."

I don’t want to be in this situation. And, this is why I’ve gone down the route of trying to get an EIP and (hopefully) multiple implementations in different languages.

He also hasn’t fully spec’d out the application of Shamir’s. He’s [spec’d out what the share format looks like](https://github.com/iancoleman/shamir39/blob/master/specification.md), but not the field used for calculations. Looking at the code, he appears to be using GF(256) with irreducible polynomial $x^8 + x^4 + x^3 + x^2 + 1$, but that isn’t defined in the spec.

So, I kinda see myself taking what he started and trying to harden it into a more concrete standard (the EIP, proposed here).

I’m also working on a UI that I hope will have various UX benefits from Ian Coleman’s prototype, including better autocomplete for entering mnemonics and a confirmation stage to ensure that users copied the mnemonics correctly.

---

**dstreit** (2021-04-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nicolas/48/3712_2.png) nicolas:

> we have shares of a seed that generates sk/pk pairs, it would have been definitely useful if we have shares of sk direclty

It’s worth noting that we never handle *seeds* in this EIP. Only entropy.

We convert the initial mnemonic to entropy, generate shares of the entropy, then convert each share “entropy” to a mnemonic. We never convert the initial mnemonic nor the shares to actual seeds.

Not sure that actually changes anything that you’ve said, but seems like an important clarification.

I’ll do some more research, thanks for the links!

---

**nicolas** (2021-04-07):

One way to think about how these wallets work: is a pseudo random generator that takes a random number s (call it a seed) extract infinite random numbers s1,s2, s_infinity. Each number is then fed into a genkey function  that take s_i and produce a public private key pair pk_i, sk_i.

---

**dstreit** (2021-04-07):

I think we may be missing one another on terminology and that may be leading us to miss on the scope of this as well.

I’m using my terms directly from BIP-39, as interoperability with BIP-39 is the primary goal here.

1. Entropy - A set of psuedorandom bits
2. Mnemonic - An encoding of the entropy into words (bips/bip-0039.mediawiki at master · bitcoin/bips · GitHub)
3. Seed - Derived from the mnemonic (bips/bip-0039.mediawiki at master · bitcoin/bips · GitHub)
4. Wallets or Keys - Derived from the seed, following any of a variety of specifications (not covered by BIP-39).

The current EIP, 3450, is only concerned with 1 and 2. Although BIP-39 has an opinion on 3, this EIP does not.

The goal is to store the entropy more securely by creating shares of it. We use mnemonics on top of the entropy to make it more user friendly.

This EIP has no opinions on how the seed is generated from the mnemonic or how wallets are derived from the seed. This is intentional. It allows us to support different wallet derivations algorithms.

I’m pretty intent on keeping the scope here to storing shares of the entropy as mnemonics. Anything around deriving wallets or signing is out of scope, in my opinion.

> it would have been definitely useful if we have shares of sk direclty

If we shared the sk directly, we would need to have an opinion on how the keys are derived **and** we would only support a single wallet. Instead, we share the entropy and we can derive however many sks we want by any algorithm we want.

> threshold signatures

This is very interesting, but, in my opinion, out of scope here. Once again, it would require the EIP to have opinions on how keys are derived.

> verifiable shares

This is also very interesting, and while it doesn’t imply any opinions on how keys are derived, it does increase the scope here. Both for this EIP and for associated UIs.

I think I’m fine with assuming a trusted distributor here.


*(10 more replies not shown)*
