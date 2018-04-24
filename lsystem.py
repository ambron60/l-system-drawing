import turtle


def derivation(axiom, steps):
    derived = [axiom]  # seed
    for i in range(steps):
        next_seq = derived[-1]
        next_axiom = [rules(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def rules(sequence):
    if sequence == "F":
        return "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF"  # quad_combo
    elif sequence == "f":
        return "ffffff"
    else:
        return sequence


def draw_l_system(turtle, rules, seg_length, angle):
    for rule in rules:
        turtle.pd()
        if rule == "F":
            turtle.forward(seg_length)
        elif rule == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif rule == "+":
            turtle.left(angle)
        elif rule == "-":
            turtle.right(angle)


def set_turtle():
    global t, ts
    t = turtle.Turtle()  # turtle
    ts = turtle.Screen()  # create graphics window
    t.pu()
    t.back(0)
    t.speed(100)
    t.setheading(90)


def quad_snowflake_curve():
    # A quadratic modification of the snowflake curve
    model = derivation("-F", 4)
    draw_l_system(t, model[-1], 5, 90)  # draw model


def quad_koch_island():
    # Quadratic Kock island
    model = derivation("F-F-F-F", 2)
    draw_l_system(t, model[-1], 5, 90)


def quad_combo():
    # Combination of islands and lakes
    model = derivation("F+F+F+F", 2)
    draw_l_system(t, model[-1], 5, 90)

def main():
    set_turtle()
    quad_combo()
    ts.exitonclick()


if __name__ == "__main__":
    main()
