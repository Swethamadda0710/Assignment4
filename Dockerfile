FROM eclipse-temurin:17-jdk

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

# Copy entire project
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r python-model/requirements.txt

# Build Spring Boot
RUN chmod +x mvnw
RUN ./mvnw clean package -DskipTests

EXPOSE 8080

CMD python3 python-model/app.py & java -jar target/*.jar