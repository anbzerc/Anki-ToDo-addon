import json
import pprint

import anki.collection
import aqt.overview
from aqt import *
from aqt.utils import showInfo, showText

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
        total_card_number = len(collection.findCards(f'deck:"{due_tree.name}"'))
        unseen_card_number = len(collection.findCards(f'deck:"{due_tree.name}" is:new'))
        card_in_learning = len(collection.findCards(f'deck:"{due_tree.name}" is:learn'))
        suspended_cards = len(collection.findCards(f'deck:"{due_tree.name}" is:suspended'))
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
                responseDict[deckId] = self.deckStatsToJson(deckNode, collection)
        return responseDict


todo = Todo()


def show_html():
    decks = todo.get_deck_names()
    with open("/home/tim/PycharmProjects/Anki-ToDo-addon/test.txt") as f:
            f.write(str(aqt.overview.OverviewContent.table))
    showText(str(todo.get_deck_stats(decks).values()))


# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, show_html)
# and add it to the tools menu

mw.form.menuTools.addAction(action)

