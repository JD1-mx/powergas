Product Requirement Details:

1. We are building a tool to help powergas track profitability of operations of delivery of gas across their different dispatching plants to their multiple customer locations

Here are the requests from the customer:

1. Do we have reliable data on Turn Around Time both for trucks and skids between all Mother Stations (dispatching plants) and Daughter Stations (customer locations) served?  
     
2. With (1) above do we have clear data for automated client profitability matrix split between the different MS for same clients
   

3. With (2) above do we have data and visibility of the changes in costs (gas, haulage, depreciation) when using e.g. Ebedei vs Ore and Ikorodu, or Ebedei versus Ogbele  
     
4. With (3) above can you provide an overview per client on the improvement/drop in profitability PEL have had in October (or November to date) by sourcing a significant percentage of total gas from Ore, Ikorodu, Ogbele, instead of Ebedei  
     
5. With (2 and 3\) above do we have data to prove how much time we have saved by Truck and Skid/Trailer respectively during this period by sourcing from these PGINL MS closer to PEL clients compared to if sourced from Ebedei


6. Are the above data (1-5) not automated so when PEL provide the monthly adjustments on **exchange rates, selling price, gas costs, and total volume sold to calculate split of plant costs and sga costs,** the client profitability report can be auto-generated, and are the data of such quality that we can use it for **scenario planning and make what/if scenarios to understand profit (or adjusted EBITDA) impact and asset utilization impact, by changing sourcing MS?**  
     
   

your job in phases:

Phases:

1. Defining formula  
   1. Create a python script well commented based on the formula defined in the documentation  
2. Test with manual input values  
   1. Create a JSON where I can make adjustments of the input values needed for the variables in the formula  
3. Comparison interface (what if) scenarios (manual)   
   1. Create a JSON where I can set multiple scenarios like  
      1. What if instead of delivering to customer from point A (and all costs /distances etc etc) associated with point A I go ahead from point B?  
      2. How would profitability be impacted? / in which component would we see the biggest change creating this impact?

I’ll give you further instructions for the steps below once we complete and verify the above

4. Processing of trip data  
5. Using trip data as input  
6. PRMS \- dispensing input  
7. Interface for monthly input of updated values (not tracked by telematics)  
   1. N8n workflow triggering update 

The formula:

**1\. Explanation of the Components** 

**Revenue Components** 

● **Gas Price (GP)** – input value per scm (mapped to each delivery location / Daughter Station). 

● **Gas Volume (GV)** – input value per trip, based on SCM defined at each Mother Station (Gas Plant). 

● **Gas Volume Dispensed (GVD)** – *future improvement: replace GV with actual dispensed volumes tracked via waybills.* 

**Truck & Skid – Costs & Expenses** 

● **Gas Cost (GC)** – input value, per scm, depending on source Mother Station. ● **Round Trip Distance (RTD)** – sensor-tracked distance (Pickup → Delivery → Pickup). ● **Fixed Trucking Cost (FTC)** – input value, contractor-based (Diadem: NGN/km; IMI: NGN/day). 

● **Variable Trucking Cost (VTC)** – input value, contractor-based, applied beyond FTC thresholds. 

● **Skid Depreciation (SD)** – input value, converted to per-hour. 

● **Truck Depreciation (TD)** – input value, converted to per-hour. 

● **Truck Interest \+ Insurance (TIS)** – input value, varies by contractor. 

● **Skid Turnaround Time (STAT)** – tracked value, currently manual, to transition to sensor. ● **Truck Turnaround Time (TTAT)** – sensor-tracked trip duration. 

● **Fuel Cost (FC)** – input value, contractor-based (USD/hr), to transition to (USD/km) ● **Plant Cost (PC)** – input value, per scm. 

● **G\&A Cost (G\&A)** – input value, per scm. 

**2\. Explanation of the Formula for the Base Scenario** 

**Applicable for trips where:** 

Pickup (Mother Station) → Delivery (Daughter Station) → Pickup (Mother Station), with a skid dispatched outbound and a skid brought back (same or different).

**`Profit = (GV × GP) - [ ((GC + PC + G&A) × GV) + ((TD + TIS + FC) × TTAT) + ((FTC + VTC) × RTD) + (SD × STAT) ]`** 

**Formula Sequence** 

1\. **Revenue from gas sales** 

○ Currently: GV×GP 

○ *Future: GVD×GP (actual dispensed volume via waybills)* 

2\. **Production & Plant Costs** 

○ (GC \+ PC \+ G\&A) × GV 

○ *Future: replace GV with GVD* 

3\. **Truck Expenses** 

○ (TD+TIS+FC)×TTAT 

○ Based on per-hour depreciation, insurance/interest, and fuel cost. 

○ *Future: include wait time at Mother Station (since depreciation applies even when idle) and transition fuel cost to be based on distance.* 

4\. **Trucking Costs** 

○ (FTC+VTC)×RTD 

○ Contractor-specific cost models (Diadem distance-based, IMI daily-based). ○ *Future: allow operation days as an input.* 

5\. **Skid Costs** 

○ SD×STAT 

○ *Future: include wait time at Mother Station in STAT.* 
