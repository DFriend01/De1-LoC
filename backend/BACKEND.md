# De1-LoC Backend

## Setup

This section gives instructions on how to setup and run the backend server locally. Follow
the instructions according to what terminal you are using.

Run the following in powershell to get access to the firebase admin:

```
cd backend
$env:GOOGLE_APPLICATION_CREDENTIALS=".\de1loc-firebase-admins.json"
```

### CMD/Powershell

A script has already been made for Windows for the sake of convenience since we mostly
developed this project on Windows.

```
# Change into the backend directory
> cd backend

# Run the script
> run.bat [OPTIONS]

[OPTIONS]
/i  - Initalize the database
/s  - Run with HTTPS (see the Configure HTTPS section)
```

When running the backend for the first time, you should add the `/i` flag to initialize the database. On subsequent runs, the 
`/i` flag is optional. If used, it will clear the database and populate it with default values and delete any new faces added that were not in the default model.

If you want to setup/run the backend server manually, then enter the following in either the command prompt 
or Powershell:

```
# Change into the backend directory
> cd backend

# Setup a python virtual environment for the dependencies (only need to do this once)
> pip install virtualenv
> python -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
> deactivate

# Setup the flask environment
> venv\Scripts\activate
> set FLASK_APP=de1loc
> set FLASK_ENV=development

# Initialize the database (must do this upon setting up for the first time)
> flask init-db

# Run the flask server
> flask run
```

### Bash

There is no bash script to run the flask server, so it must be ran manually. Enter the following:

```
# Change into the backend directory
$ cd backend

# Setup a python virtual environment for the dependencies (only need to do this once)
$ pip install virtualenv
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ deactivate

# Setup the flask environment
$ source venv/bin/activate
$ export FLASK_APP=de1loc
$ export FLASK_ENV=development

# Initialize the database (must do this upon setting up for the first time)
$ flask init-db

# Run the flask server
$ flask run
```

## Configuring HTTPS

The backend makes use of self-signed certificates to run the backend over HTTPS locally. If you completed the [Setup](#setup) step, the dependencies
are already installed for configuring HTTPS. To generate your self-signed certificates, run the following:

### CMD/Powershell
```
# Go to the backend directory and activate the venv
> cd backend
> venv\Scripts\activate

# Generate your cert files
> openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

### Bash
```
# Go to the backend directory and activate the venv
$ cd backend
$ source venv/bin/activate

# Generate your cert files
$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Upon running the `openssl` command, it will ask you to enter some information for your certs. The following is an example
of what to fill in:

```
Country Name (2 letter code) [AU]:CA
State or Province Name (full name) [Some-State]:British Columbia
Locality Name (eg, city) []:Vancouver
Organization Name (eg, company) [Internet Widgits Pty Ltd]:L2A HADDware
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:localhost
Email Address []:myemail@gmail.com
```

When running the backend at this moment, your browser will likely warn you of security risks since you are using a
self-signed certificate. See [this resource](https://support.kaspersky.com/CyberTrace/1.0/en-US/174127.htm) on how to add
self-signed certificates to your browser so these warnings do not consistently pop up.

To run the backend with your generated certs, execute the `run.bat` script with the `/s` flag (if you are using
the command prompt or Windows Powershell):

```
> run.bat /s
```

If you want to run the backend manually, or if you are using Bash, then execute the following instead (remember to do
the setup properly outlined in the [Setup](#Setup) section):

```
$ flask run --cert=cert.pem --key=key.pem
```

## Test Users

Username | Password
-------- | --------
dfriend  | Hello
billybob | World
sallysam | securepassword
asai     | puppies

## Running the Tests

Refer to the [Setup](#setup) section to setup the backend server locally before running the tests.
Run the following commmands in your terminal:

### CMD/Powershell

```
# Go to the directory containing the tests
> cd backend

# Activate the virtual environment installed from the setup step
> venv\Scripts\activate

# Go to the test directory
> cd test

# Run the tests with pytest
> pytest
```

### Bash

```
# Go to the directory containing the tests
$ cd backend

# Activate the virtual environment installed from the setup step
$ source venv/bin/activate

# Go to the test directory
$ cd test

# Run the tests with pytest
$ pytest
```

## Data Collection

To train our facial recognition model, it was necessary to collect images of other people to
allow the model to detect unknown individuals. For this, we made use of an 
[image scraping tool](https://github.com/ostrolucky/Bulk-Bing-Image-downloader).

For all other photos, we took photos of ourselves. All images that were collected
were subjected to augmentation and embedding computation that were stored in this
repository.

## API Endpoints

The endpoints are documented in the source code, but they are also here for convenicence.

```
URL: <api>/auth/code

    POST Request
    ===========
        Given a username and a code, the information is   
        verified against the data stored in the database
        and responds accordingly.

        Body Data (Key : Datatype)
        =======================
        code : string

        SUCCESS (200)
        =============
        The username matches the code given and 
        authentication was successful.

        Response Data (Key : Datatype)
        ---------------------------
            username : string

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        UNAUTHORIZED (401)
        ==================
        The code in the body is not registered with the 
        username, or the user is not logged in.

        FORBIDDEN (403)
        ===============
        The username in the body is not registered in the 
        database.


    URL: <api>/auth/face

    POST Request
    ===========
        Given a photo, verify the user against the facial recognition model to unlock the lock.

        Body Data (Key : Datatype)
        =======================
        file : file (.png, .jpg, .jpeg)

        SUCCESS (200)
        =============
        The face in the photo matches the embeddings trained in the facial recognition model.

        BAD REQUEST (400)
        =================
        Either exactly one photo has not been provided, or the file provided is not a photo.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        Either the user does not have facial recognition enabled, or the face submitted to the model
        does not match the user's facial embeddings.


URL: <api>/auth/login

    POST Request
    ============
        Given a username and a password, a user is logged in if the credentials are correct.
        The user id is loaded into a cookie until the user logs out.

        Body Data (Key : Datatype)
        ==========================
        username : string
        password : string
        token : string

        SUCCESS (200)
        =============
        The login credentials are correct and authentication was successful.

        Response Data (Key : Datatype)
        ---------------------------
            username : string

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        FORBIDDEN (403)
        ===============
        The login credentials are incorrect.


URL: <api>/auth/logout

    POST Request
    ============
        The currently logged in user is logged out and the session is cleared.

        SUCCESS (200)
        =============
        The user was successfully logged out.


URL: <api>/user/register

    POST Request
    ===========
        Registers a user in the database.

        Body Data (Key : Datatype)
        =======================
        username : string
        firstname : string
        lastname : string
        password : string

        SUCCESS (200)
        =============
        The user was successfully added to the database.

        Response Data (Key : Datatype)
        ---------------------------
            username : string

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        FORBIDDEN (403)
        ===============
        The username already exists in the database.


URL: <api>/user/profile

    GET Request
    ===========
        Gets the information of the currently logged in user.

        SUCCESS (200)
        =============
        The user's information was successfully fetched.

        Response Data (Key : Datatype)
        ------------------------------
            username : string
            firstname : string
            lastname : string
            face_enabled : boolean (0 or 1)

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.


URL: <api>/user/codes

    GET Request
    ===========
        Gets the codes corresponding to the currently logged in user.

        SUCCESS (200)
        =============
        The user's codes were successfully fetched.

        Response Data (Key : Datatype)
        ------------------------------
            (A number) : dictionary

            dictionary data
                id : integer
                code : string
                codename : string
                user_id : integer

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        SERVERERROR (500)
        =================
        Something went wrong fetching the codes.

URL: <api>/user/reguserface

    POST Request
    ===========
        Given multiple photos, register a user with facial recognition.

        Body Data (Key : Datatype)
        =======================
        p1 : file (.png, .jpg, .jpeg)
        p2 : file (.png, .jpg, .jpeg)
        .
        .
        .

        SUCCESS (200)
        =============
        The user was successfully registered with facial recognition.

        BAD REQUEST (400)
        =================
        Either no photos have not been provided, or the file provided is not a photo.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        The user has already enabled facial recognition.
        

URL: <api>/code/register

    POST Request
    ===========
        Registers a code tied to a user in the database.

        Body Data (Key : Datatype)
        =======================
        code : string
        codename : string

        SUCCESS (200)
        =============
        The code was successfully added to the database.

        Response Data (Key : Datatype)
        ---------------------------
            username : string
            firstname : string
            lastname : string

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        Either
            1) The code already exists in the database 
               (regardless of username).
            2) The username in the body does not exist in 
               the database.


URL: <api>/code/modify

    POST Request
    ===========
        Modifies a code in the database. Can change the name of the code, or the code itself.

        Body Data (Key : Datatype)
        =======================
        id : integer
        code : string
        codename : string

        SUCCESS (200)
        =============
        The code was successfully modified.

        Response Data (Key : Datatype)
        ---------------------------
            N/A

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        The username in the body does not exist in the database.

        SERVERERROR (500)
        =================
        Something went wrong updating the code.


URL: <api>/code/delete

    DELETE Request
    ===========
        Deletes a code from the database.

        Body Data (Key : Datatype)
        =======================
        id : integer

        SUCCESS (200)
        =============
        The code was successfully deleted.

        Response Data (Key : Datatype)
        ---------------------------
            N/A

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        The username in the body does not exist in the database.

        SERVERERROR (500)
        =================
        Something went wrong deleting the code.


URL: <api>/log/query?user=value1&nlogs=value2&offset=value3

    GET Request
    ===========
        Gets the most recent activity specified by nlogs. All of "user", "nlogs", and "offset" are optional
        parameters to the query string.

        Query Data (name : datatype)
        ----------------------------
        user : string (optional)
            The username of the user to be queried. If not specified, then the username is not
            considered in the query.

        nlogs : int (optional)
            The number of entries returned by the query. Note that the "nlogs" most recent entries
            are returned. If not specified, then the 50 most recent logs are returned.

        offset : int (optional)
            The offset of where to start querying. For example, if offset was 5, then the "nlogs" most recent
            entries starting at the 5th entry are returned. If not specified, then the offset is 0.

        SUCCESS (200)
        =============
            The query was successful. Note that the response data is sorted by date and then by time
            in descending order (most recent to least recent).

            Response Data (Key : Datatype)
            ------------------------------
            (A number) : Dictionary

            Dictionary Data
                user_id : int
                username : string
                codename : string
                verifDate : string  ("YYYY-MM-DD")
                verifTime : string  ("HH:MM:SS")
                success : int       (0 or 1)
```
