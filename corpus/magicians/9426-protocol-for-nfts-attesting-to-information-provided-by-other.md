---
source: magicians
topic_id: 9426
title: Protocol for NFTs attesting to information provided by other party
author: DAYvid
date: "2022-05-30"
category: Magicians > Primordial Soup
tags: [nft, token, ntt]
url: https://ethereum-magicians.org/t/protocol-for-nfts-attesting-to-information-provided-by-other-party/9426
views: 602
likes: 0
posts_count: 1
---

# Protocol for NFTs attesting to information provided by other party

Simple Summary

This decentralized protocol intends to incorporate some of the benefits expected from a soul-bound token (“SBT”) using the already-established ERC-721 standard. No restriction on functions defined by ERC-721 are necessary and neither are additions.

Summary

Information is more trusted in real life (“IRL”) when validated by more than one party, and especially by one other than the party asserting the information. This protocol will help two parties coordinate the assertion and confirmation of information stored within a non-fungible token (“NFT”) to an IRL third party.

This protocol allows for a special class of tokens: NFTs with their image digitally signed by the account that currently owns the token. The information contained in the image should be considered validated or confirmed by the NFT owner. The NFT can be transferred–unlike an SBT–but the public key of the owner will no longer confirm the signature of the image and thus the NFT no longer has a special status. The protocol defines the IRL meaning of a transfer of the NFT as a revocation of the validity of the information stored within the token.

The benefits of this protocol include a lightweight method for the public to confirm: 1) the integrity of the information stored within the blockchain, 2) the authenticity of the validating party, and 3) the on-going validation of the information by the NFT owner. This protocol defines the order and methods for minting and using the NFT by the coordinating parties in order to provide these benefits to themselves and to the public.

Abstract

The protocol establishes two mandatory events within the lifecycle of this special NFT.

1. Creation–the initial assertion and validation of the included information, and
2. Confirmation–the on-going attestation of the information by the NFT owner.

The protocol also allows the owner of the NFT to withdraw its attestation at any time, either temporarily, by transferring the token to any other account, or permanently, by burning it.

These events take advantage of standard NFT functions, only require use of common cryptographic primitives, and are assigned common-sense IRL interpretations.

Creation

In the beginning, an NFT has a creator. The creator determines the immutable image of information to include in the NFT, but that information doesn’t necessarily originate with the NFT creator. The image can be digitally signed by another party with the signature included in the NFT. This presents a simple way for a single NFT to store information validated by more than one party.

The digital signature by one account holder and the action of creating the NFT by another are considered the validation of the information stored in the NFT image. The parties must coordinate between themselves IRL which will be the asserting party and which will attest. The creator transfers the NFT to the attesting party.

Further, privacy of the information is possible but must be coordinated between the parties. The asserting party could encrypt the image before minting with a separate key to be shared only with the IRL intended recipients of the information. The attesting party must accept responsibility for encrypted information, implying the responsibility to validate the integrity of the encrypted image as well as its underlying information. The asserting party may require assurances from the attesting party of non-repudiation.

More than two parties may participate in the validation by including their digital signature. The ERC-721 approved operator role allows these additional validating parties to also serve as additional attestors. A digital signature matching an approved operator could be interpreted as providing further attestation. The NFT creator should approve the additional attesting parties as operators of the NFT.

The accounts and keys used must represent at least two different IRL “Souls” for this class of token to have IRL value higher than an NFT created by a single party. There are a minimum of three IRL parties: 1) the party asserting the information, 2) the recipient of the assertion, and 3) the party that confirms the asserted information for the recipient. It is left to the IRL receiver of the information to validate the respective identities of the parties and their reputations, as well as what level of trust to grant the information asserted within the NFT.

This protocol does not attempt to solve pervasive and persistent problems of information trust in society; only to facilitate on-chain support for parties already willing to engage in a trusted exchange of information. Creation of an instance of this special class of token is a method of asserting and validating at a specific point in time any set of information that leverages the benefits of the blockchain. It serves as a time-stamped record held in decentralized custody and made available through widespread, standardized infrastructure.

Minting, approving others, and transferring to the intended owner is considered phase 1 of this use-case for an NFT.

Confirmation

Any digitally signed piece of information on the blockchain typically represents only an affirmation of the information at the time of signing. IRL parties seeking validated information often desire a current validation. This protocol for the use of NFTs to attest information allows the established features of the ERC-721 standard for IRL parties to confirm the on-going validation of the asserted information asynchronously with the attesting party at any time.

Unlike SBTs, this class of NFT can be transferred at any time. The ability to hold, transfer, or burn an NFT presents an opportunity for the IRL interpretation of what those actions mean with respect to the information stored in the NFT. This protocol defines holding an NFT in the account that signed its image as an assertion that the information in the image is still valid. Transferring the NFT is interpreted as the attesting party withholding attestation. Burning the NFT is interpreted as a permanent revocation of the attestation.

A practical value of this type of NFT is that IRL recipients of the information within the token need only be presented with the ID of the token itself. The recipient can view the NFT image and query the current owner. The attesting party must also make their public key available to potential IRL recipients, either through a communication channel of the blockchain infrastructure or through off-chain channels trusted by the recipient. Also, if the image is encrypted for privacy, the asserting party must provide a key for decryption.

Requiring a match between the digital signature and the account of the current owner is not only for the convenience of IRL recipients. It is a necessary protection against attacks if this protocol were only partially implemented. If the current owner of an NFT is perceived as attesting to the information within its image, any digitally signed NFT could be sent to an account trusted by an IRL recipient without that account’s consent to attest. The IRL recipient might trust a public key not actually representing the current validating party. The standard protections of asymmetric cryptographic signatures still apply but only to the information at the time it was signed. The benefit of an on-going confirmation on the blockchain using only the features of an ERC-721 token is the core value of this protocol and illustrates the need for the protocol.

Approved operators of the NFT with a digital signature present in the NFT image must similarly be perceived IRL as less-reliable, on-going validation than the current token owner. Those account owners will have the ability to transfer the NFT away from the owner, thus revoking the signal of validation. However, an owner that has incorporated a digital signature into the NFT image could approve operators whose accounts are trusted by the IRL recipient but are not aware of their status as approved operators and thus on-going attesting parties. Nevertheless, the greater the number of approved accounts and the longer the time they have been approved the greater the IRL persuasion, albeit passive, of the on-going acceptance of the information that was once digitally signed by them.

Use Cases

This protocol is ideally suited for IRL situations where the recipient benefits from an updated or current confirmation that the prior validation continues to be attested by a participating party.

Fun

A team of friends succeed in an escape room within record time and each receive a token attested by the escape room venue. The escape room operator will transfer the token to revoke their status as record holders when another team sets a new record. The team members present the token to friends who use a special dApp to confirm its authenticity and the still-current record by the team. Each team member is also an approved operator of each other’s tokens to validate their membership on the record-holding team.

Financial

External auditors serve as the attesting party to a company’s financial statements by accepting the accounts signed by the company and minting them in an NFT. When uncertainties about the validity of the accounts appear, the auditors transfer the NFT financial statements–immediately suspending their attestation. After investigation, the auditors could transfer the NFT back to the confirming account to reinstate the attestation, or permanently revoke it from those financial statements by burning the NFT. High speed stock traders monitor the NFT continuously, requiring an asynchronous attestation at the expense of the traders.

The seller is a holder of a significantly sought-after asset contemplating a transaction with a potential purchaser. The seller requires evidence of funds available to the purchaser up to the time of delivery. The purchaser asserts an NFT balance statement attested by a bank under automated instructions to transfer or burn the token upon any decrease of funds. The seller confirms the ongoing attestation by the bank before rejecting any proposal before the closing.

Anti-fraud

The image of a license can be asserted to law enforcement, who confirm that it is still attested by the issuing institution.

The accrediting agency of a public notary acts as the attesting party for documents verified by accredited notaries. In case of confirmed fraud by a particular notary, the agency withdraws attestation for all documents verified by that notary by burning the relevant NFTs. Recipients of the documents are now on notice of potential fraud.
