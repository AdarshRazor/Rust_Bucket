# **Project Requirements Document (PRD): Finance-Plan**

## 1. Introduction & Vision
Finance-Plan is a comprehensive financial analysis platform designed to empower investors, analysts, and business students. It aims to demystify corporate finance by providing tools to analyze historical performance, assess real-time market value, and forecast future potential based on strategic plans. By integrating historical data, real-time market signals, and predictive analytics, Finance-Plan will serve as a co-pilot for financial decision-making.

## 2. Target Audience
*   **Retail Investors:** Individuals looking for deeper insights beyond basic stock tickers to make informed investment decisions.
*   **Financial Analysts:** Professionals who need to quickly gather and analyze data for reports, valuations, and competitor analysis.
*   **Business/Finance Students:** Students who can use the tool for academic projects, learning about company valuation and strategic financial planning.

## 3. Core Features & Functionality

The project is broken down into three main phases, with each phase building upon the last.

### **Feature Set 1: Foundation & Historical Analysis (Phase 1)**

*   **F1.1: Company Data Ingestion:**
    *   Users can input a publicly traded company's ticker symbol (e.g., AAPL, GOOGL).
    *   The system fetches 5-10 years of historical financial data from sources like `yfinance` and SEC EDGAR filings. This includes income statements, balance sheets, and cash flow statements.

*   **F1.2: Company Profile Dashboard:**
    *   A dedicated page for the selected company displays a comprehensive profile.
    *   **Business Summary:** A clear, concise overview of what the company does, its primary products/services, and its business model. (This can be sourced from APIs like Finnhub or scraped).
    *   **Financial Performance Visualization:** Interactive charts (using `react-financial-charts`) displaying key metrics over time:
        *   Revenue, Net Income, and Gross Profit.
        *   Earnings Per Share (EPS).
        *   Key growth rates (Revenue Growth, Earnings Growth).
    *   **Investment History Analysis:** A section detailing historical investment performance, including dividend history, stock splits, and major capital expenditures.
    *   **Automated Health Summary:** A generated text summary that interprets the financial data, highlighting strengths (e.g., "consistent revenue growth over 5 years") and weaknesses (e.g., "declining profit margins since 2021").

### **Feature Set 2: Real-Time Analysis & Competitive Intelligence (Phase 2)**

*   **F2.1: Real-Time Market Integration:**
    *   The platform will fetch and display real-time (or near real-time) stock prices and market data using APIs from Alpha Vantage or Finnhub.
    *   Real-time data will be visualized using TradingView Lightweight Charts.

*   **F2.2: Predictive Valuation Engine (⭐ Core Focus):**
    *   The system uses historical financial and market data to train a predictive model (e.g., ARIMA, Prophet, or a simple ML model).
    *   This model predicts the company's "intrinsic" or "expected" current value.
    *   The dashboard will clearly display:
        1.  **Actual Market Value:** The current stock price.
        2.  **Predicted Value:** The value forecast by the model.
        3.  **Prediction Error (%):** The percentage difference between actual and predicted values. This metric serves as an indicator of over/undervaluation according to the model.

*   **F2.3: Market Ranking & Competitor Analysis:**
    *   The system will identify key competitors within the same industry/sector.
    *   It will display a comparative table or chart ranking the company and its competitors based on:
        *   Market Capitalization.
        *   Key financial ratios (P/E, P/S).
        *   Our proprietary "Prediction Error" metric.

*   **F2.4: Strategic Retrospective Insights:**
    *   Using the historical data and prediction model, the system will generate insights on past performance.
    *   Example insight: "The company's value deviated negatively from predictions in Q3 2022, coinciding with a 20% increase in R&D spending that did not immediately translate to revenue growth. A more staggered investment approach could have maintained shareholder confidence." This may involve using FinBERT to analyze news sentiment from that period.

### **Feature Set 3: Future Planning & Strategic Forecasting (Phase 3)**

*   **F3.1: Future Plan Input:**
    *   A user interface (e.g., a form or structured text input) where a user can input a company's stated future plans.
    *   Examples: "Launching a new product line in Asia," "Acquiring a smaller competitor," "Investing $5B in AI research over 3 years."

*   **F3.2: Future Value Projection:**
    *   The predictive model will be enhanced to incorporate these qualitative future plans as quantitative inputs (e.g., estimating potential revenue streams or costs from the plan).
    *   It will combine past performance (Phase 1), current market conditions (Phase 2), and future plans to project the company's value 1, 3, and 5 years into the future.

*   **F3.3: Strategic Recommendation Report:**
    *   The system will generate a downloadable/viewable report that includes:
        *   The future value projection with best-case, worst-case, and most-likely scenarios.
        *   Strategic recommendations based on the analysis. Example: "Given the market's positive sentiment towards AI, accelerating the $5B investment could lead to a 15% higher valuation in 3 years, but carries a risk of short-term cash flow strain. We recommend securing a line of credit before proceeding."
        *   A summary of supporting data and assumptions.

## 4. Technical Stack Summary
*   **Frontend:** React, Next.js, react-financial-charts, TradingView Charts, Shadcn UI, Tailwind, Zustand
*   **Backend:** Python, FastAPI, Pandas, NumPy
*   **Data Sources & Tools:** yfinance, TA-Lib, Finnhub, EDGAR, Quandl
*   **Database & Caching:** TimeScaleDB, Redis
*   **ML/AI:** Scikit-learn, TensorFlow/PyTorch, Prophet, FinBERT, Quantlib

## 5. Success Metrics
*   **Prediction Accuracy:** The average prediction error of the valuation model is below a target threshold (e.g., 15%).
*   **User Engagement:** Number of reports generated, time spent on analysis pages.
*   **User Retention:** Percentage of users returning to the platform monthly.

---

Here is the **TODO File** to guide the development of the entire project.

---

# **TODO: Finance-Plan Project**

### Phase 0: Project Setup & Core Infrastructure

| ID | Task | Status | Priority | Dependency | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T0.1 | Initialize Git repository and define branching strategy (main, dev). | ✅ Completed | High | - | main, dev(development) |
| T0.2 | Setup Frontend: `create-next-app` with TypeScript, Tailwind, Shadcn. | ✅ Completed | High | T0.1 | `client` folder |
| T0.3 | Setup Backend: FastAPI project structure with virtual environment. | ✅ Completed | High | T0.1 | `server` folder |
| T0.4 | Setup Databases: Docker Compose for TimeScaleDB and Redis instances. | ✅ Completed | High | T0.1 | `server/docker-compose.yml` |
| T0.5 | Define initial database schema for historical financial data in docker:timescaledb. | ✅ Completed | High | T0.4 | `server/db/init_timescaledb2.sql` |
| T0.6 | Establish CI/CD pipeline for automated testing and deployment (e.g., GitHub Actions). | ✅ Completed | Medium | T0.2, T0.3 | `github/workflows/ci-cd.yml` |

### Phase 1: Foundation & Prototype

| ID | Task | Status | Priority | Dependency | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1.1 | **Backend:** Create a data ingestion script using `yfinance` to fetch historical data. | ✅ Completed | High | T0.3 | `server/app/data/yFinance.py` |
| T1.2 | **Backend:** Store fetched historical data into docker:timescaledb | ✅ Completed | High | T0.5, T1.1 | `server/app/data/result2timescale.py` |
| T1.3 | **Backend:** Develop FastAPI endpoint `GET /api/company/{ticker}/profile` for company info. | Not Started | High | T0.3 |
| T1.4 | **Backend:** Develop FastAPI endpoint `GET /api/company/{ticker}/financials` for historical data. | ✅ Completed | High | T1.2 | `localhost:8000/yfinance/fetch?` |
| T1.5 | **Frontend:** Build the main layout, header, and a company search bar component. | Not Started | High | T0.2 |
| T1.6 | **Frontend:** Create the Company Profile Dashboard page structure. | Not Started | High | T1.5 |
| T1.7 | **Frontend:** Integrate `react-financial-charts` to visualize revenue, profit, etc. | Not Started | High | T1.6 |
| T1.8 | **Frontend:** Connect dashboard to backend API (`/financials`) to display data. | Not Started | High | T1.4, T1.7 |
| T1.9 | **Backend:** Implement basic caching with Redis for the API endpoints. | Not Started | Medium | T1.4 |
| T1.10 | **Backend:** Implement a basic text generation function for the "Health Summary". | Not Started | Medium | T1.4 |
| T1.11 | **Integration:** Deploy a live v1 prototype. | Not Started | High | T1.8, T1.10 |

### Phase 2: Real-Time Analysis & Prediction

| ID | Task | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| T2.1 | **Data:** Integrate Finnhub or Alpha Vantage API for real-time stock quotes. | Not Started | High | T1.11 |
| T2.2 | **Backend:** Create endpoint `GET /api/company/{ticker}/realtime` for live market data. | Not Started | High | T2.1 |
| T2.3 | **Frontend:** Integrate TradingView Lightweight Charts to display real-time price. | Not Started | High | T1.8 |
| T2.4 | **Frontend:** Connect the TradingView chart to the new real-time endpoint. | Not Started | High | T2.2, T2.3 |
| T2.5 | **ML:** Research and select initial time-series model (ARIMA, Prophet). | Not Started | High | T1.2 |
| T2.6 | **ML:** Develop a script to train the selected model on historical data from DB. | Not Started | High | T2.5 |
| T2.7 | **ML:** Develop a prediction function to estimate current value. | Not Started | High | T2.6 |
| T2.8 | **Backend:** Create endpoint `POST /api/company/{ticker}/predict` to run the model and return predicted value. | Not Started | High | T2.7 |
| T2.9 | **Frontend:** Display "Predicted Value" and "Prediction Error" on the dashboard. | Not Started | High | T2.8, T2.4 |
| T2.10 | **Backend:** Develop logic to identify competitors (e.g., via Finnhub API). | Not Started | Medium | T1.3 |
| T2.11 | **Backend:** Create endpoint `GET /api/company/{ticker}/competitors` with comparative data. | Not Started | Medium | T2.10, T2.8 |
| T2.12 | **Frontend:** Build UI component to display competitor ranking table. | Not Started | Medium | T2.11 |
| T2.13 | **ML:** Develop the "Strategic Retrospective Insights" generation engine (rule-based or NLP). | Not Started | Medium | T2.7 |
| T2.14 | **Integration:** Deploy a live v2 with prediction and competitor features. | Not Started | High | T2.9, T2.12 |

### Phase 3: Future Planning & Strategy

| ID | Task | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| T3.1 | **Frontend:** Design and build the "Future Plans" input form on the dashboard. | Not Started | High | T2.14 |
| T3.2 | **Backend:** Create endpoint `POST /api/company/{ticker}/future-scenario` to receive user input. | Not Started | High | T3.1 |
| T3.3 | **ML:** Enhance the prediction model to incorporate qualitative inputs from the future plans. | Not Started | High | T2.7, T3.2 |
| T3.4 | **ML:** Develop logic to project future value for 1, 3, 5-year horizons with scenarios. | Not Started | High | T3.3 |
| T3.5 | **Backend:** Create endpoint `GET /api/company/{ticker}/future-projection` that runs the enhanced model. | Not Started | High | T3.4 |
| T3.6 | **Backend:** Develop a report generation module (e.g., creating a structured JSON or PDF). | Not Started | Medium | T3.5 |
| T3.7 | **Frontend:** Create a dedicated view/component to display the final Strategic Report. | Not Started | High | T3.6 |
| T3.8 | **Frontend:** Add a "Download Report" button. | Not Started | Medium | T3.7 |
| T3.9 | **Integration:** Deploy the final v3 of the project. | Not Started | High | T3.7 |

---

### Things to Keep in Mind : !IMPORTANT!

While providing the SubTask or any help, please keep in mind the following:

* Not make assumptions about compatibility or safety, always research and provide the latest code, modules, libraries or anything that is needed for the task. (do not look for outdated or deprecated code, !IMPORTANT!)
* Research the actual latest versions before suggesting any dependencies
* Only provide the specific code needed for the current task, instead of providing the whole code and install all the dependencies.
* Explain the logic behind any code I suggest, so I can understand the code and the logic behind it.
* Keep the code clean and readable.
* Check the dependencies and the codebase before providing the SubTask or any help, so it wont break the code.
* Follow your explicit instructions in the PRD, so I can understand the task and the instructions.