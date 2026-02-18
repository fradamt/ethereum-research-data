---
source: ethresearch
topic_id: 16774
title: Stealth Address in Account Abstraction
author: jstinhw
date: "2023-09-28"
category: Applications
tags: [account-abstraction]
url: https://ethresear.ch/t/stealth-address-in-account-abstraction/16774
views: 2459
likes: 3
posts_count: 7
---

# Stealth Address in Account Abstraction

# Stealth Address AA Plugin

TDLR; The proposal is a privacy-preserving smart account utilizing stealth address.

Thanks to [@derekchiang](/u/derekchiang) and [Filipp Makarov](https://twitter.com/filmakarov) for their invaluable feedback.

## I. Problem

While Account Abstraction (AA) has been instrumental in providing flexible verification logic beyond the traditional ECDSA signature, there remains the need to confirm your identity and prove ownership of the wallet. Whether it’s a private key, an enclave-based key, or even biometric data, some form of identification is essential.

#### ECDSAValidator

Within the ZeroDev Kernel’s [ECDSA Validator](https://github.com/zerodevapp/kernel/blob/3b38c0bb177c7130d294eba1e80010448b1b53ee/src/validator/ECDSAValidator.sol), the owner’s address is stored on-chain. This approach serves the purpose of verifying the signature originating from the signer. However, this could compromise the privacy of smart accounts by making ownership information publicly accessible.

```solidity
struct ECDSAValidatorStorage {
    address owner;
}

function validateUserOp(UserOperation calldata _userOp, bytes32 _userOpHash, uint256)
        external
        payable
        override
        returns (ValidationData validationData)
    {
        address owner = ecdsaValidatorStorage[_userOp.sender].owner;
        bytes32 hash = ECDSA.toEthSignedMessageHash(_userOpHash);
        if (owner == ECDSA.recover(hash, _userOp.signature)) {
            return ValidationData.wrap(0);
        }
        if (owner != ECDSA.recover(_userOpHash, _userOp.signature)) {
            return SIG_VALIDATION_FAILED;
        }
    }
```

## II. Solution

To mitigate this privacy concern, we employs the use of Stealth Addresses. These are designed to obfuscate the identity of smart account owners.

[![S11_eYzg6](https://ethresear.ch/uploads/default/optimized/2X/8/8b386a2b0ed7a321f1f75f171f3caeaf0d59a0ef_2_690x270.png)S11_eYzg62288×896 167 KB](https://ethresear.ch/uploads/default/8b386a2b0ed7a321f1f75f171f3caeaf0d59a0ef)

### Aggregate Signature

However, the practical limitations of generating shared secrets and corresponding private keys within existing wallet UIs present a challenge. To overcome this, we propose using aggregate signatures that can be verified by the contract.

#### Aggregate ECDSA Signing

Given private key of owner: priv_{owner}, shared secret key: priv_{shared} (derived from ephemeral private key and user’s public key) and message: m

1. Generate (r,s) signature from signing m using priv_{owner}
2. Calculate the aggregate signature s'=s(h+r*priv_{shared})
3. The aggregate signature is (r,s')

#### Aggregate ECDSA Verifying

The aggregated signature

 \begin{aligned}
s' &=s(h+r*priv_{shared})\\ &=k^{-1}(h+r*priv_{owner})(h+r*priv_{shared})\\ &=k^{-1}[h^2+hr*(priv_{owner}+priv_{shared})+r^2*priv_{owner}*priv_{shared}] \end{aligned}

We notice that:

pub_{stealth}=G*(priv_{owner}+priv_{shared})

dh_{owner\_shared}=G*{priv_{owner}*priv_{shared}}

We can thus verify the aggregate signature by:

1. Calculate the inverse of aggregate signature s_1=s'^{-1}
2. Calculate R' and take its x-coordinate r'=R'.x
 R'=(h^2*s_1)*G+(h*r*s_1)*pubkey_{stealth}+(r^2*s)*dh_{owner\_shared}
3. The result is r==r'

## III. Stealth Smart Account

#### StealthAddressValidator

Within the framework of our validator, we’ll securely store the stealth address, stealth public key, and the Diffie-Hellman key. Importantly, to bolster user privacy, **the owner’s address will not be stored** in the validator. This design ensures that there is no explicit connection between the smart account and its respective owner.

```auto
struct StealthAddressValidatorStorage {
    uint256 stealthPubkey;
    uint256 dhkey;
    address stealthAddress;
    uint8 stealthPubkeyPrefix;
    uint8 dhkeyPrefix;
}
```

#### Workflow

The following is the workflow of creating a stealth smart account:

[![Screen Shot 2023-09-28 at 3.02.39 PM](https://ethresear.ch/uploads/default/optimized/2X/9/912e9477117ccfd16620cd8205d4824b13ee0990_2_690x297.png)Screen Shot 2023-09-28 at 3.02.39 PM1364×588 25 KB](https://ethresear.ch/uploads/default/912e9477117ccfd16620cd8205d4824b13ee0990)

### Further Improvement

While our stealth smart accounts are self-created, eliminating the need for separate viewing and spending keys used in standard stealth address implementations, our aim is to ensure compatibility with [ERC-5564](https://eips.ethereum.org/EIPS/eip-5564). This will enable senders to transfer tokens to recipients while maintaining the recipient’s anonymity.

## Replies

**jstinhw** (2023-09-28):

Here’s the [repo](https://github.com/moonchute/stealth-address-aa-plugin) and the [brief doc](https://hackmd.io/@justinzen/HyY5M4tkT).

---

**dimitry-krouthfev** (2024-01-03):

Interesting use of ecdsa aggregation.

In practice, thanks to HD wallets, I feel like you would never use the signing key of a smart account to hold funds. What’s the a tradeoff between using a stealth address scheme here and creating and registering a new eoa ?

---

**shamekaa** (2024-01-11):

The article mentions that “The Stealth Address Validator Plugin are employed to mask the identity of smart account owners. This results in the decoupling of the visible link between smart account owners and their respective smart accounts, thereby ensuring a higher degree of privacy.” . Is it possible to aggregate the Invisible Address plugin with smart wallets, that is, to add the Invisible Address feature to smart wallets, thus reducing the middle ground? This is just a premature idea on my part, perhaps the author’s is the optimal solution.

---

**jstinhw** (2024-01-14):

Hi [@dimitry-krouthfev](/u/dimitry-krouthfev) Thank you for your great question. The stealth address smart account modules serves two primary functions. Firstly, it aims to dissociate the smart account from its owner. This is akin to how an HD wallet generates a series of unlinked addresses from a seed phrase, ensuring privacy and security. Secondly, it endows stealth addresses with programmability.

For example, a sender transfers tokens to a stealth smart account. The recipient can then withdraw these tokens, but only upon meeting certain conditions, such as possessing a specific NFT. This mechanism negates the need for the receiver to generate and communicate a new address to the sender through off-chain methods.

In essence, this method provides a blend of anonymity and smart contract functionality

---

**jstinhw** (2024-01-14):

Hi [@shamekaa](/u/shamekaa). Thanks for the feedback.

Can you elaborate more on the “Invisible Address plugin”? Does it employ a different method to achieve the separation of the smart account from its owner, similar to how the stealth address plugin operates?

---

**magneeo** (2024-01-15):

In the linked document, I read “that associates an individual’s EOA address with their respective smart accounts. From the feedback we’ve gathered, this utility has been instrumental in simplifying the management of multiple smart accounts. However, we believe that users should also have the freedom to choose how much privacy they want to maintain.”

This is a great way to address account privacy issues, and for users who are already accustomed to using an EOA address, adding a plugin will give them better privacy protection without having to revert to a new account. But wouldn’t it be a better experience for new users to have an aggregated account instead of the EOA+ plugin?

