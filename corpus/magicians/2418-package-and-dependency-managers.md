---
source: magicians
topic_id: 2418
title: Package and Dependency Managers
author: philipplgh
date: "2019-01-14"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/package-and-dependency-managers/2418
views: 1601
likes: 23
posts_count: 7
---

# Package and Dependency Managers

Many projects share the need for package and dependency management.

While the individual requirements and type of dependencies can be different for each project most security critical applications that we’re building would profit from a package format with built-in security features such as signatures, checksums and digital certificates.

Other points of intersection are metadata standards, decentralized certificate “authorities”, and backends / infrastructure to store and discover packages such as IPFS & Swarm.

This post should serve as a starting point to find all stakeholders and begin a discussion on how our efforts can be channeled, how we can find synergies and solutions across the different projects so that we don’t have to re-invent the wheel.

Related Projects:

- https://ethereum-magicians.org/t/erc-190-and-the-ethereum-package-registry/1328
- https://github.com/ethereum/remix-plugin
- https://github.com/ethpm/ethpm-spec
- https://hack.aragon.org/docs/apm.html
- https://github.com/PhilippLgh/electron-app-manager

Related Standards:

- https://tools.ietf.org/html/draft-yasskin-webpackage-use-cases-01#section-2.2.4
- https://docs.oracle.com/javase/7/docs/technotes/guides/jar/jar.html
- https://docs.npmjs.com/files/package.json

## Replies

**spalladino** (2019-01-14):

Hey there, Santiago from Zeppelin here. We have been working with the concept of [EVM packages](https://blog.zeppelinos.org/state-of-evm-packages-end-of-2018/) for some time via ZeppelinOS. The idea is to set up packages where the code is already deployed to the network, and you just use pre-deployed contracts via proxies. The packages we’ve been working with have an interface compatible with those of Aragon’s.

However, it still requires a package manager to make some content available at development time. We’ve been relying on npm for now, but we’d love to support other platforms. We had some discussions with [@gnidan](/u/gnidan) regarding supporting EVM packages on top of ethpm, which would require a few additions to the current interface, but nothing that breaks compatibility with the ethpm standard.

On top of the package manager itself, we are also working on using a token to [signal secure reusable packages](https://blog.zeppelinos.org/toward-a-secure-code-ecosystem/), allowing users to vouch for the packages they use, and security researchers to profit from vulnerabilities they report. It’d be great to see this information integrated with package management tools, so a user can be informed on the degree of confidence of the dependencies they are working with.

Anyway, I’d love to be part of any discussions regarding package management, in order to work towards a standard solution.

---

**yann300** (2019-01-16):

Hey,

Yann from Remix,

We are pretty much interested in this as we do have the need of securing (signatures, checksums and digital certificates) and storing (IPFS, swarm) metadatas for plugin definitions.

Beside that I think we should leverage the compilation result JSON I/O standard as described here https://solidity.readthedocs.io/en/v0.5.2/using-the-compiler.html#output-description

and propose a standard way of storing , discovering , retrieving compilation artefacts. This would serve as a base infrastructure that package managers can rely on.

So happy to contribute on this.

---

**njgheorghita** (2019-02-14):

Hey all!

Nick here, I’ve been working on EthPM with gnidan. I completely agree that finding a standard to suit all the various use cases is crucial for the ecosystem. Imo the EthPM spec is a great base to build from (eg. Zeppelin EVM packages), but it might not cover all the use cases out there? I’d love to chat with anybody if they have any questions about the EthPM spec, or conflicts between EthPM and how they envision packaging.

Currently with EthPM we have our [homepage](https://www.ethpm.com) with resources, a registry explorer @ `explorer.ethpm.com`, and integration with `web3.py` and `twig` development tools. Integration with Truffle and `web3.js` is coming soon. If anybody has any questions, please shoot me an email ([nickg@ethereum.org](mailto:nickg@ethereum.org)). I’m here to help.

Though it’s a tricky problem, I’d also love to contribute to adopting solution that helps users identify trustworthy packages/registries.

Also, short notice, but Piper (originator of the EthPM spec) and myself will be at EthDenver this weekend. As big fans of conversations in real life, we’d be happy to grab a table and continue this discussion over the weekend if anybody else is around.

Cheers!

---

**philipplgh** (2019-02-14):

Hi everyone,

I was busy working on some early draft for a specification and reference implementation of “ethereum signed packages” for the last weeks. We will incorporate package signing in the next version of mist and the accompanying application manager: [GitHub - PhilippLgh/electron-app-manager: Electron App Manager provides fast, secure, minimal and continuous updates + version and dependency management](https://github.com/PhilippLgh/electron-app-manager)

You can find the [project repo here](https://github.com/PhilippLgh/ethereum-signed-packages) and a [spec draft here](https://github.com/PhilippLgh/ethereum-signed-packages/blob/master/spec/README.md).

You are all welcome to contribute on the issue tracker, with code or suggestions and feedback in this thread ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

An EIP is on the way. Unfortunately,  I won’t be at EThDenver but I will be at EthCC in Paris and give a short presentation about some of the changes. Would love to hear your input and feedback and have a discussion on how to improve the ecosystem and our application security.

Looking forward to our discussions.

---

**crazyrabbitLTC** (2019-02-27):

Hi @ [philipplgh](https://ethereum-magicians.org/t/package-and-dependency-managers/2418/5), Dennison from Zeppelin here, I’ll be at EthCC in Paris and would love to chat about what you’re working on!  What would be the best way to get in touch?

dennison

---

**philipplgh** (2019-02-28):

Will give a talk on the first day “Update on Mist”. Will talk a little bit about signed packages and package management too and we could continue the discussion afterwards or schedule a better time.

