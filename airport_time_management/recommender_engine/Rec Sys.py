import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from math import radians, sin, cos, sqrt, atan2
import json

# Dummy data for user preferences
user_preferences = ["Tech Zone", "Culinary Masterpieces", "Fitness Zone"]

# Updated data with additional shops
data = {
    "airport": "IAH",
    "shops": [
        {"name": "Houston Wheelhouse", "latitude": 29.984245835069956, "longitude": -95.3321736706361, "Type": "Restaurant", "Tags": ["food", "dining", "restaurant"]},
        {"name": "Wendy's", "latitude": 29.985550187096567, "longitude": -95.33246195507927, "Type": "Restaurant", "Tags": ["fast food", "burgers"]},
        {"name": "Gavi", "latitude": 29.98582616870616, "longitude": -95.3328261038568, "Type": "Restaurant", "Tags": ["Italian", "pizza"]},
        {"name": "Auntie Anne's", "latitude": 29.98589516399204, "longitude": -95.33340267274399, "Type": "Restaurant", "Tags": ["pretzels", "snacks"]},
        {"name": "Yume", "latitude": 29.9858360251836, "longitude": -95.33447235974155, "Type": "Restaurant", "Tags": ["Japanese", "sushi"]},
        {"name": "Pappasito's Cantina", "latitude": 29.985619182577402, "longitude": -95.33550790781344, "Type": "Restaurant", "Tags": ["Mexican", "tex-mex"]},
        {"name": "Custom Burgers", "latitude": 29.98551404659847, "longitude": -95.33540169776099, "Type": "Restaurant", "Tags": ["burgers", "custom"]},
        {"name": "Beerhive", "latitude": 29.98552718860192, "longitude": -95.33562929073052, "Type": "Restaurant", "Tags": ["beer", "drinks"]},
        {"name": "Q smokehouse", "latitude": 29.985175639410492, "longitude": -95.33529548770854, "Type": "Restaurant", "Tags": ["barbecue", "smoked meat"]},
        {"name": "Pappadeaux Seafood Kitchen", "latitude": 29.98472552320514, "longitude": -95.33528790127416, "Type": "Restaurant", "Tags": ["seafood", "Cajun"]},
        {"name": "El Premio Tex-Mex Bar & Grill", "latitude": 29.984324688074064, "longitude": -95.33523100303238, "Type": "Restaurant", "Tags": ["Mexican", "tex-mex"]},
        {"name": "CultureMap", "latitude": 29.98584916714557, "longitude": -95.33667621849162, "Type": "Shopping", "Tags": ["news", "media"]},
        {"name": "Rip Curl", "latitude": 29.985865594594166, "longitude": -95.33740830921029, "Type": "Shopping", "Tags": ["clothing", "surfing"]},
        {"name": "NYS collections", "latitude": 29.985642181061408, "longitude": -95.33213573853298, "Type": "Shopping", "Tags": ["sunglasses", "accessories"]},
        {"name": "Space Corner", "latitude": 29.985152640825316, "longitude": -95.33239747044793, "Type": "Shopping", "Tags": ["gifts", "souvenirs"]},
        {"name": "Houston!", "latitude": 29.98582816790409, "longitude": -95.34008797036469, "Type": "Shopping", "Tags": ["gifts", "souvenirs"]},
        {"name": "Restroom 1", "latitude": 29.984826906587028, "longitude": -95.33238608829254, "Type": "Restroom", "Tags": ["restroom"]},
        {"name": "Restroom 2", "latitude": 29.98562857116221, "longitude": -95.33271230488221, "Type": "Restroom", "Tags": ["restroom"]},
        {"name": "Restroom 3", "latitude": 29.98485976182261, "longitude": -95.33534100382307, "Type": "Restroom", "Tags": ["restroom"]},
        {"name": "Restroom 4", "latitude": 29.985789560405472, "longitude": -95.33628930795449, "Type": "Restroom", "Tags": ["restroom"]},
        {"name": "Restroom 5", "latitude": 29.98522773968692, "longitude": -95.33841730230726, "Type": "Restroom", "Tags": ["restroom"]},
        {"name": "Restroom 6", "latitude": 29.985776418433552, "longitude": -95.34052633049161, "Type": "Restroom", "Tags": ["restroom"]},
        {"name": "Airport Interfaith Chapel", "latitude": 29.985656377042204, "longitude": -95.33875706248043, "Type": "Religious", "Tags": ["chapel", "religious"]},
        {"name": "Cardtronics ATM", "latitude": 29.98570655808996, "longitude": -95.3359426704987, "Type": "ATM", "Tags": ["banking", "ATM"]},
    ]
}

# Combine shop data into a DataFrame
df_shops = pd.DataFrame(data["shops"])

# Vectorize shop names using TF-IDF
vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(df_shops["name"])

# Train a basic Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(features, df_shops["Type"])

# Haversine formula to calculate distance between two points on Earth
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Define the function for proximity-aware recommendations with user-provided location
def get_proximity_aware_recommendations(user_preferences, user_latitude, user_longitude):
    # Combine user preferences into a single input
    input_data = user_preferences
    
    # Vectorize the input using the same TF-IDF vectorizer
    input_features = vectorizer.transform(input_data)
    
    # Predict preferences using the trained classifier
    predicted_preferences = classifier.predict(input_features)
    
    # Calculate distances and filter recommendations based on proximity
    df_shops["distance"] = df_shops.apply(lambda row: calculate_distance(user_latitude, user_longitude, row["latitude"], row["longitude"]), axis=1)
    recommendations = df_shops[df_shops["Type"] == predicted_preferences[0]].sort_values(by="distance").head(2)["name"].tolist()
    
    return recommendations

# Read user coordinates from a JSON file
try:
    with open("user_coordinates.json", "r") as json_file:
        user_coordinates = json.load(json_file)
        user_latitude = user_coordinates.get("latitude")
        user_longitude = user_coordinates.get("longitude")

    # Get proximity-aware recommendations for the user with user-provided location
    proximity_aware_recommendations = get_proximity_aware_recommendations(user_preferences, user_latitude, user_longitude)

    # Print recommendations
    print("User Location (Latitude:", user_latitude, "Longitude:", user_longitude, ")")
    print("Proximity-Aware Recommendations:")
    for recommendation in proximity_aware_recommendations:
        print("- " + recommendation)

except FileNotFoundError:
    print("Error: user_coordinates.json not found.")
except (ValueError, TypeError):
    print("Error: Invalid JSON format in user_coordinates.json.")
