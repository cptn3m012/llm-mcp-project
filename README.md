# Demo: Agent LLM z dostępem do bazy SQL 

Ten projekt to w pełni funkcjonalny **proof-of-concept**, który demonstruje, jak zbudować zaawansowanego agenta opartego na dużym modelu językowym (LLM), który potrafi inteligentnie korzystać z wielu różnych źródeł danych. Agent jest w stanie samodzielnie decydować, czy odpowiedzieć na pytanie użytkownika, odpytując relacyjną bazę danych **PostgreSQL** za pomocą zapytań **SQL**, czy też przeszukując semantycznie bazę wektorową **Chroma**.

Całość została zbudowana z użyciem nowoczesnych narzędzi, takich jak **LangChain** do budowy agenta, **FastAPI** do tworzenia API oraz **Docker** do konteneryzacji, co zapewnia łatwe i spójne uruchomienie całego środowiska.

---

## Kluczowe cechy projektu

* **Inteligentny Agent:** Agent LLM (GPT-4) analizuje pytanie użytkownika i decyduje, którego narzędzia użyć.
* **Dostęp do Bazy SQL:** Potrafi tłumaczyć język naturalny na zapytania SQL i wykonywać je na bazie PostgreSQL.
* **Dostęp do Bazy Wektorowej:** Potrafi wykonywać wyszukiwanie semantyczne (podobieństwa) w bazie Chroma.
* **Architektura Mikrousług:** Każdy komponent (backend, bazy danych, serwery pośredniczące) działa w osobnym kontenerze Docker.
* **Bezpieczeństwo:** Dostęp do baz danych odbywa się przez warstwę pośredniczącą (MCP), która może narzucać ograniczenia (np. zezwalać tylko na zapytania `SELECT`).

---

## 1. Wymagania

Przed rozpoczęciem upewnij się, że masz zainstalowane poniższe narzędzia:

| Narzędzie         | Wersja | Cel                                      |
| :---------------- | :----- | :--------------------------------------- |
| Docker Desktop    | 20.10+ | Do uruchamiania i zarządzania kontenerami |
| Docker Compose V2 | 2.x    | Do orkiestracji wielokontenerowej aplikacji|
| Klucz API OpenAI  | dowolny| Do komunikacji z modelem GPT-4           |

> **Uwaga:** Na systemie Windows 11 Docker Desktop wymaga włączonego WSL 2 oraz wirtualizacji w ustawieniach BIOS/UEFI.

---

## 2. Instalacja i uruchomienie

### Krok 1: Klonowanie repozytorium

Otwórz terminal i sklonuj repozytorium do wybranego folderu na swoim komputerze.

```bash
git clone https://github.com/cptn3m012/llm-mcp-project.git
cd llm-mcp-demo
```

### Krok 2: Konfiguracja klucza API (Krytyczne!)

Agent potrzebuje Twojego klucza API do komunikacji z OpenAI. Bez niego aplikacja nie zadziała.

1.  Przejdź do folderu `backend/`.
2.  Utwórz w nim nowy plik o nazwie `.env`.
3.  Otwórz ten plik w edytorze tekstu i wklej do niego poniższą linię, zastępując `sk-....` swoim prawdziwym kluczem API od OpenAI:

    ```
    OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```
### Krok 3: Budowa i uruchomienie kontenerów

W głównym folderze projektu (`llm-mcp-demo`) uruchom poniższą komendę. Docker Compose zajmie się pobraniem obrazów, zbudowaniem Twojej aplikacji i uruchomieniem wszystkich usług.

> Pierwsze uruchomienie może potrwać kilka minut.

```bash
docker-compose up --build -d
```
* Opcja `--build` jest ważna przy pierwszym uruchomieniu, aby zbudować obrazy na podstawie plików Dockerfile.
* Opcja `-d` (detached) uruchamia kontenery w tle, dzięki czemu możesz dalej korzystać z terminala.

### Krok 4: Weryfikacja

Aby upewnić się, że wszystko wystartowało poprawnie, możesz sprawdzić logi głównego kontenera aplikacji:

```bash
docker-compose logs -f backend
```
Jeśli wszystko poszło dobrze, powinieneś zobaczyć komunikaty informujące o pomyślnym pobraniu schematów z serwerów MCP i gotowości agenta do pracy. Naciśnij Ctrl+C, aby zakończyć podgląd logów.

## 3. Jak korzystać z systemu?

Do interakcji z agentem służy prosty skrypt w terminalu.

Uruchom klienta:

```bash
python scripts/ask.py
```
Pojawi się znak zachęty `🟢 >`, gdzie możesz wpisywać swoje pytania.

Przykładowe pytania, które możesz zadać:

* **Pytanie do bazy SQL:**
    * `Ilu jest użytkowników w bazie?`
    * `Pokaż wszystkie posty użytkownika o imieniu Alice.`
    * `Ile komentarzy ma każdy post?`
* **Pytanie do bazy wektorowej:**
    * `Co wiesz o bazach wektorowych?`
    * `Jakie są zalety RAG?`
* **Pytanie ogólne (bez użycia narzędzi):**
    * `Napisz krótki wiersz o programowaniu w Pythonie.`
    * `Jaka jest stolica Polski?`
 
## 4. Zatrzymywanie projektu

Aby zatrzymać wszystkie kontenery i zwolnić używane przez nie porty, wykonaj komendę:

```bash
docker-compose down
```
      
