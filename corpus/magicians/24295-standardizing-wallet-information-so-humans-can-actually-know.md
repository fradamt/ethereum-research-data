---
source: magicians
topic_id: 24295
title: Standardizing wallet information so humans can actually know what they are signing
author: PatrickAlphaC
date: "2025-05-21"
category: EIPs > EIPs informational
tags: []
url: https://ethereum-magicians.org/t/standardizing-wallet-information-so-humans-can-actually-know-what-they-are-signing/24295
views: 1296
likes: 23
posts_count: 15
---

# Standardizing wallet information so humans can actually know what they are signing

# Wallet information standardization

- Wallet information standardization
- Abstract
- Motivation
- Specification

Definitions:
- EIP-712 Digest
- Domain Hash
- Message Hash
- Calldata Digest

[Rationale](#rationale)

- What we propose instead: EIP-712 signatures
- What we propose instead: Transactions
- What we propose instead: Smart Contract Wallets
- Example workflow

[Backwards Compatibility](#backwards-compatibility)
[Security Considerations](#security-considerations)
[Acknowledgements](#acknowledgements)
[Futher Considerations](#futher-considerations)
[Copyright](#copyright)

# Abstract

This ERC aims to do two things.

1. Set out a standard of information that wallets offer

For EIP-712 signed data, wallets should always offer to show the `EIP-712 Digest`.

For transactions that include calldata, wallets should always offer to show the `Calldata Digest`.

1. Define resulting digests laid out in EIP-712

Namely:

- Domain Hash: domainSeparator = hashStruct(eip712Domain)
- Message Hash: hashStruct(message)
- EIP-712 Digest: encode(domainSeparator : 𝔹²⁵⁶, message : 𝕊) = "\x19\x01" ‖ domainSeparator ‖ hashStruct(message)

# Motivation

Verifying data on hardware devices is challenging. With the recent hacks of Bybit ($1.4B), WazirX ($200M), and Radiant Capital ($50M), we saw how important it is to verify what you’re signing on your device, because websites can be hacked and are often hacked, so we should not trust them to send the correct data to our wallets. We must rely on our wallets exclusively to show the correct data.

For EIP-712 data, if the device shows the entire struct, you have to either rely on a device to extract the struct to verify it on another device, or you have to review each character with your eyes. For small structs, this is ok, and even good, as it was the direct motivation behind EIP-712, however, for large amounts of data, this task is incredibly difficult.

For “normal” transaction calldata, we can decode the calldata to make it more human readable; however, developers often “pack” data so that it cannot be decoded, but it will save gas.

And finally, when it comes to signing smart contract wallet transactions, the terminology can get quite convoluted. A user is expected to sign a `safeMessage` which is different from the result of the `encode(domainSeparator : 𝔹²⁵⁶, message : 𝕊) = "\x19\x01" ‖ domainSeparator ‖ hashStruct(message)` computation set out in EIP-712. However, they also have a `SafeMessage hash` which is different from the `SafeMessage`, even though the `SafeMessage` is also a hash, but very different from the `SafeMessage Hash`. So if the result of the `encode(domainSeparator : 𝔹²⁵⁶, message : 𝕊) = "\x19\x01" ‖ domainSeparator ‖ hashStruct(message)` computation set out in EIP-712 had a name, we could talk about it easier, and have something less confusing than `SafeMessage` which is a hash, and `SafeMessage hash`, which is also a hash, just not the `SafeMessage hash`.

Examples of different terminology:

- Openzeppelin calls it the “typed data hash” implicitly
- Safe{Wallet} calls it either the safeTxHash, SafeMessageHash, safeMessageMessage or other depending on context

# Specification

## Definitions

## EIP-712 Digest

The result of the `encode(domainSeparator : 𝔹²⁵⁶, message : 𝕊) = "\x19\x01" ‖ domainSeparator ‖ hashStruct(message)` computation set out in EIP-712 will be henceforth referred to as the “EIP-712 digest”.

## Domain Hash

EIP-712 outlines the `domainSeparator` as `domainSeparator = hashStruct(eip712Domain)`. Many wallets and UIs have started calling this the `domain hash`. This ERC outlines to formalize this name.

## Message Hash

EIP-712 does not formalize a name for the resulting digest from the `hashStruct(message)` calculation. Many wallets and UIs have started calling this the `mesage hash`. This ERC outlines to formalize this name.

## Calldata Digest

This is a new term for a hash of the calldata sent in a transaction, defined as such:

```auto
calldataDigest = keccak256(len(calldata) ‖ calldata)
```

Python implementation

```python
from eth_hash.auto import keccak
import binascii

def compute_calldata_digest(calldata):
    if isinstance(calldata, str) and calldata.startswith("0x"):
        calldata = binascii.unhexlify(calldata[2:])
    length = len(calldata)
    length_bytes = length.to_bytes(32, byteorder="big")
    combined = length_bytes + calldata
    return "0x" + keccak(combined).hex()
```

# Rationale

Let’s say I want to do the following:

1. Approve my ERC20 token to be deposited into Aave with the approve function
2. Deposit my ERC20 into Aave using the supply function
3. Using a batch transaction with my Safe{Wallet} smart contract wallet

When I go to sign my EIP-712 typed data, my Metamask (or other software wallet) looks like so:

[![Screenshot 2025-05-21 at 11.57.51 AM](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1f7c9caa3fec24a39ea488515ab51e19c2aa7064_2_235x500.png)Screenshot 2025-05-21 at 11.57.51 AM988×2094 305 KB](https://ethereum-magicians.org/uploads/default/1f7c9caa3fec24a39ea488515ab51e19c2aa7064)

The `data` section is populated with the calldata associated with the batch transactions. As I am on a computer, it is not hard to copy paste the calldata (and the entire `SafeTx` message data) and verify its correctness.

However, let’s look at what this looks like on several different hardware wallets. What you are about to see is a single screen from each hardware wallet that is showing the EIP-712 struct.

Gridplus, with 3 pages of data similar to this:

[![IMG_2372](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4dc3be380bfbec95c02b38538183818eb01b0c79_2_375x500.jpeg)IMG_23721920×2560 385 KB](https://ethereum-magicians.org/uploads/default/4dc3be380bfbec95c02b38538183818eb01b0c79)

Trezor, with 8 pages of data similar to this:

[![IMG_2377](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c9df80c124a3244623efb47381d36c8f502b1b0a_2_375x500.jpeg)IMG_23771920×2560 230 KB](https://ethereum-magicians.org/uploads/default/c9df80c124a3244623efb47381d36c8f502b1b0a)

Ledger, with too many pages of data that Ledger just “stops” (this is mitigated by the fact that they show the domain & message hash, though. More on that soon)

[![Screenshot 2025-05-21 at 4.03.17 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c294e4537eb34f70de095f5562efd2c4295b3ea1_2_369x500.jpeg)Screenshot 2025-05-21 at 4.03.17 PM1244×1684 84.3 KB](https://ethereum-magicians.org/uploads/default/c294e4537eb34f70de095f5562efd2c4295b3ea1)

Users are then expected to do one of the following:

1. Eyeball the data in the EIP-712 struct and calldata
2. Use another device to pull the calldata off these devices

Doing number 1 is a recipe for disaster, as a single digit of calldata can easily be missed, and could be the difference between success and disaster. Number 2 seems like the wrong answer, since we are now forcing wallets to be more directly connected to external sources.

## What we propose instead: EIP-712 signatures

Instead, for this EIP-712 data, we could show the digest at the bottom (as of today, Ledger almost does this, it shows the Message Hash & Domain Hash, which can be combined to show the EIP-712 digest).

Ledger (as of today) shows the Domain & Message hash, instead (or in addition) to these two, we would show the EIP-712 Digest.

[![IMG_2381](https://ethereum-magicians.org/uploads/default/optimized/2X/b/bfd401aac01ddfc806aa0cc1972d51eb13a5e989_2_375x500.jpeg)IMG_23811920×2560 192 KB](https://ethereum-magicians.org/uploads/default/bfd401aac01ddfc806aa0cc1972d51eb13a5e989)

A user can then calculate the EIP-712 hash themselves and compare it to what they see on their wallet.

## What we propose instead: Transactions

For transactions, we propose the calldata digest is placed on the bottom of the wallet.

[![Calldata Digest](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f9084df3ff51586c56dec169fe580c2b6ebc6e91_2_80x500.png)Calldata Digest216×1346 224 KB](https://ethereum-magicians.org/uploads/default/f9084df3ff51586c56dec169fe580c2b6ebc6e91)

## What we propose instead: Smart Contract Wallets

Finally, smart contract wallets like Safe{Wallet} could use consistent terminology. Instead of `safeTxHash` they can use `EIP-712 digest`. Instead of `SafeMessage` and `SafeMessage Hash`, they can use `SafeMessage` (unchanged) and `EIP-712 digest`, which seems much less confusing.

## Example workflow

1. User initializes transaction or EIP-712 signature
2. User can either:

Walk through entire struct/calldata to make sure it is correct
3. Use tools such as safe-hash, safeutils, safe-tx-hashes-utils, swiss-knife, or other to calculate calldata digest or eip-712 digest, and compare digest on wallet
4. Use a software wallet combined with their hardware wallet to tell them the resulting digests
5. User can feel confident they are signing what they want to sign

# Backwards Compatibility

None of this EIP/ERC has any effect on the core of Ethereum. This is also merely additive, so I do not suspect it should have an impact on any backward compatibility.

# Security Considerations

Hackers will know that for large calldatas and EIP-712 structs, users will rely on the calldata and EIP-712 digests for signing their transacitons, and may wish to mine a digest with different calldata that matches what a user may expect. At this time, we consider this computationally infeasible.

We intentionally didn’t include a `chainId`, `deadline`, etc in the calldata digest, because we think users should be able to use the same calldata digest for the same calldata, no matter the chain, time, etc. But I’d love others to weigh in on if they think a different hash would be more appropriate.

For users who do choose to “hook up” their software wallets (ie, Metamask, Rabby) to their hardware wallets, they will likely start to rely on the software wallet to correctly show this new digest. This would put increased pressure on software wallets to be secure. Instead of trusting the website, a user is trusting their software wallet or EIP-712 digest/calldata digest calculation tool.

# Acknowledgements

The [argent](https://www.argent.xyz/vi/blog/argent-crypto-wallet-security-emoji-hash-cryptography-trust) team in the past did something similar, where they would hash a new account address, convert that into emojis, and show that to the user. This way, non-technical users could have some assurance they were looking at the correct new address, as the emojis could/should match.

# Futher Considerations

There are some additional improvements we could make to this.

1. Add emoji digests instead of hex digests

This is an ERC aimed at making verifying calldata and EIP-712 structs easier. It might be worth considering showing emojis instead of hex data. Users less familiar with hex data may have an easier time thinking “I’m looking for duck, flag, tree, frog” than “I’m looking for 0xe1e5c20c6a7a236391fa479108b2d621fc216932efd6945d57b963ff218f0ef0”.

1. Add a new EIP-191 type

For further gas savings, we could turn the EIP-712 digest and calldata digest into new EIP-191 types, this way, smart contract developers could have users sign off on calldata without having to store the entire calldata on-chain or in a transaction. At the moment, this seems a bit unimportant, and potentially even more confusing, because an EIP-712 signature could easily implement this without creating a new type.

1. MCP AI with calldata decoding

It could be interesting to give an AI model the ability to decode calldata, and explain a transaction in English, but today, there seem to be a lot of issues with that. Like privacy, what if the AI messes up, etc. But, there is precedent and even MVP’s of what this could like, [for example Pranesh’s MCP with foundry example.](https://github.com/PraneshASP/foundry-mcp-server)

# Copyright

Copyright and related rights waived via [CC0](https://eips.ethereum.org/LICENSE).

## Replies

**codebyMoh** (2025-05-22):

Great write-up. One question — why not incorporate `chainId` into the `calldataDigest` to prevent accidental reuse on the wrong network? Curious to hear thoughts on that tradeoff between reusability and cross-chain safety. Although it helps user in chain abstracted dapps to see at last stage which chain he is interacting.

Digest visibility on hardware wallets is one of the weakest links in current UX. Standardizing `EIP-712 Digest` and `Calldata Digest` is long overdue. Maybe worth extending this to NFT signature flows as well — especially where `EIP-712` structs are large and need digest verification on consumer wallets.

Should we include a version prefix or domain-specific tag (e.g., `"\x19CalldataDigest"` like EIP-191/EIP-712) to prevent hash collision misuse across protocols?

---

**MicahZoltu** (2025-05-22):

I strongly recommend reading over prior proposals to solve this problem, which I and many others agree is an important problem to solve in need of a champion:


      ![image](https://ethresear.ch/uploads/default/optimized/2X/b/b5d7a1aa2f70490e3de763bef97271864784994f_2_32x32.png)

      [Ethereum Research – 26 Feb 25](https://ethresear.ch/t/enforceable-human-readable-transactions-how-to-solve-bybit-like-hacks/21836)



    ![image](https://ethresear.ch/uploads/default/original/3X/b/2/b23af2169fcffd61a9c10828a15d5b934f2298d0.png)



###





          Security






Special thanks to Augusto Teixeira and Pedro Argento for reviewing this piece.  Introduction Ethereum has just suffered the largest theft in cryptocurrency history. It was neither a protocol bug nor a smart contract flaw — everything was working...



    Reading time: 9 mins 🕑
      Likes: 15 ❤













      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/719)












####



        opened 04:18AM - 22 Sep 17 UTC



          closed 12:43AM - 16 Jan 22 UTC



        [![](https://avatars.githubusercontent.com/u/886059?v=4)
          MicahZoltu](https://github.com/MicahZoltu)





          stale







A lot of debate has been happening around how we can make signing a more secure […]()process for end users.  One of the common arguments is that while all of the proposed solutions may resolve the problem for advanced users (developers, tech savvy users, professionals, etc.) it doesn't address the problem of naive users not understanding what they are signing.  They can often be thought of as the legalese presented to people in contracts: it is better than signing a blank sheet of paper, but to the average person its mostly gibberish.

An idea that @Arachnid and I started batting around in an attempt to come up with a long-term solution to this problem is to provide a mechanism by which things can be signed (ideally transactions and arbitrary messages) such that signer can present the user with informed consent without having to trust the UI.

The general premise is that the actor wanting a signature presents the signing tool with the data they want signed as well as a DSL that describes how the data should be presented to the user.  The signer would then ask the target contract if the DSL is valid, and only prompt the user to sign if the contract asserts that the DSL is in fact valid.

This is quite similar to #712, though it strives to take things a step further than just function name and parameters.

As far as the DSL itself goes, one option would be a text-only DSL that allows for replacement variables.  An example DSL may be something like
```
I would like to create an order offering ${data[0,64] as number} ${(data[64,64] as contract).name()} tokens in exchange for ${data[128,64] as number} ${(data[192,64] as contract).name()} tokens.
```
An untrusted dApp would send that DSL (exactly) to the signer along with the transaction they want signed.  The signer would then ask the `transaction.to` contract whether the hash of the DSL is an approved DSL.  If it is, then the signer would extract data from the `transaction.data` and do an `eth_call` to fetch the `name()` of the two contracts (tokens in this example) and finally generate the string to present to the user.  This solution is very simple and allows for devices with small screens that can only present text (e.g., Ledger) to be able to reasonably present the user with information that the contract author has deemed as enough for informed consent.

Another more feature rich solution (in the extreme) would be to allow the DSL to be some form of constrained layout engine markup (e.g., HTML).  The idea here would be that the signer could verify the DSL was approved just like with the text DSL, but would be able to use a basic UI to present the data to the user like the 0x OTC dApp:
![image](https://user-images.githubusercontent.com/886059/30728433-077329da-9f0d-11e7-80f4-e201230bfd44.png)

For complex contracts, a full UI is much more understandable to an end user than a paragraph or two of madlibs text, and it gives the dApp developer the ability to create a generally better user experience.

The obvious disadvantage to the full GUI DSL is that it can't reasonably be rendered on a text-only display like a watch or hardware key.  With the way this is proposed, a contract could support multiple DSLs so a well written contract may support both text only DSL (for small screens and screen readers) and also a GUI DSL for a better user experience for most users.  This would allow dApp developers to provide high quality signing experiences to users on devices that support it with graceful degradation on devices that don't.  It also allows signers to implement the presumably easier-to-implement madlibs spec fist, then expand towards the full GUI support implementation later.

Open Questions:
* What is does the madlibs DSL look like?
* What does the GUI DSL look like?
* Are the benefits of a GUI DSL over a madlibs DSL worth the additional implementation costs on signing tools?
* Are there existing DSLs that would give us broad support out of the box (e.g., HTML)?
* What datatypes should the signing UI DSL support?
  * timestamp: could present users with a date/time picker on click
  * counter: could have an up-down clicker
  * range: could have a range slider with tick DSL defined tick size
  * others?












I only glanced at the abstract of your proposal here, so I apologize if this is answered/addressed already, but I think that just showing the user a digest or hash of any kind is not going to help much.  For a user to provide informed consent, they need to see a curated human readable description of the transaction, which can (and should) be provided/validated by the author of the contract they are interacting with.  The above two links have different proposals for achieving that goal.

---

**PatrickAlphaC** (2025-05-22):

Good questions! On calldata, I think it’s more appropriate for digests to be the same no matter the chain id.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/patrickalphac/48/7343_2.png) PatrickAlphaC:

> We intentionally didn’t include a chainId, deadline, etc in the calldata digest, because we think users should be able to use the same calldata digest for the same calldata, no matter the chain, time, etc. But I’d love others to weigh in on if they think a different hash would be more appropriate.

And since this isn’t a new EIP-191 typed transaction, I don’t think adding `x19` and the likes makes sense either.

---

**mdaus** (2025-05-22):

On top of this, we can implement ERC-7730 (Clear Signing Format) that defines a JSON schema for metadata that wallets use to render smart-contract calls and EIP-712 messages in a human-readable way.

The metadata mirrors ABI types, so parsing logic is mechanically derived, minimizing divergence between off-chain previews and on-device rendering

It is only used by Ledger at the moment but we can start to test this on software wallets first before migrating to all types of hardware wallets.

Currently it only supports EIP-712 data but we should update it to support many other formats including UserOps and EIP-7702 for example.

---

**PatrickAlphaC** (2025-05-22):

I’ve read these, and I love all the work that has gone into thinking about this! While these are helpful for less security conscious people, I think they can be quite misleading, and require a lot of overhaul to smart contract design.

I think my proposal solves a different issue these two bring up.

- My proposal is looking to make it easier to verify data on a hardware device, where eyeballs will fail. Yes, this will require regular users to be a bit more educated (the average user would need to be slightly more technical)
- These two proposals look at enshrining text into the application layer to make it easier for less-technical people to have assurance.

[I’ve outlined why I think these proposals don’t make sense to prioritize here.](https://ethresear.ch/t/enforceable-human-readable-transactions-how-to-solve-bybit-like-hacks/21836/27?u=patrickalphac)

> I think that just showing the user a digest or hash of any kind is not going to help much.

On a hardware wallet, your recommendation would be to read the human-readable string embedded in the smart contract, which I agree, would be easier than reading a digest. However, I think it language is so problematic, that people would still sign “bad” transactions. For example, a [UniswapV2 swap transaction](https://docs.uniswap.org/contracts/v2/guides/smart-contract-integration/trading-from-a-smart-contract), take this solidity:

```solidity
swapExactTokensForETH(amountIn, amountOutMin, path, msg.sender, block.timestamp)
```

What would the text be?

```auto
Swap 5,000 USDC for at least 1 ETH with a deadline of xxx, and send the tokens to you
```

Hmm… You don’t want to trust USDC is the true USDC  is correct though (does your contract have a whitelist for all tokens?). And who is `you`?

```auto
Swap 5,000 tokens at address XXXXXXXX for at least 1 ETH with a deadline of YYYY, and send the tokens to ZZZZZZZZ
```

Now, if this shows up on your hardware wallet, are you eyeballing each address? Now you’ve opened yourself up to an [address poison attack](https://arxiv.org/html/2501.16681v1).

But not only that, you batched it in your Safe{Wallet}, and added an approval first. What does the “final” text say now? Does each contract need to call into each other to generate the final string? You are still eyeballing each address on your hardware wallet, yikes!

Ok… So how can we solve this? Well, your hardware wallet could show the user a hash of the description, which they could compare to the expected hash… But now we are back to my proposal here, just showing a digest of the calldata, and having another device explain the calldata.

# More thoughts

It could be interesting to have a `getDocsURI` function where a bot could read the docs in order to help decode the calldata into a human readable description, and this would be a much more gas efficient way to do this. Additionally, the `getDocsURI` could use a DSL (as your proposal says) that takes calldata as input, and outputs a human-readable description. (Sort of like a `docs_lang`), but either way, we would still want a minimal set of characters a user needs to look at on their wallets so they don’t run into security fatigue, and we don’t have to waste gas on explaining transactions - when all the information is already in the calldata!

The two proposals linked IMO are like adding a translator enshrined in the smart contracts, which seems very redundant to me.

---

**PatrickAlphaC** (2025-05-22):

Oh wow! Yes! I could see my proposal combining with ERC-7730 very well! I hadn’t read that before.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/patrickalphac/48/7343_2.png)
    [EIP-7730: Proposal for a clear signing standard format for wallets](https://ethereum-magicians.org/t/eip-7730-proposal-for-a-clear-signing-standard-format-for-wallets/20403/7) [EIPs](/c/eips/5)



> Ah I love this!!! I’d like to add some functionality that I think will make all of this “just work”.
> May I recommend a new ERC-7730 function called getWalletDocsUri. Here is an example solidity implementation
> string constant DOCS_URI = "...."; // string here
> uint256 public latestDocsVersion = 0;
>
> function getWalletDocsUri(uint256 docsVersion) external view returns(string memory) {
>    // Could easily add conditionals/mappings/etc here....
>    return DOCS_URI;
> }
>
> This would return a URI (similar …

I added a potential improvement to the ERC, I feel like 7730 could really be what we need!! I love the idea!

Then, combine these two, and we make life WAY easier for people!!!

---

**prasincs** (2025-05-23):

Great write up. I’m in favor of creating consistent naming here - and `EIP712 Digest` and `calldata Digest` seem clear in intent and what to expect.

> Add emoji digests

I’m not sure if this will translate that well unless we restrict to a very limited minimum subset of unicode that renders on all devices. I don’t think we can assume that a hardware device can render latest emojis, or even phones in developing countries

> MCP AI with calldata decoding

This could be an okay end state but there’s a simpler solution that can be a web service that decodes and includes a proof. Explaining in English is IMO nice to have after deterministic decoding and proof.

> Calldata digest vs chainID, deadline

this would require making certain keys like deadline, timestamp, chainID into some kind of well known “reserved” fields not used for digest calculations.

---

**PatrickAlphaC** (2025-05-23):

After some further consideration, here is what I think needs to be done:

# Very Soon

1. QR code to extract data off hardware wallets
2. Include EIP-712 and calldata digests

# Later

1. docsURI for a base64 encoded version of a smart contract’s documentation, including ABI (included in ERC-7730?)
2. AIs to read your decoded calldata (gathered from docsURI, or a centralized ABI database like Etherscan or Scourcify), and then transcribe it to “average” users

If an average user cannot read the decoded data, they must rely on the AI. This isn’t great, because we want people to only trust their wallets, but right now, they just blindly sign.

---

**Strapontin** (2025-06-03):

I have thought about such transaction description before reading you view on the topic, and it feels like while you are showing a best case scenario where anyone could fluently read everything that would happen in a transaction before signing it, it does feel very complicated on multiple levels.

In my thoughts, the message could be generated as follow:

**For every transactions (if batched)**

**Step 1**: The wallet checks the contract on the blockchain. If the contract is not verified, show this as a strong warning.

**Step 2**: Fetch the function name from its selector in the verified contract, and show it to the user alongside with parameters used in the call.

These simple 2 step verification has the pros of quickly yielding a warning when interacting with a potential malicious, unverified smart contract, and displaying with precision the function called with the parameters used. There is no better precision than showing such datas, even though it may not be as easily understandable for newcomers as the examples you have shown in your message.

The negative points I also see from my proposition is the displayed function in case of `fallback` execution may or may not be easy to get, and API call may reach a high rate, but users could provide their own API key.

From this basic implementation, many upgrades will be possible, but we need to start low to reach high

---

**MicahZoltu** (2025-06-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strapontin/48/15367_2.png) Strapontin:

> Fetch the function name from its selector in the verified contract, and show it to the user alongside with parameters used in the call.

This assumes that the source you are fetching from is not compromised, and the computer you are fetching with is not compromised.  The security problem many of us are trying to address is the one where you don’t trust the internet and the host you are working on may be compromised.  You *do* trust some “offline” hardware device which may have a limited trustless communication channel, but it is constrained in what it can do.

---

**Strapontin** (2025-06-04):

Can you elaborate on how transcribing a transaction hash to a human readable text without trusting anything on the internet ? I fail to understand how `0x...` could be translated to `Swapping X token and getting Y in exchange` without having a high-level grasp of the code

---

**MicahZoltu** (2025-06-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strapontin/48/15367_2.png) Strapontin:

> Can you elaborate on how transcribing a transaction hash to a human readable text without trusting anything on the internet ?

The proposal in this thread (different from EIP-719 proposal) is to have the hardware wallet hash the description text that was presented to the user (which is untrusted at this point) and append it to the transaction call parameters.  The contract would then validate that the provided hash matches the *correct* description that *should* have been provided to the user for that transaction, and if that validation fails the transaction immediately reverts.

An attacker website could still trick the user into signing a transaction by providing a fake description, but the transaction would just revert immediately and waste a bit of user gas.  It would not provide a vector to trick the user into executing a transaction they don’t intend.

---

For EIP-719, you could limit the DSL to only allow formatting strings using data available in the transaction itself, which would still allow for some protection (e.g., ERC-20 transfers could easily be resolved, and same with ERC-20 transfers via a SAFE) but more complex DeFi things would not be able to be encoded meaningfully, like Uniswap transactions would not know symbol or decimals.

You could potentially address this by having the symbol/decimals of the tokens being interacted with provided as calldata, so they are then available to the offline signer, but this will increase calldata costs (maybe worth it in some cases).

---

**PatrickAlphaC** (2025-07-10):

Whatever the methodology we choose, signing intent clarity is critical for web3 to scale. People will keep getting rugged because they don’t understand their wallets.

We will be tracking this on this website, more information coming soon.



      [github.com](https://github.com/walletbeat/walletbeat)




  ![image](https://opengraph.githubassets.com/9f2895abdd79e6532c6cc99e76219397/walletbeat/walletbeat)



###



An open repository of EVM-compatible wallets.

---

**MASDXI** (2025-07-22):

If MCP is one of possible solution then Lookup contract address on sourcify query function sig from bytes4 dict

Should be a minimum for implementation.

