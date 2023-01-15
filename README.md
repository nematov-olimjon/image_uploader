# Image uploader app
This app will upload image to AWS S3 and MySQL. AWS S3 will store the image itself while MySQL will store image meta data.

## Requirements
- Python 3.8*

## Clone the repo
> `git clone https://github.com/nematov-olimjon/image_uploader.git`

## Installation
- Install python environment
> `virtualenv env`

- Activate env
> `source env/bin/activate`

- Create `.env` file
> `cp env.example .env`

- Enter values for `.env` file and activate env variables
> `source .env`

- Install packages
> `pip3 install -r requirements.txt`

- Run
> `uvicorn main:app --reload`

- Verify go to link [http://127.0.0.1:8000](http://127.0.0.1:8000)