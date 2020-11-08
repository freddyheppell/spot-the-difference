<p align="center">
  <a href="https://www.youtube.com/watch?v=6hVnVGF87qA">
    <img src="/client/public/assets/banner.png" alt="Spot the Difference" width="750">
  </a>
</p>

Spot the Difference is an application that lets you and your friends compare music tastes. Just sign in with Spotify and share your three word code.

## Technologies
The client side is built with Vue.js and the server side is a Python-powered AWS Lambda.

### Running the client
From the client directory, `npm install` then `npm run serve` or `npm run build` for production.
There's an included `netlify.toml` file to deploy automatically to Netlify.

### Running the server
The backend is powered by a Lambda and DynamoDB table, orchestrated by [Serverless](https://www.serverless.com/).

* Use `serverless deploy --stage=dev` to deploy
* Use `sls wsgi serve --stage=dev` to run locally

To run locally you'll also need a DynamoDB mock, run `sls dynamodb install` followed by `sls dynamodb start` to run.

You'll need to copy the `env.example.json` file to `env.json` and put a set of spotify application credentials in there.