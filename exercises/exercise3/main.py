from taipy.gui import Gui
import taipy.gui.builder as tgb

# the user can input a string and a button to submit the input
# The written string should also be displayed in a text instantaneously. 
# After clicking the submit button, the game displays this GPT4o-generated cat image if it is a palindrome.

user_input = "your palindrome..."
image_path = ""
cat_image = "assets/fake_cat.png"
rabbit_image = "assets/fake_sad_rabbit.png"

def palindrome_check(state):
    if state.user_input == state.user_input[::-1]:
        state.image_path = cat_image
    else:
        state.image_path = rabbit_image


with tgb.Page() as page:
    tgb.text("# The palindrome game", mode = "md")

    tgb.text("Type a word you think is a palindrome")
    tgb.input("{user_input}")
    tgb.button("Send", on_action=palindrome_check)
    
    tgb.text("Your word: {user_input}")
    tgb.image("{image_path}")


if __name__ == '__main__':
    Gui(page).run(dark_mode=False, use_reloader=True, port=8080)