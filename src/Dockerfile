FROM manimcommunity/manim:stable

USER root
RUN pip install --no-cache-dir fastapi uvicorn

WORKDIR /app
COPY main.py /app/main.py

RUN chown -R manimuser:manimuser /app
USER manimuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
