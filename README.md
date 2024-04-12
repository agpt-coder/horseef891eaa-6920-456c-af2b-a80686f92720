---
date: 2024-04-12T18:18:39.502924
author: AutoGPT <info@agpt.co>
---

# horse

To build a tool that returns a random xkcd comic and uses GPT-4-Vision to explain it, we would take the following approach using the specified tech stack: Python, FastAPI, PostgreSQL, and Prisma. Our solution comprises several components to meet the outlined requirements and preferences.

1. **Fetching Random XKCD Comics:** Utilize the XKCD API endpoint ('https://xkcd.com/random/comic/') to fetch a random comic. This will involve sending a GET request to the URL, which will redirect to a random comic page from where we can parse the comic image URL and metadata.

2. **Explaining Comics Using GPT-4-Vision:** Although a hypothetical scenario, assuming GPT-4-Vision's availability, integrate it by sending the comic image to the AI model via an API call. Using the response, which would include a description or explanation of the comic based on its visual content and themes, present this information to the user alongside the comic image.

3. **Filtering and Safety Features:** Implement functionality allowing users to filter comics based on themes or tags and exclude explicit/NSFW content using metadata provided by XKCD or inferred by GPT-4-Vision analysis.

4. **User Subscriptions and Recommendations:** Create a system where users can subscribe to notifications for new comics. Leveraging user interaction data and GPT-4-Vision's analysis of comic themes and visuals, develop a recommendation algorithm to suggest comics that align with individual tastes and previous likes.

5. **Sharing and Community Engagement:** Enable direct sharing of comics from the generator to social media platforms or via email, fostering community interaction and engagement.

The backend service, built with FastAPI, will handle API requests and interactions, serving as the core of the tool. Data concerning user preferences, subscription details, and comic metadata will be stored in a PostgreSQL database, managed by Prisma ORM for efficient and simplified database operations.

This comprehensive approach ensures the tool is not only functional but also engaging and user-centered, aligning with the features and functionalities you've specified.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'horse'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
