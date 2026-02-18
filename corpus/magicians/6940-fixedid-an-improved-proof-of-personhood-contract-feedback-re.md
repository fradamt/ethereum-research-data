---
source: magicians
topic_id: 6940
title: "FixedID: an improved proof-of-personhood contract (feedback requested)"
author: corbt
date: "2021-08-24"
category: Magicians > Primordial Soup
tags: [identity]
url: https://ethereum-magicians.org/t/fixedid-an-improved-proof-of-personhood-contract-feedback-requested/6940
views: 1785
likes: 6
posts_count: 7
---

# FixedID: an improved proof-of-personhood contract (feedback requested)

I’d love to hear the community’s thoughts on the following concept for an improved proof-of-personhood protocol I’m tentatively calling “FixedID.” It fixes (hah) a number of issues with existing proof-of-personhood implementations that make it much more useful for authentication in both web2 and web3 apps, while fully preserving privacy.

## High-Level Overview

**Every person gets a permanent integer ID.** This is the key difference between FixedID and [existing](https://www.proofofhumanity.id/) [implementations](https://www.brightid.org/), and makes everything else possible. Instead of simply authenticating that a given wallet belongs to an individual, the system issues a static, immutable integer ID to each individual (their “FixedID”). The FixedID contract maintains a mapping of FixedIDs to wallets.

**FixedIDs are always recoverable.** An individual can recover their FixedID and assign it to a new wallet using one of three flows: (1) by using their existing FixedID wallet to sign a request, (2) by selecting “recovery users” who can then vote to recover the wallet, or finally (3) through an arbitration process on [Kleros](https://kleros.io/) or a similar platform. In all three cases, a waiting period is required before transferring ownership to allow for appeals.

**FixedIDs are ideal for authentication.** A FixedID can be used to sign in to a web2 or web3 application. This sign-in uses a zero-knowledge proof to assure the app that the account belongs to a unique human, while not revealing *which* specific human it belongs to. In addition to eliminating sybil attacks, this removes the burden of account recovery from app creators.

**FixedIDs owners receive a basic income token.** FixedIDs will issue a built-in basic income token, with issuance calculated to produce a modest annual inflation of ~2.3%. All FixedID users in good standing will qualify to receive the token.

## Signing Up/Proving Personhood

The [ProofOfHumanity](https://www.proofofhumanity.id/) signup process is a good model here. ProofOfHumanity’s process works as follows:

- Upload a picture of yourself and a video that involves speaking.
- Post collateral (currently 0.1ETH) that you’ll forfeit if your account is judged fake.
- Find an existing PoH user willing to vouch that you’re a real person (if your account is judged fake, they lose their account too).
- Wait 3 days to give challengers time to review the submission.
- If no one challenges your submission, your collateral is returned and your account is live.

There are a few modifications that I think would make this process more effective:

- The collateral should be deposited permanently. That way challengers are incentivized to always be scanning the network, instead of only focusing on new submissions. The permanently locked collateral can also be much smaller (~20USD) and still achieve its intended effect.
- Initially, no vouchers should be required to minimize barriers to entry. Over time the voucher requirements can be raised. When voucher requirements are added they should be weighted according to graph connectedness, to prevent eg. 5 scam accounts all just vouching for each other.
- The initial signup and posting of collateral can be done with a credit card to make the onboarding much simpler for non-crypto users. (I’ll need legal advice on this, but a strong case can be made that since the collateral is never returned, you’re just paying for the service of creating/verifying your account instead of buying a token, so a brokerage license/KYC shouldn’t be required.)

## Challenging Fraudulent Users

Again, ProofOfHumanity’s process here seems reasonable. As mentioned above, the primary modification I propose is dropping the challenge collateral significantly to ~$20 and locking it perpetually.

Since $20 is too little to justify a jury trial, this requires adding an extra “phase 0” arbitration. In the phase 0 arbitration, a challenger challenges a profile, submitting his evidence along with $20 in collateral. The challengee can review the evidence. If they think they’re likely to lose (for example, they submitted their proof of personhood in the wrong format, or are indeed a fraudulent account), they can opt to do nothing, lose their account, and forfeit their $20 in collateral.

If they believe they can win the challenge, they can put up a larger stake of $400, which is enough to justify a jury trial. The challenger then has to either match the $400 deposit and take the challenge to trial, or drop it and forfeit their $20 challenge deposit.

Note that this exchange only works if gas fees are fairly low, so this whole contract will likely live in a rollup. ![:upside_down_face:](https://ethereum-magicians.org/images/emoji/twitter/upside_down_face.png?v=15)

## Recovering a Lost FixedID

An important property of a FixedID is that it’s assigned to one person for life. So no matter what happens—a lost or stolen private key, or even the case where someone intentionally *sold* their FixedID or otherwise intentionally attacked the network—it should always be possible for a user to recover their FixedID. In this case, “recovering” a FixedID means assigning a new wallet to that FixedID within the FixedID smart contract. There are three ways to recover a FixedID:

1. Individual Recovery: a user can use the wallet currently associated with their FixedID to request that the FixedID be transferred to a new wallet. Once a request is initiated, the transfer happens after one week assuming it hasn’t been challenged. During the intervening week, the FixedID continues behaving as normal, it’s just associated with the previous account.
2. Social Recovery: A user can add “recovery users” to their FixedID to allow for social recovery. A majority of your recovery users can vote to associate your FixedID with a new wallet. When recovery users vote to recover your FixedID, a one-day waiting period begins. During the waiting period the account is locked and cannot be used for signing in or redeeming basic income. Adding or removing recovery users requires a 1-week delay before the change is live.
3. Recovery through Arbitration: Anyone can open an arbitration request to transfer a FixedID to themselves. This requires posting $400 in collateral in addition to the arbitration fee paid to jurors. It is the user’s responsibility to prove that they are the same person who created the FixedID account, potentially in an adversarial context if someone else is currently controlling the account and wants to maintain it. If the transfer request is ruled fraudulent, the existing account owner keeps the $400 collateral.

These three methods escalate, so a group of recovery users can overrule an individual recovery, and the ruling from an arbitration court can overrule a group of recovery users.

## Authenticating with FixedID

FixedID is designed to be an ideal authentication scheme, appropriate for replacing username/password auth, Google/Facebook/Github SSO and signing in with an Ethereum wallet directly. I’ve run large user communities before, and fraud, sockpuppeting, vote brigading, repeated trolling, and other varieties of sybil attacks are problems that every community faces. FixedID can help here, while still preserving user privacy! (Note, however, that for communities where ephemeral/throwaway accounts are an intended part of the UX FixedID login won’t be appropriate.)

When an app requests that a user sign in with FixedID, it provides the user with an app-specific string (such as the app’s URL). The user then returns an app token, which is a hash of the app-specific string concatenated with the user’s private key, eg `AppToken = Hash("{app_specific_string}.{private_key}")`. Additionally, the user provides a zero-knowledge proof that (1) the hash was correctly constructed, and (2) the private key corresponds to some public key in the set of all public keys currently associated with a FixedID (without revealing which one).

This allows the user to demonstrate that they have a valid FixedID account, and also allows they server to verify that they have **only one** account on the service, since the `AppToken` would match an existing account if they already had one. It also preserves the user’s privacy, since the app can’t map the hash `AppToken` back to a specific FixedID. And finally, it moves the burden of account recovery off of the app entirely and onto the FixedID infrastructure. These are significant benefits for an app builder!

Additionally, this can be extended with an [Ethmail](https://ethmail.cc/)-like (but less centralized) service so each app is given a single-purpose address that forwards to the user’s main email address.

*Note, however, that this scheme as written will break when a user recovers their FixedID to a new wallet. Further work is needed to handle that potentially difficult challenge.*

## Attestations

There are many types of attestations that are conceptually tied to an individual and should not be transferrable, even by selling my private keys. For example, a DAO may attest that I’m a member, a school may attest that I have a valid degree, or a country may attest that I have a valid residency permit. These types of attestations can be issued against a user’s FixedID, instead of against a specific address. That way they become both non-transferable and fully recoverable. Just as with possession of a FixedID itself, a user can generate a zero-knowledge proof that they possess a FixedID with a specific attestation, without revealing precisely who they are.

## Basic Income/Monetary Policy

All FixedID users will receive a basic income through a new token “Fixed Income” (FIN). There are three primary reasons to bake this into the protocol:

1. The issuance schedule described below will naturally reward early adopters heavily. This should drive initial adoption.
2. Controlling the issuance of FIN gives the protocol a way to punish users who try to subvert the protocol without actually removing their account (which we never want to do for legitimate people). FIN issuance can be locked or suspended for a time in response to eg. vouching for a fraudulent user.
3. It is my opinion that some amount of redistribution is fair, to partially counteract the vastly different circumstances individual humans are born into.

FIN will be issued at an initial rate of 100,000,000 tokens per year. This issuance rate will increase by 2.34% annually, leading to an overall long-term inflation rate of 2.28%. This inflation rate was chosen to (in the long term) double the total money supply every 30 years. The 30-year-doubling is somewhat arbitrary, but I chose it since that’s the approximate length of one generation and this way each new generation gets something of a fresh start.

The FIN token will be released with no “pre-mine.” The only way FIN is minted is through the standard issuance to FixedIDs.

Within each distribution period (tentatively once an hour), the total amount of FIN to be issued in that period will be calculated, and then distributed evenly among all active FixedID holders. This distribution scheme should incentivize early adopters to sign up, since **in the early days before the network becomes widely used the number of FIN tokens allotted to each user will be huge**.

The issuance dynamic is captured by the equations below:

[![Screen Shot 2021-08-24 at 6.15.32 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1ef13d7bf773b54f5ec4239c75136197328efeb7_2_690x210.png)Screen Shot 2021-08-24 at 6.15.32 PM1184×362 54.7 KB](https://ethereum-magicians.org/uploads/default/1ef13d7bf773b54f5ec4239c75136197328efeb7)

## Lots left to do!

As you can see, there’s a huge scope of work here. I’d love feedback on the protocol. And separately, if you’re interested in building a system that may one day be used to authenticate most of the planet, I’d love to hear from you! There’s plenty to do and I’m looking for someone to tackle this with me. ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=15)

## Replies

**imkharn** (2021-08-27):

This looks like a clear improvement to POH original design regarding bonds and challenging. There must always remain an incentive to challenge fake accounts. While one might expect that in a vacuum fake accounts are even more likely to be caught under the temporary large bond method than a permanent small bond, there exists friction that creates a risk of making it past the security checkpoint under the large bond. Also the security margin can be the same with a small bond as it is with a large bond when audited delegation is used to allow the courts to delegate the initial challenge to the public via a bond and audit. As long as the small bond is large enough to be worth the labor to investigate, it will be as secure as a large bond.

That said, its bad practice to ever choose a fixed number in mechanism design when that fixed number impacts incentives and security. The size of the bond in a well designed system will be dynamic and not pegged to the value of ETH or of dying currencies. The tradeoff here is between fake accounts making it into the system vs a bond that is prohibitively expensive. Thus a metric for setting the size of the bond and security expenses in general could be to target a specific percent of fake accounts making it through (such as 0.1%).

Also a partial source of your UBI here could come from yield on the deposit. You also might consider making your deposit the same token that is being inflated for purpose of UBI. Or a mixture of stable asset and the UBI token.

On a bigger picture, unique identity systems done objectively like this require an objective source of subjective truth. (because what defines a human is technically subjective…consider edge cases or try to define for an AI what a human is exactly that includes edge cases like someone whos heart just sopped for proof).

I am of the belief that the long term future of these systems is one where human-ness is not judged some court system that a majority of consensus security supports. Instead I think proof of humanity systems that are most successful are ones that see the original goal. The original goal here is to give each person confidence according to their own standards what accounts are a unique human. Its a fine stop gap to pretend there are universal standards of what is a unique human since it doesnt take much rounding or controversy. However, I believe the ultimate system to solve this problem in the long run will be subjective. In other words, do people I personally know and trust accept someone as unique? Its possible to get to anyone within 6 facebook friend hops, so such a subjective system would not fade off much in its ability to assign trust based confidence ratings to a large portion of the human population. Once the system is subjective, the worry about sibel attacks and challenges and courts goes away, and the system could even run without such mechanisms limiting them. Then when some future comes where a portion of the population is claiming their dead loved ones brought back to life as an AI are human enough, some people can choose to ignore this and others can accept it. A subjective identity system starts off with everyone in agreement with what the system says since they control the automated means of building their perspective of the data.  For the purpose of social systems, it would just require everyone to agree that everyone participating is a unique human. I do not see any value to having objective humanness truth here other than it being an easier system to make. All the same benefits exist and more with a subjective system.

---

**corbt** (2021-08-28):

Thanks imkharn, your thoughts are interesting!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/imkharn/48/3448_2.png) imkharn:

> Also the security margin can be the same with a small bond as it is with a large bond when audited delegation is used to allow the courts to delegate the initial challenge to the public via a bond and audit. As long as the small bond is large enough to be worth the labor to investigate, it will be as secure as a large bond.

Not sure I understand what you mean here – specifically, what is “audited delegation” in this context?

> The size of the bond in a well designed system will be dynamic and not pegged to the value of ETH or of dying currencies. The tradeoff here is between fake accounts making it into the system vs a bond that is prohibitively expensive. Thus a metric for setting the size of the bond and security expenses in general could be to target a specific percent of fake accounts making it through (such as 0.1%).

Yes, this will have to change dynamically. In fact, the target “percentage of undetected fake accounts” will probably be dynamic itself. Early on, when the FixedID system isn’t systematically important, a higher percentage of fake accounts is acceptable. Later on when the token becomes more valuable and more third-party apps rely on it for proof of personhood it’ll be necessary to increase the bond requirements and lock things down tighter.

> Also a partial source of your UBI here could come from yield on the deposit.

Interesting idea! I hadn’t thought about “yield farming” the deposits, but it may make sense to do that and use the proceeds to increase the FIN issued or buy and burn FIN to strengthen the currency.

> You also might consider making your deposit the same token that is being inflated for purpose of UBI.

Yes, I thought about this, and I think it’s a decent idea. One advantage is that it makes it easier to raise the collateral requirements over time if necessary, because we can simply withhold the basic income for a period of time and use the withheld income to increase each account’s collateral. But early on, since there won’t be any supply of FIN token, we need to use something that’s broadly available like ETH.

> I am of the belief that the long term future of these systems is one where human-ness is not judged some court system that a majority of consensus security supports.

I get where you’re coming from here, and there are edge cases even today (conjoined twins with various levels of independence?). But in general, I would resist going to a full-on subjective definition over those edge cases. Ultimately a shared definition of a “person” is a really useful moral/legal/societal abstraction. If the edge cases grow too large though because of AI/brain fusion or whatever then we’ll probably have to rethink this policy though.

---

**clesaege** (2021-08-29):

Proof of humanity inventor here ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> Every person gets a permanent integer ID. This is the key difference between FixedID and existing  implementations , and makes everything else possible. Instead of simply authenticating that a given wallet belongs to an individual, the system issues a static, immutable integer ID to each individual (their “FixedID”). The FixedID contract maintains a mapping of FixedIDs to wallets.
>
>
> FixedIDs are always recoverable. An individual can recover their FixedID and assign it to a new wallet using one of three flows: (1) by using their existing FixedID wallet to sign a request, (2) by selecting “recovery users” who can then vote to recover the wallet, or finally (3) through an arbitration process on Kleros or a similar platform. In all three cases, a waiting period is required before transferring ownership to allow for appeals.

This would be a good improvement.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> FixedIDs are ideal for authentication. A FixedID can be used to sign in to a web2 or web3 application. This sign-in uses a zero-knowledge proof to assure the app that the account belongs to a unique human, while not revealing which specific human it belongs to. In addition to eliminating sybil attacks, this removes the burden of account recovery from app creators.

There is a proof of concept of login with POH in the [forum](https://gov.proofofhumanity.id/). Having permanent ID would make this better.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> The collateral should be deposited permanently. That way challengers are incentivized to always be scanning the network, instead of only focusing on new submissions. The permanently locked collateral can also be much smaller (~20USD) and still achieve its intended effect.

Requiring collateral to be permanently locked would increase security, but the tradeoff is that it makes registration require more involvement (permanently lock funds instead of for a few days). In particular not permanently locking the deposit allows friends and organizations to pay the deposit of other people.

Requesting to renew registrations periodically have a similar effect along with removing deceased users.

Also keep in mind that layer 2 privacy solutions (ZKproof or ring signatures) cannot maintain the list in real time (there needs to be some registration period after which the private ID expire as it is not linked to the public one which can be removed).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> Initially, no vouchers should be required to minimize barriers to entry. Over time the voucher requirements can be raised. When voucher requirements are added they should be weighted according to graph connectedness, to prevent eg. 5 scam accounts all just vouching for each other.

I would advise against going without any voucher, as it would allows attacks “for free” (i.e. only paying money without risking to get one’s ID removed as it is the cased for people vouching for fraudulent submissions in POH).

However using the vouching graph as part of the review process would be a nice improvement.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> The initial signup and posting of collateral can be done with a credit card to make the onboarding much simpler for non-crypto users. (I’ll need legal advice on this, but a strong case can be made that since the collateral is never returned, you’re just paying for the service of creating/verifying your account instead of buying a token, so a brokerage license/KYC shouldn’t be required.)

Let’s not worry about that at the protocol layer, there are service providers allowing to do this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> Since $20 is too little to justify a jury trial, this requires adding an extra “phase 0” arbitration. In the phase 0 arbitration, a challenger challenges a profile, submitting his evidence along with $20 in collateral. The challengee can review the evidence. If they think they’re likely to lose (for example, they submitted their proof of personhood in the wrong format, or are indeed a fraudulent account), they can opt to do nothing, lose their account, and forfeit their $20 in collateral.

Yeah, it’s a good way to reduce deposit, but the tradeoff is complexifying the challenge process. It may be worth it though.

---

**corbt** (2021-08-30):

Great to hear from you [@clesaege](/u/clesaege) !

> Requesting to renew registrations periodically have a similar effect along with removing deceased users.

Yes, this is a very good point. Requiring users to post a bond on a regular basis (once a year or once every six months) may provide similar levels of security as a permanent bond, while providing much better capital efficiency. It also makes it easier to change the bond requirements (raise/lower them or change currency) over time since you don’t have to figure out what to do with the legacy bond. Requiring a specific on a regular basis may also naturally clean up records for deceased individuals as you say, although I suspect this won’t be an issue in practice since deaths are well documented nearly everywhere.

A couple of downsides though: (1) it does somewhat decrease the incentive to find fraud (relative to a fixed bond) since the challengers aren’t sure whether a given potentially-fraudulent account will post its bond again in the future, so it’s not clear whether it’s worth investigating it, and (2) for accounts that are likely fraudulent, there may be a race to be the first to issue a challenge as soon as they post their bond, which may lead to MEV/frontrunning-type dynamics.

> I would advise against going without any voucher, as it would allows attacks “for free”

I agree that vouches are critically important, and am only advocating removing them as an initial bootstrapping mechanism. For example, I was trying to sign up for ProofOfHumanity, but I realized I don’t know anyone who can vouch for me so I’m unable to sign up for now. ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

> (i.e. only paying money without risking to get one’s ID removed as it is the cased for people vouching for fraudulent submissions in POH).

It’s true that requiring vouchers gives the protocol more leverage against bad actors. I’m actually against removing accounts that provide bad vouches though—if FixedIDs become systemically important, it shouldn’t be possible to lose your FixedID, even if you behave badly. (Governments don’t rescind your national ID when you break the law.) But other penalties (withholding basic income for a time, removing the right to vouch) are reasonable.

> The initial signup and posting of collateral can be done with a credit card to make the onboarding much simpler for non-crypto users.

Let’s not worry about that at the protocol layer, there are service providers allowing to do this.

Are there service providers that let you pay with a credit card and transform that into crypto directly without going through a KYC/etc? That seems pretty risky with the potential for chargebacks/stolen cards (which is also a reason why allowing signup with a CC might be a bad idea in general, unfortunately).

---

**clesaege** (2021-08-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> I agree that vouches are critically important, and am only advocating removing them as an initial bootstrapping mechanism. For example, I was trying to sign up for ProofOfHumanity, but I realized I don’t know anyone who can vouch for me so I’m unable to sign up for now.

Well now you do ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12) (you can send me a link to your profile in PM).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> It’s true that requiring vouchers gives the protocol more leverage against bad actors. I’m actually against removing accounts that provide bad vouches though—if FixedIDs become systemically important, it shouldn’t be possible to lose your FixedID, even if you behave badly. (Governments don’t rescind your national ID when you break the law.) But other penalties (withholding basic income for a time, removing the right to vouch) are reasonable.

Well in POH, people removed can reapply again, so it’s not really like government taking your ID permanently but only putting you in a virtual jail for a week. This is also an opportunity for malicious profiles which made it to the list to be removed (and as we’ve seen what happens during attacks is that the attacker starts small and then get more profiles, thus more vouches scaling the attack).

So the important are:

- Removing temporarily the right to vouch.
- Asking to verify oneself again.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> Are there service providers that let you pay with a credit card and transform that into crypto directly without going through a KYC/etc? That seems pretty risky with the potential for chargebacks/stolen cards (which is also a reason why allowing signup with a CC might be a bad idea in general, unfortunately).

There are (for ex [Indacoin](https://indacoin.com)), but I don’t know any which would not have KYC.

---

**adamstallard** (2022-12-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/corbt/48/4493_2.png) corbt:

> Every person gets a permanent integer ID. This is the key difference between FixedID and existing  implementations , and makes everything else possible. Instead of simply authenticating that a given wallet belongs to an individual, the system issues a static, immutable integer ID to each individual (their “FixedID”). The FixedID contract maintains a mapping of FixedIDs to wallets.
>
>
> FixedIDs are always recoverable. An individual can recover their FixedID and assign it to a new wallet using one of three flows: (1) by using their existing FixedID wallet to sign a request, (2) by selecting “recovery users” who can then vote to recover the wallet, or finally (3) through an arbitration process on Kleros or a similar platform. In all three cases, a waiting period is required before transferring ownership to allow for appeals.

Immutable integers that are socially recoverable, privacy preserving, and mapped to eth accounts in a smart contract. So you basically want BrightID?

