FROM mcr.microsoft.com/playwright/python

RUN mkdir /workspace/
WORKDIR /workspace/
ADD . /workspace/
RUN pip install -r requirements.txt
ENTRYPOINT ["uvicorn", "server:app"]
