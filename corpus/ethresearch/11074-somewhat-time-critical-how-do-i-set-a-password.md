---
source: ethresearch
topic_id: 11074
title: Somewhat time critical — How do I set a password?
author: x
date: "2021-10-22"
category: Administrivia
tags: []
url: https://ethresear.ch/t/somewhat-time-critical-how-do-i-set-a-password/11074
views: 2609
likes: 7
posts_count: 9
---

# Somewhat time critical — How do I set a password?

This site required me to do OAuth to register. For privacy / data hygiene reasons I then removed my GitHub from this profile and de-authenticated the site in GitHub.

Next I changed my GitHub email address and deleted the previous address. Finally I also generated a new email address for this site to then remove the final remaining link to GitHub.

Question: How can I set a password on this site, such that I will be allowed to log in once my cookie expires? Can I just log in with the email that’s now in my profile, without a password?

## Replies

**hwwhww** (2021-10-22):

Well, the main reason why we disallow email login is for mitigating spamming. GitHub account association also provides some reputation reference in R&D community. (And considering dogfooding  Ethereum account login in the future)

I don’t think you can set password now. If you want to hide your main email/GitHub info, you could register a new GitHub account for ethresear.ch.

Sorry it’s not perfect, but IMO it’s not good to enable email login in ethresear.ch.

---

**x** (2021-10-22):

K … well the guys over at ethereum-magicians allow it. They also have 2FA ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**pavloMandryk** (2021-10-22):

Hi, this is my first reply, hope it can be helpful.

As [@hwwhww](/u/hwwhww) mentioned, there is no way you can set a password; but you still can recover access to the profile after cookie expiration.

The way to proceed would be creating a new GitHub account for the newly set “primary email” in your forum profile. You can access your profile using those GitHub credentials. This way you didn’t need to create an extra profile and still succeed to remove any trace of your main GitHub account.

To achieve privacy when creating a ethresear.ch profile just use a fresh email with a fresh GitHub account.

---

**x** (2021-10-22):

My session is still alive! Woohoo, clearly living on the edge here. Tbh, as some might have guessed, I didn’t really expect to receive a solution here. I just wanted to highlight that the current system seems inefficient.

Given how easy it is to create a separate GitHub account for registration here, what is the purpose of enforcing GitHub in the first place? If it’s for reputation purposes, then you shouldn’t be allowed to disassociate your GitHub again, and you should enforce a certain minimum GitHub account age or a certain minimum number of GitHub contributions.

The current system doesn’t protect us from anything. Instead, I only see negative outcomes:

1. People who don’t want all their profiles across the Internet correlated are forced to go through the extra step of setting up a throwaway GitHub account (it takes time to set up and secure) — there is a reason why people set their GitHub email to private
2. People who don’t have time to do that may need to unnecessarily sacrifice OpSec against their will
3. People who don’t know yet what they want are by default directed into a non-privacy maximizing choice and the use of single-sign on is wrongly presented to them as a best practice (by a reputable community)

Given the increasing scrutiny from all sides, we should all try to become less traceable, not more traceable. At least, you should allow the people who care to minimize their attack surface.

---

**MicahZoltu** (2021-10-22):

Is the theory here to try to leverage GitHub’s spam protections?  What is GitHub’s spam protection and can we just do that directly instead?

---

**pavloMandryk** (2021-10-22):

These topics were discussed [here](https://ethresear.ch/t/ethresear-ch-email-login-will-be-disabled-in-7-days/7369) alongside with the EAuth implementation.

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png)[Ethresear.ch: email login will be disabled in 7 days](https://ethresear.ch/t/ethresear-ch-email-login-will-be-disabled-in-7-days/7369/1)

> To mitigate spam and impersonator attacks, we decide to disable email login again and you can only log in with GitHub account.

[@hwwhww](/u/hwwhww) Are spamming and impersonator attacks the only reasons for disallowing email login? Did we have bad experiences with this before? How is ethereum-magicians managing these issues while allowing email login?

I agree on maximizing non-traceability and would like to point out two more implications of the GitHub login only: UX and security.

I believe that it is fair to say that a significant amount of potential users fall under a) don’t have an GitHub account or b) have a completely inactive GitHub account. For these users the lack of 2FA results on poor UX, of course, but also they are more likely to give up on security as they are probably less willing to set up and secure a GitHub account they don’t use.

On the other hand, in my personal experience as a GitHub user, the UX of the current system feels super smooth.

The advantages of having email login and GitHub auth would be:

- Privacy for those who don’t want their profile to be associated with their GitHub.
- More balanced UX.

For the current GitHub only system we have the following:

- Less privacy.
- A worst UX and security for non-GitHub-users.
- A better UX for GitHub users.
- Protection against spam and impersonator attacks.

![](https://ethresear.ch/user_avatar/ethresear.ch/x/48/7686_2.png) x:

> then you shouldn’t be allowed to disassociate your GitHub again

Is there a way to point to the GitHub account without using email as primary key? If this is non-trivial to make, we can’t enforce users to stick with one GitHub account since GitHub email can be changed.

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png)[Ethresear.ch: email login will be disabled in 7 days](https://ethresear.ch/t/ethresear-ch-email-login-will-be-disabled-in-7-days/7369/11)

> I believe we can add ENS name (or, ETH account) field in discourse. And then, we need to ask the GitHub login user to manually update that field to claim that “the one who has this ENS name / ETH account is me”. So when the user uses Eauth login later, it will be able to bind to the existing account.

When it comes to EAuth implementation we are still facing the same privacy issues, as the idea would be enabling to sign up with ENS but requiring to associate a GitHub account with it. (Still excited about EAuth though!)

---

**x** (2021-10-22):

If this is about impersonators, then the solution are cryptographic signatures, not some OAuth using some random website that some people don’t even feel comfortable using.

You could sign a message in your profile with GPG or you could even use an ETH key to sign it.

---

**x** (2021-11-02):

Hey friends — I can’t believe it, but I just came back after 10 days and my session is still live … ! Long live the cookies.

So, what did we end up with? Can this discussion be summarized as (not everyone thinks this! thank you for the constructive discussion so far):

- The reason for GitHub auth is to avoid impersonation
- Cryptographic signatures (OpenPGP, Minisign, ETH keys, …) would be a better solution than GitHub to verify identities/pseudonyms
- However, the target users of this forum don’t like using cryptographic signatures for this use case
- Thus the people in this forum want to keep using GitHub to avoid impersonation
- (They don’t care that others may not like that; either because it links their accounts unnecessarily, or because they just don’t want to use GitHub)

(There was more nuance, but I tried to dumb it down.)

**EDIT:** By the way … thank you all for voting me “User of the Month” … I feel very honored.

[![image](https://ethresear.ch/uploads/default/optimized/2X/1/1ff0d3b40d391ed0cf7671fdc8fdc68c25b8e28e_2_690x180.png)image1038×272 29 KB](https://ethresear.ch/uploads/default/1ff0d3b40d391ed0cf7671fdc8fdc68c25b8e28e)

