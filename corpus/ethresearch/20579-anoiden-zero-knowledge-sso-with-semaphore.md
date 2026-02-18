---
source: ethresearch
topic_id: 20579
title: "Anoiden: Zero Knowledge SSO with Semaphore"
author: fjm2u
date: "2024-10-07"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/anoiden-zero-knowledge-sso-with-semaphore/20579
views: 394
likes: 10
posts_count: 3
---

# Anoiden: Zero Knowledge SSO with Semaphore

## About this post

This is a cross-post of content uploaded to GitHub. I am sharing it here to introduce it to the Ethereum community and facilitate discussion.

## Summary

[![Overview](https://ethresear.ch/uploads/default/optimized/3X/a/9/a99c53ec75d00e734fc14ce4a88a614def1c05fc_2_690x327.png)Overview2156×1024 173 KB](https://ethresear.ch/uploads/default/a99c53ec75d00e734fc14ce4a88a614def1c05fc)

Anoiden is an anonymous single sign-on (SSO) protocol that uses zero-knowledge proofs. This protocol allows users to sign in to a Service Provider (SP) using information from an Identity Provider (IdP) while keeping the user’s identity secret—even if the IdP and SP collude. It utilizes the [Semaphore library](https://github.com/semaphore-protocol/semaphore).

1. Connect

The user creates an account using methods specified by the IdP (such as email or phone number registration) and links their zero-knowledge proof keys.
2. Auth

The SP trusts the IdP and knows its authentication endpoint. The user requests to log in to the SP via the IdP and obtains a nonce.
3. The user then creates a proof of their identity and sends it to the IdP. The IdP verifies the proof and, if valid, creates a corresponding signature.

## Terminology

- Extension: A browser extension (or app) that manages the user’s keys and creates proofs. It is necessary to keep the identity confidential even if the SP and IdP collude.
- anoiden.js: Provides an interface for website clients to communicate with the extension.
- Identity Provider (IdP): An entity that provides information about the user’s validity to the SP.
- Service Provider (SP): An entity that utilizes the user’s validity provided by the IdP.

## Protocol

### Registration with IdP (Connect)

After the user completes account registration with the IdP, they can link that account with the key in the extension. Through this linkage, the user can use this IdP when authentication is requested in the future. Additionally, it becomes possible to log in to the IdP anonymously using the key.

The IdP client obtains the signature and public key through anoiden.js:

```js
const {signature, publicKey} = await connect(serviceName, nonce);
```

- serviceName refers to the Identity Provider’s name and is used for key management within the extension.
- nonce is an unpredictable string obtained from the server side of the IdP.

The following diagram shows the flow until the IdP client obtains the user’s signature:

[![Connect Flow](https://ethresear.ch/uploads/default/optimized/3X/8/e/8e0f26036d0590458476d9aed15c0132bd64d615_2_591x500.png)Connect Flow876×740 44.2 KB](https://ethresear.ch/uploads/default/8e0f26036d0590458476d9aed15c0132bd64d615)

The client sends the obtained signature, public key, and nonce to the server. The server checks the session and verifies whether it issued that nonce to the user. If valid, it verifies the signature, obtains the identifier (Poseidon hash of the public key), adds the identifier to a Merkle tree, and saves the Merkle root after the addition.

[![Connect Flow](https://ethresear.ch/uploads/default/optimized/3X/5/2/523eb38b3a1fe30f597d2327ea178e4022597044_2_583x500.png)Connect Flow783×671 42.7 KB](https://ethresear.ch/uploads/default/523eb38b3a1fe30f597d2327ea178e4022597044)

### Auth

When the SP uses the IdP, it is assumed that it has informed the IdP in advance and has received a client ID from the IdP.

The SP’s client obtains a signature from the IdP through anoiden.js as follows:

```js
const idpSignature = await auth(endpoint, nonce, params);
```

- endpoint is the endpoint of the IdP.
- nonce is obtained from the server side of the SP.
- params are arbitrary parameters defined between the SP and IdP, but clientId is required.

After the extension receives the endpoint, nonce, and params, it obtains identifiers from the IdP’s endpoint and uses Semaphore to create a proof as follows:

```js
// https://js.semaphore.pse.dev/functions/_semaphore_protocol_proof.generateProof.html
await generateProof(identity, group, nonce, "signIn");
```

- identity is the key created for each IdP.
- group is an object created from identifiers.
- nonce is the nonce passed from the SP.

The extension adds the hostname of the SP to params. The IdP uses the clientId and hostname to identify the SP that requested the signature.

The IdP receives the proof and parameters, verifies the proof, and then creates a signature of the nonce and parameters using a key in a format shared in advance with the SP.

[![Authorization Flow](https://ethresear.ch/uploads/default/optimized/3X/f/2/f2da965eea0a5c5c1fe8dd36b1430094919c4b5d_2_631x500.png)Authorization Flow910×721 46.4 KB](https://ethresear.ch/uploads/default/f2da965eea0a5c5c1fe8dd36b1430094919c4b5d)

The client sends the received signature to the server, which verifies it on the server side.

### Endpoint interface

The IdP’s endpoint has GET and POST methods. GET returns the identifiers of all accounts. POST verifies the proof and confirms the validity of the user.

#### GET endpoint/identifiers

There are no parameters. The response is in JSON and returns a list of identifiers as strings under the key identifiers.

Example response:

```json
{
  "identifiers": ["6423154662976160105169106896701549153516891642211172349909782921108153674476"]
}
```

#### POST endpoint/auth

The request body requires a JSON object containing the proof and parameters (params):

```json
{
  "proof": "Semaphore proof here",
  "params": {
    "clientId": "exampleClientId",
    "hostname": "example.com",
    "other_params": "additional parameters here"
  }
}
```

The response is returned in JSON format and includes the IdP’s signature as a string under the key signature:

```json
{
  "signature": "example_signature"
}
```

## Security

The `nonce` is used to prevent replay attacks.

The `clientId` and `hostname` are mechanisms that ensure the IdP passes user validity only to SPs it has authorized. This also helps prevent requests from unauthorized domains.

## Concerns

When an SP uses only a single IdP, absolute trust in that IdP is required. However, by utilizing multiple IdPs simultaneously during sign-in (Decentralized SSO), the necessary level of trust in each IdP is reduced.

When the number of identities increases, it becomes inefficient. Therefore, we are considering dividing identity groups, but this raises privacy concerns.

## Replies

**atakoraka** (2024-10-17):

How does the Anoiden protocol leverage Semaphore and zero-knowledge proofs to ensure secure and anonymous single sign-on, and what strategies does it employ to address scalability and prevent trust centralization within the system? ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

---

**Hopium21** (2024-10-17):

How do you envision the future implementation of Anoiden in real-world use cases, especially considering potential performance challenges as the number of identity groups increases? Are there any planned solutions for scaling while maintaining a high level of privacy?

