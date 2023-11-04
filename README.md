# Korean-Vocabulary-memory-application
This code launches a small window where you can define Korean vocabulary and grammar to quiz yourself on it later on.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">TO DO</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
---
## About the project 

This project is a simple Python application to learn vocabulary and grammar in Korean. You can enter the chapter, grammar, and vocabulary in the application and then train yourself to see if you memorize them.

### Built with

* PyQt6 for the GUI applications 
* MySQL for the database management

---

## Getting started

To start using the application, you need an instance of the MySQL database on your computer and a Python environment.

### Prerequisites
You need a Python environment installed to run the code and install the library needed ( the command can change in function of your environment): 

- PyQt6: pip install PyQt6
- MySQL: pip install mysql-connector-python

### Installation

1. Download or clone the repository 
2. Install Python library if an error shows up
3. If MySQL is not installed follow the above procedure before going to step 4
4. Change the constant value of PW in the myApps_DB.py file by your root database password
5. run the Python code

Installation of MySQL database management system:
1. Install on your computer:
     * MySQL Community Server from the link: https://dev.mysql.com/downloads/mysql/
     * MySQL Workbench from the link: https://dev.mysql.com/downloads/workbench/  (if not installed)
2. During the installation you should have defined a root password for your database, and use it for your Python code.
3. If not defined: Open MySQL Workbench and create your database.

---
## Usage 

To use the application, you can follow these steps: 

 1) In your computer go into service, find MySQL80, and run.
    
<img width="534" alt="Service_mySQL" src="https://github.com/KmilleK/Korean-Vocabulary-memory-application/assets/57387482/23ca75b4-2856-4a9d-b770-084fd8635b98">

 2) Run the code myApps_DB.py and then navigate in the application to choose what you want to do:

   - You first need to create your chapter and memory card in the expend section

https://github.com/KmilleK/Korean-Vocabulary-memory-application/assets/57387482/a01af571-d839-4315-a8bb-6f971cfbf57c
  
   - You can then look at the memory card in the manage section

https://github.com/KmilleK/Korean-Vocabulary-memory-application/assets/57387482/65141eca-d973-44de-890b-c53ef4038bd4
     
   - Finaly you can train yourself on the wanted memory card in the train section

https://github.com/KmilleK/Korean-Vocabulary-memory-application/assets/57387482/08e03e80-65e1-43c5-9deb-97bc73bed18c

---
## TO DO

- [ ] Manage vocabulary suppress or modify the memory card
- [ ] Grammar testing
- [ ] Testing vocabulary upper case and small mistakes allowed
- [ ] Improve UI design   




