# Campaign Finance Dashboard
This project was built at [CALmatters](https://calmatters.org/) to make California's public data about campaign finance easier to analyze and understand. The data was scraped from [Cal-Access](http://cal-access.sos.ca.gov/), the state's messy government database about lobbying activity and politics. 

## Getting Started

The scraper was built in Python 2.7 using the web crawling framework [Scrapy](https://scrapy.org/) and pip. The dashboard was built using Mongo, Express, React, and Node.

#### 0. Prerequisites

- [MongoDB 3.6+](https://docs.mongodb.com/manual/installation/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [npm](https://www.npmjs.com/get-npm)
- [yarn](https://yarnpkg.com/lang/en/docs/install/#mac-stable)

#### 1. The Scraper

To get started, `cd calaccess_scraper` and run `pip install -r requirements.txt` to install all dependencies. The scraper will require a MongoDB URI in a `secrets.txt` file, which is not included in the repository. Place your `secrets.txt` file in `/campaign_finance/calaccess_scraper`. In the same directory, run `scrapy crawl [spider name]`. The four spiders currently available are:

- ballot_measures
- funds
- committees
- candidates

#### 2. The Dashboard

Install all dependencies by running `yarn install` in the root directory of the project. Afterwards, run `cd backend && touch secrets.js`. Store your MongoDB URI in your `secrets.js` in the following format:

```
const secrets = {
  dbUri: "your-uri-here"
};

export const getSecret = key => secrets[key];
```
Run the full app locally with the command `yarn start:dev`. You can also run the client or the backend separately with the commands `yarn start:client` and `yarn start:server`.
