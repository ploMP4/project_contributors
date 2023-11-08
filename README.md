# Project Contributors

## Getting started

_Make sure you have docker with docker-compose installed_

To get started with the project run:

```bash
docker compose up
```

Your application is now ready to go on: [127.0.0.1:8000](http://127.0.0.1:8000)

## API Docs

You can find the API documentation after starting the app at [127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)

## What is mailhog?

If you noticed a second container starting called mailhog, it is used to create an SMTP server that we use
to test the email functionallity needed for password reset.

You can find the mailhog Web dashboard after starting the app at [127.0.0.1:8025](http://127.0.0.1:8025)
