# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Add the current directory contents into the container at /app
COPY . .

# Make port  8501 available to the world outside this container
EXPOSE  8501

# Run the Streamlit app when the container launches
CMD streamlit run ui.py
