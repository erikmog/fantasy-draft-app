import requests
from bs4 import BeautifulSoup

def scrape_fantasypros_rankings():
    url = 'https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php'  # Replace with the correct URL
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser') 
        
        # Find the rankings table
        table = soup.find('table', id='ranking-table')
        players = []
        
        if table:
            rows = table.find_all('tr', class_='player-row')
            
            for row in rows:
                rank = row.find('td', class_='sticky-cell sticky-cell-one').text.strip()
                player_name = row.find('a', class_='player-cell-name').text.strip()
                team = row.find('span', class_='player-cell-team').text.strip()
                
                player_data = {
                    'rank': rank,
                    'player_name': player_name,
                    'team': team
                }
                
                players.append(player_data)
        
        return players
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

# Testing locally
if __name__ == "__main__":
    rankings = scrape_fantasypros_rankings()
    print("Testing")
    for player in rankings:
        print(player)
