import pandas as pd
import fonctions as f
import data as d 
from streamlit_lottie import st_lottie
import requests
from streamlit_extras.add_vertical_space import add_vertical_space
from mplsoccer.pitch import Pitch , VerticalPitch
import matplotlib.pyplot as plt
import math
import numpy as np 
import matplotlib as mpl
import seaborn as sns 
import matplotlib.font_manager as fm
import plotly.graph_objects as go
from scipy import stats
from mplsoccer import PyPizza, add_image
from highlight_text import fig_text


@f.st.cache_data
def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

spaces = '&nbsp;'
pos = {'GK':'Goalkeepers', 'DF':'Defenders', 'MID':'Midfielders', 'FWD':'Forwards'}

@f.st.cache_data
def display_player_card(player):
    f.st.markdown(d.css, unsafe_allow_html=True)
    html = f"""
    <div class="player-card">
        <div class="player-header">
            <img src="{player['Player Image']}" class="player-image">
            <div class="player-info">
                <h2 class="player-name">{player['Player']}</h2>
                <p class="player-team"><img src="{player['Team Logo']}" class="team-logo">{player['Team_x']}</p>
            </div>
        </div>
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{player['appearances']}</div>
                <div class="stat-label">Appearances</div>
            </div>
            <div class="stat">
                <div class="stat-value">{player['minutesPlayed']}</div>
                <div class="stat-label">Minutes Played</div>
            </div>
            <div class="stat">
                <div class="stat-value">{player['rating']:.2f}</div>
                <div class="stat-label">Rating</div>
            </div>
        </div>
        <h3>Player Bio</h3>
        <div class="player-bio">
            <div class="bio-item"><span class="bio-label">Nationality:</span><span class="bio-value">{spaces*2} {player['Nationality']}</span></div>
            <div class="bio-item"><span class="bio-label">Position:</span><span class="bio-value">{spaces*2} {player['Position']}</span></div>
            <div class="bio-item"><span class="bio-label">Age:</span><span class="bio-value">{spaces*2} {player['Age']}</span></div>
            <div class="bio-item"><span class="bio-label">Height:</span><span class="bio-value">{spaces*2} {player['Height']}</span></div>
            <div class="bio-item"><span class="bio-label">Market Value:</span><span class="bio-value">{spaces*2} {player['Market Value']}</span></div>
            <div class="bio-item"><span class="bio-label">Preferred Foot:</span><span class="bio-value">{spaces*2} {player['Preferred Foot']}</span></div>
        </div>
    </div>
    """
    f.st.markdown(html, unsafe_allow_html=True)

@f.st.cache_data
def pizza_plot(player_data, params_1, values, output):

    position_group = f.get_position_group(player_data['Position'])
    # Color palette
    background_color = "#0c1421"  # Dark blue background
    main_color = "#00CED1"  # Bright turquoise for the pizza slices
    accent_color = "#FF6B6B"  # Coral red for emphasis
    text_color = "#E0E0E0"  # Light gray for most text
    highlight_color = "#FFD700"  # Gold for important text/numbers
    # Slice colors (adjust as needed)
    colors_mapping = {'DF':[2,3,5], 'MID':[4,4,3], 'FWD':[5,4,1]}
    if position_group == 'GK':
        slice_colors = ["#11C9AF"] * 4
    else:
        num_colors = colors_mapping[position_group]
        slice_colors = ["#11C9AF"] * num_colors[0] + ["#FFA500"] * num_colors[1] + ["#D70232"] * num_colors[2]
    # Instantiate PyPizza class
    baker = PyPizza(
        params=params_1,
        straight_line_color="#2A3F5F",  # Slightly lighter than background for subtle lines
        straight_line_lw=1,
        last_circle_color="#4A6491",  # Highlighted outer circle
        last_circle_lw=2,
        other_circle_color="#2A3F5F",  # Same as straight lines
        other_circle_lw=1,
        other_circle_ls="-.",
        inner_circle_size=20
    )
    # Plot pizza
    fig, ax = baker.make_pizza(
        values,
        figsize=(8, 8),
        param_location=110,
        slice_colors=slice_colors,       # Color for individual slices
        #value_colors=text_colors,        # Color for the value-text
        #value_bck_colors=slice_colors,   # Color for the blank spaces
        blank_alpha=0.4,                 # Alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#FFFFFF", zorder=2, linewidth=1, alpha=0.8
        ),
        kwargs_params=dict(
            color=text_color, fontsize=11,
            va="center", fontweight='bold'
        ),
        kwargs_values=dict(
            color=highlight_color, fontsize=11,
            zorder=3, fontweight='bold',
            bbox=dict(
                edgecolor=accent_color, facecolor=background_color,
                boxstyle="round,pad=0.2", lw=1, alpha=0.8
            )
        )
    )
    # Set background color
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    # Add title
    fig.text(
        0.515, 0.98, f"{player_data['Player']} - {player_data['Team_x']}", size=18,
        ha="center", color=highlight_color, fontweight='bold'
    )
    # Add subtitle
    fig.text(
        0.515, 0.94,
        f" ┆ Percentile Rank vs Botola Pro {pos[position_group]} | Season 2023-24 ┆",
        size=14,
        ha="center", color=text_color
    )
    # Add image
    ax_image = add_image(
        output, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
    )
    # Add rectangles for slice categories
    if position_group != 'GK':
        fig.text(
            0.99, 0.005, f"Attacking\nPossession\nDefending", size=14,
            color=text_color,
            ha="center"
        )
        fig.patches.extend([
            plt.Rectangle(
                (0.89, 0.06), 0.025, 0.021, fill=True, color="#11C9AF",
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.89, 0.03), 0.025, 0.021, fill=True, color="#FFA500",
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.89, 0.00), 0.025, 0.021, fill=True, color="#d70232",
                transform=fig.transFigure, figure=fig
            ),
        ])
    return fig

@f.st.cache_data
def heatmap(df, player_name):
    player_df = df[df['Player'] == player_name]
    # Set up the pitch
    pitch = Pitch(pitch_type='opta',
                  pitch_color='#0f0c2b',#22312b
                  line_color='#c7d5cc',#c7d5cc
                  corner_arcs=True,
                  line_zorder=2,
                  )
    fig, ax = pitch.draw(figsize=(8, 6), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#0f0c2b')#22312b
    fig.patch.set_edgecolor('#FFA500')
    fig.patch.set_linewidth(2)

    pitch.kdeplot(player_df['x'], player_df['y'], ax=ax,
                  cmap='magma',#magma
                  fill=True,
                  n_levels=10,
                  zorder=1,
                  shade_lowest=True,
                  bw_adjust=0.3,
                 )
    plt.tight_layout(pad=0)
    return fig  

@f.st.cache_data
def display_stat(label, value, df, stat):
    
    reverse_stats = ['goalsConceded', 'errorLeadToShot', 'dribbledPast', 'offsides', 'scoringFrequency']
    color = f.get_color_category(value, df, stat, reverse_stats)
    min_value = df[stat].min()
    max_value = df[stat].max()
    percentage = ((value - min_value) / (max_value - min_value)) * 100
    if percentage == 0:
        percentage = 2
        if stat in reverse_stats:
            color = '#00ff1d'
        else:
            color = '#fe003e'
    if isinstance(value, float):
        value = f"{value:.2f}"
    else:
        value = str(value)
    if value == '0' or value == 'nan':
        percentage = 0
        if value == 'nan':
            value = '--- '

    f.st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
            <span style="color: #F5F5F5;">{label}</span>
            <span style="color: #F5F5F5;">{value + " min" if label == 'Scoring Frequency' else value}</span>
        </div>
        <div style="background-color: #F5F5F5; height: 5px; width: 100%; margin-bottom: 15px;">
            <div style="background-color: {color}; height: 100%; width: {percentage}%;"></div>
        </div>
    """, unsafe_allow_html=True)

@f.st.cache_data
def beeswarmplot(players_df, player_data, stat):
    defend_positions = [
        'Defender', 'Right-Back', 'Centre-Back', 'Left-Back'
    ]
    midfield_positions = [
        'Right Midfield', 'Left Midfield', 'Midfielder',
        'Central Midfield', 'Defensive Midfield', 'Attacking Midfield'
    ]   
    forward_positions = [
        'Striker', 'Second Striker', 'Forward',
        'Left Winger', 'Right Winger', 'Centre-Forward'
    ]
    goalkeepers = players_df[players_df['Position'] == 'Goalkeeper']
    defenders = players_df[players_df['Position'].isin(defend_positions)]
    midfielders = players_df[players_df['Position'].isin(midfield_positions)]
    forwards = players_df[players_df['Position'].isin(forward_positions)]
    
    position = player_data['Position']
    #set default colors
    text_color = '#FFFFFF'
    background = '#0c1421'
    
    if position == 'Goalkeeper':
        df = goalkeepers.copy()
        pos = 'Goalkeepers'
    elif position in defend_positions:
        df = defenders.copy()
        pos = 'Defenders'
    elif position in midfield_positions:
        df = midfielders.copy()
        pos = 'Midfielders'
    elif position in forward_positions:
        df = forwards.copy()
        pos = 'Forwards'
    
    # Remove players with played less than 900 min
    df['minutesPlayed'] = df['minutesPlayed'].replace('-', np.nan)
    df['90s'] = (df['minutesPlayed'] / 90).round(1)
    df = df[df['90s'] >= 10]
    # Remove players with 0 value for the stat
    df = df[df[stat] > 0]
    
    # Calculate quartiles
    q1, q2, q3 = df[stat].quantile([0.25, 0.5, 0.75])
    
    # Create color categories
    df['color_category'] = pd.cut(df[stat], 
                                  bins=[-np.inf, q1, q2, q3, np.inf], 
                                  labels=['Bottom 25%', '25-50%', '50-75%', 'Top 25%'])


    fig, ax = plt.subplots(figsize=(6,4))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #fig.patch.set_edgecolor('#FFA500')
    #fig.patch.set_linewidth(2)

    #set up our base layer
    mpl.rcParams['xtick.color'] = text_color
    mpl.rcParams['ytick.color'] = text_color

    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)

    reverse_stats = ['goalsConceded', 'errorLeadToShot', 'dribbledPast', 'offsides', 'scoringFrequency']
    if stat in reverse_stats:
        custom_palette={'Bottom 25%': '#00ff1d', '25-50%': '#ffef01', '50-75%': '#ffa500', 'Top 25%': '#fe003e'}
    else:
        custom_palette={'Bottom 25%': '#fe003e', '25-50%': '#ffa500', '50-75%': '#ffef01', 'Top 25%': '#00ff1d'}

    sns.swarmplot(x=stat, data=df, 
                  hue='color_category',
                  palette=custom_palette,
                  size=15, zorder=1,
                  legend=False)

    # Remove the legend if you don't need it
    #plt.legend([],[], frameon=False)

    # Set x-axis ticks based on data range
    x_min = df[stat].min()
    x_max = df[stat].max()
    x_range = x_max - x_min
    
    if x_range <= 30:
        step = 2
    elif x_range <= 50:
        step = 5
    elif x_range <= 100:
        step = 10
    else:
        step = 20
    
    x_ticks = np.arange(np.floor(x_min), np.ceil(x_max) + step, step)
    plt.xticks(x_ticks)

    #plot player
    if player_data['Player'] in df['Player'].values:
        value = df.loc[df['Player'] == player_data['Player'], stat].values[0]
        plt.scatter(x=value,y=0,c=text_color,s=250,zorder=2)
    
    title_text = f"Distribution of {stat} Among Botola Pro {pos}"
    # Get a cursive font
    cursive_fonts = [f for f in fm.fontManager.ttflist if 'cursive' in f.name.lower()]
    if cursive_fonts:
        cursive_font = cursive_fonts[0].fname
    else:
        cursive_font = 'Arial'  # Fallback to Arial if no cursive font is found

    ax.text(0.5, 0.93, title_text, 
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=12,
            fontfamily='cursive',
            fontweight='bold',
            color='white',
            wrap=True)

    plt.xlabel(stat,c=text_color)
    #plt.tight_layout(pad=-0.5)
    return fig  

@f.st.cache_data
def player_radar_chart(player_name, metrics, values, avg_values):
    # Ensure values are integers
    numeric_values = [int(v) for v in values if str(v).isdigit()]
    numeric_avg_values = [int(v) for v in avg_values if str(v).isdigit()]
    
    if not numeric_values or not numeric_avg_values:
        print("Error: No valid integer values provided.")
        return

    # Ensure the first value is repeated at the end to close the polygon
    values_plot = numeric_values + [numeric_values[0]]
    avg_values_plot = numeric_avg_values + [numeric_avg_values[0]]
    metrics_plot = metrics + [metrics[0]]
    
    # Create the trace for the average values
    avg_trace = go.Scatterpolar(
        r=avg_values_plot,
        theta=metrics_plot,
        name='GK Average',
        line=dict(color='#FFA500', width=2),
        hoverinfo='text',
        text=[f'GK Average {metric}: {value}' for metric, value in zip(metrics, numeric_avg_values)] + [f'GK Average {metrics[0]}: {numeric_avg_values[0]}']
    )

    # Create the trace for the player
    player_trace = go.Scatterpolar(
        r=values_plot,
        theta=metrics_plot,
        fill='toself',
        name=player_name,
        fillcolor='rgba(17, 201, 175, 0.5)',  # Semi-transparent fill
        line=dict(color='#11C9AF', width=2),
        hoverinfo='text',
        text=[f'{player_name} {metric}: {value}' for metric, value in zip(metrics, numeric_values)] + [f'{player_name} {metrics[0]}: {numeric_values[0]}']
    )
    
    # Create the layout
    grid_color = '#BDD0DA'
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 70],
                color='white',
                gridcolor=grid_color,
                tickfont=dict(size=13),  # Increased tick font size
                tickmode='array',
                tickvals=[0, 10, 20, 30, 40, 50, 60, 70],
            ),
            angularaxis=dict(
                gridcolor=grid_color,
                linecolor='white',
                tickfont=dict(color='white', size=14)  # Increased angular tick font size
            ),
            bgcolor='#0c1421'
        ),
        showlegend=True,
        legend=dict(font=dict(color='white', size=14), bgcolor='rgba(51, 255, 138)'),  # Increased legend font size
        width=600,
        height=500,
        paper_bgcolor='#0c1421',
        plot_bgcolor='#0c1421',
        font=dict(color='white', size=14)  # Increased global font size
    )

    # Create the figure and display it
    fig = go.Figure(data=[player_trace, avg_trace], layout=layout)
    
    # Update the radial axis to ensure consistent scaling
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, 70],
                tickmode='array',
                tickvals=[0, 10, 20, 30, 40, 50, 60, 70],
                ticktext=['0', '10', '20', '30', '40', '50', '60', '70']
            )
        )
    )
    
    f.st.plotly_chart(fig, use_container_width=True)

@f.st.cache_data
def shotmap(df, player):
    df_goal = df[(df["shotType"] == "goal") & (df["player_name"] == player)].copy()
    df_miss = df[(df["shotType"] == "miss") & (df["player_name"] == player)].copy()    
    df_save = df[(df["shotType"] == "save") & (df["player_name"] == player)].copy()    
    df_block = df[(df["shotType"] == "block") & (df["player_name"] == player)].copy()    
    df_post = df[(df["shotType"] == "post") & (df["player_name"] == player)].copy()   
    # Set up the pitch
    pitch = VerticalPitch(pitch_type='opta',
                    pitch_color='#0c1421',#22312b
                    line_color='#c7d5cc',#c7d5cc
                    corner_arcs=True,
                    #line_zorder=5,
                    half=True
                    )
    fig, ax = pitch.draw(figsize=(8, 6))
    fig.set_facecolor('#22312b')#22312b
    fig.patch.set_edgecolor('#FFA500')
    fig.patch.set_linewidth(2)

    #  goals:
    sc_g = pitch.scatter(df_goal["new_x"],
                             df_goal["new_y"],
                             marker='football',
                             #s=50,
                             s=df_goal["xg"]*500+100,
                             ax=ax,
                             label="Goals",
                             zorder=4)
    # missed
    sc_m = pitch.scatter(df_miss["new_x"],
                              df_miss["new_y"],
                              c='red',
                              #s=100,
                              s=df_miss["xg"]*500+100,
                              ax=ax,
                             label="Missed",
                             zorder=1)
    # saved
    sc_s = pitch.scatter(df_save["new_x"],
                              df_save["new_y"],
                              c='yellow',
                              #s=100,
                              s=df_save["xg"]*500+100,
                              ax=ax,
                             label="Saved",
                             zorder=3)
    # blocked
    sc_b = pitch.scatter(df_block["new_x"],
                              df_block["new_y"],
                              c='#2463AD',
                              #s=100,
                              s=df_block["xg"]*500+100,
                              ax=ax,
                             label="Blocked",
                             zorder=2)
    # post
    sc_p = pitch.scatter(df_post["new_x"],
                              df_post["new_y"],
                              c='#1C8714',
                              #s=100,
                              s=df_post["xg"]*500+100,
                              ax=ax,
                             label="Post",
                             zorder=2)

    ax.legend(loc='lower left', bbox_to_anchor=(0.05, 0.05), ncol=2, fontsize=10.2, frameon=True, edgecolor='black', markerscale=0.8)
    plt.tight_layout(pad=0)
    return fig

@f.st.cache_data
def pizza_plot_comparison(params_1, values, values_2, player_data, player_name_2, output, output2):
    position_group = f.get_position_group(player_data['Position'])
    # Color palette
    background_color = "#0c1421"  # Dark blue background
    text_color = "#E0E0E0"  # Light gray for most text
    highlight_color = "#FFD700"  # Gold for important text/numbers
    # Player colors
    player1_color = "#11C9AF"  # Turquoise for player 1
    player2_color = "#FFA500"  # Orange for player 2
    params_offset = []
    for v1, v2 in zip(values, values_2):
        distance = abs(v1 - v2)
        params_offset.append(distance < 10)
    # instantiate PyPizza class
    baker = PyPizza(
        params=params_1,
        straight_line_color="#2A3F5F",  # Slightly lighter than background for subtle lines
        straight_line_lw=1,
        last_circle_color="#4A6491",  # Highlighted outer circle
        last_circle_lw=2,
        other_circle_color="#2A3F5F",  # Same as straight lines
        other_circle_lw=1,
        other_circle_ls="-.",
        inner_circle_size=20
    )
    # plot pizza
    fig, ax = baker.make_pizza(
        values,                     # list of values
        compare_values=values_2,    # comparison values
        figsize=(8, 8),             # adjust figsize according to your need
        blank_alpha=0.4,
        kwargs_slices=dict(
            facecolor=player1_color, edgecolor="#FFFFFF", zorder=2, linewidth=1, alpha=1
        ),
        kwargs_compare=dict(
            facecolor=player2_color, edgecolor="#FFFFFF", zorder=2, linewidth=1, alpha=1
        ),
        kwargs_params=dict(
            color=text_color, fontsize=11,
            va="center", fontweight='bold'
        ),
        kwargs_values=dict(
            color='#000000', fontsize=11,
            zorder=3, fontweight='bold',
            bbox=dict(
                edgecolor='#000000', facecolor=player1_color,
                boxstyle="round,pad=0.2", lw=1, alpha=0.8
            )
        ),
        kwargs_compare_values=dict(
            color='#000000', fontsize=11, zorder=3, fontweight='bold',
            bbox=dict(
                edgecolor='#000000', facecolor=player2_color,
                boxstyle="round,pad=0.2", lw=1, alpha=0.8
            )
        )
    )
    # Set background color
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    # adjust text for comparison-values-text
    baker.adjust_texts(params_offset, offset=-0.17, adj_comp_values=True)
    # add title
    fig_text(
        0.515, 1.01, f"<{player_data['Player']}> vs <{player_name_2}>", size=17, fig=fig,
        highlight_textprops=[{"color": player1_color}, {"color": player2_color}],
        ha="center", color=text_color, fontweight='bold'
    )
    # Add subtitle
    fig.text(
        0.515, 0.94,
        f" ┆ Percentile Rank vs Botola Pro {pos[position_group]} | Season 2023-24 ┆",
        size=14,
        ha="center", color=text_color
    )
    # Add player images and names
    # Player 1
    add_image(
        output, fig, left=-0.03, bottom=0.9, width=0.13, height=0.13
    )
    # Player 2
    add_image(
        output2, fig, left=0.95, bottom=0.9, width=0.13, height=0.13
    )
    return fig

def player_details(df, player_data):
    heatmap_df = pd.read_csv('Botola-Scout\dataset botola foot\Botola Players HeatMaps.csv')
    shotmap_df = pd.read_csv('Botola-Scout\dataset botola foot\Botola Players ShotMaps.csv')
    spaces = '&nbsp;'
    f.st.set_option('deprecation.showPyplotGlobalUse', False)
    f.st.markdown("""
    <style>
    .colored-line {
        height: 3px;
        width: 1370px;
        background: linear-gradient(to right, #11C9AF, #FFA500, #9b59b6);
        margin: -10px 0;
    }
    .title {
        font-family:cursive;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        background-color: #082630;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #11C9AF;
    }
    </style>
    """, unsafe_allow_html=True)
    col1, col2 = f.st.columns((1,8))
    with col1:
        lottie_animation = load_lottieurl("https://lottie.host/a79be04b-d18c-4f2b-8341-9bd28d0ab5d5/ke10ceU8Pg.json")
        st_lottie(lottie_animation, loop=False, height=150, width=150, speed=1)
    with col2:
        add_vertical_space(1)
        #f.st.title('Pape Badji Stats for Moghreb Tetouan 2023/24')
        f.st.markdown(f"<p class='title'>{player_data['Player']} Stats for {player_data['Team_x']} 2023/24</p>", unsafe_allow_html=True)
 
    f.st.markdown('<div class="colored-line"></div>', unsafe_allow_html=True)

    col1, col2 = f.st.columns(2)
    with col1:
        f.st.markdown("<h1><span style='color:#FFA500; font-size:40px; font-family:cursive'>Player Profile </span></h1>", unsafe_allow_html=True)
        display_player_card(player_data)
    with col2:
        add_vertical_space(5)
        f.st.markdown(f"<h1>{spaces*3}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Season HeatMap </span></h1>", unsafe_allow_html=True)
        fig = heatmap(heatmap_df, player_data['Player'])
        f.st.pyplot(fig, bbox_inches='tight', pad_inches=0.00, use_container_width=True)

    col1, col2 = f.st.columns(2)
    with col1:
        add_vertical_space(4)
        f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Key Stats </span></h1>", unsafe_allow_html=True)
        add_vertical_space(4)
        position_group = f.get_position_group(player_data['Position'])
        if position_group:
            # Get the stats for the position group
            key_stats = d.stats_mapping[position_group]
        stats_df = df[df['Position'].isin(d.position_mapping[position_group])]
        # Remove players with played less than 900 min
        stats_df['minutesPlayed'] = stats_df['minutesPlayed'].replace('-', np.nan)
        stats_df['90s'] = (stats_df['minutesPlayed'] / 90).round(1)
        if player_data['minutesPlayed'] >= 900:
            stats_df = stats_df[stats_df['90s'] >= 10]
        
        midpoint = math.ceil(len(key_stats) / 2)
        col01,col02 = f.st.columns(2)
        # Display stats in two columns
        for i, stat in enumerate(key_stats):
            stats_df[stat] = stats_df[stat].replace('-', np.nan)
            pos_stats_df = stats_df[stats_df[stat] > 0]
            # Choose the column based on the index
            with col01 if i < midpoint else col02:
                stat_name = f.convert_to_readable(stat)
                display_stat(stat_name, player_data[stat], pos_stats_df, stat)

    with col2:
        add_vertical_space(1)
        f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Key Stats Distribution</span></h1>", unsafe_allow_html=True)
    

        stat = f.st.selectbox(
            label='  ╰┈➤ Select a Stat : ❗(For Players who Played >= 900 mins)',
            options=key_stats,
            index=0,
            format_func=f.convert_to_readable,
            #label_visibility="collapsed",
        )
        fig = beeswarmplot(df, player_data, stat)
        f.st.pyplot(fig, bbox_inches='tight', pad_inches=0)

    #col1, col2, col3 = f.st.columns((1,2,1))
    col1, col2 = f.st.columns((1,1.2))
    with col1:
        add_vertical_space(2)
        if position_group == 'GK':
            f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Attribute Overview </span></h1>", unsafe_allow_html=True)

            gk_df = pd.read_csv('Botola-Scout\dataset botola foot\GK Attributes.csv')
            params = list(gk_df.columns)
            params = params[2:]
            if player_data['Player'] in gk_df['Player'].values:
                player = gk_df.loc[gk_df['Player']==player_data['Player']].reset_index()
                player = list(player.loc[0])
                values = player[3:]
            else:
                values = [0,0,0,0,0]
            avg_values = [53, 64, 47, 63, 61]
            player_radar_chart(player_data['Player'], params, values, avg_values)
        else:
            f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Season ShotMap </span></h1>", unsafe_allow_html=True)
            add_vertical_space(1)
            fig = shotmap(shotmap_df, player_data['Player'])
            f.st.pyplot(fig, bbox_inches='tight', pad_inches=0)
    
    with col2:
        add_vertical_space(2)
        f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:30px; font-family:cursive'>╰┈➤ Compare with other {pos[position_group]}: </span></h1>", unsafe_allow_html=True)
        col01,col02 = f.st.columns(2)
        with col01:
            add_vertical_space(1)
            clubs = df['Team_x'].unique()
            clubs = np.insert(clubs, 0, '- - -')
            team_name_2 = f.st.selectbox(
                label=f'Team :',
                options=clubs,
                index=0,
                #label_visibility="collapsed",
            )
        with col02:
            add_vertical_space(1)
            players_pos_df = df[
                (df['Position'].isin(d.position_mapping[position_group])) &
                (df['Team_x'] == team_name_2) &
                (df['rating'] != '-')]
            players_pos = ['- - -'] + players_pos_df['Player'].tolist()
            player_name_2 = f.st.selectbox(
                label='Player :',
                options=players_pos,
                index=0,
                #label_visibility="collapsed",
            )
        pizza_df = df[df['Position'].isin(d.position_mapping[position_group])]
        params = d.stats_mapping[position_group]
        reverse_stats = ['goalsConceded', 'errorLeadToShot', 'dribbledPast', 'offsides', 'scoringFrequency']
        # Create a new list to store the filtered params
        filtered_params = []
        params_1 = []
        for param in params:
            pizza_df[param] = pizza_df[param].replace('-', 0.0)
            pizza_df[param] = pizza_df[param].replace(np.nan, 0.0)

            if param not in reverse_stats:
                filtered_params.append(param)
                params_1.append(f.convert_to_readable(param))

        player = [player_data[param] for param in filtered_params]
        values = []
        for x in range(len(filtered_params)):   
            values.append(math.floor(stats.percentileofscore(pizza_df[filtered_params[x]],player[x])))
        
        output = f.get_image_output(player_data['Player Image'])
        
        if player_name_2 == '- - -':
            fig = pizza_plot(player_data, params_1, values, output)
            f.st.pyplot(fig, bbox_inches='tight', pad_inches=0)
        else:

            player2_data = df[df['Player'] == player_name_2].iloc[0]
            player2 = [player2_data[param] for param in filtered_params]
            values_2 = []
            for x in range(len(filtered_params)):   
                values_2.append(math.floor(stats.percentileofscore(pizza_df[filtered_params[x]],player2[x])))
            output2 = f.get_image_output(player2_data['Player Image'])
            fig = pizza_plot_comparison(params_1, values, values_2, player_data, player_name_2, output, output2)
            f.st.pyplot(fig, bbox_inches='tight', pad_inches=0)



def player_details(df, player_data):
    heatmap_df = pd.read_csv('Botola-Scout\dataset botola foot\Botola Players HeatMaps.csv')
    shotmap_df = pd.read_csv('Botola-Scout\dataset botola foot\Botola Players ShotMaps.csv')
    spaces = '&nbsp;'
    f.st.set_option('deprecation.showPyplotGlobalUse', False)
    f.st.markdown("""
    <style>
    .colored-line {
        height: 3px;
        width: 1370px;
        background: linear-gradient(to right, #11C9AF, #FFA500, #9b59b6);
        margin: -10px 0;
    }
    .title {
        font-family:cursive;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        background-color: #082630;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #11C9AF;
    }
    </style>
    """, unsafe_allow_html=True)
    col1, col2 = f.st.columns((1,8))
    with col1:
        lottie_animation = load_lottieurl("https://lottie.host/a79be04b-d18c-4f2b-8341-9bd28d0ab5d5/ke10ceU8Pg.json")
        st_lottie(lottie_animation, loop=False, height=150, width=150, speed=1)
    with col2:
        add_vertical_space(1)
        #f.st.title('Pape Badji Stats for Moghreb Tetouan 2023/24')
        f.st.markdown(f"<p class='title'>{player_data['Player']} Stats for {player_data['Team_x']} 2023/24</p>", unsafe_allow_html=True)
 
    f.st.markdown('<div class="colored-line"></div>', unsafe_allow_html=True)

    col1, col2 = f.st.columns(2)
    with col1:
        f.st.markdown("<h1><span style='color:#FFA500; font-size:40px; font-family:cursive'>Player Profile </span></h1>", unsafe_allow_html=True)
        display_player_card(player_data)
    with col2:
        add_vertical_space(5)
        f.st.markdown(f"<h1>{spaces*3}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Season HeatMap </span></h1>", unsafe_allow_html=True)
        fig = heatmap(heatmap_df, player_data['Player'])
        f.st.pyplot(fig, bbox_inches='tight', pad_inches=0.00, use_container_width=True)

    col1, col2 = f.st.columns(2)
    with col1:
        add_vertical_space(4)
        f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Key Stats </span></h1>", unsafe_allow_html=True)
        add_vertical_space(4)
        position_group = f.get_position_group(player_data['Position'])
        if position_group:
            # Get the stats for the position group
            key_stats = d.stats_mapping[position_group]
        stats_df = df[df['Position'].isin(d.position_mapping[position_group])]
        # Remove players with played less than 900 min
        stats_df['minutesPlayed'] = stats_df['minutesPlayed'].replace('-', np.nan)
        stats_df['90s'] = (stats_df['minutesPlayed'] / 90).round(1)
        if player_data['minutesPlayed'] >= 900:
            stats_df = stats_df[stats_df['90s'] >= 10]
        
        midpoint = math.ceil(len(key_stats) / 2)
        col01,col02 = f.st.columns(2)
        # Display stats in two columns
        for i, stat in enumerate(key_stats):
            stats_df[stat] = stats_df[stat].replace('-', np.nan)
            pos_stats_df = stats_df[stats_df[stat] > 0]
            # Choose the column based on the index
            with col01 if i < midpoint else col02:
                stat_name = f.convert_to_readable(stat)
                display_stat(stat_name, player_data[stat], pos_stats_df, stat)

    with col2:
        add_vertical_space(1)
        f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Key Stats Distribution</span></h1>", unsafe_allow_html=True)
    

        stat = f.st.selectbox(
            label='  ╰┈➤ Select a Stat : ❗(For Players who Played >= 900 mins)',
            options=key_stats,
            index=0,
            format_func=f.convert_to_readable,
            #label_visibility="collapsed",
        )
        fig = beeswarmplot(df, player_data, stat)
        f.st.pyplot(fig, bbox_inches='tight', pad_inches=0)

    #col1, col2, col3 = f.st.columns((1,2,1))
    col1, col2 = f.st.columns((1,1.2))
    with col1:
        add_vertical_space(2)
        if position_group == 'GK':
            f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Attribute Overview </span></h1>", unsafe_allow_html=True)

            gk_df = pd.read_csv('Botola-Scout\dataset botola foot\GK Attributes.csv')
            params = list(gk_df.columns)
            params = params[2:]
            if player_data['Player'] in gk_df['Player'].values:
                player = gk_df.loc[gk_df['Player']==player_data['Player']].reset_index()
                player = list(player.loc[0])
                values = player[3:]
            else:
                values = [0,0,0,0,0]
            avg_values = [53, 64, 47, 63, 61]
            player_radar_chart(player_data['Player'], params, values, avg_values)
        else:
            f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:40px; font-family:cursive'>Season ShotMap </span></h1>", unsafe_allow_html=True)
            add_vertical_space(1)
            fig = shotmap(shotmap_df, player_data['Player'])
            f.st.pyplot(fig, bbox_inches='tight', pad_inches=0)
    
    with col2:
        add_vertical_space(2)
        f.st.markdown(f"<h1>{spaces}<span style='color:#FFA500; font-size:30px; font-family:cursive'>╰┈➤ Compare with other {pos[position_group]}: </span></h1>", unsafe_allow_html=True)
        col01,col02 = f.st.columns(2)
        with col01:
            add_vertical_space(1)
            clubs = df['Team_x'].unique()
            clubs = np.insert(clubs, 0, '- - -')
            team_name_2 = f.st.selectbox(
                label=f'Team :',
                options=clubs,
                index=0,
                #label_visibility="collapsed",
            )
        with col02:
            add_vertical_space(1)
            players_pos_df = df[
                (df['Position'].isin(d.position_mapping[position_group])) &
                (df['Team_x'] == team_name_2) &
                (df['rating'] != '-')]
            players_pos = ['- - -'] + players_pos_df['Player'].tolist()
            player_name_2 = f.st.selectbox(
                label='Player :',
                options=players_pos,
                index=0,
                #label_visibility="collapsed",
            )
        pizza_df = df[df['Position'].isin(d.position_mapping[position_group])]
        params = d.stats_mapping[position_group]
        reverse_stats = ['goalsConceded', 'errorLeadToShot', 'dribbledPast', 'offsides', 'scoringFrequency']
        # Create a new list to store the filtered params
        filtered_params = []
        params_1 = []
        for param in params:
            pizza_df[param] = pizza_df[param].replace('-', 0.0)
            pizza_df[param] = pizza_df[param].replace(np.nan, 0.0)

            if param not in reverse_stats:
                filtered_params.append(param)
                params_1.append(f.convert_to_readable(param))

        player = [player_data[param] for param in filtered_params]
        values = []
        for x in range(len(filtered_params)):   
            values.append(math.floor(stats.percentileofscore(pizza_df[filtered_params[x]],player[x])))
        
        output = f.get_image_output(player_data['Player Image'])
        
        if player_name_2 == '- - -':
            fig = pizza_plot(player_data, params_1, values, output)
            f.st.pyplot(fig, bbox_inches='tight', pad_inches=0)
        else:

            player2_data = df[df['Player'] == player_name_2].iloc[0]
            player2 = [player2_data[param] for param in filtered_params]
            values_2 = []
            for x in range(len(filtered_params)):   
                values_2.append(math.floor(stats.percentileofscore(pizza_df[filtered_params[x]],player2[x])))
            output2 = f.get_image_output(player2_data['Player Image'])
            fig = pizza_plot_comparison(params_1, values, values_2, player_data, player_name_2, output, output2)
            f.st.pyplot(fig, bbox_inches='tight', pad_inches=0)