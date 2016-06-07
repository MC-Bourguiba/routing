from views import *
from game_functions import *



number_of_games = 1

def create_ia_player(game):

    us = User(username='ai_player',password='ai_lab')
    us.save()
    player = Player(user=us)
    player.game = game
    player.superuser = False
    player.is_a_bot = True
    player.tested = True
    player.save()

    return player




def select_players_for_game():
    from game_functions import create_default_distribution
    for user in User.objects.all():
        cache.delete(get_hash(user.username) + 'allocation')
        cache.delete(get_hash(user.username) + 'path_ids')


    game = Game.objects.get(currently_in_use=True)
    current_graph = game.graph
    ai_player = Player.objects.get(user__username='ai_player')
    try:
        non_ai_player = Player.objects.filter(tested =False,superuser=False,is_a_bot = False).order_by('arrival_rank')[0]
    except:
        return
    admins = Player.objects.filter(superuser= True)

    for admin in admins:
        admin.game = game
        admin.in_use = True
        admin.save()

    ai_player.game = game
    ai_player.player_model = PlayerModel.objects.get(name='PM_AI')
    pm_ai = ai_player.player_model
    pm_ai.in_use= True
    pm_ai.historic_player=str(pm_ai.historic_player)+str(ai_player)
    ai_player.save()
    flow_distribution = create_default_distribution(pm_ai, game, ai_player)
    ai_player.flow_distribution = flow_distribution
    flow_distribution.save()
    pm_ai.save()
    ai_player.save()

    non_ai_player.game = game
    non_ai_player.tested = True
    non_ai_player.player_model = PlayerModel.objects.get(name='PM_NON_AI')
    pm_non_ai = non_ai_player.player_model
    pm_non_ai.in_use= True
    pm_non_ai.historic_player=str(pm_non_ai.historic_player)+str(non_ai_player)
    non_ai_player.save()
    flow_distribution = create_default_distribution(pm_non_ai, game, non_ai_player)
    non_ai_player.flow_distribution = flow_distribution
    flow_distribution.save()
    pm_non_ai.save()
    non_ai_player.save()
    return


def prepare_for_next_game():

    current_game = Game.objects.get(currently_in_use = True)
    name = str(current_game.name)
    number_of_games=[int(s) for s in name.split("_") if s.isdigit()][0]
    number_of_games=number_of_games+1
    current_graph = current_game.graph
    useless_graph = Graph(name='useless_'+str(number_of_games))
    useless_graph.save()
    current_game.graph =useless_graph
    current_game.save()
    next_game = Game(name='game_'+str(number_of_games),graph=current_graph)
    current_game.currently_in_use = False
    if not(current_game.stopped):
        current_game.stopped = True
    current_game.save()
    next_game.currently_in_use = True
    next_game.save()
    initial_turn = GameTurn()
    initial_turn.game = next_game
    initial_turn.iteration = 0
    initial_turn.save()
    next_game.current_turn = initial_turn
    next_game.save()


