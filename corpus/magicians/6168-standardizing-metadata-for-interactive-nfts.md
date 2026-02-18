---
source: magicians
topic_id: 6168
title: Standardizing metadata for Interactive NFTs
author: dievardump
date: "2021-05-06"
category: EIPs
tags: [nft, metadata]
url: https://ethereum-magicians.org/t/standardizing-metadata-for-interactive-nfts/6168
views: 6204
likes: 5
posts_count: 9
---

# Standardizing metadata for Interactive NFTs

Hey there,

I’m opening this discussion to talk about the need to come together on a standardize Metadata for what is called today Interactive NFTs, which are: NFTs defined by code (html/css/javascript) that are executed in a browser environment (mostly sandboxed iframes).

This is a complicated subject because there are several different implementations today.

The idea of this topic is to try to come all together to maybe define **how we can declare**, in the NFT Metadata, that an NFT is interactive, and also **how this NFT should be executed**

Some of you might know it, but I’m dievardump, creator of a platform called BeyondNFT that has for purpose to allow developers to create Interactive NFTs directly in their browser, and be able to mint them. So Interactive NFTs are kind of my primary subject of thoughts and I have been working a lot to try to make those work smoothly.

To allow this, I created a format that I called Interactive NFT that is [open source](https://github.com/beyondnft/sandbox) and is waiting for more people to participate in its evolution. It is still in its infancy and there is a lot of room for improvement. **But by opening this topic here, I actually hope that at some point it will be replaced by a common format that we might all come up with together here**.

At approximately the same time that I started the platforms, other platforms have also been doing similar things. So right now there are several ways to create Interactive NFTs, with different formats.

If we want those type of NFTs to be interoperable (loaded in things like cryptovoxels, sandbox, wallets, apps, …) and work the best, it would be nice if we could come all together about the way this should work.

As a example:

Right now, OpenSea have decided to go this way: if the content pointed by the property “animation_url” is HTML, then they copy the HTML content to their server, and when the NFT is viewed on their website, they load this content.

This is a very easy implementation, that works for some  use case, but is not very flexible and work only for the basic use cases.

- For example is the NFT distributor updates the code, they would expect the NFT to automatically show the update
- Another example, if the NFT code is in a directory and references things like “./images/my-image.jpg”, this will not work except if the whole directory is copied (which can be either impossible or a hassle and is prompt to errors).
- If the code needs its metadata or any other data to work, but the metadata changes over time, that might not be reflected and broke the NFT

This is why it would be very urgent to find a consensus on how those NFTs needs to be displayed.

# Decentralization

As the creator of a platform who decided to host every image, code, and metadata on IPFS, the fact that those NFTs need to work even if the creating platform doesn’t host the files is for me primordial.

We need to create a system  that allows the NFT to still work and be interactive even if the emitting platform dies (as long as the platform did things to make it so).

This means that we need to think of something like of a common way to define a *Manifest* in the metadata, that allows any consumer platform to show the NFT.

As a starting point of comparison:

In the interactive NFT format that was created for BeyondNFT, this is done under a property “interactive_nft” in the JSON Metadata.

This property has several properties and act kind of like a Manifest. It references:

- the code or the code_uri
- the dependencies (scripts and styles) that might need to be loaded
- editable properties (we allows NFT creators to define properties that NFT owners can edit at any time and are saved in the NFT contract; so those data can change any time and have to be passed to the NFT code at runtime)
- any other data that the NFT code knows how to handle

We have then a “shell” component that knows how to read this manifest, and build the NFT accordingly in the fronted.

This way by knowing (1) the manifest and (2) the “shell” that goes with this manifest, the NFT can be rebuild without needing the platform to be involved. All necessary elements are available in the JSON metadata. There is no dependencies to our platform which is one of the key point of this format.

# Self Awareness

If we want those NFTs to be dynamic and interactive, there needs to be self-awareness. The code rendering the NFT ought to know several things:

- its metadata (the NFT JSON defined in ERC721 and 1155)
- its current owner
- maybe its tokenId & its contract address
- anything else you can think of that might be primordial for this kind of NFT to work
- configurable properties (on Beyond this comes with an ERC721/1155 extension)

We need those data because those NFTs are not simple images or videos. They can be WebApps allowing interaction with a sercver, Minigame that shows the pseudonyme of the current owner, generative art that changes depending on its owner,

For platforms that do centralized hosting, this is easily done by updating the code or the metadata and then the NFT will render as expected.

However, **because we need those NFTs to work in a decentralized way**, we need to agree on the way to pass those data to the code, because if the NFT code & metadata are stored on IPFS, there is no way to update things like the “owner” or the “configurable properties”. **It therefore needs to be fed to the code, in some way or another**.

For Beyond, the format asks for the consumers to add data to the HTML (under `window.context`):

- nft_json: the nft JSON
- owner: the current OWNER
- owner_properties: the current owner configured “editable properties” if there are

This is because the format comes with a “builder” component call the sandbox that will do that automatically in the front end in a few lines of code (load the code, load the json, build the HTML with the code and injecting the JSON and all the needed data in the HTML, before rendering it in an iframe).

However I am not set in stone about this. I would be happy enough if we decided that those properties (and more if we decide that we want others)  are to be passed as “query parameters” to the iframe.

For example:

- tokenURI: this NFT metadata URI, so the NFT can load its own metadata and do things accordingly
- owner: an eth address
- tokenId
- contract
- ownerPropertiesURI:  this NFT owner properties file URI if there is one
- …

then the code could just read the query parameters, and load/use the data it needs.

As long as it can work in a decentralized way (i.e. consumer platforms feed those data in a way or another to the code), I think we could make something that is great, flexible and convenient for everyone.

# Web3 communication

What would very important too, would be defining a way for the code to communicate with the user’s Wallet. Maybe not giving access to all function, but things like “signing a message” from inside of the iframe would be nice.

Since mostly iframes are used (for security), we could define an interface using “[postMessage()](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)” and a list of specific messages that the consumers shuld know how to respond to

This is something that I have been wanting to implement since the beginning but didn’t find the time for. But this is asked a lot by users.

# Conclusion

I am referencing a lot my platforms and how we do this because well i’m working on it since more than 6 months and that’s my main reference point, it is also necessary to understand why some decisions were made (building the HTML and “feeding” some data to the code) and to have that in view so other platforms can compare it to their own format and so we can try to find the way they cross path.

As I said, the format we use **can evolve or be completely replaced by another one** I don’t really care, as long as we find ways to make it work in a decentralized way (the NFT must still fully work even if it’s not hosted by the platform emitting it), with the code still being able to be self-aware of the NFT Metadata and owner (and with the extension, the editable properties)…

To everyone and anyone that works with interactive NFTs or want to or is right now developing things, you’re very welcome to participate and share your point of view. Add what you think, etc…

I hope we can all do something that can fit all use cases

Have a nice day

## Replies

**tgerring** (2021-05-07):

Could [Swarm](https://swarm.ethereum.org/) (and their [Manifests](https://swarm-guide.readthedocs.io/en/latest/features/manifests.html)) be useful for this type of initiative?

---

**dievardump** (2021-05-07):

Thank you for this answer!

Well the idea would be something similar if platforms are going to “pull the whole NFT to their server”, because they will need to pull all the elements to have it working.

WebApps/Websites already have similar Manifest files where icons and files are already listed, but also other metadata about the app itself.

In ERC721 and 1155 Metadata we already have a good amount of those information in the Metadata, but we might want to add this “list of files used in this NFT” to it if they are referenced in relative paths.

---

**dievardump** (2021-06-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> However I am not set in stone about this. I would be happy enough if we decided that those properties (and more if we decide that we want others) are to be passed as “query parameters” to the iframe.

As an update to this, after researches and experimentation, it seems it is a lot easier to simply link to an HTML file in the `animation_url` property of the metadata. This can actually run any and all applications as interactive nft.

If `animation_url` contains HTML content, then it is executed in a sandboxed iframe: [<iframe>: The Inline Frame element - HTML | MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#attr-sandbox).

I think most platforms are expecting this to work the easiest way possible and the “shell component” called “Sandbox” I’ve been using for the v0 is too complicated to ask consuming platforms to run it, I can see it clearly now.

However I still think **interoperability**, **decentralization** and **self-awareness** are keys. Meaning the code should be able to have access to its own Metadata (because that’s where it will find parameters, attributes etc… to display) while still be able to be hosted on IPFS or Arweave. And simple enough so any Metaverse could actually run it easily.

For this to work, from what I’ve researched and experimented, I am leaning on simple query parameters:

- owner: since it can often change, it would be nice to have it passed as parameters.
- tokenURI: the URL of the file containing all Metadata

### Extensions

Maybe find a way for token metadata to tell consuming platforms there are more data to fetch and pass to the token. For exemple on beyondNFT we have an extension allowing owners to save on-chain configuration per token. And this is something we pass to the iframe too. And maybe you will also have this kind of extensions. It would be nice if we could find a way to declare this easily in the metadata or even on-chain so that when the NFT is rendered, the consuming platform knows that it needs to fetch those data before.

### Permissions

Maybe find a way to create “permission” so the consumer platforms could ask the end user if they allow the NFT to access their camera, before running it, if in the NFT metadata there is a “permissions” properties.

### Proof of Creation

Maybe also define a way so we can prove creation, with for example a message signed from the creator that reference the code URI, so end-user could have a “safe-list” of interactive NFTs they allow to run, and others not.

### Other

There are probably millions of things I don’t think of because the use case never occurred to me but occurred to you. Those are things we could all define together to have an interoperable

---

**thejaypee** (2021-10-09):

Ok my question is a bit simpler I just want to run a site inside the iframe on the nft while hosting files on ipfs … Just needs to trigger an htm file

---

**thejaypee** (2021-10-09):

So how can I simplify the process for a novice like myself

---

**dyske** (2021-11-17):

I’ve been looking into this issue myself, and it’s good to find someone else who has been pondering on it. It’s rather surprising that this isn’t discussed more widely. I thought NFT’ing a website or web page would be commonplace by now.

My biggest question is a bit more fundamental: Why use IPFS? Because if Web2 suffices, a lot of these issues will disappear. Using IPFS seems to over-complicate the problem.

In the tech world, we tend to mindlessly flock to the latest and greatest for its own sake. Because “decentralization” is the big hype now, we feel using any Web2 technologies would be uncool, but beyond the bragging rights of using the coolest tech, what does it offer?

IPFS would guarantee that the files would be accessible forever and that they would never change. Although that sounds good but is it really? A website is an organic product that must adapt to the changing environment. Just as the artworks I created in Macromedia Director can no longer be played, your website/page will stop working at some point. Is that a good thing or a bad thing? It depends.

For interactive work, the artist would have to choose. Do you intend to keep updating it as needed to maintain the artistic integrity, or do you intend to let it fall apart over time? If you intend to do the former, IPFS wouldn’t be a good idea. Centralization would make more sense so that different people won’t be looking at different versions (some broken).

Robert Rauschenberg created paintings that fell apart over time, but he made it clear that this was part of his artistic intention. So, whatever happens to the painting would always be part of his intended artistic statement.

You can choose this option and let your website fall apart, but one issue here is that at some point, it might become completely unviewable (like my Macromedia Director piece).

So, I would advocate for choosing a tool that best supports your artistic intent, not choosing one for its coolness. After all, 20 years from now, I’m sure IPFS would be uncool because something else cooler will emerge. At that point, any artwork hosted on IPFS would seem silly if a centralized server would work better for it.

---

**yuri** (2023-12-22):

Hello I recently made my first NFT project. It is not necessarily interactive but it is generative; being slightly different each time it is displayed. For this reason it’s not possible to display an image or an audiofile, I need to use the animation_url metadata that points to my own website with the content.

I finished my project, and tried to test it on OpenSea sepolia, only to discover that the iframe does not render my website! It turns out the reason is because my website is using SharedArrayBuffer (or webworkers). My project is basically using a SuperCollider server on a webworker that is communicating with the client. And I believe because of this non-sandboxed architecture, opensea does not allow it to render. I tried to look for solutions but could not find any.

I was wondering if anybody here knows a workaround to this issue?

This is my website: https://collider-nft-git-develop-dataexcess.vercel.app/ (you might have to click ‘play’ two times to make it work.

here’s how it renders on OpenSea:

https://testnets.opensea.io/assets/sepolia/0x41b9fd6d4a1037dc3f02aa4c0744cfa774d6f299/8

Any help or tips much appreciated! And apologie si fthis is not the right thread to ask for help.

All the best,

Yuri

---

**dievardump** (2024-02-21):

This is not really the place for it, but workaround is to detect if the feature works, and if not, tell people to “Open this NFT in its own separate tab”.

Sandboxing NFTs when displaying is important, can’t go over it. Some website allow everything except localStorage/Cookies access, but some just disallow everything.

