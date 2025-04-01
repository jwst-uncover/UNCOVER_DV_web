FROM python
WORKDIR /usr/local/app

# Disable Python byte code caching and output buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Import code, assets into image
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

# Copy in source code
COPY DV_app ./
EXPOSE 8020

# Command to launch when running image
CMD [ "python", "./dash_app.py" ]