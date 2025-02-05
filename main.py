from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World, my name is Carl"}


class Fruit(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

FRUIT_DB = [
    {'fruit_id': 0, 'name': 'Apple'},
    {'fruit_id': 1, 'name': 'Orange'},
    {'fruit_id': 2, 'name': 'Mango'}
]

@app.get('/items/{item_id}')
def items(item_id: int, q: str | None = None):
    for item in FRUIT_DB:
        if item['fruit_id'] == item_id:
            return item
    return {'item': item_id, 'error': 'Item not found'}

@app.get('/{path_str}')
def read_string(path_str: str):
    return {'you are on': path_str}

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Fruit):
    for fruit in FRUIT_DB:
        if fruit['fruit_id'] == item_id:
            fruit.update(item.dict())
            return fruit
    return {"error": "Item not found"}

@app.post('/items')
def create_item(item: Fruit):
    new_fruit = item.dict()
    new_fruit['fruit_id'] = len(FRUIT_DB)
    FRUIT_DB.append(new_fruit)
    return new_fruit

@app.delete('/items/{item_id}')
def delete_item(item_id: int):
    for index, item in enumerate(FRUIT_DB):
        if item['fruit_id'] == item_id:
            del FRUIT_DB[index]
            return {'fruit_id': item_id, 'len': len(FRUIT_DB)}
    return {'fruit_id': item_id, 'error': 'Fruit not found'}



if __name__ == '__main__':
    import subprocess
    subprocess.run(['uvicorn', 'my_api:app', '--reload'])
