"""Console interface for the team member selection system."""

from pathlib import Path

from applications import (
    ApplicationError,
    cancel_application,
    review_application,
    submit_application,
)
from models import Application, Team, User
from storage import (
    load_applications,
    load_teams,
    load_users,
    save_applications,
    save_teams,
    save_users,
)
from teams import (
    add_role,
    create_team,
    find_team_by_id,
    find_teams,
    get_available_roles,
    sort_teams,
    team_statistics,
)
from users import add_user, find_user_by_id, show_users
from utils import input_int

DATA_DIR = Path(__file__).parent / "data"
TEAMS_FILE = DATA_DIR / "teams.json"
USERS_FILE = DATA_DIR / "users.json"
APPLICATIONS_FILE = DATA_DIR / "applications.json"


def show_teams(teams: list[Team]) -> None:
    """Print all teams and their available roles."""
    if not teams:
        print("Команды пока не созданы.")
        return
    for team in teams:
        print(team)


def show_applications(applications: list[Application]) -> None:
    """Print all submitted application objects."""
    if not applications:
        print("Заявок пока нет.")
        return
    for application in applications:
        print(application)


def print_menu() -> None:
    """Print the application menu."""
    print(
        "\n=== Система подбора участников в команду ===\n"
        "1. Показать команды\n"
        "2. Найти команду\n"
        "3. Добавить пользователя\n"
        "4. Показать пользователей\n"
        "5. Создать команду\n"
        "6. Добавить роль\n"
        "7. Показать доступные роли\n"
        "8. Подать заявку\n"
        "9. Отменить заявку\n"
        "10. Рассмотреть заявку\n"
        "11. Показать заявки\n"
        "12. Показать статистику\n"
        "0. Выход"
    )


def handle_add_user(users: list[User]) -> None:
    """Read profile data and create a User object."""
    name = input("Имя пользователя: ").strip()
    email = input("Email: ").strip()
    stack = input("Основной стек: ").strip()
    experience = input_int("Опыт (лет): ", minimum=0)
    add_user(users, name, email, stack, experience)
    user = users[-1]
    print(f"Пользователь #{user.id} создан.")


def handle_create_team(teams: list[Team], users: list[User]) -> None:
    """Read team data and create a Team linked to its creator."""
    name = input("Название команды: ").strip()
    creator_id = input_int("ID пользователя-создателя: ", minimum=1)
    creator = find_user_by_id(users, creator_id)
    description = input("Описание проекта: ").strip()
    team = create_team(teams, name, creator, description)
    print(f"Команда «{team.name}» создана.")


def handle_add_role(teams: list[Team]) -> None:
    """Read role data and add a Role object to a team."""
    team_id = input_int("ID команды: ", minimum=1)
    role_name = input("Название роли: ").strip()
    stack = input("Требуемый стек: ").strip()
    experience = input_int("Минимальный опыт (лет): ", minimum=0)
    vacancies = input_int("Количество мест: ", minimum=1)
    add_role(teams, team_id, role_name, stack, experience, vacancies)
    print("Роль добавлена.")


def handle_submit_application(
    teams: list[Team],
    users: list[User],
    applications: list[Application],
) -> None:
    """Create an Application linked to existing objects."""
    team_id = input_int("ID команды: ", minimum=1)
    user_id = input_int("ID пользователя: ", minimum=1)
    applicant = find_user_by_id(users, user_id)
    role_name = input("Желаемая роль: ").strip()
    application = submit_application(
        teams, applications, team_id, applicant, role_name
    )
    print(f"Заявка #{application.id} отправлена.")


def handle_review_application(
    teams: list[Team], applications: list[Application]
) -> None:
    """Accept or reject an application."""
    application_id = input_int("ID заявки: ", minimum=1)
    decision = input("Решение (принять/отклонить): ").strip().lower()
    if decision not in {"принять", "отклонить"}:
        raise ValueError("Введите «принять» или «отклонить».")
    status = "accepted" if decision == "принять" else "rejected"
    review_application(teams, applications, application_id, status)
    print("Решение сохранено.")


def save_data(
    teams: list[Team], users: list[User], applications: list[Application]
) -> None:
    """Convert all domain objects and save them to JSON files."""
    save_users(USERS_FILE, users)
    save_teams(TEAMS_FILE, teams)
    save_applications(APPLICATIONS_FILE, applications)


def main() -> None:
    """Load object collections and run the main menu loop."""
    users = load_users(USERS_FILE)
    teams = load_teams(TEAMS_FILE, users)
    applications = load_applications(APPLICATIONS_FILE, teams, users)

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "0":
                save_data(teams, users, applications)
                print("Данные сохранены. До свидания!")
                break
            if choice == "1":
                show_teams(sort_teams(teams))
            elif choice == "2":
                show_teams(find_teams(teams, input("Строка поиска: ")))
            elif choice == "3":
                handle_add_user(users)
                save_data(teams, users, applications)
            elif choice == "4":
                show_users(users)
            elif choice == "5":
                handle_create_team(teams, users)
                save_data(teams, users, applications)
            elif choice == "6":
                handle_add_role(teams)
                save_data(teams, users, applications)
            elif choice == "7":
                team = find_team_by_id(
                    teams, input_int("ID команды: ", minimum=1)
                )
                roles = get_available_roles(team)
                print(
                    "Доступные роли:",
                    ", ".join(role.name for role in roles) or "нет",
                )
            elif choice == "8":
                handle_submit_application(teams, users, applications)
                save_data(teams, users, applications)
            elif choice == "9":
                application_id = input_int("ID заявки: ", minimum=1)
                cancel_application(applications, application_id)
                save_data(teams, users, applications)
                print("Заявка отменена.")
            elif choice == "10":
                handle_review_application(teams, applications)
                save_data(teams, users, applications)
            elif choice == "11":
                show_applications(applications)
            elif choice == "12":
                print(team_statistics(teams, applications))
            else:
                print("Неизвестный пункт меню.")
        except (ApplicationError, KeyError, ValueError) as error:
            print(f"Ошибка: {error}")
        except OSError as error:
            print(f"Не удалось сохранить данные: {error}")


if __name__ == "__main__":
    main()
