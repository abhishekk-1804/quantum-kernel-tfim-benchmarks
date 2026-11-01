# Forensic Input Availability and Schema Integrity Audit

**Audit Identifier:** `audit_20261023_155335Z`  
**Execution Timestamp:** 2026-10-23T15:53:35Z  
**Status:** ALL ORIGINAL CANDIDATE CSVs PASS INTEGRITY CHECKS  

## 1. Candidate Dataset Inventory & Key Analysis

- **Stage 2:** 980 rows across 20 seeds, 7 budgets, 7 arms. Duplicate keys: 0.
- **Stage 3:** 100 rows across 20 seeds, 5 models. Duplicate keys: 0. Nulls: 0.

## 2. Input Availability Matrix

| Data Entity | Stage 2 Status | Stage 3 Status | Audit Action Feasibility |
| :--- | :--- | :--- | :--- |
| Per-seed Summary Metrics (MAE, R²) | Available in CSV | Available in CSV | DIRECTLY AVAILABLE |
| Selected Hyperparameters (best_params) | Available in CSV | Available in CSV | DIRECTLY AVAILABLE |
| Measurement Settings & Allocations | Available in CSV | N/A (Exact simulation) | DIRECTLY AVAILABLE |
| Per-state Ground Truth Targets | Not in CSV | Not in CSV | REPLAY REQUIRED |
| Per-state Predictions | Not in CSV | Not in CSV | REPLAY REQUIRED |
| Kernel Gram Blocks | Not in CSV | Not in CSV | REPLAY REQUIRED |
| Fitted Model Parameters | Not in CSV | Not in CSV | REPLAY REQUIRED |
| RNG Stream & Seed Protocol | Documented (seed) | Documented (seed) | VERIFIED AVAILABLE |

