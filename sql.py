import mysql.connector as sql


def sql_pull(sql_code: str) -> list:
    cursor = connection.cursor()

    cursor.execute(sql_code)
    result = cursor.fetchall()

    if not result:
        print("-ERROR in sql_pull-")

    return result


def sql_push(sql_code: str) -> int:
    cursor = connection.cursor()

    cursor.execute(sql_code)

    if cursor.rowcount <= 0:
        print("-ERROR in sql_push-")

    return cursor.rowcount


"""
def sql_login(username: str, pin_code: str):
    # Tarkistetaan ensin, onko PIN-koodi numeroita
    if pin_code.isdigit():
        pin_code = int(pin_code)
    else:
        return "false_pin"

    sql = "select screen_name from game "
    sql += f"where screen_name = '{username}';"

    cursor, result = sql_execute(sql, True)

    #########################
    #########################
    # Jos käyttäjänimeä ei löydy tietokannasta game -> screen_name
    if not result:
        print(
            "User not found, create a new user? You can also type 'exit' to exit game. (Y = yes / N = no)"
        )
        login_input = input("Y / N ").lower()

        while login_input not in ["y", "n", "exit"]:
            login_input = input(
                f"{CF.RED}Invalid command, enter Y, N or exit:{CF.RESET} "
            ).lower()

        if login_input == "exit":
            exit()  # Ohjelma sulkeutuu
        elif login_input == "n":
            return False  # EI LUODA UUTTA KÄYTTÄJÄÄ, PELI EI ETENE
        # LUODAAN UUSI KÄYTTÄJÄ
        elif login_input == "y":
            new_PIN = input("Enter your new 4-digit PIN code: ")

            # Jos PIN-koodi ei ole validi
            while len(new_PIN) != 4 or not new_PIN.isdigit():
                # Pitää muistaa aina päästää käyttäjä pois
                if new_PIN == "exit":
                    exit()
                else:
                    new_PIN = input(
                        f"{CF.RED}Entered PIN code is invalid. Please enter a 4-number PIN code:{CF.RESET} "
                    )

            # Jos PIN-koodi on oikea, syötetään uusi käyttäjä tietokantaan.
            sql_new_user = "insert into game (screen_name, location, passcode) "
            sql_new_user += f"values ('{username}', 'EFHK', {int(new_PIN)});"

            cursor.reset()
            cursor.execute(sql_new_user)

            new_user = input("User created! You can now log in: ").upper()

            if new_user == "EXIT":
                exit()

            return sql_login(new_user)
    # UUDEN KÄYTTÄJÄN LUONTI LOPPUU
    #########################
    #########################
    else:
        old_user_PIN = input("Input your 4-digit PIN code: ")

        # Käyttäjän pitää aina päästä ulos
        if old_user_PIN.upper() == "EXIT":
            exit()

        old_user_PIN = int(old_user_PIN)

        sql_old_PIN = "select screen_name, passcode from game "
        sql_old_PIN += (
            f"where screen_name = '{username}' and passcode = {old_user_PIN};"
        )

        cursor, result = sql_execute(sql_old_PIN, True)

        if not result:
            print(f"{CF.RED}Invalid username or PIN code.{CF.RESET}")
            return False

        #####################
        #####################
        # Onnistunut sisäänkirjautuminen!
        if username == result[0][0] and old_user_PIN == result[0][1]:
            pelaaja["name"] = result[0][0]
            print("Successfully logged in!")
            return True
        else:
            print(f"{CF.RED}Something went wrong with login credentials...{CF.RESET}")
            return False
"""

connection = sql.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="root",
    password="metropolia",
    autocommit=True,
)
