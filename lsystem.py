import turtle

def derivation(axiom, steps):
    derived = [axiom] # seed
    for i in range(steps):
        next_seq = derived[-1]
        next_axiom = [rules(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived

def rules(sequence):
    if sequence == "F":
        return "F+F-F-F+F"
    else:
        return sequence

def draw_l_system(turtle, rules, seg_length, angle):
    for rule in rules:
        turtle.pd()
        if rule == "F":
            turtle.forward(seg_length)
        elif rule == "f":
            turtle.pu() # pen up - not drawing
            turtle.forward(seg_length)
        elif rule == "+":
            turtle.left(angle)
        elif rule == "-":
            turtle.right(angle)

def main():
    t = turtle.Turtle() # turtle
    ts = turtle.Screen() # create graphics window
    t.pu()
    t.back(300)
    t.speed(100)
    t.setheading(90)
    model = derivation("-F", 4)
    draw_l_system(t, model[-1], 5, 90) # draw model
    ts.exitonclick()

if __name__ == "__main__":
    main()