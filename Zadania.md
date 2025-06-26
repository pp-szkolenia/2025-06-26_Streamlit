# Zadania

## Formularze

Przygotuj formularz na danych `cars`, który pozwoli dodać samochód do tabeli w bazie. Wykorzystaj jak najwięcej różnych widgetów do wprowadzania inputów.



## Filtry i wykresy

Wczytaj z bazy danych zbiór `cars`. Zdefiniuj filtry dla kolumn: numerycznych, kategorycznych, dat i tekstowych. Wykonaj automatyczne przypisanie kolumn do powyższych rodzajów na podstawie przyjętych kryteriów dotyczących typów danych oraz liczby wartości unikalnych. Na koniec zaimplementuj tworzenie wykresów - histogramu oraz countplota - dla poszczególnych kolumn

1. Wczytaj dane z bazy
   - Połącz się z bazą danych
   - Wczytaj dane z tabeli `cars` do DataFrame'a
2. Przygotuj klasyfikację kolumn
   - Automatycznie przypisz kolumny do typów:
     - numeryczne (liczbowe, z dużą liczbą unikalnych wartości)
     - kategoryczne (z niewielką liczbą unikalnych wartości)
     - daty (`datetime`)
     - tekstowe (ciągi znaków niezaklasyfikowane jako kategorie)
3. Zaimplementuj filtrację danych
   - Stwórz expandery dla każdego typu filtrów (numeryczne, kategoryczne etc.)
   - Pod każdym expanderem stwórz funkcję o nazwie `<...>_filter()` (np. `numeric_filter()`). Funkcja ta będzie nanosiła na dashboard odpowiedni filtr (per jedna kolumna). Niech zwraca ona również dataframe przefiltrowany tym filtrem
   - Następnie pod tym samym expanderem powinno nastąpić wywołanie wcześniej zdefiniowanej funkcji `render_filters()`, do której przekażesz listę wszystkich nazw kolumn danego typu oraz funkcję napisaną w poprzednim podpunkcie
     
4. Dodaj podgląd przefiltrowanych danych
   - Wyświetl dane po filtracji w tabeli (`st.dataframe`)
     
5. Zaimplementuj sekcję wykresów
   - Wyświetl dwie kolumny obok siebie
   - W każdej kolumnie:
     - wybór rodzaju wykresu: `histogram` lub `countplot`
     - wybór kolumny (w zależności od typu wykresu)
     - wygenerowanie wykresu (`plotly.express`)
     - wyświetlenie wykresu na dashboardzie



## Update tabel

Stwórz dashboard, który po zalogowaniu się jako user lub admin pozwoli wyciągać dane z tabeli `cars` a następnie je modyfikować. Jeśli zalogowany użytkownik posiada rolę admina, powinien on móc nadpisać zmodyfikowane dane w bazie.



## To do lista

1. Stwórz strukturę projektu:

   - folder `database` z plikami `user.json` oraz `tasks.json`. Pierwszy z nich niech zawiera listę słowników (użytkowników) o kluczach: `id`, `username`,  `password`, `role` (admin/user), `display_name`. Drugi może być pustą listą lub zawierać slowniki o kluczach: `id`, `description`, `assigned_user_id`, `priority`, `due_date`, `pinned`, `created_by`
   - folder `pages`, w którym będą znajdować się dwa pliki: `1_Tasks.py` oraz `2_Users.py`
   - pozostałe pliki: `streamlit_app.py` , `db_connector.py`, `languages.py`

2. Napisz klasę `DatabaseConnector`, która przechowa ścieżki do obu plików `.json` oraz będzie zawierać metody do odczytywania oraz zapisywania danych o zadaniach i użytkownikach

3. Napisz skrypt w pliku `generate_tasks.py`, który wygeneruje określoną liczbę losowych zadań i zapisze je w bazie danych

4. Zaimplementuj panel logowania na głównej stronie oraz wybór języka aplikacji na sidebarze. Język powinien być zapisany w pamięci sesji

5. Zaimplementuj stronę, na której wyświetlani są uzytkownicy. Strona ta powinna obejmować takie elementy jak:

   - wczytanie z sesji języka aplikacji (jeśli ten jest zapisany)
   - wczytanie z sesji zalogowanego użytkownika lub zatrzymanie aplikacji w przeciwnym przypadku (`st.stop()`)
   - wczytanie z bazy listy użytkowników
   - implementacja zawartości sidebara
   - wyświetlenie listy użytkowników, w tym przycisku do usuwania użytkownika jeśli ktoś jest adminem
   - formularza dodawania użytkowników (tylko dla adminów)

6. Zaimplementuj  stronę, na której wyświetlane są zadania. Strona ta powinna obejmować takie elementy jak:

   - wczytanie z sesji języka aplikacji (jeśli ten jest zapisany)
   - wczytanie z sesji zalogowanego użytkownika lub zatrzymanie aplikacji w przeciwnym przypadku (`st.stop()`)
   - wczytanie z bazy listy użytkowników oraz zadań
   - implementacja zawartości sidebara
   - filtrowanie oraz sortowanie zadań
   - wyświetlanie zadań - najpierw przypiętych a następnie pozostałych. W przypadku adminów i osób przypisanych powinna być również możliwość edycji oraz usunięcia zadania
   - formularz dodający nowe zadanie

   

   
