def create_team(team_name, creator):
    return f'Команда "{team_name}" создана пользователем {creator}'


def team_info(team_name, roles):
    return f'Команда: {team_name}. Необходимые роли: {roles}'


def selection_for_the_team(stack, experience):
    if (stack == 'backend' and experience >= 2):
        return f'вы подходите на роль {stack} в команду '
    else:
        return 'Давайте подберём что то другое'


print(team_info(
    'Dream Team',
    ['backend', 'frontend', 'designer']
))
print(create_team('Dream Team', 'Артём'))
print(selection_for_the_team('backend', 3))