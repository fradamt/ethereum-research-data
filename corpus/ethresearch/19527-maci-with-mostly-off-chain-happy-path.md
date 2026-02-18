---
source: ethresearch
topic_id: 19527
title: MACI with mostly-off-chain "happy path"
author: vbuterin
date: "2024-05-11"
category: Cryptography
tags: []
url: https://ethresear.ch/t/maci-with-mostly-off-chain-happy-path/19527
views: 6742
likes: 23
posts_count: 14
---

# MACI with mostly-off-chain "happy path"

*For background, see: [Minimal anti-collusion infrastructure](https://ethresear.ch/t/minimal-anti-collusion-infrastructure/5413)*

One of the challenges of MACI is that it requires data to be submitted on-chain for each vote, which incurs significant transaction fees. This post suggests a mechanism by which votes can be off-chain by default; a vote would only need to go on-chain if the coordinator is actively attempting to censor voters.

When a user makes a vote, take the following steps:

1. The user locally generates their vote, as in regular MACI
2. The user sends their vote to the coordinator
3. The coordinator replies with a signature, specifying which position of the next batch the user’s vote will be included at
4. When the coordinator submits their next batch, they submit only a hash to the chain. The hash must be the Merkle root of all votes that have been sent to the coordinator since the previous round. The coordinator is also required to publish the full set of votes (eg. on IPFS).

The ZK-SNARK enforces that the final vote results are the result of processing all submitted votes, including votes that have been published via this hash mechanism.

Users have access to two extra features:

1. They have the ability to submit a vote directly to chain. The coordinator is forced to process both types of votes (included via hash, and included directly)
2. If a user has a cryptographically signed promise, they can publish that promise on chain as a challenge. Any future message that the coordinator submits (a batch or the final result) must come with a SNARK proving that the correct votes have been included at the provided challenge positions.

This ensures the following properties:

- Assuming an honest coordinator, onchain costs go down to O(1) per batch period
- Censorship resistance is maintained, because users can go onchain worst-case
- We mitigate attacks where the coordinator pretends to accept a vote, but then fails to include it, hoping that most voters will not notice or re-open any kind of software daemon, by providing signatures:

If a user fails to get a signature immediately, they go straight to voting onchain.
- If a user gets a signature, and they do come back to check after the batch, they can check on IPFS (or ask the coordinator) for the Merkle branch associated with their vote; if it does not match their signature, they can publish their signature to chain, which effectively halts the entire vote and prevents it from giving a result. Hence, trying to censor even one voter becomes extremely risky for a coordinator.

## Replies

**MicahZoltu** (2024-05-11):

A problem with these sort of designs is that there isn’t any way to punish censorship.  While users who are censored can get around the censorship, the operators have no incentive to *not* censor.  In this case, you can only punish the censor if they are dumb or make a mistake (promise to include but then don’t).  The system cannot stop the censor from simply ignoring the censored user.

Most services (especially those run in the US) actively censor any accounts/users who have opted-in to privacy in the past.  IIUC the proposed system would allow these users to pay extra to bypass censorship, but the censorship will continue as it is today.

I feel like we need solutions that allow us to punish censors, rather than just giving high-cost alternatives that censored users can utilize (if they are wealthy enough).

I don’t have a solution to this problem, but it feels like since we have witnessed rampant censorship on Ethereum lately, we shouldn’t be designing systems that are cheap for the uncesnored users and expensive for censored users.  I think there may be value (in the greater good sense of the word) in keeping the system equally expensive for everyone, so at least there isn’t disincentive to engaging in censored activities (which are often exactly the type of activities we should be encouraging).  If we build a two-tier system where users who don’t speak out against their government, utilize privacy tools, or express dissent about The Current Thing can do everything cheaply while users who engage in such activities have to pay more, we are driving people to not engage in those activities.

Other than the above concerns the system seems reasonable though.

---

**Mirror** (2024-05-11):

Currently working on relevance work related to MACI, which you might find interesting:

1. Accelerating user proof generation using GPUs.
GitHub - mirrorzk/vortex: Modular ZK proof layer
2. A comprehensive study on ZK auditing, including an analysis of vulnerabilities found in MACI.
Zero-Knowledge Proof Vulnerability Analysis and Security Auditing

At the same time:

Doing more work off-chain in the short term can help the popularization of ZK applications on Ethereum and the participation of more enterprise users. However, in the long term, the original intent of building Ethereum was to enable it to support more diversified functions and computing capabilities. I believe that compared to Rollups, Danksharding is the ultimate solution. Let’s keep persevering and draw strength from the imitators. I urge every reader to pay attention to the progress of work on Danksharding.


      ![](https://ethresear.ch/uploads/default/original/3X/3/d/3da83016e1c9d7be34db780fc3be1d7e411ce3da.png)

      [ethereum.org](https://ethereum.org/roadmap/danksharding/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/e/4/e4f79b3232c7ab170489ae25fbed8d07e1eaeddf_2_690x431.jpeg)

###



Learn about Proto-Danksharding and Danksharding - two sequential upgrades for scaling Ethereum.

---

**cryptskii** (2024-05-12):

#### Erasure Coding

- Fragment votes into n pieces with redundancy r.
- Use the formula for reconstruction: ( n_{required} = \lceil n/2 \rceil + r )
- Store fragments across multiple nodes.

#### Multi-party Computation (MPC)

- Use MPC protocols to securely aggregate vote fragments.
- Reveal only the computed result, keeping individual votes encrypted:
 \text{Result} = \text{MPC}(\text{Encrypted Fragments})

#### Benefits

- Fault Tolerance: Operates even with node failures.
- Security: No single node has enough data to compromise the vote.
- Privacy: Votes remain encrypted, enhancing voter confidentiality.

---

**vbuterin** (2024-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> A problem with these sort of designs is that there isn’t any way to punish censorship. While users who are censored can get around the censorship, the operators have no incentive to not censor. In this case, you can only punish the censor if they are dumb or make a mistake (promise to include but then don’t). The system cannot stop the censor from simply ignoring the censored user.

Two possible ideas:

1. Whenever we end up turning the coordinator into an MPC (or FHE decryptor), we allow each of the participants to submit batches. This gives us an N-of-N assumption for liveness. If we want to relax this, we could require such batches to get k signoffs (k is tunable), and get a (N-k)-of-N assumption
2. Make the default vote submission interface anonymized. So you “sign in” to provide an anonymized vote by proving that you are a voter without revealing which one. So the coordinator cannot refuse any specific voter without refusing all of them.

---

**imkharn** (2024-05-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> coordinator) for the Merkle branch associated with their vote; if it does not match their signature

Regarding equal treatment for censored accounts:

Is there any issue with requiring the coordinator to reimburse the gas cost of onchain voting? Is it computationally feasible onchain to check if the signature matches the Merkle branch that way the coordinators only have to reimburse censored users (and not griefers pretending to be censored) ?

---

**MicahZoltu** (2024-05-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> Is there any issue with requiring the coordinator to reimburse the gas cost of onchain voting? Is it computationally feasible onchain to check if the signature matches the Merkle branch that way the coordinators only have to reimburse censored users (and not griefers pretending to be censored) ?

You can’t differentiate between a user that was censored, and a user that lied about being censored.  Both could submit an on-chain vote and *claim* to be censored.

---

**cryptskii** (2024-05-23):

### To address the issue of potential false censorship claims while still allowing legitimately censored users to be made whole, we could implement the following system:

When a user wants to claim their vote was censored, they must put up a stake (the “claim fee”) and submit a zero-knowledge proof (ZKP) or KZG commitment along with their on-chain vote. The ZKP/KZG would prove that:

1. They are a legitimate voter (without revealing identity)
2. Their vote matches what the coordinator promised to include
3. The vote is absent from the relevant batch

The contract verifies the proof/commitment without revealing vote contents on-chain. If the claim is invalid (vote was included as promised), the user forfeits their claim fee to the coordinator. If the claim is valid (vote was censored), the user is refunded their fee and reimbursed gas costs by the coordinator.

### Benefits:

• Legitimately censored users can bypass coordinator and vote on-chain directly.

• ZKPs or KZG commitments allow censorship claims to be verified without revealing vote contents on-chain.

• Requiring a claim fee to challenge coordinators disincentivizes frivolous or false accusations.

• Honest users are reimbursed for claim fees and gas costs, while dishonest ones forfeit their stake.

• Builds on existing MACI framework and can integrate with various ZKP/commitment schemes.

### Considerations:

• The fee must be high enough to deter abuse but not so high as to exclude legitimate users.

• ZKPs or KZG commitments must be efficiently generated off-chain for on-chain verification to minimize gas costs.

• Key management: Careful key handling is needed to prevent users from altering votes after initial commitment.

• Edge cases: Situations like coordinator key loss or compromise must be addressed to avoid unfairly penalizing them. e.g (Through Governance)

• Implementation complexity: Integrating privacy-preserving proofs adds complexity to the system and may impact usability.

• Proof system selection: The choice of ZKP or commitment scheme will impact performance, security, and compatibility.

---

**cryptskii** (2024-05-23):

Introducing a slashing mechanism for the coordinator after a certain number of legitimate censorship claims within a given time frame can further enhance the system’s integrity and deterrence against malicious behavior. Here’s how this can be implemented and its potential benefits:

### Detailed Implementation

1. Tracking Legitimate Claims:

- Maintain a counter for legitimate censorship claims made against the coordinator within a specified time frame (e.g., an epoch or a number of blocks).

1. Threshold for Slashing:

- Define a threshold number of legitimate claims (e.g., x claims) that, if exceeded within the time frame, will trigger the slashing mechanism against the coordinator.

1. Slashing Mechanism:

- Once the threshold is met, a predefined penalty (slashing) is applied to the coordinator. This can involve:

Financial Penalty: Deducting a portion of the coordinator’s stake or bond.
- Reputation Penalty: Recording the incident on-chain to affect the coordinator’s reputation score.
- Operational Penalty: Temporary suspension or replacement of the coordinator.

1. Automated Enforcement:

- Implement the slashing mechanism as part of the smart contract logic, ensuring automated and transparent enforcement without manual intervention.

### Lowering the Claim Fee

1. Reduced Financial Burden on Users:

- With the additional deterrent of slashing for coordinators, the claim fee can be set lower because the primary incentive for coordinators to act honestly shifts to avoiding slashing rather than just the economic deterrent from claim fees.

1. Enhanced Accessibility:

- Lower claim fees make it easier for all users, including those with fewer financial resources, to participate in the system and challenge censorship. This inclusivity is crucial for maintaining fairness and trust in the voting process.

1. Balancing Deterrence:

- The combination of a lower claim fee and the slashing mechanism creates a balanced system where coordinators are strongly incentivized to avoid censorship, and users are not financially burdened to make legitimate claims.

### Implementation Details

1. Setting the Claim Fee:

- The claim fee should be set at a level that is affordable for most users while still deterring frivolous claims. The exact amount can be adjusted based on the network’s economic context and user feedback.

1. Threshold and Slashing Parameters:

- Carefully determine the threshold for the number of legitimate claims (x) and the severity of the slashing penalty to ensure effective deterrence without excessive punishment.

1. Automated Enforcement:

- Ensure that the smart contract logic for verifying claims, tracking legitimate claims, and enforcing slashing penalties is robust and transparent.

### Example Workflow with Lower Claim Fee

1. Vote Submission and Coordinator Action:

- Users submit their votes to the coordinator as usual. The coordinator processes these votes and submits the Merkle root to the blockchain.

1. Censorship Claim:

- If a user’s vote is censored, they submit a censorship claim with a ZKP/KZG commitment and a lower claim fee.

1. Verification:

- The smart contract verifies the censorship claim. If valid, the claim fee is refunded, and the legitimate claim counter for the coordinator is incremented.

1. Threshold Monitoring:

- The smart contract continuously monitors the number of legitimate claims. If the threshold is exceeded within the specified time frame, the slashing mechanism is triggered.

1. Slashing Enforcement:

- Upon exceeding the threshold, the smart contract automatically enforces the slashing penalty on the coordinator, applying financial or operational penalties as predefined.

### Benefits of the Combined Approach

1. Enhanced Security and Trust:

- The threat of slashing ensures coordinators act honestly, while the lower claim fee makes it feasible for all users to challenge censorship, enhancing overall trust in the system.

1. Economic Fairness:

- By reducing the financial burden on users, the system remains economically fair and inclusive, encouraging broader participation.

1. Robust Censorship Resistance:

- The dual deterrents of claim fees and slashing create a robust mechanism against censorship, ensuring that votes are processed fairly and accurately.

---

**imkharn** (2024-06-12):

Doesn’t this method of detecting censorship only work when coordinators sign off on a users vote but fail to publish? If so, it sounds ok to reimburse in this scenario since it is proven. However, if the user fails to immediately get a signature they would still have to pay extra to vote onchain. It may not be possible to tell apart users who went straight to onchain vote and those that were ignored by coordinators and then went to an onchain vote.

It looks like the only working solution presented here involves multi-party computation to avoid the problem in the first place. Let me know if I am too off with this analogy. The MPC solution to censorship is taking a censored poster, making several copies, then breaking it up into puzzle pieces, and sending batches of pieces among users and ultimately to publishers. At this point the publishers cant tell who is publishing or what they are publishing without conspiring in advance to assemble the puzzles. The publishers are required to publicly acknowledge the receipt of the puzzle pieces. Then the publishers get together while everyone watches and they build the puzzle. By the time they realize they assembled controversial information, its already too late because they must include the acknowledged pieces. If they don’t broadcast the information, distributed consensus has undeniable proof for a guilty verdict and will destroy the bond they placed to become a publisher. It can be made even more difficult to conspire to filter out undesirable pieces if the users mix up their pieces and group them into batches where the publisher is required to use every piece from a batch they acknowledge. Using batches increases the percent of publishers required to conspire and the opportunity cost of censorship because they have to reject the income offered by mundane pieces every time they reject a batch containing controversial pieces.

---

**MicahZoltu** (2024-06-23):

In theory, homomorphic encrycption or witness encryption could also solve this problem.

Another solution would be some sort of commit/reveal scheme which could lower the on-chain cost of voting to just the reveal in the worst case.  With commit reveal, everyone would give the censoring coordinator an encrypted payload, get a signature of receipt from the coordinator, send the coordinator the decryption key, then finally get an encryption key receipt from the coordinator.  The coordinator can’t do targeted censorship of acknowledging receipt of the encrypted payload as that would just be a liveness failure (not targeted censorship).  If the coordinator refuses to give a receipt for the decryption key, then the user would simply post the decryption key publicly on-chain.  At that point, we now have all of the information necessary to prove censorship if the coordinator still refuses, but the user only has to put one WORD on-chain (decryption key).

This still does make it so censored users have to pay more than uncensored users, but perhaps it allows driving the cost low enough (~40,000 gas on Ethereum) that it matters less?

---

**imkharn** (2024-07-17):

Nice. Perhaps the cost of your idea can be brought even lower if the smart contract accepting keys is enshrined. Extra gas each block that can only be used for censorship claims with its own 1559 price. Anyone who wants censorship to be expensive would have to pay for spam to keep the gas price high.

Also, perhaps the decryption key data doesn’t need to be stored long term and can be even cheaper like rollup blobs.

That said, I still suspect there is a yet to be discovered a solution that prevents censorship with no extra cost for those censored. Perhaps even a way with no extra user actions. It appears the core problem is:

1. Trustless proof of existence is not free
2. The additional cost of proof of existence is only required when reacting to censorship because censorship = exists but not published
3. Therefore to prevent the soft censorship of PoE costs, anti-censorship expenses must be socialized
4. Its difficult or impossible to prevent fraudulent claims of censorship leading to the ability to harm those covering socialized costs.
5. The solution areas seem to be limited to : How do we make the harm to those censored approach zero? Or alternatively; How do we socialize losses without enabling false claims? Or alternatively; How do we ‘trick’ or ‘force’ would be censors into offering proof of existence for free in hopes of future profits?

---

**MicahZoltu** (2024-07-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> Perhaps the cost of your idea can be brought even lower if the smart contract accepting keys is enshrined. Extra gas each block that can only be used for censorship claims with its own 1559 price.

Interesting idea for dedicating some space to certain operations that provide censorship resistance.  We would need to make sure that the space can’t be used for other things (like posting free data) somehow.  The data only needs to exist long enough to prove that it was supplied.  In theory, we just need a way for a user to prove that the data was made available, so later when they submit a censorship claim they can prove all data was made available.

---

**skilesare** (2024-07-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Make the default vote submission interface anonymized. So you “sign in” to provide an anonymized vote by proving that you are a voter without revealing which one. So the coordinator cannot refuse any specific voter without refusing all of them.

I’d be interested to know if the Internet Computer’s verifiable credentials system might suffice for this:

https://medium.com/dfinity/introducing-verifiable-credentials-to-the-internet-computer-898f5538dcfb

https://internetcomputer.org/docs/current/developer-docs/identity/verifiable-credentials/overview

If this is relevant or interesting I can help put together a grant proposal to attempt to implement it.

I can see an issuer that reads from a chain and issues a non-revokable credential that says you are a voter that another service could use to accept votes. I’m not sure it solves real-time credential issuance if IC node providers coordinate, but that would be especially hard to pull off.(as an added bonus the voting service can sign and relay directly to the chain without human intervention)

