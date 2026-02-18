---
source: magicians
topic_id: 596
title: Overview of the W3C Payment Handler API for the Web
author: jpitts
date: "2018-06-26"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/overview-of-the-w3c-payment-handler-api-for-the-web/596
views: 1165
likes: 2
posts_count: 1
---

# Overview of the W3C Payment Handler API for the Web

Below is a link-fest relevant to Ethereum UX. Also, this effort is a good example of standards work in action:

https://medium.com/coil/standardizing-payments-with-the-payment-handler-api-1bb8cefa702d

---

Here is the implementation overview for Chrome:


      ![image](https://www.gstatic.com/devrel-devsite/prod/v63a7e59e7b93b62eb99aa3751cce206090432f0c0d09ff73f0d3636dcec4ab60/web/images/favicon.png)

      [web.dev](https://web.dev/articles/web-based-payment-apps-overview)





###



Learn how to adapt your web-based payment app to work with Web Payments and provide a better user experience for customers.










---

This is a discussion on “Mozilla standards positions” regarding cryptocurrency support with Payment Request API. Provides some insight into how other dev communities regard cryptocurrencies.



      [github.com/mozilla/standards-positions](https://github.com/mozilla/standards-positions/issues/78)












####



        opened 05:13AM - 26 Mar 18 UTC



          closed 10:28AM - 03 Apr 18 UTC



        [![](https://avatars.githubusercontent.com/u/870154?v=4)
          marcoscaceres](https://github.com/marcoscaceres)










## Request for Mozilla Position on an Emerging Web Specification

* Specificat[…]()ion Title: Payment Request
* Specification or proposal URL: https://github.com/w3c/payment-request/pull/694

### Other information
The Payment Request API currently only checks that monetary values passed into it adhere to the ISO4217 currency format: ASCII 3-alpha (e.g., "USD", "EUR", etc.). However, the spec doesn't ask the browser to check if those are "real" (fiat) currencies - which would be possible by checking against ISO4217 itself (maintained and updated by ISO).

There is a proverbial elephant in the room around cryptocurrencies, such as "BTC", which, although they conform to the ISO4217 "currency format", may or may not be "real" currencies.

Recently, [Facebook](http://www.bbc.com/news/technology-42881892), [Google](https://www.cnbc.com/2018/03/13/google-bans-crypto-ads.html), and soon [possibly Twitter](https://www.theverge.com/2018/3/18/17136556/twitter-cryptocurrency-ads-bitcoin-ban-report), have banned advertising crypto currencies in their platform due to high levels of fraud.

When using the Payment Request API, I personally fear that by not checking if a currency is registered with ISO (as a "real" currency), we might subject Firefox users to fraud. For instance, a website might insist that you can only buy things with a particular crypto currency (or [similar scams already seen](https://www.theverge.com/2018/3/8/17096128/twitter-vitalik-buterin-elon-musk-cryptocurrency-scams)).

What I'd like to propose is that, at a minimum, all currencies (including cryptocurrencies) be first blessed by ISO before they can be used with the Payment Request API. Coincidently, [ISO is exploring](https://en.wikipedia.org/wiki/ISO_4217#Cryptocurrencies) the possibility of formally registering cryptocurrencies. This would be a minimum level of due diligence that would be required to use a currency.

Opinions? Is this something we (Mozilla) should push for in the spec (e.g., "if it's not in ISO4227, throw a RangeError." )? Or maybe just an assurance we implement into Firefox?

Opinions would be appreciated.
