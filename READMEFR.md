⚠️ Attention, ce plugin est encore en developpement, il reste largement utilisable mais peut comporter des bugs. Il est recommandé de faire une sauvegarde de votre collection avant de l'installer
### Présentation
Je vous présente Anki Todo, un plugin conçu pour vous aider à suivre votre progression dans l'apprentissage d'une liste de decks. Son objectif est simple : vous permettre de gérer efficacement plusieurs decks simultanément. Vous commencez par entrer une liste de decks à apprendre, et le plugin se charge de mettre en pause tous les decks de la liste, à l'exception du premier. Une fois que vous avez terminé d'apprendre le premier deck, Anki Todo vous fait commencer à apprendre le deuxième, et ainsi de suite.

De plus, ce plugin offre une fonctionnalité pratique : il affiche votre progression dans l'apprentissage du premier deck directement sur la page d'accueil. Cela vous permet de garder un œil sur votre avancement sans avoir à naviguer entre les différents decks.

Le plugin (le design notamment) n'est pas encore parfait (c'est un euphémisme) donc n'hésitez pas à contribuer ou à proposer des fonctionnalités. 

#### Fonctionnement général : 
Ce plugin fonctionne sur une à partir d'une liste de tâches qui est stockée dans le fichier task.json. Le plugin va regarder pour chaque deck qui est dans la liste de tâches, le nombre de cartes total et le nombre de cartes qui n'ont pas été vues. C'est en faisant la différence entre les 2 qu'il calcule si l'apprentissage du deck est fini. 

Quand l'apprentissage du premier deck est fini, il le supprime de la liste de tâches et change la configuration du 2e deck de la liste de tâches de la configuration pause à la configuration d'apprentissage. 

 

### Configuration :  

Vous devez préciser une configuration de deck appelée configuration pause, qui est une configuration dans laquelle il n'y a pas de nouvelle carte chaque jour. Si vous n'en avez pas créez la. 

### Utilisation :  

Hormis l'écran de progression sur la page d'accueil, tout se fait dans la fenêtre Anki-Todo. Pour l'ouvrir allez dans l'onglet outils, puis todo. Cela va ouvrir la fenêtre de Anki-Todo. Cette fenêtre comporte 4 onglets : 

#### Onglets :
* **Onglet todo** : la liste des tâches en cours avec la progression de la première tâche. 

* **Onglet completed** : La liste de tous les decks qui ont été appris. Pas uniquement avec le plugin. 

* **Onglet settings** : les settings 😉 

* **Onglet Manage Tasks** : Le haut de cet onglet sert à ajouter des tâches, le bas à en supprimer.  

#### Ajouter une tâche : 

Pour ajouter une tâche, sélectionnez le deck, puis sélectionnez la configuration future,  c'est-à-dire la configuration qui sera activée lorsque l'apprentissage du deck sera démarré. Il ne vous reste qu'alors qu'à appuyer sur le bouton ajouter une tâche pour ajouter la tâche.  

#### Supprimer une tâche : 

Pour supprimer une tâche, sélectionnez ladite tâche et appuyez sur le bouton supprimer. 

### Contribuer :

N'hésitez pas à faire des pull request. Je suis disponible si besoin de précision et pour discuter des améliorations
