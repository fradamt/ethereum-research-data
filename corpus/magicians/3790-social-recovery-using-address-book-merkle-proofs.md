---
source: magicians
topic_id: 3790
title: Social recovery using address book merkle proofs
author: miguelmota
date: "2019-11-21"
category: Web > Wallets
tags: [wallet, recovery, cba]
url: https://ethereum-magicians.org/t/social-recovery-using-address-book-merkle-proofs/3790
views: 4474
likes: 27
posts_count: 37
---

# Social recovery using address book merkle proofs

Not sure if this has been discussed before but the idea is that the contract-based account owner (Alice) can generate a merkle root based on her address book list so when Alice loses her management keys to the account contract, she can have n of m address book peer signatures submitted to set a new management key owned by Alice.

The merkle root is stored in the account contract and no other information about the address book list is required or stored on-chain. Alice selects a subset of trusted peers from her address book, generates the merkle root with the addresses as tree leaves, and sets the root on-chain. The address list used can be encrypted and emailed to her since she’ll need it when it’s time to recover the account.

Let’s say the address book list she used has the addresses of Bob, Charlie, Dave, Eve, and Frank, and requirs 2 of n signatures to set a new management key.

1. Alice loses her management keys and asks Eve to help her recover her account.
2. Alice gives Eve a newly generated address she controls and Eve takes a hash of the public address and signs the hash with her private key corresponding to the public address that Alice has stored for Eve in Alice’s address book.
3. Alice takes Eve’s signature and generates a merkle proof using her trusted peer address book list and Eve’s address as the leaf.
4. Alice submits the signature, data, and proof to her contract. The contract verifies that Eve is indeed part of the stored merkle proof and the submission is recorded in a mapping.
5. Alice then asks Bob to help her recover the account. Bob signs the hash of the new address and Alice submits the same pieces of data to the contract.
6. The contract verifies that Bob is part of the stored merkle proof, and then checks if the threshold has been met.
7. If the signatures required threshold has been met, then it verifies that all the signers agreed on the same new management key address.
8. If that succeeds, then the new management key is set and Alice can access her contract-based account again.

To demonstrate, here’s a rough proof-of-concept contract in Solidity:

```auto
pragma solidity ^0.5.2;

import './ECDSA.sol';
import './MerkleProof.sol';

contract Account {
  using ECDSA for *;
  using MerkleProof for *;

  address public owner;
  bytes32 public recoveryRoot;
  uint256 public sigsRequired;
  uint256 public seq;
  mapping (uint256 => address) sigs;

  modifier isOwner {
    require(msg.sender == owner, "Invalid sender");
    _;
  }

  constructor() public {
    owner = msg.sender;
    sigsRequired = 1;
  }

  function setOwner(address newOwner) external isOwner {
    owner = newOwner;
  }

  function setRecoveryRoot(bytes32 root) external isOwner {
    recoveryRoot = root;
  }

  function setSigsRequired(uint256 num) external isOwner {
    sigsRequired = num;
  }

  function recover(bytes32[] memory proof, bytes memory signature, address newOwner) public {
    bytes32 hash = keccak256(abi.encodePacked(newOwner));

    address recoveryKey = hash.toEthSignedMessageHash().recover(signature);
    bytes32 leaf = keccak256(abi.encodePacked(recoveryKey));
    require(proof.verify(recoveryRoot, leaf), "Invalid proof");
    sigs[seq] = newOwner;
    seq++;

    if (seq == sigsRequired) {
      address proposedOwner;
      for (uint8 i = 0; i  0 && proposedOwner != sigs[i]) {
          revert("Invalid new owner");
        }

        proposedOwner = sigs[i];
      }

      owner = proposedOwner;
      seq = 0;
    }
  }
}
```

The test would go as follows (pseudocode):

```auto
const addressBook = [Bob, Charlie, Dave, Eve, Frank]

const leaves = addressBook.map(x => keccak256(x)).sort()
const tree = new MerkleTree(leaves, keccak256)

const root = tree.getRoot()
await contract.setRecoveryRoot(root)
await contract.setSigsRequired(2)

const hash = keccak256(AliceNewKey)

const EveSig = web3.eth.sign(hash, Eve)
const EveProof = tree.getProof(keccak256(Eve))
await contract.recover(EveProof, EveSig, AliceNewKey)

const BobSig = web3.eth.sign(hash, Bob)
const BobProof = tree.getProof(keccak256(Bob))
await contract.recover(BobProof, BobSig, AliceNewKey)

assert.equal(await contract.owner.call(), AliceNewKey)
```

Working example code is on [github](https://github.com/miguelmota/solidity-social-recovery).

Things to note:

1. A benefit of this method is that it doesn’t require pre-approval of your address list beforehand, so there is no awkward UX issues, and recovery is as simple as asking the peers to sign a hash of a public address, which then you or a relayer can submit onchain.
2. Address book list is never exposed until it’s time for recovery, then the senders will of course be exposed.
3. Verifying merkle proof on-chain is expensive but recovery is something that should happen infrequently so this is fine.
4. To make it more secure, a timelock period can be initiated after the threshold is met to allow the owner to cancel the recovery and set a new merkle root in the case the peers collude which prevents them from immediately setting the new management. A recommended number would be to require at least 2 peers and 1 hardware device so in the case the peers collude they still need the hardware device signature, and in the case the hardware device is compromised then the peer signatures are still required. The contract can maintain two merkle roots, one consisting of friends and family and one consisting of hardware device keys, both with their own thresholds.
5. The address book can be maintained in decentralized fashion, such as using 3Box’s private storage, making the user’s address book be portable.
6. Instead of addreses, using ENS names can also work by resolving the name onchain when checking the recovered signer.

Would like to open up the discussion and hear what you guys think about all this. Thanks!

## Replies

**johba** (2019-11-22):

great summary.

how would you make sure that the address that you used to create the merkle tree does not become outdated? (my friend lost his wallet, or got hacked)

little remark:

> Verifying merkle proof on-chain is expensive but recovery is something that should happen infrequently so this is fine.

actually very cheap, and will become very cheap with latest gas schedule changes in Ethereum.

---

**miguelmota** (2019-11-22):

> how would you make sure that the address that you used to create the merkle tree does not become outdated? (my friend lost his wallet, or got hacked)

Great question. If you know your friends wallet got compromised, you can remove him from the address book list and recompute the merkle root and store the new root in the account contract to prevent the attacker from starting the recovery process with the compromised account.

To prevent outdated addresses from being utilized, you can periodically recompute and submit an updated merkle root using up-to-date addresses or use ENS names instead of hard coded address as the merkle leaves and resolve ENS to addresses in the recovery method.

> actually very cheap, and will become very cheap with latest gas schedule changes in Ethereum.

Nice, that’s very cool

---

**johba** (2019-11-24):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/0ea827/48.png) miguelmota:

> To prevent outdated addresses from being utilized, you can periodically recompute and submit an updated merkle root using up-to-date addresses or use ENS names instead of hard coded address as the merkle leaves and resolve ENS to addresses in the recovery method.

if the ENS can be resolved on chain, maybe encoding the ENS name into the tree would suffice.

There is a follow-on problem using ENS thought:

what if the address is not an key, but a contract? like an identity contract?

---

**miguelmota** (2019-11-24):

> what if the address is not an key, but a contract? like an identity contract?

Since contracts can’t generate signatures therefore ecrecover won’t work if the address is a contract, then the contract-based account needs to use the [EIP1271](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1271.md) standard to verify contract signatures. During the recovery process, the account contract checks if there’s bytecode stored at the leaf address. If there is, then it is a contract and not an externally owned account so it verifies the signature using `isValidSignature( data, signature)` on the friend’s contract. Authereum, Dapper wallet, 0x, and a few others are already using EIP1271 to verify signatures where the "recovered addres"s is a contract address.

---

**3esmit** (2019-11-26):

Hey [@miguelmota](/u/miguelmota), very nice.

I have also a working solution with the same concept, but I also introduced user data hash and other important (but optional) security features.

It’s fully documented here in the sol:


      [github.com](https://github.com/status-im/account-contracts/blob/develop/contracts/account/MultisigRecovery.sol)




####

```sol
pragma solidity >=0.5.0 <0.6.0;

import "../cryptography/MerkleProof.sol";
import "../cryptography/ECDSA.sol";
import "../token/ERC20Token.sol";

/**
 * @notice Select privately other accounts that will allow the execution of actions
 * @author Ricardo Guilherme Schmidt (Status Research & Development GmbH)
 */
contract MultisigRecovery {

    /**
     * Controller of Recovery
     */
    address private identity;

    /** # User Secret Data Hash
     * Hash of Semi-private information, such as a "randomly ordered personal information + secret answer", or a hash of user biometric data.
     * The secret should only be revaled together with `execute`, which requires changing the secret at every execution.
```

  This file has been truncated. [show original](https://github.com/status-im/account-contracts/blob/develop/contracts/account/MultisigRecovery.sol)








This is a WIP/Research repository, which I am working to build account contracts for Status.im, and for future interoperability between I am writing an ERC to standardize the social recovery feature.

The contract features a Secret Multisig system, which is self contained and should be used as a recovery actor in a account contract, instead of extending this into user account contract, so it’s behavior would be always consistent.

After merkle tree (or part of it) is revealed, a new merkle root needs to be defined, so every recovery requires a new recovery setup.

The user datahash is a hash of hash of user private data, which could be bio-metrics or derived from user profile data, and will be used to secure the recovery process and obfuscate the threshold.

---

**axe** (2019-11-29):

Hi [@3esmit](/u/3esmit),

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> After merkle tree (or part of it) is revealed, a new merkle root needs to be defined, so every recovery requires a new recovery setup.

There is another reason for this beside privacy?

---

**3esmit** (2019-11-29):

Yes, the point of using a merkle tree was initially privacy, and when a recovery is done some of this privacy is lost, so it should change the list.

However I see that I should instead disable recovery after user successfully recovered, and after that suggest a new recovery in the wallet UI.

---

**axe** (2019-11-29):

I think suggesting is a good option, but changing the Merkle tree should not be mandatory.

Thanks

---

**3esmit** (2019-11-29):

I think that security should be mandatory, especially if possible.

It’s possible to reuse the same exact list of friends as before, but it would change the merkle root because the way I designed it is that the userDataHash is used also in the merkle tree to obfuscate the leafs.

The semi secret stores the friend list and the user private secret, and the same seeds can be reused as many times as wanted by salting the user private secret, thats why its hashed multiple times. Therefore the UI can do all this on behind without the user even have to know.

---

**miguelmota** (2019-12-02):

This is great! Yes a bare-bones simple standard around this social recovery method would be very beneficial to anyone implementing contract-based accounts.

---

**miguelmota** (2019-12-02):

Do agree that it should be optional, though I could see a scenario where a malicious person might be less incentivized to attempt to steal a known peer’s device if it’s not certain that they are part of the same recovery merkle root again, so setting up a new root would be advantageous.

---

**axe** (2019-12-02):

Thanks for the context.

I don’t think that changing the addresses that allow recovery will improve directly the security. The userDataHash computed in the Merkle Tree will bring some obfuscation but fundamentally the security will have to be the security of the base addresses.

From what i saw in the code, you are defining the userDataHash as some kind of question / answer, and this will make it more transparent to UX, but can have a great utility for recovery. If is strong enough, as an seed phrase, maybe the addresses can be discarded. But in this setting there is no social recovery, just a personal one.

I’m talking about not change the addresses in the tree just for the potential functionality of a smart wallet (not a EOA) to help recovery a account. As is, a user smart wallet cannot be another user backup.

---

**axe** (2019-12-02):

I see that is better for privacy, but i fear that making mandatory is too opinionated, maybe this decision should be left to the wallet implementation.

But as [@3esmit](/u/3esmit) said, the wallet only have to change the userDataHash to get the same privacy in merkle tree.

---

**3esmit** (2019-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axe/48/14450_2.png) axe:

> If is strong enough, as an seed phrase, maybe the addresses can be discarded.

Using the secret alone is unsafe - as it should be easy to guess then its also easy to discover, and a totally different approach using a special commit-reveal scheme would be essential for protecting overruns, or if you suggest a seed phrase, then ECDSA should be used, in this case the recovery address can simply be hashed once, however this does not solve the problem of dealing with seed phrases or a single trusted party.

My main concerns in interoperability would be in the messaging of the recovery requests, I think that most wallets could have their own service/protocol for that, but that would break interoperability and decentralization, so it would be important for a common ground between wallets to exchange these requests.

We could leave this bridge open for now (everyone uses its own), and standardize as sub ERC-681  a`recovery request URI` and a `recovery authorization URI`, so if user is not reachable (using different bridge) within same wallet software, a recovery request URI could be sent by email (or whatever) and understood by other wallet, and produce a recovery authorization URI.

We can improve the common bridge later or seek for integration with other solutions such as wallet connect or universal logins, that are also solving the “device bridge problem”, which could be used for this purpose as well.

I am writing a detailed specification on this concept, including UX and interoperability mentioned above, and once I get all thats in my mind sorted out I’ll share here and we can have a call and start a EIP process.

---

**3esmit** (2019-12-07):

Submitted the `EIP 2429: Secret Multisig Recovery`

First draft is here: https://github.com/ethereum/EIPs/pull/2429

There is still a lot to do, and my own solidity file is not compatible with this standard, as while I was specifying it, I matured it.

I used this thread as discussion because we were already discussing this problem-solution here, or maybe what I specified dont fits here, if thats the case let me know and I create a dedicated topic to discussing the solution of using merkle trees + user secret and here would be other thing.

---

**axe** (2019-12-26):

Im reading the draft and looks good, just a couple of questions:

Should the recovery be limited to only setting a new Owner address? Only letting one operation could make the system more simple and easy to implement.

If the only operation is setting a new Owner, then when the user start the recovery process, the user_secret_data should be sign with a new address that will take ownership of the wallet. And also be passed as a parameter. The contract validade this step in the recovery logic.

The user in the configuration step should also define a secret_to_peer hash, that he reveal to the peers list (address_list) to avoid some types of social engineering attacks.

This new variable should be also change when the recovery process is completed.

I don’t see the utility of applying a nonce in this context.

Cheers

---

**3esmit** (2019-12-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axe/48/14450_2.png) axe:

> Should the recovery be limited to only setting a new Owner address? Only letting one operation could make the system more simple and easy to implement.

In order to this recovery option work with any contract, is useful that any call can be made.

It’s more simple for us to don’t define how recovery is called, and instead just say that recovery can call anything, then it’s role of the recoverable contract to provide a special access to recover the contract.

In order for a recovery to work, the wallet/UI must know how to perform it, and this includes the call the recovery contract needs to make.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axe/48/14450_2.png) axe:

> I don’t see the utility of applying a nonce in this context.

Nonces are used to aid reuse of same secret answer, but are not required in the public reveals, and should be in recovery contract. If not, the secret answer cannot be reused.

Nonces are simply the count of recoveries, and this cannot be hidden (all full nodes/etherscan can count it), and its useful to have it handy.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axe/48/14450_2.png) axe:

> The user in the configuration step should also define a secret_to_peer hash, that he reveal to the peers list (address_list) to avoid some types of social engineering attacks.

The proposal does that, and uses the same secret to all to simplify things, but the user_data_hash is the hash of hash_to_peer (used to be called in standard `proofpub_hash`), which is the hash of the hash_to_execute (used to be called `seedpub_hash`), which is the hash of private_hash (never revealed) with recovery contract address and nonce, and private hash is the hash of the user secret answer.

Based on your feedback I renamed the variables and added details to why the nonces are there.

See [ERC: Secret Multisig Recovery by 3esmit · Pull Request #2429 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2429/commits/ea6efea6ae51cd4185bf2b795f56920e91a76dca)

If you think that using double hash for the purpose of “secret_to_peer” is bad, please explain, and if there is problems with it, we can use something else, like what you suggested (an additional secret).

---

**axe** (2019-12-28):

I started one implementation based on the proposal:



      [github.com](https://github.com/shinra-corp/ERC2429/blob/master/contracts/RecoveryContract.sol)





####



```sol
pragma solidity >=0.6.0  The proposal does that, and uses the same secret to all to simplify things

Yes, is better maintain the same tree of hash, with one change.

The peers should sign the operation to execute also with chainID so there is no funny stuff as replay the signatures in other networks. (bumping solidity to version 0.5.13).

I only compile the code and didn’t tests in anyway.

Cheers

---

**3esmit** (2019-12-28):

Hey, thanks for the suggestion and implementation.

Regarding signatures replay protection, I am using the contract address in the hash composition to prevent this kind of problems, it’s very unlikely (and not recommended) to reuse smart contract addresses in different chains.

However, the problem may occur in case of a chain split. I see that EIP712 also contains a chain ID, but it needs to be initialized by the contract, so it wont prevent the problem at all.

EIP-1344 gives access to chain id from EVM, which I’m unsure how it would behave in a chain split, but seems the way to solve this problem.

I didnt used EIP-1344 because it wasn’t available at the time Secret Multisig Recovery was designed, but it seems an good protection to include… I will see where is the best place to put the chainID in the hashing schema, but probably it should be in all signatures.

---

**3esmit** (2019-12-28):

[@axe](/u/axe) You got it right using chainID around peerHash, but it dont needs to be verified in a leaf basis, it could be incorporated in the hash path of publicHash. We could make that, as publicHash depends on peerHash, the peerHash could depend on chainID and executeHash, which would tie all to only sign for the correct chain, because the peerHash will *“never”* match if the chainID returns incorrect.

However this might lead to an problem, because in case of a chain split, the recovery contract would only work in the chain that didn’t changed the id - this is also true for how you implemented chainID.

So, chainID only should be checked against signatures, so perhaps we could start using EIP-712 with the new chainID from EVM, I will check that. For now we are using EIP-191 with validator address as the recovery_contract and now also using chain ID inside of the application parameters.

I also noticed that, due the lack of information on the EIP, you implemented signature checking in your own way. So I also added this missing part of the specification on how the messages to be signed should be constructed.

I updated the account-contracts to match current version of ERC-2429…

Some changes I am considering:

- Reorder parameters of the signature to order them by their context,
- Enable bigger thresholds by counting secretCall authorizations on advance, or by enabling multiple interations on execute


*(16 more replies not shown)*
