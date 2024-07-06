from fastapi import FastAPI, HTTPException

from src.database import get_db, startup_event
from src.models import StockKeepingUnit


def create_app():
    app = FastAPI()
    app.add_event_handler("startup", startup_event)
    return app


app = create_app()


@app.post("/items/")
def create_item(item: StockKeepingUnit) -> StockKeepingUnit:
    """GET API route that inserts an item into the database.

    Args:
        item (Item): The item is to be inserted into the database.

    Returns:
        Item: The item returned as an HTTP response.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, price, is_offer) VALUES (?, ?, ?)",
        (item.name, item.price, int(item.is_offer) if item.is_offer else None),
    )
    conn.commit()
    item.id = cursor.lastrowid
    return item


@app.get("/items/{item_id}")
def read_item(item_id: int):
    connection = get_db()
    item = connection.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(item)


@app.get("/items/")
def read_items() -> list[dict[str, int | str | float | bool]]:
    """GET API route named items that retrieve all items from the database.

    Returns
    -------
    list[dict[str, int | str | float | bool]]
         All items available in the database as a list of dictionary
    """
    conn = get_db()
    items = conn.execute("SELECT * FROM items").fetchall()
    return [dict(item) for item in items]


@app.put("/items/{item_id}")
def update_item(item_id: int, item: StockKeepingUnit):
    conn = get_db()
    conn.execute(
        "UPDATE items SET name = ?, price = ?, is_offer = ? WHERE id = ?",
        (item.name, item.price, int(item.is_offer) if item.is_offer else None, item_id),
    )
    conn.commit()
    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    return {"message": "Item deleted"}
