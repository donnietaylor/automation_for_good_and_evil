# Community Risk Tracker

An n8n workflow that monitors real-time government data feeds and generates automated AI-powered community risk briefings for emergency management.

## Description

This is a "good" automation example that demonstrates how AI and public data sources can be combined to produce timely, plain-English risk summaries for communities. The workflow pulls data from seven official government APIs simultaneously, filters for local relevance, and uses GPT to synthesize the information into an actionable risk briefing.

## Features

- ✅ Monitors 7 real-time government hazard data feeds in parallel
- ✅ Filters results to a configurable geographic region
- ✅ Generates AI-powered plain-English risk briefing
- ✅ Classifies overall risk level (HIGH / MODERATE / LOW / NONE)
- ✅ Runs on-demand via manual trigger or can be scheduled

## Data Sources

| Source | API | What It Tracks |
|---|---|---|
| National Weather Service | `api.weather.gov` | Active weather alerts by state |
| USGS Earthquake Hazards | `earthquake.usgs.gov` | Seismic activity ≥ 2.5 magnitude |
| NIFC Wildfire Incidents | `inciweb.wildfire.gov` | Active wildfire incidents and acreage |
| FEMA Disaster Declarations | `www.fema.gov/api` | Federal disaster declarations by state |
| NOAA Storm Prediction Center | `www.spc.noaa.gov` | Severe weather outlook risk categories |
| AirNow AQI | `www.airnowapi.org` | Air quality index readings |
| USGS Water Resources | `waterservices.usgs.gov` | Stream gauge levels and flood stage |

## Prerequisites

- [n8n](https://n8n.io/) (self-hosted or n8n Cloud)
- OpenAI API key (for the AI risk briefing step)

## Installation

1. Import `workflow.json` into your n8n instance:
   - Open n8n → **Workflows** → **Import from File**
   - Select `workflow.json`

2. Configure credentials in n8n:
   - Add an **OpenAI** credential with your API key

3. (Optional) Update the geographic filter in the **Filter + Extract** nodes to match your region. The default region covers Texas, Oklahoma, Louisiana, New Mexico, and Arkansas.

## Usage

1. Open the imported workflow in n8n
2. Click **Execute Workflow** (or set up a Schedule trigger for automated runs)
3. The workflow will:
   - Fetch data from all 7 sources in parallel
   - Filter and normalize the results
   - Send the aggregated data to OpenAI
   - Output a risk briefing with a risk level classification

### Example Output

```
Risk Level: MODERATE

Briefing: A Tornado Watch is in effect for northern Texas through 8 PM CDT.
Moderate AQI levels (107) have been recorded in the Dallas-Fort Worth metro
due to wildfire smoke drifting from an active 3,200-acre fire in eastern
Oklahoma. Stream gauges on the Trinity River are approaching action stage.
Residents in affected areas should monitor local alerts and avoid outdoor
activities if air quality is a concern.

Generated: 2025-06-10T14:32:00Z
```

## How It Works

```
Manual Trigger
      │
      ▼
┌─────────────────────────────────────────┐
│          Parallel Data Fetch            │
│  NWS · USGS EQ · Wildfires · FEMA      │
│  SPC · AirNow · USGS Stream Gauges     │
└─────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│         Filter + Extract                │
│  - Normalize data from each source      │
│  - Filter to geographic region          │
│  - Remove non-critical events           │
└─────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│         AI Risk Briefing                │
│  - GPT synthesizes into plain English   │
│  - Prioritizes life-safety hazards      │
│  - Classifies overall risk level        │
└─────────────────────────────────────────┘
      │
      ▼
   Risk Report (briefing + risk level + timestamp)
```

## Configuration

To change the monitored region, update the state/area codes in the HTTP Request nodes:

| Node | Parameter to change |
|---|---|
| Fetch NWS Alerts | `area` query parameter (e.g., `TX`, `OK`) |
| Filter USGS Earthquakes | Bounding box coordinates in the Code node |
| Filter FEMA Declarations | `state` filter in the Code node |
| Fetch AirNow AQI | `zipCode` or `boundingBox` parameter |
| Fetch USGS Stream Gauges | `stateCd` parameter |

## Cost Estimate

Each workflow run makes one OpenAI API call to summarize the aggregated data.

| Model | Estimated cost per run |
|---|---|
| gpt-4o-mini | ~$0.001 |
| gpt-4o | ~$0.01 |

Cost will vary based on the volume of active incidents passed to the model.

## Use Cases

- Municipal emergency management dashboards
- Community alert and notification systems
- Civic engagement platforms
- Emergency preparedness training and demonstrations

## Limitations

- Requires internet access to reach all government APIs
- Some APIs (e.g., AirNow) may require a free API key registration
- Geographic filtering logic targets the south-central US by default and must be updated for other regions
- AI briefing quality depends on the OpenAI model selected

## Extending the Workflow

- Add a **Schedule Trigger** to run automatically (e.g., every hour)
- Connect an **Email** or **Slack** node to send briefings to a distribution list
- Store results in a database node for historical trend analysis
- Add additional data sources such as CDC disease outbreak feeds or local traffic incident APIs
