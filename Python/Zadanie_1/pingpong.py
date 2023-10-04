import tkinter as tk

# Parametry gry
szerokosc_okna = 400
dlugosc_okna = 400
szerokosc_prostokata = 60
dlugosc_prostokata = 10
szerokosc_kwadratu = 10
szybkosc_ruchu = 5

# Inicjalizacja gry
root = tk.Tk()
root.title("Ping Pong Game")
canvas = tk.Canvas(root, width=szerokosc_okna, height=dlugosc_okna, bg="black")
canvas.pack()

# Prostokąt gracza
gracz_x = szerokosc_okna // 2 - szerokosc_prostokata // 2
gracz_y = dlugosc_okna - dlugosc_prostokata - 5  # Przesunięcie o 5 pikseli w górę
gracz = canvas.create_rectangle(gracz_x, gracz_y, gracz_x + szerokosc_prostokata, gracz_y + dlugosc_prostokata, fill="blue")

# Kwadrat
kwadrat_x = szerokosc_okna // 2 - szerokosc_kwadratu // 2
kwadrat_y = dlugosc_okna // 2 - szerokosc_kwadratu // 2
kwadrat = canvas.create_rectangle(kwadrat_x, kwadrat_y, kwadrat_x + szerokosc_kwadratu, kwadrat_y + szerokosc_kwadratu, fill="red")

# Kierunek ruchu kwadratu
kierunek_x = 1
kierunek_y = -1

# Komentarz "Game Over"
game_over_text = None

# Funkcja ruchu gracza
def przesun_w_lewo(event):
    global gracz_x
    if gracz_x - szybkosc_ruchu >= 0:
        canvas.move(gracz, -szybkosc_ruchu, 0)
        gracz_x -= szybkosc_ruchu

def przesun_w_prawo(event):
    global gracz_x
    if gracz_x + szerokosc_prostokata + szybkosc_ruchu <= szerokosc_okna:
        canvas.move(gracz, szybkosc_ruchu, 0)
        gracz_x += szybkosc_ruchu

# Obsługa ruchu gracza przy użyciu klawiszy "a" i "d"
def obsluga_klawiatury(event):
    if event.keysym == "a":
        przesun_w_lewo(event)
    elif event.keysym == "d":
        przesun_w_prawo(event)

# Obsługa zdarzeń klawiatury
root.bind("<Key>", obsluga_klawiatury)

# Funkcja do ruchu kwadratu
def ruch_kwadratu():
    global kierunek_x, kierunek_y, game_over_text

    # Aktualizacja pozycji kwadratu
    canvas.move(kwadrat, kierunek_x, kierunek_y)

    # Pozycje kwadratu
    kwadrat_poz = canvas.coords(kwadrat)

    # Odbijanie od krawędzi okna
    if kwadrat_poz[0] <= 0 or kwadrat_poz[2] >= szerokosc_okna:
        kierunek_x *= -1
    if kwadrat_poz[1] <= 0:
        kierunek_y *= -1

    # Sprawdzenie kolizji z graczem
    if czy_kolizja(kwadrat_poz, canvas.coords(gracz)):
        kierunek_y *= -1  # Odbijanie od prostokąta gracza
    elif kwadrat_poz[3] >= dlugosc_okna:
        koniec_gry()

    if not game_over_text:
        root.after(10, ruch_kwadratu)

# Sprawdzenie kolizji
def czy_kolizja(kwadrat_poz, gracz_poz):
    if (kwadrat_poz[2] >= gracz_poz[0] and kwadrat_poz[0] <= gracz_poz[2]) and (kwadrat_poz[3] >= gracz_poz[1] and kwadrat_poz[1] <= gracz_poz[3]):
        return True
    return False

# Koniec gry
def koniec_gry():
    global game_over_text
    if not game_over_text:
        game_over_text = canvas.create_text(szerokosc_okna // 2, dlugosc_okna // 2, text="Game Over", fill="red", font=("Helvetica", 24))
        #restart_button = tk.Button(root, text="Restart", command=restart_gry)
        #restart_button.pack()

# Funkcja restartu gry
def restart_gry():
    global game_over_text, gracz_x, kierunek_x, kierunek_y

    # Usuń komunikat "Game Over"
    canvas.delete(game_over_text)
    game_over_text = None

    # Przywróć początkową pozycję gracza
    gracz_x = szerokosc_okna // 2 - szerokosc_prostokata // 2
    canvas.coords(gracz, gracz_x, gracz_y)

    # Przywróć początkową pozycję i ruch kwadratu
    kwadrat_x = szerokosc_okna // 2 - szerokosc_kwadratu // 2
    kwadrat_y = dlugosc_okna // 2 - szerokosc_kwadratu // 2
    kierunek_x = 1
    kierunek_y = -1
    canvas.coords(kwadrat, kwadrat_x, kwadrat_y, kwadrat_x + szerokosc_kwadratu, kwadrat_y + szerokosc_kwadratu)

    # Wznów ruch kwadratu
    ruch_kwadratu()

ruch_kwadratu()

# Uruchomienie gry
root.mainloop()
