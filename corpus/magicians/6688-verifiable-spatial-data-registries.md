---
source: magicians
topic_id: 6688
title: Verifiable Spatial Data Registries
author: johnx25bd
date: "2021-07-19"
category: Magicians > Primordial Soup
tags: [web3-spatial]
url: https://ethereum-magicians.org/t/verifiable-spatial-data-registries/6688
views: 1261
likes: 0
posts_count: 1
---

# Verifiable Spatial Data Registries

# Verifiable Spatial Data Registries

*note: we couldn’t include more than 2 links in this due to forum restrictions - for a version with all links, here’s one on [HackMD](https://hackmd.io/@astral/r1xko6rpO).*

At [Astral](https://astral.global/) we’ve been exploring the use of spatial and location data technologies on the decentralized web for a few years now - researching, experimenting, prototyping, writing and community building. A number of early pioneers - FOAM], IBISA Network, Geo Web, Grassroots Economics, among several others - further validate our conclusion that a broad range of useful applications exist at the intersection of these two technology domains.

Our work experimenting and prototyping[1], [2], [3], [4] has  led us to identify a few tools and standards that we think would dramatically lower barriers to entry for application developers hoping to build with location / spatial data. Our intuition is that if we can identify and build versatile tools, devs will be able to build and innovate more quickly. A powerful second order effect of the adoption of shared tools and standards: the location-based decentralized web could develop the same properties of seamless composability that are emerging in DeFi.

Specifically, we’ve discovered that many location-based dapps have a need for what we’re calling **verifiable spatial data registries**. A verifiable spatial data registry is simply a smart contract that contains a registry of spatial data objects, such as vector features (i.e. points, lines, polygons or polyhedrons), or raster spatiotemporal assets (i.e. satellite images, LIDAR scans, etc.)

Different applications will require spatial data registries with various different properties and functionality. We’ve been exploring this design space, and intend to develop and publish verifiable spatial data registries that fulfill commonly-seen requirements. We suspect that there may be a strong case to adopt an ERC standard for these verifiable spatial data registries, so that secure contracts can be developed and so interoperable tooling can mature.

So what does this really mean? It probably will help to illustrate with examples and use cases, categorized into *vector* and *raster* data.

## Vector data registries

Vector data describes the relative positions of features - primarily points, lines, curves, polygons and polyhedra - within some spatial reference system (also called a coordinate reference system).

These spatial reference systems can represent a field on which to position features in an abstract space - like a metaverse environment - or on Earth / in relation to other physical objects. Vector data registries are intended to be versatile and accommodate both situations.

Quite a few instances of vector data registries have been developed and deployed on smart contract platforms. And many other dapps don’t explicitly use location data, but are intended to have some location element (like POAP). As examples:

- The FOAM Map, “a community-verified registry of crowdsourced places”, is a token-curated registry of points of interest.
- Virtual land projects like Etheria, Cryptovoxels, Decentraland and the Geo Web enable accounts to own digital “land” parcels, often as NFTs.
- The Regen Network’s Ecological State Database includes a “geo-polygon of the portion the Earth being referred to”.
- The Proof Of Attendance Protocol issues NFTs when people check in at a particular event, often only if they’re there in person.

Most location-based applications rely on the storage and computation of spatial data. Ridesharing platforms support certain service areas. Voters are entitled to cast ballots on certain issues or candidates based on the territorial jurisdictions where they live. Local taxes are paid based on where a business operates. Congestion zone systems delineate boundaries within which vehicles pay a fee.

We believe that these verifiable spatial data registries for vector data deserve deeper research, and that an ERC standard would mean that these registries could interoperate, and community-wide tooling could be built.

### Key Functionality

In our survey of the applications that rely on verifiable spatial data registry, we’ve identified a number of common requirements. These include:

- A spatial reference system.
- Some way of encoding coordinates: [lon, lat]. Sometimes may include a third value, height - i.e. [x, y, z].
- For most registries, a way of encoding polygons - which are, to date, typically restricted to raster cells, i.e. square or hex pixels. The registries we are designing will support irregular polygons.
- Functionality to detect whether polygon features overlap or intersect.
- Fast lookups, likely with some indexing system.
- Coordinate conversions, from Solidity-friendly data to web standards (like decimal degrees).
- Governance over who has the authority to mint or modify registry entries.

We anticipate that a range of different vector spatial registries would be useful. Currently, we’re thinking `PointRegistry`, `LinestringRegistry`, `PolygonRegistry`, `PolyhedronRegistry`, along with registries of a regular arrangement of polygons such as `GridRegistry` and `HexRegistry`.

### What does this enable?

If deployed on an open smart contract platform, these registries are, of course, composable. If we include useful methods and provide access to relevant data, we believe some interesting applications could be built. Open registries could be created: for example, a polygon registry of the watersheds of the world, and a point registry of national capitals.

One of the key pieces of functionality we hope to enable: local contracts, or smart contracts that are bound to a local area. With polygon registries, we would have the geographic areas represented on chain - if a user submitted a GPS position or FOAM presence claim, contract logic could be adapted based on whether the point supplied is contained within the boundaries of a specific zone:

```solidity
IPolygonRegistry polygonRegistry = IPolygonRegistry("0x...");

modifier onlyWithin(uint[2] _coords, uint _zoneId) {
    require polygonRegistry.pointInPolygon(_coords, _zoneId);
    _;
}
```

On top of this, methods performing on-chain computational geometry could determine the distance between points / the length of a line / perimeter of a polygon, whether polygons intersect, etc. Vector features could also be returned: the coordinate array, a polygon with buffer of a certain radius etc. We can’t anticipate the breadth of applications that might be enabled by this new functionality. We’ve explored apps in broad ranging areas like parametric insurance, congestion zones, spatial and sustainable finance, fitness tracking, ride sharing / e-mobility, transportation and logistics, location-based / AR gaming, etc.

### Dependencies

Certain functionality is required to support a comprehensive suite of vector spatial data registries. This gets especially difficult if we need to support irregular polygons and not simply raster grids - though we believe that support for irregular polygons is required to support “real world” applications, i.e. registries with zones on Earth.

To achieve this, we have been developing a Solidity library of topological and geometric functions so we can perform on-chain computational geometry: `Spatial.sol`. This library requires us to complete a library developed by Lefteris Karapetsas in 2016-2018: `Trigonometry.sol` (which lacked a `tan` function, required for `bearing` and `length` functions, among others).

`Spatial.sol` will be essentially a translation of common spatial analysis libraries like Turf.js, Shapely, and PostGIS’s geometry engine.

It seems that a standard interface for `Spatial.sol` would be useful for interoperability and backwards compatibility. This is very much open to community input - at the moment we are working out which functions are necessary for v0 of the library.

Proposed Methods for `Spatial.sol` include: `sin`, `cos`, `tan`, `isPoint`, `isLinestring`, `isPolygon`, `sqrt`, `distance`, `area`, `perimeter`, `bbox`, `bearing`, `centroid`, `distanceEuclidean`, `distanceHaversine`, `length`, `booleanContains`, `booleanCrosses`, `booleanDisjoint`, `booleanEqual` , `booleanParallel`, `booleanPointInPolygon`, `booleanPointOnLine`, `booleanWithin`.

We also see likely need for helper functions like conversions between degrees and radians and, possibly, working with different measurement units.

With `Spatial.sol`, we will have the functionality required to support the different verifiable spatial data registries we want to design, *including irregular polygons*.

[![pt-in-poly](https://ethereum-magicians.org/uploads/default/original/2X/1/1b2acb59528466fc11ed22b0f97eadbfd6007a86.gif)pt-in-poly317×200 4.67 KB](https://ethereum-magicians.org/uploads/default/1b2acb59528466fc11ed22b0f97eadbfd6007a86)

*from Darel Rex Finley.*

#### eth-spatial.js / eth-spatial.py

Due to the constraints of the EVM, client libraries will be useful to ease the developer’s experience in translating between commonly-used data formats on the web (like GeoJSON) and EVM-compatible spatial data formats. The idea here is to easily accept web-friendly data, convert it so it’s compatible with Spatial.sol, and vice versa, so data read from the chain can be visualized in the browser with Leaflet or Mapbox GL JS, or seamlessly work in common python libraries like Shapely or geopandas.

## Raster data registries

There is another category of spatial data registries with a different set of use cases. We’ve done some research on the feasibility of raster data registries - mainly for registering satellite imagery and other raster datasets.

These registries have quite a different set of requirements to vector registries, and most likely would not store the spatial data on chain, but rather a reference to the data asset (like an IPFS CID, perhaps identifying an IPLD-encoded GeoTIFF - see the Astral docs).

We anticipate that raster data registries could be very useful in certain spatial finance applications, where outputs derived from analyzed satellite imagery are submitted to a smart contract. Including a reference to a record in a raster spatial data registry - i.e. to a specific satellite image registered on a smart contract - anyone could verify for themselves that the action taken on chain (like adjusting an interest rate or triggering the transfer of some indemnity) was correct.

While this is its own vein of interesting research, raster data registries are the topic of another post.

# Questions / Additional Content

- Is it easy to support mixed type registries? Or should we require all records in a registry be the same (i.e. all points, or lines, or polygons)?
- On chain vs off chain spatial data.
- More advanced geodetic functionality

Euclidean distance
- Haversine distance
- Support for multiple coordinate reference systems and on-chain geodetic transformations? i.e. Proj4.sol???

Layer 2 compatibility?
Universal location proofs and zero-knowledge location proofs: docs.astral.global/workplan/universal-location-proofs?
What is the best approach re: architectural design? For example, for many applications (especially in the metaverse) geospatial functionality would be required. Should we split out `Geospatial` from `Spatial`? i.e. `contract Geospatial is Spatial {}`? Raises questions about simplicity vs efficiency …
Is this even an appropriate use for a library? Maybe it should simply be a contract that contains methods and attributes that would be used by the spatial registries? Something like: `contract PolygonRegistry is Spatial { /* ... */ }` or `contract EtherverseParcels is GridRegistry { /* ... */ }`

# Get involved

We are working on designing these registries at Astral - if you’re interested, drop into our Discord (Cpz9RnGxwp) and say hello. ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=15)

## Footnotes

[1] Hyperaware: a spatial governance protocol for connected devices.

[2] Location-aware wallet: a smart contract-based crypto wallet with the ability to adapt behavior based on a user’s location.

[3] Geolocker: an early iteration of a spatial data registry on Ethereum.

[4] Sprout: a sustainability-linked bond in Solidity.
