---
source: magicians
topic_id: 16066
title: Trustless userop signing via browser?
author: mac
date: "2023-10-12"
category: Web > User Experience
tags: [account-abstraction, eip-4337, standards-adoption]
url: https://ethereum-magicians.org/t/trustless-userop-signing-via-browser/16066
views: 569
likes: 1
posts_count: 1
---

# Trustless userop signing via browser?

The setup:

Web developer Bob wants to build a web game using web standards, and Bob doesn’t want to require users to install browser extensions. Bob decides to use eip4337 to create accounts for all his players.

The Question:

How should Bob’s web app display a userop to be signed by a user (the sender: Alice) – without using a browser extension or window.ethereum, such that Alice can know Bobs web app isn’t doing a bait and switch?

And to make the convo realistic – let’s assume Alice doesn’t want to give Bobs web app access to the her ecdsa priv key

As an example:

WebAuthN based wallets wanting to get users to sign will send the userop struct as the Challenge in a webauthn.credentials.get() call. When the browser mediated modal pops to sign, it doesn’t show what you are signing – so how does the user trust this?

[![1000019748](https://ethereum-magicians.org/uploads/default/optimized/2X/a/af912f78e8919c6da16ffcb500121fbd6a03ad30_2_690x317.jpeg)10000197481516×698 125 KB](https://ethereum-magicians.org/uploads/default/af912f78e8919c6da16ffcb500121fbd6a03ad30)
