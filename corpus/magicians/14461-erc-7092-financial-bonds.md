---
source: magicians
topic_id: 14461
title: "ERC-7092: Financial Bonds"
author: samsay
date: "2023-05-27"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7092-financial-bonds/14461
views: 5399
likes: 20
posts_count: 42
---

# ERC-7092: Financial Bonds

Implementing a standard API for Financial Bonds. This standard allows Institutions, Corporations, Municipalities, Decentralized Exchanges and Individuals to issue bonds in the Primary Market, to exchange bonds in the Secondary Market, and to redeem bonds when they mature.

The standard defines all the basic properties needed to model a financial bond, such as the issue date, the maturity date, the coupon rate, the principal, and the currency.

The standard could then be used to create bonds with embedded options such as CALLABLE bonds, PUTTABLE bonds, and CONVERTIBLE bonds.

Link to the draft EIP:   [Financial bonds - ERC-7092](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7092.md)

https://github.com/ethereum/ERCs/pull/279

## Replies

**xinbenlv** (2023-05-29):

Thank you for the EIP. This seems interesting!

```
/**
* @notice Returns the bond maturity date, i.e, the date when the pricipal is repaid. This is a Unix Timestamp like the one returned by block.timestamp
*         The maturityDate MUST be less than the issueDate
*/
function maturityDate() external view returns(uint256);
```

Should it be “greater than” rather than “~~less than~~” here?

---

**samsay** (2023-05-30):

Hello [@xinbenlv](/u/xinbenlv)

Thank you for the comment.

You’re right, it should be “greater than”, rather than “less than”. Going to correct it right now.

---

**ToDestiny** (2023-06-01):

This is really great! Let’s disrupt the TradFi and give back power to the people!

---

**samsay** (2023-06-01):

[@ToDestiny](/u/todestiny)

Yes, By proposing Tokenized bonds, more people could be interested in the Bond Market. And since smart contracts will replace intermediaries, people will have more power on their bonds, they can manage their bonds by their own.

---

**ownerlessinc** (2023-09-22):

I’m very well inclined to help build this ERC!!

Is there an active repo open for contribution?

---

**samsay** (2023-09-25):

Hello [@ownerlessinc](/u/ownerlessinc)

Thank you for your interest.

Could you send me a message on LinkedIn ? I will let you know how you can contribute to the ERC (give you access to the repo)

Here is my LinkedIn

https://www.linkedin.com/in/samuel-ongala-edoumou/

---

**SamWilsn** (2023-10-30):

I would recommend putting the optional functions (eg. `currencyOfCoupon`, `couponType`, etc) into their own interfaces. Even if you don’t explicitly support [ERC-165](https://eips.ethereum.org/EIPS/eip-165) (which do I recommend you do), putting them into interfaces will make it easier for anyone who wants to use ERC-165.

---

**samsay** (2023-10-31):

Hello [@SamWilsn](/u/samwilsn),

Supporting ERC-165 was one of the option I thought about for ERC-7092. I abandoned that idea because these functions are optional. But now that you have pointed it out I think using the interfaces for optional functions is a good option that  need to be considered.

![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**samsay** (2023-11-01):

ERC-7092 now supports [ERC-165](https://eips.ethereum.org/EIPS/eip-165)

Thank you [@SamWilsn](/u/samwilsn) for your suggestion.

---

**Mani-T** (2023-11-01):

This is a step in the right direction for simplifying the tokenization of bonds.

---

**samsay** (2023-11-07):

Thank you [@Mani-T](/u/mani-t)

We tried to make the standard as close as to what in done in TradFi in order to let Issuers, Investors and Institutions that issue Bonds to move to Tokenize bonds without significant disruption, but also to allow people who cannot invest in the bond Market to participate, thanks to fractionalization that lowers the entry barrier for retail investors.

---

**BorisB** (2023-12-03):

Hello [@samsay](/u/samsay)

Could you please elaborate on _spender, in traditional finance that would be the buyer/lender ?

Thank you

---

**samsay** (2023-12-03):

Hello [@BorisB](/u/borisb),

In traditional finance, bonds are managed by intermediaries and orders are passed and settled by broker dealers or OTC. As a consequence, `_spender` in the traditional fiance are usually those intermediaries that are approved to spend bonds on behalf of bondholders.

The ERC-7092 has the ability to remove those intermediaries, and allows bonds to be traded from one investor to another directly, or to use the traditional schema with intermediaries replaced by smart contracts. Therefore, the `_spender` could be either the `investor` who holds the bond, or the smart contract that has been `approved` by the bondholder to spend their bonds.

If we consider a case a traditional institution would like to issue bonds on behalf of their clients (`issuers`) through the ERC-7092, they may consider the following steps:

- Create the Bond Contract, which implements the ERC-7092 standard interface
- Create a Bank Contract, which MUST be considered as the core contract where all transactions should take place. This contract is responsible for all the work done by broker dealers and Investment Banks. It MUST define an array of MANAGERS in charge of triggering some actions like calling the issueBonds function when the total issue size is reached, or calling the redeemBonds function when bonds Mature. Investors MUST approve the Bank Contract to Transfer their bonds in case bonds are traded in the secondary market. In that case, the _spender is still the bondholder (investor), but the transfer of bonds can be done only by the Bank Contract that has been approved by the holder.

There could be a case where bonds need to be listed on a bond `exchange`. Listing bonds may require the `_spender` or `investor` to transfer their bonds to the `exchange` which then becomes the `_spender` in charge of selling bonds on behalf of bondholder.

Another case is when bonds are traded from one investor to another without any intermediary. In that case, the `_spender` is always the `investor` or `bond owner`.

In short, what the bond `_spender` should be, depends on how project owners want bonds to be managed.

---

**BorisB** (2023-12-04):

Hi [@samsay](/u/samsay)

Thank you for describing the potential use cases, that is very helpful.

Boris

---

**Atlas** (2024-01-26):

Thanks for all your work on this! I’ve been looking primarily at the IERC7092CrossChain portion for adaptation to our system, and have a concern about the destination address data type.

For support to more ecosystems, might it be better to use a bytes format in case a destination chain may require larger recipient addresses?

---

**samsay** (2024-01-28):

Hello [@Atlas](/u/atlas),

Thank you for your suggestion.

- The destination address in cross-chain functions is the address of the smart contract to interact with on the destination chain. Its type MUST be address as it is defined in the IERC-7092 interface.
- However if by destination address you meant the destination chain ID which is of type bytes32, this of course could have been expressed as bytes. But it seems like a bytes32 is more likely sufficient to store this parameter. For example

ChainLink uses uint64 to represent the destination chain ID (see here). We’ve already tested successfully the cross-chain transfer of bonds issued through ERC-7092 by using chainlink CCIP.
- Toposphere uses bytes32 to represent the destination chain ID (see here). Cross-chain functionalities not yet tested, but a complete application using ERC-7092 already deployed on their chain: Bonds issuance, bonds transfer, coupon payment, listing bonds on exchange, selling and buying bonds on exchange, unlisting bonds from exchange, updating bonds price on exchange, etc. (youtube video on Bonds issued and managed with ERC-7092).
- CryptoLink uses directly the destination chain ID like 1 for Ethereum Mainnet, 5 for Ethereum Goerli, 43113 for Avalanche testnet, etc. (see here). Working on it right now to test bonds management accros several chains

I confess that your suggestion is quite interesting, but using `bytes` instead of `bytes32` could lead to some issue if one refers to this [check here](https://ethereum.stackexchange.com/questions/11770/what-is-the-difference-between-bytes-and-bytes32)

![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**Atlas** (2024-01-28):

Hello [@samsay](/u/samsay),

Thanks for your reply, and the comment on the bytes, you’re right.

I was suggesting `destination address` and not `destination chain` - for example, if I were to transfer to Cardano recipient `addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4`

I have to admit that I have just begun to dig into the specifics of ERC, and I believe that it may not come into play where you need the recipient address on the destination chains, so I think my comment here might not apply as far as recipient wallets, apologies ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) but it may apply when sending requests to destination contracts, for example:

```auto
    function crossChainApprove(address _spender, uint256 _amount, bytes32 _destinationChainID, address _destinationContract) external returns(bool);
```

I believe that the `address` type may not be large enough for example on Cardano to address a destination contract?

---

**samsay** (2024-01-28):

Hello [@Atlas](/u/atlas),

Sure! the address type couldn’t be used to store large chains of characters like some cardano addresses.

However, if you look at what is being proposed through cross-chain protocols like chainlink, topos, cryptoLink, etc., you will realize that all the chains proposed are EVM compatible.

Of course, in case of non-EVM compatible destination chain, extra functions could be added on top of IERC-7092 to deal with address format on other blockchains. These functions will have same signature as the one defined in the IER-7092, only the `type` of the `destinationContract` should be adapted to fit the length on the destination chain.

---

**bumblefudge** (2024-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samsay/48/6130_2.png) samsay:

> Of course, in case of non-EVM compatible destination chain, extra functions could be added on top of IERC-7092 to deal with address format on other blockchains

sounds like a job for [CAIP-2](https://chainagnostic.org/CAIPs/caip-2)/[CAIP-10](https://chainagnostic.org/CAIPs/caip-10)?

---

**samsay** (2024-03-08):

sounds interesting.

Why that’s not been proposed as an EIP (on Ethereum) ?


*(21 more replies not shown)*
