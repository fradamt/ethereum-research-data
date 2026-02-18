---
source: magicians
topic_id: 10670
title: "RFC: Limiting provider object injection to secure contexts"
author: kdenhartog
date: "2022-09-04"
category: EIPs > EIPs interfaces
tags: [wallet]
url: https://ethereum-magicians.org/t/rfc-limiting-provider-object-injection-to-secure-contexts/10670
views: 2902
likes: 0
posts_count: 22
---

# RFC: Limiting provider object injection to secure contexts

At Brave, we’ve been thinking more about what’s necessary to secure wallets and limit attack vectors with wallets. Recently we’ve implemented our wallet to align with the [secure contexts web API](https://www.w3.org/TR/secure-contexts/). We’d like to propose this being standardized as a common implementation point for wallets so that dApps can have a level of certainty about how they can use iframes and minimum requirements of HTTP(s) etc.

Where do other wallet providers fall on this? Implementation for this should be rather simple given that all major browsers have already implemented `window.isSecureContext` so a check just needs to be added before injecting the provider object.

## Replies

**kdenhartog** (2022-09-07):

Note, [@rekmarks](/u/rekmarks) I’ve added an additional optional test case to handle additional backward compatibility for the 3P iframe case. Here’s [the commit](https://github.com/ethereum/EIPs/pull/5593/commits/72209e0fd712d336091a68dd6aac1895d88074d6) where that was added. With that in mind, I made this a MAY given that most wallets are extensions at this point and won’t be able to support it.

Additionally, I did kick off a discussion at W3C to try and get the permissions API extensible for browser extensions [here](https://github.com/w3c/permissions/issues/383). For any implementers who are following this discussion and have implemented as an extension I’d suggest subscribing to that thread.

---

**SamWilsn** (2022-09-20):

> Provider objects SHOULD NOT be accessible in private (incognito) windows.

Should this be up to the user? I know firefox lets me choose which addons run in private browsing mode.

---

**kdenhartog** (2022-09-20):

We were debating this internally as well. I think there’s some wiggle room here. Originally I went with MUST NOT as we don’t actually inject this into incognito (chrome refers to these as off-the-record) windows so I figured stronger language would produce better webcompat across wallets.

I looked into the original discussions that occurred when we originally shipped this. It looks like we took the more conservative approach to avoid debate around the privacy impact here and what sorts of fingerprinting risks we may introduce by doing so. However, our team was open to reviewing this and allowing this to be exposed in incognito windows.

However, given that most extension based wallets are going to require the extension be toggled on by the browser first this will fundamentally be an “opt in” scenario. For this reason I think the best we could do here is a MAY in order to provide the most accurate reflection of what might happen if the dApp is in an Incognito window.

WDYT about changing to MAY?

---

**MicahZoltu** (2022-09-21):

This needs a better motivation/security considerations than “people at some point in history thought it was a good idea to limit access to extended resources to secure contexts only”.  There may be very good reasons for it, but those should be listed here rather than just saying “other people do it”.

---

In browsers, `*.localhost` and `localhost` should be tightly coupled to the loopback device (you shouldn’t do a hostname lookup), and as a consequence it should be considered a secure context.  See the fourth paragraph of [Secure contexts - Web security | MDN](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts#when_is_a_context_considered_secure) along with the note about pre-FF 84.  Because of this, the security considerations section should be adjusted to account for this (and separately, Brave should implement this if they haven’t yet, though I thought it came with Chromium latest).

Edit: Hmm, looks like you mention the localhost issue in the backwards compatibility section.  Can we just say that browsers implementing this **MUST** implement localhost as secure context as a prerequisite?  They all should be doing that anyway, and I would rather have that requirement than add complexity to *every* wallet having to deal with localhost not being secure.

---

**MicahZoltu** (2022-09-21):

I’m not a fan of this:

> Provider objects SHOULD NOT be accessible in private (incognito) windows.

As a user, I often *want* to use my wallet from a private window (sometimes behind TOR as well) because I want to minimize tracking and fingerprinting.  I can appreciate that the use of a wallet probably fingerprints me (a wallet could avoid this fingerprinting, but it would be complex/hard), but disallowing all wallet interactions in private browsers feels overly limiting to me.

---

**kdenhartog** (2022-09-22):

> This needs a better motivation/security considerations than “people at some point in history thought it was a good idea to limit access to extended resources to secure contexts only”. There may be very good reasons for it, but those should be listed here rather than just saying “other people do it”.

Do you mean the EIP as a whole or something specific to the content in there?

---

**kdenhartog** (2022-09-22):

> Can we just say that browsers implementing this MUST implement localhost as secure context as a prerequisite?

I don’t think that’s possible. How would a wallet detect if they’re operating in a browser that’s done this or not?

> They all should be doing that anyway, and I would rather have that requirement than add complexity to every wallet having to deal with localhost not being secure.

This is why I went with optional normative language here is because it should be up to the implementers to decide what sorts of security stance they want to take on this. In the case of Brave we have certainty around this so we didn’t need to consider implementation concerns around this. We have additional capabilities to do this because we hook our wallet into the browser directly where as pretty much everyone else other than Opera is limited to what’s exposed via the extensions API and the web platform.

---

**kdenhartog** (2022-09-22):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> As a user, I often want to use my wallet from a private window (sometimes behind TOR as well) because I want to minimize tracking and fingerprinting. I can appreciate that the use of a wallet probably fingerprints me (a wallet could avoid this fingerprinting, but it would be complex/hard), but disallowing all wallet interactions in private browsers feels overly limiting to me.

Sounds good, I think most people here seem to be in line with this thinking. Will update it to a MAY as that’s the best we can do given extension wallets require a user to opt in to using the wallet in a private tab. This makes it so dApps should assume by default that it’s possible that it won’t be injected in the first place. Most fail on this case properly anyways because they assume that a user may not have a wallet at all.

---

**MicahZoltu** (2022-09-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> Do you mean the EIP as a whole or something specific to the content in there?

The EIP as a whole.  The abstract and motivation section at the moment just basically says “it is considered industry best practice to do X, so we should do X”.  I have been in the industry long enough to have a mild distrust of “industry best practices” as often they are born out of regulation, a different environment, or with good intent originally but bent out of shape over time.

In the motivation/abstract of this EIP it should establish what attack vectors are present against users that are prevent/mitigated if this standard is followed.  At the moment, there are no attack vectors described so one cannot effectively evaluate whether this standard would actually protect against anything.

---

**MicahZoltu** (2022-09-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> I don’t think that’s possible. How would a wallet detect if they’re operating in a browser that’s done this or not?

Hmm, reading over this EIP again I think maybe this should be `Informational` rather than `Interface`?  IIUC, this is basically a recommended set of best practices for wallet authors, but if a wallet doesn’t comply there is no interoperability breakage that would occur?  Essentially this EIP is “if you implement this you are better able to protect users from bad things” rather than “if you implement this you’ll be able to interop with third parties more efficiently/better”?

If this understanding is correct, then my original comment doesn’t make sense.

---

**MicahZoltu** (2022-09-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> Sounds good, I think most people here seem to be in line with this thinking. Will update it to a MAY as that’s the best we can do given extension wallets require a user to opt in to using the wallet in a private tab. This makes it so dApps should assume by default that it’s possible that it won’t be injected in the first place. Most fail on this case properly anyways because they assume that a user may not have a wallet at all.

Kind of separate from this EIP, it would be nice if extensions in private mode were off by default but trivial to enable (e.g., by clicking on the extension icon).  This could perhaps be achieved by having a separate setting for “Alow this extension to …” for normal and private browsing windows, and it would default to “On all sites” for normal windows and “On click” for private windows.

---

**Pandapip1** (2022-09-22):

I mean, it’s pretty trivial to enable it in private/incognito even now:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/0/0b5787a0a3a4c1edef63b06dcef054dd2ed85233.png)image781×140 12.9 KB](https://ethereum-magicians.org/uploads/default/0b5787a0a3a4c1edef63b06dcef054dd2ed85233)

I suggest that the EIP use the following wording:

> Provider objects SHOULD NOT be accessible in private (incognito) windows, unless the user explicitly opts-in, in which case provider objects MUST be accessible in private (incognito) windows.

---

**kdenhartog** (2022-09-26):

Is there a way to detect whether it’s a private window from a web pages perspective? Ideally we should be making these statements reflect things that can be tested in code so that we can automatically check compliance rather than requiring someone to manually test it. The purpose in this would be so that we can use test suites to automatically identify areas of incompatibility between different implementations.

---

**Pandapip1** (2022-09-27):

> Is there a way to detect whether it’s a private window from a web page’s perspective?

There are only indirect methods. See [GitHub - Joe12387/detectIncognito: JavaScript detection of Incognito & other private browsing modes on Chrome, Edge, Safari, Brave, Firefox, Opera and MSIE.](https://github.com/Joe12387/detectIncognito)

---

**SamWilsn** (2022-09-30):

I think the wording in the EIP should be:

> Provider objects MUST NOT be accessible in private (incognito) windows until enabled by the end user.

---

**kdenhartog** (2022-09-30):

I believe [@Pandapip1](/u/pandapip1) suggested similar wording in the PR and my reasoning for not chasing it was that it’s not something that can be tested easily making it hard to identify if implementations are actually complying with this statement. As this moves into the later stages I intend to write a test suite for this so It doesn’t make sense to me to write normative language that requires manual testing for developers to check. I’ve chosen the language for this pretty precisely in this case to account for these aspects of the text.

---

**Pandapip1** (2022-10-03):

> I intend to write a test suite for this

I would highly suggest not doing this. I find that most problems with EIPs that contain test suites are with the test suites themselves.

---

**kdenhartog** (2022-10-03):

I may be miss-reading into your comment here, so please correct me if I’m wrong, but this seems to lead me to the conclusion that the focus of EIPs is on writing potential design specs down for public comment rather than shipping interoperable code. I’m less interested in the former and extremely interested in the latter. I’m surprised to hear you say the risks out weigh the benefits here as that exact process has been used to ship numerous web browsers. Without these test suites I doubt we’d even be able to talk on this website right now. Surely I must be misunderstanding what you’re saying here as test suites have proven invaluable in terms of shipping interoperable code.

---

**MicahZoltu** (2022-10-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> I would highly suggest not doing this. I find that most problems with EIPs that contain test suites are with the test suites themselves.

You should write tests, I think what [@Pandapip1](/u/pandapip1) is referring to is that you shouldn’t include entire testing infrastructure in the EIP itself.  A simple list of inputs and expected outputs is sufficient, you shouldn’t include a package.json, files written in JS (or whatever language), etc.

---

**Pandapip1** (2022-10-12):

I wouldn’t go so far as to make it a ‘should.’ Most EIPs don’t include them, and I find it encourages slightly vaguer specs (thankfully this isn’t the case in this EIP). Just make the tests self-contained and simple, such as a plain html file with no dependencies and inline JS.


*(1 more replies not shown)*
