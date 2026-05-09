import csv

def load_csv(filename):
    with open(filename, newline='') as csvfile:  
        csv_reader = csv.DictReader(csvfile)  #Csv reader that reads rows into dictionaries
        #removes front and back white spaces from column header
        csv_reader.fieldnames = [field.strip() for field in csv_reader.fieldnames]
        return [row for row in csv_reader]  #Return all rows as a list of dictionaries

#load data from csv files
pitchers_data = load_csv('Pitchers.csv')
position_players_data = load_csv('PositionPlayers.csv')


def convert_to_float(data, keys):
    for row in data:  
        for key in keys:  
            if row[key]:  #if the key exists in the row and is not empty
                row[key] = float(row[key])  #convert the value to float
    return data  

#lists of keys to convert to float for pitchers and position players
pitcher_keys = ['Earned Run Average', 'Wins', 'Losses', 'Innings Pitched', 'Strikeouts']
position_player_keys = ['Batting Average', 'Home Runs', 'At Bats']

#convert specified fields to float
pitchers_data = convert_to_float(pitchers_data, pitcher_keys)
position_players_data = convert_to_float(position_players_data, position_player_keys)


def get_stat_for_specific_player(player_name, stat_name, data):
    for row in data:  
        if row['PlayerNames'].strip().lower() == player_name:  #check if the players name matches
            return row.get(stat_name, None)  #return the stat or none if not found
    return None  

def get_all_stats_for_player(player_name, data):
    for row in data:  
        if row['PlayerNames'].strip().lower() == player_name: 
            return row  # return the entire row
    return None 


def player_with_best_stat(data, stat_name):
    best_player = None
    max_stat = float('-inf')  #negative infinity to ensure any stat is higher
    
    # Normalize stat_name for comparison
    stat_name = stat_name.strip().title()

    for row in data:  
        if stat_name in row:  
            value = row[stat_name]  #get the value for the stat
            if value:  #check if the value is not None or empty
                value = float(value)  #convert value to float
                if value > max_stat:  #compare with the current max_stat
                    max_stat = value  #update max_stat if the current value is higher
                    best_player = row['PlayerNames']  #update best_player to the current player
    
    return best_player, max_stat  

def player_with_worst_stat(data, stat_name):
    worst_player = None
    min_stat = float('inf')  #positive infinity to ensure any stat is lower
    
    stat_name = stat_name.strip().title()

    for row in data:  
        if stat_name in row:  
            value = row[stat_name]  
            if value: 
                value = float(value) 
                if value < min_stat:  #compare with the current min_stat
                    min_stat = value  #update min_stat if the current value is lower
                    worst_player = row['PlayerNames']  #update worst_player to the current player
    
    return worst_player, min_stat  #return the player with the worst stat and the stat value


def main():
    while True:  
        print('This is the 2013 Boston Red Sox World Series Winning Roster')
        print('Options:')
        print('1. Get a specific stat for a player')
        print('2. Get all stats for a player')
        print('3. Get the player with the best stats in a category')
        print('4. Get the player with the worst stat in a category')
        print('5. Exit')

        choice = input('Enter your choice: ') 
        if choice == '1':
            player_name = input("Enter player's name: ").strip().lower()  
            stat_name = input('Enter the stat you want to see: ').strip().title()  # title() capiltalizes the first letter of each word
    
            #try to get the stat from the pitchers data
            stat = get_stat_for_specific_player(player_name, stat_name, pitchers_data)
            #if stat isnt found in pitchers data try position players data
            if not stat:
                stat = get_stat_for_specific_player(player_name, stat_name, position_players_data)
            #if stat is found print it out along with the player name
            if stat:
                print(f"{player_name.title()}'s {stat_name}: {stat}")
            else:
                print(f"Stat {stat_name} for player {player_name} not found.")
            
        elif choice == '2':
            player_name = input("Enter player's name: ").strip().lower()  
            stats = get_all_stats_for_player(player_name, pitchers_data)  #try to get all stats from pitchers data
            if not stats:
                stats = get_all_stats_for_player(player_name, position_players_data)  #try to get all stats from position players data
            if stats:
                print(f"{player_name.title()}'s statistics: {stats}")
            else:
                print(f'Player does not exist')
               
        elif choice == '3':
            stat_name = input("Enter stat name: ").strip().title()  
            best_player, best_stat = player_with_best_stat(pitchers_data, stat_name)  #best stat from pitchers data
            if not best_player:
                best_player, best_stat = player_with_best_stat(position_players_data, stat_name)  # best stat from position players data
            
            if best_player:
                print(f"Player with the best {stat_name}: {best_player} with {best_stat}")
            else:
                print(f"Stat {stat_name} not found")
                
        elif choice == '4':
            stat_name = input("Enter stat name: ").strip().title()  
            worst_player, worst_stat = player_with_worst_stat(pitchers_data, stat_name)  #worst stat from pitchers data
            if not worst_player:
                worst_player, worst_stat = player_with_worst_stat(position_players_data, stat_name)  #worst stat from position players data
            
            if worst_player:
                print(f"Player with the worst {stat_name}: {worst_player} with {worst_stat}")
            else:
                print(f"Stat {stat_name} not found")
                
        elif choice == '5':
            break  

        else:
            print('Invalid choice, try again.')  

if __name__ == '__main__':
    main()  
