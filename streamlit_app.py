import json
import numpy as np
import pandas as pd
import random
from random import randrange
import streamlit as st
import streamlit.components.v1 as components
import time

# -------------- refrence docs: --------------

# https://www.pythonmorsels.com/making-auto-updating-attribute/
# https://developer.mozilla.org/en-US/docs/Games/Techniques/Tilemaps

# ------------------------------------------------------------
#
#                  Visual settings and functions
#
# ------------------------------------------------------------

st.set_page_config(
    page_title="The Dungeon", page_icon="🗡️", initial_sidebar_state="collapsed"
)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ------------------------------------------------------------
#
#                        Classes
#
# ------------------------------------------------------------

# object constructor for player and monsters


class Character:
    def __init__(self, x, y, file, hp, gold, alive):
        self.x = x
        self.y = y
        self.file = (
            "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/"
            + file
        )
        self.hp = hp
        self.gold = gold
        self.alive = alive

    @property
    def html(self):
        return (
            "<img src='"
            + str(self.file)
            + "' style='grid-column-start: "
            + str(self.x)
            + "; grid-row-start: "
            + str(self.y)
            + ";'>"
        )


# object constructor for chests and other inanimate objects


class InanimateObject:
    def __init__(self, x, y, file, visible):
        self.x = x
        self.y = y
        self.file = (
            "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/"
            + file
        )
        self.visible = visible

    @property
    def html(self):
        return (
            "<img src='"
            + str(self.file)
            + "' style='grid-column-start: "
            + str(self.x)
            + "; grid-row-start: "
            + str(self.y)
            + ";'>"
        )


# ------------------------------------------------------------
#
#                        Objects
#
# ------------------------------------------------------------


# ------------------------------------------------------------
#
#                  Variables and constants
#
# ------------------------------------------------------------

# ---------------- initiat session states ----------------

if "left_clicked" not in st.session_state:
    st.session_state["left_clicked"] = False

if "right_clicked" not in st.session_state:
    st.session_state["right_clicked"] = False

if "up_clicked" not in st.session_state:
    st.session_state["up_clicked"] = False

if "down_clicked" not in st.session_state:
    st.session_state["down_clicked"] = False

if "steps" not in st.session_state:
    st.session_state["steps"] = 0

if "bubble_text" not in st.session_state:
    st.session_state["bubble_text"] = ""

if "cold_start" not in st.session_state:
    st.session_state["cold_start"] = True

if "end" not in st.session_state:
    st.session_state["end"] = False


# ---------------- links ----------------

cat = "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/cat.gif"
player = "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/player.gif"

# ------------------------------------------------------------
#
#                        Callbacks
#
# ------------------------------------------------------------


def left_callback():

    if character_can_move(
        st.session_state[
            "level"
        ],  # note the different order of x and y. Done to confuse myself in the future.
        # good luck future me
        st.session_state["player"].y,
        st.session_state["player"].x - 1,
    ):
        st.session_state["player"].x -= 1
        st.session_state.left_clicked = True
        st.session_state["steps"] += 1

    # this little loop is responsible for moving the monsters and reacting to encounters
    for i in range(0, len(st.session_state["monsters"])):
        random_move(st.session_state["monsters"][i])
        encounter(st.session_state["monsters"][i])
    treasures("chest1")
    treasures("chest2")


def right_callback():
    # player movement
    if character_can_move(
        st.session_state["level"],
        st.session_state["player"].y,
        st.session_state["player"].x + 1,
    ):
        st.session_state["player"].x += 1
        st.session_state.right_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        random_move(st.session_state["monsters"][i])
        encounter(st.session_state["monsters"][i])
    treasures("chest1")
    treasures("chest2")


def up_callback():
    if character_can_move(
        st.session_state["level"],
        st.session_state["player"].y - 1,
        st.session_state["player"].x,
    ):
        st.session_state["player"].y -= 1
        st.session_state.up_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        random_move(st.session_state["monsters"][i])
        encounter(st.session_state["monsters"][i])
    treasures("chest1")
    treasures("chest2")


def down_callback():
    if character_can_move(
        st.session_state["level"],
        st.session_state["player"].y + 1,
        st.session_state["player"].x,
    ):
        st.session_state["player"].y += 1
        st.session_state.down_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        random_move(st.session_state["monsters"][i])
        encounter(st.session_state["monsters"][i])
    treasures("chest1")
    treasures("chest2")


# ------------------------------------------------------------
#
#                        Functions
#
# ------------------------------------------------------------


# ---------------- data fetch ----------------


@st.cache_data
def fetch_data(level_name):
    df = pd.read_csv(level_name, sep=",", header=None)
    return df


# ---------------- check surroundings ----------------

# this function checks all potential moves


def character_can_move(logic_layer, x, y):
    if tileset_movable[logic_layer[x - 1, y - 1]] == True:
        return True
    else:
        pass


# ---------------- random moves ----------------


def random_move(movable_object):

    # this function is responsible for random movement of monsters
    # it will be changed in the future - monsters will follow the player
    # is it possible? yes. check https://rogue-rpg.streamlit.app/

    rnd_move = randrange(100)
    # st.write("random_move" + str(rnd_move))
    if rnd_move < 25:
        if character_can_move(
            st.session_state["level"],
            movable_object.y,
            movable_object.x + 1,
        ):
            movable_object.x += 1
    if rnd_move >= 25 and rnd_move < 50:
        if character_can_move(
            st.session_state["level"],
            movable_object.y,
            movable_object.x - 1,
        ):
            movable_object.x -= 1
    if rnd_move >= 50 and rnd_move < 75:
        if character_can_move(
            st.session_state["level"],
            movable_object.y + 1,
            movable_object.x,
        ):
            movable_object.y += 1
    if rnd_move >= 75 and rnd_move < 100:
        if character_can_move(
            st.session_state["level"],
            movable_object.y - 1,
            movable_object.x,
        ):
            movable_object.y -= 1


# ---------------- encounter with monster ----------------


def encounter(enemy):

    # if you encounter an enemy and enemy is alive
    # you will lose health but enemy will die

    if (
        st.session_state["player"].x == enemy.x
        and st.session_state["player"].y == enemy.y
        and enemy.alive == True
    ):
        damage = randrange(30)
        st.session_state["bubble_text"] = text_bubble_html(
            "OMG -" + str(damage) + "hp",
            st.session_state["player"].x,
            st.session_state["player"].y - 1,
        )
        st.session_state["player"].hp = st.session_state["player"].hp - damage
        enemy.alive = False
        if st.session_state["player"].hp <= 0:
            st.session_state["player"].alive = False


def treasures(treasure):

    # if you encounter treaseure you will get gold

    if (
        st.session_state["player"].x == st.session_state[treasure].x
        and st.session_state["player"].y == st.session_state[treasure].y
        and st.session_state[treasure].visible
    ):
        gold = randrange(20)
        st.session_state["bubble_text"] = text_bubble_html(
            "yeah! +" + str(gold) + " g",
            st.session_state["player"].x,
            st.session_state["player"].y - 1,
        )
        st.session_state[treasure].visible = False
        st.session_state["player"].gold = st.session_state["player"].gold + gold


# ------------------------------------------------------------
#
#                        Graphics engine
#
# ------------------------------------------------------------

# ---------------- CSS ----------------

local_css("style.css")

# ---------------- tilset dictionary ----------------

tileset = {
    "@": "https://oshi.at/ZMUu/avRY.gif",
    "W": "https://thumbs2.imgbox.com/10/db/7zaxbIP8_t.png",  # wall
    "FP": "https://thumbs2.imgbox.com/29/22/5rTLr6WH_t.png",  # floor_plain
    # "FP": "https://oshi.at/PQkn/ExtR.png",  # floor 1 tilset 2
    "CAT": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/cat.gif",  # cat
    "M": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/monster.gif",  # monster, skeleton
    "FS": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_stain_1.png",
    "E": "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==",
    "FE3": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_edge_3.png",  # floor_edge_3
    "WON": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_n.png",  # Wall_outer_n
    "WOE": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_e.png",  # Wall_outer_e
    "WONE": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_ne.png",  # Wall_outer_ne
    "WOW": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_w.png",  # Wall_outer_w
    "WONW": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_outer_nw.png",  # wall_outer_nw
    "WFR": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Wall_front_right.png",  # wall front right
    "WTR": "https://oshi.at/QpWg/Mfxv.png",  # wall top right
    # "DK": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/wall_missing_brick_2.png",  # darkness
    "WMB": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/wall_missing_brick_2.png",  # wall missing brick 1
    "BOX": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/box.png",  # box
    "DR": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/darkness_right.png",  # darkenss right
    "DB": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/darkness_bottom.png",  # darkness bottom
    "T": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/torch.gif",  # torch
    "FMN1": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_mud_n_1.png",  # floor_mud_n_1
    "FMN2": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_mud_n_2.png",  # floor_mud_n_2
    "FMNE": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/floor_mud_ne.png",  # floor_mud_ne
    "CGOF": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/chest_golden_open_full.png",  # chest_golden_open_full
    "CGOO": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/chest_open_empty.png",  # chest_open_empty
    "FL": "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/Floor_ladder.png",  # Floor_ladder
}

tileset_movable = {
    "@": True,
    "W": False,
    "FP": True,  # floor_plain
    # "FP": "https://oshi.at/PQkn/ExtR.png",  # floor 1 tilset 2
    "CAT": True,
    "M": True,  # monster, skeleton
    "FS": True,
    "E": False,
    "FE3": False,  # floor_edge_3
    "WON": False,  # wall outer n
    "WOE": False,  # wall outer e
    "WONE": False,  # wall outer ne
    "WOW": False,  # wall outer w
    "WONW": False,  # wall_outer_nw
    "WFR": False,  # wall front right
    "WTR": False,  # wall top right
    "DK": False,  # darkness
    "WMB": False,  # wall missing brick
    "BOX": False,  # box
    "DR": False,  # darkenss right
    "DB": False,  # darkness bottom
    "T": False,  # torch
    "FMN1": True,  # floor mud n1
    "FMN2": True,
    "FMNE": True,  # floor mud ne
    "FL": True,
}

# ---------------- level renderer ----------------

# this is the heart of graphical engine
# whole game is based on a grid div with x & y columns
# placement of objects is done by manipulating grid-column-start: & grid-row-start:


def level_renderer(df, game_objects):
    i = 0
    j = 0
    level_html = '<div class="container"><div class="gamegrid">'
    for x in df:  # array from data frame: df.values
        # st.write(x)
        j = 0
        for y in x:

            # if y == "FP" and random.uniform(0, 1) > 0.7:
            #     tilset_tile = tileset["DK"]
            # else:
            #     tilset_tile = tileset[y]

            level_html = (
                level_html
                + '<img src="'
                + tileset[y]  # tilset_tile
                + '" style="grid-column-start: '
                + str(j + 1)
                + "; grid-row-start: "
                + str(i + 1)
                + ';">'
            )
            j = j + 1
        i = i + 1
    level_html = level_html + game_objects + "</div></div>"
    return level_html


# ------------------------------------------------------------
#
#             Game enigne - frontend html creator
#
# ------------------------------------------------------------

# --------------- level config ------------------------


if "level_data" not in st.session_state:
    level_config = """
{   "players_stats": {
    "file": "player.gif",
    "hp": 20,
    "gold": 0,
    "alive": true
    },
    "level1": {
        "level_name": "level1.csv",
        "player_xy": {
            "x":4,
            "y":5
        },
        "monsters": {
            "monster1":{"x":42,"y":30,"file":"monster.gif","hp":10,"gold":0,"alive":true},
            "monster2":{"x":24,"y":22,"file":"imp.gif","hp":5,"gold":0,"alive":true},
            "monster3":{"x":40,"y":12,"file":"mimic.png","hp":5,"gold":0,"alive":true}
            }
        
    }
}
"""
    st.session_state.level_data = json.loads(level_config)

# ---------------- creating player html ----------------

if "player" not in st.session_state:
    ply = st.session_state.level_data["players_stats"]
    st.session_state["player"] = Character(
        x=4, y=5, file=ply["file"], hp=ply["hp"], gold=ply["gold"], alive=ply["alive"]
    )

player = f"""
<img src="{player}" id="player" class="player" style="grid-column-start: {st.session_state["player"].x}; grid-row-start: {st.session_state["player"].y};">"""

# ---------------- creating monsters html ----------------

# we are constructing monsters in iteractions based on level configuration
if "monsters" not in st.session_state:
    st.session_state["monsters"] = []
    for i in range(0, len(st.session_state.level_data["level1"]["monsters"])):
        mst = list(st.session_state.level_data["level1"]["monsters"].values())[i]
        st.write()
        st.session_state["monsters"].append(
            Character(
                x=mst["x"],
                y=mst["y"],
                file=mst["file"],
                hp=mst["hp"],
                gold=mst["gold"],
                alive=mst["alive"],
            )
        )

# we are creating monsters html


def enemies_html(monsters_session_state):
    # empty string
    html = ""
    # creating html
    for i in range(0, len(monsters_session_state)):
        if monsters_session_state[i].alive:
            html = html + monsters_session_state[i].html
    # adding a cat - don't ask why
    html = (
        html
        + f"""
            <img src="{cat}" style="grid-column-start: 47; grid-row-start: 11;">
        """
    )
    return html


enemies = enemies_html(st.session_state["monsters"])

# ---------------- creating visual layers ----------------

# this little function provides html for additional layers
def tile_html(text, x, y, z):
    return f"""<img src="{text}" style="grid-column-start: {x}; grid-row-start: {y}; grid-column-end:{z}">"""


boxes = (
    tile_html(text=tileset["BOX"], x=4, y=17, z=4)
    + tile_html(text=tileset["BOX"], x=6, y=3, z=6)
    + tile_html(text=tileset["BOX"], x=37, y=29, z=37)
)


voids = (
    tile_html(text=tileset["DR"], x=47, y=13, z=49)
    + tile_html(text=tileset["DR"], x=19, y=23, z=21)
    + tile_html(text=tileset["DR"], x=16, y=11, z=18)
    + tile_html(text=tileset["DR"], x=40, y=37, z=42)
)


torches = (
    tile_html(text=tileset["T"], x=21, y=5, z=21)
    + tile_html(text=tileset["T"], x=18, y=25, z=18)
    + tile_html(text=tileset["T"], x=22, y=25, z=22)
    + tile_html(text=tileset["T"], x=46, y=30, z=46)
    + tile_html(text=tileset["T"], x=33, y=13, z=33)
)


if "chest1" not in st.session_state:
    st.session_state["chest1"] = InanimateObject(
        x=18, y=6, file="chest_golden_open_full.png", visible=True
    )
if "chest2" not in st.session_state:
    st.session_state["chest2"] = InanimateObject(
        x=20, y=25, file="chest_golden_open_full.png", visible=True
    )

chests = (
    st.session_state["chest1"].html if st.session_state["chest1"].visible else ""
) + (st.session_state["chest2"].html if st.session_state["chest2"].visible else "")


# ---------------- creating visual layers textboxes ----------------


def text_bubble_html(text, x, y):
    return f"""<div class="container_text" style="position: relative; grid-column-start: {x}; grid-row-start: {y}; grid-column-end: {x+4};"><img src="https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/message.png"><div style="position: absolute; top: 40%;left: 50%;transform: translate(-50%, -50%);font-size:0.875rem;">{text}</div></div>"""


if st.session_state["player"].x == 10 and st.session_state["player"].y == 5:
    # text_boxes = f"""<div class="container_text" style="position: relative; grid-column-start: 10; grid-row-start: 4; grid-column-end: 14;"><img src="https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/message.png"><div style="position: absolute; top: 40%;left: 50%;transform: translate(-50%, -50%);">What?</div></div>"""
    text_boxes = text_bubble_html("What?", 10, 4)
elif st.session_state["player"].x == 16 and st.session_state["player"].y == 11:
    text_boxes = text_bubble_html("Strange", 16, 10)
elif st.session_state["player"].x == 5 and st.session_state["player"].y == 21:
    text_boxes = text_bubble_html("Monsters?", 5, 20)
elif st.session_state["player"].x == 47 and st.session_state["player"].y == 12:
    text_boxes = text_bubble_html("Meow!", 48, 10)
elif st.session_state["player"].x == 4 and st.session_state["player"].y == 17:
    text_boxes = text_bubble_html("box (ツ)", 4, 16)
elif st.session_state["bubble_text"] != "":
    text_boxes = st.session_state["bubble_text"]
    st.session_state["bubble_text"] = ""
else:
    text_boxes = ""


# ---------------- fetching level data ----------------

# fetch level with certain number
df = fetch_data(st.session_state.level_data["level1"]["level_name"])
if "level" not in st.session_state:  # or st.session_state["level_change"]:
    st.session_state["level"] = df.values


# ---------------- END CONDITION ----------------
if st.session_state["player"].x == 33 and st.session_state["player"].y == 4:
    st.session_state["end"] = True

# ------------------------------------------------------------
#
#             Game enigne - frontend html renderer
#
# ------------------------------------------------------------

tab1, tab2 = st.tabs(["intro", "start game"])

# ----------------- game start --------

with tab1:
    st.subheader("| Intro")
    col1, col2 = st.columns(2, gap="small")
    with col1:
        # main_image
        st.image("graphics/other/dungeon_crawler.png")

        st.caption(
            "The Dungeon: a streamlit dungeon crawler game", unsafe_allow_html=True
        )
    with col2:
        intro_text = """
        Explore the depths of an ancient dungeon in the first streamlit-based dungeon crawler game!
        Navigate through dangerous traps, defeat fearsome monsters and uncover the secrets of the DuNgeOn.
        With intuitive controls and beautiful graphics, this game will keep you entertained for hours.
        Experience the thrill of adventure as you progress through levels and uncover powerful treasures.
        Join the adventure today and become the hero of the dungeon!
        """
        st.write(f'<p style="color:#9c9d9f">{intro_text}</p>', unsafe_allow_html=True)
        audio_file = open("audio/intro.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mpeg")

    st.subheader("| Game start")
    st.write(
        '<p style="color:#9c9d9f">To start the game go to the "start game" tab.</p>',
        unsafe_allow_html=True,
    )
    st.subheader("| Controls")
    st.write(
        '<p style="color:#9c9d9f">Desktop: please use keyboard arrows | Mobile (Android, Chrome): please use on-screen buttons | iOS: unfortunately, the auto-scrolling feature does not work yet for iOS.</p><br>',
        unsafe_allow_html=True,
    )


with tab2:

    ####################################################
    #
    #            THIS PART RENDERS MAIN SCREEN
    #
    ####################################################

    html = level_renderer(
        st.session_state["level"],
        player + enemies + boxes + voids + torches + text_boxes + chests,
    )

    display_html = st.empty()

    if st.session_state["end"] == False:
        if st.session_state["player"].alive == True:
            display_html = st.markdown(html, unsafe_allow_html=True)
        else:
            display_html = st.markdown(
                "💀 The monster was more powerful than expected, resulting in your defeat in battle. Your journey has come to an unexpected end. To continue playing, please restart the app.",
                unsafe_allow_html=True,
            )
    if st.session_state["end"] == True:
        display_html = st.markdown(
            "Thank you for playing the demo of The Dungeon. More content coming soom!",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
        <div><br>
        <a href="https://www.buymeacoffee.com/tomjohn" style="color: grey; text-decoration:none;">
        <div style="justify-content: center;margin:0px; border:solid 2px;background-color: #0e1117; ;border-radius:10px; border-color:#21212f; width: fit-content;padding:0.425rem">
        <img src="https://raw.githubusercontent.com/TomJohnH/streamlit-game/main/images/coffe.png" style="max-width:20px;margin-right:10px;">
        Buy me a coffee</a></div></div>""",
            unsafe_allow_html=True,
        )

    st.button("L", on_click=left_callback, key="L")
    st.button("R", on_click=right_callback, key="R")
    st.button("U", on_click=up_callback, key="U")
    st.button("D", on_click=down_callback, key="D")

    # ------------------------------------------------------------
    #
    #                Game enigne - sidebar for backup input
    #
    # ------------------------------------------------------------

    # ------------ sidebar for backup input ---------------------------

    with st.sidebar:
        st.write("Use keyboard arrows or buttons below")
        st.markdown("<br>", unsafe_allow_html=True)
        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with middle_col:
            st.button("UP", on_click=up_callback, key="UP", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with left_col:
            st.button(
                "LEFT", on_click=left_callback, key="LEFT", use_container_width=True
            )

        with right_col:
            st.button(
                "RIGHT", on_click=right_callback, key="RIGHT", use_container_width=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with middle_col:
            st.button(
                "DOWN", on_click=down_callback, key="DOWN", use_container_width=True
            )

    # ------------------------------------------------------------
    #
    #               Game enigne - console div
    #
    # ------------------------------------------------------------

    st.markdown(
        f"""
        <div class="bpad" id="bpad">HP: {st.session_state["player"].hp}/20 | Gold: {st.session_state["player"].gold} | Exp: 0 </div>""",
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------
    #
    #               Game enigne - JS trickery
    #
    # ------------------------------------------------------------

    components.html(
        """
    <script>
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'L').classList.add('bbutton-left');
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'R').classList.add('bbutton-right');
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'U').classList.add('bbutton-up');
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'D').classList.add('bbutton-down');

    const doc = window.parent.document;
    buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));
    const left_button = buttons.find(el => el.innerText === 'LEFT');
    const right_button = buttons.find(el => el.innerText === 'RIGHT');
    const up_button = buttons.find(el => el.innerText === 'UP');
    const down_button = buttons.find(el => el.innerText === 'DOWN');

    const left_button2 = buttons.find(el => el.innerText === 'L');
    const right_button2 = buttons.find(el => el.innerText === 'R');
    const up_button2 = buttons.find(el => el.innerText === 'U');
    const down_button2 = buttons.find(el => el.innerText === 'D');


    doc.addEventListener('keydown', function(e) {
    switch (e.keyCode) {
        case 37: // (37 = left arrow)
            left_button.click();
            window.parent.document.getElementById('player').scrollIntoView();
            break;
        case 39: // (39 = right arrow)
            right_button.click();
            window.parent.document.getElementById('player').scrollIntoView();
            break;
        case 38: // (39 = right arrow)
            up_button.click();
            window.parent.document.getElementById('player').scrollIntoView();
            break;
        case 40: // (39 = right arrow)
            down_button.click();
            window.parent.document.getElementById('player').scrollIntoView();
            break;
    }
    });


    left_button.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("left")
    });

    right_button.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("right")
    });

    left_button2.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("left")
    });

    right_button2.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("right")
    });

    up_button.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("up")
    });

    down_button.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("down")
    });

    up_button2.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("up")
    });

    down_button2.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("down")
    });


    </script>
    """,
        height=0,
        width=0,
    )
