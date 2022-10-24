"""
Sprite

A class to create a sprite to be displayed on a tkinter canvas
"""
import vector as v

class Sprite:
    def __init__(self, pos, dim):
        """
        Constructor method for Sprite class
        """
        # Set the initial position to the position passed in to the constructor
        self.position = v.vector(pos[0], pos[1])
        # Set the initial velocity to 0 in both axes
        self.velocity = v.vector(0, 0)
        self.dt = 0.05 # Time step

        self.width=dim[0]
        self.height=dim[1]

    def corners(self):
        """
        Method to return the corners of the Sprite's bounding box in a tuple
        
        Corners start from the top left and go clockwise
        """
        c1 = (self.position.x - self.width/2, self.position.y - self.height/2)
        c2 = (self.position.x + self.width/2, self.position.y - self.height/2)
        c3 = (self.position.x + self.width/2, self.position.y + self.height/2)
        c4 = (self.position.x - self.width/2, self.position.y + self.height/2)
        corners = (c1, c2, c3, c4)
        
        return corners
        
    def move(self):
        """
        Method to move the sprite based on its velocity

        Returns a tuple with the difference between the previous position and the current position
        """
        dx = self.velocity * self.dt
        self.position = self.position + dx

        return (dx[0], dx[1])

    def collision(self, other):
        """
        Method to determine whether the objects has collided with another sprite passed in as other
        """
        collided = False

        x_bounds = (other.corners()[0][0]-(self.width/2), other.corners()[2][0]+(self.width/2)) # Tuple containing the max and min x coords of this sprite for it to be in contact with the other
        y_bounds = (other.corners()[0][1]-(self.height/2), other.corners()[2][1]+(self.height/2)) # Tuple containing the max and min y coords of this sprite for it to be in contact with the other
        
        # If the x and y coordinates of this object are within the bounds of the other
        if (self.position.x > x_bounds[0] and self.position.x < x_bounds[1]) and (self.position.y > y_bounds[0] and self.position.y < y_bounds[1]):
            collided = True

        return collided

    def change_position(self, pos):
        """
        Method to snap the sprite to a new position
        
        Returns a tuple containing the difference between the previous position and current position
        """
        dx = self.position - v.vector(pos[0],pos[1])
        self.position = v.vector(pos[0],pos[1])

        return (dx[0], dx[1])

    def change_velocity(self, pos):
        """
        Method to snap the sprite to a new velocity
        """
        self.velocity = v.vector(pos[0],pos[1])
