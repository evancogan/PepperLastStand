# Evan Cogan

# Pepper's Last Stand — a text-based adventure.
# Collect 6 food items to avoid having to eat Mr. Broccoli.


def show_instructions():
    # Print the main menu and available commands
    print("Pepper's Last Stand (A Text-Adventure Game)")
    print("Collect 6 food items to win the game, or be forced to eat Mr. Broccoli.")
    print()
    print("Commands:")
    print("  Movement: north / south / east / west (or n, s, e, w)")
    print("  Get an item: get <item name>   (quotes optional)")
    print("  Check adjacent rooms: check  (or c)")
    print("  Show status: status")
    print("  Help: help")
    print("  Quit: quit")
    print()

def show_status(current_room, inventory, rooms):
    """Show the player's current room, inventory, and any item in the room."""
    print(f"\nYou are in the {current_room}.")
    if inventory:
        print("Inventory: " + ", ".join(inventory))
    else:
        print("Inventory: empty")

    # Number of collected items
    item_count = len(inventory)
    print(f"You have {item_count} of 6 items. Keep going!")

    # Show item(s) in the current room, if any
    room_items = rooms.get(current_room, {}).get('item', [])
    if room_items:
        print("You see here: " + ", ".join(room_items))

    # Hint when player has all items but not yet in Kitchen
    if item_count == 6 and current_room != 'Kitchen':
        print("You have all 6 items! Head to the Kitchen to finish the game.")
    print("-" * 30)

def show_check(current_room, rooms):

    # Show the rooms adjacent to the current room.
    # Prints the direction and the room name for each available move.

    entries = rooms.get(current_room, {})
    # Exclude the 'item' key and show moves
    moves = [(direction, destination) for direction, destination in entries.items() if direction.lower() != 'item']
    if moves:
        print("Rooms around you:")
        for direction, destination in moves:
            print(f"  {direction}: {destination}")
    else:
        print("There are no adjacent rooms.")
    # Show items as well
    items = entries.get('item', [])
    if items:
        print("You see here: " + ", ".join(items))

def check_kitchen_and_end(current_room, inventory):
    # Check if entering Kitchen ends the game.
    # Return a tuple (is_game_over: bool, message: str or None).
    if current_room == 'Kitchen':
        if len(inventory) == 6:
            return True, ("Congratulations! You've collected all 6 food items and reached the Kitchen safely. You win!\n"
                          "Thanks for playing the game. Hope you enjoyed it.")
        else:
            return True, ("Oh no! You've reached the Kitchen without collecting all 6 food items. "
                          "Mr. Broccoli is going to get you!! GAME OVER!\n"
                          "Thanks for playing the game. Hope you enjoyed it.")
    return False, None

def normalize_item_name(raw_item):
    
    # Normalize an item name typed by the player to match stored item names.
    # Basic approach: strip quotes, collapse whitespace, and title-case words.
    
    raw = raw_item.strip()
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        raw = raw[1:-1].strip()
    # Title-case works for the simple two-word items used here (e.g., 'Millet Seed')
    return " ".join(part.capitalize() for part in raw.split())

def main():

    # Rooms dictionary: direction keys map to neighbor room names.
    rooms = {
        'Foyer':       {'East': 'Living Room', 'item': []},
        'Living Room': {'West': 'Foyer', 'East': 'Spare Room', 'North': 'Movie Room', 'South': 'Garage', 'item': ['Millet Seed']},
        'Spare Room':  {'West': 'Living Room', 'North': 'Bathroom', 'item': ['Sunflower Seed']},
        'Movie Room':  {'South': 'Living Room', 'East': 'Kitchen', 'item': ['Pretzel']},
        'Kitchen':     {'West': 'Movie Room', 'item': []},  # Kitchen is the end (villain/location)
        'Bathroom':    {'South': 'Spare Room', 'item': ['Cracker']},
        'Garage':      {'North': 'Living Room', 'East': 'Bedroom', 'item': ['Chip']},
        'Bedroom':     {'West': 'Garage', 'item': ['Pellet']}
    }

    # Initial game state
    current_room = 'Foyer'
    inventory = []
    starting_turn = True

    # Welcome message once
    if starting_turn:
        print("Welcome to Pepper's Last Stand! Your goal is to collect 6 food items scattered around the house to avoid having to eat Mr. Broccoli.")
        print("Type 'help' for commands.\n")
        starting_turn = False

    # Main gameplay loop
    while True:
        # Show status each turn
        show_status(current_room, inventory, rooms)

        # Prompt the player
        user_input = input("Enter your move: ").strip()
        if not user_input:
            print("Please enter a command. Type 'help' for a list of commands.")
            continue

        lower_input = user_input.lower()

        # Help
        if lower_input == 'help':
            show_instructions()
            continue

        # Status
        if lower_input == 'status':
            show_status(current_room, inventory, rooms)
            continue

        # Quit
        if lower_input == 'quit':
            print("Thanks for playing. Goodbye!")
            break

        # Short commands and direction aliases
        dir_map = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West'}
        if lower_input in dir_map:
            direction = dir_map[lower_input]
            if direction in rooms.get(current_room, {}):
                current_room = rooms[current_room][direction]
                game_over, message = check_kitchen_and_end(current_room, inventory)
                if game_over:
                    print(message)
                    break
            else:
                print("You can't go that way.")
            continue

        # Full-word directions (e.g., "north" or "go north")
        tokens = lower_input.split()
        if tokens[0] == 'go' and len(tokens) > 1:
            # Accept commands like "go north"
            candidate = tokens[1].capitalize()
            if candidate in rooms.get(current_room, {}):
                current_room = rooms[current_room][candidate]
                game_over, message = check_kitchen_and_end(current_room, inventory)
                if game_over:
                    print(message)
                    break
            else:
                print("You can't go that way.")
            continue
        # Direct full-word direction without 'go' (e.g., "north")
        if lower_input in ('north', 'south', 'east', 'west'):
            direction = lower_input.capitalize()
            if direction in rooms.get(current_room, {}):
                current_room = rooms[current_room][direction]
                game_over, message = check_kitchen_and_end(current_room, inventory)
                if game_over:
                    print(message)
                    break
            else:
                print("You can't go that way.")
            continue

        # Check adjacent rooms
        if lower_input == 'check' or lower_input == 'c':
            show_check(current_room, rooms)
            continue

        # Scream (nostalgic fun command)
        if lower_input == 'scream':
            print("You scream at the top of your lungs. That was cathartic!")
            continue

        # Get / pick up an item
        if lower_input.startswith('get'):
            # Split into verb + rest of line
            parts = user_input.split(None, 1)  # preserve original casing for item parsing
            if len(parts) == 1:
                print("Get what? Please include an item name after 'get'.")
                continue
            raw_item = parts[1]
            item = normalize_item_name(raw_item)
            room_items = rooms[current_room].get('item', [])
            if item in room_items:
                inventory.append(item)
                room_items.remove(item)
                print(f"You picked up the {item}.")
                if len(inventory) == 6:
                    print("Nice! That's all 6 items — go to the Kitchen to win the game.")
            else:
                print(f"There is no {item} here.")
            continue

        # Unknown command
        print("Invalid command. Type 'help' for a list of commands.")

if __name__ == '__main__':
    main()