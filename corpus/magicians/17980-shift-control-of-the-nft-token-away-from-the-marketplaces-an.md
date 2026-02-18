---
source: magicians
topic_id: 17980
title: Shift control of the nft token away from the marketplaces and back to the nft contract
author: codetributor
date: "2024-01-09"
category: Magicians > Primordial Soup
tags: [token, erc-721]
url: https://ethereum-magicians.org/t/shift-control-of-the-nft-token-away-from-the-marketplaces-and-back-to-the-nft-contract/17980
views: 437
likes: 0
posts_count: 1
---

# Shift control of the nft token away from the marketplaces and back to the nft contract

```auto
pragma solidity >=0.8.0  Token[]) private _balances;
	mapping(uint256 tokenId => Token) private tokens;

	address[] blacklist;

	constructor(string memory name, string memory symbol) {
		_name = name;
		_symbol = symbol;
	}

	function checkIfBlacklisted(address _receipient) private view returns(bool) {
		for(uint i = 0; i < blacklist.length; i++) {
			if(_receipient == blacklist[i]) {
				return true;
			}
		}
		return false;
	}

	function mint() public {
		uint256 tokenId = _nextTokenId++;
		Token memory token = Token(tokenId, msg.sender, false, address(0), false, 0, "", 20, address(0), 0, false);
		tokens[tokenId] = token;
		_balances[msg.sender].push(token);
	}

	function makeClaimable(uint256 _tokenId, uint256 _price) public {
		require(tokens[_tokenId].tokenOwner == msg.sender, "you are not the owner");
		tokens[_tokenId].claimable = true;
		tokens[_tokenId].price = _price;
	}

	function changePrice(uint256 _tokenId, uint256 _price) public {
		require(tokens[_tokenId].tokenOwner == msg.sender, "you are not the owner");
		tokens[_tokenId].price = _price;
	}

	function setSpecifiedClaimant(address _specifiedClaimant, uint256 _tokenId) public {
		require(tokens[_tokenId].tokenOwner == msg.sender, "you are not the owner");
		require(checkIfBlacklisted(_specifiedClaimant) == false, "blacklisted");
		tokens[_tokenId].isSpecifiedClaimant = true;
		tokens[_tokenId].specifiedClaimant = _specifiedClaimant;
	}

	function addToMarketplace(uint256 _tokenId, address _marketAddress, uint256 _marketFee) public {
		tokens[_tokenId].isMarketplace = true;
		tokens[_tokenId].marketplaceFee = _marketFee;
		tokens[_tokenId].marketplaceAddress = _marketAddress;
	}

	function claim(uint256 _tokenId) public payable {
		require( tokens[_tokenId].price <= msg.value, "you did not send enough currency");
		uint royaltyPercentage = tokens[_tokenId].royalty;
		uint sellValue = msg.value * (100 - royaltyPercentage)/100;
		uint royaltyFee= msg.value * royaltyPercentage/100;
		payout(_tokenId, royaltyFee, sellValue);

	}

	function payout(uint256 _tokenId, uint256 _royaltyFee, uint256 _sellValue) public {
		if(tokens[_tokenId].isSpecifiedClaimant) {
			require(checkIfBlacklisted(msg.sender) == false, "blacklisted");
			require(tokens[_tokenId].specifiedClaimant == msg.sender, "you are not the specified claimant");
			(bool success0, ) = tokens[_tokenId].tokenOwner.call{value: _sellValue}("");
			(bool success1, ) = address(this).call{value: _royaltyFee}("");
			removeToken(_tokenId, tokens[_tokenId].tokenOwner);
			tokens[_tokenId].tokenOwner = msg.sender;
			require(success0 && success1, "distribution did not go through");
		} else {
			(bool success0, ) = tokens[_tokenId].tokenOwner.call{value: _sellValue}("");
			(bool success1, ) = address(this).call{value: _royaltyFee}("");
			removeToken(_tokenId, tokens[_tokenId].tokenOwner);
			tokens[_tokenId].tokenOwner = msg.sender;
			require(success0 && success1, "distribution did not go through");
		}
	}

	function removeToken(uint256 _tokenId, address _previousOwner) public {
		for(uint i = 0; i < _balances[_previousOwner].length; i++) {
			if(_tokenId == _balances[_previousOwner][i].tokenId) {
				_balances[_previousOwner][i] = _balances[_previousOwner][_balances[_previousOwner].length - 1];
				_balances[_previousOwner].pop();
			}
		}
	}
}```
```
