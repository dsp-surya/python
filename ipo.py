# Change this:
parsed_listing_dates = pd.to_datetime(ipo_df['Listing'], errors='coerce')

# To this:
parsed_listing_dates = pd.to_datetime(ipo_df['Listing'], errors='coerce', format='mixed')
