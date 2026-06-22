import turtle
import pandas

# --- Set up the game screen and the U.S. map background ---
screen = turtle.Screen()
screen.title("U.S States Game")
image = "blank_states_img.gif"
screen.addshape(image)      # Register the map image so turtle can use it as a shape
turtle.shape(image)         # Display the map as the background

#  Found the cordinates with this line of code
# def get_mouse_click(x,y):
#     print(x,y)
# turtle.onscreenclick(get_mouse_click)
# turtle.mainloop()

# --- Game state variables ---
keep_going = True           # Controls the main game loop
correct_answer = 0          # How many states the player has guessed correctly
correct_list = []           # Keeps track of states already guessed (prevents duplicates)

# Load the CSV containing every state's name and its x/y position on the map
data = pandas.read_csv("50_states.csv")

while keep_going:
    # Ask the player to guess a state. The title shows their current score.
    answer_state = screen.textinput(title=f"{correct_answer}/50 States Correct",
                                    prompt="What's another state's name?")

    # Pull out the columns we need from the data
    data_state = data["state"]
    data_x = data["x"]
    data_y = data["y"]

    # If the player types "Exit" or closes the popup (returns None), end the game.
    # Before quitting, save all the states they DIDN'T guess to a CSV to study later.
    if answer_state == "Exit" or answer_state == None:
        missing_states = []
        for state in data_state:
            if state not in correct_list:        # State was never guessed
                missing_states.append(state)
        df = pandas.DataFrame(missing_states)
        df.to_csv("States_to_learn.csv")
        break

    # Capitalize the guess (e.g. "texas" -> "Texas") so matching is case-insensitive
    answer_state = answer_state.title()

    # Check the guess is a real state AND hasn't already been guessed
    if answer_state in data["state"].values and answer_state not in correct_list:
        # Create a hidden turtle to write the state name on the map
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()                                # Don't draw lines while moving

        # Find the row for this state and move to its coordinates
        row = data[data_state == answer_state]
        t.goto(row.x.item(), row.y.item())
        t.write(answer_state)                    # Stamp the state name on the map

        # Record the correct guess and update the score
        correct_list.append(answer_state)
        correct_answer += 1

        # If all 50 states are guessed, end the game
        if len(correct_list) == 50:
            keep_going = False

# Keep the window open until the player clicks to close it
screen.exitonclick()
