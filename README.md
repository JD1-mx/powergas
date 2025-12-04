# PowerGas Profitability Calculator

## Overview

This tool helps PowerGas track and analyze the profitability of gas delivery operations from Mother Stations (dispatching plants) to Daughter Stations (customer locations). It implements the profitability formula and provides what-if scenario analysis capabilities.

## Table of Contents

- [Components](#components)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Streamlit Web App](#streamlit-web-app)
- [Usage Guide](#usage-guide)
- [Verification Examples](#verification-examples)
- [What-If Scenario Analysis](#what-if-scenario-analysis)
- [Understanding the Formula](#understanding-the-formula)
- [File Descriptions](#file-descriptions)

---

## Components

The system consists of the following files:

1. **profitability_calculator.py** - Main Python script with calculation engine
2. **app.py** - Streamlit web application for interactive interface
3. **config.json** - Configuration file for single trip calculations
4. **scenarios.json** - Multiple scenarios for what-if comparisons
5. **requirements.txt** - Python dependencies for the web app
6. **README.md** - This documentation file

---

## Installation

### Prerequisites

- Python 3.7 or higher
- For command-line calculator: No external dependencies required (uses only Python standard library)
- For web app: Install dependencies from requirements.txt

### Setup

1. Ensure all files are in the same directory:
   ```
   powergas/
   ├── profitability_calculator.py
   ├── app.py
   ├── config.json
   ├── scenarios.json
   ├── requirements.txt
   └── README.md
   ```

2. Verify Python installation:
   ```bash
   python --version
   ```
   or
   ```bash
   python3 --version
   ```

3. Install dependencies (for web app):
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip3 install -r requirements.txt
   ```

---

## Quick Start

### Run the Calculator

```bash
python profitability_calculator.py
```

or

```bash
python3 profitability_calculator.py
```

This will:
1. Calculate profitability for the trip defined in `config.json`
2. Compare all scenarios in `scenarios.json`
3. Generate a detailed comparison report
4. Save the report to `profitability_report.txt`

---

## Streamlit Web App

### Launch the Interactive Web Interface

For a better user experience with interactive forms, visualizations, and comparisons:

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

### Features

The Streamlit app provides three main modules:

#### 1. Single Trip Calculator
- Interactive form for all input parameters
- Real-time profitability calculation
- Visual cost breakdown with pie charts
- Key metrics display (Revenue, Costs, Profit, Margin)
- Load values from config.json with one click

#### 2. Scenario Comparison
- Compare multiple scenarios side-by-side
- Interactive charts and visualizations
  - Profit comparison bar charts
  - Profit margin comparison
  - Revenue vs Costs grouped bar charts
- Scenario rankings with medals
- Cost component impact analysis
- Detailed comparison table
- Export results as CSV or JSON

#### 3. About
- Formula reference
- Component explanations
- Feature overview
- Development roadmap

### Using the Web App

1. **Single Trip Mode**:
   - Click "Single Trip Calculator" in the sidebar
   - Fill in the form or load from config.json
   - Click "Calculate Profitability"
   - View results and charts

2. **Scenario Comparison Mode**:
   - Click "Scenario Comparison" in the sidebar
   - Load scenarios from scenarios.json
   - View automatic comparison with charts
   - Analyze cost impacts
   - Export results

3. **Quick Actions** (Sidebar):
   - "Load from config.json" - Import single trip data
   - "Load scenarios.json" - Import comparison scenarios

### Screenshots

The app includes:
- 📊 Interactive Plotly charts
- 🎨 Clean, professional UI
- 📱 Responsive design
- 💾 Export capabilities (CSV/JSON)
- 🔄 Real-time calculations

---

## Usage Guide

### Phase 1: Single Trip Calculation

To calculate profitability for a single trip:

1. **Edit `config.json`** with your trip parameters:
   - Revenue components (gas_volume, gas_price)
   - Production costs (gas_cost, plant_cost, ga_cost)
   - Truck expenses (depreciation, insurance, fuel, turnaround time)
   - Trucking costs (fixed, variable, distance)
   - Skid costs (depreciation, turnaround time)

2. **Run the calculator**:
   ```bash
   python profitability_calculator.py
   ```

3. **Review the output** showing:
   - Revenue
   - Cost breakdown by category
   - Total profit
   - Profit margin percentage

### Phase 2: Testing with Different Input Values

To test different scenarios:

1. **Modify values in `config.json`**
   - Change any parameter (e.g., gas_price, round_trip_distance)
   - Save the file

2. **Re-run the calculator** to see updated results

3. **Example testing workflow**:
   ```bash
   # Test 1: Original values
   python profitability_calculator.py

   # Edit config.json (change gas_price from 850 to 900)

   # Test 2: Higher gas price
   python profitability_calculator.py

   # Edit config.json (change round_trip_distance from 240 to 200)

   # Test 3: Shorter distance
   python profitability_calculator.py
   ```

### Phase 3: What-If Scenario Comparison

To compare multiple scenarios:

1. **Review `scenarios.json`** which contains:
   - Scenario A: Delivery from Ebedei
   - Scenario B: Delivery from Ore
   - Scenario C: Delivery from Ikorodu
   - Scenario D: Delivery from Ogbele

2. **Add or modify scenarios** by editing `scenarios.json`:
   ```json
   {
     "name": "Scenario E: Custom",
     "description": "Your custom scenario description",
     "trip_data": {
       "trip_id": "SCENARIO-E",
       "mother_station": "YourStation",
       "daughter_station": "Customer Location A",
       ... (all required parameters)
     }
   }
   ```

3. **Run the comparison**:
   ```bash
   python profitability_calculator.py
   ```

4. **Review the comparison report** in `profitability_report.txt`

---

## Verification Examples

### Manual Calculation Verification

Let's verify the calculator with a simple example:

#### Example Input (from config.json):
```
Gas Volume (GV) = 5,000 scm
Gas Price (GP) = 850 NGN/scm

Gas Cost (GC) = 450 NGN/scm
Plant Cost (PC) = 120 NGN/scm
G&A Cost (G&A) = 80 NGN/scm

Truck Depreciation (TD) = 2,500 NGN/hr
Truck Insurance (TIS) = 1,200 NGN/hr
Fuel Cost (FC) = 3,500 NGN/hr
Truck Turnaround Time (TTAT) = 12 hours

Fixed Trucking Cost (FTC) = 180 NGN/km
Variable Trucking Cost (VTC) = 45 NGN/km
Round Trip Distance (RTD) = 240 km

Skid Depreciation (SD) = 800 NGN/hr
Skid Turnaround Time (STAT) = 14 hours
```

#### Manual Calculation:

**Step 1: Revenue**
```
Revenue = GV × GP
Revenue = 5,000 × 850
Revenue = 4,250,000 NGN
```

**Step 2: Production Costs**
```
Production Costs = (GC + PC + G&A) × GV
Production Costs = (450 + 120 + 80) × 5,000
Production Costs = 650 × 5,000
Production Costs = 3,250,000 NGN
```

**Step 3: Truck Expenses**
```
Truck Expenses = (TD + TIS + FC) × TTAT
Truck Expenses = (2,500 + 1,200 + 3,500) × 12
Truck Expenses = 7,200 × 12
Truck Expenses = 86,400 NGN
```

**Step 4: Trucking Costs**
```
Trucking Costs = (FTC + VTC) × RTD
Trucking Costs = (180 + 45) × 240
Trucking Costs = 225 × 240
Trucking Costs = 54,000 NGN
```

**Step 5: Skid Costs**
```
Skid Costs = SD × STAT
Skid Costs = 800 × 14
Skid Costs = 11,200 NGN
```

**Step 6: Total Costs**
```
Total Costs = Production Costs + Truck Expenses + Trucking Costs + Skid Costs
Total Costs = 3,250,000 + 86,400 + 54,000 + 11,200
Total Costs = 3,401,600 NGN
```

**Step 7: Profit**
```
Profit = Revenue - Total Costs
Profit = 4,250,000 - 3,401,600
Profit = 848,400 NGN
```

**Step 8: Profit Margin**
```
Profit Margin = (Profit / Revenue) × 100
Profit Margin = (848,400 / 4,250,000) × 100
Profit Margin = 19.96%
```

#### Expected Output from Calculator:
```
Revenue: NGN 4,250,000.00
Costs:
  - Production Costs: NGN 3,250,000.00
  - Truck Expenses: NGN 86,400.00
  - Trucking Costs: NGN 54,000.00
  - Skid Costs: NGN 11,200.00
Total Costs: NGN 3,401,600.00
PROFIT: NGN 848,400.00
Profit Margin: 19.96%
```

### Running the Verification

1. Ensure `config.json` has the values shown above
2. Run: `python profitability_calculator.py`
3. Compare the output with the manual calculation
4. Both should match exactly

---

## What-If Scenario Analysis

### Understanding the Scenarios

The provided scenarios compare delivering to the **same customer** from **different Mother Stations**:

| Scenario | Mother Station | Distance (km) | Turnaround (hrs) | Gas Cost (NGN/scm) |
|----------|---------------|---------------|------------------|-------------------|
| A | Ebedei | 240 | 12.0 | 450 |
| B | Ore | 160 | 8.0 | 470 |
| C | Ikorodu | 180 | 9.0 | 460 |
| D | Ogbele | 150 | 7.5 | 455 |

### Key Questions Answered

#### 1. Which Mother Station is most profitable?

Run the calculator and check the ranking in the report:
```bash
python profitability_calculator.py
```

Look for the "SUMMARY (Ranked by Profit)" section.

#### 2. How much profit difference between best and worst?

Check the "COMPARATIVE ANALYSIS" section:
- Profit Difference: Shows absolute NGN difference
- Margin Difference: Shows percentage point difference

#### 3. Which cost component has the biggest impact?

The report includes "Cost Component Impact Analysis":
- Production Costs Difference
- Truck Expenses Difference
- Trucking Costs Difference
- Skid Costs Difference
- **Biggest Cost Impact**: Identifies the dominant factor

#### 4. Time savings from using closer stations?

Compare turnaround times:
```
Ebedei: 12.0 hours (truck) + 14.0 hours (skid)
Ogbele: 7.5 hours (truck) + 8.5 hours (skid)

Savings: 4.5 hours (truck) + 5.5 hours (skid) per trip
```

### Creating Custom Scenarios

To answer custom what-if questions:

**Example: "What if gas price increases by 10%?"**

1. Create a new scenario in `scenarios.json`:
   ```json
   {
     "name": "Scenario E: Price Increase",
     "description": "Same as Scenario A but with 10% gas price increase",
     "trip_data": {
       ... (copy from Scenario A)
       "gas_price": 935,  // 850 × 1.10
       ...
     }
   }
   ```

2. Run comparison to see impact

**Example: "What if we improve turnaround time by 20%?"**

1. Add scenario with reduced turnaround times:
   ```json
   "truck_turnaround_time": 9.6,  // 12 × 0.80
   "skid_turnaround_time": 11.2   // 14 × 0.80
   ```

2. Compare against baseline

---

## Understanding the Formula

### Complete Formula

```
Profit = (GV × GP) - [ ((GC + PC + G&A) × GV) + ((TD + TIS + FC) × TTAT) + ((FTC + VTC) × RTD) + (SD × STAT) ]
```

### Formula Breakdown

#### Revenue Component
- **GV × GP**: Total gas sales revenue

#### Cost Components

1. **Production Costs**: `(GC + PC + G&A) × GV`
   - Variable costs that scale with gas volume
   - Includes: gas acquisition, plant operations, overhead

2. **Truck Expenses**: `(TD + TIS + FC) × TTAT`
   - Time-based truck costs
   - Includes: depreciation, insurance/interest, fuel
   - Shorter trips reduce these costs

3. **Trucking Costs**: `(FTC + VTC) × RTD`
   - Distance-based contractor costs
   - Shorter distances directly reduce costs

4. **Skid Costs**: `SD × STAT`
   - Time-based skid/trailer costs
   - Depreciation over turnaround period

### Cost Impact Analysis

Different Mother Stations affect costs differently:

| Cost Type | Impact of Closer Station | Magnitude |
|-----------|--------------------------|-----------|
| Production Costs | May increase (higher gas cost) | Medium |
| Truck Expenses | Decreases (less time) | High |
| Trucking Costs | Decreases (less distance) | High |
| Skid Costs | Decreases (less time) | Medium |

**Net Impact**: Closer stations typically more profitable despite potential increase in gas cost.

---

## File Descriptions

### profitability_calculator.py

The main calculation engine with:
- `ProfitabilityCalculator` class
- Methods for each formula component
- Scenario comparison functionality
- Report generation

**Key Methods**:
- `calculate_trip_profit()`: Single trip calculation
- `compare_scenarios()`: Multi-scenario analysis
- `generate_comparison_report()`: Detailed report with rankings

### config.json

Single trip configuration file.

**Structure**:
- `trip_data`: All input parameters
- Inline documentation (`_comment_*`, `_note_*`)
- `_instructions`: Usage guide

**When to Use**: Testing single calculations, validating formula

### scenarios.json

Multiple scenario definitions for comparison.

**Structure**:
- `scenarios`: Array of scenario objects
- Each scenario has: name, description, trip_data
- `_instructions`: How to add scenarios
- `_example_what_if_questions`: Common use cases

**When to Use**: Comparing Mother Stations, what-if analysis

### profitability_report.txt

Auto-generated comparison report (created when running the calculator).

**Contents**:
- Summary table (ranked by profit)
- Detailed breakdown per scenario
- Comparative analysis
- Cost component impact analysis

---

## Troubleshooting

### Error: "FileNotFoundError"

**Problem**: Missing config.json or scenarios.json

**Solution**: Ensure all files are in the same directory as profitability_calculator.py

### Error: "KeyError: 'gas_volume'"

**Problem**: Missing required field in JSON

**Solution**: Check that all required fields are present in trip_data:
- gas_volume, gas_price
- gas_cost, plant_cost, ga_cost
- truck_depreciation, truck_insurance, fuel_cost, truck_turnaround_time
- fixed_trucking_cost, variable_trucking_cost, round_trip_distance
- skid_depreciation, skid_turnaround_time

### Unexpected Results

**Check**:
1. Units are correct (scm, NGN, km, hours)
2. No negative values (unless intentional)
3. Reasonable magnitudes (e.g., distance < 1000 km)

### Report Not Generated

**Problem**: Report file not created

**Solution**: Check write permissions in directory

---

## Next Steps (Future Phases)

After completing Phases 1-3:

**Phase 4**: Processing of trip data
- Automated data collection from telematics

**Phase 5**: Using trip data as input
- Replace manual inputs with actual trip data

**Phase 6**: PRMS dispensing input
- Integrate actual dispensed volumes

**Phase 7**: Monthly update interface
- N8n workflow for automated updates
- Exchange rates, pricing, costs

---

## Support

For issues or questions:
1. Verify inputs in config.json and scenarios.json
2. Run manual calculation verification
3. Check that Python version is 3.7+

---

## Version History

- **v1.0** (2025-12-03): Initial release
  - Phase 1: Formula implementation
  - Phase 2: Manual input testing
  - Phase 3: What-if scenario comparison

---

## Formula Reference Card

```
REVENUE
  Revenue = GV × GP

COSTS
  Production = (GC + PC + G&A) × GV
  Truck Exp  = (TD + TIS + FC) × TTAT
  Trucking   = (FTC + VTC) × RTD
  Skid       = SD × STAT

PROFIT
  Profit = Revenue - (Production + Truck Exp + Trucking + Skid)

MARGIN
  Margin % = (Profit / Revenue) × 100
```

---

**PowerGas Profitability Calculator v1.0**
