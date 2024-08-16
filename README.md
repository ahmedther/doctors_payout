## Doctor’s Payout

### Overview

Developed a comprehensive application used by the finance department to calculate the share of doctors for services rendered within a specific date range. The application accepts requests, processes data, and sends the finalized Excel file via email. Built with a robust tech stack, including SvelteKit for frontend operations, Django REST Framework for backend processes, and various libraries for data processing and task queuing. The application has significantly streamlined the payout calculation process, improving efficiency and accuracy.

### Key Features

- **Automated Payout Calculation**: Automatically calculates the share of doctors for services rendered within a specific date range, ensuring accuracy and efficiency.
- **Data Processing**: Utilizes Pandas and Numpy for efficient data processing and analysis.
- **Task Queuing**: Implements Celery and RabbitMQ for managing background tasks and ensuring smooth operation.
- **Email Integration**: Sends the finalized Excel file via email to the relevant parties, streamlining the communication process.

### Technologies Used

- **Front-End**: JavaScript, SvelteKit
- **Back-End**: Python, Django, Django REST Framework, psycopg2
- **Database**: PostgreSQL, Oracle
- **Data Processing**: Pandas, Numpy
- **Operations Task Queue**: Celery, RabbitMQ
- **Deployment**: Docker, Kubernetes, Nginx
