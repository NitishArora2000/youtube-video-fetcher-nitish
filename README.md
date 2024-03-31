# YouTube Video Fetcher

This is a Django-based application that fetches and stores video data from the YouTube API. It allows users to search for videos and retrieve paginated lists with details.

**Features**

* **Continuous Video Fetching:** Updates database with latest videos based on a search query.
* **API Key Rotation:** Uses multiple API keys and switches automatically when quota is reached.
* **Video Search:** Search for videos using a query string.
* **Pagination:** Efficient data retrieval with cursor-based pagination.
* **Database Storage:** Stores video data (title, description, publish date, thumbnail URL) in a PostgreSQL database with proper indexing.

## Continuous Video Fetching Feature

The YouTube Video Fetcher application boasts a feature for fetching videos from the YouTube API continuously in the background. This feature operates asynchronously at a specified interval, usually every 10 seconds. Its primary goal is to keep the database updated with the latest videos matching a predefined search query.

### How It Works

**API Key Rotation:**

- The application utilizes multiple API keys stored in a variable named `API_KEYS` to make requests to the YouTube API.
- If an API key reaches its quota limit, the application automatically switches to the next available one, ensuring uninterrupted data fetching.

**Fetching Latest Videos:**

- The application sends a search request to the YouTube Data API (using `youtube.search().list`).
- Parameters included in the request:
    - `q`: Search query
    - `order`: Sorting order (e.g., relevance, date)
    - `type`: Video type (e.g., "video")
    - `part`: Specifies video data to retrieve (e.g., "snippet")
    - `publishedAfter`: Filter for videos published after a specific date
    - `maxResults`: Maximum number of videos to retrieve

**Processing API Response:**

- The response from the YouTube API is processed to extract relevant data such as title, description, published date, and thumbnail URLs.
- This data is then structured into Video objects for storage in the database.

**Database Storage:**

- The extracted video data is stored in a database table, typically represented by a Django model named `Video`.
- The table is properly indexed for efficient data retrieval. Common fields include:
    - Video title
    - Description
    - Publishing datetime
    - Thumbnail URLs (default, medium, high)

**Bulk Insertion:**

- To optimize performance, the application employs bulk insertion (`bulk_create`) of Video objects into the database, minimizing database access overhead.

### Code Implementation

The provided code snippet demonstrates this feature's implementation using the `googleapiclient` library to interact with the YouTube API. Key aspects of the code include:

- Utilizing API keys in rotation from `API_KEYS` for API requests.
- Handling HTTP errors, such as API key exhaustion (e.g., `HttpError`).
- Asynchronous fetching of videos with a specified interval (e.g., 10 seconds).
- Processing API responses and structuring video data into Video objects.
- Bulk insertion of video objects for performance optimization.

This feature guarantees the application remains updated with the latest YouTube videos, offering users a constant stream of fresh content.

# Prerequisites

* Python 3.x
* Docker
* Docker Compose

**Getting Started**

1. Clone the repository:

```
git clone https://github.com/your-username/youtube-video-fetcher.git
```

2. Navigate to the project directory:

```
cd youtube-video-fetcher-nitish
```

4. Build and start Docker containers:

```
docker-compose up --build
```

5. To Access Databse (POSTGRES):

```
# Get running containers
docker ps

# Copy container ID to run
docker exec -it <CONTAINER ID> bash

# Enter PSQL
psql -U postgres

# Query the table
select * from youtube_api_video
```

This builds the Docker images, starts the containers, and applies database migrations.

# API Endpoints

## GET /api/videos/?page_size=<page_size>

* Retrieves a paginated list of videos with the specified number of videos per page.
* Example: `curl -X GET http://0.0.0.0:8000/api/videos/?page_size=30`
* Explanation: Fetches videos from the database, sorted by publishing date (newest first). Users can specify the number of videos per page using the `page_size` parameter.

### Optimized SQL Query:

```sql
SELECT 
    "youtube_api_video"."id", 
    "youtube_api_video"."title", 
    "youtube_api_video"."description", 
    "youtube_api_video"."published_at", 
    "youtube_api_video"."thumbnail_default", 
    "youtube_api_video"."thumbnail_medium", 
    "youtube_api_video"."thumbnail_high" 
FROM 
    "youtube_api_video" 
ORDER BY 
    "youtube_api_video"."published_at" DESC;
```

## GET /api/videos/search/?q=<search_query>

* Searches for videos based on the provided query.
* Example: `curl -X GET http://0.0.0.0:8000/api/videos/search/?q=python`
* Explanation: Performs a database search using regular expressions to match the query in video titles and descriptions. The search is case-insensitive and matches whole words.

### Optimized SQL Query:

```sql
SELECT 
    "youtube_api_video"."id", 
    "youtube_api_video"."title", 
    "youtube_api_video"."description", 
    "youtube_api_video"."published_at", 
    "youtube_api_video"."thumbnail_default", 
    "youtube_api_video"."thumbnail_medium", 
    "youtube_api_video"."thumbnail_high" 
FROM 
    "youtube_api_video" 
WHERE 
    (
        ("youtube_api_video"."title" ~* '\ytea\y' AND "youtube_api_video"."title" ~* '\yhow\y') 
        OR 
        ("youtube_api_video"."description" ~* '\ytea\y' AND "youtube_api_video"."description" ~* '\yhow\y')
    ); 
```
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/33954485-993fd13b-22e9-4fbc-81b6-ada586664ff6?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D33954485-993fd13b-22e9-4fbc-81b6-ada586664ff6%26entityType%3Dcollection%26workspaceId%3Dc1c8b68e-8aee-468e-8057-9d09d5c20ca2)
# Database Optimization

* **Indexes:**
    - `youtube_api_video_pkey` (Primary Key)
    - `published_at_idx` (Index on `published_at` for sorting)
    - `title_desc_idx` (Index on title and description for search queries)

# References
* YouTube Data API v3: Search List: https://developers.google.com/youtube/v3/docs/search/list
* YouTube API Samples (Python - Search): https://github.com/topics/youtube-data-api-v3?l=python (This link points to a directory containing various samples. You might need to explore the search.py file within that directory)
* How to Set Up a Django Project with PostgreSQL on Docker (for potential database setup): https://medium.com/a-layman/learn-docker-from-scratch-containerizing-django-application-with-postgresql-in-docker-8c112bca6e4b


