# Hermes Agent Transfer Guide

To migrate Hermes configuration and learned state to another machine:

## 1. Copy the Config File
```bash
scp ~/.hermes/config.yaml user@new-host:~/.hermes/
```

## 2. Copy Profile Data
Each profile has its own `skills/`, `plugins/`, `cron/`, and `memories/`:
```bash
scp -r ~/.hermes/profiles/default/* user@new-host:~/.hermes/profiles/default/
```
Repeat for any other profiles you use.

## 3. Verify on New Host
```bash
hermes doctor   # checks config and skill integrity
hermes skills list
```
If anything is missing, re‑install with:
```bash
hermes skill install <name>
```
or restore from backup.

This transfers all persisted settings, skills, cron jobs, and memories. The agent will behave the same as on the original machine (assuming the same Python environment and any external tools/API keys are also provisioned).