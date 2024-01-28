import json

def create_json_file(airport_name, shops_data):
    data = {
        "airport": airport_name,
        "shops": shops_data
    }

    with open('airport_shops.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

def main():
    airport_name = input("Enter the airport name: ")
    storeType = "test"
    shops_data = []
    while(storeType != "STOP"):
        try:
            shop_name = input(f"Enter the name of shop: ")
            latitude, longitude = input("Enter the location").split(",")
            storeType = input("Enter the store type")
        

            shop_info = {
                "name": shop_name,
                "latitude": latitude,
                "longitude": longitude,
                "Type": storeType,
                "Tags": []
            }

            shops_data.append(shop_info)
        except:
            continue

    create_json_file(airport_name, shops_data)
    print("JSON file created successfully.")

if __name__ == "__main__":
    main()