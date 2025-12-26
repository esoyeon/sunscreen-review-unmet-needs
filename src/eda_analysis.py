import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pathlib

# Set style for plots
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'AppleGothic' # For Mac Korean support
plt.rcParams['axes.unicode_minus'] = False

def load_data(filepath):
    """Loads the processed review data."""
    if filepath.endswith('.parquet'):
        return pd.read_parquet(filepath)
    else:
        return pd.read_json(filepath, lines=True)

def load_products(filepath):
    """Loads product data."""
    return pd.read_json(filepath, lines=True)

def plot_rating_distribution(df, output_dir):
    """Plots and saves the distribution of ratings."""
    plt.figure(figsize=(10, 6))
    sns.countplot(x='rating', data=df, palette='viridis')
    plt.title('Rating Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.savefig(os.path.join(output_dir, 'rating_distribution.png'))
    plt.close()
    print(f"Saved rating_distribution.png to {output_dir}")

def plot_review_length_distribution(df, output_dir):
    """Plots and saves the distribution of review lengths."""
    # Updated column check
    target_col = 'review_text' if 'review_text' in df.columns else 'content'
    
    if target_col in df.columns:
        df['review_length'] = df[target_col].fillna('').astype(str).apply(len)
        
        plt.figure(figsize=(12, 6))
        sns.histplot(df['review_length'], bins=50, kde=True, color='blue')
        plt.title('Review Length Distribution')
        plt.xlabel('Length (characters)')
        plt.ylabel('Count')
        plt.savefig(os.path.join(output_dir, 'review_length_distribution.png'))
        plt.close()
        print(f"Saved review_length_distribution.png to {output_dir}")
    else:
        print(f"Column '{target_col}' not found for review length analysis.")

def analyze_top_products(df, output_dir, top_n=10):
    """Analyzes and plots top N reviewed products."""
    # Check for product_name, otherwise use goods_no
    if 'product_name' in df.columns:
        col_name = 'product_name'
        title = f'Top {top_n} Most Reviewed Products'
    elif 'goods_no' in df.columns:
        col_name = 'goods_no'
        title = f'Top {top_n} Most Reviewed Products (ID)'
    else:
        print("No product column found.")
        return

    top_products = df[col_name].value_counts().head(top_n)
    
    plt.figure(figsize=(12, 8))
    # Wrap labels if names
    if col_name == 'product_name':
        top_products.index = [x[:30] + '...' if len(str(x)) > 30 else x for x in top_products.index]
        
    sns.barplot(x=top_products.values, y=top_products.index, palette='mako')
    plt.title(title)
    plt.xlabel('Number of Reviews')
    plt.ylabel('Product')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_products.png'))
    plt.close()
    print(f"Saved top_products.png to {output_dir}")

def main():
    # Define paths
    project_root = pathlib.Path(__file__).parent.parent
    data_path = project_root / 'data' / 'processed' / 'reviews_clean.parquet'
    products_path = project_root / 'data' / 'raw' / 'products_20251221.jsonl'
    output_dir = project_root / 'report' / 'figures'
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading data from {data_path}...")
    try:
        df = load_data(str(data_path))
        print(f"Reviews loaded. Shape: {df.shape}")
        
        # Load and merge products
        if os.path.exists(products_path):
            print(f"Loading products from {products_path}...")
            products_df = load_products(str(products_path))
            
            if 'goods_no' in df.columns and 'goods_no' in products_df.columns:
                df['goods_no'] = df['goods_no'].astype(str)
                products_df['goods_no'] = products_df['goods_no'].astype(str)
                df = df.merge(products_df[['goods_no', 'product_name']], on='goods_no', how='left')
                print("Merged product names.")
        
        # Basic Stats
        print("\n--- Basic Statistics ---")
        print(f"Total Reviews: {len(df)}")
        if 'rating' in df.columns:
            print(f"Average Rating: {df['rating'].mean():.2f}")
        
        # Plots
        if 'rating' in df.columns:
            plot_rating_distribution(df, str(output_dir))
        
        plot_review_length_distribution(df, str(output_dir))
        analyze_top_products(df, str(output_dir))
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
