FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Command to run both the bot and dashboard
# Use a shell script to manage both processes
RUN printf "#!/bin/bash\npython main_bot.py & streamlit run dashboard.py --server.address=0.0.0.0" > entrypoint.sh && chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
