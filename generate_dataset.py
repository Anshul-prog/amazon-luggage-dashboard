"""
Dataset generator for Amazon India luggage brands.
Produces realistic product and review data based on publicly known market positioning.
Note: Since Amazon India blocks automated scraping, this script generates a realistic
synthetic dataset modeled on actual market knowledge of these brands as of 2024-2025.
"""

import pandas as pd
import numpy as np
import json
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# ── Brand profiles (based on real market positioning) ──────────────────────
BRAND_PROFILES = {
    "Safari": {
        "price_range": (2499, 8999),
        "avg_discount": 38,
        "base_rating": 4.1,
        "market_position": "Value-Premium",
        "strengths": ["durable build", "spacious compartments", "smooth wheels", "good zippers"],
        "weaknesses": ["handle wobble", "colour fading", "lock quality"],
        "review_volume": "high",
    },
    "Skybags": {
        "price_range": (1999, 7499),
        "avg_discount": 42,
        "base_rating": 4.0,
        "market_position": "Value",
        "strengths": ["trendy designs", "lightweight", "affordable price", "vibrant colours"],
        "weaknesses": ["zipper breaking", "thin material", "wheel durability"],
        "review_volume": "very high",
    },
    "American Tourister": {
        "price_range": (3999, 14999),
        "avg_discount": 35,
        "base_rating": 4.3,
        "market_position": "Premium",
        "strengths": ["brand trust", "excellent build quality", "smooth spinner wheels", "warranty support"],
        "weaknesses": ["expensive", "heavy", "limited colour options"],
        "review_volume": "high",
    },
    "VIP": {
        "price_range": (2299, 9999),
        "avg_discount": 40,
        "base_rating": 4.0,
        "market_position": "Value-Premium",
        "strengths": ["Indian brand", "sturdy frame", "good capacity", "reliable locks"],
        "weaknesses": ["outdated design", "rough wheels", "customer service"],
        "review_volume": "medium",
    },
    "Aristocrat": {
        "price_range": (1599, 5999),
        "avg_discount": 45,
        "base_rating": 3.8,
        "market_position": "Budget",
        "strengths": ["very affordable", "lightweight", "decent capacity"],
        "weaknesses": ["poor zipper quality", "flimsy material", "wheels breaking", "short lifespan"],
        "review_volume": "medium",
    },
    "Nasher Miles": {
        "price_range": (2999, 11999),
        "avg_discount": 30,
        "base_rating": 4.2,
        "market_position": "Premium-Value",
        "strengths": ["stylish design", "hard shell quality", "good value for money", "expandable"],
        "weaknesses": ["limited availability", "handle stiffness", "delivery delays"],
        "review_volume": "medium",
    },
}

SIZES = ["Cabin (20\")", "Medium (24\")", "Large (28\")", "Set of 2", "Set of 3"]
MATERIALS = ["Polycarbonate", "ABS", "Polyester", "Nylon"]
COLOURS = ["Black", "Navy Blue", "Red", "Grey", "Teal", "Maroon", "Olive Green", "Purple"]

REVIEW_TEMPLATES = {
    "positive": [
        "Really happy with this {brand} luggage. The {strength} is excellent. Bought for a trip to Goa and it handled everything perfectly.",
        "Great product! The {strength} is exactly what I needed. My family loves it.",
        "Delivered on time, product is solid. The {strength} impressed me. Would recommend to everyone.",
        "Value for money purchase. {strength} is top notch. Already recommended to 3 friends.",
        "Been using for 6 months now. {strength} still as good as day one. Very satisfied.",
        "The {strength} is outstanding. Packaging was good too. 5 stars.",
        "Purchased as a gift and the recipient loved it. {strength} is genuinely impressive for this price.",
        "Excellent quality. {strength} is better than expected. Highly recommend.",
    ],
    "negative": [
        "Disappointed with this purchase. The {weakness} started showing after just 2 trips. Expected better from {brand}.",
        "Not worth the price. {weakness} is a real problem. Customer care was unhelpful.",
        "Returned it after first use. The {weakness} made it unusable. Waste of money.",
        "Average product. The {weakness} is a major issue. Would not buy again.",
        "Quality is below par. {weakness} within a month. Very frustrating experience.",
        "Do not buy! The {weakness} is terrible. {brand} should improve quality control.",
    ],
    "neutral": [
        "Decent product. {strength} is good but {weakness} needs improvement. 3 stars.",
        "Okay for the price. Liked the {strength} but {weakness} is a concern. Time will tell.",
        "Average experience. {strength} works fine but not blown away. Expected more from {brand}.",
        "It is okay. {strength} is fine, {weakness} is a minor issue. Gets the job done.",
    ],
}

ASPECT_KEYWORDS = {
    "wheels": ["wheel", "spinner", "rolling", "roll", "smooth ride"],
    "handle": ["handle", "telescopic", "grip", "pull"],
    "zipper": ["zipper", "zip", "closure"],
    "material": ["material", "fabric", "shell", "hard case", "soft case", "polycarbonate", "ABS"],
    "size": ["size", "capacity", "spacious", "fits", "cabin", "check-in"],
    "durability": ["durable", "sturdy", "strong", "lasted", "broke", "damage", "quality"],
    "design": ["design", "colour", "color", "look", "stylish", "appearance"],
    "price": ["price", "value", "worth", "affordable", "expensive", "money"],
}


def sentiment_score_from_rating(rating, noise=0.15):
    base = (rating - 1) / 4  # normalise 1-5 to 0-1
    return round(min(1.0, max(0.0, base + np.random.uniform(-noise, noise))), 3)


def generate_review(brand, profile, review_type):
    strength = random.choice(profile["strengths"])
    weakness = random.choice(profile["weaknesses"])
    template = random.choice(REVIEW_TEMPLATES[review_type])
    text = template.format(brand=brand, strength=strength, weakness=weakness)

    if review_type == "positive":
        rating = random.choices([4, 5], weights=[35, 65])[0]
    elif review_type == "negative":
        rating = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
    else:
        rating = 3

    date = datetime.now() - timedelta(days=random.randint(1, 730))

    # Aspect sentiments
    aspects = {}
    for aspect in ASPECT_KEYWORDS:
        if any(kw in text.lower() for kw in ASPECT_KEYWORDS[aspect]):
            aspects[aspect] = "positive" if rating >= 4 else ("negative" if rating <= 2 else "neutral")

    return {
        "review_text": text,
        "rating": rating,
        "review_date": date.strftime("%Y-%m-%d"),
        "helpful_votes": random.randint(0, 45),
        "verified_purchase": random.random() > 0.15,
        "sentiment_score": sentiment_score_from_rating(rating),
        "sentiment_label": "positive" if rating >= 4 else ("negative" if rating <= 2 else "neutral"),
        "aspects": json.dumps(aspects),
        "strength_mentioned": strength if review_type != "negative" else "",
        "weakness_mentioned": weakness if review_type != "positive" else "",
    }


def generate_products_and_reviews():
    products = []
    reviews = []
    product_id = 1

    for brand, profile in BRAND_PROFILES.items():
        num_products = random.randint(10, 15)

        for i in range(num_products):
            size = random.choice(SIZES)
            material = random.choice(MATERIALS)
            colour = random.choice(COLOURS)

            list_price = random.randint(*profile["price_range"])
            discount_pct = profile["avg_discount"] + random.randint(-8, 8)
            sell_price = round(list_price * (1 - discount_pct / 100), -1)

            num_reviews = {"high": 80, "very high": 100, "medium": 60}[profile["review_volume"]]
            num_reviews = num_reviews + random.randint(-15, 15)

            # sentiment distribution
            pos_ratio = (profile["base_rating"] - 1) / 4
            neg_ratio = max(0.05, 0.3 - pos_ratio * 0.2)
            neu_ratio = 1 - pos_ratio - neg_ratio

            product = {
                "product_id": f"P{product_id:04d}",
                "brand": brand,
                "title": f"{brand} {material} {size} Trolley Bag - {colour}",
                "size": size,
                "material": material,
                "colour": colour,
                "list_price": list_price,
                "sell_price": sell_price,
                "discount_pct": discount_pct,
                "avg_rating": round(profile["base_rating"] + np.random.uniform(-0.3, 0.3), 1),
                "review_count": num_reviews,
                "market_position": profile["market_position"],
                "asin": f"B0{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))}",
            }
            products.append(product)

            for _ in range(num_reviews):
                r_type = random.choices(
                    ["positive", "negative", "neutral"],
                    weights=[pos_ratio, neg_ratio, neu_ratio],
                )[0]
                rev = generate_review(brand, profile, r_type)
                rev["product_id"] = product["product_id"]
                rev["brand"] = brand
                reviews.append(rev)

            product_id += 1

    return pd.DataFrame(products), pd.DataFrame(reviews)


if __name__ == "__main__":
    print("Generating dataset...")
    products_df, reviews_df = generate_products_and_reviews()

    products_df.to_csv("data/products.csv", index=False)
    reviews_df.to_csv("data/reviews.csv", index=False)

    print(f"Products: {len(products_df)} rows")
    print(f"Reviews:  {len(reviews_df)} rows")
    print("\nBrand summary:")
    print(products_df.groupby("brand")[["sell_price", "discount_pct", "avg_rating", "review_count"]].mean().round(1))
    print("\nDataset saved.")
