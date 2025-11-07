import numpy as np
import pandas as pd
from scipy.stats import theilslopes


aquifers = {
    'Ogallala': {
        'color': 'lightblue',
        'path': '/Users/finleydavis/Desktop/csvs final/Ogallala_Final.csv'
    },
    'Edwards (Balcones Fault Zone)': {
        'color': 'darkblue',
        'path': '/Users/finleydavis/Desktop/csvs final/Edwards (Balcones Fault Zone) Aquifer)_Final.csv'
    },
    'Edwards-Trinity Plateau': {
        'color': 'lightgreen',
        'path': '/Users/finleydavis/Desktop/csvs final/Edwards-Trinity Plateau_Final.csv'
    },
    'Carrizo-Wilcox': {
        'color': 'red',
        'path': '/Users/finleydavis/Desktop/csvs final/Carrizo-Wilcox_Final.csv'
    },
    'Gulf Coast': {
        'color': 'yellow',
        'path': '/Users/finleydavis/Desktop/csvs final/Gulf Coast_Final.csv'
    },
    'Pecos Valley': {
        'color': 'orange',
        'path': '/Users/finleydavis/Desktop/csvs final/Pecos Valley_Final.csv'
    },
    'Seymour': {
        'color': 'brown',
        'path': '/Users/finleydavis/Desktop/csvs final/Seymour_Final.csv'
    },
    'Trinity': {
        'color': 'green',
        'path': '/Users/finleydavis/Desktop/csvs final/Trinty_Final.csv'  
    },
    'Hueco-Mesilla Bolsons': {
        'color': 'pink',
        'path': '/Users/finleydavis/Desktop/csvs final/Hueco-Mesilla Basin_Final.csv'
    }
}

aquifer_ylim = {
    'Ogallala': (800, 0),
    'Edwards (Balcones Fault Zone)': (2000, 0),
    'Edwards-Trinity Plateau': (1000, 0),
    'Carrizo-Wilcox': (1500, 0),
    'Gulf Coast': (1500, 0),
    'Pecos Valley': (1400, 0),
    'Seymour': (200, 0),
    'Trinity': (1500, 0),
    'Hueco-Mesilla Bolsons': (1500, 0)
}

import numpy as np
import pandas as pd
from scipy.stats import theilslopes
import plotly.graph_objects as go

# --- same aquifers & ylim dicts as before ---

import numpy as np
import pandas as pd
from scipy.stats import theilslopes
import plotly.graph_objects as go

# =============================
# AQUFER INFO
# =============================
aquifers = {
    'Ogallala': {
        'color': 'lightblue',
        'path': '/Users/finleydavis/Desktop/csvs final/Ogallala_Final.csv'
    },
    'Edwards (Balcones Fault Zone)': {
        'color': 'darkblue',
        'path': '/Users/finleydavis/Desktop/csvs final/Edwards (Balcones Fault Zone) Aquifer)_Final.csv'
    },
    'Edwards-Trinity Plateau': {
        'color': 'lightgreen',
        'path': '/Users/finleydavis/Desktop/csvs final/Edwards-Trinity Plateau_Final.csv'
    },
    'Carrizo-Wilcox': {
        'color': 'red',
        'path': '/Users/finleydavis/Desktop/csvs final/Carrizo-Wilcox_Final.csv'
    },
    'Gulf Coast': {
        'color': 'yellow',
        'path': '/Users/finleydavis/Desktop/csvs final/Gulf Coast_Final.csv'
    },
    'Pecos Valley': {
        'color': 'orange',
        'path': '/Users/finleydavis/Desktop/csvs final/Pecos Valley_Final.csv'
    },
    'Seymour': {
        'color': 'brown',
        'path': '/Users/finleydavis/Desktop/csvs final/Seymour_Final.csv'
    },
    'Trinity': {
        'color': 'green',
        'path': '/Users/finleydavis/Desktop/csvs final/Trinty_Final.csv'
    },
    'Hueco-Mesilla Bolsons': {
        'color': 'pink',
        'path': '/Users/finleydavis/Desktop/csvs final/Hueco-Mesilla Basin_Final.csv'
    }
}

aquifer_ylim = {
    'Ogallala': (800, 0),
    'Edwards (Balcones Fault Zone)': (2000, 0),
    'Edwards-Trinity Plateau': (1000, 0),
    'Carrizo-Wilcox': (1500, 0),
    'Gulf Coast': (1500, 0),
    'Pecos Valley': (1400, 0),
    'Seymour': (200, 0),
    'Trinity': (1500, 0),
    'Hueco-Mesilla Bolsons': (1500, 0)
}

# =============================
# DATA PROCESSING FUNCTION
# =============================
def analyze_aquifer_data_CI_data(aquifer_name, start_date, end_date):
    aquifer = aquifers[aquifer_name]
    file_path = aquifer['path']

    dtype = {'ID': 'int32', 'Lat': 'float32', 'Long': 'float32', 
             'County': 'category', 'Date': 'int16', 'Depth': 'float32'}
    chunks = pd.read_csv(file_path, chunksize=10000, dtype=dtype)
    df = pd.concat(chunks).reset_index(drop=True)
    df.columns = ['ID', 'Lat', 'Long', 'County', 'Date', 'Depth']

    # Filter
    df = df[(df['Date'].between(start_date, end_date)) & (df['Depth'] > 0)].copy()

    # Define lognormal mean
    def lognormal_mean(x):
        if len(x) == 1:
            return x.iloc[0]
        log_x = np.log(x)
        return np.exp(log_x.mean() + 0.5 * log_x.std() ** 2)

    annual_means = df.groupby('Date')['Depth'].agg(lognormal_mean).interpolate().reset_index()
    annual_means['Date'] = pd.to_numeric(annual_means['Date'], errors='coerce')

    Dates = annual_means['Date'].values
    means = annual_means['Depth'].values

    # Theil-Sen regression
    slope, intercept, low_slope, high_slope = theilslopes(means, Dates, alpha=0.90)
    trend_line = intercept + slope * Dates

    # Bootstrap CIs
    n_boot = 1000
    bootstrap_trends = np.zeros((n_boot, len(Dates)))
    for i in range(n_boot):
        sample_idx = np.random.choice(len(Dates), len(Dates), replace=True)
        sample_Dates = Dates[sample_idx]
        sample_means = means[sample_idx]
        boot_slope, boot_intercept, *_ = theilslopes(sample_means, sample_Dates)
        bootstrap_trends[i] = boot_intercept + boot_slope * Dates

    lower_ci = np.percentile(bootstrap_trends, 5, axis=0)
    upper_ci = np.percentile(bootstrap_trends, 95, axis=0)

    return pd.DataFrame({
        "Year": Dates,
        "Mean": means,
        "Lower_CI": lower_ci,
        "Upper_CI": upper_ci,
        "Trend": trend_line
    }), slope, intercept

# =============================
# INTERACTIVE PLOT WITH JS CALLBACK
# =============================
def plot_aquifer_interactive(aquifer_name, start_date=1920, end_date=2023):
    df, slope, intercept = analyze_aquifer_data_CI_data(aquifer_name, start_date, end_date)
    aquifer_color = aquifers[aquifer_name]['color']
    ylim = aquifer_ylim[aquifer_name]

    fig = go.Figure()

    # Confidence Interval band
    fig.add_trace(go.Scatter(
        x=np.concatenate([df['Year'], df['Year'][::-1]]),
        y=np.concatenate([df['Upper_CI'], df['Lower_CI'][::-1]]),
        fill='toself',
        fillcolor=aquifer_color,
        opacity=0.3,
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo='skip',
        name='90% CI'
    ))

    # Annual means
    fig.add_trace(go.Scatter(
        x=df['Year'], y=df['Mean'],
        mode='lines+markers',
        marker=dict(size=5, color='black'),
        line=dict(color='black'),
        name='Annual Lognormal Mean'
    ))

    # Trend line
    fig.add_trace(go.Scatter(
        x=df['Year'], y=df['Trend'],
        mode='lines',
        line=dict(dash='dash', color='darkblue'),
        name=f'Theil–Sen Trend (slope={slope:.2f} ft/yr)',
        hoverinfo='skip'
    ))

    # Layout
    fig.update_layout(
        title=f'{aquifer_name} Aquifer: Theil–Sen Trend with 90% Bootstrap CI',
        xaxis=dict(
            title='Year',
            range=[start_date, end_date],
            autorange=False,
            rangeslider=dict(visible=True),
            fixedrange=False
        ),
        yaxis=dict(
            title='Depth (ft)',
            autorange='reversed',
            range=ylim
        ),
        template='plotly_white',
        hovermode='x unified',
        height=600,
        width=900
    )

    # =============================
    # JavaScript for live slope updates
    # =============================
    custom_js = f"""
    <script>
    var myPlot = document.getElementsByClassName('js-plotly-plot')[0];
    var data = {df.to_json(orient='records')};

    myPlot.on('plotly_relayout', function(e) {{
        if(e['xaxis.range[0]'] && e['xaxis.range[1]']) {{
            var xMin = e['xaxis.range[0]'];
            var xMax = e['xaxis.range[1]'];

            // Filter to current visible range
            var filtered = data.filter(d => d.Year >= xMin && d.Year <= xMax);
            if (filtered.length > 5) {{
                var x = filtered.map(d => d.Year);
                var y = filtered.map(d => d.Mean);

                // Compute Theil-Sen slope (simplified median of slopes)
                var slopes = [];
                for (var i = 0; i < x.length; i++) {{
                    for (var j = i + 1; j < x.length; j++) {{
                        slopes.push((y[j] - y[i]) / (x[j] - x[i]));
                    }}
                }}
                slopes.sort((a, b) => a - b);
                var medianSlope = slopes[Math.floor(slopes.length / 2)];

                // Compute new intercept
                var meanX = x.reduce((a,b)=>a+b,0)/x.length;
                var meanY = y.reduce((a,b)=>a+b,0)/y.length;
                var intercept = meanY - medianSlope * meanX;

                // Compute new trend line
                var trendY = x.map(v => intercept + medianSlope * v);

                // Update trace and legend
                Plotly.restyle(myPlot, {{
                    y: [trendY],
                    x: [x],
                    name: [`Theil–Sen Trend (slope=${{medianSlope.toFixed(2)}} ft/yr)`]
                }}, [2]);
            }}
        }}
    }});
    </script>
    """

    # Write full HTML with injected JS
    html_str = fig.to_html(include_plotlyjs='cdn', full_html=True)
    html_str = html_str.replace("</body>", custom_js + "\n</body>")

    out_path = f"{aquifer_name.replace(' ', '_')}_interactive_dynamic.html"
    with open(out_path, "w") as f:
        f.write(html_str)

    print(f"\n✅ Saved interactive plot with dynamic slope: {out_path}")
    print(f"📈 Initial Theil–Sen slope: {slope:.4f} ft/year")

# =============================
# EXAMPLE USAGE
# =============================
plot_aquifer_interactive('Ogallala', 1920, 2023)