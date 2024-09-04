// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CredentialContract {

    struct Credential {
        string credentialType;
        string fileLink; // The link of the uploaded credential file
        address issuer;
        address holder;
        bytes32 credentialHash; // The hash of the certificate
        uint256 timestamp;
        bool valid;
    }

    mapping(bytes32 => Credential) private credentialsByHash; // Mapping from credential hash to Credential
    mapping(address => Credential[]) private credentialsByHolder; // Mapping from holder address to their credentials

    event CredentialIssued(address indexed issuer, address indexed holder, string credentialType, bytes32 credentialHash, uint256 timestamp);
    event CredentialVerified(address indexed holder, bytes32 credentialHash, bool valid, uint256 timestamp);

    // Function to issue a credential
    function issueCredential(
        address issuerWalletAddress,
        address holderWalletAddress,
        string memory credentialType,
        string memory fileLink
    ) public returns (bytes32) {
        // Generate the credential hash
        bytes32 credentialHash = keccak256(abi.encodePacked(issuerWalletAddress, holderWalletAddress, credentialType, fileLink, block.timestamp));

        Credential memory newCredential = Credential({
            credentialType: credentialType,
            fileLink: fileLink,
            issuer: issuerWalletAddress,
            holder: holderWalletAddress,
            credentialHash: credentialHash,
            timestamp: block.timestamp,
            valid: true
        });

        // Store the issued credential in the mappings
        credentialsByHash[credentialHash] = newCredential;
        credentialsByHolder[holderWalletAddress].push(newCredential);

        // Emit the CredentialIssued event
        emit CredentialIssued(issuerWalletAddress, holderWalletAddress, credentialType, credentialHash, block.timestamp);

        // Return the credential hash
        return credentialHash;
    }

    // Function to verify a credential using its hash and holder's address
    function verifyCredential(
        bytes32 credentialHash,
        address holderWalletAddress
    ) public returns (bool) {
        Credential memory cred = credentialsByHash[credentialHash];
        require(cred.holder == holderWalletAddress, "The holder address does not match the credential holder.");

        bool isValid = cred.valid;

        emit CredentialVerified(holderWalletAddress, credentialHash, isValid, block.timestamp);

        return isValid;
    }

    // Function to get certificate details if the verification is successful
    function getCertificateDetail(
        bytes32 credentialHash,
        address holderWalletAddress
    ) public view returns (string memory, string memory, address, address, uint256, bool) {
        Credential memory cred = credentialsByHash[credentialHash];
        
        // Check if the credential exists and the holder matches
        require(cred.holder == holderWalletAddress, "Verification failed: Holder address does not match or credential does not exist.");

        // Return the certificate details
        return (
            cred.credentialType,
            cred.fileLink,
            cred.issuer,
            cred.holder,
            cred.timestamp,
            cred.valid
        );
    }

    // Function to retrieve all certificates for a specific holder
    function getAllCertificates(address holderWalletAddress) public view returns (Credential[] memory) {
        return credentialsByHolder[holderWalletAddress];
    }
}
