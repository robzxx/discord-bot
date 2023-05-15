import asyncio
import nest_asyncio
nest_asyncio.apply()
from src.queue import Queue
from src.node import Node

import discord

intents = discord.Intents.all() # perm du bot

from discord.ext import commands

# Initialise notre Bot / Bienveue / msg alerte
Bot = commands.Bot(command_prefix='!') # préfix "!"

@Bot.event
async def on_ready():
    print(f'Bot {Bot.user.name} ON ({Bot.user.id})') # Print le nom du bot + le user id 

@Bot.event
async def on_typing(channel, user, when):
     await channel.send(user.name+" is typing") # user + est entrain d'écrire 

@Bot.event
async def on_member_join(member):
    general_channel = Bot.get_channel(1091260498613387267)
    await general_channel.send("Bienvenue sur le serveur ! "+ member.name) # user + bvn sur le serveur

@Bot.event
async def on_message(message):
  if message.author == Bot.user:
    return
  
  message.content = message.content.lower()

  if message.content.startswith(("hey","hi","hello", "bonjour", "salut", "wsh", "cc", "coucou")):
        await message.channel.send("Salut !")
  
  if message.content.startswith(("cv", "trkl", "ca va", "sa va", "ça va", "sa dit quoi")):
        await message.channel.send("Trkl et toi mon gars !")


## Historique

class Command:
    def __init__(self, command, user_id):
        self.command = command  # Attribut pour stocker la commande
        self.user_id = user_id  # Attribut pour stocker l'identifiant de l'utilisateur


class History:
    def __init__(self):
        self.queue = Queue()  # Crée une file d'attente vide pour stocker les commandes

    def add_command(self, command, user_id):
        new_command = Command(command, user_id)  # Crée un nouvel objet Command avec la commande et l'ID utilisateur spécifiés
        self.queue.put(new_command)  # Ajoute l'objet Command à la file d'attente

    
    def get_last_command(self):
        # Vérifie si la file n'est pas vide
        if not self.queue.empty():
            # Récupère la dernière commande de la file
            last_command = self.queue.queue[-1]

            # Construit un dictionnaire avec la commande et l'ID de l'utilisateur
            return {'commande': last_command.commande, 'user_id': last_command.user_id}
        else:
            # Retourne None si la file est vide
            return None

    def get_user_commands(self, user_id):
        user_commands = []  # Liste pour stocker les commandes de l'utilisateur
        for command in self.queue.queue:  # Parcourt toutes les commandes dans la file
            if command.user_id == user_id:  # Vérifie si l'ID utilisateur correspond
                user_commands.append({'command': command.command, 'user_id': command.user_id})  # Ajoute la commande à la liste
        return user_commands  # Retourne la liste des commandes de l'utilisateur

    def move_backwards(self, current_index):
        if current_index > 0:  # Vérifie si l'index actuel est supérieur à zéro
            return current_index - 1  # Décrémente l'index pour se déplacer vers l'arrière
        else:
            return current_index  # Renvoie l'index actuel si on est déjà au début de la file

    def move_forwards(self, current_index):
        if current_index < self.queue.qsize() - 1:  # Vérifie si l'index actuel est inférieur à la taille de la file - 1
            return current_index + 1  # Incrémente l'index pour se déplacer vers l'avant
        else:
            return current_index  # Renvoie l'index actuel si on est déjà à la fin de la file

    def clear_history(self):
        while not self.queue.empty():  # Tant que la file n'est pas vide
            self.queue.get()  # Retire et supprime chaque élément de la file




##### Questionnaire user - bot
class Node:
    def __init__(self, question, yes_node=None, no_node=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node

def ask_questions():
    # Création des nœuds de l'arbre avec les questions et les marques de voitures correspondantes
    q1 = Node("Est-ce que vous recherchez une voiture de luxe?")
    q2 = Node("Préférez-vous une voiture sportive?")
    q3 = Node("Est-ce que vous accordez de l'importance à la technologie embarquée?")
    q4 = Node("Préférez-vous une voiture de taille compacte?")
    q5 = Node("Est-ce que vous souhaitez une voiture électrique?")

    # Construction de l'arbre binaire
    q1.yes_node = q2
    q1.no_node = q3

    q2.yes_node = Node("Audi")
    q2.no_node = Node("BMW")

    q3.yes_node = Node("Mercedes")
    q3.no_node = q4

    q4.yes_node = Node("Audi")
    q4.no_node = q5

    q5.yes_node = Node("BMW")
    q5.no_node = Node("Mercedes")

    return q1

def start_conversation():
    # Construction de l'arbre
    root = ask_questions()
    current_node = root

    while True:
        # Demande à l'utilisateur de répondre à la question actuelle
        user_input = input(current_node.question + " (Oui/Non) ").lower()

        if user_input == "reset":
            # Si l'utilisateur entre "reset", on recommence la discussion à partir de la racine de l'arbre
            current_node = root
        elif user_input.startswith("speak about"):
            # Si l'utilisateur entre "speak about X", on vérifie si le sujet X est traité par le bot
            sujet = user_input.split("speak about ")[1]
            if check_sujet(sujet, root):
                print("Oui, je peux vous parler de " + sujet)
            else:
                print("Non, je ne peux pas vous parler de " + sujet)
        elif user_input == "oui":
            # Si l'utilisateur répond "oui", on passe au nœud de réponse "oui" suivant
            if current_node.yes_node is None:
                print("Je pense que vous devriez choisir une voiture de marque " + current_node.question + ".")
                break
            else:
                current_node = current_node.yes_node
        elif user_input == "non":
            # Si l'utilisateur répond "non", on passe au nœud de réponse "non" suivant
            if current_node.no_node is None:
                print("Je pense que vous devriez choisir une voiture de marque " + current_node.question + ".")
                break
            else:
                current_node = current_node.no_node
        else:
            # Si l'utilisateur entre une réponse invalide, on affiche un message d'erreur
            print("Veuillez répondre par 'oui', 'non', 'reset' ou 'speak about X'.")

def check_sujet(sujet, node):
    # Vérifie récursivement si le sujet est traité dans l'arbre
    if node is None:
        return False
    if node.question.lower() == sujet.lower():
        return True
    return check_sujet(sujet, node.yes_node) or check_sujet(sujet, node.no_node)

start_conversation()


## ADMIN COMMANDS
#ban
@Bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

#unban
@Bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

#kick
@Bot.command()
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

#clear
@Bot.command()
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()


### Gen un nombre entre 1 a 100 tombola 
@Bot.command()
async def Tambola(ctx):
    nombre = int(str(ctx.message.id)[-2:])
    await ctx.send(f"Le nombre généré est : {nombre}")


# token 
Bot.run("token")
