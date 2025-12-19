# Banking System (Python)

A domain-driven banking system implemented in Python, focusing on
correct money modeling, currency safety, and clean separation of
responsibilities.

## Features
- Money as a value object (minor units, immutable behavior)
- Currency-safe operations using Enum
- Savings and Current accounts with policy-based constraints
- Bank as an orchestrator for accounts and transfers
- External currency conversion via CurrencyConverter

## Design Principles
- No floating-point money
- No currency mixing
- No hidden global state
- Explicit error handling

## Status
- Money
- Accounts
- Bank
- Transfers
- Transaction history (planned)


