import json
import pprint

import anki.collection
import aqt.overview
from aqt import *
from aqt.utils import showInfo, showText
from aqt.gui_hooks import overview_will_render_content
from aqt.webview import WebContent

anki_version = tuple(int(segment) for segment in aqt.appVersion.split("."))


class Todo:

    # Get windows
    def window(self):
        return aqt.mw

    #Get user's collection
    def collection(self):
        collection = self.window().col
        if collection is None:
            raise Exception('collection is not available')

        return collection

    def get_deck_names(self):
        names_list = self.window().col.decks.all_names()
        print(names_list)
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

    def deckStatsToJson(self, due_tree, collection: Collection):
        name = self.collection().decks.name(due_tree.deck_id)
        if "::" in name:
            total_card_number = len(collection.find_cards(f'"deck:{name}"'))
            unseen_card_number = len(collection.find_cards(f'"deck:{name}" is:new'))
            card_in_learning = len(collection.find_cards(f'"deck:{name}" is:learn'))
            suspended_cards = len(collection.find_cards(f'"deck:{name}" is:suspended'))
            known_cards = total_card_number - unseen_card_number
            deckStats = {'deck_id': due_tree.deck_id,
                         'name': due_tree.name,
                         'total': total_card_number,
                         'unseen': unseen_card_number,
                         'inlearning': card_in_learning,
                         'suspended': suspended_cards,
                         'known': known_cards
                         }
        else:
            total_card_number = len(collection.find_cards(f'deck:{name}'))
            unseen_card_number = len(collection.find_cards(f'deck:{name} is:new'))
            card_in_learning = len(collection.find_cards(f'deck:{name} is:learn'))
            suspended_cards = len(collection.find_cards(f'deck:{name} is:suspended'))
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

    def get_deck_stats(self, decks):
        collection = self.collection()
        scheduler = self.scheduler()
        responseDict = {}
        deckIds = list(map(lambda d: collection.decks.id(d), decks))
        allDeckNodes = self.collectDeckTreeChildren(scheduler.deck_due_tree())
        for deckId, deckNode in allDeckNodes.items():
            if deckId in deckIds:
                responseDict[collection.decks.name(deckId)] = self.deckStatsToJson(deckNode, collection)
        return responseDict

    def get_addon_path(self):
        return mw.addonManager.addonsFolder("todo")

    def add_new_deck_to_task(self, deck):
        with open(f"{self.get_addon_path()}/task.json") as f:
            tasks_json = json.load(f)
        tasks_json["tasks"].append(deck)
        with open(f"{self.get_addon_path()}/task.json", "w") as f:
            json.dump(tasks_json, f)

    def move_deck_to_completed(self, deck):
        with open(f"{self.get_addon_path()}/task.json") as f:
            tasks_json = json.load(f)
        if deck in tasks_json["tasks"]:
            tasks_json["tasks"].remove(deck)
        tasks_json["completed"].append(deck)
        with open(f"{self.get_addon_path()}/task.json", "w") as f:
            json.dump(tasks_json, f)

    def get_all_task(self) -> list:
        with open(f"{self.get_addon_path()}/task.json") as f:
            tasks_json = json.load(f)
        return tasks_json["tasks"]

    def get_all_completed(self) -> list:
        with open(f"{self.get_addon_path()}/task.json") as f:
            tasks_json = json.load(f)
        return tasks_json["completed"]

    def render_tasks(self):
        tasks = self.get_all_task()
        completed = self.get_all_completed()
        stats = self.get_deck_stats(self.get_deck_names())
        print("stats")
        pprint.pp(stats)
        final_HTML = """"""

        # add progress bar library
        with open(f"{self.get_addon_path()}/progressbarLibrary.html") as f:
            final_HTML += f.read()

        # Open html div
        final_HTML += """
        <div class="todo">
        <div class="column">
        """
        for e in tasks:
            # Get element stats dict
            element_stats = stats[e]
            # Todo estimation jours restants avec config du deck
            # check element is the first task because it's different html
            if tasks.index(e) == 0:
                # Get deck progression
                pourcentage = round((element_stats["total"] - element_stats["unseen"]) / element_stats["total"] * 100,
                                    1)
                with open(f"{self.get_addon_path()}/FirstElement.html") as f:
                    element_html = f.read()
                print(element_html)
                element_html = element_html.replace("DECKTITLE", self.collection().decks.basename(e))
                element_html = element_html.replace("REMAINING", "soon")
                element_html = element_html.replace("POURCENTAGEVALUE", f"{pourcentage}")
                final_HTML += element_html
                continue
            else:
                with open(f"{self.get_addon_path()}/baseElement.html") as f:
                    element_html = f.read()
                element_html = element_html.replace("DECKTITLE", self.collection().decks.basename(e))
                element_html = element_html.replace("REMAINING", "soon")
                final_HTML += element_html

        # Add style
        with open(f"{self.get_addon_path()}/style.html") as f:
            final_HTML += f.read()

        # Close html div
        final_HTML += """
            </div>
        </div>
        """

        with open(f"{self.get_addon_path()}/test.html", "w") as f:
            f.write(final_HTML)

        return final_HTML



todo = Todo()

def on_webview_will_set_content(web_content: WebContent, context) -> None:

    web_content.body = web_content.body.split("<center>")[0] + "<center>" + todo.render_tasks() + web_content.body.split("<center>")[1]
    addon_package = mw.addonManager.addonFromModule(__name__)
    web_content.css.append(f"/_addons/{addon_package}/web/my-addon.css")
    web_content.js.append(f"/_addons/{addon_package}/web/my-addon.js")

def show_html():
    decks = todo.get_deck_names()
    showText(str(todo.get_deck_stats(decks).values()))

overview_will_render_content(on_webview_will_set_content())
# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, todo.render_tasks)
# and add it to the tools menu

mw.form.menuTools.addAction(action)
