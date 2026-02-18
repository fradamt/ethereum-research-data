---
source: ethresearch
topic_id: 15856
title: Passkey based Account Abstraction signer for smart contract wallets
author: rishotics
date: "2023-06-12"
category: Applications
tags: [account-abstraction]
url: https://ethresear.ch/t/passkey-based-account-abstraction-signer-for-smart-contract-wallets/15856
views: 10937
likes: 22
posts_count: 24
---

# Passkey based Account Abstraction signer for smart contract wallets

# Passkey Signer Package

TLDR— We represent a new signer for account abstraction wallets or SDK for having a passkey-based login mechanism. The passkey allows users to use their device’s primary authentication mechanisms like face id, touch id or passwords to create a wallet and sign a transaction.

*Thanks to [@nlok5923](/u/nlok5923) and [@0xjjpa](/u/0xjjpa) for their work, reviews and discussions*

**Definition**

According to the ethers documentation, a signer is:

“…an abstraction of an Ethereum Account, which can be used to sign messages and transactions and send signed transactions to the Ethereum Network to execute state-changing operations.”

The **PasskeySigner** package will extend the abstract signer provided by ethers and offer the functionality to sign transactions, messages, and typed messages for blockchains using passkeys. A *passkey* is a digital credential tied to a user account and a website or application. Passkeys allow users to authenticate without entering a username or password or providing any additional authentication factor. This technology aims to *replace legacy authentication mechanisms such as passwords*. Passkeys serve as a replacement for private key management, offering faster sign-ins, ease of use, and improved security.

**Bundlers and EntryPoint** in this context refer to the same concepts mentioned in ERC 4337.

## Advantages

There are several advantages:

- User Experience: Onboarding new users to the blockchain is challenging, with seed phrases and private key management being less than ideal. We aim to address this by ensuring even users unfamiliar with security concerns can safely manage their funds.
- Security: Passkeys provide inherent security by eliminating issues like weak and reused credentials, leaked credentials, and phishing.
- Plug and Play: Simplify the integration of smart contract wallets by replacing the reliance on Externally Owned Accounts (EOA) for transaction and message signing. With the passkey module, wallet infrastructure and wallets can seamlessly integrate passkey functionality, streamlining the user experience.
- Cross-platform support: Extend the solution to devices without biometric scanning but with Trusted Execution Environment (TEE) support. Utilizing QR code scanning, devices perform a secure local key agreement, establish proximity, and enable end-to-end encrypted communication. This ensures robust security against phishing attempts.

[![](https://ethresear.ch/uploads/default/optimized/2X/6/64ba5c827a3dacec883ed4f6109d96032f1e2c27_2_690x391.jpeg)2718×1544 245 KB](https://ethresear.ch/uploads/default/64ba5c827a3dacec883ed4f6109d96032f1e2c27)

## Disadvantages

**Gas cost**: On-chain signature verification for passkey-based transactions incurs significant gas costs. Efforts have been made to reduce the gas cost for verification. Opclave utilizes a custom rollup with the “secp256r1 verifier” precompile contract following Optimism’s Bedrock Release standards. Ledger is also working on further optimizing gas costs.

**Device dependency**: Though passkeys are device dependant there are workarounds. Apple device users can securely back up their passkeys in iCloud Keychain, overcoming this restriction. For other devices, the module will provide multi-device support, allowing users to add multiple owners (devices) to their smart contract wallet.

## Usage of PasskeySigner

The initialization would be straight forward if the wallet sdk has itself has exposed necessary interfaces for accepting an external signers. For example let’s suppose if there’s a wallet sdk known as abc sdk. And let’s assume it accepts the signer while initializing it’s instance so in that case the integration would look like this

```auto
// importing BananaPasskeyEoaSigner package
import { BananaPasskeyEoaSigner } from '@rize-labs/banana-passkey-manager';
import { ABCWallet } from 'ABCWallet-sdk';

// initializing jsonRpcProvider
const provider = ethers.getDefaultProvider();

// creating an instance out of it
const bananaEoaSignerInstance = new BananaPasskeyEoaSigner(provider);

// initializing the EOA with a specific username (it should be unique) corresponding to which the passkey
// would be created and later on accessing
await bananaEoaSignerInstance.init('');

// initializing signer for smart contract wallet.
const abcSmartWalletInstance = new ABCWallet(bananaEoaSignerInstance);
```

Flow of making a transaction will look like this

[![](https://ethresear.ch/uploads/default/optimized/2X/8/8c0fa887c74da3310af964e95ef03ced64043acb_2_544x499.jpeg)1600×1468 132 KB](https://ethresear.ch/uploads/default/8c0fa887c74da3310af964e95ef03ced64043acb)

## Background

One of the notable features of smart contract wallets is the provision of custom signatures for transactions. Among the prominent signature schemes, secp256R1-based signatures stand out. It’s important to note that secp256k1 is a Koblitz curve, whereas secp256r1 is not. Koblitz curves are generally considered slightly weaker than other curves. Both secp256k1 and secp256r1 are elliptic curves defined over a field z_p, where p represents a 256-bit prime (although each curve uses a different prime). Both curves adhere to the form y² = x³ + ax + b. In the case of the Koblitz curve, we have: a=0  and  b=7

For R1 we have  a = FFFFFFFF 00000001 00000000 00000000 00000000 FFFFFFFF FFFFFFFF FFFFFFFC  and b = 5AC635D8 AA3A93E7 B3EBBD55 769886BC 651D06B0 CC53B0F6 3BCE3C3E 27D2604B

The R1 curve is considered more secure than K1 and supports major hardware enclaves. Also, most security enclaves cannot generate K1-based signatures, which are commonly used by EVM blockchains for signing transactions and messages.

### Creating a new passkey

A typical ethers signer signs transactions by either having the private key itself or by being connected to a JsonRpcProvider to fetch the signer. However, the Passkey Signer operates differently as it does not possess the private key. Instead, it can sign transactions and messages by sending them to the hardware, and the signed string is provided as the output.

```auto
const publicKeyCredentialCreationOptions = {
		//The challenge is a buffer of cryptographically random bytes generated on the server, and is needed to prevent "replay attacks".
    challenge: Uint8Array.from(
        randomStringFromServer, c => c.charCodeAt(0)),
    rp: {
        name: "Your Name",
        id: "yourname.com",
    },
    user: {
        id: Uint8Array.from(
            "UZSL85T9AFC", c => c.charCodeAt(0)),
        name: "your@name.guide",
        displayName: "ABCD",
    },
//describe the cryptographic public key. -7 is for secp256R1 elliptical curve
    pubKeyCredParams: [{alg: -7, type: "public-key"}],
    authenticatorSelection: {
        authenticatorAttachment: "cross-platform",
    },
    timeout: 60000,
    attestation: "direct"
};

const credential = await navigator.credentials.create({
    publicKey: publicKeyCredentialCreationOptions
});

//credential object

PublicKeyCredential {
    id: 'ADSUllKQmbqdGtpu4sjseh4cg2TxSvrbcHDTBsv4NSSX9...',
    rawId: ArrayBuffer(59),
    response: AuthenticatorAttestationResponse {
        clientDataJSON: ArrayBuffer(121),
        attestationObject: ArrayBuffer(306),
    },
    type: 'public-key'
}

```

The public-key is extracted and that is passed to the smart contract wallet.

### Signing using passkeys

During authentication an *assertion* is created, which is proof that the user has possession of the private key.

```auto
const assertion = await navigator.credentials.get({
    publicKey: publicKeyCredentialRequestOptions
});
```

The **publicKeyCredentialCreationOptions** object contains a number of required and optional fields that a server specifies to create a new credential for a user.

```auto
const publicKeyCredentialRequestOptions = {
    challenge: Uint8Array.from(
        randomStringFromServer, c => c.charCodeAt(0)),
    allowCredentials: [{
        id: Uint8Array.from(
            credentialId, c => c.charCodeAt(0)),
        type: 'public-key',
        transports: ['usb', 'ble', 'nfc'],
    }],
    timeout: 60000,
}

```

The interaction with the hardware will be done using the webauthn library which allows us to generate new cryptographic keys within the hardware. The public key which is an (x,y) co-ordinate, corresponding to this private key is fetched. These co-ordinates should be stored inside the smart contract wallets and they will act like a owner to the smart contract wallet.

## Replies

**MicahZoltu** (2023-06-13):

What is the actual underlying key storage mechanism?  Are they stored locally in the mobile device’s secure storage?  If so, then loss of device means loss of keys.  Are they stored with Apple?  If so, then they aren’t secure against powerful adversaries (government can just ask Apple for the keys).

---

**drortirosh** (2023-06-13):

Please correct me if I’m wrong, but a signing request using this signer (or any webauthn signer) pop up a generic dialog on the device, which of unrelated to the actual signed request.

That is, the user is requested to sign blindly, not showing even the hash of the message.

---

**plusminushalf** (2023-06-13):

When it comes to backing up keys, the Webauthn spec doesn’t dive into the details. Different providers can choose to handle it in their own ways or not offer key backup at all. So, according to the [Webauthn spec](https://w3c.github.io/webauthn/#backed-up), it’s pretty much open for interpretation.

To figure out if a key can be backed up or not, you can take a peek at the third bit of the flags byte. It’s all explained in the documentation for the [Web Authentication API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API/Authenticator_data).

Now, I did some digging for Apple, and it seems like their keys can be backed up as they do set the backup-enabled flag. But, to be honest, I’m not entirely sure about the exact process they use for backup.

I did not get the chance to check for other operating systems and passkey implementations like Yubi keys.

---

**rishotics** (2023-06-13):

Yes, you’re correct. The WebAuthn specification indeed does not include a provision to display the details of the transaction being signed to the user within the authentication prompt. The signing request simply triggers a generic dialogue on the device asking the user to authenticate, without showing the details of what exactly is being signed.

However, it is still possible to provide the user with transaction details through a separate transaction confirmation page or dialogue before the WebAuthn signing request is issued. This would be similar to how Ethereum transactions are handled in MetaMask, where the user can review and confirm the transaction details before signing. In this way, users can still be fully informed about the transaction they are authorizing, even if those details are not included in the WebAuthn prompt itself.

---

**plusminushalf** (2023-06-13):

Did some digging for apple and found this:

Passkey synchronization provides convenience and redundancy in case of loss of a single device. However, it’s also important that passkeys be recoverable even in the event that all associated devices are lost. Passkeys can be recovered through [iCloud keychain escrow](https://support.apple.com/guide/security/sec3e341e75d/), which is also protected against brute-force attacks, even by Apple.

iCloud Keychain escrows a user’s keychain data with Apple without allowing Apple to read the passwords and other data it contains. The user’s keychain is encrypted using a strong passcode, and the escrow service provides a copy of the keychain only if a strict set of conditions is met.

To recover a keychain, a user must authenticate with their iCloud account and password and respond to an SMS sent to their registered phone number. After they authenticate and respond, the user must enter their device passcode. iOS, iPadOS, and macOS allow only 10 attempts to authenticate. After several failed attempts, the record is locked and the user must call Apple Support to be granted more attempts. After the tenth failed attempt, the escrow record is destroyed.

---

**MicahZoltu** (2023-06-13):

When the users set this up they are asked to enter a `passcode` and then the key is encrypted against that passcode and the encrypted data is sent to Apple?

Is this passcode just a 4-8 digit pin (like a lockscreen pin) or is it an actual password?  Are users made properly aware of the importance of both choosing a high security passcode and storing it safely/securely?

None of the brute force mitigations do any good against government/apple attacks since they can just exfiltrate the encrypted key and brute force it offline.  The 10 attempt limit only applies to less sophisticated/powerful attackers who are trying to brute force on the device itself.

---

**plusminushalf** (2023-06-13):

Passkeys afaik is set up when you set up your operating system since the passcode that is talked about here is the passcode of the device.

The flow is (this is only for apple, I am not aware of other operating systems):

1. User setups operating system - setup a OS password (this is called passcode)
2. User setups fingerprint - this is an additional security with passcode, user can open the secure enclave with either of the two i.e passcode or fingerprint
3. Application requests webauthn credentials, operating system creates a new secp256r1 public <> private key pair. Store this newly generated pair in secure enclave of the device which can be unlocked by passcode or fingerprint.
4. Apple’s operating system also backs up this secure enclave with their iCloud keychain escrow for the users so that they can recover this at any given time in future.

So in theory yes if Government get’s access to this encrypted storage from either Apple or Apple decides to go bad they don’t have a 10-attempt limit.

Users can though opt out of this backup and backup these keys manually [Remove a passkey or password from your Mac and iCloud Keychain - Apple Support (IN)](https://support.apple.com/en-in/guide/mac-help/mchl77e2cb66/mac)

But I couldn’t find any way to restore the keys.

---

**Victor928** (2023-06-13):

How much is the gas cost on Ethereum mainnet? Around 40w?

---

**nlok5923** (2023-06-14):

Specifically for verifying the r1 signatures onchain within the smart contract wallet we found the gas consumption to be approx 300k gas.

Similarly if you are looking to understand gas consumption comparison on making transaction by EOA and by 4337 compatible smart contract wallet you can refer to this article by stackup


      ![](https://ethresear.ch/uploads/default/original/3X/8/4/846e9c696df68cdcf3eb94b254242d7e5272e285.png)

      [stackup.fi](https://www.stackup.fi/resources/what-is-eip-4337)



    ![](https://ethresear.ch/uploads/default/original/3X/4/1/41cfa1999bc03e0c404fcfc076e63e96269d9030.svg)

###



Stackup explains how EIP-4337 account abstraction enables smart contract wallets with social logins, gasless transactions, one click multi-operations, and more!

---

**Victor928** (2023-06-14):

Thanks for the information.

How about an ERC20 transfer?

---

**kopy-kat** (2023-06-23):

In the 9th arrow on the tx flow chart it says “parse public values as a eth address” - what exactly do you mean by this? As far as I was aware, current implementations pass different fields from the webauthn response to be verified on-chain (eg auhtenticatorData, clientData, …)

---

**nlok5923** (2023-06-27):

Hey [@kopy-kat](/u/kopy-kat)

Once you make a create request to `navigation.credentials.create` via the webAuthn interface it returns the hex values of the X and Y coordinate of the public key over the r1 elliptic curve and we parse those values and build the H160 Ethereum compatible address.

---

**rishotics** (2023-06-30):

Hey [@Victor928](/u/victor928), the final gas amount will be directly dependant on the on-chain verification of secp256R1’s signature. This verification will vary from application to application unless and util there is a set standard.

---

**musnit** (2023-07-12):

Apple claims (and afaik there have been some audits of this) that the 10-attempt-limit is enforced by a HSM in their data centers, ie:

- Apple themselves or a government cannot brute force this. It would trigger the HSM to erase the key.
- Related, 4 - 8 digits is okay (well, maybe not 4 lol but probably 6-8 is ok) since this 10-max-attempts limit is enforced by the HSM

Of course, if Apple/Gov can physically exfiltrate the encrypted key by breaking HSM technology, this would be ineffective, but that’s much harder & more expensive to do and would require some 0-day side channel attacks or something of that sort on the HSM *(although imo those kinda 0-days likely do actually exist)*.

Apple could also be lying ofc lol.

More insights here: https://twitter.com/matthew_d_green/status/1394389869540089856

---

**dannpr** (2023-07-31):

Hey, I don’t really understand the sequence diagram.

What’s the passkey signer module give when the Dapp request for signer ?

When it’s wrote passing Signer for EOA you mean that the output of the module is store where ?

The wallet infra is the Smart contract wallet ?

what the passkey signer is used for ?

---

**nlok5923** (2023-08-20):

1. Actually the passkey signer module is a wrapper sdk which abstracts away the complexities of dealing with passkeys. And it provides you with a signer which is able to perform signing of message and transaction using device passkeys.
2. The passkey signer module output doesn’t need to be stored anywhere the passkey signer module get initializes via the device passkeys itsself which remains in the device so you don’t need to store anythng anywhere.
3. Wallet infra are the infra that provides facilities to create and use smart contract wallets.
4. The Passkeys are used for wallet creation and transaction signing it’s pretty much analogous to metamask requesting for transaction confirmation. But here instead of just confirming you authenticate  and signs a message.

---

**Joseph** (2023-08-20):

First of all I love the design approach of this system.

1. How do you manage revoking specific keys? Suppose a key is compromised how could I revoke an individual key or all keys.
2. How are permissions for the generated key managed (at the dapp level I presume)?
3. Am I understanding this process correctly? User signs a publicKeyCredentialCreationOptions with an secp256k1 key, that credentialId is respected as the original secp256k1 key within the dapp

---

**ColbyCarro** (2023-08-24):

The exact implementation of passkey-based account abstraction signers can vary based on the blockchain platform and wallet software being used.

---

**rishotics** (2023-08-24):

Thank you [@Joseph](/u/joseph) Here is the answer to your questions:

1. The process will be similar to SAFE smart contract for removing keys and permissions.
2. Currently no, the Dapp doesn’t have any authority to decide the permissions for keys
3. No, the secp256k1 does not come into the signing process. The user signs the challenge inside the publicKeyCredentialCreationOptions with their R1 key.

---

**0xjjpa** (2023-08-24):

I’m long overdue to comment here, but better late than never. First of all, kudos to [@rishotics](/u/rishotics) and the rest of the Banana SDK team for leading this conversation. As the maintainer of Passkeys[dot]is I see the potential of the tech to be applied in crypto despite some caveats already identified.

For me, there are a couple of minimal requirements needed for this setup to work:

- Multi-sig smart account - Although Passkeys are an ideal “kickstart” mechanism to onboard a user, it has a few flaws already pointed in the thread that make it unsuitable to make it a long-term solution as the only signer setup within a smart account. Here I envision something like a Safe that can be initially provisioned by a Passkey, yet can add other signers and even remove itself if needed.
- Pure client implementation - Right now we are trying to go through the traditional webauthn workflow, which involves a server that creates a request and pairs it against the user name passed as part of the key creation params. However, relying on a server to “allow” usernames instead of passing the ECDSA signature might create a unwanted centralised point of failure not required for a smart wallet.
- Lazy deployment - Because of the way Passkeys work, we can generate a public key during the generation of the first instance of the account. This key can then be passed to a contract and an entrypoint to provide a smart account address. We could use this address from day 0 until we would want to deploy it, allowing us minimal engagement with it until needed (e.g. airdrop to the account). Seems like @nlok5923 has already a way to have this address available.
- Minimal gas cost - Even on L2s, the current cost of a secp256r1 signature verification is circa 1.2m, which is a pretty penny. There are multiple groups exploring the reduction of this cost (gas bad) including doing Elliptic-curve optimisations (see Ledger’s team presentation for EthCC '23), but nothing is “official” yet. Even my own demo on github (passkeys-webauth) has this cost.
- Audit - At the end of the day we are verifying a ECDSA signature manually, since current’s Ethereum ecrecover is unable to parse this curve. Thus, it would be beneficial to the community to rally over an audit around a standard that can be used across the industry and benefit smart wallet creators as equal instead of building yet another lego block.

If we can tackle these points, I believe the other concerns can be partially or fully mitigated. For instance, we can work around Apple’s iCloud Keychain native syncing, and trusting their HSM setup provides a similar attack vector than, let’s say, a Web2 OAuth login like Web3Auth. Even then I would argue that Passkeys provide a better alternative, since they can work offline and w/o any server interface, as long as `navigator.credentials` is supported by the browser.

Now to answer some questions:

- MicahZoltu - The keys are stored in the device and synced to iCloud for iOS devices (other devices do not have automatic cloud storage). In iOS, you can’t enable Passkeys w/o iCloud Keychain enabled, but you can remove the key from iCloud once it’s synced, and only from iCloud. In terms of security, in theory, and based on statements made by various Apple spokespeople, Apple stores user’s credentials KEK’s in their HSMs, which would be wiped after 10 failed attempts to the user’s iCloud. Thus, even on the case of a governmental seizure, they would technically be unable to share the key. Of course, metadata and other IP related information, even to the point of device fingerprinting, would still be likely possible. plusminushalf shared more on this in a previous post.
- drortirosh yes, this is correct. What’s even funnier, is that the actual signing payload doesn’t matter. Because of the way webauthn works, we always sign on top of the authenticatorData and can not make use of the payload. So, the only thing we can learn from this request is “it has been signed”. It doesn’t matter what the user signs, just that it signed something at X point in time.
- Victor928 it would be safe to assume that all transactions through a Passkey-based smart account would have a minimal requirement of the secp256r1 verification, currently at 1.2m cost on a naive implementation, some research pointing it going down as low as 300k-60k (see Ledger’s presentation for EthCC '23 on this).
- Joseph under a single 1-out-of-1 naive implementation of a Passkey-based smart account, there’s no key revocation, and thus, would be awful if you need to rotate. Right now, the only way to “share” a Passkey is physically via Airdrop to a contact nearby, or using a roaming authenticator (e.g., Yubikey). Thus a multi-sig setup would likely be preferred. Other comments were already answered by @rishotics in the last post.

(**NB:** Someone with more rights kindly update to mention the people tagged).


*(3 more replies not shown)*
