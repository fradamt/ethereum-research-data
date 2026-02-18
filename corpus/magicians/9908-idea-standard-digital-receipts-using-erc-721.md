---
source: magicians
topic_id: 9908
title: "Idea: Standard digital receipts using ERC-721"
author: darcys22
date: "2022-07-11"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/idea-standard-digital-receipts-using-erc-721/9908
views: 5439
likes: 31
posts_count: 40
---

# Idea: Standard digital receipts using ERC-721

Hi Eth Magicians, wanted to discuss some thoughts I had regarding digital receipts on the blockchain and interested to hear what others think.

**Simple Summary:**

Using ERC-721/NFTs as a method of distributing digital receipts for physical purchases. Where the metadata represents an encrypted json receipt.

**Abstract:**

I’d like to propose the idea of a transaction that flows as follows:

1. A customer purchases an item from an online retailer, where checking out leads the customer to payment through a smart contract,
2. The smart contract verifys the amount transferred matches the order and provides the user with an standardized receipt NFT.
3. When fulfilling the order, the retailer will upload the metadata to this nft which will be encrypted against the customers public key.

**Motivation:**

If a customer purchases a physical item from an online retailer and uses a cryptocurrency to pay, the purchase will separately includes an invoice/receipt from the retailer that is emailed and/or physically   given to the customer. These receipts are critical for many reasons but digital receipts AFAIK have never gained traction. Instead we are left with PDFs and other analogue formats to represent transactions    that occurred digitally.

Including an NFT as a receipt will provide a traceable and private link between the funds leaving the customers account and the digital receipt which may include important information such as serial numbers   and delivery tracking etc. This means that the customer can automate their record keeping with systems and understand exactly what has been purchased without a human having to provide copies of the receipts.  Metamask for example could show this full receipt when you click into an item in your transaction history.

One of the major roadblocks to fully automating our current finance world is that businesses need to keep detailed records of our purchases and retailer systems distribute this detailed information outside of our transactional system (Printing a physical receipt, while separately processing payment through the EFTPOS machine). Requiring a human being to physically make the link between the two, usually by data     entry into the financial system. This is archaic and NFTs on the blockchain provide a method for this to be so much better.

**Outstanding thoughts:**

1. A less interesting thought is that the amount in this encrypted receipt could be proven by the retailer using some zero knowledge proof, which could mean a blockchain could reject the transaction if this   receipt does not match the amount transferred. Voiding the transaction.
2. A more interesting thought would be if the serial number encrypted in this receipt could be proven at a later time by the customer for use in warranty claims, maintenance requests, servicing etc.

Unsure if these are even possible, zero knowledge proofs are hard.

**Next Steps:**

If this has any sort of interest I could draft up the following standards for people to review:

1. Standard JSON format of the digital receipt
2. Standard for the encryption of digital receipt to be put as metadata
3. Standard for metadata of a NFT Receipt

## Replies

**DAYvid** (2022-07-12):

I think this is an excellent idea. Provides the benefits of In Real Life (IRL) receipts and solves some of their problems (e.g. warranty claims).

JSON is a great choice for data format, too. Human readable and standardized for efficient digital use.

Here’s some feedback to consider:

1. In Real Life (IRL) receipts are issued by the vendor, which make them more valid when used as evidence to third parties (e.g. taxes). If the receipt is issued by a smart contract upon receipt of payment, it loses that evidentiary quality because it only serves as proof of transferred funds. Was the item exchanged as well?
2. If the primary purpose of the NFT is the receipt, shouldn’t we store the data in the image of the NFT (rather than in metadata)? Remember that the “image” of an NFT doesn’t need to be pixel data that translates into a visual picture. ERC-721 doesn’t require that.
3. Encryption is clearly necessary to preserve privacy. Are there other privacy risks presented by common use of this? Wouldn’t some be hesitant to reveal the link between their IRL persona and their pseudonymous on-chain account? Think about how IRL receipts don’t include the full credit card number but only the last 4 digits.

These considerations are only about implementation details. I’m looking forward to seeing the first draft of this.

---

**darcys22** (2022-07-13):

These are great points! Thanks for the reply

1. I guess when I refer to a smart contract here I am also assuming the vendor is in control of the smart contract and the receipt would include some form of signature to prove that they indeed issued the receipt. I guess proof that the vendor indeed delivered the goods is another problem (Maybe solved by tracking information?).
2. I may have confused the term for metadata here. I thought I understood this but maybe not. But I guess if the URL in the token points to a JSON file (Stored on IPFS possibly) and structured like this:

```auto
{
  "version": 3,
  "id": "07a9f767-93c5-4842-9afd-b3b083659f04",
  "address": "aef8cad64d29fcc4ed07629b9e896ebc3160a8d0",
  "Crypto": {
    "ciphertext": "99d0e66c67941a08690e48222a58843ef2481e110969325db7ff5284cd3d3093",
    "cipherparams": { "iv": "7d7fabf8dee2e77f0d7e3ff3b965fc23" },
    "cipher": "aes-128-ctr",
    "kdf": "scrypt",
    "kdfparams": {
      "dklen": 32,
      "salt": "85ad073989d461c72358ccaea3551f7ecb8e672503cb05c2ee80cfb6b922f4d4",
      "n": 8192,
      "r": 8,
      "p": 1
      },
    "mac": "06dcf1cc4bffe1616fafe94a2a7087fd79df444756bb17c93af588c3ab02a913"
  }
}
```

And the cypher text decrypts to what our json receipt is.

1. Yeah there is definitely an element of privacy reduction in this, however I think a lot of it occurs simply by making the purchase. If you were analysing a wallet then knowledge that a transaction got a receipt (but not knowing the contents) is maybe only slightly more revealing than knowing they transferred to that business at all.

Appreciate the feedback, I might draft up an issue on the EIPS/ERC repos over the next few weeks to see what feedback I can get there.

---

**darcys22** (2022-07-26):

So I’ve typed up a rough draft of this here:



      [github.com](https://github.com/darcys22/digital-receipts-erc/blob/master/eip.md)





####



```md
---
eip:
title: Digital Receipt Non-Fungible Tokens
author: Sean Darcy
discussions-to: https://ethereum-magicians.org/t/idea-standard-digital-receipts-using-erc-721/9908
status:
type: Standards Track
category: ERC
created:
requires: 721
---

## Simple Summary

Using Non-Fungible Tokens as a method of distributing digital receipts for physical purchases. Where the metadata represents an encrypted json receipt.

## Abstract

This EIP proposes a standard schema for digital receipts of transactions occuring on chain. Digital Receipt Non-Fungibles Token are issued by a vendor when a customer makes a purchase from their store and contains transaction details necessary for record keeping. The transaction details are encrypted against the customers public key and kept off chain. Digital Receipt Non-Fungible Tokens extend [ERC-721](./eip-721.md) which allows for representing assets

```

  This file has been truncated. [show original](https://github.com/darcys22/digital-receipts-erc/blob/master/eip.md)










Still have a bit of work to do on it, including doing up a reference implementation.

Would love some more feedback from the community

---

**buoynous** (2022-07-27):

Great idea!

Quick question. Given that NFTs are currently tied to an image, what image are you planning to use for this specific NFT?

I think what [@DAYvid](/u/dayvid) was suggesting is to use the metadata to generate an image with texts. Something like LOOT.

Also I am not a big fan of storing things in the IPFS, especially if it is not a PFP collection that has limited supply. This can easily grow into a very large number of supply without a ceiling. In this case I think storing it on chain makes more sense.

But then that brings to another question of how do we plan on storing a large json file on-chain in a graceful way.

---

**darcys22** (2022-07-27):

So wouldn’t mind getting this clarified, my understanding of ERC-721 is that it

```auto
defines a minimum interface a smart contract must implement to allow unique tokens to be managed, owned, and traded. It does not mandate a standard for token metadata or restrict adding supplemental functions.
```

Where as ERC721Metadata is what actually ties the standard to an image and `the **metadata extension** is OPTIONAL for ERC-721 smart contracts`

So in my draft EIP i have mentioned under the backward compatibility section that

```auto
This standard is an extension of ERC-721. It is not compatible with commonly used optional extensions (IERC721Metadata and IERC721Enumerable) mentioned in the EIP-721 standard.
```

Which I think would be enough to say that the digital receipt NFT could point at a tokenURI that contains JSON that doesn’t comply with the IERC721Metadata extension. But I am not 100% sure on this. Would love some guidance here.

That way the tokenURI points to a JSON file of our encrypted receipt, containing none of the normal NFT image fields.

Alternatively I really like how loot have generated their image in the contract as a SVG containing all the text. So the image could be a printable representation of the JSON receipt. Which would be great. An SVG like this is way better than a PDF receipt.

In regards to IPFS, I actually think the vendors would host their digital receipts on their own servers. This means there is a risk that the tokenURI would eventually point to a dead link, but its probably reasonable to expect the purchaser to back that receipt up somewhere safe. If your digital receipt is signed by the vendor then you have proof that its real, even if the original disappears

---

**Property** (2022-08-03):

Love the idea, however i dont think id like giving my private key to third parties/finance systems to decrypt the receipts. Surely it would be better to encrypt the receipt with some derivative of the purchasers public key instead

---

**zzyalbert** (2022-08-04):

Great job, that will make NFT first class

---

**darcys22** (2022-08-09):

Yeah im liking this idea and still need to do some thinking about the encryption. It possibly should have optional encryption or no encryption in this ERC and then in another ERC design a way to encrypt all NFT types

---

**KeeJef** (2022-08-15):

Looks good to me, could this mix with existing digital ticketing proposals? Like buying a concert ticket and receiving a digital NFT to show as proof of entry?

---

**darcys22** (2022-08-15):

Yeah definitely, it would be the modern equivalent of showing your receipt to prove you bought a ticket

---

**darcys22** (2022-08-30):

Alright so pretty exciting times. Got a working demo, still got some rough ends to work on but we got ourselves a pretty cool looking digital receipt:

https://goerli.pixxiti.com/nfts/0xdce729ce90c35eaa36a2129bef25d0cf209fec10/12

This is all being hosted on [receipts.darcyfinancial.com](http://receipts.darcyfinancial.com)

and the source is all available here: [GitHub - darcys22/digital-receipts-erc: NFT digital receipts demo](https://github.com/darcys22/digital-receipts-erc)

Would love to get some feedback from people. Got a draft of the EIP that im not far off submitting either (Also available in that github repo)

---

**darcys22** (2022-09-01):

And have opened the PR for this now in the EIPS repo:

https://github.com/ethereum/EIPs/pull/5570

EIP-5570

---

**radek** (2022-09-05):

Even though I like the general idea, there is a significant issue with digital receipts. Jurisdictions.

Eg here is the formal template for the receipt in one of the EU countries: https://www.etrzby.cz/assets/cs/obrazky/vzorova_uctenka.jpg

The solution would require some global research for common fields and extensibility for particular jurisdictions. The extensibility would need to be flexible as the govs requirements are changing from time to time.

---

**SamWilsn** (2022-09-06):

If the only address that can update the receipt metadata is the retailer, why do you additionally need to sign the structure?

Should implementations verify the signature of the receipt upon uploading?

---

**darcys22** (2022-09-06):

The metadata is hosted by the retailer and without enforcing that the metadata is hosted on ipfs or something there is a good chance that customers end up with receipts linking to dead tokenURIs.

By signing the receipt the customer has the option to copy the whole receipt into their own financial system and that copy being sufficient evidence without needing the link. It would be the modern equivalent of keeping a copy in case the original gets destroyed.

I don’t think implementations should need to actually verify the receipt, but I can see scenarios such as auditors receiving copies of the receipts and wanting to verify that the receipt isn’t falsified by checking the signature.

---

**darcys22** (2022-09-06):

This is an awesome point and I’m glad it got raised. I know my own jurisdiction (Aus) well but seeing other countries requirements I immediately recognise that the structure needs some updating to be more flexible (variable number of taxes, additional purchase identification areas).

I think something that will both a blessing and a curse in this area is that countries will be slow to accept these digital receipts to substantiate expense claims. So even if our structure contains all the correct fields, a tax office auditor may still reject the receipt and require alternative proof of purchase (at least initially).

The opportunity that this brings would be that we don’t need to be compliant with all jurisdictions initially, and can work on making them compliant incrementally. As long as our first version is at least useful (which would be providing enough information to the customers financial systems to categorise the expense) then we can add additional fields to a v2 or even a subversion v2.1 for specific jurisdictions.

In saying that however, I have some ideas that should make the receipts more flexible and I want to add to the v1. So even if the structure isn’t perfect, a business could still achieve compliance with workarounds if necessary. For example putting an unstructured “extra” field so you can display additional fields such as the FIK, BKP and PKP fields in that cz structure you linked.

---

**SamWilsn** (2022-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/darcys22/48/6517_2.png) darcys22:

> The metadata is hosted by the retailer and without enforcing that the metadata is hosted on ipfs or something there is a good chance that customers end up with receipts linking to dead tokenURIs.

I’m still not quite sure why this needs to be on-chain. Couldn’t the retailer just send a signed receipt to the buyer over email or something?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/darcys22/48/6517_2.png) darcys22:

> By signing the receipt the customer has the option to copy the whole receipt into their own financial system and that copy being sufficient evidence without needing the link. It would be the modern equivalent of keeping a copy in case the original gets destroyed.

Hm, so what differentiates that from copying the signed transaction adding the metadata? (I’m mostly playing devil’s advocate here, I do see the value.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/darcys22/48/6517_2.png) darcys22:

> I don’t think implementations should need to actually verify the receipt, but I can see scenarios such as auditors receiving copies of the receipts and wanting to verify that the receipt isn’t falsified by checking the signature.

So I’m imagining a scenario where a retailer uploads an invalid signature, and the buyer doesn’t check the signature until much later (say during a dispute.) Since the transaction signature is valid, but the contract doesn’t check the embedded signature, you can get a disagreement about what is correct.

---

**darcys22** (2022-09-06):

Awesome points, appreciate the reply.

> I’m still not quite sure why this needs to be on-chain. Couldn’t the retailer just send a signed receipt to the buyer over email or something?

The value of being on chain is the initial link between the transaction and the receipt. A financial system monitoring a wallet sees a transaction for 10 eth which includes the nft receipt also saying 10 eth can be certain that transaction is represented by that receipt. It’s also an easy convenient place to store your receipts, even if you aren’t actively tracking them. You can come directly to the transaction if you need to review the receipt.

A good alternative would be a retailer emailing a json receipt and a financial system capable of retrieving the email and matching that to a transaction. Although less convenient to go back through emails to find the receipt if you aren’t running a system, this would be sufficient if it existed. Unfortunately the world has decided that PDFs via email is the easiest method here and parsing the pdf is actually the roadblock preventing progress. Because the retailers need to comply with tax regulations for evidence of purchase it needs to be the tax offices that lead the standardisation of the digital structure to take this pathway. Unfortunately they have shown no initiative to do so despite having decades of opportunity.

I actually expect if we get some traction for digital receipts in the cryptocurrency world that will start the fire that forces the old financial system to also standardise their local jurisdictions in a digital format. And we can update our standard to directly copy that if they eventually do.

> Hm, so what differentiates that from copying the signed transaction adding the metadata? (I’m mostly playing devil’s advocate here, I do see the value.)

This actually is interesting to explore, from the customers perspective there is no difference. The receipts purpose is simply to clarify the details, and the certainty that the receipts contents are true comes from directly experiencing the transaction. A third party needing to verify the transaction however cannot rely on an unverified statement, so the receipt contents need to be signed by any retailer to meet their evidence requirements. My thoughts are that we require the receipt contain the https url of the retailer, and their ssl certificate is used to sign the contents of the receipt. That way a third party can have 100% certainty of the receipt contents (and the customer isn’t trying to hide an alcohol purchase with a fake receipt).

> So I’m imagining a scenario where a retailer uploads an invalid signature, and the buyer doesn’t check the signature until much later (say during a dispute.) Since the transaction signature is valid, but the contract doesn’t check the embedded signature, you can get a disagreement about what is correct.

Yeah this would be possible, this is why it would be prudent to check the receipt signature is correct. But I don’t think we should enforce it here in this system, instead allow the customers to complain to the retailer, saying their receipts are incorrect and allowing the retailer to upload an amended and corrected receipt at a later date.

A business customer running a formal financial system that would likely be the place to check. Non business customers rely on the retailer satisfying its business customer needs who will complain.

I don’t think there is too high of a risk from retailers intentionally creating false receipts, there isn’t much to gain. And if we allow the metadata to change when mistakes/errors occur then it addresses the more common reason for incorrect signatures

---

**benmills** (2022-09-10):

I think this is a very interesting idea.

Would it be possible to use this to provide better security options for NFTs? Here is one way I could imagine it working as an example:

If I receive an NFT Receipt with a valid NFT purchase, I could move the Receipt NFT to a cold wallet. If I lose my NFT due to fraud, I can present the NFT Receipt to reclaim the NFT.

---

**darcys22** (2022-09-10):

I hadnt thought too deep into that side of things! But love it!

Like a nft recovery method!


*(19 more replies not shown)*
