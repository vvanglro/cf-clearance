FROM mcr.microsoft.com/playwright/python

ENV PIP_ROOT_USER_ACTION=ignore

RUN mkdir /workspace/
WORKDIR /workspace/
ADD . /workspace/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
ENTRYPOINT ["uvicorn", "server:app"]
