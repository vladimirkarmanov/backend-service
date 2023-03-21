FROM python:3.10.6-slim AS compile-image

COPY requirements/base.txt .
RUN pip install --user -r base.txt


FROM python:3.10.6-slim AS build-image
COPY --from=compile-image /root/.local /root/.local

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH=/root/.local/bin:$PATH
ENV WORKDIR=/

WORKDIR $WORKDIR

COPY ./app $WORKDIR
CMD python migrate.py && python server.py