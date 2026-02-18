---
source: magicians
topic_id: 814
title: The UX of EIP 1102
author: danfinlay
date: "2018-07-19"
category: Web > User Experience
tags: []
url: https://ethereum-magicians.org/t/the-ux-of-eip-1102/814
views: 9646
likes: 22
posts_count: 39
---

# The UX of EIP 1102

To improve Ethereum browser security, multiple browsers are now working on implementing EIP 1102, which will no longer inject the provider API by default, but instead wait for the Dapp to request a web3 API before providing one, making web3 users undetectable to sites (including dapps!)



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bitpshr/48/190_2.png)

      [EIP-1102: Opt-in provider access](https://ethereum-magicians.org/t/eip-1102-opt-in-provider-access/414) [EIPs](/c/eips/5)




> Hi everyone. My name is Paul Bouchon and I recently joined the MetaMask team.
> MetaMask and most other tools that provide access to Ethereum-enabled environments do so automatically and without user consent. This exposes users of such environments to fingerprinting attacks since untrusted websites can check for a provider object and reliably identify Ethereum-enabled clients.
> This proposal outlines a new dapp initialization strategy in which websites request access to an Ethereum provider API i…

While this change has great privacy benefits, there are open questions about the UX of this kind of invisible API. Feature detection is impossible, and so Dapps will need to present some kind of open-ended log-in button that both tries to log on *and* suggests installing a web3 browser if the user doesn’t have one yet.

You can roughly see the issue in this EIP 1102 flow chart from [the original metamask issue](https://github.com/MetaMask/metamask-extension/issues/714):

[![flow chart](https://ethereum-magicians.org/uploads/default/optimized/1X/08875cbc2ec816c5f78bcff00bbe057c1184d108_2_690x498.png)flow chart1546×1116 187 KB](https://ethereum-magicians.org/uploads/default/08875cbc2ec816c5f78bcff00bbe057c1184d108)

I just wanted to open the thread here, to get our UX ring thinking about the future of log-in with privacy-centric browsers.

cc [@bitpshr](/u/bitpshr) [@ricburton](/u/ricburton) [@boris](/u/boris) [@beltran](/u/beltran) [@andytudhope](/u/andytudhope)

## Replies

**ricburton** (2018-07-19):

This is great, Dan. I think that WalletConnect could be really helpful here. Pedro Gomes is leading the project full time and I am sure he has lots to say on this. Will send this to him.

I wrote about the flow here: https://medium.com/@ricburton/metamask-walletconnect-js-b47857efb4f7

[![09](https://ethereum-magicians.org/uploads/default/optimized/1X/7dad546eae7067547b8202804bffb2e33901cec7_2_676x500.jpg)092798×2068 437 KB](https://ethereum-magicians.org/uploads/default/7dad546eae7067547b8202804bffb2e33901cec7)

---

**bitpshr** (2018-07-19):

Thanks for starting this [@danfinlay](/u/danfinlay)! Some additional thoughts:

- Optionally inject web3
In addition to injecting a provider API after user approval, MetaMask also plans to conditionally inject web3 based on an optional web3 property on the provider request. This is for easier backwards compatibility: while dapps will still have to update to initiate the provider request, they won’t also have to bring in web3.js if they don’t want to.
- Cache approved websites
MetaMask also plans to cache website origins that have been approved for provider access. For example, if a user visits foobar.com and approves provider access, MetaMask will remember this approval in the future and bypass user approval altogether next time the user visits foobar.com. This saved approval data can be cleared at any time.
- Difficult to know dapp-level UX
EIP-1102 intentionally focuses on the protocol for requesting a provider API, not the UX around it. There’s nothing to prevent a dapp from requesting provider access immediately on page load without any user action, so it’s important for dapp developers to converge on a common UX here (like WalletConnect?) I still feel it’s inevitable that some dapps will request provider access using arbitrary UX flows. For example, what if a dapp uses a login system completely unrelated to Ethereum accounts? This type of dapp would probably request provider access immediately on load and not design it as a login button the user must click, since the dapp has an unrelated login system already in place.

---

**JaceHensley** (2018-08-09):

RE: dapp-level UX

So our flow currently allows detection of install while the user remains on our dapp’s signin page. What we do is inject an iframe that refreshes until it detects web3 (since extensions can’t inject into already loaded pages). This allows the user to come to our site without MM installed and either be instructed to install MM or continue. And the page only refreshes once the iframe has detected a web3 instance.

One way forward would be to have a timeout before switching to a different view telling the user to install a dApp browser. But there are a few problems with that, the first being users would have to wait for the timeout before being instructed to take an action, the second is what if the user just takes a little longer than the timeout to accept? This would cause the dApp to move to the “Please install a dApp Browser” step too early.

Curious if anyone has any thoughts on other ways forward that don’t cause UX regression

---

**bitpshr** (2018-08-09):

Hi [@JaceHensley](/u/jacehensley), thanks for sharing information about your dapp. You’re right that the UX issue of detecting and suggesting MetaMask (or some other dapp browser) is challenging due to EIP-1102. It’s an unavoidable UX issue: malicious sites currently track Ethereum users the exact same way honest dapps detect MetaMask, so to protect user privacy, dapps can’t know if MetaMask is installed.

Here’s one flow that may work:

1. User without MetaMask navigates to dapp
2. Dapp posts message requesting provider
3. Browser ignores message since MetaMask isn’t installed
4. User tries to interact with dapp
5. Dapp attempts to use web3 or ethereum but they aren’t defined
6. Dapp shows user warning: “Please use a supported browser such as MetaMask.”

The main difference between this flow and current flows is that detection and user warning are done only when the user attempts to interact with the dapp in a way that uses `web3` or `ethereum`. If these globals aren’t defined at that time, that means the user either hasn’t approved access or isn’t in a supported browser. In either case, the dapp could show a warning message to the user (or an iframe to install MetaMask) only when it needs to use these variables instead of checking for them immediately on page load.

---

**JaceHensley** (2018-08-09):

That seems like poor UX to me. Wait for a user to try and do something and only after a user tries to interact with your dApp do you tell them they need something else. I bet that would stop people from continuing. It just adds another layer of friction to signing up for/using a dApp.

Speaking of malicious sites wouldn’t this open it up for users to constantly get asked to accept or decline a sites request to inject ethereum?

---

**bitpshr** (2018-08-09):

[@JaceHensley](/u/jacehensley) I’m not sure if users would be more turned off by a dapp suggesting an extension be installed only when they try to interact with it (meaning they’ve seen the dapp, what it is, and chose to interact with it) as opposed to when it first loads. Both are equally as obtrusive, but the former at least allows the user to see your dapp before being asked to install new software. Still, I’m not a designer, so I probably have little value to add here. The flow above was just one example of a flow that could work, but better approaches may exist.

As for the concern of malicious sites spamming provider requests, once a user rejects access on a given site, they won’t be presented with additional approval windows unless they clear their cached approval data. This is similar to how webcam approval works in browsers today.

---

**JaceHensley** (2018-08-09):

Check out how we are handling it on [bloom.co/app/signup](http://bloom.co/app/signup). We help onboard users by laying out what they need to do to use our dApp. Laying everything out upfront helps reduce friction and doesn’t make the user guess what’s next.

I do like the request permission to get ethereum injected pattern. I just don’t like that there’s no way to tell if a user has installed MM.

So our flow wouldn’t ask for permission right away, we’d probably have the user click a button in the list of steps after “Install Metamask”. Something like “Allow Access To Metamask” with Allow Access underlined and acting like a button. When a user clicks that then we would send off the request.

The crucial part is knowing what step the user is on so they can be helped along the way without wasting their time

---

**JaceHensley** (2018-08-09):

The goal is mass adoption of dapps and crypto in general. Fingerprinting based on using a dapp browser would be like fingerprinting based on if the user’s browser has notification possibilities.

The real problem is exposing the user’s ETH address not that they are using Metamask or another dApp browser.

---

**bitpshr** (2018-08-09):

I totally agree that mass adoption is the goal, but a lack of user privacy and resulting phishing campaigns have been negatively effecting the community for some time. Fingerprinting based on dapp browser usage informs malicious sites that a user holds and uses Ethereum, and has been heavily used to run targeted ad and phishing campaigns, regardless of access to the provider or accounts.

I agree the UX needs to be ironed out for the case where a user has no dapp browser. The above approach is one way, but I’m sure there are others that are better. I wish I had more design experience to speak from.

---

**JaceHensley** (2018-08-10):

If UX still needs to be ironed out doesn’t that indicate that this EIP is not ready?

---

**bitpshr** (2018-08-10):

[@JaceHensley](/u/jacehensley) The intention of EIP-1102 is to fix user privacy. While it’s an interesting challenge, how dapps adjust their individual user experiences based on this new change is completely outside the scope of the proposal. Current UX relies on objectively unsafe injection, so changing it is unavoidable.

The only issue with the UX is that dapps can no longer detect if a user has a dapp browser installed, which is the very intention of the EIP: to remove the ability to detect this information (that [malicious sites have successfully used](https://medium.com/metamask/new-phishing-strategy-becoming-common-1b1123837168) to target Ethereum users for far too long.)

We’ve already identified one UX pattern above that works, but is arguably worse than what we currently have. That’s the whole point of this thread, to collaboratively identify the best UX to accommodate a necessary and crucial programmatic privacy change.

---

**danfinlay** (2018-08-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jacehensley/48/613_2.png) JaceHensley:

> wouldn’t this open it up for users to constantly get asked to accept or decline a sites request to inject ethereum?

I think this could be mitigated by including a “block future requests from this site” checkbox with the sign-in page.

---

**danfinlay** (2018-08-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jacehensley/48/613_2.png) JaceHensley:

> If UX still needs to be ironed out doesn’t that indicate that this EIP is not ready?

I basically agree. We’re trying to design the correct way for a browser to work, and if there isn’t even a pleasant path for users to onboard with the given changes, it’s a strong indication that we have a ways to go.

However, Paul’s points are also important: As long as web3 browsers are a minority, and as long as they are usually MetaMask users, any detectable API surface [exposes users to specific phishing attacks](https://medium.com/metamask/new-phishing-strategy-becoming-common-1b1123837168).

That said, I think there is a silver lining:

Our active response to that type of phishing attack seems to have resulted in a reduction of its incidence rate, so it’s possible “web3 detection attacks” are indeed not the worst kind of fingerprinting.

Also, if we aim for the long-term game, where everyone has a web3 browser, and there are many kinds of web3 browser, this kind of fingerprinting becomes less and less dangerous, again emphasizing that the account detection is potentially the worst part of this.

## On the other hand

While this change requires a UX change, it doesn’t need to be awful, it just would need to embrace some different assumptions:

I think the basic flow would be something like this:

- A button that says Sign in with Ethereum.
- When clicking the button, on a web3 browser, the login request appears.
- When clicking the button, it could change to “Install a Web3 browser to begin”. Since web3 browser users are seeing a login request, this is an appropriate moment to assume the user is not using a web3 browser within the site’s UI, educate, and suggest an install.

### That all said

I do think most of the discussion so far has focused on the technical aspect, not the UX, so I’m very glad that [@JaceHensley](/u/jacehensley) is thinking of the user and pushing back here. I think it’s a decision the ecosystem needs to make together, and stick to.

It seems like it’s pretty clear that the easiest way to improve the UX is to accept a limited fingerprinting surface, to allow sites to intelligently suggest user actions, and so the question for the community is:

Is it acceptable to provide web3 fingerprinting for the benefit of user experience?

In an ecosystem with so much working against our UX in the name of security, it might be a concession worth embracing.

---

**danfinlay** (2018-08-14):

We’ve been tossing around ideas for the UX more, and I do believe we can make the UX of 1102 pleasant.

In the next MetaMask release we’re going to include a mocked version of this user consent UI, so dapp developers can experiment with the changed onboarding flow.

We’re also going to produce an example dapp to demonstrate that we can have both perfect privacy and good user experience.  Hopefully that dapp will inspire others to further improve on the experience.

While web3 fingerprinting might not be a big deal in a perfect world where everyone is using web3 browsers, we’re a long way from that world. Maybe once every browser is adopting web3 standards, we can re-introduce some global APIs for the sake of purely improved UX, but in the meanwhile, I think it’s worthwhile for us to make a few changes to our UX assumptions for the sake of protecting our very highly targeted community.

---

**dustinvs** (2018-08-14):

Hoping you provide some facility a la my comments here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dustinvs/48/786_2.png)
    [EIP-1102: Opt-in provider access](https://ethereum-magicians.org/t/eip-1102-opt-in-provider-access/414/30) [EIPs](/c/eips/5)



> So, re: The UX of EIP 1102 - looking for a way to guarantee both user control of privacy and preserve the relative ease of UX available with current Metamask/web3.
> My general idea to solve this is basically to find a way to automatically push a refresh and injection of window.ethereum based on an application requesting that, upon install of Metamask, their still-open tab will be able to have a pending request of availability somehow notify the user that they’ve requested access, and then upon a…

If Metamask’s going to permanently move in the direction of an obfuscated request-access system, hopefully you can at least provide a way for apps to seamlessly request access pre-Metamask install and then receive a refresh with window.ethereum available when it’s granted.

---

**danfinlay** (2018-08-14):

Since WebExtensions are not able to receive messages when they are not installed, detecting the moment one is installed would probably require a sort of hack like described above:

> What we do is inject an iframe that refreshes until it detects web3 (since extensions can’t inject into already loaded pages).

This could be done with an iFrame that requests a login, and wrapped into a general purpose library, enabling the UX that you’re talking about.

---

**JaceHensley** (2018-08-14):

I thought about sending a request from the iframe but I don’t like that much since the user should be in control of when that request is sent.

Really I think that a limited fingerprinting surface area is a great middle ground. For instance Brave has it’s own userAgent. I think Metamask and others could follow that. Maybe not userAgent exactly but something like that

---

**ricburton** (2018-08-14):

One quick thought: every browser (including Brave) let’s the page know that it is there.

If we let the web page know a web 3 tool is there: Is it not the same principle?

I think it is really helpful for a page to know whether the user has any of the tools necessary or not. Perhaps I am missing something ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**ricburton** (2018-08-14):

Just saw this. Yeah I agree. I am comfortable with the middle ground of: “this is someone who has got set up on Ethereum”.

Another example: Opra browser on Android?

I just wonder if we are over-swinging from usability to privacy.

Would love to hear more about how MetaMask is thinking about it.

With that said, [WalletConnect.org](http://WalletConnect.org) is opt-in with the QR code.

---

**dustinvs** (2018-08-14):

Unfortunately with the iframe approach, you lack the ability to enqueue an access request prompt *before Metamask has been installed*.  If you can use a cookie or localStorage entry to enqueue a request, then you don’t have to implement something like a refreshing iframe or interval retry logic which could potentially bug the user if they’re just rejecting the requests.  I think if you implement the totally opaque approach, then it’s a must to implement a way of enqueuing a request before the extension is installed.  As a general rule it’s bad practice in JS to implement polling logic instead of promises or event callbacks, this is the same principle.


*(18 more replies not shown)*
