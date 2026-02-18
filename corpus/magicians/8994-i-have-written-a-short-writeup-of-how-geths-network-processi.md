---
source: magicians
topic_id: 8994
title: I have written a short writeup of how geth's network processing works and I'm looking for someone to verify that it is indeed correct
author: mtrycz
date: "2022-04-21"
category: Uncategorized
tags: [networking]
url: https://ethereum-magicians.org/t/i-have-written-a-short-writeup-of-how-geths-network-processing-works-and-im-looking-for-someone-to-verify-that-it-is-indeed-correct/8994
views: 1583
likes: 1
posts_count: 1
---

# I have written a short writeup of how geth's network processing works and I'm looking for someone to verify that it is indeed correct

Hi all! I have been directed here from reddit, after asking this question there.

Basically I’m compiling a writeup of how network code works for several different fullnode software. I have taken a look at geth, and the following is my description of it. Can anyone check it for correctness?

Thank you in advance.

---

`go` has the concept of goroutines, which are like “light threads” that share context with the calling thread (and sibling goroutines).

`geth` has two operating nodes, fullnode and les (Light Ethereum Subprotocol); fullnode can further run in “full” mode and in “archival” mode (which doesn’t change much for this writeup).

1. in the full mode, a global server object is created, that handles p2p networking
2. the server makes great use of channels and goroutines. goroutines run concurrently, but concurrency does not imply parallelism. Since go version 1.5, goroutines can run in parallel, tho, so that’s nice.
3. the server makes a thread in listenLoop() for accepting peer connections. The server maintains a map of connected Peers and creates a goroutine for each (run() in p2p/peer.go).
4. since goroutines are cheap, they are used liberally; for example a Peer will create one for receiving messages, one for ping, etc.
5. each peer routine will await network messages; if an incoming message is of “network-level” variety (handshakes, version negotiation, disconnects, …) then it will be processed here; otherwise of it of “application-level” variety, it will be passed to a protocol
6. a protocol is a map that connects each message type to a handler function; for example the eth66 protocol handles the 66 version of eth messages.
7. there is no message queue towards the protocol, instead there is a channel; it’s generally a similar concept with different caveats - goroutines cannot enque items into it, but will block until their message is ready to be processed; if multiple messages are ready, one will be chosen at random
8. If the message is a transaction, it will indeed be enqueued for processing in the mempool, otherwise if it’s a block, it will be processed right away

---

The `les` mode is radically different and it’s evident that it was implemented in a separate time with different architecture. It maintains a complex task queue, in which tasks are prioritized, and can be put on hold if higher priority tasks come in. Each peer is given a `buffer` (or an “allowance”) with a `recharge rate`, and messages from the peers with most `buffer` are processed first. Peers consume their `buffer` proportionally to the computational complexity of the messages they send. This ensures that peers cannot DoS us easily. There are several task processors that read the task queue, but if a task processor is idle, a task will be passed onto it without passing through the queue (cool optimization).
