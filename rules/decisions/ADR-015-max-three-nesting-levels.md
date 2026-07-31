# ADR-015 · Max three nesting levels

date: 2026-07-27
status: accepted
decided-by: brian
supersedes: —
superseded-by: —

## Context

Taken during the v2 design session (2026-07-27). Full reasoning lives in
`docs/Arquitectura_Mente_OS_v2_Bloques.md`; this record exists so the decision has its own
traceable, revertible file (see `rules/contract-adr.md`).

## Decision

Maximum three nesting levels: BLOCK > GROUP > SUB-BLOCK.

## Rationale

Consistency with the rule Brian set for owners: *"nunca más de 3, porque si no el sistema no entiende."* Rejected alternatives: 2 fixed (large work ends up with 20 flat sub-blocks) and free nesting (deep trees are the disorder we are fixing).

## Evidence

A mature external reference started with two levels and added arbitrary depth in its stable release — the need is real; the risk is the laberinto.

## Reverting

Allow free depth; expect trees nobody can navigate.
