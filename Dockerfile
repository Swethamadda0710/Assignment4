FROM eclipse-temurin:17-jdk

# Install Python and virtual environment support
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

WORKDIR /app

# Copy project files
COPY . .

# Create a virtual environment and install Python packages
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r python-model/requirements.txt

# Build Spring Boot
RUN chmod +x mvnw
RUN ./mvnw clean package -DskipTests

# Render uses port 8080
EXPOSE 8080

# Start Flask in background and Spring Boot in foreground
CMD python python-model/app.py & java -jar target/*.jar