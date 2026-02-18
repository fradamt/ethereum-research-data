---
source: magicians
topic_id: 20403
title: "EIP-7730: Proposal for a clear signing standard format for wallets"
author: lcastillo-ledger
date: "2024-06-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7730-proposal-for-a-clear-signing-standard-format-for-wallets/20403
views: 1175
likes: 4
posts_count: 10
---

# EIP-7730: Proposal for a clear signing standard format for wallets

Hi All,

As Ledger, we want to improve the way user interacts with their wallets by displaying more clearly to them what message / transaction they are going to sign (what we call clear signing).

Basing the UI on the ABI does not lead to the best experience, the types are too broad and not easily interpreted as is. This proposal complements the definitions in the ABI with metadata targeted at specifying how to format the display of a transaction / messages for review.

Our goal is to make it easy for contract developers to define & control the interaction of their end users when calling their contract. Making it an EIP will enable all wallets to benefit from this information.

The ERC pull request is here: [Add ERC: Structured Data Clear Signing Format by lcastillo-ledger · Pull Request #509 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/509)

And for more info, we’ve created an intro video: https://www.youtube.com/watch?v=-O7aX6vUvs8

Thanks!

## Replies

**Ivshti** (2025-03-16):

gm [@lcastillo-ledger](/u/lcastillo-ledger), how does this EIP handle multi-call and recursive parsing? For example, the uniswap router works via a multicall in many of the cases, so if we rely on the simple 7730 descriptors, it won’t be able to go into detail of what’s going on inside the multicall.

Let me know if this is something you’ve thought about

---

**lcastillo-ledger** (2025-03-17):

Hi [@Ivshti](/u/ivshti) and thanks for the feedback!

Indeed this is a case we’ve considered, and currently you’d handle it using the `calldata` format when defining your function, associated with a path of the form `data.[]`, specifying that the formatter should be applied to all the elements of the `data` array. The `calldata` format tells the wallet that the parameter is a nested calldata, and should come with its own ERC 7730 file to describe how to clear sign it (can be the same file).

For example this is how we’d define the ERC 7730 file for the ERC-6357 multicall:

```auto
{
    "$schema": "https://github.com/LedgerHQ/clear-signing-erc7730-registry/blob/master/specs/erc7730-v1.schema.json",

    "context": {
        "$id": "ERC-6357 Multicall",
        "contract": {
            "abi": [ ... ]
        }
    },

    "display": {
        "formats": {
            "multicall(bytes[] data)": {
                "intent": "Execute Multiple Transactions",
                "fields": [
                    {
                        "path": "data.[]",
                        "format": "calldata",
                        "params": {
                            "calleePath": "@.to"
                        }
                    }
                ],
                "required": ["calls"]
            }
        }
    }
}
```

Note that this is not yet supported on Ledger devices, so this form has not been tested extensively. Most notable caveats:

- I’m realising we’re missing a way to specify the values passed in the nested calls, and should probably be added in parameters
- We’re also not distinguishing delegate calls from normal calls. Using a target of “@.to” wold work, but we might want to show that a call is a delegate call in the UI.
- Packing / serializing calldata in unusual formats wouldn’t work without embedding complex logic in the ERC 7730, which defeats the purpose of having a descriptive model rather than a programmatic one

---

**Ivshti** (2025-03-17):

[@lcastillo-ledger](/u/lcastillo-ledger) thanks for the answer

have you thought about how the multiple calls will be displayed to the user? Would the UI need to show nested intent texts, or will they be concatenated with “and” or just flattened at the top level?

Like, what if the multicall contains a swap and a transfer, would this show “Swap X for Y and send Z to …”

---

**lcastillo-ledger** (2025-03-17):

Replying for ledger here (since this is clearly wallet specific and will probably never be specific by the erc 7730).

Given hardware wallets constraints on memory and screen size, the very first implementation will probably be flattened with a clear separator between each calls until we know we whether we can do better.

So probably something like

Embedded Call 1 -----

Swap X for Y

Embedded Call 2 -----

Send Z to A

---

**0xad1onchain** (2025-04-17):

[@lcastillo-ledger](/u/lcastillo-ledger) How would someone support signing 712 messages for multisig or smart contract wallet like gnosis safe? We have thousands of safe wallets deployed and more being deployed everyday with same EIP712 signature structure. Would not be feasible to keep adding addresses all safe wallets across all chains in PR

---

**PatrickAlphaC** (2025-05-22):

Ah I love this!!! I’d like to add some functionality that I think will make all of this “just work”.

May I recommend a new ERC-7730 function called `getWalletDocsUri`. Here is an example solidity implementation

```solidity
string constant DOCS_URI = "...."; // string here
uint256 public latestDocsVersion = 0;

function getWalletDocsUri(uint256 docsVersion) external view returns(string memory) {
   // Could easily add conditionals/mappings/etc here....
   return DOCS_URI;
}
```

This would return a URI (similar to that of an NFT) which has the JSON object with all the data. There are a few nice things about this:

1. The JSON could be base64 encoded, so the entire documentation could be placed on-chain.
2. It could be easily updatable, and map new versions of the docs based on the latestDocsVersion.

If you don’t wish to have your docs on-chain, then you could still host them on a site. Many tokens like ERC20s, could just point to another contract that already has the ERC20 ABI implemented, and would not have to spend any additional gas other than adding this additional function.

---

**PatrickAlphaC** (2025-05-22):

They could all just point to a `docs_uri` based on the `safeVersion`:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/patrickalphac/48/7343_2.png)
    [EIP-7730: Proposal for a clear signing standard format for wallets](https://ethereum-magicians.org/t/eip-7730-proposal-for-a-clear-signing-standard-format-for-wallets/20403/7) [EIPs](/c/eips/5)



> Ah I love this!!! I’d like to add some functionality that I think will make all of this “just work”.
> May I recommend a new ERC-7730 function called getWalletDocsUri. Here is an example solidity implementation
> string constant DOCS_URI = "...."; // string here
> uint256 public latestDocsVersion = 0;
>
> function getWalletDocsUri(uint256 docsVersion) external view returns(string memory) {
>    // Could easily add conditionals/mappings/etc here....
>    return DOCS_URI;
> }
>
> This would return a URI (similar …

So it would make your life actually really easy, almost no lift on your end.

---

**mdaus** (2025-08-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/patrickalphac/48/7343_2.png) PatrickAlphaC:

> latestDocsVersion

You can use the same concept from **ENS contenthash**, so it maps the off-chain storage (likely **IPFS** or similar) to the contract address itself.

Mapping that **DOCS_URI** to a smart contract means that old contracts would be vulnerable because even if we map it to any other addresses without hardcoding it to the actual wallets, it needs to fetch that smart contract address from somewhere.

Now, new contracts are okay to include the **DOCS_URI**, but they’re dependent on the developers of their contracts to make the intents really correct and available.

What about we create a singleton contract that registers new **DOCS_URI** for every contract address, so it can complement already deployed contracts?

In that case, we need a new standard for the registry itself. The pattern is very similar to **ERC-7484** but is specialized for clear signing.

As far as I know, one of the issues with the proposals (including **ERC-7484**) is that it will be one of the first standards that implement non-deterministic attestations, which are directly used for other smart contracts. If we can agree on how attestation works for the registry, then we can move to write the actual standard for clear signing descriptors.

---

**mdaus** (2025-08-21):

[@lcastillo-ledger](/u/lcastillo-ledger)

Would it be possibe if the hardware wallet can support hashing the clear signing data?

If we can run checks at the smart contract level, we can avoid corrupted or replaced data in the pipeline.

