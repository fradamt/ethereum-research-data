---
source: magicians
topic_id: 8691
title: "EIP-3475 : Multiple Callable Bonds Standard"
author: GrandGarcon
date: "2022-03-23"
category: EIPs
tags: [defi, bonds]
url: https://ethereum-magicians.org/t/eip-3475-multiple-callable-bonds-standard/8691
views: 5635
likes: 14
posts_count: 36
---

# EIP-3475 : Multiple Callable Bonds Standard

This standard proposes an generic interface  for creation , management of the financial  bonds  between issuers and redeeming parties  on blockchain , in a way which is :

- efficient to evaluate / modify the state throughout the lifecycle of the bonds .
- being (nearly*) independent of  off-chain data  for management of the issuance and redemption.
- and are Decentralized in  terms of creation / management vis a vis current alternatives.

## Why

Bonds have been one of the most  prominent fixed rate instruments by volume in the overall debt securities market of traditional markets . ([ref](https://en.wikipedia.org/wiki/Bond_market#cite_note-1)) .Majorly issued by  the world governments , so that  their stability  in returning is considered as a major factor for stability of the currency and monetary policy.

Similarly in DeFI , from major projects like [olympus DAO](https://app.olympusdao.finance/#/bonds/inverse) are issuing specific type of fixed rate bonds for LP tokens,  to more institution / Real World Finance Adoption like Societe Generale issuing bonds as guarantee for an loan to makerdao([here](https://forum.makerdao.com/t/security-tokens-refinancing-mip6-application-for-ofh-tokens/10605)) ,  bonds are going to be the next prominent asset class to grow adoption of defi after swaps and staking .

These instruments are divided into various classes , based on the nature of the bond redemption (Fixed rate or floating rate APY) , stability , etc , and each class the bonds are identified in terms of Nonce (id’s , serial number listing as explained in [BONDS | BOND MARKET | PRICES | RATES | Markets Insider](https://markets.businessinsider.com/bonds)

Apart from that , Generic bonds  minimally consist of following information :

- Debt metrics ( represented as supply) :

Active Supply : this is the current active debt obligation that has to be settled  by the current redeeming party .
- Redeemed Supply:  this supply corresponds to the amount of the given debt of the bond already redeemed
- Burned supply : consist of the part of the bond debt that is being cancelled / is being invalidated .

### Metadata information:

Info describing the information about the nature of classes , this includes the nonceInfoDescription , details concerning the

But this adoption in DeFI is lagged due to various factors , primarily factors being :

Lack of interoperability between the different bond markets :

- Inefficient : each bonds deployed (like LP’s) need the instantiation of factory of contracts which are dependent in order to do issuance and redemption of the bonds , this cause fragmentation of the liquidity pools and needs more gas fees for transferring & optimising liquidity , along with issues like ILP.
- offchain dependence  of the data for issuance / redemption of the bonds

In order to solve the issues , we have defined the data structure to store the state of the bonds in an gas and storage efficient way , along with the functions to maintain the lifecycle /transfer and redemption  of bonds.

## links

for reading further about the EIP standard check the review version [here](https://eips.ethereum.org/EIPS/eip-3475).

example of the minimal  implementation with tests are in the same repo, feel free to review and ask queries .

thanks

## Replies

**samsay** (2022-05-21):

It will be interesting to see how this standard based on the Blockchain allows to reduce the time of bond issuance, since in traditional finance, it can take more than a week for a bond to be issued. Also, removing all intermediaries which impact the cost of the bond would probably encourage investors.

---

**samsay** (2022-05-25):

On the EIP, the description of **Burn** seems not to be correct

**burn(address from, uint256 classId, uint256 nonceId, uint256 amount)** allows the transfer of any number of bond types from an address to another.

The “**_amount**” is the list of amount of the bond, that will be transferred from "**_from**"address to “**_to**” address.

There is no **_to** address in the definition

---

**GrandGarcon** (2022-05-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samsay/48/6130_2.png) samsay:

> It will be interesting to see how this standard based on the Blockchain allows to reduce the time of bond issuance, since in traditional finance, it can take more than a week for a bond to be issued. Also, removing all intermediaries which impact the cost of the bond would probably encourage investors.

thanks

indeed the motivation of this standard is to compose an structure that can be referred to issue , redeem bonds at same time without referring to any offchain / onchain smart contract protocols

---

**GrandGarcon** (2022-05-25):

thanks for finding the mistake in the description , indeed we dont need the “_to” address as in the implementation users have to reduce the amount of the bonds from the class structure . similar to the ERC20 where the _to is address(0). we will rectify the omission .

---

**BlockFi** (2022-06-02):

Could you be more price on how you are going to issue bonds through this EIP ? I know that bonds are financial instruments usually issued by corporations and government to borrow money, therefore it is more likely that the decentralized bonds you are proposing from this EIP will even face regulation from institutions or just be unauthorized in some countries.

One more question about class and nonce, in traditional bond systems there are no such parameters as characteristics of bonds, what is the advantage of introducing those news bond characteristics ?

---

**squirrel** (2022-06-03):

In the EIP it says that AMM is gas efficient, what makes it gas efficient? Is it just the structure or there is something more to it for gas savings?

---

**cheerhunter** (2022-06-03):

What is the difference between your standard and EIP 1450 which is stagnant now.

?

Link for reference: [EIP-1450: ERC-1450 A compatible security token for issuing and trading SEC-compliant securities](https://eips.ethereum.org/EIPS/eip-1450)

---

**mims85** (2022-06-03):

Hello guys,

Is this standard Fungible or not Fungible? The text doesn’t explicitly define it.

Thank you

---

**GrandGarcon** (2022-06-03):

Thanks for question .

Regarding issuance of the bonds ,  it depends on the :

- type of asset class you want to associate .
- what are the criteria for the creation of Bond  Classes and  Nonces for bond in the given class .
- and the metadata that defines the additional conditions of bonds (standards like green bonds)
- most importantly the  supplies (active , burned and redeemed supplies from the given market maker of the bonds or issuing entity) and  finally redemption time / conditions .

then we will need to understand the different counterparts  in the process of issuing the bonds . for our reference implementation we considered the following (which are explained in our whitepaper for v1 implementation [here](https://github.com/Debond-Protocol/Docs/blob/main/Debond_Whitepaper_V2_WIP.pdf)) :

1. Banks : these are the orchestrator for issuance and  redemption of bonds after maturity(and only this entity has the right to issue compliant bonds ).
2. Automated Pair Maker (APM) : this is the analogy of AMM but being single consolidated pools , where unlike the AMM , the bonds can be issued for single or multiple underlying collaterals
3. Secondary market maker(auction marketplace):  to provide  possiblity for P2P transfer and bidding of bonds .

Regarding the question of compliance :

Indeed our standard provides the minimal interface for encoding the information needed for compliance across different institutions . but we need to insure that the issuer entity (either the Bank contract as explained above or any external entity ) needs to encode the necessary information and corresponding metadata in the bond data structure , so that the destination marketplace (like the secondary market / APM or other offchain entity for  certification / price oracles etc) can decode and validate the information .

if you want an reference of the ease of our standard in handling this issue , checkout one of the latest issuance of bonds by an major french bank using modified version of ERC20 standard [here](https://forum.makerdao.com/t/security-tokens-refinancing-mip6-application-for-ofh-tokens/10605/24) , we see that the bonds issued  only defines the corresponding supply , standard and maturity date . thus it lacks the other parameters required to check the overall supply , redemption conditions and to  be sold on the secondary exchange , we will be needing the parent contract to fetch the details .

so in traditional bonds systems , we indeed have the notion of bonds and class .  for [example](https://markets.businessinsider.com/rates/u-s--rates-3-months) , the class information defines tghe category of the bond (name , category (based on redemption time , zero coupon , fixed rate and floating rate etc))and the nonce corresponds to the current state of the bonds (active , redeemed supply , interest rate , redemption time etc).

The advantage of using our implementation of bond structure is its unifies the different categories of bonds , their issuance from the single contract type .

---

**GrandGarcon** (2022-06-03):

thanks for the question ,

So if i understand correctly , you posed question from the rationate “AMM optimization” .

indeed ERC3475 allows to simplify the management of Liquidity Pool management as each bonds store the state of bond supply and type , thus there is no need to issuance of seperate contracts everytime an new LP pair is added into the pool , along with beenfits of consolidated liquidity (thus avoiding common attack vectors like Impermanent Loss etc). in our reference implementation (explained in [whitepaper](https://github.com/Debond-Protocol/Docs/blob/main/Debond_Whitepaper_V2_WIP.pdf)   , which we call as APM (Automated Pair Maker))

but along with that i wanted to also clarify that this standard is agnostic to the underlying liquidity maangement , and  you can indeed have integration across different liquidity providers (Both APM or the traditional AMM)

---

**GrandGarcon** (2022-06-03):

Thanks for the question ,

So indeed as explained before : our standard is agnostic to the issuance of various types of bonds and the entities handling the operations of the bonds (via the approvals ) , whereas seeing the standard ERC1450 seems that its hardcoded and modified version of ERC20 which is specific to standard compliance , along with the issue that we highted that it  will be needing seperate onchain contracts / offchain information in  order to check for redemption and transfer .

---

**GrandGarcon** (2022-06-03):

Thanks  for Q,

Its Non fungible in the sense that both the metadata , ownership and other details can be upgraded based on the different operations in the lifecycle , something that is an necessary process  in the bonds lifecycle (from issuance to the redemption of the bonds ).

---

**T2OTA** (2022-06-03):

Can we add memo like field for transfers? For example in Steller/Ripple, using Memo, exchange can track deposit to same address via different memo numbers. Can it be implemented here as well?

---

**Fibo** (2022-06-03):

This is awesome. I think this EIP will be the first to bring bonds to Blockchain through a dedicated standard. I had seen previous standards to bring Stocks and other similar instruments to the blockchain but none for bonds. Arguably, bonds can be complex and a dedicated standard would be really great to have.

---

**GrandGarcon** (2022-06-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/bc8723/48.png) T2OTA:

> Can we add memo like field for transfers? For example in Steller/Ripple, using Memo, exchange can track deposit to same address via different memo numbers. Can it be implemented here as well?

Indeed , so if you read the standard section **NonceInfos**

> NonceInfos
>
>
> nonceInfos(uint256 classId, uint256 nonceId) allows anyone to read the information of a bond class’ nonce.
>
>
> The "class" is the class nonce of bond, the first bond class created will be 0, and so on.
>
>
> The "nonce" is the nonce of the bond. This param is for distinctions of the issuing conditions of the bond.

if you consider the Nonce to be transaction   between  counterparties of an particular type , then the **NonceInformation** can be  define as  the reference information about the nature of transaction (as defined by the memos) , beyond that also as classInfos are also defined , this is  more helpful for transactions between the two different entities from different jurisdictions to get more information about the class of the transaction between the two different types of bond exchanges .

---

**Trotsky1984** (2022-06-09):

Hi dear developers,

I noticed that in the EIP, we have nonceInfos() to get a list of the value from the keys(classID, nonceID). But what will happen if we want to store in the same time an address, an integer and str. How the smart contract can interpreter this, and how the front end can translate those value for the users. Do we have a key dictionary. It’s this a part of EIP? I think we will need more detailed documents on the structure of the metadata.

---

**GrandGarcon** (2022-06-10):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/9fc348/48.png) Trotsky1984:

> I noticed that in the EIP, we have nonceInfos() to get a list of the value from the keys(classID, nonceID).

so the nonceInfo there can be indeed arbitrary array consisting of different types of address (and indeed our KPI ).

> But what will happen if we want to store in the same time an address, an integer and str.

Yes you can indeed store that in an array given that you provide the  sequential metadata corresponding to each of the inputs so that the counterperties and their corresponding frontend logic can decode / encode the information (its defined by nonceInfoDescription)

> How the smart contract can interpreter this, and how the front end can translate those value for the users. Do we have a key dictionary. It’s this a part of EIP?

yes you can do that by setting the **nonceInfoDescription(uint256 nonceInfo) external view returns (string[] memory nonceInfoDescription)**

PS: currently the nature of the nonceInfoDescription is defined as the **string (rather than an array of strings)** , so we will have to incorporate this correction now .

> I think we will need more detailed documents on the structure of the metadata.

correct indeed , so we  will create an PR with the changes

but if you could also explain some example of the metadata information needed to parse the store issuance and redemption information  , feel free to discuss .

---

**Trotsky1984** (2022-06-10):

Got it, looking forward to read the documents and to see how far this EIP can go.

---

**dberger26** (2022-06-14):

What is an example of the metadata you would need for a bond issued from an AMM as an LP token?

Also, I think you may have left something out here, under **Metadata Information:**

“Info describing the information about the nature of classes , this includes the nonceInfoDescription , details concerning the…”

---

**mehddcrypto** (2022-06-15):

Thank you for bringing this EIP in my notice. Being in the Banking space and also a blockchain enthusiast, I cleary see the need for this standard. Few years ago, my bank did a small experiment for bonds transfer using ERC 20 but again it did not get traction. I think that, with this standard and being able to support multiple metadata, the transition of bonds as instrument to DeFi can be surely accelerated. I am sharing the link of my bank’s smart contract for bond transfer. Indeed it was an interesting experiment


      ![image](https://coindesk-next-a6ificwar-coindesk.vercel.app/favicons/production/favicon.ico)

      [CoinDesk](https://www.coindesk.com/markets/2019/10/11/why-french-lender-socgen-issued-a-110-million-ethereum-bond-to-itself)



    ![image](https://cdn.sanity.io/images/s3y3vcno/production/ff4ed369cb1e5ace699b89e1b0b0d48bcda2b150-1320x880.jpg?auto=format)

###



Societe Generale has no plans to resell its $110 million ethereum bond, but future blockchain trials will involve external investors, an exec said.










https://etherscan.io/address/0x4914f3a6b16c3e43aec333950193e345cf167554


*(15 more replies not shown)*
