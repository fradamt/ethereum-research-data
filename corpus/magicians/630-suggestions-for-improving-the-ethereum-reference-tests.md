---
source: magicians
topic_id: 630
title: Suggestions for improving the Ethereum reference tests
author: jpitts
date: "2018-07-01"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/suggestions-for-improving-the-ethereum-reference-tests/630
views: 870
likes: 0
posts_count: 1
---

# Suggestions for improving the Ethereum reference tests

Posted by [Matthew Halpbern](https://github.com/matthalp) as an [ethereum/tests issue](https://github.com/ethereum/tests/issues/474):

> If I was to summarize this, it would be to make the Ethereum reference tests more systematic in a way that lowers the barrier to implementing a client from scratch, which include more granular test suites as well as a road map for how implementers should go about bringing capabilities online and testing them. Additionally there are opportunities to add conventions/consistency amongst test suites specifications/formats and include information about what test suites and individual test cases are evaluating.

Posted earlier to the [ethereum/tests gitter channel](https://gitter.im/ethereum/tests):

> [Matthalp] I am a core developer of Pantheon, the Java-based Ethereum client being developed at PegaSys/ConsenSys. My main area of focus has been on block processing/importing where I’ve spent a lot of time working with the various Ethereum reference tests.
>
>
> There Ethereum reference tests have been invaluable getting our block processing capabilities online and I am grateful for all of the effort everyone has put into them— thank you! I could not imagine how hard it would be to implement block processing without having that level of test coverage — especially all of the edge cases that are not immediately clear just by reading the Yellow Paper.
>
>
> While the retesteth project is underway, I think it would be a good time to revisit the different test suites and test specification formats. Having just entered the space ten months ago and implementing these functionalities these test from scratch, I think there are some good opportunities to make it easier for the next set of Ethereum clients to come online, which I am more than happy to help with/drive. Some of these improvements include:
>
>
>
>
> Making Test Specification Formats as Consistent as Possible Across Test Suites: The conventions from different test suites sometimes deviate from each other. For example, the GeneralStateTests typically contain a single property that encompasses the tests and the post field differentiates milestones while the BlockchainTests have a key per milestone. There is also a slight difference in their naming as well (e.g. _d0g0v0). Also the GeneralStateTests can nest multiple test cases by the indexes mechanism, which was done to save storage space, but now means that each JSON file corresponds to more than one test per milestone.
>
>
>
>
> Fill in the comment field to provide insight into what the test case is doing: Sometimes it’s not immediately clear what the test case is doing and testing for. For example, it’s not immediately clear that tx_e1c174e2 is testing the transaction that caused a consensus bug due to a client implementation committing data for a message that exceptionally halted to the RipeMD precompile. Another option is to provide this information in a README but that probably will not scale well and be hard to remember to always enforce when reviewing PRs.
>
>
>
>
> Decrease the scope of what is tested in a single test suite and increase the number of test suites to allow client functionalities to be developed methodically: An important aspect of the Ethereum reference test is that they make it easier for new clients to be developed. Many of the tests build on each other, such as the transition from GeneralStateTests to BlockchainTests. However we can make these test suites even more granular to create a “client implementor plan” that walks future client implementors through the steps of building a client. For example, having tests to thoroughly test RLP, creating and manipulating tries, deserialize/deserialize block constructs (e.g. blocks, transactions, etc), testing call/create messages, etc. Some of these tests exist in some aspect
>
>
>
>
> Keep the “Read the Docs” up to date:  Some documents, such as the TransactionTests are not up-to-date where the actual transaction fields are no longer there. This also goes back to point (3) as well because these fields would allow a client implementor to check more easily check/debug RLP serialization/deserialization for transactions.
>
>
>
>
> I know this is a lot and I’m more than happy to help where I can – if that would be helpful!

Related links:

**Ethereum Tests documentation**

http://ethereum-tests.readthedocs.io/en/latest/



      [github.com](https://github.com/ethereum/tests)




  ![image](https://opengraph.githubassets.com/f78a7a0c97c1b57708d34499398d3f40/ethereum/tests)



###



Common tests for all Ethereum implementations












      [github.com](https://github.com/ethereum/retesteth)




  ![image](https://opengraph.githubassets.com/1d6fb53e0f6757534c54aba1aa8dbcc9/ethereum/retesteth)



###



testeth via RPC. Test run, generation by t8ntool protocol
