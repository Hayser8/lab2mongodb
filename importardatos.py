from pymongo import MongoClient
from faker import Faker
from random import randint, choice, sample
from datetime import datetime, timedelta
from tqdm import tqdm


URI = "mongodb://127.0.0.1:27017"
client = MongoClient(URI)


db = client.lab2
collection = db.usuarios

fake = Faker()
NUM_DOCS = 100_000

def random_date(start_year=2018):
    start = datetime(start_year, 1, 1)
    return start + timedelta(days=randint(0, (datetime.now() - start).days))

def make_historial():
    return [
        {"producto": choice(["Producto 1", fake.word(), fake.word()]), "fecha": random_date()}
        for _ in range(randint(1, 10))
    ]

def make_document():
    num_amigos = randint(0, 2000)
    return {
        "nombre": fake.name(),
        "email": fake.email(),
        "fecha_registro": random_date(),
        "puntos": randint(0, 10_000),
        "historial_compras": make_historial(),
        "dirección": {
            "calle": fake.street_address(),
            "ciudad": fake.city(),
            "codigo_postal": int(fake.postcode().replace('-', '')[:5])
        },
        "tags": ["tag2"] + sample([fake.word() for _ in range(5)], k=randint(0, 4)),
        "archivo": choice([True, False]),
        "notas": fake.sentence(nb_words=10),
        "visitas": randint(0, 1000),
        "amigos": list(range(num_amigos)),
        "preferencias": {
            "color": choice(["rojo", "verde", "azul", "amarillo"]),
            "idioma": choice(["es", "en", "fr", "de"]),
            "tema": choice(["oscuro", "claro"])
        }
    }

def main():
    print(f"Inserting {NUM_DOCS:,} documents into ‘usuarios’ collection in lab2...")
    batch = []
    for _ in tqdm(range(NUM_DOCS)):
        batch.append(make_document())
        if len(batch) >= 1000:
            collection.insert_many(batch)
            batch.clear()
    if batch:
        collection.insert_many(batch)
    print("✅ Insert complete!")

if __name__ == "_main_":
    main()