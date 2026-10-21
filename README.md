# CRIVE Payroll Lint

Local Python CLI to validate **payroll CSV** files before you paste them into CRIVE Private Payroll on [usecrive.com](https://usecrive.com).

**Language:** Python 3 (stdlib only)  
**Scope:** Local file analysis — no network  
**Credentials:** None  
**GitHub:** [github.com/usecrive](https://github.com/usecrive)

## Expected CSV shape

```text
recipient,amount
0xabc...def,10.5
0x123...789,2.0
```

- Header row optional (`to`, `address`, or `recipient`)
- Separators: comma, semicolon, or tab
- Amount must be a positive decimal

## Usage

```bash
python -m crive_payroll_lint path/to/payroll.csv
python -m crive_payroll_lint path/to/payroll.csv --strict
```

Exit codes: `0` ok, `1` validation errors, `2` usage/file error.

## Safety

- Never uploads your file
- Does not connect to any RPC
- Does not modify the CSV

## License

MIT
