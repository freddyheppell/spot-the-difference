<p align="center">
  <a href="https://www.youtube.com/watch?v=6hVnVGF87qA">
    <img src="/assets/banner.png" alt="Spot the Difference" width="750">
  </a>
</p>
Spot the Difference is an application that lets you and your friends compare music tastes. Just sign in with Spotify and share your link!



## Technologies
The client side is built with Vue.js and the server side is a Python-powered AWS Lambda with a DynamoDB. We use the Spotify API to acquire users' top 50 tracks and top 50 artists over the long, medium and short term time periods Spotify provides. 



## Visualisations

Each visualisation is available within each of the three time periods provided by Spotify (long, medium and short term).



### Artists Network

The artists network builds a network graph out of the artists from each of the users, with artists as nodes and edges representing the presence of at least one mutual genre between two artists.

Each node is clickable to expand a dialogue that details the name of the artist represented by that node (which links to their spotify page), a list of the genres that artist has been labelled with by Spotify, and a list of the artists in the sample that have at least one genre in common with that artist.

This visualisation can provide interesting insights into "taste clusters" - some users may find all of their artists are highly connected, so have a strongly cohesive taste; while others may find they have two or more distinct clusters of artists; or more likely, there are distinct groups of artists whose union consists of one or two artists tying the groups together.

Bringing into question the comparison of two users, information about whether their individual taste clusters are distinct sets, are closely related in genres, or have mutual artists (coloured white as opposed to cyan/magenta) is also easily visible.

The visualisation is built using [emiliorizzo/vue-d3-network](https://github.com/emiliorizzo/vue-d3-network). Due to performance only up to the top 25 artists from each user are displayed, to keep the maximum total number of nodes displayed less than or equal to 50 as this behaved reasonably on the devices we had to hand at [HackSheffield](http://hacksheffield.com/) when this was built.



### Taste Trader

The Taste Trader constructs a query for each user from the genres and their frequencies over that user's artists. For example, if a user listened to three artists tagged "pop", and one artist tagged "electropop", their search query would contain the term "pop" repeated thrice, and "electropop" once - "pop pop pop electropop". This query is stored as a vector in which each word corresponds to a dimension with a length along that dimension - `{ pop: 3, electropop: 1 }`. 

Typically these query vectors feature a genre such as "pop" repeated orders of magnitude more than any of the other genre. To deal with this, the length of the vector along each axis is replaced by the logarithm of its sum with E - `new_length = natural_log(old_length + E)`.

All of the artists belonging to the other user are then treated as documents on which [TF.IDF ranking](https://en.wikipedia.org/wiki/Tf%E2%80%93idf#:~:text=In%20information%20retrieval%2C%20tf%E2%80%93idf,in%20a%20collection%20or%20corpus.) is performed. There is a simplification in the implementation owing to the fact that each artist only has a genre tagged on it once, or never.

Once the scores are computed for every artist, these scores are scaled by a function on the size of the union of the sets of genres in the search query and the artist (their "common genres"). This function (illustrated below) is a logarithmic curve such that an artist which shares one genre with the search query is scaled by a factor of 1 (so, is not scaled), while an artist with three common genres is scaled by a factor of two (so, doubled). The number of common genres required to double the artist's score was tuned to this value.


<p align="center">
  <img src="/assets/taste_trader_log.png" alt="A logarithmic curve used to scale arists' scores.">
</p>


Now we have scored all the artists it's simply a case of picking the artist with the highest score that does not appear in the user's own top artists. If no such artist exists, then simply the highest scoring artist is selected (and the text "[display_name] Likes" is displayed in lieu of the text "[display_name] Might Like". This can be shown in the obvious case of a user comparing themselves to themselves.


<p align="center">
  <img src="/assets/taste_trader_likes.png" alt="A screenshot of the Taste Trader">
</p>


The Taste Trader then also checks over the other user's top tracks to see if it contains a track from that artist, which it will then recommend to the user specifically instead of simply the best scoring artist.


<p align="center">
  <img src="/assets/taste_trader_track.png" alt="A screenshot of the Taste Trader">
</p>


### Mutual Genres

The mutual genres component is relatively simple. For each user, the frequency of genres over their top artists is counted to produce a vector in which each word is a dimension, and the frequency is the length of the vector along that dimension. (`{ art pop: 2, electropop: 5, metropopolis: 1, ... }`). The dot product of these two vectors is then computed (`{ art pop: 2, electropop: 4 } x { electropop: 4, indie: 10} = { art pop: 0, electropop: 16, indie: 0 }`), and up to the top 10 genres by the length of the vector along their dimension, given it is greater than zero, are selected to be displayed in a mirror bar chart.



## Local Setup

### Running the client

From the client directory, `npm install` then `npm run serve` or `npm run build` for production.
There's an included `netlify.toml` file to deploy automatically to Netlify.

### Running the server

The backend is powered by a Lambda and DynamoDB table, orchestrated by [Serverless](https://www.serverless.com/). You'll need to install the Serverless CLI globally.

Python dependencies are managed with [Pipenv](https://pipenv.pypa.io/en/latest/):

1. Make sure you've got an installation of Python 3.8 on your path and Pipenv
2. Run `pipenv install` to create a virtual environment and install pip dependencies
3. Run `npm install` to get Serverless packages
3. Copy `env.example.json` to `env.json` and put in spotify app credentials
4. Run `pipenv run sls dynamodb install --stage=dev` to install the DynamoDB mock
5. Either use the AWS CLI to setup your `~/.aws/credentials` file, or put [this dummy file](https://gist.github.com/freddyheppell/380e1ae436010a4697447606e33af410) there instead

To run the server locally:
1. Run `pipenv run dynamodb` to start the DynamoDB mock
2. Run `pipenv run server` to run the application server locally

To deploy to AWS:
* Run `pipenv run serverless deploy --stage=dev`

### Running the client

The client is just a normal vue project. You should be able to get it going by running `npm install` and then `npm run serve` from within `/client`. 

If you're wanting to run it in tandem with a backend running in a development environment, then you need to set an environment variable `VUE_APP_SPOT_DIFF_API_BASE_URI` to the base URI provided by serverless when you start the development server (e.g. `export VUE_APP_SPOT_DIFF_API_BASE_URI="http://localhost:5000"` - note the lack of a trailing slash).

## Acknowledgements

The artists graph uses [emiliorizzo/vue-d3-network](https://github.com/emiliorizzo/vue-d3-network), any icons are from [fontawesome](https://fontawesome.com/), and the background images are from [Unsplash](https://unsplash.com/), taken by [Sean Foley](https://unsplash.com/@_stfeyes).
