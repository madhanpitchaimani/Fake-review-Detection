import pandas as pd
import numpy as np
import random
import os

def generate_synthetic_reviews(num_samples=1000, output_path="data/synthetic_reviews.csv"):
    """
    Generates a synthetic dataset with product_id and richer linguistic variety 
    to support the IEEE Integrated Approach features.
    """
    data = []
    products = [f"PROD_{i:03d}" for i in range(20)]
    
    # Pre-define some product quality levels to test consistency
    product_quality = {p: np.random.uniform(3.5, 5.0) for p in products}

    for i in range(num_samples):
        # 0 = Genuine, 1 = Fake
        label = np.random.choice([0, 1], p=[0.7, 0.3])
        product_id = random.choice(products)
        
        if label == 0:
            # Genuine reviews follow product quality and have varying readability
            avg_q = product_quality[product_id]
            rating = int(np.clip(np.random.normal(avg_q, 0.5), 1, 5))
            
            text = random.choice([
                "The build quality is excellent, and it arrived much faster than expected. Highly recommended for daily use.",
                "It's a decent product for the price. Not the best in class, but definitely reliable enough for basic tasks.",
                "I've been using this for a week now, and the battery life is impressive. The interface is intuitive as well.",
                "Exactly as described. The packaging was secure, and the item works perfectly without any setup issues.",
                "A bit expensive compared to alternatives, but the performance justifies the cost. Solid choice."
            ])
            account_age = np.random.randint(100, 2000)
            verified_purchase = np.random.choice([1, 0], p=[0.9, 0.1])
            multiple_ips = 0
        else:
            # Fake reviews are often extreme (5 or 1) and have suspicious patterns
            rating = np.random.choice([1, 5], p=[0.2, 0.8])
            
            # Fake texts are either too generic, repetitive, or overly emotional (high subjectivity)
            text = random.choice([
                "BEST PRODUCT EVER!!! AMAZING QUALITY. BUY IT NOW YOU WONT REGRET IT!!!! BEST SELLER.",
                "TOTAL WASTE OF MONEY. DO NOT BUY. FRAUD SELLER. BROKE IN ONE DAY. TERRIBLE.",
                "Super excellence. Many good things. I like it very much. Very very very good quality.",
                "I am so happy with this purchase. It is the most beautiful thing I have ever seen in my life.",
                "WOW WOW WOW. UNBELIEVABLE QUALITY. FIVE STARS. BEST BEST BEST."
            ])
            account_age = np.random.randint(1, 15) # New accounts
            verified_purchase = np.random.choice([0, 1], p=[0.8, 0.2])
            multiple_ips = np.random.choice([1, 0], p=[0.7, 0.3])
            
        data.append({
            "review_id": i,
            "product_id": product_id,
            "text": text,
            "rating": rating,
            "account_age_days": account_age,
            "verified_purchase": verified_purchase,
            "multiple_ips": multiple_ips,
            "label": label
        })
        
    df = pd.DataFrame(data)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {num_samples} synthetic reviews at {output_path}")

if __name__ == "__main__":
    generate_synthetic_reviews()
