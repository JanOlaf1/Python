import csv
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt_tab')

# Lataa CSV-tiedosto
def load_csv(filename):
    try:
        with open(filename, mode='r', encoding='utf-8-sig') as file:  # Huomaa utf-8-sig
            reader = csv.DictReader(file, delimiter=';')
            data = [row for row in reader]

        if data:
            print("CSV-tiedoston sarakkeet:", data[0].keys())
            print("Ladattu data: ")
            for row in data[:5]:  # Näytä vain ensimmäiset 5 riviä
                print(row)
        else:
            print("CSV-tiedosto on tyhjä tai sitä ei luettu oikein.")
        return data
    except FileNotFoundError:
        print(f"Tiedostoa '{filename}' ei löytynyt. Tarkista tiedoston nimi.")
        return []
    except Exception as e:
        print(f"Virhe CSV-tiedoston lukemisessa: {e}")
        return []

# Hae synonyymit sanalle
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

# Tarkista, onko kaksi lausetta samankaltaisia
def are_questions_similar(question, query):
    question_tokens = set(word_tokenize(question.lower()))
    query_tokens = set(word_tokenize(query.lower()))

    for word in query_tokens:
        if word in question_tokens:
            continue
        # Tarkista, löytyykö synonyymejä kysymyksen sanoista
        query_synonyms = get_synonyms(word)
        if not query_synonyms.intersection(question_tokens):
            return False
    return True

# Hae kysymyksiä ja vastauksia
def search_question(data, query):
    results = []
    for row in data:
        if 'Kysymys' in row:
            if are_questions_similar(row['Kysymys'], query):
                if 'Vastaus' in row and row['Vastaus'].strip():
                    results.append(row)
                else:
                    results.append({'Kysymys': row['Kysymys'], 'Vastaus': 'Ei vielä vastausta.'})
    return results

# Pääohjelma
if __name__ == "__main__":
    import nltk
    nltk.download('punkt')
    nltk.download('wordnet')

    filename = 'pyt_filled.csv'
    data = load_csv(filename)

    if not data:
        print("CSV-tiedoston lukeminen epäonnistui. Lopetetaan ohjelma.")
    else:
        print("Tervetuloa chatbotin pariin! Kirjoita kysymys:")
        
        while True:
            query = input("Kysymys: ")
            if query.lower() in ['lopeta', 'exit']:
                print("Hei hei!")
                break
            
            answers = search_question(data, query)
            if answers:
                for answer in answers:
                    print(f"Kysymys: {answer['Kysymys']}")
                    print(f"Vastaus: {answer['Vastaus']}")
            else:
                print("Ei löytynyt vastausta.")
