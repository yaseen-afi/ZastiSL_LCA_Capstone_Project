import os
import plotly.graph_objects as go
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.schemas.carbon_input import TotalCarbonFootprintResponse  # Adjusted import path

router = APIRouter()

@router.post("/visualize-carbon-footprint")
async def visualize_carbon_footprint(response: TotalCarbonFootprintResponse):
    try:
        stages = response.stages
        stage_names = [stage.stage for stage in stages]
        emissions = [stage.total_emission for stage in stages]

        # Define the directory for saving visualizations
        plot_dir = "C:\\WORK - AFI\\LCA Training\\Capstone\\visualizations"
        os.makedirs(plot_dir, exist_ok=True)

        # Create Bar Chart using Plotly
        bar_chart = go.Figure(go.Bar(
            x=stage_names, 
            y=emissions, 
            marker=dict(color=emissions, colorscale='Viridis')
        ))
        bar_chart.update_layout(
            title="Carbon Footprint by Stage",
            xaxis_title="Stage",
            yaxis_title="Carbon Footprint (kg CO2 eq.)",
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,1)',
            font=dict(color='black', size=14),
            title_font=dict(color='black', size=20)
        )
        bar_chart_path = os.path.join(plot_dir, "carbon_footprint_bar.html")
        bar_chart.write_html(bar_chart_path)

        # Create Pie Chart using Plotly
        pie_chart = go.Figure(go.Pie(
            labels=stage_names, 
            values=emissions, 
            hole=0.4,
            textinfo='label+percent',
            hoverinfo='label+value+percent',
            marker=dict(line=dict(color='black', width=2))
        ))
        pie_chart.update_layout(
            title="Contribution to Total Carbon Footprint by Stage",
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,1)',
            font=dict(color='black', size=14),
            title_font=dict(color='black', size=20)
        )
        pie_chart_path = os.path.join(plot_dir, "carbon_footprint_pie.html")
        pie_chart.write_html(pie_chart_path)

        # Return the file paths for both charts
        return {
            "bar_chart": bar_chart_path,
            "pie_chart": pie_chart_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
