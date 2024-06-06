pragma solidity >= 0.8.11 <= 0.8.11;

contract FakeProduct {
    string public user_details;
    string public product_details;

    function setUserDetails(string memory ud) public {
        user_details = ud;	
    }

    function getUserDetails() public view returns (string memory) {
        return user_details;
    }

    function setProductDetails(string memory pd) public {
        product_details = pd;	
    }

    function getProductDetails() public view returns (string memory) {
        return product_details;
    }

    constructor() public {
        user_details = "empty";
	product_details = "empty";
    }
}