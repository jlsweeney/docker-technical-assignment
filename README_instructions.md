### A Simple Scheduled SQL Job

We've created a template made up of various files and scripts for you to fill out to get to the intended final product. Once you share your changes with us, we should be able to bring up the whole system with:

```docker-compose -f docker-compose.yml up```

The goal here is to set up the following containers:

1. A PostgreSQL database.
1. An instance of Adminer we can access at `http://localhost:8080` and the necessary credentials to access the main database.
1. A python script to upload the data in `data/loans.csv` using `psycopg2` to a `loans` table.
1. A CRON job that triggers a python script every minute and writes job logs to a `cron.log` file within the container. (This python script will create a table named `default_liquidation_rolling_avg_hist`. More on this later.)

That means there should be 4 services in your `docker-compose.yml` file. You're welcome to re-arrange some of what we've created in this repo or you can stick to the framework available. Entirely up to you. Just make sure the entry point remains the `docker-compose.yml` file, and you use CRON for scheduling and SQL for analytics.

### The `default_liquidation_rolling_avg_hist` Table

The loans table includes the number of loans, liquidations, and defaults by day that we've observed between August 2021 and May 2023. We would like you to create a table that includes the liquidation to default ratio per day and the rolling average of this value using the last 7 days before the date of the row. We would also like you to include a timestamp for when the new table is created so that the changes that come through the CRON job are easy to differentiate. (We realize the data will not be changing, but this is a toy dataset after all.)

### Follow-up Questions

Please fill out your answers here in the README.md file under each question.

1. Let's say that the `loans` and `default_liquidation_rolling_avg_hist` tables were much larger and the latter required a far more complex and compute heavy query that used a similar logic for the dates. For example, maybe we updated the `loans` table every week with a week's worth of data. How would you go about optimizing such a query? What considerations would go into the type of database object you would use to store the data?

If it's costly and slow to calculate the aggregated data, and we know that we're only ever receiving new data once a week, it makes sense to add new data incrementally, e.g. add a filter to the select statement in `query_db.py` that takes data `WHERE loans.repayment_date > (select max(repayment_date) from default_liquidation_rolling_avg_hist)`. This allows us to compute a smaller dataset and leave unchanged data alone in the aggregated table. In terms of the type of database object, a materialized view would make sense here, since we know the cadence at which we want to refresh the data. This saves us having to recompute it every time the view is accessed, but it still stays up-to-date with the underlying data.  


2. If we wanted to convert this toy application to a real production application that pulled source tables such as the `loans` table from an external team's database into our own, how would you go about re-desisgning this system? What data/tech stack would you use and why? How would you improve data availability, freshness, and quality? How would you increase the observability of the data and data pipelines?

The basic components this application would need are:
- a database connector
- scheduling
- orchestration
- monitoring

Since we expect the data to change at most every day, we don't need minute-by-minute kickoff of pipelines, and batch processing would be sufficient. Once the data is ingested (using some kind of database connector like like AWS Glue), we could transform the data directly using Glue (for Python/Spark-based jobs) or in the Redshift warehouse using SQL. If we needed more complex or frequent scheduling of jobs or orchestration of pipeline elements, we could use Airflow, which comes with its own monitoring of pipeline tasks. We would want to also have data quality checks to make sure the schema of the incoming data remains the same, there are no duplicate rows or null values to be dealt with, and periodically check that our aggregated process aligns with our source data. Alerting should be set up to allow for quicker handling of pipeline failures, so that they can be debugged quickly and the pipeline restored to operation. To improve freshness and availability of data, we could revisit the batch processing intervals, and potentially increase the frequency of the pipeline. 