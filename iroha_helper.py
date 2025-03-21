import os
import binascii
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc
import sys
from Crypto.Hash import keccak
import json
import logging
import integration_helpers
from loguru import logger
from dump_to_json import dump_to_json_ld, dump_project_to_json_ld
from ipfs_functions import *
import time


from typing import Optional


# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

# Load configuration from config.json file
config_path = "config.json"  # Update this path as needed
with open(config_path, "r") as f:
    config = json.load(f)

IROHA_HOST_ADDR = config["IROHA_HOST_ADDR"]
IROHA_PORT = config["IROHA_PORT"]
ADMIN_ACCOUNT_ID = config["ADMIN_ACCOUNT_ID"]
ADMIN_PRIVATE_KEY = config["ADMIN_PRIVATE_KEY"]
iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc("{}:{}".format(IROHA_HOST_ADDR, IROHA_PORT))


@integration_helpers.trace
def create_account_contract():
    bytecode = "608060405234801561001057600080fd5b5073a6abc17819738299b3b2c1ce46d55c74f04e290c6000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061096b806100746000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80634518f6b314610046578063bc53c0c414610076578063d4e804ab146100a6575b600080fd5b610060600480360381019061005b9190610486565b6100c4565b60405161006d91906106ad565b60405180910390f35b610090600480360381019061008b91906104c7565b610230565b60405161009d91906106ad565b60405180910390f35b6100ae6103fa565b6040516100bb9190610692565b60405180910390f35b60606000826040516024016100d991906106cf565b6040516020818303038152906040527f4518f6b3000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16836040516101a09190610664565b600060405180830381855af49150503d80600081146101db576040519150601f19603f3d011682016040523d82523d6000602084013e6101e0565b606091505b509150915081610225576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161021c9061073d565b60405180910390fd5b809350505050919050565b60606000848484604051602401610249939291906106f1565b6040516020818303038152906040527fbc53c0c4000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16836040516103109190610664565b600060405180830381855af49150503d806000811461034b576040519150601f19603f3d011682016040523d82523d6000602084013e610350565b606091505b509150915081610395576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161038c9061073d565b60405180910390fd5b856040516103a3919061067b565b6040518091039020876040516103b9919061067b565b60405180910390207fb4086b7a9e5eac405225b6c630a4147f0a8dcb4af3583733b10db7b91ad21ffd60405160405180910390a38093505050509392505050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600061043161042c84610782565b61075d565b90508281526020810184848401111561044957600080fd5b610454848285610833565b509392505050565b600082601f83011261046d57600080fd5b813561047d84826020860161041e565b91505092915050565b60006020828403121561049857600080fd5b600082013567ffffffffffffffff8111156104b257600080fd5b6104be8482850161045c565b91505092915050565b6000806000606084860312156104dc57600080fd5b600084013567ffffffffffffffff8111156104f657600080fd5b6105028682870161045c565b935050602084013567ffffffffffffffff81111561051f57600080fd5b61052b8682870161045c565b925050604084013567ffffffffffffffff81111561054857600080fd5b6105548682870161045c565b9150509250925092565b61056781610801565b82525050565b6000610578826107b3565b61058281856107c9565b9350610592818560208601610842565b61059b816108d5565b840191505092915050565b60006105b1826107b3565b6105bb81856107da565b93506105cb818560208601610842565b80840191505092915050565b60006105e2826107be565b6105ec81856107e5565b93506105fc818560208601610842565b610605816108d5565b840191505092915050565b600061061b826107be565b61062581856107f6565b9350610635818560208601610842565b80840191505092915050565b600061064e6027836107e5565b9150610659826108e6565b604082019050919050565b600061067082846105a6565b915081905092915050565b60006106878284610610565b915081905092915050565b60006020820190506106a7600083018461055e565b92915050565b600060208201905081810360008301526106c7818461056d565b905092915050565b600060208201905081810360008301526106e981846105d7565b905092915050565b6000606082019050818103600083015261070b81866105d7565b9050818103602083015261071f81856105d7565b9050818103604083015261073381846105d7565b9050949350505050565b6000602082019050818103600083015261075681610641565b9050919050565b6000610767610778565b90506107738282610875565b919050565b6000604051905090565b600067ffffffffffffffff82111561079d5761079c6108a6565b5b6107a6826108d5565b9050602081019050919050565b600081519050919050565b600081519050919050565b600082825260208201905092915050565b600081905092915050565b600082825260208201905092915050565b600081905092915050565b600061080c82610813565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b82818337600083830152505050565b60005b83811015610860578082015181840152602081019050610845565b8381111561086f576000848401525b50505050565b61087e826108d5565b810181811067ffffffffffffffff8211171561089d5761089c6108a6565b5b80604052505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f8301169050919050565b7f4572726f722063616c6c696e67207365727669636520636f6e7472616374206660008201527f756e6374696f6e0000000000000000000000000000000000000000000000000060208201525056fea2646970667358221220507121dff2241b458fa4a533cbbe922dffa784916f897d246f53d353adefc14664736f6c63430008040033"
    """Bytecode was generated using remix editor  https://remix.ethereum.org/ from file account.sol. """
    tx = iroha.transaction(
        [iroha.command("CallEngine", caller=ADMIN_ACCOUNT_ID, input=bytecode)]
    )
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    net.send_tx(tx)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    for status in net.tx_status_stream(tx):
        logger.info(status)
    integration_helpers.get_engine_receipts_address(hex_hash)    
    return hex_hash

@integration_helpers.trace
def create_detail_contract():
    bytecode = "608060405234801561001057600080fd5b5073a6abc17819738299b3b2c1ce46d55c74f04e290c6000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550610b4c806100746000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c80635bdb3a41146100515780637949a1b31461006f578063b7d66df71461009f578063d4e804ab146100cf575b600080fd5b6100596100ed565b6040516100669190610879565b60405180910390f35b61008960048036038101906100849190610627565b61024c565b6040516100969190610879565b60405180910390f35b6100b960048036038101906100b49190610693565b6103bb565b6040516100c69190610879565b60405180910390f35b6100d761059b565b6040516100e4919061085e565b60405180910390f35b606060006040516024016040516020818303038152906040527f5bdb3a41000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16836040516101be9190610830565b600060405180830381855af49150503d80600081146101f9576040519150601f19603f3d011682016040523d82523d6000602084013e6101fe565b606091505b509150915081610243576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161023a9061091e565b60405180910390fd5b80935050505090565b60606000838360405160240161026392919061089b565b6040516020818303038152906040527f7949a1b3000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168360405161032a9190610830565b600060405180830381855af49150503d8060008114610365576040519150601f19603f3d011682016040523d82523d6000602084013e61036a565b606091505b5091509150816103af576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016103a69061091e565b60405180910390fd5b80935050505092915050565b606060008484846040516024016103d4939291906108d2565b6040516020818303038152906040527fb7d66df7000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168360405161049b9190610830565b600060405180830381855af49150503d80600081146104d6576040519150601f19603f3d011682016040523d82523d6000602084013e6104db565b606091505b509150915081610520576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105179061091e565b60405180910390fd5b8460405161052e9190610847565b6040518091039020866040516105449190610847565b60405180910390208860405161055a9190610847565b60405180910390207f5e1b38cd47cf21b75d5051af29fa321eedd94877db5ac62067a076770eddc9d060405160405180910390a48093505050509392505050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60006105d26105cd84610963565b61093e565b9050828152602081018484840111156105ea57600080fd5b6105f5848285610a14565b509392505050565b600082601f83011261060e57600080fd5b813561061e8482602086016105bf565b91505092915050565b6000806040838503121561063a57600080fd5b600083013567ffffffffffffffff81111561065457600080fd5b610660858286016105fd565b925050602083013567ffffffffffffffff81111561067d57600080fd5b610689858286016105fd565b9150509250929050565b6000806000606084860312156106a857600080fd5b600084013567ffffffffffffffff8111156106c257600080fd5b6106ce868287016105fd565b935050602084013567ffffffffffffffff8111156106eb57600080fd5b6106f7868287016105fd565b925050604084013567ffffffffffffffff81111561071457600080fd5b610720868287016105fd565b9150509250925092565b610733816109e2565b82525050565b600061074482610994565b61074e81856109aa565b935061075e818560208601610a23565b61076781610ab6565b840191505092915050565b600061077d82610994565b61078781856109bb565b9350610797818560208601610a23565b80840191505092915050565b60006107ae8261099f565b6107b881856109c6565b93506107c8818560208601610a23565b6107d181610ab6565b840191505092915050565b60006107e78261099f565b6107f181856109d7565b9350610801818560208601610a23565b80840191505092915050565b600061081a6027836109c6565b915061082582610ac7565b604082019050919050565b600061083c8284610772565b915081905092915050565b600061085382846107dc565b915081905092915050565b6000602082019050610873600083018461072a565b92915050565b600060208201905081810360008301526108938184610739565b905092915050565b600060408201905081810360008301526108b581856107a3565b905081810360208301526108c981846107a3565b90509392505050565b600060608201905081810360008301526108ec81866107a3565b9050818103602083015261090081856107a3565b9050818103604083015261091481846107a3565b9050949350505050565b600060208201905081810360008301526109378161080d565b9050919050565b6000610948610959565b90506109548282610a56565b919050565b6000604051905090565b600067ffffffffffffffff82111561097e5761097d610a87565b5b61098782610ab6565b9050602081019050919050565b600081519050919050565b600081519050919050565b600082825260208201905092915050565b600081905092915050565b600082825260208201905092915050565b600081905092915050565b60006109ed826109f4565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b82818337600083830152505050565b60005b83811015610a41578082015181840152602081019050610a26565b83811115610a50576000848401525b50505050565b610a5f82610ab6565b810181811067ffffffffffffffff82111715610a7e57610a7d610a87565b5b80604052505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f8301169050919050565b7f4572726f722063616c6c696e67207365727669636520636f6e7472616374206660008201527f756e6374696f6e0000000000000000000000000000000000000000000000000060208201525056fea26469706673582212206ad40afbd4cc9c87ae154542d003c9538e4b89473a13cadd3cbf618ea181206864736f6c63430008040033"
    """Bytecode was generated using remix editor  https://remix.ethereum.org/ from file detail.sol. """
    tx = iroha.transaction(
        [iroha.command("CallEngine", caller=ADMIN_ACCOUNT_ID, input=bytecode)]
    )
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    net.send_tx(tx)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    for status in net.tx_status_stream(tx):
        logger.info(status)
    integration_helpers.get_engine_receipts_address(hex_hash)   
    return hex_hash

@integration_helpers.trace
def create_user_account(address, user_account_short_id, DOMAIN, user_public_key, user_account):
    params = integration_helpers.get_first_four_bytes_of_keccak(
        b"createAccount(string,string,string)"
    )
    no_of_param = 3
    for x in range(no_of_param):
        params = params + integration_helpers.left_padded_address_of_param(
            x, no_of_param
        )
    params = params + integration_helpers.argument_encoding(user_account_short_id)  # source account id
    params = params + integration_helpers.argument_encoding(DOMAIN)  # domain id
    params = params + integration_helpers.argument_encoding(user_public_key)  #  key
    tx = iroha.transaction(
        [
            iroha.command(
                "CallEngine", caller=ADMIN_ACCOUNT_ID, callee=address, input=params
            )
        ]
    )
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    response = net.send_tx(tx)
    for status in net.tx_status_stream(tx):
        logger.info(status)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    line_number = dump_to_json_ld(user_account) #dumps this data to dataset/accounts.json for later use.
    # return hex_hash


@integration_helpers.trace
def create_project_account(address, project_id, DOMAIN, project_public_key):
    params = integration_helpers.get_first_four_bytes_of_keccak(
        b"createAccount(string,string,string)"
    )
    no_of_param = 3
    for x in range(no_of_param):
        params = params + integration_helpers.left_padded_address_of_param(
            x, no_of_param
        )
    params = params + integration_helpers.argument_encoding(project_id)  # source account id
    params = params + integration_helpers.argument_encoding(DOMAIN)  # domain id
    params = params + integration_helpers.argument_encoding(project_public_key)  #  key
    tx = iroha.transaction(
        [
            iroha.command(
                "CallEngine", caller=ADMIN_ACCOUNT_ID, callee=address, input=params
            )
        ]
    )
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    response = net.send_tx(tx)
    for status in net.tx_status_stream(tx):
        logger.info(status)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    line_number = dump_project_to_json_ld(f"{project_id}@{DOMAIN}", project_public_key) #dumps this data to dataset/projects.json for later use.
    logger.info(line_number)
    # return hex_hash

@integration_helpers.trace
def set_account_detail(address, account, key, value):
    """
    Executes a transaction to update the details of an existing account.

    Args:
        address (str): The smart contract address.
        account (str): The source account ID.
        key (str): The key to update.
        value (str): The value to set.

    Returns:
        str: The transaction hash in hexadecimal form.
    """
    # Generate the params for the "setAccountDetail" function
    params = integration_helpers.get_first_four_bytes_of_keccak(
        b"setAccountDetail(string,string,string)"
    )
    no_of_param = 3
    for x in range(no_of_param):
        params = params + integration_helpers.left_padded_address_of_param(x, no_of_param)
    params = params + integration_helpers.argument_encoding(account)  # source account id
    params = params + integration_helpers.argument_encoding(key)      # key
    params = params + integration_helpers.argument_encoding(value)    # value

    # Create a transaction to call the engine
    tx = iroha.transaction(
        [
            iroha.command(
                "CallEngine", caller=ADMIN_ACCOUNT_ID, callee=address, input=params
            )
        ]
    )

    # Sign and send the transaction
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    response = net.send_tx(tx)

    # Log the response and statuses
    logger.info(response)
    committed = False
    for status in net.tx_status_stream(tx):
        logger.info(f"Transaction status: {status}")
        if status == "COMMITTED":
            committed = True

    if not committed:
        logger.error("Transaction was not committed.")
        return None

    # Get the transaction hash in hex form
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx)).decode('utf-8')

    # Retrieve and decode engine receipts
    result = integration_helpers.get_engine_receipts_result(hex_hash)
    if result:
        logger.info(f"Decoded Engine Receipts Result: {result}")
    else:
        logger.error("Failed to retrieve or decode Engine Receipts.")
    
    return hex_hash


# Function to update user account with linked project
def update_user_account_link(user_account_id, linked_project_id, accounts_filename="logs/accounts.json"):
    try:
        if os.path.exists(accounts_filename):
            with open(accounts_filename, mode='r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            logger.info(f"{accounts_filename} does not exist.")
            return

        user_found = False

        # Look for the user account and update it
        for entry in data["@graph"]:
            if entry["@type"] == "foaf:Person" and entry.get("foaf:holdsAccount", {}).get("schema:identifier") == user_account_id:
                entry["schema:linked_project"] = linked_project_id
                user_found = True
                logger.info(f"Updated user account {user_account_id} with linked project {linked_project_id}")
                break

        if not user_found:
            logger.info(f"User account {user_account_id} not found.")

        # Write back the updated data
        with open(accounts_filename, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        logger.info(f"Error updating user account in JSON-LD: {str(e)}")


# Function to update project account with linked user
def update_project_account_link(project_account_id, linked_user_id, projects_filename="logs/projects.json"):
    try:
        if os.path.exists(projects_filename):
            with open(projects_filename, mode='r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            logger.info(f"{projects_filename} does not exist.")
            return

        project_found = False

        # Look for the project account and update it
        for entry in data["@graph"]:
            if entry["@type"] == "schema:ResearchProject" and entry.get("schema:identifier") == project_account_id:
                entry["schema:linked_user"] = linked_user_id
                project_found = True
                logger.info(f"Updated project account {project_account_id} with linked user {linked_user_id}")
                break

        if not project_found:
            logger.info(f"Project account {project_account_id} not found.")

        # Write back the updated data
        with open(projects_filename, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        logger.info(f"Error updating project account in JSON-LD: {str(e)}")

@integration_helpers.trace
def get_account_detail(id):
    query = iroha.query('GetAccountDetail',account_id=id)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net.send_query(query)
    data = response.account_detail_response
    details = data.detail
    logger.info(f'Account id = {id}, {details}')
    return details  # Add this line to return the project details




# Function to dump data to JSON
@integration_helpers.trace
def append_to_json_file(file_path, id, domain, data):
    try:
        # Create the topmost key
        top_key = f"{id}@{domain}"

        # Check if the file exists, otherwise create an empty JSON structure
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({}, f)

        # Load the existing data from the file
        with open(file_path, 'r') as f:
            json_data = json.load(f)

        # Append data under the topmost key
        if top_key not in json_data:
            json_data[top_key] = []
        json_data[top_key].append(data)

        # Write the updated data back to the file
        with open(file_path, 'w') as f:
            json.dump(json_data, f, indent=4)

        logger.info(f"Appended data under '{top_key}' in {file_path}")
    except Exception as e:
        logger.error(f"Failed to append data to JSON file: {e}")

# Refactored get_account function
@integration_helpers.trace
def get_account(address, id, domain, json_file="logs/account_data.json"):
    try:
        logger.warning(f"create_account_contract_address: {address}")
        
        # Prepare the parameters for the transaction
        params = integration_helpers.get_first_four_bytes_of_keccak(b"getAccount(string)")
        no_of_param = 1
        for x in range(no_of_param):
            params += integration_helpers.left_padded_address_of_param(x, no_of_param)
        params += integration_helpers.argument_encoding(f"{id}@{domain}")  # project id

        # Create and sign the transaction
        tx = iroha.transaction(
            [
                iroha.command(
                    "CallEngine", caller=ADMIN_ACCOUNT_ID, callee=address, input=params
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)

        # Send the transaction and log the status
        response = net.send_tx(tx)
        for status in net.tx_status_stream(tx):
            logger.info(status)

        # Compute the hex hash of the transaction
        hex_hash = binascii.hexlify(IrohaCrypto.hash(tx)).decode()

        # Generate the timestamp in milliseconds
        timestamp_ms = int(time.time() * 1000)  # Current time in milliseconds

        # Prepare the data to be dumped into the JSON file
        account_data = {
            "address": address,
            "hex_hash": hex_hash,
            "timestamp": timestamp_ms
        }

        logger.warning(f"Account Data: {account_data}")
        
        # Append the data to the JSON file
        append_to_json_file(json_file, id, domain, account_data)

        return hex_hash
    except Exception as e:
        logger.error(f"Error in get_account: {e}")
        return None
    
# Functions provided earlier
@integration_helpers.trace
def get_project_details(project_ids, net, iroha):
    admin_private_key = ADMIN_PRIVATE_KEY
    project_accounts = []
    
    for project_id in set(project_ids):  # Remove duplicates by converting to a set
        query = iroha.query('GetAccountDetail', account_id=project_id)
        IrohaCrypto.sign_query(query, admin_private_key)
        response = net.send_query(query)
        project_data = response.account_detail_response
        project_details = project_data.detail
        logging.info(f"Project Account id = {project_id}, {project_details}")
        
        project_accounts.append({
            "account_id": project_id,
            "project_details": project_details
        })
    return project_accounts


#Deploys account detail setting contract
@integration_helpers.trace
def create_contract():
    bytecode = "608060405234801561001057600080fd5b5073a6abc17819738299b3b2c1ce46d55c74f04e290c6000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550610b4c806100746000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c80635bdb3a41146100515780637949a1b31461006f578063b7d66df71461009f578063d4e804ab146100cf575b600080fd5b6100596100ed565b6040516100669190610879565b60405180910390f35b61008960048036038101906100849190610627565b61024c565b6040516100969190610879565b60405180910390f35b6100b960048036038101906100b49190610693565b6103bb565b6040516100c69190610879565b60405180910390f35b6100d761059b565b6040516100e4919061085e565b60405180910390f35b606060006040516024016040516020818303038152906040527f5bdb3a41000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16836040516101be9190610830565b600060405180830381855af49150503d80600081146101f9576040519150601f19603f3d011682016040523d82523d6000602084013e6101fe565b606091505b509150915081610243576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161023a9061091e565b60405180910390fd5b80935050505090565b60606000838360405160240161026392919061089b565b6040516020818303038152906040527f7949a1b3000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168360405161032a9190610830565b600060405180830381855af49150503d8060008114610365576040519150601f19603f3d011682016040523d82523d6000602084013e61036a565b606091505b5091509150816103af576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016103a69061091e565b60405180910390fd5b80935050505092915050565b606060008484846040516024016103d4939291906108d2565b6040516020818303038152906040527fb7d66df7000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168360405161049b9190610830565b600060405180830381855af49150503d80600081146104d6576040519150601f19603f3d011682016040523d82523d6000602084013e6104db565b606091505b509150915081610520576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105179061091e565b60405180910390fd5b8460405161052e9190610847565b6040518091039020866040516105449190610847565b60405180910390208860405161055a9190610847565b60405180910390207f5e1b38cd47cf21b75d5051af29fa321eedd94877db5ac62067a076770eddc9d060405160405180910390a48093505050509392505050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60006105d26105cd84610963565b61093e565b9050828152602081018484840111156105ea57600080fd5b6105f5848285610a14565b509392505050565b600082601f83011261060e57600080fd5b813561061e8482602086016105bf565b91505092915050565b6000806040838503121561063a57600080fd5b600083013567ffffffffffffffff81111561065457600080fd5b610660858286016105fd565b925050602083013567ffffffffffffffff81111561067d57600080fd5b610689858286016105fd565b9150509250929050565b6000806000606084860312156106a857600080fd5b600084013567ffffffffffffffff8111156106c257600080fd5b6106ce868287016105fd565b935050602084013567ffffffffffffffff8111156106eb57600080fd5b6106f7868287016105fd565b925050604084013567ffffffffffffffff81111561071457600080fd5b610720868287016105fd565b9150509250925092565b610733816109e2565b82525050565b600061074482610994565b61074e81856109aa565b935061075e818560208601610a23565b61076781610ab6565b840191505092915050565b600061077d82610994565b61078781856109bb565b9350610797818560208601610a23565b80840191505092915050565b60006107ae8261099f565b6107b881856109c6565b93506107c8818560208601610a23565b6107d181610ab6565b840191505092915050565b60006107e78261099f565b6107f181856109d7565b9350610801818560208601610a23565b80840191505092915050565b600061081a6027836109c6565b915061082582610ac7565b604082019050919050565b600061083c8284610772565b915081905092915050565b600061085382846107dc565b915081905092915050565b6000602082019050610873600083018461072a565b92915050565b600060208201905081810360008301526108938184610739565b905092915050565b600060408201905081810360008301526108b581856107a3565b905081810360208301526108c981846107a3565b90509392505050565b600060608201905081810360008301526108ec81866107a3565b9050818103602083015261090081856107a3565b9050818103604083015261091481846107a3565b9050949350505050565b600060208201905081810360008301526109378161080d565b9050919050565b6000610948610959565b90506109548282610a56565b919050565b6000604051905090565b600067ffffffffffffffff82111561097e5761097d610a87565b5b61098782610ab6565b9050602081019050919050565b600081519050919050565b600081519050919050565b600082825260208201905092915050565b600081905092915050565b600082825260208201905092915050565b600081905092915050565b60006109ed826109f4565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b82818337600083830152505050565b60005b83811015610a41578082015181840152602081019050610a26565b83811115610a50576000848401525b50505050565b610a5f82610ab6565b810181811067ffffffffffffffff82111715610a7e57610a7d610a87565b5b80604052505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f8301169050919050565b7f4572726f722063616c6c696e67207365727669636520636f6e7472616374206660008201527f756e6374696f6e0000000000000000000000000000000000000000000000000060208201525056fea26469706673582212206ad40afbd4cc9c87ae154542d003c9538e4b89473a13cadd3cbf618ea181206864736f6c63430008040033"
    """Bytecode was generated using remix editor  https://remix.ethereum.org/ from file detail.sol. """
    tx = iroha.transaction(
        [iroha.command("CallEngine", caller=ADMIN_ACCOUNT_ID, input=bytecode)]
    )
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    net.send_tx(tx)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    for status in net.tx_status_stream(tx):
        logger.info(status)
    return hex_hash

# Helper function to simulate setting account details with Iroha
@integration_helpers.trace
def set_account_detail(address, account, key, value):
    # Generate the params for the "setAccountDetail" function
    params = integration_helpers.get_first_four_bytes_of_keccak(
        b"setAccountDetail(string,string,string)"
    )
    no_of_param = 3
    for x in range(no_of_param):
        params = params + integration_helpers.left_padded_address_of_param(
            x, no_of_param
        )
    params = params + integration_helpers.argument_encoding(account)  # source account id
    params = params + integration_helpers.argument_encoding(key)  # key
    params = params + integration_helpers.argument_encoding(value)  # value

    # Create a transaction to call the engine
    tx = iroha.transaction(
        [
            iroha.command(
                "CallEngine", caller=ADMIN_ACCOUNT_ID, callee=address, input=params
            )
        ]
    )
    
    # Sign and send the transaction
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    response = net.send_tx(tx)

    # Log the response and statuses
    logger.info(response)
    for status in net.tx_status_stream(tx):
        logger.info(status)
    
    # Get the transaction hash in hex form
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    integration_helpers.get_engine_receipts_result(hex_hash)
    return hex_hash


@integration_helpers.trace
def process_account(address, account_id):
    try:
        with open('logs/accounts.json', 'r', encoding='utf-8') as jsonldfile:
            data = json.load(jsonldfile)
            # logger.info(f"Processing data: {data}")
            
            # Find the account details for the specified ID
            account_metadata = next(
                (entry for entry in data['@graph'] if entry['foaf:holdsAccount']['schema:identifier'] == account_id),
                None
            )
            
            logger.info(f"Processing account: {account_id}")
            logger.info(f"User Account Metadata: {account_metadata}")

            # Uploads User JSON-LD to IPFS
            account_metadata_cid = upload_json_to_ipfs(account_metadata) 
            logger.info(f"User Account Metadata CID: {account_metadata_cid}")

            # Sends the resulting CID to Iroha 1
            hash = set_account_detail(address, account_id, "account_metadata_cid", account_metadata_cid)
            
            
            # get_account(hash) #Lets evolve this
            
            if account_metadata is None:
                logger.info(f"Account with ID '{account_id}' not found.")
                return
            
            
           
            
    except FileNotFoundError:
        logger.error("The JSON-LD file 'logs/accounts.json' does not exist.")
    except Exception as e:
        logger.error(f"Error processing account: {str(e)}")