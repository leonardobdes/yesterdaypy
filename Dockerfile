FROM python
WORKDIR /usr/local/yesterdaypy

RUN pip install --no-cache-dir yesterdaypy boto3==1.35.99 linode_api4

CMD ["yesterdaypy"]
