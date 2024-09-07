position_mapping = {
    'GK': ['Goalkeeper'],
    'DF': ['Defender', 'Right-Back', 'Centre-Back', 'Left-Back'],
    'MID': ['Right Midfield', 'Left Midfield', 'Midfielder', 'Central Midfield', 'Defensive Midfield', 'Attacking Midfield'],
    'FWD': ['Striker', 'Second Striker', 'Forward', 'Left Winger', 'Right Winger', 'Centre-Forward']
}

stats_mapping = {
    'GK': ['saves', 'aerialDuelsWonPercentage', 'accurateLongBallsPercentage', 'cleanSheet', 'goalsConceded'],
    
    'DF': ['accurateCrossesPercentage','accurateFinalThirdPasses',
          'accuratePassesPercentage','accurateLongBallsPercentage','totalDuelsWonPercentage',
          'ballRecovery',  'interceptions', 'aerialDuelsWonPercentage',   'clearances','blockedShots',
            'errorLeadToShot', 'dribbledPast', ],
    
    'MID': ['goalsAssistsSum','keyPasses','goalConversionPercentage','accurateCrossesPercentage',
           'accuratePassesPercentage',  'accurateFinalThirdPasses',  'successfulDribblesPercentage', 'accurateLongBallsPercentage',
           'ballRecovery',   'aerialDuelsWonPercentage', 'totalDuelsWonPercentage',
            'dribbledPast'],
    
    'FWD':['goalsAssistsSum','shotsOnTarget','goalConversionPercentage','keyPasses', 'accurateCrossesPercentage',
          'successfulDribblesPercentage',  'accurateFinalThirdPasses','accuratePassesPercentage',  'wasFouled',
          'aerialDuelsWonPercentage',
            'offsides', 'scoringFrequency'],
}

exclude_columns = ['Player',
 'Nationality',
 'Team_x',
 'Position',
 'Age',
 'Height',
 'Preferred Foot',
 'Shirt Number',
 'Market Value',
 'Player Image',
 'Team Logo',]  # Columns to exclude from conversion


css="""
    <style>
    body {
        color: white;
        background-color: #daedeb;
    }
    .player-card {
        background-color: #1E2A38;
        border-radius: 15px;
        padding: 25px;
        color: white;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #FFA500;
    }
    .player-header {
        display: flex;
        align-items: center;
        margin-bottom: 25px;
    }
    .player-image {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-right: 25px;
        border: 3px solid #11C9AF;
    }
    .player-info {
        flex-grow: 1;
    }
    .player-name {
        font-family:cursive;
        font-size: 30px;
        font-weight: bold;
        margin: 0;
        color: white;
    }
    .player-team {
        font-size: 18px;
        margin: 5px 0;
        color: white;
    
    }
    .team-logo {
        width: 35px;
        height: 35px;
        margin-right: 10px;
        vertical-align: middle;
    }
    .stats {
        display: flex;
        justify-content: space-between;
        margin-bottom: 25px;
        background-color: #263238;
        border-radius: 10px;
        padding: 15px;
        border: 2px solid #11C9AF;
    }
    .stat {
        text-align: center;
    }
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: white;
    }
    .stat-label {
        font-size: 16px;
        color: #BDD0DA;
    }
    .player-bio {
        display: flex;
        flex-wrap: wrap;
        background-color: #263238;
        border-radius: 10px;
        padding: 15px;
        border: 2px solid #11C9AF;
    }
    .bio-item {
        width: 50%;
        margin-bottom: 12px;
    }
    .bio-label {
        font-weight: bold;
        color: #BDD0DA;
    }
    .bio-value {
        font-size: 18px;
        font-weight: bold;
        color: white;
    }
    h3 {
        color: #FFA500;
        margin-top: 20px;
    }
    """
    
style_img= """
    <style>
    .image-container {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        position: fixed;
        bottom: 0;
        left: 0;
        background-color: white;
        padding: 10px;
        z-index: 10; /* Assure que les logos apparaissent au-dessus de tout */
    }

    .image-track {
        display: inline-block;
        animation: scroll 20s linear infinite;
        height:70px;

    }

    .image-track img {
        display: inline-block;
        width: 100px; /* Ajuster la taille des logos ici */
        height:70px;
        margin-right: 15px;
    }

    @keyframes scroll {
        0% {
            transform: translateX(100%);
        }
        100% {
            transform: translateX(-100%);
        }
    }
    </style>
    """