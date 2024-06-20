# CU-Backend

Flask RESTful API for the Creative Unison app.


## Getting Started

> [!NOTE]
> If you have any issues starting up the project with the steps below, open up a ticket in the #tickets channel in the Discord.

* Make sure you have Python installed ([View Python Installation]((https://www.python.org/downloads/release/python-3123/)))

* Clone the repo 
```
git clone https://github.com/902Youth/CU-Backend.git
```

* Navigate to the root directory
```
cd ./CU-Backend
```

* Create a virtual environment
```
python -m venv venv
```
* Activate a virtual environment (view the [Python Docs](https://docs.python.org/3/library/venv.html) if you have issues)

Mac/Linux: `source venv/bin/activate`
Windows: `venv\Scripts\activate.bat`

* Install dependencies
```
pip install -r requirements.txt
```

* Create .env file in the root of the project


* Put database connection string in .env (View #resources channel in the Discord)
```
DATABASE_URL=mysql+pymysql://root:<password>!@<host>/<database_name>
```

* Run the development server
```
python ./app/App.py
```

Thats it! You can now use/test the Flask API.
