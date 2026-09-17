"""Console interface for the team member selection system."""

from pathlib import Path

from applications import (
    ApplicationError,
    cancel_application,
    review_application,
    submit_application,
)
from storage import load_json, save_json
from teams import (
    add_role,
    create_team,
    find_team_by_id,
    find_teams,
    get_available_roles,
    sort_teams,
    team_info,
    team_statistics,
)
from utils import input_int

DATA_DIR = Path(__file__).parent / "data"
TEAMS_FILE = DATA_DIR / "teams.json"
APPLICATIONS_FILE = DATA_DIR / "applications.json"


def show_teams(teams: list[dict]) -> None:
    """Print all teams and their available roles."""
    if not teams:
        print("Команды пока не созданы.")
        return

    for team in teams:
        print(team_info(team))


def show_applications(applications: list[dict]) -> None:
    """Print all submitted applications."""
    if not applications:
        print("Заявок пока нет.")
        return

    for application in applications:
        print(
            f"#{application['id']}: {application['applicant']} -> "
            f"команда {application['team_id']}, "
            f"роль {application['role']}, "
            f"статус: {application['status']}"
        )


def print_menu() -> None:
    """Print the application menu."""
    print(
        "\n=== Система подбора участников в команду ===\n"
        "1. Показать команды\n"
        "2. Найти команду\n"
        "3. Создать команду\n"
        "4. Добавить роль\n"
        "5. Показать доступные роли\n"
        "6. Подать заявку\n"
        "7. Отменить заявку\n"
        "8. Рассмотреть заявку\n"
        "9. Показать заявки\n"
        "10. Показать статистику\n"
        "0. Выход"
    )


def handle_create_team(teams: list[dict]) -> None:
    """Read team data and append a new team."""
    name = input("Название команды: ").strip()
    creator = input("Имя создателя: ").strip()
    description = input("Описание проекта: ").strip()
    team = create_team(teams, name, creator, description)
    print(f"Команда «{team['name']}» создана.")


def handle_add_role(teams: list[dict]) -> None:
    """Read role data and add it to a team."""
    team_id = input_int("ID команды: ", minimum=1)
    role_name = input("Название роли: ").strip()
    stack = input("Требуемый стек: ").strip()
    experience = input_int("Минимальный опыт (лет): ", minimum=0)
    vacancies = input_int("Количество мест: ", minimum=1)
    add_role(teams, team_id, role_name, stack, experience, vacancies)
    print("Роль добавлена.")


def handle_submit_application(
    teams: list[dict], applications: list[dict]
) -> None:
    """Read candidate data and create an application."""
    team_id = input_int("ID команды: ", minimum=1)
    applicant = input("Имя кандидата: ").strip()
    role_name = input("Желаемая роль: ").strip()
    stack = input("Ваш основной стек: ").strip()
    experience = input_int("Опыт (лет): ", minimum=0)
    application = submit_application(
        teams,
        applications,
        team_id,
        applicant,
        role_name,
        stack,
        experience,
    )
    print(f"Заявка #{application['id']} отправлена.")


def handle_review_application(
    teams: list[dict], applications: list[dict]
) -> None:
    """Accept or reject an application."""
    application_id = input_int("ID заявки: ", minimum=1)
    decision = input("Решение (принять/отклонить): ").strip().lower()
    if decision not in {"принять", "отклонить"}:
        raise ValueError("Введите «принять» или «отклонить».")
    status = "accepted" if decision == "принять" else "rejected"
    review_application(teams, applications, application_id, status)
    print("Решение сохранено.")


def save_data(teams: list[dict], applications: list[dict]) -> None:
    """Save all application data to JSON files."""
    save_json(TEAMS_FILE, teams)
    save_json(APPLICATIONS_FILE, applications)


def main() -> None:
    """Load data and run the main menu loop."""
    teams = load_json(TEAMS_FILE, [])
    applications = load_json(APPLICATIONS_FILE, [])

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "0":
                save_data(teams, applications)
                print("Данные сохранены. До свидания!")
                break
            if choice == "1":
                show_teams(sort_teams(teams))
            elif choice == "2":
                show_teams(find_teams(teams, input("Строка поиска: ")))
            elif choice == "3":
                handle_create_team(teams)
                save_data(teams, applications)
            elif choice == "4":
                handle_add_role(teams)
                save_data(teams, applications)
            elif choice == "5":
                team_id = input_int("ID команды: ", minimum=1)
                team = find_team_by_id(teams, team_id)
                roles = get_available_roles(team)
                print("Доступные роли:", ", ".join(roles) or "нет")
            elif choice == "6":
                handle_submit_application(teams, applications)
                save_data(teams, applications)
            elif choice == "7":
                application_id = input_int("ID заявки: ", minimum=1)
                cancel_application(applications, application_id)
                save_data(teams, applications)
                print("Заявка отменена.")
            elif choice == "8":
                handle_review_application(teams, applications)
                save_data(teams, applications)
            elif choice == "9":
                show_applications(applications)
            elif choice == "10":
                print(team_statistics(teams, applications))
            else:
                print("Неизвестный пункт меню.")
        except (ApplicationError, KeyError, ValueError) as error:
            print(f"Ошибка: {error}")
        except OSError as error:
            print(f"Не удалось сохранить данные: {error}")


if __name__ == "__main__":
    main()
