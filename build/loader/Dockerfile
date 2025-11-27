# Distroless image

FROM python:3.12-slim AS build-env

RUN groupadd -g 1001 python \
   && useradd --uid 1001 --gid python --shell /bin/bash --create-home python
WORKDIR /loader
ADD . .
RUN pip install --disable-pip-version-check -r requirements.txt
RUN chown -R python:python /loader


FROM gcr.io/distroless/python3-debian12

COPY --from=build-env /loader /loader
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages
USER 1001
WORKDIR /loader
CMD ["app.py"]