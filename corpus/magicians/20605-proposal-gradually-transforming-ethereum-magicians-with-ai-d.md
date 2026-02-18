---
source: magicians
topic_id: 20605
title: "Proposal: Gradually transforming Ethereum Magicians with AI-driven governance and communication"
author: Snek
date: "2024-07-20"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/proposal-gradually-transforming-ethereum-magicians-with-ai-driven-governance-and-communication/20605
views: 428
likes: 3
posts_count: 6
---

# Proposal: Gradually transforming Ethereum Magicians with AI-driven governance and communication

Hello Ethereum Magicians,

In light of recent discussions around EOF and about protecting the EIP process from special interests, as highlighted in the [Ethereum Magicians thread](https://ethereum-magicians.org/t/protecting-the-eip-process-from-special-interests-examples-case-study/6542), I propose a transformative yet gradual approach to how we conduct discussions, plan, and make decisions within the Ethereum community. This proposal aims to supplement the current Ethereum Magicians platform with an AI-driven mail server that leverages AI to enhance efficiency, inclusivity, and transparency, while keeping every contribution recorded on the Ethereum blockchain.

### Vision:

Imagine a platform where a Linux server checks [ethereum-magicians.org](http://ethereum-magicians.org) for new submissions and a list of mailboxes every 5 minutes, parsing all new content through a preset but configurable LLM (Language Learning Model). This AI would filter and summarize all submitted data to decide the agenda points for the next All Core Dev (ACD) meeting. Here’s how it would work:

### Key Components:

1. Data Submission:

Participants submit their thoughts, ideas, and concerns here on the forum or via email.
2. Each submission could eventually be authenticated via ENS/ETH to prevent spam and ensure only relevant inputs are considered, perhaps even require a minimum gas fee to consider your contribution and prevent spam though I think current AI can sufficiently filter out spam anyway.
3. AI Aggregation and Summarization:

The AI aggregates and summarizes all inputs, identifying key issues and creating a dynamic agenda based on prioritized topics.
4. A local text/data blob file is maintained for every unique submitter and every unique discussion. AI can help people informally connect over similar topics of interest to discuss and guide them towards people also occupied with the same ideas or concerns. acdagenda@ethereum.ai (example) for all submissions around the next agenda eip3074@ethereum.ai (for all discussions around that eip) and of course you can generate new ones on the fly and have AI tell you about / announce to others who have similar enough needs for discussion. let email addresses be channels of communication that anyone can submit whatever to, and set an LLM to moderate away the spam and irrelevance (within that channel)
5. Continuous Updates:

The proposed agenda is automatically updated with every new email/datablob processed, valuing every voice equally.
6. A default agenda item is included to discuss any frustrations or proposals for updating the aggregator AI.
7. Human Control and Selection:

While the AI assists in creating the agenda and providing solutions, humans retain control over selecting and voting on the final agenda items as AI just like humans, makes mistakes. We must still verify ourselves instead of blindly trusting.
8. This ensures that all decisions are made by the community, maintaining the decentralized ethos of Ethereum.
9. Transparency and Traceability:

All raw text interactions and conversations during the ACD are recorded and stored on the Ethereum blockchain for full transparency.
10. Users can query the AI to understand decision histories and how specific agenda points were decided.
11. Privacy concerns are minimal as all discussions are technical in nature, focusing solely on improving Ethereum.
12. Technical Focus:

All conversations should be technical in nature and focused on improving Ethereum for everyone. This strict context window ensures relevant discussions and effective governance.
13. EIP Defense Mechanism:

Each EIP can defend itself by being automatically included in the ACD agenda once per meeting.
14. The AI summarizes the arguments for and against each EIP based on reactions received in advance, ensuring a balanced and comprehensive discussion.

### Proof of Concept:

To validate this approach, I will set up a web interface displaying the most recent ACD agenda proposal based on recent activity on the Ethereum Magicians forums. This interface will feature:

- An email address for anyone to freely contribute their thoughts and ideas.
- The AI will assess the relevance of each contribution to the ACD call and adjust the agenda accordingly within minutes.
- Users can ask the AI questions about the current knowledge database and ongoing discussions not yet visible on the agenda.

This initial phase can run on a regular Linux server, storing submissions locally and connecting necessary APIs. Over time, as we build trust and familiarity, we can transition to a fully functional Layer 2 solution, providing the needed scalability and decentralized trust.

### Embracing Change for True Decentralization:

For the Ethereum community to truly embrace decentralization, we must be willing to automate our own roles, even those of community moderators. Current moderators should see this as an opportunity to enhance their contributions, not as a threat to their positions. By adopting superhuman moderators, we can ensure that every voice is heard, and every relevant concern is addressed, pushing the boundaries of what we can achieve as a decentralized community.

### Call to Action:

I propose we develop this platform as a proof of concept, initially focusing on ACDE agendas and EIP discussions. By open-sourcing the aggregator AI, we can foster truly decentralized communities moderated by AI. The technology is already here; we just need to update our approach to leverage it fully.

Let’s discuss this proposal, provide feedback, and explore how we can make this vision a reality. Together, we can set a new standard for collaborative decision-making and take the next step in decentralizing our processes.

Looking forward to an enlightening discussion!

Snek 𓆙𓂀

## Replies

**mratsim** (2024-07-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/snek/48/16602_2.png) Snek:

> Imagine a platform where a Linux server checks ethereum-magicians.org for new submissions and a list of mailboxes every 5 minutes, parsing all new content through a preset but configurable LLM (Language Learning Model). This AI would filter and summarize all submitted data to decide the agenda points for the next All Core Dev (ACD) meeting.

How would you handle sybil attacks or astroturfing attempts to abuse the LLM?

> leverages AI to enhance efficiency, inclusivity, and transparency

I’m not against using AI, and it certainly improves efficiency, but inclusivity remains a problem as seen with training datasets being very western centered and errors such as tagging black people as ape.

Furthermore, public LLMs are trained to avoid political topics and privacy is certainly one and this would subject the process to whatever OpenAI/Anthropic/Google are required to censor.

In an ideal world, the LLM is provably trained on an open dataset with transparent extra instructions in its context window and it’s a reproducible build.

Bonus point if you can generate a succinct proof of validity but eh one can dream.

---

**Snek** (2024-07-23):

Thank you for your thoughtful response and for raising important concerns regarding the use of AI in our proposal.

### Addressing Sybil Attacks and Astroturfing

To mitigate the risk of sybil attacks and astroturfing, we can implement multi-factor authentication (MFA) and reputation systems tied to Ethereum addresses. This ensures that each participant is verified, reducing the chances of malicious activities. Additionally, we can employ rate-limiting and anomaly detection algorithms to identify and mitigate any astroturfing attempts.

### Inclusivity and Bias Concerns

I share your concerns about the biases in AI training datasets. To address this, we can ensure the AI model is trained on a diverse and representative dataset to minimize biases. Using open-source LLMs and transparent training methodologies will allow for community scrutiny and continuous improvement. This approach can help us build a model that is more inclusive and representative of the global Ethereum community.

### Transparency and Privacy

While public LLMs often avoid political topics and have certain privacy concerns, our focus will be on technical discussions related to Ethereum. By using a provably trained open dataset with transparent extra instructions in its context window, we can maintain the integrity and inclusivity of the AI’s outputs. Additionally, all interactions will be stored on the Ethereum blockchain, ensuring full transparency and traceability.

### Proof of Concept and Long-Term Goals

As a proof of concept, I plan to set up a web interface that displays the most recent ACD agenda proposal based on activity on the Ethereum Magicians forums. This interface will:

- Allow contributions via email, with the AI assessing relevance and adjusting the agenda accordingly.
- Enable users to query the AI about the current knowledge database and ongoing discussions.

This initial phase will run on a regular Linux server, storing submissions locally and connecting necessary APIs. Over time, as trust and familiarity with the system grow, we can transition to a fully functional Layer 2 solution for scalability and decentralized trust.

### Identity System

Additionally, I propose a new identity system where identities are defined by the contributions made to the aggregator AI database. This approach can provide access and training data, allowing individuals to build reputations based on their inputs and contributions to the community discussions. This system could foster a more inclusive and merit-based identity framework within the Ethereum ecosystem.

### Embracing Change

For true decentralization, it’s essential to automate roles, including community moderators. This approach should be seen as enhancing contributions rather than threatening positions. By adopting superhuman moderators, we ensure that every voice is heard, pushing the boundaries of what we can achieve as a decentralized community.

I hope this addresses your concerns and look forward to your feedback. Let’s work together to refine this proposal and explore how we can make this vision a reality.

---

**bumblefudge** (2024-08-05):

> To mitigate the risk of sybil attacks and astroturfing, we can implement multi-factor authentication (MFA) and reputation systems tied to Ethereum addresses. This ensures that each participant is verified, reducing the chances of malicious activities. Additionally, we can employ rate-limiting and anomaly detection algorithms to identify and mitigate any astroturfing attempts.

I’m not seeing how that would help. This isn’t a theoretical concern, there are ALREADY threads of GPT-bots talking to each other on this server, trained on the corpus of this server and other Discourses, complete with ### headings.  Requiring GPT-bots to control eth sybills in addition to discourse-sybills doesn’t add that much friction or price, IMHO-- as any airdrop-farmer could tell you, it’s not rocket science to automate.

---

**daveytea** (2024-08-07):

I just came across this and would love to help if there is enough interest. For part (2) **AI Aggregation and Summarization**, we’ve already built something similar here: https:// app.x23.ai/ethereum?feed=latest, which we could retool to be more useful for the ACD meetings.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/snek/48/16602_2.png) Snek:

> As a proof of concept, I plan to set up a web interface that displays the most recent ACD agenda proposal based on activity on the Ethereum Magicians forums.

Did you end up deploying this proof of concept?

---

**Snek** (2024-08-25):

> Did you end up deploying this proof of concept?

Haven’t gotten around to it yet, some irl stuff came up that is getting priority. Hopefully one day I’ll be able to simply code form sheer passion alone instead of having to worry about finances.

In the meantime, at least I’ve put the idea out there, it shouldn’t be too hard to get a poc ready anyway. It would mainly need community acceptance anyway.

Maybe I can dedicate some time in my calendar to it, maybe I should, I’m struggling a bit with properly allocating my time and this doesn’t help me financially short term so my mind tells me not to bother and focus my time and attention elsewhere.

And yet, there’s this comment here. Brains be weird.

