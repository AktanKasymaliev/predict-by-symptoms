# Predict by symptoms

Chat bot

## Installation

1. Clone this repository to your local machine: `git clone https://github.com/AktanKasymaliev/predict-by-symptoms.git && cd predict-by-symptoms`
1.2 `cd webapp`
2. Create settings.ini file: `cp settings.ini_template settings.ini`
3. Edit `settings.ini`: paste your OPENAI_API_KEY (without quotation marks)
4. Run the following command to download and extract the database, create a virtual environment and install dependencies, run migrations (I assume you have `curl`). It'll take ~3-4 minutes:

```shell
make build
```

5. Run the project:

```shell
make run
```

7. Go to localhost:8000 and have fun!

## Credits

This project is built using incredible framework called [LangChain](https://github.com/hwchase17/langchain)

Also, I used [MedQuaD](https://github.com/abachaa/MedQuAD) as a dataset.
To view the full list of tools, see requirements.
