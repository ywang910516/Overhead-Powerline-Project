# Overhead-Powerline-Project
This repository contains the data and scripts related to the study of "The impact of electrical hazards from overhead power lines on urban search and rescue operations during extreme flood events"

The study was published in the International Journal of Disaster Risk Reduction" in Volume 104 in April 2024.

## A brief introduction of this study:
Accurate flood forecasting and efficient emergency response operations are vital, especially in the case of urban flash floods. The dense distribution of power lines in urban areas significantly impacts search and rescue operations during extreme flood events. However, no existing emergency response frameworks have incorporated the impacts of overhead power lines on lifeboat rescue operations. This study aims to determine the necessity and feasibility of incorporating overhead power line information into an emergency response framework using Manville, New Jersey, during Hurricane Ida as a test bed. We propose an integrated framework, which includes a building-scale flood model, urban point cloud data, a human vulnerability model, and network analysis, to simulate rescue operation feasibility during Hurricane Ida. Results reveal that during the most severe point of the flood event, 46% of impacted buildings became nonrescuable due to complete isolation from the road network, and a significant 67.7% of the municipality’s areas that became dangerous for pedestrians also became inaccessible to rescue boats due to overhead power line obstruction. Additionally, we identify a continuous 10-hour period during which an average of 43.4% of the 991 impacted buildings faced complete isolation. For these structures, early evacuation emerges as the sole means to prevent isolation. This research highlights the pressing need to consider overhead power lines in emergency response planning to ensure more effective and targeted flood resilience measures for urban areas facing increasingly frequent extreme precipitation events.

## An acknowledgement

This material is based upon work supported by FEMA under HMGP DR4488, the U.S. Department of Homeland Security under Grant Award 22STESE00001-03-02, and the U.S. National Science Foundation under award 2103754, . The views and conclusions contained in this document are those of the authors and should not be interpreted as necessarily representing the official policies, either expressed or implied, of the U.S. National Science Foundation and U.S. Department of Homeland Security

## citation to the paper
Wang, Y., Josephs, H., Duan, Z., & Gong, J. (2024). The impact of electrical hazards from overhead power lines on urban search and rescue operations during extreme flood events. International Journal of Disaster Risk Reduction, 104359.

## Repository Structure
**Data/**: Contains datasets used for analysis.
**scripts/**: Contains scripts for data processing and analysis.
**plot/**: Contains plots of this study

## Reproduce the analysis
ArcGIS Pro and Python are required.
1. Prepare the necessary software and download the required data from #Data.
2. Using the introduction file (scripts/Processing_ArcGIS-Pro.txt), pre-process the data in ArcGIS Pro.
3. Follow the instructions in the Network Analysis Module (found in the command lines of scripts/makeEvaRoutes.py) to perform network analysis in ArcGIS Pro.
4. Run the script FindNotRescuable.py (scripts/FindNotRescuable.py) to identify all non-rescuable houses at each time step.
5. Run the script FindEvacuable.py (scripts/FindEvacuable.py) to identify all non-evacuable houses at each time step.
6. Run the script Compare_cross.py (scripts/Compare_cross.py) to identify houses that are "rescuable but non-evacuable" and "evacuable but non-rescuable."

| Script Name | Description | How to Run |
| --- | --- | --- |
| `scripts/makeEvaRoutes.py` | Script contains all functions for network analysis | use it in ArcGIS Pro |
| `scripts/FindNotRescuable.py` | Script to find all not-rescuable houses | `python3 FindNotRescuable.py` |
| `scripts/FindEvacuable.py` | Script to find all not-evacuable houses | `python3 FindEvacuable.py` |
| `scripts/Compare_cross.py` | Script to find "rescuable but non-evacuable" and "evacuable but non-rescuable" houses | `python3 Compare_cross.py` |

## Reproduce the figures
| Script Name | Description | How to Run |
| --- | --- | --- |
| `scripts/evac-rescue-conditions.py` | Script to plot rescue and evacuation availability | `python3 evac-rescue-conditions.py` |
| `scripts/compare_evac_rescue.py` | Script to compare rescue and evacuation availability as time-series | `python3 compare_evac_rescue.py` |
| `scripts/plot_NoRescue_loc.py` | Script to plot spatial distribution of all non-rescuable houses | `python3 plot_NoRescue_loc.py` |
| `scripts/powerline_overview.py` | Script to overview the heights of overhead power lines above the ground | `python3 powerline_overview.py` |

