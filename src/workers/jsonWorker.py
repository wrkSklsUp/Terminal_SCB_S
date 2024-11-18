import json

def jsonWriter(dataArr: list[dict], fileName: str) -> None:

        with open(fileName, 'w') as f:
            json.dump(dataArr, f, sort_keys=True, indent=1)

def jsonReader(fileName: str) -> list[dict]:
    with open(fileName, 'r') as file:
        return json.load(file)
