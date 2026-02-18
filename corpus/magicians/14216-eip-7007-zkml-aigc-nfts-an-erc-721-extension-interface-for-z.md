---
source: magicians
topic_id: 14216
title: "EIP-7007: zkML AIGC-NFTs, an ERC-721 extension interface for zkML based AIGC-NFTs"
author: socathie
date: "2023-05-10"
category: EIPs
tags: [erc, nft, token, erc-721]
url: https://ethereum-magicians.org/t/eip-7007-zkml-aigc-nfts-an-erc-721-extension-interface-for-zkml-based-aigc-nfts/14216
views: 6084
likes: 23
posts_count: 27
---

# EIP-7007: zkML AIGC-NFTs, an ERC-721 extension interface for zkML based AIGC-NFTs

## Abstract

The zkML AIGC-NFTs standard is an extension of the ERC-721 token standard for AI Generated Content. It proposes a set of interfaces for basic interactions and enumerable interactions for AIGC-NFTs. The standard includes a new mint event and a JSON schema for AIGC-NFT metadata. Additionally, it incorporates zkML capabilities to enable verification of AIGC-NFT ownership. In this standard, the `tokenId` is indexed by the `prompt`.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

**Every compliant contract must implement the ERC-7007, ERC-721, and ERC-165 interfaces.**

The zkML AIGC-NFTs standard includes the following interfaces:

ERC-7007: Defines a mint event and a mint function for minting AIGC-NFTs. It also includes a verify function to check the validity of a combination of prompt and proof using zkML techniques.

```solidity
pragma solidity ^0.8.18;

/**
 * @dev Required interface of an ERC7007 compliant contract.
 */
interface IERC7007 is IERC165 {
    /**
     * @dev Emitted when `tokenId` token is minted.
     */
    event Mint(
        uint256 indexed tokenId,
        bytes indexed prompt,
        bytes indexed aigcData,
        string uri,
        bytes proof
    );

    /**
     * @dev Mint token at `tokenId` given `prompt`, `aigcData`, `uri` and `proof`.
     *
     * Requirements:
     * - `tokenId` must not exist.'
     * - verify(`prompt`, `aigcData`, `proof`) must return true.
     *
     * Optional:
     * - `proof` should not include `aigcData` to save gas.
     */
    function mint(
        bytes calldata prompt,
        bytes calldata aigcData,
        string calldata uri,
        bytes calldata proof
    ) external returns (uint256 tokenId);

    /**
     * @dev Verify the `prompt`, `aigcData` and `proof`.
     */
    function verify(
        bytes calldata prompt,
        bytes calldata aigcData,
        bytes calldata proof
    ) external view returns (bool success);
}
```

Optional Extension: Enumerable

The **enumeration extension** is OPTIONAL for ERC-7007 smart contracts. This allows your contract to publish its full list of mapping between `tokenId` and `prompt` and make them discoverable.

```solidity
pragma solidity ^0.8.18;

/**
 * @title ERC7007 Token Standard, optional enumeration extension
 */
interface IERC7007Enumerable is IERC7007 {
    /**
     * @dev Returns the token ID given `prompt`.
     */
    function tokenId(bytes calldata prompt) external view returns (uint256);

    /**
     * @dev Returns the prompt given `tokenId`.
     */
    function prompt(uint256 tokenId) external view returns (string calldata);
}
```

ERC-7007 Metadata JSON Schema for reference

```json
{
    "title": "AIGC Metadata",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Identifies the asset to which this NFT represents"
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this NFT represents"
        },
        "image": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this NFT represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive."
        },

        "prompt": {
            "type": "string",
            "description": "Identifies the prompt from which this AIGC NFT generated"
        },
        "aigc_type": {
            "type": "string",
            "description": "image/video/audio..."
        },
        "aigc_data": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this AIGC NFT represents."
        }
    }
}
```

## Rationale

The zkML AIGC-NFTs standard aims to extend the existing ERC-721 token standard to accommodate the unique requirements of AI Generated Content NFTs representing models in a collection. This standard provides interfaces to use zkML to verify whether or not the AIGC data for an NFT is generated from a certain ML model with certain input (prompt). The proposed interfaces allow for additional functionality related to minting, verifying, and enumerating AIGC-NFTs. Additionally, the metadata schema provides a structured format for storing information related to AIGC-NFTs, such as the prompt used to generate the content and the proof of ownership.

With this standard, model owners can publish their trained model and its ZKP verifier to Ethereum. Any user can claim an input (prompt) and publish the inference task, any node that maintains the model and the proving circuit can perform the inference and proving, then submit the output of inference and the ZK proof for the inference trace into the verifier that is deployed by the model owner. The user that initiates the inference task will own the output for the inference of that model and input (prompt).

## Backwards Compatibility

This standard is backward compatible with the ERC-721 as it extends the existing functionality with new interfaces.

## Test Cases

The reference implementation includes sample implementations of the ERC-7007 interfaces under `contracts/` and corresponding unit tests under `test/`. This repo can be used to test the functionality of the proposed interfaces and metadata schema.

## Reference Implementation



      [github.com](https://github.com/AIGC-NFT/implementation)




  ![image](https://opengraph.githubassets.com/3ef78fcfa322f85c91ee7441c1d3c8f4/AIGC-NFT/implementation)



###



Contribute to AIGC-NFT/implementation development by creating an account on GitHub.










## Security Considerations

Needs discussion.

## Replies

**hiddenintheworld** (2023-05-11):

Interesting, this should be a standard for verifying zkML.

---

**kartin** (2023-05-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> be a standard for verifying zkML.

The implementation of this EIP will act as a catalyst for tangible productivity within the Ethereum ecosystem. Furthermore, it stands to revolutionize AI by financializing open-source AI models, creating a synergy between blockchain and artificial intelligence like never before.

---

**xhyumiracle** (2023-05-14):

# Adding EIP-7007 Project Workflow:

We decide to post this part of the content here first to receive more comments & feedbacks before merging to EIP7007.

The suggested workflow of a simplified ZKML-AIGC-NFTs (EIP7007 compliant) project is as follows:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/b/b3bdd003422751e0e159836d8586727f25fa9d6d.png)image938×866 19.3 KB](https://ethereum-magicians.org/uploads/default/b3bdd003422751e0e159836d8586727f25fa9d6d)

There are 4 components in this project:

- ML Model - contains weights of a pre-trained model, given an inference input, generate the output;
- ZKML Prover - given an inference task with input & output, generate a zk proof;
- AIGC-NFT Smart Contract - ERC7007 compliant contract, with full ERC721 functionalities;
- Verifier Smart Contract - implementing a verify function, given an inference task & its zk proof, return the verification bool result.

**The key idea** here is to encourage users to propose novel prompts that can generate valuable AIGC, by issuing NFTs for each <prompt, aigc> pair to the user as an ownership claim.

---

**xhyumiracle** (2023-05-14):

[![image](https://ethereum-magicians.org/uploads/default/original/2X/c/c615ff29539c0bb1ed7decfecebd5df7fda37b50.png)image588×422 13.6 KB](https://ethereum-magicians.org/uploads/default/c615ff29539c0bb1ed7decfecebd5df7fda37b50)

## User Interaction Workflow (the left one)

1. A user proposes a Prompt, send it to the ML Model
2. ML Model does the inference and generate AIGC File
3. ZKML Prover generates a zk proof, given the prompt and aigc file as public input, model weights as witness
4. Either the project owner or the user calls the ERC7007 compliant AIGC-NFT contract on the mint function; the contract calls verify function internally, and mint a new NFT for the original users who proposed the prompt, claiming that the user owned the prompt & the corresponding aigc content.

optionally, the verification logic can be implemented in another Verifier Smart Contract with a view interface, to separate the code logic.

## Project Creation Workflow (the right one)

In order to launch this type of project. The project creator needs to create these 4 components with the following workflow.

---

**xhyumiracle** (2023-05-14):

## Adding Claimable EIP-7007 Workflow

In the previous design, the prompt is sent to model owner first before claim ownership for the user. That brings up a potential issue when the AIGC of that prompt is in high quality and can have high value, then the model owner might choose to steal it and claim by itself, infringing the user’s right.

To solve it, we hereby propose the Claimable Extension of EIP7007. The suggested workflow is like this:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a8c0943b4508fc44078a003d3867ac9b98f939ad_2_690x440.png)image1632×1042 43.3 KB](https://ethereum-magicians.org/uploads/default/a8c0943b4508fc44078a003d3867ac9b98f939ad)

The difference is that, the user will send a tx to Ethereum **before** send it to the ML Model, calling the `claim` interface of the AIGC-NFT Smart Contract to claim the ownership of the prompt. In this way, the model owner can only upload the aigc and mint the NFT for the user, but cannot steal the ownership anymore.

It costs the user an extra interaction, but secured the prompt ownership if (s)he thinks worth it. Probably it can become an option for all users.

---

**socathie** (2023-05-14):

## Adding IERC7007Claimable

To supplement the above diagram of the Claimable Extension of EIP7007, we propose the following interface:

```solidity
pragma solidity ^0.8.18;

/**
 * @title ERC7007 Token Standard, optional claimable extension
 */
interface IERC7007Claimable is IERC7007 {
    /**
     * @dev Emitted when `owner` claims `prompt`.
     */
    event Claim(bytes indexed prompt, address indexed owner);

    /**
     * @dev Claim ownership of given `prompt`.
     *
     * Requirements:
     * - `prompt` must not be claimed.
     */
    function claim(bytes calldata prompt) external returns (address owner);
}
```

---

**hiddenintheworld** (2023-05-16):

```auto
pragma solidity ^0.8.18;

interface IERC7007 is IERC165 {
    event Mint(
        uint256 indexed tokenId,
        string indexed prompt,
        bytes32 indexed aigcDataHash,
        string uri,
        bytes proof
    );

    function mint(
        string calldata prompt,
        bytes32 aigcDataHash,
        string calldata uri,
        bytes calldata proof
    ) external returns (uint256 tokenId);

    function verify(
        string calldata prompt,
        bytes32 aigcDataHash,
        bytes calldata proof
    ) external view returns (bool success);
}

interface IERC7007Enumerable is IERC7007 {
    function tokenId(string calldata prompt) external view returns (uint256);

    function prompt(uint256 tokenId) external view returns (string memory);
}

interface IERC7007Claimable is IERC7007 {
    event Claim(string indexed prompt, address indexed owner);

    function claim(string calldata prompt) external returns (address owner);
}
```

# Suggestion

1. Minimize the use of bytes:Using bytes for the prompt and aigcData parameters may be inefficient if these are typically short strings, as bytes uses more gas than string. If possible, consider using string instead.
2. Optimize the mint function:In the mint function, the aigcData is included in the Mint event. This could potentially be a lot of data and thus expensive in terms of gas costs. If possible, consider storing a hash of the aigcData instead.

# Changes made

1. Changed bytes to string for prompt in all interfaces. This assumes that your prompt can be represented as a string rather than bytes.
2. Changed bytes to bytes32 for aigcData in mint and verify functions, and renamed it to aigcDataHash. This assumes that you are able to hash the aigcData off-chain and store only the hash on-chain.
3. Changed prompt function in IERC7007Enumerable to return string memory instead of string calldata. This is because calldata is a data location that can only be used for external function parameters.

---

**socathie** (2023-05-16):

Great minds think alike! These are some of the considerations we have had as well. Let us explain our thought process and see what you think

## prompt

Regarding the use of `bytes` vs `string`, our primary condition is that `prompt`, depending on the model, *might* end up containing more than just the text prompt. We might need to keep `prompt` as more flexible to include any data that uniquely identifies an output media, including but not limited to e.g. seed, latent, etc.

## aigcData

The hash of `aigcData` is also something we have considered. We decided to keep it as `bytes` to allow the flexibility of minting it in raw form or hashed form. Our primary concern is that we need to have a single source of truth about what the NFT content is (especially if it is not an image) and not sure if we should rely on off-chain computation to verify the hash itself. We do foresee that some model/contract owners will opt for `aigcData` to be a hash instead.

We are definitely open to hearing about what everyone thinks is the best practice in this case.

---

**totorovirus** (2023-05-18):

> Regarding the use of bytes vs string, our primary condition is that prompt, depending on the model, might end up containing more than just the text prompt. We might need to keep prompt as more flexible to include any data that uniquely identifies an output media, including but not limited to e.g. seed, latent, etc.

While the text to image generation is the most common usage case of stable diffusion variants, there are some other commonly used method such as image to image generation, vectorized text to image generation, etc. I think this proposal should state somewhere that it limits the scope to text to image generation, along with some hyperparameters (ex. seed). There are too many methods to generated images and advanced users are deploying this method to customize their images, that it may be too much for a single proposal to capture all the use cases.

---

**socathie** (2023-05-18):

The intention of this proposal is to support a wide range of AI-generated content, with input data including but not limited to text, and output data including but not limited to images. Perhaps `prompt` itself is a misnomer, but we really meant any input data of the AIGC model. Are there any cases that you think a `bytes` variable wouldn’t be sufficient to capture those other cases?

I do agree that a single proposal would not be able to capture all the use cases. This is just a starting point.

---

**hiddenintheworld** (2023-05-28):

Maybe adding the specification will be able to justify so it is not just string based and could be any bytes.

---

**SamWilsn** (2023-06-08):

From the initial pull request:

> Generally minting is an application-specific operation. In other words, it is unusual to standardize mint because how it works is usually tied pretty closely to each token.
>
>
> The question I’ll need you to answer is: will anyone other than the deployer of the contract (or the deployer’s specific dapp, like OpenSea) be calling the mint function?
>
>
> If not, you don’t really need to standardize it, though I think adding the ML metadata extensions make sense.

---

**rishotics** (2023-06-14):

Interesting, one doubt(correct me if I am wrong) isnt the ML model and ZKML Prover the same? According to me we send the prompt to the ZKML Prover/ML model and get the output of AIGC File and Proof.

---

**socathie** (2023-06-16):

The prompt variable by design could be the actual prompt or a hash of the prompt to maintain privacy. It depends on the use case.

---

**socathie** (2023-06-16):

They could be the same thing. But the flexibility allows for provers to precompute the results in pure ML first and use those as input signals into the ZK circuit.

---

**cc271793784** (2023-06-16):

Go it thanks for the answer! Would like to discuss the possibility of deploying verifier on-chain but not the ML model. It might be costly to run model on-chain. Could user run model offchain, but generate proof of <prompt, aigc> on chain?

---

**socathie** (2023-06-16):

The model is never deployed on chain in this design! That’s why we need to use ZK for verifiability.

---

**cc271793784** (2023-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/socathie/48/9426_2.png) socathie:

> model owners can publish their trained model and its ZKP verifier to Ethereum.

Apologize for the misunderstanding - I revisit the proposal, it only publish the model on eth but not deploy it. Thanks for the clarification.

Could you explain a little bit more about the process of -

"model is published on eth, and the user could apply the model to do inference process on their prompt. How the publish and inference process is working?

---

**xhyumiracle** (2023-06-20):

Right, thanks for the great question.

The key point here is that we need to ‘ping’ the model to Ethereum, either through a commitment data or publish the original model weights, this is what we meant by ‘publish the model’. Because we think an aigc-nft project should be able to convince the community that a given aigc is generated from a specific pre-defined ml model.

As for the ‘publish’ style, it depends on how the zkml project designs their zk circuit, and how they consider the privacy of the ml model.

In one case, a zkml project only needs to publish the zk verifier on-chain, and since the verifier usually contains the commitment info of the model structure as well as weights, it’s considered to be ‘publishing’ the model to Ethereum.

In another case, a zkml project can also choose to define the model weights and even its structure as the public input of the zk circuit. Then the model weights & structure info should be stored in the smart contract, in order to ‘ping’ the model. This is literally ‘publish’ the model.

Alternatively, a zkml project can define the model weights & structure as the witness (private input) of the zk circuit, which won’t be revealed during the verification and provides more privacy. But then it needs to include the commitment of the ml model in the public input of the circuit, and store it in the smart contract. So that the model is ‘pinged’ on-chain and won’t change. This is like separating the ml model commitment from the verifier, comparing to the first case.

Anyway, we consider an aigc-nft project should ‘publish’ their model, to commit on using a specific pre-defined ml model.

I hope this answers part of your question. And open to any suggestions & discussions, regarding either our considerations or the specifications.

---

**jseam** (2023-07-03):

I would propose that another EIP for the verifier be implemented too. This EIP hides two standards.

1. The interface for a zkml erc721 contract
2. The interface for the verifier contract

Making a generic verifier contract specification might be valuable as similar computations might be used in other applications beyond the ERC721 extension.


*(6 more replies not shown)*
