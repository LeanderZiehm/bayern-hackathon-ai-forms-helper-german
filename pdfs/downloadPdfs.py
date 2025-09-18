import requests
import os

# List of PDF URLs
urls = [
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=1790",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=1786",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=2895",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4326",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=3435",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=5776",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=5774",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=5775",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=6033",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=3512",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=3576",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=3561",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=3429",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=6299",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4748",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4750",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4535",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4537",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4536",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4598",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4599",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4663",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=5425",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=5426",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=5427",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4634",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4628",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4654",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4627",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4626",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=2552",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4529",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4531",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4530",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4532",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4924",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4925",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4930",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4926",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4927",
    "https://formulare.landkreis-muenchen.de/cdm/cfs/eject/pdf?MANDANTID=22&FORMID=4929"
]

# Get directory of the Python script
save_dir = os.path.dirname(os.path.abspath(__file__))

# Download each PDF into that directory
for url in urls:
    formid = url.split("FORMID=")[-1]
    filename = f"form_{formid}.pdf"
    filepath = os.path.join(save_dir, filename)

    print(f"Downloading {filename} ...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Saved {filename}")
    else:
        print(f"❌ Failed to download {filename}, status code: {response.status_code}")