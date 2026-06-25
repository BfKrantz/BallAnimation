import math
import time
import sys


ASPECT = 2.5  # horizontal stretch so the ball looks round 


def make_frame(radius: int, cx: float, cy: float,
               x_scale: float, y_scale: float,
               canvas_width: int, canvas_height: int) -> str:
    """
    Render one frame: an ellipse of '#' centred at (cx, cy), clipped to canvas.

    Args:
        radius:        Base radius in rows.
        cx:            Horizontal centre in character columns.
        cy:            Vertical centre in canvas rows.
        x_scale:       Horizontal squish factor (>1 = wider).
        y_scale:       Vertical squish factor (<1 = flatter).
        canvas_width:  Total canvas width in characters.
        canvas_height: Total canvas height in rows.

    Returns:
        A string of exactly canvas_height lines, each canvas_width chars wide.
    """
    r_y = radius * y_scale
    r_x = radius * x_scale
    row_range = math.ceil(r_y)
    blank = " " * canvas_width
    row_map = {}

    for row_i in range(-row_range, row_range + 1):
        inner = 1 - (row_i / r_y) ** 2
        if inner <= 0:
            continue
        half_chars = math.sqrt(inner) * r_x * ASPECT
        count = round(half_chars)
        if count <= 0:
            continue

        canvas_row = round(cy) + row_i
        if not (0 <= canvas_row < canvas_height):
            continue

        hash_width = count * 2 - 1
        start_col  = round(cx) - hash_width // 2
        clip_left  = max(0, -start_col)
        clip_right = max(0, (start_col + hash_width) - canvas_width)
        if clip_left >= hash_width - clip_right:
            continue

        hashes  = " ".join(["#"] * count)
        visible = hashes[clip_left: hash_width - clip_right]
        col     = max(0, start_col)
        if visible.strip():
            row_map[canvas_row] = " " * col + visible

    return "\n".join(row_map.get(r, blank) for r in range(canvas_height))


def clear_lines(n: int) -> None:
    """Move cursor up n lines and clear each."""
    for _ in range(n):
        sys.stdout.write("\033[F\033[2K")
    sys.stdout.flush()


def build_physics_frames(radius: int, fps: int):
    """
    Simulate ball physics and return frames + canvas dimensions.

    The ball falls from the top, drifts right during two bounces (squishing
    on each impact), then rolls right and exits the canvas edge.

    Args:
        radius: Ball radius in rows.
        fps:    Frames per second.

    Returns:
        Tuple of (frames, canvas_width, canvas_height) where frames is a list
        of (cx, cy, x_scale, y_scale) tuples.
    """
    ball_w     = round(radius * ASPECT) * 2

    # Drop height: ball falls radius*2 rows before first bounce
    drop_rows  = radius * 2
    # ground_row is the canvas row of the ball's CENTRE when sitting on the ground
    ground_row = radius + drop_rows + radius   # = radius + drop_rows + radius
    # Canvas height = ground_row + 1 (ground is the very last visible row)
    canvas_height = ground_row + 1

    # Canvas width: fits 2 full ball-widths for the bouncing phase,
    # then the ball exits at the right edge during the roll.
    canvas_width = ball_w * 2 + 4

    start_cy = float(radius)           # centre at top, ball's top edge at row 0
    start_cx = float(ball_w // 2 + 2) # a little in from the left

    gravity     = 0.7
    restitution = 0.55
    num_bounces = 2
    min_bounce  = radius * 0.15
    # Slow drift right during bounces; speed up to roll after final landing
    drift_vx    = max(1, round(radius * ASPECT * 0.10))
    roll_vx     = max(3, round(radius * ASPECT * 0.40))
    recovery    = 0.20

    cy, cx   = start_cy, start_cx
    vy, vx   = 0.0, float(drift_vx)
    xs, ys   = 1.0, 1.0
    bounces_done = 0
    rolling      = False

    frames = []
    for _ in range(fps * 12):
        frames.append((cx, cy, xs, ys))
        cx += vx

        if rolling:
            xs += (1.0 - xs) * recovery
            ys += (1.0 - ys) * recovery
            # Stop once the ball is fully off the right edge
            if cx - ball_w // 2 > canvas_width:
                break
            continue

        vy += gravity
        cy += vy
        xs += (1.0 - xs) * recovery
        ys += (1.0 - ys) * recovery

        bottom = cy + radius * ys
        if bottom >= ground_row and vy > 0:
            impact = vy
            bounces_done += 1

            if bounces_done >= num_bounces or impact * restitution < min_bounce:
                cy  = float(ground_row - radius)
                strength = min(impact / (radius * 3.0), 1.0)
                xs  = 1.0 + 0.30 * strength
                ys  = max(0.75, 1.0 - 0.28 * strength)
                rolling = True
                vx  = float(roll_vx)
            else:
                cy  = ground_row - radius * ys
                vy  = -impact * restitution
                strength = min(impact / (radius * 2.5), 1.0)
                xs  = 1.0 + 0.45 * strength
                ys  = max(0.52, 1.0 - 0.50 * strength)

    return frames, canvas_width, canvas_height


def interpolate_frames(frames: list, substeps: int = 2) -> list:
    """Smoothstep-interpolate between physics ticks for smoother playback."""
    def smooth(t):
        return t * t * (3 - 2 * t)

    out = []
    for i in range(len(frames) - 1):
        cx0, cy0, xs0, ys0 = frames[i]
        cx1, cy1, xs1, ys1 = frames[i + 1]
        for s in range(substeps):
            t = smooth(s / substeps)
            out.append((
                cx0 + (cx1 - cx0) * t,
                cy0 + (cy1 - cy0) * t,
                xs0 + (xs1 - xs0) * t,
                ys0 + (ys1 - ys0) * t,
            ))
    out.append(frames[-1])
    return out


def animate(radius: int, fps: int = 24, loop: bool = False) -> None:
    """
    Animate the ball: falls, bounces twice (with squish), drifts right,
    then rolls off the right edge of the canvas.

    Args:
        radius: Ball radius in rows. Must be a whole number >= 3.
        fps:    Frames per second (default 24).
        loop:   Repeat forever if True. Press Ctrl-C to stop.

    Raises:
        TypeError:  If radius is not an integer.
        ValueError: If radius is less than 3.
    """
    if not isinstance(radius, int):
        raise TypeError(f"radius must be a whole number (int), got {type(radius).__name__}")
    if radius < 3:
        raise ValueError(f"radius must be >= 3, got {radius}")

    delay = 1.0 / fps
    physics, canvas_width, canvas_height = build_physics_frames(radius, fps)
    all_frames = interpolate_frames(physics, substeps=2)

    def run_once() -> int:
        cx, cy, xs, ys = all_frames[0]
        first = make_frame(radius, cx, cy, xs, ys, canvas_width, canvas_height)
        print(first)
        prev_lines = first.count("\n") + 1

        for cx, cy, xs, ys in all_frames[1:]:
            time.sleep(delay)
            frame = make_frame(radius, cx, cy, xs, ys, canvas_width, canvas_height)
            clear_lines(prev_lines)
            print(frame)
            prev_lines = frame.count("\n") + 1

        return prev_lines

    if loop:
        while True:
            prev = run_once()
            time.sleep(0.3)
            clear_lines(prev)
    else:
        run_once()


if __name__ == "__main__":
    try:
        raw = input("Enter ball radius (whole number >= 3): ")
        if "." in raw:
            raise TypeError("radius must be a whole number (int), not a decimal")
        radius = int(raw)

        loop_raw = input("Loop animation? (y/n, default n): ").strip().lower()
        loop = loop_raw in ("y", "yes")

        print()
        animate(radius, loop=loop)

    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nStopped.")