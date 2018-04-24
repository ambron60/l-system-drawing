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
    for rule in rules:
        turtle.pd()
        if rule == "F":
            turtle.forward(seg_length)
        elif rule == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif rule == "+":
            turtle.left(angle)  # adjust these angles to tilt on y axis
        elif rule == "-":
            turtle.right(angle)


def set_turtle():
    global t, ts
    t = turtle.Turtle()  # turtle
    ts = turtle.Screen()  # create graphics window
    ts.screensize(1000, 1000)
    t.pu()
    # t.back(100) # adjust or comment out as needed
    t.speed(150)
    t.setheading(0)


def main():
    global rules
    rules = dict()
    rule_num = 1
    while True:
        rule = input("Enter rule[%d]:rewrite term (0 when done): " % rule_num)
        if rule == '0':
            break
        key, value = rule.split(":")
        rules[key] = value
        rule_num += 1
    print("\nL-System notes -> %s\n" % rules)

    set_turtle()

    axiom = input("Enter axiom (initial string): ")
    iterations = int(input("Enter number of iterations (n): "))
    model = derivation(axiom, iterations)  # axiom (initial string), nth iterations

    segment_length = int(input("Enter step size (segment length): "))
    angle = int(input("Enter angle: "))
    draw_l_system(t, model[-1], segment_length, angle)  # draw model (turtle, generator, segment length, angle)

    ts.exitonclick()


if __name__ == "__main__":
    main()
