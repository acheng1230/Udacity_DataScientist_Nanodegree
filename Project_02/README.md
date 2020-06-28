## Udacity Data Scientist Nanodegree

### Project 02 - Disaster Response Pipeline Project

#### Table of Contents
1. [Project Summary](#summary)
2. [Installation](#installation)
3. [Data](#data)
4. [Project Files](#project_files)
5. [Credits](#credits)

#### 1. Project Summary <a name="summary"></a>

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam pretium malesuada metus, non tincidunt ipsum varius eget. Nam in porta magna, sollicitudin scelerisque neque. Suspendisse tempor non eros non luctus. Suspendisse tristique sed massa malesuada tincidunt. Fusce non tellus non justo aliquam ullamcorper. 

#### 2. Installation <a name="installation"></a>
There are required packages in order to run 

- Plotly

#### 10. Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
