
import turtle

turtle.down()


def draw_triangle():
    """This function draws a triangle."""
    turtle.forward(45)
    turtle.right(120)
    turtle.forward(45)
    turtle.right(120)
    turtle.forward(45)
    turtle.right(120)


def draw_sail():
    """This function draws a sail."""
    turtle.left(90)
    turtle.forward(50)
    turtle.right(150)
    draw_triangle()
    turtle.right(30)


def draw_ship():
    """This function draws a ship."""
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    turtle.left(90)
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    turtle.left(90)
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    turtle.left(90)
    turtle.forward(50)
    turtle.right(120)
    turtle.forward(20)
    turtle.right(60)
    turtle.forward(180)
    turtle.right(60)
    turtle.forward(20)
    turtle.right(30)


def draw_fleet():
    """This draws a fleet of 2 ships."""
    # First ship on the right gets drawn, cursor ends pointing up
    draw_ship()
    # Turning cursor to the left
    turtle.left(90)
    # Turning cursor up, so it won't draw, we don't want a line connecting the two ships.
    turtle.up()
    # Going forward 300 steps to the point where we start drawing the second ship from.
    turtle.forward(300)
    # Turning to the right to start drawing the second ship.
    turtle.right(180)
    # Placing cursor back down, so we can draw the second ship.
    turtle.down()
    # Drawing second ship.
    draw_ship()
    # Turning right after finishing drawing the second ship.
    turtle.right(90)
    # Turning cursor up, so it won't draw, we don't want a line connecting the two ships.
    turtle.up()
    # Going forward 300 steps to the point where we started.
    turtle.forward(300)


if __name__ == "__main__":
    draw_fleet()
    turtle.done()