---
source: magicians
topic_id: 3392
title: "ERC-2126: Signature Type Recognition"
author: pedrouid
date: "2019-06-19"
category: ERCs
tags: [wallet, signatures]
url: https://ethereum-magicians.org/t/erc-2126-signature-type-recognition/3392
views: 4716
likes: 14
posts_count: 26
---

# ERC-2126: Signature Type Recognition

Enable Dapps to be able to recognize how a given signature was signed (e.g. by owner of a smart contract, EOA, etc) so that they can use the correct mechanism to verify the signature.

Inspired by 0x Protocol V2.0 Signature Types

https://github.com/ethereum/EIPs/pull/2126

## Replies

**pedrouid** (2019-06-19):

I would like to get some feedback on the Web3 JSON API support

IMO I think that the typeBytes shouldn’t be optional and they would technically be backwards compatible since the byte as appended at the end of the signature.

However [@hiddentao](/u/hiddentao) raised a good point that a longer signature length can break verification of some modules that exist right now.

Although technically the `r,s,v` parameters are left untouch with this proposal, there could be libraries that may error if provided with a longer signature.

My suggestion would be to audit the most used javascript libraries (web3.js, ethers,js and eth.s) first to consider the implications of signature length before introducing this optional parameter to signing schemes on the Web3 API

PS - not just javascript libraries, which should also consider Geth and Parity clients plus other provider implementations in other languages like Swift, Kotlin, Python, etc

---

**dekz** (2019-08-02):

Note we recently amended the Wallet Signature Type to return a known value rather than bool. To prevent a contract with truthy return value being used as a signature verification function.

```auto
# When wallet signature this value must be returned or revert
bytes32 magic_salt = bytes32(bytes4(keccak256("isValidWalletSignature(bytes32,address,bytes)")));
```

Looks like this EIP still has `boolean isValid`

```auto
function isValidSignature(
    bytes32 hash,
    address signerAddress,
    bytes memory signature
)
    public
    view
    returns (bool isValid);
```

EIP1271 uses:

```auto
bytes4(keccak256("isValidSignature(bytes,bytes)")
```

We opted for changing it rather than returning the function signature as an additional safety mechanism.

[@pedrouid](/u/pedrouid) what do you think about reserving some additional types and providing an offset for custom types to start from? I wonder what `0x05` will be in the wild after a year, it could mean a number of different signatures.

---

**hiddentao** (2019-08-03):

Good point. The `isValidSignature` example in ERC-2126 needs to be updated - that method is not part of ERC-2126 anyway, it’s just referring to it.

---

**Amxx** (2019-08-05):

The issue with ERC1271 is that everyone is implementing it differently.

References at the bottom of the EIP point to 0x using it in the format (bytes32, bytes) → (bool). I have an implementation in kitsune wallet that uses the same interface. So does iExec’s signature verification.

I understand the rationnal behind returning a magic_salt but it looks like no one is using it. I’ve also seen the addition of the ‘address signerAddress’ for the first time here, which could make sens, but then why limit it to an address and not a bytes32 to support more DIDs format ?

It’s high time discussion on ERC1271 restart …

---

**PhABC** (2019-10-23):

[@pedrouid](/u/pedrouid) [@hiddentao](/u/hiddentao)

After so long, seems like the community is still divided between the `(bytes32,bytes)` vs `(bytes,bytes)`. To come to a place of proper standardization instead of being in limbo, I believe ERC-1271 should bite the bullet and support both. If that was the case, what do you guys think of having something like

| Signature byte | Signature type |
| --- | --- |
| 0x00 | Illegal |
| 0x01 | Invalid |
| 0x02 | EIP712 |
| 0x03 | EthSign |
| 0x04 | WalletBytes |
| 0x05 | WalletBytes32 |

Also, I don’t think `Invalid` should be part of the standard as it’s mainly for testing IIRC. What do you guys think? Imo the split between the `bytes` and `bytes32` hurts more than having people supporting both.

---

**hiddentao** (2019-10-24):

I’m ok with removing `Invalid` since `Illegal` is likely good enough for testing purposes.

As for `bytes` vs `bytes32`, i’d rather standardize on one of them and have the community update their implementations. This will avoid confusion (e.g. “which one should I use?” type of questions) and follows the generally agreed-upon “less is more” convention.

It seems to me that `bytes` would be the one to standardize since it provides the most flexibility and is already what’s stated in 1271.

---

**PhABC** (2019-10-24):

I don’t disagree with you, however it’s been over a year and people still can’t seem to agree on bytes or bytes32. For instance, [ERC-1654](https://github.com/ethereum/EIPs/issues/1654) was created for people that want to use the `bytes32` version for it. Imo having some people using bytes32 and others using bytes is worst than having everyone agree to implement both.

`bytes32` is definitely simpler than `bytes` (smart wallet receiving the bytes array need to know what the data is and how to hash it), so I can see the appeal of `bytes32` as well.

---

**wighawag** (2019-10-28):

Actually since EIP-1654 is already using the bytes32 version, there is no need for EIP-1271 to support bytes32.

EIP-1654 could be a Signature type, like EIP-1271 is described here.

That’s actually how we do it here : https://github.com/pixowl/sandbox-smart-contracts/blob/master/src/Sand/erc20/NativeMetaTransactionProcessor.sol#L180

Also relevant to the option of supporting both is my comment on EIP-1271 : https://github.com/ethereum/EIPs/issues/1271

---

**PhABC** (2019-10-28):

Right, but now some project will support ERC-1654 while others ERC-1271 and we will have a divide that will be annoying. If both are always implemented together, might as well une one “umbrella” standard.

As per your comment, I don’t think your flow of checking for one then trying the other if the first fails is necessary if we use ERC-2126, it seems like added complexity. The signature identifier would be 0x04 if you used `isValidSignature(bytes,bytes)` or `0x05` if you used `isValidSignature(bytes32,bytes)`.

[0x uses](https://github.com/0xProject/0x-monorepo/blob/d85e9c7fbbeb5d5165539031742fa2d88e5ea395/contracts/exchange/contracts/src/interfaces/ISignatureValidator.sol#L29) `0x04` for the `(bytes32,bytes)` method and the `0x07` for the `(bytes,bytes)`.

At Horizon, [we use](https://github.com/arcadeum/multi-token-standard/blob/f30bfacb7fa9f1d82f0bf27981a7d2fb59115aca/contracts/utils/SignatureValidator.sol#L24) `0x03` for the `(bytes,bytes)` and `0x04` for the `(bytes32,bytes)`.

---

**wighawag** (2019-10-28):

The flow was to show the potential issue of supporting both on the wallet side.

As I mentioned in our implementation we use a parameter signatureType to not have to do that but my point was that if a wallet support both and do not throw on EIP-1654 version, an attacker could use the gas issue to always use the EIP-1654 and skip the check that would have been performed by EIP1271.

But this is even easier for the attacker if we use SignatureType as the way to decide which one to use

---

**wighawag** (2019-10-28):

As for the division, I don’t think it is an issue, Contract would be incentivised to support both.

Edit: does not make sense ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

~~And as mentioned anyway due to the (gas / signature type skipping) attack vector , when enabling EIP-1271 version the EIP-1654 version need to be disabled.

As such every wallet contract that want to support will have to support both version</del~~

But at the same time, if the goal of EIP-1271 is to clarify the situation, I am all for it.

---

**Amxx** (2019-10-30):

The current specification states that:

> the signature is encoded in the following way:
>
>
>
>
>
> Offset
> Length
> Contents
>
>
>
>
> 0x00
> 1
> v (always 27 or 28)
>
>
> 0x01
> 32
> r
>
>
> 0x21
> 32
> s

While this could be a valid encoding, it is not (AFAIK) the one commonly used by wallet. Usually, the signature is encoded (`r`,`s`,`v`). Decoding is ususally done in assembly [like this](https://github.com/iExecBlockchainComputing/PoCo/blob/master/contracts/SignatureVerifier.sol)

FYI: the code I use to verify signature and support both EOA & ERC1271 (old) in one single function is also part of this file)

---

**pedrouid** (2019-11-19):

Hey everyone, I’d like to pick up on this EIP so that we can merge a draft that we could start sharing with other projects.

Regarding the illegal vs invalid discussion, I would like to have [@dekz](/u/dekz) opinion on this too since they are already using this in their stack. I agree that it seems a bit duplicated but don’t want to introduce unnecessary breaking changes

Regarding the bytes vs bytes32 discussion, I think that they can coexist specially since that there are EIPs for each and about the same number of projects implementing each. Therefore I would signal to make them separate signatures labelled by the respective EIPs

| Signature byte | Signature type |
| --- | --- |
| 0x00 | Illegal |
| 0x01 | Invalid |
| 0x02 | EIP712 |
| 0x03 | EthSign |
| 0x04 | EIP1271 |
| 0x05 | EIP1654 |

I will ping more community members and projects that would be relevant to this EIP too so that we can move this further

cc [@juniset](/u/juniset) [@itamarl](/u/itamarl) [@rmeissner](/u/rmeissner) [@Stefan](/u/stefan) [@alexvandesande](/u/alexvandesande) [@marek](/u/marek)

---

**Amxx** (2019-11-20):

I might be missing something, but would the “signature bytes” be when doing a ERC712 signature that has to be recognised through an ERC1271 redirection?

EthSign and ERC712 way to build a digest from a message/object … and the digest is then signed by the PK. In case of ERC1271 you just have to pass this digest, it gets verified by the “identity” contract using erecover, without necessarily knowing whats actually signed. Does it have to know?

My point is the contract verifying the dignature has to know how to build the digest (ethsign vs erc712) and then it has to know weither to check the validity using ecrecover or asking the “identity” through ERC1271.

Example:

function verifySignature is called with an ERC712 hash and a `bytes` signature


      [github.com](https://github.com/iExecBlockchainComputing/PoCo/blob/master/contracts/IexecClerk.sol#L209)




####

```sol

1.
2. /**
3. * Check orders authenticity
4. */
5. Identities memory ids;
6. ids.hasDataset = _datasetorder.dataset != address(0);
7.
8. // app
9. ids.appHash  = _apporder.hash().toEthTypedStructHash(EIP712DOMAIN_SEPARATOR);
10. ids.appOwner = App(_apporder.app).owner();
11. require(m_presigned[ids.appHash] || verifySignature(ids.appOwner, ids.appHash, _apporder.sign));
12.
13. // dataset
14. if (ids.hasDataset) // only check if dataset is enabled
15. {
16. ids.datasetHash  = _datasetorder.hash().toEthTypedStructHash(EIP712DOMAIN_SEPARATOR);
17. ids.datasetOwner = Dataset(_datasetorder.dataset).owner();
18. require(m_presigned[ids.datasetHash] || verifySignature(ids.datasetOwner, ids.datasetHash, _datasetorder.sign));
19. }
20.
21. // workerpool

```









      [github.com](https://github.com/iExecBlockchainComputing/PoCo/blob/master/contracts/SignatureVerifier.sol#L22)




####

```sol

1. return bytes32(uint256(_addr));
2. }
3.
4. function checkIdentity(address _identity, address _candidate, uint256 _purpose)
5. internal view returns (bool valid)
6. {
7. return _identity == _candidate || IERC734(_identity).keyHasPurpose(addrToKey(_candidate), _purpose); // Simple address || ERC 734 identity contract
8. }
9.
10. // internal ?
11. function verifySignature(
12. address      _identity,
13. bytes32      _hash,
14. bytes memory _signature)
15. public view returns (bool)
16. {
17. return recoverCheck(_identity, _hash, _signature) || IERC1271(_identity).isValidSignature(_hash, _signature);
18. }
19.
20. // recoverCheck does not revert if signature has invalid format
21. function recoverCheck(address candidate, bytes32 hash, bytes memory sign)

```

---

**miguelmota** (2019-11-21):

Regarding the `(bytes32,bytes)`  vs  `(bytes,bytes)` discussion; I’m in favor of  `(bytes,bytes)` because we have a use case where the `isValidSignature` method needs to validate against multiple signatures at once for it to be considered valid, and the different message data and signatures are concatenated and separated with solidity abi encoder so the data type needs to be a `bytes`.

---

**PhABC** (2019-11-29):

Other than the “Invalid” one, I personally agree with this proposal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> Signature byte
> Signature type
>
>
>
>
> 0x00
> Illegal
>
>
> 0x01
> Invalid
>
>
> 0x02
> EIP712
>
>
> 0x03
> EthSign
>
>
> 0x04
> EIP1271
>
>
> 0x05
> EIP1654

I also agree with [@pedrouid](/u/pedrouid) That the `bytes` vs `bytes32` seems too difficult to agree on and might as well have a standard for each. It will be clearer for everyone which method is supported or not, or both.

---

**3esmit** (2019-11-30):

In regards of ERC 1271 for account contracts, I see the correct method would use `bytes, bytes` as they are more flexible and future proof.

In regards of signature type, I think that might be useful… I have a usecase where the account contract is a multisig, and each of these address may or may not be an account contract aswell.

For a very simple account contract, let say [SimpleAccount.sol](https://gist.github.com/3esmit/ef9fbaaab13b62c1b1b459a170db3caa#file-simpleaccount-sol), I can have an owner, which can also be an account contract, or an externally owner account, so I have:

```auto
    /**
     * @notice checks if owner signed `_data`. ERC1271 interface.
     * @param _data Data signed
     * @param _signature owner's signature(s) of data
     */
    function isValidSignature(
        bytes memory _data,
        bytes memory _signature
    )
        public
        view
        returns (bytes4 magicValue)
    {
        if(isContract(owner)){
            return ERC1271(owner).isValidSignature(_data, _signature);
        } else {
            return owner == ECDSA.recover(ECDSA.toERC191SignedMessage(_data), _signature) ? MAGICVALUE : bytes4(0xffffffff);
        }
    }

    /**
     * @dev Internal function to determine if an address is a contract
     * @param _target The address being queried
     * @return True if `_addr` is a contract
     */
    function isContract(address _target) internal view returns(bool result) {
        assembly {
            result := gt(extcodesize(_target), 0)
        }
    }
```

However, if this Account contract happened to be a [MultisigAccount.sol](https://gist.github.com/3esmit/ef9fbaaab13b62c1b1b459a170db3caa#file-multisigaccount-sol), then all the addresses must be externally owned accounts, because the contract have no way of telling where to check the signature.

Imagine could be a multisig of all account contracts, that themselves could also be signed by other account contracts - I see this would be a very edgy use case but It seems a valid use case that may happen in future as account contracts get more popular.

---

**pedrouid** (2019-12-02):

I think there are good arguments regarding `bytes` vs `bytes32` made by everyone on the EIP-1271, let’s signal these on the EIP1271 thread below

cc [@miguelmota](/u/miguelmota) [@PhABC](/u/phabc) [@3esmit](/u/3esmit) [@Amxx](/u/amxx) [@wighawag](/u/wighawag)



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1271)












####



        opened 01:25AM - 28 Jul 18 UTC



          closed 05:10AM - 28 May 22 UTC



        [![](https://avatars.githubusercontent.com/u/9306422?v=4)
          PhABC](https://github.com/PhABC)










**Simple Description**

Many blockchain based applications allow users to sign[…]() off-chain messages instead of directly requesting users to do an on-chain transaction. This is the case for decentralized exchanges with off-chain orderbooks like [0x](https://0xproject.com/) and [etherdelta](https://etherdelta.com/). These applications usually assume that the message will be signed by the same address that owns the assets. However, one can hold assets directly in their regular account (controlled by a private key) or in a smart contract that acts as a wallet (e.g. a multisig contract). The current design of many smart contracts prevent contract based accounts from interacting with them, since contracts do not possess private keys and therefore can not directly sign messages. The proposal here outlines a standard way for contracts to verify if a provided signature is valid when the account is a contract.

See [EIP draft](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1271.md).












Finally regarding solely on the signature type recognition, I would propose to remove the ambiguity of the `Illegal` and `Invalid` and also order signature types by date created as follows:

| Signature byte | Signature type |
| --- | --- |
| 0x00 | Illegal |
| 0x01 | EthSign |
| 0x02 | EIP712 |
| 0x03 | EIP1271 |
| 0x04 | EIP1654 |

I would like [@dekz](/u/dekz) feedback on this since it would break the backwards compatibility on their stack. Hopefully it shouldn’t be too extensive to fix and it would make it clearer for new projects integrating this standard.

---

**dekz** (2019-12-04):

For purely selfish reasons this would be very annoying. Developers could work around this by checking who the sender is and branching logic off of that.

Our v3 version uses the following:

```auto
enum SignatureType {
        Illegal,                // 0x00, default value
        Invalid,                // 0x01
        EIP712,                 // 0x02
        EthSign,                // 0x03
        Wallet,                 // 0x04
        Validator,              // 0x05
        PreSigned,              // 0x06
        EIP1271Wallet,          // 0x07
        NSignatureTypes         // 0x08, number of signature types. Always leave at end.
    }
```

`EIP712` and `EthSign` are the most used in our protocol (note: verified by our contracts not by third party contracts).

We could adopt the standard in the next version of the protocol but it would be some time. We would probably look to move some of the more 0x specific Sig types into a namespace safe area (`PreSigned`, `Validator`). So an agreement on which bytes are future reserved, which are safe for application specific etc, would be useful as well.

---

**PhABC** (2020-01-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> Signature byte
> Signature type
>
>
>
>
> 0x00
> Illegal
>
>
> 0x01
> EthSign
>
>
> 0x02
> EIP712
>
>
> 0x03
> EIP1271
>
>
> 0x04
> EIP1654

[@pedrouid](/u/pedrouid) Would you mind updating the official ERC draft to reflect this? Also, why did the `EIP712` and `EthSign` type swap? `EIP712` used to be the one before. I don’t mind either way, but I’ve personally been using the following:

| Signature byte | Signature type |
| --- | --- |
| 0x00 | Illegal |
| 0x01 | EIP712 |
| 0x02 | EthSign |
| 0x03 | EIP1271 |
| 0x04 | EIP1654 |

As can be seen in [this contract](https://github.com/arcadeum/multi-token-standard/blob/master/contracts/utils/SignatureValidator.sol#L26).


*(5 more replies not shown)*
