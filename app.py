"""
PowerGas Profitability Calculator - Streamlit App

Interactive web interface for calculating and comparing profitability
of gas delivery operations from Mother Stations to Daughter Stations.
"""

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from profitability_calculator import ProfitabilityCalculator
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="PowerGas Profitability Calculator",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def format_currency(value):
    """Format number as Nigerian Naira"""
    return f"₦{value:,.2f}"

def calculate_single_trip(trip_data):
    """Calculate profitability for a single trip"""
    calculator = ProfitabilityCalculator.__new__(ProfitabilityCalculator)
    calculator.config = {}
    result = calculator.calculate_trip_profit(trip_data)
    return result

def create_cost_breakdown_chart(result):
    """Create a pie chart for cost breakdown"""
    costs = result['costs_breakdown']

    fig = go.Figure(data=[go.Pie(
        labels=['Production Costs', 'Truck Expenses', 'Trucking Costs', 'Skid Costs'],
        values=[
            costs['production_costs'],
            costs['truck_expenses'],
            costs['trucking_costs'],
            costs['skid_costs']
        ],
        hole=0.3,
        marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    )])

    fig.update_layout(
        title="Cost Breakdown by Category",
        height=400
    )

    return fig

def create_profit_comparison_chart(scenarios_results):
    """Create a bar chart comparing profits across scenarios"""
    df = pd.DataFrame(scenarios_results)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['scenario_name'],
        y=df['profit'],
        text=df['profit'].apply(lambda x: f"₦{x:,.0f}"),
        textposition='auto',
        marker_color='#45B7D1'
    ))

    fig.update_layout(
        title="Profit Comparison Across Scenarios",
        xaxis_title="Scenario",
        yaxis_title="Profit (NGN)",
        height=400,
        showlegend=False
    )

    return fig

def create_detailed_comparison_chart(scenarios_results):
    """Create a grouped bar chart showing revenue and costs"""
    df = pd.DataFrame(scenarios_results)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Revenue',
        x=df['scenario_name'],
        y=df['revenue'],
        marker_color='#2ECC71'
    ))

    fig.add_trace(go.Bar(
        name='Total Costs',
        x=df['scenario_name'],
        y=df['costs_breakdown'].apply(lambda x: x['total_costs']),
        marker_color='#E74C3C'
    ))

    fig.add_trace(go.Bar(
        name='Profit',
        x=df['scenario_name'],
        y=df['profit'],
        marker_color='#3498DB'
    ))

    fig.update_layout(
        title="Revenue, Costs, and Profit Comparison",
        xaxis_title="Scenario",
        yaxis_title="Amount (NGN)",
        barmode='group',
        height=500
    )

    return fig

def main():
    # Header
    st.title("⛽ PowerGas Profitability Calculator")
    st.markdown("**Track and analyze gas delivery profitability across Mother Stations**")
    st.divider()

    # Sidebar
    with st.sidebar:
        st.header("📊 Navigation")
        page = st.radio(
            "Select Module:",
            ["Single Trip Calculator", "Scenario Comparison", "About"]
        )

        st.divider()
        st.markdown("### 📁 Quick Actions")

        if st.button("📥 Load from config.json"):
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                st.session_state.loaded_config = config['trip_data']
                st.success("Config loaded successfully!")
            except Exception as e:
                st.error(f"Error loading config: {e}")

        if st.button("📥 Load scenarios.json"):
            try:
                with open('scenarios.json', 'r') as f:
                    scenarios = json.load(f)
                st.session_state.scenarios = scenarios['scenarios']
                st.success("Scenarios loaded successfully!")
            except Exception as e:
                st.error(f"Error loading scenarios: {e}")

    # Main content based on selected page
    if page == "Single Trip Calculator":
        show_single_trip_calculator()
    elif page == "Scenario Comparison":
        show_scenario_comparison()
    else:
        show_about()

def show_single_trip_calculator():
    st.header("🚚 Single Trip Profitability Calculator")
    st.markdown("Calculate profit for a single gas delivery trip")

    # Load default values from config if available
    default_values = {}
    if 'loaded_config' in st.session_state:
        default_values = st.session_state.loaded_config

    col1, col2 = st.columns(2)

    with col1:
        # Trip Information Section
        st.markdown("### 📍 Trip Information")
        trip_id = st.text_input("Trip ID", value=default_values.get('trip_id', 'TRIP-001'))
        mother_station = st.text_input("Mother Station (Pickup)", value=default_values.get('mother_station', 'Ebedei'))
        daughter_station = st.text_input("Daughter Station (Delivery)", value=default_values.get('daughter_station', 'Customer Location A'))
        return_mother_station = st.text_input("Return Mother Station", value=default_values.get('return_mother_station', default_values.get('mother_station', 'Ebedei')))

        st.markdown("")
        st.divider()

        # Revenue Components - Highlighted
        st.markdown("### 💰 REVENUE COMPONENTS")
        with st.container(border=True):
            gas_volume = st.number_input("Gas Volume (scm)", min_value=0.0, value=float(default_values.get('gas_volume', 5000)), step=100.0, key="rev_gv")
            gas_price = st.number_input("Gas Price (NGN/scm)", min_value=0.0, value=float(default_values.get('gas_price', 850)), step=10.0, key="rev_gp")

    with col2:
        # Cost Components - Highlighted
        st.markdown("### 💸 COST COMPONENTS")

        with st.container(border=True):
            st.markdown("**Production Costs (per scm)**")
            gas_cost = st.number_input("Gas Cost (NGN/scm)", min_value=0.0, value=float(default_values.get('gas_cost', 450)), step=10.0)
            plant_cost = st.number_input("Plant Cost (NGN/scm)", min_value=0.0, value=float(default_values.get('plant_cost', 120)), step=5.0)
            ga_cost = st.number_input("G&A Cost (NGN/scm)", min_value=0.0, value=float(default_values.get('ga_cost', 80)), step=5.0)

            st.divider()
            st.markdown("**Truck Expenses (per hour)**")
            truck_depreciation = st.number_input("Truck Depreciation (NGN/hr)", min_value=0.0, value=float(default_values.get('truck_depreciation', 2500)), step=100.0)
            truck_insurance = st.number_input("Truck Interest + Insurance (NGN/hr)", min_value=0.0, value=float(default_values.get('truck_insurance', 1200)), step=100.0)
            fuel_cost = st.number_input("Fuel Cost (NGN/hr)", min_value=0.0, value=float(default_values.get('fuel_cost', 3500)), step=100.0)
            truck_turnaround_time = st.number_input("Truck Turnaround Time (hours)", min_value=0.0, value=float(default_values.get('truck_turnaround_time', 12)), step=0.5)

            st.divider()
            st.markdown("**Trucking Costs (per km)**")
            fixed_trucking_cost = st.number_input("Fixed Trucking Cost (NGN/km)", min_value=0.0, value=float(default_values.get('fixed_trucking_cost', 180)), step=10.0)
            variable_trucking_cost = st.number_input("Variable Trucking Cost (NGN/km)", min_value=0.0, value=float(default_values.get('variable_trucking_cost', 45)), step=5.0)
            round_trip_distance = st.number_input("Round Trip Distance (km)", min_value=0.0, value=float(default_values.get('round_trip_distance', 240)), step=10.0)

            st.divider()
            st.markdown("**Skid Costs (per hour)**")
            skid_depreciation = st.number_input("Skid Depreciation (NGN/hr)", min_value=0.0, value=float(default_values.get('skid_depreciation', 800)), step=50.0)
            skid_turnaround_time = st.number_input("Skid Turnaround Time (hours)", min_value=0.0, value=float(default_values.get('skid_turnaround_time', 14)), step=0.5)

    st.divider()

    # Display Live Formula
    st.markdown("### 📐 Profitability Formula (Live Calculation)")

    # Calculate intermediate values
    revenue_calc = gas_volume * gas_price
    production_calc = (gas_cost + plant_cost + ga_cost) * gas_volume
    truck_exp_calc = (truck_depreciation + truck_insurance + fuel_cost) * truck_turnaround_time
    trucking_calc = (fixed_trucking_cost + variable_trucking_cost) * round_trip_distance
    skid_calc = skid_depreciation * skid_turnaround_time
    total_costs_calc = production_calc + truck_exp_calc + trucking_calc + skid_calc
    profit_calc = revenue_calc - total_costs_calc
    profit_margin = (profit_calc/revenue_calc*100) if revenue_calc > 0 else 0

    # Display formula in a clean format
    with st.container(border=True):
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**💰 Revenue**")
            st.code(f"GV × GP = {gas_volume:,.0f} × {gas_price:,.2f}")
            st.success(f"Revenue = ₦{revenue_calc:,.2f}")

        with col_b:
            st.markdown("**💸 Total Costs**")
            st.code(f"""Production = ({gas_cost:,.0f} + {plant_cost:,.0f} + {ga_cost:,.0f}) × {gas_volume:,.0f} = ₦{production_calc:,.0f}
Truck Exp = ({truck_depreciation:,.0f} + {truck_insurance:,.0f} + {fuel_cost:,.0f}) × {truck_turnaround_time:.1f} = ₦{truck_exp_calc:,.0f}
Trucking = ({fixed_trucking_cost:,.0f} + {variable_trucking_cost:,.0f}) × {round_trip_distance:.0f} = ₦{trucking_calc:,.0f}
Skid = {skid_depreciation:,.0f} × {skid_turnaround_time:.1f} = ₦{skid_calc:,.0f}""")
            st.error(f"Total Costs = ₦{total_costs_calc:,.2f}")

        st.divider()

        st.markdown("**📊 Cost Breakdown**")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Production", f"₦{production_calc:,.0f}",
                     f"{(production_calc/gas_volume):,.2f}/scm")
        with col2:
            st.metric("Truck Expenses", f"₦{truck_exp_calc:,.0f}",
                     f"{truck_turnaround_time:.1f} hrs")
        with col3:
            st.metric("Trucking", f"₦{trucking_calc:,.0f}",
                     f"{round_trip_distance:.0f} km")
        with col4:
            st.metric("Skid", f"₦{skid_calc:,.0f}",
                     f"{skid_turnaround_time:.1f} hrs")

        st.divider()

        st.markdown("**💵 Profitability**")
        col_x, col_y = st.columns(2)

        with col_x:
            profit_color = "normal" if profit_calc >= 0 else "inverse"
            st.metric("Profit", f"₦{profit_calc:,.2f}",
                     f"{profit_margin:.2f}% margin",
                     delta_color=profit_color)

        with col_y:
            if profit_calc >= 0:
                st.success(f"✅ Profitable - Making ₦{profit_calc:,.2f}")
            else:
                st.error(f"⚠️ Loss - Losing ₦{abs(profit_calc):,.2f}")

    st.divider()

    if st.button("🔢 Calculate Profitability", type="primary", use_container_width=True):
        # Prepare trip data
        trip_data = {
            'trip_id': trip_id,
            'mother_station': mother_station,
            'daughter_station': daughter_station,
            'return_mother_station': return_mother_station,
            'gas_volume': gas_volume,
            'gas_price': gas_price,
            'gas_cost': gas_cost,
            'plant_cost': plant_cost,
            'ga_cost': ga_cost,
            'truck_depreciation': truck_depreciation,
            'truck_insurance': truck_insurance,
            'fuel_cost': fuel_cost,
            'truck_turnaround_time': truck_turnaround_time,
            'fixed_trucking_cost': fixed_trucking_cost,
            'variable_trucking_cost': variable_trucking_cost,
            'round_trip_distance': round_trip_distance,
            'skid_depreciation': skid_depreciation,
            'skid_turnaround_time': skid_turnaround_time
        }

        # Calculate
        result = calculate_single_trip(trip_data)

        # Display results
        st.success("✅ Calculation Complete!")
        st.divider()

        # Key metrics
        st.subheader("📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Revenue", format_currency(result['revenue']))
        with col2:
            st.metric("Total Costs", format_currency(result['costs_breakdown']['total_costs']))
        with col3:
            st.metric("Profit", format_currency(result['profit']),
                     delta=f"{result['profit_margin_percent']:.2f}%")
        with col4:
            profit_color = "normal" if result['profit'] > 0 else "inverse"
            st.metric("Profit Margin", f"{result['profit_margin_percent']:.2f}%")

        st.divider()

        # Detailed breakdown
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("💰 Cost Breakdown")
            costs = result['costs_breakdown']

            cost_data = {
                'Category': ['Production Costs', 'Truck Expenses', 'Trucking Costs', 'Skid Costs'],
                'Amount (NGN)': [
                    costs['production_costs'],
                    costs['truck_expenses'],
                    costs['trucking_costs'],
                    costs['skid_costs']
                ],
                'Percentage': [
                    f"{costs['production_costs']/costs['total_costs']*100:.1f}%",
                    f"{costs['truck_expenses']/costs['total_costs']*100:.1f}%",
                    f"{costs['trucking_costs']/costs['total_costs']*100:.1f}%",
                    f"{costs['skid_costs']/costs['total_costs']*100:.1f}%"
                ]
            }

            df_costs = pd.DataFrame(cost_data)
            st.dataframe(df_costs, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("📈 Cost Distribution")
            fig = create_cost_breakdown_chart(result)
            st.plotly_chart(fig, use_container_width=True)

def show_scenario_comparison():
    st.header("🔄 Scenario Comparison")
    st.markdown("Compare profitability across multiple Mother Stations delivering to the same customer")

    # Check if scenarios are loaded
    if 'scenarios' not in st.session_state:
        st.info("📥 Click 'Load scenarios.json' in the sidebar to load predefined scenarios")

        # Option to load scenarios
        if st.button("Load Default Scenarios"):
            try:
                with open('scenarios.json', 'r') as f:
                    scenarios_data = json.load(f)
                st.session_state.scenarios = scenarios_data['scenarios']
                st.rerun()
            except Exception as e:
                st.error(f"Error loading scenarios: {e}")
                return
    else:
        scenarios = st.session_state.scenarios

        # Calculate all scenarios
        results = []
        for scenario in scenarios:
            result = calculate_single_trip(scenario['trip_data'])
            result['scenario_name'] = scenario['name']
            result['description'] = scenario.get('description', '')
            results.append(result)

        # Sort by profit
        sorted_results = sorted(results, key=lambda x: x['profit'], reverse=True)

        # Summary cards
        st.subheader("🏆 Scenario Rankings")
        cols = st.columns(len(sorted_results))

        for idx, (col, result) in enumerate(zip(cols, sorted_results)):
            with col:
                rank_emoji = ["🥇", "🥈", "🥉"][idx] if idx < 3 else f"{idx+1}️⃣"
                st.markdown(f"### {rank_emoji} {result['scenario_name'].split(':')[1].strip()}")
                st.metric("Profit", format_currency(result['profit']))
                st.metric("Margin", f"{result['profit_margin_percent']:.2f}%")
                st.caption(f"Route: {result['mother_station']} → {result['daughter_station']}")

        st.divider()

        # Comparison charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Profit Comparison")
            fig_profit = create_profit_comparison_chart(sorted_results)
            st.plotly_chart(fig_profit, use_container_width=True)

        with col2:
            st.subheader("💹 Profit Margin Comparison")
            df = pd.DataFrame(sorted_results)
            fig_margin = go.Figure()
            fig_margin.add_trace(go.Bar(
                x=df['scenario_name'],
                y=df['profit_margin_percent'],
                text=df['profit_margin_percent'].apply(lambda x: f"{x:.2f}%"),
                textposition='auto',
                marker_color='#2ECC71'
            ))
            fig_margin.update_layout(
                title="Profit Margin Comparison",
                xaxis_title="Scenario",
                yaxis_title="Profit Margin (%)",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_margin, use_container_width=True)

        # Detailed comparison
        st.subheader("📈 Detailed Revenue & Cost Comparison")
        fig_detailed = create_detailed_comparison_chart(sorted_results)
        st.plotly_chart(fig_detailed, use_container_width=True)

        st.divider()

        # Comparative analysis
        st.subheader("🔍 Comparative Analysis")

        best = sorted_results[0]
        worst = sorted_results[-1]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🥇 Best Scenario")
            st.success(f"**{best['scenario_name']}**")
            st.write(f"Profit: {format_currency(best['profit'])}")
            st.write(f"Margin: {best['profit_margin_percent']:.2f}%")

        with col2:
            st.markdown("#### 📊 Difference")
            profit_diff = best['profit'] - worst['profit']
            margin_diff = best['profit_margin_percent'] - worst['profit_margin_percent']
            st.info(f"**Profit: {format_currency(profit_diff)}**")
            st.info(f"**Margin: {margin_diff:.2f} pp**")

        with col3:
            st.markdown("#### 📉 Worst Scenario")
            st.error(f"**{worst['scenario_name']}**")
            st.write(f"Profit: {format_currency(worst['profit'])}")
            st.write(f"Margin: {worst['profit_margin_percent']:.2f}%")

        # Cost component impact
        st.divider()
        st.subheader("💡 Cost Component Impact Analysis")

        prod_diff = abs(best['costs_breakdown']['production_costs'] - worst['costs_breakdown']['production_costs'])
        truck_exp_diff = abs(best['costs_breakdown']['truck_expenses'] - worst['costs_breakdown']['truck_expenses'])
        trucking_diff = abs(best['costs_breakdown']['trucking_costs'] - worst['costs_breakdown']['trucking_costs'])
        skid_diff = abs(best['costs_breakdown']['skid_costs'] - worst['costs_breakdown']['skid_costs'])

        impact_data = {
            'Cost Component': ['Production Costs', 'Truck Expenses', 'Trucking Costs', 'Skid Costs'],
            'Difference (NGN)': [prod_diff, truck_exp_diff, trucking_diff, skid_diff],
            'Impact': [
                f"{prod_diff/(prod_diff+truck_exp_diff+trucking_diff+skid_diff)*100:.1f}%",
                f"{truck_exp_diff/(prod_diff+truck_exp_diff+trucking_diff+skid_diff)*100:.1f}%",
                f"{trucking_diff/(prod_diff+truck_exp_diff+trucking_diff+skid_diff)*100:.1f}%",
                f"{skid_diff/(prod_diff+truck_exp_diff+trucking_diff+skid_diff)*100:.1f}%"
            ]
        }

        df_impact = pd.DataFrame(impact_data)
        df_impact = df_impact.sort_values('Difference (NGN)', ascending=False)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.dataframe(df_impact, use_container_width=True, hide_index=True)

        with col2:
            biggest_impact = df_impact.iloc[0]
            st.success(f"**Biggest Impact: {biggest_impact['Cost Component']}**")
            st.write(f"Difference: {format_currency(biggest_impact['Difference (NGN)'])}")
            st.write(f"Represents {biggest_impact['Impact']} of total cost difference")

        # Detailed table
        st.divider()
        st.subheader("📋 Detailed Comparison Table")

        table_data = []
        for result in sorted_results:
            table_data.append({
                'Scenario': result['scenario_name'],
                'Mother Station': result['mother_station'],
                'Revenue': result['revenue'],
                'Production Costs': result['costs_breakdown']['production_costs'],
                'Truck Expenses': result['costs_breakdown']['truck_expenses'],
                'Trucking Costs': result['costs_breakdown']['trucking_costs'],
                'Skid Costs': result['costs_breakdown']['skid_costs'],
                'Total Costs': result['costs_breakdown']['total_costs'],
                'Profit': result['profit'],
                'Margin %': result['profit_margin_percent']
            })

        df_table = pd.DataFrame(table_data)
        st.dataframe(df_table, use_container_width=True, hide_index=True)

        # Export options
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            csv = df_table.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"powergas_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            json_data = json.dumps(sorted_results, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"powergas_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

def show_about():
    st.header("ℹ️ About PowerGas Profitability Calculator")

    st.markdown("""
    ### Overview

    This tool helps PowerGas track and analyze the profitability of gas delivery operations
    from **Mother Stations** (dispatching plants) to **Daughter Stations** (customer locations).

    ### The Formula

    ```
    Profit = (GV × GP) - [ ((GC + PC + G&A) × GV) + ((TD + TIS + FC) × TTAT) + ((FTC + VTC) × RTD) + (SD × STAT) ]
    ```

    ### Components

    #### Revenue
    - **GV**: Gas Volume (scm per trip)
    - **GP**: Gas Price (NGN per scm)

    #### Production Costs
    - **GC**: Gas Cost (NGN per scm)
    - **PC**: Plant Cost (NGN per scm)
    - **G&A**: General & Administrative Cost (NGN per scm)

    #### Truck Expenses (time-based)
    - **TD**: Truck Depreciation (NGN per hour)
    - **TIS**: Truck Interest + Insurance (NGN per hour)
    - **FC**: Fuel Cost (NGN per hour)
    - **TTAT**: Truck Turnaround Time (hours)

    #### Trucking Costs (distance-based)
    - **FTC**: Fixed Trucking Cost (NGN per km)
    - **VTC**: Variable Trucking Cost (NGN per km)
    - **RTD**: Round Trip Distance (km)

    #### Skid Costs (time-based)
    - **SD**: Skid Depreciation (NGN per hour)
    - **STAT**: Skid Turnaround Time (hours)

    ### Features

    ✅ **Single Trip Calculator**: Calculate profitability for individual trips

    ✅ **Scenario Comparison**: Compare multiple Mother Stations delivering to the same customer

    ✅ **Visual Analytics**: Interactive charts and graphs

    ✅ **Cost Analysis**: Identify biggest cost drivers

    ✅ **Export Data**: Download results as CSV or JSON

    ### Development Phases

    - ✅ **Phase 1**: Formula implementation
    - ✅ **Phase 2**: Manual input testing
    - ✅ **Phase 3**: What-if scenario comparison
    - ⏳ **Phase 4**: Processing of trip data
    - ⏳ **Phase 5**: Using trip data as input
    - ⏳ **Phase 6**: PRMS dispensing input
    - ⏳ **Phase 7**: Monthly update interface

    ### Version

    **v1.0** - December 2025

    ---

    Made with ❤️ using Streamlit
    """)

if __name__ == "__main__":
    main()
