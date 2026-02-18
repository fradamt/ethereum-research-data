---
source: magicians
topic_id: 5429
title: "EIP-42 : Proposition of the T-REX token standard for securities"
author: Joachim-Lebrun
date: "2021-02-26"
category: EIPs
tags: [erc-20]
url: https://ethereum-magicians.org/t/eip-42-proposition-of-the-t-rex-token-standard-for-securities/5429
views: 1532
likes: 4
posts_count: 9
---

# EIP-42 : Proposition of the T-REX token standard for securities

Hello,

We would like to propose the T-REX token standard, which is currently used by Tokeny Solutions, as ERC-42. This standard is used to tokenize securities and is based on ERC-20, on top of which we added 2 permission layers :

- the first permission layer being linked to the identity of the transaction’s receiver and its eligibility following preset rules defined by the token issuer (using ERC 734/735 for the identities and checking if the required claims are present on the identity and are signed by the trusted claim issuers)
- the second permission layer being based on global restictions applied to the token as such, e.g. maximum amount of token volume per day, maximum amount of token holders, …

You can find the complete description of the EIP-42 here [GitHub - TokenySolutions/EIP42: proposition of the eip42 standard for security tokens](https://github.com/TokenySolutions/EIP42)

Thanks in advance for your consideration and your feedbacks ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

## Replies

**Joachim-Lebrun** (2021-03-15):

it would be great to have the feedback of some members of the community on this, it would be greatly appreciated ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**matt** (2021-03-15):

EIP-42 isn’t a valid EIP number.

---

**Joachim-Lebrun** (2021-03-15):

why not? can you give me a link stating about the rules to chose a valid EIP number in this case?

---

**matt** (2021-03-15):

Please see this section of EIP-1: [EIPs/EIPS/eip-1.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md#eip-header-preamble)

> EIP number (this is determined by the EIP editor)

An editor must assign the EIP number to you, it is not correct to select a number.

---

**Joachim-Lebrun** (2021-03-16):

Ok thank you, i was not aware of that. I will leave it like that for the moment but mention that the final number needs to be determined by an EIP editor (i put a note on the github to mention the fact that we are using the EIP n° 42 until we have a final number… for the topic on the forum, i cannot edit the title anymore, but the important point is more about the content than the number)

If you have any comment on the content of the proposition i would be happy to discuss about it ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**Joachim-Lebrun** (2021-04-26):

How can i proceed to get an EIP editor looking at this? It’s been pending for weeks now…

---

**matt** (2021-04-26):

What is your PR number?

---

**Joachim-Lebrun** (2021-08-12):

topic replaced by [EIP-3643 : Proposition of the T-REX token standard for securities](https://ethereum-magicians.org/t/eip-3643-proposition-of-the-t-rex-token-standard-for-securities/6844)

