"""
PowerGas Profitability Calculator

This script calculates the profitability of gas delivery operations from Mother Stations
(dispatching plants) to Daughter Stations (customer locations).

Formula:
Profit = (GV × GP) - [ ((GC + PC + G&A) × GV) + ((TD + TIS + FC) × TTAT) + ((FTC + VTC) × RTD) + (SD × STAT) ]

Components:
- GV: Gas Volume (scm per trip)
- GP: Gas Price (NGN per scm)
- GC: Gas Cost (NGN per scm)
- PC: Plant Cost (NGN per scm)
- G&A: General & Administrative Cost (NGN per scm)
- TD: Truck Depreciation (NGN per hour)
- TIS: Truck Interest + Insurance (NGN per hour)
- FC: Fuel Cost (NGN per hour)
- TTAT: Truck Turnaround Time (hours)
- FTC: Fixed Trucking Cost (NGN per km)
- VTC: Variable Trucking Cost (NGN per km)
- RTD: Round Trip Distance (km)
- SD: Skid Depreciation (NGN per hour)
- STAT: Skid Turnaround Time (hours)
"""

import json
from typing import Dict, List, Any
from datetime import datetime


class ProfitabilityCalculator:
    """
    Calculator for gas delivery profitability analysis.

    Attributes:
        config (dict): Configuration parameters for the calculation
    """

    def __init__(self, config_file: str = 'config.json'):
        """
        Initialize the calculator with configuration from a JSON file.

        Args:
            config_file (str): Path to the configuration JSON file
        """
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def calculate_revenue(self, gas_volume: float, gas_price: float) -> float:
        """
        Calculate revenue from gas sales.

        Formula: GV × GP

        Args:
            gas_volume (float): Gas volume in scm
            gas_price (float): Gas price in NGN per scm

        Returns:
            float: Total revenue in NGN
        """
        revenue = gas_volume * gas_price
        return revenue

    def calculate_production_costs(self, gas_volume: float, gas_cost: float,
                                   plant_cost: float, ga_cost: float) -> float:
        """
        Calculate production and plant costs.

        Formula: (GC + PC + G&A) × GV

        Args:
            gas_volume (float): Gas volume in scm
            gas_cost (float): Gas cost in NGN per scm
            plant_cost (float): Plant cost in NGN per scm
            ga_cost (float): G&A cost in NGN per scm

        Returns:
            float: Total production costs in NGN
        """
        per_scm_cost = gas_cost + plant_cost + ga_cost
        total_cost = per_scm_cost * gas_volume
        return total_cost

    def calculate_truck_expenses(self, truck_depreciation: float, truck_insurance: float,
                                fuel_cost: float, turnaround_time: float) -> float:
        """
        Calculate truck-related expenses.

        Formula: (TD + TIS + FC) × TTAT

        Args:
            truck_depreciation (float): Truck depreciation in NGN per hour
            truck_insurance (float): Truck interest + insurance in NGN per hour
            fuel_cost (float): Fuel cost in NGN per hour
            turnaround_time (float): Truck turnaround time in hours

        Returns:
            float: Total truck expenses in NGN
        """
        per_hour_cost = truck_depreciation + truck_insurance + fuel_cost
        total_expense = per_hour_cost * turnaround_time
        return total_expense

    def calculate_trucking_costs(self, fixed_trucking_cost: float,
                                variable_trucking_cost: float,
                                round_trip_distance: float) -> float:
        """
        Calculate contractor trucking costs.

        Formula: (FTC + VTC) × RTD

        Args:
            fixed_trucking_cost (float): Fixed trucking cost in NGN per km
            variable_trucking_cost (float): Variable trucking cost in NGN per km
            round_trip_distance (float): Round trip distance in km

        Returns:
            float: Total trucking costs in NGN
        """
        per_km_cost = fixed_trucking_cost + variable_trucking_cost
        total_cost = per_km_cost * round_trip_distance
        return total_cost

    def calculate_skid_costs(self, skid_depreciation: float,
                            skid_turnaround_time: float) -> float:
        """
        Calculate skid depreciation costs.

        Formula: SD × STAT

        Args:
            skid_depreciation (float): Skid depreciation in NGN per hour
            skid_turnaround_time (float): Skid turnaround time in hours

        Returns:
            float: Total skid costs in NGN
        """
        total_cost = skid_depreciation * skid_turnaround_time
        return total_cost

    def calculate_trip_profit(self, trip_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate profit for a single trip.

        Args:
            trip_data (dict): Dictionary containing all trip parameters

        Returns:
            dict: Detailed breakdown of revenue, costs, and profit
        """
        # Revenue calculation
        revenue = self.calculate_revenue(
            trip_data['gas_volume'],
            trip_data['gas_price']
        )

        # Cost calculations
        production_costs = self.calculate_production_costs(
            trip_data['gas_volume'],
            trip_data['gas_cost'],
            trip_data['plant_cost'],
            trip_data['ga_cost']
        )

        truck_expenses = self.calculate_truck_expenses(
            trip_data['truck_depreciation'],
            trip_data['truck_insurance'],
            trip_data['fuel_cost'],
            trip_data['truck_turnaround_time']
        )

        trucking_costs = self.calculate_trucking_costs(
            trip_data['fixed_trucking_cost'],
            trip_data['variable_trucking_cost'],
            trip_data['round_trip_distance']
        )

        skid_costs = self.calculate_skid_costs(
            trip_data['skid_depreciation'],
            trip_data['skid_turnaround_time']
        )

        # Total costs
        total_costs = production_costs + truck_expenses + trucking_costs + skid_costs

        # Profit
        profit = revenue - total_costs

        # Profit margin percentage
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0

        return {
            'trip_id': trip_data.get('trip_id', 'N/A'),
            'mother_station': trip_data.get('mother_station', 'N/A'),
            'daughter_station': trip_data.get('daughter_station', 'N/A'),
            'revenue': round(revenue, 2),
            'costs_breakdown': {
                'production_costs': round(production_costs, 2),
                'truck_expenses': round(truck_expenses, 2),
                'trucking_costs': round(trucking_costs, 2),
                'skid_costs': round(skid_costs, 2),
                'total_costs': round(total_costs, 2)
            },
            'profit': round(profit, 2),
            'profit_margin_percent': round(profit_margin, 2)
        }

    def compare_scenarios(self, scenarios_file: str = 'scenarios.json') -> List[Dict[str, Any]]:
        """
        Compare multiple what-if scenarios.

        Args:
            scenarios_file (str): Path to the scenarios JSON file

        Returns:
            list: Results for each scenario with comparison metrics
        """
        with open(scenarios_file, 'r') as f:
            scenarios_data = json.load(f)

        results = []

        for scenario in scenarios_data['scenarios']:
            scenario_result = self.calculate_trip_profit(scenario['trip_data'])
            scenario_result['scenario_name'] = scenario['name']
            scenario_result['description'] = scenario.get('description', '')
            results.append(scenario_result)

        return results

    def generate_comparison_report(self, scenarios_file: str = 'scenarios.json') -> str:
        """
        Generate a detailed comparison report for multiple scenarios.

        Args:
            scenarios_file (str): Path to the scenarios JSON file

        Returns:
            str: Formatted comparison report
        """
        results = self.compare_scenarios(scenarios_file)

        if not results:
            return "No scenarios found."

        # Sort by profit (descending)
        sorted_results = sorted(results, key=lambda x: x['profit'], reverse=True)

        # Build report
        report = "\n" + "="*80 + "\n"
        report += "POWERGAS PROFITABILITY COMPARISON REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "="*80 + "\n\n"

        # Summary table
        report += "SUMMARY (Ranked by Profit)\n"
        report += "-"*80 + "\n"
        report += f"{'Rank':<6}{'Scenario':<25}{'Profit (NGN)':<18}{'Margin %':<12}{'Route'}\n"
        report += "-"*80 + "\n"

        for idx, result in enumerate(sorted_results, 1):
            route = f"{result['mother_station']} → {result['daughter_station']}"
            report += f"{idx:<6}{result['scenario_name']:<25}{result['profit']:>15,.2f}   {result['profit_margin_percent']:>8.2f}%   {route}\n"

        # Detailed breakdown for each scenario
        report += "\n" + "="*80 + "\n"
        report += "DETAILED BREAKDOWN\n"
        report += "="*80 + "\n"

        for idx, result in enumerate(sorted_results, 1):
            report += f"\n{idx}. {result['scenario_name']}\n"
            report += f"   Description: {result['description']}\n"
            report += f"   Route: {result['mother_station']} → {result['daughter_station']}\n"
            report += f"   -" + "-"*75 + "\n"
            report += f"   Revenue:                    NGN {result['revenue']:>15,.2f}\n"
            report += f"   Costs:\n"
            report += f"     - Production Costs:       NGN {result['costs_breakdown']['production_costs']:>15,.2f}\n"
            report += f"     - Truck Expenses:         NGN {result['costs_breakdown']['truck_expenses']:>15,.2f}\n"
            report += f"     - Trucking Costs:         NGN {result['costs_breakdown']['trucking_costs']:>15,.2f}\n"
            report += f"     - Skid Costs:             NGN {result['costs_breakdown']['skid_costs']:>15,.2f}\n"
            report += f"   Total Costs:                NGN {result['costs_breakdown']['total_costs']:>15,.2f}\n"
            report += f"   " + "-"*75 + "\n"
            report += f"   PROFIT:                     NGN {result['profit']:>15,.2f}\n"
            report += f"   Profit Margin:              {result['profit_margin_percent']:>15.2f}%\n"

        # Comparative analysis
        if len(sorted_results) > 1:
            report += "\n" + "="*80 + "\n"
            report += "COMPARATIVE ANALYSIS\n"
            report += "="*80 + "\n\n"

            best = sorted_results[0]
            worst = sorted_results[-1]

            profit_diff = best['profit'] - worst['profit']
            margin_diff = best['profit_margin_percent'] - worst['profit_margin_percent']

            report += f"Best Scenario:  {best['scenario_name']}\n"
            report += f"Worst Scenario: {worst['scenario_name']}\n\n"
            report += f"Profit Difference:       NGN {profit_diff:>15,.2f}\n"
            report += f"Margin Difference:       {margin_diff:>15.2f} percentage points\n\n"

            # Cost comparison
            report += "Cost Component Impact Analysis:\n"
            report += "-"*80 + "\n"

            prod_diff = best['costs_breakdown']['production_costs'] - worst['costs_breakdown']['production_costs']
            truck_exp_diff = best['costs_breakdown']['truck_expenses'] - worst['costs_breakdown']['truck_expenses']
            trucking_diff = best['costs_breakdown']['trucking_costs'] - worst['costs_breakdown']['trucking_costs']
            skid_diff = best['costs_breakdown']['skid_costs'] - worst['costs_breakdown']['skid_costs']

            report += f"Production Costs Difference:    NGN {prod_diff:>15,.2f}\n"
            report += f"Truck Expenses Difference:      NGN {truck_exp_diff:>15,.2f}\n"
            report += f"Trucking Costs Difference:      NGN {trucking_diff:>15,.2f}\n"
            report += f"Skid Costs Difference:          NGN {skid_diff:>15,.2f}\n"

            # Find biggest impact
            impacts = {
                'Production Costs': abs(prod_diff),
                'Truck Expenses': abs(truck_exp_diff),
                'Trucking Costs': abs(trucking_diff),
                'Skid Costs': abs(skid_diff)
            }
            biggest_impact = max(impacts, key=impacts.get)

            report += f"\nBiggest Cost Impact: {biggest_impact} (NGN {impacts[biggest_impact]:,.2f})\n"

        report += "\n" + "="*80 + "\n"

        return report


def main():
    """
    Main function to demonstrate the calculator usage.
    """
    print("PowerGas Profitability Calculator")
    print("="*80)

    try:
        # Initialize calculator with config file
        calculator = ProfitabilityCalculator('config.json')

        # Calculate single trip from config
        print("\nCalculating trip profitability from config.json...")
        trip_result = calculator.calculate_trip_profit(calculator.config['trip_data'])

        print(f"\nTrip ID: {trip_result['trip_id']}")
        print(f"Route: {trip_result['mother_station']} → {trip_result['daughter_station']}")
        print(f"Revenue: NGN {trip_result['revenue']:,.2f}")
        print(f"Total Costs: NGN {trip_result['costs_breakdown']['total_costs']:,.2f}")
        print(f"Profit: NGN {trip_result['profit']:,.2f}")
        print(f"Profit Margin: {trip_result['profit_margin_percent']:.2f}%")

        # Generate comparison report
        print("\n" + "="*80)
        print("\nGenerating scenario comparison report...")
        report = calculator.generate_comparison_report('scenarios.json')
        print(report)

        # Save report to file
        with open('profitability_report.txt', 'w') as f:
            f.write(report)
        print("\nReport saved to: profitability_report.txt")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please ensure config.json and scenarios.json exist in the same directory.")
    except KeyError as e:
        print(f"\nError: Missing required field {e}")
        print("Please check your JSON configuration files.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
