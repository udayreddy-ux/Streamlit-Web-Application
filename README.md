# Streamlit based Web Application with Docker Containerization.


In this study, we developed a dynamic web application using Streamlit, a Python-based framework, which incorporates customized HTML and inline CSS for a seamless user experience. The primary objective of this project was to design an authenticated user account service with a feature allowing users to upload a text file. Upon upload, the system processes the text file to display the count of unique words and the frequency of each word on the screen. Additionally, users have the option to download the results as a text file.

To handle data transactions, we utilized MySQL, managed via Amazon Relational Database Services (RDS). This ensures reliable and scalable database management. The application was containerized using Docker, enabling consistent and efficient deployment. The Docker image was subsequently stored in the Elastic Container Registry (ECR) using AWS CLI.

Deployment was achieved through a cluster with defined task definitions for the Docker image. To facilitate this, we leveraged AWS Fargate, a serverless compute engine that simplifies the management of containerized applications. Autoscaling and an application load balancer were incorporated to efficiently manage traffic and ensure high availability and performance.
