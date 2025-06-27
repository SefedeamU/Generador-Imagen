FROM public.ecr.aws/lambda/python:3.11

# Instala dependencias
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Instala graphviz binario del sistema
RUN yum -y install graphviz

# Verifica que los imports funcionan
COPY test_imports.py ./test_imports.py
RUN python test_imports.py

# Copia la función Lambda
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

# Comando principal de Lambda
CMD ["lambda_function.handler"]


