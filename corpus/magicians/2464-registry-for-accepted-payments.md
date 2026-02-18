---
source: magicians
topic_id: 2464
title: Registry for accepted payments
author: ligi
date: "2019-01-17"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/registry-for-accepted-payments/2464
views: 1473
likes: 4
posts_count: 6
---

# Registry for accepted payments

I was running this idea with some of you already - but always offline - so moving this online to refine a bit further in direction of an potential EIP

What do you think of a registry where wallets can register which payment forms they accept? I think user experience could really improve here.  As e.g. in a payment situation where the user is presented with a ERC-681 QR code we could signal to the user e.g. that a raiden payment would be accepted.

I imagine these functions,

```
registerPaymentType(id,string)

setSupportedPaymentType(id)
removeSupportedPaymentType(id)

getPaymentTypesForAddress(address)
```

still a bit unsure about the string in the register. Would be neat to be able to list services. But not sure if it belongs there and sure it will get into a localisation mess later on. Perhaps just register and do the metadata for id’s off chain. They could be signed with the key that was used for registering the type.

## Replies

**ligi** (2019-02-09):

One thing that could also be interesting - some vendors might want to accept e.g. DAI and xDAI. Here it gets a bit more complicated as it is not only the transport - but also the token. I think for this use-case we need to modify the interface.

---

**ligi** (2019-02-10):

Just to visualize it a bit:

[![device-2019-02-10-201943](https://ethereum-magicians.org/uploads/default/optimized/2X/f/fb255da794eb0562df14986b74c7070215efbfa4_2_690x446.png)device-2019-02-10-2019431622×1050 227 KB](https://ethereum-magicians.org/uploads/default/fb255da794eb0562df14986b74c7070215efbfa4)

offering more payment options we would need more checkboxes - the UX would be horrible.

Perhaps instead of a registry - the QR code shows an IPFS or swarm hash and the content contains an json with the invoice. Then we would also get the message field that the burner wallet has. In this json there would then also be the accepted payment methods. DAI/xDAI/DAI over raiden/PlasmaSystemXY/..

[symbolic image](https://twitter.com/__BrettWilson__/status/1094412708374433793)

---

**Alexintosh** (2019-02-11):

I totally agree with this proposal. I also feel we need to have a standard way to present which payments method are accepted for a specific request. Inside Dexpay (dai/xdai pos) we are currently listening both the xDAI network and mainnet when we are waiting for a payment in DAI to allow more flexibility from the user side, this should be formalized somehow to avoid confusion.

---

**skywinder** (2019-02-11):

Hey, ligi! That’s a great idea! Looks Inspiring! In continue of our talk: I’ll back to you with Ignis API implementation as soon as we will bake it for beta testing!

fyi: demo is here: https://ignis.thematter.io

And we start to do an alpha test our Ignis Plasma protocol: for now iOS only.

Our app here:


      ![image](https://testflight.apple.com/favicon.ico)

      [testflight.apple.com](https://testflight.apple.com/join/FVWgauFQ)



    ![image](https://testflight.apple.com/images/testflight-1200_27.jpg)

###



Using TestFlight is a great way to help developers test beta versions of their apps.










GitHub:

https://github.com/matterinc/FranklinPay-iOS

We are going to implement DAI support in the next versions.

---

**pedrouid** (2019-02-20):

Agreed, we tried to hack on a PoS system at ETH Denver and this was by far our biggest challenge. The lack of adoption of standards from Wallets right now is really bad. Another thing to note is how most wallets don’t emphasize QR Code scanning, this feature is usually hidden under a single asset or send transaction screen.

At the end of the hackathon we solved it by using WalletConnect which reduce the number of compatible wallets but still better adoption than ERC-681. Using Metamask or WalletConnect provides a good solution for registering accept payments but it looses the provability of these payments as the merchant is in control of this payment confirmation. Ideally users are able to verify this on-chain and by matching their payments with the an on-chain invoice.

