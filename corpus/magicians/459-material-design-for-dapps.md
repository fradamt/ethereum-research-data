---
source: magicians
topic_id: 459
title: Material Design for DApps
author: andytudhope
date: "2018-05-25"
category: Web > User Experience
tags: []
url: https://ethereum-magicians.org/t/material-design-for-dapps/459
views: 6715
likes: 22
posts_count: 23
---

# Material Design for DApps

This is a thread for all the people coming together to work on some basic principles and components for good UX across the ecosystem.

cc [@ricburton](/u/ricburton) [@danfinlay](/u/danfinlay) [@qnou](/u/qnou)

## Replies

**ricburton** (2018-05-25):

Thank you for making this. One issue with this software is the inability to reply by email. Does any FOSS tool allow that/

---

**boris** (2018-05-26):

it does allow it, it just needs to be configured and maintained. [@jpitts](/u/jpitts) you do all this right now, right?

Hmm. There is no site feedback / meta topic yet, probably should be.

---

**danfinlay** (2018-05-29):

I love the idea of leveraging community effort to create strong interfaces faster.

That said, each app/client probably has its own aesthetics and frameworks.

If common components are created, what is their format? Are we assuming they can be easily styled?

If I had to make a flippant call, I’d say “JS components with very specific CSS namespaces for custom styling”, but there are probably better, deeper answers to it.

---

**qnou** (2018-05-31):

[@danfinlay](/u/danfinlay) Precisely, similar to something like bootstrap where basic styling guidelines are provided for the ideal UX. The actual aesthetics and overall styling is done by each app/client should they choose to not use the boilerplate framework. Additionally, with the standardized JS components you open up the possibility of creating libraries of various UX/UI implementations through community effort and submissions.

The main purpose of the effort is to provide guidance and advocate interoperability throughout the eco-system. Making it easier for users to jump between dAPPs without the UX being jarringly different. This is where such things such as Walletconnect, Federated Logins, Standardized On-boarding flows play an instrumental role.

To be Continued on conflux discuss.

---

**sarahmills** (2018-06-01):

I joined so I could come here to post this survey: https://www.surveygizmo.com/s3/4395554/Design-System-Kickoff-Survey

but I am so happy to see you all have already started talking about this!

We’re looking to build a design system for the Ethereum community to make building dapps with great user experience easier. Currently we’re doing a component audit and kicking off research. We’d really appreciate it if you’d give us your input through the survey and share with any buidl-ers you know <3

---

**andytudhope** (2018-06-02):

Alright, as promised [@ricburton](/u/ricburton) and others, here is my take on things, along with some comments from a few of the UXR people at Status: https://docs.google.com/document/d/14gmA-6Z1m8dH9eSe4iwJCVW2ajMfY1-JNldrOvHG6eQ/edit?usp=sharing

I can see this already spreading in 1000 directions and that there are a lot of people with similar ideas, but quite different approaches. Decentralized chaos is generative, but difficult to manage well…

We have a call with someone later today about a tool call threads which might solve some of the cat herding here in terms of different discourses etc.

I also think we are going to need to specify a team (which will not in any way preclude others from working on this) based on past experience and running code/good research. Any ideas on how to do this well and wha the best way to manage bounties for this work would be much appreciated - I have outlined some ideas in the doc above, but they are very much open to change/discussion.

---

**ricburton** (2018-06-02):

My preference would be to pick off a piece of the action and let us focus on it.

We find remote creation does not work for us. We all gather around a whiteboard every day to get stuff done. If we could apply for a specific chunk that would be great.

---

**boris** (2018-06-04):

This is great. Will you be sharing the results of the survey [@sarahmills](/u/sarahmills)?

---

**andytudhope** (2018-06-04):

I agree quite closely with this. Some folks have also found that there are too many time pressures on them currently to really help with ETHPrize stuff, and so I need to focus on getting the report out and open sourcing the data analysis and UXR tools we use so that everyone from across the community can easily gather their own research and do UXR with good data insights at scale. This means it will be a while before we can get formal bounties behind this as only Mitch and I really have time committed to the initiative right now. If anyone else would like to help (do interviews, handle admin, PM bounties and teams, organise and herd all the cats), you are more than welcome!!


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/status-im/ETHPrize-interviews/tree/master/bounties_report)





###



A repository for the ETHPrize website. Contribute to status-im/ETHPrize-interviews development by creating an account on GitHub.










The beginnings of that are happening above. There is also a kaggle data set made from the spreadsheet you see in analysis there.

On topic again, I think it’d be great to start with seamless logins for everyone (as this will likely also help with transaction signing a little later down the line). We can start here, for instance: [ERC-1077 and ERC-1078: The magic of executable signed messages to login and do actions - #12 by cwgoes](https://ethereum-magicians.org/t/erc-1077-and-erc-1078-the-magic-of-executable-signed-messages-to-login-and-do-actions/351/12)

---

**sarahmills** (2018-06-04):

Sure! I want to get to ~100 responses. So far it’s a lot of designers, I am hoping for more founders and developers.

---

**ligi** (2018-06-04):

I love the material design language and try to use it in [WallETH](https://walleth.org) as much as possible

---

**beltran** (2018-06-11):

Hi all, sorry I missed this ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

[@andytudhope](/u/andytudhope) I’d like to voice in as we are building “exactly” this: a bootstrap like library for developers to quickly develop dapp front-ends that automatically implement the [Web3 Design Principles](http://bit.ly/web3DesignPrinciples) which I proposed to the community

(you can start with the [Tweet summary](https://twitter.com/lyricalpolymath/status/979689345937477632) if you want ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) )

I’m interested in collaborating with anyone who wants to work on this, even on just parts. looking forward to learning more from your survey [@sarahmills](/u/sarahmills) ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

I have both a local team and some remote developers, from various different projects, who have started implementing on their own some of the principles for their own dapps. (the feedback for the Web3Design Principles has surprised me a lot… it struck a nerve ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) )

our general approach for now:

- web3 is not the web2 and hence the web3 components should bring to the front-end the trustlessness and transparency of the blockchain
- we are opinionated on functionality but not on aesthetics: I agree with @danfinlay and @qnou that components need to be easily styled
- there are things that are “solved” and can be readily provided in a framework (ie from which contract does a certain datapoint come from),
but there are things that are not currently solved  (ie: the “universal login system”), there is no consensus and the community should work on proposing different solutions until we can all agree which one is the best option; therefore a framework like this should implement light interfaces and connectors to allow developers to plug in their experimental flows but still using basic components and “touchpoints” of the framework.
- a dapp framework needs to implement and handle Flows, interactive and non-interactive elements that span multiple views (and not only static or two state components like in a normal web2 material design library):
for example sending a transaction entails:
1- a screen showing how the state will change,
2- a screen showing the TX data and gas configuration (if on Ethereum) which mainly is on the wallet, or Walletconnect’s QR Code (@ricburton please add anything you see would be the appropriate description on the flow here  )
3- a screen handling the wait for the TX to be processed and to handle the user’s wait
4- a confirmation or error screen

I’ll stop here for now ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

but would love to know what you guys think already of these few points ![:sunny:](https://ethereum-magicians.org/images/emoji/twitter/sunny.png?v=9) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**pedrouid** (2018-06-12):

I think this is super important and we are fortunately seeing more discussions about this. The most critical points are easily informing the user of events which didn’t exist for web2 UX, the ones I find more critical are for example:

- Account Ownership: the user is used to relying on platforms to solve their problems and be responsible for most of its experience, it’s required to clearly show how much accountability the user has for it’s actions and how responsible they are for their own account
- Blockchain Finality: broadcasting and confirming transactions take time which affects in UX but also they are immutable

This affects a lot of the design and development of Dapps and once solved will increase user adoption. In my opinion, a Material Design for Dapps should focus on clearly showing:

- what accounts they are using to interact with the Dapp and where they are stored/managed (it’s a very new concept for users that the account is not stored/managed by the platform/app)
- that the state of the dapp is dependent only on their confirmed actions/transactions (users will except immediacy from their actions which is not true with blockchain)

How could Material Design help with these issues? The focus is to provide easy guidelines for these concepts to be implement by developers building frontend for their Dapps. If we consider the fundamentals for most Web3 UX, it involves mostly in three features

- Getting Accounts
- Signing Messages
- Sending Transactions

These are at least the first three features that I’m focusing the WalletConnect development to help developers implement best practices for Web3 UX but also allowing the user to be aware of each step and make informed actions based on them

---

**beltran** (2018-06-12):

totally agree.

Your thoughts make me think that we have to clarify/ create 2 different tools

1- a set of guidelines and best practices like the Web3 Design Principle (you’ve pointed to some interesting things that need to be added)

2- a series of tools and components that help implement these principles and that are “web3 native”

for instance the “account ownership warning” is a very important point (untill we solve key managent and don’t requires users to actually be aware of those), that I’d classify in point 1, as a guideline

but then the “dapp state” and the “account in use” should clearly belong to point 2 and be implemented as reusable components

---

**qnou** (2018-06-12):

[@beltran](/u/beltran) agreed. When developing a design system it is almost necessary to have the underlying design principles that in turn guide the development of components and libraries of various assets. Less so 2 “different tools” per say but complimentary parts necessary to addressing the bigger systems design issues. Look forward to discussing more soon ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**Kames** (2018-06-13):

Good Day All,

Arrived here after asking about Storybook integration with Web3 components on Twitter.

Thank You Pedro Gomes for pointing me in the right direction ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

Recently been very interested in the idea of composable blockchain components to quickly create interface components for distributed applications. Would love to see designers and product managers have more freedom to prototype and build minimal viable products with Ethereum specific features, without requiring developers.

It started when I became aware of the ORY editor, which promises an Open Source Drag-and-Drop editor. Was very excited to see a React/Redux based drag-and-drop editor that I could easily build Ethereum components and more easily build DApps that could be edited by others more easily.



      [github.com](https://github.com/react-page/react-page)




  ![image](https://opengraph.githubassets.com/d512842a679edbf734fcf547adf898ee/react-page/react-page)



###



Next-gen, highly customizable content editor for the browser - based on React and written in TypeScript. WYSIWYG on steroids.










What intrigued me the most about the ORY editor was the ability to save the UI layout in JSON format. A distributed application could save it’s interface layout in nested JSON to describe the DOM structure upon application hydration using custom built components. Add IPFS to the backend, slap on a SimpleStorage.sol smart contract and potentially a “SquareSpace for building distributed applications”.

          [https://kamescg.github.io/mvp/static/media/previewEdit.e09c9ea6.gif(image larger than 10 MB)](https://kamescg.github.io/mvp/static/media/previewEdit.e09c9ea6.gif)

### Styled Components & Atomic Design

Using `styled-components` and the Atomic Design techniques I’ve found decent success decoupling my applications from a particular CSS methodology like Bootstrap. The atomic design approach basically dictates building up a collection of composable components, including very small units likes Atoms (Paragraphs, BackgroundImage, Flex, Box) to Organisms (MacbookDisplay, VideoPlayer, Slideshow) and easily layering them together.

bradfrost .com/blog/post/atomic-web-design

### Meta Language to Describe Interfaces

I know not everyone is sold on CSS in Javascript for a number of valid reasons.

However to make my case for moving in this direction I would like to reference a talk at React Conference last year “Cheng Lou - Taming the Meta Language - React Conf 2017” which talks about the future of abstracting write coding using a “meta description of an interface” and think it might be good starting point to start thinking about UI/UX interfaces for distributed blockchain applications.

            ![image](https://img.youtube.com/vi/_0T5OSSzxms/maxresdefault.jpg)


My assumption is this will eventually lead to a better “meta langauge” standard for shareable components, that aren’t just React specific, but for any Frontend library or even in vanilla Javascript/HTML

Using the `styled-components` and atomic design approach approach has allowed me to stop writing CSS entirely. Instead passing `props` into any and all components to describe design features: background, gradients, box shadow, flex, positioning, etc… More detailed design attributes like gradients and design attributes are defined globally, so it’s easier to define application specific brand styles.

github .com/uport-project/buidlbox/blob/master/src/interface/theme/settings/index.js

### MVP - Mesh Viable Platform

At EthereumDenver hackathon I was able to build a prototype using the ORY Editor and  several blockchain components wrapping the ether.js library: blockchain scanning, wallet generator and a few uPort specific components for demonstration.

GitHub: github .com/kamescg/mvp

Demo: kamescg .github.io/mvp/?#/

I think the idea of Material Design for DApps would be great, because I would absolutely love to build website builder for non-technical people to build distributed applications using the collection of components that we build ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=15)

### DAppify

To extend the capabilities of the drag-and-drop builder I experimented with a “dapp embed plugin” that would provide the ability for anyone to easily embed distributed applications using a single line of Javascript.

The idea was designers and product developers could easily use the drag-and-drop builder, save the layout, the embed their applications anywhere on the web in a single line of Javascript.

The snippet below automatically loads a couple of React components around an event registration smart contract. The idea was anyone could create an event using the blockchain then embed the registration form easily on a website. Eventually I want to add token staking for events, but the deploy process would be easy enough for anyone to launch the “mini application” and to start utilizing the blockchain for incentivized event RSVPing.

```auto

```

github .com/uport-project/dappify

### BuidlBox

As a Developer turned Community Manager for uPort I’ve been working on the BuidlBox to help future distributed applications developers more easily launch DApps with uPort at the core ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15) but at the present moment it’s a very small collection of Ethereum components and basic blockchain interactions using Infura, uPort, Metamask, Truffle and in the near future other ecosystem libraries.

It’s pretty opinionated and still in beta, but mostly where I’m currently experimenting with building a set of shareable components and patterns.

Was thinking about starting a Storybook on the BuidlBox repo to create a Frontend Designer/Developer sandbox to create more nuanced blockchain interactions, but was thinking that might actually be better handled as a standalone applications that we can all contributed to more easily?

Link:github .com/storybooks/storybook

Link:github .com/uport-project/buidlbox

P.S. Links have spaces, because I’m a newbie and limited on link limits ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

---

**ale** (2018-06-15):

Hey guys, I’m glad that this discussion is still alive and kicking!

I worked on (1 - set of guidelines and best practices) along with Cande Mosse and the Zeppelin team. Inspired by Beltrán’s thorough blog post, we aimed to make universal, shareable guidelines and post them in [designforcrypto.com](http://designforcrypto.com). Still unsure whether this is the optimal vehicle for this information, but it does feel like having a reference website and detailed writeups would help spread the word.

I also took on a Status design bounty and performed a UX audit of 5 Ðapps. You can [read the whole report here](https://hackmd.io/FhfCq-rCTyKFQ_j6eyKSjw).

---

**mitch_kosowski** (2018-06-15):

Great work [@ale](/u/ale) and [@Kames](/u/kames) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) I will start processing a bit more information this weekend and brainstorming with Andy et al to start thinking a bit more formally how ETHPrize best slots into all of this.

---

**Kames** (2018-06-17):

What are the appropriate next steps for the Material Design for DApps thread?

Does an Ethereum Magicians GitHub Organization exist for spin-off projects?

Perhaps a good place to start will be to identify a list of potential generalized blockchain containers/components (React specific terminology), that can be shared amongst distributed applications in a meaningful way?

Was thinking it might also be be worthwhile to create patterns for reading/writing to the Ethereum Blockchain using ES6 async and generator functions? Not saying this is the right solution for the job, but I do like the DUCKS methodology for managing cross-project state management patterns.



      [github.com](https://github.com/erikras/ducks-modular-redux)




  ![image](https://opengraph.githubassets.com/811d179b7f17a5dcb29f2919e9faeccf/erikras/ducks-modular-redux)



###



A proposal for bundling reducers, action types and actions when using Redux










Mine are little messy, but so far setting up my state management plugin using this strategy is nice, because it abstracts blockchain away requests away from individual components and allows movement between large chunks of logic between DApp prototypes. I call my blockchain integrations “assimilations”, because I like to think my projects are forming multi-protocol symbiotic relationships and assimilating new shareable blockchain features ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=15)

https://github.com/uport-project/buidlbox/tree/master/src/assimilation/store

#### Example Component List

##### Ethers

- EthersBlockchainBlockGet
- EthersBlockchainBlockNumber
- EthersBlockchainGasPrice
- EthersBlockchainTransaction
- EthersBlockchainTransactionReceipt
- EthersProviderInitializeEtherscan
- EthersProviderNewInfura
- EthersWalletCreateRandom
- EthersContactDynamic
- EthersEnsResolveName
- EthersEnsLookupAddress
- EthersAccountGetBalance
- EthersAccountGetTransactionCount

##### IPFS (Internet File System)

- IpfsFileAdd
- IpfsFileAddStream
- IpfsFileCat
- IpfsFileGet
- IpfsBlockGet
- IpfsBlockPut
- IpfsBlockStat
- IpfsDagGet
- IpfsDagPut
- IpfsDagTree

#### Storj (Storage File System)

- StorjFileGet
- StorjFileCreate
- StorjFileDelete
- StorjFilesList
- StorjBucketGet
- StorjBucketCreate
- StorjBucketDelete
- StorjBucketMakePublic
- StorjBucketsList

##### Dether (Transaction Machines)

- DetherGetAllTellers
- DetherAddSellPointForm
- DetherDeleteSellPointForm
- DetherGetTellerBalanceForm
- DetherGetTellerForm
- DetherGetTellersInZoneForm
- DetherSendToBuyerForm

#### Shapeshift (Cryptocurrency Conversion)

- ShapeshiftCoins
- ShapeshiftDepositLimit
- ShapeshiftEmailReceipt
- ShapeshiftIsDown
- ShapeshiftMarketInfo
- ShapeshiftRecent
- ShapeshiftShift
- ShapeshiftStatus
- ShapeshiftTransactions

##### uPort (Decentralized Identity)

- IdentityLogin
- IdentityAttest
- IdentityDelegate
- IdentityRevoke

---

**mitch_kosowski** (2018-06-23):

Hi all, we’ve recently started a Telegram group called “Open Source Web3Design” on Telegram to more synchronously talk about concepts related to design in this space ![:+1:t2:](https://ethereum-magicians.org/images/emoji/twitter/+1/2.png?v=9)Please feel no obligation to join the Telegram channel as I think main concepts will still be crystallized in this forum, but the channel should provide a nice way to have back-and-forth on design topics quickly. We’ve used this model nicely with the “Open Source Block Explorer” Telegram channel built out by the excellent Griff Green.

Please message me on Telegram at Mitch_Kosowski if you’d like to be added! Thanks


*(2 more replies not shown)*
