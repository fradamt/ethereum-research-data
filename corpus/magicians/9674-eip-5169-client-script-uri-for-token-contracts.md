---
source: magicians
topic_id: 9674
title: "EIP-5169: Client Script URI for Token Contracts"
author: JamesB
date: "2022-06-19"
category: EIPs
tags: [nft, token, tokenscript]
url: https://ethereum-magicians.org/t/eip-5169-client-script-uri-for-token-contracts/9674
views: 4317
likes: 5
posts_count: 16
---

# EIP-5169: Client Script URI for Token Contracts

**Abstract**

This EIP provides a contract interface adding a `scriptURI()` function for locating executable scripts associated with the token.

**Motivation**

Often, smart contract authors want to provide some user functionality to their tokens through client scripts. The idea is made popular with function-rich NFTs. It’s important that a token’s contract is linked to its client script, since the client script may carry out trusted tasks such as creating transactions for the user.

This EIP allows users to be sure they are using the correct script through the contract by providing a URI to an official script, made available with a call to the token contract itself (`scriptURI`). This URI can be any RFC 3986-compliant URI, such as a link to an IPFS multihash, GitHub gist, or a cloud storage provider. Each contract implementing this EIP  implements a `scriptURI` function which returns the download URI to a client script. The script provides a client-side executable to the hosting token. Examples of such a script could be:

- A ‘miniDapp’, which is a cut-down DApp tailored for a single token.
- A ‘TokenScript’ which provides TIPS from a browser wallet.
- An extension that is downloadable to the hardware wallet with an extension framework, such as Ledger.

**Script location**

While the most straightforward solution to facilitate specific script usage associated with NFTs, is clearly to store such a script on the smart contract. However, this has several disadvantages:

1. The smart contract signing key is needed to make updates, causing the key to become more exposed, as it is used more often.
2. Updates require smart contract interaction. If frequent updates are needed, smart contract calls can become an expensive hurdle.
3. Storage fee. If the script is large, updates to the script will be costly. A client script is typically much larger than a smart contract.

For these reasons, storing volatile data, such as token enhancing functionality, on an external resource makes sense. Such an external resource can be either be  hosted centrally, such as through a cloud provider, or privately hosted through a private server, or decentralized hosted, such as the interplanetary filesystem.

While centralized storage for a decentralized functionality goes against the ethos of web3, fully decentralized solutions may come with speed, price or space penalties. This ERC handles this by allowing the function `scriptURI` to return multiple URIs, which could be a mix of centralized, individually hosted and decentralized locations.

While this ERC does not dictate the format of the stored script, the script itself could contain pointers to multiple other scripts and data sources, allowing for advanced ways to expand token scripts, such as lazy loading.

The handling of the integrity of such secondary data sources is left dependent on the format of the script. For example, HTML format uses [the integrity property](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity), while [signed XML format has <Manifest/>](https://www.w3.org/TR/xmldsig-core2/#sec-Manifest).

**Overview**

With the discussion above in mind, we outline the solution proposed by this ERC. For this purpose, we consider the following variables:

- SCPrivKey: The private signing key to administrate a smart contract implementing this ERC. Note that this doesn’t have to be a new key especially added for this ERC. Most smart contracts made today already have an administration key to manage the tokens issued. It can be used to update the scriptURI.
- newScriptURI: an array of URIs for different ways to find the client script.

We can describe the life cycle of the `scriptURI` functionality:

- Issuance

1. The token issuer issues the tokens and a smart contract implementing this ERC, with the admin key for the smart contract being SCPrivKey.
2. The token issuer calls setScriptURI with the scriptURI.

- Update scriptURI

1. The token issuer stores the desired script at all the new URI locations and constructs a new scriptURI structure based on this.
2. The token issuer calls setScriptURI with the new scriptURI structure.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

We define a scriptURI element using the `string[]`.

Based on this, we define the smart contract interface below:

```auto
interface IERC5169 {
    /// @dev This event emits when the scriptURI is updated,
    /// so wallets implementing this interface can update a cached script
    event ScriptUpdate(string[] memory newScriptURI);

    /// @notice Get the scriptURI for the contract
    /// @return The scriptURI
    function scriptURI() external view returns(string[] memory);

    /// @notice Update the scriptURI
    /// emits event ScriptUpdate(scriptURI memory newScriptURI);
    function setScriptURI(string[] memory newScriptURI) external;
}
```

The interface MUST be implemented under the following constraints:

- The smart contract implementing IERC5169 MUST store variables address owner in its state.
- The smart contract implementing IERC5169 MUST set owner=msg.sender in its constructor.
- The ScriptUpdate(...) event MUST be emitted when the setScriptURI function updates the scriptURI.
- The setScriptURI(...) function MUST validate that owner == msg.sender before executing its logic and updating any state.
- The setScriptURI(...) function MUST update its internal state such that currentScriptURI = newScriptURI.
- The scriptURI() function MUST return the currentScriptURI state.
- The scriptURI() function MAY be implemented as pure or view.
- Any user of the script learned from scriptURI MUST validate the script is either at an immutable location, its URI contains its hash digest, or it implements ERC 5169, which asserts authenticity using signatures instead of a digest.

### Rationale

This method avoids the need for building secure and certified centralized hosting and allows scripts to be hosted anywhere: IPFS, GitHub or cloud storage.

### Backwards Compatibility

This standard is compatible with all Token standards (ERC20, 721, 777, 1155 etc.)

### Examples

We here go through a couple of examples of where an authenticated script is relevant for adding additional functionality for tokens.

1. A Utility NFT is an event ticket and the authenticated script is a JavaScript ‘minidapp’ which asks the user to sign a challenge message that shows ownership of the key controlling the ticket. The dapp would then render the signature as a QR code which can be scanned by a ticketing app, which could then mark the ticket as used.
2. Smart Token Labs uses a framework called TokenScript; one element of which is a user interface description for contract interaction through tokens.
Consider a simple ‘mint’ verb associated with an already existing NFT. The associated script can for example allow the owner to mint a derivative through a contract already holding enough ether for the minting fee, without needing to connect their wallet.
3. An NFT Script which controls a Smartlock. For example consider the lock  being linked to a digital NFT twin and being controlled with the verbs “lock” and “unlock”, each of which has an associated JavaScript. Each of these scripts could be executed after the user signs a challenge in a web-view. This is an off-chain example that uses on-chain assets for functionality.

## Tests

### Test Contract

```auto
import "@openzeppelin/contracts/access/Ownable.sol";
import "./IERC5169.sol";
contract ERC5169 is IERC5169, Ownable {
    string[] private _scriptURI;
    function scriptURI() external view override returns(string[] memory) {
        return _scriptURI;
    }

    function setScriptURI(string[] memory newScriptURI) external onlyOwner override {
        _scriptURI = newScriptURI;

        emit ScriptUpdate(newScriptURI);
    }
}
```

### Test case

```auto
const { expect } = require('chai');
const { BigNumber, Wallet } = require('ethers');
const { ethers, network, getChainId } = require('hardhat');

describe('ERC5169', function () {
  before(async function () {
    this.ERC5169 = await ethers.getContractFactory('ERC5169');
  });

  beforeEach(async function () {
    // targetNFT
    this.erc5169 = await this.ERC5169.deploy();
  });

  it('Should set script URI', async function () {
    const scriptURI = [
      'uri1', 'uri2', 'uri3'
    ];

    await expect(this.erc5169.setScriptURI(scriptURI))
      .emit(this.erc5169, 'ScriptUpdate')
      .withArgs(scriptURI);

    const currentScriptURI = await this.erc5169.scriptURI();

    expect(currentScriptURI.toString()).to.be.equal(scriptURI.toString());
  });
```

## Security Considerations

**When a server is involved**

When the client script does not purely rely on connection to a blockchain node, but also calls server APIs,  the trustworthiness of the server API is called into question. This ERC doesn’t provide the mechanism to assert the authenticity of the API access point. Instead, as long as the client script is trusted, it’s assumed that it can call any server API in order to carry out token functions. This means the client script can mistrust a server API access point.

**When the scriptURI doesn’t contain integrity (hash) information**

We separately authored ERC5170 to guide on how to use digital signatures to efficiently and concisely to ensure authenticity and integrity of scripts not stored at an URI which is a digest of the script itself.

## Replies

**JamesB** (2022-06-19):

The main purpose of the EIP is to improve functionality for tokens, “making tokens smart”. The EIP improves the flow of using tokens when thinking from the token perspective.

EG:

Alice’s office is operated by a smart lock operated by NFT tokens. Alice wants to collaborate with Bob who will need to use the office. Alice sends Bob an NFT to operate the office door.

A wallet which recognises EIP-5169 will use the `scriptURI` function to download a simple javascript to provide the ‘unlock’ function, which would consist of an API to provide a challenge which the wallet can do a signPersonalMessage on, and return the signature via an endpoint provided by the script to operate the lock.

ERC20 Token A is swappable for Token B, at a rate provided by an endpoint. Token A implements a script which an EIP-5169 enabled wallet can download from the `scriptURI` in Token A. This script will supply the authorised swap path, even if it’s just a link to a decentralised exchange with the required URI switches. This could make interacting with the tokens simpler and more secure; as assuming Token A is an established token and that we trust the authors we can trust the swap script.

Clearly, EIP5169 only applies to new tokens or tokens that can be proxy-updatable. There is an additional proposal EIP5170 which allows authorised scripts to be supplied in any way to existing contracts.

---

**SamWilsn** (2022-08-05):

Most EIPs omit set functions, because setting is usually a dapp specific action, while getting needs to be standardized across all dapps so third parties can read the information. I’d omit the `setScriptURI` function, and simply require that when the script URI changes, `ScriptUpdate` is emitted.

---

**JamesB** (2022-08-25):

Hi Sam, if the script is hosted on IPFS (without a certificate infrastructure this is the best way to provide a validated script) we’d be unable to update the script without the setScriptURI. It’s intended that the script is stored offchain in much the same way as ERC721’s tokenURI() or contractURI() is usually handled.

EDIT: Ok I think I got your point now - the script update could be implemented by the developer in whichever way they like but that method MUST emit the ScriptUpdate event if the script is updated.

---

**vrypan** (2022-11-19):

Is there an overlap with EIP 5559?

“The cross chain write deferral protocol provides a mechanism to defer the storage & resolution of mutations to off-chain handlers”

---

**sullof** (2023-02-25):

The proposal is interesting but I it is easy to work-around it.

I can write a perfect smart contract that set correctly the script URI then the script URI points to a dynamic generated file that I can change when I want bypassing any control on the smart contract, fooling the user.

I suggest you should force the user to set only URIs that point to immutable files, like on IPFS or Arweave, that can be easily checked in the smart contract.

---

**xinbenlv** (2023-03-09):

Hey just came across this interesting EIP. QQ: was it intentional that `scriptURI()` carries no input parameters?

---

**JamesB** (2023-03-13):

Hi [@sullof](/u/sullof) yes that should be covered in the detail of the EIP. You can do 2 approaches:

- Store on IPFS, this is accepted as a validated script, because it’s immutable and must be the file that the developer set using the deployment key.
- Store on FTP: This will be treated as untrusted, unless the script contains a signature from an approved key. This key management system will probably use EAS.

This EIP has a sister EIP which is still in progress: EIP5160 - this provides means to enable trust in the served file, either through a contained signature or separately bundled signature. The implementation is largely left to the implementer but within certain guidelines.

---

**JamesB** (2023-03-13):

Hi [@xinbenlv](/u/xinbenlv) yes it is intentional: there should only be one script per contract. Any nuances between tokenIds should be handled within the script itself.

---

**JamesB** (2023-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vrypan/48/5055_2.png) vrypan:

> EIP 5559

I hadn’t seen EIP5559 - it looks quite interesting and in theory there is an overlap - it may be possible to achieve 5169 using 5559 but I think 5169 is a lot more focused - it serves a trusted interface script that wallets, applications etc. can quickly check for, whereas 5559 is a catch-all for any offchain and L2 data.

---

**xinbenlv** (2023-03-22):

This EIP is now in “Stagnant” status. If you want to continue driving this EIP to final, first step is to send a GitHub PR to move it back to “Draft” and fix all linter errors if needed.

---

**JamesB** (2023-03-25):

Here is a reference implementation for EIP-5169:


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/AlphaWallet/Web3E-Application/tree/master/New%20Office%20Door)





###



[master/New%20Office%20Door](https://github.com/AlphaWallet/Web3E-Application/tree/master/New%20Office%20Door)



Applications Using Web3E. Contribute to AlphaWallet/Web3E-Application development by creating an account on GitHub.










The contract can be seen here on Mumbai: [STLDoor | Address 0xcf05782decfbf996a4082c9b2648f9ff5b12fdca | PolygonScan](https://mumbai.polygonscan.com/address/0xcf05782decfbf996a4082c9b2648f9ff5b12fdca#readContract)

---

**JamesB** (2023-04-26):

Are there any further comments before we move to final?

---

**fulldecent** (2024-04-02):

I’m not sure why the setScriptURI function should be standardized.

Is there some wallet that will be updating lots of contracts at the same time?

It this connected to a factory pattern where contracts are created in a series?

If not then it is not necessary to explain how the scriptURI is set.

---

**JamesB** (2024-04-08):

The name of the function itself doesn’t need to be standardised but the operation should be, according to the guidelines in the specification.

The script linked to by scriptURI may expose token functions and could be abused, since if the script is immutable (ie hosted on IPFS) it is treated as certified by the contract authors (with any trust the user has for the contract authors extended to the script). Therefore, setScriptURI is sufficiently sensitive to need to adhere to these standards.

---

**KK779** (2024-12-29):

I really like scriptURI because there are various checks I want to do off-chain instead of in the contract but I feel like this could’ve been an extension to tokenURI’s metadata [ERC-1046: tokenURI Interoperability](https://eips.ethereum.org/EIPS/eip-1046) with the event for cache handling. The tokenURI’s json would basically point to other uris. I like that it’s explicitly controlled by the contract owner but I think we assume that’s the case for tokenURI as well. Are there big cases I’m missing that make it necessary to be another URI(s) stored on-chain? Also I wish the event was called “NewScriptURI” because “ScriptUpdate” could imply the underlying data has changed but really the functionality is different uris. I get that sometimes both change but this isn’t always the case. At this point since it’s final, I’ll properly just implement it as-is for the sake of standards but I would sleep better if there were stronger reasons.

