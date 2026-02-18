---
source: magicians
topic_id: 23229
title: "z_PeerDAS: Z-Order Mapped PeerDAS"
author: sbacha
date: "2025-03-21"
category: EIPs > EIPs networking
tags: [peerdas]
url: https://ethereum-magicians.org/t/z-peerdas-z-order-mapped-peerdas/23229
views: 132
likes: 0
posts_count: 2
---

# z_PeerDAS: Z-Order Mapped PeerDAS

# Z-Order Mapped Responsibility-Driven Dissemination (ZORDD)

> This is intended for ‘supernodes’, assumes they are already sync’d (no backfilling in progress)

## ZORDD

ZORDD changes the data dissemination method and the peer selection logic by creating a stronger correlation between network topology and eventual data custody responsibilities. It relies on several key principles:

1. Z-Order Mapping: Data is mapped to positions on a Z-order curve (a space-filling curve that preserves locality)
2. Responsibility-Driven Forwarding: Messages are primarily forwarded to nodes whose responsibility zones align with the target data
3. Adaptive Redundancy: Limited redundancy is applied based on network conditions, data criticality, and Z-distance to target
4. Optimized Connection Topology: The network connection pattern is optimized for Z-order traversal

- Non-supernodes retain the existing PeerDAS gossiping, and can use the peer selection logic when searching for missing columns.
- Supernodes adopt the peer selection logic

### Z-Order Mapping

The Z-order curve (also known as Morton ordering) maps multi-dimensional data to a one-dimensional space while preserving locality relationships. In ZORDD, we map both data objects and node responsibilities to positions on this curve.

For a data column, we calculate its Z-order position using the block root and column index:

```python
def compute_subnet_for_data_column_sidecar_zordd(column_index: ColumnIndex, block_root: Root) -> SubnetID:
    # Extract coordinates from block_root and column_index
    coordinates = []
    coordinates.append(uint64(int.from_bytes(block_root[:16], byteorder='big')))
    coordinates.append(uint64(column_index))

    # Calculate Z-order position
    z_position = calculate_z_order(coordinates, BITS_PER_DIMENSION)

    # Map Z-order position to subnet
    return SubnetID(z_position % DATA_COLUMN_SIDECAR_SUBNET_COUNT)
```

This creates a relationship between data positions and node responsibilities that can be leveraged for efficient routing.

[![zordd_gossip](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b7a14b1fec2c92b03bc77a9d300632e1fac3994c_2_690x271.png)zordd_gossip2346×924 202 KB](https://ethereum-magicians.org/uploads/default/b7a14b1fec2c92b03bc77a9d300632e1fac3994c)

### Responsibility-Driven Forwarding

Instead of broadcasting to all peers, nodes forward data primarily to peers whose responsibility zones are close to the data’s Z-order position. This dramatically reduces unnecessary transmissions.

> Responsibility zones are just a subnet cluster of nodes

### Traditional Gossip

> Where N is the number of target nodes

- O(N × log(N) × redundancy_factor)

### ZORDD

- O(N × (1 + limited_redundancy))

The peer selection algorithm uses a scoring formula:

```auto
Score(peer) = 0.6 * (1 - Z_distance/Z_max) + 0.3 * NetworkQuality + 0.1 * ReliabilityHistory
```

Where:

- Z_distance is the distance between the peer’s responsibility zone and the data position
- NetworkQuality considers latency, bandwidth, and congestion
- ReliabilityHistory reflects past delivery success rates

## Tuneable Parameters

### Adaptive Redundancy

To ensure reliable delivery while minimizing redundancy, ZORDD applies an adaptive redundancy factor:

```auto
RedundancyFactor = BASE_REDUNDANCY * (1 + NetworkLossFactor) * CriticalityMultiplier * DistanceFactor
```

This formula increases redundancy when:

- Network conditions deteriorate (higher loss rates)
- Data is particularly critical
- Target responsibilities are distant from the current node

This can be done in response to node churn results, mass exists, etc.

## Remarks

Feedback welcomed

## Replies

**sbacha** (2025-03-28):

## Z-Order Mapper

```python
class ZOrderMapper:
    def __init__(self, dimensions=2, bits_per_dimension=16):
        self.dimensions = dimensions
        self.bits_per_dimension = bits_per_dimension
        # Calculate max distance based on total bits
        self.total_bits = self.dimensions * self.bits_per_dimension
        self.max_z_value = (1 = (1 > bit_position) & 1
                result = (result  list[int]:
         # Example: use first 16 bytes of root for one dimension, column index for other
         # Ensure types match expected coordinate types (e.g., uint64)
         # This needs refinement based on final spec for coordinate generation
         coord1 = int.from_bytes(block_root[:8], byteorder='big') # Example: uint64 from first 8 bytes
         coord2 = int(column_index) # Example: uint64 for column index
         # Adjust number of dimensions and extraction logic as needed
         if self.dimensions == 2:
             # Clamp coordinates to fit within bits_per_dimension
             max_coord_val = (1 2 dimensions not defined here")
```

## Forwarding Decision Engine

```auto
import math
import random # For redundancy tie-breaking or selection

# Placeholder types/classes
class DataColumn: # Simplified representation
    def __init__(self, index: ColumnIndex, block_root: Root, data: bytes):
        self.index = index
        self.block_root = block_root
        self.data = data

class Peer: # Simplified representation
    def __init__(self, peer_id: str):
        self.id = peer_id
        # Other attributes like IP, port etc.

class NetworkMonitor: # Placeholder
    def get_quality(self, peer: Peer) -> float:
        # Returns a score 0.0-1.0 indicating network quality (latency, bw)
        return random.uniform(0.5, 1.0) # Dummy value

    def get_reliability(self, peer: Peer) -> float:
        # Returns a score 0.0-1.0 indicating historical reliability
        return random.uniform(0.7, 1.0) # Dummy value

    def get_loss_factor(self) -> float:
        # Returns estimated network loss factor (e.g., 0.05 for 5% loss)
        return random.uniform(0.01, 0.1) # Dummy value

class ForwardingDecisionEngine:
    def __init__(self, z_order_mapper: ZOrderMapper, profiler: ResponsibilityProfiler, network_monitor: NetworkMonitor):
        self.z_order_mapper = z_order_mapper
        self.profiler = profiler
        self.network_monitor = network_monitor
        self.BASE_REDUNDANCY = 3 # Example base redundancy

    def calculate_z_distance(self, z_position: int, peer: Peer) -> int:
        """Calculates the minimum Z-distance from a position to any of a peer's zones."""
        peer_zones = self.profiler.get_peer_zones(peer.id)
        if not peer_zones:
            # If no zone info, treat as max distance or use alternative metric
            return self.z_order_mapper.max_distance

        min_dist = self.z_order_mapper.max_distance
        for segment in peer_zones:
            if z_position >= segment.start and z_position  int:
        """Calculates the adaptive redundancy factor."""
        # This uses the calculate_redundancy function structure from the appendix
        base_redundancy = self.BASE_REDUNDANCY
        network_loss_factor = self.network_monitor.get_loss_factor()
        criticality = 1.0  # Could vary based on data type or context

        # Calculate distance factor based on distance to *closest responsible peer zone known*
        # This is complex: requires finding minimum distance across *all* peers' zones
        # Simplified: use distance to *local* zones as a proxy for how far data is 'from home'
        node_min_distance = self.z_order_mapper.max_distance
        for segment in self.profiler.local_responsibility_zones:
             if z_position >= segment.start and z_position  0:
             normalized_distance = min(1.0, node_min_distance / self.z_order_mapper.max_distance)
        else:
             normalized_distance = 0.0

        distance_factor = 1.0 + (normalized_distance * 0.5)  # Ranges from 1.0 to 1.5

        # Calculate final redundancy count, ensuring it's at least 1
        redundancy_count = math.ceil(base_redundancy * (1 + network_loss_factor) * criticality * distance_factor)
        return max(1, int(redundancy_count)) # Ensure at least one target

    def decide_forwarding(self, data_column: DataColumn, peers: list[Peer]) -> list[Peer]:
        """Decides which peers to forward a data column to."""
        # Calculate Z-order position for the data column
        coordinates = self.z_order_mapper.hash_to_coordinates(data_column.block_root, data_column.index)
        z_position = self.z_order_mapper.calculate_z_order(coordinates)

        # Rank peers by score
        ranked_peers = []
        for peer in peers:
            # Calculate Z-proximity score (higher is better/closer)
            z_distance = self.calculate_z_distance(z_position, peer)
            # Ensure max_distance > 0 to avoid division by zero
            if self.z_order_mapper.max_distance > 0:
                # Clamp distance to max_distance to prevent negative scores if calculation exceeds max
                clamped_distance = min(z_distance, self.z_order_mapper.max_distance)
                z_proximity_score = 1.0 - (clamped_distance / self.z_order_mapper.max_distance)
            else:
                z_proximity_score = 1.0 if z_distance == 0 else 0.0 # Max proximity if distance is 0

            # Get other metrics
            network_quality = self.network_monitor.get_quality(peer)
            reliability = self.network_monitor.get_reliability(peer)

            # Calculate final score using weighted factors
            score = (0.6 * z_proximity_score +
                     0.3 * network_quality +
                     0.1 * reliability)

            ranked_peers.append((peer, score))

        # Sort peers by score, descending (highest score first)
        ranked_peers.sort(key=lambda x: x[1], reverse=True)

        # Determine number of peers to forward to based on redundancy factor
        num_peers_to_select = self.calculate_redundancy(z_position)

        # Select the top N peers
        selected_peers = [peer for peer, score in ranked_peers[:num_peers_to_select]]

        return selected_peers
```

### Commitment Root

Use the **root of the blob_kzg_commitments list** from the BeaconBlockBody.  We can call this the `CommitmentRoot`.

```
- ZPos = map_column_to_z_position(ColumnIndex, CommitmentRoot)
```

