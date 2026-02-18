---
source: magicians
topic_id: 10553
title: EIP-5999 - Legal Use, Sharing, Repurposing, and Remixing Standard compatible with Creative Commons
author: izkp
date: "2022-08-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5999-legal-use-sharing-repurposing-and-remixing-standard-compatible-with-creative-commons/10553
views: 1977
likes: 1
posts_count: 1
---

# EIP-5999 - Legal Use, Sharing, Repurposing, and Remixing Standard compatible with Creative Commons

We have drafted a standard interface and licensing scheme for describing and enforcing the use, sharing, repurposing, and remixing rights associated with an NFT. We intend to establish an on-chain registry of IP rights associated with NFTs, and the corresponding attribution and derivative links.

NFTs still face legal uncertainty, and many now realize that the rights associated with an NFT are just as important as the NFT itself. Our goal is to help the ecosystem reach clear consensus and broad understanding of what purchasers of NFTs are acquiring in terms of copyright or other rights.

EIP-5999 tokens extend any other token standard to provide:

- Explicit rights for the token holder related to commercial exploitation, derivative works, and reproduction;
- EIP-5218 interface for creating, viewing, and checking the status of licenses
- Standard format for extended license information in the token metadata;
- Standard events to track off chain creation of derivative works, commercial exploitation, and reproduction;
- On chain tracking of derivative works and reproductions
- Additional required fields in the smart contract to reference the copyright owner
- Function calls for commercial exploitation, derivative works and reproduction.

```auto
interface IERC5999 is IERC5218 {

    event CommercialExploitation(uint256 _tokenId, uint256 _licenseId, string _externalUri);
    event ReproductionCreated(uint256 _tokenId, uint256 _licenseId, address _reproduction);
    event DerivativeCreated(uint256 _tokenId, uint256 _licenseId, address _derivative);

    /// @notice Retrieve the copyright owner address
    /// @dev Throws unless the token exists
    /// @param tokenId The identifier for the queried token
    /// @return address of the copyright owner
    function getCopyrightOwner(uint256 tokenId)
        external
        virtual
        returns (address);

    /// @notice Requests to log an execution of a license
    /// @dev Throws unless the token issuance conditions are met
    /// @param tokenId The identifier for the queried token
    /// @return uint256 tracking reproduction ID
    function logReproduction(uint256 tokenId, address reproduction)
        external
        virtual
        returns (uint256);

    /// @notice Requests to log an executions of a license
    /// @dev Throws unless the token issuance conditions are met
    /// @param tokenId The identifier for the queried token
    /// @return uint256 tracking derivative ID
    function logDerivative(uint256 tokenId, address derivative)
        external
        virtual
        returns (uint256);

    /// @notice Requests to log an execution of a license
    /// @dev Throws unless the commercial exploitation conditions are met
    /// @param tokenId The identifier for the queried token
    function logCommercialExploitation(uint256 tokenId, string calldata uri)
        external;

    /// @notice Retrieve the token associated with a reproduction
    /// @dev Throws unless the reproduction exists
    /// @param _reproductionId The identifier for the reproduction
    /// @return uint256 The identifier for the token used to generate the reproduction
    function getReproductionTokenId(uint256 _reproductionId)
        external
        view
        returns (uint256);

    /// @notice Retrieve the token associated with a reproduction
    /// @dev Throws unless the reproduction exists
    /// @param _reproductionId The identifier for the reproduction
    /// @return uint256 The identifier for the license used to generate the reproduction
    function getReproductionLicenseId(uint256 _reproductionId)
        external
        view
        returns (uint256);

    /// @notice Retrieve the token associated with a reproduction
    /// @dev Throws unless the reproduction exists
    /// @param _reproductionId The identifier for the derivative work
    /// @return address The address of the reproduction collection
    function getReproductionCollection(uint256 _reproductionId)
        external
        view
        returns (address);

    /// @notice Retrieve the token associated with a derivative
    /// @dev Throws unless the derivative exists
    /// @param _derivativeId The identifier for the derivative work
    /// @return uint256 The identifier for the token used to generate the derivative work
    function getDerivativeTokenId(uint256 _derivativeId)
        external
        view
        returns (uint256);

    /// @notice Retrieve the token associated with a derivative
    /// @dev Throws unless the derivative exists
    /// @param _derivativeId The identifier for the derivative work
    /// @return uint256 The identifier for the license used to generate the derivative work
    function getDerivativeLicenseId(uint256 _derivativeId)
        external
        view
        returns (uint256);

    /// @notice Retrieve the token associated with a derivative
    /// @dev Throws unless the derivative exists
    /// @param _derivativeId The identifier for the derivative work
    /// @return address The address of the derivative collection
    function getDerivativeCollection(uint256 _derivativeId)
        external
        view
        returns (address);

}
```

We have an ongoing task force working on this specification and implementations. If anyone would like to join feel free to email me at [ipatka@gmail.com](mailto:ipatka@gmail.com).
