---
source: magicians
topic_id: 13885
title: "ERC-6900: Modular Smart Contract Accounts and Plugins"
author: adamegyed
date: "2023-04-19"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-6900-modular-smart-contract-accounts-and-plugins/13885
views: 16027
likes: 109
posts_count: 54
---

# ERC-6900: Modular Smart Contract Accounts and Plugins

A proposal for modular smart contract accounts and account plugins, which allow for composable logic. This proposal is compliant with ERC-4337, and builds on the existing work from ERC-2535 when defining interfaces for updating and querying modular function implementations.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6900)





###



Interfaces for smart contract accounts and modules, optionally supporting upgradability and introspection










https://github.com/ethereum/EIPs/pull/6900

Please note, this standard is still in the draft state, and will likely be significantly amended with the input of the community.

A software standard is only as useful as its ability to coordinate the development of different parties. We hope this standard can coordinate plugin developers with account developers to unlock the full potential of account abstraction.

## Replies

**fmc** (2023-04-19):

Thanks [@adamegyed](/u/adamegyed) for initiating this EIP!

Having a standard for AA-enabled wallets is crucial, and it is impossible without having standard for the wallets themselves.

I’ve been working on the architecture of what you call Validation Plugins for the last several days.

I have a couple of questions:

> When the function validateUserOp is called on an MSCA by the EntryPoint, it MUST find the user operation validator defined for the selector in userOp.callData

1. Where is it expected for MSCA to look for the operation validator address? do you suggest having some ‘selector=>validator’ registry?
2. If we’re using userOp.callData, to look for the validator address, we won’t be able to forward signature validation flow for the EIP1271 flow, as isValidSignature only operates with hash and signature.

What do you think of adding the validator address to the signature?

```auto
let signatureWithValidatorAddress = ethers.utils.defaultAbiCoder.encode(
        ["bytes", "address"],
        [signature, validatorAddress]
      );
```

and then decode it at `validateUserOp` or `_validateSignature`.

Like this:

```auto
(bytes memory moduleSignature, address authorizationModule) = abi
            .decode(userOp.signature, (bytes, address));

        if (address(modules[authorizationModule]) != address(0)) {
            return
                IModule(authorizationModule).validateSignature(
                    userOp,
                    userOpHash,
                    moduleSignature
                );
        } else {
            revert WrongAuthorizationModule(authorizationModule);
        }
```

it requires no registry as it expects a standard validation method interface.

In the case above it is

```auto
validateSignature(UserOperation, bytes32, bytes);
```

and it is compatible with `isValidSignature` like

```auto
function isValidSignature(
        bytes32 _dataHash,
        bytes memory _signature
    ) public view override returns (bytes4) {
        (bytes memory moduleSignature, address authorizationModule) = abi
            .decode(_signature, (bytes, address));
        if (address(modules[authorizationModule]) != address(0)) {
            return
                ISignatureValidator(authorizationModule).isValidSignature(
                    _dataHash,
                    moduleSignature
                );
        } else {
            revert WrongAuthorizationModule(authorizationModule);
        }
    }
```

That will allow MSCAs to verify signed messages for dapps with validation plugins.

This example above is for passing the signature validation flow to the plug-in (module) , however it is possible to validate not only the signature but the whole userOp (for the recurring payments and similar use cases) in the similar way

---

**jamesmccomish** (2023-04-19):

Is the idea that all non `updatePlugins` or `validateUserOp` functions are handled in a fallback?

Or would it be useful to have an `execute` function which handles routing to the appropriate plugin? Since we build on Safe there is already a fallback handler which could be edited, but it may be an unnecessary call.

---

**trinity-0111** (2023-04-19):

[@fmc](/u/fmc) thanks for the feedback.

> Where is it expected for MSCA to look for the operation validator address? do you suggest having some ‘selector=>validator’ registry?

MSCA must be able to find all functions (validation, execution, hooks) and their relationships in some form. For any incoming execution request, MSCA will need to look up the associated functions. Depends on the account implementation, a registry can be useful. That’s what I did in the sample implementation (coming soon).

> If we’re using userOp.callData, to look for the validator address, we won’t be able to forward signature validation flow for the EIP1271 flow, as isValidSignature only operates with hash and signature.

Are you treating `validateUserOp` as an execution function and forwarding data that way? It is doable, but can be very messy.

For `validateUserOp`, the recommendation is that the account implements it directly, can calls to validation plugins to do the actual validation. Accounts passes  `userOp, userOpHash`, and `userOpValidator` Plugin implementations can safely expect them as params.

Whenever you implement `userOpValidator`, make sure either implement an `runtimeValidator` that handles calls not directly from `EntryPoint` or disable that call path altogether.

---

**trinity-0111** (2023-04-19):

Thanks [@jamesmccomish](/u/jamesmccomish) for the feedback!

> Is the idea that all non updatePlugins or validateUserOp functions are handled in a fallback?

`updatePlugins` can certainly be handled in a fallback.

As for `validateUserOp`, as mentioned in the [above comment](https://ethereum-magicians.org/t/eip-modular-smart-contract-accounts-and-plugins/13885/4), it is recommended to be handled on the account directly, though it is doable in the fallback (can be very messy).

> Or would it be useful to have an execute function which handles routing to the appropriate plugin? Since we build on Safe there is already a fallback handler which could be edited, but it may be an unnecessary call.

The routing to appropriate plugins is expected to happen in the account level before the [4 steps](https://ethereum-magicians.org/t/eip-modular-smart-contract-accounts-and-plugins/13885/4) starts.

What you may need to think with `build on Safe` are:

- How can you add global hooks for execution functions?
- How can you add custom validation and hooks for execution functions?

---

**fmc** (2023-04-19):

> Are you treating validateUserOp as an execution function and forwarding data that way? It is doable, but can be very messy.

Nope, `validateUserOp` is not an execution function.

What I’m trying to say, is that if we have a module that validates signatures via some alternative algorithm (say passkey module), we may want to sign messages to verify them via `isValidSignature` via same alternative algorithm.

In this case, we will need `isValidSignature` on the MSCA to understand where to forward this signature validation flow to, and it only can take it from `signature`.

I realize, that we can have different flows, like

- For the AA flow we get the operation validator plug-in address from the callData
- For the EIP-1271 flow we take get the operation validator plug-in address from the signature

but it can be confusing.

---

**rmeissner** (2023-04-19):

Happy to see that discussions around this topic start. In my opinion it would have been nicer if the ERC would not enforce a specific proxy (e.g. currently the Diamond Proxy). The choice of a proxy depends on your use case and therefore a standard a standard that is agnostic to the proxy would be more widely applicable.

I would be interested in more details how hooks are designed. For example the Safe currently has a similar concept called Guards and it would be interesting to see the differences.

> What do you think of adding the validator address to the signature?

Imo it should not be up to the signer, but the account what validator should be used. But this depends on the setup of the account (i.e. is there 1 address that fully controls the account, than there is no issue with this approach).

There is been some work around this also in conjunction with the Safe and the approach there was to enforce EIP-712 and then route the signing validation based on the domain separator. This allows high security guarantees. An WIP example can be seen here: [safe-contracts/contracts/handler/extensible/SignatureVerifierMuxer.sol at merged-efh-sigmuxer · rndlabs/safe-contracts · GitHub](https://github.com/rndlabs/safe-contracts/blob/merged-efh-sigmuxer/contracts/handler/extensible/SignatureVerifierMuxer.sol#L99-L139)

---

**fmc** (2023-04-20):

Totally agree with not enforcing a specific proxy pattern!

> Imo it should not be up to the signer, but the account what validator should be used.

Yep, ideally it is the account that should decide, what validator to use.

However, if we consider, some SDK/dApp as a part of the account, it can decide what module address to append to the signature based on how this signature (or any other validation information) has been obtained from the signer.

It can be cheaper and easier than performing this search on-chain.

> There is been some work around this also in conjunction with the Safe and the approach there was to enforce EIP-712 and then route the signing validation based on the domain separator.

Thanks for the link ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**fmc** (2023-04-20):

> When the function validateUserOp is called on an MSCA by the EntryPoint , it MUST find the user operation validator defined for the selector in userOp.callData

Also, does this mean that there is only one operation validator at a time defined for a given method of the Smart Account?

Let’s say, there is a method `execute(address dest, uint256 value, bytes calldata func)` that just calls an external smart contract on behalf of MSCA

Does it mean, that for all the calls with `execute.selector` in `userOp.calldata` there will be the same operation validator?

---

**jamesmccomish** (2023-04-20):

From how I see it, you could have different validators for the same executionSelector.

The ExecutionUpdate struct allows for an array of AssociatedFuntions, so based on some conditions in validateUserOp you could select which implAddress/implSelector you want.

I guess it depends on how the plugin information is stored… but like you asked above, I think I’ll go for some mappings in the MSCA. Could be worth standardising that storage into some IPluginManager interface so dapps could easily check if particular plugins are enabled

---

**kopykat** (2023-04-20):

While the rhinestone team has been initiating open discourse about modularising ERC-4337 with multiple teams working in the space and we have been looking to push the space forward in a positive sum way, we feel that this EIP does not aim to start a conversation about this topic but is rather a way for the authors to further their own reputations.

The main reason we have for thinking this is that the EIP is clearly very heavily inspired by the work we did during the ETHDenver hackathon, yet fails to attribute or even mention our project ([GitHub - kopy-kat/ethdenver-aa: Account Abstraction Project for ETHDenver](https://github.com/kopy-kat/ethdenver-aa)). During the hackathon we built the (to our knowledge) first implementation of ERC-4337 using the Diamond Proxy Standard.

It is obvious that this EIP takes inspiration from our code for several reasons, most notably because it exactly follows our peculiar naming convention exactly and repeats many of the errors and security vulnerabilities present in our proof of concept.

Unlike Safe, who call their extensions modules, or ERC-2535, who call them facets, this EIP has chosen to call them plugins, naming that we hadn’t seen in solidity before we chose it. Further, while the extensions are called plugins, the functions that call them are called hooks, a name inspired by frontend libraries and that is completely absent in other solidity contracts today. Further, our names for the specific hooks, such as preExecution and postExecution have equally been retained exactly by the authors.

Unlike ERC-2535, which stores function selectors in a mapping, this EIP has chosen to use arrays, something that we had done during the hackathon but is, on second thought, a very suboptimal implementation. Perhaps most interestingly, during the hackathon we were unable to finish testing our implementations of the hooks, so they are left blank on the public GitHub repo. It seems that rather than trying to figure out our intentions and planned implementation of these hooks, the authors just left them out of the EIP, perhaps hoping for others to tell them how to implement these.

Since we have been working on improving the code we had written during ETHDenver over the last month, there are many design choices that we have now revisited in order to make a modular implementation of ERC-4337 using diamond Proxies viable to be used in production. As stated above, we are happy to share our progress in public in order to propel the space forward and have already done so with select teams. However, because we are not yet confident in the security guarantees of our code, we have for now kept most of it internal and are planning on releasing it, together with detailed explanations of our design choices and extensive testing, at a later date.

Due to the numerous “coincidental” similarities to our code, examples of which were given above, but the clear lack of attribution or even mention of the rhinestone project, we feel like this EIP does not aim to create and improve public discourse around modular ERC-4337 in a positive-sun way and hence we will abstain from commenting and pointing out the numerous flaws that we have since discovered in our original code, most of which have been repeated in this EIP.

---

**noam** (2023-04-24):

We want to quickly address the above comment, which we’ve attempted to mediate directly, in a public comment and then move towards focusing discussions on technical criteria and improvements.

1. Our motivation for creating this EIP is not to “further our reputations” and indeed an EIP is not a vehicle to do that. We see contract accounts as an absolute requirement to get 1B people on crypto rails, and to that extent we’re pushing things forward where we can, including standards, open source software, and developer products. Standards specifically streamline the ecosystem, maximize developer leverage, minimize fragmentation and developer lock-in, and allow more cohesion in moving the space forward.
2. We were actually entirely unaware of Rhinestone when publishing. We reached out to engage the Rhinestone team as soon as a community member flagged the similarities. It’s actually cool to see convergence in design here. That generally means as a collective group we’re trending in the right direction. That said, similarities are a large step from copies - we demonstrated live to the Rhinestone team the history of how we landed at this conclusion after months of iteration. Nomenclature like “plugins” and “preExecution” are not unique to either this standard or Rhinestone’s implementation and are canonical and intuitive terms to capture the intended meaning.
3. The reason we moved our internal discussions into a public forum is to engage in the discourse and discussions, such as the ones from @rmeissner, @fmc, and @jamesmccomish, that forces us to either justify our design decisions or incorporate feedback and adapt the design. To that point, all decisions in the standard now have been prototyped and battle tested internally, and we have not seen counter arguments to standard specifications - including when we presented these “error laden” decisions to the Rhinestone team.
4. We’d been hoping to reach a resolution directly with the Rhinestone team, but unfortunately the asks they were making were not appropriate for this EIP or any other. Specifically, the two asks are:

a) Calling out Rhinestone in the EIP abstract. EIPs are not a vehicle for products or teams to gain relative standing or distribution. This is a conscious decision to maintain neutrality in standards for an open decentralized platform, and to that extent Alchemy is not mentioned a single time in the EIP, and we reference examples we researched in design where appropriate in the context of the specification.

b) Adding a Rhinestone author to the EIP authorset. We plan on collaboratively defining a set of criteria for expanding the author set that we can apply equally to everyone. We’ll share those in the TG facilitating these discussions next week, but can’t create special cases. That’s not to say Rhinestone doesn’t or won’t eventually qualify based on these criteria but we need a system that is uniform and applies equally to everyone in the community based on contributions and body of work. Working on parallel implementations that result in similarities to the standard likely don’t suffice and aren’t sufficient constraints on growing the authorset responsibly.

Taking a step back here: the goal is to provide an open standard that streamlines development and maximizes outcomes for the ecosystem. The goal here is not to assume individual ownership of this standard, use it to promote teams or products, or otherwise bias it towards a particular entity. To make sure that we’re able to do this, we need to enforce an equal process for each stakeholder and a conscious mitigation of any brand and product associations.The TL;DR of this situation:

1. We unequivocally did not copy work, and demonstrated our methodology to the Rhinestone team.
2. To that point this work is now in the public domain and should be owned by the ecosystem.
3. This is not a zero sum game, and the most outsized outcome will be a result of everyone working together, agreeing on scope, charter, and process, and pushing this forward in a timely manner.
4. This is not a vehicle for products or teams to gain standing or distribution.

Moving forward, let’s keep the discussions on Eth Magicians and similar public forums focused on technical discussions. There’s an open Telegram group as well to facilitate higher bandwidth conversation, per suggestion from the Rhinestone team. We’re always happy and available to chat with any teams directly on other matters.

---

**kopykat** (2023-04-24):

I fully agree with your point that this discussion should be reserved for comments on this EIP, so I think it makes sense to leave it at this. However, we also don’t want any misrepresentations to hang around so I just wanted to briefly clarify a few points:

Primarily, the asks that you mention were in fact **not our asks, but your suggestion** on the call with myself, you (Noam), Adam and Fangting (all from the Alchemy team) on Friday April 21. After discussing your proposal to add me as co-author and referencing our code from ETHDenver in exchange for removing my comment above, my team agreed to this and informed you over the weekend. After this you changed your mind, said this was no longer an option and followed up with this comment.

My understanding was that our discussions were centred around collaboration and clearing the air between us, not promoting rhinestone, so this comment is disappointing.

We are committed to building modular AA in the open and ensuring it is valuable to all in the ecosystem (as seen in the telegram conversations [Telegram: Join Group Chat](https://t.me/+KfB9WuhKDgk5YzIx)). However, as I pointed out on the call, we do not think that it is beneficial for the ecosystem to try to enshrine a specific implementation of modular AA as a standard, but we should rather aim to standardise interfaces for modules and how they interact with smart accounts, allowing for a diverse set of implementations to exist. We have initiated discussion about this in the group chat and will move some of the arguments into this forum should that be useful in the future.

---

**mudgen** (2023-04-26):

I looked at the standard and in general I like it and I think it is a great idea. In order to leverage the EIP-2535 Diamonds community and its tooling, interoperability and documentation I think it would be great, if possible, to make the smart contract accounts compliant with EIP-2535 Diamonds.

Making it compliant with EIP-2535 Diamonds may be easier than first considered.

The upgrade function `diamondCut` specified in EIP-2535 Diamonds is optional so smart contract accounts would not have to implement that and the standard allows other custom or standardized upgrade functions to be used like `updatePlugins`.

The EIP-2535 Diamonds standard only requires that the `DiamondCut` event be emitted and the four `IDiamondLoupe` read-only functions be implemented. The standard requires these for interoperability and interfacing with tooling and other software, for example [louper.dev](https://louper.dev/). A great article on EIP-2535 Diamond compliance is here: [Compliance with EIP-2535 Diamonds Standard](https://eip2535diamonds.substack.com/p/compliance-with-eip-2535-diamonds)

It seems possible to me that a smart contract account could implement the `IPluginLoupe` interface and `IPluginUpdate` interface other interfaces defined by the smart contract account EIP as well as implement the `IDiamondLoupe` interface and emit the `DiamondCut` event when adding/replacing/removing functions.

I would love for EIP-2535 Diamonds and this smart contract accounts EIP to work together.

---

**cejay** (2023-04-30):

“EIP: Modular Smart Contract Accounts and Plugins” is generally feasible!

But I think there are several points that may need attention:

1. add/remove Hook plugins may need to be divided into two parts:
For example: 1. add plugin → 2. wait for a security time delay (e.g. 48 hours) → 3. user confirms that the plugin has been added.At least the implementation in soulwallet is like this, this is mainly for security reasons, for full context see the previous discussion with the author of ‘EIP-2535 Diamonds’ mudgen at here . So for us only PluginAdd function is not enough, at least a PluginPreAdd similar process is needed, and this process for monitoring purposes, will also emit event
2. validateUserOp because it will be called at high frequency, so we need to consider the ‘gas efficiency’, in our consideration for the time being will be validateUserOp logic fixed in the contract (rather than through the plugin way to achieve), later if user need to upgrade the logic of validateUserOp, the user can update the ‘proxy contract’->‘logic contract’ address pointer(lower gas).
3. I think MSCA implicitly aims to create a set of standards that any standard-compliant SCA can use any standard-compatible frontEnd (users don’t need to rely on ‘ONE’ frontEnd only), while the signature assembly and verification process often differs from one SCA to another (gas efficiency first｜stability first｜code readability first… etc.), I’m thinking that this area could be a major challenge for MSCA implementation.

---

**fmc** (2023-05-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cejay/48/9815_2.png) cejay:

> validateUserOp because it will be called at high frequency, so we need to consider the ‘gas efficiency’, in our consideration for the time being will be validateUserOp logic fixed in the contract (rather than through the plugin way to achieve), later if user need to upgrade the logic of validateUserOp, the user can update the ‘proxy contract’->‘logic contract’ address pointer(lower gas).

Can you elaborate on this topic please, and/or drop code examples from Soul Wallet repo?

---

**adamegyed** (2023-05-10):

Hi everyone, I’m happy to check in on this thread and provide an update on this proposal’s progress. There is now an updated and merged draft of the proposal on the main EIP site:

https://eips.ethereum.org/EIPS/eip-6900

The current draft is a response to the helpful and engaged dialogue happening here and on the related telegram channel. The feedback so far has pointed to some concerns about the the multi-facet proxy approach and interfaces, particularly in the context of where storage can feasibly reside. We’ve revised the EIP to be more explicitly agnostic in its approach to proxies and interfaces — this version allows for (but no longer requires) ERC-2535 style ‘delegatecall’ operations as the basis for execution.

This change has had a number of implications for security, interoperability, plugin management, and other issues that we’re currently exploring through research and development. In particular, we’re currently working on a library to address some of the storage limitations for plugins when using `call`. (In more detail, this library would aid in storing bulk data within an account’s associated storage, allowing for “nested” mappings and dynamic arrays).  We are also working on benchmarking some of the implementation options allowed by the new spec, and on developing a reference implementation. We look forward to sharing the results of that work in the coming weeks.

In the meantime, we’d be very grateful for your perspectives on some key unanswered questions that we’re also working on. First, interfaces: the changes we’ve made to `IPluginUpdate.sol` and `IPluginLoupe.sol` have made them more flexible, but with some tradeoffs in complexity. Are there implications for this approach that we haven’t yet discussed? We would appreciate your feedback in either implementing an account or writing plugins for modular accounts.

Second, changing the interaction flow from accounts to plugins to use `call` instead of `delegatecall` requires both standardizing execution and explicitly allowing for multiple validator functions on the same execution function. These are additional changes to the spec that we’re considering, while also weighing the costs of added complexity. Thank you to [@fmc](/u/fmc) for the suggestion on self-identifying signatures, that strategy (or a similar one in calldata) can provide the flexibility needed to adopt these changes. We would appreciate any additional insight into what baseline features execute function(s) should have.

Also, at this time I’d like to introduce [@JasonW](/u/jasonw) to the ERC-6900 author team. He will be helping with research and organization, making sure this standard is the best it can be and enabling community members to become contributors.

---

**fmc** (2023-05-11):

Thanks, Adam, glad to hear my suggestion has been helpful.

Here are the links to the wip implementation of this strategy: [Smart Account](https://github.com/bcnmy/scw-contracts/blob/Ownerless-SA-Auth-Modules-hardhat-deploy/contracts/smart-contract-wallet/SmartAccount.sol) and [sample EOA Ownership Module](https://github.com/bcnmy/scw-contracts/blob/Ownerless-SA-Auth-Modules-hardhat-deploy/contracts/smart-contract-wallet/modules/EOAOwnershipRegistryModule.sol) following Associated Storage requirements.

Excited to hear about the library that addresses storage limitations for plugins when using `call`! Let me know if you need any assistance with r&d of it

---

**cejay** (2023-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fmc/48/5774_2.png) fmc:

> Can you elaborate on this topic please, and/or drop code examples from Soul Wallet repo?

must of discussion at the link above. In terms of adding and removing plugins, we think it’s slightly different. We think it’s more important for the user to have the wallet address ‘forever’, but plugins pose a security risk, for example, if a hacker steals your private key, can the hacker modify the storage by adding a plugin ( This would make the social recovery function unavailable), and we are trying to make the social recovery always available if the user is concerned

---

**adamegyed** (2023-05-26):

Hi everyone - thank you everyone who has continued to work with us on this proposal. We wanted to give an update to bring everyone up to speed on some of the design decisions we’re considering as a result of these conversations, including open areas we’re still working through.

We’re still in the process of formalizing the wording around this proposed change, and would like to get feedback and and bring the community into the decision process around these changes. The current draft is viewable here:


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [GitHub](https://github.com/alchemyplatform/EIPs/compare/comparison-base...alchemyplatform:EIPs:spec-update-1)



    ![](https://opengraph.githubassets.com/802798b72ad66f0c37ebea09f7023d41d85d8e4b2e78792627700c48cab92f1f/alchemyplatform/EIPs)

###



The Ethereum Improvement Proposal repository. Contribute to alchemyplatform/EIPs development by creating an account on GitHub.










We’re still actively seeking collaboration and co-authorship in order to make this as useful as possible for the ecosystem. Please reach out if you want to work together on this proposal!

## Proposed updates to the spec

The biggest change we’ve been testing is the idea of updating all function invocations, including execution functions, validation functions, and hooks, to use `call` instead of `delegatecall`. This isolates storage and execution code to be per-plugin, preventing accidental or malicious storage overrides across plugins and fundamentally changes the plugin trust model.

- To preserve the capabilities of modular accounts to make arbitrary external calls, we introduce two standardized execution functions to ERC-6900, grouped together in a new interface IStandardExecutor. The two functions are execute and executeBatch, taking the same names as the functions from ERC-4337’s SimpleAccount but with new parameters.
- These functions become necessary to provide through the standard when moving from delegatecall to call, because otherwise every single new contract interaction target would need to be added as a new plugin.
- The IPlugin interface (with the method pluginStorageRoot()) would be removed, due to the changes in storage management no longer necessitating this.

We propose consolidating global hooks and regular hooks into one concept called “hook groups”. Hook groups have each hook type as an optional field, and accounts must maintain an association between execution functions and which hook groups apply for the execution function. This addresses a comment from [@dror](/u/dror) on how postExecHooks can take in data parsed from a preExecHook to reduce the number of calldata copies.

We propose a new hook type, pre-validation hooks, that run before either a user op validator or a runtime validator. The intended use case for these hooks is permission checking and similar pre-transaction checks that are not related to signature validation itself.

- With the new storage model, it is possible to limit the blast radius of unverified validation and execution plugins using pre-validation hooks. These hooks can scope which external contracts or what parameters a given function is using.
- The code implementations and storage of these two contracts are independent, which allows for independent security assessments to be valid. E.g. a formally verified permissions plugin can limit an unverified validation plugin.

Plugin Loupe functions have been scoped down to reduce implementation overhead. We are actively looking for feedback in this area, as it affects the implementation process for off-chain entities.

## Tradeoffs we’re considering

The current plugin update function (`updatePlugins` in `IPluginUpdate`) allows for “slim” updates that only specify the fields that actually need to be set. This is done by using only the minimum number of array fields needed to express the desired plugin configuration, specifying function types using the defined enums and omitting any function types that aren’t used.

- This allows, for example, a function that only has a user op validator and an execution function to not need to specify anything for other fields, like hook groups or a runtime validator. This reduces calldata size when the other fields are not needed.
- However, this requires all function references to be casted as bytes24. This is what Solidity internally uses as the ABI-encoded type, but requires casting back to a function (or unpacking into address + selector) to perform the call. It might be possible to change the interface to take in function types in the struct (i.e. declare a struct as follows), but doing so would require defining new structs for each function type:

```solidity
struct UserOpValidatorUpdate {
    PluginAction action;
    function(UserOperation calldata, bytes32) external validatorFunction;
}
```

With hooks passing data from preExec to postExec, it now requires a pairwise association with across each, to be able to track which preExecHook returned data should be sent to which postExecHook. However, with the introduction of preValidate hooks, it is unclear exactly what the data flows should look like, if any.

- The group association is still valuable with the new hook types, as some preValidation hooks will want to defer state updates until execution. For example, preValidate hook that enforces an ETH spend limit will not want to perform the state update for tallying up ETH used by a key during the validateUserOp step. That should be avoided because in the case that execution reverts, the validation step will not be reverted, resulting in the spend limit usage increasing without an actual spend. For this reason, a preHook that performs the state update should be used.

Specifying the intended validator in the calldata of the standard execute functions limits the custom validation routing to just those two functions. This reduces the account-internal storage requirements (how the mappings and/or arrays look) for ERC-6900 implementing accounts. As an alternative, [@fmc](/u/fmc) has suggested specifying the validator in the signature. We’re leaning towards not taking this direction to limit the scope of required validator storage in the modular account, but if there’s interest and a compelling reason to move it into the signature field, we can make that change.

## PluginStorageLib

We’re still hard at work on testing and securing a reference implementation. In the meantime, we’ve realized there are some common components that many plugin developers will need to create when developing using the new `call` model that they did not need to do under the previous `delegatecall` model, specifically around designing storage layouts that abide by the [account-associated storage rules of ERC-4337](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-4337.md#storage-associated-with-an-address).  To aid in developing these plugins, we’re sharing the first version of PluginStorageLib - a solidity library that presents account associated storage as one giant `(bytes32 => bytes)` mapping, allowing for both nested mappings and dynamic arrays in associated storage. This is intended for singleton plugin contracts to have storage per-account.



      [gist.github.com](https://gist.github.com/adam-alchemy/9a2cdde12ece0467c88fcb4e897d124b)





####



##### PluginStorageLib.sol



```
/// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

/// @title Plugin Storage Library for ERC-4337 Address-associated Storage
/// @author Adam Egyed
/// @notice This library treats storage available to associated addresses as one big global mapping of (bytes32 => bytes).
///
/// THIS IS HIGHLY EXPERIMENTAL AND NOT READY FOR PRODUCTION USE.
///
/// It is up to the implementer to define the serialization and deserialization of structs,
```

   This file has been truncated. [show original](https://gist.github.com/adam-alchemy/9a2cdde12ece0467c88fcb4e897d124b)










This is an unaudited library intended only as a starting point for plugin development. DO NOT USE THIS IN A PRODUCTION ENVIRONMENT. It requires custom serialization and deserialization for data stored, and care when designing key derivation schemes (i.e. protecting from manufactured key collisions).

We hope this can help explain and potentially alleviate some of the tradeoffs of switching from `delegatecall` to `call`, and look forward to feedback on its implementation and usage.

## Conclusion

These proposed changes to ERC-6900 need to involve community input. Please feel free to leave comments and let us know what you think!

---

**fmc** (2023-05-26):

Very happy to hear about the pivot from delegatecall to call.

Can’t wait get my hands dirty with the Plugin Storage lib!

Meanwhile, msged you on Telegram regarding contributing to the proposal.


*(33 more replies not shown)*
