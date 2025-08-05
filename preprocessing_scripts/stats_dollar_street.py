import pandas as pd
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    # Create output directory for plots
    output_dir = "dollar-street/plots"
    os.makedirs(output_dir, exist_ok=True)

    # Load the Dollar Street dataset metadata
    df = pd.read_csv("dollar-street/images_v2.csv")

    # Count number of entries per country and sort in descending order
    country_counts = df['country.name'].value_counts()
    print("\nNumber of entries per country:")
    print(country_counts)
    
    plt.figure(figsize=(15, 8))
    country_counts.head(20).plot(kind='bar', color='purple')
    plt.title('Number of Entries for Top 20 Countries in Dollar Street Dataset', fontsize=14)
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Number of Entries', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/country_distribution.png')
    plt.close()

    # Count number of entries per region and sort in descending order
    region_counts = df['region.id'].value_counts()
    print("\nNumber of entries per region:")
    print(region_counts)
    
    plt.figure(figsize=(15, 8))
    region_counts.plot(kind='bar', color='skyblue')
    plt.title('Number of Entries by Region in Dollar Street Dataset', fontsize=14)
    plt.xlabel('Region', fontsize=12)
    plt.ylabel('Number of Entries', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/region_distribution.png')
    plt.close()

    # Get number of unique places per country
    places_by_country = df.groupby('country.name')['place'].nunique().sort_values(ascending=False)
    print("\nNumber of unique places photographed per country (all countries):")
    for country, count in places_by_country.items():
        print(f"{country}: {count}")
    # Count countries with multiple places
    countries_with_multiple_places = len(places_by_country[places_by_country > 1])
    print(f"\nNumber of countries with multiple places photographed: {countries_with_multiple_places}")
    
    # Filter entries for United States
    us_data = df[df['country.name'] == 'United States']
    
    # Get income by place
    us_incomes = us_data.groupby('place')['income'].first()
    print("\nIncome distribution across places in United States:")
    print(us_incomes)

    # Plot income distribution for US places
    plt.figure(figsize=(15, 8))
    us_incomes.plot(kind='bar', color='red')
    plt.title('Income Distribution Across Places in United States', fontsize=14)
    plt.xlabel('Place', fontsize=12)
    plt.ylabel('Income ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/us_income_distribution.png')
    plt.close()

    # Get top 20 countries by number of entries
    top_20_countries = country_counts.head(20).index

    # Create a pivot table of topics by country
    topics_by_country = df[df['country.name'].isin(top_20_countries)].groupby(['country.name', 'topics'])['id'].count().unstack()
    
    # Find topics present in all top 20 countries (no NaN values)
    topics_in_all_top20 = topics_by_country.dropna(axis=1).columns.tolist()
    
    print(f"\nNumber of topics with full coverage across top 20 countries: {len(topics_in_all_top20)}")
    print("\nTopics with coverage across all top 20 countries:")
    print(topics_in_all_top20)

    # Create word cloud of topics
    from wordcloud import WordCloud
    
    # Get all topics and their frequencies
    topic_frequencies = df['topics'].value_counts()
    topic_dict = topic_frequencies.to_dict()
    
    # Generate word cloud
    plt.figure(figsize=(15, 8))
    wordcloud = WordCloud(width=1600, height=800, 
                         background_color='white',
                         min_font_size=10).generate_from_frequencies(topic_dict)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Topics in Dollar Street Dataset', fontsize=14)
    plt.tight_layout(pad=0)
    plt.savefig(f'{output_dir}/topics_wordcloud.png')
    plt.close()

    # Get average income per country for top 20 countries
    top_20_avg_income = df[df['country.name'].isin(top_20_countries)].groupby('country.name')['income'].mean().sort_values(ascending=False)
    
    print("\nAverage income per country (top 20 countries):")
    print(top_20_avg_income)

    # Plot income distribution for top 20 countries
    plt.figure(figsize=(15, 8))
    top_20_avg_income.plot(kind='bar', color='lightgreen')
    plt.title('Average Income by Country (Top 20 Countries)', fontsize=14)
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Average Income ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/income_distribution_top20.png')
    plt.close()
    
    # Get unique places per country for top 20
    places_per_country = df[df['country.name'].isin(top_20_countries)].groupby('country.name')['place'].nunique()
    
    print("\nNumber of unique places photographed per country (top 20 countries):")
    print(places_per_country)

    # Get average income per country for countries with multiple places
    multi_place_countries = places_by_country[places_by_country > 1].index
    multi_place_avg_income = df[df['country.name'].isin(multi_place_countries)].groupby('country.name')['income'].mean().sort_values(ascending=False)
    
    print("\nAverage income per country (countries with multiple places):")
    print(multi_place_avg_income)
    
    # Get unique places per country for countries with multiple places
    multi_place_counts = df[df['country.name'].isin(multi_place_countries)].groupby('country.name')['place'].nunique()
    
    print("\nNumber of unique places photographed per country (countries with multiple places):")
    print(multi_place_counts)

    # Create a pivot table of topics by country for countries with multiple places
    topics_by_multi_place = df[df['country.name'].isin(multi_place_countries)].groupby(['country.name', 'topics'])['id'].count().unstack()
    
    # Find topics present in all countries with multiple places (no NaN values)
    topics_in_all_multi_place = topics_by_multi_place.dropna(axis=1).columns.tolist()
    
    print(f"\nNumber of topics with full coverage across countries with multiple places: {len(topics_in_all_multi_place)}")
    print("\nTopics with coverage across all countries with multiple places:")
    print(topics_in_all_multi_place)