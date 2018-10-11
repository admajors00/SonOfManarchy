# Son Of Manarchy Part 1
from anytree import Node, RenderTree, NodeMixin, AsciiStyle, Walker
from random import*
import random
from tkinter import*
import os

commands = ['help', 'search', 'take', 'my stats', "items stats", 'move', 'talk', 'continue', 'attack', 'buy', 'equip']
states = ['safe', 'neutral', 'dangerous']
# safe means cannot attack anyone no one can attack you
# neutral means you wont be attacked unless you attack someone else
# dangerous means you will randomly be attack by others
area_types = ['shop', 'route', 'outdoors', 'indoors']
x = 0
place = 0
pos = 0
user_inputs = []
save_path = []


class Items:
    def __init__(self, name, ap, dp, weight, price, spec, hit_chance):
        self.name = name
        self.ap = ap
        self.dp = dp
        self.weight = weight
        self.price = price
        self.spec = spec
        self.hit_chance = hit_chance
        all_items.append(self.name)
all_items = []


class Characters:

    def __init__(self, name, ap, dp, carry_weight, money, hp):
        self.name = name
        self.ap = ap
        self.dp = dp
        self.carry_weight = carry_weight
        self.money = money
        self.hp = hp
        self.life = True
        self.items = []
        self.reply = []
        self.speechop = []
        self.choice = ''
        self.equipped = dagger.name
        all_characters.append(self.name)
all_characters = []


class You:
    def __init__(self, name, ap, dp, carry_weight, money, state, area, life, hp):
        self.name = name
        self.ap = ap
        self.dp = dp
        self.carry_weight = carry_weight
        self.money = money
        self.state = state
        self.area = area
        self.life = life
        self.hp = hp
        self.items = []
        self.choice = []
        self.node = ''


class Areas:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.items = []
        self.people = []
        self.directions = {}
        self.shopitems = []
areas = []


class Decision(NodeMixin):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.statement = ''
        self.choices = ''
        self.next = ''
        self.hascode = False
        self.code = ''

# Items
quote_gun = Items('quote_gun', 20, 8, 10, 175, 'This gun is Jeb Bushes only weakness', 95)
dagger = Items('dagger', 5, 0, 3, 7, '', 80)
Unrelenting_Failure = Items('Unrelenting_Failure', 15, 4, 10, 20, '', 89)
simple_helmet = Items('simple_helmet', 0, 8, 8, 3, '', 0)
Book = Items('Book', 0, 0, 2, 4, 'This book will take you far', 0)
How_to_Coach_by_Herb = Items('How_to_Coach_by_Herb', 0, 0, 2, 10, 'AGAIN', 0)
really_big_knife = Items('really_big_knife', 25, 2, 0, 50, '(Austrailian accent)Now thats a knife!', 89)
fathers_lightsaber = Items('fathers_lightsaber', 30, 8, 0, 60000, 'Left behind by your father right before he disappeared', 95)
common_pistol = Items('common_pistol', 4, 0, 5, 5, '', 80)
PLS_Clap = Items('PLS_Clap', 20, 7, 10, 200, '', 95)
fidget_spinner = Items('fidget_spinner', 0, 0, 0, 6, 'This may just solve all of the worlds problems', 100)
umbrella = Items('umbrella', 4, 8, 8, 20, 'cant stop the rain', 85)
tazer = Items('tazer', 6, 0, 0, 20, 'Its effects are electrifying!', 85)
sharp_stick = Items('sharp_stick', 15, 0, 0, 40, 'A man with a sharp stick and nothing left to lose can win the day!', 92)
machete = Items('machete', 15, 2, 0, 9, 'Machete very cheap, 9 cents a piece', 89)
leather_armor = Items('leather_armor', 0, 10, 0, 15, 'Made from rabbits', 0)
fashionable_hat = Items('fashionable_hat', 0, 0, 0, 50, 'Doesnt do much for you but it sure does look nice', 0)
military_grade_armor = Items('military_grade_armor', 0, 35, 0, 55, 'Armor of worriors', 0)
makeshift_armor = Items('makeshift_armor', 0, 13, 0, 10, 'Its falling apart but better than nothing.', 0)
diamond_armor = Items('diamond_armor', 10, 60, 0, 10000, 'Notch would be proud', 100)


# Characters
# all_characters.append()
Sarah_Gooch = Characters('Sarah_Gooch', 10, 10, 10, 10, 100)
Sarah_Gooch.items = [dagger.name]
Sarah_Gooch.speechop = {'wake_up': ["0: What is going on?",
                                    "1: What does he want?"],
                        'suspicious': ['0: (whispering) What do you think?'],
                        'believe_mom': ['0: Now what?',
                                        '1: What do we do?',
                                        '2: Ok now what?'],
                        'believe_will': ['0: He is not a crook. He told me so.']}
Sarah_Gooch.reply = {'wake_up': ["There is a soldier here saying he is with the Liberlandian Malitia.",
                                 "He is saying they need some information about your father."],
                     'suspicious': ["Mom:(whispering very loud) I don't think we should trust these guys"
                                    " I'm pretty sure they're impostors. *"],
                     'believe_mom': ['Now this is where the fun begins.',
                                     'Go into the closet and theres some stuff your dad left that you will need',
                                     'Now head over to Herbs house and wait for me*'],
                     'believe_will': ['Your going to get us killed'],
                     'run_jeb': ['']}


private_williams = Characters('private_williams', 50, 60, 100, 100, 100)
private_williams.items = [simple_helmet.name, dagger.name]
private_williams.speechop = {'wake_up': ["0: What do you need us for?",
                                         "1: Why should we do that?",
                                         "2: What do you need with my dad?"],
                             'suspicious': ['0: Are you a crook?'],
                             'believe_will': ['0: Ok lets go.'],
                             'believe_mom': ["0: You can't hear us plotting aginst you can you?"],
                             'goto_armybase': ['0: What am I supposed to do here?',
                                               "1: And if I dont?"]}

private_williams.reply = {'wake_up': ["I need both of you to come with me right now. ",
                                      "Because it concerns the whereabouts of your father The Gooch",
                                      "Hes the only one that can bring balance to our land*"],
                          'suspicious': ['I am not a crook!'],
                          'believe_will': ['Great follow me*'],
                          'beleive_mom': ['Nahhh Dude'],
                          'goto_armybase': ['Just sit on that bench and dont go into the hq_tent',
                                            "Well then you are lost!*"]}

private_williams.equipped = common_pistol.name

Donald_Trump = Characters('Donald_Trump', 80, 60, 100, 10, 250)
Donald_Trump.items = [quote_gun.name]
Donald_Trump.equipped = quote_gun.name

Jeb_Bush = Characters('Jeb_Bush', 70, 60, 90, 9, 200)
Jeb_Bush.items = []
Jeb_Bush.equipped = PLS_Clap.name

Herb = Characters('Herb', 20, 20, 20, 1000, 100)
Herb.items = [How_to_Coach_by_Herb.name]
Herb.equipped = dagger.name
Herb.speechop = {'talk_herb': ['0: Hey Herb.',
                               '1: just before they took my mom she told me to come here',
                               '2: You are the only one that can help please',
                               '3: I AM THE SON OF THE GOOCH AND I PLAY FOR LIBERLAND, FOR MANARCHY!!']}
Herb.reply = {'talk_herb': ['Get out of my face I am to busy planning my hockey team ',
                            'Didnt you hear me kid',
                            'I SAID GET OUT OF MY FACE! NOW GET ON THE GOAL LINE!',
                            'Okay kid why dont you talk to this other kid he might be able to tell you something.*']}


herbs_kid = Characters('herbs_kid', 15, 21, 20, 10, 100)
herbs_kid.items = [fidget_spinner.name]
herbs_kid.speechop = {'talk_kid': ['0: Who are you dude?',
                                   '1: Whats your name?',
                                   '2: Can you help me find my dad and my mother.',
                                   '3: where exactly in the badlands are they?'
                                   '4: Anything else?']}
herbs_kid.reply = {'talk_kid': ['I am Herbs kid',
                                'I dunno he was too busy to give me a name i guess.',
                                'Sure the Gist army took my mom once my dada didnt notice so i had to find her. \n'
                                    'you need to head through the badlands and find the Chrisleegion.\n '
                                    'They are the ones who know whats going on',
                                 "they're on the far eastern side in the top of mount Mustafar."
                                    " You'll have to go through some maze too.",
                                "Yeah if you go across the street I work the sh and could sell you some equipment.*"]}

hutu_soldier = Characters('hutu_soldier', 17, 20, 20, 10, 100)
hutu_soldier.items = [dagger.name]
hutu_soldier.equipped = common_pistol.name


# User
user = You('Andrew', 10, 10, 10, 10, 'safe', 'room', True, 100)
user.items = []
user.equipped = dagger.name

# Areas
# areas.append()
blocked = "You can't go that way"
N = "North"
S = "South"
E = "East"
W = "West"
room = Areas('room', 'Safe')
room.items = [Book.name, dagger.name]
room.directions = {N: blocked, E: blocked, S: 'downstairs', W: blocked}
areas.append(room.name)

downstairs = Areas('downstairs', 'Safe')
downstairs.people = [Sarah_Gooch.name, private_williams.name]
downstairs.items = [Book.name]
downstairs.directions = {N: 'room', E: 'Steamtown', S: 'closet', W: 'back_door'}
areas.append(downstairs.name)

back_door = Areas('back_door', 'dangerous')
back_door.directions = {N: 'Herbs_house', S: '', E: 'downstairs', W: 'badlands'}
back_door.people = [hutu_soldier.name]

closet = Areas('closet', 'safe')
closet.items = [simple_helmet.name, dagger.name, Unrelenting_Failure.name, fathers_lightsaber.name, makeshift_armor.name]
closet.directions = {N: blocked, E: blocked, S: 'downstairs', W: blocked}
areas.append(closet.name)

Steamtown = Areas('Steamtown', 'neutral')
Steamtown.people = [private_williams.name]
Steamtown.items = all_items
Steamtown.directions = {N: "main_street_north", E: "army_base", S: "main_street_south", W: "downstairs" }
areas.append(Steamtown.name)

army_base = Areas('army_base', 'neutral')
army_base.people = [private_williams.name, hutu_soldier.name, hutu_soldier.name, hutu_soldier.name, hutu_soldier.name]
army_base.directions = {E: 'army_truck', S: 'hq_tent', W: 'Steamtown', N: blocked}
areas.append(army_base.name)

hq_tent = Areas('hq_tent', 'neutral')
hq_tent.people = [Donald_Trump.name, Jeb_Bush.name]
hq_tent.directions = {N: 'army_base', S: blocked, E: blocked, W: blocked}
areas.append(hq_tent.name)

army_truck = Areas('army_truck', 'neutral')
army_truck.people = [private_williams.name, hutu_soldier, hutu_soldier, hutu_soldier, hutu_soldier]
army_truck.directions = {W: 'Steamtown'}

main_street_north = Areas('main_street_north', 'neutral')
main_street_north.directions = {N: 'somewhere', E: 'main_street_north_shop', S: 'Steamtown', W: 'Herbs_house'}
main_street_north.items = []

main_street_north_shop = Areas('main_street_north_shop', 'shop')
main_street_north_shop.directions = {N: blocked, S: blocked, E: blocked, W: 'main_street_north'}
main_street_north_shop.people = [Herb.name]
main_street_north_shop.shopitems = ['dagger', 'Unrelenting_Failure', 'simple_helmet', 'Book', 'How_to_Coach_by_Herb', 'really_big_knife', 'common_pistol',
                                    'fidget_spinner', 'umbrella', 'tazer', 'sharp_stick', 'machete', 'leather_armor', 'fashionable_hat',]

Herbs_house = Areas("Herbs_house", 'safe')
Herbs_house.items = [How_to_Coach_by_Herb]
Herbs_house.directions = {N: blocked, S: blocked, E: 'main_street_north', W: blocked}
Herbs_house.people = [Herb.name, herbs_kid.name]

main_street_south = Areas('main_street_south', 'neutral')
main_street_south.people = []
main_street_south.directions = {N: 'Steamtown', S: 'Route_100', E: blocked, W: 'Steamtown_hospital'}

Steamtown_hospital = Areas('Steamtown_hospital', 'neutral')
Steamtown_hospital.directions = {N: blocked, S: blocked, E: 'main_street_south', W: blocked}

Route_100 = Areas('Route_100', 'neutral')
Route_100.people = [hutu_soldier.name]


# Decisions
wake_up = Decision('wake_up', parent=None)
wake_up.statement = "You wake up to the sound of your mom calling you down stairs"
wake_up.next = 'suspicious'

suspicious = Decision('suspicious', parent=wake_up)
suspicious.statement = "Private_williams: Kid, your mom is obviously insaine. Come with me.\n" \
                       "Mom: Who do you believe me or this wakanoodle?"
suspicious.choices = {1: 'believe_mom', 2: 'believe_will'}

believe_will = Decision('believe_will', parent=suspicious)
believe_will.statement = 'Both of you follow me to the our base'
believe_will.next = 'goto_armybase'

goto_armybase = Decision('goto_army_base', parent=believe_will)
goto_armybase.choices = {1: 'goto_hq_tent', 2: 'sit_still'}

goto_hq_tent = Decision('goto_hq_tent', parent=goto_armybase)
goto_hq_tent.next = 'run_jeb'

run_jeb = Decision('run_jeb', parent=goto_hq_tent)
run_jeb.next = 'kill_jeb'

kill_jeb = Decision('kill_jeb', parent=run_jeb)
kill_jeb.next = 'talk_herb'

sit_still = Decision('sit_still', parent=goto_armybase)
sit_still.next = 'run_jeb'

believe_mom = Decision('believe_mom', parent=suspicious)
believe_mom.statement = 'Mom (To the private): Just give us a few minutes we will be right out\n'
believe_mom.next = 'goto_herbs'

goto_herbs = Decision('goto_herbs', parent=believe_mom)
goto_herbs.statement = 'Game: Suddenly private_williams busts down the door'
goto_herbs.next = 'fight_guy'

fight_guy = Decision('fight_guy', parent=goto_herbs)
fight_guy.next = 'talk_herb'

talk_herb = Decision('talk_herb', parent=fight_guy)
talk_herb.next = 'talk_kid'

talk_kid = Decision('talk_kid', parent=talk_herb)
talk_kid.next = 'into_the_badlands'



# get ap and dp
def get_ap_dp():
    for character in all_characters:
        character = eval(character)
        ch_ap = '{}.ap'.format(character.equipped)
        ch_ap = eval(ch_ap)
        character.ap = character.ap + ch_ap
        for item in character.items:
            d_p = '{}.dp'.format(item)
            character.dp = character.dp + eval(d_p)

get_ap_dp()


# Call this for a command prompt
def prompt_command():
    while True:
        story_control()
        get_ap_dp()
        y = str(user.area)
        area_items = '{}.items'.format(y)
        area_items = eval(area_items)

        area_directions = '{}.directions'.format(y)
        area_directions = eval(area_directions)

        area_people = '{}.people'.format(y)
        area_people = eval(area_people)

        area_state = '{}.type'.format(y)
        area_state = eval(area_state)
        y = str(user.area)
        user.state = area_state


        area_shopitems = '{}.shopitems'.format(y)
        area_shopitems = eval(area_shopitems)

        area_items_list = []
        command_prompt = input("What do you want to do? : ")
        if command_prompt == 'jerk off':
            user.ap = user.ap + 5
            user.dp = user.dp + 5
            user.hp = user.hp + 5
            print('Your new ap is', user.ap)
            print('Your new dp is', user.dp)
            print('Your new hp is', user.hp)
        if command_prompt not in commands:
            print("That is not valid.")

        elif command_prompt == "help":
            print("Here is a list of commands: ")
            print("")
            print(commands)

        elif command_prompt == 'my stats':
            print(user.__dict__)
            print(user.ap)

        elif command_prompt == 'search':
            for item in area_items:
                area_items_list.append(item)
            print(area_directions.items())
            print(area_items_list)
            print(area_people)
            area_items_list.clear()

        # This could be simplified
        elif command_prompt == 'move':
            print("here are the directions you can go")
            print(area_directions)
            direction = input("Which direction do you want to go? : ")
            if direction == "north" and (N, blocked) not in area_directions.items():
                user.area = area_directions.get(N, 'it doesnt work like that')
                print(user.area)
                user.state = area_state
            elif direction == "north" and (N, blocked) in area_directions.items():
                print("You can't go that way.")
            elif direction == "east" and (E, blocked) not in area_directions.items():
                user.area = area_directions.get(E, 'it doesnt work like that')
                user.state = area_state
                print(user.area)
            elif direction == "east" and (E, blocked) in area_directions.items():
                print("You can't go that way.")
            elif direction == "south" and (S, blocked) not in area_directions.items():
                user.area = area_directions.get(S, 'it doesnt work like that')
                user.state = area_state
                print(user.area)
            elif direction == "south" and (S, blocked) in area_directions.items():
                print("You can't go that way.")
            elif direction == "west" and (W, blocked) not in area_directions.items():
                user.area = area_directions.get(W, 'it doesnt work like that')
                user.state = area_state
                print(user.area)
            elif direction == "west" and (W, blocked) in area_directions.items():
                print("You can't go that way.")
            else:
                print('you cant go that way')

        elif command_prompt == 'equip':
            print('Here are your items :', user.items, '\n and what you have equipped: ', user.equipped)
            item_eq = input('What weapon do you want to equip? : ')
            if item_eq in user.items:
                item_eq = '{}.name'.format(item_eq)
                item_eq = eval(item_eq)
                user.items.remove(item_eq)
                user.items.append(user.equipped)
                user.equipped = item_eq
                print('Equipped item: ', user.equipped)

        elif command_prompt == 'take':
            if len(area_items) == 0:
                print("There is nothing here.")
            print("Here is a what is in the area.")
            for object in area_items:
                print(object)

            take = input("What do you want to take? : ")
            if take in area_items:
                take_it = eval(take)
                user.items.append(take_it.name)
                area_items.remove(take)
                for item in user.items:
                    item = eval(item)
                    new_ap = item.ap + user.ap
                    new_dp = item.dp + user.dp
                user.ap = new_ap
                user.dp = new_dp
                print('your ap: ', user.ap, 'your dp: ', user.dp)
                print('Your items:', user.items)
                print('Area items:', area_items)
            elif take not in area_items:
                print("There is nothing like that here.")

        elif command_prompt == 'talk':
            talk_()

        if command_prompt == 'attack':
            fight(area_people, area_state, area_items)

        elif command_prompt == 'buy' and user.state == 'shop':
            shopitems = []
            print('What do you want to buy? ')
            for item in area_shopitems:
                item = str(item)
                #item = '{}.name'.format(item)
                item = eval(item)
                print(item.name, ':', item.price, '$')
                shopitems.append(item.name)
            buy_ = input('Item name: ')
            if buy_ in shopitems:
                get_cost = '{}.price'.format(buy_)
                get_cost = eval(get_cost)
                if user.money < get_cost:
                    print('you cant afford that, you only have ', user.money, ' $')
                    shopitems.clear()
                else:
                    print('Here you go!')
                    if buy_ in shopitems:
                        user.items.append(buy_)
                        area_shopitems.remove(buy_)
                        user.money = user.money - get_cost
                        print('You still have ', user.money, '$ left.')
                        shopitems.clear()
                    else:
                        print('We dont have that.')
            else:
                print('We do not have that.')

attack_list = ['hit', 'block']


def rand100():
    return int(randint(0, 100))


def rand_ap():
    return()


def randfloat_6_1():
    return random.uniform(.6, 1)


def fight(area_people, area_state, area_items):
    if area_state != 'Safe':
        if len(area_people) >= 1:
            print('Here is everybody in the area :', area_people)
            enemy = input('Who do you want to fight? : ')
            if enemy in area_people:
                enemy_ = eval(enemy)
                #enemy_alive = '{}.life'.format(enemy)
                #enemy_alive = eval(enemy_alive)
                enemy_weapon = '{}.equipped'.format(enemy)
                enemy_weapon = eval(enemy_weapon)
                enemy_ap = '{}.ap'.format(enemy)
                enemy_ap = eval(enemy_ap)
                enemy_dp = '{}.dp'.format(enemy)
                enemy_dp = eval(enemy_dp)
                enemy_hp = '{}.hp'.format(enemy)
                enemy_hitchance = '{}.hit_chance'.format(enemy_weapon)
                enemy_hitchance = eval(enemy_hitchance)
                user_hitchance = '{}.hit_chance'.format(user.equipped)
                user_hitchance = eval(user_hitchance)
                enemy_money = '{}.money'.format(enemy)
                enemy_money = eval(enemy_money)

                print('{} : You think you can beat me on talent alone!? \n'
                      '{} : You dont have enough talent to win on talent alone!! '.format(enemy, enemy))

                def retaliate(fight):
                    attack_op = input('How do you want to retaliate? : ')
                    if attack_op == 'hit':
                        if rand100() <= user_hitchance:
                            print('You use your {} on {}'.format(user.equipped, enemy))
                            ap = enemy_ap * randfloat_6_1()
                            ap = int(ap)
                            enemy_.hp = enemy_.hp - ap - (enemy_.dp * .3125)
                            enemy_.hp = round(enemy_.hp)
                            print(ap - enemy_.dp * .3125, ':ap')
                            print("{} has {} hp left".format(enemy, enemy_.hp))
                        elif rand100() > user_hitchance:
                            print('Shoot dude You missed')
                    else:
                        print('You cant do that! ')
                        retaliate(fight)

                def enemy_attack():
                    if rand100() <= enemy_hitchance:
                        print('{} Attacks you with a {}'.format(enemy, enemy_weapon))
                        ap = enemy_.ap * randfloat_6_1()
                        user.hp = user.hp - ap - (user.dp * .325)
                        user.hp = round(user.hp, 2)
                        print('You have {} hp left>'.format(user.hp))
                        retaliate(area_people)
                        if enemy_.name == Jeb_Bush.name:
                            print("Jeb: Eat your heart hlout zuckerburg")
                    elif rand100() > enemy_hitchance:
                        if enemy_.name == Jeb_Bush.name:
                            print("Jeb: This weapon is'nt as intuitive as the others")
                        else:
                            print("{} Wiffed lol".format(enemy))
                        retaliate(area_people)

                while enemy_.hp >= 0 and user.life:
                    retaliate(area_people)
                    enemy_attack()
                if enemy_.hp <= 0:
                    if enemy_.name == Jeb_Bush.name:
                        print("Jeb: oh God, This is gonna tank my polls.")
                        print('Game: Jeb runs off like napoleon dynomite does when after he dances for the talent show')
                    else:
                        print(enemy, 'is dead.')
                        print('You capped their ass\n')
                    user.hp = 100
                    user.money = user.money + enemy_money
                    area_people.remove(enemy_.name)
                    area_items.append(enemy_.items)
                    story_control()
                if user.life == False:
                    dead()
            else:
                print('There is no one here by that name.')

        else:
            print('There is no one here to fight.')

    elif area_state == 'Safe':
        print('Chill bro this is a safe space!')


def talk_():
    y = str(user.area)
    h = str(user.node)
    # user_node = '{}.name'.format(h)
    # user_node = eval(user_node)
    area_people = '{}.people'.format(y)
    area_people = eval(area_people)
    node_people = '{}.name'.format(h)
    node_people = eval(node_people)
    # p_choice = '{}.speechop'.format(talk)
    p_choice = 'be'
    people = []
    if len(area_people) == 0:
        print("There is no one here.")

    print("Here are the people you can talk to.")
    for person in area_people:
        print(person)
        people.append(person)
    talk = input("Who do you want to talk to? : ")
    if talk in people:
        speak_(talk, p_choice, people, node_people)
    elif talk == "no one":
        people.clear()

    else:
        people.clear()
        print('no one here has that name.')
        talk_()


def speak_(talk, p_choice, people, node_people):
    h = str(user.node)
    user_node = '{}.name'.format(h)
    user_node = eval(user_node)
    p_choice = '{}.speechop'.format(talk)
    p_choice = eval(p_choice)
    reply = '{}.reply'.format(talk)
    reply = eval(reply)
    print(p_choice[user.node])
    speak = input("What do you want to say? : ")
    if speak.isdigit():
        speak = int(speak)
        if speak in range(0, len(p_choice.get(user.node, 'What?'))):
            p_reply = reply[user.node][speak]
            print(talk, ':', p_reply)
            if '*' in p_reply:
                people.clear()
                story()
            else:
                people.clear()
                prompt_command()
        else:
            print("They did'nt understand.")
            people.clear()
            talk_()
    else:
        print('You must type a number')
        speak_(talk, p_choice, people, node_people)

def dead():
    print('shoot dude you dead.')
    print('GAME OVER!!!')
    quit()


def story():
    h = str(user.node)
    user_node = '{}'.format(h)
    user_node = eval(user_node)
    has_code = '{}.hascode'.format(h)
    has_code = eval(has_code)
    node_code = '{}.code'.format(h)
    node_statement = '{}.statement'.format(h)
    node_statement = eval(node_statement)
    node_choices = '{}.choices'.format(h)
    node_choices = eval(node_choices)

    if len(node_choices) >= 2:
        print(node_choices)
        choice = input('What do you chose? : ')
        if choice.isdigit():
            choice = int(choice)
            print(h)
        else:
            print('You must type a number')
            story()
        if choice in node_choices.keys():
            user.node = node_choices.get(choice, 'what?')
            print(h)
            #story_control()
            prompt_command()
        else:
            print('Not an option!')
            story()
    else:
        next_node = '{}.next'.format(h)
        # print(next_node)
        next_node = eval(next_node)
        user.node = next_node
        print(user.node)
        #story_control()


def update_node():
    h = str(user.node)
    user_node = '{}'.format(h)
    user_node = eval(user_node)
    next_node = '{}.next'.format(h)
    # print(next_node)
    next_node = eval(next_node)
    user.node = next_node
    print(user.node)


def story_control():
    if user.area == back_door.name and user.node == 'goto_herbs':
        print('\nAs you close the door you see soldiers walk in and take your mom.\n'
              'You: NOOOOO I need her!\n'
              'You: I will avenge You Mother!\n'
              'Game: private_williams starts towards you. You block the door so he cant get to you\n'
              'Game: when you turn around you see a hutu soldier(you wont be able to move on until you defeat him ')
        downstairs.people.remove(Sarah_Gooch.name)
        update_node()

    if user.area == back_door.name and user.node == 'fight_guy':
        newdir = {N: 'blocked', S: 'blocked', E: 'blocked', W: 'blocked' }
        if hutu_soldier.name in back_door.people:
            back_door.directions = newdir
        elif hutu_soldier.name not in back_door.people:
            back_door.directions = {N: 'Herbs_house', S: blocked, E: 'downstairs', W: 'badlands'}

    if user.area == downstairs.name and user.node == 'goto_armybase':
        print("Game: private_williams leaves the room. You should probably follow him.")
        if private_williams.name in downstairs.people:
            downstairs.people.remove(private_williams.name)

    if user.area == army_base.name and user.node == 'goto_armybase':
        print("Game: You see private williams is waiting you could "
              "talk to him or you could ignore him which would be funny")

    if user.area == army_base.name and user.node == 'goto_hq_tent':
        print("Game: You over hear 2 voices and to your surprise you hear the voices of \n"
              "     Gist _army generals Donald Trump and Jeb Bush\n"
              "Game: You make out just a few words coming from Trump 'you think your a god general\n"
              "     ...I DON'T")
        print("Trump: Jeb did you hear that? \n"
              "Jeb: No..uh.. no no\n"
              "Trump: its the kid, sick em Jeb\n"
              "Game: Jeb is chasing you you better run home")
        update_node()
    if user.area == downstairs.name and user.node == 'run_jeb':
        print("Mom: Hurry grab your fathers stuff out of the closet and head to Herbs house")
        print("Game: Jeb breaks in followed by trump, private williams and some soldiers\n"
              "Game: Trump grabs your mother.\n"
              "Trump: Take care of the boy jeb\n"
              "Game: you should probably grab that stuff from the closet and you cant leave untill jeb is defeated")
        downstairs.type = 'neutral'
        downstairs.people.append(Jeb_Bush.name)
        if Sarah_Gooch.name in downstairs.people:
            downstairs.people.remove(Sarah_Gooch.name)
        update_node()

    if user.area == downstairs.name and user.node == 'kill_jeb':
        newdir = {N: 'blocked', S: 'closet', E: 'blocked', W: 'blocked'}
        if Jeb_Bush.name in downstairs.people:
            downstairs.directions = newdir
        elif Jeb_Bush.name not in downstairs.people:
            downstairs.directions = {N: 'room', E: 'Steamtown', S: 'closet', W: 'back_door'}
            update_node()

    if user.area == army_base.name and user.node == 'dont_goto_hq_tent':
        print("Game: Sitting there like a bubber ducky you realize the guards at the doors are hutu and not tutsi\n"
              "Game: Knowing that hutu's are part of the gist army you realize your mom was right\n"
              "Game: Out of no where Jeb Bush starts chasing you. You better run home")
        update_node()
    if user.area == Herbs_house and user.node == 'talk_herb':
        print('Game: You see Herb sitting at a desk working on something')

    if user.area == army_base.name and user.node == 'talk_kid':
        if herbs_kid not in Herbs_house.people:
            print("Game: Some kid walks into the room")
            Herbs_house.people.append(herbs_kid)

def startt():
    start.destroy()
    print("SON OF MANARCHY")
    print("type 'help' for help\n")
    print(RenderTree(wake_up, style=AsciiStyle()).by_attr())
    user.node = suspicious.name
#    print(wake_up.statement)
 #   print(all_items, all_characters)

    prompt_command()

start = Tk()
photo_path = ""
start_label = Label(start, text='Son Of Manarchy')
start_label.pack()
canvas = Canvas(width=480, height=254, bg='black')
canvas.pack(expand=YES, fill=BOTH)
gif1 = PhotoImage(file='SoM OpenScreen.gif')
canvas.create_image(240, 127, image=gif1, anchor=CENTER)
start_button = Button(start, text='Start', command=startt)
start_button.pack()
start.mainloop()




