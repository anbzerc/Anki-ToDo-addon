import json
import pprint


def get_deck_name_id_list():
    #deck_json = str(mw.col.decks.deck_tree())
    with open("/home/tim/PycharmProjects/Anki-ToDo-addon/test.txt") as f:
        deck_json = "{"+f.read()+"}"
        # convert to json
        deck_json = deck_json.replace("children", '"children" :')
        deck_json = deck_json.replace("name", '"name" ')
        deck_json = deck_json.replace("level", '"level" ')
        deck_json = deck_json.replace("collapsed", '"collapsed" ')
        deck_json = deck_json.replace("deck_id", '"collapsed" ')
        deck_json = deck_json.replace("true", '"true" ')
        #Split str line by line
        line_list = deck_json.splitlines()

        # Set list of character we don't have to add comma
        banned_character = ["{", ","]
        #Iterate over to add required comma
        counter = 0
        for element in line_list:
            # Check if our element isn't the end of a dic
            if element[-1] == '}':
                # check if the next line is also a } bracket
                if "}" in line_list[counter+1] :
                    #line_list[counter + 1]+=","
                    continue
            if element != "":
                if element[-1] not in banned_character:
                    print("YESSSS", element[-1])
                    line_list[counter] = element+","
            counter += 1

        final = "".join(line_list)
        pprint.pprint("".join(line_list))
        print("pb",final[210:])
        json.loads(final)

    return deck_json

get_deck_name_id_list()