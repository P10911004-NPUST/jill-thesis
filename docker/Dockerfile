FROM python:3.10-slim

WORKDIR /jill-thesis

COPY ./.streamlit .
COPY requirements.txt .
COPY app.py .

RUN apt-get update
# RUN pip install wheel
RUN apt-get install -y gdal-bin libgdal-dev 
# RUN apt-get install -y build-essential curl
RUN pip install -r requirements.txt
# RUN pip install Fiona
# RUN pip install streamlit
# RUN pip install geopandas
# RUN pip install rioxarray
# RUN pip install pycaret

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]
# CMD ["python", "app.py"]