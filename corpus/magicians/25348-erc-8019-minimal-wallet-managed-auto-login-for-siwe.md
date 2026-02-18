---
source: magicians
topic_id: 25348
title: "ERC-8019: Minimal Wallet-Managed Auto-Login for SIWE"
author: Ivshti
date: "2025-09-04"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8019-minimal-wallet-managed-auto-login-for-siwe/25348
views: 545
likes: 31
posts_count: 13
---

# ERC-8019: Minimal Wallet-Managed Auto-Login for SIWE

Users repeatedly sign identical SIWE messages for trusted apps. A small, explicit match policy enables zero-prompt login without involving apps.

Users already get prompted by their wallets if they trust a certain app when they initially connect to it - this flow can also authorize auto-login if applicable.

This ERC defines a wallet-local allowlist for automatic signing of EIP-4361 messages when simple, deterministic match rules succeed. Policies are created and managed only by the wallet/user, but we include reasonable defaults.

The end goal is to ensure that dapps like Fileverse and Lens don’t bother you to re-sign the same message on a regular basis.

More here: [ERCs/ERCS/erc-8019.md at aa5a30ab9b23c317c8a3206b70ee4ff7fbe8dc33 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/blob/aa5a30ab9b23c317c8a3206b70ee4ff7fbe8dc33/ERCS/erc-8019.md)

## Replies

**kdenhartog** (2025-09-07):

How do you plan to address the privacy issue where the wallet address gets used as a cross-origin identifier to track users? This would allow a site or RPC service to automatically track the user based on their wallet address across sites they visit.

---

**Ivshti** (2025-09-08):

In two ways addressed in the ERC itself:

1. the wallet should not apply the policy before a single user signature
2. the policies are only applied for the specific origin they were approved for

If a website/dapp/origin has already done this once for you and you’ve allowed it, you can argue that you’ve allowed this dapp to know your address.

---

**kdenhartog** (2025-09-10):

Oh very nice, I didn’t catch that when reading through it.

Might I suggest adding in a permissions policy similar to what browsers do within the wallet.

E.g. Save for 24 hours, 7 days, forever type thing

---

**Ivshti** (2025-09-17):

so, maybe something that “A wallet MAY ask the user how long they want to keep the policy for”?

---

**kdenhartog** (2025-09-17):

I’d advocate for a SHOULD over MAY, but don’t think a MUST is necessary.

---

**Ankita.eth** (2025-11-05):

Really like how ERC-8019 balances UX and security by letting wallets manage deterministic auto-login policies instead of pushing complexity to dapps.

A few questions:

- How will wallets standardize the policy UI/UX so users clearly understand which apps are whitelisted?
- Could deterministic matching be extended for session-bound variations (like short-lived nonces)?

Great to see Ambire already implementing this concept in action — their post gives a nice real-world perspective on how ERC-8019 improves SIWE usability:

![:link:](https://ethereum-magicians.org/images/emoji/twitter/link.png?v=12) https://x.com/ambire/status/1985678098893869159

---

**Ivshti** (2025-11-05):

Hey,

I think standardizing policy UI is out of scope for this EIP, but a good recommendation would be to have a settings page showing all the currently active policies. Still, I think the EIP itself shouldn’t go into specifics.

I’m not sure I understand the short-lived nonces question, if you mean short sessions - I don’t see the use case, as a dApp shouldn’t be spamming the wallet with SIWE requests within one session. If we are talking about something more than SIWE, then I think permissions/delegations are a much better standard.

---

**ryanshahine** (2025-11-05):

signing in on apps can and should be improved, but we have to stay aligned with/consider (web) security standards. most apps that use siwe pair it with sessions, where the backend issues a cookie signed with its secret. that secret lets the backend verify/ensure the user’s session can’t be forged. if a session is invalid or expires, the user is forced to re-authenticate.

by letting wallets auto-sign for trusted domains, authentication no longer depends on session validation. the wallet can generate new siwe signatures anytime, so the backend’s session secret becomes optional. have you considered the trust/security implications of this?

---

**Ivshti** (2025-11-05):

Can you please clarify what you mean by “session validation”?

Of course the security implications have been considered, and this ERC is just an easier way to allow users choose how long their actual sessions they want to be.

---

**ryanshahine** (2025-11-05):

> Can you please clarify what you mean by “session validation”?

many apps enforce short sessions, sometimes for regulatory reasons. if a wallet silently renews siwe sessions, i argue that silent auto-login undermines app intent.

for that reason, i’d would argue that auto-sign MUST be disabled by default.

if an app uses long-lived sessions, i.e.: siwe session expiration == erc-8019’s defaultExpiration, the user action required will be the same as the user will be prompted to sign-in.

---

**Ivshti** (2025-11-06):

That’s why it’s recommended for the implementer wallet to maintain a per-app policy list, adding only apps that would benefit from this.

This ERC comes from a specific real-world example, Fileverse, which needs a separate SIWE message but definitely doesn’t need user approval for each one.

---

**vijaykrishnavanshi** (2025-11-12):

Hello [@ryanshahine](/u/ryanshahine),

Adding some pointers on top of what Ivo has shared.

Use case: auto-logins for Apps that are constrained security or reg wise and don’t want to see that new login behaviours.

Clarifications: the ERC will not impose new login behaviour on apps and will propose auto-logins to be OFF by default. Also, this should not stop wallets from maintaining a preferential list of apps that want to facilitate the auto-login for their users. dDocs and dSheets for example are non-financial apps and this is a fantastic UX improvement, no issues on that front.

Next: We will make it more explicit in the core part of the ERC to address the above. Thank you for this, yanshahine!

