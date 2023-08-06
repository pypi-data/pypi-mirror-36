Raiden Network Smart Contracts
==============================

.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/raiden-network/raiden?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Chat on Gitter

`Raiden Network Smart Contract specs`_

.. _Raiden Network Smart Contract specs: https://raiden-network-specification.readthedocs.io/en/latest/smart_contracts.html

Prerequisites
-------------

-  Python 3.6
-  https://pip.pypa.io/en/stable/

Installation
------------

Recommended::

    pip install raiden-contracts


Usage
-----

We do not recommend the smart contracts to be used in production before a stable ``1.0.0`` release is made. All contracts are WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Use at your own risk.

If you want to use the officially deployed contracts, please use the ``raiden_contracts/data/contracts.json`` file to get the ABI and bytecode for initializing the contract instances.

You can find the addresses of the deployed contracts in ``raiden_contracts/constants.py``, along with other useful constants that you can import.

If you are using the ``raiden-contracts`` package in your project, you can use::

    from raiden_contracts.contract_manager import (
        ContractManager,
        CONTRACTS_PRECOMPILED_PATH,
    )
    from raiden_contracts.constants import (
        CONTRACT_TOKEN_NETWORK_REGISTRY,
        ROPSTEN_TOKEN_NETWORK_REGISTRY_ADDRESS,
        EVENT_TOKEN_NETWORK_CREATED,
    )

    manager = ContractManager(CONTRACTS_PRECOMPILED_PATH)
    compiled_contract_data = manager.get_contract(CONTRACT_TOKEN_NETWORK_REGISTRY)
    # And then use:
    # compiled_contract_data['abi']
    # compiled_contract_data['bin']
    # ROPSTEN_TOKEN_NETWORK_REGISTRY_ADDRESS
    # to initialize the contract instance


All contracts under ``raiden_contracts/contracts/test/`` are only for testing purposes and they should not be used in production.

Development
-----------

If you want to test and further develop outside the officially provided source code, compiled files and deployed addresses, you can do it at your own risk.


If you want to install the package from source::

    make install

To verify that the precompiled ``raiden_contracts/data/contracts.json`` file corresponds to the source code of the contracts::

    make verify_contracts

For development and testing, you have to install additional dependencies::

    pip install -r requirements-dev.txt


Compile the contracts
^^^^^^^^^^^^^^^^^^^^^

Make sure you have `solc` installed: https://solidity.readthedocs.io/en/latest/installing-solidity.html

::

    make compile_contracts


Testing
^^^^^^^

::

    # tests
    pytest
    pytest raiden_contracts/tests/test_token_network.py

    # Recommended for speed:
    pip install pytest-xdist==1.17.1
    pytest -n NUM_OF_CPUs


If you are using the ``raiden-contracts`` package in your project, you can also test the source code directly (not only the precompiled contract data)::

    from raiden_contracts.contract_manager import (
        ContractManager,
        CONTRACTS_SOURCE_DIRS,
    )

    manager = ContractManager(CONTRACTS_SOURCE_DIRS)


Deployment on a testnet
^^^^^^^^^^^^^^^^^^^^^^^

Check deployment options::

    python -m raiden_contracts.deploy --help

Deploying the main Raiden Network contracts with the ``raiden`` command::

    python -m raiden_contracts.deploy raiden --rpc-provider http://127.0.0.1:8545 --private-key /path/to/your/private_key/file --gas-price 10 --gas-limit 6000000

Deploying a token for testing purposes (please DO NOT use this for production purposes) with the ``token`` command::

    python -m raiden_contracts.deploy token --rpc-provider http://127.0.0.1:8545 --private-key /path/to/your/private_key/file --gas-price 10 --token-supply 10000000 --token-name TestToken --token-decimals 18 --token-symbol TTT

Registering a token with the ``TokenNetworkRegistry`` contract, so it can be used by the Raiden Network, with the ``register`` command::

    python -m raiden_contracts.deploy register --rpc-provider http://127.0.0.1:8545 --private-key /path/to/your/private_key/file --gas-price 10 --token-address TOKEN_TO_BE_REGISTERED_ADDRESS --registry-address TOKEN_NETWORK_REGISTRY_ADDRESS
