import sys

VALID_DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]
MIN_POS = 0
MAX_POS = 4


class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.facing = "NORTH"
        self.placed = False

    def is_valid_position(self, x, y):
        return MIN_POS <= x <= MAX_POS and MIN_POS <= y <= MAX_POS

    def place(self, x, y, facing):
        if facing not in VALID_DIRECTIONS:
            return False
        if not self.is_valid_position(x, y):
            return False

        self.x = x
        self.y = y
        self.facing = facing
        self.placed = True
        return True

    def move(self):
        if not self.placed:
            return False

        new_x, new_y = self.x, self.y

        if self.facing == "NORTH":
            new_y += 1
        elif self.facing == "SOUTH":
            new_y -= 1
        elif self.facing == "EAST":
            new_x += 1
        elif self.facing == "WEST":
            new_x -= 1

        if self.is_valid_position(new_x, new_y):
            self.x, self.y = new_x, new_y
            return True

        return False  # ignore move if it would fall off

    def left(self):
        if not self.placed:
            return False
        idx = VALID_DIRECTIONS.index(self.facing)
        self.facing = VALID_DIRECTIONS[(idx - 1) % len(VALID_DIRECTIONS)]
        return True

    def right(self):
        if not self.placed:
            return False
        idx = VALID_DIRECTIONS.index(self.facing)
        self.facing = VALID_DIRECTIONS[(idx + 1) % len(VALID_DIRECTIONS)]
        return True

    def report(self):
        if not self.placed:
            return None
        return f"{self.x},{self.y},{self.facing}"


class RobotPlotter:
    """
    Optional plotting class. Only used if --plot flag is passed.
    """

    def __init__(self):
        import matplotlib.pyplot as plt

        self.plt = plt
        self.plt.close("all")
        self.plt.ion()  # interactive mode ON

        self.fig, self.ax = self.plt.subplots()
        self.setup_grid()

    def setup_grid(self):
        self.ax.set_xticks(range(5))
        self.ax.set_yticks(range(5))
        self.ax.grid(True)
        self.ax.set_xlim(-0.5, 4.5)
        self.ax.set_ylim(-0.5, 4.5)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title("Mars Rover Simulator")

    def update(self, robot: Robot):
        self.ax.clear()
        self.setup_grid()

        if robot.placed:
            # draw robot point
            self.ax.scatter(robot.x, robot.y, s=200)

            # draw facing arrow
            arrow_map = {
                "NORTH": (0, 0.4),
                "SOUTH": (0, -0.4),
                "EAST": (0.4, 0),
                "WEST": (-0.4, 0),
            }
            dx, dy = arrow_map[robot.facing]
            self.ax.arrow(
                robot.x,
                robot.y,
                dx,
                dy,
                head_width=0.15,
                length_includes_head=True,
            )

            # label robot
            self.ax.text(robot.x + 0.1, robot.y + 0.1, robot.facing, fontsize=10)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def pause(self, seconds: float = 0.25):
        """
        Small pause to allow the plot to refresh (important in file-mode).
        """
        self.plt.pause(seconds)

    def show_blocking(self):
        self.plt.ioff()
        self.plt.show()


def parse_place(command: str):
    # Expected: PLACE X,Y,FACING
    try:
        args = command[6:].split(",")
        x = int(args[0].strip())
        y = int(args[1].strip())
        facing = args[2].strip().upper()
        return x, y, facing
    except (ValueError, IndexError):
        return None


def process_command(robot: Robot, cmd_upper: str):
    """
    Returns (changed: bool, quit_requested: bool)
    """
    changed = False
    quit_requested = False

    if cmd_upper.startswith("PLACE "):
        parsed = parse_place(cmd_upper)
        if parsed:
            x, y, facing = parsed
            changed = robot.place(x, y, facing)

    elif cmd_upper == "MOVE":
        changed = robot.move()
        if not changed and not robot.placed:
            print("Robot not placed yet. Please use: PLACE X,Y,FACING first")

    elif cmd_upper == "LEFT":
        changed = robot.left()
        if not changed and not robot.placed:
            print("Robot not placed yet. Please use: PLACE X,Y,FACING first")

    elif cmd_upper == "RIGHT":
        changed = robot.right()
        if not changed and not robot.placed:
            print("Robot not placed yet. Please use: PLACE X,Y,FACING first")

    elif cmd_upper == "REPORT":
        result = robot.report()
        if result:
            print(result)
        else:
            print("Robot not placed yet. Please use: PLACE X,Y,FACING first")

    elif cmd_upper in ["EXIT", "QUIT"]:
        quit_requested = True

    # Unknown commands are ignored silently
    return changed, quit_requested


def main():
    # ------------------------------------------------
    # Parse arguments:
    #   py rover.py [commands_file] [--plot]
    # ------------------------------------------------
    plot_enabled = "--plot" in sys.argv

    # Find input filename (first arg that isn't script name and isn't --plot)
    filename = None
    for arg in sys.argv[1:]:
        if arg != "--plot":
            filename = arg
            break

    robot = Robot()

    plotter = None
    if plot_enabled:
        try:
            plotter = RobotPlotter()
            plotter.update(robot)      # empty grid at start
            plotter.pause(0.2)         # small refresh
        except ModuleNotFoundError:
            print("matplotlib is not installed. Running without plot.")
            plotter = None

    print("Mars Rover Simulator")
    print("Commands: PLACE X,Y,FACING | MOVE | LEFT | RIGHT | REPORT | QUIT")
    print("Plot mode:", "ENABLED (--plot)" if plot_enabled else "DISABLED (use --plot)")
    print()

    # ------------------------------------------------
    # FILE MODE
    # ------------------------------------------------
    if filename:
        try:
            with open(filename, "r") as f:
                commands = f.readlines()
        except FileNotFoundError:
            print(f"Error: file '{filename}' not found.")
            return

        for line in commands:
            command = line.strip()
            if not command:
                continue

            cmd_upper = command.upper()
            changed, quit_requested = process_command(robot, cmd_upper)

            if changed and plotter:
                plotter.update(robot)
                plotter.pause(0.25)  # ✅ so you can SEE movement in file-mode

            if quit_requested:
                break

        # Always show final state on plot (if enabled)
        if plotter:
            plotter.update(robot)
            plotter.pause(0.25)
            plotter.show_blocking()

        return

    # ------------------------------------------------
    # INTERACTIVE MODE
    # ------------------------------------------------
    print("Interactive mode. Type commands (Ctrl+C or QUIT to exit).")

    while True:
        try:
            command = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not command:
            continue

        cmd_upper = command.upper()
        changed, quit_requested = process_command(robot, cmd_upper)

        if changed and plotter:
            plotter.update(robot)

        if quit_requested:
            print("Exiting...")
            break

    if plotter:
        plotter.show_blocking()


if __name__ == "__main__":
    main()
