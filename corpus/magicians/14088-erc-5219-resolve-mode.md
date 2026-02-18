---
source: magicians
topic_id: 14088
title: ERC-5219 Resolve Mode
author: Pandapip1
date: "2023-05-01"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/erc-5219-resolve-mode/14088
views: 3171
likes: 6
posts_count: 13
---

# ERC-5219 Resolve Mode

Adds an ERC-4804 resolve mode for ERC-5219

## Replies

**qizhou** (2023-05-26):

PR is here [Add EIP: ERC-5219 Resolve Mode by Pandapip1 · Pull Request #6944 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6944/files)

And the gateways [w3eth.io](http://w3eth.io) and [w3link.io](http://w3link.io) are now supporting the draft.  A test contract can be browsed at testnet https://0x6587e67f1fbeaabdee8b70efb396e750e216283b.w3q-g.w3link.io/request/asdf/1234?abc=567&aaa=bar&xxx=yyy

The source code of the contract can be found at https://explorer.galileo.web3q.io/address/0x6587e67F1FBEAabDEe8b70EFb396E750e216283B/contracts

[@Pandapip1](/u/pandapip1) could you please take a look at the code and see if the gateway is working as intended (including customized response headers)

---

**qizhou** (2023-05-29):

One more question is regarding URL encoding/decoding, where we should expect the inputs of the following function

```auto
function request(string[] memory resource, KeyValue[] memory params) external view returns (uint16 statusCode, string memory body, KeyValue[] headers);
```

are the UTF-8 encoded string after URL decoding the Web3 URL?

For example, for the following Web3 URL

```auto
web3://0x6587e67f1fbeaabdee8b70efb396e750e216283b:3334/asdf%CE%B1/1234?abc=567&aaa=%20bar&xxx=yyy
```

the sources will be `asdfα` / `1234` and query of `aaa` is ` bar` (space before `bar`).

Could you please confirm this? [@Pandapip1](/u/pandapip1)

---

**Pandapip1** (2023-06-11):

That is correct.

Extra text so that this post is over the character minimum.

---

**nand** (2023-11-02):

Hi!

In the ERC-5219 contract interface, the returned body is of type `string`, so question:

Is it intended that only text should be returned, or any binary data could be returned, and I guess the interface needs to be updated with `bytes` instead of `string`?

Use case: I could easily see non text data be returned, e.g. some stored gzipped content, some crafted binary data, …

ERC-5219 being final, what would be the best way forward?

- Add an alteration on ERC-6944 indicating a slight change? It would be a bit messy.
- Like ERC-6860 was created to evolve a final ERC-4804, create a new ERC to evolve 5219, with binary return support, and also input HTTP header support?

---

**nand** (2023-11-30):

Hi!

[@qizhou](/u/qizhou) had the idea to add support for “big request”, i.e. requests whose returned content needs to be fetched over several RPC calls because of max gas limitations.

One initial idea would be: In a call to `request`, if the smart contract wants to return more bytes on that already returned :

- the smart contract returns in one of the headers a special header with a web3:// pointer to fetch the next chunk of bytes, e.g. x-web3-next-chunk: web3://0xabcd/getFile/xxx?chunk=2
- the web3 client send right away the HTTP code and the first bytes it received, and then fetchs this next URL, continue to stream the returned bytes, and loop until there is no longer a x-web3-next-chunk header.

([@qizhou](/u/qizhou): I removed the use of a special `statusCode` as we need right away the HTTP code to start streaming the answer, and the presence of `x-web3-next-chunk` in itself indicate the “big request” mode)

[@Pandapip1](/u/pandapip1) : What do you think of this small extension of ERC-5219, and do you think it could be in the non-final ERC-6944, or shall it be in a separate ERC? Thanks!

---

**qizhou** (2023-11-30):

Hi nand, do you want to provide more context about how HTTP chunked encoding solves the issue?

---

**nand** (2023-12-01):

Hi [@qizhou](/u/qizhou),

Sure, I thought about the use of the [Transfer-Encoding: chunked](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding) header method, which allows the server to send to the client the chunk of binary data right away after each call to the smart contract, effectively streaming the result.

Then I realized this was a HTTP/1 concept, and HTTP/2 has already native streaming support with their concept of DATA frames for a given request, so there isn’t even something special to do for HTTP/2.

On the server libs tested (golang http server lib, electron), they natively give the opportunity to send response chunk by chunk, and handle themselves the switch to chunked transfer encoding if HTTP/1.

---

**qizhou** (2024-01-22):

An interesting idea of using ERC6944 web3:// with a customized header to `Content-Encoding: gzip` so that the browser will decompress on-chain data returned by the contract

`web3://0xb464cac335daec57d4f50657ec846c3109c774b2:3334/gzip.js` or

https://0xb464cac335daec57d4f50657ec846c3109c774b2.3334.w3link.io/gzip.js

---

**nand** (2024-01-23):

I was wondering if it is a good idea, because this is part of the `Accept-Encoding` / `Content-Encoding` HTTP mechanism : the client sends a list of compression protocol it supports (e.g. `Accept-Encoding: gzip, deflate, br`) and the HTTP server choose one it supports and returns in which format it is encoded (e.g. `Content-Encoding: gzip`). If these is no match between client supported encoding and server supported encoding, the data is sent without compression – so this mechanism guarantee 100% that the client will be able to read the data.

In our case, we (the web3 client) are not able to specify the supported compression encodings, so we cannot garantee 100% that the client will be able to read the data.

For example we sent a response with `Content-Encoding: br` but the HTTP client does not support `br`.

Possible options I see :

1. We introduce a special header (e.g. web3-content-encoding) in which the smartcontract return specify the compression algorithm. A list of supported compression algorithms are required by the ERC spec. The web3 client itself will see this header, decompress the data, and send it to the HTTP client decompressed, and without forwarding the web3-content-encoding header – it will be invisible to the HTTP client.
2. The same than above, but we don’t use a new special header, we consume Content-Encoding (which is not forwarded to the HTTP client, so it stays invisible to the HTTP client). I like it less because it is reusing the name of a header of another mechanism we are not using.
3. We don’t care : we just forward the Content-Encoding: xxx header to the HTTP client, and if it is not supported by the HTTP client, it breaks. (It will work 99.9% of the time for common algorithms such as gzip, but we cannot guarantee 100%)

For option 1 and 2, there should work with the “large file”/“chunk” feature.

Let me know if you see others options and what are your thoughts.

---

**nand** (2024-02-09):

Hi!

I have put 2 PRs for 2 new features of the resource request mode :

- ERC-7617: Chunk support for ERC-5219 mode in Web3 URL : Introduce a special returned HTTP header which contains a web3:// pointing to the next chunk of data of the returned data.
- ERC-7618: Content encoding in ERC-5219 mode Web3 URL : Indicate that the returned HTTP header content-encoding is processed at the protocol level, returning decompressed data to the client (as we don’t want to do the Accept-Encoding/Content-Encoding handshake)

These features have been implemented on [web3protocol-js v0.5.8](https://github.com/web3-protocol/web3protocol-js) and are usable with [web3curl-js v0.1.5](https://github.com/web3-protocol/web3curl-js).

**Chunk test**

This call implements chunking and return 3 chunks:

```auto
web3curl "web3://0x64850db133e088fc1657c7bf9c00303d36d92736:11155111/getFile/abcd"
```

returns

```auto
startmiddleend
```

in a visible streaming fashion.

**Content-encoding test**

This call returned gziped data, and the HTTP header `Content-encoding: gzip`

```auto
web3curl "web3://0xb464cac335daec57d4f50657ec846c3109c774b2:3334/gzip.js"
```

returns

```auto
* HTTP Status code: 200
* HTTP Headers:
*   Content-Type: application/javascript

  console.log("hello world");

```

---

**SamWilsn** (2024-05-22):

If the client advertises, for example, `Accept-Encoding: br`, and the contract provides `Content-Encoding: br`, why does the gateway have to decode the data?

---

**nand** (2024-05-23):

Good point, I’ll add that decoding is optional if the returned `content-encoding` match one of the encoding advertised in `Accept-Encoding`.

