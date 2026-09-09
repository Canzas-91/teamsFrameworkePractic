def selection_for_the_team(stack, experience):
    if (stack == 'backend' and experience >= 2):
        return 'вы подходите на роль в команду '
    else:
        return 'Давайте подберём что то другое'

print(selection_for_the_team('backend', 1))