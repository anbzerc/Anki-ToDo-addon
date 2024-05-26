⚠️ Attention, this plugin is still in development. It's largely usable but may contain bugs. It's recommended to back up your collection before installing it. 😊

### Introduction
Let me introduce you to Anki Todo, a plugin designed to help you track your progress while learning from a list of decks. 📚 Its goal is simple: to allow you to manage multiple decks efficiently. You start by entering a list of decks you want to learn, and the plugin will pause all decks on the list except the first one. Once you've finished learning the first deck, Anki Todo will have you start learning the second one, and so on. 📝

Additionally, this plugin offers a handy feature: it displays your progress on the homepage for the first deck. 🏠 This allows you to keep an eye on your progress without having to navigate between different decks.

The plugin (especially the design) is not perfect (that's an understatement), so feel free to contribute or suggest features. 💡

### General Functionality:
This plugin works from a task list stored in the task.json file. The plugin looks at each deck in the task list, checks the total number of cards and the number of unseen cards. By comparing the two, it calculates if the deck's learning is complete. ✅

When the first deck is finished, it removes it from the task list and changes the second deck's configuration from paused to active learning. 🔄

### Configuration:
You need to specify a deck configuration called "pause configuration," which is a setup where no new cards are added each day. If you don't have one, create it. ⚙️

### Usage:
Aside from the progress screen on the homepage, everything happens in the Anki Todo window. To open it, go to the Tools tab, then Todo. This opens the Anki Todo window, which has four tabs:

#### Tabs:
- **Todo Tab:** The list of current tasks with the progress of the first task. 📋
- **Completed Tab:** The list of all decks that have been learned, not just with this plugin. 🏆
- **Settings Tab:** The settings 😉
- **Manage Tasks Tab:** The top part of this tab is for adding tasks, the bottom for removing them. 🔧
#### Adding a Task:
To add a task, select the deck, then select the future configuration, which is the setup that will be activated when the deck's learning begins. Then, just press the "Add Task" button to add the task. ➕

#### Deleting a Task:
To delete a task, select the task and press the "Delete" button. 🗑️

### Contributing:
Feel free to make pull requests. I'm available for any questions and to discuss improvements. 🤝

#### Acknowledgments:
Thanks to the entire Anki team for this great software and thanks to FooSoft (https://github.com/FooSoft) and their plugin Ankiconnect, which provided some very useful code snippets. 🙏
