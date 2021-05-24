# google-text-to-speech-container

## How to use

1. Get a google cloud service account JSON credential for your text-to-speech API. This is a paid service that requires a credit card to be entered, but the first 1 million characters are free. (See https://www.youtube.com/watch?v=I5-P2o5yToI 0:40-4:00 on how to set up the text-to-speech API and get the service account credential)

2. Edit the example.yml file or create new `.yml` files in the input directory - the app will load all yaml files and process them. You can use Google Cloud's Text-to-speech demo (https://cloud.google.com/text-to-speech) to play around with voice settings and find something that you like. Use the `Show JSON` button to show the values that get sent to the API. The values should be copy-pasteable into the yaml files used by this app. The app supports reading in the text to be spoken via plain strings, which can be put in the texts array, or via ssml (see the text-to-speech API docs), by putting the ssml strings in the ssmls array.

3. Run the container (it is assumed that your current working directory is the root of this repo)

~~~
docker run \
    -v $(pwd)/input:/input \
    -v /path/to/key.json:/app/key.json \
    spiridonovpolytechnic/text-to-speech:latest
~~~

## Note

Not all configuration properties of the API are currently supported. Feel free to create an issue if you want support for something, or fork, implement, and do a pull request to get it into the image.