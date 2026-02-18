---
source: magicians
topic_id: 9907
title: "EIP-5219 Discussion: Contract Resource Requests"
author: Pandapip1
date: "2022-07-11"
category: EIPs
tags: [http]
url: https://ethereum-magicians.org/t/eip-5219-discussion-contract-resource-requests/9907
views: 3657
likes: 4
posts_count: 35
---

# EIP-5219 Discussion: Contract Resource Requests

https://github.com/ethereum/EIPs/pull/5219

## Replies

**hskang9** (2022-07-21):

I think the proposal is grammatically incorrect. What does “decentralized” mean in this proposal when you are eventually sending http request already to a pre-occupied RPC node? Isn’t this just worthless when we already have http connection physically on top of TCP? Why would you make another http on http itself?

---

**Pandapip1** (2022-07-21):

What I mean is that you are “sending” an HTTP-*like* request to a smart contract. Yes, it’s not a true HTTP request, and will likely involve using actual HTTP to connect to an RPC.

This EIP is all about being able to access smart contracts as if they were websites / HTTP servers.

---

**hskang9** (2022-07-23):

If you mean that, I think you have to eventually add a new RPC endpoint to Ethereum node as smart contract communicates with ABI. If RPC logic processes the Post method with request url then generate function signature then it would work. but it is definitely not smart contract that needs to be changed.

---

**Pandapip1** (2022-07-23):

This proposal is very similar to [EIP-4804: Web3 URL to EVM Call Message Translation](https://eips.ethereum.org/EIPS/eip-4804) (which I was unaware of when I was writing this EIP). An HTTP request to a smart contract actually just calls a view function of that smart contract. It doesn’t actually change anything about smart contracts (which is why this is an ERC, not a Core EIP!)

---

**hskang9** (2022-07-23):

Yeah but it is core EIP.  You need to check the tech. If this is going to work, the contract has to not mark itself as sender when calling other contracts. Finding that this is similar to EIP-4804, Isn’t this an reiteration of it, and plagiarism? You should have included this in your reference, otherwise you are stealing their idea.

---

**hskang9** (2022-07-23):

```auto
This proposal is very similar to EIP-4804: Web3 URL to EVM Call Message Translation 1 (which I was unaware of when I was writing this EIP). An HTTP request to a smart contract actually just calls a view function of that smart contract. It doesn’t actually change anything about smart contracts (which is why this is an ERC, not a Core EIP!)
```

EIP-4804 is just giving an idea of entrypoint string where a parser can parse those urls into rawCall form. It does not specify whether it is an Core EIP. Your rebuttal is grammatically incorrect. You are also misunderstanding the concept of HTTP. HTTP is a protocol to parse raw byte data from a sending computer to do something, not a view function. Your assumption that your “HTTP” call can be a view function is wrong, as the call can actually alter the state of a contract(e.g. ERC20 transfer). Stop glorifying terms like “HTTP” or “Decentralized” and start studying definition of it. Make logical sentences based on its use cases and background. period.

---

**hskang9** (2022-07-23):

After you understand:

1. how view function and other contract functions differ
2. how to clarify your “HTTP” with vs EIP-4804 and its network sequence or logic flow in Ethereum state machine
3. how to really implement your EIP in the real code
4. how to clarify “decentralization” or compare with “usability”
5. why plagiarism is bad and reference is good

We can proceed with productive discussion. More intellectual effort without feelings is required for this.

---

**Pandapip1** (2022-07-24):

1. I am aware enough of how they differ. View functions are unable to make state-changing transactions, but their return value can be determined without needing to submit a transaction. I will not pretend I know everything about view functions, but I believe that I know enough. If there is a specific concern here, please state it.
2. I should repeat: I learned about of EIP-4804 yesterday, while I was watching the latest URL/URI specs meeting. I have not yet had the time to update my EIP to add a comparison.
3. I have described it in the specification. Is this interface sufficient? If not, may you please suggest an improvement?
4. I consulted with another editor (@MicahZoltu) and he said “[the EIP describes something] closer to RESTful contract calls.” While that’s not entirely what the intent is (there’s only one function here that could be called), I would be okay with a name change. What would be your suggestion?
5. I agree that plagiarism is bad. The EIP process is a bit special, however, in that work that informed the design decisions of the EIP shouldn’t be referenced (source). This is not plagiarism.

---

**Pandapip1** (2022-07-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> EIP-4804 is just giving an idea of entrypoint string where a parser can parse those urls into rawCall form. It does not specify whether it is an Core EIP. Your rebuttal is grammatically incorrect. You are also misunderstanding the concept of HTTP. HTTP is a protocol to parse raw byte data from a sending computer to do something, not a view function. Your assumption that your “HTTP” call can be a view function is wrong, as the call can actually alter the state of a contract(e.g. ERC20 transfer). Stop glorifying terms like “HTTP” or “Decentralized” and start studying definition of it. Make logical sentences based on its use cases and background. period.

1.

> EIP-4804 is just giving an idea of entrypoint string where a parser can parse those urls into rawCall form. It does not specify whether it is an Core EIP. Your rebuttal is grammatically incorrect.
> EIP-4804 is objectively not a core EIP. Its category is ERC: ERC-4804: Web3 URL to EVM Call Message Translation. Core EIPs are generally EIPs that require a hard fork. I’m sorry I misunderstood you, I thought that you were saying I was changing the way that smart contracts work.

1.

> ou are also misunderstanding the concept of HTTP. HTTP is a protocol to parse raw byte data from a sending computer to do something, not a view function.

I understand what HTTP is. Throughout the draft, I very explicitly mention that this allows sending “HTTP-*like*” requests. Here are all the relevant instances of the string “HTTP” in the PR diff:

```auto
EIPS/eip-5219.md
L3: title: Decentralized HTTP
L4: description: Allows the sending of HTTP-like requests to smart contracts
L16: ... To solve these issues, this EIP introduces an interface allowing "Web3 Browsers" to make HTTP-like requests (containing a method, a resource to request, a request body, and headers) to smart contracts, and to receive HTTP-like responses (containing headers and a body).

assets/eip-5219/IDecentralizedApp.sol
L5: /// @notice                     Send an HTTP-like request to this contract
L6: /// @param  method              The HTTP method to use (e.g. GET, POST, PUT, DELETE)
```

1.

> Your assumption that your “HTTP” call can be a view function is wrong, as the call can actually alter the state of a contract(e.g. ERC20 transfer).

I am well aware of this issue. I will point to the relevant section from the draft:

```md
The `request` method was chosen to be readonly because all data should be sent to the contract from the parsed DApp. Here are some reasons why:

- Submitting a transaction to send a request would be costly and would require waiting for the transaction to be mined, resulting in quite possibly the worst user-experience possible.
- Complicated front-end logic should not be stored in the smart contract, as it would be costly to deploy and would be better ran on the end-user's machine.
- Separation of Concerns: the front-end contract shouldn't have to worry about interacting with the back-end smart contract.
```

I am well aware that the HTTP `PUT`, `POST`, `PATCH`, and `DELETE` methods are very typically state-changing. And technically, the following is a valid return value according to the current draft:

```auto
statusCode: 303
body: web3://
resultHeaders: []
resultHeaderValues: []
```

Which then prompts the wallet to submit a transaction. Simple, and allows for all use-cases to be covered with a single view function.

4.

> Stop glorifying terms like “HTTP” or “Decentralized” and start studying definition of it.

HTTP: HyperText Transfer Protocol. I can’t think of a rigorous definition off the top of my head, but for the purposes of this EIP it suffices as a way to request data from another computer. In this EIP, “another computer” can be a smart contract instead. (The chain is deliberately left unspecified so that implementations can feel free to include every chain the user has added).

Decentralized: No single entity (where entity depends on context) has the power to significantly affect the thing that is being described. In this case, entity refers to a person, a company, or an Ethereum address other than the ones responsible for name resolution.

Again, the name of HTTP makes it explicit that the RFC is about the *transfer* of information. State-changing operations are a happy side-effect and are not needed to create a functional replacement for it.

---

**Pandapip1** (2022-07-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> Yeah but it is core EIP. You need to check the tech. If this is going to work, the contract has to not mark itself as sender when calling other contracts. Finding that this is similar to EIP-4804, Isn’t this an reiteration of it, and plagiarism? You should have included this in your reference, otherwise you are stealing their idea.

1.

> Yeah but it is core EIP. You need to check the tech.

No, it is not a Core EIP:

```md
- A **Standards Track EIP** describes any change that affects most or all Ethereum implementations, such as—a change to the network protocol, a change in block or transaction validity rules, proposed application standards/conventions, or any change or addition that affects the interoperability of applications using Ethereum. Standards Track EIPs consist of three parts—a design document, an implementation, and (if warranted) an update to the [formal specification](https://github.com/ethereum/yellowpaper). Furthermore, Standards Track EIPs can be broken down into the following categories:
  - **Core**: improvements requiring a consensus fork (e.g. [EIP-5](./eip-5.md), [EIP-101](./eip-101.md)), as well as changes that are not necessarily consensus critical but may be relevant to [“core dev” discussions](https://github.com/ethereum/pm) (for example, [EIP-90], and the miner/node strategy changes 2, 3, and 4 of [EIP-86](./eip-86.md)).
  ...
  - **ERC**: application-level standards and conventions, including contract standards such as token standards ([EIP-20](./eip-20.md)), name registries ([EIP-137](./eip-137.md)), URI schemes, library/package formats, and wallet formats.
```

EIP-4804 explicitly has the `ERC` category:

```md
type: Standards Track
category: ERC
```

I’ve already discussed that however, so I will move on,

1.

> If this is going to work, the contract has to not mark itself as sender when calling other contracts.

It can’t call other contracts, except for view ones, where `msg.sender` is undefined or meaningless anyways.

1.

> Finding that this is similar to EIP-4804, Isn’t this an reiteration of it, and plagiarism?

Independently creating a work that is similar to another work that has already been created is something that happens. In fact, [there’s an entire Wikipedia article about it!](https://en.wikipedia.org/wiki/Multiple_discovery)

1.

> You should have included this in your reference, otherwise you are stealing their idea.

This is straight-up false. See [Add an optional `relates-to` preamble key · Issue #5274 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/5274#issuecomment-1193049343) for more information. Note that all EIPs are licensed under CC0-1.0.

---

**hskang9** (2022-07-24):

1. You do not understand that your “http” request can also change states in other contracts and claims that your every “http” request is processed as view function. I gave you this question to rethink, but it seems you dont.
2. Learning this yesterday does not mean that you don’t put reference. You put this asap.
3. Unnecessary, headers are not really needed and you do not put any specification on some of the interfaces. You just copy/pasted http request in solidity. You need to remove unneeded properties as this is the protocol on top of HTTP. Also, as I repeat, if you are going to send through http request interacting with that contract, the sender is marked as the interacting contract, not the original sender. If each dapp provider can make a custom controller contract with the interface and some custom library on top of ethers.js or web3.js to interact with the contract with function signature, it would be feasible. If there is one-stop solution, it is definitely change in Core RPC.
4. The term “decentralized” must be removed. The term is just showing one’s unprofessionalism to describe their ideas and show their low commitment hidden with it. I suggest “REST-compatible smart contract interface for usability”.
5. I am not sure about this as each EIP is protected with Creative Commons(CC) license. I think you still need to refer the previous works.

Now that answering 4), I suggest you refer your interface not “http”. Rather “RESTful” interface is better fit as [@MicahZoltu](/u/micahzoltu) refers.

---

**Pandapip1** (2022-07-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hskang9/48/1151_2.png) hskang9:

> You do not understand that your “http” request can also change states in other contracts and claims that your every “http” request is processed as view function. I gave you this question to rethink, but it seems you dont.

1. I very explicitly stated exactly why I am not allowing state-changing modifications in this EIP. Unless someone provides me with a solution I deem better, I will have the function remain a view function.
2. The rules are explicit, and I will only put the reference there if they can be. As of right now, they cannot be.
3. There’s a lot to unpack here.

> Unnecessary, headers are not really needed and you do not put any specification on some of the interfaces.

I could get behind removing the headers. I personally kept them in for one reason: to keep the spec more backward-compatible with real HTTP. **I agree that this could use more discussion.**

> You just copy/pasted http request in solidity.

Objectively false, but I accept the compliment nontheless.

> Also, as I repeat, if you are going to send through http request interacting with that contract, the sender is marked as the interacting contract, not the original sender.

**There is no reliable msg.sender when you are dealing with view functions anyways.**

> If each dapp provider can make a custom controller contract with the interface and some custom library on top of ethers.js or web3.js to interact with the contract with function signature, it would be feasible.

I’m not sure I understand you, but I believe that is roughly what I am proposing,

> If there is one-stop solution, it is definitely change in Core RPC.

Core != RPC. In fact, RPC version changes specifically fall into the `Interface` category. I originally had the EIP listed as an Interface EIP, but it was determined that the content of the EIP meant that it was better categorized as an ERC.

1. Using a term correctly is not a sign of unprofessionalism. However, I will consider that title, as at least one other person has suggested a similar one.
2. CC0 does not require attribution: CC0 FAQ - Creative Commons.

---

**hskang9** (2022-07-25):

1. You do not define Ethereum here. It is not you allowing state-changing modifications. It is EVM to decide. Not you. You need to understand world does not revolve around you and this technology does not rely on trust on you nor someone you look for to have enough trust. This technology exists because of cryptographic proof. Read and understand the code. How is all other PUT, DELETE, POST request processed as view function? Your proof that all requests are processed in view function is delusional in that you do not provide enough detail on how the request is processed in EVM but just specify result message from it. You just do not allow state-chainging modifications because you do not want to get criticized. This is the reason why you do not get attention. This explanation is just unacceptable.
2. You confirm yourself that you do not put reference on EIP-4804, because you simply don’t want to.
3. A lot to unpack here.

```auto
I could get behind removing the headers. I personally kept them in for one reason: to keep the spec more backward-compatible with real HTTP. I agree that this could use more discussion.
```

3-1) To correct your perspective, real HTTP is already working in the background, so there is no such thing as backward compatibility. You are making a protocol on top of HTTP. I seriously recommend to take CS course around Coursera or just watch a youtube video briefly describing it before having discussion.

```auto
Objectively false, but I accept the compliment nontheless.
```

3-2) Objectively true, there are headers and most of required properties in HTTP data structure, and you said that you are saying that you are keeping backward compatibility.

```auto
There is no reliable msg.sender when you are dealing with view functions anyways.
```

3-3) Fair point. but what about your oxymoron that state-changing methods that you say it is processed “well”?

```auto
I’m not sure I understand you, but I believe that is roughly what I am proposing,
```

You never proposed nor understood anything on your proposal.

```auto
Core != RPC. In fact, RPC version changes specifically fall into the Interface category. I originally had the EIP listed as an Interface EIP, but it was determined that the content of the EIP meant that it was better categorized as an ERC.
```

I am not sure if I understood this from your “special” perspective, but Core == RPC when RPC involves getting Core data(e.g. DB).

1. You used term wrong. you showed unprofessionalism. This EIP is about RESTful, but this is not related to decentralization at all.
2. Ok

---

**Pandapip1** (2022-07-25):

1. Again, state-changing operations are supported, just indirectly through redirects. I see no need to complicate the specification.
2. No, it’s because the EIP editors (including me) have come to the consensus that this is unnecessary.
3.

- We’re at cross purposes here. We both understand that this EIP builds on top of HTTP. Therefore, I felt it necessary to mimic HTTP as much as possible. I think that’s what you’re saying, and I agree with this sentiment.
- I meant that I didn’t literally do a google search for “HTTP in solidity,” but that I was honored to think that it was good enough to be mistaken for a top result. (Side note: Sorry if I offended you with my sarcasm, my apologies).
- State-changing methods are deliberately outside of the scope of this EIP, but I have provided an example flow above to demonstrate how they could be implemented. Would you like me to include it in my EIP? (This would probably give me an excuse to reference EIP-4804)
- How the browsers fetch the data from the chain is outside the scope of this EIP.  It would be like the HTTP spec describing how to connect to a router (bad example, but I hope it gets the point across).

1.

- I think I’m getting to the root of the misunderstanding here. REST, to my very limited knowledge, is typically about changing state as well as reading it (“REpresentational State Transfer”), but this doesn’t have to be the case. This EIP is specifically about smart contracts transferring state to the clients (not the other way round), whereas REST is typically used to transfer state from clients to servers (or the analogy here would be smart contracts). Crucially here, a different EIP (4804) can be used to provide the missing piece and actually change the state. (Personally, I normally wouldn’t consider a blog (for example) a “RESTful API,” but considering it can transfer a representation (HTML) of an object (the text a user wrote), I guess it satisfies the definition.)
- While I would argue that this EIP still describes decentralized something (as everything that is fully built on Ethereum is by necessity decentralized), I can definitely see how it might start to blur the line. To avoid any more unnecessary litigation, I will remove that word from the EIP unless it is essential (such as when describing decentralized applications).
- With that in mind, how about “Contract REST” as a title? It’s a bit brief, but I think it gets the point across. Thoughts?

---

**hskang9** (2022-07-25):

1. Again, stop saying bullshit and answer the question. It is not right because you say it is right. You just answer the question. It is simple as 5 year old can understand. You are like Machinsky saying bitcoin generates yields without process, Do Kwon saying has 20% yield without source. You are also one of them saying that these things have to be ‘simple’.
2. So EIP editors do not want to include a reference. Nice to know.

---

**Pandapip1** (2022-07-25):

The question has already been answered:

> I am well aware that the HTTP PUT, POST, PATCH, and DELETE methods are very typically state-changing. And technically, the following is a valid return value according to the current draft:
>
>
>
> ```auto
> statusCode: 303
> body: web3://
> resultHeaders: []
> resultHeaderValues: []
> ```
>
>
>
> Which then prompts the wallet to submit a transaction. Simple, and allows for all use-cases to be covered with a single view function.

---

**Pandapip1** (2022-07-25):

I think I’m starting to see your point of view with regards to point 1. Since, in general terms, this EIP is trying to enable smart contracts to serve websites, upon reflection I see no need to support any HTTP status other than GET, nor do I see a particular need for query parameters or request headers in this scenario.

---

**MicahZoltu** (2022-07-26):

> Think about this EIP as standardizing a way for smart contracts to become websites. HTTP just happens to be the current standard for that, and so this EIP tries to mimic that.

Perhaps there is some “bigger picture” I’m missing here, but I don’t understand how this specification would help make it so contracts can become websites?  If you wanted to serve a website from Ethereum storage (which I recommend against because it is too expensive to be practical), presumably you will need some middleware to convert an HTTP GET request to `ethereum://domain/path/query=string` into a contract call on Ethereum, and it seems that middleware could simply convert that to `domain.path(string)` just as easily as it could break up the URI into its components and pass them to a contract method.

---

**Pandapip1** (2022-07-26):

> presumably you will need some middleware to convert an HTTP GET request to ethereum://domain/path/query=string into a contract call on Ethereum, and it seems that middleware could simply convert that to domain.path(string) just as easily as it could break up the URI into its components and pass them to a contract method.

That’s my proposition, but the other part of this is that not all the stoage *does* need to be on Ethereum. A later EIP I will be proposing will add a “application/ipfs-multihash” content-type (the advantage of this over plain IPFS is that the URLs can later be changed.

---

**MicahZoltu** (2022-07-26):

I must be misunderstanding something then because it *looks* like your proposition is to turn an HTTP GET request into a single contract call where you pass a bunch of strings to it, rather than dispatching it to the appropriate function directly and doing the string to  type conversion elsewhere.  By doing it the way you have it specified, you are putting a lot of work on the EVM that could be done in some middleware component which feels like a bad trade since EVM execution is many many many orders of magnitude more costly than middleware execution.


*(14 more replies not shown)*
