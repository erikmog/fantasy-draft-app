from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load the existing dataset
df = pd.read_csv('data/players.csv')

# In-memory storage for favorite players
favorites = set()

# API Endpoint for ADP Data
ADP_API_URL = "https://fantasyfootballcalculator.com/api/v1/adp/"

# Global variable to store FFC rankings
ffc_rankings = {}

# Function to scrape rookie details

def scrape_rookie_details():
    url = 'https://www.draftsharks.com/dynasty-rankings/rookies'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table for rookies under the correct class and tag
        rankings_table = soup.find('table', class_='sort-numerical dynasty-rankings')
        rookies = []
        
        if rankings_table:
            rows = rankings_table.find_all('tr', {'data-key': True})  # Main row
            for row in rows:
                # Extract basic data from the main row
                rank = row.find('td', class_='rank-centered').text.strip()
                player_name = row.find('td', class_='player-name').text.strip()
                position_team = row.find('td', class_='position').text.strip()
                
                # Separate position and team
                position, team = position_team.split(' ') if ' ' in position_team else (position_team, "")
                
                # Find additional data
                adp = row.find('td', class_='adp').text.strip()
                bye_week = row.find('td', class_='bye').text.strip()
                
                rookie_data = {
                    'rank': rank,
                    'player_name': player_name,
                    'position': position,
                    'team': team,
                    'adp': adp,
                    'bye_week': bye_week
                }
                
                rookies.append(rookie_data)
        
        return rookies
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

# Route for the home page
@app.route('/')
def index():
    global ffc_rankings  # Use the global variable

    # If FFC data is not yet fetched or cached, fetch it
    if not ffc_rankings:
        response = requests.get(f"{ADP_API_URL}ppr?teams=12&year=2024")
        if response.status_code == 200:
            ffc_data = response.json()['players']
            # Create a dictionary mapping player names to their ranks
            ffc_rankings = {player['name']: i+1 for i, player in enumerate(ffc_data)}

    # Get filter options from the query parameters
    position = request.args.get('position')
    round_num = request.args.get('round')
    
    filtered_df = df.copy()
    if position:
        filtered_df = filtered_df[filtered_df['Position'] == position]
    if round_num:
        filtered_df = filtered_df[filtered_df['Round'] == int(round_num)]
    
    # Add FFC rank to the DataFrame if available
    filtered_df['FFC Rank'] = filtered_df['Player Name'].map(ffc_rankings)

    positions = df['Position'].unique()
    rounds = df['Round'].unique()

    return render_template('index.html', players=filtered_df.to_dict(orient='records'), positions=positions, rounds=rounds)

# Route for the ADP data page
@app.route('/adp')
def adp_view():
    # Retrieve parameters for API call
    scoring_format = request.args.get('format', 'standard')
    teams = request.args.get('teams', 12)
    year = request.args.get('year', 2024)
    position = request.args.get('position', '')

    # Make API call to Fantasy Football Calculator
    response = requests.get(f"{ADP_API_URL}{scoring_format}?teams={teams}&year={year}&position={position}")
    
    if response.status_code == 200:
        adp_data = response.json()['players']
        # Assign ranks manually since the API does not provide it
        for i, player in enumerate(adp_data, start=1):
            player['rank'] = i
    else:
        adp_data = []

    return render_template('adp.html', players=adp_data, format=scoring_format, teams=teams, year=year, position=position)

# Route for the favorites page
@app.route('/favorites')
def favorites_view():
    fav_df = df.loc[list(favorites)]
    return render_template('favorites.html', favorites=fav_df.to_dict(orient='records'))

# Route for the rookie details page
@app.route('/rookies')
def rookies_view():
    # Scrape the rookie details
    rookies = scrape_rookie_details()
    
    # Render the rookie data in a template
    return render_template('rookies.html', rookies=rookies)

# Route to toggle favorite players
@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    player_id = int(request.form.get('player_id'))
    
    if player_id in favorites:
        favorites.remove(player_id)
        return jsonify({'status': 'removed'})
    else:
        favorites.add(player_id)
        return jsonify({'status': 'added'})

if __name__ == '__main__':
    app.run(debug=True)
