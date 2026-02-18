---
source: magicians
topic_id: 13138
title: "Pebble: Embedded key-value Store"
author: StEvUgnIn
date: "2023-03-03"
category: Uncategorized
tags: [infrastructure, database]
url: https://ethereum-magicians.org/t/pebble-embedded-key-value-store/13138
views: 774
likes: 0
posts_count: 2
---

# Pebble: Embedded key-value Store

Go Ethereum and Bitcoin Core rely on an unmaintained embedded on-disk key-value store named LevelDB created by Google inspired by SSTable which Bigtable is based on. Multiple companies Facebook and Cockroach Labs designed new solutions which manage better data corruption compared to LevelDB and also include support out of the box widecolumn store

[Introducing Pebble: A RocksDB-inspired key-value store written in Go (cockroachlabs.com)](https://www.cockroachlabs.com/blog/pebble-rocksdb-kv-store/)

Why can’t Ethereum migrate over Pebble, so that Ethereum uses a native key-values store instead of relying on Cgo?

## Replies

**abcoathup** (2023-03-03):

Geth released [v1.11.0](https://github.com/ethereum/go-ethereum/releases/tag/v1.11.0) two weeks ago that included Pebble as an option to replace LevelDB

