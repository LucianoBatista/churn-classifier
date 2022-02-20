import gdown

# data
FILE_INFO = [
    {
        "client_tr": {
            "url": "https://drive.google.com/uc?id=1GaDgzqFJz-ATMU5ePDD7BPjpSjzZ7kQm",
            "output": "data/client.train.csv",
        }
    },
    {
        "client_te": {
            "url": "https://drive.google.com/uc?id=1Pg6AIpM-krtf1aNS3IKUSkoHhun_OxKw",
            "output": "data/client.test.csv",
        }
    },
    {
        "client_ch": {
            "url": "https://drive.google.com/uc?id=1JBo7SlIuzmkQgRg9VytkNgXLhZyKmPJV",
            "output": "data/client.challenge.csv",
        }
    },
    {
        "orders": {
            "url": "https://drive.google.com/uc?id=1sk7p66kMAu4ZfAUmYVH0YF-cx2kHd4UZ",
            "output": "data/orders.csv",
        }
    },
    {
        "product": {
            "url": "https://drive.google.com/uc?id=1wU65H2mwrdd8BhVM8hITCB9sfRVNHFwQ",
            "output": "data/product.csv",
        }
    },
]


# downloading data
def main(file_info: list):
    for specs in file_info:
        # get specs
        key = list(specs.keys())
        url = specs[key[0]].get("url")
        output = specs[key[0]].get("output")

        # downlaod
        gdown.download(url=url, output=output)
        print(f"Downloading key: {key}")


if __name__ == "__main__":
    main(FILE_INFO)
