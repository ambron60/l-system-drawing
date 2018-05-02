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
    stack = list()
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
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)


def set_turtle(alpha_zero):
    global t, ts
    t = turtle.Turtle()  # turtle
    ts = turtle.Screen()  # create graphics window
    ts.screensize(1500, 1500)
    t.screen.title("Fractal Curve")
    t.speed(0)  # adjust as needed (0 = fastest)
    t.setheading(alpha_zero)  # initial heading


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

    axiom = input("Enter axiom (w): ")
    iterations = int(input("Enter number of iterations (n): "))

    model = derivation(axiom, iterations)  # axiom (initial string), nth iterations

    segment_length = int(input("Enter step size (segment length): "))
    alpha_zero = float(input("Enter initial heading (alpha-0): "))
    angle = float(input("Enter angle increment (i): "))

    set_turtle(alpha_zero)
    draw_l_system(t, model[-1], segment_length, angle)  # draw model (turtle, generator, segment length, angle)
    ts.exitonclick()


if __name__ == "__main__":
    main()
