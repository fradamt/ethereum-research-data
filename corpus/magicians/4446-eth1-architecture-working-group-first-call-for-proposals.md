---
source: magicians
topic_id: 4446
title: Eth1 architecture working group - first call for proposals
author: AlexeyAkhunov
date: "2020-07-25"
category: Working Groups
tags: []
url: https://ethereum-magicians.org/t/eth1-architecture-working-group-first-call-for-proposals/4446
views: 2420
likes: 4
posts_count: 4
---

# Eth1 architecture working group - first call for proposals

After writing my previous post [Eth1 architecture working group](https://ethereum-magicians.org/t/eth1-architecture-working-group/4424), I have been thinking a bit about how to kick-start this group and what process should we have. What I did not want to have:

1. Vanity Q&A calls or lectures of “experts” educating the crowds
2. Lots of chatter or calls without substantive documents and code to work on
3. Group relying on a one-two individuals doing all the work and everyone else being observers

To try how this will work (or not work), I would like us to start solving a concrete architectural task. Solution of this task can enable a host of practical applications, and will be a good test of how such group can work. We might also conclude that it simply does not work unless we just hire people and set them to work (which is my current suspicion).

Here is the first task.[![arch1](https://ethereum-magicians.org/uploads/default/optimized/2X/8/85fb7b625a713b5c83e904094e2fc237a5e90464_2_690x412.png)arch11886×1127 123 KB](https://ethereum-magicians.org/uploads/default/85fb7b625a713b5c83e904094e2fc237a5e90464)

On the first diagram we have a very rough architecture of eth1 client. The important thing to note is that transaction pool, downloader, and block relay all communicate with the peers via a “networking stack”. That stack includes a few “layers” and concerns, but pervasive theme I found in the code is the proliferation of the “peer management”, which, in go-ethereum code, for example, translates into having at least three entities called `peer` in different packages (`p2p` package, `eth` package, and `eth/downloader` package). I wonder if the concern of peer management can be abstracted away into a separate component (and this component perhaps even separated into a different process). In order to do that, we need to devise a good interface (and protocol) that would connect these parts, something like that:

[![arch2](https://ethereum-magicians.org/uploads/default/optimized/2X/0/06a966e3874be4925a504dc9e1ce81281b05fdba_2_690x371.png)arch22035×1096 157 KB](https://ethereum-magicians.org/uploads/default/06a966e3874be4925a504dc9e1ce81281b05fdba)

There is also a potential (and some interesting uses) of the aggregator component, which would allow to connect a single node to multiple networks, like this:

[![arch3](https://ethereum-magicians.org/uploads/default/optimized/2X/d/dacc02585c80aaed42bb489dde7d8871284f61e5_2_690x390.png)arch32091×1182 162 KB](https://ethereum-magicians.org/uploads/default/dacc02585c80aaed42bb489dde7d8871284f61e5)

I hope I gave enough info about the problem and what is desired (I am cautious of not overcommitting to this effort unless I see solid participation), but if not, please ask questions in the comments. Please also let me know if you think this is a wrong first task for the eth1 architecture group, and if so, what would be a better starting task.

I would like participants to make concrete proposals (in any form) about the design of the interfaces - what functionality should the interfaces allow, how can peer management be abstracted away without taking away crucial functionality, etc. Depending on how many proposals there are, we will decide later on the review process, and schedule a discussion.

## Replies

**vorot93** (2020-07-25):

So basically what Alexey proposes is make peers and devp2p available as an abstract *network* entity that could be blindly called by Ethereum client.

There is a blueprint for this that I have developed as part of rust-devp2p library.


      [github.com](https://github.com/rust-ethereum/devp2p/blob/vorot93/wip/src/eth/mod.rs#L39)




####

```rs

1. Shutdown,
2. }
3.
4. impl From for Error {
5. fn from(_: Shutdown) -> Self {
6. Self::Shutdown
7. }
8. }
9.
10. #[async_trait]
11. pub trait EthRequestHandler: Send + Sync {
12. async fn handle_new_block_hashes(&self, hashes: Vec);
13. async fn handle_new_transaction_hashes(&self, hashes: ());
14. async fn handle_new_block(&self, block: Block, total_difficulty: U256);
15. }
16.
17. #[async_trait]
18. pub trait EthProtocol {
19. async fn new_block_hashes(&self, hashes: Vec) -> Result;
20. async fn get_pooled_transactions(
21. &self,

```








Let’s cover the simple case: one network, one protocol (eth/66). Architecturally it looks like this:

There are 2 sides: *devp2p node* and *Ethereum client*. devp2p node does the peer management and provides an interface to e.g. request blocks. It also has to respond to requests from other peers and thus requires Ethereum client to handle ingress gossip and data requests.

This means we have 2 servers:

- devp2p node’s server that provides get_blocks call, and
- Ethereum client’s server that provides handle_new_blocks and respond_to_get_blocks calls

Naturally, it is possible to split them into 2 separate processes. In that case we have to connect them through some kind of RPC protocol. I incline towards *gRPC* as it has mature tools for *code generation* for many languages, which will allow client teams to generate much of the boilerplate.

---

**AlexeyAkhunov** (2020-07-25):

It is a good start, thank you! More “fundamental” questions I would like to be answered are:

1. Which parts of the interface need to be “request-response” like (that fits into RPC), and which parts are more “stream like” (this can be made by reverse RPC)?
2. How much knowledge about Ethereum (headers, blocks, state) does devp2p component need to have in order to operate? Obviously, we would like to minimise this knowledge, but preserve as much functionality and resilience as we can.
3. How safe can the interface between devp2p and the rest of the node be? For example, current assumption is that the devp2p outer interface of an Ethereum node is unsafe, and we expect all sorts of attacks coming from there, but we assume that front-end (JSON RPC) is relatively safe interface, so there is no so much defensive programming in there. Can we move all or most the “defensiveness” into the devp2p component?

---

**vorot93** (2020-07-25):

> How much knowledge about Ethereum (headers, blocks, state) does devp2p component need to have in order to operate? Obviously, we would like to minimise this knowledge, but preserve as much functionality and resilience as we can.

This is a very interesting point that I also had to think about when designing rust-devp2p. There is natural difference between peer management with capability negotiation and capabilities themselves.

For this reason I propose to separate devp2p node into two parts: *rlpx node* and *capability server*.

*rlpx node* will handle peer connection pool, discover and connect to new peers and accept incoming peer connections. It will also provide a simple *byte pipe* for various *capability servers* - which in turn will provide a programmatic interface for consumers. Internally, *capability servers* will achieve this by forming egress packets and demultiplexing ingress messages.

The two will interact like this:

*capability server* registers itself with *rlpx node*, telling it which capabilities it supports, and provides an ingress handler which is called on each incoming message of these capabilities. For example, in case of eth/66 *capability server* can easily:

- forward incoming requests / gossip and optionally send back a response, or
- multiplex responses to our requests based on request_id introduced in eth/66.

In any case, this logic will vary protocol-by-protocol, and is of no concern to *rlpx node* which will just pump through raw bytes.

In return *rlpx node* gives the protocol server a handle which can be used to send out requests.

In programmatic terms here is how *rlpx node*’s interface would look like in Rust-style pseudocode:

```auto
impl PeerToken {
	fn send_message(self, bytes: Vec);
}

impl NodeHandle {
	fn get_peer(&self) -> PeerToken;
}

struct RLPxNode {
	...
}

impl RLPxNode {
	fn register(&self, capabilities: Vec, ingress_handler: impl Fn(PeerId, Message)) -> NodeHandle {
    	...
    }
}
```

As for *capability server*:

```auto
struct EthCapabilityServer {
    active_requests: HashMap>,
    node_handle: NodeHandle
}

impl EthCapabilityServer {
    fn handle(&self, peer_id: PeerId, message: Vec) {
        let request_id = decode_request_id(message);

        if let Some(active_peer_requests) = active_requests.get(peer_id) {
    	    if let Some(response_handler) = active_peer_requests.remove(request_id) {
                (response_handler)(message)
            }
        }
    }

    fn new(node: &RLPxNode) -> Self {
        let server = EthCapabilityServer {
            active_requests: HashMap::new()
        }

        node.register(vec![("eth", 66)], |peer_id, message| server.handle(peer_id, message));

        return server;
    }

    fn get_block(&self, block_id: BlockId) -> Vec {
        let req_id = random();

        let req_bytes = make_get_block_request(request_id, block_id);

        let (tx, rx) = channel();
        self.active_requests.insert(request_id, |message| tx.send(message))

        self.get_peer().send_message(bytes);

        // Block on receiving multiplexed response
        let rsp_bytes = rx.recv();

        let blocks = decode_response(rsp_bytes);

        return blocks;
    }
}
```

(This code does not cover timeouts, errors or corner cases, or even compile - it simply demonstrates the approach).

If we split *rlpx node* and *capability server* into separate processes then instead of registration we can simply point them at each other’s different ports:

rlpx_config.toml

```auto
[handlers.eth]
65 = "eth64_handler_addr"
66 = "eth65_handler_addr"

[handlers.les]
4 = "les_handler_addr"
```

capability_server.toml

```auto
server_addr = "rlpx_node_addr"
```

