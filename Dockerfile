# Use an Ubuntu base image
FROM ubuntu:22.04

LABEL maintainer="PPTX to JPEG Converter Service"

# Prevent apt-get from asking questions during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update system and install dependencies
# LibreOffice for PPTX to PDF conversion (soffice)
# ImageMagick for PDF to JPEG conversion (convert)
# Ghostscript is required by ImageMagick to handle PDF files
# Python and pip for running the FastAPI application
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        libreoffice \
        imagemagick \
        ghostscript \
        python3 \
        python3-pip \
        && apt clean && \
        rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy for PDF conversion
# As per the blog post, ImageMagick might restrict PDF processing by default.
# We modify its policy.xml to allow reading and writing PDFs.
RUN cp /etc/ImageMagick-6/policy.xml /etc/ImageMagick-6/policy.xml.bak && \
    sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read|write" pattern="PDF" \/>/g' /etc/ImageMagick-6/policy.xml

# Set the working directory inside the container
WORKDIR /app

# Create static directory for serving images
RUN mkdir -p /app/static && chmod 755 /app/static

# Copy the Python dependency file and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY . .

# Expose the port on which FastAPI will listen
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
# --host 0.0.0.0 makes the server accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
