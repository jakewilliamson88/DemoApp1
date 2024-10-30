FROM public.ecr.aws/lambda/python:3.12
LABEL authors="jake"

# Copy the requirements for running the container on Lambda.
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . ${LAMBDA_TASK_ROOT}

CMD ["main.handler"]