"""
Generates all goose sprite frames as pixel art and saves them to the sprites/ folder.
Run this once to create all the images.

Canvas: 32x32 logical pixels, SCALE=6 → 192x192 actual pixels (3x the original 64px)
"""

from PIL import Image, ImageDraw
import os

SCALE = 6
W, H = 32, 32

WHITE  = (240, 240, 235, 255)
OFFWHITE = (220, 220, 210, 255)
GRAY   = (160, 160, 155, 255)
DGRAY  = ( 90,  90,  85, 255)
ORANGE = (235, 115,  15, 255)
DORANGE= (190,  80,   5, 255)
BLACK  = (  10, 10,  10, 255)
NONE   = (  0,   0,   0,   0)
PINK   = (230, 130, 130, 255)
RED    = (200,  40,  40, 255)
BROWN  = (100,  60,  20, 255)


def new_canvas():
    return Image.new("RGBA", (W * SCALE, H * SCALE), NONE)


def px(draw, x, y, color):
    s = SCALE
    if 0 <= x < W and 0 <= y < H:
        draw.rectangle([x*s, y*s, x*s+s-1, y*s+s-1], fill=color)


def draw_goose(draw,
               body_y=20,        # vertical position of body center
               neck_curve=0,     # lean of neck: -2 left, 0 straight, 2 right
               head_tilt=0,      # shifts head sideways
               eye_style="normal", # normal | mad | dead | squint | wide
               beak_open=False,
               wing_state="rest", # rest | up | flap
               feet_state="stand", # stand | waddle_l | waddle_r
               butt_up=False):   # raises tail for dramatic effect

    # ── BODY ──────────────────────────────────────────────────────
    # Fat oval, slightly wider than tall — classic dumb goose body
    by = body_y
    body_pixels = [
        # row by-4 (top shoulder)
        (11,by-4),(12,by-4),(13,by-4),(14,by-4),(15,by-4),(16,by-4),(17,by-4),(18,by-4),(19,by-4),(20,by-4),
        # row by-3
        (9,by-3),(10,by-3),(11,by-3),(12,by-3),(13,by-3),(14,by-3),(15,by-3),(16,by-3),(17,by-3),(18,by-3),(19,by-3),(20,by-3),(21,by-3),(22,by-3),
        # row by-2
        (8,by-2),(9,by-2),(10,by-2),(11,by-2),(12,by-2),(13,by-2),(14,by-2),(15,by-2),(16,by-2),(17,by-2),(18,by-2),(19,by-2),(20,by-2),(21,by-2),(22,by-2),(23,by-2),
        # row by-1
        (8,by-1),(9,by-1),(10,by-1),(11,by-1),(12,by-1),(13,by-1),(14,by-1),(15,by-1),(16,by-1),(17,by-1),(18,by-1),(19,by-1),(20,by-1),(21,by-1),(22,by-1),(23,by-1),
        # row by (widest)
        (8,by),(9,by),(10,by),(11,by),(12,by),(13,by),(14,by),(15,by),(16,by),(17,by),(18,by),(19,by),(20,by),(21,by),(22,by),(23,by),
        # row by+1
        (9,by+1),(10,by+1),(11,by+1),(12,by+1),(13,by+1),(14,by+1),(15,by+1),(16,by+1),(17,by+1),(18,by+1),(19,by+1),(20,by+1),(21,by+1),(22,by+1),(23,by+1),
        # row by+2
        (10,by+2),(11,by+2),(12,by+2),(13,by+2),(14,by+2),(15,by+2),(16,by+2),(17,by+2),(18,by+2),(19,by+2),(20,by+2),(21,by+2),(22,by+2),
        # row by+3 (belly)
        (11,by+3),(12,by+3),(13,by+3),(14,by+3),(15,by+3),(16,by+3),(17,by+3),(18,by+3),(19,by+3),(20,by+3),
    ]
    for x, y in body_pixels:
        px(draw, x, y, WHITE)

    # Body outline
    outline = [
        (10,by-5),(11,by-5),(12,by-5),(13,by-5),(14,by-5),(15,by-5),(16,by-5),(17,by-5),(18,by-5),(19,by-5),(20,by-5),(21,by-5),
        (7,by-3),(8,by-4),(23,by-4),(24,by-3),
        (7,by-2),(24,by-2),(7,by-1),(24,by-1),(7,by),(24,by),
        (8,by+1),(23,by+1),(9,by+2),(23,by+2),(10,by+3),(22,by+3),
        (11,by+4),(12,by+4),(13,by+4),(14,by+4),(15,by+4),(16,by+4),(17,by+4),(18,by+4),(19,by+4),(20,by+4),
    ]
    for x, y in outline:
        px(draw, x, y, GRAY)

    # Tail (right side, slightly raised if butt_up)
    tail_lift = -2 if butt_up else 0
    for x, y in [(23,by-3),(24,by-4),(25,by-4),(25,by-3),(24,by-2)]:
        px(draw, x, y + tail_lift, OFFWHITE)
    for x, y in [(26,by-5),(26,by-4),(25,by-5)]:
        px(draw, x, y + tail_lift, GRAY)

    # Belly shading
    for x, y in [(13,by+2),(14,by+2),(15,by+2),(16,by+2),(17,by+2),(12,by+1),(18,by+1)]:
        px(draw, x, y, OFFWHITE)

    # ── WING ──────────────────────────────────────────────────────
    if wing_state == "up":
        for x, y in [(10,by-4),(11,by-5),(12,by-5),(13,by-6),(14,by-6),(15,by-5),(11,by-6)]:
            px(draw, x, y, GRAY)
    elif wing_state == "flap":
        for x, y in [(9,by-6),(10,by-7),(11,by-7),(12,by-8),(13,by-7),(14,by-6),(10,by-8),(11,by-8)]:
            px(draw, x, y, OFFWHITE)
        for x, y in [(8,by-6),(9,by-7),(13,by-8),(14,by-7),(15,by-6)]:
            px(draw, x, y, GRAY)
    else:  # rest — subtle wing line
        for x, y in [(11,by-2),(12,by-2),(13,by-2),(14,by-2),(15,by-2),(16,by-2)]:
            px(draw, x, y, GRAY)

    # ── NECK ──────────────────────────────────────────────────────
    # Long S-curve neck — what separates a goose from a duck!
    # Base of neck starts at top-left of body
    nc = neck_curve  # lean offset
    neck_segs = [
        # (x, y) for each neck row, top-to-bottom
        (14+nc, by-5), (13+nc, by-5),   # base wide
        (14+nc, by-6), (13+nc, by-6),
        (14+nc, by-7), (13+nc, by-7),
        (15+nc, by-8), (14+nc, by-8),   # slight curve
        (15+nc, by-9), (14+nc, by-9),
        (15+nc, by-10),(14+nc, by-10),
        (16+nc, by-11),(15+nc, by-11),  # lean into head
        (16+nc, by-12),(15+nc, by-12),
    ]
    for x, y in neck_segs:
        px(draw, x, y, WHITE)
    # neck outline
    neck_left  = [(12+nc, by-6),(12+nc, by-7),(13+nc, by-8),(13+nc, by-9),(13+nc, by-10),(14+nc, by-11),(14+nc, by-12)]
    neck_right = [(15+nc, by-6),(15+nc, by-7),(16+nc, by-8),(16+nc, by-9),(16+nc, by-10),(17+nc, by-11),(17+nc, by-12)]
    for x, y in neck_left + neck_right:
        px(draw, x, y, GRAY)

    # ── HEAD ──────────────────────────────────────────────────────
    # Tiny round head — looks hilariously small on the long neck
    hx = 15 + nc + head_tilt
    hy = by - 13
    head_pixels = [
        (hx-1,hy),(hx,hy),(hx+1,hy),(hx+2,hy),
        (hx-2,hy+1),(hx-1,hy+1),(hx,hy+1),(hx+1,hy+1),(hx+2,hy+1),(hx+3,hy+1),
        (hx-2,hy+2),(hx-1,hy+2),(hx,hy+2),(hx+1,hy+2),(hx+2,hy+2),(hx+3,hy+2),
        (hx-1,hy+3),(hx,hy+3),(hx+1,hy+3),(hx+2,hy+3),
    ]
    for x, y in head_pixels:
        px(draw, x, y, WHITE)
    head_outline = [
        (hx-2,hy),(hx+3,hy),
        (hx-3,hy+1),(hx+4,hy+1),
        (hx-3,hy+2),(hx+4,hy+2),
        (hx-2,hy+3),(hx+3,hy+3),
        (hx-1,hy+4),(hx,hy+4),(hx+1,hy+4),(hx+2,hy+4),
    ]
    for x, y in head_outline:
        px(draw, x, y, GRAY)

    # ── BEAK ──────────────────────────────────────────────────────
    beak_y = hy + 2
    if beak_open:
        # open honk beak
        for x, y in [(hx+3,beak_y),(hx+4,beak_y),(hx+5,beak_y),(hx+6,beak_y)]:
            px(draw, x, y, ORANGE)
        for x, y in [(hx+3,beak_y+1),(hx+4,beak_y+1),(hx+5,beak_y+1)]:
            px(draw, x, y, DORANGE)
        for x, y in [(hx+3,beak_y+2),(hx+4,beak_y+2),(hx+5,beak_y+2),(hx+6,beak_y+2)]:
            px(draw, x, y, ORANGE)
        # teeth — geese actually have serrated beaks, looks hilarious as tiny squares
        px(draw, hx+4, beak_y, BLACK)
        px(draw, hx+6, beak_y, BLACK)
    else:
        # closed flat beak
        for x, y in [(hx+3,beak_y),(hx+4,beak_y),(hx+5,beak_y),(hx+6,beak_y)]:
            px(draw, x, y, ORANGE)
        for x, y in [(hx+3,beak_y+1),(hx+4,beak_y+1),(hx+5,beak_y+1),(hx+6,beak_y+1)]:
            px(draw, x, y, DORANGE)
        px(draw, hx+7, beak_y, DORANGE)

    # ── EYE ───────────────────────────────────────────────────────
    ex, ey = hx+2, hy+1
    if eye_style == "normal":
        px(draw, ex, ey, BLACK)
        px(draw, ex+1, ey, BLACK)      # slightly rectangular eye
    elif eye_style == "mad":
        px(draw, ex, ey, BLACK)
        px(draw, ex+1, ey, BLACK)
        px(draw, ex-1, ey-1, BLACK)    # angry eyebrow
        px(draw, ex, ey-1, BLACK)
    elif eye_style == "dead":
        # X eyes
        px(draw, ex-1, ey-1, BLACK); px(draw, ex+1, ey-1, BLACK)
        px(draw, ex,   ey,   BLACK)
        px(draw, ex-1, ey+1, BLACK); px(draw, ex+1, ey+1, BLACK)
    elif eye_style == "squint":
        px(draw, ex, ey, DGRAY)
        px(draw, ex+1, ey, DGRAY)
        px(draw, ex, ey-1, DGRAY)     # half-closed lid
        px(draw, ex+1, ey-1, DGRAY)
    elif eye_style == "wide":
        # panic eyes — big white ring + tiny pupil
        px(draw, ex-1, ey-1, WHITE); px(draw, ex, ey-1, WHITE); px(draw, ex+1, ey-1, WHITE)
        px(draw, ex-1, ey,   WHITE); px(draw, ex, ey,   BLACK); px(draw, ex+1, ey,   WHITE)
        px(draw, ex-1, ey+1, WHITE); px(draw, ex, ey+1, WHITE); px(draw, ex+1, ey+1, WHITE)
        # outline
        for ox, oy in [(ex-2,ey-1),(ex-2,ey),(ex-2,ey+1),(ex+2,ey-1),(ex+2,ey),(ex+2,ey+1),
                       (ex-1,ey-2),(ex,ey-2),(ex+1,ey-2),(ex-1,ey+2),(ex,ey+2),(ex+1,ey+2)]:
            px(draw, ox, oy, BLACK)

    # ── FEET ──────────────────────────────────────────────────────
    fy = by + 5
    if feet_state == "stand":
        # left foot
        for x, y in [(11,fy),(12,fy),(10,fy+1),(11,fy+1),(12,fy+1),(13,fy+1)]:
            px(draw, x, y, ORANGE)
        # right foot
        for x, y in [(17,fy),(18,fy),(16,fy+1),(17,fy+1),(18,fy+1),(19,fy+1)]:
            px(draw, x, y, ORANGE)
        # legs
        px(draw, 12, fy-1, ORANGE); px(draw, 13, fy-1, ORANGE)
        px(draw, 17, fy-1, ORANGE); px(draw, 18, fy-1, ORANGE)
    elif feet_state == "waddle_l":
        # left foot forward, right foot back
        for x, y in [(9,fy),(10,fy),(11,fy),(8,fy+1),(9,fy+1),(10,fy+1),(11,fy+1)]:
            px(draw, x, y, ORANGE)
        for x, y in [(18,fy-1),(19,fy-1),(18,fy),(19,fy),(20,fy)]:
            px(draw, x, y, ORANGE)
        px(draw, 11, fy-1, ORANGE); px(draw, 12, fy-2, ORANGE)
        px(draw, 18, fy-2, ORANGE)
    elif feet_state == "waddle_r":
        # right foot forward, left foot back
        for x, y in [(9,fy-1),(10,fy-1),(9,fy),(10,fy),(11,fy)]:
            px(draw, x, y, ORANGE)
        for x, y in [(19,fy),(20,fy),(21,fy),(18,fy+1),(19,fy+1),(20,fy+1),(21,fy+1)]:
            px(draw, x, y, ORANGE)
        px(draw, 10, fy-2, ORANGE)
        px(draw, 19, fy-1, ORANGE); px(draw, 20, fy-2, ORANGE)
    elif feet_state == "air":
        # feet up (jumping / falling over)
        for x, y in [(10,fy-2),(11,fy-2),(12,fy-2),(10,fy-1),(11,fy-1)]:
            px(draw, x, y, ORANGE)
        for x, y in [(18,fy-2),(19,fy-2),(20,fy-2),(19,fy-1),(20,fy-1)]:
            px(draw, x, y, ORANGE)


def goose_on_canvas(xo=0, **kwargs):
    """Draw goose on a temp canvas then paste at x-offset onto a fresh canvas.
    Positive xo shifts right, negative shifts left (goose waddling off-screen left)."""
    temp = new_canvas()
    draw_goose(ImageDraw.Draw(temp), **kwargs)
    img = new_canvas()
    img.paste(temp, (xo * SCALE, 0), temp)
    return img


def draw_poop(draw, bx, by):
    """Classic pixel poop pile. bx/by = base-center position."""
    POOP     = (101,  55,   0, 255)
    POOP_LT  = (145,  85,  15, 255)
    POOP_DK  = ( 65,  30,   0, 255)
    SHINE    = (200, 160,  60, 255)

    # base mound (widest)
    for x in range(bx-3, bx+4):
        px(draw, x, by,   POOP)
        px(draw, x, by-1, POOP)
    # middle tier
    for x in range(bx-2, bx+3):
        px(draw, x, by-2, POOP)
        px(draw, x, by-3, POOP)
    # top swirl
    for x in range(bx-1, bx+2):
        px(draw, x, by-4, POOP)
    px(draw, bx, by-5, POOP)

    # outline
    for ox, oy in [
        (bx-4,by),(bx+4,by),(bx-4,by-1),(bx+4,by-1),
        (bx-3,by-2),(bx+3,by-2),(bx-3,by-3),(bx+3,by-3),
        (bx-2,by-4),(bx+2,by-4),(bx-1,by-5),(bx+1,by-5),
        (bx,by-6),
        (bx-3,by+1),(bx-2,by+1),(bx-1,by+1),(bx,by+1),(bx+1,by+1),(bx+2,by+1),(bx+3,by+1),
    ]:
        px(draw, ox, oy, POOP_DK)

    # highlight & shine
    px(draw, bx-1, by-4, POOP_LT)
    px(draw, bx-2, by-2, POOP_LT)
    px(draw, bx-3, by,   POOP_LT)
    px(draw, bx-1, by-5, SHINE)   # little glint on top

    # two little stink flies
    px(draw, bx-5, by-3, POOP_DK)
    px(draw, bx+5, by-4, POOP_DK)


def save(img, name):
    path = os.path.join(os.path.dirname(__file__), "sprites", f"{name}.png")
    img.save(path)
    print(f"  saved {name}.png")


# ── ANIMATION SETS ────────────────────────────────────────────────────────────

def make_idle():
    """Slow breathing — body rises and falls, occasional blink."""
    configs = [
        (20, 0, 0, "normal", False, "rest", "stand", False),
        (20, 0, 0, "normal", False, "rest", "stand", False),
        (21, 0, 0, "squint", False, "rest", "stand", False),
        (20, 0, 0, "normal", False, "rest", "stand", False),
    ]
    for i, (by, nc, ht, eye, bk, wing, feet, butt) in enumerate(configs):
        img = new_canvas()
        draw_goose(ImageDraw.Draw(img), body_y=by, neck_curve=nc, head_tilt=ht,
                   eye_style=eye, beak_open=bk, wing_state=wing, feet_state=feet, butt_up=butt)
        save(img, f"idle_{i+1}")


def make_enter():
    """Excited flap-hop when Telegram opens."""
    configs = [
        (20, 0, 0, "wide",   True,  "up",   "stand",   False),
        (18, 1, 1, "wide",   True,  "flap", "air",     False),
        (20, 0, 0, "mad",    True,  "up",   "stand",   True),
        (19, 1, 0, "wide",   False, "flap", "waddle_r",False),
        (20,-1, 0, "normal", False, "up",   "waddle_l",False),
        (20, 0, 0, "normal", False, "rest", "stand",   False),
    ]
    for i, (by, nc, ht, eye, bk, wing, feet, butt) in enumerate(configs):
        img = new_canvas()
        draw_goose(ImageDraw.Draw(img), body_y=by, neck_curve=nc, head_tilt=ht,
                   eye_style=eye, beak_open=bk, wing_state=wing, feet_state=feet, butt_up=butt)
        save(img, f"enter_{i+1}")


def make_dance():
    """Goofy waddle side-to-side dance."""
    configs = [
        (20,-2, 0, "mad",    False, "up",   "waddle_l",False),
        (19,-1, 0, "wide",   True,  "flap", "stand",   False),
        (20, 0, 0, "squint", False, "rest", "waddle_r",False),
        (19, 1, 0, "wide",   True,  "flap", "stand",   False),
        (20, 2, 0, "mad",    False, "up",   "waddle_l",False),
        (19, 1, 0, "normal", True,  "flap", "stand",   True),
    ]
    for i, (by, nc, ht, eye, bk, wing, feet, butt) in enumerate(configs):
        img = new_canvas()
        draw_goose(ImageDraw.Draw(img), body_y=by, neck_curve=nc, head_tilt=ht,
                   eye_style=eye, beak_open=bk, wing_state=wing, feet_state=feet, butt_up=butt)
        save(img, f"dance_{i+1}")


def make_sleep():
    """Eyes closed, head drooping, ZZZs."""
    for i, (by, nc, lean) in enumerate([(21,0,0),(21,1,0),(22,1,1),(21,0,0)]):
        img = new_canvas()
        draw_goose(ImageDraw.Draw(img), body_y=by, neck_curve=nc, head_tilt=lean,
                   eye_style="squint", beak_open=False, wing_state="rest",
                   feet_state="stand", butt_up=False)
        # floating Z's
        d = ImageDraw.Draw(img)
        zs = [(26,8),(27,6),(28,4)] if i % 2 == 0 else [(27,7),(28,5)]
        for zx, zy in zs:
            px(d, zx, zy, DGRAY)
        save(img, f"sleep_{i+1}")


def make_bye():
    """Wave goodbye."""
    configs = [
        (20, 0, 0, "normal", False, "up",   "stand",   False),
        (20, 1, 1, "wide",   True,  "flap", "waddle_r",False),
        (20, 0, 0, "normal", False, "up",   "stand",   False),
        (20,-1,-1, "squint", False, "rest", "waddle_l",False),
    ]
    for i, (by, nc, ht, eye, bk, wing, feet, butt) in enumerate(configs):
        img = new_canvas()
        draw_goose(ImageDraw.Draw(img), body_y=by, neck_curve=nc, head_tilt=ht,
                   eye_style=eye, beak_open=bk, wing_state=wing, feet_state=feet, butt_up=butt)
        save(img, f"bye_{i+1}")


def make_poop_waddle():
    """
    The goose squats, drops a poop, then waddles left with smug pride.

    Frames:
      1  – standing normal, about to do something
      2  – butt raised, eyes half-closed (concentrating)
      3  – butt raised further, effort squint, poop mid-drop
      4  – poop lands, goose looks incredibly smug, beak open in silent honk
      5  – goose starts waddling LEFT, proud head held high, poop stays
      6  – goose further left, waddle step, glances back smugly
      7  – goose almost off-screen, tail still raised in triumph
      8  – just the poop sits there alone, goose gone
    """
    POOP_X, POOP_Y = 20, 27   # where the poop lands (tail region)

    # (xo, by, nc, ht, eye, beak, wing, feet, butt, show_poop, poop_falling)
    frames = [
        ( 0, 20,  0,  0, "normal", False, "rest",   "stand",   False, False, False),
        ( 0, 20,  0,  0, "squint", False, "rest",   "stand",   True,  False, False),
        ( 0, 20,  1,  0, "squint", False, "rest",   "stand",   True,  False, True ),  # mid-drop
        ( 0, 20,  1,  0, "squint", True,  "up",     "stand",   True,  True,  False),  # lands + honk
        (-4, 20, -1,  0, "squint", False, "up",     "waddle_l",False, True,  False),  # waddle
        (-8, 20, -1,  0, "squint", False, "rest",   "waddle_r",False, True,  False),
        (-13,20, -2,  0, "squint", True,  "up",     "waddle_l",True,  True,  False),  # triumphant
        (None,0,  0,  0, "normal", False, "rest",   "stand",   False, True,  False),  # poop alone
    ]

    for i, (xo, by, nc, ht, eye, bk, wing, feet, butt, show_poop, falling) in enumerate(frames):
        img = new_canvas()
        d   = ImageDraw.Draw(img)

        if show_poop:
            draw_poop(d, POOP_X, POOP_Y)
        elif falling:
            # poop mid-air: smaller blob halfway down
            for ox, oy in [(POOP_X, POOP_Y-4),(POOP_X+1, POOP_Y-4),(POOP_X, POOP_Y-3)]:
                px(d, ox, oy, (101, 55, 0, 255))

        if xo is not None:
            goose = goose_on_canvas(xo=xo, body_y=by, neck_curve=nc, head_tilt=ht,
                                    eye_style=eye, beak_open=bk, wing_state=wing,
                                    feet_state=feet, butt_up=butt)
            img = Image.alpha_composite(img, goose)

        save(img, f"poop_waddle_{i+1}")


if __name__ == "__main__":
    print("Generating goose sprites (32x32 @ 6x scale = 192px)...")
    make_idle()
    make_enter()
    make_dance()
    make_sleep()
    make_bye()
    make_poop_waddle()
    print("Done! All sprites saved to sprites/")
