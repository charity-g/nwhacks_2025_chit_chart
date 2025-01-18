import os
from supabase import create_client, Client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# TODO RUN ONCE
os.environ['SUPABASE_URL'] = 'https://mhsatlgwdnlnvbacmcue.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1oc2F0bGd3ZG5sbnZiYWNtY3VlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcyMjY4NzYsImV4cCI6MjA1MjgwMjg3Nn0.XMnJ-YD7x2-j1TQjejSZKA9ppr9T2SJ6R_fHlNrPn-Q'

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173/",
    "localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"Charity Says": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "q": "SUP SUP"}

@app.get("/clinicians")
def read_clinicians():
   response = supabase.table("clinician").select("*").execute()
   return {"data": response.data}

#    return {"a": response}

# note disable RLS in supabase to get permissions to write and read
@app.get("/patient/{name}")
def insert_patient(name: str):
    firstname, last_name = name.split("_")
    response = (
    supabase.table("patient")
    .insert({"first_name": firstname, "last_name": last_name})
    .execute()
   )

    return {"a": response}


class Encounter(BaseModel):
    transcript: str

@app.post("/create_encounter")
async def create_encounter(data: Encounter):
    print(data)
    return {'response': 200, "transcript": data.transcript}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/itemsTEMP/")
async def create_item(item: Item):
    return item


# @app.get("/audio")
# def get_audio():
#     response = supa.storage.from_('audio_transcripts').download('times_by_tenth.mp3')
#     return {"a": response}

# > fastapi dev main.py