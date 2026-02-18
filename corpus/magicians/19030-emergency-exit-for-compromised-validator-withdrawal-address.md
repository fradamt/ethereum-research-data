---
source: magicians
topic_id: 19030
title: Emergency exit for compromised validator withdrawal address - 2FA
author: noe
date: "2024-03-03"
category: Magicians > Process Improvement
tags: [erc-4337, withdrawals]
url: https://ethereum-magicians.org/t/emergency-exit-for-compromised-validator-withdrawal-address-2fa/19030
views: 1262
likes: 6
posts_count: 16
---

# Emergency exit for compromised validator withdrawal address - 2FA

Hi Magicians!

## Abstract

Implement an emergency mode for ETH validators with one function, to exit to the validators initial deposit address.

## Motivation

As of now, if a validators withdrawal address is compromised, one would loose access to both, the deposits and rewards of that specific validator. There is currently no alternative in such a case and all funds would be lost/locked.

With an ever growing number of solo validators affected by this, there should be a secure alternative for legit operators to mitigate a compromised or broken wallet.

The initial deposit address could be function as a backup, this would solve the mentioned issue for many solo validators and provide real 2FA (deposit address + validator keys) in an emergency situation.

In my opinion there has to be an option on consensus layer to make the protocol more attractive and secure, especially as a prerequisit and/or addition for future account abstraction models like ERC 4337.

## Security Considerations

Rightnow there are already some MEV smoothing pools accepting the ‘withdrawal’ and ‘deposit’ address as authentication, this seem to work fine. I’m open to discuss further security considerations, with the goal in mind to get this ready as a proposal one day.

## Links

few of many links in regards to the issue:

[Reddit - The heart of the internet](https://www.reddit.com/r/ethstaker/comments/12kodrr/compromised_withdrawal_address/)

https://decrypt.co/140317/ledger-crypto-wallet-under-fire-over-seed-phrase-recovery-service

## Replies

**yorickdowne** (2024-03-03):

The difficulty I see with this is that the deposit address, which has always been treated as not security critical, can now grab the ETH in the validator, if the deposit address is compromised.

And with 7002, a compromised withdrawal address can already drain a validator. This would happen fast enough that the operator cannot counteract with the deposit address.

This change would add a vulnerability vector, not resolve one.

---

**noe** (2024-03-03):

You’re right. At the point 7002 is live, this wouldn’t make too much sense anymore. On the other side, till then, there is this unique situation right now that some validator operators have still full control over the validator and in addition to the deposit address, which would “for now” be a source of trust and at least mitigate the mentioned issue of a lock out. From a perspective of a bad actor: Yes, some validator keys might be compromised as well or even shared on purpose, but actual wallets (including deposit wallets, with at least 32ETH on it at some point) shouldn’t be treated differently like any other sensitive wallet at any point in time. For now there are only very limit options to solve this, but without 7002 in place, I could still see this as an alternative, maybe combined with a social prove option qualified for when the validator is in “emergency mode”. The social prove thing already happend during Phase 1.5, if i recall correctly.

---

**maverickandy** (2024-03-03):

On an added note: there is a group of people (myself included) that have been staking pre-genesis AND have lost access to their mnemonic. There was no possibility to add a withdrawal address then so my creds are 0x00.

I have the power to exit my validator (but that would send all ETH straight into the matrix) but not the power to actually access my funds. Which seems very unfair for individuals that have been staking since day 1.

Can we not create a process for all validators that still have 0x00 to use the initial deposit address + the keystore JSONs + even the deposit JSON to prove ownership of a validator and setup a withdrawal address?

I fail to see how this could be an attack vector.

---

**stubbie** (2024-06-24):

I am the one with a validator that has a compromised withdrawal address as described in the reddit thread, and I was happy to just wait and see if something would change so that I could change the withdrawal address again, or perhaps have an option to return the funds to the deposit address. But now it looks like EIP 7002 will cause the 32 ETH stake to pretty much immediately be lost to me.

Perhaps they could implement a optional one-off 0x02 withdrawal address change?

---

**noe** (2024-12-29):

Hi,

As almost a year has passed and I haven’t seen any good alternatives to my proposal, I would like to elaborate on a few points.

A withdrawal to the deposit address could be a valid option, as an attacker would need to bypass two factors of security: 2FA (which is still considered the de facto standard in security), the validator’s credentials, and access to the deposit address.

In the meantime, the following initiatives —along with many others— do not only “trust” the deposit address but also accept it for authentication.

- MEV smoothly https://smoothly.money/
- Stakersunion https://www.stakersunion.com/
- Guardians of https://www.etherguardians.xyz/
- Stakecat https://www.stakecat.space/

I have had several discussions with other stakers who have been affected by a compromised withdrawal address. Given that there is no longer even a clear ownership of the withdrawal address (as with Eigenlayer), it is crucial that the community has a disaster recovery option for such a critical piece of software.

btw: EIP-7002 looks somewhat on hold, due to the mentioned security conserns of eliminating a 2nd factor, any news here ?

---

**noe** (2025-01-05):

From a high-level perspective, staking infrastructure should be treated as any other critical infrastructure, requiring resilience from both a business continuity and disaster recovery standpoint. We have already seen a significant number of stakers who may be locked out or at risk of being locked out, so mechanisms must be in place to prevent such situations. As long as ownership can be verified through two-factor authentication—such as using validator credentials and a deposit address—users should retain the ability to recover their funds and regain control of their validator.

On a side note, could [EIP-7251](https://eips.ethereum.org/EIPS/eip-7251) be an option to modify the withdrawal address if validator credentials are present ?

---

**aviadshimoni** (2025-04-15):

[@noe](/u/noe) I’m also affected by this scenario due to a friend’s PC being hacked.

Like you, I’ve access to the deposit address, the validator, and the withdrawal address.

I wish we could have the option to somehow change the withdrawal address.

currently I’m really thinking about exiting and running a script to fetch the funds, looking for any eth dev help

---

**noe** (2025-04-18):

[@magicians](/u/magicians). I’m in the tech industry for over 20 years working with critical infrastructure focusing on scaling and high availability.  It is a necessity that you have a disaster recovery and business continuity plan. I don’t see this in the current staking design, as all the value, leverage, money, stake however you want to call it, is dependent on one withdrawal address (wallet). Every good Authentication/Access Management solution has a fail-safe, usually when decentralized, it utilizes an alternate authentication method or recovery codes. Therefore, i fully agree that in our case, defining an additional address (maybe just for stake withdrawals) makes a lot of sense to mitigating the potential risk of losing everything.

Since staking is ideally a long-term commitment, the likelihood of a wallet becoming compromised over time is not negligible. An additional (backup) address could be added in the same manner as the 0x1 withdrawal address was configured previously, which would similarly require access to the validator credentials.

This approach should not introduce any additional security concerns. Perhaps [@yorickdowne](/u/yorickdowne) or someone else more closely involved with the actual implementation may have thoughts or comments on this.

---

**yorickdowne** (2025-04-18):

[@noe](/u/noe) You might be overthinking this. Rather than mandate certain forms of resilience in the protocol, users have the option of choosing what they want. A wallet with social recovery option. A multisig wallet - if it’s just for recovery then 1 of 2 would be fine.

By having no particular opinion about the withdrawal address, the protocol enables innovation by wallets - no one solution is preferred or kept out by the protocol.

---

**noe** (2025-04-18):

Just to be clear. I’m not trying to mandate anything here. I just want to highlight that in the first half of 2023, many stakers set their withdrawal address using tools that were still very much in development at the time.

I was partly involved in the Prysm “script,” and back then, the main focus was on getting the `bls2exec` change right. There wasn’t much attention yet on best practices when it came to wallet security (best practice).

EthStaker recommended using a hardware wallet, which was definitely solid advice. On Prysm’s website, the only real disclaimer was a simple line: *“Attention: You can only set your withdrawal address once.”*

I’d just like to see an open discussion at this point. One where we explore the options available for stakers who have already been affected by a compromised wallet, and how we can use those insights and potential mitigation to prevent harm for future stakers.

Up to now, the general response has seemed to shift from “we’re too busy to think about it” to “we don’t care anymore,” which is disheartening.

I also want to encourage everyone who have reached out to me, whether on Discord or via PMs here on the forum—to share their experiences in this thread, so becomes more clear that this issue affects more than just a handful of stakers.

---

**sentin** (2025-04-19):

+1

Affected by a compromised wallet (Ledger data breach + very targeted attack) as well. Please, as the funds are still in the validators, please find a way to support such a recovery scenario. The funds needed for running a validator are in the realm of “live changing” therefore we need that option. Unfortunately most of my validators having the same compromised withdrawal address, so if there will be a way in the future, i’m willing to donate a good portion of my stake for the development.

Thanks for the support

---

**TZE** (2025-04-21):

+1

affected as well. Thanks for the support!

---

**Michael2Crypt** (2025-05-14):

+1

this is a very wise and useful proposal

---

**Trying2Cook** (2025-09-26):

I too have the problem of compromised wallet. My deposit and withdrawal address are the same.

EIP-7002 allowed the attacker to request an exit request. 30 seconds after I realized how I had been compromised, then there was already 4 transaction requests made to trigger the exit.

Now I’m stuck just watching and waiting for the race to begin to see who ends up with my 32 ETH.

I would propose that if the Validator is 0x01, you must use your nemonic phrase & withdrawal address to send signed message to update the deposit address to a “safe address”. Then this could work, but because of EIP-7002, then you would need to allow this for validators that are exiting.

Long term there needs to be a strategy for how to create a secure exit strategy for validators connected to a compromised wallet and how to protect validators against loss if their withdrawal address gets compromised.  These better protections could be added over the course of time vs introducing them all at once.

EIP-7002: Trigger exit with withdrawal address only

EIP-7804: Update withdrawal address using withdrawal address?

Emergency dump funds using withdrawal address only.

Yes, people should be more careful, but today we are talking about a minimum of 32 ETH to max 2048 ETH. At $4,000  that’s $128,000 to $8,192,000 all secured by 1 key.

As the value of ETH increases, then that value increases too.

Validators need better protocols for protection.

Attackers already know how to sweep wallets and they know how to instantly trigger exits.

They will learn how to do any of these “fixes” that are all controlled by withdrawal address.

---

**maverickandy** (2025-11-24):

I’ve built a dashboard to track progress of deprecating the BLS withdrawal credentials.

Also developed a proposed mechanism for validators that are unable to migrate (e.g. due to loss of private key/ mnemonic). I will lobby for support to include these proofs into the hardfork to quantum-proof signatures.

All information can be found here: [deprecatebls.com](http://deprecatebls.com/)

