FROM node:20-alpine3.16

LABEL maintainer='ahmed'


WORKDIR /doctor_payout_sveltekit

COPY ./ ./


RUN npm ci  \
    && chmod -R 777 /doctor_payout_sveltekit

EXPOSE 8007

ENV VITE_DJANGO_BASE_URL=http://0.0.0.0:8008

ENV PATH="/doctor_payout_sveltekit/scripts:${PATH}"

CMD ["./scripts/node_run.sh"]