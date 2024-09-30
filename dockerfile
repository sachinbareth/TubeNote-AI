# Step 1: Use official Python image from DockerHub
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt into the container
COPY requirements.txt .

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the app code into the container
COPY . .

# Step 6: Expose the Streamlit port
EXPOSE 8501

# Step 7: Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
