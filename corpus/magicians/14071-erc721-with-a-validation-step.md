---
source: magicians
topic_id: 14071
title: ERC721 With a validation step
author: eduardfina
date: "2023-04-30"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/erc721-with-a-validation-step/14071
views: 2181
likes: 1
posts_count: 8
---

# ERC721 With a validation step

We all know someone who has had their private key stolen and all their assets (NFT and tokens) taken.

The power of the Blockchain is at the same time its weakness, giving the user full responsibility for their data.

I believe that with a small modification of the ERC721 standard we could add an optional validation step for transfer or approve transactions.

This step could be regulated in different ways, for example from a centralized server the user could validate his transactions, giving the security of web2 to web3.

I did an example implementation where there is an address validator that could be executed from a centralized server when the user validates his transactions.

I have also added a Smart Contract Permission so that the user can choose if he wants to use this new system or control his NFTs in the traditional way.

Having a separate Smart Contract Permission would allow to have the same preference settings for multiple NFT Smart Contracts.

Github link: [GitHub - eduardfina/ERC721V: ERC721 implementation with a validation step](https://github.com/eduardfina/ERC721V)

I have also done the same implementation but with ERC-20 tokens: [GitHub - eduardfina/ERC20V: ERC20 implementation with a validation step](https://github.com/eduardfina/ERC20V)

I think it would be a good EIP, what do you think?

## Replies

**SamWilsn** (2023-08-22):

I’m no expert on NFTs or Solidity, but I do have some non-editorial concerns that I want to bring up before moving this into last call.

First and foremost, this proposal pretty dramatically changes the behaviour of the transfer and approve functions, to the point that dapps relying on the common approve-then-transfer workflow would break. The proposal needs to go more in-depth on how this change would affect existing applications. Is it possible to exploit this? Say, for example, an escrow contract exists where one party deposits ether and the other party deposits their NFT. Once both deposits are made, the escrow releases funds to the appropriate counterparty. If the NFT is not actually transferred (and `transfer` doesn’t revert), the escrow contract may be tricked into thinking it has received the token when it hasn’t.

Secondly, do smart contract wallets solve this in a better and more generic way?

---

**Weixiao-Tiao** (2023-08-23):

[Devpost](https://devpost.com/software/securechain-p7w6u2)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/1/1569094c0f32f42a25230fd8c6f91ce50388fd30.png)

###



Securechain is an hybrid transfer validation system to protect NFTs and Tokens in hot wallets against wallet draining attacks.










This is the reward winning project of the author, I think it’s based on the two related EIPs (6997 and 7144)

---

**eduardfina** (2023-09-22):

Hello Sam,

As mentioned by [@Weixiao-Tiao](/u/weixiao-tiao), two EIPs were created specifically for the winning project, Securechain:

[Securechain](https://devpost.com/software/securechain-p7w6u2)

To address your initial query, both of these EIPs facilitate direct transfers from approved accounts. Consider OpenSea, for instance. If you authorize OpenSea to manage your assets, they will be able to transfer them seamlessly. This process does not compromise the integrity of their transfer procedures.

Regarding the use of an escrow Smart Contract, it might be more prudent to approve the Smart Contract itself rather than transferring assets directly. However, if both parties opt to first transfer assets to the escrow Smart Contract, two pivotal considerations arise:

1. **Uncompleted Transfer to the Escrow:**I recommend a best practice of verifying the NFT owner using the ownerOf function. If the approval process or owner validation is not adhered to, there exists a potential vulnerability not only with the escrow Smart Contract but also with numerous other Smart Contracts that do not validate NFT ownership.
2. **Escrow Transfer to the User:**I’ve already contemplated this scenario. The example implementation of the EIP should be adjusted to include an additional function allowing accounts to enable a two-step verification process. This extra step would prevent all existing Smart Contracts from facilitating such transfers by default, ensuring that their NFTs remain usable just like regular NFTs.

Now, concerning the Smart Contract Wallet question:

When your assets are held in a Smart Contract Wallet, you do not have direct ownership of them. They are technically owned by the Smart Contract, while you possess ownership of the wallet itself.

Our implementation offers the advantage of safeguarding your assets while maintaining your direct ownership. For instance, if you wish to use your NFT as your X/Twitter profile picture or utilize your NFTs in a game like Axie Infinity, both scenarios are possible with our security system but not when using a Smart Contract Wallet.

Our goal is to protect your assets and, at the same time, ensure you can fully enjoy them!

---

**SamWilsn** (2023-09-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eduardfina/48/9178_2.png) eduardfina:

> Regarding the use of an escrow Smart Contract, it might be more prudent to approve the Smart Contract itself rather than transferring assets directly

That is what I meant, but I must have missed this line in the proposal when I last read it:

> When the transfer is called by an approved account and not the owner, it MUST be executed directly without the need for validation.

Now it makes sense. Thanks!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eduardfina/48/9178_2.png) eduardfina:

> When your assets are held in a Smart Contract Wallet, you do not have direct ownership of them. They are technically owned by the Smart Contract, while you possess ownership of the wallet itself.

Why make the distinction between EOAs and smart contract wallets? You own your NFT because you have the private key (or whatever) you need to sign transactions, not because the validation logic is written in Go or Solidity.

If a service doesn’t support [ERC-1271](https://eips.ethereum.org/EIPS/eip-1271) (and related smart contract wallet standards), that’s a bug on their end ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

I will concede, however, that there are a bunch of services that suffer from this bug, so maybe this does make sense.

I’d reach out to some wallets and see if they’d build UI/UX for this, because if they don’t like it, it’s unlikely to catch on. We have a selection of wallet devs and a monthly call over here: https://allwallet.dev/

---

**eduardfina** (2023-09-23):

Absolutely! I agree that you have ownership of the NFTs in your Smart Contract Wallets. However, the reality is that many dApps do not currently support this feature.

For instance, Axie Infinity only permits the use of MetaMask and Trezor for simple accounts, and even OpenSea, the largest NFT Marketplace, does not accept ERC-1271.

With our implementation, you will be able to view your NFTs on OpenSea and transfer them by granting approval to OpenSea for the transfer.

We aim to enhance the security of your NFTs without compromising usability. I believe that for many existing dApps, it would be more practical to add an additional front-end page to clarify the two-step approval validation, rather than overhauling their entire structure to accommodate Smart Contract Wallets.

---

**SamWilsn** (2023-09-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eduardfina/48/9178_2.png) eduardfina:

> OpenSea, the largest NFT Marketplace, does not accept ERC-1271

I’m pretty sure that OpenSea does support ERC-1271, and they do [mention it in SeaPort](https://github.com/ProjectOpenSea/seaport/blob/22ea29df3c241ebc17c95268164dde47e1186287/reference/lib/ReferenceVerifiers.sol#L66). I haven’t tried a smart contract wallet on OpenSea in some time though.

---

I’m just hesitant to standardize something like this, if the Ethereum ecosystem will be moving to smart contract wallets eventually anyway.

In any case, I think you’re fine to move to the next status if you’d like.

---

**eduardfina** (2023-09-23):

I apologize for any confusion. I previously had information suggesting that [Opensea didn’t support ERC-1271](https://levelup.gitconnected.com/how-to-allow-multi-sig-wallets-to-authenticate-with-your-dapp-8f8a74e145ea), but it’s possible that this has changed recently.

Can you confirm whether you can view both your NFTs and the NFTs in your contract wallet on your Opensea profile page?

We are currently working on a professional version of my Hackathon Winner project, Securechain, with the aim of enhancing asset security for the web3 community. While we are implementing these standards, we are also evaluating the advantages and disadvantages of using a contract wallet with a verification step instead.

Regardless of our final decision, I believe having these standards in place would be beneficial for the ecosystem.

