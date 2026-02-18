---
source: magicians
topic_id: 21704
title: Ethereum Colored Address Protocol
author: AdamLeeeee
date: "2024-11-15"
category: ERCs
tags: [erc, wallet, ui]
url: https://ethereum-magicians.org/t/ethereum-colored-address-protocol/21704
views: 432
likes: 6
posts_count: 8
---

# Ethereum Colored Address Protocol

### update change

sha256 → keccak256

---

## Abstract

This proposal introduces an ERC for a wallet address coloring protocol that assigns a unique color to each Ethereum wallet address. The color is generated using the hash of the wallet address and is designed to help users easily verify addresses visually, reducing errors and preventing phishing attacks.

## Motivation

Ethereum addresses are long and complex, making them hard to recognize at a glance. This can lead to mistakes when copying or inputting addresses and exposes users to phishing scams where attackers use similar-looking addresses. By adding a distinct color identifier to each address, users gain an easy way to visually confirm the accuracy of the address they are interacting with

## How It Works

1. Unique Color Generation: The protocol hashes the wallet address (e.g., with keccak256), extracts specific bits, and maps them to RGB values to create a unique color.
2. Noticeable Differences: Even a one-character change in an address results in a visibly different color, making discrepancies easier to spot.
3. Easy Integration: This system is compatible with existing wallet and blockchain explorer interfaces, so it can be implemented without major changes.
4. Security Measures: The color generation process is designed to be complex enough to prevent attackers from creating false color matches or spoofing addresses.

## Algorithm

[![color-overflow](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9ad2496d0d60ec7cab667cd11e00ac437b79c6c1_2_690x304.png)color-overflow1948×860 222 KB](https://ethereum-magicians.org/uploads/default/9ad2496d0d60ec7cab667cd11e00ac437b79c6c1)

```auto
import { keccak256 } from "js-sha3";

export const calculateColors = (address: string): string[] => {
    const hash = keccak256(address);
    const firstThirtyHexChars = hash.slice(0, 30);
    const colors = [];

    for (let i = 0; i < 10; i++) {
        const segment = firstThirtyHexChars.slice(i * 3, i * 3 + 3);
        const r = parseInt(segment[0], 16) * 10 + 50;
        const g = parseInt(segment[1], 16) * 10 + 50;
        const b = parseInt(segment[2], 16) * 10 + 50;
        colors.push(`rgb(${r}, ${g}, ${b})`);
    }

    return colors;
};
```

## Use Cases

- Wallet Applications: Displaying a unique color next to addresses helps users confirm that the address they are sending to or interacting with is correct.
- Blockchain Explorers: Enhanced address verification with visual color markers, enabling users to quickly identify if an address matches known, trusted addresses.
- Browser Extensions: Plugins that add color markers to addresses on webpages can alert users if an address differs from the expected color.
- Smart Contract Interfaces: Tools interacting with contracts can display colored addresses to assist users in verifying recipient and sender details.

## Benefits

- Visual Verification: Users can quickly identify if an address matches by checking its color.
- Reduced Errors: Enhances confidence during address input and transaction verification.
- Phishing Protection: Makes it harder for attackers to mimic legitimate addresses.

## Conclusion

The wallet address coloring protocol is a simple yet effective way to add an extra layer of security and ease of use to Ethereum address handling. It helps users recognize addresses more confidently, reduces mistakes, and protects against scams.

## Q & A

### 1. What is the user experience for colorblind users?

We plan to introduce brightness as an additional distinguishing factor in the future. This will help colorblind users differentiate between addresses, even if they can’t perceive the color differences clearly.

### 2. Why color only the first and last five characters (excluding “0x”) of the wallet address?

Wallet components often abbreviate the middle part of the address, displaying only the first five and last five characters. By coloring these portions, the address remains distinguishable even in shortened form.

### 3. How does the protocol ensure the security of the address coloring algorithm?

The ERC employs a high-complexity algorithm that offers 16 color possibilities for each character. This makes generating a similar address with identical colored characters 16 ** 10 times more difficult than generating addresses with only matching characters.

### 4. How does the protocol ensure the clarity of the colored characters?

The coloring algorithm ensures that character colors fall within a range of 50 to 200, avoiding extremely dark or light colors. This range ensures the colors stand out clearly against common background colors like black and white.

### 5. Why use color to display differences in addresses?

Color is a built-in property of fonts, making it easier for users to visually distinguish differences. Additionally, the protocol improves wallet address security while simplifying development, avoiding the need for layout changes (e.g., adding special symbols) in the UI.

## Learn more in website

https://eth-colored-address.dnevend.site/

Needs discussion!

## Replies

**0xTraub** (2024-11-16):

Fun idea. Definitely interesting. I’ve noticed that characters in the example near each-other alphabetically or numerically can be quite similar, ex: 6, 8, and 9. Is this not a concern as they may appear visually similar in terms of both color and shape that could be weaponized by an attacker using brute force address generation? I can see how 6s and 9s and others may be misinterpreted or can this be considered statistically unlikely, and if so is there a way to ensure that this becomes less frequent?

---

**Dahka2321** (2024-11-17):

How does the wallet address coloring protocol handle potential conflicts where two different addresses might generate similar or indistinguishable colors, and what measures are in place to ensure that the color differences are always noticeable to users?

---

**AdamLeeeee** (2024-11-17):

Thanks for joining the discussion!

You are discussing possible misunderstandings when numbers or letters are similar. Obviously this is different from the topic of “color” we are discussing.

But let’s talk about it. In my opinion, it is indeed possible to achieve confusion through the shape of the characters. If you want to reduce the occurrence of this situation, you can have the following options:

1. Using this ERC, colored addresses can significantly distinguish different wallet addresses.
2. Additional font backgrounds are added to characters that may cause confusion to remind users to check carefully. The disadvantage is that the background color will appear more abrupt.
3. Adding additional marks such as underlines to characters that may cause confusion will also appear more abrupt.

The above is my idea. You are welcome to come and participate in our discussion!

---

**AdamLeeeee** (2024-11-17):

Thanks for joining the discussion!

When users verify wallet addresses, they usually check the first and last digits, so even if the colors are the same, users will check whether the first and last characters are consistent. In other words, the same color of the ERC does not mean that the wallet address is the same. The color is just a way to help users distinguish different addresses.

As mentioned in the article, after using the ERC address display, it will be approximately 1 trillion (16 ** 10) times more difficult to generate the same address and the same color with the first and last five digits than before.

Regarding the color difference, the possible RGB values ​​of each character differ by 10, such as 50, 60, 70… This difference will make the color difference more obvious.

The above are my thoughts, you are welcome to come again to participate in our discussion!

---

**0xTraub** (2024-11-17):

I think this answers my questions about brute force generation and differentiation of colors. Thanks! I like the idea a lot. Simple to implement. How do you think this might work with future address extension schemes or chain-prefixing? If we started prefixing addresses with chain identifiers would those also be colored using a similar scheme?

---

**AdamLeeeee** (2024-11-18):

Great question! You thought about the scalability of this ERC.

Chaining identifiers will not affect the overall scheme of this ERC, but some decisions need to be made. Do identifiers also need to be colored?

From a technical point of view, the prefix part can be processed by the same hashing and coloring algorithm, but whether the coloring of the prefix part is necessary needs to be decided after the chain-prefixing ERC is adopted.

As mentioned in the coloring algorithm, even if there are other address expansion schemes in the future, as long as the address can be calculated by the hash algorithm, then the ERC is universal.

The above is my idea, welcome to join our discussion again!

---

**BohemianHacks** (2024-11-21):

Amazing! Thank you! ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12) ![:purple_heart:](https://ethereum-magicians.org/images/emoji/twitter/purple_heart.png?v=12) ![:blue_heart:](https://ethereum-magicians.org/images/emoji/twitter/blue_heart.png?v=12) ![:green_heart:](https://ethereum-magicians.org/images/emoji/twitter/green_heart.png?v=12) ![:yellow_heart:](https://ethereum-magicians.org/images/emoji/twitter/yellow_heart.png?v=12) ![:orange_heart:](https://ethereum-magicians.org/images/emoji/twitter/orange_heart.png?v=12)

