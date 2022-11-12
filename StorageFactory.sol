// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;
import "./SimpleStorage.sol";

contract StorageFactory {

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    //sf stands for storage factory
    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNum) public {
        //SimpleStorage simpleStorage = simpleStorageArray[_simpleStorageIndex];
        simpleStorageArray[_simpleStorageIndex].store(_simpleStorageNum);
    }

    function sfGet(uint256 _simpleStorageIndex) view public returns(uint256) {
        SimpleStorage simpleStorage = simpleStorageArray[_simpleStorageIndex];
        return simpleStorage.retrieve();
    }
}

    