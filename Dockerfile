# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port  8501 available to the world outside this container
EXPOSE  8501

# Run the Streamlit app when the container launches
CMD streamlit run your_script_name.py --server.port=8501 --server.address=0.0.0.0
