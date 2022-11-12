// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

//Override keyword for the function jiska modification kar rahe and child class/contract ka hai.
import "./SimpleStorage.sol";
contract ExtendedStorage is SimpleStorage {
function store(uint256 _favoriteNumber) public override {
        favoriteNumber = _favoriteNumber + 5;
    }
}