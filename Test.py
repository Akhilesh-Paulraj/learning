import requests


def print_character_grid(doc_url: str):
    """
    Retrieves data from a Google Doc URL, parses it, and prints a grid
    of characters forming a graphic.

    Args:
        doc_url (str): The URL for the Google Doc containing the character data.
                       This URL should ideally be a "published to web" link
                       that exports as plain text (e.g., .../export?format=txt).
    """
    characters_data = []
    max_x = 0
    max_y = 0

    try:
        # Step 1: Retrieve the content from the URL
        response = requests.get(doc_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        doc_content = response.text

        # Step 2: Parse the data
        lines = doc_content.strip().split('\n')
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace from the line itself
            if not line:  # Skip empty lines
                continue

            parts = line.split(',')
            if len(parts) == 3:
                char = parts[0]
                # Try to convert x and y to integers
                try:
                    x = int(parts[1].strip())  # .strip() removes leading/trailing spaces
                    y = int(parts[2].strip())  # to prevent issues like ' 5'
                except ValueError:
                    print(f"Warning: Skipping line '{line}' - X or Y coordinate is not a valid integer.")
                    continue  # Skip to the next line
                except IndexError:
                    print(f"Warning: Skipping line '{line}' - Not enough parts after splitting.")
                    continue

                characters_data.append({'char': char, 'x': x, 'y': y})

                # Step 3: Determine grid dimensions
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            else:
                print(f"Warning: Skipping malformed line: '{line}' - Expected 'char,x,y' format.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching document from URL: {e}")
        return
    except ValueError as e:
        # This catch-all ValueError might still occur if a problem slips past the inner try-except,
        # but the inner one is more specific.
        print(f"Error parsing content: {e}. Check document format or data types.")
        return
    except IndexError as e:
        # This catch-all IndexError might still occur if a problem slips past the inner try-except.
        print(f"Error processing document lines: {e}. Check delimiter or line structure.")
        return

    # Handle case where no data was parsed after error handling
    if not characters_data:
        print("No valid character data found in the document after parsing.")
        return

    # Step 4: Create the grid structure
    grid_width = max_x + 1
    grid_height = max_y + 1

    # Initialize grid with spaces
    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]

    # Step 5: Populate the grid with characters
    for item in characters_data:
        # y corresponds to row, x corresponds to column in a 2D list
        # Add a check to prevent IndexError if coordinates are out of bounds after max_x/max_y calculation
        if 0 <= item['y'] < grid_height and 0 <= item['x'] < grid_width:
            grid[item['y']][item['x']] = item['char']
        else:
            print(
                f"Warning: Character '{item['char']}' at ({item['x']},{item['y']}) is out of calculated grid bounds. Skipping.")

    # Step 6: Print the final grid
    for row in grid:
        print("".join(row))


# --- Example Usage with the provided URL ---
if __name__ == "__main__":
    doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    print_character_grid(doc_url)