import turtle


def derivation(axiom, steps):
    derived = [axiom]  # seed
    for i in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def rule(sequence):
    if sequence in rules:
        return rules[sequence]
    else:
        return sequence


def draw_l_system(turtle, rules, seg_length, angle):
    # global heading, position
    for command in rules:
        turtle.pd()
        if command in ["F", "G", "R", "L"]:
            turtle.forward(seg_length)
        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif command == "+":
            turtle.left(angle)
        elif command == "-":
            turtle.right(angle)
        print(get_turtle_state(turtle))


def set_turtle(alpha_zero):
    global t, ts
    t = turtle.Turtle()  # turtle
    ts = turtle.Screen()  # create graphics window
    ts.screensize(1500, 1500)
    t.screen.bgcolor("black")
    t.color("white")
    t.screen.title("Fractal Curve")
    t.pu()
    # t.back(300) # move the turtle backward by distance, opposite to heading
    t.speed(100)  # adjust as needed
    t.setheading(alpha_zero)  # initial heading


def get_turtle_state(turtle):
    return turtle.position(), turtle.heading()


def main():
    global rules
    rules = dict()
    rule_num = 1
    while True:
        rule = input("Enter rule[%d]:rewrite term (0 when done): " % rule_num)
        if rule == '0':
            break
        key, value = rule.split("->")
        rules[key] = value
        rule_num += 1

    axiom = input("Enter axiom (initial string): ")
    iterations = int(input("Enter number of iterations (n): "))

    model = derivation(axiom, iterations)  # axiom (initial string), nth iterations

    segment_length = int(input("Enter step size (segment length): "))
    alpha_zero = float(input("Enter initial heading (alpha-0): "))
    angle = float(input("Enter angle: "))

    set_turtle(alpha_zero)
    draw_l_system(t, model[-1], segment_length, angle)  # draw model (turtle, generator, segment length, angle)
    ts.exitonclick()


if __name__ == "__main__":
    main()
