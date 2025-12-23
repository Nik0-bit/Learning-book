# ==========================================================
# LESSON 2: MODULE 1 - CORE
# constants.py - Application Constants
# 
# This file contains all constants (immutable values) used throughout
# the application: roles, statuses, subscription plans.
# ==========================================================


# Line 1: Comment - user roles section
# Roles determine user access rights in the system
# Analogy: like job positions - admin can do everything, regular user is limited

# ----- User Roles -----
# Line 2: USER_ROLE_ADMIN - constant for administrator role
# Constant = variable whose value doesn't change (convention: write in UPPERCASE)
# "admin" - string value of the role
# Why: instead of magic strings "admin" everywhere, we use a constant (fewer errors)
USER_ROLE_ADMIN = "admin"
# Line 3: USER_ROLE_USER - constant for regular user role
# Regular user - basic access level (can only view, register)
USER_ROLE_USER = "user"
# Line 4: USER_ROLE_SUBSCRIBER - constant for subscriber role
# Subscriber - paid user with extended privileges
USER_ROLE_SUBSCRIBER = "subscriber"  # paid user
# Analogy: like access levels in a game - free player, premium player, admin


# Line 5: Comment - user statuses section
# Status shows the current state of the user (active, banned)

# ----- User Statuses -----
# Line 6: USER_STATUS_ACTIVE - constant for active status
# Active = user can use the system
USER_STATUS_ACTIVE = "active"
# Line 7: USER_STATUS_BANNED - constant for banned status
# Banned = user is blocked, cannot use the system
USER_STATUS_BANNED = "banned"
# Analogy: like bank card status - active or blocked


# Line 8: Comment - subscription statuses section
# Subscription status shows the state of payment/subscription

# ----- Subscription Statuses -----
# Line 9: SUBSCRIPTION_STATUS_ACTIVE - constant for active subscription
# Active = subscription is paid and working
SUBSCRIPTION_STATUS_ACTIVE = "active"
# Line 10: SUBSCRIPTION_STATUS_PENDING - constant for pending subscription
# Pending = in process (waiting for payment confirmation)
SUBSCRIPTION_STATUS_PENDING = "pending"
# Line 11: SUBSCRIPTION_STATUS_FAILED - constant for failed subscription
# Failed = didn't succeed (payment didn't go through)
SUBSCRIPTION_STATUS_FAILED = "failed"
# Analogy: like order status in online store - ordered, in delivery, cancelled


# Line 12: Comment - subscription plans section
# Plans = different subscription options with different prices and durations

# ----- Subscription Plans -----
# Line 13: Comment about prices
# Prices are in USD equivalent (USDT/USDC - stable cryptocurrencies pegged to dollar)
# USD = US dollars, equivalent = equal value
# Prices in USD equivalent (USDT/USDC etc.)
# Line 14: SUBSCRIPTION_PLANS - dictionary with subscription plans
# Dictionary (dict) = key-value data structure (like dictionary: word → definition)
# "month" - key (plan name), value - dictionary with plan parameters
SUBSCRIPTION_PLANS = {
    # Line 15: "month" - key for monthly plan
    # Value - dictionary with parameters: title (name), days (duration), price_usd (price)
    "month": {
        # Line 16: "title" - key, "1 month" - value (plan name for user)
        "title": "1 month",
        # Line 17: "days" - subscription duration in days
        # int - integer, 30 = 30 days
        "days": 30,
        # Line 18: "price_usd" - price in US dollars
        # float - floating point number (15.0 instead of 15, to make it clear it's a price)
        "price_usd": 15.0,
    },
    # Line 19: "quarter" - key for quarterly plan (3 months)
    "quarter": {
        # Line 20: "title" - plan name
        "title": "3 months",
        # Line 21: "days" - 90 days (3 months × 30 days)
        "days": 90,
        # Line 22: "price_usd" - price for 3 months
        "price_usd": 35.0,
    },
    # Line 23: "year" - key for yearly plan
    "year": {
        # Line 24: "title" - plan name
        "title": "12 months",
        # Line 25: "days" - 365 days (year)
        "days": 365,
        # Line 26: "price_usd" - price for year
        "price_usd": 120.0,
    },
}
# Analogy: like restaurant menu - different dishes (plans) with different prices
# Why dictionary: convenient to get plan by key: SUBSCRIPTION_PLANS["month"]


# Line 27: Comment - supported blockchain networks section
# Blockchain networks = cryptocurrency networks through which payments can be made

# ----- Supported Networks -----
# Line 28: SUPPORTED_NETWORKS - list of supported blockchain networks
# List (list) = ordered collection of elements in square brackets []
# Each element - network name (string)
SUPPORTED_NETWORKS = ["ethereum", "polygon", "arbitrum", "optimism", "solana"]
# "ethereum" - main Ethereum network (expensive but reliable transactions)
# "polygon" - Polygon network (cheap transactions, works on top of Ethereum)
# "arbitrum" - Arbitrum network (Layer 2 for Ethereum, fast and cheap)
# "optimism" - Optimism network (another Layer 2 for Ethereum)
# "solana" - Solana network (separate fast blockchain network)
# Analogy: like payment methods - can pay through different payment systems


# Line 29: Comment - project wallets section
# Wallets = addresses in blockchain where users send payments

# ----- Project Wallets by Network -----
# Line 30: Comment - reminder to replace with real addresses
# TODO = task that needs to be done (To Do = make)
# TODO: replace with real project addresses
# Line 31: NETWORK_WALLETS - dictionary of project wallets by network
# Key - network name, value - wallet address (string)
NETWORK_WALLETS = {
    # Line 32: "ethereum" - key for Ethereum network
    # "0x8A32985652a72B26FfA9bdb852Ed59b9977017F9" - wallet address in Ethereum
    # 0x - prefix indicating this is a hex number (hexadecimal)
    "ethereum": "0x8A32985652a72B26FfA9bdb852Ed59b9977017F9",
    # Line 33: "polygon" - key for Polygon network
    # Same address (can be same for EVM-compatible networks)
    "polygon": "0x8A32985652a72B26FfA9bdb852Ed59b9977017F9",
    # Line 34: "arbitrum" - key for Arbitrum network
    "arbitrum": "0x8A32985652a72B26FfA9bdb852Ed59b9977017F9",
    # Line 35: "optimism" - key for Optimism network
    "optimism": "0x8A32985652a72B26FfA9bdb852Ed59b9977017F9",
    # Line 36: "solana" - key for Solana network
    # "8nX9c66wJxh6cCoSiERU5UQQCEcypXM8v5XowFe3fFv8" - wallet address in Solana
    # Different format because Solana uses a different address system
    "solana": "8nX9c66wJxh6cCoSiERU5UQQCEcypXM8v5XowFe3fFv8",
}
# Analogy: like payment details - different bank accounts for different currencies
# Why dictionary: convenient to get address by network: NETWORK_WALLETS["ethereum"]


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 2:
# ==========================================================
# 
# 1. What is a constant and why are they written in UPPERCASE letters?
#    Why use constants instead of directly writing strings "admin" in code?
#
# 2. What's the difference between user role (role) and status?
#    Can a user have role "admin" and status "banned" at the same time?
#
# 3. What do subscription statuses mean: active, pending, failed?
#    In what sequence do they usually change when paying for subscription?
#
# 4. What is a dictionary (dict) in Python and how does it differ from a list?
#    Why is a dictionary used for SUBSCRIPTION_PLANS instead of a list?
#
# 5. What does float (15.0) and int (30) mean in the context of plans?
#    Why is float used for price, but int for days?
#
# 6. What are blockchain networks and how do they differ from each other?
#    Why does Solana use a different address format than Ethereum?
#
# 7. What are Layer 2 networks (Arbitrum, Optimism) and why are they needed?
#    How are they better than the main Ethereum network?
#
# 8. What does 0x at the start of Ethereum wallet address mean?
#    Why can addresses in Ethereum and Polygon be the same?
#
# 9. Why do we need NETWORK_WALLETS dictionary?
#    What happens if user sends payment to wrong address?
#
# 10. Why is the "quarter" plan price 35.0, not 45.0 (15 × 3)?
#     What is a discount for longer term purchase?
#
# ==========================================================
