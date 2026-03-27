from fastapi import FastAPI, HTTPException

app = FastAPI()

# Products
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499},
    {"id": 2, "name": "Notebook", "price": 99},
    {"id": 3, "name": "USB Hub", "price": 799},
    {"id": 4, "name": "Pen Pack", "price": 49},
]

cart = []
orders = []


# Helper
def get_product(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


# Q1 — Add to Cart
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int):

    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    subtotal = product["price"] * quantity

    item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": subtotal
    }

    cart.append(item)

    return {"message": "Added to cart", "cart_item": item}


# Q2 — View Cart
@app.get("/cart")
def view_cart():

    total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": total
    }


# Q3 — Remove Item
@app.delete("/cart/{product_id}")
def remove_item(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed"}

    raise HTTPException(status_code=404, detail="Item not in cart")


# Q4 — Clear Cart
@app.delete("/cart/clear")
def clear_cart():
    cart.clear()
    return {"message": "Cart cleared"}


# Q5 — Checkout
@app.post("/cart/checkout")
def checkout():

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(item["subtotal"] for item in cart)

    order = {
        "order_id": len(orders) + 1,
        "items": cart.copy(),
        "total": total
    }

    orders.append(order)
    cart.clear()

    return {"message": "Order placed", "order": order}


# Q6 — View Orders
@app.get("/orders")
def get_orders():
    return {
        "total_orders": len(orders),
        "orders": orders
    }


# ⭐ BONUS — Cart Summary
@app.get("/cart/summary")
def cart_summary():

    if not cart:
        return {"message": "Cart is empty"}

    total_items = sum(item["quantity"] for item in cart)
    total_price = sum(item["subtotal"] for item in cart)

    return {
        "total_items": total_items,
        "total_price": total_price
    }
