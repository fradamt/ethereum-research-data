---
source: magicians
topic_id: 12903
title: "EIP-6492: Signature validation for pre-deploy contracts"
author: Ivshti
date: "2023-02-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-6492-signature-validation-for-pre-deploy-contracts/12903
views: 5852
likes: 14
posts_count: 53
---

# EIP-6492: Signature validation for pre-deploy contracts

EIP 1271 allows contracts to sign messages and works great in tandem with EIP 4337 (account abstraction), but unfortunately contracts (and by extension contract wallets) are not able to sign messages before they’re deployed.

At the same time, using counterfactual deployment to defer this step to a later stage of the use cycle (eg when the first transaction is sent) is a de-facto standard for most wallets, creating the issue of those wallets being unable to sign messages before the user sends their first transaction.

As a solution, we propose an EIP that extends EIP 1271 that allows this by introducing a new signature wrapper format.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6492)














####


      `master` ← `AmbireTech:master`




          opened 10:59AM - 10 Feb 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/3/329c5125a1f68891e6b35abfb3cfb7f417cebfff.jpeg)
            Ivshti](https://github.com/Ivshti)



          [+146
            -0](https://github.com/ethereum/EIPs/pull/6492/files)







This PR adds an EIP that extends EIP-1271 with an addition that allows counterfa[…](https://github.com/ethereum/EIPs/pull/6492)ctual contracts to sign messages and get them verified. It was initially inspired by this thread in the EIP-4337 implementation: https://github.com/eth-infinitism/account-abstraction/issues/188

btw sorry for assigning a number, I read that this is the editor responsibility later on but figured I'd leave it in as it should make life easier

## Replies

**Agusx1211** (2023-02-13):

I like it!

---

An interesting scenario that may be worth considering is if we want these signatures to be usable on-chain. I can think of two approaches:

1. Manually split creationCode and signature, then using a contract send creationCode once (per wallet) and then all other signatures.
2. Provide a singleton or library that performs the whole thing (as shown by the example).

For both cases I wonder if it isn’t a better idea to check for `magicBytes` BEFORE cheking if the wallet is deployed, the rationale is that if you want to validate multiple signatures (on-chain) the wallet will sign them using the `universal` format, but only the first one will be non-deployed. That way these signatures can be a drop-in replacement for regular signatures, and the consumer never needs to mutate them.

It may be required to increase the size of `magicBytes` to avoid collisions, I also wonder if it doesn’t make some sense to use some `0s` for the value to make it cheaper on calldata.

---

**Ivshti** (2023-02-13):

Yep, one of the EIP reviewers also suggested checking  magicBytes FIRST because otherwise previous signatures will be invalidated when the account is deployed and would need to be mutated. I agree with this and also that magicBytes needs to be longer in this case. Will adapt this change.

as for the points:

1. I’m not quite sure what you’re saying - do you mean that verification can be batched? As for using those sigs on-chain, the main problem is that we force CALL rather than the much safer STATICCALL to allow for the deployment
2. Yep, working on it

---

**Ivshti** (2023-03-08):

hey [@Agusx1211](/u/agusx1211), your suggestions have been implemented

But rather than a singleton, we went with a contract that doesn’t need to be deployed and can just be eth_call’d - it will return a bool value from it’s constructor. Here’s an overall example of how the verification of all signature types works: [ERC-6492 verification by Ivshti · Pull Request #3 · AmbireTech/signature-validator · GitHub](https://github.com/AmbireTech/signature-validator/pull/3) and the contract itself: [signature-validator/DeploylessUniversalSigValidator.sol at 6492-verification · AmbireTech/signature-validator · GitHub](https://github.com/AmbireTech/signature-validator/blob/6492-verification/contracts/DeploylessUniversalSigValidator.sol)

---

**Agusx1211** (2023-03-08):

Hey, great! Thank you

---

What is the rationale for using the “create new contract” approach? I think this is equivalent to shipping a library, because the verification code needs to be embedded (in order to create the new contract). If that’s the case, doesn’t make more sense to ship a library instead of deploying a new contract?

Also I think this may be inefficient, because this approach leaves 2 deployed contracts every time a signature needs to be validated on-chain. These contracts are not reused.

---

Small piece of feedback, here:

`bytes memory contractCode = address(_signer).code;`

Solidity won’t optimize this, even if you only use the length of the code, the whole bytecode will be copied into memory. I think something like this does avoid copying:

`uint256 codeSize = address(_signer).code.length;`

But I’m not 100% sure, we should test it and worst case scenario we can just use `EXTCODESIZE`.

---

**Ivshti** (2023-03-08):

Hey [@Agusx1211](/u/agusx1211), thanks for the feedback

the approach is meant to be used for off-chain validation, so that signatures can be validated on any chain without needing to have a singleton pre-deployed. As for on-chain validation, the approach should be completely different, but I personally think that 6492 shouldn’t be used for on-chain validation anyway. The reasons are

1. arguably, most of the cases when you want onchain validation, you already have the contract deployed
2. the security concern of having to use CALL over STATICCALL, and therefore enabling reentrancy attacks

As for the optimization, sure.

---

**Agusx1211** (2023-03-08):

Thanks for the clarification, I had the impression that 6492 was also meant for on-chain verification.

I do think it’s worth the effort to try to find something that works both on-chain and off-chain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> arguably, most of the cases when you want onchain validation, you already have the contract deployed

I disagree here, with the current heavy usage of the `permit` I can totally see a future with most of the wallets doing their first transaction because they signed a message.

Also if EIP-6492 only works off-chain then the wallet has to “guess” how the signature will be used; and if there is not certainty on that result then the wallet must deploy the wallet “just in case”. This erodes most of the benefits of the EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> the security concern of having to use CALL over STATICCALL, and therefore enabling reentrancy attacks

This is a real concern, one possibility could be to force a `revert` and then return if the signature was valid or not (on the revert return), that way we can undo any side-effects of the contract deployment while still retrieving the information we care about. We would do this internally on the singleton/library, and for the caller this would look like a normal `CALL` (but it acts as a `STATICALL`).

The issue with this is that it’s more expensive, but we can add a parameter on the singleton, if the caller wants it to be “side-effects free” then we use the revert approach, if not then we can just do the regular process of deploying → validating, without any reverts.

---

**Ivshti** (2023-03-08):

It could be used on-chain but it does add an extra security dimension to it, so it’s a tradeoff. I don’t see any other clean solution that could work on-chain that doesn’t actually require deploying the contract.

As for the guessing how the signature will be used, this part completely went over my head, can you elaborate? Do you mean that the wallet doesn’t know if the verifier supports 6492?

As for the revert, this is a clever workaround, I’ll think about how to incorporate it. It would require multiple nested calls.

---

**Agusx1211** (2023-03-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> As for the guessing how the signature will be used, this part completely went over my head, can you elaborate? Do you mean that the wallet doesn’t know if the verifier supports 6492?

Not just that, even if the wallet knows that `6492` is supported, then it doesn’t know if the signature will be used on-chain or off-chain, so should the wallet deploy and send a regular signature, or should it send a 6492 encoded signature?

The only “safe” option is to send a regular signature, only on very specific circumstances you can know that the requested signature is for off-chain usage.

If we allow EIP-6492 signatures to be used on-chain then the wallet can always safely encode them that way, and never has to manually deploy a wallet before signing a message.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> As for the revert, this is a clever workaround, I’ll think about how to incorporate it. It would require multiple nested calls.

I haven’t analyzed this completely, but I think this is a solution. The contract is deployed but only temporarily, so any reentrancy, side-effects, etc… those are all erased. It works like a `STATICCALL` in practice.

The way to implement this is:

1. Call a singleton with a regular CALL.
2. The singleton calls itself (some other method) using another CALL.
3. The inner method implements the EIP-6492 logic.
4. If noSideEffects == true and the contract had to be deployed then the inner method returns with revert (if not it returns normally). In both cases the return data is a single boolean with true if the signature is valid.
5. The top level call on the singleton ignores the result of the inner CALL (success or revert) and it just reads RETURNDATACOPY.
6. Then the top level returns true if the signature is valid.

---

**Ivshti** (2023-03-08):

That makes a lot of sense. I’ll continue working on a singleton that enables safe on-chain verification

---

**Ivshti** (2023-03-08):

[@Agusx1211](/u/agusx1211) I forgot that I already thought about `permit`. The thing with permit is - let’s take the most common use case, Uniswap. In order to call the swap in the first place, the account needs to be deployed. So it’s likely going to exist on-chain. Of course, this creates a minor hell for the wallet providers, as you already pointed out - as they need to be aware of how the sig will be used.

The good thing is that the EIP is already 99% there.

Here’s the plan:

- rather than returning 0x01 or 0x00, always revert - just with a different value; one of the revert values will be “magic” (meaning successful sig verification)
- there will be two contracts (as there are now), UniversalSigValidator and ConstructorUniversalSigValidator; UniversalSigValidator.isValidSig always reverts, so UniversalSigValidator can be used as a singleton itself for onchain verification
- ConstructorUniversalSigValidator is more of a helper that verifies a sig in it’s constructor, and also always reverts; this will be used for eth_call off-chain verification, but it could be used for on-chain verification as well for any reason (no need for a separate singleton but slightly more expensive)
- the UniversalSigValidator may have an extra method intended to be used for user-facing on-chain verification, that CALLs itself and handles the revert reason and translates it into a true/false boolean

how does it sound?

---

**Agusx1211** (2023-03-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> In order to call the swap in the first place, the account needs to be deployed.

This may be true for Uniswap, but it’s not strictly true. There are some other use-cases where the `permit` is either executed by a relayer or by other user (like Cowswap or Opensea). Nothing stops Uniswap to implementing a similar model.

---

I think we should leave an easy path for validating EIP-6492 signatures without reverting, at the end of the day reverting is way more expensive, and some architectures may already be “hardened” against reentry, so they may not care if validating a signature has side-effects (and could use the savings).

If we can put all logic in the same contract it would be even better, it would be cheaper to call (because a single address has to be warmed up) and if we design it correctly then we shouldn’t have to duplicate any code.

---

Another opinion of mine is that the “constructor” approach is not worth it, it’s too expensive on-chain and the only advantage that brings is that “it doesn’t have to be deployed” as a singleton for off-chain validations.

But the thing is… the factory **has** to be deployed already (otherwise the signatures will fail to verify anyway), so a team that implements EIP-6492 has to make sure that both the `factory` and `singleton` are deployed. If we use the constructor pattern they don’t need to deploy the `singleton`, but they still have to go and deploy the `factory`.

So I think is better to avoid using it for 3 reasons:

1. It’s more expensive on-chain (so we need to build the singleton anyway).
2. It makes the whole process more complex (on-chain and off-chain work differently).
3. The advantage of using the pattern is eroded by the factory problem.

---

**Ivshti** (2023-03-08):

AA wallet providers need to deploy the factory by definiton just to exist. There are exceptions to this ofc but generally speaking it’s true.

This is not necessarily true for the singleton - let’s say that someone deploys the singleton to a unified address between all major chains. Now, if a team starts working on an AA wallet on a different chain that’s not in that set, they would have to deploy the singleton themselves. This is not really a big deal though.

I agree now that the constructor approach is best left for off-chain validation, and that some projects may be fine with the side-effects so the gas savings could be worth it.

new plan:

- UniversalSigValidator.validateSigWithSideEffects(signer, hash, signature) returns (bool) (better name suggestions?)
- UniversalSigValidator.validateSig(signer, hash, signature) - does a CALL to an additional function (UniversalSigValidator.validateSigWithRevert) that wraps validateSigWithSideEffects but with a revert no matter what happens
- offchain helper remains the same, calls UniversalSigValidator.validateSigWithRevert directly in the constructor

---

**Agusx1211** (2023-03-08):

New plan sounds a lot better to me.

I still think that it would be better to use the singleton for the off-chain case too, teams would need to deploy it anyway (to support the on-chain validation) and maybe having an alternative method leads to them not realizing that an extra step is needed to “fully” support EIP-6492 on a given chain (they test it, it works off-chain, and assume that’s it).

But if we use the singleton for both cases, then testing one case should be enough to guarantee that it will work in the other case.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> but with a revert no matter what happens

Can we skip the revert if the signature didn’t require a contract to be created? `isValidSignature` would still be called using `STATICCALL` so it should be safe.

Naming sounds good to me!

---

**Ivshti** (2023-03-09):

Here’s the new version: [EIPs/eip-6492.md at c2fba9b28c6c7dd2b83ec5bae482ef24c98d4ea0 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/c2fba9b28c6c7dd2b83ec5bae482ef24c98d4ea0/EIPS/eip-6492.md)

we have

- the offhchain helper, doesn’t require singleton deployment
- the singleton with a method that has no side effects, and one that doesn’t
- the one that doesn’t only reverts if needed
- actual exceptions are bubbled up

---

**SamWilsn** (2023-03-10):

From Solidity’s [Contract ABI Specification](https://docs.soliditylang.org/en/v0.8.19/abi-spec.html#non-standard-packed-mode), we see:

> Dynamically-sized types like […] bytes […] are encoded without their length field.

In EIP-6492, we have:

> abi.encodePacked((create2Factory, factoryCalldata, originalERC1271Signature), (address, bytes32, bytes, bytes, bytes))

I’m not a Solidity developer, so perhaps I’m misinterpreting the syntax, but if the lengths of `bytes` variables aren’t encoded, how can the verifier know when the `factoryCalldata` ends and the `originalERC1271Signature` begins?

---

The verifier algorithm doesn’t seem as flexible as it should be. What if, for example, a user signs multiple messages before deploying their contract, and some of those messages are verified after? My interpretation of the steps would mean:

1. Check if the signature ends with the magic bytes (it does.)
2. Call into the multicall+factory (it fails because the contract is already deployed.)
3. Verification failed.

I think the intended behaviour is to fall through each of the bullets? If so, the proposal could make that more clear.

---

> check if there’s contract code at the address. If so perform ERC-1271 verification as usual by invoking isValidSignature

Does the verifier have to unwrap the signature if it’s wrapped? Should mention that in the proposal.

---

> If all this fails, […]

This is slightly ambiguous. If `isValidSignature` returns false, the verifier is supposed to try an `ecrecover`? That would make this proposal incompatible with any upgrade that allows code to be deployed at EOAs (e.g. [EIP-5003](https://eips.ethereum.org/EIPS/eip-5003), [other approaches](https://ethresear.ch/t/a-brief-note-on-the-future-of-accounts/12395).)

---

Something you might want to add to your security considerations is using a signature for mainnet on other networks, like L2s. If the wallet is recreated on a different network (perhaps using a universal deployer), the permissions couldn’t have been updated to match the ones on mainnet, so old keys would still have authority there.

---

**Ivshti** (2023-03-10):

> I’m not a Solidity developer, so perhaps I’m misinterpreting the syntax, but if the lengths of bytes variables aren’t encoded, how can the verifier know when the factoryCalldata ends and the originalERC1271Signature begins?
> That’s correct, it should be abi.encode rather than abi.encodePacked. Will fix.

> The verifier algorithm doesn’t seem as flexible as it should be. What if, for example, a user signs multiple messages before deploying their contract, and some of those messages are verified after? My interpretation of the steps would mean:
> That’s not how it works - see line 120 of the EIP - we only try to deploy the contract if it’s non-existent.
> The use case you’re describing will work without an issue.

I’ll change the first bullet point to add “if it isn’t already deployed”.

> Does the verifier have to unwrap the signature if it’s wrapped? Should mention that in the proposal.
> The bullets are meant to fall through. I’ll add “Then, call contract.isValidSignature as usual with the unwrapped signature” to the first one.

> This is slightly ambiguous. If isValidSignature returns false, the verifier is supposed to try an ecrecover? That would make this proposal incompatible with any upgrade that allows code to be deployed at EOAs (e.g. EIP-5003, other approaches.)

nope, if there’s contract code, we end with the result of `isValidSignature`. I’ll try to rewrite the bullets so that they’re more clear.

> Something you might want to add to your security considerations is using a signature for mainnet on other networks, like L2s. If the wallet is recreated on a different network (perhaps using a universal deployer), the permissions couldn’t have been updated to match the ones on mainnet, so old keys would still have authority there.
> Thiis is intended behavior IMO, and any dapp using signatures should implement it’s own chainId based replay protection. Will add it.

---

**yoavw** (2023-03-11):

[@Ivshti](/u/ivshti) following up on our discussion (and I apologize for the late reply, I’ve been busy with the ERC-4337 launch and ethdenver).

I think the order of the checks goes against how users perceive key rotation, and opens attack vectors (as I [suggested](https://github.com/eth-infinitism/account-abstraction/issues/188#issuecomment-1412628298) in the original issue). If the account already has code, it may have also rotated its signing key and no longer wishes to accept the old key that may have been leaked. But a person in possession of the old key can generate a counterfactual signature for it, bypassing the contract’s current sig check.

Line [109](https://github.com/ethereum/EIPs/blob/8fdf5706e53abacf5b60a92fcee49fe6977feee7/EIPS/eip-6492.md?plain=1#L109) says exactly the opposite, trying to keep counterfactual sigs valid after deployment. This constitutes an attack vector.

Example:

1. Alice deploys an account with Key1.
2. Bob steals Alice’s Key1 through a phishing scam.
3. Alice immediately realizes her mistake, rotates her account’s key to Key2 and revokes Key1.
4. Alice goes on with her life, happy about her decision to use a SCW, which made it possible to stop Bob’s attack.
5. Bob signs a counterfactual permit with the revoked Key1, stealing Alice’s tokens (from ERC-20 contracts that use EIP-6492 for the signature check).
6. Bob logs into OpenSea by signing with Key1 (if OpenSea uses EIP-6492 for offchain signature verification) and performs actions on her behalf.

The order of the checks makes it impossible for Alice to revoke her old key, which is one of the primary benefits of account abstraction.

The behavior is also inconsistent.  The account’s first key always remains valid and cannot be revoked, but the 2nd key can be revoked.  If we wanted old keys to remain valid forever, we would have to do this for all the keys, not just the first one.

Given that the current order causes non-intuitive UX (not being able to revoke the first key but being able to revoke the second), and that it opens an attack vector, what benefit does it bring that makes this trade-off worthwhile?  Are there situations where the user decides to revoke the old key from the account but still wants it to be valid for signing messages?

---

**dror** (2023-03-11):

Afaik, the comment should be fixed to match the implementation:

In case a magic exists but the code is already deployed, it ignores the initcode (since you can’t deploy twice) but still use isValidSignature

Also, the eip implementation differ quite a lot from the GitHub version

---

**Ivshti** (2023-03-11):

[@yoavw](/u/yoavw) this is a misunderstanding, and perhaps the EIP should make it more clear. Counterfactual format signatures remain valid in terms of their format, but they still get validated **against the deployed contract if there is one**, which means that old signatures will get invalidated upon key rotation regardless of whether they’re in the 6492 wrap format or 1271. So this whole thing is a moot point, but apparently it’s not clear from the EIP text.

From the implementation

```auto
    uint contractCodeLen = address(_signer).code.length;
    bytes memory sigToValidate;
    // The order here is striclty defined in https://eips.ethereum.org/EIPS/eip-6492
    // - ERC-6492 suffix check and verification first, while being permissive in case the contract is already deployed; if the contract is deployed we will check the sig against the deployed version, this allows 6492 signatures to still be validated while taking into account potential key rotation
    // - ERC-1271 verification if there's contract code
    // - finally, ecrecover
    bool isCounterfactual = bytes32(_signature[_signature.length-32:_signature.length]) == ERC6492_DETECTION_SUFFIX;
    if (isCounterfactual) {
      address create2Factory;
      bytes memory factoryCalldata;
      (create2Factory, factoryCalldata, sigToValidate) = abi.decode(_signature[0:_signature.length-32], (address, bytes, bytes));

      if (contractCodeLen == 0) {
        (bool success, bytes memory err) = create2Factory.call(factoryCalldata);
        if (!success) revert ERC6492DeployFailed(err);
      }
    } else {
      sigToValidate = _signature;
    }

    // Try ERC-1271 verification
    if (isCounterfactual || contractCodeLen > 0) {
      try IERC1271Wallet(_signer).isValidSignature(_hash, sigToValidate) returns (bytes4 magicValue) {
        bool isValid = magicValue == ERC1271_SUCCESS;
```

In fact, the issue that you’re mentioning isn’t even possible with any implementation, because you can’t “delete” the original contract and deploy the initial version on the same address.

This is covered in security considerations:

> It must be noted that contract accounts can dynamically change their methods of authentication. This issue is mitigated by design in this EIP - even when validating counterfactual signatures, if the contract is already deployed, we will still call it,

---

Hey [@dror](/u/dror) which GitHub version are you referring to? If it’s signature-validator, then the logic is absolutely the same - the implementation there doesn’t need the revert hacks because it’s off-chain (see security considerations), but the order and logic is absolutely identical. This can be tested by copy/pasting the bytecode from the reference implementation - all tests will pass as well.

---

**dror** (2023-03-12):

Right, they seem to match. the only problem was the comment that yoav described.

About the code in the ERC: it isn’t executable as it is, at least for small issue:  it truncate to `length-4` instead be `length-32`.

Maybe should use the actual tested code from the supporting library - or change the code to a “pseudo-python code”, which is usually shorter, and never expected to be executable…


*(32 more replies not shown)*
