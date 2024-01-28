import json

def create_json_file(airport_name, gates_data):
    data = {
        "airport": airport_name,
        "gate": gates_data
    }

    with open('gates.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

def main():
    airport_name = input("Enter the airport name: ")
    gates_data = []
    for i in range(5):
        gates_name = str(i)
        latitude, longitude = input("Enter the location").split(",")


        gate_info = {
            "name": gates_name,
            "latitude": latitude,
            "longitude": longitude,
        }

        gates_data.append(gate_info)

    create_json_file(airport_name, gates_data)
    print("JSON file created successfully.")

if __name__ == "__main__":
    main()