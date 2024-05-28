import functools
import json
import math
import pprint
import time

import anki.collection
import aqt.overview
from aqt import *
from aqt.operations import QueryOp
from aqt.utils import showInfo, showText
from aqt.webview import WebContent

# Append a path to sys.path in order to import element from other python files
import sys

# sys.path show a list of path, the first element of this list is the addons folder
# todo get propser folder name
print(sys.path)
path = sys.path[0]
platform = sys.platform
# Check if platform is window
if platform == "win32" :
    sys.path.append(path + "\\1807500231\\")
else:
    sys.path.append(path + "/1807500231/")
    print(sys.path)

from ToDoQtWindows import ToDoQtWindows

anki_version = tuple(int(segment) for segment in aqt.appVersion.split("."))


class Todo:

    # Get windows
    def window(self):
        return aqt.mw

    # Get user's collection
    def collection(self):
        collection = self.window().col
        if collection is None:
            raise Exception('collection is not available')

        return collection

    def get_path(self, name):
        if "win" in platform:
            return self.get_addon_path() + f"\\{name}"
        else:
            return self.get_addon_path() + f"/{name}"

    def get_deck_names(self):
        names_list = []
        for e in self.window().col.decks.all_names_and_ids():
            names_list.append(e.name)
        # print(names_list)
        return names_list

    def scheduler(self):
        scheduler = self.collection().sched
        if scheduler is None:
            raise Exception('scheduler is not available')
        return scheduler

    def collectDeckTreeChildren(self, parent_node):
        allNodes = {parent_node.deck_id: parent_node}
        for child in parent_node.children:
            for deckId, childNode in self.collectDeckTreeChildren(child).items():
                allNodes[deckId] = childNode
        return allNodes

    def deckStatsToJson(self, due_tree):
        name = self.collection().decks.name(due_tree.deck_id)
        total_card_number = len(self.collection().find_cards(f'"deck:{name}"'))
        unseen_card_number = len(self.collection().find_cards(f'"deck:{name}" is:new'))
        card_in_learning = len(self.collection().find_cards(f'"deck:{name}" is:learn'))
        suspended_cards = len(self.collection().find_cards(f'"deck:{name}" is:suspended'))
        known_cards = total_card_number - unseen_card_number
        deckStats = {'deck_id': due_tree.deck_id,
                     'name': due_tree.name,
                     'total': total_card_number,
                     'unseen': unseen_card_number,
                     'inlearning': card_in_learning,
                     'suspended': suspended_cards,
                     'known': known_cards
                     }

        return deckStats

    def deckStatsToJsonByName(self, name):
        total_card_number = len(self.collection().find_cards(f'"deck:{name}"'))
        unseen_card_number = len(self.collection().find_cards(f'"deck:{name}" is:new'))
        card_in_learning = len(self.collection().find_cards(f'"deck:{name}" is:learn'))
        suspended_cards = len(self.collection().find_cards(f'"deck:{name}" is:suspended'))
        known_cards = total_card_number - unseen_card_number
        deckStats = {'deck_id': self.collection().decks.id(name),
                     'name': name,
                     'total': total_card_number,
                     'unseen': unseen_card_number,
                     'inlearning': card_in_learning,
                     'suspended': suspended_cards,
                     'known': known_cards
                     }

        return deckStats

    def get_deck_stats(self, decks: list):
        collection = self.collection()
        scheduler = self.scheduler()
        responseDict = {}
        deckIds = list(map(lambda d: collection.decks.id(d), decks))
        allDeckNodes = self.collectDeckTreeChildren(scheduler.deck_due_tree())
        for deckId, deckNode in allDeckNodes.items():
            if deckId in deckIds:
                responseDict[collection.decks.name(deckId)] = self.deckStatsToJson(deckNode)
        return responseDict

    def get_addon_path(self):
        return mw.addonManager.addonsFolder("1807500231")

    def add_new_deck_to_task(self, deck, config):
        # Add to json
        with open(self.get_path("user_files/task.json")) as f:
            tasks_json = json.load(f)
            pause_id = int(tasks_json["config"]["pauseConfigId"])
        tasks_json["tasks"][deck] = config
        with open(self.get_path("user_files/task.json"), "w") as f:
            json.dump(tasks_json, f)

        # Check that the deck isn't the only one in tasks
        if len(tasks_json["tasks"]) > 1:
            # Set pause config
            self.setDeckConfigId([deck], pause_id)

    def move_deck_to_completed(self, deck):
        with open(self.get_path("user_files/task.json")) as f:
            tasks_json = json.load(f)
        if deck in list(tasks_json["tasks"].keys()):
            del tasks_json["tasks"][deck]
        with open(self.get_path("user_files/task.json"), "w") as f:
            json.dump(tasks_json, f)

    def get_all_task(self) -> list:
        with open(self.get_path("user_files/task.json")) as f:
            tasks_json = json.load(f)
        return list(tasks_json["tasks"].keys())
        # return tasks_json["tasks"]

    def get_all_completed(self) -> list:
        completed_list = []
        decks_stats = self.get_deck_stats(self.get_deck_names())
        for key, value in decks_stats.items():
            if value["unseen"] == 0:
                completed_list.append(key)

        return completed_list

    def getDeckConfig(self, deck):
        if deck not in self.get_deck_names():
            return False
        collection = self.collection()
        did = collection.decks.id(deck)
        return collection.decks.config_dict_for_deck_id(did)

    def getAllDeckConfig(self):
        decks = self.get_deck_names()
        configs = []
        for e in decks:
            configs.append(self.getDeckConfig(e))

        # removing duplicates
        return list(set(configs))

    def removeTask(self, task):
        with open(self.get_path("user_files/task.json")) as f:
            tasks_json = json.load(f)
        try:
            del tasks_json["tasks"][task]
            with open(self.get_path("user_files/task.json"), "w") as f:
                json.dump(tasks_json, f)
        except Exception as error:
            print("Error removing task", error)

    def getAllDeckConfigNames(self) -> dict:
        decks = self.get_deck_names()
        configs = {}
        for e in decks:
            configs[self.getDeckConfig(e)["name"]] = self.getDeckConfig(e)["id"]
        # removing duplicates
        return configs

    def setPauseConfig(self, config, cid):
        with open(self.get_path("user_files/task.json")) as f:
            tasks_json = json.load(f)
        tasks_json["config"]["pauseConfig"] = config
        tasks_json["config"]["pauseConfigId"] = cid
        with open(self.get_path("user_files/task.json"), "w") as f:
            json.dump(tasks_json, f)

    def remaining_days(self, deck, number_of_unseen_cards):
        with open(self.get_path("user_files/task.json")) as f:
            tasks_json = json.load(f)
        if deck in tasks_json["tasks"]:
            deck_config_id = tasks_json["tasks"][deck]
        else:
            deck_config_id = self.collection().decks.config_dict_for_deck_id(self.collection().decks.id(deck))["id"]
        deck_config = self.collection().decks.get_config(deck_config_id)
        new_cards = int(deck_config["new"]["perDay"])
        if new_cards == 0:
            return 0
        return math.ceil(number_of_unseen_cards / new_cards)

    def checkIfTaskDone(self) -> str:
        tasks = self.get_all_task()
        for e in tasks:
            stat = self.deckStatsToJsonByName(e)
            print(e, stat)
            # If deck is done, remove it from task list
            if stat["unseen"] == 0:

                # Enable the folowing deck
                deck_index = tasks.index(e)
                print(f"len {len(tasks)} index {deck_index+1}")
                # Check that deck isn't the last in tasks
                if len(tasks) > deck_index + 1:
                    with open(self.get_path("user_files/task.json")) as f:
                        config = json.load(f)
                        did = int(config["tasks"][tasks[deck_index+1]])
                    self.setDeckConfigId([tasks[deck_index+1]], did)
                    # Move deck to completed
                    self.move_deck_to_completed(e)
                    self.successfully_moved_deck(e)
                else:
                    self.move_deck_to_completed(e)
                    self.successfully_moved_deck(e)
                return e
        print("No done task")

    def setDeckConfigId(self, decks, configId):
        configId = int(configId)
        for deck in decks:
            if not deck in self.get_deck_names():
                return False

        collection = self.collection()

        for deck in decks:
            try:
                did = str(collection.decks.id(deck))
                deck_dict = aqt.mw.col.decks.decks[did]
                deck_dict['conf'] = configId
                collection.decks.save(deck_dict)
            except:
                return False

        return True

    def backgroundSave(self, *args):
        # Not working
        # To implement later ;)
        print("\n Saving collection ...")
        saving = QueryOp(
            parent=mw,
            op=lambda col: self.collection().save(),
            success=lambda col: print("Collection saved\n"),
        )
        saving.run_in_background()

    def runBackgroundCheck(self, *args):
        print("Checking if there are done tasks")
        self.checkIfTaskDone()
        # We accept several args because the callback give many args
        op = QueryOp(
            parent=mw,
            op=lambda col: self.checkIfTaskDone,
            success=lambda col: self.successfully_moved_deck,
        )
        #op.run_in_background()

    pass

    def successfully_moved_deck(self, deck) -> None:
        showInfo(f"Congratulation ! You'd learnt all cards in {deck}")

    def render_tasks(self, deck_list):
        # display blank is there's no tasks
        if len(deck_list) == 0:
            # Open html div
            final_HTML = """
                                            <div class="todo">
                                            <div class="column">
                                            """
            final_HTML += """<div class="element"><h3 class="decktitle">Time to add some tasks...</h3></div>
            """
            # Add style
            with open(self.get_path("style.html")) as f:
                final_HTML += f.read()
                f.close()
            # Close html div
            final_HTML += """
                                                </div>
                                            </div>
                                            """

            return final_HTML
        completed = self.get_all_completed()
        if isinstance(deck_list[0], list):
            finals_HTML = []
            for deck_element in deck_list:
                tasks = deck_element

                stats = self.get_deck_stats(self.get_deck_names())  # self.get_deck_names())
                final_HTML = """"""
                # add progress bar library
                with open(self.get_path("progressbarLibrary.html")) as f:
                    final_HTML += f.read()

                # Open html div
                final_HTML += """
                                <div class="todo">
                                <div class="column">
                                """

                with open(self.get_path("FirstElement.html")) as f:
                    base_element = f.read()

                for e in tasks:

                    # Get element stats dict
                    element_stats = stats[e]

                    # check element is the first task because it's different html
                    if e in completed:
                        pourcentage = 100
                    # Get deck progression
                    else:
                        pourcentage = round(
                            (element_stats["total"] - element_stats["unseen"]) / element_stats["total"] * 100,
                            1)

                    element_html = base_element
                    element_html = element_html.replace("DECKTITLE", self.collection().decks.basename(e))
                    element_html = element_html.replace("POURCENTAGEVALUE", f"{pourcentage}")

                    if tasks.index(e) == 0:
                        element_html = element_html.replace('class="example"', 'class="firstelementprogressbar"')
                        element_html = element_html.replace("REMAINING",
                                                            str(self.remaining_days(e, element_stats["unseen"]))+"remaining days")
                    else:
                        element_html = element_html.replace("REMAINING",
                                                            str(self.remaining_days(e, element_stats["unseen"]))+" days estimated")
                    final_HTML += element_html

                # Add style
                with open(self.get_path("style.html")) as f:
                    final_HTML += f.read()
                    f.close()
                # Close html div
                final_HTML += """
                                    </div>
                                </div>
                                """

                finals_HTML.append(final_HTML)

            return finals_HTML
        else:

            tasks = deck_list

            stats = self.get_deck_stats(self.get_deck_names())  # self.get_deck_names())
            final_HTML = """"""

            # add progress bar library
            with open(self.get_path("progressbarLibrary.html")) as f:
                final_HTML += f.read()

            # Open html div
            final_HTML += """
                    <div class="todo">
                    <div class="column">
                    """

            with open(self.get_path("FirstElement.html")) as f:
                base_element = f.read()

            for e in tasks:

                # Get element stats dict
                element_stats = stats[e]
                # Todo estimation jours restants avec config du deck
                # check element is the first task because it's different html
                # Get deck progression
                if e in completed:
                    pourcentage = 100
                # Get deck progression
                else:
                    pourcentage = round(
                        (element_stats["total"] - element_stats["unseen"]) / element_stats["total"] * 100,
                        1)

                element_html = base_element
                element_html = element_html.replace("DECKTITLE", self.collection().decks.basename(e))
                element_html = element_html.replace("POURCENTAGEVALUE", f"{pourcentage}")

                if tasks.index(e) == 0:
                    element_html = element_html.replace('class="example"', 'class="firstelementprogressbar"')
                    element_html = element_html.replace("REMAINING",
                                                        str(self.remaining_days(e, element_stats[
                                                            "unseen"])) + " days remaining")
                else:
                    element_html = element_html.replace("REMAINING",
                                                        str(self.remaining_days(e, element_stats[
                                                            "unseen"])) + " days estimated")
                final_HTML += element_html

            # Add style
            with open(self.get_path("style.html")) as f:
                final_HTML += f.read()
                f.close()
            # Close html div
            final_HTML += """
                        </div>
                    </div>
                    """

            return final_HTML


todo = Todo()


def show_to_do_window():
    pprint.pp(todo.collection().decks.get_config(1682080877248))
    mw.toDoWindows = toDoWindows = ToDoQtWindows(todo, mw)
    toDoWindows.show()


def on_webview_will_set_content(web_content, context):
    # Vérifier si le contexte est la page d'accueil
    body = web_content.body
    splited = body.split("<center>")
    # Ajouter du HTML personnalisé avant la balise de fermeture </body>
    if len(splited) > 1:
        web_content.body = body.split("<center>")[0] + "<center>" + todo.render_tasks(todo.get_all_task()) + \
                           body.split("<center>")[1]


def register_webview():
    # Save collection to prevent problems
    todo.collection().save()
    gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
    # Add deck progression check to operation_did_execute hook
    gui_hooks.operation_did_execute.append(functools.partial(todo.backgroundSave))
    gui_hooks.operation_did_execute.append(functools.partial(todo.runBackgroundCheck))
    # show_to_do_window()


gui_hooks.main_window_did_init.append(register_webview)

# create a new menu item, "test"
action = QAction("Todo", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, show_to_do_window)
# and add it to the tools menu

mw.form.menuTools.addAction(action)
