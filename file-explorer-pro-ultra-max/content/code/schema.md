# Schema for TimeScaleDB to Handle Financial Data

```sql
-- server/schema.sql

-- 1. Company Table (Core entity)
CREATE TABLE company (
    company_id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    industry VARCHAR(100),
    description TEXT,
    website VARCHAR(255),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Income Statement (Quarterly/Annual)
CREATE TABLE income_statement (
    company_id INT REFERENCES company(company_id),
    period_end DATE NOT NULL,
    frequency VARCHAR(10) NOT NULL CHECK (frequency IN ('Q', 'A')),
    total_revenue NUMERIC,
    cost_of_revenue NUMERIC,
    gross_profit NUMERIC,
    operating_expenses NUMERIC,
    operating_income NUMERIC,
    interest_income NUMERIC,
    interest_expense NUMERIC,
    other_income_expense NUMERIC,
    pretax_income NUMERIC,
    income_tax NUMERIC,
    net_income NUMERIC,
    eps_basic NUMERIC,
    eps_diluted NUMERIC,
    PRIMARY KEY (company_id, period_end, frequency)
);

-- 3. Balance Sheet (Quarterly/Annual)
CREATE TABLE balance_sheet (
    company_id INT REFERENCES company(company_id),
    period_end DATE NOT NULL,
    frequency VARCHAR(10) NOT NULL CHECK (frequency IN ('Q', 'A')),
    total_assets NUMERIC,
    total_current_assets NUMERIC,
    cash_and_equivalents NUMERIC,
    short_term_investments NUMERIC,
    accounts_receivable NUMERIC,
    inventory NUMERIC,
    total_liabilities NUMERIC,
    total_current_liabilities NUMERIC,
    accounts_payable NUMERIC,
    long_term_debt NUMERIC,
    total_equity NUMERIC,
    retained_earnings NUMERIC,
    PRIMARY KEY (company_id, period_end, frequency)
);

-- 4. Cash Flow Statement (Quarterly/Annual)
CREATE TABLE cash_flow (
    company_id INT REFERENCES company(company_id),
    period_end DATE NOT NULL,
    frequency VARCHAR(10) NOT NULL CHECK (frequency IN ('Q', 'A')),
    operating_cash_flow NUMERIC,
    investing_cash_flow NUMERIC,
    financing_cash_flow NUMERIC,
    free_cash_flow NUMERIC,
    capital_expenditures NUMERIC,
    dividends_paid NUMERIC,
    PRIMARY KEY (company_id, period_end, frequency)
);

-- 5. Historical Stock Prices (Time-series)
CREATE TABLE stock_price (
    company_id INT REFERENCES company(company_id),
    time TIMESTAMP NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    adjusted_close NUMERIC,
    PRIMARY KEY (company_id, time)
);

-- 6. Dividends History
CREATE TABLE dividend (
    company_id INT REFERENCES company(company_id),
    ex_date DATE NOT NULL,
    payment_date DATE,
    amount NUMERIC,
    PRIMARY KEY (company_id, ex_date)
);

-- 7. Stock Splits
CREATE TABLE stock_split (
    company_id INT REFERENCES company(company_id),
    date DATE NOT NULL,
    ratio NUMERIC NOT NULL,
    PRIMARY KEY (company_id, date)
);

-- Convert time-series tables to hypertables
SELECT create_hypertable('income_statement', 'period_end');
SELECT create_hypertable('balance_sheet', 'period_end');
SELECT create_hypertable('cash_flow', 'period_end');
SELECT create_hypertable('stock_price', 'time');
```