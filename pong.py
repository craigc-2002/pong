"""
Pong
Craig Cochrane 2022

A clone of pong made using tkinter
"""

import tkinter as tk
import random
import sprite
import vector as v

#===============================================================================
#  Ball Class
#===============================================================================
class Ball(sprite.Sprite):
    """
    Class to create a ball
    Child class of Sprite
    """
    def __init__(self, game, pos, dim):
        """
        Constructor method for the Ball class
        """
        super().__init__(pos, dim) # Call the parent class constructor

        self.game = game
        
        self.draw()

    def new_point(self):
        """
        Method to reset the ball for a new point
        """
        self.reposition((self.game.window_width/2,random.randint(0,self.game.window_height)))
        # Give the ball a velocity which is constant in the x direction with random direction and random in the y direction
        v_x = self.game.x_velocity * random.choice((1, -1))
        v_y = (self.game.x_velocity / random.randint(1,10)) * random.choice((1, -1))
        self.change_velocity((v_x, v_y))

    def update(self):
        """
        Method to update the ball by calculating the new position based on speed and moving the ball on the screen
        """
        d_pos = self.move()
        self.game.canvas.move(self.id, d_pos[0], d_pos[1])

    def draw(self):
        """
        Method to draw the ball on the screen
        """
        # Draw the ball on the canvas at the position given by the coordinates of the top left and bottom right corners of the bounding box
        self.id = self.game.canvas.create_oval((self.corners()[0], self.corners()[2]), fill="white")

    def redraw(self):
        """
        Method to redraw the ball in a new position by removing the old ball and redrawing it
        """
        self.game.canvas.delete(self.id)
        self.draw()

    def reposition(self, new_pos):
        """
        Method to instantly move the ball to a new position
        """
        self.change_position(new_pos)
        self.redraw()

    def check_point(self):
        """
        Method to check whether a point has been won by the ball moving off either side of the screen
        """
        if self.position.x > self.game.window_width or self.position.x < 0:
            return True

    def paddle_bounce(self, paddle):
        """
        Method to make the ball bounce off a paddle
        """
        self.change_velocity((self.velocity.x*(-1), (self.velocity.y + paddle.velocity.y)))

    def wall_bounce(self):
        """
        Method to make the ball bounce off a wall
        """
        self.change_velocity((self.velocity.x, self.velocity.y * (-1)))
        
#===============================================================================
#  Paddle Class
#===============================================================================
class Paddle(sprite.Sprite):
    """
    Class to create the paddles
    Child class of Sprite
    """
    def __init__(self, game, pos, dim):
        """
        Constructor method for the Paddle class
        """
        super().__init__(pos, dim) # Call the parent class constructor

        self.game = game
        self.old_pos = v.vector()
        
        self.id = game.canvas.create_rectangle(self.corners()[0][0], self.corners()[0][1], self.corners()[2][0], self.corners()[2][1], fill="white")

    def update(self):
        """
        Method to update the paddle by calculating the new position based on speed and moving the paddle on the screen
        """
        d_pos = self.move()
        self.game.canvas.move(self.id, d_pos[0], d_pos[1])

    def move_paddle(self, event):
        """
        Method to move the paddle when the mouse is moved
        Called by a binding to mouse motion when the game is running
        """
        d_pos = self.change_position((self.position.x, event.y))
        self.game.canvas.move(self.id, d_pos[0], -d_pos[1])
        self.velocity = (self.old_pos - self.position) * self.dt
        self.old_pos = self.position

    def new_point(self):
        """
        Method to return the paddle to the centre when a new point is  started
        """
        d_pos = self.change_position((self.position.x, event.y))
        self.game.canvas.move(self.id, d_pos[0], d_pos[1])
        
#===============================================================================
#  Pong AI Class
#===============================================================================
class Pong_AI:
    """
    Class to create an AI to play against
    """
    def __init__(self, game, paddle, max_speed):
        """
        Constructor method for the Pong AI class
        """
        self.game = game
        self.paddle = paddle

        self.position = paddle.position
        self.max_speed = max_speed
        
    def move_paddle(self):
        """
        Method for the AI to choose a coordinate to aim the paddle to and move it accodingly
        The paddle will be limited to a set speed
        """
        target = self.game.ball.position.y # Aim to move the paddle to the ball's current y coordinate

        if (target - self.position.y) < 0:
            self.paddle.change_velocity((0, -self.max_speed))
        elif (target - self.position.y) > 0:
            self.paddle.change_velocity((0, self.max_speed))
        else:
            self.paddle.change_velocity((0, 0))

        self.paddle.update()
        self.position = self.paddle.position

#===============================================================================
#  Pong Class
#===============================================================================
class Pong:
    """
    Main game class for the pong clone
    """
    def __init__(self):
        """
        Constructor method for the Pong class
        Creates the game window and creates the necessary objects to start the game
        """
        # Create the class variables needed
        self.window_width = 600
        self.window_height = 400

        self.x_velocity = 4 # x velocity for the ball
        
        #Create the game window
        self.root = tk.Tk()
        self.root.geometry("+350+150")
        self.root.title("Pong")
        # Create the canvas to draw the game on
        self.canvas = tk.Canvas(self.root, bg="black", width=self.window_width, height=self.window_height)
        self.canvas.pack()

        # Create the net as a dashed grey line down the middle of the screen
        self.net = self.canvas.create_line(self.window_width/2, 0, self.window_width/2, self.window_height, width=5, dash=(200,255), fill="gray")

        self.scores_player_1 = self.canvas.create_text(150, 70, text="0", fill="black", font=("Helvetica", "25"))
        self.scores_player_2 = self.canvas.create_text(450, 70, text="0", fill="black", font=("Helvetica", "25"))

        self.play_again_text = 0
        
        # Create the game objects for the ball and player
        self.ball = Ball(self, (self.window_width/2, self.window_height/2), (15,15))
        self.player1 = Paddle(self, (40, self.window_height/2), (10,85))
        self.player2 = Paddle(self, (self.window_width - 40, self.window_height/2), (10,85))

        self.max_computer_speed = 1
        self.computer = Pong_AI(self, self.player1, self.max_computer_speed)

        # Call the title page method
        self.title_page()

    def title_page(self):
        """
        Method to draw the elements needed for the title page to the screen
        """
        self.canvas.create_text(300, 100, text="PONG", fill="white", font=("Helvetica", "50"), tags="title")
        self.canvas.create_text(300, 150, text="CLICK THE MOUSE TO START", fill="white", font=("Helvetica", "10"), tags="title")

        self.canvas.bind_all('<Button-1>', self.start_game)

    def start_game(self, event=None):
        """
        Method to start the game loop

        Is bound to the left mouse button on the title screen
        """
        # Remove the title page text
        self.canvas.delete("title")

        self.scores = [0,0] # List containing the two player's scores
        self.update_points()

        self.canvas.unbind_all('<Button-1>')
        self.canvas.bind_all('<Motion>', self.player2.move_paddle)
        
        self.new_point()
        # Call the main game loop method
        self.game_loop()
        
    def game_loop(self):
        """
        Method to contain the main game loop

        Tasks that need done in the loop:
        - Move ball based on velocity
        - Move paddles based on user input
        - Check for collision between the ball and paddles
        - Check for the ball bouncing off the top or bottom of the screen
        - Check for the ball hitting either end of the court
        - Update the score counter
        - Replace the ball in the centre
        - Check to see if the max score has been reached
        """
        done = False

        while done != True:
            self.ball.update()
            self.computer.move_paddle()

            if self.ball.collision(self.player2):
                self.ball.paddle_bounce(self.player2)
            if self.ball.collision(self.player1):
                self.ball.paddle_bounce(self.player1)

            if (self.ball.position.y < 0) or (self.ball.position.y > self.window_height):
                self.ball.wall_bounce()
            
            if self.ball.check_point():
                if self.ball.position.x > 0:
                    self.scores[0] += 1
                else:
                    self.scores[1] += 1
                    
                self.new_point()

            if self.check_win_condition():
                done = True
                self.game_over()
            
            self.root.update() # Update the game window
            
        self.game_over()

    def update_points(self):
        """
        Method to update the points scoreboard
        """
        self.canvas.itemconfigure(self.scores_player_1, text=self.scores[0], fill="white")
        self.canvas.itemconfigure(self.scores_player_2, text=self.scores[1], fill="white")

    def new_point(self):
        """
        Method to reset the game for a new point
        """
        self.update_points()
        self.ball.new_point()
        self.player1.move_paddle(v.vector(40, self.window_height/2))
        self.player2.move_paddle(v.vector(self.window_width - 40, self.window_height/2))

    def check_win_condition(self):
        """
        Method to check whether the game has been won
        Returns a boolean of whether the game is over or not
        """
        if self.scores[0] > 10:
            game_over = True
            self.winner = 1
            
        elif  self.scores[1] > 10:
            game_over = True
            self.winner = 2
            
        else:
            game_over = False

        return game_over

    def game_over(self):
        """
        Method for when the game is finished
        Displays the game over screen
        """
        self.canvas.create_text(300, 100, text="GAME OVER", fill="white", font=("Helvetica", "50"), tags="gameover")
        self.canvas.create_text(300, 380, text="CLICK TO PLAY AGAIN", fill="white", font=("Helvetica", "10"), tags="gameover")

        # Move the final scores
        self.canvas.coords(self.scores_player_1, self.window_width/4, self.window_height*(3/4))
        self.canvas.coords(self.scores_player_2, self.window_width*(3/4), self.window_height*(3/4))

        # Make the text displaying the winner
        winner_text = self.canvas.create_text(0,0, text="".format(self.winner), fill="white", font=("Helvetica", "30"), tags="gameover")
        # Move the text to the correct side
        if self.winner == 1:
            self.canvas.itemconfigure(winner_text, text="COMPUTER\nWINS", justify=tk.RIGHT)
            self.canvas.coords(winner_text, (self.window_width/4)+25, self.window_height/2)
        else:
            self.canvas.itemconfigure(winner_text, text="PLAYER\nWINS")
            self.canvas.coords(winner_text, (self.window_width*(3/4))-25, self.window_height/2)

        self.canvas.unbind_all('<Motion>')
        self.canvas.bind_all('<Button-1>', self.new_game)

    def new_game(self, event):
        """
        Method to start a new game by clearing the game over screen and starting again
        """
        self.canvas.coords(self.scores_player_1, 150, 70)
        self.canvas.coords(self.scores_player_2, 450, 70)
        self.canvas.delete("gameover")
        
        self.start_game()
        
if __name__ == "__main__":
    Pong()
