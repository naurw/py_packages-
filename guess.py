# higher-lower 

## variation of a simple random number & choice 
## framework: 
## 1) home route displays <h1> "Guess a number between 0-19" 
## 2) add a giphy associated with each number 
## 3) generate random number 
## 4) generate a route that can detect the number entered by the user e.g. url/page/<int>
## 5) response if the user input is too low, too high, or spot 


import random 
from flask import Flask, request, redirect, url_for 
from functools import wraps

random_number = random.randint(0,19)
print(random_number) 

# generic html decorator 
## - rewrap the original function since it is wrapped and won't be accessible if not wrapped again to preserve original purpose 
def html_decorator(func): 
    @wraps(func)
    def wrapper(*args, **kwargs): 
        message, message_color, image_url, retry = func(*args, **kwargs)
        # use func to pass along any arguments it receves and expect func to return a tuple which will be packed into 3 variables 
        response =  f"<h1 style='text-align: center'; 'color: {message_color}'>{message}</h1>" \
            f"<div style='text-align: center; margin-top: 20px;'>" \
            f"<img src='{image_url}'/></div>"
        
        if retry: 
            response += f'<div style="text-align: center; margin-top: 20px"><a href="{url_for("home_page")}"><button>Try Again</button></a></div>'

        return response
    return wrapper 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) # same as app.add_url_rule('/', 'home', home_page, methods = ['GET', 'POST'])
def home_page(): 
    if request.method =='POST': 
        guess = request.form['number']
        return redirect(url_for('guess_number', guess = guess))
    
    return '''
        <h1 style="text-align: center">Guess a number between 0 and 19</h1>
        <div style="text-align: center; margin-top: 20px;">
            <form action="/" method="post">
                <input type="number" name="number" min="0" max="19" required>
                <input type="submit" value="Guess!">
            </form>
            <img src="https://media.giphy.com/media/1Z0g3Y5WxKqU7FdHbI/giphy.gif" style="display: block; margin-left: auto; margin-right: auto;">
        </div>
        '''
@app.route("/<int:guess>")
@html_decorator
def guess_number(guess):
    if guess > random_number:
        return ("Too high, try again!", 'purple', "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif", True) # add retry flag
    elif guess < random_number:
        return ("Too low, try again!", 'red', "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif", True) # add retry flag
    else:
        return ("You found me!", 'green', "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif", False) # no retry flag 

if __name__ == '__main__':
    app.run()