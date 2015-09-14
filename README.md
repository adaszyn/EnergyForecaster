## Synopsis

Small script written during my summer internship for calculating linear regression of energy consumption measurements stored in the mysql database. Script connects with database with mysql.connector and fetches rows for buildings specified in the constructor. Values are joined with temperature measurements from the nearest weather station. Using numpy library slope, intercept and standard error are calculated based on two variables: HDD/CDD and difference between consumption and profile(average throughout the year).   

## Code Example

To establish connection with the database credentials should be provided in settings.py file.
Running the script is as easy as typing:
```python
python main.py
```


## Motivation

The script was written during summer internship in Softeco Sismat. It was a part of CREEM application.


## Contributors

Wojciech Adaszynski

## License

MIT