FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install poetry
RUN git clone https://github.com/Hashobrin/meishi.git
RUN ssh-keygen -t rsa -f key4github

COPY pyproject.toml* poetry.lock* ./

RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
