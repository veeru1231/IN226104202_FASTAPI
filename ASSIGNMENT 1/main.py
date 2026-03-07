from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 70000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Wireless Mouse", "price": 500, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Notebook", "price": 50, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 2000, "category": "Accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": False},
    {"id": 7, "name": "Webcam", "price": 3000, "category": "Electronics", "in_stock": True}
]


# Q1 - Show all products

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# Q2 - Filter by category

@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):

    filtered_products = [
        p for p in products
        if p["category"].lower() == category_name.lower()
    ]

    if not filtered_products:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": filtered_products,
        "total": len(filtered_products)
    }


# Q3 - In-stock products

@app.get("/products/instock")
def get_instock_products():

    in_stock_products = [
        p for p in products
        if p["in_stock"] == True
    ]

    return {
        "in_stock_products": in_stock_products,
        "count": len(in_stock_products)
    }

# Q4 - Store summary

@app.get("/store/summary")
def store_summary():

    total_products = len(products)

    in_stock = len([p for p in products if p["in_stock"] == True])
    out_of_stock = len([p for p in products if p["in_stock"] == False])

    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }

# Q5 - Search products

@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "matched_products": matched_products,
        "total_matches": len(matched_products)
    }
# BONUS - Cheapest & Expensive
@app.get("/products/deals")
def product_deals():

    best_deal = min(products, key=lambda p: p["price"])
    premium_pick = max(products, key=lambda p: p["price"])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }
