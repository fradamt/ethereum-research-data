---
source: magicians
topic_id: 22755
title: "ERC-7878: Bequeathable Tokens. A standard to allow tokens to be inherited after the owner's death"
author: Wamith
date: "2025-02-02"
category: ERCs
tags: [nft, token, erc-721]
url: https://ethereum-magicians.org/t/erc-7878-bequeathable-tokens-a-standard-to-allow-tokens-to-be-inherited-after-the-owners-death/22755
views: 307
likes: 8
posts_count: 9
---

# ERC-7878: Bequeathable Tokens. A standard to allow tokens to be inherited after the owner's death

We developed a “Bequeathable” property contract at ScanSan Properties to enable the transfer of ownership after a person’s death, as we found no existing ERC standards that met this need. We are now sharing our solution with the crypto community for feedback and potential adoption as a new standard.

## Abstract

This EIP proposes a standard interface for contracts to allow tokens to be inherited after the owner’s death. The interface allows token owners to set up a Will and designate executors to enable the transfer of tokens to inheritors after a specified waiting period.

## Motivation

Crypto Tokens in general and NFTs in particular are starting to be used to tokenise real-world assets. In order for them to be adopted by the main stream finance world, there needs to be a way to inherit these tokens after the owner has passed away. Currently, there is no standardised way for token holders to pass on their digital assets in the event of their death.

This EIP aims to solve this problem by providing a standard interface for “bequeathable” tokens, allowing for a secure and transparent process of token inheritance.

In designing this interface we have tried to follow the real world process of Will creation and execution.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

Every compliant contract MUST implement the `Bequeathable` interface:

```solidity
/// @title EIP-xxxx Bequeathable tokens
/// @dev See https://eips.ethereum.org/EIPS/eip-xxxx

pragma solidity ^0.8.0;

/**
 * @notice Bequeathable interface
 */

interface Bequeathable {

   /**
    * @notice                 The core struct for recording Wills
    * @dev     Will           A struct that keeps track of each owner's Will. One Will per owner
    * @param   executors      An array of addresses that can set an obituary and then subsequently perform the transfer to the inheritor
    * @dev                    It maybe advisable to limit the number of executors for gas efficiency
    * @param   moratoriumTTL  The time that the moratorium must remain in place before the transfer can happen. This is a safety buffer to allow for any other executors to object. We recommend at least a month (60*60*24*30 = 2592000)
    * @param   inheritor      The address that will inherit these tokens, the inheritor is only set at the time of raising the obituary
    * @param   obituaryStart  The time that obituary was announced and moratorium started
    */
   struct Will {
      address[] executors;
      uint256 moratoriumTTL;
      address inheritor;
      uint256 obituaryStart;
   }

   /**
    * @notice              Announce the owner's tokens are to be inherited
    * @dev                 Emitted by `announceObit`
    * @param   owner       The original owner of the tokens
    * @param   inheritor   The address of the wallet that will inherit the tokens once the moratoriumTTL time has passed
    */
   event ObituaryStarted(address indexed owner, address indexed inheritor);

   /**
    * @notice               Announce the obituary (and moratorium) for the owner has been cancelled, as well as who cancelled it
    * @dev                  Emitted by `cancelObit`
    * @param   owner        The original owner of the tokens
    * @param   cancelledBy  The address that triggered this cancellation. This can be the owner or any of the inheritors
    */
   event ObituaryCancelled(address indexed owner, address indexed cancelledBy);

   /**
    * @notice                 A token owner can set a Will and names one or more executors who are able to transfer their tokens after their death
    * @dev                    Although more than one executor address can be set, only one is required to start the process and then do the transfer
    * @dev                    Subsequent calls to this function should overwrite any existing Will
    * @param   executors      An array of executors eg legal council, spouse, child 1, child 2 etc..
    * @param   moratoriumTTL  The time that must pass (in seconds) from when the obituary is announced to when the inheritance transfer can take place
    * @dev                    The moratoriumTTL is a safety buffer time frame that allows for any intervention before the tokens get transferred
    */
   function setWill(address[] memory executors, uint256 moratoriumTTL) external;

   /**
    * @notice                  Get the details of a Will if set
    * @dev                     This is a way for the owner to confirm that they have correctly set their Will
    * @param    owner          The current owner of the tokens
    * @return   executors      A list of all the executors for this owners will
    * @return   moratoriumTTL  The length of time (in seconds) that must elapse after calling announceObit before the actual transfer can happen
    */
   function getWill(address owner) external view returns (address[] memory executors, uint256 moratoriumTTL);

   /**
    * @notice              Start the Obituary process, by announcing it and declaring who is the intended inheritor
    * @param   owner       The current owner of the tokens
    * @param   inheritor   The address of the owner to be
    */
   function announceObit(address owner, address inheritor) external;

   /**
    * @notice          Cancel the Obituary that has been previously announced. Can be called by any of the executors (or the owner if still around)
    * @param   owner   The original owner of the tokens
    */
   function cancelObit(address owner) external;

   /**
    * @notice                   Get the designated inheritor and how much time is left before the moratoriumTTL is satisfied
    * @param    owner           The current owner of the tokens
    * @return   inheritor       The named inheritor when the obituary was announced
    * @return   moratoriumTTL   The time left for the moratoriumTTL before the transfer can be done
    * @dev                      A minus figure for moratoriumTTL indicates that the wait time has elapsed and the tokens can be bequeathed
    */
   function getObit(address owner) external view returns (address inheritor, int256 moratoriumTTL);

   /**
    * @notice         Bequeath ie transfer the tokens to the previously declared inheritor
    * @param   owner  The original owner of the tokens
    * @dev            The transfer should happen to the inheritor address when `announceObit` was called
    */
   function bequeath(address owner) external;

}
```

### Will Structure

The `Will` struct MUST contain:

- executors: An array of addresses authorized to manage the Will.
- moratoriumTTL: The time that must elapse before the token transfer can occur.
- inheritor: The address designated to receive the tokens.
- obituaryStart: The timestamp when the obituary was announced and the moratorium started.

### Functions

1. setWill: Allows a token owner to set up or update their Will.
2. getWill: Returns the current Will details for a given owner.
3. announceObit: Initiates the inheritance process by an executor.
4. cancelObit: Cancels an active obituary process.
5. getObit: Retrieves the current obituary status.
6. bequeath: Transfers tokens to the inheritor after the waiting period.

### Events

1. ObituaryStarted: Emitted when an obituary is announced.
2. ObituaryCancelled: Emitted when an obituary is cancelled.

## Rationale

The standard follows what currently happens in real life when preparing and executing a Will.

1. An owner writes a Will and in doing so names the executor(s) of their Will
2. Upon passing away, the executor will announce the Obituary
3. The Will is read and the inheritors are identified
4. The transfer of ownership is executed according to the wishes of the Will

However, real life is not always as straight forward as this. Conflicts happen all the time. To handle this situation and to keep the interface simple, we added the ability to cancel the Obituary by ANY of the executors. In this way, if there is any conflict, it can be challenged out in the courts and once the matter is settled, the Obituary process can start again.

Again to keep the interface clean, all the tokens get transferred to one address. It is then that person’s responsibility to execute any further transfers.

## Backwards Compatibility

This EIP is compatible with existing token standards like ERC-20, ERC-721 and ERC-1155. It can be implemented alongside these standards without affecting their core functionality.

## Security Considerations

Implementers should carefully consider access control mechanisms to ensure that only authorized parties can execute Will-related functions.

The moratoriumTTL should be set to a reasonable duration to allow for potential disputes or corrections. We recommend at least 30 days, especially for tokens that are of high value.  It limits the potential damage in scenarios such as the obituray process being triggered by a bad actor who has taken over one of the executor wallets.

## Replies

**wisecameron** (2025-02-14):

This is an interesting concept and it’s definitely a real problem.  The approach you’ve taken also makes a lot of sense as a holistic solution that does consider the nuances of the wider real-world context.

In terms of practical application I think the biggest hindrance is going to be the fact that the interface is pretty heavy, and users might not be inclined to utilize it on a token-by-token basis.  I think it might make more sense as a feature for custodial wallets, however I also think that if this is something the community wants, your approach is the way to do it.

---

**Wamith** (2025-02-18):

I agree that having this functionality in the wallet would be better. However, we at Scansan have no control over the wallet providers and couldn’t wait around for them to find a solution that worked for us.

Scansan does however control the smart contract and so we built this into our real-estate tokens. Realising we’re not the only ones likely to be facing this problem, it made sense to give it back to the community and agree a common standard.

---

**wisecameron** (2025-02-18):

That’s super cool that you guys have already implemented it in a practical setting – it does certainly make sense for RWA assets.

---

**Signordev** (2025-06-14):

Glad to see ERC-7878 tackling crypto inheritance! This standard brings crucial features:

- On-chain Will creation
- Executor-based inheritance
- Moratorium periods for safety
- Standardized interface for adoption

Solid initiative for a real problem! ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=12)

I spotted some challenges while reviewing the specification:

ERC-7878 Challenges:

• Single executor can trigger inheritance

• No asset custody mechanism

• Missing dispute resolution

• No death verification

Solution:

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Multi-executor consensus (min 2)

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Full asset custody (ETH/ERC20/721/1155)

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Oracle death verification (none yet)

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) 3-day challenge period

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Realtime notifications

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Percentage-based distribution

---

**Wamith** (2025-07-13):

Sorry for the late reply (I was on holiday)

Firstly, thank you for your comments. Glad that you agree this is a real problem.

You make some valuable suggestions, here is a response for each of your points:

**Multi-executor consensus:**

It make sense for you to want to have more than one person involved in this part of the process. However, the way we’ve set up the logic is that actually ALL the executors must agree before the transfer can happen. At any point (during the moratorium period) any of the executors can cancel the Obituary.  It’s just the initial trigger that is done by one of the executors.

As well as keeping this simple, this allows for flexibility and (hopefully) greater adoption as not everyone has more than one executor - nor do we want to force people into having multiple executors. It is also gas efficient.

**Full asset custody:**

I think by this you mean the ability to work with the types you mention (ETH/ERC20/721/1155). If that’s the case, it does; the proposal does mention these ([ERC-7878: Bequeathable Contracts](https://eips.ethereum.org/EIPS/eip-7878)) but we’ve also written it as a standalone so it can be used with future types as well.

**Missing Dispute Resolution:**

We had many a discussion about this when writing the proposal. We ended up adopting the simple approach by allowing any of the executors to put a pause on proceedings until they all agree. This forces the dispute to happen offline (possibly in the law courts) and only when consensus is reached can any transfer happen.

We recommend a 30 day moratorium period (which is longer than your 3 day proposal), but we deliberately left this open for the implementor/owner. Some assets will be very valuable so a long time period makes sense, other assets will be throw away, so possibly a few hours is more than enough for them to be transferred - so we left it flexible for the owner and contract write to decide.

**Realtime notifications:**

There is an ‘ObituaryStarted’ event in the standard. Anyone listening to these events should be able to then email/contact the relevant parties in near time.

**Oracle death verification:**

There is no agreed upon, widely available, trusted in all territories oracle at the moment - maybe that should be the next standard we work on.

However, the contract implementor can choose to make a call to an oracle when the `announceObit` function is called and return an error if they dont get a satisfactory response from the oracle.

There is no reason why this cant be added to the standard in the future.

**Percentage-based distribution:**

Not everyone wants to distribute their wealth as a percentage. eg someone may want a million pounds to go to their favourite charity and then anything left to be divided equally to their children. A purely percentage based system could not support this.

Again, to keep things simple and flexible, it was much easier to agree upon a trusted wallet to transfer the assets to and that wallet owner can divide up the sums in any way the original owner wanted.

Hopefully I’ve addressed all your points.

Please let me know if I’ve missed any or misunderstood your comments.

---

**wjmelements** (2025-08-25):

I think Account Abstraction should handle this. That would be a better solution because it would work for all assets, without requiring approval for each token.

---

**zergity** (2025-08-29):

Yes, and also because there is so many non-token thing that can be inherited, like: roles, finance positions, unlockable assets, etc.

---

**Wamith** (2025-08-30):

I agree that doing this at the account/wallet level would be better.

But we have no control over that and couldn’t wait for them to come up with a solution

