---
source: magicians
topic_id: 17538
title: "ERC: Short Representation for Leading Zeros in Address"
author: xinbenlv
date: "2023-12-20"
category: ERCs
tags: [erc, wallet]
url: https://ethereum-magicians.org/t/erc-short-representation-for-leading-zeros-in-address/17538
views: 1454
likes: 12
posts_count: 11
---

# ERC: Short Representation for Leading Zeros in Address

Hi, as I presented in previous AllWalletDevs about a proposal to represent leading zeros in address which reduces chance of phishing, I am thinking of starting an ERC.

## Motivation

- reduce phishing

## Specification

The format will be `0{N}xAA..BBBB`, where

- N is the number of leading zeros in decimal form
- AA is the two hex digits of two digits since first non-zero hex digit
- BBBB is the last four hex digits

## Rationale

- We choose 0{N}x format so it can be easily differentiate from 0x
- We choose 2 digits before and 4 digits after in the non-zero part, instead of 4,4 for length restriction, but up for discussion
- We choose to turn into upper case ditching ERC-55 or ERC-1191 because those case switching no longer serves the purpose of checksum.
- We shall anticipate the short-form will need to be compatible with assumptions made in CAIPs

## Reference Implementation

```js
// Javascript
function convertHexString(hexString) {
    // Ensure the input is a string
    if (typeof hexString !== 'string') {
        throw new Error('Input must be a string.');
    }

    // Regex to match leading zeros
    const leadingZeros = hexString.match(/^0x0+/);
    if (!leadingZeros) {
        return hexString.toUpperCase(); // Return original in uppercase if no leading zeros
    }

    const zeroCount = leadingZeros[0].length - 2; // Subtract 2 for '0x'
    const remainingString = hexString.slice(zeroCount + 2).toUpperCase(); // +2 for '0x', then convert to uppercase
    const truncated = remainingString.substring(0, 2) + '...' + remainingString.slice(-4);

    return `0{${zeroCount}}x${truncated}`;
}

// Example usage
const result = convertHexString('0x00000000219ab540356cbb839cbe05303d7705fa');
console.log(result); // Outputs: 0{8}x21...05FA
```

## Test

| original | short | note |
| --- | --- | --- |
| 0x00000000219ab540356cbb839cbe05303d7705fa | 0{8}x21...05FA | ETH 2.0 deposit |
| 0x000000000022d473030f116ddee9f6b43ac78ba3 | 0{10}x22...8BA3 | Uniswap Permit2 |
| 0x0000000000A39bb272e79075ade125fd351887Ac | 0{10}xA3...87AC | Blur |
| 0x00000000000000adc04c56bf30ac9d3c0aaf14dc | 0{14}xAD...14DC | OpenSea Seaport 1.4 |

## Soliciting Reviewers

We kindly invite the following reviewers for feedback

- ERC-55: @vbuterin Vitalik Buterin , @alexvandesande , Alex Van de Sande
- ERC-1191 authors: Juliano Rizzo (@juli)
- CAIPs: @ligi, @bumblefudge
- ethers.js @ricmoo
- HomeWork / OpenSea: @0age
- MetaMask: @frangio

And anyone whose work and interest involves short form address representation.

## Replies

**wjmelements** (2023-12-20):

The `0x` prefix signals that the constant literal immediate is hexadecimal. This prefix should not be split up.

The syntax you suggest is similar to the regular expression syntax but it is not a valid regular expression.

For both of these reasons your suggested format is an abomination.

Hiding the middle digits also increases the ease of phishing, though this is your supposed motivation.

I’d be more interested in a solution like Bitcoin’s base58 which would increase the number of bits encoded per character while remaining alphanumeric.

---

**wjmelements** (2023-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> I’d be more interested in a solution like Bitcoin’s base58 which would increase the number of bits encoded per character while remaining alphanumeric.

Unicode emoji are good candidates for compressed addresses since they are easy to recognize. There are almost 4000 of them so far.

---

**bumblefudge** (2023-12-21):

If you like Base58-style encoding gymnastics, you are gonna LOVE the multibase project over in IPFS land:

https://github.com/multiformats/multibase/pull/88

---

**bumblefudge** (2023-12-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> For both of these reasons your suggested format is an abomination.

I’m not sure I’d go as far as `abomination` but I agree that this scheme risks being confused for or mistaken for schemes it rhymes with but breaks.  What about something like

`0x0*8x21...05FA` or `0x8x21...05FA`?

Another wierd nit while we’re in pre-draft spitballing phase-- don’t those `00` always come in pairs? Wouldn’t it be `0x4x21...` since there are 4 bits of `00` rather than 8 characters of `0`?

---

**xinbenlv** (2023-12-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bumblefudge/48/7449_2.png) bumblefudge:

> I’m not sure I’d go as far as abomination but I agree that this scheme risks being confused for or mistaken for schemes it rhymes with but breaks. What about something like
> 0x0*8x21...05FA or 0x8x21...05FA?

You mean compare to

0{8}x21…05FA, use `0x0*8x21...05FA` or `0x8x21...05FA`

I think that’s doable!

The pros is that they are less like RegEx. Though the cons is they might look more like a math formular.

I am totally open to all suggestions regarding the best format. Having your opinion helps we gauge possible response from broader user base.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bumblefudge/48/7449_2.png) bumblefudge:

> Another wierd nit while we’re in pre-draft spitballing phase-- why don’t those 00 always come in pairs? Wouldn’t it be 0x4x21... since there are 4 bits that are 00 rather than 8 that are 0?

I think it’s possible there are odd number of zeros and it’s easier for general (non-tech) user to understand “this is the first non-zero digit” as opposed on zero always come in pair because its a “byte”

---

**bumblefudge** (2023-12-22):

but the first byte of 000005 isn’t 5 it’s 05-- i take your point, tho, 0x2x05 might be confusing to a normie

---

**xinbenlv** (2023-12-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> The 0x prefix signals that the constant literal immediate is hexadecimal. This prefix should not be split up.

Yes. That’s a rationale that deserves consideration. In that case it could be something like

`{9}0x1234`, but it may confuse user to think 0x1234 is the beginning of full 20bytes wallet address. I am still debating whether it’s better or less ideal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> The syntax you suggest is similar to the regular expression syntax but it is not a valid regular expression.

It’s possible for someone like you and I who are developers to be confused it with RegEx.

If our target is end user who are general and non-tech savvy, RegEx is not a widely known thing outside of developers. I won’t worry too much about it being confused with RegEx.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Hiding the middle digits also increases the ease of phishing, though this is your supposed motivation.
>
>
> I’d be more interested in a solution like Bitcoin’s base58 which would increase the number of bits encoded per character while remaining alphanumeric.

That’s possible, except for that it could create a bigger barrier to existing EVM wallet users, it’s too much a change and a much higher learning curve. Also could mistaken user from recognizing them and compare it with the hex string

---

**xinbenlv** (2023-12-28):

I encountered this scam attempt today

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/a/aa809f42af81150b45249a893a2e7971bd51a1dc_2_690x350.png)image3456×1754 718 KB](https://ethereum-magicians.org/uploads/default/aa809f42af81150b45249a893a2e7971bd51a1dc)

---

**wjmelements** (2023-12-28):

Can that wallet’s “Address book” feature help with distinguishing these addresses?

---

**wjmelements** (2024-04-01):

I have created an ERC for this solution.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png)
    [ERC: Distinguishable Account Addresses](https://ethereum-magicians.org/t/erc-distinguishable-account-addresses/19461) [EIPs](/c/eips/5)



> Addressing several recurring topics in this forum, this will improve the resiliency of account addresses against spoofing attacks.

