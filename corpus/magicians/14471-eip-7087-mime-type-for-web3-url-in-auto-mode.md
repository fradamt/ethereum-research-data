---
source: magicians
topic_id: 14471
title: "EIP-7087: MIME Type For Web3 URL in Auto Mode"
author: qizhou
date: "2023-05-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7087-mime-type-for-web3-url-in-auto-mode/14471
views: 1750
likes: 6
posts_count: 12
---

# EIP-7087: MIME Type For Web3 URL in Auto Mode

---

## eip: 7087
title: MIME Type For Web3 URL in Auto Mode
description: Deteremine the MIME type of a Web3 URL in auto mode
author: Qi Zhou (), Nand2 (@nand2)
discussions-to: TBD
status: Draft
type: Standards Track
category: ERC
created: 2023-05-28
requires: 4804

See [Add EIP: MIME Type For Web3 URL in Auto Mode by qizhou · Pull Request #7087 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7087)

## Replies

**MidnightLightning** (2023-07-27):

Overall, I think this EIP’s stated goal of “determine the MIME type of a link” by using query parameters lacks clarity on how it’s helping the “auto” mode. The EIP does not describe a process that an implementing script could “automatically” follow, but rather seems to be just describing how a client can request an arbitrary format for the return value.

Notably, I think there needs to be separation between what the resulting data ***IS*** compared to what the requesting client is ***ASKING FOR***. At a base level, all data can be transmitted as `text/plain`, so at the base level the server can always assume it’s that format. I think what this EIP needs to lay out is a set of specific MIME types that an EIP4804-supporting server could implement to add more logic on top of just returning everything as `text/plain`. It also should define the error-tolerance for adhering to the standard (similar to how a web browser as software has a set of MIME types it knows how to natively render rather than download, and it allows some tolerance for partially-broken implementations of those types).

I’d recommend this EIP cover text formats (plain, JSON, HTML, and XML), and image formats (SVG, PNG, JPG, GIF, BMP), and lay out a hierarchy of how a server is expected to determine what format the data is (e.g. start by assuming it’s plain text. First look for a comma in the data and see if what comes before it is a valid MIME-type. If it is, then parse as RFC 2397 to determine what format it is. If no comma, use magic bytes to guess what type it is: if it starts with a “<”, assume XML, and continue to parse to guess if it’s HTML, etc.). The result of that determining should set the Content-Type for the return value ***when no query parameters are set***.

The query parameters then are there only for overrides needed in edge cases (e.g. the data is SVG, but the user pulling it up in a web browser wants to see the code, so requests `text/plain` delivery).

If the current structure is desired to be kept, a few comments on the query parameters:

> mime.dataurl=(true|false), which determines whether to decode the returned EVM data and set the MIME type according to data URL standard defined in RFC 2397. If the data cannot be parsed as data URL, an error will be returned.

How strict should the “cannot be parsed” be adhered to? Some contracts that use this structure don’t have `data:` as a prefix before the data starts; should that result in an error being returned, or just parsing the rest of the string as following the rest of that format?

Being able to set `?mime.dataurl=false` seems to be a useless option? What behavior is the server supposed to take for that?

Having `mime.type` as a separate query parameter seems like it’s a lot of extra boilerplate to do `accessorizedImageOf/1289?mime.type=svg` compared to `accessorizedImageOf/1289.svg`. Just using the file extension as an extension is more human-intuitive and an overall shorter URL. Is there a benefit to a more verbose query parameter?

---

**qizhou** (2023-08-07):

Many good thought!  I share my comments below:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> I’d recommend this EIP cover text formats (plain, JSON, HTML, and XML), and image formats (SVG, PNG, JPG, GIF, BMP), and lay out a hierarchy of how a server is expected to determine what format the data is (e.g. start by assuming it’s plain text. First look for a comma in the data and see if what comes before it is a valid MIME-type. If it is, then parse as RFC 2397 to determine what format it is. If no comma, use magic bytes to guess what type it is: if it starts with a “ How strict should the “cannot be parsed” be adhered to? Some contracts that use this structure don’t have data: as a prefix before the data starts; should that result in an error being returned, or just parsing the rest of the string as following the rest of that format?
>
>
> Being able to set ?mime.dataurl=false seems to be a useless option? What behavior is the server supposed to take for that?

I agree that `dataurl=false` may be uesless.  I think a better way may define `mine.dataurl=(default|noprefix)` so that we can cover the cases with or without `data:` prefix.  Please let me know if you have further considerations here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> Having mime.type as a separate query parameter seems like it’s a lot of extra boilerplate to do accessorizedImageOf/1289?mime.type=svg compared to accessorizedImageOf/1289.svg. Just using the file extension as an extension is more human-intuitive and an overall shorter URL. Is there a benefit to a more verbose query parameter?

EIP-4804 already specifies using suffix (file extension) to determine MIME of an URL request. EIP-7087 mainly serves the purpose of determine MIME if such suffix does not exist (mostly for existing contracts that is not aware of EIP-4804 web3://).

---

**MidnightLightning** (2023-08-16):

Okay, then I think what this EIP needs is a clear definition of what it’s trying to do. Given a specific contract function call with specific parameters returns a specific data blob that’s to be parsed as the contents of a virtual file (via EIP-4804), is this EIP trying to define how to make the **server smarter** (on “auto”, what logic does it apply *on its own* to try and determine what type of file that virtual file is; an extension of the description of the five-step “auto mode” in that EIP where `type` must be “string” because all the other types have been checked for), or is it trying to provide error-correction options for the end user (in a case where the server’s “auto” mode is wrong, allow the user hooks to make the **server dumber** and just return what the user is explicitly asking for)?

Providing parameters for the user to specify that make the server just slap a specific `Content-Type` header on the returned value can be useful, but doesn’t seem to fall under an overall description of “making auto mode smarter”, to me.

---

**nand** (2023-08-21):

Hi!

I’ll summarize :

In auto mode, we are dealing with common smartcontracts, that may or may not be designed to be interacted with with ERC-4804.

When not designed for ERC-4804, we cannot ask these contracts for a specific content type we want, and they don’t tell us which is the content type of the resulting data.

When we make a smartcontract call, we get raw bytes as return.

But because we read the source code, documentation, …  we know the content type we will get.

So we add it on the URL, so that it is forwarded back as a content-type header.

ERC-4804 natively covers this usecase when the smartcontract was coded with ERC-4804 in mind. Example :

`web3://xxx.eth/getFile/file.svg` will call `getFile()` with `file.svg` as argument, and then since there is `.svg` at the end, the returned bytes will be accompanied by a `content-Type: image/svg+xml`

But there is a problem when the smartcontract was not coded with ERC-4804 in mind. Example :

`web3://xxx.eth/tokenSVG/38` will call `tokenSVG` with `38` as argument, returns some SVG data, but since there is no `.svg` at the end, the returned bytes will NOT be accompanied by a `content-Type`. But I know it is SVG. So what do I do? If I call `web3://xxx.eth/tokenSVG/38.svg` , then it will call `tokenSVG` with `38.svg` as argument, and the function will break (it expects a number).

So that is what this ERC-7087 is fixing : In this example, we would do : `web3://xxx.eth/tokenSVG/38?mime.type=svg` : it will call `tokenSVG` with `38`, and the returned bytes will be accompanied by a `content-Type: image/svg+xml`

On top of that, it add support for contracts returning dataurls.

---

**MidnightLightning** (2023-08-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nand/48/9249_2.png) nand:

> When not designed for ERC-4804, we cannot ask these contracts for a specific content type we want, and they don’t tell us which is the content type of the resulting data.
> When we make a smartcontract call, we get raw bytes as return.
> But because we read the source code, documentation, … we know the content type we will get.
> So we add it on the URL, so that it is forwarded back as a content-type header.

My concern is that “we” in your statement changea from “the web server that is acting as gateway for the ERC4804 request” to “the user making the `web3://` call” partway through the statement.

I think that your statement would be more accurately put as:

> When not designed for ERC-4804, the only “types” a contract will return are solidity types. When the solidity return type is string or bytes, the ERC-4804 gateway can return it to the requesting user as text/plain, but many contracts return specifically-formatted data as bytes that users would expect to be handled differently. If the requesting user has read the target smart contract’s source code, documentation, etc, they may know a more-specific MIME type the bytes conform to. To get the gateway to conform, the user adds the MIME-type to the URL, and the gateway sets that as the Content-Type header instead of text/plain.

Because it’s the gateway that makes the call, but then you seem to be describing that the end user steps in to help the gateway service figure it out.

Which means you’re targeting the second option of what I was asking: EIP-7078 aims to make the gateway server dumber (“don’t analyze this `bytes` blob, just stick this header on it”), and requires the requesting user be smarter (make a more-complicated query structure, and know not to use an incorrect MIME-type for specific queries).

That’s fine to have as a feature, but I personally (as a potential end-user and developer in the space) find it less interesting/useful. That seems to be a small addition that I’d opt to just make part of EIP4804 because it’s so small a change, and the naming I’d update to make it clear it’s only targeting “`string` and `bytes` return types in Auto Mode”, and not adding logic to the gateway to make “auto mode” more automatic.

---

**nand** (2023-08-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> When not designed for ERC-4804, the only “types” a contract will return are solidity types. When the solidity return type is string or bytes, the ERC-4804 gateway can return it to the requesting user as text/plain, but many contracts return specifically-formatted data as bytes that users would expect to be handled differently. If the requesting user has read the target smart contract’s source code, documentation, etc, they may know a more-specific MIME type the bytes conform to. To get the gateway to conform, the user adds the MIME-type to the URL, and the gateway sets that as the Content-Type header instead of text/plain.

I agree to the rewording of the statement, except one thing : it is not good to assume a default mime type of `text/plain`. The gateway don’t have the information and cannot get it, so the gateway should return no content type.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> Because it’s the gateway that makes the call, but then you seem to be describing that the end user steps in to help the gateway service figure it out.

I agree.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> Which means you’re targeting the second option of what I was asking: EIP-7078 aims to make the gateway server dumber (“don’t analyze this bytes blob, just stick this header on it”)

Without this extension, using my example of ` `web3://xxx.eth/tokenSVG/38`, the gateway cannot determine the content-type by itself. With this extension, the gateway still cannot determine the content-type by itself : To me the gateway is not dumber.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> requires the requesting user be smarter (make a more-complicated query structure, and know not to use an incorrect MIME-type for specific queries).

On a onchain website, I’d like to use this : `<img src="web3://xxx.eth/tokenSVG/38?mime.type=svg" />`  ; I think it’s fair to say it’s pretty straightforward, and to me, useful.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> That seems to be a small addition that I’d opt to just make part of EIP4804 because it’s so small a change

I totally agree with that, but unfortunately ERC-4804 is final and cannot be edited.

---

**qizhou** (2023-08-21):

One thing I would like to point out is that it is not necessarily a gateway that makes the call - the call can be done by

- a browser that supports web3:// and directly calls eth_call JSON-RPC or even via P2P, e.g., via portal network.  @nand has done a great job on this, and an anonymous developer develops a Chrome extension here;
- a cmd line like curl to make the web3:// request via eth_call JSON-RPC.

The question is whether we should ask all these methods to follow a standardized `bytes`-type detection or leave it to

- smart applications (e.g., browser/OS can auto-detect it); or
- the smart users that write a web3:// URL to display a special data type? Note that most users may just copy and paste, so they do not need to understand the MIME here.

---

**SamWilsn** (2024-02-02):

Is there a risk of cross-site scripting or something similar if an attacker crafts a URL with a particular MIME type and gets me to click on it? Probably worth discussing a bit (or at least explaining why it isn’t a problem) in the security considerations section.

---

**nand** (2024-02-08):

Indeed, an attacker with some write permission on a well-known legitimate auto-mode `web3://` website can write some HTML+JS and “make it executable” with the use of the `?mime.type=` field. Every method returning a string or bytes would be affected.

And since we aim to be close to regular HTTP with support of localStorage, cookies, …, those could be stolen.

We could say that future likely “well-known legitimage `web3://` websites” are more likely going to use the resolve modes more practical for `web3://` website development (manual or resourceRequest), but I could see websites using a mix of manual/resource and auto smart contracts (the JSON returning capabilities of auto smart contracts are practical).

A developer would have to keep in mind that returning user data in auto mode is not safe in string/bytes returning methods, and would need to do some workarounds (multi-vars returning methods, escaping, …) – a mess.

Initially this ERC was made to add the ability in a single URL to display content from existing auto contracts (e.g. `tokenSVG` of NFT contracts), but with these security implications, maybe it’s not a good idea, and these auto contracts will require an extra wrapper contract to be displayed in a single URL.

What are your thoughts [@qizhou](/u/qizhou) ? Should we drop the ERC?

---

**qizhou** (2024-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Is there a risk of cross-site scripting or something similar if an attacker crafts a URL with a particular MIME type and gets me to click on it? Probably worth discussing a bit (or at least explaining why it isn’t a problem) in the security considerations section.

I guess the click can only steal the local user data of the same domain (i.e., the website hosted by the contract in `auto` mode)?  If so, we should suggest that a well-developed dynamic website (a.k.a., contract) should never use the `auto` model.  That said, we should be safe if a website in `auto` mode is pure static with no local data (cookie, storage).  We should add some discussions in our security section.

For websites in “manual” or “resourceRequest”, we do need some best practices to address XSS since server-side validation may be gas-inefficient.  A client-side validation using a library downloaded via web3:// sounds to be the best practice.

---

**nand** (2024-02-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/qizhou/48/2964_2.png) qizhou:

> I guess the click can only steal the local user data of the same domain (i.e., the website hosted by the contract in auto mode)? If so, we should suggest that a well-developed dynamic website (a.k.a., contract) should never use the auto model. That said, we should be safe if a website in auto mode is pure static with no local data (cookie, storage). We should add some discussions in our security section.

Ok I have added this in the security section, let me know if you have comments:

> These new query parameters introduces Cross Site Scripting attack vectors : an attacker could exploit string or bytes returning methods he can influence by making them return unfiltered data injected by him, and then craft an URL to make the returned data interpreted as HTML, and then send the URL to victims. If the web3 hostname is well known, the victim may get a false sense of security.
>
>
> Malicious actions using javascript are broad and can include :
>
>
> Extraction of data of web storage APIs (cookies, localStorage, sessionStorage, indexedDB), sent to the attacker
> Triggering a signature request or transaction confirmation request (via EIP-1193/other wallet javascript interface)
>
>
> Cross Site Scripting is a classical attack vector in HTTP websites, we expect developers to be wary of this. Nonetheless the ability to specify the MIME type is unusual. auto mode websites should be discouraged and the attack vectors well documented.

