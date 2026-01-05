# ==========================================================
# LESSON 13: MODULE 6 - SERVICES (Business Logic)
# payment_service.py - Service for verifying blockchain payments
# 
# This file contains the PaymentService class for verifying transactions across various
# blockchain networks (EVM chains via Alchemy and Solana via Helius).
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import httpx for HTTP requests
import httpx
# httpx - asynchronous HTTP library for requests to blockchain RPC nodes

# Line 3: Import logging for logging
import logging

# Line 4: Empty line for readability

# Line 5: Import constants from config.py (lesson 1)
from app.core.config import (
    # ALCHEMY_ETHEREUM_URL - URL of Alchemy RPC node for Ethereum
    ALCHEMY_ETHEREUM_URL,
    # ALCHEMY_POLYGON_URL - URL for Polygon
    ALCHEMY_POLYGON_URL,
    # ALCHEMY_ARBITRUM_URL - URL for Arbitrum
    ALCHEMY_ARBITRUM_URL,
    # ALCHEMY_OPTIMISM_URL - URL for Optimism
    ALCHEMY_OPTIMISM_URL,
    # HELIUS_SOLANA_URL - URL of Helius RPC node for Solana
    HELIUS_SOLANA_URL,
    # PAYMENT_STRICT - strict mode flag for verification (prohibits fallback)
    PAYMENT_STRICT,
)

# Line 6: Import constants from constants.py (lesson 2)
from app.core.constants import SUPPORTED_NETWORKS

# Line 7: logger - creating logger for this module
logger = logging.getLogger(__name__)


# Line 8: Empty line for readability


# Line 9: Definition of PaymentService class
class PaymentService:
    # Line 10: Class docstring
    """
    Verify transaction in blockchain.

    For EVM chains (ethereum / polygon / arbitrum / optimism) we use JSON-RPC (Alchemy).
    For Solana — Helius (compatible with Solana RPC).

    If RPC-URL for network is not configured (no environment variable) —
    the method does NOT break the application, but falls back to "fake" verification and
    simply returns min_amount as "confirmed" amount.
    """
    # JSON-RPC = protocol for exchanging data with blockchain nodes
    # RPC = Remote Procedure Call

    # Line 11: EVM_RPC_URLS - dictionary with RPC node URLs for EVM networks
    EVM_RPC_URLS = {
        # Line 12: "ethereum": ALCHEMY_ETHEREUM_URL - URL for Ethereum
        "ethereum": ALCHEMY_ETHEREUM_URL,
        # Line 13: "polygon": ALCHEMY_POLYGON_URL - URL for Polygon
        "polygon": ALCHEMY_POLYGON_URL,
        # Line 14: "arbitrum": ALCHEMY_ARBITRUM_URL - URL for Arbitrum
        "arbitrum": ALCHEMY_ARBITRUM_URL,
        # Line 15: "optimism": ALCHEMY_OPTIMISM_URL - URL for Optimism
        "optimism": ALCHEMY_OPTIMISM_URL,
    }
    # EVM = Ethereum Virtual Machine (used by many networks)

    # Line 16: Comment about decimal places
    # for native coins (ETH/MATIC etc.) we use 18 decimal places
    # Line 17: EVM_NATIVE_DECIMALS - dictionary with number of decimal places for each network
    EVM_NATIVE_DECIMALS = {
        # Line 18: "ethereum": 18 - ETH has 18 decimal places
        "ethereum": 18,
        # Line 19: "polygon": 18 - MATIC has 18 decimal places
        "polygon": 18,
        # Line 20: "arbitrum": 18 - ETH on Arbitrum has 18 decimal places
        "arbitrum": 18,
        # Line 21: "optimism": 18 - ETH on Optimism has 18 decimal places
        "optimism": 18,
    }
    # Decimals = number of decimal places (e.g., 1 ETH = 1e18 wei)

    # Line 22: @staticmethod decorator
    @staticmethod
    # Line 23: Definition of verify_transaction method
    # verify_transaction - main method for verifying transaction
    # network: str - network name
    # tx_hash: str - transaction hash
    # expected_to_address: str - expected recipient address
    # min_amount_required: float - minimum required amount
    # -> float - returns actual payment amount
    def verify_transaction(
        network: str,
        tx_hash: str,
        expected_to_address: str,
        min_amount_required: float,
    ) -> float:
        # Line 24: Method docstring
        """
        Main method for verifying transaction.

        Returns actual amount (in network's native token), confirmed on blockchain.
        If RPC is not configured — returns min_amount_required (fallback for dev).
        """
        # native token = main coin of network (ETH, MATIC, SOL etc.)
        
        # Line 25: network - normalize network name
        network = network.lower().strip()
        # lower() - convert to lowercase
        # strip() - remove whitespace

        # Line 26: if network not in SUPPORTED_NETWORKS - check network support
        if network not in SUPPORTED_NETWORKS:
            # Line 27: raise ValueError - error for unsupported network
            raise ValueError(f"Unsupported network '{network}'")

        # Line 28: if not tx_hash or len(tx_hash) < 10 - validate tx_hash
        if not tx_hash or len(tx_hash) < 10:
            # Line 29: raise ValueError - error for invalid hash
            raise ValueError("Invalid transaction hash")

        # Line 30: if not expected_to_address - check recipient address
        if not expected_to_address:
            # Line 31: raise ValueError - error for empty address
            raise ValueError("Expected destination address is empty")

        # Line 32: if network == "solana" - check network type
        if network == "solana":
            # Line 33: return - call verification method for Solana
            return PaymentService._verify_solana_tx(
                tx_hash=tx_hash,
                expected_to_address=expected_to_address,
                min_amount_required=min_amount_required,
            )

        # Line 34: return - call verification method for EVM networks
        return PaymentService._verify_evm_tx(
            network=network,
            tx_hash=tx_hash,
            expected_to_address=expected_to_address,
            min_amount_required=min_amount_required,
        )

    # Line 35: Comment - EVM networks verification section
    # --------------------------------------------------
    # EVM networks via JSON-RPC (Alchemy and similar)
    # --------------------------------------------------

    # Line 36: @staticmethod decorator
    @staticmethod
    # Line 37: Definition of private method _verify_evm_tx
    # _verify_evm_tx - verify transaction in EVM network
    def _verify_evm_tx(
        network: str,
        tx_hash: str,
        expected_to_address: str,
        min_amount_required: float,
    ) -> float:
        # Line 38: rpc_url - get RPC node URL for network
        rpc_url = PaymentService.EVM_RPC_URLS.get(network)

        # Line 39: Comment - fallback when RPC is missing
        # Fallback: no RPC — act as fake checker, but log it
        # Line 40: if not rpc_url - check that RPC URL is configured
        if not rpc_url:
            # Line 41: if PAYMENT_STRICT - check strict mode
            if PAYMENT_STRICT:
                # Line 42: raise ValueError - error in strict mode
                raise ValueError(f"RPC URL for {network} not configured (strict mode)")
            # Line 43: logger.warning - log warning
            logger.warning("Missing RPC URL for %s. Fallback to fake verification.", network)
            # Line 44: return min_amount_required - return minimum amount (fallback)
            return min_amount_required
            # Why: in dev mode can work without RPC (for testing)

        # Line 45: try - start of error handling block
        try:
            # Line 46: with httpx.Client() - create HTTP client
            with httpx.Client(timeout=10.0) as client:
                # Line 47: Comment - get transaction
                # 1. Get transaction
                # Line 48: payload_tx - form JSON-RPC request
                payload_tx = {
                    # Line 49: "jsonrpc": "2.0" - JSON-RPC protocol version
                    "jsonrpc": "2.0",
                    # Line 50: "id": 1 - unique request ID
                    "id": 1,
                    # Line 51: "method": "eth_getTransactionByHash" - method to get transaction
                    "method": "eth_getTransactionByHash",
                    # Line 52: "params": [tx_hash] - request parameters (transaction hash)
                    "params": [tx_hash],
                }
                # Line 53: resp_tx - send POST request to RPC node
                resp_tx = client.post(rpc_url, json=payload_tx)
                # Line 54: resp_tx.raise_for_status() - check response status
                resp_tx.raise_for_status()
                # raise_for_status() - raises exception if status is not 200
                # Line 55: data_tx - get JSON from response
                data_tx = resp_tx.json()

                # Line 56: tx - get transaction data from response
                tx = data_tx.get("result")
                # Line 57: if not tx - check that transaction is found
                if not tx:
                    # Line 58: raise ValueError - error if transaction not found
                    raise ValueError("Transaction not found on chain")

                # Line 59: to_addr - get recipient address
                to_addr = tx.get("to")
                # Line 60: if not to_addr - check that address exists
                if not to_addr:
                    # Line 61: raise ValueError - error if address is empty
                    raise ValueError("Transaction 'to' field is empty")

                # Line 62: Comment - verify destination address
                # compare destination address with project wallet
                # Line 63: if to_addr.lower() != expected_to_address.lower() - compare addresses
                if to_addr.lower() != expected_to_address.lower():
                    # Case-insensitive comparison for EVM addresses
                    # Line 64: raise ValueError - error if addresses don't match
                    raise ValueError("Transaction destination address mismatch")

                # Line 65: value_hex - get transaction amount in hex format
                value_hex = tx.get("value") or "0x0"
                # or "0x0" - default value if value is empty
                # Line 66: value_wei - convert hex to decimal number (wei)
                value_wei = int(value_hex, 16)
                # int(value_hex, 16) - convert from hex (base 16) to decimal number
                # wei = smallest unit of ETH (1 ETH = 1e18 wei)

                # Line 67: decimals - get number of decimal places for network
                decimals = PaymentService.EVM_NATIVE_DECIMALS.get(network, 18)
                # Line 68: amount_native - convert wei to native token
                amount_native = value_wei / (10 ** decimals)
                # 10 ** decimals = 10 to the power of decimals (e.g., 10^18)
                # Dividing by 10^18 converts wei to ETH

                # Line 69: Comment - verify transaction status
                # 2. Check receipt (status)
                # receipt = transaction receipt (contains execution information)
                # Line 70: payload_rcpt - form request to get receipt
                payload_rcpt = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    # Line 71: "method": "eth_getTransactionReceipt" - method to get receipt
                    "method": "eth_getTransactionReceipt",
                    "params": [tx_hash],
                }
                # Line 72: resp_rcpt - send request
                resp_rcpt = client.post(rpc_url, json=payload_rcpt)
                resp_rcpt.raise_for_status()
                data_rcpt = resp_rcpt.json()
                # Line 73: receipt - get receipt from response
                receipt = data_rcpt.get("result")
                # Line 74: if not receipt - check that receipt is found
                if not receipt:
                    # Line 75: raise ValueError - error if receipt not found (transaction pending)
                    raise ValueError("Transaction receipt not found (tx might be pending)")

                # Line 76: status - get transaction status
                status = receipt.get("status")
                # Line 77: if status != "0x1" - check transaction success
                if status != "0x1":
                    # "0x1" = successful transaction in hex format
                    # Line 78: raise ValueError - error if transaction failed
                    raise ValueError("Transaction failed on chain")

                # Line 79: return amount_native - return amount in native token
                return amount_native

        # Line 80: except httpx.HTTPError - catch HTTP request errors
        except httpx.HTTPError as e:
            # Line 81: raise ValueError - convert to understandable error
            raise ValueError(f"RPC request error: {str(e)}")

    # Line 82: Comment - Solana verification section
    # --------------------------------------------------
    # Solana via Helius
    # --------------------------------------------------

    # Line 83: @staticmethod decorator
    @staticmethod
    # Line 84: Definition of private method _verify_solana_tx
    # _verify_solana_tx - verify transaction in Solana
    def _verify_solana_tx(
        tx_hash: str,
        expected_to_address: str,
        min_amount_required: float,
    ) -> float:
        # Line 85: rpc_url - get Helius RPC node URL
        rpc_url = HELIUS_SOLANA_URL
        # Line 86: if not rpc_url - check that URL is configured
        if not rpc_url:
            # Line 87: if PAYMENT_STRICT - check strict mode
            if PAYMENT_STRICT:
                # Line 88: raise ValueError - error in strict mode
                raise ValueError("HELIUS_SOLANA_URL not configured (strict mode)")
            # Line 89: logger.warning - log warning
            logger.warning("Missing HELIUS_SOLANA_URL. Fallback to fake verification.")
            # Line 90: return min_amount_required - return minimum amount (fallback)
            return min_amount_required

        # Line 91: try - start of error handling block
        try:
            # Line 92: payload - form JSON-RPC request for Solana
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                # Line 93: "method": "getTransaction" - method to get Solana transaction
                "method": "getTransaction",
                "params": [
                    tx_hash,
                    {
                        # Line 94: "encoding": "json" - response encoding format
                        "encoding": "json",
                        # Line 95: "commitment": "confirmed" - transaction confirmation level
                        "commitment": "confirmed",
                        # confirmed = transaction confirmed (more reliable than processed)
                    },
                ],
            }

            # Line 96: with httpx.Client() - create HTTP client
            with httpx.Client(timeout=10.0) as client:
                # Line 97: resp - send POST request
                resp = client.post(rpc_url, json=payload)
                resp.raise_for_status()
                # Line 98: data - get JSON from response
                data = resp.json()

            # Line 99: result - get result from response
            result = data.get("result")
            # Line 100: if not result - check that transaction is found
            if not result:
                # Line 101: raise ValueError - error if transaction not found
                raise ValueError("Transaction not found on Solana")

            # Line 102: meta - get transaction metadata
            meta = result.get("meta") or {}
            # Line 103: if meta.get("err") is not None - check transaction errors
            if meta.get("err") is not None:
                # Line 104: raise ValueError - error if transaction failed
                raise ValueError("Solana transaction failed")

            # Line 105: tx - get transaction data
            tx = result.get("transaction") or {}
            # Line 106: message - get transaction message
            message = tx.get("message") or {}
            # Line 107: account_keys - get list of accounts
            account_keys = message.get("accountKeys") or []

            # Line 108: try - start of block for address search
            try:
                # Line 109: idx - find index of expected address in account list
                idx = account_keys.index(expected_to_address)
                # index() - list method to find element index
            # Line 110: except ValueError - catch error if address not found
            except ValueError:
                # Line 111: raise ValueError - error if address not found
                raise ValueError("Destination address mismatch on Solana")

            # Line 112: pre_balances - get balances before transaction
            pre_balances = meta.get("preBalances") or []
            # Line 113: post_balances - get balances after transaction
            post_balances = meta.get("postBalances") or []

            # Line 114: if idx >= len(...) - check that indices are valid
            if idx >= len(pre_balances) or idx >= len(post_balances):
                # Line 115: raise ValueError - error if arrays are too short
                raise ValueError("Balance arrays too short for Solana transaction")

            # Line 116: lamports_diff - calculate balance difference
            lamports_diff = post_balances[idx] - pre_balances[idx]
            # lamports = smallest unit of SOL (1 SOL = 1e9 lamports)
            # Line 117: if lamports_diff <= 0 - check that there was a transfer
            if lamports_diff <= 0:
                # Line 118: raise ValueError - error if no transfer occurred
                raise ValueError("No positive transfer to destination on Solana")

            # Line 119: amount_sol - convert lamports to SOL
            amount_sol = lamports_diff / 1_000_000_000  # 1 SOL = 1e9 lamports
            # 1_000_000_000 = 1e9 (underscore for number readability)
            # Line 120: return amount_sol - return amount in SOL
            return amount_sol

        # Line 121: except httpx.HTTPError - catch HTTP request errors
        except httpx.HTTPError as e:
            # Line 122: raise ValueError - convert to understandable error
            raise ValueError(f"Solana RPC request error: {str(e)}")


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 13:
# ==========================================================
# 
# 1. What is JSON-RPC and how is it used for working with blockchain?
#    What JSON-RPC methods are needed for verifying transactions?
#
# 2. What is an RPC node and why do we need services like Alchemy and Helius?
#    What's the difference between public and private RPC nodes?
#
# 3. What are wei and lamports?
#    Why are such small units needed for native tokens?
#
# 4. What does "decimals" mean in blockchain context?
#    How to convert wei to ETH (divide by 10^18)?
#
# 5. Why check transaction receipt in EVM networks?
#    What's the difference between transaction and receipt?
#
# 6. What does status "0x1" mean in receipt?
#    What other statuses can a transaction have?
#
# 7. Why do we need fallback to fake verification when RPC URL is missing?
#    In what cases is this useful, and in what cases is it dangerous?
#
# 8. What does PAYMENT_STRICT mean?
#    Why do we need strict payment verification mode?
#
# 9. How does Solana transaction verification work?
#    What are the differences from EVM transaction verification?
#
# 10. What is commitment level in Solana?
#     What's the difference between "processed", "confirmed", and "finalized"?
#
# ==========================================================
