---
source: ethresearch
topic_id: 7369
title: "Ethresear.ch: email login will be disabled in 7 days"
author: hwwhww
date: "2020-05-08"
category: Administrivia
tags: []
url: https://ethresear.ch/t/ethresear-ch-email-login-will-be-disabled-in-7-days/7369
views: 3892
likes: 9
posts_count: 16
---

# Ethresear.ch: email login will be disabled in 7 days

Thank you for using etheresear.ch forum!

Email login was enabled during the last time we restored the system. To mitigate spam and impersonator attacks, we decide to disable email login again and you can only log in with GitHub account.

If you were using email login, don’t worry! Please register a GitHub account **with the same email** to log in ethresear.ch, your previous posts and account content would remain unchanged.

Thanks.

## Replies

**vbuterin** (2020-05-08):

Should we just dogfood and enable logging in with an ethereum account? I remember [@virgil](/u/virgil) or [@Ping](/u/ping) had a prototype for log-in-with-ETH on discourse?

---

**hwwhww** (2020-05-08):

It’s still on our radar! I *think* one of pending issues that [@virgil](/u/virgil) wanted to solve with ENS team is how to handle ENS transfer for authorization on discourse side, or even on ENS side.

A future issue is how the merge people’s current discourse account and new Eauth login account gracefully.

Interesting issues, we  *can*  introduce Eauth now if we sacrifice some (?) UX though.

---

**axic** (2020-05-08):

Just as discourse supports linking and login via Github, cannot the eauth login be added optionally, so that both github and eauth work at the same time?

---

**hwwhww** (2020-05-08):

We can have multiple authorization options at the same time.

If we have both email login and GitHub oauth (as status-quo), and they can be merged together automatically well since the GitHub account identifier is the email you used to register GitHub account.

But for Eauth case, since you don’t register your Ethereum address / ENS with an email address, it will create a new discourse account when you use Eauth login. ([@Ping](/u/ping) please correct me if I’m wrong!)

---

**axic** (2020-05-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> But for Eauth case, since you don’t register your Ethereum address / ENS with an email address,

I see. But wouldn’t it be possible to add a field for “ENS name” in discourse (like now there’s the email field + github link) so the linking happens?

Alternatively (though I am not a big fan due to the privacy aspect) [EIP-634](https://eips.ethereum.org/EIPS/eip-634) could be used to link an ENS record to an email.

---

**kmichel** (2020-05-09):

Successfully logged in with it.

---

**vbuterin** (2020-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> how to handle ENS transfer for authorization on discourse side, or even on ENS side.

By ENS transfer you mean what happens if an ENS name is transferred to another account? Wouldn’t the natural answer be “well, for future logins start verifying signatures against that new account instead of the current one”? What’s the problem?

---

**hwwhww** (2020-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> I see. But wouldn’t it be possible to add a field for “ENS name” in discourse (like now there’s the email field + github link) so the linking happens?

I believe we can add ENS name (or, ETH account) field in discourse. And then, we need to ask the GitHub login user to manually update that field to claim that “the one who has this ENS name / ETH account is me”. So when the user uses Eauth login later, it will be able to bind to the existing account.

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> Alternatively (though I am not a big fan due to the privacy aspect) EIP-634 could be used to link an ENS record to an email.

Right, adding the email field in ENS can also solve the password recovery issue on discourse! I understand why we may be against it, we are trying to dogfood with a decentralized solution, but we still want the email system to prevent a user from losing their properties forever. ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> By ENS transfer you mean what happens if an ENS name is transferred to another account?

Yes.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Wouldn’t the natural answer be “well, for future logins start verifying signatures against that new account instead of the current one”? What’s the problem?

I think the authentication follows the authorized controller of the ENS name, and use ENS name as the default handle name? It doesn’t take ENS as the first-class [when searching for an associated account](https://github.com/pelith/discourse-eauth/blob/10b14d9fa37fe453a1f77671842159925afa3fce/plugin.rb#L39) (ping [@Ping](/u/ping) to verify it).

---

**Ping** (2020-05-09):

[@virgil](/u/virgil) suggests that we can use ethmail.cc by default, but at present ethmail seems not so well functioned and decentralized. ![:cry:](https://ethresear.ch/images/emoji/facebook_messenger/cry.png?v=14)

In Eauth scenario, account address is the primary key. And for ENS you need to not only own an ENS but also set it as your address’s reverse lookup name, then it would be displayed as your nickname.

BTW, Eauth supports contract address login with EIP1271. I highly recommend this one. You can have multiple authenticate keys, timelock, social recovery, and lots of good stuff, without overhead to the platform. ![:mage:](https://ethresear.ch/images/emoji/facebook_messenger/mage.png?v=14) ![:mage:](https://ethresear.ch/images/emoji/facebook_messenger/mage.png?v=14) ![:mage:](https://ethresear.ch/images/emoji/facebook_messenger/mage.png?v=14)

Login with: Gnosis safe / Argent / Authereum / Dapper / etc

code: [GitHub - pelith/node-eauth-server: An OAuth-compatiable service based on Ethereum credentials to authenticate users on a website. See live version at https://eauth.pelith.com/ https://forum.hakka.finance](https://github.com/pelith/node-eauth-server)

demo: https://eauth.pelith.com/

Discourse + Eauth prototype: https://discourse-ens.pelith.com/

---

**vbuterin** (2020-05-10):

I definitely like eauth!

---

**gkapkowski** (2020-05-13):

Hi, I’ve build Cryptoauth and I have working plugin for discord that enabled authentication with Ethereum address. Let me know if you would be interested in experimenting with it.

Working example: https://community.cryptoverse.cc/

It also has ability to limit logins to only those addresses that hold certain tokens. Example: https://marketpunks.cryptoverse.cc/

---

**gkapkowski** (2020-05-13):

[@Ping](/u/ping) nice work with Eauth! I would love Cryptoauth to look like this ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

I’m also the person behind ETHMail so if you need something done with it let me know ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=14)

---

**gkapkowski** (2020-05-13):

You can find [cryptoauth.io](http://cryptoauth.io) discord plugin at https://github.com/CryptoverseCC/discourse-openid-connect It’s a fork that creates users in the background instead of asking people to confirm creating users.

---

**x** (2021-10-22):

Just found this discussion and realized that it’s related to my thread here: [Somewhat time critical — How do I set a password?](https://ethresear.ch/t/somewhat-time-critical-how-do-i-set-a-password/11074)

In my opinion, it’s not a good idea to restrict people to GitHub OAuth, and I explain in detail why that is in the thread above.

Besides, some people just don’t feel comfortable using GitHub and instead use self-hosted repositories or [codeberg.org](http://codeberg.org). We shouldn’t force those people to sign up for a website that they don’t feel comfortable using.

