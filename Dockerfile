# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app

RUN pip install --upgrade pip

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Add the current directory contents into the container at /app
COPY . .

# Run the Streamlit app when the container launches
CMD streamlit run ui.py
